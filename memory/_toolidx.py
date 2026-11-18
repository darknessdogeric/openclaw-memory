# -*- coding: utf-8 -*-
import io, sys, os, re, json, glob, ast, tempfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"

GEN = r'''# -*- coding: utf-8 -*-
"""build_tool_index.py - 工具索引生成器（内容级取证，不靠名字猜）
★ 输出 output/audit_skills/TOOL_INDEX.json
★ 分类三态：capability（有复用价值的成品工具） / oneoff_family（一次性脚本族） / orphan（待人工裁决）
★ 每个工具标注 owner_skill（归属技能）与 family（同族前缀），使"工具归属哪个技能"成为可校验的事实
用法: python build_tool_index.py
"""
import io, sys, os, re, json, glob, tempfile
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HOME = os.path.expanduser("~")
TB = os.path.join(ROOT, "toolbox")
AUD = os.path.join(ROOT, "output", "audit_skills")

ONE_OFF_VERB = re.compile(r"^(append|add|check|atomic|mk|make|tmp|temp|patch|fix|gen|build|upd|update|del|rm|mv|cp|mkdir|wipe|scan|dump|show|list|print|sync|conv|convert|merge|split|clean|pull|push|save|load|export|import|backup|rename|move|copy|insert|remove|extract|replace|finalize|final|mk_|patch_)(_|$)")
CAPABILITY_KW = re.compile(r"(docx|render|ocr|pptx|pdf|router|selfcheck|semantic|search|fetch|index|crawler|crawl|scrap|image|infographic|topology|encoding|repair|eval|review|agent)", re.I)
DOCSTRING = re.compile(r'^\s*(?:"""|\'\'\')(.*?)(?:"""|\'\'\')', re.S)

def jwrite(p, o):
    d = os.path.dirname(p); os.makedirs(d, exist_ok=True)
    fd, t = tempfile.mkstemp(dir=d, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(o, f, ensure_ascii=False, indent=1)
    os.replace(t, p)

def read_head(p, n=4000):
    try:
        return open(p, encoding="utf-8", errors="replace").read()[:n]
    except Exception:
        return ""

def skill_names():
    names = set()
    for base in (os.path.join(ROOT, "skills"), os.path.join(HOME, "skills"), os.path.join(HOME, ".claude", "skills")):
        if not os.path.isdir(base):
            continue
        for f in glob.glob(os.path.join(base, "**", "SKILL.md"), recursive=True):
            rel = os.path.relpath(os.path.dirname(f), base).split(os.sep)
            if any(x.startswith("_") for x in rel):
                continue
            anc = rel[:-1]
            if any(os.path.exists(os.path.join(base, *anc[:i+1], "SKILL.md")) for i in range(len(anc))):
                continue
            tx = read_head(f, 4000)
            m = re.search(r"^name:\s*(.+)$", tx, re.M)
            names.add((m.group(1).strip() if m else rel[-1]).strip('"\''))
    return sorted(names, key=len, reverse=True)

SKILLS = skill_names()

def classify(base_name, head, owner_hint):
    """内容级判定：docstring 质量 + 是否引用领域词 + 是否一次性动词前缀 + 家族规模"""
    ds = DOCSTRING.search(head)
    doc = ds.group(1).strip() if ds else ""
    first = next((l.strip() for l in head.split("\n")[:12]
                  if l.strip() and not l.strip().startswith("#") and not l.strip().startswith(("-*-", "coding:"))
                  and not l.strip().startswith('"""') and not l.strip().startswith("'''")), "")
    purpose = (doc.split("\n")[0] if doc else first)[:180]
    has_doc = bool(doc)
    # 引用领域词（内容取证）
    hit_kw = sorted({m.group(0).lower() for m in CAPABILITY_KW.finditer(head)})
    oneoff = bool(ONE_OFF_VERB.match(base_name))
    dated = bool(re.search(r"20\d{2}[-_]?\d{2}|_\d{4}|v\d+\b", base_name))
    if oneoff or dated:
        cat = "oneoff_family"
    elif has_doc and (hit_kw or owner_hint):
        cat = "capability"
    elif has_doc:
        cat = "capability"
    else:
        cat = "orphan"
    return cat, purpose, has_doc, hit_kw[:6]

def owner_of(head, path):
    best = ""
    for n in SKILLS:
        if len(n) < 4:
            continue
        if n in head:
            if len(n) > len(best):
                best = n
    # 路径归属：toolbox/<skill>/... 或 skills/<skill>/...
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    m = re.match(r"skills/([^/]+)/", rel)
    if m and m.group(1) not in ("_archive",):
        if len(m.group(1)) > len(best):
            best = m.group(1)
    return best

def family_of(name):
    b = os.path.splitext(name)[0]
    b = re.sub(r"[_-]?\d{2,}$", "", b)
    b = re.sub(r"[_-]?(v\d+|final|finalize|fix\d*|new|copy|bak)$", "", b)
    parts = b.split("_")
    return parts[0] if len(parts) > 1 else b

def main():
    files = [p for p in sorted(glob.glob(os.path.join(TB, "*.py"))) if not os.path.basename(p).startswith("_")]
    tools = {}
    for p in files:
        b = os.path.basename(p)
        head = read_head(p, 6000)
        owner = owner_of(head, p)
        cat, purpose, has_doc, kw = classify(b, head, owner)
        tools["toolbox/" + b] = {
            "bytes": os.path.getsize(p),
            "category": cat,
            "purpose": purpose,
            "owner_skill": owner,
            "family": family_of(b),
            "has_docstring": has_doc,
            "keywords": kw,
            "path": os.path.relpath(p, ROOT).replace(os.sep, "/"),
        }
    # 家族规模（内容级之后再统计，用于标注"同族 N 件"）
    fams = {}
    for k, v in tools.items():
        fams.setdefault(v["family"], []).append(k)
    for k, v in tools.items():
        v["family_size"] = len(fams.get(v["family"], []))
    # 已有映射（skill_equivalent / scope_note）沿用
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
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''
os.makedirs(os.path.join(ROOT,"skills","tool-index-builder","scripts"), exist_ok=True)
gp = os.path.join(ROOT,"skills","tool-index-builder","scripts","build_tool_index.py")
open(gp,"w",encoding="utf-8",newline="\n").write(GEN)
ast.parse(GEN)
print("✔ 生成器已落技能层:", os.path.relpath(gp,ROOT).replace(os.sep,"/"), os.path.getsize(gp), "B")

SK = """---
name: tool-index-builder
description: 工具索引生成器：扫描 toolbox 全部非临时脚本，按内容级证据（docstring 质量／领域词／一次性动词前缀／日期后缀）分类为 capability／oneoff_family／orphan，并标注每个工具的归属技能 owner_skill 与同族 family，使"工具归属哪个技能"成为可校验事实。触发：工具层审计、toolbox 治理、工具注册、哪些工具没被用、工具该归到哪个技能、重复造轮子的工具层证据。
---

# tool-index-builder

> **来源**：2026-11-18 技能库审计后续（工具层治理第一段）
> **脚本**：`scripts/build_tool_index.py` → 输出 `output/audit_skills/TOOL_INDEX.json`

## 何时用

- 审计 toolbox 有多少工具、哪些是真能力工具、哪些是一次性脚本
- 判定某个工具该归到哪个技能（owner_skill）
- 给出"重复造轮子"的工具层证据（同族 N 件）

## 纪律

- **不靠名字猜**：分类依据来自文件内容（docstring／引用领域词／动词前缀／日期后缀），名称只作家族聚合用
- **索引是程序生成**：不手改 `TOOL_INDEX.json`，改逻辑改脚本后重跑
"""
open(os.path.join(ROOT,"skills","tool-index-builder","SKILL.md"),"w",encoding="utf-8",newline="\n").write(SK)
print("✔ 技能已建: skills/tool-index-builder/")

import subprocess
r = subprocess.run([sys.executable, gp], capture_output=True, timeout=400)
print(r.stdout.decode("utf-8","replace"))
print(r.stderr.decode("utf-8","replace")[-500:] if r.returncode else "")
