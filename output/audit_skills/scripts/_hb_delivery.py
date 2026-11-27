# -*- coding: utf-8 -*-
"""_hb_delivery.py - hb 家族内容是否已交付到记忆层（逐件核对 HB 编号）

★ 判据：该脚本内嵌的 HB 编号（#NNNN）是否出现在 memory/*.md 或 HEARTBEAT.md 中
★ 命中 = 内容已交付 → 可归档（移动，不删除）
★ 未命中 = 内容可能只存在于脚本里 → 保留，且把 payload 单独留档
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
TB = os.path.join(ROOT, "toolbox")
AUD = os.path.join(ROOT, "output", "audit_skills")

HBID = re.compile(r"#\s?(\d{3,5})\b")
ENTRY = re.compile(r'(?:NEW_ENTRY|ENTRY|TEXT|CONTENT|BODY)\s*=\s*r?["\']{1,3}(.*?)["\']{1,3}\s*(?:\n|$)', re.S)

# 记忆层语料
corpus_files = []
for pat in (os.path.join(ROOT, "memory", "*.md"),
            os.path.join(ROOT, "HEARTBEAT.md"),
            os.path.join(ROOT, "memory", "**", "*.md")):
    corpus_files += glob.glob(pat, recursive=True)
corpus_files = sorted(set(corpus_files))
blob = []
for f in corpus_files:
    try:
        blob.append(open(f, encoding="utf-8", errors="replace").read())
    except Exception:
        pass
BLOB = "\n".join(blob)
print("记忆层语料: %d 个文件 / %d 字符" % (len(corpus_files), len(BLOB)))

rows = []
for p in sorted(glob.glob(os.path.join(TB, "hb*.py"))):
    b = os.path.basename(p)
    try:
        t = open(p, encoding="utf-8", errors="replace").read()
    except Exception:
        continue
    ids = sorted(set(HBID.findall(t)))
    ent = ENTRY.search(t)
    payload = re.sub(r"\s+", " ", ent.group(1)).strip() if ent else ""
    hits = [i for i in ids if ("#" + i) in BLOB]
    rows.append({"file": b, "bytes": os.path.getsize(p), "hb_ids": ids,
                 "payload": payload[:600], "delivered": bool(hits), "matched": hits})

delivered = [r for r in rows if r["delivered"]]
undelivered = [r for r in rows if not r["delivered"]]
print()
print("=" * 100)
print("### 交付核对结果")
print("=" * 100)
print("  已交付（HB 编号在记忆层命中）: %d 件" % len(delivered))
print("  未交付（编号未命中，payload 可能只存在脚本里）: %d 件" % len(undelivered))
if undelivered:
    print("  ★ 未交付样例:")
    for r in undelivered[:8]:
        print("     %-32s ids=%s payload=%s" % (r["file"][:32], r["hb_ids"][:2], (r["payload"] or "（无）")[:56]))

# 未交付的 payload 单独留档（不丢内容）
KEEP = os.path.join(AUD, "_hb_undelivered_payloads.json")
json.dump(undelivered, open(KEEP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print()
print("  未交付 payload 留档:", os.path.basename(KEEP), "(%d 件)" % len(undelivered))

# 归档：仅已交付的 + 目标已消失的
EVI = json.load(open(os.path.join(AUD, "_hb_evidence.json"), encoding="utf-8"))
dead = set(EVI["ready"])
ARCH = os.path.join(AUD, "_hb_archive_list.json")
todo = sorted({r["file"] for r in delivered if r["file"] in dead})
print()
print("  可归档（内容已交付 且 目标已消失）: %d 件" % len(todo))
print("  需保留（未交付 或 目标仍在）: %d 件" % (len(rows) - len(todo)))
json.dump(todo, open(ARCH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("  归档清单落盘:", os.path.basename(ARCH))
