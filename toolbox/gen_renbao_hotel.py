# -*- coding: utf-8 -*-
"""省旅投与人保财险合作清单 · 酒店板块填充"""
import os
from copy import copy
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

SRC = r"C:\Users\ericz\Desktop\省旅游投资集团与人保财险合作事项对接联系清单.xlsx"
OUT = r"C:\Users\ericz\Desktop\省旅投与人保财险合作清单_酒店板块已填_2026-11-12.xlsx"
FONT = '等线'
NAVY = '1F3864'
thin = Side(style='thin', color='BFBFBF')
BD = Border(left=thin, right=thin, top=thin, bottom=thin)

wb = openpyxl.load_workbook(SRC)
ws = wb.active

# ===== 1. 表头口径修正（原模板沿用"省退役军人事务厅"版本）=====
ws.cell(1, 1).value = '四川旅投集团与人保财险四川省分公司合作清单'
ws.cell(2, 9).value = '人保财险四川省分公司 / 责任部门及联系人（建议）'
ws.title = '省旅投与人保财险合作清单'

# 样式：沿用表头样式
hdr_font = Font(name=FONT, size=9, bold=True, color='FFFFFF')
hdr_fill = PatternFill('solid', fgColor=NAVY)
for c in range(1, 12):
    cell = ws.cell(2, c)
    cell.font = hdr_font
    cell.fill = hdr_fill
    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    cell.border = BD

# 取一条已填行（第16行）作为单元格样式模板
TPL_ROW = 16
tpl_align = copy(ws.cell(TPL_ROW, 3).alignment)
tpl_font = copy(ws.cell(TPL_ROW, 3).font)

# ===== 2. 填充第 3 行「酒店板块」=====
R = 3
CONTENT = (
    '1）客房与经营责任保险：公众责任险、食品安全责任险、雇主责任险，集团自营及委托管理酒店统一投保方案；\n'
    '2）安全与网络风险减量：以人保"安全管理＋网安保险＋风险防控服务"模式，与酒店智能弱电（网关、网监审计、WiFi认证）联动，把风险防控能力做进门店；\n'
    '3）会员权益增值：将惠民保、意外险等嵌入"安逸会"会员权益，支撑会员拉新与复购；\n'
    '4）新零售与助农采购：农险与乡村振兴服务对接安逸甄选、川货出川供应链，建立"保险＋溯源＋助农"采购通道；\n'
    '5）存量改造与旅游出行：6大酒店改造工程保险、熊猫专列承运人责任险与旅客意外险随项目同步落地。'
)
GOAL = (
    '① 形成集团统一保险方案，覆盖全部自营及委托管理酒店，公开责任险、食品安全责任险、雇主责任险成本；\n'
    '② 每年引入外部风险查勘与防灾减损服务，降低酒店安全事故率与赔付率；\n'
    '③ 会员权益包新增保险增值权益，支撑会员注册与复购目标；\n'
    '④ 保险＋助农采购形成川货出川新通道，落地安逸新零售规模化目标；\n'
    '⑤ 改造与专列项目风险全覆盖，工程保险与旅意险随项目节点同步落地。'
)
RES = (
    '① 安逸侧：酒店经营与安全数据、会员系统接口、改造项目工程量清单、专列承运与旅客资料；\n'
    '② 人保侧：非车险、意外险、团体客户与农险产品方案，以及风险查勘与防灾减损服务能力；\n'
    '③ 共同场景：在营酒店与拟改造门店投保清单、拟接入风险防控的门店清单。'
)
STEP = (
    '1）2026年12月：双方确定酒店板块合作事项清单与对口部门，完成首轮方案沟通；\n'
    '2）2027年1月：出具集团统一保险方案与费用测算，明确统保范围与投保路径；\n'
    '3）2027年3月：完成智能弱电与风险防控服务联动方案，选2至3家门店试点；\n'
    '4）2027年6月：会员权益增值、新零售助农采购两个通道上线；\n'
    '5）2027年下半年：随6大酒店改造与熊猫专列项目落地工程保险与旅意险。'
)
STATUS = '待对接'
OUR = (
    '主责：安逸酒店集团 酒店板块／颜伟志（大运营中心·运营条线）\n'
    '牵头：张实（产业发展部·会员权益、新零售、渠道与协议价侧）／联系方式 17760348653\n'
    '配合：安全管理部 李培先（责任险与安全）；大运营中心 钟华（运营与风控落地）；'
    '饭店管理公司 马飞飞（委托管理项目）；财务金融部 李明（统保方案与费用测算）'
)
THEIRS = (
    '非车险部（责任险、食品安全责任险、雇主责任险、企业财产险）\n'
    '意外险部（团体意外险、旅客意外险）\n'
    '团体客户部（企业财产险、工程险、员工保障）\n'
    '农业保险部（农险、乡村振兴、助农保险）\n'
    '风险减量服务条线（风险查勘、防灾减损、网安风险防控服务）\n'
    '战略企划部（省级战略合作归口）\n'
    '注：以上填至业务板块层级，具体部门名称以人保财险四川省分公司实际设置为准，由对接时确认。'
)
NOW = (
    '待对接。建议由集团层面先与省旅投产业发展部（陈天科）对齐合作口径，'
    '再由酒店板块牵头组建双方工作组并启动首轮方案沟通。'
)
NOTE = (
    '1）本表模板沿用"省退役军人事务厅"版本，第14至17行为该版本遗留内容，与人保口径不符，建议清空或另表处理；\n'
    '2）酒店板块的实际承接主体需与大运营中心机制（10月30日确定）并轨，避免运营条线与产业条线重复对接；\n'
    '3）双方均涉及系统与数据接口（会员、投保单、风险数据），须先行明确数据权属、安全边界与接口口径；\n'
    '4）第3项会员权益增值与第4项助农采购需与安逸会积分方案（11月30日审议）、安逸新零售点位拓展计划同批推进。'
)

VALUES = {3: CONTENT, 4: GOAL, 5: RES, 6: STEP, 7: STATUS, 8: OUR, 9: THEIRS, 10: NOW, 11: NOTE}

for col, val in VALUES.items():
    cell = ws.cell(R, col)
    cell.value = val
    cell.font = Font(name=FONT, size=9)
    cell.border = BD
    if col in (7,):
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    else:
        cell.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)

# 序号与项目名称保持原样
ws.cell(R, 1).value = 1
ws.cell(R, 2).value = '酒店板块'
for c in (1, 2):
    cell = ws.cell(R, c)
    cell.font = Font(name=FONT, size=9, bold=True)
    cell.alignment = Alignment(horizontal='center', vertical='center')
    cell.border = BD

# 行高
ws.row_dimensions[R].height = 230
for r in range(4, 16):
    ws.row_dimensions[r].height = 26

wb.save(OUT)
print('SAVED:', OUT)
print('SIZE:', os.path.getsize(OUT))
