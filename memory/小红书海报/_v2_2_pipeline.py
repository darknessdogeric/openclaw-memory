"""v2.2 范式: B标左上调 + section 序号 + 协调排版"""
import os
import shutil
from playwright.sync_api import sync_playwright

SRC = r"D:\B166ER-openclaw\workspace\memory\小红书海报"
DST = r"C:\Users\ericz\Desktop\小红书海报_酒店选址_2026-10-17"

THEMES = {
    "_xhs_sakura": {
        "#1a0e08": "#1a0a14",
        "#fff0e0": "#fff0f4",
        "#e07020": "#e8a0b8",
        "#a07040": "#a07080",
        "#241408": "#1a1424",
        "#1f1208": "#1a0c14",
        "#e87060": "#d8a0b0",
        "#80c870": "#a890c0",
        "rgba(224,112,32,": "rgba(232,160,184,",
        "rgba(180,80,80,": "rgba(216,160,180,",
        "rgba(80,180,120,": "rgba(160,144,192,",
    },
    "_luxe_gold": {
        "#1a0e08": "#0a0a0f",
        "#fff0e0": "#e8dcc8",
        "#e07020": "#d4a74a",
        "#a07040": "#6a5a4a",
        "#241408": "#1a1410",
        "#1f1208": "#0d0a06",
        "#e87060": "#b89060",
        "#80c870": "#a0b070",
        "rgba(224,112,32,": "rgba(212,167,74,",
        "rgba(180,80,80,": "rgba(216,180,120,",
        "rgba(80,180,120,": "rgba(160,176,112,",
    },
}

base = open(os.path.join(SRC, "hotel_location_v2_2_brand_orange.html"), encoding="utf-8").read()

# 生成变体
for suffix, mapping in THEMES.items():
    txt = base
    for old, new in mapping.items():
        txt = txt.replace(old, new)
    out = "hotel_location_v2_2" + suffix + ".html"
    open(os.path.join(SRC, out), "w", encoding="utf-8").write(txt)
    print(f"GENERATED {out}")

# 渲染
files = [
    "hotel_location_v2_2_brand_orange.html",
    "hotel_location_v2_2_xhs_sakura.html",
    "hotel_location_v2_2_luxe_gold.html",
]
with sync_playwright() as p:
    browser = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
    for html in files:
        path = os.path.join(SRC, html)
        png = path.replace(".html", ".png")
        with open(path, encoding="utf-8") as f:
            content = f.read()
        page = browser.new_page(viewport={"width": 1080, "height": 1440}, device_scale_factor=2)
        page.set_content(content, wait_until="domcontentloaded")
        page.wait_for_timeout(500)
        page.screenshot(path=png, full_page=False, omit_background=False, timeout=15000)
        print(f"RENDERED {os.path.basename(png)} {os.path.getsize(png)} bytes")
        page.close()
    browser.close()

# 同步桌面
os.makedirs(DST, exist_ok=True)
for f in os.listdir(SRC):
    if f.endswith(".png") and "v2_2" in f:
        shutil.copy(os.path.join(SRC, f), DST)
print(f"DESKTOP SYNCED to {DST}")
print("DONE")
