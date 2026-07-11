---
skill_id: "task-manager"
title: "Task Manager Skill"
category: "AI/ML"
description: "## Metadata - **Name**: task-manager - **Version**: 1.0.0 - **Author**: OpenClaw - **Description**: Personal task and project management"
when_to_use: ""
size_kb: 1.0
refactored: "2026-06-24"
source: "skills/task-manager/SKILL.md"
tags:
  - skills
  - AI/ML
---

# Task Manager Skill

## Metadata
- **Name**: task-manager
- **Version**: 1.0.0
- **Author**: OpenClaw
- **Description**: Personal task and project management

## Requirements
- Local storage

## Configuration
```yaml
# ~/.openclaw/skills/task-manager/config.yaml
storage_path: ~/.openclaw/tasks
default_priority: medium
auto_archive_completed: true
archive_after_days: 30
```

## Usage
```python
# Add task
add_task(title="Review HAL proposal", priority="high", due_date="2026-03-01")

# List tasks
list_tasks(status="pending", priority="high")

# Complete task
complete_task(task_id="task_001")

# Project management
create_project(name="HAL Development", description="AI hotel platform")
add_task_to_project(project_id="proj_001", task_id="task_001")
```

## Tools
- add_task: Create new task
- list_tasks: List all tasks
- complete_task: Mark task as complete
- delete_task: Delete task
- create_project: Create project
- get_project_tasks: Get all tasks in project
