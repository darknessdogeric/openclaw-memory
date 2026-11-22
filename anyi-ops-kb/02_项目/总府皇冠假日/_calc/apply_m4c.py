# -*- coding: utf-8 -*-
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
B = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
src = open(os.path.join(B, "_calc", "apply_m4.py"), encoding="utf-8").read()
i = src.index('BLK = """'); j = src.index('"""', i + 9)
BLK = src[i + 9:j]

def fn(s):
    h = [f for f in os.listdir(B) if f.startswith("总府皇冠改造_综合改造报告_") and s in f]
    if not h: raise SystemExit("NOT FOUND " + s)
    return os.path.join(B, h[0])

edits = []
state = None
cur = None; oldl = []; newl = []
def flush():
    global cur, oldl, newl
    if cur is not None and oldl:
        edits.append((cur, "\n".join(oldl), "\n".join(newl)))
    oldl = []; newl = []

for line in BLK.split("\n"):
    if line.startswith("###FILE:"):
        flush(); cur = line[8:].strip(); state = None
    elif line == "###OLD":
        state = "old"; oldl = []
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
        print(f"  [SKIP x{c}] {suffix} :: {o[:40]}"); fail += 1; continue
    open(p, "w", encoding="utf-8").write(t.replace(o, n, 1))
    print(f"  [OK] {suffix} :: {o[:40]}"); ok += 1
print(f"\n替换: {ok} 成功 / {fail} 未命中")

print("\n=== 校验 ===")
for s in ("第一二部分","第三部分","第四部分","第五部分","第六部分","第七部分","第八部分","第九部分","第十部分"):
    p = fn(s); t = open(p, encoding="utf-8").read()
    a = t.count("84.5 ㎡/间") + t.count("84.5 ㎡/间")
    b = t.count("2026-11-05 修正") + t.count("2026-11-05 数据修正说明")
    c = t.count("351 正常售卖")
    bad = ("###FILE:" in t) or ("###OLD" in t) or ("###NEW" in t)
    print(f"  {s:<10} 84.5标记 {a:>2} | 修正标注 {b:>2} | 351口径 {c:>2} | 残留标记 {'⚠️有' if bad else '无'}")