"""2027 酒店行业全景预测 v2.0 - 9:16 浅底 3 色变体 + 渲染"""
import os, shutil
from playwright.sync_api import sync_playwright

SRC = r"D:\B166ER-openclaw\workspace\memory\小红书海报"
DST = r"C:\Users\ericz\Desktop\2027_酒店行业全景预测_9x16_2026-10-21"

# 3 个浅底主题
THEMES = {
    # 暖米白 + 金 (原始)
    "_gold": {},
    # 冷白 + 靛青
    "_indigo": {
        "#F7F3EC": "#F4F6FA", "#EFE8DA": "#E8ECF4", "#F2ECE0": "#EEF1F7",
        "#1E3A5F": "#1A2744", "#6B5C42": "#5A6478", "#3D4A5C": "#39445A",
        "#C8963E": "#3E6BA8", "#8A7A5E": "#7C88A0",
        "#2E7D52": "#2E7D52", "#B4503E": "#B4503E",
    },
    # 淡青 + 松绿
    "_mint": {
        "#F7F3EC": "#EFF5F2", "#EFE8DA": "#E4EFE9", "#F2ECE0": "#E9F2EE",
        "#1E3A5F": "#1B3A34", "#6B5C42": "#4F6B60", "#3D4A5C": "#38504A",
        "#C8963E": "#2F7A63", "#8A7A5E": "#6F9086",
        "#2E7D52": "#2E7D52", "#B4503E": "#B4503E",
    },
}

base = open(os.path.join(SRC, "hotel_2027_forecast_v2_gold.html"), encoding="utf-8").read()

for suffix, mapping in THEMES.items():
    txt = base
    for old, new in mapping.items():
        txt = txt.replace(old, new)
    out = "hotel_2027_forecast_v2" + suffix + ".html"
    open(os.path.join(SRC, out), "w", encoding="utf-8").write(txt)
    print(f"GENERATED {out}")

files = [
    "hotel_2027_forecast_v2_gold.html",
    "hotel_2027_forecast_v2_indigo.html",
    "hotel_2027_forecast_v2_mint.html",
]
with sync_playwright() as p:
    browser = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
    for html in files:
        path = os.path.join(SRC, html)
        png = path.replace(".html", ".png")
        with open(path, encoding="utf-8") as f:
            c = f.read()
        page = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=2)
        page.set_content(c, wait_until="domcontentloaded")
        page.wait_for_timeout(500)
        page.screenshot(path=png, full_page=False, omit_background=False, timeout=15000)
        print(f"PNG {os.path.basename(png)} {os.path.getsize(png)} bytes")
        page.close()
    browser.close()

os.makedirs(DST, exist_ok=True)
for f in os.listdir(SRC):
    if f.endswith(".png") and "2027_forecast_v2" in f:
        shutil.copy(os.path.join(SRC, f), DST)
        print(f"  -> Desktop: {f}")
print(f"DESKTOP {DST}")
print("DONE")