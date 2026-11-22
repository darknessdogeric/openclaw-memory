#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""深度抓取:数字旮旯京东商品页、淘宝Top商品页、1688工厂详情"""
import sys, os, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONUTF8'] = '1'

from scrape_matrix import scrape, scrape_search

# ============= Step 1: Direct product URL deep fetch =============
TARGET_URLS = {
    # 淘宝: 已发现的具体商品
    "taobao_xiaomi_blue": "https://world.taobao.com/item/ZHByRWxmV3RQZTRScjNiT3pQTVF5UT09.htm",  # 智驾小蓝灯 usb款
    "taobao_zhijia_yuanjian": "https://www.taobao.com/list/item/a1VOejdLaXdPbHIwN1piOW9VVy9XZz09.htm",  # 智驾小蓝灯自动驾驶指示灯配件
    "taobao_xingjiyuan": "https://www.taobao.com/list/item/L3lJU3A2Zml6bGs1Q0JNZVpjcHRCdz09.htm",  # 星纪元ET

    # 京东: 数字旮旯产品
    "jd_saierlansi": "https://so.m.jd.com/pinpai/6740-559122.html",  # 塞尔兰斯
    "jd_qichezhaungshi": "https://www.jd.com/chanpin/1712026.html",  # 汽车灯光改装
    "jd_zhinengzhui": "https://www.jd.com/chanpin/3363093.html",  # 汽车太阳能警示灯 - 智驾小蓝灯

    # 1688: 工厂直供
    "1688_zhijia_blue": "https://s.1688.com/kq/-B5E7B6AFC6FBB3B5B5C6BEDF.html?beginPage=3",  # 智驾蓝色装饰灯
    "1688_laserradar": "https://s.1688.com/kq/-C6FBB3B5B7C0D7B7CEB2BCA4B9E2B5C6.html",  # 防追尾激光灯

    # 拼多多: 商品页直试
    "pdd_xiaoland": "https://mobile.yangkeduo.com/search_result.html?search_key=%E5%B0%8F%E8%93%9D%E7%81%AF+%E6%96%B0%E8%83%BD%E6%BA%90",  # 搜索页
    "pdd_zhijiaxiaoland": "https://mobile.yangkeduo.com/search_result.html?search_key=%E6%99%BA%E9%A9%BE%E5%B0%8F%E8%93%9D%E7%81%AF",

    # 闲鱼
    "xianyu_xiaoland": "https://www.goofish.com/search?q=%E5%B0%8F%E8%93%9D%E7%81%AF%E6%96%B0%E8%83%BD%E6%BA%90",

    # 苏宁
    "suning_search": "https://search.suning.com/%E5%B0%8F%E8%93%9D%E7%81%AF.html",
}

deep_results = {}
print("=" * 80)
print("深度抓取 - 直连商品页/搜索页")
print("=" * 80)

for label, url in TARGET_URLS.items():
    print(f"\n[{label}] -> {url}")
    try:
        r = scrape(url, wait_ms=5000)
        deep_results[label] = {
            "url": url,
            "tool_used": r.tool_used,
            "ok": r.ok if hasattr(r, 'ok') else True,
            "content": r.content if hasattr(r, 'content') else "",
        }
        # 简短 preview
        preview = (r.content or "")[:500].replace("\n", " ")
        print(f"  -> tool: {r.tool_used}, content len: {len(r.content or '')}")
        print(f"  preview: {preview[:300]}...")
    except Exception as e:
        deep_results[label] = {"url": url, "error": str(e)}
        print(f"  -> ERROR: {e}")

# ============= Step 2: 数字旮旯专项 - 已知上京东 =============
print("\n" + "=" * 80)
print("数字旮旯专项搜索")
print("=" * 80)
shuzhigala_searches = [
    "数字旮旯 智驾灯 京东 价格",
    "数字旮旯 小蓝灯 销量",
    "数字旮旯 小米 SU7 YU7 智驾灯",
    "数字旮旯 小蓝灯 评价",
    "数字旮旯 蔚来 小蓝灯",
]
for q in shuzhigala_searches:
    print(f"\n[搜索] {q}")
    try:
        r = scrape_search(q, max_results=8)
        deep_results[f"search_{q}"] = {
            "tool": r.tool_used,
            "content": r.content,
        }
        print(f"  -> tool: {r.tool_used}, content len: {len(r.content)}")
        print(f"  preview: {r.content[:400].replace(chr(10), ' | ')}")
    except Exception as e:
        print(f"  -> ERROR: {e}")

# ============= Step 3: Save =============
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_xiaoland_deepdive.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(deep_results, f, ensure_ascii=False, indent=2)
print(f"\n[SAVE] -> {out_path}")