# -*- coding: utf-8 -*-
import io, sys, os, shutil, copy
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC = r'C:\Users\ericz\Desktop\产业发展部\项目\美团本地生活\安逸酒店集团与美团合作框架协议_起草稿_20261029.docx'
OUT = r'C:\Users\ericz\Desktop\安逸酒店集团与美团合作框架协议_双方合作内容补充稿_v2.2_20261031.docx'
COPY_DIRS = [r'C:\Users\ericz\Desktop\产业发展部\项目\美团本地生活',
             r'D:\B166ER-openclaw\workspace\anyi\anyi-ops-kb\02_项目\安逸×美团本地生活合作']

NEW_CLAUSE = ('7．双方平台资源与会员权益合作。除本协议前述约定外，乙方应以其充电宝业务平台资源支持甲方会员体系建设与会员增长，'
              '具体包括：（一）在充电宝借宝流程中为甲方提供会员跳转入口及会员积分权益兑换入口；'
              '（二）为甲方所属酒店提供平台侧经营评价指标支持及平台流量资源支持；'
              '（三）按甲方标识要求提供充电宝设备的外观定制服务，并在甲方酒店场景投放；'
              '（四）按国家相关标准及行业通行要求提供充电宝设备的安全与运维售后服务。'
              '甲方负责统筹协调其下属各酒店及三级公司，按照本协议及各专项协议配合乙方完成前述资源的落地实施。'
              '前述资源的具体内容、开通范围、量化标准、数据口径与结算方式，'
              '由甲方下属各酒店或三级公司与乙方授权的业务合作方另行签订专项协议约定。')

FONT = '仿宋_GB2312'

def setfont(run, name, size, bold=False):
    run.font.size = Pt(size); run.font.name = name; run.bold = bold
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts'); rpr.append(rf)
    rf.set(qn('w:eastAsia'), name); rf.set(qn('w:ascii'), 'Times New Roman'); rf.set(qn('w:hAnsi'), 'Times New Roman')

d = Document(SRC)
before = [p.text for p in d.paragraphs]
clause6 = None; target = None
for p in d.paragraphs:
    t = p.text.strip()
    if t.startswith('6．合作酒店清单与专项协议安排'): clause6 = p
    if t.startswith('二、商业秘密'): target = p
assert clause6 is not None and target is not None

np = target.insert_paragraph_before('')
src_pPr = clause6._p.find(qn('w:pPr'))
if src_pPr is not None:
    old = np._p.find(qn('w:pPr'))
    if old is not None: np._p.remove(old)
    np._p.insert(0, copy.deepcopy(src_pPr))
r = np.add_run(NEW_CLAUSE); setfont(r, FONT, 16)

d.save(OUT)
print('saved %d bytes' % os.path.getsize(OUT))
for cd in COPY_DIRS:
    os.makedirs(cd, exist_ok=True)
    shutil.copy2(OUT, os.path.join(cd, os.path.basename(OUT)))

d2 = Document(OUT)
after = [p.text for p in d2.paragraphs]
lost = [x for x in before if x.strip() and x not in after]
added = [x for x in after if x not in before]
print('原稿 %d -> 新稿 %d | 丢失 %d | 新增 %d' % (len(before), len(after), len(lost), len(added)))
for a in added: print('  ADD:', a[:200])
print()
print('--- 第一条条目顺序 ---')
for i, p in enumerate(d2.paragraphs):
    t = p.text.strip()
    if i < 26 and (t.startswith(('一、','二、')) or t[:2] in ('1．','2．','3．','4．','5．','6．','7．') or t.startswith('会员跳转')):
        print('%2d | %s' % (i, t[:46]))
print()
f = ''.join(x.text for x in d2.paragraphs)
for k in ['9:1','原告所在地人民法院','有效期一年','由乙方业务合作方承接全部技术开发与对接工作','设置（）小时免费权益方案','乙方：美团（XXXX）']:
    print('  原文保留 %-30s %s' % (k, 'YES' if k in f else '*** NO ***'))
