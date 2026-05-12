# -*- coding: utf-8 -*-
"""
OTA-Scraper 核心数据模型
所有平台的数据统一标准化到此结构
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class ScrapeStatus(Enum):
    SUCCESS = "success"
    PARTIAL = "partial"      # 部分数据获取成功
    BLOCKED = "blocked"       # 被反爬拦截
    CAPTCHA = "captcha"       # 触发验证码
    TIMEOUT = "timeout"
    FAILED = "failed"

class BackendType(Enum):
    API = "api"               # 直接API调用
    SCRAPLING = "scrapling"   # Scrapling stealth fetch
    PLAYWRIGHT = "playwright" # Playwright浏览器
    OBSCURA = "obscura"       # Obscura Rust浏览器
    DIRECT = "direct"         # 直接HTTP请求

@dataclass
class OTAPrice:
    """标准化价格信息"""
    currency: str = "CNY"
    lowest_price: Optional[float] = None       # 最低价
    original_price: Optional[float] = None     # 原价
    discounted_price: Optional[float] = None   # 折扣价
    price_per_night: Optional[float] = None    # 每晚均价
    tax_included: bool = False
    breakfast_included: bool = False
    cancellation: str = ""                     # 取消政策

@dataclass
class OTARoom:
    """标准化房型信息"""
    room_type: str = ""
    bed_type: str = ""
    price: Optional[float] = None
    available: bool = True
    max_guests: int = 2
    amenities: list[str] = field(default_factory=list)
    cancellation: str = ""

@dataclass
class OTAReview:
    """标准化评价信息"""
    score: Optional[float] = None              # 综合评分(0-5或0-10归一化到0-5)
    review_count: int = 0
    cleanliness: Optional[float] = None
    location: Optional[float] = None
    service: Optional[float] = None
    facilities: Optional[float] = None
    value: Optional[float] = None              # 性价比
    positive_tags: list[str] = field(default_factory=list)
    negative_tags: list[str] = field(default_factory=list)
    recent_reviews: list[dict] = field(default_factory=list)  # 最近评论

@dataclass
class OTAHotel:
    """标准化酒店信息 - 所有平台统一输出格式"""
    # 基础标识
    hotel_id: str = ""                         # 平台内ID
    hotel_name: str = ""
    platform: str = ""                         # 来源平台
    source_url: str = ""

    # 位置信息
    address: str = ""
    city: str = ""
    district: str = ""                         # 商圈/区域
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    nearby_landmarks: list[str] = field(default_factory=list)

    # 等级与分类
    star_rating: Optional[int] = None          # 星级 (1-5)
    hotel_type: str = ""                       # 酒店类型(商务/度假/民宿等)
    brand: str = ""                            # 品牌/集团

    # 价格
    prices: list[OTAPrice] = field(default_factory=list)
    rooms: list[OTARoom] = field(default_factory=list)

    # 评价
    review: Optional[OTAReview] = None

    # 设施与服务
    amenities: list[str] = field(default_factory=list)
    services: list[str] = field(default_factory=list)

    # 图片
    image_urls: list[str] = field(default_factory=list)
    cover_image: str = ""

    # 元数据
    scraped_at: str = ""                       # ISO时间戳
    data_quality: float = 1.0                  # 数据完整度 0-1
    raw_data: dict = field(default_factory=dict)  # 原始数据(用于调试)

@dataclass
class ScrapeAttempt:
    """单次抓取尝试记录"""
    backend: BackendType
    status: ScrapeStatus
    duration_ms: float = 0
    error: str = ""
    content_length: int = 0
    retry_count: int = 0

@dataclass
class OTAResult:
    """一次OTA抓取的完整结果"""
    platform: str
    url: str
    status: ScrapeStatus
    hotels: list[OTAHotel] = field(default_factory=list)
    total_count: int = 0                       # 平台显示的总数
    page: int = 1
    attempts: list[ScrapeAttempt] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    scraped_at: str = ""
    duration_seconds: float = 0.0

    @property
    def success(self) -> bool:
        return self.status in (ScrapeStatus.SUCCESS, ScrapeStatus.PARTIAL)

    @property
    def data_quality(self) -> float:
        if not self.hotels:
            return 0.0
        return sum(h.data_quality for h in self.hotels) / len(self.hotels)
