# Data Model: CLI Todo Application (Phase I)

**Feature**: Command-Line Todo Application (Phase I)
**Date**: 2025-12-03
**Status**: Complete

## Overview

This document defines the data model for the CLI Todo Application Phase I. The model is intentionally simple to match the in-memory storage constraint and focuses on the single Task entity with its attributes, validation rules, and state transitions.

## Entities

### Task

Represents a single todo item in the system.

**Purpose**: Store all information related to a user's task, including title, optional description, completion status, and creation timestamp.

**Storage**: In-memory dictionary with task ID as key (`dict[int, Task]`)

**Attributes**:

| Attribute | Type | Required | Default | Constraints | Description |
|-----------|------|----------|---------|-------------|-------------|
| `id` | `int` | Yes | Auto-assigned | Positive integer, unique, auto-increment starting from 1 | Unique identifier for the task |
| `title` | `str` | Yes | None | 1-200 characters, cannot be empty or whitespace-only | Short description of what needs to be done |
| `description` | `str` | No | Empty string `""` | Max 1000 characters | Optional detailed information about the task |
| `completed` | `bool` | No | `False` | True or False | Whether the task has been marked as done |
| `created_at` | `datetime` | No | Current timestamp | Valid datetime | Timestamp when the task was created |

**Key Characteristics**:
- **Uniqueness**: Task ID is unique across all tasks
- **Immutable ID**: Once assigned, task ID never changes
- **Mutable content**: Title, description, and completed status can be updated
- **Immutable timestamp**: `created_at` is set once at creation and never modified

## Validation Rules

### Field-Level Validation

**ID (`id`)**:
- **Rule**: Must be positive integer ≥ 1
- **Enforced by**: TaskService auto-increment logic
- **Error condition**: N/A (system-generated, never user-provided)

**Title (`title`)**:
- **Rule 1**: Cannot be empty string
  - Validation: `title.strip() != ""`
  - Error: "Task title cannot be empty."
  - Source: FR-027, FR-035

- **Rule 2**: Must be between 1 and 200 characters (after strip)
  - Validation: `1 <= len(title.strip()) <= 200`
  - Error (too long): "Task title must be 200 characters or less."
  - Error (empty): Covered by Rule 1
  - Source: FR-028, FR-036

- **Rule 3**: Whitespace normalized
  - Validation: Apply `title.strip()` before storage
  - Effect: Leading/trailing whitespace removed
  - Source: FR-027 (reject whitespace-only)

**Description (`description`)**:
- **Rule 1**: Maximum 1000 characters
  - Validation: `len(description) <= 1000`
  - Enforcement strategy: Truncate to 1000 chars (user-friendly) or reject with error
  - Source: FR-029

- **Rule 2**: Empty string is valid (description optional)
  - Default value: `""`
  - Source: FR-007 (optional description)

**Completed (`completed`)**:
- **Rule**: Must be boolean (True or False)
  - Type validation via Python type hints
  - Default: `False`
  - Source: FR-009, FR-021

**Created At (`created_at`)**:
- **Rule**: Must be valid datetime object
  - Generated automatically via `datetime.now()`
  - Never modified after creation
  - Source: FR-010

### Entity-Level Validation

**Task Creation**:
1. ID must not already exist in storage (enforced by auto-increment)
2. Title must pass all title validation rules
3. Description must pass description validation
4. `completed` defaults to `False` if not provided
5. `created_at` auto-generated if not provided

**Task Update**:
1. Task ID must exist in storage (FR-030)
2. If title provided, must pass title validation rules
3. If description provided, must pass description validation
4. `id` and `created_at` cannot be modified

**Task Deletion**:
1. Task ID must exist in storage (FR-030)
2. Confirmation required before permanent deletion (FR-024, FR-025)

**Task Status Toggle**:
1. Task ID must exist in storage (FR-030)
2. Toggle operation: `completed = not completed`

## State Transitions

### Task Lifecycle States

```
[Non-existent]
    |
    | add_task()
    v
[Incomplete] (completed=False)
    |
    | toggle_complete()
    v
[Complete] (completed=True)
    |
    | toggle_complete()
    v
[Incomplete] (completed=False)
    |
    | delete_task()
    v
[Deleted/Non-existent]
```

**State Descriptions**:

1. **Non-existent**: Task does not exist in system
   - Transitions to: Incomplete (via add_task)

2. **Incomplete** (`completed=False`): Task exists but not marked done
   - Can transition to: Complete (via toggle_complete), Deleted (via delete_task)
   - Can be updated: title, description can change
   - Initial state for new tasks

3. **Complete** (`completed=True`): Task exists and marked done
   - Can transition to: Incomplete (via toggle_complete), Deleted (via delete_task)
   - Can be updated: title, description can change
   - Note: Completion is toggleable, not permanent

4. **Deleted**: Task permanently removed from system
   - Terminal state (no transitions out)
   - ID may be reused in future (though not required)

### Update Operations

**Update Title/Description**:
- Valid from: Incomplete or Complete state
- Effect: Modifies title and/or description fields
- Does not change: `id`, `completed`, `created_at`
- Preserves: Current completion state

**Toggle Completion**:
- Valid from: Incomplete or Complete state
- Effect: Flips `completed` boolean
- Does not change: `id`, `title`, `description`, `created_at`

## Data Relationships

### Phase I: No Relationships

In Phase I (in-memory storage), Task is the only entity. No relationships exist.

**Future Phase Considerations**:

- **Phase II/III**: May introduce User entity with one-to-many relationship
  - One User has many Tasks
  - Each Task belongs to one User

- **Future**: May introduce Category/Tag entities with many-to-many relationships
  - One Task can have many Tags
  - One Tag can apply to many Tasks

## Storage Implementation Details

### In-Memory Dictionary Structure

**Storage container**: `dict[int, Task]`

**Key**: Task ID (int)
**Value**: Task object

**Example**:
```python
{
    1: Task(id=1, title="Buy groceries", description="milk, eggs", completed=False, created_at=datetime(2025,12,3,10,0)),
    2: Task(id=2, title="Finish report", description="", completed=True, created_at=datetime(2025,12,3,11,0)),
    5: Task(id=5, title="Call dentist", description="Schedule checkup", completed=False, created_at=datetime(2025,12,3,12,0))
}
```

**Note**: Dictionary keys may have gaps (e.g., 1, 2, 5) if tasks are deleted. This is acceptable per specification assumptions.

### ID Generation Strategy

**Approach**: Auto-increment counter

**Implementation**:
```python
class TaskService:
    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        task_id = self._next_id
        self._next_id += 1
        # Create and store task
```

**Properties**:
- IDs are sequential and predictable
- IDs are never reused (counter only increments)
- No collision detection needed (counter guarantees uniqueness)
- Simple and efficient (no max calculation needed)

**Alternative (not used)**: `max(self._tasks.keys(), default=0) + 1`
- More complex
- Requires calculation on each add
- Reuses IDs after deletion (may confuse users)

## Data Access Patterns

### CRUD Operations

**Create (Add Task)**:
- Input: title (required), description (optional)
- Validation: Title validation rules
- Operation: Create Task object, assign next ID, insert into dictionary
- Output: Created Task object
- Complexity: O(1)

**Read (Get Task by ID)**:
- Input: task_id (int)
- Validation: ID exists in dictionary
- Operation: Dictionary lookup by ID
- Output: Task object or None if not found
- Complexity: O(1)

**Read (Get All Tasks)**:
- Input: None
- Validation: None
- Operation: Iterate dictionary values
- Output: List of all Task objects
- Complexity: O(n) where n = number of tasks

**Update (Modify Task)**:
- Input: task_id (int), optional new_title (str), optional new_description (str)
- Validation: ID exists, title validation if provided
- Operation: Lookup task, modify fields, keep existing if not provided
- Output: Updated Task object or None if not found
- Complexity: O(1)

**Delete (Remove Task)**:
- Input: task_id (int)
- Validation: ID exists
- Operation: Delete dictionary entry by ID
- Output: Boolean success indicator
- Complexity: O(1)

**Update (Toggle Completion)**:
- Input: task_id (int)
- Validation: ID exists
- Operation: Lookup task, flip `completed` boolean
- Output: Updated Task object or None if not found
- Complexity: O(1)

## Data Persistence

### Phase I: No Persistence

**Constraint**: FR-041 explicitly prohibits file or database persistence in Phase I

**Implications**:
- All data lost when application exits (FR-042)
- No save/load functionality
- No crash recovery
- Fresh state on each application launch

**User Communication**: Exit message should remind users data is not saved (though spec defines specific goodbye message)

### Future Phases: Persistence Strategy

**Phase II: File-Based Persistence**
- Serialize dictionary to JSON/CSV file
- Load on startup, save on exit (or after each operation)
- Consider atomic writes for crash safety

**Phase III: Database Persistence**
- SQLite or PostgreSQL
- Task table schema mirrors data model
- Add created_at, updated_at timestamps
- Support for concurrent users

## Performance Characteristics

### Time Complexity

| Operation | Complexity | Notes |
|-----------|------------|-------|
| Add task | O(1) | Dictionary insert + ID increment |
| Get task by ID | O(1) | Dictionary lookup |
| Get all tasks | O(n) | Iterate all values |
| Update task | O(1) | Dictionary lookup + field assignment |
| Delete task | O(1) | Dictionary deletion |
| Toggle complete | O(1) | Dictionary lookup + boolean flip |

### Space Complexity

**Per Task**: O(1) - fixed size object (5 fields)

**Total Storage**: O(n) where n = number of tasks

**Estimated Memory** (1000 tasks):
- Task object: ~200 bytes (strings + int + bool + datetime)
- Dictionary overhead: ~50 bytes per entry
- Total: ~250 KB for 1000 tasks
- Well within memory constraints

### Scalability

**Phase I Capacity**:
- Target: 1000 tasks (per SC-006)
- Expected: Can handle 10,000+ tasks without issue
- Bottleneck: View operation (O(n) formatting), not storage

**Future Scaling**:
- Phase II/III: Database enables millions of tasks
- Pagination required for large datasets
- Indexing on frequently queried fields

## Code Implementation Preview

### Task Dataclass

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique identifier (auto-assigned)
        title: Short description (1-200 chars, required)
        description: Optional detailed info (max 1000 chars)
        completed: Whether task is marked done (default False)
        created_at: Timestamp of creation (auto-generated)
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate task fields after initialization."""
        # Normalize title (strip whitespace)
        self.title = self.title.strip()

        # Validate title length
        if not self.title:
            raise ValueError("Task title cannot be empty.")
        if len(self.title) > 200:
            raise ValueError("Task title must be 200 characters or less.")

        # Truncate description if too long
        if len(self.description) > 1000:
            self.description = self.description[:1000]
```

### TaskService Class (Storage & Operations)

```python
class TaskService:
    """Manages task storage and business operations."""

    def __init__(self) -> None:
        """Initialize empty task storage."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """Create and store a new task."""
        task = Task(
            id=self._next_id,
            title=title,
            description=description
        )
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get_task(self, task_id: int) -> Task | None:
        """Retrieve task by ID, or None if not found."""
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks as a list."""
        return list(self._tasks.values())

    def update_task(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None
    ) -> Task | None:
        """Update task fields, or None if not found."""
        task = self._tasks.get(task_id)
        if task is None:
            return None

        if title is not None:
            task.title = title.strip()
            if not task.title or len(task.title) > 200:
                raise ValueError("Invalid title")

        if description is not None:
            task.description = description[:1000]  # Truncate

        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete task by ID, return True if deleted."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def toggle_complete(self, task_id: int) -> Task | None:
        """Toggle task completion status."""
        task = self._tasks.get(task_id)
        if task is None:
            return None

        task.completed = not task.completed
        return task
```

## Summary

**Data Model Simplicity**: One entity (Task) with five attributes, stored in-memory dictionary

**Key Design Principles**:
- **Validation-first**: Multiple layers ensure data integrity
- **Type-safe**: Python type hints and dataclass
- **Immutable ID**: Once assigned, never changes
- **Toggleable completion**: Can mark done/undone repeatedly
- **No persistence**: Data lost on exit (Phase I constraint)

**Performance**: All operations O(1) except viewing all tasks O(n)

**Future-ready**: Clean model enables easy addition of persistence and relationships in future phases
