"""
Configuration model for sync settings, authentication, and user preferences.
"""

from typing import Dict, List, Optional, Any
from pathlib import Path
from pydantic import BaseModel, Field, validator
from not_warrior.models.mapping import MappingConfiguration


class NotionConfig(BaseModel):
    """Notion-specific configuration."""
    
    # Authentication
    api_token: Optional[str] = None
    
    # API settings
    api_version: str = "2022-06-28"
    timeout: int = 30
    
    # Rate limiting
    requests_per_second: int = 3
    
    class Config:
        extra = "forbid"
    
    @validator('api_token')
    def validate_api_token(cls, v):
        """Validate API token format."""
        if v and not v.startswith('secret_'):
            raise ValueError('Notion API token must start with "secret_"')
        return v


class TaskwarriorConfig(BaseModel):
    """Taskwarrior-specific configuration."""
    
    # Command configuration
    command_path: str = "task"
    data_location: Optional[str] = None
    
    # Sync settings
    notion_tag: str = "notion"
    
    # Hook settings
    hook_enabled: bool = False
    hook_events: List[str] = Field(default_factory=lambda: ["on-modify"])
    
    class Config:
        extra = "forbid"
    
    @validator('notion_tag')
    def validate_notion_tag(cls, v):
        """Validate notion tag."""
        if not v or not v.strip():
            raise ValueError('Notion tag cannot be empty')
        return v.strip()


class SyncConfig(BaseModel):
    """Synchronization configuration."""
    
    # Sync behavior
    direction: str = Field(default="both", regex="^(both|to-notion|to-taskwarrior)$")
    auto_sync: bool = False
    
    # Conflict resolution
    conflict_resolution: str = Field(default="manual", regex="^(manual|notion|taskwarrior)$")
    
    # Sync intervals
    sync_interval_minutes: int = 15
    
    # Backup settings
    backup_before_sync: bool = True
    backup_count: int = 5
    
    class Config:
        extra = "forbid"


class LoggingConfig(BaseModel):
    """Logging configuration."""
    
    # Log level
    level: str = Field(default="INFO", regex="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    
    # Log file settings
    log_file: Optional[str] = None
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    
    # Output format
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        extra = "forbid"


class AppConfig(BaseModel):
    """Main application configuration."""
    
    # Version
    version: str = "0.1.0"
    
    # Component configurations
    notion: NotionConfig = Field(default_factory=NotionConfig)
    taskwarrior: TaskwarriorConfig = Field(default_factory=TaskwarriorConfig)
    sync: SyncConfig = Field(default_factory=SyncConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    
    # Field mappings
    mappings: List[MappingConfiguration] = Field(default_factory=list)
    
    # File paths
    config_file: Optional[str] = None
    data_dir: Optional[str] = None
    
    class Config:
        extra = "forbid"
    
    @validator('data_dir')
    def validate_data_dir(cls, v):
        """Validate data directory."""
        if v:
            path = Path(v)
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
            return str(path.absolute())
        return v
    
    def get_default_config_path(self) -> Path:
        """Get default configuration file path.
        
        Returns:
            Path to default config file
        """
        # TODO: Handle different OS configurations
        home = Path.home()
        
        # Try XDG config directory first
        xdg_config = home / ".config" / "not-warrior"
        if xdg_config.exists() or not (home / ".not-warrior").exists():
            xdg_config.mkdir(parents=True, exist_ok=True)
            return xdg_config / "config.yml"
        
        # Fall back to home directory
        return home / ".not-warrior" / "config.yml"
    
    def get_default_data_dir(self) -> Path:
        """Get default data directory.
        
        Returns:
            Path to default data directory
        """
        # TODO: Handle different OS configurations
        home = Path.home()
        
        # Try XDG data directory first
        xdg_data = home / ".local" / "share" / "not-warrior"
        if xdg_data.exists() or not (home / ".not-warrior").exists():
            xdg_data.mkdir(parents=True, exist_ok=True)
            return xdg_data
        
        # Fall back to home directory
        data_dir = home / ".not-warrior" / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir
    
    def get_mapping_by_database_id(self, database_id: str) -> Optional[MappingConfiguration]:
        """Get mapping configuration by database ID.
        
        Args:
            database_id: Notion database ID
            
        Returns:
            Mapping configuration or None
        """
        for mapping in self.mappings:
            if mapping.notion_database_id == database_id:
                return mapping
        return None
    
    def add_mapping(self, mapping: MappingConfiguration) -> None:
        """Add mapping configuration.
        
        Args:
            mapping: Mapping configuration to add
        """
        # Remove existing mapping for the same database
        self.mappings = [
            m for m in self.mappings 
            if m.notion_database_id != mapping.notion_database_id
        ]
        self.mappings.append(mapping)
    
    def remove_mapping(self, database_id: str) -> bool:
        """Remove mapping by database ID.
        
        Args:
            database_id: Notion database ID
            
        Returns:
            True if mapping was removed
        """
        original_length = len(self.mappings)
        self.mappings = [m for m in self.mappings if m.notion_database_id != database_id]
        return len(self.mappings) < original_length
    
    def validate_config(self) -> List[str]:
        """Validate entire configuration.
        
        Returns:
            List of validation errors
        """
        errors = []
        
        # Check authentication
        if not self.notion.api_token:
            errors.append("Notion API token is required")
        
        # Check mappings
        if not self.mappings:
            errors.append("At least one database mapping is required")
        
        # Validate each mapping
        for i, mapping in enumerate(self.mappings):
            mapping_errors = mapping.validate_mappings()
            for error in mapping_errors:
                errors.append(f"Mapping {i+1}: {error}")
        
        # Check for duplicate database IDs
        database_ids = [m.notion_database_id for m in self.mappings]
        if len(database_ids) != len(set(database_ids)):
            errors.append("Duplicate database ID mappings found")
        
        # TODO: Add more validation rules
        # TODO: Validate file paths
        # TODO: Test connections
        
        return errors
    
    def is_configured(self) -> bool:
        """Check if application is properly configured.
        
        Returns:
            True if configuration is valid
        """
        errors = self.validate_config()
        return len(errors) == 0
    
    def get_log_file_path(self) -> Optional[Path]:
        """Get log file path.
        
        Returns:
            Path to log file or None
        """
        if self.logging.log_file:
            return Path(self.logging.log_file)
        
        # Default log file location
        data_dir = Path(self.data_dir) if self.data_dir else self.get_default_data_dir()
        return data_dir / "not-warrior.log"
    
    def get_backup_dir(self) -> Path:
        """Get backup directory path.
        
        Returns:
            Path to backup directory
        """
        data_dir = Path(self.data_dir) if self.data_dir else self.get_default_data_dir()
        backup_dir = data_dir / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        return backup_dir