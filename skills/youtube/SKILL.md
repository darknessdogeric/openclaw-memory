---
skill_id: "youtube"
title: "YouTube Video Skill"
category: "开发工具"
description: "## Metadata - **Name**: youtube - **Version**: 1.0.0 - **Author**: OpenClaw - **Description**: YouTube video download, subtitle extraction, and search"
when_to_use: ""
size_kb: 0.9
refactored: "2026-06-24"
source: "skills/youtube/SKILL.md"
tags:
  - skills
  - 开发工具
---

# YouTube Video Skill

## Metadata
- **Name**: youtube
- **Version**: 1.0.0
- **Author**: OpenClaw
- **Description**: YouTube video download, subtitle extraction, and search

## Requirements
- yt-dlp (already installed)

## Configuration
```yaml
# ~/.openclaw/skills/youtube/config.yaml
# Optional: API key for YouTube Data API
api_key: your_youtube_api_key
download_path: ~/Downloads/YouTube
format: best  # or worst, bestaudio, etc.
```

## Usage
```bash
# Download video
yt-dlp "https://youtube.com/watch?v=VIDEO_ID"

# Extract subtitles
yt-dlp --write-sub --skip-download "URL"

# Get video info
yt-dlp --dump-json "URL"

# Download audio only
yt-dlp -x --audio-format mp3 "URL"
```

## Tools
- download_video: Download YouTube video
- extract_subtitles: Extract video subtitles
- get_video_info: Get video metadata
- download_audio: Download audio only
- search_videos: Search YouTube videos
