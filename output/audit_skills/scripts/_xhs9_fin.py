# -*- coding: utf-8 -*-
import os, sys, shutil, glob
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
KB = "D:/B166ER-openclaw/workspace/anyi-ops-kb/00_全域商业市场认知/01_酒店行业"
mdp = os.path.join(KB, "酒店业全产业链拓扑_小红书9图_v1.0_2026-11-07.md")
print("MD:", os.path.exists(mdp), os.path.getsize(mdp), "B")
d = "C:/Users/ericz/Desktop/小红书_酒店全产业链拓扑_9图v1_2026-11-07"
os.makedirs(d, exist_ok=True)
shutil.copy2(mdp, os.path.join(d, "酒店业全产业链拓扑_小红书9图_文字版.md"))
print("--- 桌面文件夹 ---")
for f in sorted(os.listdir(d)):
    print("   %-56s %6d KB" % (f[:56], os.path.getsize(os.path.join(d, f))//1024))
print("--- KB ---")
for f in sorted(os.listdir(KB)):
    if "拓扑" in f:
        print("   %-52s %8d B" % (f[:52], os.path.getsize(os.path.join(KB, f))))
n = 0
for pat in ["_xhs_topo9.py", "_patch9.py", "_xhs9_deliver.py", "_rd_v6tail.py"]:
    for p in glob.glob(os.path.join("D:/B166ER-openclaw/workspace/memory", pat)):
        try:
            os.remove(p); n += 1
        except Exception:
            pass
print("cleaned temp:", n)
