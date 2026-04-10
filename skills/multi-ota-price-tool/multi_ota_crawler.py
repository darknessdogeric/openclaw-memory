"""
Multi-OTA Price Crawler - 多平台自动化爬虫
基于chrome-devtools + AI视觉分析

调用方式:
    python multi_ota_crawler.py <酒店名称> [城市] [携程酒店ID]

示例:
    python multi_ota_crawler.py 大理金沙半岛海景养生酒店 大理 750295
    python multi_ota_crawler.py 滁州君家酒店 滁州 1064543
"""

import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

# ============================================================
# 配置
# ============================================================

OPENCLAW_HOST = "http://127.0.0.1:18789"
API_KEY = ""  # Local gateway, no auth needed

OUTPUT_DIR = Path("C:/Users/ericz/.openclaw/workspace/skills/multi-ota-price-tool/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 携程已知城市映射
# ============================================================

CTRIP_CITY_MAP = {
    "大理": {"cityId": 36, "cityName": "大理"},
    "滁州": {"cityId": 214, "cityName": "滁州"},
    "重庆": {"cityId": 4, "cityName": "重庆"},
    "乐山": {"cityId": 36, "cityName": "乐山"},
    "成都": {"cityId": 28, "cityName": "成都"},
    "北京": {"cityId": 1, "cityName": "北京"},
    "上海": {"cityId": 2, "cityName": "上海"},
    "深圳": {"cityId": 30, "cityName": "深圳"},
    "广州": {"cityId": 32, "cityName": "广州"},
}

# ============================================================
# OTA平台配置
# ============================================================

OTA_CONFIG = {
    "ctrip": {
        "name": "携程",
        "priority": 0.40,
        "cityId_key": "cityId",
        "search_keyword_param": "searchWord"
    },
    "meituan": {
        "name": "美团",
        "priority": 0.30,
        "url_template": "https://www.meituan.com/s/{city}%20{hotel}"
    },
    "qunar": {
        "name": "去哪儿", 
        "priority": 0.20,
        "url_template": "https://www.qunar.com/site/oneshot/{city}/{hotel}.htm"
    }
}

# ============================================================
# 标准房判定
# ============================================================

EXCLUDE_KW = ["套", "家庭", "亲子", "行政", "复式", "别墅", "泳池", "私人"]
INCLUDE_KW = ["高级", "豪华", "单间", "标间", "大床", "双床", "标准"]

def is_standard_room(room_name: str) -> bool:
    name = room_name.strip()
    # 排除检查
    for kw in EXCLUDE_KW:
        if kw in name:
            return False
    # 纳入检查
    for kw in INCLUDE_KW:
        if kw in name:
            return True
    return False

def calc_real_price(listed_price: float, discount: float = 0) -> float:
    """还原真实裸房收益: (挂牌价 - 优惠) × 0.85"""
    return (listed_price - discount) * 0.85

# ============================================================
# OCC估算
# ============================================================

def estimate_occ(city: str, star: int = 4) -> float:
    base = {"一线": 0.75, "二线": 0.65, "三线": 0.55}
    adj = {5: 0.05, 4: 0.00, 3: -0.05, 2: -0.10}
    b = base.get("二线", 0.65)  # 默认二线
    a = adj.get(star, 0.00)
    return min(0.90, max(0.40, b + a))

# ============================================================
# 携程爬取主函数
# ============================================================

def crawl_ctrip(hotel_name: str, city: str = None, hotel_id: str = None) -> dict:
    """
    爬取携程酒店价格
    返回: {"platform": "ctrip", "adr": xxx, "rooms": [...], "screenshot": "path"}
    """
    print(f"\n[携程] 开始爬取: {hotel_name}")
    
    # 确定城市参数
    if city and city in CTRIP_CITY_MAP:
        city_info = CTRIP_CITY_MAP[city]
        cityId = city_info["cityId"]
        cityName = city_info["cityName"]
    else:
        # 默认大理
        cityId = 36
        cityName = "大理"
    
    # 如果有hotelId，直接进详情页
    if hotel_id:
        url = f"https://hotels.ctrip.com/hotels/detail/?cityId={cityId}&hotelId={hotel_id}"
    else:
        # 搜索页面
        url = f"https://hotels.ctrip.com/hotels/list/?cityName={cityName}&cityId={cityId}"
    
    print(f"[携程] URL: {url}")
    
    # TODO: 这里实际执行chrome-devtools调用
    # 由于是脚本模式，需要通过subprocess调用openclaw工具
    # 建议: 在OpenClaw内直接使用chrome-devtools工具更稳定
    
    return {
        "platform": "ctrip",
        "hotel_name": hotel_name,
        "city": cityName,
        "cityId": cityId,
        "hotel_id": hotel_id,
        "status": "pending",
        "note": "请在OpenClaw内使用chrome-devtools工具执行实际爬取"
    }

# ============================================================
# 多平台加权ADR计算
# ============================================================

def calculate_multi_ota_adr(platform_results: list, city: str = "二线", star: int = 4) -> dict:
    """
    综合多平台数据计算加权ADR
    
    platform_results: [
        {"platform": "ctrip", "adr": 305, "rooms": 3},
        {"platform": "meituan", "adr": 285, "rooms": 2},
        ...
    ]
    """
    occ = estimate_occ(city, star)
    
    total_weighted = 0
    total_weight = 0
    valid = []
    
    for p in platform_results:
        if p.get("adr") and p["adr"] > 0:
            cfg = OTA_CONFIG.get(p["platform"], {"priority": 0.25})
            w = cfg["priority"]
            eff = p["adr"] * occ
            total_weighted += eff * w
            total_weight += w
            valid.append({
                "platform": cfg["name"],
                "adr": p["adr"],
                "eff_adr": round(eff, 2),
                "weight": w,
                "rooms": p.get("rooms", 0)
            })
    
    if not valid:
        return {"error": "无有效数据"}
    
    weighted_adr = total_weighted / total_weight
    simple_adr = sum(v["adr"] * v["weight"] for v in valid) / sum(v["weight"] for v in valid)
    revpar = weighted_adr * occ
    
    # 置信度
    if len(valid) >= 3:
        confidence = "high"
    elif len(valid) == 2:
        confidence = "medium"
    else:
        confidence = "low"
    
    return {
        "hotel_name": platform_results[0].get("hotel_name", "未知") if platform_results else "未知",
        "weighted_adr": round(weighted_adr, 2),
        "simple_adr": round(simple_adr, 2),
        "occ": occ,
        "revpar": round(revpar, 2),
        "currency": "CNY",
        "sources": valid,
        "confidence": confidence,
        "timestamp": datetime.now().isoformat()
    }

# ============================================================
# 输出格式化报告
# ============================================================

def format_report(result: dict) -> str:
    if "error" in result:
        return f"❌ {result['error']}"
    
    lines = [
        "",
        "=" * 55,
        "  🏨 Multi-OTA 价格情报报告",
        "=" * 55,
        f"  酒店: {result['hotel_name']}",
        f"  生成: {result['timestamp']}",
        "-" * 55,
        f"  📊 综合加权ADR:   ¥{result['weighted_adr']}",
        f"  📈 简单均值ADR:   ¥{result['simple_adr']}",
        f"  📉 估算入住率:    {result['occ']*100:.0f}%",
        f"  💰 估算RevPAR:    ¥{result['revpar']}",
        f"  🎯 置信度:        {result['confidence']}",
        "-" * 55,
        "  各平台明细:",
    ]
    
    for v in result["sources"]:
        eff_pct = v["eff_adr"] / result['weighted_adr'] * 100 if result['weighted_adr'] else 0
        lines.append(
            f"  • {v['platform']:<6} ADR ¥{v['adr']:>6} × OCC {result['occ']*100:.0f}%"
            f" = ¥{v['eff_adr']:>6} (权重{v['weight']*100:.0f}%)"
        )
    
    lines.extend([
        "-" * 55,
        f"  有效样本: {len(result['sources'])}/{len(OTA_CONFIG)} 个平台",
        "  ⚠️  此为估算值，仅供市场定位参考",
        "  ⚠️  AHL运营后请用真实成交数据替代",
        "=" * 55,
    ])
    
    return "\n".join(lines)

# ============================================================
# 主入口
# ============================================================

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n📋 快速测试:")
        # 用已知数据模拟
        mock_results = [
            {"platform": "ctrip", "adr": 305, "rooms": 3, "hotel_name": "测试酒店"},
            {"platform": "meituan", "adr": 285, "rooms": 2},
            {"platform": "qunar", "adr": 292, "rooms": 2},
        ]
        r = calculate_multi_ota_adr(mock_results, city="二线", star=4)
        print(format_report(r))
        return
    
    hotel = sys.argv[1]
    city = sys.argv[2] if len(sys.argv) > 2 else None
    hotel_id = sys.argv[3] if len(sys.argv) > 3 else None
    
    print(f"\n{'='*50}")
    print(f"Multi-OTA Price Crawler v2.0")
    print(f"{'='*50}")
    print(f"酒店: {hotel}")
    print(f"城市: {city or '自动检测'}")
    print(f"携程ID: {hotel_id or '待搜索'}")
    
    # Step 1: 携程爬取
    ctrip_result = crawl_ctrip(hotel, city, hotel_id)
    print(f"\n携程结果: {json.dumps(ctrip_result, ensure_ascii=False, indent=2)}")
    
    # Step 2: 截图保存
    # (chrome-devtools工具在实际执行时保存截图)
    
    # Step 3: AI分析截图
    # (使用image工具分析截图)
    
    # Step 4: 汇总计算
    # (需要各平台数据汇总后调用calculate_multi_ota_adr)
    
    print("\n✅ 脚本结构已就绪。")
    print("📝 执行方式:")
    print("   1. 在OpenClaw内使用chrome-devtools工具导航到各OTA")
    print("   2. 使用image工具分析截图")
    print("   3. 将数据填入platform_results调用calculate_multi_ota_adr")

if __name__ == "__main__":
    main()
