"""
Default settings, environment variables, and configuration constants.
"""

import os
from pathlib import Path
from typing import Dict, Any, List

# Application information
APP_NAME = "not-warrior"
APP_VERSION = "0.1.0"
APP_DESCRIPTION = "Notion-Taskwarrior Synchronization Service"

# Environment variables
ENV_NOTION_TOKEN = "NOTION_API_TOKEN"
ENV_CONFIG_FILE = "NOT_WARRIOR_CONFIG"
ENV_DATA_DIR = "NOT_WARRIOR_DATA_DIR"
ENV_LOG_LEVEL = "NOT_WARRIOR_LOG_LEVEL"
ENV_LOG_FILE = "NOT_WARRIOR_LOG_FILE"

# Default configuration values
DEFAULT_CONFIG = {
    "notion": {
        "api_version": "2022-06-28",
        "timeout": 30,
        "requests_per_second": 3
    },
    "taskwarrior": {
        "command_path": "task",
        "notion_tag": "notion",
        "hook_enabled": False,
        "hook_events": ["on-modify"]
    },
    "sync": {
        "direction": "both",
        "auto_sync": False,
        "conflict_resolution": "manual",
        "sync_interval_minutes": 15,
        "backup_before_sync": True,
        "backup_count": 5
    },
    "logging": {
        "level": "INFO",
        "max_file_size": 10 * 1024 * 1024,  # 10MB
        "backup_count": 5,
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    }
}

# Notion API settings
NOTION_API_BASE_URL = "https://api.notion.com/v1"
NOTION_API_VERSION = "2022-06-28"
NOTION_RATE_LIMIT = 3  # requests per second
NOTION_TIMEOUT = 30  # seconds

# Taskwarrior settings
TASKWARRIOR_DEFAULT_COMMAND = "task"
TASKWARRIOR_NOTION_TAG = "notion"
TASKWARRIOR_DATE_FORMAT = "%Y%m%dT%H%M%SZ"

# Sync settings
SYNC_DIRECTIONS = ["both", "to-notion", "to-taskwarrior"]
CONFLICT_RESOLUTIONS = ["manual", "notion", "taskwarrior"]
DEFAULT_SYNC_INTERVAL = 15  # minutes

# File and directory settings
CONFIG_FILE_NAME = "config.yml"
SAMPLE_CONFIG_FILE_NAME = "config.sample.yml"
LOG_FILE_NAME = "not-warrior.log"
BACKUP_DIR_NAME = "backups"

# Hook settings
HOOK_SCRIPT_NAME = "on-modify-notion-sync"
HOOK_EVENTS = ["on-add", "on-modify", "on-delete"]

# Logging settings
LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# File size limits
MAX_LOG_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_BACKUP_COUNT = 5
MAX_CONFIG_FILE_SIZE = 1024 * 1024  # 1MB

# Validation patterns
UUID_PATTERN = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
NOTION_TOKEN_PATTERN = r'^secret_[A-Za-z0-9]+$'
NOTION_DATABASE_ID_PATTERN = r'^[0-9a-f]{8}[0-9a-f]{4}[0-9a-f]{4}[0-9a-f]{4}[0-9a-f]{12}$'

# Default field mappings
DEFAULT_FIELD_MAPPINGS = {
    "title": "description",
    "status": "status",
    "priority": "priority",
    "due_date": "due",
    "tags": "tags",
    "project": "project"
}

# Notion field types
NOTION_FIELD_TYPES = {
    "title": "title",
    "rich_text": "rich_text",
    "number": "number",
    "select": "select",
    "multi_select": "multi_select",
    "date": "date",
    "checkbox": "checkbox",
    "url": "url",
    "email": "email",
    "phone_number": "phone_number",
    "relation": "relation",
    "rollup": "rollup",
    "created_time": "created_time",
    "created_by": "created_by",
    "last_edited_time": "last_edited_time",
    "last_edited_by": "last_edited_by"
}

# Taskwarrior field types
TASKWARRIOR_FIELD_TYPES = {
    "string": ["description", "project", "status"],
    "date": ["due", "scheduled", "start", "end", "entry", "modified"],
    "duration": ["estimate"],
    "numeric": ["priority", "urgency"],
    "list": ["tags", "depends"]
}

# Status mappings
STATUS_MAPPINGS = {
    "notion_to_taskwarrior": {
        "Not started": "pending",
        "In progress": "pending",
        "Done": "completed",
        "Cancelled": "deleted"
    },
    "taskwarrior_to_notion": {
        "pending": "Not started",
        "completed": "Done",
        "deleted": "Cancelled",
        "waiting": "In progress"
    }
}

# Priority mappings
PRIORITY_MAPPINGS = {
    "notion_to_taskwarrior": {
        "Low": "L",
        "Medium": "M",
        "High": "H",
        "Critical": "H"
    },
    "taskwarrior_to_notion": {
        "L": "Low",
        "M": "Medium",
        "H": "High",
        "": "Medium"  # Default for empty priority
    }
}


def get_config_dir() -> Path:
    """Get configuration directory path.
    
    Returns:
        Path to configuration directory
    """
    # Check environment variable first
    if ENV_CONFIG_FILE in os.environ:
        config_file = Path(os.environ[ENV_CONFIG_FILE])
        return config_file.parent
    
    # Try XDG config directory
    xdg_config_home = os.environ.get('XDG_CONFIG_HOME')
    if xdg_config_home:
        return Path(xdg_config_home) / APP_NAME
    
    # Default to ~/.config/not-warrior
    home = Path.home()
    config_dir = home / '.config' / APP_NAME
    
    # Fall back to ~/.not-warrior if .config doesn't exist
    if not config_dir.parent.exists() and (home / f'.{APP_NAME}').exists():
        return home / f'.{APP_NAME}'
    
    return config_dir


def get_data_dir() -> Path:
    """Get data directory path.
    
    Returns:
        Path to data directory
    """
    # Check environment variable first
    if ENV_DATA_DIR in os.environ:
        return Path(os.environ[ENV_DATA_DIR])
    
    # Try XDG data directory
    xdg_data_home = os.environ.get('XDG_DATA_HOME')
    if xdg_data_home:
        return Path(xdg_data_home) / APP_NAME
    
    # Default to ~/.local/share/not-warrior
    home = Path.home()
    data_dir = home / '.local' / 'share' / APP_NAME
    
    # Fall back to ~/.not-warrior/data if .local doesn't exist
    if not data_dir.parent.parent.exists() and (home / f'.{APP_NAME}').exists():
        return home / f'.{APP_NAME}' / 'data'
    
    return data_dir


def get_cache_dir() -> Path:
    """Get cache directory path.
    
    Returns:
        Path to cache directory
    """
    # Try XDG cache directory
    xdg_cache_home = os.environ.get('XDG_CACHE_HOME')
    if xdg_cache_home:
        return Path(xdg_cache_home) / APP_NAME
    
    # Default to ~/.cache/not-warrior
    home = Path.home()
    cache_dir = home / '.cache' / APP_NAME
    
    # Fall back to ~/.not-warrior/cache if .cache doesn't exist
    if not cache_dir.parent.exists() and (home / f'.{APP_NAME}').exists():
        return home / f'.{APP_NAME}' / 'cache'
    
    return cache_dir


def get_log_dir() -> Path:
    """Get log directory path.
    
    Returns:
        Path to log directory
    """
    # Use data directory for logs
    return get_data_dir() / 'logs'


def get_backup_dir() -> Path:
    """Get backup directory path.
    
    Returns:
        Path to backup directory
    """
    return get_data_dir() / BACKUP_DIR_NAME


def get_notion_token() -> str:
    """Get Notion API token from environment.
    
    Returns:
        Notion API token or empty string
    """
    return os.environ.get(ENV_NOTION_TOKEN, '')


def get_log_level() -> str:
    """Get log level from environment.
    
    Returns:
        Log level string
    """
    level = os.environ.get(ENV_LOG_LEVEL, DEFAULT_LOG_LEVEL)
    return level.upper() if level.upper() in LOG_LEVELS else DEFAULT_LOG_LEVEL


def get_log_file() -> str:
    """Get log file path from environment.
    
    Returns:
        Log file path or empty string
    """
    return os.environ.get(ENV_LOG_FILE, '')


def create_directories() -> None:
    """Create necessary directories."""
    directories = [
        get_config_dir(),
        get_data_dir(),
        get_cache_dir(),
        get_log_dir(),
        get_backup_dir()
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def get_taskwarrior_data_dir() -> Path:
    """Get Taskwarrior data directory.
    
    Returns:
        Path to Taskwarrior data directory
    """
    # Check TASKDATA environment variable
    taskdata = os.environ.get('TASKDATA')
    if taskdata:
        return Path(taskdata)
    
    # Default to ~/.task
    return Path.home() / '.task'


def get_taskwarrior_hooks_dir() -> Path:
    """Get Taskwarrior hooks directory.
    
    Returns:
        Path to Taskwarrior hooks directory
    """
    return get_taskwarrior_data_dir() / 'hooks'


def is_development_mode() -> bool:
    """Check if running in development mode.
    
    Returns:
        True if in development mode
    """
    return os.environ.get('NOT_WARRIOR_DEV', '').lower() in ('1', 'true', 'yes')


def get_user_agent() -> str:
    """Get user agent string for API requests.
    
    Returns:
        User agent string
    """
    return f"{APP_NAME}/{APP_VERSION}"


# Configuration validation rules
VALIDATION_RULES = {
    "notion.api_token": {
        "required": True,
        "pattern": NOTION_TOKEN_PATTERN,
        "error": "Notion API token must start with 'secret_'"
    },
    "notion.timeout": {
        "type": int,
        "min": 1,
        "max": 300,
        "error": "Timeout must be between 1 and 300 seconds"
    },
    "notion.requests_per_second": {
        "type": int,
        "min": 1,
        "max": 10,
        "error": "Requests per second must be between 1 and 10"
    },
    "sync.direction": {
        "choices": SYNC_DIRECTIONS,
        "error": f"Sync direction must be one of: {', '.join(SYNC_DIRECTIONS)}"
    },
    "sync.conflict_resolution": {
        "choices": CONFLICT_RESOLUTIONS,
        "error": f"Conflict resolution must be one of: {', '.join(CONFLICT_RESOLUTIONS)}"
    },
    "logging.level": {
        "choices": LOG_LEVELS,
        "error": f"Log level must be one of: {', '.join(LOG_LEVELS)}"
    }
}

# Help text for configuration options
CONFIG_HELP = {
    "notion.api_token": "Your Notion API integration token",
    "notion.api_version": "Notion API version to use",
    "notion.timeout": "Timeout for API requests in seconds",
    "notion.requests_per_second": "Rate limit for API requests",
    "taskwarrior.command_path": "Path to taskwarrior command",
    "taskwarrior.notion_tag": "Tag used to identify Notion-synced tasks",
    "sync.direction": "Default sync direction (both, to-notion, to-taskwarrior)",
    "sync.auto_sync": "Enable automatic synchronization",
    "sync.conflict_resolution": "How to handle sync conflicts",
    "logging.level": "Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    "logging.log_file": "Path to log file (empty for stdout only)"
}