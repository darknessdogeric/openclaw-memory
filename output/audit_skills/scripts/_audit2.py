# -*- coding: utf-8 -*-
import io, sys, os, re, glob, json, hashlib, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
REPORT = os.path.join(ROOT, "output", "audit_skills")
os.makedirs(REPORT, exist_ok=True)
def md5f(p):
    return hashlib.md5(open(p,"rb").read()).hexdigest()[:10]
def rd(p, n=300000):
    try: return open(p, encoding="utf-8", errors="replace").read()[:n]
    except Exception: return ""

LOCS = [("WS", os.path.join(ROOT,"skills")), ("HOME", os.path.join(HOME,"skills")),
        ("CLAUDE", os.path.join(HOME,".claude","skills"))]
skills = {}
for label, base in LOCS:
    if not os.path.isdir(base): continue
    for f in sorted(glob.glob(os.path.join(base,"**","SKILL.md"), recursive=True)):
        t = rd(f); fm = {}
        if t.startswith("---"):
            e = t.find("\n---", 3)
            if e > 0:
                for line in t[3:e].split("\n"):
                    if ":" in line:
                        k,v = line.split(":",1); fm[k.strip().lower()] = v.strip().strip("\"'")
        name = fm.get("name") or os.path.basename(os.path.dirname(f))
        skills.setdefault(name, []).append({"path":f,"loc":label,"dir":os.path.basename(os.path.dirname(f)),
            "desc":fm.get("description",""),"bytes":len(t),
            "scripts":len([x for x in glob.glob(os.path.join(os.path.dirname(f),"**","*"),recursive=True) if os.path.isfile(x)])})
R = {}
R["counts"] = {l: len(glob.glob(os.path.join(b,"**","SKILL.md"), recursive=True)) for l,b in LOCS if os.path.isdir(b)}
R["n_names"] = len(skills); R["n_files"] = sum(len(v) for v in skills.values())

# 重名
dupes = {k:v for k,v in skills.items() if len(v)>1}
identical = 0; differ = []
for k,v in dupes.items():
    hs = {md5f(x["path"]) for x in v}
    if len(hs) == 1: identical += 1
    else: differ.append((k, v))
R["dupes"] = {"groups": len(dupes), "identical": identical, "differ": [(k,[x["loc"] for x in v]) for k,v in differ]}
# 无 desc / desc 短 / 编码损损 / 引用缺失
nodesc = [k for k,v in skills.items() if not any(x["desc"] for x in v)]
shortdesc = [(k, max(len(x["desc"]) for x in v)) for k,v in skills.items()
             if any(x["desc"] for x in v) and max(len(x["desc"]) for x in v) < 60]
encbad = []; broken = []
for k,v in skills.items():
    for x in v:
        b = open(x["path"],"rb").read()
        try: b.decode("utf-8")
        except UnicodeDecodeError as e: encbad.append((x["path"], "decode fail @%d"%e.start))
        if b.count(b"\xef\xbf\xbd") > 2: encbad.append((x["path"], "U+FFFD x%d"%b.count(b"\xef\xbf\xbd")))
        base = os.path.dirname(x["path"])
        for m in re.finditer(r"(?:scripts|references|templates|assets)/([A-Za-z0-9_\-\.]+)", rd(x["path"],60000)):
            if not os.path.exists(os.path.join(base, m.group(0).replace("/",os.sep))):
                broken.append((k, m.group(0))); break
R["nodesc"] = nodesc; R["shortdesc"] = shortdesc; R["encbad"] = encbad; R["broken_ref"] = broken

# 范式库
SI = os.path.join(HOME,"self-improving")
KB = os.path.join(ROOT,"anyi-ops-kb")
para = []
for label, base, pat in [("KB_04_方法论", os.path.join(KB,"04_方法论"), "*.md"),
                         ("KB_全部方法论向", KB, "*.md"),
                         ("SI_rules.md", SI, "rules.md"),
                         ("SI_rules_目录", os.path.join(SI,"rules"), "*.md"),
                         ("SI_专题", SI, "rules_*.md")]:
    if label.startswith("KB_全部"): fs = [f for f in glob.glob(os.path.join(KB,"**","*.md"),recursive=True) if "方法论" in f or "04_" in f]
    elif label == "SI_rules.md": fs = [os.path.join(SI,"rules.md")] if os.path.exists(os.path.join(SI,"rules.md")) else []
    else: fs = sorted(glob.glob(os.path.join(base,pat),recursive=True)) if os.path.isdir(base) else []
    para.append({"label":label,"n":len(fs),"kb":round(sum(os.path.getsize(f) for f in fs)/1024.0,1),
                 "files":[os.path.relpath(f,KB if "KB" in label else SI).replace(os.sep,"/") for f in fs[:400]]})
R["paradigm"] = para

# 闲置（真实提及）
corpus = []
for pat in [os.path.join(ROOT,"memory","*.md"), os.path.join(SI,"*.md"), os.path.join(KB,"**","*.md")]:
    for f in glob.glob(pat, recursive=True): corpus.append(rd(f, 300000))
blob = "\n".join(corpus)
idle = sorted([k for k in skills if blob.count(k)==0], key=lambda k: -max(x["bytes"] for x in skills[k]))
hot = sorted([(blob.count(k),k) for k in skills], reverse=True)
R["idle"] = idle; R["hot"] = hot[:40]; R["corpus_mb"] = round(len(blob)/1048576.0,1)
# 范式文件闲置
pfiles = []
for e in para:
    if e["label"] in ("KB_04_方法论","SI_专题"):
        for f in e["files"]:
            if blob.count(os.path.basename(f).split(".")[0]) == 0: pfiles.append(f)
R["paradigm_idle"] = pfiles
json.dump(R, open(os.path.join(REPORT,"inventory.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)

print("="*94); print("摘要（明细见 output/audit_skills/inventory.json）"); print("="*94)
print("技能：物理 %d 份 / 去重 %d 命名 ｜ 重名 %d 组（其中内容完全相同 %d 组、不同 %d 组）" % (
    R["n_files"], R["n_names"], len(dupes), identical, len(differ)))
print("  各位置:", R["counts"])
print()
print("完整性问题：")
print("  无 description（无法关键词路由）: %d" % len(nodesc))
print("  description <60 字符: %d" % len(shortdesc))
print("  编码损损: %d" % len(encbad))
print("  引用配套文件缺失: %d" % len(broken))
print()
print("范式库:")
for e in para: print("  %-16s %4d 份 / %8.1f KB" % (e["label"], e["n"], e["kb"]))
print()
print("闲置：从未被提及的技能 %d / %d" % (len(idle), len(skills)))
print("  ", ", ".join(idle[:26]))
print("范式文件闲置: %d" % len(pfiles))
print()
print("真在用（被提及最多）:")
for n,k in hot[:16]: print("  %-34s %d" % (k[:34], n))
