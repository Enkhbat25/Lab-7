"""Test fixtures for the task manager."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Generator

import pytest

from task_manager import storage


@pytest.fixture()
def tasks_file(
    request: pytest.FixtureRequest,
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[Path, None, None]:
    """Provide an isolated tasks.json path and patch CLI storage calls."""
    base = Path("tests") / ".tmp"
    base.mkdir(parents=True, exist_ok=True)
    path = base / f"{request.node.name}.json"

    def _load_tasks() -> list[storage.Task]:
        return storage.load_tasks(path)

    def _save_tasks(tasks: Iterable[storage.Task]) -> None:
        storage.save_tasks(tasks, path)

    monkeypatch.setattr("task_manager.cli.load_tasks", _load_tasks)
    monkeypatch.setattr("task_manager.cli.save_tasks", _save_tasks)
    yield path
    if path.exists():
        path.unlink()
