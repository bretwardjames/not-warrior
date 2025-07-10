"""
Taskwarrior integration for CLI interface and task operations.
"""

import json
import subprocess
from typing import Dict, List, Optional, Any
from not_warrior.models.task import Task
from not_warrior.utils.logger import get_logger

logger = get_logger(__name__)


class TaskwarriorClient:
    """Client for interacting with Taskwarrior."""
    
    def __init__(self, taskwarrior_cmd: str = "task"):
        """Initialize Taskwarrior client.
        
        Args:
            taskwarrior_cmd: Path to taskwarrior command
        """
        self.cmd = taskwarrior_cmd
        self.notion_tag = "notion"  # Tag to identify Notion-synced tasks
    
    def test_connection(self) -> bool:
        """Test if Taskwarrior is available and accessible.
        
        Returns:
            True if Taskwarrior is available
        """
        try:
            # TODO: Test taskwarrior command
            result = subprocess.run([self.cmd, "version"], capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Taskwarrior connection test failed: {e}")
            return False
    
    def get_tasks(self, filter_expr: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get tasks from Taskwarrior.
        
        Args:
            filter_expr: Taskwarrior filter expression
            
        Returns:
            List of task dictionaries
        """
        try:
            # TODO: Build command with filter
            cmd = [self.cmd, "export"]
            if filter_expr:
                cmd.append(filter_expr)
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return json.loads(result.stdout) if result.stdout.strip() else []
            else:
                logger.error(f"Failed to get tasks: {result.stderr}")
                return []
        except Exception as e:
            logger.error(f"Failed to get tasks: {e}")
            return []
    
    def get_notion_tasks(self) -> List[Dict[str, Any]]:
        """Get tasks tagged with notion tag.
        
        Returns:
            List of Notion-synced tasks
        """
        return self.get_tasks(f"+{self.notion_tag}")
    
    def add_task(self, task_data: Dict[str, Any]) -> Optional[str]:
        """Add new task to Taskwarrior.
        
        Args:
            task_data: Task data dictionary
            
        Returns:
            Task UUID if successful
        """
        try:
            # TODO: Build add command from task data
            cmd = [self.cmd, "add"]
            
            # Add description
            if "description" in task_data:
                cmd.append(task_data["description"])
            
            # Add other attributes
            for key, value in task_data.items():
                if key != "description":
                    cmd.append(f"{key}:{value}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                # TODO: Extract UUID from output
                return "uuid-placeholder"
            else:
                logger.error(f"Failed to add task: {result.stderr}")
                return None
        except Exception as e:
            logger.error(f"Failed to add task: {e}")
            return None
    
    def update_task(self, task_uuid: str, updates: Dict[str, Any]) -> bool:
        """Update existing task.
        
        Args:
            task_uuid: Task UUID
            updates: Updates to apply
            
        Returns:
            True if successful
        """
        try:
            # TODO: Build modify command
            cmd = [self.cmd, task_uuid, "modify"]
            
            for key, value in updates.items():
                if value is None:
                    cmd.append(f"{key}:")
                else:
                    cmd.append(f"{key}:{value}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Failed to update task: {e}")
            return False
    
    def complete_task(self, task_uuid: str) -> bool:
        """Mark task as completed.
        
        Args:
            task_uuid: Task UUID
            
        Returns:
            True if successful
        """
        try:
            result = subprocess.run([self.cmd, task_uuid, "done"], capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Failed to complete task: {e}")
            return False
    
    def delete_task(self, task_uuid: str) -> bool:
        """Delete task.
        
        Args:
            task_uuid: Task UUID
            
        Returns:
            True if successful
        """
        try:
            result = subprocess.run([self.cmd, task_uuid, "delete"], capture_output=True, text=True, input="yes\n")
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Failed to delete task: {e}")
            return False
    
    def get_task_by_uuid(self, task_uuid: str) -> Optional[Dict[str, Any]]:
        """Get specific task by UUID.
        
        Args:
            task_uuid: Task UUID
            
        Returns:
            Task data or None
        """
        tasks = self.get_tasks(task_uuid)
        return tasks[0] if tasks else None
    
    def task_to_taskwarrior(self, task: Task) -> Dict[str, Any]:
        """Convert Task object to Taskwarrior format.
        
        Args:
            task: Task object
            
        Returns:
            Taskwarrior task data
        """
        # TODO: Implement conversion logic
        return {}
    
    def taskwarrior_to_task(self, tw_task: Dict[str, Any]) -> Task:
        """Convert Taskwarrior data to Task object.
        
        Args:
            tw_task: Taskwarrior task data
            
        Returns:
            Task object
        """
        # TODO: Implement conversion logic
        return Task()
    
    def add_notion_tag(self, task_uuid: str) -> bool:
        """Add notion tag to task.
        
        Args:
            task_uuid: Task UUID
            
        Returns:
            True if successful
        """
        return self.update_task(task_uuid, {"tags": f"+{self.notion_tag}"})
    
    def remove_notion_tag(self, task_uuid: str) -> bool:
        """Remove notion tag from task.
        
        Args:
            task_uuid: Task UUID
            
        Returns:
            True if successful
        """
        return self.update_task(task_uuid, {"tags": f"-{self.notion_tag}"})