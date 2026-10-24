# -*- coding: utf-8 -*-
"""
apply_routing.py - 把 routing_update_needed.json 的新增路由写入
skills/knowledge-base/SKILL.md 的路由决策表（追加区，幂等）。
"""
import json, sys, re
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

WS = Path(r"D:\B166ER-openclaw\workspace")
JSON_PATH = WS / "memory" / "routing_update_needed.json"
SKILL = WS / "skills" / "knowledge-base" / "SKILL.md"
MARKER = "<!-- AUTO-ROUTING:BEGIN -->"
MARKER_END = "<!-- AUTO-ROUTING:END -->"

data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
routes = data["routing_table"]

# 只收录有明确语义归类的（排除"未分类"）
usable = [r for r in routes if r["semantic"] != ["未分类"]]
usable.sort(key=lambda r: (r["semantic"][0], r["name"]))

groups = {}
for r in usable:
    groups.setdefault(r["semantic"][0], []).append(r)

lines = []
lines.append(MARKER)
lines.append("")
lines.append(f"## 路由决策表 · 自动增量（{data['generated_at']}）")
lines.append("")
lines.append(f"> 由 `kb_routing_table.py` 自动生成，纳入 {len(usable)} 个新 KB 文件。")
lines.append("> 语义列可直接匹配任务意图；文件名含版本号时以最新版为准。")
lines.append("")
lines.append("| 语义类型 | KB 文件 | 触发词 |")
lines.append("|---------|---------|--------|")
for sem in sorted(groups.keys()):
    for r in groups[sem]:
        name = r["name"].replace("|", "／")
        trig = "/".join(sem.split("/"))
        lines.append(f"| {sem} | `{name}` | {trig} |")
lines.append("")
lines.append(MARKER_END)

block = "\n".join(lines)

text = SKILL.read_text(encoding="utf-8")
if MARKER in text:
    pre = text.split(MARKER)[0]
    post = text.split(MARKER_END)[-1]
    new_text = pre + block + post
    action = "replaced"
else:
    new_text = text.rstrip() + "\n\n---\n\n" + block
    action = "appended"

SKILL.write_text(new_text, encoding="utf-8")
print(f"[apply] {action}: {SKILL}")
print(f"[apply] 写入路由 {len(usable)} 条 / {len(groups)} 个语义类")
for sem, rs in sorted(groups.items()):
    print(f"   {sem}: {len(rs)}")
skipped = len(routes) - len(usable)
print(f"[apply] 跳过未分类 {skipped} 条（保留在 routing_update_needed.json 待人工确认）")
