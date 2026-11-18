# -*- coding: utf-8 -*-
import io, sys, os, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
p = os.path.join(ROOT,"toolbox","md2docx.py")
t = open(p, encoding="utf-8", errors="replace").read()
print("="*100); print("### A. toolbox/md2docx.py 能力与用法（研判报告版式）"); print("="*100)
print("  %d B ｜ %d 行" % (len(t), t.count("\n")+1))
for i,l in enumerate(t.split("\n")):
    if re.search(r"(def |RE_|FONT|字体|^\s*#\s*-{2,}|__main__|sys\.argv|标题|表格|table|add_)", l):
        print("   L%-4d %s" % (i+1, l[:120]))
print()
print("="*100); print("### B. 字体可用性（宋体/黑体/仿宋/方正小标宋）"); print("="*100)
WIN = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
want = {"宋体":"simsun.ttc","黑体":"simhei.ttf","仿宋":"simfang.ttf","楷体":"simkai.ttf",
        "方正小标宋简体":None,"等线":"Deng.ttf","等线 Light":"Dengb.ttf"}
for name, fn in want.items():
    if fn is None:
        hit = [f for f in glob.glob(os.path.join(WIN,"*")) if "FZ" in os.path.basename(f).upper() or "小标宋" in os.path.basename(f)]
        print("   %-14s %s" % (name, ("可能存在: "+", ".join(os.path.basename(x) for x in hit[:3])) if hit else "★ 未发现（需如实声明）"))
    else:
        ok = os.path.exists(os.path.join(WIN,fn))
        print("   %-14s %s (%s)" % (name, "有" if ok else "★无", fn))
print()
print("="*100); print("### C. 交付位置先例（自我觉醒报告在哪）"); print("="*100)
for f in glob.glob(os.path.join(ROOT,"anyi-ops-kb","04_方法论","*觉醒*")) + glob.glob(os.path.join(ROOT,"anyi-ops-kb","04_方法论","*.md")):
    print("   %8d B  %s" % (os.path.getsize(f), os.path.basename(f)))
