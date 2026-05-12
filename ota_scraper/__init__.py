# -*- coding: utf-8 -*-
"""
OTA-Scraper Framework v1.0
攻破所有OTA和OTP网站的数据和信息抓取系统

支持的平台:
  国内: 携程/艺龙/去哪儿/同程/美团/飞猪/马蜂窝/驴妈妈
  国际: Agoda/Booking/Expedia/TripAdvisor/Hotels.com/Airbnb

核心能力:
  - 四层后端策略 (API → Scrapling stealth → Playwright → Obscura)
  - 平台专属CSS选择器库
  - 自动降级与重试
  - 数据标准化Pipeline
  - 缓存与速率限制
  - 持续迭代的配置驱动架构
"""
from .scraper import OTAScraper, scrape_ota
from .core import OTAResult, OTAHotel, OTAReview, OTAPrice

__version__ = "1.0.0"
__all__ = ["OTAScraper", "scrape_ota", "OTAResult", "OTAHotel", "OTAReview", "OTAPrice"]
