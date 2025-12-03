# CLI Interface Contract

**Component**: `src/cli/menu.py`
**Consumer**: `src/main.py` (application entry point)
**Dependencies**: `src/services/task_service.py` (TaskService)
**Date**: 2025-12-03

## Overview

This contract defines the CLI interface for the todo application. The CLI layer is responsible for:
- Displaying menus and prompts to the user
- Capturing and validating user input
- Formatting and displaying output
- Delegating business operations to TaskService

## Class: MenuUI

### Constructor

```python
def __init__(self, service: TaskService) -> None
```

**Purpose**: Initialize the menu-driven user interface

**Parameters**:
- `service` (TaskService, required): The task service instance for business operations

**Postconditions**:
- UI is ready to run
- Service reference stored for later use

**Side Effects**: None

---

### Method: run

```python
def run(self) -> None
```

**Purpose**: Main application loop - display menu, process user input, execute operations

**Parameters**: None

**Returns**: None (runs until user selects Exit)

**Raises**: None (all errors caught and handled internally)

**Behavior**:
1. Display welcome message once at startup
2. Loop:
   - Display menu with 6 options
   - Get user input (menu choice)
   - Validate input
   - Route to appropriate operation handler
   - Display results/confirmation
   - Return to menu (unless Exit selected)
3. Display goodbye message
4. Clean exit

**Side Effects**:
- Reads from stdin
- Writes to stdout
- Modifies task storage via service (indirectly)

**Exit Conditions**:
- User selects option 6 (Exit)
- Displays: "Thank you for using Todo App! Goodbye!"
- Returns control to caller (main.py calls sys.exit(0))

---

## User Interaction Flow

### Menu Display

**Format**:
```
================================================================================
                         TODO APPLICATION
================================================================================

Main Menu:
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task as Complete/Incomplete
6. Exit

Enter your choice (1-6):
```

**Requirements**:
- Clear separators (80 equals signs)
- Numbered options (1-6)
- User-friendly prompts
- Consistent formatting

---

### Operation 1: Add Task

**User Flow**:
```
Enter your choice (1-6): 1

--- Add New Task ---

Enter task title: Buy groceries
Enter task description (optional, press Enter to skip): milk, eggs, bread

✓ Success: Task #1 'Buy groceries' added successfully

[Return to menu]
```

**Behavior**:
1. Prompt for title
2. Validate title:
   - If empty/whitespace: Display error, re-prompt
   - If > 200 chars: Display error, re-prompt
3. Prompt for description (optional)
4. If description > 1000 chars: Truncate silently
5. Call `service.add_task(title, description)`
6. Display confirmation with task ID and title
7. Return to menu

**Error Messages**:
- Empty title: "Task title cannot be empty."
- Title too long: "Task title must be 200 characters or less."

---

### Operation 2: View All Tasks

**User Flow (with tasks)**:
```
Enter your choice (1-6): 2

--- All Tasks ---

================================================================================
ID | Status        | Title                    | Description
================================================================================
1  | ✗ Pending     | Buy groceries            | milk, eggs, bread
2  | ✓ Complete    | Finish report            |
3  | ✗ Pending     | Call dentist             | Schedule appointment
================================================================================

Total tasks: 3

[Return to menu]
```

**User Flow (empty)**:
```
Enter your choice (1-6): 2

--- All Tasks ---

No tasks found. Add your first task!

[Return to menu]
```

**Behavior**:
1. Call `service.get_all_tasks()`
2. If empty: Display empty state message
3. If not empty:
   - Display table header
   - For each task: Display formatted row with ID, status symbol, title, description
   - Display separator
   - Display total count
4. Return to menu

**Formatting**:
- Status symbols: `✓ Complete` or `✗ Pending`
- Columns aligned with padding
- Truncate long titles/descriptions to fit table
- Use separators for readability

---

### Operation 3: Update Task

**User Flow**:
```
Enter your choice (1-6): 3

--- Update Task ---

Enter task ID to update: 1

Current task details:
  ID: 1
  Title: Buy groceries
  Description: milk, eggs, bread
  Status: ✗ Pending

Enter new title (press Enter to keep current): Buy groceries and supplies
Enter new description (press Enter to keep current):

✓ Success: Task #1 updated successfully

[Return to menu]
```

**Behavior**:
1. Prompt for task ID
2. Validate ID:
   - If non-numeric: Display error, re-prompt
   - If task not found: Display error, return to menu
3. Display current task details
4. Prompt for new title (optional):
   - If Enter pressed: Keep existing
   - If provided: Validate and use new title
5. Prompt for new description (optional):
   - If Enter pressed: Keep existing
   - If provided: Use new description
6. Call `service.update_task(task_id, title, description)`
7. Display confirmation
8. Return to menu

**Error Messages**:
- Invalid ID format: "Please enter a valid task ID (number)."
- Task not found: "Task #[ID] not found. Use 'View All Tasks' to see available IDs."
- Empty title: "Task title cannot be empty."
- Title too long: "Task title must be 200 characters or less."

---

### Operation 4: Delete Task

**User Flow**:
```
Enter your choice (1-6): 4

--- Delete Task ---

Enter task ID to delete: 1

Task to delete:
  ID: 1
  Title: Buy groceries
  Description: milk, eggs, bread
  Status: ✗ Pending

Are you sure you want to delete this task? (y/n): y

✓ Success: Task #1 deleted successfully

[Return to menu]
```

**User Flow (cancelled)**:
```
Are you sure you want to delete this task? (y/n): n

Deletion cancelled.

[Return to menu]
```

**Behavior**:
1. Prompt for task ID
2. Validate ID and check existence
3. Retrieve and display task details
4. Prompt for confirmation (y/n)
5. If 'y': Call `service.delete_task(task_id)`, display success
6. If 'n': Display cancellation message
7. Return to menu

**Error Messages**:
- Invalid ID format: "Please enter a valid task ID (number)."
- Task not found: "Task #[ID] not found. Use 'View All Tasks' to see available IDs."

---

### Operation 5: Mark Task as Complete/Incomplete

**User Flow**:
```
Enter your choice (1-6): 5

--- Toggle Task Completion ---

Enter task ID: 1

✓ Success: Task #1 marked as complete

[Return to menu]
```

**Behavior**:
1. Prompt for task ID
2. Validate ID and check existence
3. Call `service.toggle_complete(task_id)`
4. Display confirmation with new status (complete/incomplete)
5. Return to menu

**Error Messages**:
- Invalid ID format: "Please enter a valid task ID (number)."
- Task not found: "Task #[ID] not found. Use 'View All Tasks' to see available IDs."

---

### Operation 6: Exit

**User Flow**:
```
Enter your choice (1-6): 6

Thank you for using Todo App! Goodbye!

[Application exits]
```

**Behavior**:
1. Display goodbye message
2. Return from `run()` method
3. Caller (main.py) calls `sys.exit(0)`

---

## Input Validation Requirements

### Menu Choice Validation

**Valid Input**: Integer 1-6

**Validation Steps**:
1. Try to parse input as integer
2. Check if in range [1, 6]
3. If invalid: Display "Invalid choice. Please select 1-6."
4. Re-prompt for input

**Example**:
```python
while True:
    try:
        choice = int(input("Enter your choice (1-6): "))
        if 1 <= choice <= 6:
            break
        else:
            print("Invalid choice. Please select 1-6.")
    except ValueError:
        print("Invalid choice. Please select 1-6.")
```

### Task ID Validation

**Valid Input**: Positive integer

**Validation Steps**:
1. Try to parse input as integer
2. If parse fails: Display "Please enter a valid task ID (number)."
3. If parse succeeds: Attempt operation
4. If task not found: Display "Task #[ID] not found. Use 'View All Tasks' to see available IDs."

**Example**:
```python
try:
    task_id = int(input("Enter task ID: "))
    task = service.get_task(task_id)
    if task is None:
        print(f"Task #{task_id} not found. Use 'View All Tasks' to see available IDs.")
        return
    # Proceed with operation
except ValueError:
    print("Please enter a valid task ID (number).")
    return
```

### Title Validation

**Valid Input**: Non-empty string, 1-200 characters (after strip)

**Validation Steps**:
1. Strip whitespace: `title.strip()`
2. Check not empty: `if not title: ...`
3. Check length: `if len(title) > 200: ...`
4. If invalid: Display error, re-prompt

**Example**:
```python
while True:
    title = input("Enter task title: ").strip()
    if not title:
        print("Task title cannot be empty.")
    elif len(title) > 200:
        print("Task title must be 200 characters or less.")
    else:
        break
```

### Description Validation

**Valid Input**: Any string, max 1000 characters

**Validation Steps**:
1. No validation required (description is optional)
2. If > 1000 chars: Truncate silently
3. Empty string is valid

### Confirmation (y/n) Validation

**Valid Input**: 'y', 'Y', 'n', 'N'

**Validation Steps**:
1. Get input
2. Convert to lowercase
3. Check if 'y' or 'n'
4. If invalid: Re-prompt

**Example**:
```python
while True:
    confirm = input("Are you sure? (y/n): ").lower()
    if confirm in ['y', 'n']:
        break
    print("Please enter 'y' for yes or 'n' for no.")
```

---

## Output Formatting Requirements

### Status Symbols

**Complete Task**: `✓ Complete`
**Incomplete Task**: `✗ Pending`

**Implementation**:
```python
def format_status(completed: bool) -> str:
    return "✓ Complete" if completed else "✗ Pending"
```

### Table Formatting

**Requirements**:
- Fixed-width columns with padding
- Header row with separator
- Aligned content
- Truncate long values with ellipsis (...)

**Example**:
```python
def format_task_table(tasks: list[Task]) -> str:
    # Calculate column widths
    # Format header
    # Format each task row
    # Add separators
    pass
```

### Separators

**Major Separator** (sections): `"=" * 80`
**Minor Separator** (table rows): `"-" * 80`

---

## Error Handling Contract

### No Exceptions Propagated

The CLI layer MUST catch and handle all exceptions:
- `ValueError` from service methods
- `KeyboardInterrupt` (Ctrl+C)
- Any other unexpected errors

### User-Friendly Messages

All error messages MUST:
- Be clear and actionable
- Guide user to correct action
- Avoid technical jargon
- Follow specification exact wording where defined

### Graceful Degradation

The application MUST:
- Never crash from user input
- Always return to menu after errors
- Allow user to retry operations
- Provide exit option at all times

---

## Integration Example

### main.py

```python
import sys
from src.services.task_service import TaskService
from src.cli.menu import MenuUI

def main() -> None:
    """Application entry point."""
    # Initialize service
    service = TaskService()

    # Initialize CLI
    menu = MenuUI(service)

    # Run application
    try:
        menu.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")

    # Clean exit
    sys.exit(0)

if __name__ == "__main__":
    main()
```

---

## Testing Contract

### Manual Testing Checklist

Each operation must be manually tested for:

1. **Add Task**:
   - [ ] Valid title and description
   - [ ] Valid title, no description
   - [ ] Empty title (error)
   - [ ] Title with whitespace only (error)
   - [ ] Title > 200 chars (error)
   - [ ] Description > 1000 chars (truncate)
   - [ ] Verify confirmation message
   - [ ] Verify task appears in list

2. **View All Tasks**:
   - [ ] View with 0 tasks (empty message)
   - [ ] View with 1 task
   - [ ] View with multiple tasks
   - [ ] Verify status symbols correct
   - [ ] Verify table formatting aligned
   - [ ] Verify total count correct

3. **Update Task**:
   - [ ] Update title only
   - [ ] Update description only
   - [ ] Update both fields
   - [ ] Skip both (press Enter twice)
   - [ ] Invalid task ID (error)
   - [ ] Non-numeric ID (error)
   - [ ] Empty new title (error)
   - [ ] Verify changes persist

4. **Delete Task**:
   - [ ] Delete with confirmation (y)
   - [ ] Cancel deletion (n)
   - [ ] Invalid task ID (error)
   - [ ] Non-numeric ID (error)
   - [ ] Verify task removed from list

5. **Toggle Complete**:
   - [ ] Mark incomplete task as complete
   - [ ] Mark complete task as incomplete
   - [ ] Invalid task ID (error)
   - [ ] Non-numeric ID (error)
   - [ ] Verify status changes in list

6. **Menu Navigation**:
   - [ ] Valid choices 1-6 work correctly
   - [ ] Invalid choice (0, 7, 100) shows error
   - [ ] Non-numeric input shows error
   - [ ] Return to menu after each operation
   - [ ] Exit option terminates cleanly

7. **Edge Cases**:
   - [ ] All tasks deleted (empty list)
   - [ ] 1000+ tasks (performance)
   - [ ] UTF-8 symbols display correctly
   - [ ] Long titles/descriptions format correctly
   - [ ] Rapid input (no crashes)

---

## Version History

- **v1.0** (2025-12-03): Initial CLI interface definition for Phase I
