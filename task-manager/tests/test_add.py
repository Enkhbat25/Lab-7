"""Tests for the task add command."""

from __future__ import annotations

import json

from click.testing import CliRunner

from task_manager.cli import main


def test_task_add_creates_task(tasks_file) -> None:
    """Adding a task persists it to storage."""
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "add",
            "Write report",
            "--description",
            "Q1 summary",
            "--due",
            "2026-04-01",
            "--priority",
            "high",
        ],
    )

    assert result.exit_code == 0
    assert "Added task 1" in result.output

    payload = json.loads(tasks_file.read_text(encoding="utf-8"))
    tasks = payload.get("tasks", [])
    assert len(tasks) == 1
    task = tasks[0]
    assert task["title"] == "Write report"
    assert task["description"] == "Q1 summary"
    assert task["due_date"] == "2026-04-01"
    assert task["priority"] == "high"
    assert task["status"] == "todo"
    assert task["id"] == 1
    assert task["created_at"]
    assert task["updated_at"]
