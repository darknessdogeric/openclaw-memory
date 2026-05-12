# -*- coding: utf-8 -*-
"""
OTA平台配置文件
每个平台定义: 基本信息 + 抓取策略 + CSS选择器 + 特殊处理逻辑

设计原则:
  1. 配置驱动 - 改变策略无需改代码
  2. 降级链 - 每个平台有多个备选后端
  3. 选择器版本化 - 网站改版时只需更新配置
"""
from typing import Optional

# 策略枚举
STRATEGY_SCRAPLING = "scrapling"   # Scrapling StealthyFetcher (主力)
STRATEGY_PLAYWRIGHT = "playwright" # Playwright 浏览器
STRATEGY_CLI = "scrapling_cli"     # Scrapling CLI
STRATEGY_DIRECT = "direct"         # 直接HTTP

# 反爬难度分级
LEVEL_EASY = 1
LEVEL_MODERATE = 2
LEVEL_HARD = 3
LEVEL_EXTREME = 4
LEVEL_IMPOSSIBLE = 5

PLATFORMS = {}

# ═══════════════════════════════════════════════════════════════
# 国内OTA
# ═══════════════════════════════════════════════════════════════

PLATFORMS["ctrip"] = {
    "name": "携程",
    "domains": ["ctrip.com", "trip.com"],
    "base_url": "https://hotels.ctrip.com",
    "search_url": "https://m.ctrip.com/webapp/hotel/{city}1/",
    "mobile_url": "https://m.ctrip.com/html5/hotel/",
    "anti_bot_level": LEVEL_EXTREME,
    "description": "携程系核心平台，使用Akamai+自研WAF",

    "backends": [
        {"type": STRATEGY_SCRAPLING, "priority": 1, "wait_ms": 5000},
        {"type": STRATEGY_PLAYWRIGHT, "priority": 2, "wait_ms": 8000, "scroll": True},
        {"type": STRATEGY_CLI, "priority": 3, "wait_ms": 6000},
    ],

    "selectors": {
        "hotel_list": "div.card-item-wrap",
        "hotel_name": "div.list-card-title",
        "hotel_price": "span.real-price, .price-display, [class*=price]",
        "hotel_score": "span.score, [class*=score], [class*=rating]",
        "hotel_reviews": "span.review-count, [class*=comment], [class*=review]",
        "hotel_address": "span.address, [class*=address], [class*=position]",
        "hotel_image": "img.hotel-img, .list-avatar-wrap img",
        "next_page": "a.next, .pagination .next:not(.disabled)",
        "detail_name": "h1.hotel-name, .hotel-info .cn",
        "detail_price": ".room-list .price, .hotel-room-price, .real-price",
    },

    "rate_limit": {"delay_seconds": 5, "max_per_minute": 8, "max_retries": 3, "retry_delay": 30},
    "normalize": {"price_selector_type": "text", "score_scale": 5.0, "currency": "CNY"},
    "notes": "Akamai Bot Manager + 动态加载 + 价格JS渲染。优先StealthyFetcher",
}

PLATFORMS["elong"] = {
    "name": "艺龙",
    "domains": ["elong.com"],
    "base_url": "https://hotel.elong.com",
    "search_url": "https://hotel.elong.com/search/{city}/",
    "anti_bot_level": LEVEL_HARD,
    "description": "携程旗下，反爬策略与携程类似但稍弱",

    "backends": [
        {"type": STRATEGY_SCRAPLING, "priority": 1, "wait_ms": 4000},
        {"type": STRATEGY_CLI, "priority": 2},
    ],
    "selectors": {
        "hotel_list": "div.hotel_list > li, div.hotelItem",
        "hotel_name": "h3.hotelName a, .hotel-info .name",
        "hotel_price": "span.price_num, .hotel-price em",
        "hotel_score": "span.comment-score, .rating",
        "hotel_reviews": "span.comment-count, .judge-count",
        "hotel_address": ".hotel-address, .address",
        "hotel_image": "img.hotel-img, .hotel-pic img",
        "next_page": "a.next, .pager .next",
        "detail_name": "h1.hotel-name",
        "detail_price": ".room-price em, .price .num",
    },
    "rate_limit": {"delay_seconds": 3, "max_per_minute": 12, "max_retries": 3, "retry_delay": 20},
    "normalize": {"score_scale": 5.0, "currency": "CNY"},
}

PLATFORMS["qunar"] = {
    "name": "去哪儿",
    "domains": ["qunar.com"],
    "base_url": "https://hotel.qunar.com",
    "search_url": "https://hotel.qunar.com/city/{city}/",
    "anti_bot_level": LEVEL_HARD,
    "description": "携程旗下，独立技术栈",

    "backends": [
        {"type": STRATEGY_SCRAPLING, "priority": 1, "wait_ms": 5000},
        {"type": STRATEGY_PLAYWRIGHT, "priority": 2, "wait_ms": 6000, "scroll": True},
    ],
    "selectors": {
        "hotel_list": "div.hotel-list > div, li.hotel-item",
        "hotel_name": "a.hotel-name, .hotel-title a",
        "hotel_price": "span.price-num, .price em",
        "hotel_score": "span.score-num, .comment-score",
        "hotel_reviews": "span.review-count, .judge-num",
        "hotel_address": ".address, .hotel-position",
        "hotel_image": "img.hotel-pic, .pic-wrap img",
        "next_page": "a.next, .pager-next",
        "detail_name": "h1.hotel-name",
        "detail_price": ".room-item .price, .room-price em",
    },
    "rate_limit": {"delay_seconds": 4, "max_per_minute": 10, "max_retries": 3, "retry_delay": 25},
    "normalize": {"score_scale": 5.0, "currency": "CNY"},
}

PLATFORMS["tongcheng"] = {
    "name": "同程旅行",
    "domains": ["ly.com", "17u.cn", "tongcheng.com"],
    "base_url": "https://www.ly.com",
    "search_url": "https://www.ly.com/hotel/{city}/",
    "anti_bot_level": LEVEL_HARD,
    "description": "独立OTA，微信生态强势",

    "backends": [
        {"type": STRATEGY_SCRAPLING, "priority": 1, "wait_ms": 4000},
        {"type": STRATEGY_PLAYWRIGHT, "priority": 2, "wait_ms": 6000},
    ],
    "selectors": {
        "hotel_list": "div.hotel-list-item, li.hotel-item",
        "hotel_name": "a.hotel-title, .hotel-name a",
        "hotel_price": "span.price, .price-info em",
        "hotel_score": "span.score, .comment-score",
        "hotel_reviews": "span.comment-num, .review-count",
        "hotel_address": ".hotel-addr, .address-info",
        "hotel_image": "img.hotel-img, .hotel-cover img",
        "next_page": "a.next, .pagination .next",
        "detail_name": "h1.hotel-title",
        "detail_price": ".room-price .num, .price em",
    },
    "rate_limit": {"delay_seconds": 4, "max_per_minute": 8, "max_retries": 3, "retry_delay": 30},
    "normalize": {"score_scale": 5.0, "currency": "CNY"},
}

PLATFORMS["meituan"] = {
    "name": "美团酒店",
    "domains": ["meituan.com", "dianping.com"],
    "base_url": "https://hotel.meituan.com",
    "search_url": "https://hotel.meituan.com/{city}/",
    "anti_bot_level": LEVEL_EXTREME,
    "description": "反爬最严格的国内平台，自研WAF+行为分析+设备指纹",

    "backends": [
        {"type": STRATEGY_SCRAPLING, "priority": 1, "wait_ms": 8000},
        {"type": STRATEGY_PLAYWRIGHT, "priority": 2, "wait_ms": 10000, "scroll": True,
         "geolocation": {"latitude": 39.9042, "longitude": 116.4074}},
    ],
    "selectors": {
        "hotel_list": "div.hotel-list-item, div.poi-item",
        "hotel_name": "a.hotel-name, .poi-name h3",
        "hotel_price": "span.price-num, .price strong",
        "hotel_score": "span.score-wraper, .comment-score",
        "hotel_reviews": "span.review-num, .comment-num",
        "hotel_address": ".address, .poi-addr",
        "hotel_image": "img.poi-pic, .hotel-img img",
        "next_page": "a.next, .pagination-next:not(.disabled)",
        "detail_name": "h1.hotel-title",
        "detail_price": ".room-price .num, .price strong",
    },
    "rate_limit": {"delay_seconds": 8, "max_per_minute": 5, "max_retries": 2, "retry_delay": 60},
    "normalize": {"score_scale": 5.0, "currency": "CNY"},
    "notes": "价格图片渲染(需OCR) + 登录态强制 + 滑块验证码",
}

PLATFORMS["fliggy"] = {
    "name": "飞猪",
    "domains": ["fliggy.com", "alitrip.com"],
    "base_url": "https://www.fliggy.com",
    "search_url": "https://hotel.fliggy.com/search/{city}/",
    "anti_bot_level": LEVEL_EXTREME,
    "description": "阿里系，淘宝技术栈，反爬与淘宝同级别",

    "backends": [
        {"type": STRATEGY_SCRAPLING, "priority": 1, "wait_ms": 6000},
        {"type": STRATEGY_PLAYWRIGHT, "priority": 2, "wait_ms": 10000, "scroll": True},
        {"type": STRATEGY_CLI, "priority": 3, "wait_ms": 8000},
    ],
    "selectors": {
        "hotel_list": "div.hotel-list-item, .hotel-item",
        "hotel_name": "a.hotel-name, .hotel-title span",
        "hotel_price": "span.price-num, .price em",
        "hotel_score": "span.score-num, .rating-value",
        "hotel_reviews": "span.review-num, .comment-count",
        "hotel_address": ".hotel-addr, .address",
        "hotel_image": "img.hotel-pic, .pic-box img",
        "next_page": "a.next, .pagination-next",
        "detail_name": "h1.hotel-name",
        "detail_price": ".room-price .num, .price strong",
    },
    "rate_limit": {"delay_seconds": 6, "max_per_minute": 6, "max_retries": 2, "retry_delay": 45},
    "normalize": {"score_scale": 5.0, "currency": "CNY"},
}

PLATFORMS["mafengwo"] = {
    "name": "马蜂窝",
    "domains": ["mafengwo.cn"],
    "base_url": "https://www.mafengwo.cn",
    "search_url": "https://www.mafengwo.cn/hotel/{city}/",
    "anti_bot_level": LEVEL_MODERATE,
    "description": "内容社区+OTA，反爬中等",

    "backends": [
        {"type": STRATEGY_SCRAPLING, "priority": 1, "wait_ms": 2000},
        {"type": STRATEGY_DIRECT, "priority": 2},
    ],
    "selectors": {
        "hotel_list": "div.hotel-list > li, div.hotel-item",
        "hotel_name": "a.hotel-title, .hotel-name",
        "hotel_price": "span.price, .price-num",
        "hotel_score": "span.score, .comment-grade",
        "hotel_reviews": "span.review-num, .comment-count",
        "hotel_address": ".address, .hotel-location",
        "hotel_image": "img.hotel-cover, .hotel-img img",
        "next_page": "a.next, .page-next",
        "detail_name": "h1.hotel-name",
        "detail_price": ".room-price em, .price-info .num",
    },
    "rate_limit": {"delay_seconds": 2, "max_per_minute": 20, "max_retries": 3, "retry_delay": 10},
    "normalize": {"score_scale": 5.0, "currency": "CNY"},
}

PLATFORMS["lvmama"] = {
    "name": "驴妈妈",
    "domains": ["lvmama.com"],
    "base_url": "https://www.lvmama.com",
    "search_url": "https://hotel.lvmama.com/search-{city}.html",
    "anti_bot_level": LEVEL_MODERATE,
    "description": "中型OTA，周边游/景区门票为主",

    "backends": [
        {"type": STRATEGY_SCRAPLING, "priority": 1, "wait_ms": 2000},
        {"type": STRATEGY_DIRECT, "priority": 2},
    ],
    "selectors": {
        "hotel_list": "div.hotel-list-item, li.hotel-item",
        "hotel_name": "a.hotel-name, .product-name h3",
        "hotel_price": "span.price, .product-price em",
        "hotel_score": "span.score, .satisfaction",
        "hotel_reviews": "span.comment-num, .dp-count",
        "hotel_address": ".address, .hotel-addr",
        "hotel_image": "img.hotel-img, .product-pic img",
        "next_page": "a.next, .page-next",
        "detail_name": "h1.product-name",
        "detail_price": ".price-num em, .real-price",
    },
    "rate_limit": {"delay_seconds": 2, "max_per_minute": 20, "max_retries": 3, "retry_delay": 10},
    "normalize": {"score_scale": 5.0, "currency": "CNY"},
}

# ═══════════════════════════════════════════════════════════════
# 国际OTA
# ═══════════════════════════════════════════════════════════════

PLATFORMS["agoda"] = {
    "name": "Agoda",
    "domains": ["agoda.com", "agoda.cn"],
    "base_url": "https://www.agoda.com",
    "search_url": "https://www.agoda.com/search?city={city}",
    "anti_bot_level": LEVEL_HARD,
    "description": "Booking Holdings旗下，亚洲市场强势",

    "backends": [
        {"type": STRATEGY_SCRAPLING, "priority": 1, "wait_ms": 4000},
        {"type": STRATEGY_PLAYWRIGHT, "priority": 2, "wait_ms": 5000},
    ],
    "selectors": {
        "hotel_list": "li.PropertyCard, div[data-element-name='property-card']",
        "hotel_name": "h3.PropertyCard__HotelName, [data-selenium='hotel-name']",
        "hotel_price": "span.PropertyCard__Price, [data-selenium='display-price']",
        "hotel_score": "span.ReviewScore, [data-selenium='review-score']",
        "hotel_reviews": "span.ReviewCount, [data-selenium='review-count']",
        "hotel_address": "span.PropertyCard__Address, .hotel-address",
        "hotel_image": "img.PropertyCard__Image, .hotel-image img",
        "next_page": "a.next, button[aria-label='Next']",
        "detail_name": "h1.PropertyHeader, [data-selenium='hotel-header-name']",
        "detail_price": "[data-selenium='room-price'], .room-price",
    },
    "rate_limit": {"delay_seconds": 3, "max_per_minute": 15, "max_retries": 3, "retry_delay": 20},
    "normalize": {"score_scale": 10.0, "currency": "CNY"},
}

PLATFORMS["booking"] = {
    "name": "Booking.com",
    "domains": ["booking.com"],
    "base_url": "https://www.booking.com",
    "search_url": "https://www.booking.com/searchresults.html?ss={city}",
    "anti_bot_level": LEVEL_EXTREME,
    "description": "全球最大OTA，Akamai+自研多层防护",

    "backends": [
        {"type": STRATEGY_SCRAPLING, "priority": 1, "wait_ms": 8000},
        {"type": STRATEGY_PLAYWRIGHT, "priority": 2, "wait_ms": 10000, "scroll": True},
    ],
    "selectors": {
        "hotel_list": "div[data-testid='property-card']",
        "hotel_name": "[data-testid='title']",
        "hotel_price": "[data-testid='price-and-discounted-price']",
        "hotel_score": "[data-testid='review-score']",
        "hotel_reviews": "[data-testid='review-score'], [data-testid='review-score-link']",
        "hotel_address": "[data-testid='address-link']",
        "hotel_distance": "[data-testid='distance']",
        "hotel_image": "[data-testid='image'] img",
        "next_page": "button[aria-label='Next page']",
        "detail_name": "[data-testid='hotel-header-name']",
        "detail_price": "[data-testid='room-price']",
    },
    "rate_limit": {"delay_seconds": 8, "max_per_minute": 5, "max_retries": 2, "retry_delay": 60},
    "normalize": {"score_scale": 10.0, "currency": "CNY"},
    "notes": "data-testid属性经2026-05-11实调校准，选择器已验证25/25提取成功",
}

PLATFORMS["expedia"] = {
    "name": "Expedia",
    "domains": ["expedia.com", "expedia.cn", "hotels.com"],
    "base_url": "https://www.expedia.com",
    "search_url": "https://www.expedia.com/Hotel-Search?destination={city}",
    "anti_bot_level": LEVEL_HARD,
    "description": "全球第二大OTA集团",

    "backends": [
        {"type": STRATEGY_SCRAPLING, "priority": 1, "wait_ms": 5000},
        {"type": STRATEGY_PLAYWRIGHT, "priority": 2, "wait_ms": 8000, "scroll": True},
    ],
    "selectors": {
        "hotel_list": "li[data-stid='property-listing'], div.uitk-card",
        "hotel_name": "h2[data-stid='property-name'], .uitk-heading",
        "hotel_price": "span[data-stid='price'], .uitk-text-emphasis",
        "hotel_score": "span[data-stid='review-score'], .review-score",
        "hotel_reviews": "span[data-stid='review-count'], .review-count",
        "hotel_address": "span[data-stid='address'], .hotel-address",
        "hotel_image": "img[data-stid='image'], .hotel-image img",
        "next_page": "button[data-stid='next'], .pagination-next",
        "detail_name": "h1[data-stid='hotel-name'], .property-name",
        "detail_price": "[data-stid='room-price'], .room-price",
    },
    "rate_limit": {"delay_seconds": 5, "max_per_minute": 8, "max_retries": 3, "retry_delay": 30},
    "normalize": {"score_scale": 10.0, "currency": "CNY"},
}

PLATFORMS["tripadvisor"] = {
    "name": "TripAdvisor",
    "domains": ["tripadvisor.com", "tripadvisor.cn"],
    "base_url": "https://www.tripadvisor.com",
    "search_url": "https://www.tripadvisor.com/Hotels-g{city_id}-{city}-Hotels.html",
    "anti_bot_level": LEVEL_MODERATE,
    "description": "全球最大旅游评论网站，内容数据相对开放",

    "backends": [
        {"type": STRATEGY_SCRAPLING, "priority": 1, "wait_ms": 3000},
        {"type": STRATEGY_DIRECT, "priority": 2},
    ],
    "selectors": {
        "hotel_list": "div[data-automation='hotel-card'], .listing-item",
        "hotel_name": "div[data-automation='hotel-card-title'], a.hotel-name",
        "hotel_price": "div[data-automation='hotel-card-price'], .price",
        "hotel_score": "span[data-automation='hotel-card-rating'], .bubble-rating",
        "hotel_reviews": "span[data-automation='hotel-card-review-count'], .review-count",
        "hotel_address": "span[data-automation='hotel-card-address'], .address-text",
        "hotel_image": "img[data-automation='hotel-card-cover'], .hotel-image img",
        "next_page": "a[data-automation='next'], nav .next",
        "detail_name": "h1[data-automation='hotel-header-name'], .hotel-name",
        "detail_price": "[data-automation='room-price'], .vendor-price",
    },
    "rate_limit": {"delay_seconds": 2, "max_per_minute": 20, "max_retries": 3, "retry_delay": 10},
    "normalize": {"score_scale": 5.0, "currency": "CNY"},
}

PLATFORMS["airbnb"] = {
    "name": "Airbnb",
    "domains": ["airbnb.com", "airbnb.cn"],
    "base_url": "https://www.airbnb.com",
    "search_url": "https://www.airbnb.com/s/{city}/homes",
    "anti_bot_level": LEVEL_EXTREME,
    "description": "全球最大民宿平台，反爬技术在科技公司中属顶级",

    "backends": [
        {"type": STRATEGY_SCRAPLING, "priority": 1, "wait_ms": 6000},
        {"type": STRATEGY_PLAYWRIGHT, "priority": 2, "wait_ms": 10000, "scroll": True},
    ],
    "selectors": {
        "hotel_list": "div[itemprop='itemListElement'], div[data-testid='listing-card']",
        "hotel_name": "div[data-testid='listing-card-title'], div[itemprop='name']",
        "hotel_price": "span[data-testid='price'], span[itemprop='price']",
        "hotel_score": "span[data-testid='rating'], .rating-num",
        "hotel_reviews": "span[data-testid='review-count'], .review-count",
        "hotel_address": "span[data-testid='listing-card-address'], .location",
        "hotel_image": "img[data-testid='listing-card-image'], .listing-image img",
        "next_page": "a[data-testid='next'], .pagination-next",
        "detail_name": "h1[data-testid='listing-name'], .listing-title",
        "detail_price": "[data-testid='price-details'], .price",
    },
    "rate_limit": {"delay_seconds": 5, "max_per_minute": 8, "max_retries": 2, "retry_delay": 45},
    "normalize": {"score_scale": 5.0, "currency": "CNY"},
}

# 补充平台
PLATFORMS["tujia"] = {
    "name": "途家",
    "domains": ["tujia.com"],
    "base_url": "https://www.tujia.com",
    "search_url": "https://www.tujia.com/search/{city}/",
    "anti_bot_level": LEVEL_HARD,
    "description": "国内最大民宿平台，携程系",

    "backends": [
        {"type": STRATEGY_SCRAPLING, "priority": 1, "wait_ms": 5000},
        {"type": STRATEGY_PLAYWRIGHT, "priority": 2, "wait_ms": 6000},
    ],
    "selectors": {
        "hotel_list": "div.house-item, li.search-result-item",
        "hotel_name": "a.house-name, .listing-title h3",
        "hotel_price": "span.price-num, .price em",
        "hotel_score": "span.score, .rating",
        "hotel_reviews": "span.review-count, .comment-num",
        "hotel_address": ".address, .location-info",
        "hotel_image": "img.house-img, .listing-pic img",
        "next_page": "a.next, .pagination-next",
        "detail_name": "h1.house-title",
        "detail_price": ".room-price em, .price .num",
    },
    "rate_limit": {"delay_seconds": 4, "max_per_minute": 10, "max_retries": 3, "retry_delay": 25},
    "normalize": {"score_scale": 5.0, "currency": "CNY"},
}

PLATFORMS["hotels"] = {
    "name": "Hotels.com",
    "domains": ["hotels.com", "hoteis.com"],
    "base_url": "https://www.hotels.com",
    "search_url": "https://www.hotels.com/Hotel-Search?destination={city}",
    "anti_bot_level": LEVEL_HARD,
    "description": "Expedia集团旗下，与Expedia共享技术栈",

    "backends": [
        {"type": STRATEGY_SCRAPLING, "priority": 1, "wait_ms": 5000},
        {"type": STRATEGY_PLAYWRIGHT, "priority": 2, "wait_ms": 8000},
    ],
    "selectors": {
        "hotel_list": "li[data-stid='property-listing'], div.listing",
        "hotel_name": "h2[data-stid='property-name'], .hotel-title h3",
        "hotel_price": "span[data-stid='price'], .price strong",
        "hotel_score": "span[data-stid='review-score'], .rating",
        "hotel_reviews": "span[data-stid='review-count'], .review-count",
        "hotel_address": "span[data-stid='address'], .location",
        "hotel_image": "img[data-stid='image'], .hotel-img img",
        "next_page": "button[data-stid='next'], .next-page",
        "detail_name": "h1[data-stid='hotel-name'], .property-title",
        "detail_price": "[data-stid='room-price'], .room-rate",
    },
    "rate_limit": {"delay_seconds": 5, "max_per_minute": 8, "max_retries": 3, "retry_delay": 30},
    "normalize": {"score_scale": 10.0, "currency": "CNY"},
}

PLATFORMS["tuniu"] = {
    "name": "途牛",
    "domains": ["tuniu.com"],
    "base_url": "https://www.tuniu.com",
    "search_url": "https://hotel.tuniu.com/search?q={city}",
    "anti_bot_level": LEVEL_MODERATE,
    "description": "以旅游度假为主的OTA",

    "backends": [
        {"type": STRATEGY_SCRAPLING, "priority": 1, "wait_ms": 2000},
        {"type": STRATEGY_DIRECT, "priority": 2},
    ],
    "selectors": {
        "hotel_list": "div.hotel-list-item, li.hotel-item",
        "hotel_name": "a.hotel-name, h3.title",
        "hotel_price": "span.price em, .price-num",
        "hotel_score": "span.score, .satisfaction",
        "hotel_reviews": "span.review-num, .comment-count",
        "hotel_address": ".address, .location",
        "hotel_image": "img.hotel-img, .pic img",
        "next_page": "a.next, .page-next",
        "detail_name": "h1.hotel-name",
        "detail_price": ".price em, .room-price",
    },
    "rate_limit": {"delay_seconds": 2, "max_per_minute": 20, "max_retries": 3, "retry_delay": 10},
    "normalize": {"score_scale": 5.0, "currency": "CNY"},
}

PLATFORMS["kayak"] = {
    "name": "Kayak",
    "domains": ["kayak.com", "kayak.cn"],
    "base_url": "https://www.kayak.com",
    "search_url": "https://www.kayak.com/hotels/{city}",
    "anti_bot_level": LEVEL_HARD,
    "description": "Booking Holdings旗下元搜索",

    "backends": [
        {"type": STRATEGY_SCRAPLING, "priority": 1, "wait_ms": 4000},
        {"type": STRATEGY_PLAYWRIGHT, "priority": 2, "wait_ms": 6000},
    ],
    "selectors": {
        "hotel_list": "div.hotel-card, div[data-resultid]",
        "hotel_name": "div.hotel-name, h3.title",
        "hotel_price": "span.price-text, .price",
        "hotel_score": "span.rating, .review-score",
        "hotel_reviews": "span.review-count, .reviews-total",
        "hotel_address": ".address, .location-text",
        "hotel_image": "img.hotel-img, .hotel-pic img",
        "next_page": "a.next, .pagination-next",
        "detail_name": "h1.hotel-title",
        "detail_price": ".price .amount, .rate",
    },
    "rate_limit": {"delay_seconds": 3, "max_per_minute": 12, "max_retries": 3, "retry_delay": 20},
    "normalize": {"score_scale": 10.0, "currency": "CNY"},
}


# ═══════════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════════

def get_platform(platform_id: str) -> Optional[dict]:
    return PLATFORMS.get(platform_id.lower())

def get_all_platforms() -> dict:
    return PLATFORMS

def list_platforms() -> list[dict]:
    return [
        {"id": pid, "name": p["name"], "domains": p["domains"],
         "anti_bot_level": p["anti_bot_level"], "backends_count": len(p["backends"])}
        for pid, p in PLATFORMS.items()
    ]

def get_platforms_by_level(max_level: int) -> dict:
    return {pid: p for pid, p in PLATFORMS.items() if p["anti_bot_level"] <= max_level}

def resolve_platform(url: str) -> Optional[str]:
    from urllib.parse import urlparse
    domain = urlparse(url).netloc.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    for pid, p in PLATFORMS.items():
        for d in p["domains"]:
            if d in domain:
                return pid
    return None
