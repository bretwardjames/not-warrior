"""
Unified task model for both Notion and Taskwarrior representations.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class TaskStatus(str, Enum):
    """Task status enumeration."""
    PENDING = "pending"
    COMPLETED = "completed"
    DELETED = "deleted"
    WAITING = "waiting"
    RECURRING = "recurring"


class TaskPriority(str, Enum):
    """Task priority enumeration."""
    LOW = "L"
    MEDIUM = "M"
    HIGH = "H"
    NONE = ""


class Task(BaseModel):
    """Unified task model for Notion and Taskwarrior."""
    
    # Core fields
    id: Optional[str] = None
    uuid: Optional[str] = None  # Taskwarrior UUID
    notion_id: Optional[str] = None  # Notion page ID
    
    # Basic task information
    description: str = Field(..., min_length=1, max_length=1000)
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.NONE
    
    # Timestamps
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
    due: Optional[datetime] = None
    scheduled: Optional[datetime] = None
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    
    # Tags and projects
    tags: List[str] = Field(default_factory=list)
    project: Optional[str] = None
    
    # Additional fields
    annotations: List[str] = Field(default_factory=list)
    depends: List[str] = Field(default_factory=list)  # Task dependencies
    
    # System fields
    urgency: Optional[float] = None
    
    # Sync metadata
    last_sync: Optional[datetime] = None
    sync_source: Optional[str] = None  # 'notion' or 'taskwarrior'
    
    # Raw data for debugging
    raw_notion_data: Optional[Dict[str, Any]] = None
    raw_taskwarrior_data: Optional[Dict[str, Any]] = None
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
    
    @validator('tags')
    def validate_tags(cls, v):
        """Validate tags list."""
        if v is None:
            return []
        return [tag.strip() for tag in v if tag.strip()]
    
    @validator('description')
    def validate_description(cls, v):
        """Validate description."""
        if not v or not v.strip():
            raise ValueError('Description cannot be empty')
        return v.strip()
    
    def to_notion_properties(self) -> Dict[str, Any]:
        """Convert task to Notion page properties.
        
        Returns:
            Notion page properties dictionary
        """
        # TODO: Implement conversion to Notion format
        # TODO: Handle field mappings
        # TODO: Convert datetime to Notion format
        
        properties = {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": self.description
                        }
                    }
                ]
            }
        }
        
        # Add status
        if self.status:
            properties["Status"] = {
                "select": {
                    "name": self.status.value
                }
            }
        
        # Add priority
        if self.priority != TaskPriority.NONE:
            properties["Priority"] = {
                "select": {
                    "name": self.priority.value
                }
            }
        
        # Add due date
        if self.due:
            properties["Due"] = {
                "date": {
                    "start": self.due.isoformat()
                }
            }
        
        # Add tags
        if self.tags:
            properties["Tags"] = {
                "multi_select": [
                    {"name": tag} for tag in self.tags
                ]
            }
        
        return properties
    
    def to_taskwarrior_data(self) -> Dict[str, Any]:
        """Convert task to Taskwarrior format.
        
        Returns:
            Taskwarrior task dictionary
        """
        # TODO: Implement conversion to Taskwarrior format
        # TODO: Handle field mappings
        # TODO: Convert datetime to Taskwarrior format
        
        data = {
            "description": self.description,
            "status": self.status.value,
        }
        
        if self.uuid:
            data["uuid"] = self.uuid
        
        if self.priority != TaskPriority.NONE:
            data["priority"] = self.priority.value
        
        if self.due:
            data["due"] = self.due.strftime("%Y%m%dT%H%M%SZ")
        
        if self.scheduled:
            data["scheduled"] = self.scheduled.strftime("%Y%m%dT%H%M%SZ")
        
        if self.project:
            data["project"] = self.project
        
        if self.tags:
            data["tags"] = self.tags
        
        if self.annotations:
            data["annotations"] = [
                {"description": ann, "entry": datetime.now().strftime("%Y%m%dT%H%M%SZ")}
                for ann in self.annotations
            ]
        
        return data
    
    @classmethod
    def from_notion_page(cls, notion_page: Dict[str, Any]) -> 'Task':
        """Create Task from Notion page data.
        
        Args:
            notion_page: Notion page data
            
        Returns:
            Task instance
        """
        # TODO: Implement conversion from Notion format
        # TODO: Handle field mappings
        # TODO: Parse Notion properties
        
        properties = notion_page.get("properties", {})
        
        # Extract basic fields
        description = ""
        if "Name" in properties:
            title = properties["Name"].get("title", [])
            if title:
                description = title[0].get("text", {}).get("content", "")
        
        # Extract status
        status = TaskStatus.PENDING
        if "Status" in properties:
            status_data = properties["Status"].get("select")
            if status_data:
                status = TaskStatus(status_data.get("name", "pending"))
        
        # Extract priority
        priority = TaskPriority.NONE
        if "Priority" in properties:
            priority_data = properties["Priority"].get("select")
            if priority_data:
                priority = TaskPriority(priority_data.get("name", ""))
        
        # Extract due date
        due = None
        if "Due" in properties:
            due_data = properties["Due"].get("date")
            if due_data and due_data.get("start"):
                due = datetime.fromisoformat(due_data["start"])
        
        # Extract tags
        tags = []
        if "Tags" in properties:
            tags_data = properties["Tags"].get("multi_select", [])
            tags = [tag["name"] for tag in tags_data]
        
        return cls(
            notion_id=notion_page.get("id"),
            description=description,
            status=status,
            priority=priority,
            due=due,
            tags=tags,
            created=datetime.fromisoformat(notion_page.get("created_time", "")) if notion_page.get("created_time") else None,
            modified=datetime.fromisoformat(notion_page.get("last_edited_time", "")) if notion_page.get("last_edited_time") else None,
            sync_source="notion",
            raw_notion_data=notion_page
        )
    
    @classmethod
    def from_taskwarrior_data(cls, tw_data: Dict[str, Any]) -> 'Task':
        """Create Task from Taskwarrior data.
        
        Args:
            tw_data: Taskwarrior task data
            
        Returns:
            Task instance
        """
        # TODO: Implement conversion from Taskwarrior format
        # TODO: Handle field mappings
        # TODO: Parse Taskwarrior timestamps
        
        # Parse timestamps
        created = None
        if "entry" in tw_data:
            created = datetime.strptime(tw_data["entry"], "%Y%m%dT%H%M%SZ")
        
        modified = None
        if "modified" in tw_data:
            modified = datetime.strptime(tw_data["modified"], "%Y%m%dT%H%M%SZ")
        
        due = None
        if "due" in tw_data:
            due = datetime.strptime(tw_data["due"], "%Y%m%dT%H%M%SZ")
        
        scheduled = None
        if "scheduled" in tw_data:
            scheduled = datetime.strptime(tw_data["scheduled"], "%Y%m%dT%H%M%SZ")
        
        # Parse status
        status = TaskStatus(tw_data.get("status", "pending"))
        
        # Parse priority
        priority = TaskPriority(tw_data.get("priority", ""))
        
        # Parse tags
        tags = tw_data.get("tags", [])
        if isinstance(tags, str):
            tags = [tags]
        
        # Parse annotations
        annotations = []
        if "annotations" in tw_data:
            annotations = [ann.get("description", "") for ann in tw_data["annotations"]]
        
        return cls(
            uuid=tw_data.get("uuid"),
            description=tw_data.get("description", ""),
            status=status,
            priority=priority,
            created=created,
            modified=modified,
            due=due,
            scheduled=scheduled,
            tags=tags,
            project=tw_data.get("project"),
            annotations=annotations,
            urgency=tw_data.get("urgency"),
            sync_source="taskwarrior",
            raw_taskwarrior_data=tw_data
        )
    
    def is_notion_synced(self) -> bool:
        """Check if task is synced with Notion.
        
        Returns:
            True if task has Notion ID
        """
        return self.notion_id is not None
    
    def is_taskwarrior_synced(self) -> bool:
        """Check if task is synced with Taskwarrior.
        
        Returns:
            True if task has Taskwarrior UUID
        """
        return self.uuid is not None
    
    def needs_sync(self, other: 'Task') -> bool:
        """Check if task needs synchronization with another task.
        
        Args:
            other: Other task to compare with
            
        Returns:
            True if synchronization is needed
        """
        # TODO: Implement sync comparison logic
        # TODO: Compare modification times
        # TODO: Compare field values
        
        if not self.modified or not other.modified:
            return True
        
        return self.modified != other.modified