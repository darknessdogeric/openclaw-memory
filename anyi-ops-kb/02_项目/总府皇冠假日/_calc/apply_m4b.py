# -*- coding: utf-8 -*-
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
B = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
P = os.path.join(B, "_calc", "apply_m4.py")
src = open(P, encoding="utf-8").read()
i = src.index('BLK = """'); j = src.index('"""', i + 9)
BLK = src[i + 9:j]

def fn(s):
    h = [f for f in os.listdir(B) if f.startswith("总府皇冠改造_综合改造报告_") and s in f]
    if not h: raise SystemExit("NOT FOUND " + s)
    return os.path.join(B, h[0])

edits = []
cur = None; state = None; oldl = []; newl = []
def flush():
    global cur, oldl, newl
    if cur is not None and oldl:
        edits.append((cur, "\n".join(oldl), "\n".join(newl)))
    cur = None; oldl = []; newl = []; state = None

for line in BLK.split("\n"):
    if line.startswith("###FILE:"):
        flush(); cur = line[8:].strip()
    elif line == "###OLD":
        flush(); state = "old"; oldl = []
    elif line == "###NEW":
        state = "new"; newl = []
    elif state == "old":
        oldl.append(line)
    elif state == "new":
        newl.append(line)
flush()

print(f"解析到 {len(edits)} 条替换")
ok = fail = 0
for suffix, o, n in edits:
    p = fn(suffix)
    t = open(p, encoding="utf-8").read()
    c = t.count(o)
    if c != 1:
        print(f"  [SKIP x{c}] {suffix} :: {o[:40]!r}"); fail += 1; continue
    open(p, "w", encoding="utf-8").write(t.replace(o, n, 1))
    print(f"  [OK] {suffix} :: {o[:40]}"); ok += 1
print(f"\n替换: {ok} 成功 / {fail} 未命中")