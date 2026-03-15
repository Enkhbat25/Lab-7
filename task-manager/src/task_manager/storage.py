"""JSON storage utilities for tasks."""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable

from .models import Task

TASKS_FILE = Path("tasks.json")


def _serialize_task(task: Task) -> dict:
    """Convert a Task to a JSON-serializable dict."""
    data = asdict(task)
    data["created_at"] = task.created_at.isoformat()
    data["updated_at"] = task.updated_at.isoformat()
    return data


def _deserialize_task(data: dict) -> Task:
    """Convert a dict into a Task instance."""
    return Task(
        id=int(data["id"]),
        title=str(data["title"]),
        description=str(data.get("description", "")),
        due_date=str(data.get("due_date", "")),
        priority=str(data.get("priority", "medium")),
        status=str(data.get("status", "todo")),
        created_at=datetime.fromisoformat(data["created_at"]),
        updated_at=datetime.fromisoformat(data["updated_at"]),
    )


def load_tasks(path: Path = TASKS_FILE) -> list[Task]:
    """Load tasks from a JSON file."""
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    tasks = payload.get("tasks", [])
    return [_deserialize_task(task) for task in tasks]


def save_tasks(tasks: Iterable[Task], path: Path = TASKS_FILE) -> None:
    """Save tasks to a JSON file."""
    payload = {"tasks": [_serialize_task(task) for task in tasks]}
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
