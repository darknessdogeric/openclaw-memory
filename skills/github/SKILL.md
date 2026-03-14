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
