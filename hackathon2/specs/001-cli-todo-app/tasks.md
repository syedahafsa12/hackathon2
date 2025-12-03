# Tasks: Command-Line Todo Application (Phase I)

**Input**: Design documents from `/specs/001-cli-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Manual acceptance testing only (automated tests not requested in specification)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below follow single project structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create root-level project files (README.md, requirements.txt)
- [ ] T002 [P] Create src/ package structure (src/__init__.py)
- [ ] T003 [P] Create src/models/ package (src/models/__init__.py)
- [ ] T004 [P] Create src/services/ package (src/services/__init__.py)
- [ ] T005 [P] Create src/cli/ package (src/cli/__init__.py)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Task Model (Required for all user stories)

- [ ] T006 Implement Task dataclass in src/models/task.py with fields (id, title, description, completed, created_at)
- [ ] T007 Add Task validation in __post_init__ method (title strip, empty check, length validation, description truncation)
- [ ] T008 Add Task docstring documenting all fields and validation rules

### Service Layer Foundation (Required for all user stories)

- [ ] T009 Create TaskService class skeleton in src/services/task_service.py
- [ ] T010 Implement TaskService.__init__ with empty task dictionary and ID counter
- [ ] T011 Add TaskService type hints for internal storage (_tasks: dict[int, Task], _next_id: int)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add tasks with titles and descriptions, then view them in a formatted list

**Independent Test**: Launch app, add 3 tasks with varying titles/descriptions, view the list showing all tasks with proper formatting

### Implementation for User Story 1

- [ ] T012 [US1] Implement TaskService.add_task method with title/description validation and ID auto-increment
- [ ] T013 [US1] Implement TaskService.get_all_tasks method returning list of all tasks
- [ ] T014 [P] [US1] Create formatters module in src/cli/formatters.py
- [ ] T015 [P] [US1] Implement format_status function in src/cli/formatters.py (✓ Complete / ✗ Pending symbols)
- [ ] T016 [P] [US1] Implement format_task_table function in src/cli/formatters.py (ASCII table with aligned columns)
- [ ] T017 [P] [US1] Implement format_separator function in src/cli/formatters.py (separator lines)
- [ ] T018 [US1] Create MenuUI class skeleton in src/cli/menu.py with service dependency
- [ ] T019 [US1] Implement MenuUI._show_welcome method displaying welcome message
- [ ] T020 [US1] Implement MenuUI._display_menu method showing 6 numbered options
- [ ] T021 [US1] Implement MenuUI._get_menu_choice method with input validation (1-6 range, integer parsing)
- [ ] T022 [US1] Implement MenuUI._handle_add_task method with title/description prompts and validation
- [ ] T023 [US1] Implement MenuUI._handle_view_all method with table formatting and empty state message
- [ ] T024 [US1] Implement MenuUI.run main loop (welcome → menu → choice → handler → repeat until exit)
- [ ] T025 [US1] Create main.py entry point with TaskService and MenuUI initialization
- [ ] T026 [US1] Add KeyboardInterrupt handling and sys.exit(0) in main.py
- [ ] T027 [US1] Test US1 manually: Add 3 tasks, view list, verify formatting and empty state

**Checkpoint**: At this point, User Story 1 (MVP) should be fully functional and testable independently

---

## Phase 4: User Story 2 - Mark Tasks as Complete (Priority: P2)

**Goal**: Enable users to mark tasks as complete or incomplete, tracking progress visually

**Independent Test**: Add 2 tasks, mark first as complete (verify ✓ status), mark it incomplete again (verify ✗ status), attempt to mark non-existent task (verify error)

### Implementation for User Story 2

- [ ] T028 [US2] Implement TaskService.get_task method returning Task by ID or None
- [ ] T029 [US2] Implement TaskService.toggle_complete method flipping completed boolean
- [ ] T030 [US2] Implement MenuUI._handle_toggle_complete method with ID prompt, validation, and status confirmation
- [ ] T031 [US2] Integrate toggle_complete handler into MenuUI.run main loop (option 5)
- [ ] T032 [US2] Add ID validation helper method in MenuUI for integer parsing with error messages
- [ ] T033 [US2] Test US2 manually: Add 2 tasks, mark complete, mark incomplete, test non-existent ID error

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Enable users to update existing task titles and descriptions

**Independent Test**: Add task with title "Old", update to "New Title", verify change persists; update description only, verify title unchanged; press Enter to skip both fields

### Implementation for User Story 3

- [ ] T034 [US3] Implement TaskService.update_task method with optional title and description parameters
- [ ] T035 [US3] Add update validation logic (title validation if provided, keep existing if None)
- [ ] T036 [US3] Implement MenuUI._handle_update_task method with ID prompt and current details display
- [ ] T037 [US3] Add optional input handling (press Enter to keep existing values)
- [ ] T038 [US3] Integrate update handler into MenuUI.run main loop (option 3)
- [ ] T039 [US3] Test US3 manually: Update title only, update description only, skip both, test with non-existent ID

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Enable users to delete tasks permanently with confirmation

**Independent Test**: Add 3 tasks, delete task #2 with confirmation (y), verify removed; attempt delete task #4 with cancellation (n), verify not removed

### Implementation for User Story 4

- [ ] T040 [US4] Implement TaskService.delete_task method returning boolean success indicator
- [ ] T041 [US4] Implement MenuUI._handle_delete_task method with ID prompt and task details display
- [ ] T042 [US4] Add confirmation prompt (y/n) with validation loop in delete handler
- [ ] T043 [US4] Integrate delete handler into MenuUI.run main loop (option 4)
- [ ] T044 [US4] Test US4 manually: Delete with confirmation (y), cancel deletion (n), test non-existent ID error

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Exit and Polish

**Purpose**: Complete the application with exit functionality and polish

### Exit Functionality

- [ ] T045 Implement MenuUI._show_goodbye method displaying exit message
- [ ] T046 Integrate exit option (6) into MenuUI.run to break loop and show goodbye
- [ ] T047 Test exit: Verify goodbye message displays and app terminates cleanly

### Error Handling Polish

- [ ] T048 [P] Add consistent error messages across all handlers per specification (FR-033 through FR-037)
- [ ] T049 [P] Verify all input validation allows retry without crash (FR-038)
- [ ] T050 [P] Test all edge cases from spec.md (invalid menu choice, empty title, title too long, etc.)

### Documentation

- [ ] T051 [P] Write README.md with setup instructions, requirements (Python 3.13+), and usage examples
- [ ] T052 [P] Add module docstrings to all Python files (src/models/task.py, src/services/task_service.py, src/cli/menu.py, src/cli/formatters.py, src/main.py)
- [ ] T053 [P] Add function/method docstrings following Google or NumPy style
- [ ] T054 [P] Verify all type hints are present on function signatures

### Final Validation

- [ ] T055 Run manual acceptance test for all 4 user stories following spec.md acceptance scenarios
- [ ] T056 Test all 8 edge cases from spec.md edge cases section
- [ ] T057 Verify all 44 functional requirements (FR-001 through FR-044) are met
- [ ] T058 Verify all 8 success criteria (SC-001 through SC-008) are achieved
- [ ] T059 Constitution compliance check: PEP 8, type hints, docstrings, separation of concerns
- [ ] T060 Performance test: Add 1000 tasks, verify view renders in under 2 seconds (SC-006)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Exit & Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Reuses US1's view functionality but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Reuses US1's view functionality but independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Reuses US1's view functionality but independently testable

**Key Insight**: After Phase 2, all 4 user stories can be implemented in parallel by different developers since they share only the foundation (Task model and TaskService base).

### Within Each User Story

**User Story 1 (Add and View)**:
- T012 (add_task) before T022 (CLI add handler)
- T013 (get_all_tasks) before T023 (CLI view handler)
- Formatters (T014-T017) can be parallel
- MenuUI methods (T018-T024) must be sequential (build up the menu system)
- T025-T026 (main.py) after MenuUI is complete

**User Story 2 (Mark Complete)**:
- T028 (get_task) and T029 (toggle_complete) can be parallel
- T030-T032 (CLI handler) after service methods complete

**User Story 3 (Update)**:
- T034-T035 (update_task service) before T036-T038 (CLI handler)

**User Story 4 (Delete)**:
- T040 (delete_task service) before T041-T043 (CLI handler)

### Parallel Opportunities

**Setup Phase (Phase 1)**: ALL tasks can run in parallel (T002-T005 all marked [P])

**Foundational Phase (Phase 2)**:
- T006-T008 (Task model) must be sequential
- T009-T011 (TaskService base) must be sequential
- But: Task model and TaskService base can run in parallel with each other

**User Story 1**:
- T014, T015, T016, T017 (all formatters) can run in parallel

**Exit & Polish Phase**:
- T048, T049, T050 (error handling polish) can run in parallel
- T051, T052, T053, T054 (documentation) can run in parallel

**All User Stories (Phase 3-6)**: Can run in parallel once Phase 2 completes (different developers/agents)

---

## Parallel Example: User Story 1

```bash
# After Phase 2 completes, launch formatters in parallel:
Task: "Implement format_status function in src/cli/formatters.py"
Task: "Implement format_task_table function in src/cli/formatters.py"
Task: "Implement format_separator function in src/cli/formatters.py"

# These can run simultaneously since they're in different functions
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T011) - CRITICAL, blocks all stories
3. Complete Phase 3: User Story 1 (T012-T027)
4. Complete Phase 7: Exit functionality (T045-T047)
5. **STOP and VALIDATE**: Test User Story 1 independently with exit
6. Deploy/demo if ready (basic task tracker works!)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 + Exit → Test independently → Deploy/Demo (MVP! ✅)
3. Add User Story 2 → Test independently → Deploy/Demo (can now mark tasks complete)
4. Add User Story 3 → Test independently → Deploy/Demo (can now edit tasks)
5. Add User Story 4 → Test independently → Deploy/Demo (can now delete tasks)
6. Add Polish → Final testing → Deploy/Demo (production ready)

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T011)
2. Once Foundational is done:
   - Developer A: User Story 1 (T012-T027)
   - Developer B: User Story 2 (T028-T033)
   - Developer C: User Story 3 (T034-T039)
   - Developer D: User Story 4 (T040-T044)
3. Each developer tests their story independently
4. Integrate and test all stories together
5. Team completes Exit & Polish together (T045-T060)

---

## Notes

- **[P] tasks**: Different files or functions, no dependencies between them
- **[Story] label**: Maps task to specific user story for traceability
- **Each user story is independently completable and testable**
- **No automated tests**: Manual acceptance testing per spec requirements
- **Commit strategy**: Commit after each task or logical group (per user story)
- **Stop at any checkpoint**: Validate story independently before continuing
- **Avoid**: Vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Summary

**Total Tasks**: 60

**By Phase**:
- Phase 1 (Setup): 5 tasks
- Phase 2 (Foundational): 6 tasks (BLOCKING)
- Phase 3 (US1 - Add/View): 16 tasks
- Phase 4 (US2 - Mark Complete): 6 tasks
- Phase 5 (US3 - Update): 6 tasks
- Phase 6 (US4 - Delete): 5 tasks
- Phase 7 (Exit & Polish): 16 tasks

**By User Story**:
- US1: 16 tasks (includes formatters, menu system, main.py)
- US2: 6 tasks (reuses US1's infrastructure)
- US3: 6 tasks (reuses US1's infrastructure)
- US4: 5 tasks (reuses US1's infrastructure)
- Infrastructure: 11 tasks (setup + foundational)
- Polish: 16 tasks (exit, error handling, docs, validation)

**Parallel Opportunities**: 14 tasks marked [P] can run in parallel

**MVP Scope**: Phase 1 + Phase 2 + Phase 3 + Exit (T001-T027, T045-T047) = **33 tasks for MVP**

**Independent Test Criteria**:
- US1: Can add and view tasks without any other features
- US2: Can mark tasks complete independently (needs US1 for task creation)
- US3: Can update tasks independently (needs US1 for task creation)
- US4: Can delete tasks independently (needs US1 for task creation)

All tasks include exact file paths and are immediately executable by implementation agents.
