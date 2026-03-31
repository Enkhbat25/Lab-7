"""Tests for the task delete command."""

from __future__ import annotations

import json

from click.testing import CliRunner

from task_manager.cli import main


def test_task_delete_removes_task(tasks_file) -> None:
    """Deleting a task removes it from persisted storage."""
    runner = CliRunner()
    runner.invoke(main, ["add", "Write report"])
    runner.invoke(main, ["add", "Plan meeting"])

    result = runner.invoke(main, ["delete", "1"])

    assert result.exit_code == 0
    assert "Deleted task 1: Write report" in result.output

    payload = json.loads(tasks_file.read_text(encoding="utf-8"))
    tasks = payload.get("tasks", [])
    assert len(tasks) == 1
    assert tasks[0]["id"] == 2
    assert tasks[0]["title"] == "Plan meeting"


def test_task_delete_updates_list_output(tasks_file) -> None:
    """Deleted tasks no longer appear in list results."""
    runner = CliRunner()
    runner.invoke(main, ["add", "Write report"])
    runner.invoke(main, ["add", "Plan meeting"])

    runner.invoke(main, ["delete", "1"])
    result = runner.invoke(main, ["list"])

    assert result.exit_code == 0
    assert "Write report" not in result.output
    assert "2. [todo] Plan meeting" in result.output


def test_task_delete_missing_id(tasks_file) -> None:
    """Deleting a missing task id returns an error."""
    runner = CliRunner()

    result = runner.invoke(main, ["delete", "99"])

    assert result.exit_code != 0
    assert "Task 99 not found." in result.output
