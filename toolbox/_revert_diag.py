# -*- coding: utf-8 -*-
"""回退 _split_top 自动修复 + 精确诊断 main 区未闭合的 div"""
import io, os, re, sys, subprocess
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

MK = r'D:\B166ER-openclaw\workspace\toolbox\_mk_xhs9_light.py'
t = open(MK, encoding='utf-8').read()

# 1) 回退：page() 改回简单版，保留 _split_top 函数但不调用
SIMPLE = '''
def page(meta, main):
    return ("<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><title>" + meta + "</title><style>"
            + CSS + "</style></head><body><div class='poster'>"
            + "<div class='top'>" + BTOP + "<div class='meta'>" + meta + "</div></div>"
            + "<div class='main'>" + main + "</div>"
            + "<div class='bottom'><div class='stamp'>酒店 · 财务 · 工具</div>" + BBOT + "</div>"
            + "</div></body></html>")

'''
ps = t.find("def page(meta, main):")
if ps > 0:
    pe = t.find("\n\n", t.find('+ "</div></body></html>")', ps))
    t = t[:ps] + SIMPLE.strip("\n") + t[pe:]
    open(MK, 'w', encoding='utf-8').write(t)
    print('page() 已回退为简单版')

r = subprocess.run([sys.executable, MK], capture_output=True, text=True, encoding='utf-8', errors='replace')
print(r.stdout[-800:])
if r.stderr:
    print('STDERR:', r.stderr[-300:])

# 2) 精确诊断：main 区内未闭合的 div（带 class 与位置）
HTMLD = r'C:\Users\ericz\Desktop\产业发展部\外部相关资料\全面预算管理\小红书9图_预算模板\html'
print('')
print('=== main 区标签诊断 ===')
for f in sorted(os.listdir(HTMLD)):
    if not f.endswith('.html'):
        continue
    h = open(os.path.join(HTMLD, f), encoding='utf-8').read()
    i = h.find("<div class='main'>")
    j = h.find("<div class='bottom'>")
    if i < 0 or j < 0:
        print('  %-18s 边界未找到' % f[:-5]); continue
    core = h[i + 16:j]
    stack = []
    for m in re.finditer(r'<div\b([^>]*)>|</div>', core):
        if m.group(0) != '</div>':
            cls = re.search(r"class='([^']*)'", m.group(1))
            stack.append([cls.group(1) if cls else '?', m.start()])
        else:
            if stack:
                stack.pop()
            else:
                print('  %-18s 多余 </div> @%d' % (f[:-5], m.start())); break
    if stack:
        for s in stack:
            print('  %-18s 未闭合 <div class=%s> 位置@%d  片段: %s' %
                  (f[:-5], s[0], s[1], core[s[1]:s[1] + 110].replace('\n', ' ')))
    else:
        print('  %-18s main 区配平' % f[:-5])
