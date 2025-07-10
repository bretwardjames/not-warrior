"""
Field mapping model for mapping between Notion properties and Taskwarrior attributes.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class FieldType(str, Enum):
    """Field type enumeration."""
    TEXT = "text"
    NUMBER = "number"
    DATE = "date"
    DATETIME = "datetime"
    SELECT = "select"
    MULTI_SELECT = "multi_select"
    CHECKBOX = "checkbox"
    RICH_TEXT = "rich_text"
    TITLE = "title"
    TAGS = "tags"
    STATUS = "status"
    PRIORITY = "priority"


class FieldMapping(BaseModel):
    """Single field mapping between Notion and Taskwarrior."""
    
    notion_field: str = Field(..., min_length=1)
    taskwarrior_field: str = Field(..., min_length=1)
    field_type: FieldType
    
    # Transformation options
    required: bool = False
    default_value: Optional[Any] = None
    
    # Type conversion options
    date_format: Optional[str] = None
    
    # Select/multi-select mappings
    value_mappings: Dict[str, str] = Field(default_factory=dict)
    
    class Config:
        use_enum_values = True
    
    @validator('notion_field')
    def validate_notion_field(cls, v):
        """Validate Notion field name."""
        if not v or not v.strip():
            raise ValueError('Notion field name cannot be empty')
        return v.strip()
    
    @validator('taskwarrior_field')
    def validate_taskwarrior_field(cls, v):
        """Validate Taskwarrior field name."""
        if not v or not v.strip():
            raise ValueError('Taskwarrior field name cannot be empty')
        return v.strip()
    
    def convert_notion_to_taskwarrior(self, notion_value: Any) -> Any:
        """Convert Notion value to Taskwarrior format.
        
        Args:
            notion_value: Value from Notion
            
        Returns:
            Converted value for Taskwarrior
        """
        if notion_value is None:
            return self.default_value
        
        # Handle different field types
        if self.field_type == FieldType.TEXT:
            return str(notion_value) if notion_value else self.default_value
        
        elif self.field_type == FieldType.TITLE:
            # Extract text from Notion title object
            if isinstance(notion_value, list) and notion_value:
                return notion_value[0].get("text", {}).get("content", "")
            return str(notion_value) if notion_value else self.default_value
        
        elif self.field_type == FieldType.RICH_TEXT:
            # Extract text from Notion rich text object
            if isinstance(notion_value, list) and notion_value:
                return notion_value[0].get("text", {}).get("content", "")
            return str(notion_value) if notion_value else self.default_value
        
        elif self.field_type == FieldType.SELECT:
            # Handle Notion select field
            if isinstance(notion_value, dict):
                select_value = notion_value.get("name", "")
                return self.value_mappings.get(select_value, select_value)
            return str(notion_value) if notion_value else self.default_value
        
        elif self.field_type == FieldType.MULTI_SELECT:
            # Handle Notion multi-select field
            if isinstance(notion_value, list):
                values = [item.get("name", "") for item in notion_value]
                return [self.value_mappings.get(v, v) for v in values]
            return self.default_value or []
        
        elif self.field_type == FieldType.CHECKBOX:
            return bool(notion_value)
        
        elif self.field_type == FieldType.DATE:
            # Handle Notion date field
            if isinstance(notion_value, dict):
                date_str = notion_value.get("start")
                if date_str:
                    # TODO: Parse date and convert to Taskwarrior format
                    return date_str
            return self.default_value
        
        elif self.field_type == FieldType.DATETIME:
            # Handle Notion datetime field
            if isinstance(notion_value, dict):
                datetime_str = notion_value.get("start")
                if datetime_str:
                    # TODO: Parse datetime and convert to Taskwarrior format
                    return datetime_str
            return self.default_value
        
        elif self.field_type == FieldType.NUMBER:
            try:
                return float(notion_value) if notion_value is not None else self.default_value
            except (ValueError, TypeError):
                return self.default_value
        
        return notion_value
    
    def convert_taskwarrior_to_notion(self, tw_value: Any) -> Any:
        """Convert Taskwarrior value to Notion format.
        
        Args:
            tw_value: Value from Taskwarrior
            
        Returns:
            Converted value for Notion
        """
        if tw_value is None:
            return None
        
        # Handle different field types
        if self.field_type == FieldType.TEXT:
            return {
                "rich_text": [
                    {
                        "text": {
                            "content": str(tw_value)
                        }
                    }
                ]
            }
        
        elif self.field_type == FieldType.TITLE:
            return {
                "title": [
                    {
                        "text": {
                            "content": str(tw_value)
                        }
                    }
                ]
            }
        
        elif self.field_type == FieldType.SELECT:
            # Reverse mapping for select fields
            reverse_mapping = {v: k for k, v in self.value_mappings.items()}
            mapped_value = reverse_mapping.get(str(tw_value), str(tw_value))
            return {
                "select": {
                    "name": mapped_value
                }
            }
        
        elif self.field_type == FieldType.MULTI_SELECT:
            # Handle tags/multi-select
            if isinstance(tw_value, list):
                reverse_mapping = {v: k for k, v in self.value_mappings.items()}
                mapped_values = [reverse_mapping.get(str(v), str(v)) for v in tw_value]
                return {
                    "multi_select": [
                        {"name": value} for value in mapped_values
                    ]
                }
            return {"multi_select": []}
        
        elif self.field_type == FieldType.CHECKBOX:
            return {"checkbox": bool(tw_value)}
        
        elif self.field_type == FieldType.DATE:
            # TODO: Convert Taskwarrior date to Notion format
            return {
                "date": {
                    "start": str(tw_value)
                }
            }
        
        elif self.field_type == FieldType.DATETIME:
            # TODO: Convert Taskwarrior datetime to Notion format
            return {
                "date": {
                    "start": str(tw_value)
                }
            }
        
        elif self.field_type == FieldType.NUMBER:
            try:
                return {"number": float(tw_value)}
            except (ValueError, TypeError):
                return {"number": None}
        
        return tw_value


class MappingConfiguration(BaseModel):
    """Complete mapping configuration between Notion and Taskwarrior."""
    
    # Database configuration
    notion_database_id: str = Field(..., min_length=1)
    database_name: Optional[str] = None
    
    # Field mappings
    mappings: List[FieldMapping] = Field(default_factory=list)
    
    # Sync configuration
    sync_direction: str = Field(default="both", regex="^(both|to-notion|to-taskwarrior)$")
    auto_sync: bool = False
    
    # Filter configuration
    notion_filter: Optional[Dict[str, Any]] = None
    taskwarrior_filter: Optional[str] = None
    
    class Config:
        use_enum_values = True
    
    @validator('notion_database_id')
    def validate_database_id(cls, v):
        """Validate Notion database ID."""
        if not v or not v.strip():
            raise ValueError('Notion database ID cannot be empty')
        return v.strip()
    
    def get_mapping_by_notion_field(self, notion_field: str) -> Optional[FieldMapping]:
        """Get mapping by Notion field name.
        
        Args:
            notion_field: Notion field name
            
        Returns:
            Field mapping or None
        """
        for mapping in self.mappings:
            if mapping.notion_field == notion_field:
                return mapping
        return None
    
    def get_mapping_by_taskwarrior_field(self, tw_field: str) -> Optional[FieldMapping]:
        """Get mapping by Taskwarrior field name.
        
        Args:
            tw_field: Taskwarrior field name
            
        Returns:
            Field mapping or None
        """
        for mapping in self.mappings:
            if mapping.taskwarrior_field == tw_field:
                return mapping
        return None
    
    def add_mapping(self, mapping: FieldMapping) -> None:
        """Add field mapping.
        
        Args:
            mapping: Field mapping to add
        """
        # Remove existing mapping for the same fields
        self.mappings = [
            m for m in self.mappings 
            if m.notion_field != mapping.notion_field and m.taskwarrior_field != mapping.taskwarrior_field
        ]
        self.mappings.append(mapping)
    
    def remove_mapping(self, notion_field: str) -> bool:
        """Remove mapping by Notion field name.
        
        Args:
            notion_field: Notion field name
            
        Returns:
            True if mapping was removed
        """
        original_length = len(self.mappings)
        self.mappings = [m for m in self.mappings if m.notion_field != notion_field]
        return len(self.mappings) < original_length
    
    def convert_notion_to_taskwarrior(self, notion_properties: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Notion properties to Taskwarrior format using mappings.
        
        Args:
            notion_properties: Notion page properties
            
        Returns:
            Taskwarrior task data
        """
        tw_data = {}
        
        for mapping in self.mappings:
            if mapping.notion_field in notion_properties:
                notion_value = notion_properties[mapping.notion_field]
                tw_value = mapping.convert_notion_to_taskwarrior(notion_value)
                if tw_value is not None:
                    tw_data[mapping.taskwarrior_field] = tw_value
        
        return tw_data
    
    def convert_taskwarrior_to_notion(self, tw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Taskwarrior data to Notion properties using mappings.
        
        Args:
            tw_data: Taskwarrior task data
            
        Returns:
            Notion page properties
        """
        notion_properties = {}
        
        for mapping in self.mappings:
            if mapping.taskwarrior_field in tw_data:
                tw_value = tw_data[mapping.taskwarrior_field]
                notion_value = mapping.convert_taskwarrior_to_notion(tw_value)
                if notion_value is not None:
                    notion_properties[mapping.notion_field] = notion_value
        
        return notion_properties
    
    def validate_mappings(self) -> List[str]:
        """Validate all field mappings.
        
        Returns:
            List of validation errors
        """
        errors = []
        
        # Check for duplicate mappings
        notion_fields = [m.notion_field for m in self.mappings]
        tw_fields = [m.taskwarrior_field for m in self.mappings]
        
        if len(notion_fields) != len(set(notion_fields)):
            errors.append("Duplicate Notion field mappings found")
        
        if len(tw_fields) != len(set(tw_fields)):
            errors.append("Duplicate Taskwarrior field mappings found")
        
        # TODO: Add more validation rules
        # TODO: Validate field types
        # TODO: Validate required fields
        
        return errors