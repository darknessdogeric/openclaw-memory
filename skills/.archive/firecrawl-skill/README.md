# Firecrawl - OpenClaw Skill

Web scraping and crawling with Firecrawl API. Fetch webpage content as markdown, take screenshots, extract structured data, search the web, and crawl documentation sites.

## Features

- 📄 **Markdown Conversion** - Clean markdown from any webpage
- 📸 **Screenshots** - Full-page captures of any URL
- 🔍 **Structured Extraction** - Pull specific data using JSON schemas
- 🌐 **Web Search** - Search and scrape results
- 🕷️ **Documentation Crawling** - Crawl entire doc sites
- 🗺️ **Site Mapping** - Discover all URLs on a website

## Quick Start

### 1. Get Your API Key

Get your API key from [Firecrawl](https://www.firecrawl.dev/app/api-keys)

### 2. Install SDK

```bash
pip3 install firecrawl
```

### 3. Set Environment Variable

```bash
export FIRECRAWL_API_KEY=fc-your-key-here
# Or add to ~/.env
echo "FIRECRAWL_API_KEY=fc-your-key" >> ~/.env
```

### 4. Installation

```bash
# Via ClawHub (once published)
clawdhub install firecrawl

# Via GitHub
git clone https://github.com/capt-marbles/firecrawl ~/.openclaw/skills/firecrawl
```

## Usage Examples

### Get Page as Markdown

```bash
# Fetch any URL as clean markdown
python3 fc.py markdown "https://blog.example.com/post"

# Skip nav/footer
python3 fc.py markdown "https://example.com" --main-only
```

### Take Screenshots

```bash
# Full-page screenshot
python3 fc.py screenshot "https://example.com" -o screenshot.png
```

### Extract Structured Data

Create a schema file:
```json
{
  "type": "object",
  "properties": {
    "title": { "type": "string" },
    "price": { "type": "number" },
    "features": { "type": "array", "items": { "type": "string" } }
  }
}
```

Extract data:
```bash
python3 fc.py extract "https://example.com/product" --schema schema.json
```

### Web Search

```bash
# Search the web and get content
python3 fc.py search "Python 3.13 new features" --limit 5
```

### Crawl Documentation

```bash
# Crawl entire doc site
python3 fc.py crawl "https://docs.example.com" --limit 30

# Save to directory
python3 fc.py crawl "https://docs.example.com" --output ./docs
```

### Map Site URLs

```bash
# Discover all URLs
python3 fc.py map "https://example.com" --limit 100

# Search within URLs
python3 fc.py map "https://example.com" --search "api"
```

## Use Cases

Perfect for:
- 📚 **Content Research** - Scrape articles and blog posts
- 🛍️ **Price Monitoring** - Track product prices
- 📊 **Data Extraction** - Pull structured data from websites
- 🤖 **LLM Training** - Gather documentation for RAG
- 🔍 **Competitive Analysis** - Monitor competitor websites
- 📸 **Website Monitoring** - Capture page screenshots

## Pricing

- **Free Tier**: 500 credits included
- **Cost**: 1 credit = 1 page/screenshot/search query
- Set reasonable limits to avoid burning credits

## Commands Reference

| Command | Description | Credits |
|---------|-------------|---------|
| `markdown <url>` | Fetch page as markdown | 1 per page |
| `screenshot <url>` | Take full-page screenshot | 1 per page |
| `extract <url>` | Extract structured data | 1 per page |
| `search <query>` | Search and scrape results | 1 per result |
| `crawl <url>` | Crawl entire site | 1 per page |
| `map <url>` | Discover site URLs | 1 per 100 URLs |

## Requirements

- Python 3.6+
- Firecrawl API key
- `firecrawl` Python SDK

## Documentation

See [SKILL.md](SKILL.md) for complete documentation.

## License

MIT

## Author

captmarbles