# -*- coding: utf-8 -*-
"""
B166ER 海报生成器 v1.0
使用 Playwright 渲染 HTML 模板为高质量图片
"""
import asyncio, sys, os, json
from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

TEMPLATES = {
    "01_roadshow": {
        "name": "融资路演封面",
        "file": "tpl_01_roadshow.html",
        "size": (1920, 1080),
        "desc": "16:9横版，适合融资路演BP封面"
    },
    "02_product": {
        "name": "产品一页纸",
        "file": "tpl_02_product.html",
        "size": (1080, 1920),
        "desc": "9:16竖版，适合酒店服务介绍"
    },
    "03_social": {
        "name": "朋友圈素材",
        "file": "tpl_03_social.html",
        "size": (1080, 1920),
        "desc": "9:16竖版，适合朋友圈/小红书"
    },
    "04_card": {
        "name": "商务名片",
        "file": "tpl_04_card.html",
        "size": (1920, 1080),
        "desc": "16:9横版，创始人名片"
    },
    "05_hotel": {
        "name": "酒店场景展示",
        "file": "tpl_05_hotel.html",
        "size": (1920, 1080),
        "desc": "16:9横版，酒店多场景展示"
    },
}

def get_template(name_or_key):
    for key, tpl in TEMPLATES.items():
        if key == name_or_key or tpl["name"] == name_or_key:
            return key, tpl
    return None, None

async def render_template(key, tpl, output_path=None):
    """使用 Playwright 渲染单个模板"""
    from playwright.async_api import async_playwright

    html_path = TEMPLATE_DIR / tpl["file"]
    if not html_path.exists():
        print(f"[ERROR] 模板文件不存在: {html_path}")
        return False

    if output_path is None:
        output_path = OUTPUT_DIR / f"{key}_output.png"

    w, h = tpl["size"]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": w, "height": h})
        await page.goto(f"file:///{html_path.as_posix()}")
        await page.wait_for_timeout(2000)  # 等待字体加载和动画
        await page.screenshot(path=str(output_path), full_page=False)
        await browser.close()

    print(f"[OK] {tpl['name']} → {output_path.name} ({w}×{h})")
    return True

async def render_all():
    """渲染所有模板"""
    print(f"\n{'='*50}")
    print("B166ER 海报生成器")
    print(f"模板目录: {TEMPLATE_DIR}")
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"{'='*50}\n")

    results = {}
    for key, tpl in TEMPLATES.items():
        output_path = OUTPUT_DIR / f"{key}_{tpl['name']}.png"
        ok = await render_template(key, tpl, output_path)
        results[key] = ok

    print(f"\n{'='*50}")
    ok_count = sum(results.values())
    print(f"完成: {ok_count}/{len(TEMPLATES)} 个模板")
    print(f"输出目录: {OUTPUT_DIR}")
    return results

async def render_one(key_or_name):
    """渲染单个模板"""
    key, tpl = get_template(key_or_name)
    if key is None:
        print(f"[ERROR] 未知模板: {key_or_name}")
        print(f"可用模板: {', '.join(TEMPLATES.keys())}")
        return False
    output_path = OUTPUT_DIR / f"{key}_{tpl['name']}.png"
    return await render_template(key, tpl, output_path)

if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        # 渲染所有
        asyncio.run(render_all())
    elif args[0] == "--list":
        print("\n可用模板:")
        for key, tpl in TEMPLATES.items():
            print(f"  {key}: {tpl['name']} - {tpl['desc']}")
        print()
    else:
        # 渲染指定模板
        key_or_name = args[0]
        asyncio.run(render_one(key_or_name))
