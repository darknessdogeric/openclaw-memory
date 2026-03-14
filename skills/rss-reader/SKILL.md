# RSS Feed Reader Skill

## Metadata
- **Name**: rss-reader
- **Version**: 1.0.0
- **Author**: OpenClaw
- **Description**: RSS/Atom feed reader and subscription manager

## Requirements
- Python feedparser (already installed)

## Configuration
```yaml
# ~/.openclaw/skills/rss-reader/config.yaml
feeds:
  - name: "Hotel News"
    url: "https://www.hotelmanagement.net/rss"
  - name: "Hospitality Net"
    url: "https://www.hospitalitynet.org/rss"
  - name: "Skift"
    url: "https://skift.com/feed"
  - name: "PhocusWire"
    url: "https://www.phocuswire.com/rss"

# Update settings
update_interval: 3600  # seconds
max_entries_per_feed: 10
```

## Usage
```python
# Read feed
read_feed(url="https://example.com/rss")

# List all feeds
list_feeds()

# Add new feed
add_feed(name="My Feed", url="https://example.com/rss")

# Search entries
search_entries(keyword="AI hotel")
```

## Tools
- read_feed: Read RSS feed entries
- list_feeds: List all subscribed feeds
- add_feed: Add new feed subscription
- remove_feed: Remove feed subscription
- search_entries: Search across all feeds
