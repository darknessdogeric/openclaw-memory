# LinkedIn Integration Skill

## Metadata
- **Name**: linkedin
- **Version**: 1.0.0
- **Author**: OpenClaw
- **Description**: LinkedIn professional networking and B2B outreach

## Requirements
- linkedin-scraper-mcp or similar tool
- LinkedIn account

## Configuration
```yaml
# ~/.openclaw/skills/linkedin/config.yaml
cookies: |
  # Paste LinkedIn cookies from Cookie-Editor
  # Format: JSON array of cookie objects
username: your_linkedin_username
password: your_linkedin_password  # Optional, cookie preferred
```

## Usage
```python
# Search profiles
search_profiles(keywords="hotel manager", location="China")

# Get profile details
get_profile(url="https://linkedin.com/in/username")

# Send connection request
send_invitation(profile_url, message="Hello, I'd like to connect")

# Search jobs
search_jobs(keywords="revenue manager", location="Shanghai")
```

## Tools
- search_profiles: Search LinkedIn profiles
- get_profile: Get detailed profile information
- send_invitation: Send connection request
- search_jobs: Search job postings
- send_message: Send direct message
