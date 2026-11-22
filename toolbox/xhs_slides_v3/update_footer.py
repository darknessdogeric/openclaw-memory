import os

HTML_DIR = r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_slides_v3"

files = [
    "slide_01_cover.html",
    "slide_02_el1.html",
    "slide_03_el2.html",
    "slide_04_el3.html",
    "slide_05_el4.html",
    "slide_06_el5.html",
    "slide_07_results.html",
]

OLD_TEXT = "方法论系列 · 限制功能性产品本地社区化设计 · v2.0"
NEW_TEXT = "酒店限制性功能产品 · 方法论系列 · v2.0"

for fname in files:
    fpath = os.path.join(HTML_DIR, fname)
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        if OLD_TEXT in content:
            content = content.replace(OLD_TEXT, NEW_TEXT)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated: {fname}")
        else:
            print(f"Not found in: {fname}")

print("Done!")