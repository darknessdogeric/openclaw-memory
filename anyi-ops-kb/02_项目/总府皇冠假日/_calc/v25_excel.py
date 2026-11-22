
# -*- coding: utf-8 -*-
"""v25：重出 Word + 生成 Excel 附表 + 终检"""
import io, os, sys, re, json, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
CALC=r'D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc'
KB=r'D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日'
TGT=r'C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店'
REP=os.path.join(TGT,'改造报告交付'); CALC_OUT=os.path.join(TGT,'测算与中间产物')
PY=r'C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe'
ENV=dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')
# ── 1. Word ──
r=subprocess.run([PY,os.path.join(CALC,'v25_docx.py')],capture_output=True,text=True,encoding='utf-8',errors='replace',env=ENV,timeout=1800)
print('docx rc=',r.returncode)
if r.returncode: print((r.stderr or '')[-600:])
lg=os.path.join(r'D:\B166ER-openclaw\workspace\.tmp','v17.log')
LOG=io.open(lg,encoding='utf-8').read()
print('--- docx log 末 6 行 ---')
print('\n'.join(LOG.split('\n')[-6:]))
# ── 2. Excel ──
V25=json.load(open(r'D:\B166ER-openclaw\workspace\.tmp\v25.json',encoding='utf-8'))
V25B=json.load(open(r'D:\B166ER-openclaw\workspace\.tmp\v25b.json',encoding='utf-8'))
V25C=json.load(open(r'D:\B166ER-openclaw\workspace\.tmp\v25c.json',encoding='utf-8'))
P=V25['P']; BRS=V25B['ROWS']; SENS=V25C
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as XLImage
wb=Workbook()
H=Font(bold=True,color='FFFFFF',size=10); FILL=PatternFill('solid',fgColor='1F4E79')
SUB=PatternFill('solid',fgColor='DDEBF7'); BD=Border(*[Side(style='thin',color='B4C6E7')]*4)
def f0(v): return '{:,}'.format(int(round(v)))
def sg(v): return ('\u2212'+f0(abs(v))) if v<0 else ('\uff0b'+f0(v))
def pc(v): return ('%.2f%%'%(100*v)) if v is not None else '为负'
def yr(v): return ('%.1f 年'%v) if v else '未回本'
def sheet(name, hdr, rows, widths=None, freeze='A2'):
    ws=wb.create_sheet(name)
    ws.append(hdr)
    for c in ws[1]:
        c.font=H; c.fill=FILL; c.alignment=Alignment(horizontal='center',vertical='center',wrap_text=True)
    for r in rows: ws.append(r)
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.border=BD
            c.alignment=Alignment(horizontal='center',vertical='center',wrap_text=True)
    for i in range(1,len(hdr)+1):
        ws.column_dimensions[get_column_letter(i)].width=(widths[i-1] if widths and i-1<len(widths) else max(10,min(26,len(str(hdr[i-1]))*2+8)))
    ws.freeze_panes=freeze; ws.row_dimensions[1].height=32
    return ws
# 00 读我
ws=wb.active; ws.title='00 说明与口径'
INFO=[('项目','总府皇冠假日酒店重大安全隐患改造项目 · 可行性研究报告（v25.0）'),
 ('编制日期','2026-11-16'),
 ('本版修正一','段一停业损失恢复 034 造价构成表口径 815 万元/月（营业收入损失 564.5＋刚性支出 250.5）'),
 ('本版修正二','停业期按工程流水重核：19／23／26／20／29／29／33 个月'),
 ('本版修正三','取消特许／全委财务分支，统一按品牌档次费率'),
 ('本版修正四','房价锚点改用本物业实测 ADR（2026-10 实测 418.6 元），OTA 挂牌价仅作上限检验'),
 ('评价期','20 年（240 个月），折现率 8%，按月折现'),
 ('口径','项目口径（不含存量债务利息 60,677 万元／年息 2,088.85 万元，另案处理）'),
 ('增量口径','项目臂与不改造臂同窗口逐月对齐，停业期经营损失完整计入'),
 ('反事实基线','不改造继续经营：业主口径年均 −1,924 万元/年（USALI 实测），项目口径 −139 万元/年，按 −5%/年劣化'),
 ('关键结论','七路径增量口径 NPV 均为负；P4 洲至奢选·保留·不减房最优（−6,653 万元、IRR 4.91%、回收 13.6 年）'),
 ('本项目性质','刚性安全合规改造，非商业投资；立项须以增量现金流而非全口径 IRR 考核'),
 ('模型引擎','_calc/v25_model.py（USALI 部门制＋HMA 品牌费用结构）｜_calc/v25_figs.py（敏感性与图件）'),
]
ws.append(['项目','内容'])
for c in ws[1]: c.font=H; c.fill=FILL; c.alignment=Alignment(horizontal='center')
for a,b in INFO: ws.append([a,b])
for row in ws.iter_rows(min_row=2):
    row[0].font=Font(bold=True,size=10); row[0].fill=SUB
    for c in row: c.border=BD; c.alignment=Alignment(vertical='center',wrap_text=True)
ws.column_dimensions['A'].width=16; ws.column_dimensions['B'].width=96
# 01 投资基数
sheet('01 投资基数与停业期',['方案','品牌与做法','房量','客房套内㎡','停业月','段二','段三','改造投资','段一现金口径','段一经济口径815月','项目总投资','面积门槛'],
 [[p['k'],p['nm'],p['rm'],p['suite'],p['du'],f0(p['s2']),f0(p['s3']),f0(p['cap']),f0(p['seg1_cash']),f0(p['seg1_econ']),f0(p['invest_total']),p['gate']] for p in P],
 [8,24,8,11,9,11,11,12,15,16,12,12])
# 02 停业期流水
WK={'P1':4,'P2':6,'P3':8,'P4':4,'P5':9,'P6':9,'P7':11}
sheet('02 停业期工程流水',['方案','路径','准备拆除','机电主干','楼层流水月','单层周数','设备就绪','联调消防验收','整改复评','品牌方验收','试营业','合计月'],
 [[p['k'],p['nm'],p['dt']['t_mep'],p['dt']['t_mep'],p['dt']['floor_m'],WK[p['k']],p['dt']['t_eq'],p['dt']['t_fire'],p['dt']['t_fix'],p['dt']['t_brand'],p['dt']['t_trial'],p['dt']['total']] for p in P],
 [8,24,10,10,11,10,10,13,10,12,9,9])
# 03 七路径结果
sheet('03 七路径结果',['方案','路径','ADR中档','平衡价全口径','平衡价增量','全口径NPV','增量NPV','IRR全口径','IRR增量','静态回收期增量','正数格增量'],
 [[p['k'],p['nm'],p['adr'][1],('%d'%p['be_full']) if p['be_full'] else '不可达',('%d'%p['be_inc']) if p['be_inc'] else '不可达',
   sg(p['full_mid']),sg(p['inc_mid']),pc(p['irr_full']),pc(p['irr_inc']),yr(p['pb_inc']),'%d/15'%p['pos_inc']] for p in P],
 [8,24,11,13,13,13,13,12,12,15,12])
# 04 增量动态区间
rows=[]
for p in P:
    for i,a in enumerate(p['adr']):
        rows.append([p['k'],p['nm'],a]+[sg(v) for v in p['g_inc'][i]]+[sum(1 for v in p['g_inc'][i] if v>0)])
sheet('04 增量口径动态区间',['方案','路径','ADR','65%','70%','75%','80%','85%','正数格'],rows,[8,24,9,12,12,12,12,12,10])
# 05 全口径动态区间
rows=[]
for p in P:
    for i,a in enumerate(p['adr']):
        rows.append([p['k'],p['nm'],a]+[sg(v) for v in p['g_full'][i]]+[sum(1 for v in p['g_full'][i] if v>0)])
sheet('05 全口径动态区间',['方案','路径','ADR','65%','70%','75%','80%','85%','正数格'],rows,[8,24,9,12,12,12,12,12,10])
# 06 25 品牌
sheet('06 25品牌统一表',['级别','品牌','集团','品牌标准','做法','房量','面积门槛','改造投资','ADR低','ADR中','ADR高','平衡价75%','增量NPV','IRR增量','静态回收期','成都落位与可得性'],
 [[r['lvl'],r['nm'],r['grp'],r['std'],r['route'],r['rm'],r['gate'],f0(r['cap']),r['adr'][0],r['adr'][1],r['adr'][2],
   ('%d'%r['be']) if r['be'] else '不可达',sg(r['inc_mid']),pc(r['irr']),yr(r['pb']),r['loc']] for r in BRS],
 [9,15,11,12,8,8,12,12,9,9,9,12,12,11,13,30])
# 07 敏感性
rows=[]
for pk in ('P1','P4','P6'):
    s=SENS[pk]
    for n,v in s['rows']: rows.append([pk,s['base'],n,v,v-s['base']])
sheet('07 敏感性分析',['方案','基准NPV','变量与变化','NPV','相对基准'],rows,[10,14,26,14,14])
# 08 20年现金流
for pk in ('P1','P4'):
    p=[x for x in P if x['k']==pk][0]
    rows=[[y+1,p['adr20'][y]/p['adr'][1],p['adr20'][y],p['occ20'][y],f0(p['rev20'][y]),f0(p['tr20'][y]),f0(p['cf20'][y])] for y in range(20)]
    sheet('08 %s 20年现金流'%pk,['年','爬坡系数','ADR元','出租率%','总营收万元','TRevPAR元间','营业现金流万元'],rows,[7,11,11,11,13,13,15])
# 09 实测基线
sheet('09 实测基线',['指标','数值','来源'],[
 ['客房收入（2026-10）','412.8 万元','2026年10月利润表 Rooms Revenue'],
 ['已售间夜（2026-10）','10,048 间','Rooms Sold'],
 ['入住间夜（2026-10）','9,862 间','Rooms Occupied'],
 ['可售间夜（2026-10）','12,460 间','Rooms Available（402 间×31 天）'],
 ['ADR（2026-10）','418.6 元/间夜','利润表 Average Room Rate'],
 ['ADR（2026-01至10累计）','373.1 元/间夜','利润表 YTD'],
 ['出租率（10月／YTD）','79.14% ／ 73.75%','利润表 Room Occupancy'],
 ['RevPAR（10月／YTD）','331.2 ／ 275.2 元','利润表'],
 ['现状单位面积价','13.7 元/㎡·夜','ADR 418.6 ÷ 可售房型面积 30.57 ㎡'],
 ['OTA 挂牌对照','728 元 ÷ 30 ㎡ ＝ 24.3 元/㎡·夜','携程挂牌（展示价，非可达价；实测达成仅为其 57%）'],
 ['停业损失口径','815 万元/月','造价构成表 02 表：收入损失 564.5＋刚性支出 250.5'],
 ['项目口径停业刚性支出','162.5 万元/月','715 附件6：3,674 万元/年（含存量利息 1,724）剔除后'],
 ['段二合计（不减房）','8,790 万元','039 表逐项相加校验'],
 ['品牌专项移入段三','1,990 万元','智能化500＋厨房500＋庭院220＋网络270＋电视100＋梯控260＋车库140'],
 ['反事实基线（业主口径）','−1,924 万元/年','USALI 实测'],
 ['反事实基线（项目口径）','−139 万元/年','剔除存量利息 1,785 万元/年'],
 ['存量债务','60,677 万元／年息 2,088.85 万元','另案处理，不进项目现金流'],
],[24,32,52])
# 10 图件索引
FIGD=os.path.join(CALC,'fig')
figs=[f for f in sorted(os.listdir(FIGD)) if f.startswith('fig') and f.lower().endswith('.png')]
ws=sheet('10 图件',['图号','文件名','用途'],[
 ['图1','fig1_现金流曲线.png','20 年营业现金流与 TRevPAR 趋势'],
 ['图2','fig2_NPV路径.png','七路径 NPV 与 IRR 对比'],
 ['图3','fig3_敏感性.png','P4 敏感性龙卷风图'],
 ['图4','fig4_NPV对ADR.png','增量口径 NPV 对 ADR 敏感性与单位面积价天花板'],
 ['图5','fig5_停业期流水.png','各路径停业期工程流水甘特'],
],[8,34,52])
for i,f in enumerate(figs[:5]):
    try:
        im=XLImage(os.path.join(FIGD,f)); im.width=760; im.height=430
        ws.add_image(im,'D%d'%(i+2))
    except Exception as e: print('  img skip',f,e)
X=os.path.join(CALC_OUT,'总府皇冠改造_测算附表_v25.0_2026-11-16.xlsx')
wb.save(X)
print('xlsx %.1f KB sheets %d' % (os.path.getsize(X)/1024, len(wb.sheetnames)))
print('sheets:', wb.sheetnames)
