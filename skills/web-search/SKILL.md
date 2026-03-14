# Web Search Skill

## Metadata
- **Name**: web-search
- **Version**: 1.0.0
- **Author**: OpenClaw
- **Description**: AI-powered web search using Exa API

## Requirements
- Python 3.8+
- Exa API key (optional, free tier available)

## Configuration
```yaml
# ~/.openclaw/skills/web-search/config.yaml
provider: exa
api_key: your_exa_api_key  # Optional
```

## Usage
```python
# Search web
search("AI hotel technology")

# Search with filters
search("startup funding", time_range="week")
```

## Tools
- search: Search the web
- search_news: Search news articles
- search_academic: Search academic papers
