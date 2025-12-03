# Research & Architectural Decisions: CLI Todo Application (Phase I)

**Feature**: Command-Line Todo Application (Phase I)
**Date**: 2025-12-03
**Status**: Complete

## Overview

This document captures research findings and architectural decisions made during the planning phase. Since the technical context is straightforward (Python 3.13+ CLI with in-memory storage), the research focuses on best practices for the chosen architecture and design patterns.

## Technical Stack Research

### Decision 1: Python 3.13+ with Standard Library Only

**Decision**: Use Python 3.13+ with no external dependencies

**Rationale**:
- **Simplicity**: Standard library provides all required functionality (`datetime`, `sys`, `input`, `print`)
- **Zero setup**: No pip install required, just Python runtime
- **Portability**: Works identically across Windows, macOS, Linux
- **Constitution alignment**: Minimizes complexity per Principle VI (simplicity first)
- **Specification alignment**: FR-041 explicitly prohibits external dependencies for Phase I

**Alternatives Considered**:
1. **Rich/Textual** (terminal UI libraries)
   - Rejected: Adds external dependency, unnecessary for Phase I menu-driven interface
   - Future consideration: Could enhance Phase II/III with better formatting

2. **Click/Typer** (CLI frameworks)
   - Rejected: Spec requires interactive menu, not command-line arguments
   - Would add complexity without providing value for this use case

3. **Pydantic** (data validation)
   - Rejected: Standard dataclasses + manual validation sufficient for 5 simple fields
   - Adds dependency when stdlib adequate

**Best Practices Applied**:
- Use `dataclasses` for Task model (Python 3.7+)
- Type hints on all functions and class methods
- Docstrings following Google/NumPy style
- Input validation using str methods (`strip()`, `len()`, `isdigit()`)

### Decision 2: In-Memory Storage with Dictionary

**Decision**: Store tasks in `dict[int, Task]` with int keys as task IDs

**Rationale**:
- **O(1) lookup**: Direct ID access for get/update/delete operations
- **Simple ID generation**: `max(keys) + 1` or track `next_id` counter
- **Memory efficient**: No overhead beyond task data
- **Specification mandated**: FR-039, FR-040 explicitly require in-memory dictionary

**Alternatives Considered**:
1. **List storage**
   - Rejected: O(n) lookup, would require linear search by ID
   - Less efficient for delete/update by ID operations

2. **SQLite in-memory** (`:memory:` database)
   - Rejected: FR-041 explicitly prohibits database usage in Phase I
   - Over-engineered for current requirements

3. **Global dictionary**
   - Rejected: Violates Principle III (separation of concerns)
   - Chosen approach: Encapsulate storage in TaskService class

**Implementation Details**:
```python
class TaskService:
    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1
```

## Architecture Research

### Decision 3: Three-Layer Architecture (Model-Service-CLI)

**Decision**: Strict separation into models, services, and CLI layers

**Rationale**:
- **Constitution mandated**: Principle III requires separation of concerns
- **Testability**: Each layer independently testable (Principle IV)
- **Future-proof**: Easy to add persistence layer in Phase II without modifying business logic
- **Clean contracts**: Clear interfaces between layers

**Layer Responsibilities**:

1. **Models Layer** (`src/models/task.py`)
   - Task dataclass definition
   - Field-level validation (title length, description length)
   - No business logic or I/O

2. **Services Layer** (`src/services/task_service.py`)
   - TaskService class managing task dictionary
   - CRUD operations: add, get, get_all, update, delete, toggle_complete
   - Business rules: ID auto-increment, validation enforcement
   - Returns task objects or None (no UI concerns)

3. **CLI Layer** (`src/cli/`)
   - MenuUI class: Display menu, handle user input, route to operations
   - Formatters: Table formatting, status symbols (✓/✗), separators
   - Error message display and user prompts
   - Delegates to TaskService for all business operations

**Alternatives Considered**:
1. **Single-file monolith**
   - Rejected: Violates Principle III (separation of concerns)
   - Would make testing and future evolution difficult

2. **Repository pattern**
   - Rejected: Over-engineered for in-memory storage
   - Complexity tracking would be required
   - Simple service class is sufficient

### Decision 4: Dataclass for Task Model

**Decision**: Use Python `@dataclass` for Task entity

**Rationale**:
- **Built-in**: No external dependencies
- **Automatic `__init__`, `__repr__`, `__eq__`**: Reduces boilerplate
- **Type hints integrated**: Works seamlessly with type checking
- **Immutability option**: Can use `frozen=True` if needed (not required for Phase I)
- **Default values**: Easy to specify defaults for `completed` and `created_at`

**Alternatives Considered**:
1. **NamedTuple**
   - Rejected: Immutable, but we need to support update operations
   - No built-in default factory for `created_at`

2. **Regular class with `__init__`**
   - Rejected: More boilerplate, dataclass provides same functionality
   - Dataclass is Pythonic standard for data containers

**Implementation Pattern**:
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
```

## Input Validation Research

### Decision 5: Validation Strategy

**Decision**: Two-tier validation (model-level + service-level)

**Rationale**:
- **Defense in depth**: Multiple validation points catch errors early
- **Clear error messages**: Service layer can provide context-specific messages
- **Specification compliance**: All FR-027 through FR-032 validation rules enforced

**Validation Tiers**:

1. **Model-level** (Task dataclass)
   - Basic type validation (via type hints)
   - Simple invariants (e.g., title not empty in factory method)

2. **Service-level** (TaskService methods)
   - Title length (1-200 chars): Check before creating/updating
   - Description length (max 1000 chars): Truncate or reject
   - Title not empty/whitespace: `title.strip()` check
   - ID exists: Check `id in self._tasks` before update/delete
   - ID is integer: CLI layer validates input parsing

**Best Practices Applied**:
- Fail fast: Validate at entry points before state changes
- Explicit errors: Return None or raise ValueError with clear messages
- Input sanitization: Strip whitespace from title/description inputs

## CLI Design Research

### Decision 6: Menu-Driven Interface with Numbered Options

**Decision**: Infinite loop with numbered menu (1-6), input validation, operation dispatch

**Rationale**:
- **Specification mandated**: FR-001 through FR-005 define exact menu structure
- **User-friendly**: Simple numeric selection, clear prompts
- **Error recovery**: Invalid inputs return to menu (FR-038)

**Menu Flow**:
```
1. Display welcome message (once at startup)
2. Loop:
   a. Display menu (6 options)
   b. Get user input (1-6)
   c. Validate input (numeric, in range)
   d. Route to operation handler
   e. Display results/confirmation
   f. If not Exit, return to step 2a
3. Display goodbye message
4. Clean exit (sys.exit(0))
```

**Input Handling Patterns**:
- Try/except for integer parsing (catch ValueError)
- Range validation (1-6 for menu, positive int for IDs)
- Empty input handling (allow Enter to skip in update operation)
- Confirmation prompts (y/n for delete operation)

### Decision 7: Output Formatting

**Decision**: ASCII table with aligned columns and UTF-8 symbols

**Rationale**:
- **Specification required**: FR-015 requires column alignment
- **Visual clarity**: Table structure improves readability
- **Status symbols**: ✓ and ✗ provide quick visual feedback (FR-013)
- **Cross-platform**: UTF-8 symbols supported on modern terminals

**Formatting Utilities**:
- Status formatter: `"✓ Complete" if task.completed else "✗ Pending"`
- Table formatter: Calculate column widths, pad values, add separators
- Separator lines: Use `"=" * 80` for major sections, `"-" * 80` for subsections

**Example Output Format**:
```
================================================================================
ID | Status        | Title                    | Description
================================================================================
1  | ✗ Pending     | Buy groceries            | milk, eggs, bread
2  | ✓ Complete    | Finish report            |
3  | ✗ Pending     | Call dentist             | Schedule appointment
================================================================================
```

## Error Handling Research

### Decision 8: Error Handling Strategy

**Decision**: Graceful error handling with user-friendly messages and retry capability

**Rationale**:
- **Specification mandated**: FR-033 through FR-038 define specific error messages
- **User experience**: Clear errors help users correct mistakes
- **Robustness**: Application never crashes, always returns to menu

**Error Handling Patterns**:

1. **Invalid menu selection**:
   - Catch: Non-numeric input or out-of-range number
   - Message: "Invalid choice. Please select 1-6."
   - Action: Redisplay menu

2. **Invalid task ID**:
   - Catch: Non-numeric input when expecting ID
   - Message: "Please enter a valid task ID (number)."
   - Action: Reprompt for ID

3. **Task not found**:
   - Catch: ID doesn't exist in dictionary
   - Message: "Task #{ID} not found. Use 'View All Tasks' to see available IDs."
   - Action: Return to menu

4. **Empty title**:
   - Catch: Title is empty or whitespace-only after strip
   - Message: "Task title cannot be empty."
   - Action: Reprompt for title

5. **Title too long**:
   - Catch: len(title) > 200
   - Message: "Task title must be 200 characters or less."
   - Action: Reprompt for title

6. **Description too long**:
   - Options: Truncate silently or reject with message
   - Recommendation: Truncate to 1000 chars (user-friendly)

**Implementation Pattern**:
```python
while True:
    try:
        choice = int(input("Enter choice: "))
        if 1 <= choice <= 6:
            # Route to handler
            break
        else:
            print("Invalid choice. Please select 1-6.")
    except ValueError:
        print("Invalid choice. Please select 1-6.")
```

## Performance Considerations

### Decision 9: Performance Optimization Strategy

**Decision**: Optimize for correctness first, performance adequate without optimization

**Rationale**:
- **Specification goals met**: SC-006 requires handling 1000 tasks with <2s view rendering
- **In-memory operations**: All operations O(1) or O(n) with small constant factors
- **No premature optimization**: Clean code more important than micro-optimizations

**Performance Analysis**:
- **Add task**: O(1) - dictionary insert and ID increment
- **Get task by ID**: O(1) - dictionary lookup
- **Get all tasks**: O(n) - iterate dictionary values
- **Update task**: O(1) - dictionary lookup + field assignment
- **Delete task**: O(1) - dictionary deletion
- **View all tasks**: O(n) for iteration + O(n) for formatting = O(n) total

**Expected Performance** (1000 tasks):
- Launch: <100ms (pure Python, no imports)
- Add task: <1ms
- View all tasks: <50ms (format 1000 rows)
- Update/delete: <1ms

All well within specification goals. No optimization needed for Phase I.

## Testing Strategy (Manual Acceptance Testing)

### Decision 10: Manual Testing Approach

**Decision**: Manual acceptance testing following spec scenarios (no automated tests)

**Rationale**:
- **Specification**: Tests not requested in requirements
- **Phase I scope**: Focus on core functionality delivery
- **Constitution compliance**: Testing optional per Constitution unless requested

**Test Plan** (Manual execution):

1. **User Story 1 (P1): Add and View Tasks**
   - Test Scenario 1: Add task with title and description
   - Test Scenario 2: View multiple tasks in formatted table
   - Test Scenario 3: View empty task list (empty state message)
   - Test Scenario 4: Add task with title only (no description)

2. **User Story 2 (P2): Mark Complete**
   - Test Scenario 1: Mark incomplete task as complete
   - Test Scenario 2: Mark complete task as incomplete (toggle)
   - Test Scenario 3: Attempt to mark non-existent task (error)

3. **User Story 3 (P3): Update Task**
   - Test Scenario 1: Update task title
   - Test Scenario 2: Update description only (skip title)
   - Test Scenario 3: View current details before update

4. **User Story 4 (P4): Delete Task**
   - Test Scenario 1: Delete task with confirmation (y)
   - Test Scenario 2: Cancel deletion (n)
   - Test Scenario 3: Attempt to delete non-existent task (error)

5. **Edge Cases**:
   - Invalid menu choice (7, abc)
   - Empty title
   - Title > 200 chars
   - Description > 1000 chars
   - Non-numeric task ID
   - Non-existent task ID
   - Exit and verify goodbye message

## Summary of Key Decisions

| Decision | Choice | Primary Rationale |
|----------|--------|-------------------|
| Language | Python 3.13+ | Specification requirement, standard library sufficient |
| Dependencies | None (stdlib only) | Specification constraint, simplicity |
| Storage | In-memory dict | Specification requirement, O(1) operations |
| Architecture | 3-layer (Model-Service-CLI) | Constitution Principle III (separation of concerns) |
| Task model | @dataclass | Pythonic, reduces boilerplate, type-safe |
| Validation | Two-tier (model + service) | Defense in depth, clear error messages |
| Interface | Menu-driven loop | Specification requirement |
| Formatting | ASCII table + UTF-8 symbols | Specification requirement, visual clarity |
| Error handling | Graceful with retry | Specification requirement, user-friendly |
| Testing | Manual acceptance | Tests not requested, focus on delivery |

## Future Considerations (Out of Scope for Phase I)

The following research items are deferred to future phases:

1. **Phase II: File Persistence**
   - JSON vs CSV vs custom format
   - File locking for concurrent access
   - Atomic writes for crash safety

2. **Phase III: Database Storage**
   - SQLite vs PostgreSQL vs NoSQL
   - Schema design and migrations
   - Connection pooling and performance

3. **Enhanced UI**
   - Rich/Textual for colored output
   - Pagination for large task lists
   - Sorting and filtering options

4. **Automated Testing**
   - pytest framework integration
   - Unit tests for all service methods
   - Integration tests for CLI workflows
   - Test coverage measurement

All Phase I decisions are made to facilitate these future enhancements without requiring major refactoring.
