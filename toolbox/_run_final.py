# -*- coding: utf-8 -*-
"""删除残留的 balance() 调用循环，重出重验"""
import io, os, re, sys, subprocess
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

MK = r'D:\B166ER-openclaw\workspace\toolbox\_mk_xhs9_light.py'
t = open(MK, encoding='utf-8').read()

STALE = """for _k in list(P.keys()):
    _fixed, _note = balance(P[_k])
    if _note != "删多余</div>0 补缺失</div>0":
        P[_k] = _fixed
        print("  配平修复 " + _k + ": " + _note)

"""
if STALE in t:
    t = t.replace(STALE, "", 1)
    open(MK, 'w', encoding='utf-8').write(t)
    print('已删除残留 balance() 调用循环')
else:
    print('未找到残留循环（可能已清理）')

# 确认新 page() 与断言存在
print('page() 顶层切分:', '_split_top' in t)
print('结构断言:', '_check_structure' in t)
print('旧 balance 定义残留:', 'def balance(html):' in t)

r = subprocess.run([sys.executable, MK], capture_output=True, text=True, encoding='utf-8', errors='replace')
print(r.stdout)
if r.stderr:
    print('STDERR:', r.stderr[-500:])

RD = r'D:\B166ER-openclaw\workspace\toolbox\_render_xhs9.py'
r2 = subprocess.run([sys.executable, RD], capture_output=True, text=True, encoding='utf-8', errors='replace')
print(r2.stdout)
if r2.stderr:
    print('STDERR:', r2.stderr[-500:])
