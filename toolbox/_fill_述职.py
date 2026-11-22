# -*- coding: utf-8 -*-
import io, sys, os, re, copy, zipfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn

SRC = r'C:\Users\ericz\Desktop\安逸酒店集团有限责任公司2025年度经理层向董事会述职报告（待补充批注版）20261028.docx'
DST = r'C:\Users\ericz\Desktop\安逸酒店集团有限责任公司2025年度经理层向董事会述职报告（产发部已补充版）20261028.docx'

P52 = '【补充】一是“静”的载体由单点酒店升级为目的地级度假综合体。都江堰国堰宾馆拥有235间客房、11个温泉汤池、19个会议室及党政机关会议定点资质，2026年1至10月实现营业收入1296.09万元，餐饮、会议等非房收入占比44.66%，已形成“客房＋餐饮＋会议＋温泉”复合收入结构。产业部以“品牌重塑＋文化主题轻量改造＋策展联营＋数智化体系穿透”为主线推进改造，已完成5家专业机构方案汇总，计划11月15日前形成整体方案，改造后第1年目标出租率50%至55%、平均房价280至320元、RevPAR 140至176元。'
P52b = '二是“动”的通道由单一OTA转向商旅直连。已与国网商旅、中青旅商旅、道旅、华为汇通4家差旅管理机构完成对接，协议价设计以集团平台实测平均房价266.80元为基准，纠正了以门市价488元为锚的定价失真；同步推进酒店会员联网与直销通道建设，据测算会员直销贯通可减少15%的OTA中介费用，“安逸会”积分体系方案已形成并提交审议。'
P52c = '三是高净值客群导入建立国际品牌通道。2026年10月27日与悦榕集团完成集团级会谈，悦榕方主动提出“古尔沟悦榕庄”式联合品牌路径；并以峨眉山悦榕庄2700至8000元房价区间形成高净值客群定价参照，为国堰改造及古尔沟项目提供价格锚。'
P52d = '四是跨界合作由单点采购转为平台级协同。完成抖音集团账号后台授权，可获取委托管理与执行项目全量数据；对接小红书本地生活取得酒店类7.5%专属费率；以成都大景3万间客房电视屏资源置换降低弱电投入；联动中国旅游集团西南分公司推进爱达邮轮上架、中免含税商品店铺及境外签证中心点位合作，并依托集团统战资源转化通道拓展港澳台侨及海外客源。'

P54 = '【补充】一是旅游列车项目实现投运见效。自主投资打造的“锦绣天府号”熊猫旅游专列已于5月19日正式运营，18节车厢、可承载92名乘客，第二季度款项已到账；目前正推进成铁商旅三方协议落地，已与重庆文旅集团旗下心已远旅行社完成线路产品对接、与爱达邮轮形成宣推置换，并完成交旅融合大会参展及乌兹别克斯坦参展资料准备，运营方落地与宣发内容同步完善。'
P54b = '二是巴蜀文旅走廊协同形成实质进展。与重庆文旅集团签署会员互通协议并进入测试，列车、游轮、酒店相互租赁三个方向同步推进，成都渝州宾馆与重庆四川宾馆年底前各自完成投资决策；10月27日与中国旅游集团西南分公司完成集团级会谈，明确爱达邮轮产品上架、中免含税商品店铺、境外签证中心点位三项合作方向，并与双方党政培训资源形成互补。'
P54c = '三是重点改造项目按节点推进。都江堰国堰宾馆文化主题改造已完成5家机构方案汇总，计划11月15日前形成整体方案；总府皇冠假日酒店改造完成现场调研与需求清单编制，按11月2日回收信息清单、11月7日形成决策包节点推进三方向比选，并结合与悦榕集团会谈增列联合品牌方向；古尔沟华美达酒店品牌授权即将到期，已同步推进整体租赁、破产重整与外部品牌合作三条路径的方案比选。'
P54d = '四是二销供应链形成落地载体。与商投集团框架协议由产业发展部牵头签订，天府优选与蒙顶山茶业公司已实现总府皇冠、双流机场点位互换；蒙顶山茶业公司承接二销业务，形成模块化货架铺货联营与私域、运营商合作模式，并同步推进跨境业务探索。'
P54e = '（待资产部核对补充）'

d = Document(SRC)
paras = d.paragraphs


def strip_marker(p):
    """删除段末的（待…）标记 run，返回被删文本"""
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
    """取正文（非标记）run 的 rPr 作为模板"""
    for r in p.runs:
        rpr = r._element.find(qn('w:rPr'))
        if rpr is None:
            continue
        hl = rpr.find(qn('w:highlight'))
        if hl is not None:
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
    if highlight:
        rpr = r._element.get_or_add_rPr()
        hl = rpr.makeelement(qn('w:highlight'), {qn('w:val'): highlight})
        rpr.append(hl)
    if color:
        rpr = r._element.get_or_add_rPr()
        co = rpr.makeelement(qn('w:color'), {qn('w:val'): color})
        rpr.append(co)
    return r


for idx, blocks in ((52, [(P52, None, None), (P52b, None, None), (P52c, None, None), (P52d, None, None)]),
                    (54, [(P54, None, None), (P54b, None, None), (P54c, None, None), (P54d, None, None),
                          (P54e, 'yellow', 'FF0000')])):
    p = paras[idx]
    gone, cnt = strip_marker(p)
    tpl = body_rpr(p)
    for txt, hl, col in blocks:
        add_text(p, txt, tpl, hl, col)
    print('P%d: 删除标记 %d 个 run（%s），追加 %d 段' % (idx, cnt, gone, len(blocks)))

d.save(DST)
print()
print('已保存: %s' % DST)

# 校验
z = zipfile.ZipFile(SRC)
zn = zipfile.ZipFile(DST)
src_names = set(z.namelist())
dst_names = set(zn.namelist())
lost = src_names - dst_names
print()
print('原文件部件 %d  新文件部件 %d  丢失 %d' % (len(src_names), len(dst_names), len(lost)))
if lost:
    print('  丢失: ' + ', '.join(sorted(lost)))
print('批注相关部件: ' + ', '.join(sorted([n for n in dst_names if 'comment' in n.lower()])) or '无')

d2 = Document(DST)
p52 = d2.paragraphs[52]
p54 = d2.paragraphs[54]
print()
print('=== P52 复核 ===')
print(p52.text[:200])
print('  残留"（待产发": %s   长度 %d' % ('是' if '（待产发' in p52.text else '否', len(p52.text)))
print('=== P54 复核 ===')
print(p54.text[:200])
print('  残留"（待资产、产发": %s   长度 %d' % ('是' if '（待资产、产发' in p54.text else '否', len(p54.text)))
print('  末段标记: %s' % ('OK' if '（待资产部核对补充）' in p54.text else 'MISSING'))
# 其余 14 处标记是否保留
keep = 0
for i, p in enumerate(d2.paragraphs):
    if re.search(r'（待[^）]*核对补充）|（待董事会补充）|（待财务、运管核对补充）', p.text):
        keep += 1
print()
print('全文保留的其他部门待补充标记: %d 处（应为 14）' % keep)
print('文件大小 %.1f KB' % (os.path.getsize(DST) / 1024))
