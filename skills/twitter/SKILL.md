# Twitter/X Social Media Skill

## Metadata
- **Name**: twitter
- **Version**: 1.0.0
- **Author**: OpenClaw
- **Description**: Twitter/X social media monitoring and posting

## Requirements
- xreach-cli: `npm install -g xreach-cli`
- Twitter account cookies

## Configuration
```yaml
# ~/.openclaw/skills/twitter/config.yaml
cookies: |
  [paste your cookie-editor exported cookies here]
```

## Usage
```bash
# Search tweets
xreach search "query" --json

# Read tweet
xreach tweet https://twitter.com/user/status/id --json

# Get user timeline
xreach timeline username --json
```

## Tools
- search_tweets: Search for tweets
- read_tweet: Read a specific tweet
- get_user_timeline: Get user's timeline
- get_trends: Get trending topics
