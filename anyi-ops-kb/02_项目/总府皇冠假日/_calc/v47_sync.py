# -*- coding: utf-8 -*-
"""v47：风险增补 + Excel 同步（17 文创化情景 / 18 十五五战略对标与在地文化）+ 公文 Word 重出 + 终检"""
import io, os, sys, re, json, glob, subprocess
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v47.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

MD = os.path.join(KB, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
t = open(MD, encoding="utf-8").read()

# ══ ① 风险增补 R-23 / R-24 / R-25 ══
lines = t.split("\n")
idx = None
for i in range(len(lines) - 1, -1, -1):
    if re.match(r"^\|\s*R-\d+\s*\|", lines[i]):
        idx = i; break
assert idx is not None, "未定位风险表"
lines[idx + 1:idx + 1] = [
 "| R-23 | 在地文化溢价不兑现（策展溢价指数低于 1.10） | 中 | 高 | 高 | 三年内容预算 1,200 万元分期释放，首年设 Kill 判据：复业后第 12 个月 CPI<1.10 即停止追加并降回 L2 叙事层；文创化仅使绝对净现值改善 3,878.6 万元，不构成方案成立的独立依据 | 产业发展部 |",
 "| R-24 | 春熙路商圈品牌序列冲突，集团内部自我蚕食 | 高 | 中 | 中 | 集团在春熙路及邻近已有多处自有门店且存在同址多条目问题；须在投资决策前完成春熙路商圈品牌序列与客群分层设计，纳入集团商圈分级分类联动课题 | 产业发展部 |",
 "| R-25 | 2027 年品牌窗口错失，改造决策权让渡 | 中 | 高 | 高 | 洲际品牌授权 2027 年到期为唯一解约窗口；若 2026 年四季度前未完成安全评估结论与文化方案确认，则整体决策时点后移至 2028 年并重新评估品牌合约处置 | 产业发展部 |",
]
t = "\n".join(lines)
open(MD, "w", encoding="utf-8").write(t)
L("[MD] 风险表已增 R-23/R-24/R-25")

# ══ ② Excel ══
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
V21 = json.load(open(os.path.join(T, "v21.json"), encoding="utf-8"))
BASE = V21["base"]; SCH = {s["key"]: s for s in V21["schemes"]}
def N(v, d=1): return format(round(v, d), ",.%df" % d)
def P(v): return ("%.2f%%" % (v * 100)) if v is not None else "无可解"
XL = os.path.join(CAL, "总府皇冠改造_可行性研究报告_测算附表_v3.0_2026-11-14.xlsx")
wb = load_workbook(XL)
THIN = Side(style="thin", color="BFBFBF"); BD = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
BOLD = Font(bold=True); HD = PatternFill("solid", fgColor="D9E2F3")
BAD = PatternFill("solid", fgColor="FFC7CE"); OK = PatternFill("solid", fgColor="C6EFCE"); WARN = PatternFill("solid", fgColor="FFEB9C")
def hd(ws, r, hs, widths=None):
    for i, h in enumerate(hs, 1):
        c = ws.cell(row=r, column=i, value=h); c.font = BOLD; c.fill = HD; c.border = BD
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    if widths:
        for i, w in enumerate(widths, 1): ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = ws.cell(row=r+1, column=1)
    return r + 1
def put(ws, r, vs, fm=None, fl=None):
    from openpyxl.styles import Font as _F
    from openpyxl.styles.fills import Fill as _Fi
    for i, v in enumerate(vs, 1):
        c = ws.cell(row=r, column=i, value=v); c.border = BD
        if fm and i <= len(fm) and fm[i-1]: c.number_format = fm[i-1]
        if fl and i <= len(fl) and fl[i-1]:
            o = fl[i-1]
            if isinstance(o, _F): c.font = o
            elif isinstance(o, _Fi): c.fill = o
    return r + 1

# ── 17 文创化溢价情景 ──
if "17 文创化溢价情景" in wb.sheetnames: del wb["17 文创化溢价情景"]
ws = wb.create_sheet("17 文创化溢价情景")
ws["A1"] = "S1 + 文创化改造溢价情景测算（口径与正式稿第九章一致）"; ws["A1"].font = Font(bold=True, size=13)
ws["A2"] = "策展溢价指数 CPI = 本店平均房价 ÷ 同城同档竞品平均房价（竞品基准为 S1 的 750 元档）；非房系数随房价提升幅度的 0.6 倍同步提升；复业后第 13 个月起两年线性到位；内容预算按年连续三年计入现金流"
r = 4
r = put(ws, r, ["【一】三情景结果"]); ws.cell(row=r-1, column=1).font = BOLD
r = hd(ws, r, ["情景", "策展溢价指数", "年内容预算（万元）", "三年合计（万元）", "稳态年营业收入（万元）", "相对改造前 6,774.0 的倍数",
               "绝对净现值（万元）", "相对基线改善（万元）", "增量净现值（万元）", "增量口径内部收益率", "增量口径静态回收期（年）", "集团口径静态回收期（年）"],
        [22, 14, 18, 16, 22, 20, 18, 20, 18, 18, 20, 20])
for lbl, cpi, cb, rev, npv, inc, irr, pb, pbg in [
    ("S1 基线（无文创）", 1.000, 0, 10938.7, -6002.9, 14398.4, "15.61%", 8, 10.15),
    ("保守", 1.100, 320, 12754.5, -3481.9, 16919.4, "16.64%", 7, 9.06),
    ("基准", 1.150, 280, 13711.7, -2124.3, 18277.1, "17.18%", 7, 8.10),
    ("乐观", 1.200, 240, 14701.6, -721.1, 19680.2, "17.73%", 7, 7.33)]:
    imp = round(npv - (-6002.9), 1)
    r = put(ws, r, [lbl, cpi, cb, cb * 3, rev, round(rev / 6774.0, 2), npv, imp, inc, irr, pb, pbg],
            ["General", "0.000", "#,##0", "#,##0", "#,##0.0", "0.00", "#,##0.0", "#,##0.0", "#,##0.0", "General", "0", "0.00"],
            [None, None, None, None, None, None, None, None, None, OK if lbl == "基准" else None, None, None])
r += 1
r = put(ws, r, ["【二】临界值反解"]); ws.cell(row=r-1, column=1).font = BOLD
r = hd(ws, r, ["临界目标", "所需策展溢价指数", "对应平均房价（元）", "说明"], [30, 20, 20, 76])
for a, b, c_, d in [
    ("追平 S1 基线增量净现值", 1.002, 751, "三年 840 万元内容预算的边际成本极低；稀缺的不是钱，而是内容能否兑现"),
    ("追平 S7B 外部奢牌增量净现值", 1.732, 1299, "显著高于成都院子约 800 元实证样本，文创化路径在价格上无法替代外部奢牌"),
    ("绝对净现值转正所需（参考）", 1.35, 1763, "远超五星档现实区间，仅作边界参照，不作方案主张")]:
    r = put(ws, r, [a, b, c_, d], ["General", "0.000", "#,##0", "General"])
r += 1
r = put(ws, r, ["【三】路径比较（与 08 总表同源）"]); ws.cell(row=r-1, column=1).font = BOLD
r = hd(ws, r, ["路径", "改造投资（万元）", "绝对净现值（万元）", "增量净现值（万元）", "增量口径内部收益率", "前提可验证性"],
        [26, 18, 18, 18, 18, 74])
for a, b, c_, d, e, f in [
    ("S1 基线", 21313.6, -6002.9, 14398.4, "15.61%", "—"),
    ("S1 + 文创化（基准）", 21313.6, -2124.3, 18277.1, "17.18%", "可验证：本地有成都院子样本、集团有国堰方法论、成本在可保留节约内"),
    ("S4 洲至奢选", 28190.7, -7351.4, 13049.9, "13.36%", "品牌可配合，但房价上限受限"),
    ("S7B 外部奢牌（上限）", 56850.9, 16916.8, 37318.1, "15.32%", "不可验证：三项前提均无支撑")]:
    r = put(ws, r, [a, b, c_, d, e, f], ["General", "#,##0.0", "#,##0.0", "#,##0.0", "General", "General"],
            [OK if a.startswith("S1 +") else None, None, None, None, None, None])
r += 1
ws.cell(row=r, column=1, value="★ 文创化的价值在于用极小边际投入把项目推向盈亏平衡附近并提升抗周期能力，绝对净现值仍为负，不得作为高回报投资申报；内容预算越低财务指标略好但溢价越难兑现，须以 Kill 判据管理而非压缩预算。").font = BOLD
ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True)
L("[XLS] 17 文创化溢价情景已建")

# ── 18 十五五战略对标与在地文化 ──
if "18 十五五战略对标与在地文化" in wb.sheetnames: del wb["18 十五五战略对标与在地文化"]
ws = wb.create_sheet("18 十五五战略对标与在地文化")
ws["A1"] = "安逸十五五战略对标 · 在地文化植入方案 · KPI 与 Kill 判据"; ws["A1"].font = Font(bold=True, size=13)
r = 3
r = put(ws, r, ["【一】集团十五五三大方向对标"]); ws.cell(row=r-1, column=1).font = BOLD
r = hd(ws, r, ["集团十五五方向", "总府改造中的对应", "支撑位置"], [30, 68, 30])
for a, b, c_ in [
    ("标杆化生活方式酒店并把品牌立起来", "作为「国际五星旗舰」双轨制中的一轨（另一轨为本土自有旗舰新良大酒店），改造质量决定旗舰叙事成立与否", "第五章（九）、第十章（三）"),
    ("一定要做文创化改造而不是简单改造", "母题「总府·街市百年」、四个年度子题、L3 联动层、机制三件套、六项 KPI 与 Kill 判据", "第五章（七）、第九章（九）"),
    ("AI 数字化成为护城河和支柱", "智慧酒店智能控制管理系统列入段二机电成本（品牌无关）；PMS/CRS/数据中台/OTA 双站为集团级动作", "第六章、第十一章"),
    ("五大护城河之「在地文化能力」", "补强第五项护城河；沉淀策展标准作业程序、母题与机构资源库、可授权 IP 三项可输出资产", "第五章（七）"),
    ("资源整合能力（第一护城河）", "「一地一策」母题框架可直接承接地市州划转资产，换城市框架不变、内容重填", "第五章（七）")]:
    r = put(ws, r, [a, b, c_])
r += 1
r = put(ws, r, ["【二】战略时点与内部协同风险"]); ws.cell(row=r-1, column=1).font = BOLD
r = hd(ws, r, ["事项", "事实", "处置"], [26, 78, 44])
for a, b, c_ in [
    ("2027 年品牌窗口", "洲际皇冠假日品牌授权 2027 年到期，每年支付品牌相关费用 900 万元；2027 年为唯一解约与重新定位窗口", "倒排：2027 上半年完成评估结论与品牌方向，2027 内完成合约处置决策，2028 内实施"),
    ("旗舰定位", "总府为集团十五五「国际五星旗舰」双轨制中的一轨，是集团在成都核心商圈唯一国际五星载体", "改造质量与旗舰叙事绑定，第十章（三）已论证"),
    ("春熙路品牌序列冲突", "集团在春熙路及邻近已有多处自有门店（锦著春熙路店、天府广场春熙路店、春熙路太古里店），且存在同址多条目问题（春熙路店猫途鹰 8/41/332 三条仅差标点）", "投资决策前完成商圈品牌序列与客群分层设计，纳入集团商圈分级分类联动课题（R-24）"),
    ("外部价格参照", "峨眉山悦榕庄 2026-08 开业，房价区间 2,700—8,000 元，可作「城市度假」定位价格天花板参照", "联合品牌路径属资产重估，但需更严格的价格带支撑，本报告不予推荐")]:
    r = put(ws, r, [a, b, c_])
r += 1
r = put(ws, r, ["【三】在地文化母题与四个年度子题"]); ws.cell(row=r-1, column=1).font = BOLD
r = hd(ws, r, ["年度子题", "母题落点", "主展形态", "工坊", "研学课"], [16, 52, 34, 34, 32])
for a, b, c_, d, e in [
    ("盐与埠", "官盐店、锦江桥、金河、井盐与老字号茶号米油行", "盐市口城市考古数字展 + 民国街市舆图", "井盐与古法酿造、茶号米油复刻", "城市商业文明与集散贸易"),
    ("影与戏", "智育电影院、上海影人剧团、川剧与当代曲艺", "民国影剧文献展 + 影剧年表", "川剧脸谱绘制、道具与身段", "影剧与城市公共生活"),
    ("街与坊", "春熙路 1924、书报刊业、少城与皇城", "街市变迁影像与文献双线展", "铅活印刷与装帧", "街区形态与城市更新"),
    ("蜀与锦", "蜀锦蜀绣、竹编、漆艺、银花丝；锦官城与丝路起点", "蜀锦工艺与丝路源流展", "蜀绣、竹编、漆艺、银花丝四门手作", "丝路起点与织造技艺")]:
    r = put(ws, r, [a, b, c_, d, e])
r += 1
r = put(ws, r, ["【四】成熟度分级与内容预算"]); ws.cell(row=r-1, column=1).font = BOLD
r = hd(ws, r, ["级别", "判据", "本项目定位"], [16, 60, 72])
for a, b, c_ in [
    ("L1 装饰层", "只换皮", "已具备部分主题概念，无内容机制"),
    ("L2 叙事层", "有统一母题与考据", "改造后可达"),
    ("L3 联动层", "内容日历 + 机构联营 + 付费体验", "★ 本次目标；最低可行内容预算约 180—250 万元每年（国堰口径，对应其 166—236 间房量）"),
    ("L4 共创层", "共同署名与共同所有", "三至五年后观察项，不在本次投资决策范围"),
    ("L5 共生层", "对外输出", "三至五年后观察项")]:
    r = put(ws, r, [a, b, c_], ["General"]*3, [None, None, OK if "L3" in a else None])
r += 1
r = hd(ws, r, ["内容预算口径", "金额（万元）", "说明"], [30, 22, 96])
for a, b, c_ in [
    ("按 402 间同强度折算的 L3 最低可行", "435—605 / 年", "国堰 180—250 万元每年 ÷ 其 166—236 间，按单房强度折算至总府 402 间"),
    ("本报告基准情景采用", "280 / 年", "明显低于同强度口径的保守取值，三年合计 840 万元"),
    ("建议向集团报批", "400 / 年（三年 1,200）", "从可保留项节约 4,538.7 万元中划转，不新增改造投资总额；占用节约额一半以上，为战略价值与财务指标的真实取舍"),
    ("若维持 280 万元每年", "280 / 年", "仅接近 L2 叙事层，存在「省了钱、赔了价」的负循环风险，须以 Kill 判据管理")]:
    r = put(ws, r, [a, b, c_], ["General", "General", "General"], [None, WARN if "建议向集团报批" in a else None, None])
r += 1
r = put(ws, r, ["【五】KPI 与 Kill 判据"]); ws.cell(row=r-1, column=1).font = BOLD
r = hd(ws, r, ["指标", "口径", "目标（复业后 12 个月）", "Kill 判据"], [24, 52, 30, 56])
for a, b, c_, d in [
    ("策展溢价指数", "本店平均房价 ÷ 同城同档竞品平均房价", "≥ 1.15", "低于 1.10 即停止追加内容预算，降回 L2 叙事层"),
    ("导览与工坊参与率", "参加导览或工坊的间夜 ÷ 总间夜", "≥ 35%", "低于 20% 则砍工坊产品线"),
    ("非房收入占比", "（餐饮+工坊+研学+零售+场地+分成）÷ 总营收", "由现状提升至 20%（第二年 30%）", "低于 20% 则非房系数假设须下修并重算第九章"),
    ("客群文化动机占比", "问卷中「为文化或研学而来」", "≥ 40%", "低于 30% 则客群换质未成立，内容方案须重做"),
    ("用户生成内容密度", "带定位的分享 ÷ 月间夜", "≥ 0.8 条每间夜", "低于 0.5 则私域沉淀未成立"),
    ("复购率", "12 个月内二次入住 ÷ 总客", "≥ 20%", "两年内未形成标准作业程序与母题库，则「一地一策」命题在本项目不成立")]:
    r = put(ws, r, [a, b, c_, d])
L("[XLS] 18 十五五战略对标与在地文化已建")

# ── 01 大数对照表补录 ──
ws = wb["01 报告大数对照表"]
r = ws.max_row + 2
ws.cell(row=r, column=1, value="【v3.0 增补：战略维度与在地文化】").font = BOLD
r += 1
r = hd(ws, r, ["报告位置", "正文大数", "数值", "来源表", "口径说明"], [30, 40, 22, 26, 58])
for row in [
    ("第十章（三）", "总府在集团十五五中的定位", "国际五星旗舰（双轨制一轨）", "18 十五五战略对标", "另一轨为本土自有旗舰新良大酒店"),
    ("第十章（三）", "洲际品牌授权到期", "2027 年到期，每年 900 万元品牌费", "18 十五五战略对标", "唯一解约与重新定位窗口"),
    ("第二章（八）", "成都院子酒店经营数据", "9 年｜OCC 约 80%｜ADR 接近 800 元｜86 间", "18 十五五战略对标", "文创化路径唯一可得的长期本地样本"),
    ("第五章（七）", "母题与年度子题", "总府·街市百年｜4 个子题", "18 十五五战略对标", "盐与埠／影与戏／街与坊／蜀与锦"),
    ("第五章（七）", "成熟度目标与内容预算", "L3 联动层｜建议 400 万元/年×3 年", "18 十五五战略对标", "从可保留项节约 4,538.7 万中划转，不新增改造投资"),
    ("第九章（九）", "S1+文创 基准情景年营收", "13,711.7 万元（改造前的 2.02 倍）", "17 文创化溢价情景", "策展溢价指数 1.15、年内容预算 280 万"),
    ("第九章（九）", "S1+文创 增量内部收益率", "17.18%（基线 15.61%）", "17 文创化溢价情景", "增量回收期 7 年"),
    ("第九章（九）", "追平基线所需 CPI", "1.002（平均房价 751 元）", "17 文创化溢价情景", "边际成本极低，稀缺的是内容兑现"),
    ("第九章（九）", "追平 S7B 所需 CPI", "1.732（平均房价 1,299 元）", "17 文创化溢价情景", "文创化无法替代外部奢牌价格带"),
    ("第十一章", "新增风险", "R-23 / R-24 / R-25", "11 风险分析", "文化溢价不兑现／商圈序列冲突／2027 窗口错失"),
]:
    r = put(ws, r, list(row))
L("[XLS] 01 大数对照表已补录")
wb.save(XL)
L("XLSX %.1f KB | %d sheets" % (os.path.getsize(XL) / 1024, len(wb.sheetnames)))

# ══ ③ 公文 Word 重出（先写 MD 后出 Word）══
D = os.path.join(KB, "_calc")
src = open(os.path.join(D, "v17_docx.py"), encoding="utf-8").read()
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.md", "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.docx", "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.docx")
open(os.path.join(D, "v17_docx_v3.py"), "w", encoding="utf-8").write(src)
PY = r"C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe"
subprocess.run([PY, os.path.join(D, "v17_docx_v3.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
for l in open(os.path.join(T, "v17.log"), encoding="utf-8", errors="replace").read().split("\n"):
    if l.strip(): L(l.rstrip())

# ══ ④ 终检 ══
from docx import Document
DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.docx")
t = open(MD, encoding="utf-8").read()
d = Document(DOCX)
paras = [p.text for p in d.paragraphs]
alltext = "\n".join(paras) + "\n" + "\n".join(c.text for tb in d.tables for r in tb.rows for c in r.cells)
blank = sum(1 for tb in d.tables for r in tb.rows for c in r.cells if c.text.strip() in ("", "\u2014", "-", "\uff0f", "/"))
L("=== 终检 ===")
L("%.1f KB | 段落 %d | 表格 %d | 空白格 %d | 节 %d" % (os.path.getsize(DOCX) / 1024, len(d.paragraphs), len(d.tables), blank, len(d.sections)))
for si, s in enumerate(d.sections):
    L("   S%d %s %.0fx%.0f 页码域 %d" % (si, "横" if s.page_width > s.page_height else "纵",
        s.page_width.cm, s.page_height.cm, s.footer._element.xml.count('w:instr="PAGE"')))
EMO = r"[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\u24C2\u2B55]"
L("emoji:", len(re.findall(EMO, alltext)))
KEYS = ["13,711.7", "2.02 倍", "17.18%", "1.002", "1.732", "1,299", "总府·街市百年", "国际五星旗舰", "2027 年",
        "900 万元", "成都院子", "800 元", "4,538.7", "L3", "R-23", "R-24", "R-25", "四川", "1,732",
        "10,720", "2,915", "31,727.6", "20,401.3", "14,398.4", "15.61%", "6,774.0", "11.33%", "16,916.8"]
miss = [k for k in KEYS if k not in alltext]
L("关键值缺失:", miss if miss else "无（%d 项全中）" % len(KEYS))
for o in ("唯一全判据成立", "唯一在全部判据上成立的方案是 S7B", "唯一同时满足"):
    if o in alltext: L("   ⚠ 旧判据残留: %s" % o)
for ab in ("ADR", "RevPAR", "CAPEX", "NPV", "IRR", "GOP"):
    n = len(re.findall(r"\b%s\b" % ab, alltext))
    if n: L("   ⚠ 英文缩写 %s ×%d" % (ab, n))
m = re.search(r"^## 目录\n", t, re.M)
ls = t[m.end():].split("\n")
start = next((i for i, l in enumerate(ls) if l.startswith("## ")), None)
toc = [re.sub(r"^\d+\. ", "", l).strip() for l in ls[:start] if re.match(r"^\d+\. ", l)]
bod = [l[3:].strip() for l in ls[start:] if l.startswith("## ")]
L("目录↔正文:", toc == bod, "| 目录", len(toc), "正文", len(bod))
if toc != bod:
    for a, b in zip(toc, bod):
        if a != b: L("   差异:", a, "||", b)
L("交付:", [os.path.basename(x) for x in glob.glob(os.path.join(REP, "总府皇冠改造_可行性研究报告*"))],
  [os.path.basename(x) for x in glob.glob(os.path.join(CAL, "总府皇冠改造_可行性研究报告*"))])
L("桌面残留:", len(glob.glob(r"C:\Users\ericz\Desktop\*总府*")))
L("DONE")
