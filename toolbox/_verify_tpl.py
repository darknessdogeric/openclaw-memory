# -*- coding: utf-8 -*-
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document

T = r'C:\Users\ericz\Desktop\产业发展部\战略合作框架协议_通用模板_20261106.docx'
d = Document(T)
print('段落 %d  表格 %d' % (len(d.paragraphs), len(d.tables)))
print()
print('=== 全文（前 34 段 = 使用说明页）===')
for i, p in enumerate(d.paragraphs[:34]):
    t = p.text.strip()
    print('%2d | %s' % (i, (t[:96] + '...') if len(t) > 96 else t))

print()
print('=== 正文关键位置抽查 ===')
for i in (35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 50, 51, 52, 53, 54, 55, 93, 94, 95):
    if i < len(d.paragraphs):
        t = d.paragraphs[i].text.strip()
        if t:
            print('%2d | %s' % (i, t[:100]))

print()
print('=== 占位符清单 ===')
f = ''.join(x.text for x in d.paragraphs)
import re
ph = sorted(set(re.findall(r'【[^】]+】', f)))
for p in ph:
    print('  %-24s 出现 %d 次' % (p, f.count(p)))
print()
print('=== 品牌标识残留（必须全 0）===')
for w in ['美团', '三快', '安逸', '91510100MA7DERN160', '横丁字街', '锦江区',
          '四川省旅游投资集团', '本地生活服务平台运营主体', '天津']:
    n = f.count(w)
    print('  %-24s %d %s' % (w, n, 'OK' if n == 0 else '*** 残留 ***'))
