# -*- coding: utf-8 -*-
"""安逸集团AI智能化体系 · 需求条目与应答表（致合作方 v2.0）"""
import io, os, re
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\07_战略与改革"
MD = os.path.join(KB, "2026-11-21_安逸集团AI智能化体系技术服务需求说明书_致合作方_v2.0.md")
DST = r"C:\Users\ericz\Desktop\产业发展部\项目\集团企业级AI平台"
OUT = os.path.join(DST, "安逸集团AI智能化体系_需求条目_应答表_报价表_致合作方_v2.0_2026-11-21.xlsx")

md = io.open(MD, encoding="utf-8").read().split("\n")
items = []
for l in md:
    m = re.match(r"^\|\s*((?:AR|S)-\d{2})\s*\|", l)
    if m:
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        items.append(c[:5])
print("parsed items:", len(items), "AR:", sum(1 for x in items if x[0].startswith("AR")),
      "S:", sum(1 for x in items if x[0].startswith("S")))

NAVY, ORANGE, LBLUE, GREY = "1B2A41", "E8792B", "EAF0F6", "F5F7F9"
thin = Side(style="thin", color="C9D2DD")
BORD = Border(left=thin, right=thin, top=thin, bottom=thin)
wb = Workbook()


def sheet(name, title, subtitle, widths):
    ws = wb.create_sheet(name)
    ws.sheet_view.showGridLines = False
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(widths))
    c = ws.cell(row=1, column=1, value=title)
    c.font = Font(name="Microsoft YaHei", size=13, bold=True, color="FFFFFF")
    c.fill = PatternFill("solid", fgColor=NAVY)
    c.alignment = Alignment(vertical="center", indent=1)
    ws.row_dimensions[1].height = 26
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(widths))
    c = ws.cell(row=2, column=1, value=subtitle)
    c.font = Font(name="Microsoft YaHei", size=9, color="44546A")
    c.alignment = Alignment(vertical="center", indent=1)
    return ws


def head(ws, row, vals, fill=NAVY):
    for j, v in enumerate(vals, 1):
        c = ws.cell(row=row, column=j, value=v)
        c.font = Font(name="Microsoft YaHei", size=10, bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=fill)
        c.alignment = Alignment(vertical="center", horizontal="center", wrap_text=True)
        c.border = BORD
    ws.row_dimensions[row].height = 26


def put(ws, row, vals, bold=False, fill=None):
    for j, v in enumerate(vals, 1):
        c = ws.cell(row=row, column=j, value=v)
        c.font = Font(name="Microsoft YaHei", size=10, bold=bold)
        c.border = BORD
        c.alignment = Alignment(vertical="center", horizontal=("left" if j == 1 else "center"), wrap_text=True)
        if fill:
            c.fill = PatternFill("solid", fgColor=fill)
    return row + 1


# 1 需求条目与应答
ws = sheet("1_需求条目与应答", "需求条目总清单与逐条应答表（先架构后场景）",
           "AR 为总体架构条目（先行提交、单独成册）｜S 为场景开发条目｜P0 必答，P0 不满足视为不响应｜灰底为合作方填写栏",
           [9, 12, 30, 34, 8, 12, 30, 24, 12, 10, 10])
r = 4
head(ws, r, ["编号", "类别", "需求摘要", "关键指标", "优先级", "满足状态", "实现方式说明", "偏差与前置条件", "证明材料索引", "工作量(人日)", "完成时间"])
r += 1
for i, it in enumerate(items):
    r = put(ws, r, list(it) + [None, None, None, None, None, None], fill=(GREY if i % 2 == 0 else None))
r += 1
r = put(ws, r, ["合计 %d 条：总体架构 %d 条（AR-01 至 AR-14），场景开发 %d 条（S-01 至 S-25）；P0 %d 条 / P1 %d 条 / P2 %d 条。总体架构方案须单独成册并先行提交，通过评审后再进入场景方案与报价确认。"
            % (len(items), sum(1 for x in items if x[0].startswith("AR")), sum(1 for x in items if x[0].startswith("S")),
               sum(1 for x in items if x[4] == "P0"), sum(1 for x in items if x[4] == "P1"), sum(1 for x in items if x[4] == "P2"))],
        bold=True, fill=LBLUE)

# 2 交付物与验收
ws = sheet("2_交付物与验收指标", "交付物清单与验收量化指标", "时限自合同签订与进场起算", [8, 26, 40, 16, 18, 22])
r = 4
head(ws, r, ["序号", "交付物", "内容要求", "形式", "时限", "验收方"])
r += 1
for i, s in enumerate([
 ("1", "总体架构方案", "四层架构、多入口适配、可拓展机制、三大业务线适配、演进路径", "文档与架构图", "第4周", "产业发展部"),
 ("2", "基座模型候选与许可说明", "候选对比、许可文件、量化与并发评估", "文档", "第5周", "产业发展部"),
 ("3", "集团语料清单与治理成果", "语料目录、密级与有效期标注表、清洗去敏记录", "文档与数据", "第6周", "产业发展部"),
 ("4", "集团本地大模型", "权重、加载说明、依赖清单", "模型与文档", "第12周", "产业发展部"),
 ("5", "微调与训练资产", "训练脚本、数据版本、超参数、复现说明", "代码与文档", "第12周", "产业发展部"),
 ("6", "评测集与回归工具", "四类任务各不少于50条、回归脚本与报告模板", "数据与工具", "第10周", "产业发展部"),
 ("7", "部署架构与数据流向说明", "架构图、租户边界控制、出域审计方案", "文档与部署", "第6周", "集团安全与审计"),
 ("8", "九类场景应用", "办公、收益管理、获客雷达、AICRM、在店服务、工单分发、预订需求匹配、新媒体、新零售", "应用与文档", "第14至18周", "产业发展部"),
 ("9", "计量与结算体系", "原始账、折算规则、套餐目录、内外部价目分离、计量钱包、报表", "系统与文档", "第10周", "产业发展部"),
 ("10", "统一接入协议与能力目录", "协议模板、能力目录、对外报价工具", "文档与配置", "第12周", "产业发展部与法务"),
 ("11", "系统接口封装", "各业务系统接口清单与封装成果", "代码与文档", "第12周", "集团IT"),
 ("12", "安全与合规配套", "网段隔离、权限矩阵、熔断、审计、供应链管控、注入防护", "方案与演练记录", "第10周", "集团安全"),
 ("13", "运维与服务水平", "运维手册、SLA、响应与恢复机制、季度增量训练机制", "文档", "第12周", "产业发展部"),
 ("14", "模型与语料资产归档包", "权重、语料、脚本、评测集资产清单", "归档包", "第12周", "产业发展部"),
]):
    r = put(ws, r, list(s), fill=(GREY if i % 2 == 0 else None))
r += 1
head(ws, r, ["类别", "验收指标", "目标值", "验收方式", "验收方", ""], fill=ORANGE)
r += 1
for i, s in enumerate([
 ("架构", "总体架构通过评审", "四层齐备、多入口可复用、可横向扩展", "集团架构评审", "产业发展部", ""),
 ("模型", "评测集相对基座提升", "不低于15个百分点", "集团评测集回归", "产业发展部", ""),
 ("模型", "资产归档完整度", "清单逐项签收", "资产清单签收", "产业发展部", ""),
 ("拓展", "新增场景接入周期", "不超过15个工作日", "接入台账与计时记录", "产业发展部", ""),
 ("多入口", "同一能力复用入口数", "不少于3类", "调用链路核验", "产业发展部", ""),
 ("办公", "抽测准确率／带出处比例", "不低于90%／100%", "50题抽测与抽样核验", "产业发展部", ""),
 ("收益管理", "试点门店RevPAR提升", "不低于3%", "试点前后同口径对照", "产业发展部与运营条线", ""),
 ("获客雷达", "负面主题预警时效／分类准确率", "24小时内／不低于80%", "连续30天运行记录", "产业发展部", ""),
 ("客户管理", "标签准确率", "不低于80%", "抽样标注核对", "产业发展部", ""),
 ("工单", "自动分派准确率", "不低于85%", "工单抽样复核", "产业发展部", ""),
 ("计量", "原始账可对账率／敏感出域事件", "100%／零", "月度对账与审计抽检", "产业发展部与审计", ""),
 ("外部拓展", "外部接入认证周期", "不超过15个工作日", "接入台账与计时记录", "产业发展部", ""),
 ("安全", "安全门槛自检", "全部通过", "自检表与第三方渗透测试", "集团安全", ""),
]):
    r = put(ws, r, list(s), fill=(GREY if i % 2 == 0 else None))

# 3 报价表
ws = sheet("3_报价表模板", "报价表模板（合作方填写）",
           "算力与模型服务按量结算并设年度上限，严禁年包干；价格锁定三年并约定年度涨幅上限",
           [6, 30, 14, 14, 14, 26, 16, 34, 22])
r = 4
head(ws, r, ["序号", "报价项", "首年(万元)", "第二年(万元)", "第三年(万元)", "计价单位与口径", "含税与税率", "包含范围", "备注"])
r += 1
for i, s in enumerate([
 ("1", "总体架构与底座构建", None, None, None, None, None, "架构设计、基座许可、语料治理、微调评测、部署", None),
 ("2", "九类场景开发", None, None, None, None, None, "办公、收益管理、获客雷达、AICRM、在店服务、工单、预订匹配、新媒体、新零售", None),
 ("3", "计量与结算体系", None, None, None, None, None, "原始账、折算、套餐目录、价目分离、计量钱包、报表", None),
 ("4", "算力与模型服务", None, None, None, "按量结算，须列年度上限", None, "训练与推理、专用实例", None),
 ("5", "运行维护与迭代", None, None, None, None, None, "驻场或远程、升级、故障响应", None),
 ("6", "合计", None, None, None, None, None, None, None),
 ("7", "规模分档单价表", None, None, None, "按场景与接入规模分档", None, "含外部接入与场景分档", None),
 ("8", "一次性费用与年度涨幅上限承诺", None, None, None, None, None, "列明涨幅上限", None),
]):
    r = put(ws, r, list(s), fill=(GREY if i % 2 == 0 else None))

# 4 演示与时间
ws = sheet("4_演示与时间安排", "现场演示要求与时间安排", "不参加演示的按未响应处理；架构方案先行、场景方案随后", [8, 30, 50, 16])
r = 4
head(ws, r, ["序号", "演示内容", "演示标准", "时长"])
r += 1
for i, s in enumerate([
 ("1", "总体架构", "现场讲解四层架构、多入口适配与可拓展机制，并演示一个能力在两类入口上的复用", "40分钟"),
 ("2", "模型构建与语料治理", "展示语料治理流程、评测集构成与微调前后对比", "30分钟"),
 ("3", "场景应用", "从九类场景中任选三类现场演示", "60分钟"),
 ("4", "计量与对账", "展示原始账到月度账单的完整链路", "20分钟"),
]):
    r = put(ws, r, list(s), fill=(GREY if i % 2 == 0 else None))
r += 1
head(ws, r, ["事项", "时点", "", ""], fill=ORANGE)
r += 1
for i, s in enumerate([
 ("需求说明书发出", "2026年11月21日", "", ""),
 ("答疑截止", "2026年12月5日", "", ""),
 ("总体架构方案提交截止", "2026年12月8日", "", ""),
 ("架构方案评审", "2026年12月10日至12日", "", ""),
 ("场景方案与报价提交截止", "2026年12月22日", "", ""),
 ("现场演示", "2026年12月24日至25日", "", ""),
 ("商务评审与定标", "2027年1月", "", ""),
 ("合同签订与进场", "2027年2月", "", ""),
]):
    r = put(ws, r, list(s), fill=(GREY if i % 2 == 0 else None))

# 5 集团规模信息（对外口径）
ws = sheet("5_集团规模信息", "集团业务规模（对外口径）", "本表仅提供规模信息，不含经营与财务数据；如需其他口径请在答疑中提出", [26, 66, 26])
r = 4
head(ws, r, ["业务板块", "规模", "备注"])
r += 1
for i, s in enumerate([
 ("自有资产酒店", "17家，覆盖全服务式、精选生活方式、文化精品、度假康养等档次", "重资产自营"),
 ("轻资产委托管理及品牌输出项目", "43家，其中已开业33家", "分布四川省内及重庆、海南等省市"),
 ("在营酒店项目合计", "50余家，客房规模约1万间", "口径为已开业项目"),
 ("茶业", "茶山及茶产业相关业务，含自有茶园、茶山文旅与非遗茶空间", "含文创礼赠业务"),
 ("新零售", "自营零售门店、电商与集采渠道、文创与礼赠业务", "含多渠道电商运营"),
 ("现有数字化系统", "涵盖酒店PMS与中央预订、财务、合同、办公、会员与商城等", "暂无统一AI底座"),
]):
    r = put(ws, r, list(s), fill=(GREY if i % 2 == 0 else None))

# 6 商务硬性条款
ws = sheet("6_商务硬性条款", "商务硬性条款（七项）与架构承诺", "缺一即为合同评审不通过", [6, 20, 72, 26])
r = 4
head(ws, r, ["#", "条款", "要点", "对应风险"])
r += 1
for i, s in enumerate([
 ("1", "数据主权与可导出", "客人信息、员工薪酬、财务明细与集团语料不得离开集团指定环境；不得留存、不得用于训练以外用途；终止后删除并出具证明", "数据主权外溢"),
 ("2", "开放接口与互操作", "提供标准接口，集团自有系统可对接；不得设置排他性、独家绑定或接口封锁条款", "供应商锁定"),
 ("3", "付款与验收挂钩", "按底座与模型、场景应用、计量与结算体系三个节点分阶段验收付款；集团评测集结果为验收硬条件", "效果不达预期"),
 ("4", "服务水平", "明确可用性、响应时限、故障恢复时限、版本升级节奏与重大故障通报；未达标约定服务费扣减", "断供"),
 ("5", "价格与调整机制", "锁定三年服务价格与年度涨幅上限；模型与算法升级不得单独加价；新增需求另行履行限额判定与审批", "范围蔓延"),
 ("6", "模型资产与语料资产归属", "基座许可须覆盖商用与对外赋能；权重、语料、提示词版本、特征工程代码、训练脚本与评测集归集团并归档逐项交付", "模型资产流失"),
 ("7", "退出与迁移机制", "约定终止条件、数据与模型资产导出格式、迁移协助义务与过渡期安排，集团具备更换服务方的能力", "断供与锁定"),
 ("8", "违约责任与保密", "明确未达服务水平与未交资产的违约责任、知识产权侵权责任与保密义务，保密义务在合作结束后继续有效", "整体违约风险"),
 ("9", "能力可拓展与多入口复用承诺", "承诺新增场景接入周期不超过15个工作日、同一能力可在不少于3类入口复用、接入机制以标准SDK与开发规范交付", "体系僵化"),
]):
    r = put(ws, r, list(s), fill=(GREY if i % 2 == 0 else None))

del wb["Sheet"]
os.makedirs(os.path.dirname(OUT), exist_ok=True)
wb.save(OUT)
print("SAVED:", OUT, os.path.getsize(OUT))
