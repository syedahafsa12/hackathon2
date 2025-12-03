# CLI Todo Application (Phase I)

A command-line todo application with in-memory storage built in Python.

## Features

- **Add Tasks**: Create tasks with titles and optional descriptions
- **View Tasks**: Display all tasks in a formatted table with completion status
- **Mark Complete**: Toggle task completion status
- **Update Tasks**: Modify task titles and descriptions
- **Delete Tasks**: Remove tasks with confirmation
- **Interactive Menu**: User-friendly numbered menu interface

## Requirements

- Python 3.13 or higher
- No external dependencies (uses standard library only)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hackathon2
```

2. Verify Python version:
```bash
python --version  # Should be 3.13 or higher
```

## Usage

Run the application:
```bash
python -m src.main
```

### Menu Options

1. **Add Task** - Create a new task
2. **View All Tasks** - Display all tasks in a table
3. **Update Task** - Modify an existing task
4. **Delete Task** - Remove a task (with confirmation)
5. **Mark Task as Complete/Incomplete** - Toggle task status
6. **Exit** - Close the application

### Example Session

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

Enter your choice (1-6): 1

--- Add New Task ---

Enter task title: Buy groceries
Enter task description (optional, press Enter to skip): milk, eggs, bread

✓ Success: Task #1 'Buy groceries' added successfully

[Returns to menu]
```

## Architecture

The application follows a clean three-layer architecture:

- **Models** (`src/models/`): Task data model with validation
- **Services** (`src/services/`): Business logic and task management
- **CLI** (`src/cli/`): User interface and presentation layer

## Project Structure

```
src/
├── models/
│   ├── __init__.py
│   └── task.py              # Task dataclass
├── services/
│   ├── __init__.py
│   └── task_service.py      # TaskService class
├── cli/
│   ├── __init__.py
│   ├── menu.py              # MenuUI class
│   └── formatters.py        # Output formatting
├── __init__.py
└── main.py                  # Application entry point
```

## Data Storage

**Phase I** uses in-memory storage only:
- All tasks stored in memory (dictionary)
- Data is lost when application exits
- No file persistence or database

This is intentional for Phase I. Future phases will add:
- **Phase II**: File persistence (JSON/CSV)
- **Phase III**: Database storage (SQLite/PostgreSQL)

## Validation Rules

- **Title**: Required, 1-200 characters, cannot be empty/whitespace
- **Description**: Optional, max 1000 characters
- **Task ID**: Must be valid integer, must exist for operations
- **Menu Choice**: Must be 1-6

All errors are handled gracefully with user-friendly messages and retry capability.

## Development

### Running Tests

Manual acceptance testing is used for Phase I. Test each user story:

1. **Add and View Tasks** (Priority 1 - MVP)
   - Add tasks with various titles/descriptions
   - View task list
   - Verify formatting and empty state

2. **Mark Complete** (Priority 2)
   - Mark tasks as complete
   - Toggle back to incomplete
   - Verify status symbols (✓/✗)

3. **Update Tasks** (Priority 3)
   - Update titles and descriptions
   - Skip fields to keep existing values

4. **Delete Tasks** (Priority 4)
   - Delete with confirmation
   - Cancel deletion

### Code Style

- Follows PEP 8 guidelines
- Type hints on all functions
- Docstrings on all public APIs
- 88-character line limit (Black formatter)

## Limitations (Phase I)

- No data persistence (memory only)
- No multi-user support
- No task categories or tags
- No due dates or reminders
- No search or filtering
- No undo functionality

These features are intentionally deferred to future phases.

## License

[Add license information]

## Contributing

[Add contribution guidelines]
