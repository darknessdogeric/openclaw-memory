# -*- coding: utf-8 -*-
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
D = r"C:\Users\ericz\self-improving"
p = os.path.join(D, "rules_OpenClaw配置与自动化踩坑_v1.0_2026-10-24.md")
t = open(p, encoding="utf-8", errors="replace").read()
print("=" * 92); print("### cron 配置范式（权威）"); print("=" * 92)
print(t[:7000])
