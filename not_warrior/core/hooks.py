"""
Hook system for Taskwarrior integration and automatic synchronization.
"""

import os
import shutil
import stat
from pathlib import Path
from typing import Dict, List, Optional
from not_warrior.utils.logger import get_logger

logger = get_logger(__name__)


class HookManager:
    """Manager for Taskwarrior hooks."""
    
    def __init__(self, hook_dir: Optional[str] = None):
        """Initialize hook manager.
        
        Args:
            hook_dir: Custom hook directory path
        """
        self.hook_dir = Path(hook_dir) if hook_dir else self._get_default_hook_dir()
        self.hook_name = "on-modify-notion-sync"
        self.hook_path = self.hook_dir / self.hook_name
    
    def _get_default_hook_dir(self) -> Path:
        """Get default Taskwarrior hook directory.
        
        Returns:
            Path to hook directory
        """
        # TODO: Detect Taskwarrior data directory
        # TODO: Handle different OS configurations
        home = Path.home()
        
        # Try common locations
        locations = [
            home / ".task" / "hooks",
            home / ".taskrc" / "hooks",
            Path("/usr/share/task/hooks")
        ]
        
        for location in locations:
            if location.exists():
                return location
        
        # Default to ~/.task/hooks
        return home / ".task" / "hooks"
    
    def is_hook_installed(self) -> bool:
        """Check if hook is installed.
        
        Returns:
            True if hook is installed
        """
        return self.hook_path.exists() and self.hook_path.is_file()
    
    def install_hook(self, force: bool = False) -> bool:
        """Install Taskwarrior hook.
        
        Args:
            force: Force reinstall if hook exists
            
        Returns:
            True if installation successful
        """
        try:
            if self.is_hook_installed() and not force:
                logger.info("Hook already installed")
                return True
            
            # Create hook directory if it doesn't exist
            self.hook_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate hook script
            hook_script = self._generate_hook_script()
            
            # Write hook script
            with open(self.hook_path, 'w') as f:
                f.write(hook_script)
            
            # Make executable
            self.hook_path.chmod(self.hook_path.stat().st_mode | stat.S_IEXEC)
            
            logger.info(f"Hook installed at {self.hook_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to install hook: {e}")
            return False
    
    def remove_hook(self) -> bool:
        """Remove Taskwarrior hook.
        
        Returns:
            True if removal successful
        """
        try:
            if self.is_hook_installed():
                self.hook_path.unlink()
                logger.info("Hook removed successfully")
            else:
                logger.info("Hook not installed")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to remove hook: {e}")
            return False
    
    def _generate_hook_script(self) -> str:
        """Generate hook script content.
        
        Returns:
            Hook script as string
        """
        # TODO: Generate actual hook script
        # TODO: Handle different hook types (on-add, on-modify, etc.)
        # TODO: Include proper error handling
        
        script = f'''#!/usr/bin/env python3
"""
Taskwarrior hook for not-warrior synchronization.
Generated automatically - do not edit manually.
"""

import sys
import json
import subprocess
from pathlib import Path

def main():
    """Hook entry point."""
    try:
        # Read task data from stdin
        old_task = json.loads(sys.stdin.readline())
        new_task = json.loads(sys.stdin.readline())
        
        # Check if task has notion tag
        if "notion" in new_task.get("tags", []):
            # Trigger sync
            subprocess.run(["not-warrior", "sync", "run", "--direction", "to-notion"], 
                         capture_output=True)
        
        # Output modified task
        print(json.dumps(new_task))
        
    except Exception as e:
        # Log error but don't fail the task operation
        with open(Path.home() / ".task" / "hook.log", "a") as f:
            f.write(f"Hook error: {{e}}\\n")
        
        # Pass through the new task
        if 'new_task' in locals():
            print(json.dumps(new_task))

if __name__ == "__main__":
    main()
'''
        return script
    
    def test_hook(self) -> bool:
        """Test hook functionality.
        
        Returns:
            True if hook works correctly
        """
        try:
            if not self.is_hook_installed():
                logger.error("Hook not installed")
                return False
            
            # TODO: Test hook with sample data
            # TODO: Verify hook executes correctly
            
            return True
            
        except Exception as e:
            logger.error(f"Hook test failed: {e}")
            return False
    
    def get_hook_status(self) -> Dict[str, any]:
        """Get hook status information.
        
        Returns:
            Hook status details
        """
        try:
            return {
                "installed": self.is_hook_installed(),
                "path": str(self.hook_path),
                "executable": self.hook_path.is_file() and os.access(self.hook_path, os.X_OK) if self.hook_path.exists() else False,
                "hook_dir": str(self.hook_dir),
                "hook_name": self.hook_name
            }
        except Exception as e:
            logger.error(f"Failed to get hook status: {e}")
            return {}
    
    def handle_hook_event(self, event_type: str, old_task: Dict, new_task: Dict) -> bool:
        """Handle hook event.
        
        Args:
            event_type: Type of event ('add', 'modify', 'delete')
            old_task: Previous task state
            new_task: New task state
            
        Returns:
            True if handled successfully
        """
        try:
            # TODO: Implement event handling logic
            # TODO: Determine if sync is needed
            # TODO: Trigger appropriate sync operation
            
            logger.info(f"Hook event: {event_type}")
            
            # Check if task has notion tag
            if "notion" in new_task.get("tags", []):
                # TODO: Trigger sync
                pass
            
            return True
            
        except Exception as e:
            logger.error(f"Hook event handling failed: {e}")
            return False