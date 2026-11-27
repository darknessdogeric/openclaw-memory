# -*- coding: utf-8 -*-
"""_hb_safety.py - hb 家族归档前安全闸

★ 查：是否被自动化配置 / cron / openclaw.json / 其它脚本引用
★ 被引用的一律不搬（保留在原位），只把未引用的搬进归档区
"""
import io
import sys
import os
import re
import glob
import json

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

# ---- 1. 配置面扫描（自动化 / cron / openclaw.json）----
CONFIG_DIRS = [
    os.path.join(ROOT, ".."),
    os.path.join(HOME, ".openclaw"),
    os.path.join(HOME, ".claude"),
    os.path.join(ROOT, "toolbox"),
]
scan_ext = (".json", ".yaml", ".yml", ".toml", ".js", ".ps1", ".bat", ".sh", ".md", ".py")
cfg_hits = {}
files_scanned = 0
for d in CONFIG_DIRS:
    if not os.path.isdir(d):
        continue
    for base, dirs, fs in os.walk(d):
        dirs[:] = [x for x in dirs if x not in
                   ("node_modules", ".git", "__pycache__", ".chroma_db", "venv", ".venv", "output")]
        for f in fs:
            if not f.endswith(scan_ext):
                continue
            p = os.path.join(base, f)
            if os.path.dirname(p) == TB and f in hb:
                continue  # 自身跳过
            try:
                if os.path.getsize(p) > 3_000_000:
                    continue
                t = open(p, encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            files_scanned += 1
            for name in hb:
                stem = name[:-3]
                # 只认"像路径或命令的引用"，避免正文提及
                if (name in t) or re.search(r"(?:^|[\s\"'`/])%s(?:\s|$|[\"'])" % re.escape(stem), t):
                    cfg_hits.setdefault(name, set()).add(os.path.relpath(p, ROOT).replace(os.sep, "/"))
print()
print("=" * 100)
print("### 配置面引用扫描（%d 个文件）" % files_scanned)
print("=" * 100)
print("  被引用（不得搬）: %d 件" % len(cfg_hits))
for name, srcs in sorted(cfg_hits.items()):
    print("     %-34s ← %s" % (name[:34], ", ".join(sorted(srcs)[:2])))

json.dump({k: sorted(v) for k, v in cfg_hits.items()},
          open(os.path.join(AUD, "_hb_referenced.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

free = [n for n in hb if n not in cfg_hits]
print()
print("  未被任何配置引用: %d 件" % len(free))
json.dump(free, open(os.path.join(AUD, "_hb_free.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- 2. 交付状态叠加 ----
EVI = json.load(open(os.path.join(AUD, "_hb_evidence.json"), encoding="utf-8"))
delivered = set(json.load(open(os.path.join(AUD, "_hb_archive_list.json"), encoding="utf-8")))
dead = set(EVI["ready"])
plan = {}
for n in hb:
    if n in cfg_hits:
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
json.dump(plan, open(os.path.join(AUD, "_hb_plan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k in cnt:
    ex = [n for n, v in plan.items() if v == k][:6]
    print("     %-24s %3d 件  例: %s" % (k, cnt[k], ", ".join(ex)))
