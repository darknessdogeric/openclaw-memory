"""2027 酒店行业全景预测 一页纸 - 渲染 3 色 + 同步桌面"""
import os, shutil
from playwright.sync_api import sync_playwright

SRC = r"D:\B166ER-openclaw\workspace\memory\小红书海报"
DST = r"C:\Users\ericz\Desktop\2027_酒店行业全景预测_一页纸_2026-10-21"

THEMES = {
    "_brand_orange": {
        "#0a0a0f": "#1a0e08", "#e8dcc8": "#fff0e0",
        "#d4a74a": "#e07020", "#6a5a4a": "#a07040",
        "#1a1410": "#241408", "#0d0a06": "#1f1208", "#060604": "#0a0503",
        "#7fc08a": "#80c870", "#d98a7f": "#e87060", "#c9a86a": "#f08030",
        "rgba(212,167,74,": "rgba(224,112,32,",
        "rgba(127,192,138,": "rgba(128,200,112,",
        "rgba(217,138,127,": "rgba(232,112,96,",
    },
    "_xhs_sakura": {
        "#0a0a0f": "#1a0a14", "#e8dcc8": "#fff0f4",
        "#d4a74a": "#e8a0b8", "#6a5a4a": "#a07080",
        "#1a1410": "#1a1424", "#0d0a06": "#1a0c14", "#060604": "#0a0508",
        "#7fc08a": "#a890c0", "#d98a7f": "#d8a0b0", "#c9a86a": "#f0b8c8",
        "rgba(212,167,74,": "rgba(232,160,184,",
        "rgba(127,192,138,": "rgba(168,144,192,",
        "rgba(217,138,127,": "rgba(216,160,176,",
    },
}

base = open(os.path.join(SRC, "hotel_2027_forecast_1page_gold.html"), encoding="utf-8").read()
for suffix, mapping in THEMES.items():
    txt = base
    for old, new in mapping.items():
        txt = txt.replace(old, new)
    out = "hotel_2027_forecast_1page" + suffix + ".html"
    open(os.path.join(SRC, out), "w", encoding="utf-8").write(txt)
    print(f"GENERATED {out}")

files = [
    "hotel_2027_forecast_1page_gold.html",
    "hotel_2027_forecast_1page_brand_orange.html",
    "hotel_2027_forecast_1page_xhs_sakura.html",
]
with sync_playwright() as p:
    browser = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
    for html in files:
        path = os.path.join(SRC, html)
        png = path.replace(".html", ".png")
        with open(path, encoding="utf-8") as f:
            c = f.read()
        page = browser.new_page(viewport={"width": 1080, "height": 1440}, device_scale_factor=2)
        page.set_content(c, wait_until="domcontentloaded")
        page.wait_for_timeout(500)
        page.screenshot(path=png, full_page=False, omit_background=False, timeout=15000)
        print(f"PNG {os.path.basename(png)} {os.path.getsize(png)} bytes")
        page.close()
    browser.close()

os.makedirs(DST, exist_ok=True)
for f in os.listdir(SRC):
    if f.endswith(".png") and "2027_forecast" in f:
        shutil.copy(os.path.join(SRC, f), DST)
        print(f"  -> Desktop: {f}")
print(f"DESKTOP {DST}")
print("DONE")