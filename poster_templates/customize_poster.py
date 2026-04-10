# -*- coding: utf-8 -*-
"""
B166ER 海报内容定制器 v1.0
快速替换模板中的内容，无需编辑HTML

用法:
  python customize_poster.py <模板ID> <字段=新值>
  
示例:
  python customize_poster.py 01_roadshow name=张三 phone=13800000000
  python customize_poster.py 04_card title=首席顾问 org=某某集团
  python customize_poster.py 02_product title=智慧酒店解决方案
  
字段说明:
  name        姓名（04名片）
  title       职位（04名片）
  org         公司名（04名片）
  phone       电话
  email       邮箱（04名片）
  website     网站
  tagline     主标语（替换用AI重新定义...）
  round       融资阶段（01路演）
  amount      融资金额（01路演）
"""
import sys, os, json, re
from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent
OUTPUT_DIR = TEMPLATE_DIR / "output"

# 默认联系人信息
DEFAULT = {
    "name": "张实 Eric",
    "title": "创始人 / CEO",
    "org": "AHL · 去中心化旅行平台",
    "phone": "17760348653",
    "email": "ericzhangshi@163.com",
    "website": "ahlprotocol.ai",
    "round": "种子轮融资",
    "amount": "500-800",
    "tagline": "用AI重新定义酒店交易",
    "tagline2": "去中心化交易 · 双AGENT协同 · 87个细分场景",
}

# 各模板替换映射
REPLACEMENTS = {
    "01_roadshow": [
        ("种子轮融资", "round"),
        ("500-800", "amount"),
        ("用AI重新定义酒店交易", "tagline"),
        ("去中心化交易 · 双AGENT协同 · 87个细分场景", "tagline2"),
        ("ahlprotocol.ai", "website"),
        ("17760348653", "phone"),
    ],
    "02_product": [
        ("17760348653", "phone"),
        ("ahlprotocol.ai", "website"),
    ],
    "03_social": [
        ("17760348653", "phone"),
        ("ahlprotocol.ai", "website"),
    ],
    "04_card": [
        ("张实 Eric", "name"),
        ("创始人 / CEO", "title"),
        ("AHL · 去中心化旅行平台", "org"),
        ("17760348653", "phone"),
        ("ericzhangshi@163.com", "email"),
        ("ahlprotocol.ai", "website"),
    ],
    "05_hotel": [
        ("17760348653", "phone"),
        ("ahlprotocol.ai", "website"),
        ("用AI重新定义酒店服务", "tagline"),
    ],
}

TEMPLATE_FILES = {
    "01_roadshow": "tpl_01_roadshow.html",
    "02_product": "tpl_02_product.html",
    "03_social": "tpl_03_social.html",
    "04_card": "tpl_04_card.html",
    "05_hotel": "tpl_05_hotel.html",
}

def apply_customizations(tpl_key, customizations):
    """对指定模板应用定制内容"""
    tpl_file = TEMPLATE_DIR / TEMPLATE_FILES[tpl_key]
    if not tpl_file.exists():
        print(f"[ERROR] 模板不存在: {tpl_file}")
        return False

    with open(tpl_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 依次替换
    for old_text, field in REPLACEMENTS.get(tpl_key, []):
        if field in customizations:
            new_text = customizations[field]
            if old_text in content:
                content = content.replace(old_text, new_text)
                print(f'  [OK] {old_text} -> {new_text}')
            else:
                print(f'  [WARN] not found: {old_text}')

    # 保存定制版
    out_name = f"{tpl_key}_custom.html"
    out_path = TEMPLATE_DIR / out_name
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n已保存: {out_path}")
    return out_path

def render_custom(tpl_key, html_path):
    """渲染定制模板"""
    from playwright.async_api import async_playwright

    w = 1920 if "roadshow" in tpl_key or "card" in tpl_key or "hotel" in tpl_key else 1080
    h = 1080 if w == 1920 else 1920
    out_png = OUTPUT_DIR / f"{tpl_key}_custom.png"

    async def shoot():
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(viewport={"width": w, "height": h})
            await page.goto(f"file:///{html_path.as_posix()}")
            await page.wait_for_timeout(2000)
            await page.screenshot(path=str(out_png))
            await browser.close()
        print(f"[OK] 输出: {out_png.name} ({w}×{h})")

    import asyncio
    asyncio.run(shoot())
    return out_png

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n当前默认信息:")
        for k, v in DEFAULT.items():
            print(f"  {k}: {v}")
        return

    tpl_key = sys.argv[1]
    if tpl_key == "--list":
        print("\n可用模板:")
        for k, v in TEMPLATE_FILES.items():
            print(f"  {k}: {v}")
        return

    if tpl_key not in TEMPLATE_FILES:
        print(f"[ERROR] 未知模板: {tpl_key}")
        print(f"可用: {', '.join(TEMPLATE_FILES.keys())}")
        return

    # 解析自定义字段
    customizations = {}
    for arg in sys.argv[2:]:
        if "=" in arg:
            k, v = arg.split("=", 1)
            customizations[k.strip()] = v.strip()

    print(f"\n>>> 定制模板: {tpl_key}")
    if customizations:
        print("定制内容:")
        for k, v in customizations.items():
            print(f"  {k}: {v}")

    out_html = apply_customizations(tpl_key, customizations)
    if out_html:
        render_custom(tpl_key, out_html)

if __name__ == "__main__":
    main()
