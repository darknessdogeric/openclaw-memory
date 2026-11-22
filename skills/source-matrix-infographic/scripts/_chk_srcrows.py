# -*- coding: utf-8 -*-
"""_chk_srcrows.py - 逐源表口径核对（独立校验脚本）

用途：验证 79 源排查总表的逐源表解析结果与官方总表一致
      —— 类别数、每类条目数、合计编号行、逐类取得率
★ 校验点（都是踩过的坑）：
   1) 13 个类码必须齐备（A–M）
   2) J 类必须是 8 条（按标题分段会把 K/L/M 并进 J，J 会变成 26）
   3) 合计 80 个编号行（官方 79 源，A5 与 A2 疑重复故记 80）
   4) 逐类取得率与逐源表行标记一致
用法:
   python skills/source-matrix-infographic/scripts/_chk_srcrows.py
"""
import io
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sm_srcrows as SR
import sm_parse as SP

F79 = SP.F_H79
EXPECT_CLASSES = list("ABCDEFGHIJKLM")
EXPECT_TOTAL = 80
EXPECT_J = 8


def main():
    t = SP.rd(F79)
    if not t:
        print("★ 读不到源表: " + F79)
        return 2
    rows = SR.parse_src_rows(t)
    pc = SR.per_class_rate(rows)
    off = {c["code"]: c["n"] for c in SP.load()["h79_cats"]}

    print("=" * 88)
    print("逐源表口径核对 ｜ " + os.path.basename(F79))
    print("=" * 88)
    print("%-4s %-16s %6s %6s %7s   %s" % ("类", "名称", "条目", "官方", "取得率", "结果分布"))
    print("-" * 88)
    bad = []
    for code in EXPECT_CLASSES:
        d = pc.get(code)
        if not d:
            bad.append(code + " 缺失")
            print("%-4s %-16s %6s %6s %7s" % (code, "(缺)", "-", off.get(code, "-"), "-"))
            continue
        nm = SP.clean(d["rows"][0]["name"])[:16] if d["rows"] else ""
        print("%-4s %-16s %6d %6s %6d%%   %s" % (
            code, nm, d["total"], off.get(code, "-"), d["rate"], d["dist"]))
        if code in off and off[code] != d["total"]:
            bad.append("%s 条目 %d != 官方 %d" % (code, d["total"], off[code]))
    total = sum(len(v) for v in rows.values())
    print("-" * 88)
    print("合计编号行: %d （应为 %d）" % (total, EXPECT_TOTAL))
    if len(rows) != 13:
        bad.append("类别数 %d != 13" % len(rows))
    if total != EXPECT_TOTAL:
        bad.append("合计 %d != %d" % (total, EXPECT_TOTAL))
    jn = pc.get("J", {}).get("total")
    if jn != EXPECT_J:
        bad.append("J 类 %s != %d（标题分段会把它撑到 26）" % (jn, EXPECT_J))
    print()
    if bad:
        print("★ 校验未通过：")
        for b in bad:
            print("   - " + b)
        return 1
    print("✅ 校验通过：13 类齐备 ｜ J 类 8 条 ｜ 合计 80 编号行 ｜ 逐类取得率与逐源表一致")
    return 0


if __name__ == "__main__":
    sys.exit(main())
