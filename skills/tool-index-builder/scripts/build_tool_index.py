# -*- coding: utf-8 -*-
"""build_tool_index.py - 工具索引生成器（内容级取证，不靠名字猜）

输出: output/audit_skills/TOOL_INDEX.json
分类三态: capability（有复用价值的成品工具） / oneoff_family（一次性脚本族） / orphan（待人工裁决）
每个工具标注 owner_skill（归属技能）与 family（同族），使"工具归属哪个技能"成为可校验事实。

用法: python build_tool_index.py
"""
import io
import sys
import os
import re
import json
import glob
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
HOME = os.path.expanduser("~")
TB = os.path.join(ROOT, "toolbox")
AUD = os.path.join(ROOT, "output", "audit_skills")

DQ = chr(34) * 3
SQ = chr(39) * 3

EMBEDDED_ID = re.compile(r"(?:^|[_\-])(\d{3,})(?:[_\-]|$)|^(?:[a-z]+)?(\d{3,})[_\-]")
ONE_OFF_VERB = re.compile(
    r"^(append|add|check|atomic|mk|make|tmp|temp|patch|fix|gen|build|upd|update|del|rm|mv|cp|"
    r"mkdir|wipe|scan|dump|show|list|print|sync|conv|convert|merge|split|clean|pull|push|save|load|"
    r"export|import|backup|rename|move|copy|insert|remove|extract|replace|finalize|final)"
    r"(_|$)"
)
CAPABILITY_KW = re.compile(
    r"(docx|render|ocr|pptx|pdf|router|selfcheck|semantic|search|fetch|index|crawler|crawl|scrap|"
    r"image|infographic|topology|encoding|repair|eval|review|agent)",
    re.I,
)
DOCSTRING = re.compile(r"^\s*(?:" + DQ + r"|" + SQ + r")(.*?)(?:" + DQ + r"|" + SQ + r")", re.S)


def jwrite(p, o):
    d = os.path.dirname(p)
    os.makedirs(d, exist_ok=True)
    fd, t = tempfile.mkstemp(dir=d, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(o, f, ensure_ascii=False, indent=1)
    os.replace(t, p)


def read_head(p, n=6000):
    try:
        return open(p, encoding="utf-8", errors="replace").read()[:n]
    except Exception:
        return ""


def skill_names():
    """真实技能名（祖先判据：祖先目录不含 SKILL.md 才算独立技能）"""
    names = set()
    for base in (os.path.join(ROOT, "skills"), os.path.join(HOME, "skills"),
                 os.path.join(HOME, ".claude", "skills")):
        if not os.path.isdir(base):
            continue
        for f in glob.glob(os.path.join(base, "**", "SKILL.md"), recursive=True):
            rel = os.path.relpath(os.path.dirname(f), base).split(os.sep)
            if any(x.startswith("_") for x in rel):
                continue
            anc = rel[:-1]
            if any(os.path.exists(os.path.join(base, *anc[:i + 1], "SKILL.md")) for i in range(len(anc))):
                continue
            tx = read_head(f, 4000)
            m = re.search(r"^name:\s*(.+)$", tx, re.M)
            names.add((m.group(1).strip() if m else rel[-1]).strip('"\''))
    return sorted(names, key=len, reverse=True)


SKILLS = skill_names()


def first_line(head):
    for l in head.split("\n")[:14]:
        s = l.strip()
        if not s:
            continue
        if s.startswith("#"):
            continue
        if s.startswith("-*-") or s.startswith("coding:"):
            continue
        if s.startswith(DQ) or s.startswith(SQ):
            continue
        return s
    return ""


def classify(base_name, head, owner_hint):
    """内容级判定：docstring 质量 / 是否引用领域词 / 一次性动词前缀 / 日期后缀"""
    ds = DOCSTRING.search(head)
    doc = ds.group(1).strip() if ds else ""
    purpose = (doc.split("\n")[0] if doc else first_line(head))[:180]
    has_doc = bool(doc)
    hit_kw = sorted({m.group(0).lower() for m in CAPABILITY_KW.finditer(head)})
    oneoff = bool(ONE_OFF_VERB.match(base_name))
    dated = bool(re.search(r"20\d{2}[-_]?\d{2}|_\d{4}|v\d+\b", base_name))
    # ★ 内嵌编号 = 一次性实例（例 hb1127_append.py / _670 / 2193）——
    #   这类每个编号一份的脚本是"造轮子"的典型形态，不能因有 docstring 就当成能力工具
    embedded_id = bool(EMBEDDED_ID.search(base_name))
    if oneoff or dated or embedded_id:
        cat = "oneoff_family"
    elif has_doc:
        cat = "capability"
    else:
        cat = "orphan"
    return cat, purpose, has_doc, hit_kw[:6], embedded_id


def owner_of(head, path):
    """归属技能：内容里引用的技能名（取最长匹配）；路径落在 skills/<name>/ 下则取目录名"""
    best = ""
    for n in SKILLS:
        if len(n) < 4:
            continue
        if n in head and len(n) > len(best):
            best = n
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    m = re.match(r"skills/([^/]+)/", rel)
    if m and m.group(1) != "_archive" and len(m.group(1)) > len(best):
        best = m.group(1)
    return best


def family_of(name):
    b = os.path.splitext(name)[0]
    b = re.sub(r"[_-]?\d{2,}$", "", b)
    b = re.sub(r"[_-]?(v\d+|final|finalize|fix\d*|new|copy|bak)$", "", b)
    parts = b.split("_")
    return parts[0] if len(parts) > 1 else b


def main():
    files = [p for p in sorted(glob.glob(os.path.join(TB, "*.py")))
             if not os.path.basename(p).startswith("_")]
    tools = {}
    for p in files:
        b = os.path.basename(p)
        head = read_head(p, 6000)
        owner = owner_of(head, p)
        cat, purpose, has_doc, kw, embedded_id = classify(b, head, owner)
        tools["toolbox/" + b] = {
            "bytes": os.path.getsize(p),
            "category": cat,
            "purpose": purpose,
            "owner_skill": owner,
            "family": family_of(b),
            "has_docstring": has_doc,
            "embedded_id": embedded_id,
            "keywords": kw,
            "path": os.path.relpath(p, ROOT).replace(os.sep, "/"),
        }
    fams = {}
    for k, v in tools.items():
        fams.setdefault(v["family"], []).append(k)
    for k, v in tools.items():
        v["family_size"] = len(fams.get(v["family"], []))
    ti = os.path.join(AUD, "TOOL_INDEX.json")
    if os.path.exists(ti):
        try:
            old = json.load(open(ti, encoding="utf-8"))
        except Exception:
            old = {}
        for k, v in old.items():
            if k in tools:
                tools[k]["skill_equivalent"] = v.get("skill_equivalent", "")
                tools[k]["scope_note"] = v.get("scope_note", "")
    for k, v in tools.items():
        v.setdefault("skill_equivalent", "")
        v.setdefault("scope_note", "")
    jwrite(ti, tools)
    cnt = {}
    for v in tools.values():
        cnt[v["category"]] = cnt.get(v["category"], 0) + 1
    owned = sum(1 for v in tools.values() if v["owner_skill"])
    print("工具索引: %d 个工具 → %s" % (len(tools), os.path.basename(ti)))
    print("  分类: %s" % cnt)
    print("  已归属技能: %d ｜ 未归属: %d" % (owned, len(tools) - owned))
    big = sorted(((v["family_size"], v["family"]) for v in tools.values()), reverse=True)[:12]
    print("  最大同族: %s" % ", ".join("%s(%d)" % (f, n) for n, f in big[:8]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
