# Slack Integration Skill

## Metadata
- **Name**: slack
- **Version**: 1.0.0
- **Author**: OpenClaw
- **Description**: Slack workspace integration for messaging and notifications

## Requirements
- Slack account
- Slack Bot Token

## Configuration
```yaml
# ~/.openclaw/skills/slack/config.yaml
token: xoxb-your-bot-token
# Get token from: https://api.slack.com/apps

default_channel: "#general"
```

## Usage
```python
# Send message
send_message(channel="#general", text="Hello team!")

# Send to specific user
send_direct_message(user="@username", text="Private message")

# List channels
list_channels()

# Get channel history
get_history(channel="#general", limit=10)
```

## Tools
- send_message: Send message to channel
- send_direct_message: Send DM to user
- list_channels: List workspace channels
- get_history: Get channel message history
- upload_file: Upload file to channel
