---
name: price-comparison
description: Automatically compare prices across multiple e-commerce platforms (Taobao, JD, PDD, Amazon, etc.) and provide the best purchase options. When user wants to buy something, just tell the item name and get optimal price recommendations.
---

# Price Comparison Skill

A comprehensive price comparison tool that searches multiple e-commerce platforms and provides the best purchase options.

## Features

- 🔍 Multi-platform price search (Taobao, JD, PDD, Amazon, Tmall, Suning)
- 💰 Price comparison with shipping costs
- 🎟️ Coupon and discount detection
- 📊 Price history tracking
- ⭐ Seller rating consideration
- 🚚 Delivery time comparison
- 🔔 Price drop alerts

## Usage

### Basic Usage
```bash
# Compare prices for a product
price-compare "iPhone 16 Pro 256GB"

# Compare with specific platforms
price-compare "Sony WH-1000XM5" --platforms jd,tmall,amazon

# Set price alert
price-compare "Nintendo Switch" --alert 1800
```

### Python API
```python
from price_comparison import PriceComparator

comparator = PriceComparator()
results = comparator.compare("MacBook Air M3 16GB")
print(results.best_option())
```

## Supported Platforms

| Platform | Support Status | Notes |
|----------|---------------|-------|
| 京东 (JD) | ✅ Full | Price, coupon, delivery |
| 淘宝 (Taobao) | ✅ Full | Price, seller rating |
| 天猫 (Tmall) | ✅ Full | Official stores |
| 拼多多 (PDD) | ✅ Full | Group buy prices |
| 亚马逊 (Amazon) | ✅ Full | CN/US/UK/JP |
| 苏宁 (Suning) | ⚠️ Partial | Price only |
| 唯品会 (Vipshop) | 🔄 Planned | - |

## Output Format

```json
{
  "query": "iPhone 16 Pro 256GB",
  "timestamp": "2026-03-13T21:55:00+08:00",
  "results": [
    {
      "platform": "京东",
      "price": 8999,
      "original_price": 9999,
      "coupon": "满8000减500",
      "final_price": 8499,
      "seller": "Apple京东自营",
      "rating": 4.9,
      "delivery": "次日达",
      "url": "https://...",
      "recommendation_score": 95
    }
  ],
  "best_option": {
    "platform": "拼多多",
    "price": 8299,
    "reason": "最低价，百亿补贴"
  }
}
```

## Configuration

Create `~/.price-comparison/config.json`:
```json
{
  "default_platforms": ["jd", "taobao", "tmall", "pdd"],
  "timeout": 30,
  "cache_duration": 3600,
  "alert_threshold": 0.05
}
```

## Dependencies

- Python 3.8+
- requests
- beautifulsoup4
- playwright (for dynamic content)
- fake-useragent

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install playwright browsers
playwright install
```

## Notes

- Some platforms may require authentication for full access
- Rate limiting applies - be respectful to e-commerce platforms
- Prices are cached for 1 hour by default
- Affiliate links are not used - completely unbiased comparison
