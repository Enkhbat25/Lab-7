"""Tests for the task done command."""

from __future__ import annotations

from click.testing import CliRunner

from task_manager.cli import main


def test_task_done_marks_complete(tasks_file) -> None:
    """Marking done updates status."""
    runner = CliRunner()
    runner.invoke(main, ["add", "Write report"])

    result = runner.invoke(main, ["done", "1"])

    assert result.exit_code == 0
    assert "Marked task 1 as done" in result.output

    list_result = runner.invoke(main, ["list", "--status", "done"])
    assert "[done] Write report" in list_result.output


def test_task_done_missing_id(tasks_file) -> None:
    """Missing task id returns error."""
    runner = CliRunner()
    result = runner.invoke(main, ["done", "99"])

    assert result.exit_code != 0
    assert "Task 99 not found" in result.output
