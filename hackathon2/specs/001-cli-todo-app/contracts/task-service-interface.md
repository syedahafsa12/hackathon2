# TaskService Interface Contract

**Component**: `src/services/task_service.py`
**Consumer**: `src/cli/menu.py` (MenuUI)
**Date**: 2025-12-03

## Overview

This contract defines the interface for the TaskService class, which manages task storage and business operations. The CLI layer depends on this interface to perform all task-related operations.

## Class: TaskService

### Constructor

```python
def __init__(self) -> None
```

**Purpose**: Initialize empty task storage with auto-incrementing ID counter

**Postconditions**:
- Internal task dictionary is empty
- Next ID counter is set to 1

**Side Effects**: None (pure initialization)

---

### Method: add_task

```python
def add_task(self, title: str, description: str = "") -> Task
```

**Purpose**: Create a new task and add it to storage

**Parameters**:
- `title` (str, required): Task title, will be stripped of whitespace
- `description` (str, optional): Task description, defaults to empty string

**Returns**: `Task` object with auto-assigned ID

**Raises**:
- `ValueError`: If title is empty after strip
- `ValueError`: If title length > 200 characters after strip

**Preconditions**:
- Title must be provided (non-None)

**Postconditions**:
- New task exists in storage with unique ID
- ID counter incremented
- Task has `completed=False` and `created_at` set to current time

**Side Effects**: Modifies internal task dictionary and ID counter

**Example**:
```python
task = service.add_task("Buy groceries", "milk, eggs, bread")
# Returns: Task(id=1, title="Buy groceries", description="milk, eggs, bread", completed=False, created_at=...)
```

**Validation Rules**:
- Title is stripped: `title.strip()`
- Title cannot be empty: `title.strip() != ""`
- Title max length: 200 characters
- Description max length: 1000 characters (truncated if longer)

---

### Method: get_task

```python
def get_task(self, task_id: int) -> Task | None
```

**Purpose**: Retrieve a single task by its ID

**Parameters**:
- `task_id` (int, required): The ID of the task to retrieve

**Returns**:
- `Task` object if found
- `None` if task ID doesn't exist

**Raises**: None

**Preconditions**: None

**Postconditions**: No state changes

**Side Effects**: None (read-only operation)

**Example**:
```python
task = service.get_task(1)
if task is not None:
    print(f"Found: {task.title}")
else:
    print("Task not found")
```

---

### Method: get_all_tasks

```python
def get_all_tasks(self) -> list[Task]
```

**Purpose**: Retrieve all tasks in storage

**Parameters**: None

**Returns**: `list[Task]` containing all tasks (may be empty)

**Raises**: None

**Preconditions**: None

**Postconditions**: No state changes

**Side Effects**: None (read-only operation)

**Example**:
```python
all_tasks = service.get_all_tasks()
print(f"Total tasks: {len(all_tasks)}")
for task in all_tasks:
    print(f"- {task.title}")
```

**Note**: Order of tasks in list is not guaranteed (dictionary values are unordered). CLI layer should sort if needed.

---

### Method: update_task

```python
def update_task(
    self,
    task_id: int,
    title: str | None = None,
    description: str | None = None
) -> Task | None
```

**Purpose**: Update title and/or description of an existing task

**Parameters**:
- `task_id` (int, required): ID of task to update
- `title` (str | None, optional): New title, or None to keep existing
- `description` (str | None, optional): New description, or None to keep existing

**Returns**:
- Updated `Task` object if task found
- `None` if task ID doesn't exist

**Raises**:
- `ValueError`: If new title is empty after strip
- `ValueError`: If new title length > 200 characters

**Preconditions**:
- Task ID should exist (returns None if not)

**Postconditions**:
- If title provided: task title updated
- If description provided: task description updated
- If neither provided: no changes (but returns task)
- `id`, `completed`, `created_at` never change

**Side Effects**: Modifies task object in internal dictionary

**Example**:
```python
# Update title only
task = service.update_task(1, title="Buy groceries and supplies")

# Update description only
task = service.update_task(1, description="Updated description")

# Update both
task = service.update_task(1, title="New title", description="New desc")

# Keep existing (no update, but returns task)
task = service.update_task(1)
```

**Validation Rules**:
- Title is stripped if provided
- Title cannot be empty if provided
- Title max length: 200 characters
- Description truncated to 1000 characters if longer

---

### Method: delete_task

```python
def delete_task(self, task_id: int) -> bool
```

**Purpose**: Permanently delete a task from storage

**Parameters**:
- `task_id` (int, required): ID of task to delete

**Returns**:
- `True` if task was deleted
- `False` if task ID didn't exist

**Raises**: None

**Preconditions**: None

**Postconditions**:
- If task existed: task no longer in storage
- If task didn't exist: no changes

**Side Effects**: Removes entry from internal dictionary

**Example**:
```python
deleted = service.delete_task(1)
if deleted:
    print("Task deleted successfully")
else:
    print("Task not found")
```

**Note**: Deleted task IDs are not reused (ID counter only increments)

---

### Method: toggle_complete

```python
def toggle_complete(self, task_id: int) -> Task | None
```

**Purpose**: Toggle completion status of a task (incomplete ↔ complete)

**Parameters**:
- `task_id` (int, required): ID of task to toggle

**Returns**:
- Updated `Task` object with flipped `completed` status if task found
- `None` if task ID doesn't exist

**Raises**: None

**Preconditions**:
- Task ID should exist (returns None if not)

**Postconditions**:
- If task existed: `completed` status flipped (True → False or False → True)
- Other fields unchanged

**Side Effects**: Modifies `completed` field of task in internal dictionary

**Example**:
```python
task = service.toggle_complete(1)
if task is not None:
    status = "complete" if task.completed else "incomplete"
    print(f"Task marked as {status}")
else:
    print("Task not found")
```

---

## Error Handling Contract

### CLI Layer Responsibilities

The CLI layer (MenuUI) is responsible for:

1. **Input validation** before calling service methods:
   - Parse and validate integer task IDs
   - Handle non-numeric input
   - Validate menu choice range (1-6)

2. **Error handling** from service methods:
   - Catch `ValueError` exceptions
   - Display user-friendly error messages
   - Allow user to retry operations

3. **None handling**:
   - Check return values for None (task not found)
   - Display appropriate "task not found" messages

### Service Layer Responsibilities

The TaskService is responsible for:

1. **Business logic validation**:
   - Validate title and description constraints
   - Enforce data integrity rules
   - Raise `ValueError` for validation failures

2. **State management**:
   - Maintain task dictionary and ID counter
   - Ensure ID uniqueness
   - Prevent invalid state transitions

3. **Return values**:
   - Return None when task ID doesn't exist
   - Return actual objects when operations succeed
   - Raise exceptions only for invalid inputs, not missing IDs

---

## Usage Examples

### Complete Workflow Example

```python
from src.services.task_service import TaskService

# Initialize service
service = TaskService()

# Add tasks
task1 = service.add_task("Buy groceries", "milk, eggs, bread")
task2 = service.add_task("Finish report")
print(f"Created task {task1.id}: {task1.title}")

# View all tasks
all_tasks = service.get_all_tasks()
print(f"Total tasks: {len(all_tasks)}")

# Mark first task as complete
task = service.toggle_complete(task1.id)
print(f"Task {task.id} is now {'complete' if task.completed else 'incomplete'}")

# Update second task
task = service.update_task(task2.id, description="Q4 financial report")

# Delete a task
deleted = service.delete_task(task1.id)
print(f"Task deleted: {deleted}")

# Try to get deleted task
task = service.get_task(task1.id)
print(f"Task after deletion: {task}")  # None
```

### Error Handling Example

```python
try:
    # This will raise ValueError (empty title)
    task = service.add_task("   ")
except ValueError as e:
    print(f"Error: {e}")
    # Re-prompt user for valid title

# This returns None (task not found)
task = service.get_task(999)
if task is None:
    print("Task #999 not found. Use 'View All Tasks' to see available IDs.")
```

---

## Contract Guarantees

### Invariants

The TaskService maintains these invariants at all times:

1. **ID Uniqueness**: No two tasks have the same ID
2. **ID Monotonicity**: IDs only increase (next_id never decreases)
3. **ID Range**: All task IDs are positive integers ≥ 1
4. **Title Non-Empty**: No stored task has empty title (after strip)
5. **Title Length**: No stored task has title > 200 characters
6. **Description Length**: No stored task has description > 1000 characters

### Thread Safety

**Phase I**: TaskService is NOT thread-safe
- Assumes single-threaded CLI application
- No locking or synchronization mechanisms
- Concurrent access will cause race conditions

**Future Phases**: May require thread-safe implementation if:
- Multi-threaded server environment
- Concurrent user sessions
- Background task processing

---

## Testing Contract

### Unit Test Requirements

Each method should have tests covering:

1. **add_task**:
   - Normal case: valid title and description
   - Normal case: title only (no description)
   - Edge case: title with leading/trailing whitespace
   - Error case: empty title
   - Error case: title > 200 characters
   - Verify: ID auto-increment
   - Verify: created_at is set

2. **get_task**:
   - Normal case: existing task ID
   - Edge case: non-existent task ID (returns None)
   - Verify: returns correct task object

3. **get_all_tasks**:
   - Normal case: multiple tasks
   - Edge case: empty storage (returns empty list)
   - Verify: all tasks returned

4. **update_task**:
   - Normal case: update title only
   - Normal case: update description only
   - Normal case: update both
   - Normal case: update neither (no-op)
   - Edge case: non-existent task ID (returns None)
   - Error case: invalid new title

5. **delete_task**:
   - Normal case: existing task (returns True)
   - Edge case: non-existent task (returns False)
   - Verify: task actually removed

6. **toggle_complete**:
   - Normal case: toggle incomplete → complete
   - Normal case: toggle complete → incomplete
   - Edge case: non-existent task (returns None)
   - Verify: other fields unchanged

---

## Version History

- **v1.0** (2025-12-03): Initial interface definition for Phase I
- Future versions will maintain backward compatibility or use versioned interfaces
