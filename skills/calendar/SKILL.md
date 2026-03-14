# Calendar Management Skill

## Metadata
- **Name**: calendar
- **Version**: 1.0.0
- **Author**: OpenClaw
- **Description**: Calendar management and scheduling across providers

## Requirements
- Python 3.8+
- CalDAV or API access

## Configuration
```yaml
# ~/.openclaw/skills/calendar/config.yaml
google:
  client_id: your_client_id
  client_secret: your_client_secret
  
microsoft:
  client_id: your_client_id
  tenant_id: your_tenant_id
```

## Usage
```python
# List events
list_events(start_date, end_date)

# Create event
create_event(title, start_time, end_time, attendees=[])

# Check availability
check_availability(date)
```

## Tools
- list_events: List calendar events
- create_event: Create new event
- update_event: Update existing event
- delete_event: Delete event
- check_availability: Check free/busy time
