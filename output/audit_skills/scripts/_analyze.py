# -*- coding: utf-8 -*-
"""_analyze.py - 从真实纹样名做构词法分析（母题 × 结构词 → 变体生成规则）

★ 数据源：《纹样之美》完整目录 432 条 + 《纹样设计速查手册》编号表 81 条
★ 目的：把"图鉴"变成"可推演的规则"—— 知道结构词，才能自己长出新纹样名，而不是背 1200 个死条目
"""
import io
import sys
import os
import re
import json
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
EV = r"D:\B166ER-openclaw\workspace\output\book_纹样设计速查手册"
P = json.load(open(os.path.join(EV, "纹样索引.json"), encoding="utf-8"))
names = [x["name"] for x in P["index_meihua"]] + [x["name"] for x in P["numbered_4722198"]]
names = [n for n in names if len(n) >= 3]
print("样本 %d 条纹样名" % len(names))

# ---------- 结构词（可复用的"骨架"） ----------
STRUCT = ["四合", "八达晕", "团窠", "龟背", "球路", "盘肠", "锁子", "方胜", "万字", "如意",
          "连钱", "八仙", "连环", "折枝", "方心", "散点", "团花", "散花", "缠枝", "卷草",
          "联珠", "宝相", "几何", "变形", "连续", "回纹", "菱形", "十字", "双", "对", "双凤",
          "仙", "金鱼", "福寿", "葫芦", "喜相逢", "岁寒三友", "福", "寿", "喜"]
# ---------- 母题（题材主体） ----------
MOTIF = ["云", "龙", "凤", "鹤", "鸾", "鸟", "雀", "鸳鸯", "鸡", "蝴蝶", "蝶", "鱼", "龟",
         "莲", "牡丹", "菊", "茶花", "花", "叶", "藤", "枝", "草", "瓜", "果", "石榴", "桃",
         "兽面", "面", "人物", "飞天", "仙", "如意", "绶带", "宝相", "忍冬", "茱萸", "山石",
         "水", "火", "雷", "星", "字", "钱", "宝", "绶", "戟", "斧", "锁", "锦"]
counts = Counter()
struct_count = Counter()
motif_count = Counter()
pairs = Counter()
for n in names:
    hit_s = [s for s in STRUCT if s in n]
    hit_m = [m for m in MOTIF if m in n]
    for s in hit_s:
        struct_count[s] += 1
    for m in hit_m:
        motif_count[m] += 1
    if hit_s and hit_m:
        for s in hit_s:
            for m in hit_m:
                pairs[(s, m)] += 1

print()
print("=" * 96)
print("### 一、结构词（骨架）Top 22 —— 这些是可复用的组合位")
print("=" * 96)
for k, v in struct_count.most_common(22):
    print("   %-10s %3d 次" % (k, v))

print()
print("=" * 96)
print("### 二、母题（题材）Top 30")
print("=" * 96)
for k, v in motif_count.most_common(30):
    print("   %-10s %3d 次" % (k, v))

print()
print("=" * 96)
print("### 三、结构词 × 母题 实际共现（哪些组合真的存在，可直接调用）")
print("=" * 96)
for (s, m), v in pairs.most_common(30):
    print("   %-8s × %-6s %3d 次" % (s, m, v))

print()
print("=" * 96)
print("### 四、章节资源分布（《纹样之美》7 章）")
print("=" * 96)
bys = {}
for x in P["index_meihua"]:
    bys.setdefault(x["chapter"], []).append(x)
for c, rs in sorted(bys.items(), key=lambda kv: -len(kv[1])):
    ps = [r["page"] for r in rs]
    print("   %-8s %3d 条 ｜ 页码 %3d-%3d ｜ 例: %s" % (
        c, len(rs), min(ps), max(ps), "、".join(r["name"] for r in rs[:4])))

print()
print("=" * 96)
print("### 五、命名长度分布（可视化规则：多长算正常）")
print("=" * 96)
lc = Counter(len(n) for n in names)
for L in sorted(lc):
    print("   %d 字 %3d 条  %s" % (L, lc[L], "█" * min(40, lc[L])))

print()
print("=" * 96)
print("### 六、纹样名里的『寓意线索词』占比（可推导象征义）")
print("=" * 96)
SYM = ["万", "寿", "福", "喜", "如", "意", "吉", "祥", "瑞", "仙", "佛", "禅", "道", "八仙"]
tot = 0
for w in SYM:
    c = sum(1 for n in names if w in n)
    tot += c
    if c:
        print("   %-4s %3d 条" % (w, c))
print("   合计 %d 条含寓意线索（占 %.0f%%）" % (tot, tot * 100.0 / len(names)))

out = {"struct": struct_count.most_common(), "motif": motif_count.most_common(),
       "pairs": [{"struct": s, "motif": m, "n": n} for (s, m), n in pairs.most_common(120)],
       "chapters": {c: len(rs) for c, rs in bys.items()},
       "len_dist": dict(lc), "sample_n": len(names)}
json.dump(out, open(os.path.join(EV, "纹样构词法分析.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print()
print("  落盘: 纹样构词法分析.json")
