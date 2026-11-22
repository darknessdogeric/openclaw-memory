# -*- coding: utf-8 -*-
"""v26_excel.py：12 表测算附表（口径与 v26 模型一致）"""
import io, os, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
CALC = r'D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc'
TGT = r'C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店'
REP = os.path.join(TGT,'改造报告交付'); CALC_OUT = os.path.join(TGT,'测算与中间产物')
os.makedirs(REP, exist_ok=True); os.makedirs(CALC_OUT, exist_ok=True)
T = r'D:\B166ER-openclaw\workspace\.tmp'
V = json.load(open(os.path.join(T,'v26a.json'), encoding='utf-8'))
VB = json.load(open(os.path.join(T,'v26b.json'), encoding='utf-8'))
VC = json.load(open(os.path.join(T,'v26c.json'), encoding='utf-8'))
P = V['P']; RES = V['RES']; BE = V['BE']; CAP = V['CAP']; THR = V['THR']
GRID = V['GRID']; GRID_INC = V['GRID_INC']; M = V['M']; MINC = V['MIN_COMPLY']
BRS = VB['ROWS']
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as XLImage
wb = Workbook()
H = Font(bold=True, color='FFFFFF', size=10); FILL = PatternFill('solid', fgColor='1F4E79')
SUB = PatternFill('solid', fgColor='DDEBF7'); BD = Border(*[Side(style='thin', color='B4C6E7')]*4)
def f0(v): return '{:,}'.format(int(round(v)))
def sg(v): return ('\u2212' + f0(abs(v))) if v < 0 else ('\uff0b' + f0(v))
def pc(v): return ('%.2f%%' % (100*v)) if v is not None else '为负'
def yr(v): return ('%.1f 年' % v) if v else '未回本'
def res(k, lbl):
    for r in RES:
        if r['k']==k and r['lbl']==lbl: return r
    return {}
def sheet(name, hdr, rows, widths=None, freeze='A2'):
    ws = wb.create_sheet(name)
    ws.append(hdr)
    for c in ws[1]:
        c.font=H; c.fill=FILL; c.alignment=Alignment(horizontal='center',vertical='center',wrap_text=True)
    for r in rows: ws.append(r)
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.border=BD; c.alignment=Alignment(horizontal='center',vertical='center',wrap_text=True)
    for i in range(1, len(hdr)+1):
        ws.column_dimensions[get_column_letter(i)].width = (widths[i-1] if widths and i-1<len(widths) else max(10,min(26,len(str(hdr[i-1]))*2+8)))
    ws.freeze_panes = freeze; ws.row_dimensions[1].height = 32
    return ws

# 00 说明与口径
ws = wb.active; ws.title = '00 说明与口径'
INFO = [('项目','总府皇冠假日酒店重大安全隐患改造项目 · 可行性研究报告（v26.0）'),
 ('编制日期','2026-11-20'),
 ('测算方法','市场分析价格 → 反算投资承受力：先由市场分析确定各档次可达价格，再在该价格下求 20 年可承受改造投资上限，最后比选路径'),
 ('路径体系','①保留客房体量·轻改　②保留客房体量·重改　③客房体量变化·重改'),
 ('评价期','20 年（240 个月），折现率 8%，按月折现；经营状态为抛物线（7 年一循环，逐循环衰减）'),
 ('价格口径','以市场分析价格为锚，OTA 挂牌价仅作上限检验；凡涉面积妥协取档位下限，凡涉减房不采信上限'),
 ('经营模型','按 2026 年 10 月实测利润表结构复现，模型与实测误差 0.03%'),
 ('反事实臂','最小合规臂：段二 11,060 万元＋停业 18 个月＋产品力逐年老化 5%；纪要明确依法合规停业整改'),
 ('项目口径','不含存量债务利息（60,677 万元／年息 2,088.85 万元，另案处理）；存量利息在增量口径下两臂对冲'),
 ('关键结论','A1 皇冠假日·保留体量轻改：增量 NPV ＋3,457 万元、IRR 11.35%、回收 9.8 年；A2 安逸集团自有五星：＋3,290 万元、11.22%、9.9 年'),
 ('成立条件','25 个候选中仅 3 个增量 NPV 为正（皇冠假日、安逸自有五星、voco），全部为不减房方案'),
 ('模型引擎','_calc/v26_model.py（造价与现金流）｜_calc/v26_brands.py（25 品牌）｜_calc/v26_sens.py（敏感性）｜_calc/v26_figs.py（图件）'),
]
ws.append(['项目','内容'])
for c in ws[1]: c.font=H; c.fill=FILL; c.alignment=Alignment(horizontal='center')
for a,b in INFO: ws.append([a,b])
for row in ws.iter_rows(min_row=2):
    row[0].font=Font(bold=True,size=10); row[0].fill=SUB
    for c in row: c.border=BD; c.alignment=Alignment(vertical='center',wrap_text=True)
ws.column_dimensions['A'].width=16; ws.column_dimensions['B'].width=100

# 01 投资基数与停业期
sheet('01 投资基数与停业期',['方案','路径分类','档次','品牌与做法','房量','客房套内㎡','停业月','段二','段三','品牌专项','改造投资','停业损失经济口径','项目总投资','面积门槛'],
 [[p['k'],p['grp'],p['tier'],p['b'],p['rooms'],p['suite'],p['du'],f0(p['s2']),f0(p['s3']),f0(p['special']),f0(p['capex']),f0(p['down_loss_econ']),f0(p['capex']+p['down_loss_econ']),p['gate']] for p in P],
 [8,20,11,14,8,11,8,11,11,11,12,16,12,22])

# 02 停业期工程流水
sheet('02 停业期工程流水',['方案','路径','准备＋拆除＋机电主干','楼层流水月','单层周数','设备就绪','联调消防验收','整改复评','品牌方验收','试营业','合计月'],
 [[p['k'],p['nm'],p['dt']['t_mep'],p['dt']['floor_m'],p['dt']['wk'],p['dt']['t_eq'],p['dt']['t_fire'],p['dt']['t_fix'],p['dt']['t_brand'],p['dt']['t_trial'],round(p['dt']['total'])] for p in P],
 [8,26,17,12,10,11,13,10,12,9,9])

# 03 八路径财务结果
rows=[]
for p in P:
    for lbl in ('低','中','高'):
        r = res(p['k'], lbl)
        rows.append([p['k'],p['nm'],lbl,p['mkt'][['低','中','高'].index(lbl)],sg(r['full']),sg(r['inc']),pc(r['irr']),pc(r['irr_inc']),yr(r['pb'])])
sheet('03 八路径财务结果',['方案','路径','档','ADR','全口径NPV','增量NPV','IRR全口径','IRR增量','静态回收期'],rows,[8,26,6,9,14,14,12,12,13])

# 04 增量动态区间
rows=[]
for p in P:
    for lbl, adr, row in GRID_INC[p['k']]:
        rows.append([p['k'],p['nm'],lbl,adr]+[sg(v) for v in row]+[sum(1 for v in row if v>0)])
sheet('04 增量动态区间',['方案','路径','定价档','ADR','65%','70%','75%','80%','85%','正数格'],rows,[8,26,9,9,12,12,12,12,12,10])

# 05 全口径动态区间
rows=[]
for p in P:
    for lbl, adr, row in GRID[p['k']]:
        rows.append([p['k'],p['nm'],lbl,adr]+[sg(v) for v in row]+[sum(1 for v in row if v>0)])
sheet('05 全口径动态区间',['方案','路径','定价档','ADR','65%','70%','75%','80%','85%','正数格'],rows,[8,26,9,9,12,12,12,12,12,10])

# 06 可承受改造投资上限
rows=[]
for p in P:
    for lbl in ('低','中','高'):
        c = CAP[p['k']][lbl]; ci = c['cap_inc']
        rows.append([p['k'],p['nm'],lbl,p['mkt'][['低','中','高'].index(lbl)],f0(p['capex']),f0(c['cap_full']),f0(ci) if ci else '不可达',
                    f0(p['capex']-ci) if ci else '—','成立' if (ci and ci>=p['capex']) else '不成立'])
sheet('06 可承受改造投资上限',['方案','路径','档','ADR','估算改造投资','全口径可承受上限','增量可承受上限','增量缺口','结论'],rows,[8,26,6,9,14,16,16,12,10])

# 07 25 品牌统一表
rows=[]
for r in sorted(BRS, key=lambda x:(0 if x['inc']>0 else 1, -x['inc'])):
    rows.append([r['lvl'],r['nm'],r['grp'],r['cfg'],r['rm'],r['suite'],r['thr'],r['gate'],r['du'],f0(r['cap']),r['adr'][0],r['adr'][1],r['adr'][2],
                 sg(r['inc']),pc(r['irr']),yr(r['pb']),f0(r['cmax']) if r['cmax'] else '不可达',r['loc'],r['avail']])
sheet('07 25品牌统一表',['级别','品牌','集团','做法','房量','客房套内㎡','面积门槛㎡','面积妥协条件','停业月','改造投资','ADR低','ADR中','ADR高','增量NPV','IRR增量','静态回收期','可承受上限','成都落位','可得性与商务前提'],rows,
 [9,14,11,8,7,11,11,22,8,11,8,8,8,13,11,12,12,26,34])

# 08 敏感性分析
rows=[]
for pk in ('A1','A2','A4R'):
    s = VC[pk]
    for n,v in s['rows']: rows.append([pk,s['base'],n,v,v-s['base']])
    rows.append([pk,s['base'],'组合：投资 −10% 且停业 −3 月',s['combo'],s['combo']-s['base']])
sheet('08 敏感性分析',['方案','基准增量NPV','变量与变化','增量NPV','相对基准'],rows,[10,15,28,14,14])

# 09 平衡点与阈值区间
rows=[]
for t in THR:
    if not t.get('be'): continue
    p = [x for x in P if x['k']==t['k']][0]
    d = {r[0]: r[1] for r in t['rows']}
    rows.append([t['k'],p['nm'],round(t['be']),sg(BE[t['k']]['be_inc']),
                 sg(d.get('改造投资 −20%',0)),sg(d.get('改造投资 −10%',0)),sg(d.get('改造投资 ＋10%',0)),sg(d.get('改造投资 ＋20%',0)),
                 sg(d.get('开房率 −5pp',0)),sg(d.get('开房率 ＋5pp',0)),sg(d.get('停业期 −3 月',0)),sg(d.get('停业期 ＋3 月',0)),
                 sg(d.get('ADR −10%',0)),sg(d.get('ADR ＋10%',0))])
sheet('09 平衡点与阈值区间',['方案','路径','平衡ADR','增量平衡ADR','投资−20%','−10%','＋10%','＋20%','开房−5pp','＋5pp','停业−3月','＋3月','ADR−10%','＋10%'],rows,
 [8,26,11,13,12,12,12,12,12,12,12,12,12,12])

# 10 实测基线
sheet('10 实测基线',['指标','数值','来源'],[
 ['客房收入（2026-10）','412.8 万元','2026 年 10 月利润表 Rooms Revenue'],
 ['已售间夜（2026-10）','10,048 间','Rooms Sold'],
 ['入住间夜（2026-10）','9,862 间','Rooms Occupied'],
 ['可售间夜（2026-10）','12,460 间','Rooms Available（402 间×31 天）'],
 ['ADR（2026-10）','418.6 元/间夜','雅高 Average Room Rate'],
 ['ADR（2026-01 至 10 累计）','373.1 元/间夜','雅高 YTD'],
 ['出租率（10 月／YTD）','79.14% ／ 73.75%','雅高 Room Occupancy'],
 ['RevPAR（10 月／YTD）','331.2 ／ 275.2 元','雅高'],
 ['现状单位面积价','13.7 元/㎡·夜','ADR 418.6 ÷ 可售房型面积 30.57 ㎡'],
 ['OTA 挂牌价对照','728 元（30 ㎡），折 24.3 元/㎡·夜','携程挂牌（展示价，非可达价）'],
 ['GOI 率（实测）','62.73%','P&L Summary：3,812.77／6,078.07（年化）'],
 ['未分配费用率（实测）','33.21%','P&L Summary：2,018.53／6,078.07（年化）'],
 ['Adjusted GOP（实测）','1,672.68 万元','P&L Summary（年化）'],
 ['激励费（实测）','83.63 万元','P&L Summary（年化）'],
 ['项目口径经营现金流','＋1,589 万元/年','Adjusted GOP 1,672.68 − 激励费 83.63'],
 ['实测 NOP','−499.81 万元/年','P&L Summary（年化，含存量利息 1,724）'],
 ['Other Non-Operating','2,088.86 万元/年','P&L Summary（年化）'],
 ['停业损失（业主经济口径）','815 万元/月','039 表 02 表：营业收入损失 564.5＋刚性支出 250.5'],
 ['停业期刚性支出（项目口径）','162.5 万元/月','715 定稿附件 6：3,674 万元/年剔除存量利息 1,724'],
 ['段二（不减房／减房）','11,060 ／ 11,600 万元','039 表 07 G 列原值'],
 ['品牌专项','1,620（国际联号）／1,500（安逸自有）万元','智能化 500＋推广 500＋渠道 220＋软接 260＋灯饰 140'],
 ['反事实臂（最小合规臂）','段二 11,060＋停业 18 个月＋年衰减 5%','纪要明确依法合规停业整改'],
 ['反事实臂 20 年 NPV','−3,433 万元','项目口径，折现率 8%'],
 ['存量债务','60,677 万元，年息 2,088.85 万元','另案处理，不进项目现金流'],
],[26,30,54])

# 11 图件
FIGD = os.path.join(CALC,'fig26')
figs = [f for f in sorted(os.listdir(FIGD)) if f.lower().endswith('.png')]
ws = sheet('11 图件',['图号','文件名','用途'],[])
USE = {'fig01':'增量口径 NPV 对 ADR 的敏感性与市场分析价格带','fig02':'八路径 NPV 与 IRR 对比（三路径分类）',
       'fig03':'A1 平衡点左右的阈值区间（敏感性龙卷风）','fig04':'推荐路径的 15 格动态区间热力图',
       'fig05':'各路径停业期工程流水核定','fig06':'25 个品牌候选增量口径 NPV 比较','fig07':'20 年现金流与累计增量现金流'}
for i,f in enumerate(figs):
    k = f[:5]
    ws.append(['图 %d'%(i+1), f, USE.get(k,'图件')])
    try:
        im = XLImage(os.path.join(FIGD,f)); im.width=760; im.height=430
        ws.add_image(im,'D%d'%(i+2))
    except Exception as e: print('  img skip', f, e)
ws.column_dimensions['B'].width=40; ws.column_dimensions['C'].width=52

X = os.path.join(CALC_OUT,'总府皇冠改造_测算附表_v26.0_2026-11-20.xlsx')
wb.save(X)
print('xlsx %.1f KB  sheets %d' % (os.path.getsize(X)/1024, len(wb.sheetnames)))
print('sheets:', wb.sheetnames)