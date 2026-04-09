"""
Multi-OTA Price Intelligence Agent
多平台OTA价格采集 + AI视觉解析 + OCC加权

使用方法:
    python multi_ota_price_agent.py <酒店名称> [城市]
    
示例:
    python multi_ota_price_agent.py 大理金沙半岛海景养生酒店 大理
    python multi_ota_price_agent.py 滁州君家酒店 滁州
"""

import sys
import json
import time
from datetime import datetime
from pathlib import Path

# ============================================================
# OTA平台配置
# ============================================================

OTA_PLATFORMS = {
    "ctrip": {
        "name": "携程",
        "search_url": "https://hotels.ctrip.com/hotels/list/?cityName={city}&cityId={cityId}",
        "hotel_detail_url": "https://hotels.ctrip.com/hotels/detail/?cityId={cityId}&hotelId={hotelId}",
        "priority": 0.40,  # 权重40%
        "city_known": {
            "大理": {"cityId": 36, "cityName": "大理"},
            "滁州": {"cityId": 214, "cityName": "滁州"},
            "重庆": {"cityId": 4, "cityName": "重庆"},
            "乐山": {"cityId": 36, "cityName": "乐山"},
        }
    },
    "meituan": {
        "name": "美团",
        "search_url": "https://www.meituan.com/s/{city}%20{hotel}",
        "priority": 0.30,  # 权重30%
        "city_known": {}
    },
    "qunar": {
        "name": "去哪儿",
        "search_url": "https://www.qunar.com/site/oneshot/{city}/{hotel}.htm",
        "priority": 0.20,  # 权重20%
        "city_known": {}
    },
    "fliggy": {
        "name": "飞猪",
        "search_url": "https://www.fliggy.com/hotel/{city}/{hotel}",
        "priority": 0.10,  # 权重10%
        "city_known": {}
    }
}

# ============================================================
# OCC估算参数（城市等级 × 酒店档次）
# ============================================================

def estimate_occ(city_level: str, hotel_star: int) -> float:
    """
    估算典型入住率(OCC)
    
    city_level: "一线" | "二线" | "三线"
    hotel_star: 钻级(1-5)
    """
    base_occ = {
        "一线": 0.75,
        "二线": 0.65,
        "三线": 0.55
    }.get(city_level, 0.60)
    
    star_adj = {
        5: 0.05,   # 高端豪华
        4: 0.00,   # 中高端
        3: -0.05,  # 经济型
        2: -0.10,  # 快捷
    }.get(hotel_star, 0.00)
    
    return min(0.90, max(0.40, base_occ + star_adj))

# ============================================================
# 标准房判定
# ============================================================

EXCLUDE_KEYWORDS = [
    "套房", "商务套", "家庭房", "亲子房", "行政房",
    "复式", "loft", "别墅", "泳池别墅", "私人泳池",
    "豪华套", "总统套", "蜜月房", "婚房"
]

INCLUDE_KEYWORDS = [
    "高级间", "高级房", "豪华间", "豪华房",
    "单间", "标间", "标准间", "标准房",
    "大床房", "双床房", "标准大床", "标准双床"
]

def is_standard_room(room_name: str) -> tuple[bool, str]:
    """
    判断是否为标准房
    返回: (是否纳入, 判定原因)
    """
    name_lower = room_name.lower()
    
    # 排除检查
    for kw in EXCLUDE_KEYWORDS:
        if kw.lower() in name_lower:
            return False, f"排除关键词:{kw}"
    
    # 纳入关键词检查
    for kw in INCLUDE_KEYWORDS:
        if kw in room_name:
            return True, f"纳入关键词:{kw}"
    
    # 无法判断
    return False, "无法判定"

# ============================================================
# 价格提取（由AI视觉分析调用）
# ============================================================

def extract_prices_from_screenshot(screenshot_path: str, platform: str) -> list[dict]:
    """
    通过截图提取价格
    实际调用image工具分析
    这里定义结构，AI分析逻辑在外部执行
    """
    # AI分析指令模板
    prompt = f"""你是酒店价格分析师。请从截图中提取{platform}上该酒店的所有房间类型和价格。

分析要求：
1. 识别所有房间名称和对应的价格
2. 对每个房间判断是否为"标准房"（排除：套房/家庭房/亲子房/行政房/复式Loft/别墅）
3. 纳入：高级房/豪华房/单间/标间/大床房(1.5米以下)/双床房
4. 返回JSON数组格式

输出格式：
{{
  "rooms": [
    {{"name": "房间名称", "original_price": 挂牌价, "discounted_price": 折后价, "is_standard": true/false, "reason": "判定原因"}}
  ],
  "analysis_notes": "备注"
}}

请直接输出JSON，不要其他文字。"""

    return {
        "screenshot": screenshot_path,
        "prompt": prompt,
        "platform": platform,
        "analysis_needed": True
    }

# ============================================================
# ADR计算
# ============================================================

def calculate_weighted_adr(
    platform_data: dict,
    city_level: str = "二线",
    hotel_star: int = 4
) -> dict:
    """
    计算加权ADR（含OCC加权）
    
    platform_data: {
        "ctrip": {"adr": 305, "rooms": [...], "weight": 0.4},
        "meituan": {"adr": 285, "rooms": [...], "weight": 0.3},
        ...
    }
    """
    occ = estimate_occ(city_level, hotel_star)
    
    # 计算加权ADR
    total_weighted_adr = 0
    total_weight = 0
    valid_sources = []
    
    for platform, data in platform_data.items():
        if data.get("adr") and data["adr"] > 0:
            weight = data.get("weight", 0.25)
            # OCC加权: 实际ADR × OCC = 有效收益
            effective_adr = data["adr"] * occ
            total_weighted_adr += effective_adr * weight
            total_weight += weight
            valid_sources.append({
                "platform": platform,
                "adr": data["adr"],
                "effective_adr": round(effective_adr, 2),
                "weight": weight,
                "rooms_count": len(data.get("rooms", []))
            })
    
    if total_weight == 0:
        return {"error": "无有效数据"}
    
    weighted_adr = total_weighted_adr / total_weight
    simple_adr = sum(d["adr"] * d.get("weight", 0.25) for d in valid_sources) / sum(d.get("weight", 0.25) for d in valid_sources)
    revpar = weighted_adr * occ
    
    return {
        "hotel_name": platform_data.get("hotel_name", "未知"),
        "weighted_adr": round(weighted_adr, 2),
        "simple_adr": round(simple_adr, 2),
        "occ_estimate": occ,
        "revpar_estimate": round(revpar, 2),
        "currency": "CNY",
        "sources": valid_sources,
        "confidence": _calc_confidence(valid_sources),
        "timestamp": datetime.now().isoformat()
    }

def _calc_confidence(sources: list) -> str:
    count = len([s for s in sources if s.get("adr")])
    if count >= 3:
        return "high"
    elif count == 2:
        return "medium"
    else:
        return "low"

# ============================================================
# 输出报告
# ============================================================

def generate_report(result: dict) -> str:
    """生成格式化报告"""
    if "error" in result:
        return f"❌ 错误: {result['error']}"
    
    lines = [
        "=" * 50,
        "🏨 Multi-OTA 价格情报报告",
        "=" * 50,
        f"酒店: {result['hotel_name']}",
        f"生成时间: {result['timestamp']}",
        "-" * 50,
        f"📊 综合加权ADR: ¥{result['weighted_adr']}",
        f"📈 简单均值ADR: ¥{result['simple_adr']}",
        f"📉 估算入住率(OCC): {result['occ_estimate']*100:.0f}%",
        f"💰 估算RevPAR: ¥{result['revpar_estimate']}",
        f"🎯 数据置信度: {result['confidence']}",
        "-" * 50,
        "各平台明细:",
    ]
    
    for src in result["sources"]:
        lines.append(
            f"  • {src['platform']}: "
            f"ADR ¥{src['adr']} × OCC {result['occ_estimate']*100:.0f}% = "
            f"有效 ¥{src['effective_adr']} (权重{src['weight']*100:.0f}%)"
        )
    
    lines.append("-" * 50)
    lines.append(f"⚠️ 注: 此为估算值，仅供参考。AHL运营后用真实数据替代。")
    
    return "\n".join(lines)

# ============================================================
# 主入口（供外部调用）
# ============================================================

def main(hotel_name: str, city: str = None):
    """主流程"""
    print(f"开始采集: {hotel_name}")
    print(f"目标平台: {', '.join(OTA_PLATFORMS.keys())}")
    print(f"OCC估算: {estimate_occ('二线', 4)*100:.0f}% (默认二线城市4钻酒店)")
    
    # TODO: 实现chrome-devtools自动化
    # Step 1: 携程搜索 + 截图
    # Step 2: 美团搜索 + 截图
    # Step 3: 去哪儿搜索 + 截图
    # Step 4: image工具解析各截图
    # Step 5: 汇总计算加权ADR
    
    print("\n⚠️ 自动化脚本待部署。当前为结构定义版本。")
    print("下一步: 集成chrome-devtools API进行实际爬取。")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    hotel = sys.argv[1]
    city = sys.argv[2] if len(sys.argv) > 2 else None
    main(hotel, city)
