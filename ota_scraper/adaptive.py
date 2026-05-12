# -*- coding: utf-8 -*-
"""
OTA-Scraper 深化 v1.4 — 自适配 + 移动API + 代理支持

新增能力:
1. AdaptiveSelector — 多候选自动匹配
2. Mobile API端点库 — 移动端通常防护更弱
3. Proxy配置 — 突破网络瓶颈
"""
import re

# ═══════════════════════════════════════════════
# 1. 自适配选择器引擎
# ═══════════════════════════════════════════════

ADAPTIVE_SELECTORS = {
    # 每个字段有多个候选，按优先级排列
    "hotel_list": [
        # Booking系 (data-testid)
        'div[data-testid="property-card"]',
        '[data-testid="property-card"]',
        # Agoda系 (data-selenium)
        'li[data-selenium*="property"]',
        'div[data-element-name*="property-card"]',
        'li.PropertyCard',
        # Expedia/Hotels系 (data-stid)
        'li[data-stid="property-listing"]',
        'div[data-stid*="property"]',
        # 携程系
        'div.card-item-wrap',
        'div.list-item-target',
        # 同程系
        'div.hotelItem',
        # 美团系  
        'div.poi-item',
        'div.hotel-list-item',
        # 通用
        'div[class*="hotel"][class*="card"]',
        'div[class*="hotel"][class*="item"]',
        'li[class*="hotel"]',
        'article[class*="hotel"]',
        'div[class*="listing"]',
    ],
    
    "hotel_name": [
        # Booking
        '[data-testid="title"]', '[data-testid="title-link"]',
        # Agoda
        '[data-selenium="hotel-name"]', 'h3.PropertyCard__HotelName',
        # Expedia
        'h2[data-stid="property-name"]',
        # 携程
        'div.list-card-title', 'h2.list-card-title',
        # 同程
        'div.name', 'h3.title',
        # 通用
        'h3[class*="name"]', 'a[class*="name"]',
        'h2[class*="title"]', '[class*="hotel-name"]',
    ],
    
    "hotel_price": [
        # Booking
        '[data-testid="price-and-discounted-price"]',
        '[data-testid="price-for-x-nights"]',
        # Agoda
        '[data-selenium="display-price"]',
        'span.PropertyCard__Price',
        # Expedia
        'span[data-stid="price"]',
        # 通用
        'span[class*="price"]:not([class*="filter"])',
        'div[class*="price"] em',
        'strong[class*="price"]',
        '[class*="realPrice"]', '[class*="salePrice"]',
    ],
    
    "hotel_score": [
        # Booking
        '[data-testid="review-score"]',
        # Agoda  
        '[data-selenium="review-score"]',
        'span.ReviewScore',
        # Expedia
        'span[data-stid="review-score"]',
        # 携程/同程
        'div.score', 'span.score', 'p.score',
        # 通用
        '[class*="score"]:not([class*="filter"])',
        '[class*="rating"]',
        'div[class*="comment"] [class*="score"]',
    ],
    
    "hotel_reviews": [
        '[data-testid="review-score"]',  # 含评论数
        '[data-selenium="review-count"]',
        'span.ReviewCount',
        '[class*="comment"] [class*="count"]',
        'p.count', 'span.count',
        '[class*="review-count"]',
    ],
    
    "hotel_address": [
        '[data-testid="address-link"]',
        '[data-selenium*="address"]',
        'span[data-stid="address"]',
        'span.position', 'span.ads',
        '[class*="address"]', '[class*="location"]',
    ],
}

# ═══════════════════════════════════════════════
# 2. 移动API端点库
# ═══════════════════════════════════════════════

MOBILE_APIS = {
    "ctrip": {
        "search_url": "https://m.ctrip.com/webapp/hotel/{city}1/",
        "api_hints": [
            "https://m.ctrip.com/restapi/soa2/13444/json/getHotelList",
            "https://m.ctrip.com/restapi/soa2/13444/json/getHotelPrice",
        ],
        "notes": "价格需登录，但移动端HTML包含更完整元数据"
    },
    "qunar": {
        "search_url": "https://touch.qunar.com/hotel/city/{city}/",
        "api_hints": [
            "https://touch.qunar.com/api/hotel/list",
        ],
        "notes": "触摸版(touch)比桌面版防护弱"
    },
    "meituan": {
        "search_url": "https://i.meituan.com/hotel/{city}/",
        "api_hints": [
            "https://ihotel.meituan.com/hbsearch/HotelSearch",
        ],
        "notes": "i.meituan.com是mobile站，价格需登录+图片渲染"
    },
    "tongcheng": {
        "search_url": "https://m.ly.com/hotel/{city}/",
        "notes": "登录查看最低价"
    },
    "fliggy": {
        "search_url": "https://h5.fliggy.com/hotel/search/",
        "api_hints": [
            "https://h5api.m.taobao.com/h5/mtop.fliggy.hotel.search/1.0/",
        ],
        "notes": "阿里mtop网关，需签名认证"
    },
    "agoda": {
        "api_hints": [
            "https://www.agoda.com/api/cronos/search/GetSearchResult",
        ],
        "notes": "GraphQL API可能存在，需抓包确认"
    },
    "booking": {
        "api_hints": [
            "https://www.booking.com/dml/graphql",
        ],
        "notes": "GraphQL端点已确认存在，需auth token"
    },
    "expedia": {
        "api_hints": [
            "https://www.expedia.com/graphql",
        ],
        "notes": "GraphQL端点"
    },
    "tripadvisor": {
        "api_hints": [
            "https://www.tripadvisor.com/data/graphql",
        ],
        "notes": "GraphQL端点，部分数据公开"
    },
}

# ═══════════════════════════════════════════════
# 3. 代理配置
# ═══════════════════════════════════════════════

PROXY_CONFIG = """
# 代理配置模板
# 在平台profiles中设置 "proxy": "http://user:pass@host:port"

# 需要代理的平台 (从中国大陆访问慢)
PROXY_REQUIRED = [
    "agoda",       # 东南亚CDN，大陆慢
    "booking",     # 偶发超时
    "expedia",     # 需代理
    "tripadvisor", # 被403
    "airbnb",      # 需代理
]

# 不需要代理的平台 (国内直连快)
PROXY_NOT_REQUIRED = [
    "ctrip", "qunar", "elong", "tongcheng",
    "meituan", "fliggy", "mafengwo", "lvmama",
    "tujia", "tuniu",
]
"""

# ═══════════════════════════════════════════════
# 4. 自适配选择器函数
# ═══════════════════════════════════════════════

def adaptive_select(page, field_name, platform_id=None):
    """
    自适配选择器: 从page中自动找到匹配field_name的最佳选择器
    
    Args:
        page: Scrapling Response对象
        field_name: hotel_list/hotel_name/hotel_price/...
        platform_id: 平台ID (可选, 用于优先尝试平台特定选择器)
    
    Returns:
        (selector_string, element_count) 或 (None, 0)
    """
    candidates = ADAPTIVE_SELECTORS.get(field_name, [])
    
    # 如果有平台ID，优先尝试该平台已知选择器
    if platform_id:
        from ota_scraper.platforms import get_platform
        plat = get_platform(platform_id)
        if plat:
            plat_sel = plat.get("selectors", {}).get(field_name, "")
            if plat_sel:
                # 分割多选 (用逗号分隔的多个选择器)
                for sel in plat_sel.split(","):
                    sel = sel.strip()
                    if sel and sel not in candidates:
                        candidates.insert(0, sel)
    
    # 逐个测试
    for sel in candidates:
        try:
            matches = page.css(sel)
            count = len(matches) if matches else 0
            # 不同字段的合理范围不同
            if field_name == "hotel_list":
                if 3 <= count <= 200:  # 3-200个酒店卡片是合理的
                    return sel, count
            else:
                if count >= 1:
                    return sel, count
        except:
            continue
    
    return None, 0

# ═══════════════════════════════════════════════
# 5. 平台选择器推断
# ═══════════════════════════════════════════════

def infer_selectors(page, platform_id=None):
    """
    从页面自动推断所有字段的最佳选择器
    返回: {field_name: (selector, count)}
    """
    inferred = {}
    priority_fields = ["hotel_list", "hotel_name", "hotel_price", "hotel_score", "hotel_reviews", "hotel_address"]
    
    # 先找hotel_list
    list_sel, list_count = adaptive_select(page, "hotel_list", platform_id)
    if not list_sel:
        return None
    
    inferred["hotel_list"] = (list_sel, list_count)
    
    # 然后在第一个卡片内找其他字段
    cards = page.css(list_sel)
    if not cards:
        return inferred
    
    first_card = cards[0]
    
    for field in priority_fields[1:]:
        # 尝试在卡片上下文内找
        for sel in ADAPTIVE_SELECTORS.get(field, []):
            try:
                matches = first_card.css(sel)
                if matches and len(matches) >= 1:
                    inferred[field] = (sel, len(matches))
                    break
            except:
                continue
    
    return inferred
