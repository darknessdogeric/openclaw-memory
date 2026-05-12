# Second Brain Knowledge Management

## Metadata
- **Name**: second-brain
- **Version**: 1.0.0
- **Author**: OpenClaw
- **Description**: Personal knowledge base for capturing and retrieving insights

## Requirements
- Local storage
- Markdown support

## Configuration
```yaml
# ~/.openclaw/skills/second-brain/config.yaml
storage_path: ~/.openclaw/knowledge
format: markdown
auto_tag: true
```

## Usage
```python
# Save knowledge
save_knowledge(content, tags=["AI", "hotel"])

# Search knowledge
search_knowledge(query="pricing strategy")

# Get related
get_related(topic="revenue management")
```

## Tools
- save_knowledge: Save new knowledge
- search_knowledge: Search knowledge base
- get_related: Get related knowledge
- summarize_notes: Summarize notes on a topic
