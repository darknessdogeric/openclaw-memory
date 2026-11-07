"""AI 概念全景 v2.0 - 3 浅色变体 + 渲染 9:16"""
import os, shutil
from playwright.sync_api import sync_playwright

SRC = r"D:\B166ER-openclaw\workspace\memory\小红书海报"
DST = r"C:\Users\ericz\Desktop\AI概念全景_9x16_2026-10-21"

THEMES = {
    "_mint": {},
    "_gold": {
        "#EFF5F2": "#F7F3EC",
        "#E4EFE9": "#EFE8DA",
        "#E9F2EE": "#F2ECE0",
        "#1B3A34": "#1E3A5F",
        "#4F6B60": "#6B5C42",
        "#38504A": "#3D4A5C",
        "#2F7A63": "#C8963E",
        "#6F9086": "#8A7A5E",
        "rgba(47,122,99,": "rgba(200,150,62,",
        "rgba(27,58,52,": "rgba(30,58,95,",
    },
    "_indigo": {
        "#EFF5F2": "#F4F6FA",
        "#E4EFE9": "#E8ECF4",
        "#E9F2EE": "#EEF1F7",
        "#1B3A34": "#1A2744",
        "#4F6B60": "#5A6478",
        "#38504A": "#39445A",
        "#2F7A63": "#3E6BA8",
        "#6F9086": "#7C88A0",
        "rgba(47,122,99,": "rgba(62,107,168,",
        "rgba(27,58,52,": "rgba(26,39,68,",
    },
}

base = open(os.path.join(SRC, "ai_concepts_v2_mint.html"), encoding="utf-8").read()

for suffix, mapping in THEMES.items():
    txt = base
    for old, new in mapping.items():
        txt = txt.replace(old, new)
    out = "ai_concepts_v2" + suffix + ".html"
    open(os.path.join(SRC, out), "w", encoding="utf-8").write(txt)
    print(f"GENERATED {out}")

files = [
    "ai_concepts_v2_mint.html",
    "ai_concepts_v2_gold.html",
    "ai_concepts_v2_indigo.html",
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
    if f.endswith(".png") and "ai_concepts_v2" in f:
        shutil.copy(os.path.join(SRC, f), DST)
        print(f"  -> Desktop: {f}")
print(f"DESKTOP {DST}")
print("DONE")