# -*- coding: utf-8 -*-
"""述职报告产发部补充：只补源文件已列事项的进展，不新增事项、不重复"""
import io, sys, os, re, copy, zipfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn

SRC = r'C:\Users\ericz\Desktop\安逸酒店集团有限责任公司2025年度经理层向董事会述职报告（待补充批注版）20261028.docx'
DST = r'C:\Users\ericz\Desktop\安逸酒店集团有限责任公司2025年度经理层向董事会述职报告（产发部已补充版）20261028.docx'

# ---------- P52：深耕高净值客群价值 ----------
# 原文要素：动/静体验产品｜健身房社交空间联名产品｜品质生活场景｜跨界合作｜内部多元消费场景｜黏性复购
P52 = [
    '【补充】一是“静”的产品化落地。以都江堰国堰宾馆为载体，该店2026年1至10月实现营业收入1296.09万元，餐饮、会议等非房收入占比44.66%，已形成“客房＋餐饮＋会议＋温泉”复合收入结构；改造以“品牌重塑＋文化主题轻量改造＋策展联营＋数智化体系穿透”为主线推进，已汇总5家专业机构方案，计划11月15日前形成整体方案，改造后第1年目标出租率50%至55%、平均房价280至320元、RevPAR 140至176元。',
    '二是“动”的场景延伸。以三岔湖项目为载体，与成都体育学院就运动休闲、运动培训等资源开展对接，对方已组织多个学院赴现场调研，“动”的方向先从运动客群与场地联动切入。',
    '三是联名产品与多元消费场景落地。与成都大景以智能电视合作方式置换其3万间客房屏幕展示资源；与商投集团天府优选、蒙顶山茶业公司推进二销模块化货架，点位互换已落地总府皇冠、双流机场两处，酒店内部零售消费场景实现实体化。',
    '四是客户黏性与复购支撑。“安逸会”积分体系方案已形成并提交审议，会员直销贯通后可减少15%的OTA中介费用。',
]

# ---------- P54：释放重点项目效能 ----------
# 原文要素：锦绣天府号改造路测投运｜省农科院海南分院合资公司｜四川宾馆等改造与一店一档｜巴蜀文旅走廊与重庆文旅协同
P54 = [
    '【补充】一是旅游列车投运见效。“锦绣天府号”已于5月19日正式运营，18节车厢、可承载92名乘客，第二季度款项已到账；目前正推进成铁商旅三方协议落地，已与重庆文旅集团旗下心已远旅行社完成列车产品对接，并与爱达邮轮形成宣推置换，运营方落地与宣发内容同步完善。',
    '二是巴蜀文旅走廊协同落地。与重庆文旅集团已签署会员互通协议并进入测试；列车、游轮、酒店相互租赁三个方向同步推进，其中酒店相互租赁涉及的成都渝州宾馆与重庆四川宾馆计划年底前各自完成投资决策；厨艺技能比赛由重庆文旅主导推进。',
    '三是重点改造项目按节点实施。国堰宾馆文化主题改造已完成5家机构方案汇总；总府皇冠假日酒店改造已完成现场调研与需求清单编制，按11月2日回收信息清单、11月7日形成决策包推进三方向比选；古尔沟华美达酒店品牌授权即将到期，同步推进整体租赁、破产重整与外部品牌合作三条路径比选。',
    '四是“一店一档”建立基础档案。以集团新媒体账号现状采集为切口，已完成19家酒店逐店基础数据采集与建档，为老旧酒店改造台账、权属瑕疵化解和“应改尽改”提供底层数据支撑。',
]
P54_MARK = '（待资产部核对补充）'

d = Document(SRC)
paras = d.paragraphs


def strip_marker(p):
    texts = [r.text for r in p.runs]
    joined = ''.join(texts)
    k = joined.find('（待')
    if k < 0:
        return None, 0
    pos = 0
    victims = []
    for i, t in enumerate(texts):
        if pos + len(t) > k:
            victims.append(i)
        pos += len(t)
    gone = ''.join(texts[i] for i in victims)
    for i in reversed(victims):
        p._element.remove(p.runs[i]._element)
    return gone, len(victims)


def body_rpr(p):
    for r in p.runs:
        rpr = r._element.find(qn('w:rPr'))
        if rpr is None:
            continue
        if rpr.find(qn('w:highlight')) is not None:
            continue
        return copy.deepcopy(rpr)
    return None


def add_text(p, text, template, highlight=None, color=None):
    r = p.add_run(text)
    if template is not None:
        old = r._element.find(qn('w:rPr'))
        if old is not None:
            r._element.remove(old)
        r._element.insert(0, copy.deepcopy(template))
        rpr = r._element.find(qn('w:rPr'))
        for tag in (qn('w:highlight'), qn('w:color')):
            el = rpr.find(tag)
            if el is not None:
                rpr.remove(el)
    if highlight or color:
        rpr = r._element.get_or_add_rPr()
        if highlight:
            rpr.append(rpr.makeelement(qn('w:highlight'), {qn('w:val'): highlight}))
        if color:
            rpr.append(rpr.makeelement(qn('w:color'), {qn('w:val'): color}))
    return r


for idx, blocks in ((52, [(t, None, None) for t in P52]),
                    (54, [(t, None, None) for t in P54] + [(P54_MARK, 'yellow', 'FF0000')])):
    p = paras[idx]
    gone, cnt = strip_marker(p)
    tpl = body_rpr(p)
    for txt, hl, col in blocks:
        add_text(p, txt, tpl, hl, col)
    print('P%d: 删除标记 %d run（%s），追加 %d 段' % (idx, cnt, gone, len(blocks)))

d.save(DST)
print('已保存: %s' % os.path.basename(DST))

# ---------- 校验 ----------
a = {n for n in zipfile.ZipFile(SRC).namelist() if not n.endswith('/')}
b = {n for n in zipfile.ZipFile(DST).namelist() if not n.endswith('/')}
print('部件 %d -> %d，丢失 %s' % (len(a), len(b), ', '.join(sorted(a - b)) or '无'))

d2 = Document(DST)
P = d2.paragraphs
print()
print('=== 全文待补充标记（%d 处，均为其他部门）===' % sum(1 for p in P if re.search(r'（待[^）]*）', p.text)))
for i, p in enumerate(P):
    m = re.findall(r'（待[^）]*）', p.text)
    if m:
        print('  P%-3d %s' % (i, ' | '.join(m)))

print()
print('=== 字体核验（异常应�� 0）===')
for idx in (52, 54):
    bad = 0
    for r in P[idx].runs:
        rpr = r._element.find(qn('w:rPr'))
        ea = sz = hl = None
        if rpr is not None:
            f = rpr.find(qn('w:rFonts'))
            if f is not None:
                ea = f.get(qn('w:eastAsia'))
            h = rpr.find(qn('w:highlight'))
            if h is not None:
                hl = h.get(qn('w:val'))
            s = rpr.find(qn('w:sz'))
            if s is not None:
                sz = int(s.get(qn('w:val'))) / 2.0
        if hl != 'yellow' and (ea != '仿宋_GB2312' or sz != 16.0):
            bad += 1
    pf = P[idx].paragraph_format
    print('  P%d  异常run=%d  缩进=%s 行距=%s  长度=%d' % (idx, bad, pf.first_line_indent, pf.line_spacing, len(P[idx].text)))

print()
print('=== P52 补充全文 ===')
print(P[52].text[P[52].text.index('【补充】'):])
print()
print('=== P54 补充全文 ===')
print(P[54].text[P[54].text.index('【补充】'):])
