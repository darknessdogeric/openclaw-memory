# -*- coding: utf-8 -*-
"""安逸集团企业级AI平台 v3.0：场景与价值锚 / 计量与套餐 / 轻资产管道测算 / 采购包 / 合同条款 / 询价台账"""
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUT = r"C:\\Users\\ericz\\Desktop\\产业发展部\\项目\\集团企业级AI平台\\安逸集团企业级AI平台_场景_计量套餐_管道测算_v3.0_2026-11-21.xlsx"
NAVY, ORANGE, LBLUE, GREY = "1B2A41", "E8792B", "EAF0F6", "F5F7F9"
thin = Side(style="thin", color="C9D2DD"); BORD = Border(left=thin, right=thin, top=thin, bottom=thin)
wb = Workbook()

def sheet(name, title, subtitle, widths):
    ws = wb.create_sheet(name); ws.sheet_view.showGridLines = False
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(widths))
    c = ws.cell(row=1, column=1, value=title)
    c.font = Font(name="Microsoft YaHei", size=13, bold=True, color="FFFFFF")
    c.fill = PatternFill("solid", fgColor=NAVY); c.alignment = Alignment(vertical="center", indent=1)
    ws.row_dimensions[1].height = 26
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(widths))
    c = ws.cell(row=2, column=1, value=subtitle)
    c.font = Font(name="Microsoft YaHei", size=9, color="44546A"); c.alignment = Alignment(vertical="center", indent=1)
    return ws

def head(ws, row, vals, fill=NAVY):
    for j, v in enumerate(vals, 1):
        c = ws.cell(row=row, column=j, value=v)
        c.font = Font(name="Microsoft YaHei", size=10, bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=fill)
        c.alignment = Alignment(vertical="center", horizontal="center", wrap_text=True); c.border = BORD
    ws.row_dimensions[row].height = 24

def put(ws, row, vals, bold=False, fill=None, num=None):
    for j, v in enumerate(vals, 1):
        c = ws.cell(row=row, column=j, value=v)
        c.font = Font(name="Microsoft YaHei", size=10, bold=bold); c.border = BORD
        c.alignment = Alignment(vertical="center", horizontal=("left" if j == 1 else "center"), wrap_text=True)
        if fill: c.fill = PatternFill("solid", fgColor=fill)
        if num and num.get(j): c.number_format = num[j]
    return row + 1

# 1 场景与价值锚
ws = sheet("1_场景与价值锚", "四类场景应用与首年价值锚",
           "价值锚来源：旗下酒店经营看板（40家口径，截至2026-11-16累计年化）｜行业公开监测数据",
           [18, 34, 26, 34, 22])
r = 4
head(ws, r, ["场景", "核心能力", "服务对象", "首年价值锚", "测算口径"]); r += 1
for i, s in enumerate([
 ("集团智能化办公", "制度与知识问答、文稿起草、纪要与待办、数据分析问答", "集团总部职能与门店", "知识工作者提效；答案带出处比例100%", "提效类，无直接收入锚"),
 ("AI收益管理", "需求预测、动态定价、库存与超售、渠道比价、竞品监测", "自营与在营酒店、轻资产在管酒店", "客房RevPAR提升3%至5%，年增收约519万至865万元", "客房年化收入1.73亿元 × 3%~5%"),
 ("智能营销获客雷达", "渠道与点评动态监测、竞品与舆情跟踪、目的地需求感知、获客机会与投放建议", "自营与在营酒店、轻资产在管酒店", "渠道份额与点评资产由不可见转为可运营", "OTA五家占92.9%份额、携程56%；依托集团既有OTA运营与点评知识资产"),
 ("智能化资源匹配", "客需与房型、餐饮、会议、康养、供应商、渠道资源的撮合与推荐", "自营与在营酒店", "餐饮收入提升1%约275万元；会议收入提升1.5%约31万元", "餐饮年化2.75亿元同比仅增2.12%，与客房增速差10.25个百分点；会议年化2075万元"),
]):
    r = put(ws, r, list(s), fill=(GREY if i % 2 == 0 else None))
r += 1
r = put(ws, r, ["三项经营价值合计约825万元（收益管理519~865万取519万 + 资源匹配275万 + 会议31万），对应首年总投入245.8万元，投入产出比约3.4倍。"], bold=True, fill=LBLUE)

# 2 计量与套餐
ws = sheet("2_计量与套餐体系", "两种承载方式与套餐目录建议",
           "计量单位：1安逸算力点（AIP）＝10,000tokens，缓存命中按0.2AIP计｜定价建议待集团核定",
           [18, 26, 24, 18, 30])
r = 4
head(ws, r, ["承载方式", "计量单位", "适用对象", "定价方式", "备注"]); r += 1
for i, s in enumerate([
 ("按计量", "安逸算力点（AIP）", "集团内部结算、超额加购、定制调用", "0.15元/AIP（内部结算价）", "成本加成，原始账可逐月对账"),
 ("按计量", "安逸算力点（AIP）", "轻资产业主与合作方", "0.30元/AIP（合作方价，首年七折渗透0.21）", "对外真收入，按计量钱包月结"),
 ("按套餐", "席位／门店／客房规模", "五类套餐（见下表）", "订阅年费＋含月度配额，超出按计量加购", "签约对象是套餐，计量是履约与结算依据"),
]):
    r = put(ws, r, list(s), fill=(GREY if i % 2 == 0 else None))
r += 1
head(ws, r, ["套餐", "适用场景", "计费单位", "建议价（待核定）", "含配额建议"], fill=ORANGE); r += 1
for i, s in enumerate([
 ("办公协同包", "集团智能化办公", "席位／年", "0.3万至0.8万", "300至600 AIP/席/月"),
 ("收益管理包", "AI收益管理", "店／年", "2万至8万（营收0.4%至1.2%）", "2000至4000 AIP/月"),
 ("获客雷达包", "智能营销获客雷达", "店／年", "1万至4万", "1500至3000 AIP/月"),
 ("资源匹配包", "智能化资源匹配", "店／年", "1万至3万", "1000至2000 AIP/月"),
 ("轻资产赋能包", "对外拓展赋能（主推）", "委托管理店／年", "1.5万（<100房）／3.5万（100至300房）／6万（>300房）", "3000至6000 AIP/月"),
]):
    r = put(ws, r, list(s), fill=(GREY if i % 2 == 0 else None))

# 3 轻资产管道测算
ws = sheet("3_轻资产赋能管道测算", "轻资产赋能管道收入测算",
           "基数来源：轻资产在管酒店名录（2026-09-15，43家）＋2026年度已签约项目11个",
           [30, 26, 18, 18, 18, 30])
r = 4
head(ws, r, ["项", "口径", "数量", "单店房量", "金额（万元）", "说明"]); r += 1
for i, s in enumerate([
 ("在管酒店名录", "2026-09-15 口径", "43家", "5925间／均132间", "", "管理公司：饭店管理公司33／安逸连锁6／安逸远山2／国堰4"),
 ("其中已上线", "可立即落地赋能", "28家", "—", "约98", "按赋能包均价3.5万元/店测算"),
 ("其中未上线", "随开业挂载", "13家", "—", "约45", "按3.5万元/店，2027年内逐步接入"),
 ("2026年已签约项目", "品牌输出5／委托管理运营4／民宿文旅4", "11个", "—", "约20", "按50%挂载率、3.5万元/店测算"),
 ("首年对外管道收入", "不含内部结算", "", "", "约100至120", "不含计量超额与增值"),
 ("2029年对外管道收入", "含累积挂载与规模扩张", "", "", "约400至550", "随在管店数与新签项目增长"),
]):
    r = put(ws, r, list(s), fill=(GREY if i % 2 == 0 else None))
r += 1
r = put(ws, r, ["口径说明：管道收入指对外赋能的商机管道与落地收入，与行业开业管道（pipeline）为不同概念，须在合同与台账中分别表述，避免口径混淆。"], bold=True, fill="FFF3E8")

# 4 采购包
ws = sheet("4_采购包与方式", "采购包划分、限额对照与采购方式",
           "依据《川旅投发〔2026〕147号 招标及采购管理办法（2026年修订）》｜成文 2026-11-21",
           [8, 44, 14, 20, 28, 14, 22])
r = 4
head(ws, r, ["包号", "采购标的", "估算金额（万元）", "限额对照", "拟采用采购方式", "依据条款", "审批权限"]); r += 1
f = r
for i, s in enumerate([
 ("主包", "本地大模型构建与场景应用开发及运营服务外包（基座许可、语料治理、领域微调与评测、模型部署与推理、四类场景应用、计量与套餐体系、对外赋能工具、运维与增量训练）", 150.0, "服务类单项达50万元以上", "公开招标（依法必招），适用中标候选人评定分离机制", "第十四条第四项、第三十六条、第二十三条", "达两会一层限额，按总部决策程序报批（限额待核定）"),
 ("包2", "第三方独立服务（等级保护测评配合、渗透测试、安全审计复核）", 8.0, "5万元以上、50万元以下", "询比采购", "第十五条", "总经理审批权限以内"),
 ("包3", "培训与变革（部门培训、场景陪跑）", 3.8, "5万元以下", "向不少于3家合格供应商询价比价", "第十九条", "总经理审批权限以内"),
]):
    r = put(ws, r, list(s), fill=(GREY if i % 2 == 0 else None), num={3: "0.0"})
r = put(ws, r, ["合计", "三个采购包", f"=SUM(C{f}:C{r-1})", "整体落在第二十二条20万至200万区间", "主包公开招标＋两包限额以下方式", "第十四至十九条", "要件审查由招标领导小组专题会审批"], bold=True, fill=LBLUE, num={3: "0.0"})

# 5 最高限价测算
ws = sheet("5_主包最高限价测算", "主包招标最高限价测算口径", "投标价超过最高限价的按废标处理", [8, 30, 50, 16])
r = 4
head(ws, r, ["#", "测算项", "口径", "估算（万元）"]); r += 1
f2 = r
for i, s in enumerate([
 ("1", "本地大模型构建与迭代", "基座许可、语料治理、领域微调、评测、部署、季度增量训练", 30.0),
 ("2", "四类场景应用开发", "集团智能化办公、AI收益管理、智能营销获客雷达、智能化资源匹配，含验收与迭代", 60.0),
 ("3", "计量与套餐体系", "计量原始账、套餐目录、内部结算与对外计费、计量钱包", 20.0),
 ("4", "算力与模型服务", "训练与推理、专用实例、按量结算并设年度上限", 22.0),
 ("5", "运行维护与迭代", "驻场或远程运维、版本升级、故障响应", 18.0),
]):
    r = put(ws, r, list(s), fill=(GREY if i % 2 == 0 else None), num={4: "0.0"})
r = put(ws, r, ["", "合计（招标最高限价）", "按三年总拥有成本折算的年均服务价格，参考不少于3家潜在供应商初步报价", f"=SUM(D{f2}:D{r-1})"], bold=True, fill=LBLUE, num={4: "0.0"})

# 6 合同八项
ws = sheet("6_合同八项硬条款", "合同必须写明的八项事项", "缺一即为合同评审不通过", [6, 20, 72, 26])
r = 4
head(ws, r, ["#", "条款", "要点", "对应风险"]); r += 1
for i, s in enumerate([
 ("1", "数据主权与可导出", "客人信息、员工薪酬、财务明细与集团语料不得离开集团指定环境；供应商不得留存、不得用于训练以外用途；终止后删除并出具证明", "数据主权外溢"),
 ("2", "开放接口与互操作", "提供标准接口，集团自有系统可对接；不得设置排他性、独家绑定或接口封锁条款", "供应商锁定"),
 ("3", "付款与验收挂钩", "按本地大模型、四类场景应用、计量与套餐体系三个节点分阶段验收付款；集团评测集结果为验收硬条件", "效果不达预期"),
 ("4", "服务水平", "明确可用性、响应时限、故障恢复时限、版本升级节奏与重大故障通报；未达标约定服务费扣减", "断供"),
 ("5", "价格与调整机制", "锁定三年服务价格与年度涨幅上限；模型与算法升级不得单独加价；新增需求另行履行限额判定与审批", "范围蔓延"),
 ("6", "模型资产与语料资产归属", "基座许可须覆盖商用与对外赋能；权重、语料、提示词版本、特征工程代码、训练脚本与评测集归集团并归档逐项交付；供应商不得留存或主张任何权利", "模型资产流失"),
 ("7", "退出与迁移机制", "约定终止条件、数据与模型资产导出格式、迁移协助义务与过渡期安排，集团具备更换服务方的能力", "断供与锁定"),
 ("8", "违约责任与保密", "明确未达服务水平与未交资产（权重、语料、评测集）的违约责任、知识产权侵权责任与保密义务", "整体违约风险"),
]):
    r = put(ws, r, list(s), fill=(GREY if i % 2 == 0 else None))

# 7 询价台账
ws = sheet("7_询价记录台账", "询价记录台账（待填）", "用于最高限价测算；每个包不少于3家；含税口径；报价有效期不少于30日；须签认", [8, 26, 14, 16, 12, 12, 12, 20])
r = 4
head(ws, r, ["包号", "询价对象", "询价日期", "报价金额（含税）", "是否含税", "有效期", "签认", "备注"]); r += 1
for pk in ["主包"] * 9 + ["包2"] * 3 + ["包3"] * 3:
    r = put(ws, r, [pk, None, None, None, None, None, None, None], fill=(GREY if r % 2 == 0 else None))
r += 1
r = put(ws, r, ["询价函要点：①采购标的与包号；②测算口径与工作量口径；③报价须含税并注明税率；④报价有效期不少于30日；⑤须提供资格材料（营业执照、业绩、财务、资质）；⑥报价截止时间与送达方式；⑦声明所报价格不得高于最高限价；⑧须逐条回应合同八项硬条款；⑨须单列模型权重、语料、评测集的交付与归属条款。"], bold=True, fill=LBLUE)

del wb["Sheet"]
os.makedirs(os.path.dirname(OUT), exist_ok=True)
wb.save(OUT)
print("SAVED:", OUT, os.path.getsize(OUT))