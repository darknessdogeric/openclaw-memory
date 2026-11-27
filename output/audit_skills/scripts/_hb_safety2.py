# -*- coding: utf-8 -*-
"""_hb_safety2.py - hb 家族归档前安全闸（收窄到执行面）

★ 只查"会真的执行这些脚本"的地方：
    1) toolbox 里其它 .py 对它们的调用（subprocess / import / 命令行拼装）
    2) 配置文件里的路径引用（json / yaml / js / ps1 / bat / sh，仅顶层与配置目录）
    3) 记忆层里"正在用"的表述（仅最近 30 天日记，排除历史归档日志）
★ 文档正文提及不算引用（那是历史记录，不是执行依赖）
"""
import io
import sys
import os
import re
import glob
import json
import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
TB = os.path.join(ROOT, "toolbox")
AUD = os.path.join(ROOT, "output", "audit_skills")

hb = sorted(os.path.basename(p) for p in glob.glob(os.path.join(TB, "hb*.py")))
print("hb 家族: %d 件" % len(hb))

CALL = re.compile(r"(?:subprocess\.(?:run|Popen|call|check_output)|os\.system|os\.popen|exec\(|spawn|python3?\s+|import\s+)")

# ---------- 1) 其它脚本的调用面 ----------
hits_scripts = {}
for p in glob.glob(os.path.join(TB, "*.py")):
    b = os.path.basename(p)
    if b.startswith("hb"):
        continue
    try:
        t = open(p, encoding="utf-8", errors="replace").read()
    except Exception:
        continue
    for name in hb:
        stem = name[:-3]
        if name in t or re.search(r"[\s\"'`/\\]%s\b" % re.escape(stem), t):
            # 只在有执行语义的行才算
            for line in t.split("\n"):
                if (name in line or re.search(r"[\s\"'`/\\]%s\b" % re.escape(stem), line)) and CALL.search(line):
                    hits_scripts.setdefault(name, set()).add("%s: %s" % (b, line.strip()[:88]))
                    break

# ---------- 2) 配置文件面 ----------
cfg_files = []
for d in (os.path.join(ROOT, ".."), os.path.join(HOME, ".openclaw")):
    if not os.path.isdir(d):
        continue
    for base, dirs, fs in os.walk(d):
        dirs[:] = [x for x in dirs if x not in
                   ("node_modules", ".git", "__pycache__", ".chroma_db", "venv", ".venv",
                    "output", "skills", "toolbox", "memory", "anyi-ops-kb", "agents", "workspace")]
        depth = len(os.path.relpath(base, d).split(os.sep))
        if depth > 2:
            dirs[:] = []
            continue
        for f in fs:
            if f.endswith((".json", ".yaml", ".yml", ".toml", ".js", ".ps1", ".bat", ".sh")):
                cfg_files.append(os.path.join(base, f))
hits_cfg = {}
for p in cfg_files:
    try:
        if os.path.getsize(p) > 2_000_000:
            continue
        t = open(p, encoding="utf-8", errors="replace").read()
    except Exception:
        continue
    for name in hb:
        stem = name[:-3]
        if name in t or re.search(r"[\"'`/\\]%s\b" % re.escape(stem), t):
            hits_cfg.setdefault(name, set()).add(os.path.relpath(p, ROOT).replace(os.sep, "/"))

# ---------- 3) 最近 30 天日记（"正在用"的表述）----------
cutoff = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
hits_recent = {}
for f in sorted(glob.glob(os.path.join(ROOT, "memory", "2026-*.md"))):
    b = os.path.basename(f)
    if b[:10] < cutoff:
        continue
    try:
        t = open(f, encoding="utf-8", errors="replace").read()
    except Exception:
        continue
    for name in hb:
        stem = name[:-3]
        if re.search(r"(?:运行|执行|调用|跑)\s*[^\n]{0,40}%s" % re.escape(stem), t):
            hits_recent.setdefault(name, set()).add(b)

print()
print("=" * 100)
print("### 安全闸结果（执行面）")
print("=" * 100)
print("  其它脚本调用: %d 件" % len(hits_scripts))
for n, s in list(hits_scripts.items())[:10]:
    print("     %-30s ← %s" % (n[:30], list(s)[0][:88]))
print("  配置文件引用: %d 件" % len(hits_cfg))
for n, s in list(hits_cfg.items())[:10]:
    print("     %-30s ← %s" % (n[:30], ", ".join(sorted(s))[:80]))
print("  最近 30 天日记称正在运行: %d 件" % len(hits_recent))
for n, s in list(hits_recent.items())[:10]:
    print("     %-30s ← %s" % (n[:30], ", ".join(sorted(s))[:70]))

referenced = set(hits_scripts) | set(hits_cfg) | set(hits_recent)
print()
print("  ★ 合计被引用（不得搬）: %d 件 ｜ 可搬: %d 件" % (len(referenced), len(hb) - len(referenced)))

# ---------- 4) 叠加交付状态，出处置计划 ----------
EVI = json.load(open(os.path.join(AUD, "_hb_evidence.json"), encoding="utf-8"))
delivered = set(json.load(open(os.path.join(AUD, "_hb_archive_list.json"), encoding="utf-8")))
dead = set(EVI["ready"])
plan = {}
for n in hb:
    if n in referenced:
        plan[n] = "keep_referenced"
    elif n in delivered:
        plan[n] = "archive_delivered"
    elif n in dead:
        plan[n] = "archive_target_gone"
    else:
        plan[n] = "keep_payload_only"
cnt = {}
for v in plan.values():
    cnt[v] = cnt.get(v, 0) + 1
print()
print("  处置计划: %s" % cnt)
for k in sorted(cnt):
    ex = [n for n, v in plan.items() if v == k][:5]
    print("     %-22s %3d 件  例: %s" % (k, cnt[k], ", ".join(ex)))
json.dump({"plan": plan, "referenced": sorted(referenced),
           "hits_scripts": {k: sorted(v) for k, v in hits_scripts.items()},
           "hits_cfg": {k: sorted(v) for k, v in hits_cfg.items()},
           "hits_recent": {k: sorted(v) for k, v in hits_recent.items()}},
          open(os.path.join(AUD, "_hb_plan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print()
print("  计划落盘: _hb_plan.json")
