# -*- coding: utf-8 -*-
"""安逸集团企业级AI平台项目 采购包划分（整体外包·公开招标版）与控制价、评标、合同条款、询价记录一体表"""
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUT = r"C:\Users\ericz\Desktop\产业发展部\项目\集团企业级AI平台\安逸集团企业级AI平台_采购包划分_评标与合同条款_询价记录_v2.0_2026-11-20.xlsx"
NAVY, ORANGE, LBLUE, GREY, RED = "1B2A41", "E8792B", "EAF0F6", "F5F7F9", "B4232B"
thin = Side(style="thin", color="C9D2DD")
BORD = Border(left=thin, right=thin, top=thin, bottom=thin)
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
        c.font = Font(name="Microsoft YaHei", size=10, bold=bold)
        c.border = BORD
        c.alignment = Alignment(vertical="center", horizontal=("left" if j == 1 else "center"), wrap_text=True)
        if fill: c.fill = PatternFill("solid", fgColor=fill)
        if num and num.get(j): c.number_format = num[j]
    return row + 1

ws = sheet("1_采购包与方式", "采购包划分、限额对照与采购方式（整体外包版）",
           "依据《川旅投发〔2026〕147号 招标及采购管理办法（2026年修订）》｜成文 2026-11-20｜内部讨论稿",
           [8, 44, 14, 20, 30, 14, 24])
r = 4
head(ws, r, ["包号", "采购标的", "估算金额（万元）", "限额对照", "拟采用采购方式", "依据条款", "审批权限"]); r += 1
pk = [
 ("主包", "安逸集团企业级AI平台建设与运营服务外包（平台软件、算力与微调、六系统工具接口封装、三个首发场景、计量结算模块、安全运行时、运维与迭代）", 130.0, "服务类单项达50万元以上", "公开招标（依法必招），按中标候选人评定分离机制确定中标人", "第十四条第四项、第三十六条、第二十三条", "达两会一层限额，按总部决策程序报批（限额待核定）"),
 ("包2", "第三方独立服务（等级保护测评配合、渗透测试、安全审计复核）", 8.0, "5万元以上、50万元以下", "询比采购", "第十五条", "总经理审批权限以内"),
 ("包3", "培训与变革（部门培训、业务自建陪跑、变革沟通）", 3.8, "5万元以下", "向不少于3家合格供应商询价比价并形成书面比价记录", "第十九条", "总经理审批权限以内"),
]
first = r
for i, p in enumerate(pk):
    r = put(ws, r, list(p), fill=(GREY if i % 2 == 0 else None), num={3: "0.0"})
r = put(ws, r, ["合计", "三个采购包", f"=SUM(C{first}:C{r-1})", "整体落在第二十二条20万至200万区间", "主包公开招标＋两包限额以下方式", "第十四至十九条", "要件审查由招标领导小组专题会审批"], bold=True, fill=LBLUE, num={3: "0.0"})
r += 1
r = put(ws, r, ["拆分合规说明：主包已按服务类招标限额以上以公开招标方式实施，不存在以限额以下方式规避公开招标的情形；包2为第三方检测认证独立服务，包3为培训服务，均与主包标的性质不同。按第十九条同一标的不得拆分多次以限额以下方式采购的规定，上述分包不构成对同一标的的分割规避。招标办须就标的独立性出具确认意见后方可实施。"], bold=True, fill="FFF3E8")

ws = sheet("2_主包最高限价测算", "主包招标最高限价测算口径", "投标价超过最高限价的按废标处理；最终以招标结果与合同为准", [8, 30, 46, 16])
r = 4
head(ws, r, ["#", "测算项", "口径", "估算（万元）"]); r += 1
base = [
 ("1", "平台软件许可与订阅", "首年，含编排、知识库、向量库、计量、评估、审计", 18.0),
 ("2", "算力承载与模型微调", "训练、推理、专有实例与微调蒸馏，按量结算并设年度上限", 22.0),
 ("3", "六类系统工具接口封装", "办公、PMS、CRS、财务、合同、经营分析，按接口数与人日单价", 15.0),
 ("4", "三个首发场景建设", "制度与知识问答、会议纪要与待办、材料起草", 32.0),
 ("5", "计量与结算模块建设", "计量原始账、AIP价目、内部结算与对外计费、计量钱包", 20.0),
 ("6", "安全运行时建设", "七条上线门槛落地、技能包白名单、审计留存加固", 12.0),
 ("7", "运行维护与迭代", "驻场或远程运维、版本升级、迭代支持", 11.0),
]
f2 = r
for i, b in enumerate(base):
    r = put(ws, r, list(b), fill=(GREY if i % 2 == 0 else None), num={4: "0.0"})
r = put(ws, r, ["", "合计（招标最高限价）", "按三年总拥有成本折算的年均服务价格，参考不少于3家潜在供应商初步报价与同类产品市场报价区间", f"=SUM(D{f2}:D{r-1})"], bold=True, fill=LBLUE, num={4: "0.0"})

ws = sheet("3_评标办法与流程", "主包评标办法建议与实施流程七步", "最终权重与评标细则由集团总部招标办审查、招标领导小组专题会审定后发布", [10, 20, 58, 22])
r = 4
head(ws, r, ["评分要素", "建议权重", "评分要点", "定档要求"]); r += 1
for i, s in enumerate([
 ("技术方案", "40%", "架构合理性、六系统接口能力、模型与微调能力、评估与可观测性", "具备三项以上同类案例且方案通过技术评审"),
 ("价格", "30%", "投标价与三年总拥有成本测算", "不超过招标最高限价"),
 ("服务与保障", "20%", "SLA、驻场与响应、版本与业务连续性", "响应时限与恢复时限优于招标要求"),
 ("数据主权与退出机制", "10%", "数据处理边界、权重与语料归属、可导出与迁移承诺", "须全部接受合同八项硬条款"),
]):
    r = put(ws, r, list(s), fill=(GREY if i % 2 == 0 else None))
r += 1
head(ws, r, ["步骤", "内容", "时限要求", "依据条款"], fill=ORANGE); r += 1
for i, s in enumerate([
 ("1 招采立项", "编制招采立项方案（项目概况、采购方式及原因、控制价设定依据），完成立项审批", "随立项报审同步完成", "第二十一条"),
 ("2 要件审查", "采购需求文件、资格条件与评标办法报总部招标办审查并专题会审批", "立项批复后10个工作日内提交", "第二十二条"),
 ("3 计划与报备", "纳入年度招标采购计划；每季度30日前备案；数字旅投平台线上办理", "年度计划每年2月末前上报", "第六条、第二十四条"),
 ("4 招标实施", "发布招标公告，潜在供应商不少于3家；依法必招按第三十六条评标并适用中标候选人评定分离", "公告期不少于5个工作日", "第十四条、第三十六条"),
 ("5 结果审批与合同", "确定中标人；公告公示、发出中标通知书、签订合同", "评标结束后5个工作日内启动公示", "第二十三条、第三十七条"),
 ("6 验收与结算", "分阶段验收（底座与计量模块、三个首发场景、安全运行时），合格后结算付款", "按合同约定节点分阶段验收", "第三十八条"),
 ("7 归档", "谁采购谁留痕，整理寻源决策、招采过程、合同与供应商管理资料", "采购档案保存不少于15年", "第三十九条"),
]):
    r = put(ws, r, list(s), fill=(GREY if i % 2 == 0 else None))

ws = sheet("4_合同八项硬条款", "合同必须写明的八项事项", "缺一即为合同评审不通过；这是外包模式下集团不被锁死的技术保障", [6, 18, 70, 26])
r = 4
head(ws, r, ["#", "条款", "要点", "对应风险"]); r += 1
for i, s in enumerate([
 ("1", "数据主权与可导出", "客人信息、员工薪酬、财务明细等敏感数据不得离开集团指定环境；供应商不得留存、不得用于训练以外的用途；服务终止后按约定删除并出具证明", "数据主权外溢"),
 ("2", "开放接口与互操作", "提供标准接口，集团自有系统可对接；不得设置排他性、独家绑定或接口封锁条款", "供应商锁定"),
 ("3", "付款与验收挂钩", "按底座与计量模块、三个首发场景、安全运行时三个节点分阶段验收付款；评估集结果为验收硬条件", "效果不达预期"),
 ("4", "服务水平", "明确可用性、响应时限、故障恢复时限、版本升级节奏与重大故障通报；未达标约定服务费扣减", "单一供应商断供"),
 ("5", "价格与调整机制", "锁定三年服务价格与年度涨幅上限；模型与算法升级不得单独加价；新增需求另行履行限额判定与审批", "范围蔓延"),
 ("6", "模型权重与语料归属", "微调产出的模型权重、训练语料、提示词版本与特征工程代码归集团所有并归档交付；供应商不得留存或另作他用", "供应商锁定"),
 ("7", "退出与迁移机制", "约定终止条件、数据与资产导出格式、迁移协助义务与过渡期安排，集团具备更换服务方的能力", "单一供应商断供"),
 ("8", "违约责任与保密", "明确未达服务水平的违约责任、知识产权侵权责任与保密义务，保密义务在终止后继续有效", "整体违约风险"),
]):
    r = put(ws, r, list(s), fill=(GREY if i % 2 == 0 else None))

ws = sheet("5_计划报备与审批时点", "计划、报备与审批时点", "公开招标链条长，倒排时点必须早于场景上线需求", [34, 22, 18, 20])
r = 4
head(ws, r, ["事项", "时点", "依据", "责任"]); r += 1
for i, s in enumerate([
 ("招采立项方案报审", "2026年11月", "第二十一条", "产业发展部"),
 ("初步询价与最高限价测算", "2026年12月", "第二十一条", "产业发展部"),
 ("采购需求文件、资格条件与评标办法报审", "2026年12月", "第二十二条", "总部招标办"),
 ("招标领导小组专题会审定要件与最高限价", "2026年12月", "第二十二条", "招标领导小组"),
 ("纳入2027年度招标采购计划上报", "2027年2月末前", "第六条", "产业发展部"),
 ("数字旅投平台线上办理报批报备", "招标实施前", "第二十四条", "总部招标办"),
 ("招标公告发布与投标", "2027年3月", "第十四条、第三十六条", "总部招标办"),
 ("开标评标与定标", "2027年4月", "第三十六条、第二十三条", "招标领导小组"),
 ("合同签订与平台建设进场", "2027年5月", "第三十七条", "产业发展部"),
 ("季度招采完成情况备案", "每季度30日前", "第二十四条", "产业发展部"),
]):
    r = put(ws, r, list(s), fill=(GREY if i % 2 == 0 else None))

ws = sheet("6_询价记录台账", "询价记录台账（待填）", "用于最高限价测算；每个包不少于3家；含税口径；报价有效期不少于30日；须签认", [8, 26, 14, 16, 12, 12, 12, 20])
r = 4
head(ws, r, ["包号", "询价对象", "询价日期", "报价金额（含税）", "是否含税", "有效期", "签认", "备注"]); r += 1
for pk2 in ["主包"] * 9 + ["包2"] * 3 + ["包3"] * 3:
    r = put(ws, r, [pk2, None, None, None, None, None, None, None], fill=(GREY if r % 2 == 0 else None))
r += 1
r = put(ws, r, ["询价函要点：① 采购标的与包号；② 测算口径与工作量口径；③ 报价须含税并注明税率；④ 报价有效期不少于30日；⑤ 须提供资格材料（营业执照、业绩、财务、资质）；⑥ 报价截止时间与送达方式；⑦ 声明所报价格不得高于最高限价；⑧ 须逐条回应合同八项硬条款；⑨ 采购人联系方式与监督部门。"], bold=True, fill=LBLUE)

del wb["Sheet"]
os.makedirs(os.path.dirname(OUT), exist_ok=True)
wb.save(OUT)
print("SAVED:", OUT, os.path.getsize(OUT))
