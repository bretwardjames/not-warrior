"""
Helper functions for date/time utilities, string formatting, and common operations.
"""

import re
import uuid
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Union
from pathlib import Path


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime to string.
    
    Args:
        dt: Datetime object
        format_str: Format string
        
    Returns:
        Formatted datetime string
    """
    if dt is None:
        return ""
    return dt.strftime(format_str)


def parse_datetime(date_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
    """Parse datetime from string.
    
    Args:
        date_str: Date string
        format_str: Format string
        
    Returns:
        Parsed datetime or None
    """
    if not date_str:
        return None
    
    try:
        return datetime.strptime(date_str, format_str)
    except ValueError:
        return None


def parse_taskwarrior_datetime(tw_date: str) -> Optional[datetime]:
    """Parse Taskwarrior datetime format.
    
    Args:
        tw_date: Taskwarrior date string (YYYYMMDDTHHMMSSZ)
        
    Returns:
        Parsed datetime or None
    """
    if not tw_date:
        return None
    
    try:
        # Taskwarrior format: 20230101T120000Z
        return datetime.strptime(tw_date, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def format_taskwarrior_datetime(dt: datetime) -> str:
    """Format datetime for Taskwarrior.
    
    Args:
        dt: Datetime object
        
    Returns:
        Taskwarrior formatted date string
    """
    if dt is None:
        return ""
    
    # Convert to UTC if timezone aware
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc)
    
    return dt.strftime("%Y%m%dT%H%M%SZ")


def parse_notion_datetime(notion_date: str) -> Optional[datetime]:
    """Parse Notion datetime format.
    
    Args:
        notion_date: Notion date string (ISO 8601)
        
    Returns:
        Parsed datetime or None
    """
    if not notion_date:
        return None
    
    try:
        # Notion uses ISO 8601 format
        return datetime.fromisoformat(notion_date.replace('Z', '+00:00'))
    except ValueError:
        return None


def format_notion_datetime(dt: datetime) -> str:
    """Format datetime for Notion.
    
    Args:
        dt: Datetime object
        
    Returns:
        Notion formatted date string
    """
    if dt is None:
        return ""
    
    # Notion expects ISO 8601 format
    return dt.isoformat()


def get_current_utc_datetime() -> datetime:
    """Get current UTC datetime.
    
    Returns:
        Current UTC datetime
    """
    return datetime.now(timezone.utc)


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for filesystem safety.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove or replace problematic characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = re.sub(r'\s+', '_', filename)
    filename = filename.strip('.')
    
    # Ensure filename is not empty
    if not filename:
        filename = "unnamed"
    
    return filename


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate string to maximum length.
    
    Args:
        text: Original text
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def clean_whitespace(text: str) -> str:
    """Clean excessive whitespace from text.
    
    Args:
        text: Original text
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Replace multiple whitespace with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    return text.strip()


def generate_uuid() -> str:
    """Generate a UUID string.
    
    Returns:
        UUID string
    """
    return str(uuid.uuid4())


def is_valid_uuid(uuid_str: str) -> bool:
    """Check if string is a valid UUID.
    
    Args:
        uuid_str: UUID string to validate
        
    Returns:
        True if valid UUID
    """
    try:
        uuid.UUID(uuid_str)
        return True
    except ValueError:
        return False


def safe_get(data: Dict, key: str, default: Any = None) -> Any:
    """Safely get value from dictionary.
    
    Args:
        data: Dictionary
        key: Key to get (supports dot notation)
        default: Default value if key not found
        
    Returns:
        Value or default
    """
    if not isinstance(data, dict):
        return default
    
    keys = key.split('.')
    current = data
    
    for k in keys:
        if isinstance(current, dict) and k in current:
            current = current[k]
        else:
            return default
    
    return current


def safe_set(data: Dict, key: str, value: Any) -> None:
    """Safely set value in dictionary.
    
    Args:
        data: Dictionary
        key: Key to set (supports dot notation)
        value: Value to set
    """
    keys = key.split('.')
    current = data
    
    # Navigate to parent
    for k in keys[:-1]:
        if k not in current:
            current[k] = {}
        current = current[k]
    
    # Set final value
    current[keys[-1]] = value


def flatten_dict(data: Dict, separator: str = '.') -> Dict[str, Any]:
    """Flatten nested dictionary.
    
    Args:
        data: Dictionary to flatten
        separator: Separator for nested keys
        
    Returns:
        Flattened dictionary
    """
    def _flatten(obj, parent_key=''):
        items = []
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_key = f"{parent_key}{separator}{key}" if parent_key else key
                items.extend(_flatten(value, new_key).items())
        else:
            return {parent_key: obj}
        
        return dict(items)
    
    return _flatten(data)


def unflatten_dict(data: Dict[str, Any], separator: str = '.') -> Dict:
    """Unflatten dictionary with separator-based keys.
    
    Args:
        data: Flattened dictionary
        separator: Separator used in keys
        
    Returns:
        Nested dictionary
    """
    result = {}
    
    for key, value in data.items():
        safe_set(result, key, value)
    
    return result


def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """Merge two dictionaries recursively.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary
        
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result


def filter_dict(data: Dict, keys: List[str]) -> Dict:
    """Filter dictionary to only include specified keys.
    
    Args:
        data: Dictionary to filter
        keys: Keys to include
        
    Returns:
        Filtered dictionary
    """
    return {k: v for k, v in data.items() if k in keys}


def remove_none_values(data: Dict) -> Dict:
    """Remove None values from dictionary.
    
    Args:
        data: Dictionary to clean
        
    Returns:
        Dictionary without None values
    """
    return {k: v for k, v in data.items() if v is not None}


def ensure_list(value: Any) -> List:
    """Ensure value is a list.
    
    Args:
        value: Value to convert
        
    Returns:
        List containing value(s)
    """
    if value is None:
        return []
    elif isinstance(value, list):
        return value
    else:
        return [value]


def deduplicate_list(items: List) -> List:
    """Remove duplicates from list while preserving order.
    
    Args:
        items: List with potential duplicates
        
    Returns:
        List without duplicates
    """
    seen = set()
    result = []
    
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    
    return result


def chunk_list(items: List, chunk_size: int) -> List[List]:
    """Split list into chunks of specified size.
    
    Args:
        items: List to chunk
        chunk_size: Size of each chunk
        
    Returns:
        List of chunks
    """
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]


def human_readable_size(size_bytes: int) -> str:
    """Convert bytes to human readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Human readable size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def create_backup_filename(original_path: Union[str, Path], suffix: str = None) -> Path:
    """Create backup filename for a file.
    
    Args:
        original_path: Original file path
        suffix: Optional suffix (defaults to timestamp)
        
    Returns:
        Backup file path
    """
    path = Path(original_path)
    
    if suffix is None:
        suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    return path.with_suffix(f".{suffix}{path.suffix}")


def ensure_directory(path: Union[str, Path]) -> Path:
    """Ensure directory exists.
    
    Args:
        path: Directory path
        
    Returns:
        Directory path
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def get_file_age(path: Union[str, Path]) -> Optional[timedelta]:
    """Get age of file.
    
    Args:
        path: File path
        
    Returns:
        File age as timedelta or None if file doesn't exist
    """
    file_path = Path(path)
    
    if not file_path.exists():
        return None
    
    modified_time = datetime.fromtimestamp(file_path.stat().st_mtime)
    return datetime.now() - modified_time


def validate_email(email: str) -> bool:
    """Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid email format
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_url(url: str) -> bool:
    """Validate URL format.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid URL format
    """
    pattern = r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$'
    return bool(re.match(pattern, url))


def retry_with_backoff(max_retries: int = 3, backoff_factor: float = 1.0):
    """Decorator for retrying functions with exponential backoff.
    
    Args:
        max_retries: Maximum number of retries
        backoff_factor: Backoff multiplication factor
        
    Returns:
        Decorated function
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries:
                        raise
                    
                    wait_time = backoff_factor * (2 ** attempt)
                    time.sleep(wait_time)
            
        return wrapper
    return decorator