# -*- coding: utf-8 -*-
"""_hb_evidence.py - hb 家族（284 件心跳写入器）内容交付取证
★ 判据：脚本写入的目标文件是否还存在；其内嵌 payload（HB 编号）是否已在目标文件/记忆中
★ 只有"已交付"或"目标文件已不存在"才可归档；未交付的必须保留并标注
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

TARGET = re.compile(r"(?:MEM_PATH|HB_PATH|HEARTBEAT_PATH|MD_PATH|TARGET)\s*=\s*r?['\"]([^'\"]+)['\"]")
HBID = re.compile(r"#(\d{3,5})\b")
ENTRY = re.compile(r'(?:NEW_ENTRY|ENTRY|TEXT|CONTENT)\s*=\s*r?["\']{1,3}(.*?)["\']{1,3}\s*\n', re.S)

rows = []
for p in sorted(glob.glob(os.path.join(TB, "hb*.py"))):
    b = os.path.basename(p)
    try:
        t = open(p, encoding="utf-8", errors="replace").read()
    except Exception:
        continue
    tgts = TARGET.findall(t)
    ids = sorted(set(HBID.findall(t)))
    ent = ENTRY.search(t)
    payload = ""
    if ent:
        payload = re.sub(r"\s+", " ", ent.group(1)).strip()
    # 目标文件是否还在（把绝对路径落到本机实际位置）
    real = []
    for g in tgts:
        q = g
        if q.lower().startswith("d:\\b166er-openclaw"):
            q = os.path.join(ROOT, q.split("\\", 2)[-1]) if "\\" in q[15:] else q
        q2 = q.replace("D:\\B166ER-OpenClaw", ROOT).replace("D:\\B166ER-openclaw", ROOT)
        real.append((g, os.path.exists(q2)))
    rows.append({"file": b, "bytes": os.path.getsize(p), "targets": real,
                 "hb_ids": ids, "payload_head": payload[:150]})

print("=" * 100)
print("### A. hb 家族内容交付取证（%d 件）" % len(rows))
print("=" * 100)
no_target = [r for r in rows if not r["targets"]]
dead = [r for r in rows if r["targets"] and all(not ex for _, ex in r["targets"])]
alive = [r for r in rows if r["targets"] and any(ex for _, ex in r["targets"])]
print("  无目标路径声明: %d ｜ 目标文件已不存在: %d ｜ 目标文件仍存在: %d"
      % (len(no_target), len(dead), len(alive)))
tg = {}
for r in rows:
    for g, ex in r["targets"]:
        tg.setdefault(os.path.basename(g), [0, 0])
        tg[os.path.basename(g)][0 if ex else 1] += 1
print("  目标文件分布（存在/已消失）：")
for k, (a, b) in sorted(tg.items(), key=lambda x: -(x[1][0] + x[1][1]))[:12]:
    print("     %-34s 存在 %3d ｜ 已消失 %3d" % (k[:34], a, b))

print()
print("=" * 100)
print("### B. payload 是否已落进记忆/心跳文件（抽样 6 件逐字核对）")
print("=" * 100)
checked = 0
for r in alive[:6]:
    g, ex = next(((a, b) for a, b in r["targets"] if b), (None, False))
    if not g:
        continue
    q = g.replace("D:\\B166ER-OpenClaw", ROOT).replace("D:\\B166ER-openclaw", ROOT)
    try:
        content = open(q, encoding="utf-8", errors="replace").read()
    except Exception:
        continue
    ids = r["hb_ids"]
    hit = [i for i in ids if ("#" + i) in content]
    key = (r["payload_head"][:40] or "（无payload）")
    print("  %-30s → %s" % (r["file"][:30], os.path.basename(q)))
    print("     HB id %s ｜ 目标文件中命中 %s ｜ payload 首 40 字命中=%s"
          % (ids[:3], hit or "无", (key in content.replace("\n", " ")) if key != "（无payload）" else "—"))
    checked += 1

print()
print("=" * 100)
print("### C. 归档资格判定")
print("=" * 100)
ready = [r for r in rows if not r["targets"] or all(not ex for _, ex in r["targets"])]
need = [r for r in rows if r["targets"] and any(ex for _, ex in r["targets"])]
print("  可归档（无目标声明 或 目标文件已消失）: %d 件" % len(ready))
print("  需保留（目标文件仍在）: %d 件" % len(need))
if need:
    tg2 = {}
    for r in need:
        for g, ex in r["targets"]:
            if ex:
                tg2[os.path.basename(g)] = tg2.get(os.path.basename(g), 0) + 1
    print("  需保留的目标分布:", ", ".join("%s(%d)" % (k[:26], v) for k, v in sorted(tg2.items(), key=lambda x: -x[1])[:8]))
out = os.path.join(ROOT, "output", "audit_skills", "_hb_evidence.json")
json.dump({"rows": rows, "ready": [r["file"] for r in ready], "need_keep": [r["file"] for r in need]},
          open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("  取证落盘:", os.path.basename(out))
