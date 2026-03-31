"""CLI entry point for task manager."""

from __future__ import annotations

from datetime import datetime

import click

from .models import Task
from .storage import load_tasks, save_tasks


def _find_task(tasks: list[Task], task_id: int) -> Task | None:
    """Return the task matching the given id, if it exists."""
    for task in tasks:
        if task.id == task_id:
            return task
    return None


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


@main.command("list")
@click.option(
    "--status",
    "status_filter",
    type=click.Choice(["todo", "done"], case_sensitive=False),
    default=None,
)
@click.option(
    "--priority",
    "priority_filter",
    type=click.Choice(["high", "medium", "low"], case_sensitive=False),
    default=None,
)
def list_tasks(status_filter: str | None, priority_filter: str | None) -> None:
    """List tasks with optional filters."""
    tasks = load_tasks()
    if status_filter:
        tasks = [task for task in tasks if task.status == status_filter.lower()]
    if priority_filter:
        tasks = [task for task in tasks if task.priority == priority_filter.lower()]

    if not tasks:
        click.echo("No tasks found.")
        return

    for task in tasks:
        due = f" (due {task.due_date})" if task.due_date else ""
        click.echo(
            f"{task.id}. [{task.status}] {task.title} "
            f"({task.priority}){due}"
        )


@main.command("done")
@click.argument("task_id", type=int)
def mark_done(task_id: int) -> None:
    """Mark a task as complete."""
    tasks = load_tasks()
    task = _find_task(tasks, task_id)
    if task is not None:
        task.status = "done"
        task.updated_at = datetime.now()
        save_tasks(tasks)
        click.echo(f"Marked task {task_id} as done.")
        return

    click.echo(f"Task {task_id} not found.")
    raise SystemExit(1)


@main.command("delete")
@click.argument("task_id", type=int)
def delete_task(task_id: int) -> None:
    """Delete a task from the list."""
    tasks = load_tasks()
    task = _find_task(tasks, task_id)
    if task is None:
        click.echo(f"Task {task_id} not found.")
        raise SystemExit(1)

    remaining_tasks = [saved_task for saved_task in tasks if saved_task.id != task_id]
    save_tasks(remaining_tasks)
    click.echo(f"Deleted task {task_id}: {task.title}")
