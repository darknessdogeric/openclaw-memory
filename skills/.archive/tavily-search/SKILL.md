---
skill_id: "tavily-search"
title: "Tavily Search API Skill"
category: "数据/分析"
description: "## Metadata - **Name**: tavily-search - **Version**: 1.0.0 - **Author**: OpenClaw - **Description**: AI-powered web search using Tavily API"
when_to_use: ""
size_kb: 0.9
refactored: "2026-06-24"
source: "skills/tavily-search/SKILL.md"
tags:
  - skills
  - 数据/分析
---

# Tavily Search API Skill

## Metadata
- **Name**: tavily-search
- **Version**: 1.0.0
- **Author**: OpenClaw
- **Description**: AI-powered web search using Tavily API

## Requirements
- Tavily API Key

## Configuration
```yaml
# ~/.openclaw/skills/tavily-search/config.yaml
api_key: tvly-your-api-key
# Get API key from: https://tavily.com

# Optional settings
max_results: 5
search_depth: "basic"  # or "advanced"
include_answer: true
include_images: false
```

## Usage
```python
# Search web
search(query="latest hotel AI technology trends")

# Search with filters
search(query="revenue management", time_range="week", include_answer=True)

# Get Q&A answer
get_answer(question="What is the current state of AI in hospitality?")
```

## Tools
- search: Search the web with AI
- get_answer: Get direct answer to question
- search_news: Search news articles
