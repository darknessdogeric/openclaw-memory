"""
v2 范式一键管线：
- 从 brand_orange 模板生成 xhs_sakura + luxe_gold 变体
- 渲染 3 个 HTML 为 1080×1440 PNG
- 同步到桌面
"""
import os
import shutil
from playwright.sync_api import sync_playwright

SRC = r"D:\B166ER-openclaw\workspace\memory\小红书海报"
DST = r"C:\Users\ericz\Desktop\小红书海报_酒店选址_2026-10-17"

# 颜色主题: (文件名后缀, 替换映射)
THEMES = {
    "_xhs_sakura": {
        "#1a0e08": "#1a0a14",         # 背景
        "#fff0e0": "#fff0f4",         # 主文字
        "#e07020": "#e8a0b8",         # 强调
        "#a07040": "#a07080",         # 副文字
        "#2a1810": "#1a1424",         # 渐变
        "#231408": "#1a0c14",
        "#e87060": "#d8a0b0",         # 差
        "#80c870": "#a890c0",         # 好
        "rgba(224,112,32,": "rgba(232,160,184,",
        "rgba(180,80,80,": "rgba(216,160,180,",
        "rgba(80,180,120,": "rgba(160,144,192,",
    },
    "_luxe_gold": {
        "#1a0e08": "#0a0a0f",
        "#fff0e0": "#e8dcc8",
        "#e07020": "#d4a74a",
        "#a07040": "#6a5a4a",
        "#2a1810": "#1a1410",
        "#231408": "#0d0a06",
        "#e87060": "#b89060",
        "#80c870": "#a0b070",
        "rgba(224,112,32,": "rgba(212,167,74,",
        "rgba(180,80,80,": "rgba(184,144,96,",
        "rgba(80,180,120,": "rgba(160,176,112,",
    },
}

# 1) 生成 2 个变体
base = open(os.path.join(SRC, "hotel_location_v2_brand_orange.html"), encoding="utf-8").read()
for suffix, mapping in THEMES.items():
    txt = base
    for old, new in mapping.items():
        txt = txt.replace(old, new)
    out_name = "hotel_location_v2" + suffix + ".html"
    with open(os.path.join(SRC, out_name), "w", encoding="utf-8") as f:
        f.write(txt)
    print(f"GENERATED {out_name}")

# 2) 渲染 3 个 HTML 为 PNG
files = [
    "hotel_location_v2_brand_orange.html",
    "hotel_location_v2_xhs_sakura.html",
    "hotel_location_v2_luxe_gold.html",
]

with sync_playwright() as p:
    browser = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
    for html_name in files:
        src_path = os.path.join(SRC, html_name)
        dst_path = os.path.join(SRC, html_name.replace(".html", ".png"))
        with open(src_path, encoding="utf-8") as f:
            html = f.read()
        page = browser.new_page(viewport={"width": 1080, "height": 1440}, device_scale_factor=2)
        page.set_content(html, wait_until="domcontentloaded")
        page.wait_for_timeout(500)
        page.screenshot(path=dst_path, full_page=False, omit_background=False, timeout=15000)
        print(f"RENDERED {os.path.basename(dst_path)} {os.path.getsize(dst_path)} bytes")
        page.close()
    browser.close()

# 3) 同步到桌面
os.makedirs(DST, exist_ok=True)
for f in os.listdir(SRC):
    if f.endswith(".png") and "v2" in f:
        shutil.copy(os.path.join(SRC, f), DST)
print(f"DESKTOP SYNCED to {DST}")
print("DONE")
