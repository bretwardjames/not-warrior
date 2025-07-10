"""
Logging utilities for structured logging and output formatting.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional

# Global logger instance
_logger_configured = False


def setup_logger(verbose: bool = False, log_file: Optional[str] = None) -> None:
    """Setup application logging.
    
    Args:
        verbose: Enable verbose (DEBUG) logging
        log_file: Path to log file
    """
    global _logger_configured
    
    if _logger_configured:
        return
    
    # Determine log level
    log_level = logging.DEBUG if verbose else logging.INFO
    
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        try:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.handlers.RotatingFileHandler(
                log_path,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(logging.DEBUG)  # File gets all messages
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
            
        except Exception as e:
            root_logger.error(f"Failed to setup file logging: {e}")
    
    # Set up third-party logger levels
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    _logger_configured = True
    
    # Log initial message
    logger = get_logger(__name__)
    logger.info(f"Logging configured (level: {logging.getLevelName(log_level)})")


def get_logger(name: str) -> logging.Logger:
    """Get logger instance for module.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def set_log_level(level: str) -> None:
    """Set logging level.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    try:
        numeric_level = getattr(logging, level.upper())
        logging.getLogger().setLevel(numeric_level)
        
        # Update console handler level
        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stdout:
                handler.setLevel(numeric_level)
                break
                
    except AttributeError:
        logger = get_logger(__name__)
        logger.error(f"Invalid log level: {level}")


def configure_file_logging(log_file: str, max_size: int = 10 * 1024 * 1024, backup_count: int = 5) -> bool:
    """Configure file logging.
    
    Args:
        log_file: Path to log file
        max_size: Maximum file size in bytes
        backup_count: Number of backup files to keep
        
    Returns:
        True if configured successfully
    """
    try:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Remove existing file handlers
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            if isinstance(handler, logging.FileHandler):
                root_logger.removeHandler(handler)
        
        # Create new file handler
        file_handler = logging.handlers.RotatingFileHandler(
            log_path,
            maxBytes=max_size,
            backupCount=backup_count
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Set formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        # Add to root logger
        root_logger.addHandler(file_handler)
        
        logger = get_logger(__name__)
        logger.info(f"File logging configured: {log_file}")
        
        return True
        
    except Exception as e:
        logger = get_logger(__name__)
        logger.error(f"Failed to configure file logging: {e}")
        return False


def get_log_file_path() -> Optional[Path]:
    """Get current log file path.
    
    Returns:
        Path to log file or None if not configured
    """
    root_logger = logging.getLogger()
    
    for handler in root_logger.handlers:
        if isinstance(handler, logging.FileHandler):
            return Path(handler.baseFilename)
    
    return None


def disable_logging() -> None:
    """Disable all logging."""
    logging.disable(logging.CRITICAL)


def enable_logging() -> None:
    """Re-enable logging."""
    logging.disable(logging.NOTSET)


class LogCapture:
    """Context manager for capturing log messages."""
    
    def __init__(self, logger_name: str = '', level: int = logging.INFO):
        """Initialize log capture.
        
        Args:
            logger_name: Name of logger to capture (empty for root)
            level: Minimum log level to capture
        """
        self.logger_name = logger_name
        self.level = level
        self.handler = None
        self.messages = []
    
    def __enter__(self):
        """Start capturing log messages."""
        self.handler = logging.Handler()
        self.handler.setLevel(self.level)
        self.handler.emit = self._capture_message
        
        logger = logging.getLogger(self.logger_name)
        logger.addHandler(self.handler)
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop capturing log messages."""
        if self.handler:
            logger = logging.getLogger(self.logger_name)
            logger.removeHandler(self.handler)
            self.handler = None
    
    def _capture_message(self, record):
        """Capture log message.
        
        Args:
            record: Log record
        """
        self.messages.append(record)
    
    def get_messages(self) -> list:
        """Get captured messages.
        
        Returns:
            List of log records
        """
        return self.messages
    
    def get_message_strings(self) -> list:
        """Get captured messages as strings.
        
        Returns:
            List of formatted log messages
        """
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        return [formatter.format(record) for record in self.messages]


class ColoredFormatter(logging.Formatter):
    """Colored log formatter for terminal output."""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }
    
    def format(self, record):
        """Format log record with colors.
        
        Args:
            record: Log record
            
        Returns:
            Formatted log message
        """
        # Get color for log level
        color = self.COLORS.get(record.levelname, '')
        reset = self.COLORS['RESET']
        
        # Format message
        formatted = super().format(record)
        
        # Add color if terminal supports it
        if sys.stdout.isatty():
            formatted = f"{color}{formatted}{reset}"
        
        return formatted


def setup_colored_logging(verbose: bool = False) -> None:
    """Setup colored console logging.
    
    Args:
        verbose: Enable verbose logging
    """
    global _logger_configured
    
    if _logger_configured:
        return
    
    # Determine log level
    log_level = logging.DEBUG if verbose else logging.INFO
    
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Create colored formatter
    formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Set up third-party logger levels
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    _logger_configured = True
    
    # Log initial message
    logger = get_logger(__name__)
    logger.info(f"Colored logging configured (level: {logging.getLevelName(log_level)})")


def log_function_call(func):
    """Decorator to log function calls.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} returned: {result}")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} raised exception: {e}")
            raise
    
    return wrapper