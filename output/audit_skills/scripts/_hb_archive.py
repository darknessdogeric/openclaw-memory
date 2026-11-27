# -*- coding: utf-8 -*-
"""_hb_archive.py - 执行 hb 家族归档（移动，不删除；可回滚）

★ 依据 _hb_plan.json：
    archive_delivered / archive_target_gone  → 移动到 toolbox/_archive/hb_family_2026-11-18/
    keep_referenced / keep_payload_only      → 留在原位
★ 移动保留原文件全部内容（payload 不丢），清单含 sha256 与回滚路径
"""
import io
import sys
import os
import re
import json
import glob
import shutil
import hashlib
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = r"D:\B166ER-openclaw\workspace"
TB = os.path.join(ROOT, "toolbox")
AUD = os.path.join(ROOT, "output", "audit_skills")
PLAN = json.load(open(os.path.join(AUD, "_hb_plan.json"), encoding="utf-8"))["plan"]
ARC = os.path.join(TB, "_archive", "hb_family_2026-11-18")


def jwrite(p, o):
    d = os.path.dirname(p)
    os.makedirs(d, exist_ok=True)
    fd, t = tempfile.mkstemp(dir=d, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(o, f, ensure_ascii=False, indent=1)
    os.replace(t, p)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]


os.makedirs(ARC, exist_ok=True)
moved, kept = [], []
for name, act in sorted(PLAN.items()):
    src = os.path.join(TB, name)
    if not os.path.exists(src):
        kept.append({"file": name, "action": act, "note": "文件已不在原位（先前已处理）"})
        continue
    if act not in ("archive_delivered", "archive_target_gone"):
        kept.append({"file": name, "action": act, "note": "有引用或目标仍在，留在原位"})
        continue
    dst = os.path.join(ARC, name)
    if os.path.exists(dst):
        continue
    b = open(src, "rb").read()
    h = hashlib.sha256(b).hexdigest()[:16]
    sz = len(b)
    shutil.move(src, dst)
    moved.append({"file": name, "action": act, "bytes": sz, "sha256": h,
                  "from": "toolbox/" + name, "to": os.path.relpath(dst, ROOT).replace(os.sep, "/"),
                  "rollback": "移回 toolbox/" + name})

jwrite(os.path.join(AUD, "hb_family_archive_manifest_2026-11-18.json"),
       {"date": "2026-11-18",
        "rule": "一次性心跳写入器：内容已交付 或 目标文件已消失 → 移动归档（不删除，payload 全保留）",
        "evidence": {
            "delivered_check": "脚本内嵌 HB 编号是否出现在 memory/*.md 与 HEARTBEAT.md",
            "target_check": "脚本声明的目标文件是否仍存在",
            "safety_gate": "是否被其它脚本调用 / 配置文件引用 / 近 30 天日记称正在运行",
        },
        "moved": moved, "kept": kept})

print("=" * 100)
print("### 归档执行结果")
print("=" * 100)
print("  已移动归档: %d 件 → %s" % (len(moved), os.path.relpath(ARC, ROOT).replace(os.sep, "/")))
print("  留在原位: %d 件" % len(kept))
for k in kept:
    print("     %-30s %-22s %s" % (k["file"][:30], k["action"], k["note"]))
tot = sum(m["bytes"] for m in moved)
print("  归档体积: %.1f KB（内容全保留于归档区，可回滚）" % (tot / 1024.0))
left = [os.path.basename(p) for p in glob.glob(os.path.join(TB, "hb*.py"))]
print()
print("  toolbox 根目录剩余 hb* 文件: %d 件" % len(left))
print("   ", ", ".join(left[:10]))
allpy = [p for p in glob.glob(os.path.join(TB, "*.py")) if not os.path.basename(p).startswith("_")]
print("  toolbox 根目录非临时 .py: %d 件（治理前 698）" % len(allpy))
