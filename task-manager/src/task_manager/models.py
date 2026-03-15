"""Domain models for the task manager."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

Priority = Literal["high", "medium", "low"]
Status = Literal["todo", "done"]


@dataclass
class Task:
    """Represents a single task item."""

    id: int
    title: str
    description: str
    due_date: str
    priority: Priority
    status: Status
    created_at: datetime
    updated_at: datetime
