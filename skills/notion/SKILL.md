# Notion Integration Skill

## Metadata
- **Name**: notion
- **Version**: 1.0.0
- **Author**: OpenClaw
- **Description**: Notion workspace integration for notes, databases, and wikis

## Requirements
- Notion account
- Notion Integration Token

## Configuration
```yaml
# ~/.openclaw/skills/notion/config.yaml
token: your_notion_integration_token
# Get token from: https://www.notion.so/my-integrations

default_database: "your_database_id"
```

## Usage
```python
# Query database
query_database(database_id, filter={"property": "Status", "equals": "Done"})

# Create page
create_page(parent_id, title="My Note", content="Content here")

# Update page
update_page(page_id, properties={"Status": "In Progress"})

# Search pages
search_pages(query="hotel project")
```

## Tools
- query_database: Query Notion database
- create_page: Create new page
- update_page: Update existing page
- search_pages: Search across workspace
- get_page: Get page content
