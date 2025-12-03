# Todo App - Phase I: In-Memory Python Console Application

A command-line todo application built with Python that allows you to manage tasks in an interactive console interface.

## Features

- **Add Task**: Create new tasks with title and optional description
- **View All Tasks**: Display all tasks with their details and status
- **Update Task**: Modify task title and description
- **Delete Task**: Remove tasks with confirmation
- **Mark Complete/Incomplete**: Toggle task completion status
- **Input Validation**: Comprehensive validation for all user inputs
- **Error Handling**: User-friendly error messages with retry capability

## Requirements

- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

## Installation

1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd todo-app-hackthon2
   ```

## Usage

Run the application:
```bash
python todo_app.py
```

### Menu Options

When the app starts, you'll see a menu with the following options:

1. **Add Task**
   - Enter a task title (required, 1-200 characters)
   - Enter a task description (optional, max 1000 characters)
   - Task is automatically assigned a unique ID and set as incomplete

2. **View All Tasks**
   - Displays all tasks in a formatted table
   - Shows task ID, title, status (✓ Complete / ✗ Pending), description, and creation date

3. **Update Task**
   - Enter the task ID you want to update
   - Optionally update the title (press Enter to keep current)
   - Optionally update the description (press Enter to keep current)

4. **Delete Task**
   - Enter the task ID you want to delete
   - Confirm deletion with 'y' or cancel with 'n'

5. **Mark Task as Complete/Incomplete**
   - Enter the task ID
   - Toggles between complete and incomplete status

6. **Exit**
   - Exits the application

## Data Model

Each task has the following properties:

- **id**: Unique integer identifier (auto-assigned)
- **title**: Task title (1-200 characters, required)
- **description**: Task description (0-1000 characters, optional)
- **completed**: Boolean completion status (default: False)
- **created_at**: Timestamp of task creation

## Validation Rules

- Task title cannot be empty or whitespace only
- Task title must be between 1-200 characters
- Task description maximum 1000 characters (optional)
- Task ID must be a valid integer that exists in the system
- Menu selection must be between 1-6

## Error Handling

The application handles the following errors gracefully:

- Invalid menu selection
- Task not found
- Empty or invalid task title
- Title/description exceeding character limits
- Invalid task ID format

All errors display user-friendly messages and allow retry without crashing.

## Storage

**Phase I** stores tasks in memory only (Python dictionary). Data is lost when the program exits. This is the expected behavior for this phase.

## Testing

Run the test suite to verify all functionality:
```bash
python test_app.py
```

The test suite validates:
- Task creation and initialization
- Input validation functions
- CRUD operations (Create, Read, Update, Delete)
- Completion status toggling
- Edge cases and boundary conditions

## Example Session

```
============================================================
               WELCOME TO TODO APP
============================================================

------------------------------------------------------------
MAIN MENU
------------------------------------------------------------
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task as Complete/Incomplete
6. Exit
------------------------------------------------------------

Enter your choice (1-6): 1

============================================================
ADD NEW TASK
============================================================
Enter task title (required, 1-200 characters): Buy groceries
Enter task description (optional, max 1000 characters): Milk, eggs, bread

✓ Task #1 'Buy groceries' added successfully
```

## Project Structure

```
todo-app-hackthon2/
├── todo_app.py      # Main application file
├── test_app.py      # Test suite
└── README.md        # This file
```

## Implementation Details

- **Language**: Python 3
- **Architecture**: Object-oriented with Task and TodoApp classes
- **Storage**: In-memory dictionary
- **Interface**: Console-based with menu-driven navigation
- **Validation**: Comprehensive input validation at all entry points

## Future Enhancements (Not in Phase I)

- File persistence (save/load tasks)
- Task categories and tags
- Due dates and reminders
- Task priority levels
- Search and filter functionality
- Export to CSV/JSON

## License

This project is for educational purposes.

## Author

Created as part of Phase I implementation for the Todo App project.
