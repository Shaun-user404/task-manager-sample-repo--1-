import json
import os
import pytest
import app.tasks as tasks  



# Tests for load_tasks and save_tasks


def test_save_and_load_tasks(tmp_path, monkeypatch):
    """Checks that tasks can be successfully saved to disk and reloaded correctly."""
    file_path = tmp_path / "tasks.json"
    monkeypatch.setattr(tasks, "TASKS_FILE", str(file_path))

    sample_tasks = [{"id": 1, "title": "Test Task", "priority": 1, "tags": [], "done": False}]
    
    tasks.save_tasks(sample_tasks)
    loaded_tasks = tasks.load_tasks()

    assert loaded_tasks == sample_tasks


def test_load_tasks_file_not_exists(monkeypatch, tmp_path):
    """Checks that load_tasks returns an empty list when the tasks file does not exist."""
    non_existent_file = tmp_path / "non_existent.json"
    monkeypatch.setattr(tasks, "TASKS_FILE", str(non_existent_file))

    result = tasks.load_tasks()
    assert result == []



# Tests for add_task


def test_add_task_default_arguments():
    """Checks that a task is correctly created with default priority (1) and empty tags."""
    task_list = []
    new_task = tasks.add_task(task_list, "Learn PyTest")

    assert new_task["id"] == 1
    assert new_task["title"] == "Learn PyTest"
    assert new_task["priority"] == 1
    assert new_task["tags"] == []
    assert new_task["done"] is False
    assert len(task_list) == 1


def test_add_task_custom_arguments():
    """Checks that a task is correctly created with custom priority and tags."""
    task_list = [{"id": 1, "title": "Existing"}]
    new_task = tasks.add_task(task_list, "Deploy app", priority=3, tags=["devops", "release"])

    assert new_task["id"] == 2
    assert new_task["priority"] == 3
    assert new_task["tags"] == ["devops", "release"]
    assert task_list[-1] == new_task



# Tests for complete_task


def test_complete_task_success():
    """Checks that an existing task is marked as done and returns True."""
    task_list = [{"id": 1, "title": "Write docs", "done": False}]
    result = tasks.complete_task(task_list, 1)

    assert result is True
    assert task_list[0]["done"] is True


def test_complete_task_not_found():
    """Checks that completing a non-existent task returns False and makes no changes."""
    task_list = [{"id": 1, "title": "Write docs", "done": False}]
    result = tasks.complete_task(task_list, 99)

    assert result is False
    assert task_list[0]["done"] is False



# Tests for get_pending_tasks


def test_get_pending_tasks():
    """Checks that only tasks with 'done': False are returned."""
    task_list = [
        {"id": 1, "title": "Task 1", "done": True},
        {"id": 2, "title": "Task 2", "done": False},
        {"id": 3, "title": "Task 3", "done": False}
    ]
    pending = tasks.get_pending_tasks(task_list)

    assert len(pending) == 2
    assert pending[0]["id"] == 2
    assert pending[1]["id"] == 3



# Tests for average_priority


def test_average_priority():
    """Checks the correct calculation of the average priority across all tasks."""
    task_list = [
        {"priority": 1},
        {"priority": 3},
        {"priority": 5}
    ]
    avg = tasks.average_priority(task_list)
    assert avg == 3.0



# Tests for find_task_by_title


def test_find_task_by_title_found():
    """Checks that the correct task dictionary is returned when a matching title exists."""
    task_list = [
        {"id": 1, "title": "Buy groceries"},
        {"id": 2, "title": "Do laundry"}
    ]
    result = tasks.find_task_by_title(task_list, "Do laundry")
    assert result == {"id": 2, "title": "Do laundry"}


def test_find_task_by_title_not_found():
    """Checks that None is returned when no task matches the given title."""
    task_list = [{"id": 1, "title": "Buy groceries"}]
    result = tasks.find_task_by_title(task_list, "Clean room")
    assert result is None


# Tests for remove_task


def test_remove_task_existing():
    """Checks that the specified task is successfully removed in-place by its ID."""
    task_list = [
        {"id": 1, "title": "Task A"},
        {"id": 2, "title": "Task B"}
    ]
    tasks.remove_task(task_list, 1)
    assert task_list == [{"id": 2, "title": "Task B"}]


def test_remove_task_not_existing():
    """Checks that the task list remains unchanged if the provided task ID does not exist."""
    task_list = [{"id": 1, "title": "Task A"}]
    tasks.remove_task(task_list, 99)
    assert task_list == [{"id": 1, "title": "Task A"}]



# Tests for calculate_discount


def test_calculate_discount_premium():
    """Checks that a 20% discount is applied correctly for premium users."""
    price = 100.0
    result = tasks.calculate_discount(price, is_premium=True)
    assert result == 80.0


def test_calculate_discount_non_premium():
    """Checks that no discount is applied for non-premium users."""
    price = 100.0
    result = tasks.calculate_discount(price, is_premium=False)
    assert result == 100.0