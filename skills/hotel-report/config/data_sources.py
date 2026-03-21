#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
酒店行业数据自动采集配置
Data Source Configuration for Hotel Industry Reports
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

class DataSourceTier(Enum):
    """数据源等级"""
    TIER_1 = "核心数据"  # 每日/每周采集
    TIER_2 = "重要数据"  # 每周/每月采集
    TIER_3 = "参考数据"  # 每月/每季度采集

class DataSourceType(Enum):
    """数据源类型"""
    OFFICIAL = "官方数据"
    INDUSTRY = "行业数据"
    PLATFORM = "平台数据"
    FINANCIAL = "金融数据"
    SOCIAL = "社交数据"
    INTERNATIONAL = "国际数据"

@dataclass
class DataSource:
    """数据源配置"""
    name: str
    name_en: str
    url: str
    tier: DataSourceTier
    source_type: DataSourceType
    data_types: List[str]
    update_frequency: str
    collection_method: str  # api / scraper / manual
    api_endpoint: Optional[str] = None
    api_key_required: bool = False
    scraper_tool: Optional[str] = None
    status: str = "active"  # active / inactive / deprecated
    notes: str = ""

# ==================== 核心数据源配置 ====================

DATA_SOURCES = {
    # ===== 1. 国内官方数据 =====
    "national_bureau_statistics": DataSource(
        name="国家统计局",
        name_en="National Bureau of Statistics",
        url="https://www.stats.gov.cn",
        tier=DataSourceTier.TIER_2,
        source_type=DataSourceType.OFFICIAL,
        data_types=["GDP", "CPI", "社零总额", "居民收入"],
        update_frequency="月度/季度/年度",
        collection_method="api",
        api_endpoint="https://data.stats.gov.cn/easyquery.htm",
        api_key_required=False,
        notes="宏观经济核心指标"
    ),
    
    "ministry_culture_tourism": DataSource(
        name="文化和旅游部",
        name_en="Ministry of Culture and Tourism",
        url="https://www.mct.gov.cn",
        tier=DataSourceTier.TIER_2,
        source_type=DataSourceType.OFFICIAL,
        data_types=["国内旅游人次", "旅游收入", "出境游数据"],
        update_frequency="季度/年度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="官方旅游统计数据"
    ),
    
    "ministry_transport": DataSource(
        name="交通运输部",
        name_en="Ministry of Transport",
        url="https://www.mot.gov.cn",
        tier=DataSourceTier.TIER_1,
        source_type=DataSourceType.OFFICIAL,
        data_types=["跨区域人员流动", "铁路客运", "公路客运", "航空客运"],
        update_frequency="日度/月度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="春运/节假日出行核心数据"
    ),
    
    "civil_aviation_administration": DataSource(
        name="民航局",
        name_en="CAAC",
        url="http://www.caac.gov.cn",
        tier=DataSourceTier.TIER_1,
        source_type=DataSourceType.OFFICIAL,
        data_types=["航班量", "旅客吞吐量", "机场排名"],
        update_frequency="月度/年度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="航空运输核心数据"
    ),
    
    # ===== 2. 国际官方/权威机构 =====
    "str_global": DataSource(
        name="STR Global",
        name_en="STR Global",
        url="https://str.com",
        tier=DataSourceTier.TIER_1,
        source_type=DataSourceType.INTERNATIONAL,
        data_types=["OCC", "ADR", "RevPAR", "酒店业绩"],
        update_frequency="周度/月度",
        collection_method="api",
        api_endpoint="https://str.com/api",
        api_key_required=True,
        notes="酒店行业数据黄金标准"
    ),
    
    "unwto": DataSource(
        name="世界旅游组织",
        name_en="UNWTO",
        url="https://www.unwto.org",
        tier=DataSourceTier.TIER_2,
        source_type=DataSourceType.INTERNATIONAL,
        data_types=["全球旅游数据", "入境游统计"],
        update_frequency="季度/年度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="全球旅游官方数据"
    ),
    
    "wttc": DataSource(
        name="世界旅行与旅游理事会",
        name_en="WTTC",
        url="https://wttc.org",
        tier=DataSourceTier.TIER_2,
        source_type=DataSourceType.INTERNATIONAL,
        data_types=["旅游业经济贡献", "就业数据"],
        update_frequency="年度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="旅游业经济影响研究"
    ),
    
    # ===== 3. 航空公司数据 =====
    "air_china": DataSource(
        name="中国国航",
        name_en="Air China",
        url="https://www.airchina.com.cn",
        tier=DataSourceTier.TIER_2,
        source_type=DataSourceType.PLATFORM,
        data_types=["航线网络", "客座率", "客运量"],
        update_frequency="月度/季度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="商务客源指标"
    ),
    
    "china_southern": DataSource(
        name="南方航空",
        name_en="China Southern",
        url="https://www.csair.com",
        tier=DataSourceTier.TIER_2,
        source_type=DataSourceType.PLATFORM,
        data_types=["航线网络", "客座率", "客运量"],
        update_frequency="月度/季度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="华南市场指标"
    ),
    
    "china_eastern": DataSource(
        name="东方航空",
        name_en="China Eastern",
        url="https://www.ceair.com",
        tier=DataSourceTier.TIER_2,
        source_type=DataSourceType.PLATFORM,
        data_types=["航线网络", "客座率", "客运量"],
        update_frequency="月度/季度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="华东市场指标"
    ),
    
    "iata": DataSource(
        name="国际航空运输协会",
        name_en="IATA",
        url="https://www.iata.org",
        tier=DataSourceTier.TIER_2,
        source_type=DataSourceType.INTERNATIONAL,
        data_types=["全球航空客运量", "航线数据"],
        update_frequency="月度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="全球航空数据"
    ),
    
    # ===== 4. 铁路/交通数据 =====
    "china_railway": DataSource(
        name="国铁集团",
        name_en="China Railway",
        url="https://www.china-railway.com.cn",
        tier=DataSourceTier.TIER_1,
        source_type=DataSourceType.OFFICIAL,
        data_types=["铁路客运量", "高铁网络", "热门线路"],
        update_frequency="日度/月度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="国内出行核心数据"
    ),
    
    "12306": DataSource(
        name="12306",
        name_en="12306",
        url="https://www.12306.cn",
        tier=DataSourceTier.TIER_1,
        source_type=DataSourceType.PLATFORM,
        data_types=["票务数据", "热门线路", "余票信息"],
        update_frequency="实时",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="铁路出行热度指标"
    ),
    
    "amap": DataSource(
        name="高德地图",
        name_en="Amap",
        url="https://www.amap.com",
        tier=DataSourceTier.TIER_1,
        source_type=DataSourceType.PLATFORM,
        data_types=["拥堵指数", "出行热度", "迁徙数据"],
        update_frequency="实时/日度",
        collection_method="api",
        api_key_required=True,
        notes="城市热度/自驾数据"
    ),
    
    "baidu_map": DataSource(
        name="百度地图",
        name_en="Baidu Map",
        url="https://map.baidu.com",
        tier=DataSourceTier.TIER_1,
        source_type=DataSourceType.PLATFORM,
        data_types=["迁徙数据", "出行热度", "POI数据"],
        update_frequency="日度",
        collection_method="api",
        api_key_required=True,
        notes="人口流动大数据"
    ),
    
    # ===== 5. 上市公司数据 =====
    "huazhu_group": DataSource(
        name="华住集团",
        name_en="Huazhu Group",
        url="https://ir.huazhu.com",
        tier=DataSourceTier.TIER_1,
        source_type=DataSourceType.FINANCIAL,
        data_types=["财报", "经营数据", "开店数据"],
        update_frequency="季度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="国内最大酒店集团"
    ),
    
    "jinjiang_hotels": DataSource(
        name="锦江酒店",
        name_en="Jinjiang Hotels",
        url="http://www.jinjianghotels.com.cn",
        tier=DataSourceTier.TIER_1,
        source_type=DataSourceType.FINANCIAL,
        data_types=["财报", "经营数据", "品牌数据"],
        update_frequency="季度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="国内第二大酒店集团"
    ),
    
    "btg_hotels": DataSource(
        name="首旅酒店",
        name_en="BTG Hotels",
        url="http://www.bthhotels.com",
        tier=DataSourceTier.TIER_1,
        source_type=DataSourceType.FINANCIAL,
        data_types=["财报", "经营数据", "如家数据"],
        update_frequency="季度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="首旅如家集团"
    ),
    
    "atour_group": DataSource(
        name="亚朵集团",
        name_en="Atour Group",
        url="https://ir.atour.com",
        tier=DataSourceTier.TIER_1,
        source_type=DataSourceType.FINANCIAL,
        data_types=["财报", "经营数据", "零售数据"],
        update_frequency="季度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="中高端生活方式酒店"
    ),
    
    "ctrip_group": DataSource(
        name="携程集团",
        name_en="Trip.com Group",
        url="https://ir.trip.com",
        tier=DataSourceTier.TIER_1,
        source_type=DataSourceType.FINANCIAL,
        data_types=["财报", "平台数据", "行业洞察"],
        update_frequency="季度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="国内最大OTA"
    ),
    
    "meituan": DataSource(
        name="美团",
        name_en="Meituan",
        url="https://about.meituan.com",
        tier=DataSourceTier.TIER_1,
        source_type=DataSourceType.FINANCIAL,
        data_types=["财报", "酒旅数据", "本地生活"],
        update_frequency="季度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="本地生活平台"
    ),
    
    # ===== 6. OTA/平台数据 =====
    "ctrip_research": DataSource(
        name="携程研究院",
        name_en="Ctrip Research",
        url="https://www.ctrip.com",
        tier=DataSourceTier.TIER_1,
        source_type=DataSourceType.PLATFORM,
        data_types=["预订量", "搜索热度", "价格数据", "行业报告"],
        update_frequency="周度/月度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="行业风向标"
    ),
    
    "meituan_research": DataSource(
        name="美团研究院",
        name_en="Meituan Research",
        url="https://about.meituan.com/research",
        tier=DataSourceTier.TIER_1,
        source_type=DataSourceType.PLATFORM,
        data_types=["本地住宿", "餐饮", "玩乐", "消费趋势"],
        update_frequency="月度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="本地生活指标"
    ),
    
    "fliggy": DataSource(
        name="飞猪",
        name_en="Fliggy",
        url="https://www.fliggy.com",
        tier=DataSourceTier.TIER_1,
        source_type=DataSourceType.PLATFORM,
        data_types=["年轻客群", "出境游", "度假数据"],
        update_frequency="月度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="Z世代指标"
    ),
    
    "qunar": DataSource(
        name="去哪儿",
        name_en="Qunar",
        url="https://www.qunar.com",
        tier=DataSourceTier.TIER_1,
        source_type=DataSourceType.PLATFORM,
        data_types=["价格敏感客群", "机票酒店", "搜索数据"],
        update_frequency="周度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="性价比指标"
    ),
    
    "mafengwo": DataSource(
        name="马蜂窝",
        name_en="Mafengwo",
        url="https://www.mafengwo.cn",
        tier=DataSourceTier.TIER_2,
        source_type=DataSourceType.PLATFORM,
        data_types=["攻略", "自由行", "目的地热度"],
        update_frequency="月度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="内容种草指标"
    ),
    
    "xiaohongshu": DataSource(
        name="小红书",
        name_en="Xiaohongshu",
        url="https://www.xiaohongshu.com",
        tier=DataSourceTier.TIER_2,
        source_type=DataSourceType.SOCIAL,
        data_types=["种草", "打卡", "生活方式"],
        update_frequency="实时",
        collection_method="api",
        api_key_required=True,
        notes="营销趋势"
    ),
    
    "douyin": DataSource(
        name="抖音",
        name_en="Douyin",
        url="https://www.douyin.com",
        tier=DataSourceTier.TIER_2,
        source_type=DataSourceType.SOCIAL,
        data_types=["短视频", "直播", "POI数据"],
        update_frequency="实时",
        collection_method="api",
        api_key_required=True,
        notes="新营销指标"
    ),
    
    # ===== 7. 行业媒体/研究机构 =====
    "meadin": DataSource(
        name="迈点研究院",
        name_en="Meadin Research",
        url="https://www.meadin.com",
        tier=DataSourceTier.TIER_1,
        source_type=DataSourceType.INDUSTRY,
        data_types=["MBI指数", "行业报告", "品牌榜单", "市场研究"],
        update_frequency="日度/周度/月度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="行业福布斯榜单"
    ),
    
    "traveldaily": DataSource(
        name="环球旅讯",
        name_en="TravelDaily",
        url="https://www.traveldaily.cn",
        tier=DataSourceTier.TIER_1,
        source_type=DataSourceType.INDUSTRY,
        data_types=["行业新闻", "深度分析", "研究报告", "数据周报"],
        update_frequency="日度/周度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="行业媒体标杆"
    ),
    
    "hangyan": DataSource(
        name="小牛行研",
        name_en="Hangyan Research",
        url="https://www.hangyan.co",
        tier=DataSourceTier.TIER_1,
        source_type=DataSourceType.INDUSTRY,
        data_types=["酒店周度数据", "OCC/ADR/RevPAR", "行业图表"],
        update_frequency="周度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="酒店数据专业平台"
    ),
    
    "hotelgaocan": DataSource(
        name="酒店高参",
        name_en="Hotel GaoCan",
        url="https://www.hotelgaocan.com",
        tier=DataSourceTier.TIER_2,
        source_type=DataSourceType.INDUSTRY,
        data_types=["行业新闻", "深度报道", "人物专访"],
        update_frequency="日度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="酒店行业深度媒体"
    ),
    
    "shiji": DataSource(
        name="石基信息",
        name_en="Shiji Group",
        url="https://www.shijigroup.com",
        tier=DataSourceTier.TIER_2,
        source_type=DataSourceType.INDUSTRY,
        data_types=["酒店数字化报告", "技术趋势", "白皮书"],
        update_frequency="季度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="酒店数字化领军"
    ),
    
    "horwath": DataSource(
        name="浩华",
        name_en="HVS",
        url="https://www.horwathhtl.com",
        tier=DataSourceTier.TIER_2,
        source_type=DataSourceType.INTERNATIONAL,
        data_types=["酒店估值", "投资分析", "市场报告"],
        update_frequency="季度/年度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="酒店投资咨询"
    ),
    
    # ===== 8. 投资/金融数据 =====
    "iresearch": DataSource(
        name="艾瑞咨询",
        name_en="iResearch",
        url="https://www.iresearch.com.cn",
        tier=DataSourceTier.TIER_2,
        source_type=DataSourceType.INDUSTRY,
        data_types=["互联网研究报告", "在线旅游", "用户研究"],
        update_frequency="月度/季度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="互联网研究"
    ),
    
    "analysys": DataSource(
        name="易观分析",
        name_en="Analysys",
        url="https://www.analysys.cn",
        tier=DataSourceTier.TIER_2,
        source_type=DataSourceType.INDUSTRY,
        data_types=["互联网研究报告", "APP数据", "用户分析"],
        update_frequency="月度/季度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="互联网数据分析"
    ),
    
    "pedaily": DataSource(
        name="投中网",
        name_en="PE Daily",
        url="https://www.pedaily.cn",
        tier=DataSourceTier.TIER_2,
        source_type=DataSourceType.FINANCIAL,
        data_types=["投融资事件", "PE/VC数据", "并购数据"],
        update_frequency="日度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="投融资数据"
    ),
    
    "jll": DataSource(
        name="仲量联行",
        name_en="JLL",
        url="https://www.jll.com.cn",
        tier=DataSourceTier.TIER_2,
        source_type=DataSourceType.INTERNATIONAL,
        data_types=["酒店投资报告", "地产数据", "市场研究"],
        update_frequency="季度/年度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="国际地产咨询"
    ),
    
    "cbre": DataSource(
        name="世邦魏理仕",
        name_en="CBRE",
        url="https://www.cbre.com.cn",
        tier=DataSourceTier.TIER_2,
        source_type=DataSourceType.INTERNATIONAL,
        data_types=["酒店市场研究", "投资数据", "地产报告"],
        update_frequency="季度/年度",
        collection_method="scraper",
        scraper_tool="scrapling",
        notes="国际地产咨询"
    ),
}

# ==================== 采集任务配置 ====================

COLLECTION_SCHEDULE = {
    "daily": [
        "ministry_transport",
        "china_railway",
        "amap",
        "baidu_map",
    ],
    "weekly": [
        "str_global",
        "hangyan",
        "meadin",
        "traveldaily",
        "ctrip_research",
        "qunar",
    ],
    "monthly": [
        "national_bureau_statistics",
        "ministry_culture_tourism",
        "civil_aviation_administration",
        "meituan_research",
        "fliggy",
        "mafengwo",
        "iresearch",
        "analysys",
    ],
    "quarterly": [
        "huazhu_group",
        "jinjiang_hotels",
        "btg_hotels",
        "atour_group",
        "ctrip_group",
        "meituan",
        "shiji",
        "horwath",
        "jll",
        "cbre",
    ],
    "annual": [
        "unwto",
        "wttc",
    ]
}

# ==================== 导出配置 ====================

def get_data_sources_by_tier(tier: DataSourceTier) -> Dict[str, DataSource]:
    """按等级获取数据源"""
    return {k: v for k, v in DATA_SOURCES.items() if v.tier == tier}

def get_data_sources_by_type(source_type: DataSourceType) -> Dict[str, DataSource]:
    """按类型获取数据源"""
    return {k: v for k, v in DATA_SOURCES.items() if v.source_type == source_type}

def get_active_data_sources() -> Dict[str, DataSource]:
    """获取活跃数据源"""
    return {k: v for k, v in DATA_SOURCES.items() if v.status == "active"}

def export_to_yaml() -> str:
    """导出为YAML格式配置"""
    import yaml
    
    config = {
        "version": "2.0",
        "last_updated": "2026-03-18",
        "data_sources": {},
        "collection_schedule": COLLECTION_SCHEDULE
    }
    
    for key, source in DATA_SOURCES.items():
        config["data_sources"][key] = {
            "name": source.name,
            "name_en": source.name_en,
            "url": source.url,
            "tier": source.tier.value,
            "type": source.source_type.value,
            "data_types": source.data_types,
            "update_frequency": source.update_frequency,
            "collection_method": source.collection_method,
            "status": source.status,
        }
    
    return yaml.dump(config, allow_unicode=True, sort_keys=False)

if __name__ == "__main__":
    # 打印统计信息
    print("=" * 60)
    print("酒店行业数据源配置统计")
    print("=" * 60)
    
    print(f"\n总计数据源: {len(DATA_SOURCES)} 个")
    
    print("\n按等级分布:")
    for tier in DataSourceTier:
        count = len(get_data_sources_by_tier(tier))
        print(f"  {tier.value}: {count} 个")
    
    print("\n按类型分布:")
    for source_type in DataSourceType:
        count = len(get_data_sources_by_type(source_type))
        print(f"  {source_type.value}: {count} 个")
    
    print("\n按采集频率分布:")
    for freq, sources in COLLECTION_SCHEDULE.items():
        print(f"  {freq}: {len(sources)} 个")
    
    print("\n活跃数据源:", len(get_active_data_sources()))
    
    # 导出YAML配置
    yaml_config = export_to_yaml()
    with open("data_sources_config.yaml", "w", encoding="utf-8") as f:
        f.write(yaml_config)
    print("\n配置已导出至: data_sources_config.yaml")
