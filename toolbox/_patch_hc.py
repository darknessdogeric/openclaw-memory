# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = r'D:\B166ER-openclaw\workspace\toolbox\_xmt_assemble2.py'
t = open(P, encoding='utf-8').read()
old = """def hc(r):
    f = r.get('fulltime') or ''
    n = r.get('hc') or ''
    m = re.search(r'(\\d+)', n)
    if m: return m.group(1) + '人'
    if '否' in f:
        i = f.find('否')
        if not any(c in f[max(0,i-3):i] for c in CHK): return '0人'
    if any(c in f for c in CHK): return '未填'
    return '未填'"""
new = """def hc(r):
    f = r.get('fulltime') or ''
    n = r.get('hc') or ''
    m = re.search(r'(\\d+)', n)
    if m: return m.group(1) + '人'
    def pre(k):
        i = f.find(k)
        return any(c in f[max(0,i-3):i] for c in CHK) if i >= 0 else False
    if pre('是'): return '有(未填数)'
    if pre('否'): return '0人'
    return '未填'"""
assert old in t, 'anchor missing'
t = t.replace(old, new)
open(P, 'w', encoding='utf-8').write(t)
print('hc() 已修正')