# -*- coding: utf-8 -*-
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

WS = 'D:\\B166ER-openclaw\\workspace'
OUT_DIR = 'C:\\Users\\ericz\\Desktop\\产业发展部\\重要文件'
XLSX = os.path.join(OUT_DIR, '一店一策_产业发展部归口填报_v1.0_20261118.xlsx')
MD = os.path.join(WS, 'anyi-ops-kb', '07_战略与改革', '2026-11-18_一店一策_产业发展部归口填报_v1.0.md')

# 序号 -> (S码, 牵头主体, 关键节点)
M = {
 1: ('S01 集团与本部定位', '牵头：本部董事会，产业发展部主笔集团与本部口径',
     '节点：2026 年底前统一家数与房数口径；2027 年 6 月前完成 6 大改造重新排队；数字化中台二期 2026 年底前过会'),
 2: ('S01 集团与本部定位', '牵头：本部董事会，产业发展部主笔轻重分离方案',
     '节点：2026 年底前完成轻重分离平台拆分方案；11 处房数冲突 2026-11-30 前核定；壳公司处置与商标对价补正同步推进'),
 3: ('S02 破产重整与及时止损 ＋ S05 优先出租还债', '牵头：战投与法务、财务金融部主责资本结构重组；产业发展部主责轻资产端品牌化',
     '节点：2026 年底前完成品牌手册与运营标准输出；2027 年上半年完成资源型度假品牌注册与首批对外输出；债务置换 2026 年底前签署'),
 4: ('S07 及时改造，打造自营标杆', '牵头：产业发展部＋运管中心；资产与工程由投资和资产部主责',
     '节点：品牌 2027 年授权到期前 6 个月锁定；改造按 200 间/批、3 批×6 月推进，2028 年底前完成'),
 5: ('S07 及时改造，打造自营标杆', '牵头：产业发展部＋运管中心；产权与工程由投资和资产部主责',
     '节点：2026 年底前完成产权申办与 40 余名小业主协调；2027 年上半年完成双品牌区段划分、改造立项与消防合规方案；2028 年底前完成改造'),
 6: ('S08 分年度经营转正路线图', '牵头：产业发展部＋运管中心',
     '节点：2027 年 EBITDA 转正、2028 年经营现金流转正、2029 年利润总额转正、2030 年 ROE 3.5%'),
 7: ('S07 及时改造，打造自营标杆', '牵头：产业发展部＋运管中心',
     '节点：2026 年底前锁定双品牌方案与投资决策；2027 年起分区改造不停业；2027 年 EBITDA 转正、2028 年经营现金流转正、2029 年利润总额转正'),
 8: ('S07 及时改造，打造自营标杆', '牵头：产业发展部＋运管中心；工程由投资和资产部主责',
     '节点：2026 年底前完成方案与投资决策；次年高考结束后重装开业（2027 年 7 月）；品牌手册与五项模型同期交付'),
 9: ('S07 及时改造，打造自营标杆', '牵头：产业发展部＋运管中心',
     '节点：2026 年底前完成在地化改造立项；2027 年 GOP 转正、2028 年利润总额转正、2030 年 ROE 3.5%'),
 10: ('S07 及时改造，打造自营标杆', '牵头：产业发展部＋运管中心；产权划转由投资和资产部主责',
      '节点：2026 年底前完成产权划转并明确投资主体；2027 年上半年交付锦著 2.0 产品母版与培训基地；未划转前不做大额投入'),
 11: ('S10 品牌与运营输出（轻资产）', '牵头：产业发展部',
      '节点：2027 年上半年形成平台合同模板、费率标准与盈亏平衡测算；2027 年起承接资阳区域存量项目整合'),
 12: ('S11 止损且不新增投入 ＋ S08 分年度转正路线图', '牵头：资产经营条线＋本部人力主责人资分离；产业发展部主责体旅融合方向与品牌统一',
      '节点：2026 年底前完成人资分离与业务边界清理；2027 年 EBITDA 转正、2028 年经营现金流转正；2027 年内完成出售或出租二选一'),
 13: ('S06 人资分离、本部统一管资产', '牵头：本部＋人力；产业发展部配合资产推介',
      '节点：2026 年底前完成人资分离与租金重估签约'),
 14: ('S06 人资分离、本部统一管资产', '牵头：本部＋人力；产业发展部配合资产推介',
      '节点：2026 年底前完成人资分离与租金重估签约'),
 15: ('S06 人资分离、本部统一管资产', '牵头：本部＋人力；产业发展部配合资产推介',
      '节点：2026 年底前完成人资分离、权属登记与租金归集路径明确'),
 14.1: ('', '', ''),
 16: ('S07 及时改造，打造自营标杆', '牵头：产业发展部＋运管中心；工程由投资和资产部主责',
      '节点：2026 年底前完成立项与模块清单；2027 年完成改造并实现 RevPAR 140 至 176 元；2027 年 EBITDA 转正'),
 17: ('S04 闲置资产出租优先、其次出售', '牵头：资产经营条线；产业发展部负责度假资源包招商',
      '节点：2026 年底前完成出租或转让方案；资源包招商 2027 年上半年启动'),
 18: ('S04 闲置资产出租优先、其次出售', '牵头：资产经营条线；产业发展部配合资源包招商',
      '节点：2026 年底前完成出租或转让方案'),
 19: ('S04 闲置资产出租优先、其次出售', '牵头：资产经营条线；产业发展部配合捆绑转让与资源包打包',
      '节点：2026 年底前完成捆绑协议转让或资产置换方案，挂牌 7 次无报名后不再沿用纯市场挂牌'),
 20: ('S11 止损且不新增投入', '牵头：资产经营条线；产业发展部配合资产与经营核查，不承接品牌与运营投入',
      '节点：2026 年底前形成山集园债务隔离与化解方案及时间表'),
 21: ('S08 分年度经营转正路线图', '牵头：产业发展部＋运管中心',
      '节点：2027 年 EBITDA 转正、2028 年经营现金流转正、2029 年利润总额转正；品牌切换与标准接入 2026 年底前完成'),
 22: ('S03 关停清算与注销退出', '牵头：资产经营条线＋法务；产业发展部负责品牌授权终止、预收款与会员权益清理',
      '节点：2026 年底前完成品牌终止、预收款与未住订单清理，同步完成同类在管项目穿透排查'),
 23: ('S04 闲置资产出租优先、其次出售', '牵头：资产经营条线；产业发展部提供品牌合作与联合空间方案',
      '节点：2026 年底前完成联合空间合作可行性判断与最迟处置时点'),
 24: ('S03 关停清算与注销退出', '牵头：资产经营条线＋法务；产业发展部负责品牌与预收款清理',
      '节点：2026 年底前完成会员权益责任划分与预收款处理，沉淀清算操作标准清单'),
 25: ('S11 止损且不新增投入', '牵头：资产经营条线；产业发展部负责体旅融合方向与品牌统一',
      '节点：2026 年底前完成业务与资产边界清理；2027 年前完成转正或退出二选一'),
 26: ('S04 闲置资产出租优先、其次出售', '牵头：资产经营条线；产业发展部配合资产池推介',
      '节点：2026 年底前完成出租或转让方案'),
 27: ('S04 闲置资产出租优先、其次出售', '牵头：资产经营条线；产业发展部负责品牌与运营方案',
      '节点：2026 年底前完成品牌运营权合作方案，不接受收购产权'),
 28: ('S10 品牌与运营输出（轻资产）＋ S12 尽快决策', '牵头：本部＋产业发展部',
      '节点：2026 年底前完成管道费台账归集与合同口径统一；2027 年上半年建立对外报价基准与收费用途比例原则'),
 29: ('S12 尽快决策（待定）', '牵头：本部＋产业发展部',
      '节点：2026 年底前补齐数据并明确决策人；与锦森天成合并打包推介'),
 30: ('S12 尽快决策（待定）', '牵头：本部＋产业发展部',
      '节点：2026 年底前补齐数据并明确决策人；与锦城悦都合并打包推介'),
}

wb = openpyxl.load_workbook(XLSX)
ws = wb.active
rows = []
for r in range(2, ws.max_row + 1):
    no = ws.cell(r, 1).value
    name = ws.cell(r, 2).value
    diag = ws.cell(r, 3).value
    sol = ws.cell(r, 4).value
    rows.append([no, name, diag, sol])

out = []
patched = []
for no, name, diag, sol in rows:
    k = int(no)
    sc, lead, node = M.get(k, ('', '', ''))
    if sc:
        sol2 = sc + '｜' + lead + '｜' + node + '：' + sol
        patched.append(k)
    else:
        sol2 = sol
    out.append([no, name, diag, sol2])

# 重写 Excel
wb2 = openpyxl.Workbook()
w2 = wb2.active
w2.title = '一店一策_产发部归口'
w2.append(['序号', '公司名称', '问题诊断', '解决方案'])
thin = Side(style='thin', color='BFBFBF')
bd = Border(left=thin, right=thin, top=thin, bottom=thin)
hf = PatternFill('solid', fgColor='D9E2F3')
for c in range(1, 5):
    cell = w2.cell(row=1, column=c)
    cell.font = Font(name='微软雅黑', size=10, bold=True)
    cell.fill = hf
    cell.alignment = Alignment(horizontal='center', vertical='center')
    cell.border = bd
for row in out:
    w2.append(row)
for r in range(2, len(out) + 2):
    for c in range(1, 5):
        cell = w2.cell(row=r, column=c)
        cell.border = bd
        cell.font = Font(name='微软雅黑', size=9)
        if c == 1:
            cell.alignment = Alignment(horizontal='center', vertical='top')
        elif c == 2:
            cell.alignment = Alignment(horizontal='center', vertical='top', wrap_text=True)
        else:
            cell.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
w2.column_dimensions['A'].width = 5
w2.column_dimensions['B'].width = 14
w2.column_dimensions['C'].width = 66
w2.column_dimensions['D'].width = 80
for r in range(2, len(out) + 2):
    w2.row_dimensions[r].height = 150
w2.row_dimensions[1].height = 26
w2.freeze_panes = 'A2'
wb2.save(XLSX)
print('Excel 已升级 -> ' + os.path.basename(XLSX))
print('  已补 S码/牵头/节点 的行: ' + str(patched))
print('  未覆盖行: ' + str([int(o[0]) for o in out if int(o[0]) not in patched]))

# 重写 Markdown
lines = ['# 一店一策梳理 · 产业发展部归口填报 v1.1', '',
         '> **编制**：B166ER｜**编制时间**：2026-11-18｜**版本**：v1.1（在 v1.0 基础上补入 S 策略码、牵头主体与关键节点，满足《一企一策分析范式 v1.0》V06／V10 阻断级校验）',
         '> **用途**：集团一店一策共享表格的产业发展部归口部分，供直接复制粘贴',
         '> **归口依据**：《一企一策分析范式 v1.0》（2026-11-11）—— 产发部牵头项为 S07 及时改造打造自营标杆、S08 分年度经营转正路线图、S10 品牌与运营输出、S12 尽快决策',
         '> **格内格式**：解决方案＝「策略码｜牵头主体｜关键节点：具体动作」',
         '> **口径**：行序与集团共享表一致（序号 1 至 30）；问题诊断与解决方案均为产业发展部视角，其他部门已填内容建议追加而非覆盖',
         '', '| 序号 | 公司名称 | 问题诊断 | 解决方案 |', '|---|---|---|---|']
for no, name, diag, sol in out:
    lines.append('| ' + str(no) + ' | ' + name + ' | ' + diag + ' | ' + sol + ' |')
lines.append('')
lines.append('## 产发部归口速查')
lines.append('')
lines.append('| 策略码 | 序号 | 公司 |')
lines.append('|---|---|---|')
for no, name, diag, sol in out:
    k = int(no)
    sc = M.get(k, ('', '', ''))[0] or 'S09 存量资产盘活与对外转让'
    lines.append('| ' + sc + ' | ' + str(k) + ' | ' + name + ' |')
lines.append('')
open(MD, 'w', encoding='utf-8').write('\n'.join(lines))
print('Markdown 已升级: ' + str(len(lines)) + ' 行')

# 校验
wb3 = openpyxl.load_workbook(XLSX)
w3 = wb3.active
bad = []
for r in range(2, w3.max_row + 1):
    for c in (1, 2, 3, 4):
        if not w3.cell(r, c).value:
            bad.append((r, c))
print('')
print('空缺单元格: ' + (str(bad) if bad else '无'))
print('维度: %d x %d' % (w3.max_row, w3.max_column))
s07 = [int(w3.cell(r, 1).value) for r in range(2, w3.max_row + 1) if 'S07' in str(w3.cell(r, 4).value) or 'S08' in str(w3.cell(r, 4).value)]
print('S07/S08 行（V10 适用）: ' + str(s07))
miss10 = []
for r in range(2, w3.max_row + 1):
    s = str(w3.cell(r, 4).value)
    if ('S07' in s or 'S08' in s) and ('节点：' not in s or '牵头：' not in s):
        miss10.append(int(w3.cell(r, 1).value))
print('V10 未满足行: ' + (str(miss10) if miss10 else '无'))
miss06 = [int(w3.cell(r, 1).value) for r in range(2, w3.max_row + 1) if not re.match(r'^S\d\d', str(w3.cell(r, 4).value))]
print('V06 未落 S 码行: ' + (str(miss06) if miss06 else '无'))
