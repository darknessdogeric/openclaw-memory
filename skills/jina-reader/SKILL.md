---
skill_id: "jina-reader"
title: "Jina Reader Skill"
category: "学术/研究"
description: "## Metadata - **Name**: jina-reader - **Version**: 1.0.0 - **Author**: OpenClaw - **Description**: Read and extract content from any webpage"
when_to_use: ""
size_kb: 0.5
refactored: "2026-06-24"
source: "skills/jina-reader/SKILL.md"
tags:
  - skills
  - 学术/研究
---

# Jina Reader Skill

## Metadata
- **Name**: jina-reader
- **Version**: 1.0.0
- **Author**: OpenClaw
- **Description**: Read and extract content from any webpage

## Requirements
- Internet connection
- No API key required

## Usage
```bash
# Read webpage
curl https://r.jina.ai/http://example.com

# Read with options
curl https://r.jina.ai/http://example.com?format=text
```

## Tools
- read_url: Read webpage content
- extract_text: Extract text from HTML
- summarize_page: Summarize webpage content
