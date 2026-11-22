# -*- coding: utf-8 -*-
"""sm_srcrows.py - 79 源排查总表「逐源表」解析

★ 归类按**每行自己的编号前缀**，不靠标题分段：
  该表把 K/L/M 合并成一个标题「### K/L/M 类｜…（18 源）」，而 A–J 各有独立标题
  —— 按标题切段会把 K/L/M 的行全并进 J 类（实测 J 被算成 26，实际 8）
★ 同一 code 只保留首次出现，后续同码行视为汇总行
★ 本文件经 String.raw -> base64 落盘：JS 字符串字面量会吞掉反斜杠
"""
import re

RES_KEY = {
    "✅": "取得", "⚠️": "仅摘要", "💰": "付费终端",
    "❌": "未取得", "🔒": "反爬硬挡", "⚪": "主体存疑",
}
CODE_RE = re.compile(r"^([A-M])(\d+)(?:\s*[-–—~]\s*(?:[A-M])?(\d+))?$")
HEAD_RE = re.compile(r"###\s*([A-M](?:/[A-M])*)\s*类｜([^(\n]+)（([^）]+)）")


def clean(s):
    return re.sub(r"\*\*", "", s).replace("　", " ").strip()


def res_of(sym):
    for k, v in RES_KEY.items():
        if sym.startswith(k):
            return v
    return "其他"


def head_names(t):
    """标题给出的类名（K/L/M 合并标题无法拆出单类名，故单类名由调用方补）"""
    out = {}
    for m in HEAD_RE.finditer(t):
        codes = m.group(1).split("/")
        nm = clean(m.group(2))
        for c in codes:
            out[c] = nm if len(codes) == 1 else out.get(c, "")
    return out


def parse_src_rows(t):
    """返回 {类码: [{"code","name","res"}...]}；按每行编号前缀归类"""
    seen = set()
    out = {}
    for line in t.split("\n"):
        ls = line.strip()
        if not ls.startswith("|"):
            continue
        cells = [c.strip() for c in ls.strip("|").split("|")]
        if len(cells) < 3:
            continue
        cm = CODE_RE.match(clean(cells[0]))
        if not cm:
            continue
        L = cm.group(1)
        a = int(cm.group(2))
        b = int(cm.group(3)) if cm.group(3) else a
        nm = clean(cells[1])
        if not nm:
            continue
        rs = res_of(cells[2])
        for k in range(a, b + 1):
            cd = "%s%d" % (L, k)
            if cd in seen:
                continue
            seen.add(cd)
            out.setdefault(L, []).append({"code": cd, "name": nm, "res": rs})
    return out


def per_class_rate(rows):
    """逐类：总数 / 取得数 / 取得率 / 结果分布 / 每源明细"""
    out = {}
    for code, lst in rows.items():
        d = {}
        for r in lst:
            d[r["res"]] = d.get(r["res"], 0) + 1
        hit = d.get("取得", 0)
        out[code] = {"code": code, "total": len(lst), "hit": hit,
                     "rate": round(hit * 100.0 / len(lst)) if lst else 0,
                     "dist": d, "rows": lst}
    return out


def picks(lst, n=3):
    """取代表信源：取得优先，其次仅摘要/付费终端，最后未取得"""
    order = {"取得": 0, "仅摘要": 1, "付费终端": 1, "未取得": 2,
             "反爬硬挡": 3, "主体存疑": 4, "其他": 5}
    s = sorted(lst, key=lambda r: (order.get(r["res"], 9), r["code"]))
    return s[:n]
