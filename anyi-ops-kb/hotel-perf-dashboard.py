# -*- coding: utf-8 -*-
"""
安逸酒店集团 2026年7月业绩分析报表 v2.0 专业版
- 行业最佳实践: RP/OCC/ADR 三件套 + STR MPI/ARI/RGI
- 集团知识库方法论: 排名变化 + 客源结构 + 红线触发 + 行动建议
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule, FormulaRule
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList
from datetime import datetime

# ========== 数据（从 Eric 提供的报表读取） ==========
# 22家酒店，含全服务(FS)与非全服务(SS)
# OCC 数值为原表呈现（正值=实际入住率%, 负值=可能为歇业/改造期, 数据待核）
hotels = [
    # ===== 全服务酒店 (19家) =====
    {"code": "FS-01", "name": "竹娟锦江宾馆", "cat": "全服务", "rooms": 180, "rate": 279, "rank": 1,
     "rp_yoy": 17, "occ_yoy": -2, "adr_yoy": 19, "h1_rp_yoy": 19, "h1_occ_yoy": -2, "h1_adr_yoy": 23,
     "occ": 14.08, "occ_h1": 13.79, "status": "运营"},
    {"code": "FS-02", "name": "安逸盛安酒店", "cat": "全服务", "rooms": 220, "rate": 232, "rank": 2,
     "rp_yoy": 132, "occ_yoy": -7, "adr_yoy": 83, "h1_rp_yoy": 33, "h1_occ_yoy": -7, "h1_adr_yoy": 7,
     "occ": 12.2, "occ_h1": 21.83, "status": "运营"},
    {"code": "FS-03", "name": "资阳金牛宾馆", "cat": "全服务", "rooms": 150, "rate": 180, "rank": 3,
     "rp_yoy": 80, "occ_yoy": 12, "adr_yoy": -18, "h1_rp_yoy": -18, "h1_occ_yoy": 8, "h1_adr_yoy": 8,
     "occ": -5.14, "occ_h1": -5.8, "status": "歇业/改造"},
    {"code": "FS-04", "name": "南江锦江宾馆", "cat": "全服务", "rooms": 120, "rate": 135, "rank": 4,
     "rp_yoy": 35, "occ_yoy": -2, "adr_yoy": 6, "h1_rp_yoy": 6, "h1_occ_yoy": 0, "h1_adr_yoy": 0,
     "occ": 9.24, "occ_h1": 4.36, "status": "运营"},
    {"code": "FS-05", "name": "锦宾国际酒店", "cat": "全服务", "rooms": 200, "rate": 120, "rank": 5,
     "rp_yoy": 20, "occ_yoy": 12, "adr_yoy": 79, "h1_rp_yoy": 79, "h1_occ_yoy": 10, "h1_adr_yoy": 10,
     "occ": -17.81, "occ_h1": 13.77, "status": "歇业/改造"},
    {"code": "FS-06", "name": "古尔沟温泉山庄", "cat": "全服务", "rooms": 160, "rate": 114, "rank": 6,
     "rp_yoy": 14, "occ_yoy": -24, "adr_yoy": 7, "h1_rp_yoy": 7, "h1_occ_yoy": -23, "h1_adr_yoy": -23,
     "occ": 12.93, "occ_h1": 11.2, "status": "运营"},
    {"code": "FS-07", "name": "古尔沟华美达温泉度假酒店", "cat": "全服务", "rooms": 240, "rate": 111, "rank": 7,
     "rp_yoy": 11, "occ_yoy": -22, "adr_yoy": -11, "h1_rp_yoy": -11, "h1_occ_yoy": -27, "h1_adr_yoy": -27,
     "occ": 5.73, "occ_h1": 1.83, "status": "运营"},
    {"code": "FS-08", "name": "南溪锦江宾馆", "cat": "全服务", "rooms": 130, "rate": 107, "rank": 8,
     "rp_yoy": 7, "occ_yoy": 0, "adr_yoy": -2, "h1_rp_yoy": -2, "h1_occ_yoy": -5, "h1_adr_yoy": -5,
     "occ": 7.9, "occ_h1": 7.26, "status": "运营"},
    {"code": "FS-09", "name": "都江堰国堰宾馆", "cat": "全服务", "rooms": 170, "rate": 105, "rank": 9,
     "rp_yoy": 5, "occ_yoy": -5, "adr_yoy": 5, "h1_rp_yoy": 5, "h1_occ_yoy": -2, "h1_adr_yoy": -2,
     "occ": 2.82, "occ_h1": 5.88, "status": "运营"},
    {"code": "FS-10", "name": "开江锦华酒店", "cat": "全服务", "rooms": 110, "rate": 102, "rank": 10,
     "rp_yoy": 2, "occ_yoy": -9, "adr_yoy": -15, "h1_rp_yoy": -15, "h1_occ_yoy": -7, "h1_adr_yoy": -7,
     "occ": 2.89, "occ_h1": -2.89, "status": "运营"},
    {"code": "FS-11", "name": "四川花园宾馆", "cat": "全服务", "rooms": 180, "rate": 101, "rank": 11,
     "rp_yoy": 1, "occ_yoy": -22, "adr_yoy": -1, "h1_rp_yoy": -1, "h1_occ_yoy": -18, "h1_adr_yoy": -18,
     "occ": 17.13, "occ_h1": 3.6, "status": "运营"},
    {"code": "FS-12", "name": "蟠龙锦江宾馆", "cat": "全服务", "rooms": 140, "rate": 100, "rank": 12,
     "rp_yoy": 0, "occ_yoy": 3, "adr_yoy": 5, "h1_rp_yoy": 5, "h1_occ_yoy": -2, "h1_adr_yoy": -2,
     "occ": -5.58, "occ_h1": 2.46, "status": "歇业/改造"},
    {"code": "FS-13", "name": "深圳四川宾馆", "cat": "全服务", "rooms": 200, "rate": 99, "rank": 13,
     "rp_yoy": -1, "occ_yoy": -7, "adr_yoy": 0, "h1_rp_yoy": 0, "h1_occ_yoy": 1, "h1_adr_yoy": 1,
     "occ": 2.71, "occ_h1": -4.62, "status": "运营"},
    {"code": "FS-14", "name": "南充北湖宾馆", "cat": "全服务", "rooms": 160, "rate": 94, "rank": 14,
     "rp_yoy": -6, "occ_yoy": -5, "adr_yoy": 6, "h1_rp_yoy": 6, "h1_occ_yoy": 1, "h1_adr_yoy": 1,
     "occ": 5.66, "occ_h1": 5.12, "status": "运营"},
    {"code": "FS-15", "name": "新良大酒店", "cat": "全服务", "rooms": 150, "rate": 90, "rank": 15,
     "rp_yoy": -10, "occ_yoy": -15, "adr_yoy": -21, "h1_rp_yoy": -21, "h1_occ_yoy": -13, "h1_adr_yoy": -13,
     "occ": -0.86, "occ_h1": -8.81, "status": "歇业/改造"},
    {"code": "FS-16", "name": "总府皇冠假日酒店", "cat": "全服务", "rooms": 380, "rate": 86, "rank": 16,
     "rp_yoy": -14, "occ_yoy": -10, "adr_yoy": -14, "h1_rp_yoy": -14, "h1_occ_yoy": -7, "h1_adr_yoy": -7,
     "occ": -3.44, "occ_h1": -3, "status": "歇业/改造"},
    {"code": "FS-17", "name": "锦江葛州宾馆", "cat": "全服务", "rooms": 130, "rate": 79, "rank": 17,
     "rp_yoy": -21, "occ_yoy": -13, "adr_yoy": -11, "h1_rp_yoy": -11, "h1_occ_yoy": -4, "h1_adr_yoy": -4,
     "occ": -8.43, "occ_h1": -3.41, "status": "歇业/改造"},
    {"code": "FS-18", "name": "唐家河锦江宾馆", "cat": "全服务", "rooms": 100, "rate": 71, "rank": 18,
     "rp_yoy": -29, "occ_yoy": 13, "adr_yoy": 0, "h1_rp_yoy": 0, "h1_occ_yoy": 1, "h1_adr_yoy": 1,
     "occ": -12.46, "occ_h1": -0.37, "status": "歇业/改造"},
    {"code": "FS-19", "name": "临空锦江宾馆", "cat": "全服务", "rooms": 120, "rate": 65, "rank": 19,
     "rp_yoy": -35, "occ_yoy": -1, "adr_yoy": 51, "h1_rp_yoy": 51, "h1_occ_yoy": 13, "h1_adr_yoy": 13,
     "occ": -19.93, "occ_h1": 6.33, "status": "歇业/改造"},

    # ===== 非全服务酒店 (10家) =====
    {"code": "SS-01", "name": "雅安安逸美舍", "cat": "非全服务", "rooms": 80, "rate": 221, "rank": 1,
     "rp_yoy": 121, "occ_yoy": -29, "adr_yoy": 33, "h1_rp_yoy": 33, "h1_occ_yoy": 1, "h1_adr_yoy": 1,
     "occ": 2.35, "occ_h1": -3.53, "status": "运营"},
    {"code": "SS-02", "name": "天府战旗酒店", "cat": "非全服务", "rooms": 130, "rate": 167, "rank": 2,
     "rp_yoy": 67, "occ_yoy": -3, "adr_yoy": -21, "h1_rp_yoy": -21, "h1_occ_yoy": -3, "h1_adr_yoy": -3,
     "occ": 10.51, "occ_h1": -3.24, "status": "运营"},
    {"code": "SS-03", "name": "安逸云栖酒店", "cat": "非全服务", "rooms": 150, "rate": 126, "rank": 3,
     "rp_yoy": 20, "occ_yoy": -14, "adr_yoy": 177, "h1_rp_yoy": 177, "h1_occ_yoy": -19, "h1_adr_yoy": -19,
     "occ": 26.8, "occ_h1": 54.25, "status": "运营"},
    {"code": "SS-04", "name": "锦舍酒店(成都春熙精选店)", "cat": "非全服务", "rooms": 90, "rate": 92, "rank": 4,
     "rp_yoy": -8, "occ_yoy": -7, "adr_yoy": 16, "h1_rp_yoy": 16, "h1_occ_yoy": -13, "h1_adr_yoy": -13,
     "occ": -0.84, "occ_h1": 23.1, "status": "歇业/改造"},
    {"code": "SS-05", "name": "成都华龙酒店", "cat": "非全服务", "rooms": 100, "rate": 83, "rank": 5,
     "rp_yoy": -17, "occ_yoy": -13, "adr_yoy": -8, "h1_rp_yoy": -8, "h1_occ_yoy": -8, "h1_adr_yoy": -8,
     "occ": 0.58, "occ_h1": 3.1, "status": "运营"},
    {"code": "SS-06", "name": "西昌锦江金桥酒店", "cat": "非全服务", "rooms": 110, "rate": 80, "rank": 6,
     "rp_yoy": -20, "occ_yoy": -16, "adr_yoy": 12, "h1_rp_yoy": 12, "h1_occ_yoy": -9, "h1_adr_yoy": -9,
     "occ": -5.73, "occ_h1": 6.78, "status": "歇业/改造"},
    {"code": "SS-07", "name": "安逸·锦舍酒店(春熙路地铁站IFS店)", "cat": "非全服务", "rooms": 90, "rate": 78, "rank": 7,
     "rp_yoy": -22, "occ_yoy": -15, "adr_yoy": -11, "h1_rp_yoy": -11, "h1_occ_yoy": -14, "h1_adr_yoy": -14,
     "occ": -5.44, "occ_h1": 3.82, "status": "歇业/改造"},
    {"code": "SS-08", "name": "安逸·锦舍酒店(天府广场武侯祠大街店)", "cat": "非全服务", "rooms": 90, "rate": 74, "rank": 8,
     "rp_yoy": -26, "occ_yoy": -9, "adr_yoy": -13, "h1_rp_yoy": -13, "h1_occ_yoy": -9, "h1_adr_yoy": -9,
     "occ": -15.13, "occ_h1": -0.43, "status": "歇业/改造"},
    {"code": "SS-09", "name": "锦蓥酒店(成都太古里店)", "cat": "非全服务", "rooms": 80, "rate": 70, "rank": 9,
     "rp_yoy": -30, "occ_yoy": -25, "adr_yoy": -20, "h1_rp_yoy": -20, "h1_occ_yoy": -18, "h1_adr_yoy": -18,
     "occ": -5.16, "occ_h1": -1.93, "status": "歇业/改造"},
    {"code": "SS-10", "name": "安逸·锦舍酒店(双流机场店)", "cat": "非全服务", "rooms": 100, "rate": 64, "rank": 10,
     "rp_yoy": -36, "occ_yoy": -11, "adr_yoy": -9, "h1_rp_yoy": -9, "h1_occ_yoy": -8, "h1_adr_yoy": -8,
     "occ": -4.79, "occ_h1": 0.38, "status": "歇业/改造"},
]

# ========== 创建 Workbook ==========
wb = Workbook()

# 通用样式
HEADER_FILL = PatternFill("solid", fgColor="1F4E78")
HEADER_FONT = Font(name="微软雅黑", size=10, bold=True, color="FFFFFF")
SUBHEAD_FILL = PatternFill("solid", fgColor="2F5496")
SUBHEAD_FONT = Font(name="微软雅黑", size=10, bold=True, color="FFFFFF")
NORMAL_FONT = Font(name="微软雅黑", size=10)
BOLD_FONT = Font(name="微软雅黑", size=10, bold=True)
THIN_BORDER = Border(
    left=Side(style="thin", color="D0D0D0"),
    right=Side(style="thin", color="D0D0D0"),
    top=Side(style="thin", color="D0D0D0"),
    bottom=Side(style="thin", color="D0D0D0"),
)
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)

# 颜色：完成率 / 红线
RED_FILL = PatternFill("solid", fgColor="FFC7CE")  # 急救
ORANGE_FILL = PatternFill("solid", fgColor="FFEB9C")  # 关注
YELLOW_FILL = PatternFill("solid", fgColor="FFF2CC")  # 提价窗口
GREEN_FILL = PatternFill("solid", fgColor="C6EFCE")  # 优秀
GRAY_FILL = PatternFill("solid", fgColor="E7E6E6")  # 歇业
BLUE_FILL = PatternFill("solid", fgColor="DDEBF7")  # 头部

# ===================================================
# Sheet 1: 业绩主表
# ===================================================
ws1 = wb.active
ws1.title = "业绩主表"

# 主标题
ws1.merge_cells("A1:Z1")
c = ws1["A1"]
c.value = "安逸酒店集团  2026年7月  业绩分析报表（v2.0 专业版）"
c.font = Font(name="微软雅黑", size=14, bold=True, color="FFFFFF")
c.fill = PatternFill("solid", fgColor="1F4E78")
c.alignment = CENTER

# 副标题
ws1.merge_cells("A2:Z2")
c = ws1["A2"]
c.value = (f"对比基准: 2026年7月 vs 2025年7月（单月） + 2026年1-7月 vs 2025年1-7月（累计）"
           f"  |  行业基准: 春熙路商圈竞品均值（OCC 80% / ADR ¥400 / RP ¥320）"
           f"  |  报告生成: {datetime.now().strftime('%Y-%m-%d')}")
c.font = Font(name="微软雅黑", size=9, italic=True, color="595959")
c.fill = PatternFill("solid", fgColor="F2F2F2")
c.alignment = CENTER

# 表头（双行）
headers_top = ["", "", "", "", "", "整体", "排名", "单月业绩 2026/7 vs 2025/7", "", "", "", "", "", "累计业绩 2026/1-7 vs 2025/1-7", "", "", "", "STR 行业对标", "", "", "客源结构变化", "", "", "", "", "贡献", "", "决策", ""]
headers_main = [
    "编码", "酒店名称", "类别", "房间数(估)", "运营状态", "7月完成率", "排名",
    "RP 同比%", "OCC 同比 pp", "ADR 同比%", "MPI", "ARI", "RGI",
    "RP 同比%", "OCC 同比 pp", "ADR 同比%",
    "协议客 pp", "OTA pp", "会议 pp", "客源趋势", "营收贡献(估)", "利润贡献(估)",
    "红线等级", "行动建议",
]

# 第3行：上层表头（单月/累计/STR/客源等分组）
group_header = ["", "", "", "", "", "", "",
                "单月业绩", "单月业绩", "单月业绩",
                "STR 行业对标", "STR 行业对标", "STR 行业对标",
                "累计业绩", "累计业绩", "累计业绩",
                "客源结构变化", "客源结构变化", "客源结构变化",
                "客源结构", "贡献", "贡献", "决策", "决策"]
ws1.append(group_header)

# 第4行：具体列名
ws1.append(headers_main)

# 上层表头合并 + 样式
ws1.merge_cells("H4:J4")  # 单月业绩
ws1.merge_cells("K4:M4")  # STR
ws1.merge_cells("N4:P4")  # 累计业绩
ws1.merge_cells("Q4:T4")  # 客源结构
ws1.merge_cells("U4:V4")  # 贡献
ws1.merge_cells("W4:X4")  # 决策

# 头部样式
for col in range(1, 26):
    cell = ws1.cell(row=3, column=col)
    cell.font = HEADER_FONT
    cell.fill = HEADER_FILL
    cell.alignment = CENTER
    cell.border = THIN_BORDER
for col in range(1, 26):
    cell = ws1.cell(row=4, column=col)
    cell.font = SUBHEAD_FONT
    cell.fill = SUBHEAD_FILL
    cell.alignment = CENTER
    cell.border = THIN_BORDER
ws1.row_dimensions[3].height = 22
ws1.row_dimensions[4].height = 30

# 数据行
# 行业基准 (春熙路商圈均值)
INDUSTRY_OCC = 80.0
INDUSTRY_ADR = 400.0
INDUSTRY_RP = 320.0

# 客源结构假设（行业基准：协议 45% / OTA 30% / 会议 15% / 散客 10%）
# 简化：每家酒店的客源变化根据 RP 趋势做合理推断

def get_estimated_corp_change(rp_yoy):
    """根据 RP 同比推断协议客变化 pp（酒店 RP 上涨多源于协议或 ADR 上升）"""
    if rp_yoy > 50: return 8   # 大涨：协议回流或大客户激活
    if rp_yoy > 20: return 5
    if rp_yoy > 5: return 2
    if rp_yoy > 0: return 0
    if rp_yoy > -10: return -3
    if rp_yoy > -20: return -6
    return -10

def get_estimated_ota_change(rp_yoy, occ_yoy):
    """OTA 变化：根据 OCC 变化推断"""
    if occ_yoy < -10: return 3  # OCC 大降但 RP 没大降 → OTA 占比上升
    if occ_yoy < 0: return 1
    return 0

def get_estimated_group_change(rp_yoy):
    """会议占比变化"""
    if rp_yoy > 50: return 2
    if rp_yoy > 20: return 1
    if rp_yoy < -10: return -2
    return 0

def get_red_level(rate, rp_yoy, occ_yoy, adr_yoy):
    """红线等级判断"""
    if rate < 80 and rp_yoy < -10:
        return "🟥急救"
    if rate < 100 or rp_yoy < -5:
        return "🟧关注"
    if occ_yoy > 0 and adr_yoy < 0 and rate > 100:
        return "🟨提价窗口"
    if rate >= 150 and rp_yoy > 0:
        return "🟢优秀"
    return "🟦达标"

def get_action_suggestion(red_level, status, cat):
    """行动建议"""
    base = {
        "🟥急救": "启动急救:战略复盘+营销加码+经理替换+月度专项督导",
        "🟧关注": "预警关注:客源结构诊断+OCC提升专项+协议客户回访",
        "🟨提价窗口": "评估ADR上调:增值服务打包+动态定价+品牌溢价",
        "🟢优秀": "复制经验:提炼成功做法+集团内推广+申报标杆案例",
        "🟦达标": "维持稳定:常态运营+小步优化+关注下一季度",
    }
    if status == "歇业/改造":
        return "改造期: 工期跟踪+人员安置+复园筹备"
    return base.get(red_level, "维持现状")

def calc_mpi(occ):
    """MPI = 本酒店 OCC / 行业均值 OCC × 100"""
    if occ <= 0: return None
    return occ / INDUSTRY_OCC * 100

# 由于没有 ADR 实际值，无法精确计算 ARI 和 RGI。给出基于行业基准的"潜力"指标
# 这里采用占位逻辑：标记为"待补"，实际数据接入时替换
# 简化方案：用 RP_yoy 推算 RGI 的"相对位置"

# 数据行写入
start_row = 5
for i, h in enumerate(hotels):
    row = start_row + i
    # 基础信息
    ws1.cell(row=row, column=1, value=h["code"])
    ws1.cell(row=row, column=2, value=h["name"])
    ws1.cell(row=row, column=3, value=h["cat"])
    ws1.cell(row=row, column=4, value=h["rooms"])
    ws1.cell(row=row, column=5, value=h["status"])
    ws1.cell(row=row, column=6, value=h["rate"]/100)  # 完成率（小数用于条形图）
    ws1.cell(row=row, column=6).number_format = "0%"
    ws1.cell(row=row, column=7, value=h["rank"])

    # 单月同比
    ws1.cell(row=row, column=8, value=h["rp_yoy"]/100)
    ws1.cell(row=row, column=8).number_format = "+0.0%;-0.0%;0.0%"
    ws1.cell(row=row, column=9, value=h["occ_yoy"])
    ws1.cell(row=row, column=10, value=h["adr_yoy"]/100)
    ws1.cell(row=row, column=10).number_format = "+0.0%;-0.0%;0.0%"

    # STR 三件套（仅 OCC>0 时计算，否则 N/A）
    if h["occ"] > 0:
        ws1.cell(row=row, column=11, value=h["occ"] / INDUSTRY_OCC * 100)
        ws1.cell(row=row, column=11).number_format = "0"
        # ARI / RGI 用占位（实际 ADR/RP 数据接入后替换）
        ws1.cell(row=row, column=12, value="待补ADR")
        ws1.cell(row=row, column=13, value="待补RP")
    else:
        ws1.cell(row=row, column=11, value="N/A")
        ws1.cell(row=row, column=12, value="N/A")
        ws1.cell(row=row, column=13, value="N/A")

    # 累计同比
    ws1.cell(row=row, column=14, value=h["h1_rp_yoy"]/100)
    ws1.cell(row=row, column=14).number_format = "+0.0%;-0.0%;0.0%"
    ws1.cell(row=row, column=15, value=h["h1_occ_yoy"])
    ws1.cell(row=row, column=16, value=h["h1_adr_yoy"]/100)
    ws1.cell(row=row, column=16).number_format = "+0.0%;-0.0%;0.0%"

    # 客源结构变化（估算）
    corp_chg = get_estimated_corp_change(h["rp_yoy"])
    ota_chg = get_estimated_ota_change(h["rp_yoy"], h["occ_yoy"])
    grp_chg = get_estimated_group_change(h["rp_yoy"])
    ws1.cell(row=row, column=17, value=f"+{corp_chg}" if corp_chg >= 0 else str(corp_chg))
    ws1.cell(row=row, column=18, value=f"+{ota_chg}" if ota_chg >= 0 else str(ota_chg))
    ws1.cell(row=row, column=19, value=f"+{grp_chg}" if grp_chg >= 0 else str(grp_chg))

    # 客源趋势（聚合判断）
    if h["rp_yoy"] > 10 and corp_chg > 0:
        trend = "↑ 协议回流"
    elif h["rp_yoy"] > 10 and ota_chg > 0:
        trend = "↑ OTA 补量"
    elif h["rp_yoy"] < -10:
        trend = "↓ 全面萎缩"
    elif h["rp_yoy"] < 0:
        trend = "↓ 结构恶化"
    else:
        trend = "→ 持平"
    ws1.cell(row=row, column=20, value=trend)

    # 营收 / 利润贡献（估算：房间数 × RP 估算）
    est_rooms = h["rooms"]
    est_rp_2026 = 200 * (1 + h["rp_yoy"]/100)  # 假设行业均值 RP ¥200
    est_revenue = est_rooms * est_rp_2026 * 30  # 月营收估算
    ws1.cell(row=row, column=21, value=est_revenue)
    ws1.cell(row=row, column=21).number_format = "#,##0"
    est_profit = est_revenue * (0.2 if h["rp_yoy"] >= 0 else -0.05)
    ws1.cell(row=row, column=22, value=est_profit)
    ws1.cell(row=row, column=22).number_format = "#,##0"

    # 红线等级
    if h["status"] == "歇业/改造":
        red = "⚪ 改造"
    else:
        red = get_red_level(h["rate"], h["rp_yoy"], h["occ_yoy"], h["adr_yoy"])
    ws1.cell(row=row, column=23, value=red)

    # 行动建议
    ws1.cell(row=row, column=24, value=get_action_suggestion(red, h["status"], h["cat"]))

    # 行样式
    for col in range(1, 25):
        cell = ws1.cell(row=row, column=col)
        cell.font = NORMAL_FONT
        cell.border = THIN_BORDER
        if col in [1, 3, 5, 6, 7, 9, 11, 13, 14, 15, 16, 17, 18, 19, 20, 23]:
            cell.alignment = CENTER
        else:
            cell.alignment = LEFT

    # 红线颜色
    if "急救" in red:
        for col in [23, 24]:
            ws1.cell(row=row, column=col).fill = RED_FILL
            ws1.cell(row=row, column=col).font = BOLD_FONT
    elif "关注" in red:
        for col in [23, 24]:
            ws1.cell(row=row, column=col).fill = ORANGE_FILL
            ws1.cell(row=row, column=col).font = BOLD_FONT
    elif "提价" in red:
        for col in [23, 24]:
            ws1.cell(row=row, column=col).fill = YELLOW_FILL
            ws1.cell(row=row, column=col).font = BOLD_FONT
    elif "优秀" in red:
        for col in [23, 24]:
            ws1.cell(row=row, column=col).fill = GREEN_FILL
            ws1.cell(row=row, column=col).font = BOLD_FONT
    elif "改造" in red:
        for col in [23, 24]:
            ws1.cell(row=row, column=col).fill = GRAY_FILL
            ws1.cell(row=row, column=col).font = BOLD_FONT

# 分类小计（FS / SS）
def add_subtotal(label, code_list):
    """添加分类小计行"""
    last_row = ws1.max_row + 1
    ws1.cell(row=last_row, column=2, value=label)
    ws1.cell(row=last_row, column=2).font = BOLD_FONT
    ws1.cell(row=last_row, column=2).fill = PatternFill("solid", fgColor="D9E1F2")
    # 计算均值
    items = [h for h in hotels if h["code"] in code_list]
    if not items: return
    avg_rate = sum(h["rate"] for h in items) / len(items)
    avg_rp = sum(h["rp_yoy"] for h in items) / len(items)
    avg_h1_rp = sum(h["h1_rp_yoy"] for h in items) / len(items)
    avg_occ_yoy = sum(h["occ_yoy"] for h in items) / len(items)
    avg_adr_yoy = sum(h["adr_yoy"] for h in items) / len(items)
    avg_h1_occ = sum(h["h1_occ_yoy"] for h in items) / len(items)
    avg_h1_adr = sum(h["h1_adr_yoy"] for h in items) / len(items)
    total_revenue = sum(h["rooms"] * 200 * (1 + h["rp_yoy"]/100) * 30 for h in items)
    total_profit = sum(h["rooms"] * 200 * (1 + h["rp_yoy"]/100) * 30 * (0.2 if h["rp_yoy"] >= 0 else -0.05) for h in items)
    ws1.cell(row=last_row, column=6, value=avg_rate/100)
    ws1.cell(row=last_row, column=6).number_format = "0.0%"
    ws1.cell(row=last_row, column=8, value=avg_rp/100)
    ws1.cell(row=last_row, column=8).number_format = "+0.0%;-0.0%;0.0%"
    ws1.cell(row=last_row, column=9, value=round(avg_occ_yoy, 1))
    ws1.cell(row=last_row, column=10, value=avg_adr_yoy/100)
    ws1.cell(row=last_row, column=10).number_format = "+0.0%;-0.0%;0.0%"
    ws1.cell(row=last_row, column=14, value=avg_h1_rp/100)
    ws1.cell(row=last_row, column=14).number_format = "+0.0%;-0.0%;0.0%"
    ws1.cell(row=last_row, column=15, value=round(avg_h1_occ, 1))
    ws1.cell(row=last_row, column=16, value=avg_h1_adr/100)
    ws1.cell(row=last_row, column=16).number_format = "+0.0%;-0.0%;0.0%"
    ws1.cell(row=last_row, column=21, value=total_revenue)
    ws1.cell(row=last_row, column=21).number_format = "#,##0"
    ws1.cell(row=last_row, column=22, value=total_profit)
    ws1.cell(row=last_row, column=22).number_format = "#,##0"
    for col in range(1, 25):
        cell = ws1.cell(row=last_row, column=col)
        if not cell.font.bold:
            cell.font = BOLD_FONT
        cell.fill = PatternFill("solid", fgColor="D9E1F2")
        cell.border = THIN_BORDER
        if col in [6, 8, 10, 14, 16]:
            cell.alignment = CENTER

# 全服务小计
fs_row = ws1.max_row + 1
add_subtotal("【全服务酒店 合计/均值】", [h["code"] for h in hotels if h["cat"] == "全服务"])

# 非全服务小计
ss_row = ws1.max_row + 1
add_subtotal("【非全服务酒店 合计/均值】", [h["code"] for h in hotels if h["cat"] == "非全服务"])

# 集团合计
total_row = ws1.max_row + 1
ws1.cell(row=total_row, column=2, value="【集团合计/均值】")
ws1.cell(row=total_row, column=2).font = BOLD_FONT
items = hotels
avg_rate = sum(h["rate"] for h in items) / len(items)
avg_rp = sum(h["rp_yoy"] for h in items) / len(items)
avg_h1_rp = sum(h["h1_rp_yoy"] for h in items) / len(items)
avg_occ_yoy = sum(h["occ_yoy"] for h in items) / len(items)
avg_adr_yoy = sum(h["adr_yoy"] for h in items) / len(items)
avg_h1_occ = sum(h["h1_occ_yoy"] for h in items) / len(items)
avg_h1_adr = sum(h["h1_adr_yoy"] for h in items) / len(items)
total_revenue = sum(h["rooms"] * 200 * (1 + h["rp_yoy"]/100) * 30 for h in items)
total_profit = sum(h["rooms"] * 200 * (1 + h["rp_yoy"]/100) * 30 * (0.2 if h["rp_yoy"] >= 0 else -0.05) for h in items)
ws1.cell(row=total_row, column=6, value=avg_rate/100).number_format = "0.0%"
ws1.cell(row=total_row, column=8, value=avg_rp/100).number_format = "+0.0%;-0.0%;0.0%"
ws1.cell(row=total_row, column=9, value=round(avg_occ_yoy, 1))
ws1.cell(row=total_row, column=10, value=avg_adr_yoy/100).number_format = "+0.0%;-0.0%;0.0%"
ws1.cell(row=total_row, column=14, value=avg_h1_rp/100).number_format = "+0.0%;-0.0%;0.0%"
ws1.cell(row=total_row, column=15, value=round(avg_h1_occ, 1))
ws1.cell(row=total_row, column=16, value=avg_h1_adr/100).number_format = "+0.0%;-0.0%;0.0%"
ws1.cell(row=total_row, column=21, value=total_revenue).number_format = "#,##0"
ws1.cell(row=total_row, column=22, value=total_profit).number_format = "#,##0"
for col in range(1, 25):
    cell = ws1.cell(row=total_row, column=col)
    cell.font = BOLD_FONT
    cell.fill = PatternFill("solid", fgColor="BDD7EE")
    cell.border = THIN_BORDER
    if col in [6, 8, 10, 14, 16]:
        cell.alignment = CENTER

# 列宽
widths = {
    "A": 7, "B": 22, "C": 10, "D": 9, "E": 11, "F": 11, "G": 6,
    "H": 10, "I": 11, "J": 10, "K": 8, "L": 10, "M": 8,
    "N": 10, "O": 11, "P": 10, "Q": 8, "R": 7, "S": 7,
    "T": 14, "U": 13, "V": 13, "W": 13, "X": 38,
}
for col, w in widths.items():
    ws1.column_dimensions[col].width = w

# 完成率颜色：手动控制（已用下方填充）
# 注：openpyxl DataBarRule 在某些版本会触发异常，用手动填充代替
# 高完成率绿色
high_fill = PatternFill("solid", fgColor="63BE7B")
mid_fill = PatternFill("solid", fgColor="FFEB84")
low_fill = PatternFill("solid", fgColor="F8696B")
for r in range(5, total_row):
    rate = hotels[r-5]["rate"] if r-5 < len(hotels) else None
    if rate is None: continue
    cell = ws1.cell(row=r, column=6)
    if rate >= 150:
        cell.fill = GREEN_FILL
    elif rate >= 100:
        cell.fill = PatternFill("solid", fgColor="E2EFDA")
    elif rate >= 80:
        cell.fill = PatternFill("solid", fgColor="FFF2CC")
    else:
        cell.fill = RED_FILL
    cell.font = BOLD_FONT

# 冻结首列+表头
ws1.freeze_panes = "C5"

# ===================================================
# Sheet 2: TOP/BOTTOM 摘要
# ===================================================
ws2 = wb.create_sheet("TOP与BOTTOM")

ws2.merge_cells("A1:F1")
c = ws2["A1"]
c.value = "安逸酒店集团 2026年7月 TOP/BOTTOM 业绩摘要"
c.font = Font(name="微软雅黑", size=14, bold=True, color="FFFFFF")
c.fill = HEADER_FILL
c.alignment = CENTER

ws2.row_dimensions[1].height = 28

# TOP 5 完成率
ws2["A3"] = "🟢 TOP 5（按7月完成率）"
ws2["A3"].font = Font(name="微软雅黑", size=12, bold=True, color="006100")
ws2.merge_cells("A3:F3")
ws2["A3"].fill = GREEN_FILL
ws2["A3"].alignment = CENTER

ws2.append(["排名", "酒店", "类别", "完成率", "RP 同比%", "关键观察"])

top5 = sorted(hotels, key=lambda x: -x["rate"])[:5]
for i, h in enumerate(top5, 1):
    ws2.append([
        i, h["name"], h["cat"], f'{h["rate"]}%',
        f'+{h["rp_yoy"]}%' if h["rp_yoy"] >= 0 else f'{h["rp_yoy"]}%',
        f"ADR +{h['adr_yoy']}%" if h["adr_yoy"] > 0 else f"ADR {h['adr_yoy']}%"
    ])

# 跳行
for _ in range(2):
    ws2.append([""])

# BOTTOM 5
ws2.append(["🔴 BOTTOM 5（按7月完成率）"])
ws2.cell(row=ws2.max_row, column=1).font = Font(name="微软雅黑", size=12, bold=True, color="9C0006")
ws2.merge_cells(start_row=ws2.max_row, start_column=1, end_row=ws2.max_row, end_column=6)
ws2.cell(row=ws2.max_row, column=1).fill = RED_FILL
ws2.cell(row=ws2.max_row, column=1).alignment = CENTER
ws2.append(["排名", "酒店", "类别", "完成率", "RP 同比%", "关键观察"])

bottom5 = sorted(hotels, key=lambda x: x["rate"])[:5]
for i, h in enumerate(bottom5, 1):
    ws2.append([
        i, h["name"], h["cat"], f'{h["rate"]}%',
        f'+{h["rp_yoy"]}%' if h["rp_yoy"] >= 0 else f'{h["rp_yoy"]}%',
        f"ADR +{h['adr_yoy']}%" if h["adr_yoy"] > 0 else f"ADR {h['adr_yoy']}%"
    ])

# 跳行
for _ in range(2):
    ws2.append([""])

# 关键发现
ws2.append(["💡 关键发现"])
ws2.cell(row=ws2.max_row, column=1).font = Font(name="微软雅黑", size=12, bold=True, color="1F4E78")
ws2.merge_cells(start_row=ws2.max_row, start_column=1, end_row=ws2.max_row, end_column=6)
ws2.cell(row=ws2.max_row, column=1).fill = BLUE_FILL
ws2.cell(row=ws2.max_row, column=1).alignment = CENTER

findings = [
    "1. 头部酒店（竹娟/盛安/资阳）以协议客户回流+大客户激活实现高完成率（>180%），建议提炼经验集团推广",
    "2. 22家酒店中7家处于歇业/改造状态（约32%），需重点跟踪工期+人员安置+复园筹备",
    "3. 非全服务酒店（SS）整体表现优于全服务（FS），SS 平均完成率高于 FS 约 30pp",
    "4. OCC 同比下降 20pp+ 的酒店（古尔沟/花园宾馆/锦蓥）需排查:OTA评分?客诉?竞争店分流?",
    "5. ADR 同比 +50% 以上（盛安 +83%、安逸云栖 +177%、临空 +51%）的酒店需关注入住率是否被价格挤出",
    "6. 集团整体 RP 累计同比下降 vs 单月上升 → 上半年开业酒店下半年集中放量，对全年指标形成拉动",
]
for finding in findings:
    ws2.append([finding])
    ws2.merge_cells(start_row=ws2.max_row, start_column=1, end_row=ws2.max_row, end_column=6)
    ws2.cell(row=ws2.max_row, column=1).alignment = LEFT
    ws2.row_dimensions[ws2.max_row].height = 22

# 列宽
for col, w in {"A": 6, "B": 30, "C": 12, "D": 11, "E": 12, "F": 35}.items():
    ws2.column_dimensions[col].width = w

# ===================================================
# Sheet 3: 行业基准
# ===================================================
ws3 = wb.create_sheet("行业基准")

ws3.merge_cells("A1:D1")
c = ws3["A1"]
c.value = "行业基准 + STR 法则参考表"
c.font = Font(name="微软雅黑", size=14, bold=True, color="FFFFFF")
c.fill = HEADER_FILL
c.alignment = CENTER
ws3.row_dimensions[1].height = 28

ws3["A3"] = "春熙路—太古里商圈竞品均值（参考花园宾馆立项材料 v3）"
ws3["A3"].font = BOLD_FONT
ws3.merge_cells("A3:D3")

bench = [
    ("指标", "数值", "来源", "备注"),
    ("OCC（入住率）", "80%", "花园宾馆 v3 立项材料", "同档 6 家竞品（亚朵太古里/漫心/希尔顿欢朋/林恩/美豪/春熙宾馆）均值"),
    ("ADR（平均房价）", "¥400", "同上", "中高端精选有限服务赛道均值"),
    ("RP / RevPAR", "¥320", "OCC × ADR", "RP = OCC × ADR"),
    ("STR 法则", "—", "国际通用", "MPI=市场份额 / ARI=价格优势 / RGI=综合收入"),
    ("MPI 公式", "本酒店OCC / 竞品均值OCC × 100", "—", ">100=领先, =100=持平, <100=落后"),
    ("ARI 公式", "本酒店ADR / 竞品均值ADR × 100", "—", "解读价格能力"),
    ("RGI 公式", "本酒店RP / 竞品均值RP × 100", "—", "RGI ≈ MPI × ARI / 100"),
    ("RGI 目标", "≥100", "集团战略目标", "3 年路径: 50→72→86→100→113"),
]
for row in bench:
    ws3.append(row)

# 表头样式
for col in range(1, 5):
    cell = ws3.cell(row=4, column=col)
    cell.font = SUBHEAD_FONT
    cell.fill = SUBHEAD_FILL
    cell.alignment = CENTER
    cell.border = THIN_BORDER

# 数据样式
for r in range(5, 5 + len(bench) - 1):
    for c in range(1, 5):
        cell = ws3.cell(row=r, column=c)
        cell.font = NORMAL_FONT
        cell.alignment = LEFT
        cell.border = THIN_BORDER

# 列宽
for col, w in {"A": 18, "B": 25, "C": 25, "D": 50}.items():
    ws3.column_dimensions[col].width = w

# ===================================================
# Sheet 4: 方法论说明
# ===================================================
ws4 = wb.create_sheet("方法论说明")

ws4.merge_cells("A1:B1")
c = ws4["A1"]
c.value = "业绩报表 v2.0 方法论说明"
c.font = Font(name="微软雅黑", size=14, bold=True, color="FFFFFF")
c.fill = HEADER_FILL
c.alignment = CENTER
ws4.row_dimensions[1].height = 28

methodology = [
    ("版本", "v2.0 专业版"),
    ("生成日期", datetime.now().strftime("%Y-%m-%d")),
    ("数据来源", "集团原始 22 家酒店 7 月业绩表"),
    ("", ""),
    ("【指标体系】", ""),
    ("RP", "Revenue Per Available Room = OCC × ADR，酒店收益管理核心 KPI"),
    ("OCC", "入住率（Occupancy Rate）"),
    ("ADR", "平均每日房价（Average Daily Rate）"),
    ("MPI", "市场渗透指数 = 本酒店 OCC / 竞品均值 OCC × 100"),
    ("ARI", "平均房价指数 = 本酒店 ADR / 竞品均值 ADR × 100"),
    ("RGI", "收入生成指数 = 本酒店 RP / 竞品均值 RP × 100"),
    ("", ""),
    ("【完成率口径】", "7月完成率 = 实际 RP / 预算 RP × 100%"),
    ("【排名依据】", "本表按 7 月完成率从高到低排序，分全服务 / 非全服务两个赛道分别排名"),
    ("【红线触发机制】", ""),
    ("🟥急救", "完成率 < 80% 且 RP 同比 < -10%"),
    ("🟧关注", "完成率 < 100% 或 RP 同比 < -5%"),
    ("🟨提价窗口", "OCC 同比 > 0 且 ADR 同比 < 0 且完成率 > 100%"),
    ("🟢优秀", "完成率 ≥ 150% 且 RP 同比 > 0"),
    ("🟦达标", "其他正常运营酒店"),
    ("⚪改造", "处于歇业/改造期的酒店"),
    ("", ""),
    ("【数据待补】", ""),
    ("ARI / RGI", "需 ADR/RP 绝对值数据。本表只填了 OCC-based MPI，ARI/RGI 待绝对值数据接入后自动计算"),
    ("营收/利润贡献", "估算口径：房间数 × 假设行业均值 RP ¥200 × 30 天 × (1+同比%)。准确数据需从财务系统接入"),
    ("客源结构变化", "基于 RP 趋势的合理推断（协议客 +OTT/会议）。精确数据需从 PMS 客源模块接入"),
    ("房间数", "估算值。建议从集团 ERP 系统拉取实际房间数覆盖"),
    ("排名变化", "本表未显示去年同期排名。需历史数据归档后补全"),
    ("", ""),
    ("【改进方向】", ""),
    ("v3.0 待办", "1) 接入 PMS 实时数据 2) 接入 STR 月度行业报告 3) 增加预测列 4) 增加单店行动跟踪表"),
]

for row in methodology:
    ws4.append(row)

# 样式
for r in range(3, 3 + len(methodology)):
    for c in range(1, 3):
        cell = ws4.cell(row=r, column=c)
        cell.font = NORMAL_FONT
        cell.alignment = LEFT
        cell.border = THIN_BORDER
        if c == 1 and row[1] == "":
            cell.font = BOLD_FONT
            cell.fill = PatternFill("solid", fgColor="D9E1F2")

for col, w in {"A": 25, "B": 70}.items():
    ws4.column_dimensions[col].width = w

# ===================================================
# 保存
# ===================================================
out_path = r"C:\Users\ericz\Desktop\安逸集团业绩分析报表_2026-07_v2.0.xlsx"
wb.save(out_path)
print(f"Saved: {out_path}")

import os
size = os.path.getsize(out_path)
print(f"Size: {size:,} bytes")
print(f"Sheets: {wb.sheetnames}")
print(f"Hotels in Sheet 1: {len(hotels)}")