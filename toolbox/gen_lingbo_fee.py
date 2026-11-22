# -*- coding: utf-8 -*-
"""岭博网关方案 · 费用对比与三层匹配改造建议 v1.0"""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = r"C:\Users\ericz\Desktop\岭博网关方案_费用对比与三层匹配改造建议_v1.0_2026-11-05.docx"
NAVY = RGBColor(0x1F, 0x38, 0x64); BLUE = RGBColor(0x2F, 0x54, 0x96)
GREY = RGBColor(0x80, 0x80, 0x80); RED = RGBColor(0xC0, 0x00, 0x00)

doc = Document()
st = doc.styles['Normal']; st.font.name = '仿宋_GB2312'; st.font.size = Pt(10.5)
st.element.rPr.rFonts.set(qn('w:eastAsia'), '仿宋_GB2312')
st.paragraph_format.space_after = Pt(3); st.paragraph_format.line_spacing = 1.28
for sec in doc.sections:
    sec.top_margin = Cm(2.0); sec.bottom_margin = Cm(2.0)
    sec.left_margin = Cm(2.2); sec.right_margin = Cm(2.0)


def F(run, name='仿宋_GB2312', size=10.5, bold=False, color=None):
    run.font.name = name; run.font.size = Pt(size); run.bold = bold
    run._element.rPr.rFonts.set(qn('w:eastAsia'), name)
    if color is not None:
        run.font.color.rgb = color


def p(t, font='仿宋_GB2312', size=10.5, bold=False, indent=2, align=None, color=None,
      before=0, after=3):
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing = 1.28
    par.paragraph_format.space_before = Pt(before); par.paragraph_format.space_after = Pt(after)
    if align is not None:
        par.alignment = align
    if indent:
        par.paragraph_format.first_line_indent = Pt(size * indent)
    F(par.add_run(t), font, size, bold, color)
    return par


def h1(t):
    p(t, font='黑体', size=12.5, before=13, after=4)


def h2(t):
    p(t, font='楷体_GB2312', size=11, bold=True, before=8, after=3)


def bl(t, lv=0):
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing = 1.28
    par.paragraph_format.left_indent = Pt(22 + lv * 13)
    par.paragraph_format.space_after = Pt(2)
    F(par.add_run(('　' * lv) + '· ' + t), '仿宋_GB2312', 10.5)


def note(t, color=RED):
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing = 1.28
    par.paragraph_format.left_indent = Pt(12); par.paragraph_format.space_after = Pt(5)
    F(par.add_run(t), '仿宋_GB2312', 10, False, color)


def shade(cell, hexc):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:fill'), hexc)
    tcPr.append(sh)


def tbl(headers, rows, widths=None, fs=9, fill='1F3864'):
    """rows: list of tuple"""
    t = doc.add_table(rows=1, cols=len(headers)); t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hc = t.rows[0].cells
    for i, htxt in enumerate(headers):
        hc[i].text = ''
        pp = hc[i].paragraphs[0]; pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        F(pp.add_run(htxt), '仿宋_GB2312', fs, True, RGBColor(0xFF, 0xFF, 0xFF)); shade(hc[i], fill)
    for ri, row in enumerate(rows):
        cs = t.add_row().cells
        for ci, val in enumerate(row):
            cs[ci].text = ''
            pp = cs[ci].paragraphs[0]; pp.paragraph_format.space_after = Pt(1)
            txt = str(val); bold = txt.startswith('**')
            F(pp.add_run(txt.replace('**', '')), '仿宋_GB2312', fs, bold)
            if ri % 2 == 1:
                shade(cs[ci], 'F2F5FA')
    if widths:
        for r in t.rows:
            for i, w in enumerate(widths):
                r.cells[i].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


# ==================== 测算 ====================
TIER = {'MG200': (10000, 5000, 1500), '1510': (19800, 10000, 3000),
        '1560': (29800, 15000, 4500), '2200': (59800, 30000, 9000)}

# 逐店房量，源自《安逸集团酒店名录三表内化 v1.0》（2026-09-16）
ROOMS = [
    (707, '在营'), (166, '在营'), (345, '在营'), (91, '在营'), (120, '在营'),
    (150, '在营'), (96, '在营'), (123, '在营'), (142, '在营'), (36, '在营'),
    (100, '在营'), (153, '在营'), (32, '在营'), (88, '在营'), (107, '在营'),
    (114, '在营'), (236, '在营'), (52, '在营'), (195, '在营'), (120, '在营'),
    (151, '在营'), (402, '委托外资管理'), (858, '在营'),
]
AVG_TRUST = 204  # 受托 39 家按在营平均房量估算


def tier_of(rooms):
    if rooms <= 100:
        return 'MG200'
    if rooms <= 200:
        return '1510'
    if rooms <= 350:
        return '1560'
    return '2200'


def calc(rooms_list):
    buy = svc = yr3 = 0
    n = 0
    for r in rooms_list:
        k = tier_of(r)
        b, y, s = TIER[k]
        n += 1; buy += b; svc += s; yr3 += y * 3
    return n, buy, svc, yr3


n1, buy1, svc1, _ = calc([r for r, st in ROOMS])
n4, buy4, svc4, _ = calc([AVG_TRUST] * 39)
nA, buyA, svcA, _ = calc([r for r, st in ROOMS] + [AVG_TRUST] * 39)
GRP_ONCE = 15
PLAT_YR = 12
three = (buyA + GRP_ONCE * 10000 + PLAT_YR * 10000 * 2) // 10000
cur3 = (buyA + svcA * 2) // 10000
print("在营 %d 家: 硬件 %d 万, 年服务 %d 万" % (n1, buy1 // 10000, svc1 // 10000))
print("受托 %d 家: 硬件 %d 万, 年服务 %d 万" % (n4, buy4 // 10000, svc4 // 10000))
print("合计 %d 家: 硬件 %d 万, 年服务 %d 万, 现行三年 %d 万" % (nA, buyA // 10000, svcA // 10000, cur3))
print("三层改造三年 %d 万, 差 %d 万" % (three, cur3 - three))

# ==================== 封面 ====================
p('岭博网关方案', font='方正小标宋简体', size=17,
  align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, after=2)
p('费用对比与三层匹配改造建议', font='方正小标宋简体', size=17,
  align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, after=2)
p('安逸酒店集团产业发展部　2026 年 11 月', font='仿宋_GB2312', size=11,
  align=WD_ALIGN_PARAGRAPH.CENTER, color=GREY, after=10)

# ==================== 一 ====================
h1('一、口径说明')
bl('本件聚焦两件事：一是岭博与同类厂商的费用方案对比；二是按集团“三层匹配”要求改造费用结构。')
bl('**前次表述更正**：此前所列集团层面四项、酒店层面四项功能说明，'
   '**是岭博科技向我方提供的产品能力说明与价值主张，不是我方的需求清单**。'
   '前次报告将其表述为“九项诉求”，属定性偏差，本次予以更正。')
bl('费用测算依据：岭博 2026 年 11 月 2 日报价单原件（有效期 30 天）；'
   '安逸逐店房量引自《安逸集团酒店名录三表内化 v1.0》（2026-09-16）；'
   '竞品价格引自厂商公开零售价与公开项目采购清单。')

# ==================== 二 ====================
h1('二、费用对比')
h2('（一）岭博现有报价（按店售卖）')
tbl(['机型', '适用房量 / 并发', '购销模式硬件', '次年起服务费/年', '年服务费模式（三年期）每年'],
    [('MG200', '≤100 间 / 400 并发', '10,000 元', '1,500 元', '5,000 元'),
     ('YunGW 1510', '100-200 间 / 800 并发', '19,800 元', '3,000 元', '10,000 元'),
     ('YunGW 1560', '200-350 间 / 1,500 并发', '29,800 元', '4,500 元', '15,000 元'),
     ('YunGW 2200', '>350 间', '59,800 元', '9,000 元', '30,000 元')],
    widths=[3.0, 3.6, 2.8, 3.4, 4.4])
p('另：集团会员系统对接、酒店 PMS 对接、集团短信平台对接、Portal 定制设计 5 万元（集团合作赠送）；'
  '上门实施调试 1,800 元/店，远程可免；短信认证服务费未含在报价内，需另购套餐。')

h2('（二）同类厂商公开价格')
tbl(['厂商', '产品与公开单价', '价格带', '与岭博的可比性'],
    [('**锐捷睿易**（公开零售价）',
      'RG-NBR6135-E 2Gbps ¥4,000；RG-NBR6205-E 3Gbps ¥6,000（明示适用星级酒店）；'
      'RG-NBR6210-E 4Gbps ¥11,400（推荐带终端 1,000 个）；'
      'RG-NBR-N7820-E 1500-2000 终端 1U 集成 AC ¥76,600',
      '0.4 万-7.66 万/台',
      '单台硬件价格低于岭博，但不含各地网监对接与 CCRC 审计认证，'
      '亦不含会员引流与跨店漫游运营，属通用网络设备，不可直接替代'),
     ('**智慧光迅 AINOPOL**（公开项目采购清单单价）',
      'ZH-M1 防火墙 ¥28,519；ZH-AC500 Ultra 出口路由 ¥26,668；ZH-H200 Ultra 流媒体网关 ¥37,942；'
      'ZH-5530TGX-SI 核心交换机 ¥18,810；ZH-CS5228P-PWR 24 口 PoE 云交换机 ¥9,075/台；'
      'ZH-4O 外线电话网关 ¥5,445；客房区 98 台双频 PON 光云 AP、公区 6 台光电融合 AP',
      '核心层单台 1.9 万-3.8 万；客房层 AP 数量级数十至上百台',
      '口径最接近集团采购要求：其公开清单本身即为'
      '「核心层统一业务中枢＋客房区域批量部署＋无源光纤布线」的三层结构整包。'
      '但交付范围含全光布线与 AP，与岭博不同，总价不可直接比'),
     ('**任子行 / 东软 NetEye / 博达**', '未公开零售价', '—',
      '专业审计强项（东软长时日志 180 天以上、博达 SSL 解密），但属审计设备，非酒店会员运营工具'),
     ('**深信服 / 信锐**', '未公开零售价', '—',
      '安全底子厚、连续十一年市占第一；但信锐 AP 与网关私有协议、扩容必须同品牌'),
     ('**运营商系方案**', '未公开零售价', '按带宽或终端包年',
      '覆盖广、价格低，但数据在运营商侧，会员与营销能力弱')],
    widths=[3.4, 6.2, 2.6, 4.8])

h2('（三）费用层面的三条结论')
bl('**结论一：岭博的单店价格并不贵。** 四档机型 0.5 万至 5.98 万元/台，'
   '与锐捷睿易同档位公开零售价处于同一水平甚至更低。问题不在单价，在计价口径。')
bl('**结论二：岭博与锐捷不可直接比，因为交付范围不同。** 锐捷不含各地网监对接与 CCRC 审计认证、'
   '不含会员引流与跨店漫游运营；这两项恰恰是岭博溢价所在，也是安逸真正需要的部分。'
   '把锐捷当比价锚点会误判，须按“含网监与会员能力的整套”口径比。')
bl('**结论三：智慧光迅是最值得拉进比选的对手，因为它本身就是三层整包。** '
   '其公开清单显示核心层、客房区域层、布线层三层结构，且宣称合规成本降低 75% 以上、'
   '布线降低 80%、支持 2000+ 终端同时高速在线、PMS 联动“入住即认证”、年省人工审计时间 200 小时以上。'
   '它天然符合集团三层采购口径，是检验岭博报价是否合理的最佳参照物。')

# ==================== 三 ====================
h1('三、集团“三层匹配”的要求，与岭博报价的八处错位')
h2('（一）三层匹配的通行口径')
tbl(['层级', '内容', '计价原则'],
    [('**集团层**',
      '统一会员系统对接、统一数据中台与合规总览、统一 SSID 与跨店漫游、'
      '集团品牌 Portal 与多屏投放规范、集团短信平台、集团网监对接接口',
      '一次性建设、全集团共享，按集团打包价，不随门店数增加'),
     ('**平台层**',
      '多租户云服务：认证、审计、日志、PMS 接口、漫游控制、网络监控',
      '平台能力按集团打包计费，应体现规模阶梯，不按门店线性叠加'),
     ('**门店层**',
      '网关等终端设备、AP、端口与实施调试',
      '按门店数配置，可线性')],
    widths=[2.4, 8.0, 6.6])
p('智慧光迅的公开项目清单即为此结构；而岭博报价单的结构是“每店一台网关＋每店每年服务费＋'
  '5 万元赠送的集团对接”，本质上是以单店售卖方式提供一套本应集团统采的能力。')

h2('（二）八处错位')
tbl(['#', '错位', '岭博现有口径', '三层匹配应有的口径'],
    [('1', '**平台层按店叠加**',
      '服务费 1,500-9,000 元/店/年，%d 家线性叠加约 %d 万元/年' % (nA, svcA // 10000),
      '多租户平台 %d 家共用，应按集团打包价，目标 %d 万元/年以内并写阶梯' % (nA, PLAT_YR)),
     ('2', '**集团层近乎未计价**', '会员系统对接、PMS 对接、短信平台对接、Portal 定制合计 5 万元“赠送”',
      '集团层是本项目最值钱也最便宜的一层，须正式计价并明确交付清单，目标 10-15 万元一次性'),
     ('3', '**统一 SSID 未列价**', '云服务包含跨店漫游控制，但统一 SSID 属配置工作量，未单列',
      '写入集团层交付清单，明确配置范围与验收标准'),
     ('4', '**集团品牌 Portal 未计价**', 'Portal 页面制作“需客户提供素材”，按单店计',
      '集团版 Portal 模板、多屏投放规范、品牌资产适配属集团层，须单独计价'),
     ('5', '**集团数据看板未计价**', '双 ISP 出口流量报表为单店报表',
      '集团层需经营与合规总览看板（会员拉新、跨店漫游、OTA 依赖度、网监合规率），须单独计价'),
     ('6', '**会员对接工作量未计**', '会员系统对接 1 项 5 万元，隐含 1 店 1 对接',
      '62 家与安逸会打通须含数据模型、权益规则、跨店漫游逻辑，属集团层工程'),
     ('7', '**短信费未含在内**', '需要购买短信费用套餐支持，未报价',
      '单列预算科目，并以微信小程序连 Wi-Fi 替代方案测算节省额'),
     ('8', '**网监对接按“已覆盖城市”表述**', '网监对接“岭博已覆盖城市全部提供”',
      '须逐店确认属地网监接入状态，未覆盖城市明确替代方案与费用')],
    widths=[0.8, 3.2, 6.4, 6.6])

# ==================== 四 ====================
h1('四、三层匹配改造后的费用结构')
tbl(['层级', '现行岭博口径', '三层匹配改造后（目标）', '说明'],
    [('**门店层**', '硬件一次性 %d 万元（%d 家）' % (buyA // 10000, nA),
      '基本不变，%d 万元' % (buyA // 10000), '以集团统采一次性下单换取阶梯价；按实际房量复核机型配置'),
     ('**集团层**', '5 万元（赠送）', '一次性 15 万元',
      '含统一会员对接、统一 SSID 与跨店漫游、集团品牌 Portal 与多屏规范、集团数据与合规看板、集团网监对接接口'),
     ('**平台层**', '%d 万元/年（%d 家按单店均值叠加）' % (svcA // 10000, nA), '12 万元/年（集团打包）',
      '按集团打包计费，并在合同中写入规模阶梯价与扩容价'),
     ('实施与短信', '实施 1,800 元/店；短信费未含', '实施并入单店价；短信费单列预算',
      '远程调试优先，现场实施按实结算'),
     ('**三年总拥有成本**', '约 %d 万元' % cur3, '约 %d 万元' % three,
      '价差不大，结构改变的价值远大于价差')],
    widths=[2.4, 5.2, 4.6, 4.8])
note('★ 三层匹配的价值不在总价差，在三件事：一是平台层由 62 份订阅变为 1 套集团资产，'
     '数据与配置真正沉淀在集团；二是集团层能力（统一 SSID、跨店漫游、集团 Portal、'
     '集团看板、集团网监接口）在现行单店售卖口径下根本买不到；'
     '三是扩容价格写入合同，后续新增门店不必逐年重新议价。')

# ==================== 五 ====================
h1('五、谈判要点')
bl('**第一句话就定口径**：我方按集团三层匹配采购，要求按“集团层一次性＋平台层集团打包＋'
   '门店层按店配置”三段报价，不接受按店线性叠加的平台服务费。')
bl('**用智慧光迅做参照**：其公开项目清单为三层整包，且公开主张合规成本降低 75% 以上、'
   '年省人工审计 200 小时以上，要求岭博提供同口径三年总拥有成本测算与分层报价。')
bl('**把集团层从“赠送”变成计价项**：5 万元赠送说明对方自己也认为集团层工作量有限；'
   '但集团层恰是集团真正要买的东西，应要求明确交付清单与验收标准。')
bl('**启动平替价**：按报价单 E 条，以集团现有弱电与网监年度付费记录换平替价；'
   '与三层匹配叠加使用，互不冲突。')
bl('**坚持服务与平台的资产属性**：平台层服务在合同期内不得因门店数变化而重新定价，'
   '并约定合同终止时的数据导出、配置迁移与过渡支持。')
bl('**同步拉齐大景**：按 10 月 26 日集团例会“资源置换优先、岭博网关与大景电视屏打包谈判”的要求，'
   '在 11 月 15 日联合方案中一并呈现，让岭博的现金需求与大景的零投入结构形成互补。')

p('注：竞品价格引自厂商公开零售价页面与公开项目采购清单，属公开信息；'
  '岭博数据引自 2026 年 11 月 2 日报价单原件；'
  '安逸逐店房量引自《安逸集团酒店名录三表内化 v1.0》。'
  '三层匹配改造后的目标价为按现有公开信息推算的谈判目标区间，非最终定价，签约前以实际清单与谈判结果为准。',
  size=9, color=GREY, before=10)

doc.add_paragraph()
p('安逸酒店集团产业发展部', align=WD_ALIGN_PARAGRAPH.RIGHT, after=2)
p('2026 年 11 月 5 日', align=WD_ALIGN_PARAGRAPH.RIGHT)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc.save(OUT)
print('SAVED:', OUT)
print('SIZE:', os.path.getsize(OUT))
