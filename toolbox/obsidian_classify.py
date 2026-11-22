#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""观察每个桌面文件夹的内容"""
import os
from pathlib import Path

DESK = Path(r"C:\Users\ericz\Desktop")

dirs = [
    "张实项目总控",
    "新媒体产品线",
    "小红书产品线",
    "AHL源代码",
    "AHL专利申请文件",
    "专利",
    "专利补正",
    "软著申请材料-AHL",
    "安逸集团_入职物料_20260707",
    "知局_完整版_v1.0",
    "自我革命",
    "AHL-BP-2026",
    "工作文档",
    "简历及应聘文件",
    "劳动合同",
    "小白的保单",
    "项目资料",
    "图片",
]

for d in dirs:
    p = DESK / d
    if not p.exists():
        continue
    print(f"\n=== {d} ===")
    items = list(p.iterdir())
    subs = [x for x in items if x.is_dir()]
    files = [x for x in items if x.is_file()]
    if subs:
        print(f"  一级子目录 (共 {len(subs)} 个):")
        for s in sorted(subs)[:30]:
            cnt = sum(1 for _ in s.rglob('*') if _.is_file())
            print(f"    [{cnt:4d}] {s.name}")
        if len(subs) > 30:
            print(f"    ...还有 {len(subs)-30} 个")
    if files:
        print(f"  直接文件 (共 {len(files)} 个):")
        for f in sorted(files)[:30]:
            sz = f"{f.stat().st_size/1024:.0f}KB"
            print(f"    [{sz:>8}] {f.name}")
        if len(files) > 30:
            print(f"    ...还有 {len(files)-30} 个")
