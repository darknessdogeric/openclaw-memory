#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""详细盘点 vault 报告 vs HEARTBEAT 该有的报告"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")
WORKSPACE = Path(r"D:\B166ER-OpenClaw\workspace")

# ===== 1. vault 当前报告 =====
print("=" * 70)
print("VAULT 当前报告 (按大小排序)")
print("=" * 70)
report_dir = VAULT / "20-我们共同维护的" / "报告"
if report_dir.exists():
    for f in sorted(report_dir.glob("*.md"), key=lambda x: -x.stat().st_size):
        print(f"  {f.name}  ({f.stat().st_size/1024:.1f}KB)")

# ===== 2. workspace 报告 =====
print("\n" + "=" * 70)
print("WORKSPACE reports/ 全部 (源文件)")
print("=" * 70)
ws_reports = WORKSPACE / "reports"
if ws_reports.exists():
    for f in sorted(ws_reports.glob("*.md"), key=lambda x: -x.stat().st_size):
        in_vault = "✓" if (report_dir / f.name).exists() else "❌"
        print(f"  {in_vault} {f.name}  ({f.stat().st_size/1024:.1f}KB)")

# ===== 3. 记忆中的大文件（可能包含报告内容） =====
print("\n" + "=" * 70)
print("MEMORY 中的大文件 (>10KB，可能含报告)")
print("=" * 70)
mem_dir = WORKSPACE / "memory"
if mem_dir.exists():
    big = sorted([f for f in mem_dir.glob("*.md") if f.stat().st_size > 10000],
                 key=lambda x: -x.stat().st_size)[:15]
    for f in big:
        in_vault = "✓" if (VAULT / "01-日记" / f.name).exists() else "❌"
        print(f"  {in_vault} {f.name}  ({f.stat().st_size/1024:.1f}KB)")

# ===== 4. 关键节日报告应该有的清单 =====
print("\n" + "=" * 70)
print("HEARTBEAT 该有的报告清单 (从 HEARTBEAT.md 解析)")
print("=" * 70)
EXPECTED = [
    # 春节
    ("春节预测", "2026-01 春节预测报告", "T-2"),
    ("春节复盘", "2026-02 春节复盘报告", "T+7"),
    # 5 月月度
    ("5月月度报告", "2026-05-12 5月月度报告", "T+月末"),
    # 五一
    ("五一预测", "2026-04-28-30 五一预测报告", "T-2"),
    ("五一复盘 T+7", "2026-05-12 五一复盘 T+7", "T+7"),
    ("五一 STR 补充", "2026-05-19 五一 STR 补充复盘", "T+14"),
    # 端午
    ("端午预测", "2026-06-17 端午预测报告", "T-2"),
    ("端午复盘", "2026-06-30 端午复盘 T+9", "T+9"),
    ("端午 STR 补充", "2026-07-07 端午 STR 补充复盘", "T+16"),
    # 暑期
    ("暑期预测", "2026-06-25 暑期预测报告", "T-6"),
    ("暑期复盘", "2026-09-10 暑期复盘 T+12", "T+12"),
    # 中秋
    ("中秋预测", "2026-09-23 中秋预测", "T-2"),
    # 十一
    ("十一预测", "2026-09-29 十一预测", "T-2"),
    # 月度
    ("4月月度报告", "2026-04 月度报告", "T+月末"),
    ("6月月度报告", "2026-06 月度报告", "T+月末"),
    # Q2 半年分析
    ("Q2 半年分析", "2026-07-01 Q2 半年分析", "T+月末"),
    # 行业双周
    ("行业双周报", "每 14 天 10:00", "定期"),
]
for event, name, when in EXPECTED:
    print(f"  {event:20s}  {name:35s}  [{when}]")
