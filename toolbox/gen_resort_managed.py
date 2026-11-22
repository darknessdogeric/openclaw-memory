# -*- coding: utf-8 -*-
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = r"C:\Users\ericz\Desktop\景区度假型业态_外部品牌托管模式分析_v1.0_2026-11-20.docx"
NAVY = RGBColor(0x1F, 0x38, 0x64); RED = RGBColor(0xC0, 0x00, 0x00)

doc = Document()
st = doc.styles['Normal']
st.font.name = '仿宋_GB2312'; st.font.size = Pt(11)
st.element.rPr.rFonts.set(qn('w:eastAsia'), '仿宋_GB2312')
st.paragraph_format.space_after = Pt(0)
st.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
st.paragraph_format.line_spacing = Pt(21)
for sec in doc.sections:
    sec.top_margin = Cm(2.4); sec.bottom_margin = Cm(2.2)
    sec.left_margin = Cm(2.2); sec.right_margin = Cm(2.0)


def F(run, name='仿宋_GB2312', size=11, bold=False, color=None):
    run.font.name = name; run.font.size = Pt(size); run.bold = bold
    run._element.rPr.rFonts.set(qn('w:eastAsia'), name)
    if color is not None:
        run.font.color.rgb = color


def P(t, font='仿宋_GB2312', size=11, bold=False, indent=2, align=None, color=None,
      before=0, after=0, spacing=21):
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    par.paragraph_format.line_spacing = Pt(spacing)
    par.paragraph_format.space_before = Pt(before); par.paragraph_format.space_after = Pt(after)
    if align is not None:
        par.alignment = align
    if indent:
        par.paragraph_format.first_line_indent = Pt(size * indent)
    F(par.add_run(t), font, size, bold, color)
    return par


def h1(t):
    P(t, font='黑体', size=12.5, before=10, after=2, color=NAVY)


def h2(t):
    P(t, font='楷体_GB2312', size=11, bold=True, before=6, after=2)


def item(t):
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    par.paragraph_format.line_spacing = Pt(21)
    par.paragraph_format.first_line_indent = Pt(22)
    F(par.add_run(t), '仿宋_GB2312', 11, False)
    return par


def note(t):
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    par.paragraph_format.line_spacing = Pt(21)
    par.paragraph_format.left_indent = Pt(22); par.paragraph_format.first_line_indent = Pt(0)
    F(par.add_run(t), '楷体_GB2312', 10.5, False, RED)
    return par


def shade(cell, hexc):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:fill'), hexc)
    tcPr.append(sh)


def tbl(headers, rows, widths=None, fs=9):
    t = doc.add_table(rows=1, cols=len(headers)); t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hc = t.rows[0].cells
    for i, h in enumerate(headers):
        hc[i].text = ''
        pp = hc[i].paragraphs[0]; pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pp.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        pp.paragraph_format.line_spacing = Pt(15)
        F(pp.add_run(h), '黑体', fs, False); shade(hc[i], 'D9D9D9')
    for ri, row in enumerate(rows):
        cs = t.add_row().cells
        for ci, v in enumerate(row):
            cs[ci].text = ''
            pp = cs[ci].paragraphs[0]
            pp.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            pp.paragraph_format.line_spacing = Pt(15)
            F(pp.add_run(str(v)), '仿宋_GB2312', fs, False)
            if ri % 2 == 1:
                shade(cs[ci], 'F2F2F2')
    if widths:
        for r in t.rows:
            for i, w in enumerate(widths):
                r.cells[i].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(3)
    return t


P('安逸酒店集团产业发展部', font='仿宋_GB2312', size=12, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
P('景区度假型业态 · 外部品牌托管模式分析', font='方正小标宋简体', size=17,
  align=WD_ALIGN_PARAGRAPH.CENTER, spacing=30, after=2)
P('Mandai 先例验证、合同经济结构与三岔湖试点建议', font='方正小标宋简体', size=15,
  align=WD_ALIGN_PARAGRAPH.CENTER, spacing=28, after=4)
P('2026 年 11 月 20 日', font='仿宋_GB2312', size=11, align=WD_ALIGN_PARAGRAPH.CENTER, after=12)

h1('〇、结论')
item('一、**方向可以走，先例真实存在，命名法可复制。**'
     '您举的 Mandai Rainforest Resort by Banyan Tree 是悦榕集团的第 100 家度假村（2025 年），'
     '**其命名格式本身就是"托管制命名"——物业名在前，"by 品牌名"在后**，'
     '即业主保留物业名与品牌，外部品牌输出管理与标准。国内同类先例为'
     '合利创兴 × 悦榕（广州海珠湖悦榕庄，业主开发、悦榕品牌与管理）。')
item('二、**而且这件事集团 10 月 27 日就已经谈过了。**'
     '当日量化清单已记录：命名"安逸加悦榕组合命名，示例"古尔沟悦榕庄安逸"，无需完全替换原有品牌标识"；'
     '目标一"借悦榕品牌影响力快速提升存量资产市场估值"，目标二"突破安逸在度假酒店领域的品牌发展瓶颈"。'
     '**本次要做的是把它从纪要口径变成可签的合同条款。**')
item('三、**但要成立必须补三个前置条件，缺一条就是纸上谈兵：**'
     '一、"保留集团品牌"的法律含义须在合同中写死；'
     '二、必须算清扣完管理费、激励费、品牌费后的净收益；'
     '三、**必须先解决资产与授权问题——川西资源型项目的真瓶颈不是品牌。**')
item('四、**落地排序建议：三岔湖先行，古尔沟不宜作首个试点。**'
     '古尔沟同时是资产处置对象、洲际川西意向、悦榕考察意向的三重身份，'
     '且正在推进破产重整与关停处置；'
     '三岔湖产权完整、无品牌、无历史包袱，是"资源型项目"最干净的载体。')

h1('一、模式确认：先例、命名法与集团既有口径')
tbl(['先例', '结构', '可借鉴之处'],
    [
        ['**Mandai Rainforest Resort by Banyan Tree**\n（新加坡，2025）',
         '物业名在前、"by Banyan Tree"在后——**托管制命名**；'
         '悦榕集团第 100 家度假村',
         '**命名法本身可复制**：'
         '"××（悦榕管理）"形式让业主资产与品牌方管理在同一名称中共存'],
        ['合利创兴 × 悦榕\n（广州海珠湖悦榕庄）',
         '业主开发并持有，悦榕提供品牌与管理',
         '国内"业主品牌 + 品牌方托管"的已落地样本'],
        ['Capella Living Room / Marriott Soft Brand / Hyatt Unbound Collection',
         '品牌方仅输出品牌、预订系统与标准，业主保留经营',
         '反向参照：**这是"品牌输出方"模式，安逸做的是"付方"**'],
    ],
    widths=[4.0, 5.2, 7.6])
note('★ 集团既有口径（2026-10-27 量化清单，已核实）：'
     '命名＝"安逸加悦榕组合命名，示例古尔沟悦榕庄安逸，无需完全替换原有品牌标识"；'
     '目标一＝借悦榕品牌影响力快速提升存量资产市场估值；'
     '目标二＝突破安逸在度假酒店领域的品牌发展瓶颈；'
     '另记有"悦榕赴古尔沟考察""全产业链四方向合作（人才培训／康养／旅行社／物业）"。')

h1('二、三条必须先摆的反向证据')
h2('（一）九寨沟悦榕庄：安逸自己家门口的样本，经营不佳、模式过气')
item('集团 2026-08-13《酒店业务现状分析与发展建议·战略规划专家座谈》对九寨沟悦榕庄的判断是'
     '**"经营不佳""模式过气"**；'
     '2026-08-17《战略全景·月底报告素材底座》进一步记录'
     '**"度假酒店衰退：安缦／悦榕庄全部跌落，玩情怀／园艺／枯山水模式祛魅"**。')
item('**集团 2026-10-25《悦榕集团前来安逸酒店集团拜访·报告》已经写明这句话：**')
P('"悦榕在华项目的经营表现可作为参照。集团内部既有分析认为九寨沟悦榕庄经营不佳、'
  '模式存在过时问题，说明国际品牌叠加优质目的地并不必然成功，'
  '安逸在借鉴悦榕经验的同时应保留自身运营判断，不宜简单对标。"',
  font='楷体_GB2312', size=11, indent=2, after=4)
note('★ 这条最要紧：STR 数据显示西南 ADR 指数最高的是九寨沟（115），'
     '**位置与品牌都在最优区间，结果仍然不佳。**'
     '这说明"位置 ＋ 品牌"不是度假项目的充分条件，'
     '**真正的约束是运营能力与业主方的管理。**'
     '而"托管"恰恰是把运营交给外部——所以这条既是风险提示，也是本模式的合理性所在。')

h2('（二）悦榕已在四川，且正在同一个赛道')
item('悦榕庄**天府新区已签约**；**峨眉山店 2025 年 8 月已开**（位于世界遗产地内）；'
     'Banyan Tree Mount Emei（峨眉山）列入其 2026 年中国管线；'
     '另有广州九龙湖（Banyan Tree Guangzhou Jiulong Lake）等新开与管线项目。'
     '**川西与川西南的资源型目的地，正是悦榕的扩张方向——我们要谈的项目，他们也在谈。**'
     '这既是机会（说明对方重视该区域），也是竞争（**我们不是唯一买家，且对方自带品牌**）。')
item('**推论：在"资源型项目"上，外部品牌方是竞争者而不是纯赋能者。**'
     '谈判中必须意识到：**对方拿出的是全球通行品牌，'
     '而我们能拿出的是本地资源与属地关系——这是我们的筹码，不是我们的短板。**')

h2('（三）本模式对集团的真实价值：是"学运营"与"建品牌资产"，不是"提房价"')
item('九寨沟样本已经证明：**单纯挂牌国际品牌，不必然带来经营改善。**'
     '那么托管对安逸的价值到底在哪？'
     '有三项，且都与品牌溢价无关：'
     '一、**借外部标准把团队练出来**（悦榕有 20 多年中国经验、'
     '140 余家 SPA 与画廊、Banyan Spa & Wellbeing Academy 自 2001 年培训逾 2,800 名理疗师）；'
     '二、**借外部渠道拿到高端客源**（其会员与直销体系）；'
     '三、**在合同期内沉淀自己的品牌资产与会员数据**（这是唯一能通向"轨道 A"的东西）。'
     '**若谈不到第三项，这个模式对集团就只是"花钱买管理"，价值有限。**')

h1('三、"保留集团品牌"的三种含义与各自合同风险')
tbl(['方案', '具体做法', '实质', '风险', '建议'],
    [
        ['**A**', '仅保留物业名／地名（如"古尔沟悦榕庄·安逸"）',
         '**实质是挂牌悦榕**，安逸只是名字里带一个前缀',
         '**拿不到任何品牌溢价**；'
         '客诉、声誉、会员计入均归品牌方',
         '起步方案；**谈判须争取品牌费减免或管理费折抵作为补偿**'],
        ['**B**', '保留"安逸"作为在地副品牌（VI、客用品、权益、在地内容）',
         '双品牌并存',
         'VI 主导权、会员数据归属、客诉与声誉责任归属不清',
         '谈判中预留；**必须逐项写明**'],
        ['**C**', '保留合同终止后的品牌资产（未来转自有品牌或转轨道 A）',
         '**品牌孵化路径**',
         '最难；品牌方通常不接受',
         '**作为目标条款争取**；'
         '配合"退出过渡期协议""员工保留协议""经营数据所有权"'],
    ],
    widths=[1.2, 4.2, 3.6, 3.8, 4.0])
note('★ 一条实务提醒：组合命名的前提是品牌方同意。'
     '"古尔沟悦榕庄安逸"这类"悦榕在前、安逸在后"的写法，'
     '**悦榕未必接受**（涉及品牌层级、客诉归属、会员计入、OTA 展示顺序）。'
     '须准备让步版本，如"安逸·××（悦榕管理）"。'
     '**命名谈到哪一步，往往能看出对方对合作的认真程度。**')

h1('四、这笔账怎么算：三种合同经济结构')
tbl(['结构', '安逸收入侧', '安逸成本侧', '成立条件'],
    [
        ['**结构一**\n业主自营 ＋ 品牌输出\n（轨道 A）',
         '**品牌费 ＋ 系统费**（经常性、可预测、不承担资产风险）',
         '系统与品牌建设投入',
         '安逸已有品牌资产与会员基础；**这是终局形态**'],
        ['**结构二**\n托管 ＋ 品牌授权\n（轨道 B）',
         '经营收入，但**让渡品牌溢价**',
         '管理费 2%-5% ＋ GOP 激励 8%-15%；'
         '若另计特许：房费 4%-6% ＋ 忠诚度／营销 2%-4%',
         'ADR 溢价显著大于全部费率；**多数项目不成立**'],
        ['**结构三**\n托管 ＋ 风险共担',
         '经营收入',
         '**只保留低基础管理费或无基础费**，'
         'GOP 超门槛分成，**不足分担、超额分享**',
         '**最值得争取**：把经营风险按结果分摊，'
         '与"九寨沟教训"直接对应'],
    ],
    widths=[3.4, 4.0, 5.2, 4.2])
P('判据：净收益提升 ＝ 改造后增量 GOP －（管理费与激励费）－（品牌费）－（会员与渠道增量获取成本）',
  font='楷体_GB2312', size=11, indent=2, after=4)
note('★ 提醒：度假与奢华类的其他经营部门（温泉、SPA、零售、康养）分成比例高达 5%-25%，'
     '而精选服务类几乎为零。'
     '**川西资源型项目的收入结构恰恰是温泉、康养、研学、零售为主，'
     '这部分正是管理费分成最高的一类，必须单独议定，不能套用客房口径。**')
item('**若三个扣减后算不成立，那结论不是"换个更强的品牌"，而是"换一个更好的资产"。**'
     '——这条要在项目评估阶段就说清楚，避免把资产问题错诊成品牌问题。')

h1('五、川西／川西南资源型项目的准入五问')
tbl(['#', '问题', '为什么关键', '判定'],
    [
        ['1', '**资源是否独占？景区经营权在谁手里**',
         '若经营权不在我方，托管只是在别人的资源上做运营',
         '无控制权 → 不做'],
        ['2', '**物业与经营授权期限**',
         '**最易被忽略的一项**：品牌与会员沉淀需 5-8 年，'
         '而业主授权期可能只有 3-5 年，'
         '**一期投资回收期与品牌资产寿命错配**',
         '**授权期 < 8 年 → 一期投资须按可回收部分测算，'
         '且合同须有到期不续的退出补偿**'],
        ['3', '**到达性**',
         'STR 西南数据表明川西溢价真实存在（九寨沟 ADR 指数 115），'
         '**但溢价能否兑现取决于到达成本**',
         '与核心景区车程 > 1.5 小时 → 慎入'],
        ['4', '**淡旺季结构与全年运营天数**',
         '决定固定成本摊薄；度假项目的成本刚性高',
         '有效运营天数 < 200 天 → 慎入'],
        ['5', '**淡季产品是什么**',
         '**康养是 2026 最确定的产品级新变量**'
         '（KB 度假酒店知识体系；Banyan 自身 2026 议程亦为 wellbeing 主导，'
         'Banyan Tree Connections 已扩至 8 家度假村）',
         '无淡季产品 → **不适用度假业态，应改走会议培训型**'],
    ],
    widths=[0.8, 3.8, 6.6, 5.6])

h1('六、与三业态框架的挂接')
item('一、**第三业态（旅游度假型）有两条落地路径，本模式是其中一条：**'
     '轨道 A（品牌与系统输出，收品牌费）对应终局；'
     '轨道 B（托管 ＋ 品牌授权，付费）对应起步。'
     '**建议先 B 后 A：用 B 学运营、建品牌资产、拿会员沉淀，期满转 A 或转自有品牌。**')
item('二、**每一个 B 项目都必须预置"通向 A"的合同条款**，共五项：'
     '品牌归属、会员数据归属、员工保留协议、退出后过渡期、经营数据所有权。'
     '**这五项不写进去，B 就只是一次性的费用，A 就永远无从谈起。**')
item('三、**与三岔湖双路径并行的问题必须统筹。**'
     'KB 已记：成体院路径（近中远三段框架，节点 11-30）与悦榕路径（共同开发）'
     '**指向同一资产，须统筹排他条款与时序，避免竞合。**')
item('四、**与 11 月 20 日发展路径件的接口：**'
     '三业态的第三类为"景区与湖泊山林的度假品牌"，'
     '其关键指标为 ADR 溢价率、淡旺季比、二次消费占比；'
     '**本模式直接服务于这三项，但同时也带来一个新的必答题——'
     '当外部品牌与自有品牌并存时，二次消费归属谁？**'
     '这一条须写进合同，不能留到运营期扯皮。')

h1('七、三个项目的落地排序与现有节点')
tbl(['项目', '客观状态', '建议'],
    [
        ['**三岔湖天府山庄**\n（建议首个试点）',
         '88.8 亩；3 个独立岛屿；水域约 4 个杭州西湖；天府国际机场旁；'
         '**完整国有商业建设用地**；原四川省人大培训中心，现闲置；**无品牌**；'
         '安逸重资产投资压力大，希望引入合作方共同开发、条件可协商',
         '**产权完整是对悦榕的最大卖点，也是资源型项目最干净的载体**'
         '（无历史包袱、无品牌锁定、命名可重塑）。'
         '**建议作为首个"外部品牌托管"或"共同开发"试点**；'
         '注意与成体院路径排他与时序'],
        ['**古尔沟华美达**\n（不建议作首个试点）',
         '总投资约 6.9 亿元；200 余间客房；市场估值 3 亿元；账面负债 6 亿元；'
         '**资不抵债 181.74%**；安逸 52% 控股；'
         '**华美达品牌授权即将到期**；悦榕拟赴现场考察；'
         '同时是洲际川西布局意向方；新媒体投入 40 万元为全集团最高',
         '**三重身份交叉 ＋ 正在推进破产重整与关停处置**，'
         '此时引入托管品牌会与处置进程冲突。'
         '**建议：先出"自主／洲际／悦榕"三条路径并列的系统性解决方案，'
         '再谈合作；不宜作为托管试点**'],
        ['**总府皇冠**',
         '900 万元／年为刚性现金流出，2027 年到期是唯一解约窗口',
         '**属城市高星，不适用本模式**（见 11-20 四层品牌矩阵），'
         '按高星全服务逻辑另案处理'],
    ],
    widths=[3.4, 6.4, 7.0])
h2('现有节点与到期提醒')
item('一、**"悦榕三项目资料交付"节点 11-15，今日已 11-20 —— 须核实是否已交付。**'
     '若未交付，第一轮评估窗口已错过，须在下次沟通中明确补交时间。')
item('二、三岔湖成体院路径节点 **11-30**（改造投资额）；'
     '全产业链四方向合作细则框架节点 **12-31**（人才培训／康养／旅行社／物业，各方对接人）。')
item('三、**古尔沟 6.9 亿投资、3 亿估值、6 亿负债的口径核实原定 11-05，状态待确认**；'
     '古尔沟系统性解决方案要求"本周内"上报。')
item('四、**建议下一步：把"全产业链四方向"与"托管模式"合成一张谈判清单，**'
     '避免两条线分别沟通、彼此打架。'
     '托管合同与四方向细则应作为**同一套文件的两个附件**提交悦榕。')

h1('八、待核清单')
tbl(['#', '事项', '归口'],
    [
        ['1', '**Mandai 项目所有权与运营结构**（物业持有方、是否政府关联实体、'
         '悦榕的角色是品牌授权还是委托管理）——本件未取到硬证据，'
         '**须核实后再对外引用此先例**', '产发部'],
        ['2', '11-15 悦榕三项目资料是否已交付', '产发部'],
        ['3', '古尔沟 6.9 亿投资／3 亿估值／6 亿负债口径核实（原定 11-05）', '产发部 ＋ 投资资产部'],
        ['4', '悦榕是否接受组合命名、具体命名格式与让步空间', '产发部'],
        ['5', '三个项目的**经营授权期限**（决定品牌沉淀与投资回收是否匹配）', '投资资产部'],
        ['6', '古尔沟破产重整与托管的可行性与冲突', '投资资产部 ＋ 法务'],
        ['7', '三岔湖成体院路径与悦榕路径的排他条款与时序', '产发部'],
    ],
    widths=[0.8, 12.4, 3.6])

gap = doc.add_paragraph()
gap.paragraph_format.line_spacing = Pt(12)
P('本件为内部研讨用。集团内部数据引自 2026-10-27 近期重点工作量化清单、'
  '2026-10-25 悦榕拜访报告、集团战略全景与专家座谈纪要；'
  '国际先例与费率引自公开信息。结论为按现有信息推算，落地前须逐项核实。',
  font='仿宋_GB2312', size=10, after=8)

doc.add_paragraph()
P('安逸酒店集团产业发展部', align=WD_ALIGN_PARAGRAPH.RIGHT, after=2)
P('2026 年 11 月 20 日', align=WD_ALIGN_PARAGRAPH.RIGHT)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc.save(OUT)
print('SAVED:', OUT)
print('SIZE:', os.path.getsize(OUT))

