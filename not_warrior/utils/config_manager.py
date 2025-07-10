"""
Configuration management for loading, saving, and validating configuration.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Optional, Any
from not_warrior.models.config import AppConfig
from not_warrior.utils.logger import get_logger

logger = get_logger(__name__)


class ConfigManager:
    """Manager for application configuration."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path) if config_path else None
        self._config: Optional[AppConfig] = None
    
    def load_config(self) -> AppConfig:
        """Load configuration from file.
        
        Returns:
            Application configuration
        """
        if self._config is not None:
            return self._config
        
        config_path = self.config_path or self._get_default_config_path()
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config_data = yaml.safe_load(f)
                
                self._config = AppConfig(**config_data)
                self._config.config_file = str(config_path)
                
                logger.info(f"Configuration loaded from {config_path}")
                return self._config
                
            except Exception as e:
                logger.error(f"Failed to load configuration from {config_path}: {e}")
                logger.info("Using default configuration")
        
        # Create default configuration
        self._config = AppConfig()
        self._config.config_file = str(config_path)
        
        return self._config
    
    def save_config(self, config: Optional[AppConfig] = None) -> bool:
        """Save configuration to file.
        
        Args:
            config: Configuration to save (uses current if None)
            
        Returns:
            True if saved successfully
        """
        if config is None:
            config = self._config
        
        if config is None:
            logger.error("No configuration to save")
            return False
        
        config_path = self.config_path or self._get_default_config_path()
        
        try:
            # Create directory if it doesn't exist
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert to dictionary for YAML serialization
            config_dict = config.dict(exclude={'config_file'})
            
            with open(config_path, 'w') as f:
                yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False)
            
            logger.info(f"Configuration saved to {config_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save configuration to {config_path}: {e}")
            return False
    
    def _get_default_config_path(self) -> Path:
        """Get default configuration file path.
        
        Returns:
            Path to default config file
        """
        # Use AppConfig method to get default path
        default_config = AppConfig()
        return default_config.get_default_config_path()
    
    def create_default_config(self, force: bool = False) -> bool:
        """Create default configuration file.
        
        Args:
            force: Overwrite existing configuration
            
        Returns:
            True if created successfully
        """
        config_path = self.config_path or self._get_default_config_path()
        
        if config_path.exists() and not force:
            logger.info(f"Configuration already exists at {config_path}")
            return True
        
        try:
            # Create default configuration
            config = AppConfig()
            config.config_file = str(config_path)
            
            # Save to file
            return self.save_config(config)
            
        except Exception as e:
            logger.error(f"Failed to create default configuration: {e}")
            return False
    
    def validate_config(self) -> tuple[bool, list[str]]:
        """Validate current configuration.
        
        Returns:
            Tuple of (is_valid, errors)
        """
        try:
            config = self.load_config()
            errors = config.validate_config()
            return len(errors) == 0, errors
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return False, [str(e)]
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key.
        
        Args:
            key: Configuration key (dot-separated)
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        try:
            config = self.load_config()
            
            # Handle dot-separated keys
            keys = key.split('.')
            value = config
            
            for k in keys:
                if hasattr(value, k):
                    value = getattr(value, k)
                else:
                    return default
            
            return value
            
        except Exception as e:
            logger.error(f"Failed to get config value '{key}': {e}")
            return default
    
    def set_config_value(self, key: str, value: Any) -> bool:
        """Set configuration value by key.
        
        Args:
            key: Configuration key (dot-separated)
            value: Value to set
            
        Returns:
            True if set successfully
        """
        try:
            config = self.load_config()
            
            # Handle dot-separated keys
            keys = key.split('.')
            current = config
            
            # Navigate to parent object
            for k in keys[:-1]:
                if hasattr(current, k):
                    current = getattr(current, k)
                else:
                    logger.error(f"Invalid config key: {key}")
                    return False
            
            # Set the final value
            final_key = keys[-1]
            if hasattr(current, final_key):
                setattr(current, final_key, value)
                self._config = config
                return True
            else:
                logger.error(f"Invalid config key: {key}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to set config value '{key}': {e}")
            return False
    
    def get_notion_token(self) -> Optional[str]:
        """Get Notion API token from config or environment.
        
        Returns:
            Notion API token or None
        """
        # Check environment variable first
        env_token = os.getenv('NOTION_API_TOKEN')
        if env_token:
            return env_token
        
        # Check configuration file
        return self.get_config_value('notion.api_token')
    
    def set_notion_token(self, token: str) -> bool:
        """Set Notion API token in configuration.
        
        Args:
            token: Notion API token
            
        Returns:
            True if set successfully
        """
        return self.set_config_value('notion.api_token', token)
    
    def get_data_dir(self) -> Path:
        """Get data directory path.
        
        Returns:
            Path to data directory
        """
        config = self.load_config()
        if config.data_dir:
            return Path(config.data_dir)
        
        return config.get_default_data_dir()
    
    def backup_config(self) -> bool:
        """Create backup of current configuration.
        
        Returns:
            True if backup created successfully
        """
        try:
            config_path = self.config_path or self._get_default_config_path()
            
            if not config_path.exists():
                logger.info("No configuration file to backup")
                return True
            
            # Create backup filename with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = config_path.with_suffix(f".{timestamp}.bak")
            
            # Copy configuration file
            import shutil
            shutil.copy2(config_path, backup_path)
            
            logger.info(f"Configuration backed up to {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to backup configuration: {e}")
            return False
    
    def restore_config(self, backup_path: str) -> bool:
        """Restore configuration from backup.
        
        Args:
            backup_path: Path to backup file
            
        Returns:
            True if restored successfully
        """
        try:
            backup_file = Path(backup_path)
            config_path = self.config_path or self._get_default_config_path()
            
            if not backup_file.exists():
                logger.error(f"Backup file not found: {backup_path}")
                return False
            
            # Copy backup to config location
            import shutil
            shutil.copy2(backup_file, config_path)
            
            # Reload configuration
            self._config = None
            self.load_config()
            
            logger.info(f"Configuration restored from {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to restore configuration: {e}")
            return False
    
    def reset_config(self) -> bool:
        """Reset configuration to defaults.
        
        Returns:
            True if reset successfully
        """
        try:
            # Backup current config
            self.backup_config()
            
            # Create new default config
            self._config = AppConfig()
            
            # Save to file
            return self.save_config()
            
        except Exception as e:
            logger.error(f"Failed to reset configuration: {e}")
            return False
    
    @property
    def config(self) -> AppConfig:
        """Get current configuration.
        
        Returns:
            Current application configuration
        """
        return self.load_config()