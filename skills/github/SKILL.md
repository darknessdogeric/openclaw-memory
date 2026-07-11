---
skill_id: "github"
title: "GitHub Integration Skill"
category: "开发工具"
description: "## Metadata - **Name**: github - **Version**: 1.0.0 - **Author**: OpenClaw - **Description**: GitHub repository management and API integration"
when_to_use: ""
size_kb: 0.8
refactored: "2026-06-24"
source: "skills/github/SKILL.md"
tags:
  - skills
  - 开发工具
---

# GitHub Integration Skill

## Metadata
- **Name**: github
- **Version**: 1.0.0
- **Author**: OpenClaw
- **Description**: GitHub repository management and API integration

## Requirements
- gh CLI installed
- GitHub account

## Configuration
```yaml
# ~/.openclaw/skills/github/config.yaml
token: your_github_token
username: your_username
```

## Usage
```bash
# List repositories
gh repo list

# Create repository
gh repo create name

# View repository
gh repo view owner/repo

# Search repositories
gh search repos "query"
```

## Tools
- repo_list: List repositories
- repo_view: View repository details
- repo_create: Create new repository
- repo_clone: Clone repository
- search_repos: Search GitHub repositories
- issue_list: List issues
- pr_list: List pull requests
