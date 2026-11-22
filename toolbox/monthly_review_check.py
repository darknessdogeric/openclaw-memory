#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
月度复盘报告「缺席检测」脚本 (2026-10-26 新增)

背景：2026-09-26 的月度复盘 cron 静默失败，无任何告警，缺口直到
2026-10-26 复盘时才被发现。机制需要「缺席检测」，不只是「在场检测」。

用法:
    python toolbox/monthly_review_check.py              # 检查当前月 + 上一月
    python toolbox/monthly_review_check.py --quiet      # 仅在异常时输出
    python toolbox/monthly_review_check.py --month 2026-09   # 指定月份

退出码:
    0 = 全部就绪
    1 = 存在缺月（需要补做）
"""

import argparse
import datetime as _dt
import io
import os
import sys

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_DIR = os.path.join(WORKSPACE, "memory")


def report_path(month: str) -> str:
    return os.path.join(MEMORY_DIR, "{0}-月报.md".format(month))


def month_of(dt: _dt.date) -> str:
    return "{0:04d}-{1:02d}".format(dt.year, dt.month)


def prev_month(m: str) -> str:
    y, mm = int(m.split("-")[0]), int(m.split("-")[1])
    y, mm = (y - 1, 12) if mm == 1 else (y, mm - 1)
    return "{0:04d}-{1:02d}".format(y, mm)


def check(month: str):
    p = report_path(month)
    if not os.path.exists(p):
        return {"month": month, "path": p, "ok": False, "size": 0,
                "mtime": None, "note": "缺失"}
    st = os.stat(p)
    mtime = _dt.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M")
    # 空文件视为未生成
    if st.st_size == 0:
        return {"month": month, "path": p, "ok": False, "size": 0,
                "mtime": mtime, "note": "空文件"}
    return {"month": month, "path": p, "ok": True, "size": st.st_size,
            "mtime": mtime, "note": "OK"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--month", default=None, help="YYYY-MM，默认当前月")
    ap.add_argument("--quiet", action="store_true", help="仅异常时输出")
    args = ap.parse_args()

    cur = args.month or month_of(_dt.date.today())
    prev = prev_month(cur)
    targets = [cur, prev]

    results = [check(m) for m in targets]
    missing = [r for r in results if not r["ok"]]

    lines = []
    for r in results:
        flag = "OK " if r["ok"] else "!! "
        lines.append("{0}{1}  {2:>7,} B  {3}  ({4})".format(
            flag, r["month"], r["size"], r["mtime"] or "-", r["note"]))

    if not missing:
        if not args.quiet:
            print("[monthly-review-check] 全部就绪")
            for l in lines:
                print("  " + l)
        return 0

    print("[monthly-review-check] 存在缺月，需补做：")
    for l in lines:
        print("  " + l)
    for r in missing:
        print("  → 补做指引：执行月度自动复盘并写入 {0}".format(r["path"]))
        print("     (cron: B166ER-月度自动复盘 · 每月26日 09:00 Asia/Shanghai)")
    return 1


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.exit(main())
