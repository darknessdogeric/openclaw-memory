# -*- coding: utf-8 -*-
"""sm_parse.py - 信源矩阵数据解析层（只取官方表格原文，不自算比率）
★ 口径纪律: A–J 10 大类 61 源 + K/L/M 扩展 18 源 = 79；总表与逐类命中均引官方原文
"""
import io, sys, os, re

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
KB1 = os.path.join(ROOT, "anyi-ops-kb")
F_MAIN = os.path.join(KB1, "00_安逸集团知识库总览", "B166ER信源矩阵_v1.1_2026-10-11.md")
F_KLM = os.path.join(KB1, "00_全域商业市场认知", "02_资本资产金融",
                     "05_信源矩阵扩展KLM_资本资产金融_v1.0_2026-10-25.md")
F_H79 = os.path.join(KB1, "00_全域商业市场认知", "01_酒店行业",
                     "信源矩阵_酒店行业复苏判断排查总表_v1.0_2026-11-10.md")
F_N = os.path.join(KB1, "00_全域商业市场认知", "01_酒店行业",
                    "06_信源矩阵扩展N_奢华与顶奢_v1.0_2026-11-28.md")
F_GQ = os.path.join(KB1, "04_行业研究", "2026国庆酒店行业全景",
                    "信源矩阵2026国庆排查总表_2026-10-11.md")

RES_COLORS = {
    "取得": "#2E7D5B", "确认发布": "#2E7D5B", "仅摘要": "#C08A1E", "单源待补": "#C08A1E",
    "付费终端": "#8A6BB1", "未取得": "#B04A42", "未发现公开发布": "#B04A42",
    "反爬硬挡": "#4A5568", "主体存疑": "#9AA0A6",
}


def rd(p):
    return open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else ""


def clean(s):
    return re.sub(r"\*\*", "", s).replace("\u3000", " ").strip()


def rows_of(t):
    out = []
    for l in t.split("\n"):
        s = l.strip()
        if s.startswith("|") and s.count("|") >= 3:
            cs = [clean(c) for c in s.strip("|").split("|")]
            if cs and not re.match(r"^[\-\:\s]+$", cs[0]):
                out.append(cs)
    return out


def sec_of(t, a, b=None):
    i = t.find(a)
    if i < 0:
        return ""
    j = t.find(b, i) if b else -1
    return t[i:j] if j > 0 else t[i:]


def load():
    D = {}
    tm = rd(F_MAIN)
    cats = []
    heads = list(re.finditer(r"###\s*([A-J])\.\s*([^\n\uff08(]+)[\uff08(]([^\uff09)]+)[\uff09)]", tm))
    for i, m in enumerate(heads):
        en = heads[i + 1].start() if i + 1 < len(heads) else len(tm)
        srcs = []
        for l in tm[m.end():en].split("\n"):
            ls = l.strip()
            if ls.startswith("- "):
                srcs.append(clean(ls[2:]))
            elif ls.startswith("|") and ls.count("|") >= 3:
                cs = [clean(c) for c in ls.strip("|").split("|")]
                if cs and cs[0] and not re.match(r"^[\-\:\s]+$", cs[0]):
                    srcs.append(cs[0])
        cats.append({"code": m.group(1), "name": clean(m.group(2)), "spec": clean(m.group(3)),
                     "srcs": srcs[:4]})
    D["cats_aj"] = cats
    D["conf"] = rows_of(sec_of(tm, "## 1. \u56db\u6863\u7f6e\u4fe1\u5ea6\u6807\u8bb0", "## 2."))[1:5]
    D["sop"] = rows_of(sec_of(tm, "## 0. \u6570\u636e\u83b7\u53d6\u4f18\u5148\u7ea7 SOP", "## 1."))[1:5]

    tk = rd(F_KLM)
    D["cats_klm"] = [{"code": c, "name": clean(n), "spec": clean(s)}
                     for c, n, s in re.findall(
                         r"##\s*\d+\.\s*([KLM])\s*\u7c7b\uff5c([^\uff08\n]+)\uff08([^\uff09]+)\uff09", tk)]
    D["gap"] = rows_of(sec_of(tk, "## 6. \u5df2\u77e5\u4fe1\u606f\u6e90\u7f3a\u53e3", None))[1:5]
    tn = rd(F_N)
    D["cats_n"] = [{"code": c, "name": clean(n), "spec": clean(s)}
                   for c, n, s in re.findall(
                       r"##\s*\d+\.\s*(N)\s*\u7c7b\uff5c([^\uff08\n]+)\uff08([^\uff09]+)\uff09", tn)]

    th = rd(F_H79)
    D["h79"] = rows_of(sec_of(th, "## 1. \u603b\u7edf\u8ba1", "## 2."))[1:6]
    D["h79_cats"] = [{"code": c, "name": clean(n), "n": int(k)}
                     for c, n, k in re.findall(
                         r"###\s*([A-J])\s*\u7c7b\uff5c([^\uff08\n]+)\uff08(\d+) \u6e90\uff09", th)]

    tg = rd(F_GQ)
    D["gq"] = rows_of(sec_of(tg, "## 1. \u603b\u7edf\u8ba1", "## 2."))[1:6]
    D["gq_cats"] = [{"code": c, "name": clean(n), "hit": clean(h)}
                    for c, n, h in re.findall(
                        r"###\s*([A-J])\s*\u7c7b\uff5c([^\uff08\n]+)\uff08([^\uff09]+)\uff09", tg)]
    return D


def bars(rows):
    segs = []
    for r in rows:
        if len(r) < 3:
            continue
        label = r[0]
        m = re.match(r"^[\u2705\u26a0\ufe0f\ud83d\udcb8\u274c\ud83d\udd12\u26aa]\s*(.*)$", label)
        name = clean(m.group(1)) if m else label
        for k in RES_COLORS:
            if name.startswith(k):
                name = k
                break
        num = re.sub(r"[^\d]", "", r[1]) or "0"
        pct = re.sub(r"[^\d]", "", r[2]) or "0"
        segs.append({"name": name, "raw": label, "n": int(num), "pct": int(pct),
                     "color": RES_COLORS.get(name, "#9AA0A6")})
    return segs


def cat_hit_rows(D):
    out = []
    for g in D["gq_cats"]:
        h = g["hit"]
        nums = [int(x) for x in re.findall(r"\d+", h)]
        src_n = nums[0] if nums else 0
        hit_n = nums[1] if len(nums) > 1 else 0
        rest = re.sub(r"^\d+\s*\u6e90\s*\u2192\s*\d+\s*\u5bb6?\s*", "", h).strip()
        out.append({"code": g["code"], "name": g["name"], "src": src_n, "hit": hit_n,
                    "rest": rest, "pct": round(hit_n * 100.0 / src_n) if src_n else 0})
    return out
