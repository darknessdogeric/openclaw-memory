# -*- coding: utf-8 -*-
"""pattern_index.py - 中国传统纹样检索与组合校验

★ 数据：output/book_纹样设计速查手册/纹样索引.json（422 条，源自公开目录原文）
★ 用法:
    python pattern_index.py search 云            # 按名称/母题/结构词检索
    python pattern_index.py chapter 几何物语      # 按章列出
    python pattern_index.py motifs               # 母题表（题材位）
    python pattern_index.py structures            # 结构词表（骨架位）
    python pattern_index.py compose 团花 云       # 组合校验：这个名字合不合规、是否已存在
    python pattern_index.py stats                # 规模统计
"""
import io
import sys
import os
import re
import json
from collections import Counter

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
IDX = os.path.join(ROOT, "output", "book_纹样设计速查手册", "纹样索引.json")
ANALYSIS = os.path.join(ROOT, "output", "book_纹样设计速查手册", "纹样构词法分析.json")

STRUCT = ["四合", "八达晕", "团窠", "龟背", "球路", "盘肠", "锁子", "方胜", "万字", "如意",
          "连钱", "八仙", "连环", "折枝", "方心", "散点", "团花", "散花", "缠枝", "卷草",
          "联珠", "宝相", "几何", "变形", "连续", "回纹", "菱形", "十字", "金鱼", "福寿",
          "葫芦", "喜相逢", "岁寒三友", "卷云", "方胜"]
MOTIF = ["云", "龙", "凤", "鹤", "鸾", "鸟", "雀", "鸳鸯", "鸡", "蝶", "鱼", "龟",
         "莲", "牡丹", "菊", "茶花", "花", "叶", "草", "藤", "枝", "瓜", "果", "石榴", "桃",
         "兽面", "人物", "飞天", "仙", "忍冬", "茱萸", "山石", "水", "雷", "星", "字", "钱",
         "宝", "寿", "福", "喜", "吉", "祥", "瑞", "八宝"]


def load():
    if not os.path.exists(IDX):
        print("缺索引:", IDX)
        return None, None
    P = json.load(open(IDX, encoding="utf-8"))
    A = json.load(open(ANALYSIS, encoding="utf-8")) if os.path.exists(ANALYSIS) else None
    return P, A


def rows(P):
    out = []
    for r in P.get("index_meihua", []):
        out.append({"name": r["name"], "chapter": r.get("chapter"), "page": r.get("page"), "src": "纹样之美"})
    for r in P.get("numbered_4722198", []):
        out.append({"name": r["name"], "chapter": r.get("chapter"), "no": r.get("no"), "src": "速查手册"})
    return out


def cmd_search(P, kw):
    rs = rows(P)
    hits = [r for r in rs if kw in r["name"]]
    print("『%s』命中 %d 条（总 %d）" % (kw, len(hits), len(rs)))
    bych = {}
    for r in hits:
        bych.setdefault(r["chapter"] or "?", []).append(r)
    for c in sorted(bych):
        names = bych[c]
        tag = " ".join("%s%s" % (n["name"], (" p%d" % n["page"]) if n.get("page") else (" #%04d" % n["no"]) if n.get("no") else "")
                       for n in names[:40])
        print("  [%s] %d 条 ｜ %s" % (c, len(names), tag))
    if len(hits) > 40:
        print("  …（仅显示前 40 条）")


def cmd_chapter(P, name):
    rs = [r for r in rows(P) if (r["chapter"] or "") == name]
    print("《%s》命中 %d 条" % (name, len(rs)))
    for r in sorted(rs, key=lambda x: (x.get("page") or 0, x.get("no") or 0)):
        print("   %s" % (r["name"] + (" p%d" % r["page"] if r.get("page") else " #%04d" % r["no"] if r.get("no") else "")))


def cmd_compose(P, struct, motif):
    rs = rows(P)
    exact = [r for r in rs if r["name"] == struct + motif]
    loose = [r for r in rs if struct in r["name"] and motif in r["name"]]
    print("组合：%s × %s → 『%s%s』" % (struct, motif, struct, motif))
    if exact:
        print("  ✔ 已存在（可直接引用）: %s" % ", ".join(
            r["name"] + (" p%d" % r["page"] if r.get("page") else "") for r in exact[:6]))
    else:
        print("  ○ 原书无同名条目 —— 命名层合法（骨架＋母题均为实存词），但形态须回原书/文物核对")
    if loose:
        print("  ○ 同族实存组合（形态参照）: %s" % ", ".join(r["name"] for r in loose[:12]))
    else:
        print("  ★ 该结构×母题组合在已取 %d 条中未见实存 —— 属自创命名，须谨慎" % len(rs))
    print()
    print("  命名长度 %d 字（经验规律：5 字占 49%%，7 字占 17%%）" % len(struct + motif))
    if motif in ("龙", "凤", "兽面", "人物", "飞天"):
        print("  ⚠ 母题带权力/神祇象征 —— 酒店公共空间慎用")
    if any(w in struct + motif for w in ("寿", "福", "喜", "吉", "祥", "万", "八仙")):
        print("  ⚠ 含吉祥寓意 —— 须与场景/客群/节令匹配（喜婚、寿诞、丧仪各自禁忌）")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    P, A = load()
    if P is None:
        return
    cmd = sys.argv[1]
    if cmd == "search" and len(sys.argv) > 2:
        cmd_search(P, sys.argv[2])
    elif cmd == "chapter" and len(sys.argv) > 2:
        cmd_chapter(P, sys.argv[2])
    elif cmd == "compose" and len(sys.argv) > 3:
        cmd_compose(P, sys.argv[2], sys.argv[3])
    elif cmd == "motifs":
        c = Counter()
        for r in rows(P):
            for m in MOTIF:
                if m in r["name"]:
                    c[m] += 1
        print("母题（题材位）%d 个:" % len(c))
        for k, v in c.most_common():
            print("   %-6s %3d" % (k, v))
    elif cmd == "structures":
        c = Counter()
        for r in rows(P):
            for s in STRUCT:
                if s in r["name"]:
                    c[s] += 1
        print("结构词（骨架位）%d 个:" % len(c))
        for k, v in c.most_common():
            print("   %-6s %3d" % (k, v))
    elif cmd == "stats":
        rs = rows(P)
        bych = Counter(r["chapter"] or "?" for r in rs)
        print("总条目 %d" % len(rs))
        for k, v in bych.most_common():
            print("   %-10s %3d" % (k, v))
        lc = Counter(len(r["name"]) for r in rs)
        print("   命名长度: %s" % ", ".join("%d字×%d" % (k, v) for k, v in sorted(lc.items())))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
