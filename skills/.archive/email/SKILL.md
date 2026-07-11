---
skill_id: "email"
title: "Email Management Skill"
category: "行业专属"
description: "## Metadata - **Name**: email - **Version**: 1.0.0 - **Author**: OpenClaw - **Description**: Email management and automation across multiple providers"
when_to_use: ""
size_kb: 0.9
refactored: "2026-06-24"
source: "skills/email/SKILL.md"
tags:
  - skills
  - 行业专属
---

# Email Management Skill

## Metadata
- **Name**: email
- **Version**: 1.0.0
- **Author**: OpenClaw
- **Description**: Email management and automation across multiple providers

## Requirements
- Python 3.8+
- IMAP/SMTP access

## Configuration
```yaml
# ~/.openclaw/skills/email/config.yaml
imap:
  server: imap.gmail.com
  port: 993
  username: your_email@gmail.com
  password: your_app_password

smtp:
  server: smtp.gmail.com
  port: 587
  username: your_email@gmail.com
  password: your_app_password
```

## Usage
```python
# Send email
send_email(to, subject, body)

# Read inbox
read_inbox(limit=10)

# Search emails
search_emails(query="from:boss")
```

## Tools
- send_email: Send an email
- read_inbox: Read inbox messages
- search_emails: Search for emails
- reply_email: Reply to an email
- forward_email: Forward an email
