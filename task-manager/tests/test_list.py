"""Tests for the task list command."""

from __future__ import annotations

import re

from click.testing import CliRunner

from task_manager.cli import main


def test_task_list_outputs_tasks(tasks_file) -> None:
    """Listing tasks shows saved entries."""
    runner = CliRunner()
    runner.invoke(main, ["add", "Write report", "--priority", "high"])
    runner.invoke(main, ["add", "Plan meeting", "--priority", "low"])

    result = runner.invoke(main, ["list"])

    assert result.exit_code == 0
    assert "1. [todo] Write report" in result.output
    assert "2. [todo] Plan meeting" in result.output


def test_task_list_filters(tasks_file) -> None:
    """Listing can filter by priority."""
    runner = CliRunner()
    runner.invoke(main, ["add", "Write report", "--priority", "high"])
    runner.invoke(main, ["add", "Plan meeting", "--priority", "low"])

    result = runner.invoke(main, ["list", "--priority", "high"])

    assert result.exit_code == 0
    assert "Write report" in result.output
    assert re.search(r"Plan meeting", result.output) is None
