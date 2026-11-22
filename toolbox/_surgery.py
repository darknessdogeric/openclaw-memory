# -*- coding: utf-8 -*-
import io, sys, os, re, subprocess, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_LINE_SPACING, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

WS = r'D:\B166ER-openclaw\workspace'
KB = os.path.join(WS, 'anyi-ops-kb', '07_战略与改革')
NAME = '2026-11-13_关于安逸酒店集团发展赛道与存量改造路径的指导意见的报告_v1.0'
MD = os.path.join(KB, NAME + '.md')
MD_DESK = r'C:\Users\ericz\Desktop\关于安逸酒店集团发展赛道与存量改造路径的指导意见的报告_20261113.md'
DX = r'C:\Users\ericz\Desktop\关于安逸酒店集团发展赛道与存量改造路径的指导意见的报告_20261113.docx'
CONV = os.path.join(WS, 'skills', 'gongwen-docx-cn', 'scripts', 'md2docx_gongwen.py')

t = open(MD, encoding='utf-8').read()
ch5 = open(os.path.join(WS, 'tmp', '_chapter5.md'), encoding='utf-8').read()
att3 = open(os.path.join(WS, 'tmp', '_att3.md'), encoding='utf-8').read()
print('原文件 %d 字符' % len(t))
print('现有章标题: ' + ' / '.join(l for l in t.split(chr(10)) if re.match(r'^[一二三四五六七八九十]+、[^，。]', l) and len(l) < 30)[:200])

# ---- 1. 文中引用占位（先做，避免与标题混淆）----
for a, b in (('第八章', '@8@'), ('第七章', '@7@'), ('第六章', '@6@'), ('第五章', '@5@')):
    t = t.replace(a, b)
print('引用占位完成')

# ---- 2. 章标题重编号（倒序，避免串号）----
heads = [('八、风险提示', '九、风险提示'), ('七、需集团决策事项', '八、需集团决策事项'),
         ('六、组织与机制保障', '七、组织与机制保障'), ('五、存量改造路径与范式', '六、存量改造路径与范式')]
for a, b in heads:
    if a in t:
        t = t.replace(a, b, 1)
        print('  标题 ' + a + ' -> ' + b)
    else:
        print('  !! 未命中 ' + a)
for a, b in (('@8@', '第九章'), ('@7@', '第八章'), ('@6@', '第七章'), ('@5@', '第六章')):
    t = t.replace(a, b)

# ---- 3. 插入第五章 ----
anchor = '六、存量改造路径与范式'
assert anchor in t, '插入锚点未命中'
t = t.replace(anchor, ch5.strip() + chr(10) + chr(10) + anchor, 1)
print('第五章已插入')

# ---- 4. 第四章指向管道体系 ----
a2 = '（二）轻资产输出的商业条款设计'
if a2 in t:
    t = t.replace(a2, '上述三段收入的结构性来源是集团管道体系，其设计详见第五章。' + chr(10) + chr(10) + a2, 1)
    print('第四章已加指向')
else:
    print('!! 第四章锚点未命中')

# ---- 5. 决策事项第 9 条 ----
a3 = '8. 授权产业发展部就与国际头部品牌的联合品牌方案开展谈判，并按本报告第三、四章的产品与商业条款框架报审。'
if a3 in t:
    t = t.replace(a3, a3 + chr(10) + '9. 同意启动集团管道费体系建设，由产业发展部牵头，用一年时间完成管道归集、定价设计、合同改造与试点验证，并明确管道收入的用途安排原则。', 1)
    print('决策事项已加第 9 条')
else:
    print('!! 决策锚点未命中')

# ---- 6. 风险第六条 ----
a4 = '五是本报告对 2026 年度考核口径的推断尚待确认，相关结论以财务金融部书面口径为准。'
if a4 in t:
    t = t.replace(a4, a4 + chr(10) + '六、管道费体系首次定价必然触动集团与输出业主之间的利益分配，且部分项目名义可选与实质可选并不一致，若沟通不足，容易引发输出业主对集团收费合理性的质疑。', 1)
    print('风险提示已加第六条')
else:
    print('!! 风险锚点未命中')

# ---- 7. 组织保障补管道归口 ----
a5 = '专班按双周调度，重大分歧直报集团。'
if a5 in t:
    t = t.replace(a5, a5 + '专班同步承担管道费体系的归口与口径统一职责。', 1)
    print('组织保障已补管道归口')
else:
    print('!! 组织锚点未命中')

# ---- 8. 附件清单与附件三 ----
a6 = '附件二、存量改造分级与投资上限速查表'
if a6 in t:
    t = t.replace(a6, a6 + chr(10) + '附件三、集团对外输出收费管线清单（必选与可选）', 1)
    print('附件清单已更新')
else:
    print('!! 附件清单锚点未命中')
t = t.rstrip() + chr(10) + att3
print('附件三已追加，总长度 %d 字符' % len(t))

open(MD, 'w', encoding='utf-8').write(t)
shutil.copy2(MD, MD_DESK)
r = subprocess.run([sys.executable, CONV, MD, DX], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('公文转换:', (r.stdout or '').strip(), (r.stderr or '').strip()[:160])

d = Document(DX)
n = 0; sg = 0
for p in d.paragraphs:
    tx = p.text.strip()
    if p.alignment is not None and str(p.alignment).endswith('CENTER'):
        continue
    pf = p.paragraph_format
    pf.line_spacing = Pt(28)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    n += 1
    if tx == '安逸酒店集团产业发展部' or re.match(r'^\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日$', tx):
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        pf.first_line_indent = None
        sg += 1
d.save(DX)
shutil.copy2(DX, os.path.join(KB, NAME + '.docx'))
print('行距校准 %d 段，落款右对齐 %d 处' % (n, sg))

d2 = Document(DX)
full = ''.join(p.text for p in d2.paragraphs) + chr(10) + ''.join(cl.text for tb in d2.tables for rr in tb.rows for cl in rr.cells)
print()
print('DOCX %.1f KB  段落 %d  表格 %d' % (os.path.getsize(DX)/1024, len(d2.paragraphs), len(d2.tables)))
print('粗体残留: %s' % ('有' if '**' in full else '无'))
CK = ['五、集团化管道费用体系建设', '六、存量改造路径与范式', '七、组织与机制保障', '八、需集团决策事项', '九、风险提示',
 '附件三', '管道体系的三层结构', '收益管理', '代收代付', '名义可选', '接入层', '主干层', '增值层',
 '市场推广费、品牌营销基金', '管道收入要么回流体系化的品宣', '管道费体系的四步工作', '管道收入规模及结构',
 '属结构性来源是集团管道体系', '详见第五章', '见第六章', '同意启动集团管道费体系建设',
 '管道费体系首次定价必然触动', '专班同步承担管道费体系的归口', '集团对外输出收费管线清单', '与第三个订单无关']
miss = 0
for k in CK:
    ok = k in full
    if not ok:
        miss += 1
    print('  %-32s %s' % (k, 'OK' if ok else 'MISSING'))
print()
print('缺项 %d' % miss)
print('章节序列: ' + ' / '.join(p.text.strip()[:16] for p in d2.paragraphs if re.match(r'^[一二三四五六七八九十]+、[^，。]', p.text.strip()) and len(p.text.strip()) < 26))