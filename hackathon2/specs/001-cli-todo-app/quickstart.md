# Quickstart Guide: CLI Todo Application (Phase I)

**Feature**: Command-Line Todo Application (Phase I: In-Memory Storage)
**Date**: 2025-12-03
**For**: Developers implementing this feature

## Overview

This guide helps developers quickly understand the architecture and start implementing the CLI Todo Application Phase I. The application is a command-line tool for managing tasks with in-memory storage.

## Project Context

**What**: Interactive CLI todo app with menu-driven interface
**Phase**: I - In-memory storage (no persistence)
**Language**: Python 3.13+
**Dependencies**: None (standard library only)
**Architecture**: 3-layer (Model-Service-CLI)

## Key Documents

| Document | Purpose | Read First? |
|----------|---------|-------------|
| [spec.md](spec.md) | Feature requirements, user stories, acceptance criteria | ✅ Yes |
| [plan.md](plan.md) | Implementation plan, technical context, constitution check | ✅ Yes |
| [research.md](research.md) | Architectural decisions, best practices, rationale | 📖 Reference |
| [data-model.md](data-model.md) | Task entity definition, validation rules, storage | 📖 Reference |
| [contracts/task-service-interface.md](contracts/task-service-interface.md) | TaskService API contract | 📖 Reference |
| [contracts/cli-interface.md](contracts/cli-interface.md) | CLI behavior and user flows | 📖 Reference |

**Reading Order**: spec.md → plan.md → (start coding) → reference other docs as needed

## Architecture at a Glance

```
┌─────────────────────────────────────────────────────────┐
│                    src/main.py                          │
│            (Entry point, bootstrap)                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  src/cli/menu.py                        │
│       (MenuUI - User interface, I/O, formatting)        │
│  • Display menus and prompts                            │
│  • Validate user input                                  │
│  • Format and display output                            │
│  • Route operations to service                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│            src/services/task_service.py                 │
│     (TaskService - Business logic, CRUD operations)     │
│  • Manage task storage (in-memory dict)                 │
│  • Validate business rules                              │
│  • Perform CRUD operations                              │
│  • Generate unique IDs                                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│               src/models/task.py                        │
│          (Task - Data model, validation)                │
│  • Task dataclass definition                            │
│  • Field-level validation                               │
│  • No business logic or I/O                             │
└─────────────────────────────────────────────────────────┘
```

**Key Principle**: Strict separation of concerns
- **Models**: Data definition only
- **Services**: Business logic only
- **CLI**: Presentation only
- **No mixing**: Each layer has clear boundaries

## Directory Structure

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
│   └── formatters.py        # Output formatting utilities
├── __init__.py
└── main.py                  # Application entry point

README.md                    # User-facing usage guide
requirements.txt             # Empty (no dependencies)
```

## Implementation Checklist

### Phase 1: Models Layer

- [ ] Create `src/models/__init__.py` (empty)
- [ ] Create `src/models/task.py`:
  - [ ] Import dataclass, field, datetime
  - [ ] Define Task dataclass with 5 fields (id, title, description, completed, created_at)
  - [ ] Implement `__post_init__` for validation
  - [ ] Test: Title strip, empty check, length check
  - [ ] Test: Description truncation

**Key Implementation Detail**:
```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        # Validate and normalize
        pass
```

### Phase 2: Services Layer

- [ ] Create `src/services/__init__.py` (empty)
- [ ] Create `src/services/task_service.py`:
  - [ ] Define TaskService class
  - [ ] `__init__`: Initialize empty dict and ID counter
  - [ ] `add_task(title, description)`: Create and store task
  - [ ] `get_task(task_id)`: Retrieve by ID (or None)
  - [ ] `get_all_tasks()`: Return list of all tasks
  - [ ] `update_task(task_id, title, description)`: Modify task
  - [ ] `delete_task(task_id)`: Remove task (bool return)
  - [ ] `toggle_complete(task_id)`: Flip completed status

**Key Implementation Detail**:
```python
class TaskService:
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        # Create task, increment ID, return
        pass
```

### Phase 3: CLI Layer

- [ ] Create `src/cli/__init__.py` (empty)
- [ ] Create `src/cli/formatters.py`:
  - [ ] `format_status(completed: bool) -> str`: Status symbols (✓/✗)
  - [ ] `format_task_table(tasks: list[Task]) -> str`: ASCII table
  - [ ] `format_separator(char: str, length: int) -> str`: Lines

- [ ] Create `src/cli/menu.py`:
  - [ ] Define MenuUI class with service dependency
  - [ ] `__init__(service)`: Store service reference
  - [ ] `run()`: Main loop
  - [ ] `_display_menu()`: Show menu options
  - [ ] `_get_menu_choice() -> int`: Validate 1-6 input
  - [ ] `_handle_add_task()`: Operation 1
  - [ ] `_handle_view_all()`: Operation 2
  - [ ] `_handle_update_task()`: Operation 3
  - [ ] `_handle_delete_task()`: Operation 4
  - [ ] `_handle_toggle_complete()`: Operation 5
  - [ ] `_show_welcome()`: Welcome message
  - [ ] `_show_goodbye()`: Goodbye message

**Key Implementation Detail**:
```python
class MenuUI:
    def __init__(self, service: TaskService) -> None:
        self._service = service

    def run(self) -> None:
        self._show_welcome()
        while True:
            self._display_menu()
            choice = self._get_menu_choice()
            if choice == 6:
                break
            # Route to handlers
        self._show_goodbye()
```

### Phase 4: Application Entry Point

- [ ] Create `src/__init__.py` (empty)
- [ ] Create `src/main.py`:
  - [ ] Import sys, TaskService, MenuUI
  - [ ] Define `main()` function
  - [ ] Initialize TaskService
  - [ ] Initialize MenuUI with service
  - [ ] Call `menu.run()`
  - [ ] Handle KeyboardInterrupt gracefully
  - [ ] Exit with `sys.exit(0)`
  - [ ] Add `if __name__ == "__main__": main()`

**Key Implementation Detail**:
```python
import sys
from src.services.task_service import TaskService
from src.cli.menu import MenuUI

def main() -> None:
    service = TaskService()
    menu = MenuUI(service)
    try:
        menu.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Phase 5: Documentation & Config

- [ ] Create `README.md`:
  - [ ] Project description
  - [ ] Requirements (Python 3.13+)
  - [ ] Installation steps
  - [ ] Usage instructions
  - [ ] Examples
  - [ ] License (if applicable)

- [ ] Create `requirements.txt` (empty file - no dependencies)

## Common Pitfalls to Avoid

### ❌ Don't Do This

1. **Mixing layers**:
   ```python
   # BAD: Business logic in CLI
   class MenuUI:
       def add_task(self):
           task_id = self._next_id
           self._next_id += 1  # Wrong layer!
   ```

2. **UI in service layer**:
   ```python
   # BAD: I/O in service
   class TaskService:
       def add_task(self, title):
           print("Task added!")  # Wrong layer!
   ```

3. **Hardcoded validation values**:
   ```python
   # BAD: Magic numbers
   if len(title) > 200:  # Use named constant
   ```

4. **Ignoring None returns**:
   ```python
   # BAD: No None check
   task = service.get_task(id)
   print(task.title)  # Crashes if task is None!
   ```

5. **Letting exceptions crash app**:
   ```python
   # BAD: Unhandled exception
   choice = int(input())  # Crashes on non-numeric input
   ```

### ✅ Do This Instead

1. **Respect layer boundaries**:
   ```python
   # GOOD: Delegate to service
   class MenuUI:
       def _handle_add_task(self):
           task = self._service.add_task(title, desc)
   ```

2. **Use constants**:
   ```python
   # GOOD: Named constants
   MAX_TITLE_LENGTH = 200
   MAX_DESCRIPTION_LENGTH = 1000
   ```

3. **Check None returns**:
   ```python
   # GOOD: Safe None handling
   task = service.get_task(id)
   if task is None:
       print("Task not found")
       return
   print(task.title)
   ```

4. **Handle all exceptions**:
   ```python
   # GOOD: Graceful error handling
   try:
       choice = int(input())
   except ValueError:
       print("Invalid input")
   ```

## Testing Strategy

### Manual Testing (Required)

**Test Each User Story**:

1. **P1 - Add and View**:
   - Add task with title + description
   - Add task with title only
   - View multiple tasks
   - View empty list

2. **P2 - Mark Complete**:
   - Mark incomplete → complete
   - Mark complete → incomplete

3. **P3 - Update**:
   - Update title only
   - Update description only
   - Skip both (no changes)

4. **P4 - Delete**:
   - Delete with confirmation (y)
   - Cancel deletion (n)

**Test All Edge Cases** (from spec.md):
- Invalid menu choice (7, abc)
- Empty title
- Title > 200 chars
- Description > 1000 chars
- Non-numeric task ID
- Non-existent task ID
- Exit and verify goodbye

### Automated Testing (Optional - Future)

If adding unit tests later:
```
tests/
├── unit/
│   ├── test_task.py         # Test Task validation
│   └── test_task_service.py # Test all service methods
└── integration/
    └── test_cli_workflow.py  # Test complete workflows
```

Use pytest framework:
```bash
pip install pytest
pytest tests/
```

## Running the Application

### Development

```bash
# From repository root
python -m src.main
```

### Production (after packaging)

```bash
# Install (future)
pip install .

# Run
todo-app
```

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`
**Solution**: Run from repository root, not from src/ directory

**Issue**: UTF-8 symbols (✓✗) show as `?` or `[]`
**Solution**: Ensure terminal supports UTF-8. Windows: Use Windows Terminal or set `chcp 65001`

**Issue**: Type hints cause syntax error
**Solution**: Verify Python 3.13+ installed: `python --version`

**Issue**: Application crashes on invalid input
**Solution**: Wrap all input operations in try/except blocks

## Development Workflow

1. **Read spec.md** - Understand requirements
2. **Read plan.md** - Understand architecture
3. **Implement bottom-up**: Models → Services → CLI → Main
4. **Test each layer** before moving to next
5. **Manual test** all user stories and edge cases
6. **Document** README.md
7. **Ready for review**

## Next Steps After Phase I

**Phase II**: Add file persistence (JSON/CSV)
- Extend TaskService with save/load methods
- No changes to models or CLI (clean architecture pays off!)

**Phase III**: Add database storage (SQLite)
- Replace in-memory dict with database
- Add migration scripts
- No changes to CLI layer

**Future**: Enhanced features
- Sorting and filtering
- Categories and tags
- Due dates and reminders
- Search functionality

## Code Style Guidelines

**Follow Constitution Principle II** (Clean Code Standards):

- ✅ Type hints on all functions and methods
- ✅ Docstrings for all public APIs (Google/NumPy style)
- ✅ snake_case for functions and variables
- ✅ PascalCase for classes
- ✅ UPPERCASE for constants
- ✅ 88-character line limit (Black formatter)
- ✅ No manual code edits (AI-first development per Constitution Principle VII)

**Example**:
```python
MAX_TITLE_LENGTH: int = 200  # Constant

class TaskService:  # PascalCase
    """Manages task storage and operations."""  # Docstring

    def add_task(self, title: str, description: str = "") -> Task:  # Type hints
        """Create and store a new task.

        Args:
            title: Task title (1-200 characters, required)
            description: Optional detailed information

        Returns:
            Created Task object with auto-assigned ID

        Raises:
            ValueError: If title is empty or too long
        """
        task_id = self._next_id  # snake_case
        # Implementation...
```

## Getting Help

**Questions about**:
- **Requirements**: Check spec.md
- **Architecture**: Check plan.md and research.md
- **Data model**: Check data-model.md
- **Interfaces**: Check contracts/
- **Constitution compliance**: Check .specify/memory/constitution.md

**Still stuck?**: Create a detailed question referencing:
- Which file/layer you're working on
- What you've tried
- Specific error messages
- Which requirement you're implementing (FR-XXX)

## Success Criteria Recap

Your implementation is complete when:

- ✅ All 4 user stories work as specified
- ✅ All 44 functional requirements (FR-001 through FR-044) met
- ✅ All 8 success criteria (SC-001 through SC-008) achieved
- ✅ All edge cases handled gracefully
- ✅ No crashes from any user input
- ✅ Clean separation of concerns (3 layers)
- ✅ Type hints on all functions/methods
- ✅ Docstrings on all public APIs
- ✅ README.md with usage instructions
- ✅ Manual testing complete

**Ready to implement?** Start with `src/models/task.py` and work your way up!
