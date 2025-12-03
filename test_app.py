"""
Test script to verify all todo app functionality
"""

from todo_app import Task, TodoApp
from datetime import datetime


def test_task_creation():
    """Test Task class initialization."""
    print("Testing Task Creation...")
    task = Task(1, "Test Task", "Test Description")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed == False
    assert isinstance(task.created_at, datetime)
    print("[PASS] Task creation test passed")


def test_validation():
    """Test input validation."""
    print("\nTesting Validation Functions...")
    app = TodoApp()

    # Test title validation
    valid, msg = app.validate_title("")
    assert not valid
    assert "empty" in msg.lower()

    valid, msg = app.validate_title("Valid Title")
    assert valid

    valid, msg = app.validate_title("x" * 201)
    assert not valid
    assert "200" in msg

    # Test description validation
    valid, msg = app.validate_description("Valid description")
    assert valid

    valid, msg = app.validate_description("x" * 1001)
    assert not valid
    assert "1000" in msg

    print("[PASS] Validation tests passed")


def test_task_operations():
    """Test task CRUD operations."""
    print("\nTesting Task Operations...")
    app = TodoApp()

    # Test adding tasks
    assert len(app.tasks) == 0
    assert app.next_id == 1

    task1 = Task(app.next_id, "Task 1", "Description 1")
    app.tasks[app.next_id] = task1
    app.next_id += 1

    task2 = Task(app.next_id, "Task 2", "Description 2")
    app.tasks[app.next_id] = task2
    app.next_id += 1

    assert len(app.tasks) == 2
    assert app.next_id == 3

    # Test task ID validation
    valid, task_id, msg = app.validate_task_id("1")
    assert valid
    assert task_id == 1

    valid, task_id, msg = app.validate_task_id("99")
    assert not valid
    assert "not found" in msg.lower()

    valid, task_id, msg = app.validate_task_id("abc")
    assert not valid
    assert "valid" in msg.lower()

    # Test updating task
    app.tasks[1].title = "Updated Task 1"
    assert app.tasks[1].title == "Updated Task 1"

    # Test completing task
    assert app.tasks[1].completed == False
    app.tasks[1].completed = True
    assert app.tasks[1].completed == True
    app.tasks[1].completed = False
    assert app.tasks[1].completed == False

    # Test deleting task
    del app.tasks[2]
    assert len(app.tasks) == 1
    assert 2 not in app.tasks

    print("[PASS] Task operations tests passed")


def test_edge_cases():
    """Test edge cases and boundary conditions."""
    print("\nTesting Edge Cases...")
    app = TodoApp()

    # Test title with exactly 200 characters
    valid, msg = app.validate_title("x" * 200)
    assert valid

    # Test title with 201 characters
    valid, msg = app.validate_title("x" * 201)
    assert not valid

    # Test description with exactly 1000 characters
    valid, msg = app.validate_description("x" * 1000)
    assert valid

    # Test description with 1001 characters
    valid, msg = app.validate_description("x" * 1001)
    assert not valid

    # Test empty description (should be valid)
    valid, msg = app.validate_description("")
    assert valid

    # Test whitespace-only title
    valid, msg = app.validate_title("   ")
    assert not valid

    print("[PASS] Edge cases tests passed")


def run_all_tests():
    """Run all test suites."""
    print("=" * 60)
    print("RUNNING TODO APP TESTS")
    print("=" * 60)

    try:
        test_task_creation()
        test_validation()
        test_task_operations()
        test_edge_cases()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED [SUCCESS]")
        print("=" * 60)
        print("\nThe Todo App is ready to use!")
        print("Run: python todo_app.py")
        print("=" * 60)

    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        return False

    return True


if __name__ == "__main__":
    run_all_tests()
