# Task Manager CLI

A small command-line task manager built with Python and Click. It stores tasks in `tasks.json` so your data persists between runs.

## Features

- Add tasks with a title, description, due date, and priority
- List all tasks or filter by status and priority
- Mark tasks as done
- Delete tasks
- Persist task data in JSON

## Requirements

- Python 3.11 or newer

## Setup

From the repository root:

```powershell
cd task-manager
py -3.14 -m pip install -e .[dev]
```

## Usage

Add a task:

```powershell
task add "Write report" --description "Q1 summary" --due 2026-04-01 --priority high
```

List tasks:

```powershell
task list
task list --status todo
task list --priority high
```

Mark a task as done:

```powershell
task done 1
```

Delete a task:

```powershell
task delete 1
```

## Testing

Run the test suite from the `task-manager` directory:

```powershell
py -3.14 -m pytest -q tests
```

## Data Storage

Tasks are saved in `tasks.json` in the `task-manager` directory, so they remain available between sessions.
