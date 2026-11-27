# -*- coding: utf-8 -*-
"""_clean.py - 清理纹样索引噪声 + 取出纹样简史章明细 + 提取国堰/文漾都江应用上下文"""
import io
import sys
import os
import re
import json
import glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
EV = r"D:\B166ER-openclaw\workspace\output\book_纹样设计速查手册"
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")

P = json.load(open(os.path.join(EV, "纹样索引.json"), encoding="utf-8"))

# ---------- 1. 去噪：剔除电商文案 / 章节名误切 ----------
NOISE = re.compile(r"(領券|到貨|歷時|共計|優惠|折扣|運費|送貨|庫存|頁數|評價|客服|購物|書城|簡體書|大陸圖書|分類|售價|我要買|編輯推薦|內容簡介|關於作者|頁|圖|冊)")
CN = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7}
CH = {"一": "纹样简史", "二": "几何物语", "三": "植物之美", "四": "祥瑞兽谱",
      "五": "鸟鸣花落", "六": "万物生灵", "七": "人物之美"}
before = len(P["index_meihua"])
clean = []
for r in P["index_meihua"]:
    if NOISE.search(r["name"]):
        continue
    if not re.search(r"[纹雲云]", r["name"]):
        continue
    if r["chapter"] == "?":
        continue
    clean.append(r)
P["index_meihua"] = clean
print("索引去噪: %d → %d 条（剔除电商文案与误切）" % (before, len(clean)))

# ---------- 2. 纹样简史章明细（时代搭配禁忌的方法论内核） ----------
print()
print("=" * 96)
print("### 纹样简史章明细（按朝代分期 —— 这就是『避免时代搭配错误』的底层依据）")
print("=" * 96)
hist = [r for r in clean if r["chapter"] == "纹样简史"]
for r in sorted(hist, key=lambda x: x["page"]):
    print("   p%-4d %s" % (r["page"], r["name"]))

# ---------- 3. 各类分布 + 校验 ----------
print()
bys = {}
for r in clean:
    bys.setdefault(r["chapter"], []).append(r)
print("=== 《纹样之美》7 章资源分布 ===")
for c in ["纹样简史", "几何物语", "植物之美", "祥瑞兽谱", "鸟鸣花落", "万物生灵", "人物之美"]:
    rs = bys.get(c, [])
    ps = [r["page"] for r in rs]
    print("   %-8s %3d 条 ｜ 页 %s" % (c, len(rs), ("%d-%d" % (min(ps), max(ps))) if ps else "—"))

# 编号表（纹样设计速查手册 0001+）第一章 = 云纹
print()
num = P["numbered_4722198"]
print("=== 《纹样设计速查手册》编号表已抓到 %d 条（%04d-%04d，均属第一章 云纹）===" % (len(num), num[0]["no"], num[-1]["no"]))

json.dump(P, open(os.path.join(EV, "纹样索引.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------- 4. 应用上下文：国堰项目 ＋ 文漾都江纹样 IP 库 ----------
print()
print("=" * 96)
print("### 应用上下文取证（国堰项目 + 文漾都江纹样 IP 库）")
print("=" * 96)
DESK = os.path.join(HOME, "Desktop", "产业发展部", "旗下酒店", "国堰宾馆")
if os.path.isdir(DESK):
    print("  国堰项目文件夹存在，顶层:")
    for x in sorted(os.listdir(DESK))[:14]:
        print("     %s" % x)
# 检索 KB 中"文漾都江 88 款纹样"的原文
kb = r"D:\anyi-ops-kb"
if not os.path.isdir(kb):
    kb = os.path.join(ROOT, "anyi-ops-kb")
found = 0
for base, dirs, fs in os.walk(kb):
    dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "__pycache__")]
    for f in fs:
        if not f.endswith(".md"):
            continue
        p = os.path.join(base, f)
        try:
            t = open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        if "88 款纹样" in t or "88款纹样" in t:
            for m in re.finditer(r".{0,120}88\s?款纹样.{0,260}", t):
                print()
                print("   ▸ %s" % os.path.relpath(p, kb).replace(os.sep, "/")[:70])
                print("     " + m.group(0).replace("\n", " ")[:340])
                found += 1
                break
        if found >= 5:
            break
    if found >= 5:
        break
if not found:
    print("   ★ 未在 KB 找到『88 款纹样』原文")
