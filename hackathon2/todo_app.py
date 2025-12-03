"""
Command-Line Todo Application - Phase I: In-Memory Python Console App
"""

from datetime import datetime
from typing import Dict, Optional


class Task:
    """Task data model with all required attributes."""

    def __init__(self, task_id: int, title: str, description: str = ""):
        self.id = task_id
        self.title = title
        self.description = description
        self.completed = False
        self.created_at = datetime.now()

    def __str__(self):
        status = "✓ Complete" if self.completed else "✗ Pending"
        desc = self.description if self.description else "(No description)"
        return f"ID: {self.id} | {status}\nTitle: {self.title}\nDescription: {desc}\nCreated: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class TodoApp:
    """Main Todo Application class managing all operations."""

    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self.next_id = 1

    def display_welcome(self):
        """Display welcome message on startup."""
        print("\n" + "=" * 60)
        print(" " * 15 + "WELCOME TO TODO APP")
        print("=" * 60 + "\n")

    def display_menu(self):
        """Display main menu options."""
        print("\n" + "-" * 60)
        print("MAIN MENU")
        print("-" * 60)
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task as Complete/Incomplete")
        print("6. Exit")
        print("-" * 60)

    def validate_title(self, title: str) -> tuple[bool, str]:
        """Validate task title according to rules."""
        if not title or title.strip() == "":
            return False, "Task title cannot be empty."
        if len(title) > 200:
            return False, "Task title must be 200 characters or less."
        return True, ""

    def validate_description(self, description: str) -> tuple[bool, str]:
        """Validate task description according to rules."""
        if len(description) > 1000:
            return False, "Task description must be 1000 characters or less."
        return True, ""

    def validate_task_id(self, task_id_str: str) -> tuple[bool, Optional[int], str]:
        """Validate and parse task ID."""
        try:
            task_id = int(task_id_str)
            if task_id not in self.tasks:
                return False, None, f"Task #{task_id} not found. Use 'View All Tasks' to see available IDs."
            return True, task_id, ""
        except ValueError:
            return False, None, "Please enter a valid task ID (number)."

    def add_task(self):
        """Add a new task with user input."""
        print("\n" + "=" * 60)
        print("ADD NEW TASK")
        print("=" * 60)

        # Get and validate title
        while True:
            title = input("Enter task title (required, 1-200 characters): ").strip()
            valid, error_msg = self.validate_title(title)
            if valid:
                break
            print(f"Error: {error_msg}")

        # Get and validate description
        while True:
            description = input("Enter task description (optional, max 1000 characters): ").strip()
            valid, error_msg = self.validate_description(description)
            if valid:
                break
            print(f"Error: {error_msg}")

        # Create and store task
        task = Task(self.next_id, title, description)
        self.tasks[self.next_id] = task
        print(f"\n✓ Task #{self.next_id} '{title}' added successfully")
        self.next_id += 1

    def view_all_tasks(self):
        """Display all tasks in formatted list."""
        print("\n" + "=" * 60)
        print("ALL TASKS")
        print("=" * 60)

        if not self.tasks:
            print("\nNo tasks found. Add your first task!")
            return

        for task_id in sorted(self.tasks.keys()):
            task = self.tasks[task_id]
            print("\n" + "-" * 60)
            print(task)
        print("\n" + "=" * 60)
        print(f"Total tasks: {len(self.tasks)}")

    def update_task(self):
        """Update an existing task's title and/or description."""
        print("\n" + "=" * 60)
        print("UPDATE TASK")
        print("=" * 60)

        task_id_str = input("Enter task ID to update: ").strip()
        valid, task_id, error_msg = self.validate_task_id(task_id_str)

        if not valid:
            print(f"Error: {error_msg}")
            return

        task = self.tasks[task_id]
        print("\nCurrent task details:")
        print("-" * 60)
        print(task)
        print("-" * 60)

        # Update title
        print(f"\nCurrent title: {task.title}")
        new_title = input("Enter new title (press Enter to keep current): ").strip()

        if new_title:
            valid, error_msg = self.validate_title(new_title)
            if not valid:
                print(f"Error: {error_msg}")
                return
            task.title = new_title

        # Update description
        print(f"\nCurrent description: {task.description if task.description else '(No description)'}")
        new_description = input("Enter new description (press Enter to keep current): ").strip()

        if new_description:
            valid, error_msg = self.validate_description(new_description)
            if not valid:
                print(f"Error: {error_msg}")
                return
            task.description = new_description

        print(f"\n✓ Task #{task_id} updated successfully")

    def delete_task(self):
        """Delete a task after confirmation."""
        print("\n" + "=" * 60)
        print("DELETE TASK")
        print("=" * 60)

        task_id_str = input("Enter task ID to delete: ").strip()
        valid, task_id, error_msg = self.validate_task_id(task_id_str)

        if not valid:
            print(f"Error: {error_msg}")
            return

        task = self.tasks[task_id]
        print("\nTask details for confirmation:")
        print("-" * 60)
        print(task)
        print("-" * 60)

        confirmation = input("\nAre you sure? (y/n): ").strip().lower()

        if confirmation == 'y':
            del self.tasks[task_id]
            print(f"\n✓ Task #{task_id} deleted successfully")
        else:
            print("\nDeletion cancelled.")

    def mark_complete_incomplete(self):
        """Toggle task completion status."""
        print("\n" + "=" * 60)
        print("MARK TASK AS COMPLETE/INCOMPLETE")
        print("=" * 60)

        task_id_str = input("Enter task ID: ").strip()
        valid, task_id, error_msg = self.validate_task_id(task_id_str)

        if not valid:
            print(f"Error: {error_msg}")
            return

        task = self.tasks[task_id]
        task.completed = not task.completed
        status = "complete" if task.completed else "incomplete"
        print(f"\n✓ Task #{task_id} marked as {status}")

    def run(self):
        """Main application loop."""
        self.display_welcome()

        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-6): ").strip()

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.view_all_tasks()
            elif choice == "3":
                self.update_task()
            elif choice == "4":
                self.delete_task()
            elif choice == "5":
                self.mark_complete_incomplete()
            elif choice == "6":
                print("\n" + "=" * 60)
                print("Thank you for using Todo App! Goodbye!")
                print("=" * 60 + "\n")
                break
            else:
                print("\nError: Invalid choice. Please select 1-6.")


def main():
    """Entry point for the application."""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()
