# Feature Specification: Command-Line Todo Application (Phase I)

**Feature Branch**: `001-cli-todo-app`
**Created**: 2025-12-03
**Status**: Draft
**Input**: User description: "Build a command-line todo application (Phase I: In-Memory Python Console App)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add and View Tasks (Priority: P1)

As a user, I want to add tasks with titles and optional descriptions, then view them in a formatted list, so I can track what I need to do.

**Why this priority**: This is the core functionality - without the ability to add and view tasks, the application has no value. This represents the minimum viable product (MVP).

**Independent Test**: Can be fully tested by launching the application, adding several tasks with varying titles and descriptions, then viewing the complete list. Delivers immediate value as a basic task tracker.

**Acceptance Scenarios**:

1. **Given** the application is running and showing the main menu, **When** user selects "Add Task" and enters title "Buy groceries" with description "milk, eggs, bread", **Then** system displays "Task #1 'Buy groceries' added successfully"

2. **Given** the application has 3 tasks added, **When** user selects "View All Tasks", **Then** system displays a formatted table showing all tasks with ID, Title, Status (✗ Pending), and Description for each

3. **Given** no tasks exist in the system, **When** user selects "View All Tasks", **Then** system displays "No tasks found. Add your first task!"

4. **Given** the application is running, **When** user adds a task with only a title (no description), **Then** task is created successfully with empty description field

---

### User Story 2 - Mark Tasks as Complete (Priority: P2)

As a user, I want to mark tasks as complete or incomplete, so I can track my progress and see what I've accomplished.

**Why this priority**: After creating tasks, the most common action is marking them done. This enables the primary use case of task completion tracking.

**Independent Test**: Can be fully tested by adding a few tasks, marking some as complete, viewing the list to see status symbols change (✓ vs ✗), and toggling status back to incomplete.

**Acceptance Scenarios**:

1. **Given** a task with ID 2 exists and is marked incomplete, **When** user selects "Mark Task as Complete/Incomplete" and enters ID "2", **Then** system displays "Task #2 marked as complete" and task shows ✓ status in list view

2. **Given** a task with ID 3 exists and is marked complete, **When** user selects "Mark Task as Complete/Incomplete" and enters ID "3", **Then** system displays "Task #3 marked as incomplete" and task shows ✗ status in list view

3. **Given** user attempts to mark task ID 99 (which doesn't exist), **When** user enters "99", **Then** system displays "Task #99 not found. Use 'View All Tasks' to see available IDs." and returns to menu

---

### User Story 3 - Update Task Details (Priority: P3)

As a user, I want to update existing task titles and descriptions, so I can correct mistakes or refine task information.

**Why this priority**: While useful, editing is less common than adding and completing tasks. Users can work around this by deleting and re-adding tasks.

**Independent Test**: Can be fully tested by adding a task, then updating its title and/or description, and verifying the changes persist in the task list.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 exists with title "Buy groceries", **When** user selects "Update Task", enters ID "1", and provides new title "Buy groceries and supplies", **Then** system displays "Task #1 updated successfully" and task shows new title in list

2. **Given** a task with ID 2 exists, **When** user selects "Update Task", enters ID "2", and presses Enter to skip title (keeping existing), but updates description to "New description", **Then** only the description is updated

3. **Given** task with ID 5 exists, **When** user selects "Update Task" and enters ID "5", **Then** system displays current task details before prompting for updates

---

### User Story 4 - Delete Tasks (Priority: P4)

As a user, I want to delete tasks I no longer need, so I can keep my task list clean and relevant.

**Why this priority**: Deletion is useful but not critical for core functionality. Users can simply ignore completed or irrelevant tasks.

**Independent Test**: Can be fully tested by adding several tasks, deleting specific ones with confirmation, and verifying they're removed from the list.

**Acceptance Scenarios**:

1. **Given** a task with ID 3 exists, **When** user selects "Delete Task", enters ID "3", and confirms with "y", **Then** system displays "Task #3 deleted successfully" and task no longer appears in list

2. **Given** a task with ID 4 exists, **When** user selects "Delete Task", enters ID "4", views confirmation prompt showing task details, and enters "n", **Then** task is NOT deleted and remains in the list

3. **Given** user attempts to delete task ID 99 (which doesn't exist), **When** user enters "99", **Then** system displays "Task #99 not found. Use 'View All Tasks' to see available IDs."

---

### Edge Cases

- What happens when user enters an invalid menu choice (e.g., "7" or "abc")? System displays "Invalid choice. Please select 1-6." and shows menu again
- What happens when user enters empty title when adding a task? System displays "Task title cannot be empty." and prompts again
- What happens when user enters a title longer than 200 characters? System displays "Task title must be 200 characters or less." and prompts again
- What happens when user enters a description longer than 1000 characters? System truncates to 1000 characters or rejects with error message
- What happens when user enters non-numeric input for task ID? System displays "Please enter a valid task ID (number)." and prompts again
- What happens when user enters a task ID that doesn't exist for any operation? System displays task-not-found error message
- What happens when all tasks are deleted? System shows empty state message "No tasks found. Add your first task!"
- What happens when user exits the application? All tasks are lost (expected behavior for Phase I in-memory storage)

## Requirements *(mandatory)*

### Functional Requirements

**User Interface:**

- **FR-001**: System MUST display a welcome message when application starts
- **FR-002**: System MUST present a numbered menu with 6 options: Add Task, View All Tasks, Update Task, Delete Task, Mark Task as Complete/Incomplete, Exit
- **FR-003**: System MUST accept numeric user input (1-6) for menu selection
- **FR-004**: System MUST loop back to main menu after each operation completes until user chooses Exit
- **FR-005**: System MUST display clear, formatted output with separators (dashes or equals signs) for readability

**Task Management:**

- **FR-006**: System MUST allow users to add new tasks with a required title (1-200 characters)
- **FR-007**: System MUST allow users to add optional description (max 1000 characters) when creating tasks
- **FR-008**: System MUST auto-assign unique, auto-incrementing task IDs starting from 1
- **FR-009**: System MUST set new tasks with completion status as False (incomplete) by default
- **FR-010**: System MUST record creation timestamp (datetime) when task is created
- **FR-011**: System MUST display confirmation message after successful task creation showing task ID and title

**Task Viewing:**

- **FR-012**: System MUST display all tasks in a formatted table-like structure
- **FR-013**: System MUST show for each task: ID, Title, Status symbol (✓ Complete / ✗ Pending), and Description
- **FR-014**: System MUST display "No tasks found. Add your first task!" when no tasks exist
- **FR-015**: System MUST align columns for improved readability when displaying multiple tasks

**Task Updates:**

- **FR-016**: System MUST allow users to update task title and/or description by task ID
- **FR-017**: System MUST display current task details before prompting for updates
- **FR-018**: System MUST keep existing values unchanged if user presses Enter without input
- **FR-019**: System MUST display confirmation message after successful update

**Task Completion:**

- **FR-020**: System MUST allow users to toggle completion status by task ID
- **FR-021**: System MUST change status from incomplete (False) to complete (True) or vice versa
- **FR-022**: System MUST display confirmation showing new status after toggle

**Task Deletion:**

- **FR-023**: System MUST allow users to delete tasks by task ID
- **FR-024**: System MUST show task details and request confirmation ("Are you sure? (y/n)") before deletion
- **FR-025**: System MUST permanently remove task only if user confirms with "y"
- **FR-026**: System MUST display confirmation message after successful deletion

**Validation:**

- **FR-027**: System MUST reject empty or whitespace-only task titles
- **FR-028**: System MUST enforce task title length between 1-200 characters
- **FR-029**: System MUST enforce task description maximum length of 1000 characters
- **FR-030**: System MUST validate that task ID exists before performing update, delete, or status change operations
- **FR-031**: System MUST validate that task ID input is a valid integer
- **FR-032**: System MUST validate that menu selection is between 1-6

**Error Handling:**

- **FR-033**: System MUST display "Invalid choice. Please select 1-6." for invalid menu selections
- **FR-034**: System MUST display "Task #[ID] not found. Use 'View All Tasks' to see available IDs." when task ID doesn't exist
- **FR-035**: System MUST display "Task title cannot be empty." when user provides empty title
- **FR-036**: System MUST display "Task title must be 200 characters or less." when title exceeds limit
- **FR-037**: System MUST display "Please enter a valid task ID (number)." for non-numeric ID input
- **FR-038**: System MUST allow user to retry after any error without crashing

**Data Storage:**

- **FR-039**: System MUST store all tasks in memory during runtime
- **FR-040**: System MUST use in-memory data structure (dictionary with ID as key)
- **FR-041**: System MUST NOT persist data to files or databases (Phase I constraint)
- **FR-042**: System MUST accept that all data is lost when application exits

**Exit Behavior:**

- **FR-043**: System MUST display "Thank you for using Todo App! Goodbye!" when user selects Exit
- **FR-044**: System MUST terminate cleanly without errors when exiting

### Key Entities

- **Task**: Represents a single todo item with the following attributes:
  - **id** (integer): Unique identifier, auto-incremented starting from 1
  - **title** (string): Task name/description, required, 1-200 characters
  - **description** (string): Optional detailed information, max 1000 characters, can be empty
  - **completed** (boolean): Completion status, defaults to False (incomplete)
  - **created_at** (datetime): Timestamp when task was created, automatically set

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can launch application and see welcome message and menu within 1 second
- **SC-002**: Users can add a new task in under 30 seconds (including reading prompts and entering data)
- **SC-003**: Users can view their complete task list with clear visual distinction between complete and incomplete tasks
- **SC-004**: Users can successfully complete all 5 core operations (add, view, update, delete, mark complete) without application crashes
- **SC-005**: Users receive clear, actionable error messages for all invalid inputs, allowing them to correct and retry
- **SC-006**: Application handles at least 1000 tasks in memory without performance degradation (view list loads in under 2 seconds)
- **SC-007**: 100% of validation rules are enforced (empty titles rejected, length limits enforced, invalid IDs caught)
- **SC-008**: Users can exit application cleanly with goodbye message and zero exit code

## Assumptions *(optional)*

- Users will run application on system with Python 3.13 or higher installed
- Console/terminal supports UTF-8 encoding for displaying ✓ and ✗ symbols
- Users understand basic command-line interaction (reading menus, entering text input)
- No concurrent users - single user operates the application at a time
- Task IDs do not need to be reused after deletion (gaps in ID sequence are acceptable)
- Application runs in single session - no need to resume previous state after restart
- English language interface is sufficient (no internationalization required for Phase I)
- Console window size is at least 80 characters wide for proper table formatting

## Out of Scope *(optional)*

The following features are explicitly excluded from Phase I and may be considered for future phases:

- File persistence (saving/loading tasks from disk)
- Database storage
- Multi-user support or user authentication
- Task categories, tags, or priorities
- Task due dates or reminders
- Task search or filtering capabilities
- Sorting tasks by different criteria
- Undo/redo functionality
- Task export (CSV, JSON, etc.)
- Graphical user interface (GUI)
- Web interface
- Mobile application
- Task sharing or collaboration features
- Task history or audit trail
- Configuration file or user preferences
- Color-coded output (beyond simple symbols)
- Internationalization or localization

## Dependencies *(optional)*

**External Dependencies:**

- Python 3.13+ runtime environment
- Python standard library only (no third-party packages required)
  - `datetime` module for timestamps
  - `sys` module for clean exit
  - Built-in `input()` and `print()` for I/O

**System Dependencies:**

- Operating system: Windows, macOS, or Linux with terminal/console
- Terminal/console with UTF-8 support for special characters (✓, ✗)

**No external APIs, services, or databases required for Phase I.**
