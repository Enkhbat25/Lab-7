"""CLI entry point for task manager."""

from __future__ import annotations

from datetime import datetime

import click

from .models import Task
from .storage import load_tasks, save_tasks


@click.group()
def main() -> None:
    """Run the task manager CLI."""
    return None


@main.command("add")
@click.argument("title")
@click.option("--description", default="", show_default=True)
@click.option("--due", "due_date", default="", show_default=True)
@click.option(
    "--priority",
    type=click.Choice(["high", "medium", "low"], case_sensitive=False),
    default="medium",
    show_default=True,
)
def add_task(title: str, description: str, due_date: str, priority: str) -> None:
    """Add a task to the list."""
    tasks = load_tasks()
    next_id = max((task.id for task in tasks), default=0) + 1
    timestamp = datetime.now()
    task = Task(
        id=next_id,
        title=title,
        description=description,
        due_date=due_date,
        priority=priority.lower(),
        status="todo",
        created_at=timestamp,
        updated_at=timestamp,
    )
    tasks.append(task)
    save_tasks(tasks)
    click.echo(f"Added task {task.id}: {task.title}")
