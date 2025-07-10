"""
Default field mappings between Notion and Taskwarrior.
"""

from typing import Dict, List
from not_warrior.models.mapping import FieldMapping, FieldType, MappingConfiguration


# Default field mappings for a typical task database
DEFAULT_TASK_MAPPINGS = [
    FieldMapping(
        notion_field="Name",
        taskwarrior_field="description",
        field_type=FieldType.TITLE,
        required=True
    ),
    FieldMapping(
        notion_field="Status",
        taskwarrior_field="status",
        field_type=FieldType.SELECT,
        value_mappings={
            "Not started": "pending",
            "In progress": "pending",
            "Done": "completed",
            "Cancelled": "deleted"
        }
    ),
    FieldMapping(
        notion_field="Priority",
        taskwarrior_field="priority",
        field_type=FieldType.SELECT,
        value_mappings={
            "Low": "L",
            "Medium": "M",
            "High": "H",
            "Critical": "H"
        }
    ),
    FieldMapping(
        notion_field="Due Date",
        taskwarrior_field="due",
        field_type=FieldType.DATE
    ),
    FieldMapping(
        notion_field="Tags",
        taskwarrior_field="tags",
        field_type=FieldType.MULTI_SELECT
    ),
    FieldMapping(
        notion_field="Project",
        taskwarrior_field="project",
        field_type=FieldType.SELECT
    )
]


# Alternative mappings for different database schemas
ALTERNATIVE_MAPPINGS = {
    "simple": [
        FieldMapping(
            notion_field="Task",
            taskwarrior_field="description",
            field_type=FieldType.TITLE,
            required=True
        ),
        FieldMapping(
            notion_field="Done",
            taskwarrior_field="status",
            field_type=FieldType.CHECKBOX,
            value_mappings={
                "true": "completed",
                "false": "pending"
            }
        ),
        FieldMapping(
            notion_field="Due",
            taskwarrior_field="due",
            field_type=FieldType.DATE
        )
    ],
    "detailed": [
        FieldMapping(
            notion_field="Title",
            taskwarrior_field="description",
            field_type=FieldType.TITLE,
            required=True
        ),
        FieldMapping(
            notion_field="Status",
            taskwarrior_field="status",
            field_type=FieldType.SELECT,
            value_mappings={
                "Backlog": "pending",
                "Todo": "pending",
                "In Progress": "pending",
                "Review": "pending",
                "Done": "completed",
                "Cancelled": "deleted"
            }
        ),
        FieldMapping(
            notion_field="Priority",
            taskwarrior_field="priority",
            field_type=FieldType.SELECT,
            value_mappings={
                "P1": "H",
                "P2": "M",
                "P3": "L",
                "P4": "L"
            }
        ),
        FieldMapping(
            notion_field="Due Date",
            taskwarrior_field="due",
            field_type=FieldType.DATE
        ),
        FieldMapping(
            notion_field="Start Date",
            taskwarrior_field="scheduled",
            field_type=FieldType.DATE
        ),
        FieldMapping(
            notion_field="Labels",
            taskwarrior_field="tags",
            field_type=FieldType.MULTI_SELECT
        ),
        FieldMapping(
            notion_field="Project",
            taskwarrior_field="project",
            field_type=FieldType.SELECT
        ),
        FieldMapping(
            notion_field="Estimate",
            taskwarrior_field="estimate",
            field_type=FieldType.NUMBER
        )
    ],
    "gtd": [  # Getting Things Done style
        FieldMapping(
            notion_field="Task",
            taskwarrior_field="description",
            field_type=FieldType.TITLE,
            required=True
        ),
        FieldMapping(
            notion_field="Status",
            taskwarrior_field="status",
            field_type=FieldType.SELECT,
            value_mappings={
                "Inbox": "pending",
                "Next Action": "pending",
                "Waiting For": "waiting",
                "Someday/Maybe": "pending",
                "Done": "completed",
                "Cancelled": "deleted"
            }
        ),
        FieldMapping(
            notion_field="Context",
            taskwarrior_field="tags",
            field_type=FieldType.MULTI_SELECT
        ),
        FieldMapping(
            notion_field="Area",
            taskwarrior_field="project",
            field_type=FieldType.SELECT
        ),
        FieldMapping(
            notion_field="Due Date",
            taskwarrior_field="due",
            field_type=FieldType.DATE
        ),
        FieldMapping(
            notion_field="Waiting For",
            taskwarrior_field="wait",
            field_type=FieldType.DATE
        )
    ]
}


# Common Notion property names and their typical Taskwarrior equivalents
COMMON_FIELD_SUGGESTIONS = {
    # Title fields
    "Name": "description",
    "Title": "description",
    "Task": "description",
    "Description": "description",
    "Summary": "description",
    
    # Status fields
    "Status": "status",
    "State": "status",
    "Progress": "status",
    "Done": "status",
    "Complete": "status",
    "Completed": "status",
    
    # Priority fields
    "Priority": "priority",
    "Importance": "priority",
    "Urgency": "priority",
    
    # Date fields
    "Due": "due",
    "Due Date": "due",
    "Deadline": "due",
    "Start": "scheduled",
    "Start Date": "scheduled",
    "Scheduled": "scheduled",
    "Created": "entry",
    "Created Date": "entry",
    "Modified": "modified",
    "Updated": "modified",
    
    # Project/category fields
    "Project": "project",
    "Category": "project",
    "Area": "project",
    "Folder": "project",
    
    # Tags fields
    "Tags": "tags",
    "Labels": "tags",
    "Categories": "tags",
    "Context": "tags",
    
    # Other fields
    "Estimate": "estimate",
    "Time Estimate": "estimate",
    "Notes": "annotations",
    "Comments": "annotations",
    "Depends On": "depends"
}


# Taskwarrior field types and their recommended Notion equivalents
TASKWARRIOR_TO_NOTION_SUGGESTIONS = {
    "description": (FieldType.TITLE, "Title"),
    "status": (FieldType.SELECT, "Status"),
    "priority": (FieldType.SELECT, "Priority"),
    "project": (FieldType.SELECT, "Project"),
    "due": (FieldType.DATE, "Due Date"),
    "scheduled": (FieldType.DATE, "Start Date"),
    "start": (FieldType.DATETIME, "Started"),
    "end": (FieldType.DATETIME, "Completed"),
    "entry": (FieldType.DATETIME, "Created"),
    "modified": (FieldType.DATETIME, "Modified"),
    "tags": (FieldType.MULTI_SELECT, "Tags"),
    "annotations": (FieldType.RICH_TEXT, "Notes"),
    "depends": (FieldType.MULTI_SELECT, "Dependencies"),
    "estimate": (FieldType.NUMBER, "Estimate"),
    "urgency": (FieldType.NUMBER, "Urgency")
}


def create_default_mapping_config(database_id: str, mapping_type: str = "default") -> MappingConfiguration:
    """Create default mapping configuration.
    
    Args:
        database_id: Notion database ID
        mapping_type: Type of mapping (default, simple, detailed, gtd)
        
    Returns:
        Mapping configuration
    """
    if mapping_type == "default":
        mappings = DEFAULT_TASK_MAPPINGS
    elif mapping_type in ALTERNATIVE_MAPPINGS:
        mappings = ALTERNATIVE_MAPPINGS[mapping_type]
    else:
        mappings = DEFAULT_TASK_MAPPINGS
    
    return MappingConfiguration(
        notion_database_id=database_id,
        database_name=f"Tasks ({mapping_type})",
        mappings=mappings
    )


def suggest_mapping_for_notion_field(notion_field: str) -> tuple[str, FieldType]:
    """Suggest Taskwarrior field and type for Notion field.
    
    Args:
        notion_field: Notion field name
        
    Returns:
        Tuple of (taskwarrior_field, field_type)
    """
    # Check common suggestions
    if notion_field in COMMON_FIELD_SUGGESTIONS:
        tw_field = COMMON_FIELD_SUGGESTIONS[notion_field]
        
        # Determine field type based on Taskwarrior field
        if tw_field == "description":
            return tw_field, FieldType.TITLE
        elif tw_field in ["status", "priority", "project"]:
            return tw_field, FieldType.SELECT
        elif tw_field in ["due", "scheduled"]:
            return tw_field, FieldType.DATE
        elif tw_field == "tags":
            return tw_field, FieldType.MULTI_SELECT
        elif tw_field == "annotations":
            return tw_field, FieldType.RICH_TEXT
        elif tw_field == "estimate":
            return tw_field, FieldType.NUMBER
        else:
            return tw_field, FieldType.TEXT
    
    # Default suggestion based on common patterns
    notion_lower = notion_field.lower()
    
    if "date" in notion_lower or "due" in notion_lower or "deadline" in notion_lower:
        return "due", FieldType.DATE
    elif "status" in notion_lower or "state" in notion_lower:
        return "status", FieldType.SELECT
    elif "priority" in notion_lower or "importance" in notion_lower:
        return "priority", FieldType.SELECT
    elif "project" in notion_lower or "category" in notion_lower:
        return "project", FieldType.SELECT
    elif "tag" in notion_lower or "label" in notion_lower:
        return "tags", FieldType.MULTI_SELECT
    elif "note" in notion_lower or "comment" in notion_lower:
        return "annotations", FieldType.RICH_TEXT
    elif "estimate" in notion_lower or "time" in notion_lower:
        return "estimate", FieldType.NUMBER
    else:
        # Default to description field
        return "description", FieldType.TITLE


def suggest_notion_field_for_taskwarrior(tw_field: str) -> tuple[str, FieldType]:
    """Suggest Notion field name and type for Taskwarrior field.
    
    Args:
        tw_field: Taskwarrior field name
        
    Returns:
        Tuple of (notion_field, field_type)
    """
    if tw_field in TASKWARRIOR_TO_NOTION_SUGGESTIONS:
        field_type, notion_field = TASKWARRIOR_TO_NOTION_SUGGESTIONS[tw_field]
        return notion_field, field_type
    else:
        # Default suggestion
        return tw_field.title(), FieldType.TEXT


def get_common_status_values() -> List[str]:
    """Get common status values for Notion.
    
    Returns:
        List of common status values
    """
    return [
        "Not started",
        "In progress",
        "Done",
        "Cancelled",
        "Backlog",
        "Todo",
        "Review",
        "Blocked",
        "Waiting"
    ]


def get_common_priority_values() -> List[str]:
    """Get common priority values for Notion.
    
    Returns:
        List of common priority values
    """
    return [
        "Low",
        "Medium",
        "High",
        "Critical",
        "P1",
        "P2",
        "P3",
        "P4"
    ]


def validate_mapping_compatibility(mappings: List[FieldMapping]) -> List[str]:
    """Validate mapping compatibility.
    
    Args:
        mappings: List of field mappings
        
    Returns:
        List of validation errors
    """
    errors = []
    
    # Check for required fields
    has_description = any(m.taskwarrior_field == "description" for m in mappings)
    if not has_description:
        errors.append("Missing required mapping for 'description' field")
    
    # Check for duplicate Notion fields
    notion_fields = [m.notion_field for m in mappings]
    duplicates = set([f for f in notion_fields if notion_fields.count(f) > 1])
    if duplicates:
        errors.append(f"Duplicate Notion fields: {', '.join(duplicates)}")
    
    # Check for duplicate Taskwarrior fields
    tw_fields = [m.taskwarrior_field for m in mappings]
    duplicates = set([f for f in tw_fields if tw_fields.count(f) > 1])
    if duplicates:
        errors.append(f"Duplicate Taskwarrior fields: {', '.join(duplicates)}")
    
    # Check field type compatibility
    for mapping in mappings:
        if mapping.taskwarrior_field in ["due", "scheduled", "start", "end"]:
            if mapping.field_type not in [FieldType.DATE, FieldType.DATETIME]:
                errors.append(f"Field '{mapping.taskwarrior_field}' should use DATE or DATETIME type")
        
        elif mapping.taskwarrior_field == "tags":
            if mapping.field_type != FieldType.MULTI_SELECT:
                errors.append(f"Field '{mapping.taskwarrior_field}' should use MULTI_SELECT type")
        
        elif mapping.taskwarrior_field == "description":
            if mapping.field_type != FieldType.TITLE:
                errors.append(f"Field '{mapping.taskwarrior_field}' should use TITLE type")
    
    return errors


def get_mapping_templates() -> Dict[str, Dict]:
    """Get available mapping templates.
    
    Returns:
        Dictionary of mapping templates
    """
    return {
        "default": {
            "name": "Default Task Mapping",
            "description": "Standard task mapping with status, priority, due date, and tags",
            "mappings": DEFAULT_TASK_MAPPINGS
        },
        "simple": {
            "name": "Simple Task Mapping",
            "description": "Minimal mapping with just task name, completion status, and due date",
            "mappings": ALTERNATIVE_MAPPINGS["simple"]
        },
        "detailed": {
            "name": "Detailed Task Mapping",
            "description": "Comprehensive mapping with additional fields like estimates and start dates",
            "mappings": ALTERNATIVE_MAPPINGS["detailed"]
        },
        "gtd": {
            "name": "Getting Things Done (GTD)",
            "description": "GTD-style mapping with contexts, areas, and waiting states",
            "mappings": ALTERNATIVE_MAPPINGS["gtd"]
        }
    }