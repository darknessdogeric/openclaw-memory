"""
把 01_集团与56家酒店账号现状.docx 改成下发采集表单
- 删除原"找什么/从哪里找/找谁要"维度表
- 替换为：填写说明 + 9 个采集板块 + 签字确认
- 字体：公文模板（方正小标宋 + 仿宋_GB2312）
"""
import shutil
import os
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement

TEMPLATE = r'C:\Users\ericz\Desktop\邹士勇发言稿_2026高参圆桌国资酒店_2026-08-29_v5.5_基于十五五规划复盘版.docx'
TARGET = r'C:\Users\ericz\Desktop\2026-08-29_立项信息搜集\立项1_集团新媒体矩阵统筹\01_集团与56家酒店账号现状.docx'

# 字体工具
def set_run_font(run, font_eastasia, font_name_ascii='Times New Roman', size_pt=18, bold=False):
    run.font.name = font_name_ascii
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rFonts')
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.append(rfonts)
    rfonts.set('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}eastAsia', font_eastasia)
    rfonts.set('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ascii', font_name_ascii)
    rfonts.set('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}hAnsi', font_name_ascii)

def T1(doc, text):
    """一级标题 22pt 加粗居中"""
    p = doc.add_paragraph()
    run = p.add_run(text)
    set_run_font(run, '方正小标宋简体', size_pt=22, bold=True)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

def T2(doc, text):
    """二级标题 16pt 加粗"""
    p = doc.add_paragraph()
    run = p.add_run(text)
    set_run_font(run, '黑体', size_pt=16, bold=True)

def T3(doc, text):
    """三级标题 14pt 加粗"""
    p = doc.add_paragraph()
    run = p.add_run(text)
    set_run_font(run, '黑体', size_pt=14, bold=True)

def P(doc, text='', bold=False, center=False, indent=False):
    p = doc.add_paragraph()
    if text:
        run = p.add_run(text)
        set_run_font(run, '仿宋_GB2312', size_pt=18, bold=bold)
    if center: p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if indent: p.paragraph_format.first_line_indent = Cm(0.74)

def add_table(doc, headers, rows, header_font='黑体', header_size=14):
    """添加表格 - 4列标准表"""
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Light Grid Accent 1'
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ''
        para = cell.paragraphs[0]
        run = para.add_run(h)
        set_run_font(run, header_font, size_pt=header_size, bold=True)
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for row_data in rows:
        row = table.add_row()
        for i, ct in enumerate(row_data):
            cell = row.cells[i]
            cell.text = ''
            para = cell.paragraphs[0]
            run = para.add_run(str(ct))
            set_run_font(run, '仿宋_GB2312', size_pt=14)
    return table

# 从模板复制并清空
def new_doc():
    tmp = os.path.join(os.environ['TEMP'], f'_form_{os.getpid()}.docx')
    if os.path.exists(tmp):
        os.remove(tmp)
    shutil.copyfile(TEMPLATE, tmp)
    doc = Document(tmp)
    body = doc.element.body
    sectPrs = body.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}sectPr')
    for child in list(body):
        if child.tag.endswith('}sectPr'):
            continue
        body.remove(child)
    for sp in sectPrs:
        body.append(sp)
    return doc

doc = new_doc()

# ========== 封面 ==========
T1(doc, '集团旗下酒店新媒体账号现状采集表')
T2(doc, '立项1：集团新媒体矩阵统筹 · 信息搜集')
P(doc, '')
P(doc, '编制：B166ER（产业发展部）', center=True)
P(doc, '版本：v1.0 · 2026-08-29', center=True)
P(doc, '')

# ========== 一、填写说明 ==========
T2(doc, '一、填写说明')
P(doc, '1. 本表由各酒店营销/新媒体负责人填写，**总经理审核签字后**提交。')
P(doc, '2. 数据截止日期：**2026 年 8 月 31 日**（粉丝量、阅读量等数据以 8 月 31 日 24:00 为准）。')
P(doc, '3. 提交截止日期：**2026 年 9 月 8 日 18:00 前**。')
P(doc, '4. 提交方式：集团 OA 系统 → 产业发展部 → [蒋抒伶 / B166ER]。')
P(doc, '5. **标注 * 为必填项**；标注 ○ 为选填项；标注 ☐ 为单选/多选框，请打勾。')
P(doc, '6. 数字统一格式：粉丝数/阅读量用阿拉伯数字 + 万/千单位（如 12.5万）；增长率/互动率用百分比（如 15%）；金额用元为单位（如 500000）。')
P(doc, '')
P(doc, '**保密声明**：', bold=True)
P(doc, '本表所填数据仅用于集团"新媒体矩阵统筹"立项决策，集团对所有数据**严格保密**——不公开、不对外披露、不用于外部用途。各酒店提交的数据仅在集团内部立项决策范围内使用。')
P(doc, '')

# ========== 二、酒店基础信息 ==========
T2(doc, '二、酒店基础信息')
add_table(doc,
    ['序号 *', '字段 *', '填写说明 *', '填写内容'],
    [
        ['1', '酒店全称', '与营业执照一致，加挂"安逸"品牌前缀', ''],
        ['2', '酒店类型', '单选（商务/度假/文化主题/公寓/其他）', '☐ 商务 ☐ 度假 ☐ 文化主题 ☐ 公寓 ☐ 其他（请注明 _______）'],
        ['3', '详细地址', '省市区 + 街道 + 门牌号', ''],
        ['4', '管理类型', '自营 / 受托管理（与集团 715 定稿一致）', '☐ 自营 ☐ 受托管理'],
        ['5', '总经理姓名 *', '在任总经理', ''],
        ['6', '总经理联系电话 *', '座机或手机', ''],
        ['7', '营销/新媒体负责人姓名 *', '当前对接新媒体工作的负责人', ''],
        ['8', '营销负责人联系电话 *', '手机', ''],
        ['9', '营销负责人邮箱', '常用邮箱', ''],
    ]
)
P(doc, '')

# ========== 三、新媒体账号配置清单 ==========
T2(doc, '三、新媒体账号配置清单')
P(doc, '请按平台分别填写。**有账号的平台必须填**，没有的请在"账号名"列写"无"。')
P(doc, '')
P(doc, '【表头说明】', bold=True)
P(doc, '· 粉丝数（截止 2026-08-31）；近 12 个月净增（2025-09 至 2026-08）；月均发布（过去 3 个月平均）；平均阅读/播放（过去 3 个月平均）；平均互动率（点赞+评论+转发 / 阅读量）。')
P(doc, '· 运营方：①自有团队 ②第三方代运营 ③部分外包 ④停更')
P(doc, '')

add_table(doc,
    ['平台', '账号名', '认证主体\n（集团/单店/第三方）', '粉丝数', '近12月净增', '月均发布数', '平均阅读/播放', '平均互动率', '运营方'],
    [
        ['微信公众号', '', '', '', '', '', '', '', ''],
        ['微信视频号', '', '', '', '', '', '', '', ''],
        ['抖音', '', '', '', '', '', '', '', ''],
        ['小红书', '', '', '', '', '', '', '', ''],
        ['微博', '', '', '', '', '', '', '', ''],
        ['B 站', '', '', '', '', '', '', '', ''],
        ['知乎', '', '', '', '', '', '', '', ''],
        ['官网 / PC 端', '', '', '', '', '', '', '', ''],
        ['微信小程序', '', '', '', '', '', '', '', ''],
        ['携程 / 美团商家版', '', '', '', '', '', '', '', ''],
        ['其他（请注明）', '', '', '', '', '', '', '', ''],
    ]
)
P(doc, '')

# ========== 四、运营团队情况 ==========
T2(doc, '四、运营团队情况')
add_table(doc,
    ['序号 *', '字段 *', '填写说明', '填写内容'],
    [
        ['1', '是否有专职新媒体运营人员 *', '单选', '☐ 是 ☐ 否'],
        ['2', '专职运营人数', '整数（含主管）', '_______ 人'],
        ['3', '兼职 / 借调人数', '整数', '_______ 人'],
        ['4', '团队负责人姓名 *', '姓名 + 岗位', ''],
        ['5', '团队负责人联系电话 *', '手机', ''],
        ['6', '运营团队是否有设计/视频/拍摄能力', '单选', '☐ 自有 ☐ 外包 ☐ 部分外包 ☐ 无'],
    ]
)
P(doc, '')

# ========== 五、第三方代运营情况 ==========
T2(doc, '五、第三方代运营情况')
P(doc, '* 若无第三方代运营，本节第 1 题选"否"后其余可空。')
add_table(doc,
    ['序号 *', '字段 *', '填写说明', '填写内容'],
    [
        ['1', '是否有第三方代运营 *', '单选', '☐ 是 ☐ 否'],
        ['2', '代运营公司全称', '含品牌名/主体公司', ''],
        ['3', '合同期限', '起止日期', '_______ 至 _______'],
        ['4', '年费金额', '元/年', '¥ _______'],
        ['5', '服务内容', '简述（如：内容生产 / 投流 / 直播等）', ''],
        ['6', '续约计划', '单选', '☐ 续约 ☐ 不续约 ☐ 待评估'],
        ['7', '对第三方服务的核心诉求', '主观填空（最多 200 字）', ''],
    ]
)
P(doc, '')

# ========== 六、现有内容特色 ==========
T2(doc, '六、现有内容特色')
add_table(doc,
    ['序号 *', '字段 *', '填写说明', '填写内容'],
    [
        ['1', '常发布内容类型 *', '多选', '☐ 产品 ☐ 活动 ☐ UGC ☐ 品牌故事 ☐ 当地文化 ☐ 其他'],
        ['2', '过去 6 个月最高传播内容', '标题 + 阅读量', '标题：_____________________ 阅读量：_______'],
        ['3', '酒店专属 IP（如有）', 'IP 名称 + 运营状态', 'IP 名称：_____________________ 状态：☐ 已运营 ☐ 筹备中 ☐ 无'],
        ['4', '客户 / 会员社群', '社群名称 + 规模', '社群：_____________________ 规模：_______ 人'],
        ['5', '酒店自媒体传播亮点', '简述 1 个最具代表性的传播案例', ''],
    ]
)
P(doc, '')

# ========== 七、营销协同情况 ==========
T2(doc, '七、营销协同情况')
add_table(doc,
    ['序号 *', '字段 *', '填写说明', '填写内容'],
    [
        ['1', '是否参与过集团统一营销活动 *', '单选', '☐ 是 ☐ 否'],
        ['2', '是否使用集团会员体系（安逸会）*', '单选', '☐ 是 ☐ 否'],
        ['3', '会员体系名称', '如使用，填写体系名称', ''],
        ['4', '客群结构（商务/度假/亲子/老年）', '各占比 %，合计 100%', '商务 ___% 度假 ___% 亲子 ___% 老年 ___%'],
        ['5', '主要 OTA 渠道占比', '携程/美团/同程/飞猪/抖音/自营，各占比 %', '携程 ___% 美团 ___% 同程 ___% 飞猪 ___% 抖音 ___% 自营 ___%'],
        ['6', '酒店年度新媒体相关预算', '元/年', '¥ _______'],
    ]
)
P(doc, '')

# ========== 八、签字确认 ==========
T2(doc, '八、签字确认')
P(doc, '本表所填数据真实有效，授权集团产业发展部在"集团新媒体矩阵统筹"立项决策范围内使用。')
P(doc, '')

add_table(doc,
    ['岗位 *', '姓名 *', '签字 / 盖章 *', '日期 *'],
    [
        ['营销 / 新媒体负责人', '', '', ''],
        ['酒店总经理', '', '', ''],
        ['集团产业发展部接收人', '', '', ''],
    ]
)
P(doc, '')
P(doc, '—— 本表结束 ——', center=True)

# 保存
doc.save(TARGET)
print(f'[OK] {TARGET}')
print(f'文件大小：{os.path.getsize(TARGET) / 1024:.1f} KB')