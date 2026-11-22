# -*- coding: utf-8 -*-
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import docx
md = r'C:\Users\ericz\Desktop\2026-10-27_安逸集团新媒体业务整体诊断报告_v1.0.md'
dx = r'C:\Users\ericz\Desktop\2026-10-27_安逸集团新媒体业务整体诊断报告_v1.0.docx'
kb = r'D:\B166ER-openclaw\workspace\anyi-ops-kb\04_方法论\2026-10-27_安逸集团新媒体业务整体诊断报告_v1.0.md'
d = docx.Document(dx)
f = ''.join(x.text for x in d.paragraphs) + chr(10) + ''.join(c.text for t in d.tables for r in t.rows for c in r.cells)
print('DOCX %.1f KB  PARAS %d  TABLES %d  CHARS %d' % (os.path.getsize(dx)/1024, len(d.paragraphs), len(d.tables), len(f)))
print('KB copy: %s (%d B)' % (os.path.exists(kb), os.path.getsize(kb) if os.path.exists(kb) else 0))
print()
print('--- 章节 ---')
for k in ['摘要','一、采集基础','二、矩阵现状','三、投入结构','四、预算结构','五、渠道结构','六、内容能力','七、与集团战略的三处脱节','八、国堰专项','九、诊断结论','十、行动建议','附录A','附录B','附录C']:
    print('  %-22s %s' % (k, 'OK' if k in f else 'MISSING'))
print()
print('--- 关键数字 ---')
for k in ['26.8%','47%','3,877','3,000 元','132,800','133 倍','0.01%','15% OTA','123','7.5%','96,000','36,800','34.86%']:
    print('  %-12s %s' % (k, 'OK' if k in f else 'MISSING'))
print()
print('--- 台账行数 / 判定 ---')
print('  台账酒店行: %d' % sum(1 for ln in f.split(chr(10)) if ln.startswith('| ') and ('人 |' in ln or '扫描件' in ln)))
print('  古尔沟判定: %s' % ('OK' if '有(未填数)' in f else 'MISSING'))
print('  扫描件标注: %d 处' % f.count('无文本层'))
print()
print('--- 置信度标注完整性 ---')
for e in ['🟢🟢','🟠🟠','🔴🔴','🟡🟡']:
    print('  %s x%d' % (e, f.count(e)))