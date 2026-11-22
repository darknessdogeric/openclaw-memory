# -*- coding: utf-8 -*-
"""build_skill_registry.py - 技能注册表生成器（可复现）

★ 输出 output/audit_skills/SKILL_REGISTRY.json
★ 真实技能判据（与 selfcheck C14 完全同一定义）：
    一个 SKILL.md 的所有祖先目录都不含 SKILL.md，且路径中无 "_" 开头的目录
    → 才算独立技能；技能内部的 examples/ variants/ references/ 不算
★ 每个技能记录：description / 可执行件 / 参考文档 / 三处位置 / 活跃状态

用法: python build_skill_registry.py
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
AUD = os.path.join(ROOT, "output", "audit_skills")
EXEC_EXT = (".py", ".sh", ".js", ".ts", ".ps1", ".bat", ".cmd", ".exe", ".mjs")


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


def frontmatter(t):
    fm = {}
    if t.startswith("---"):
        e = t.find("\n---", 3)
        if e > 0:
            for line in t[3:e].split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm[k.strip().lower()] = v.strip().strip("\"'")
    return fm


def real_skills(base):
    """真实技能：祖先目录不含 SKILL.md，且无 "_" 前缀目录"""
    out = {}
    if not os.path.isdir(base):
        return out
    for f in sorted(glob.glob(os.path.join(base, "**", "SKILL.md"), recursive=True)):
        d = os.path.dirname(f)
        rel = os.path.relpath(d, base).split(os.sep)
        if any(x.startswith("_") for x in rel):
            continue
        anc = rel[:-1]
        if any(os.path.exists(os.path.join(base, *anc[:i + 1], "SKILL.md")) for i in range(len(anc))):
            continue
        t = read_head(f)
        fm = frontmatter(t)
        nm = fm.get("name") or rel[-1]
        ex = [os.path.relpath(x, d).replace(os.sep, "/")
              for x in glob.glob(os.path.join(d, "**", "*"), recursive=True)
              if os.path.isfile(x) and x.lower().endswith(EXEC_EXT)]
        docs = len([x for x in glob.glob(os.path.join(d, "**", "*.md"), recursive=True)
                    if os.path.basename(x) != "SKILL.md"])
        out[nm] = {"dir": rel[-1], "path": f, "desc": fm.get("description", ""),
                   "scripts": len(glob.glob(os.path.join(d, "scripts", "*.py"))),
                   "refs": len(glob.glob(os.path.join(d, "references", "*.md"))),
                   "bytes": len(t), "files": len([x for x in glob.glob(os.path.join(d, "**", "*"), recursive=True)
                                                 if os.path.isfile(x)]),
                   "exec": ex, "docs": docs}
    return out


def main():
    LOCS = [("WS", os.path.join(ROOT, "skills")),
             ("HOME", os.path.join(HOME, "skills")),
             ("CLAUDE", os.path.join(HOME, ".claude", "skills"))]
    reg = {}
    for lab, base in LOCS:
        for nm, i in real_skills(base).items():
            reg.setdefault(nm, {"name": nm, "locs": {}})["locs"][lab] = i

    def canon(e):
        for lab in ("WS", "CLAUDE", "HOME"):
            if lab in e["locs"]:
                return lab, e["locs"][lab]
        return "WS", list(e["locs"].values())[0]

    old = {}
    ti = os.path.join(AUD, "SKILL_REGISTRY.json")
    if os.path.exists(ti):
        try:
            old = {r["name"]: r for r in json.load(open(ti, encoding="utf-8"))}
        except Exception:
            old = {}

    rows = []
    for nm, e in reg.items():
        lab, i = canon(e)
        o = old.get(nm, {})
        rows.append({"name": nm, "canonical": i["path"], "canonical_loc": lab, "desc": i["desc"],
                     "scripts": i["scripts"], "refs": i["refs"], "bytes": i["bytes"], "files": i["files"],
                     "exec": i["exec"], "docs": i["docs"], "all_locs": sorted(e["locs"].keys()),
                     "has_desc": bool(i["desc"]),
                     "status": o.get("status", "active"), "idle_verdict": o.get("idle_verdict", "")})
    rows.sort(key=lambda r: r["name"].lower())
    jwrite(ti, rows)

    nod = [r["name"] for r in rows if not r["has_desc"]]
    by = {}
    for r in rows:
        for l in r["all_locs"]:
            by[l] = by.get(l, 0) + 1
    st = {}
    for r in rows:
        st[r["status"]] = st.get(r["status"], 0) + 1
    print("技能注册表: %d 条 → %s" % (len(rows), os.path.basename(ti)))
    print("  各位置: %s" % by)
    print("  状态: %s" % st)
    print("  无 description: %d %s" % (len(nod), nod[:5]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
