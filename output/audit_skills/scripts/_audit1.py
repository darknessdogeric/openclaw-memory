# -*- coding: utf-8 -*-
import io, sys, os, re, glob, json, datetime, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
REPORT = os.path.join(ROOT, "output", "audit_skills")
os.makedirs(REPORT, exist_ok=True)

def rd(p, n=200000):
    try:
        return open(p, encoding="utf-8", errors="replace").read()[:n]
    except Exception:
        return ""

# ================= 1. 技能库全量清点 =================
LOCS = [
 ("WS_skills", os.path.join(ROOT, "skills")),
 ("WS_agents_workshop", os.path.join(ROOT, "agents", "main", "agent", "workshop-skills")),
 ("HOME_skills", os.path.join(HOME, "skills")),
 ("HOME_claude_skills", os.path.join(HOME, ".claude", "skills")),
 ("HOME_openclaw_skills", os.path.join(HOME, ".openclaw", "skills")),
 ("HOME_selfimproving_skills", os.path.join(HOME, ".self-improving", "obsidian-skills", "skills")),
]
skills = {}
print("=" * 96); print("### 1. 技能库全量清点（按位置）"); print("=" * 96)
for label, base in LOCS:
    if not os.path.isdir(base):
        print("  %-28s (不存在)" % label); continue
    files = sorted(glob.glob(os.path.join(base, "**", "SKILL.md"), recursive=True))
    print("  %-28s %3d 个 SKILL.md" % (label, len(files)))
    for f in files:
        d = os.path.basename(os.path.dirname(f))
        t = rd(f)
        fm = {}
        if t.startswith("---"):
            end = t.find("\n---", 3)
            if end > 0:
                for line in t[3:end].split("\n"):
                    if ":" in line:
                        k, v = line.split(":", 1); fm[k.strip().lower()] = v.strip().strip("\"'")
        name = fm.get("name") or d
        skills.setdefault(name, []).append({"path": f, "label": label, "dir": d,
            "desc": fm.get("description", ""), "fm": fm, "bytes": len(t),
            "scripts": len(glob.glob(os.path.join(os.path.dirname(f), "**", "*"), recursive=True))})
print()
print("  去重后技能名: %d ｜ 物理 SKILL.md 文件: %d" % (len(skills), sum(len(v) for v in skills.values())))

# ================= 2. 完整性 / 损损 =================
print()
print("=" * 96); print("### 2. 完整性审计"); print("=" * 96)
issues = []
dupes = {k: v for k, v in skills.items() if len(v) > 1}
print("  重名技能（同名多处）: %d 组" % len(dupes))
for k, v in list(dupes.items())[:12]:
    print("     %-30s %s" % (k[:30], " | ".join(x["label"] for x in v)))
    if len(v) > 1 and len({md5f(x["path"]) for x in v}) < len(v):
        issues.append(("同名但内容不同", k))
nodesc = [k for k, v in skills.items() if not any(x["desc"] for x in v)]
print()
print("  ★ 无 description（无法被关键词路由）: %d 个" % len(nodesc))
for k in nodesc[:20]: print("     ", k)
shortdesc = [(k, max((len(x["desc"]) for x in v))) for k, v in skills.items() if any(x["desc"] for x in v) and max((len(x["desc"]) for x in v)) < 60]
print("  description 过短（<60 字符，触发困难）: %d 个" % len(shortdesc))
for k, n in sorted(shortdesc, key=lambda x: x[1])[:14]: print("     %-32s %d" % (k[:32], n))
# 编码损损
encbad = []
for k, v in skills.items():
    for x in v:
        b = open(x["path"], "rb").read()
        try: b.decode("utf-8")
        except UnicodeDecodeError as e: encbad.append((x["path"], "decode fail @%d" % e.start))
        if b.count(b"\xef\xbf\xbd") > 2: encbad.append((x["path"], "U+FFFD x%d" % b.count(b"\xef\xbf\xbd")))
print()
print("  ★ 编码损损: %d" % len(encbad))
for p, why in encbad[:12]: print("     %-58s %s" % (os.path.basename(p)[:58], why))
# 引用脚本缺失
broken_ref = []
for k, v in skills.items():
    for x in v:
        base = os.path.dirname(x["path"])
        for m in re.finditer(r"(?:scripts|references|templates|assets)/([A-Za-z0-9_\-\.]+)", rd(x["path"])):
            cand = os.path.join(base, m.group(0).replace("/", os.sep))
            if not os.path.exists(cand):
                broken_ref.append((k, m.group(0))); break
print()
print("  ★ SKILL.md 引用的配套文件缺失: %d" % len(broken_ref))
for k, p in broken_ref[:14]: print("     %-32s %s" % (k[:32], p))

# ================= 3. 范式库清点 =================
print()
print("=" * 96); print("### 3. 范式库（方法论/规则）清点"); print("=" * 96)
PARA = [
 ("KB_04_方法论", os.path.join(ROOT, "anyi-ops-kb", "04_方法论")),
 ("SI_rules", os.path.join(HOME, "self-improving")),
 ("WS_04_方法论", os.path.join(ROOT, "anyi-ops-kb", "04_方法论")),
]
for label, base in PARA:
    if not os.path.isdir(base): print("  %-18s (不存在)" % label); continue
    md = [f for f in glob.glob(os.path.join(base, "**", "*.md"), recursive=True)]
    print("  %-18s %3d 个 .md ｜ %8.1f KB" % (label, len(md), sum(os.path.getsize(f) for f in md)/1024.0))
# 专题范式文件
SI = os.path.join(HOME, "self-improving")
topics = sorted(glob.glob(os.path.join(SI, "rules_*.md")))
print()
print("  SI 专题 rules_*.md: %d 个" % len(topics))
for f in topics:
    t = rd(f, 800)
    ttl = next((l.lstrip("# ").strip() for l in t.split("\n") if l.startswith("#")), "?")
    print("     %-58s %6d B  %s" % (os.path.basename(f)[:58], os.path.getsize(f), ttl[:40]))

# ================= 4. 闲置检测（按真实调用记录）=================
print()
print("=" * 96); print("### 4. 闲置检测（按 memory/corrections/KB 真实提及）"); print("=" * 96)
corpus = []
for pat in [os.path.join(ROOT, "memory", "*.md"), os.path.join(SI, "*.md"),
            os.path.join(ROOT, "anyi-ops-kb", "**", "*.md")]:
    for f in glob.glob(pat, recursive=True):
        corpus.append(rd(f, 400000))
blob = "\n".join(corpus)
print("  语料规模: %d 文件 / %.1f MB" % (len(corpus), len(blob)/1048576.0))
idle = []
for k, v in sorted(skills.items(), key=lambda x: -max(y["bytes"] for y in x[1])):
    n = blob.count(k)
    if n == 0: idle.append(k)
print("  ★ 从未被提及（疑似闲置）: %d / %d" % (len(idle), len(skills)))
print("     " + ", ".join(idle[:40]))
hot = sorted(((blob.count(k), k) for k in skills), reverse=True)[:18]
print()
print("  被提及最多的（真在用）:")
for n, k in hot: print("     %-32s %d 次" % (k[:32], n))

json.dump({"skills": {k: v for k, v in skills.items()}, "issues": issues,
           "idle": idle, "hot": hot, "dupes": list(dupes),
           "nodesc": nodesc, "shortdesc": shortdesc, "encbad": encbad,
           "broken_ref": broken_ref, "topics": [os.path.basename(x) for x in topics]},
          open(os.path.join(REPORT, "inventory.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print()
print("清单落盘:", os.path.join(REPORT, "inventory.json"))
