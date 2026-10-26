import pytest
import json
import app.tasks as task_module

from app.tasks import (
    find_task_by_title,
    remove_task,
    load_tasks
)

#Test for find_task_by_title function
def test_find_task_by_title_returns_matching_task():
    tasks = [
        {"id": 1, "title": "Write report"},
        {"id": 2, "title": "Study Python"},
    ]

    result = find_task_by_title(tasks, "Study Python")

    assert result == {"id": 2, "title": "Study Python"}


def test_find_task_by_title_returns_first_match():
    tasks = [
        {"id": 1, "title": "Write report"},
        {"id": 2, "title": "Write report"},
    ]

    result = find_task_by_title(tasks, "Write report")

    assert result == {"id": 1, "title": "Write report"}


def test_find_task_by_title_returns_none_when_no_match():
    tasks = [
        {"id": 1, "title": "Write report"},
        {"id": 2, "title": "Study Python"},
    ]

    result = find_task_by_title(tasks, "Exercise")

    assert result is None


def test_find_task_by_title_returns_none_for_empty_list():
    tasks = []

    result = find_task_by_title(tasks, "Write report")

    assert result is None


def test_find_task_by_title_raises_key_error_when_title_is_missing():
    tasks = [
        {"id": 1, "name": "Write report"}
    ]

    with pytest.raises(KeyError):
        find_task_by_title(tasks, "Write report")


#Test for remove_task function
def test_remove_task_removes_task_with_matching_id():
    tasks = [
        {"id": 1, "title": "Write report"},
        {"id": 2, "title": "Study Python"},
    ]

    remove_task(tasks, 1)

    assert tasks == [{"id": 2, "title": "Study Python"}]


def test_remove_task_removes_only_the_matching_task():
    tasks = [
        {"id": 1, "title": "Task A"},
        {"id": 2, "title": "Task B"},
        {"id": 3, "title": "Task C"},
    ]

    remove_task(tasks, 2)

    assert len(tasks) == 2
    assert [task["id"] for task in tasks] == [1, 3]


def test_remove_task_does_nothing_when_id_does_not_exist():
    tasks = [
        {"id": 1, "title": "Write report"},
        {"id": 2, "title": "Study Python"},
    ]
    original_tasks = tasks.copy()

    remove_task(tasks, 99)

    assert tasks == original_tasks


def test_remove_task_handles_empty_list():
    tasks = []

    remove_task(tasks, 1)

    assert tasks == []


def test_remove_task_removes_first_match_when_ids_are_duplicated():
    tasks = [
        {"id": 1, "title": "Task A"},
        {"id": 1, "title": "Task B"},
    ]

    remove_task(tasks, 1)

    assert tasks == [{"id": 1, "title": "Task B"}]

#Test for load_tasks function
def test_load_tasks_returns_saved_tasks(tmp_path, monkeypatch):
    tasks_file = tmp_path / "tasks.json"
    expected_tasks = [
        {"id": 1, "title": "Write report", "done": False},
        {"id": 2, "title": "Study Python", "done": True},
    ]

    tasks_file.write_text(
        json.dumps(expected_tasks),
        encoding="utf-8"
    )

    monkeypatch.setattr(task_module, "TASKS_FILE", str(tasks_file))

    result = task_module.load_tasks()

    assert result == expected_tasks


def test_load_tasks_returns_empty_list_when_file_does_not_exist(
    tmp_path, monkeypatch
):
    tasks_file = tmp_path / "missing_tasks.json"
    monkeypatch.setattr(task_module, "TASKS_FILE", str(tasks_file))

    result = task_module.load_tasks()

    assert result == []


def test_load_tasks_returns_empty_list_for_empty_json_list(
    tmp_path, monkeypatch
):
    tasks_file = tmp_path / "tasks.json"
    tasks_file.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(task_module, "TASKS_FILE", str(tasks_file))

    result = task_module.load_tasks()

    assert result == []


def test_load_tasks_raises_json_decode_error_for_invalid_json(
    tmp_path, monkeypatch
):
    tasks_file = tmp_path / "tasks.json"
    tasks_file.write_text("{invalid json}", encoding="utf-8")
    monkeypatch.setattr(task_module, "TASKS_FILE", str(tasks_file))

    with pytest.raises(json.JSONDecodeError):
        task_module.load_tasks()


def test_load_tasks_preserves_task_data_types(tmp_path, monkeypatch):
    tasks_file = tmp_path / "tasks.json"
    expected_tasks = [
        {
            "id": 1,
            "title": "Write report",
            "priority": 2,
            "tags": ["school", "work"],
            "done": False,
        }
    ]

    tasks_file.write_text(
        json.dumps(expected_tasks),
        encoding="utf-8"
    )
    monkeypatch.setattr(task_module, "TASKS_FILE", str(tasks_file))

    result = task_module.load_tasks()

    assert result == expected_tasks
    assert isinstance(result[0]["id"], int)
    assert isinstance(result[0]["tags"], list)
    assert isinstance(result[0]["done"], bool)