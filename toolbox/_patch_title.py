# -*- coding: utf-8 -*-
"""封面大标题改为「酒店全面预算管理工具」，并同步 kicker 与导语口径"""
import io, os, re, sys, subprocess
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

MK = r'D:\B166ER-openclaw\workspace\toolbox\_mk_xhs9_v3.py'
t = open(MK, encoding='utf-8').read()

REPL = [
 # 封面主标题
 (">酒店经营<br>预算模板<br><em>空白模板 v1.0</em></h1>",
  ">酒店全面<br>预算管理工具<br><em>空白模板 v1.0</em></h1>"),
 # 封面 kicker
 ("\"<div class='kicker'>集团酒店经营预算 · 空白模板 V1.0</div>\"",
  "\"<div class='kicker'>集团全面预算管理 · 空白模板 V1.0</div>\""),
 # 封面导语
 ("\"<p class='lede' style='font-size:19px;max-width:900px'>把集团酒店经营预算，从<b>带着一家酒店历史数据的旧表</b>，\"",
  "\"<p class='lede' style='font-size:19px;max-width:900px'>把集团酒店全面预算，从<b>带着一家酒店历史数据的旧表</b>，\""),
 # P02 总览导语
 ("\"<p class='lede'>把集团酒店经营预算，从<b>带着一家酒店历史数据的旧表</b>，改成<b>任何一家店都能重算的空白模型</b>。\"",
  "\"<p class='lede'>把集团酒店全面预算，从<b>带着一家酒店历史数据的旧表</b>，改成<b>任何一家店都能重算的空白模型</b>。\""),
]
n = 0
for a, b in REPL:
    if a in t:
        t = t.replace(a, b, 1); n += 1
    else:
        print('!! 未命中: ' + a[:56])
open(MK, 'w', encoding='utf-8').write(t)
print('已替换 %d/%d 处' % (n, len(REPL)))

r = subprocess.run([sys.executable, MK], capture_output=True, text=True, encoding='utf-8', errors='replace')
print(r.stdout[-400:])
if r.stderr:
    print('STDERR:', r.stderr[-300:])
RD = r'D:\B166ER-openclaw\workspace\toolbox\_render_xhs9.py'
r2 = subprocess.run([sys.executable, RD], capture_output=True, text=True, encoding='utf-8', errors='replace')
print(r2.stdout)
if r2.stderr:
    print('STDERR:', r2.stderr[-300:])

# 单独导出封面缩略图供目视
from PIL import Image
P = r'C:\Users\ericz\Desktop\产业发展部\外部相关资料\全面预算管理\小红书9图_预算模板\png\p00_title.png'
im = Image.open(P).convert('RGB')
im.thumbnail((760, 760))
im.save(r'D:\B166ER-openclaw\workspace\tmp\_cover_check.png')
print('封面缩略图', im.size)
