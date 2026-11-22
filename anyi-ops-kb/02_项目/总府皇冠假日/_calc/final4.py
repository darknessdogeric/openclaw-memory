# -*- coding: utf-8 -*-
"""v3.0 收尾：MD 改名 / 残留口径修正 / 破折号填充 / Excel 口径重建 / 数据源清单补录"""
import io, os, sys, re, json, glob, shutil
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "final4.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
def esc(s): return str(s).encode("unicode_escape").decode("ascii")

# ══════════ 1. MD 修正 ══════════
MD_OLD = os.path.join(KB, "总府皇冠改造_立项报告_集团汇报件_v2.0_2026-11-13.md")
MD = os.path.join(KB, "总府皇冠改造_立项报告_集团汇报件_v3.0_2026-11-14.md")
t = open(MD_OLD, encoding="utf-8").read()

# 1a 第四章残留口径句
t2, n = re.subn(
    r">\*\*须同时注意：按国资委 10 年口径复核.*?结论部分第 4 条。\*\*",
    ">**须同时注意：内部收益率须按三套口径分别列示，详见第九章第四节；全口径下四个方向净现值均为负，成因与应对见结论部分第六条。**",
    t)
L("第四章残留句替换:", n); t = t2

# 1b 破折号空位填实
FILLS = [
 ("| — |  集团可比口径内部收益率仅 2.57% |",
  "| 沿用皇冠品牌可免去品牌重新谈判与系统重建成本 |  集团可比口径内部收益率仅 2.57% |"),
 ("| — |  集团可比口径内部收益率 8.68%，仍低于集团规划值 17.00% |",
  "| 六个方向情景中唯一完整落实规划“国际五星全服务型标杆”五板块的方案 |  集团可比口径内部收益率 8.68%，仍低于集团规划值 17.00% |"),
 ("| — |  成都同城已有洲至奢选（棕榈泉 336 间）、丽晶（已签约 2029Q3）、2026 年新开兰博基尼与丽笙精选，一城一店约束下不可行 |",
  "| 通过减房使客房套内 40 ㎡ 以上，房间标准在四个方向中无短板 |  成都同城已有洲至奢选（棕榈泉 336 间）、丽晶（已签约 2029Q3）、2026 年新开兰博基尼与丽笙精选，一城一店约束下不可行 |"),
]
for a, b in FILLS:
    if a in t:
        t = t.replace(a, b); L("[FILL]", esc(a[:30]))
    else:
        L("[MISS-FILL]", esc(a[:30]))

# 1c 目录重建
m = re.search(r"^## 目录\n", t, re.M)
if m:
    lines = t[m.end():].split("\n")
    h2s = []
    for l in lines:
        if l.startswith("## ") and l[3:].strip() != "目录":
            h2s.append(l[3:].strip())
    idx = 0
    for i, l in enumerate(lines):
        if l.strip() == "" and i > 0 and any(x.strip() for x in lines[:i]):
            idx = i; break
    toc = "\n".join("%d. %s" % (i + 1, h) for i, h in enumerate(h2s))
    t = t[:m.end()] + toc + "\n\n" + "\n".join(lines[idx + 1:])
    L("目录重建:", len(h2s), "条")

open(MD, "w", encoding="utf-8").write(t)
os.remove(MD_OLD)
L("MD -> v3.0, bytes:", len(t.encode("utf-8")))

# 残留复查（白名单为"说明不存在10年门槛"的正确表述）
for k in ("国资委 10 年", "10 年门槛", "10年门槛", "10 年国资", "10年国资"):
    c = t.count(k)
    if c: L("  [残留-待核]", k, c)

# ══════════ 2. 出 Word ══════════
sys.path.insert(0, r"D:\B166ER-openclaw\workspace\.tmp")
from md2docx_cn import convert
out = os.path.join(REP, "总府皇冠改造_立项报告_集团汇报件_v3.0_2026-11-14.docx")
convert(MD, out)
L("DOCX %.1f KB" % (os.path.getsize(out)/1024))
from docx import Document
d = Document(out)
n = 0
for ti, tb in enumerate(d.tables, 1):
    for ri, row in enumerate(tb.rows):
        for ci, cell in enumerate(row.cells):
            if cell.text.strip() in ("", "\u2014", "-", "\uff0f", "/"):
                n += 1
                L("  BLANK 表%d 行%d 列%d : %s" % (ti, ri, ci, " || ".join(esc(c.text.strip()[:26]) for c in row.cells)))
L("表格 %d，空白格 %d" % (len(d.tables), n))

# ══════════ 3. Excel 口径重建 ══════════
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
XL_OLD = os.path.join(CAL, "总府皇冠改造_立项方案_细项概算表_v2.0_2026-11-13.xlsx")
XL = os.path.join(CAL, "总府皇冠改造_立项方案_细项概算表_v3.0_2026-11-14.xlsx")
V8 = json.load(open(os.path.join(T, "v8.json"), encoding="utf-8"))
DV = V8["dirs"]
wb = load_workbook(XL_OLD)
THIN = Side(style="thin", color="BFBFBF"); BD = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
B = Font(bold=True); T13 = Font(bold=True, size=13)
OK = PatternFill("solid", fgColor="C6EFCE"); BAD = PatternFill("solid", fgColor="FFC7CE")
HD = PatternFill("solid", fgColor="D9E2F3")
def hd(ws, r, hs, ws_=None):
    for i, h in enumerate(hs, 1):
        c = ws.cell(row=r, column=i, value=h); c.font = B; c.fill = HD; c.border = BD
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    if ws_:
        for i, w in enumerate(ws_, 1): ws.column_dimensions[get_column_letter(i)].width = w
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

# 3a 修正 01 口径说明
ws = wb["01 口径说明"]
for r in range(1, ws.max_row + 1):
    k = ws.cell(row=r, column=1).value
    if k == "国资考核口径":
        ws.cell(row=r, column=1, value="集团考核口径")
        ws.cell(row=r, column=2, value="《集团改革发展情况汇报材料》投资原则：回收期控制在 5-8 年。经核查国家层面无“回收期不超过 10 年”规定，亦无统一内部收益率数字（《中央企业投资监督管理办法》国资委令第 34 号：负面清单外由企业自主决策；财务基准收益率由投资者确定）")
        L("[XLS] 01 口径说明已改")
    if k == "财务评价口径":
        ws.cell(row=r, column=2, value="20 年全周期现金流（含建设期停业现金流、复业爬坡、品牌费用与激励费、家具装置设备储备、复业后两年全渠道声誉折损）。本表另设“三重口径校准与集团 715 定稿对照”工作表，同时列示全口径、增量口径、集团可比口径")
    if k == "折现率" or k == "国资考核口径":
        pass

# 3b 修正 02 方向总览
ws = wb["02 方向总览对比"]
ws["A1"] = "六个方案改造投资与回报总览（三重口径）"
ws["A2"] = "改造投资单位：万元；单间＝改造投资÷改造房量；判定基准＝集团《改革发展情况汇报材料》投资原则“回收期控制在 5-8 年”"
hdrs = ["方案","改造房量（间）","改造投资（万元）","单间（万元）","公共区域情景",
        "稳态年营业收入（万元）","每间可售房收入（元）","业主年度经营利润（万元）",
        "全口径内部收益率","全口径净现值（万元）","全口径静态回收期（年）",
        "增量口径内部收益率","增量口径净现值（万元）","增量口径静态回收期（年）",
        "集团可比口径内部收益率","集团可比口径静态回收期（年）","是否落入集团 5-8 年区间"]
for i, h in enumerate(hdrs, 1):
    c = ws.cell(row=4, column=i, value=h); c.font = B; c.fill = HD; c.border = BD
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
for i, w in enumerate([26,12,15,12,22,18,16,18,14,16,15,16,16,16,16,16,16], 1):
    ws.column_dimensions[get_column_letter(i)].width = w
LB = {"D1":"一 沿用皇冠·不减房","D1X":"一 沿用皇冠·不减房（公区拆除重做）","D2":"二 沿用皇冠·3改2",
      "D3":"三 换奢牌·不减房（公区拆除重做）","D3R":"三 换奢牌·不减房（公区保留石材）","D4":"四 换奢牌·3改2"}
r = 5
for k in ("D1", "D1X", "D2", "D3", "D3R", "D4"):
    x = DV[k]
    pbi = x.get("pb_inc")
    inrange = (pbi is not None and 5 <= pbi <= 8)
    r = put(ws, r, [LB[k], x["n_rooms"] if "n_rooms" in x else (402 if k in ("D1","D1X","D3","D3R") else 268),
                    x["capex"], x["per_key"], "", x["steady_rev"], "", x["owner_gop"],
                    round(x["irr_full"]*100,2) if x["irr_full"] is not None else "无可解内部收益率",
                    x["npv_full"], x["pb_full"] or "20年内未回收",
                    round(x["irr_inc"]*100,2) if x["irr_inc"] is not None else "无可解内部收益率",
                    x["npv_inc"], pbi or "未回收",
                    round(x["irr_grp"]*100,2) if x["irr_grp"] is not None else "无可解内部收益率",
                    x["pb_grp"] or "未回收",
                    "是" if inrange else "否"],
            ["General","0","#,##0","0.00","General","#,##0","General","#,##0","0.00","#,##0","General",
             "0.00","#,##0","General","0.00","General","General"],
            [None]*16 + [None if inrange else BAD])
# 从原表补公共区域情景与每间可售房收入
src = wb["02 方向总览对比"]
for rr in range(5, 5 + 6):
    sc = src.cell(row=rr, column=5).value
    rv = src.cell(row=rr, column=7).value
    if sc: ws.cell(row=rr, column=5, value=sc)
    if rv: ws.cell(row=rr, column=7, value=rv)
ws.cell(row=r+1, column=1, value="结论：按集团“回收期 5-8 年”口径，仅「一 沿用皇冠·不减房」落入区间（增量口径回收期 7 年、增量口径内部收益率 19.93%）；换奢牌方向回收期 10 年超出区间且投资超集团预留额度。").font = B
L("[XLS] 02 方向总览已改为三重口径")

# 3c 新增工作表：三重口径校准与集团 715 定稿对照
if "02b 三重口径校准与集团对照" in wb.sheetnames:
    del wb["02b 三重口径校准与集团对照"]
ws = wb.create_sheet("02b 三重口径校准与集团对照", 2)
ws["A1"] = "三重口径校准与集团《改革发展情况汇报材料》715 定稿对照"; ws["A1"].font = T13
ws["A2"] = "口径一 全口径（含存量亏损与停业净流出）｜口径二 增量口径（相对“不改造”反事实，改造前年均经营现金流 −1,924 万元）｜口径三 集团可比口径（改造后现金流 20 年等额年金、停业支出单列不进内部收益率）"
r = 4
r = hd(ws, r, ["方向","改造投资（万元）","改造房量（间）","单间（万元）","全口径内部收益率","全口径净现值（万元）",
               "增量口径内部收益率","增量口径净现值（万元）","增量口径静态回收期（年）","增量口径（反事实劣化 5%/年）内部收益率",
               "增量口径静态回收期（年）","集团可比口径内部收益率","集团可比口径净现值（万元）","集团可比口径静态回收期（年）",
               "是否落入集团 5-8 年区间","与集团 17.00% 比较（百分点）"],
        [26,15,13,12,14,16,14,16,17,20,17,16,17,17,17,20])
for k in ("D1","D2","D3","D3R","D4"):
    x = DV[k]
    pbi = x.get("pb_inc")
    inr = (pbi is not None and 5 <= pbi <= 8)
    diff = (x["irr_inc"] - 0.17) * 100 if x["irr_inc"] is not None else None
    r = put(ws, r, [LB[k], x["capex"], 402 if k in ("D1","D3","D3R") else 268, x["per_key"],
                    round(x["irr_full"]*100,2) if x["irr_full"] is not None else "无可解内部收益率",
                    x["npv_full"], round(x["irr_inc"]*100,2) if x["irr_inc"] is not None else "无可解内部收益率",
                    x["npv_inc"], pbi or "未回收",
                    round(x["irr_inc_decay"]*100,2) if x["irr_inc_decay"] is not None else "无可解内部收益率",
                    x["pb_inc_decay"] or "未回收",
                    round(x["irr_grp"]*100,2) if x["irr_grp"] is not None else "无可解内部收益率",
                    x["npv_grp"], x["pb_grp"] or "未回收",
                    "是" if inr else "否", ("%+.2f" % diff) if diff is not None else "—"],
            ["General","#,##0","0","0.00","0.00","#,##0","0.00","#,##0","General","0.00","General","0.00","#,##0","General","General","0.00"],
            [None]*14 + [None if inr else BAD, None])
r += 1
r = put(ws, r, ["集团 715 定稿对总府的规划值：改造投资 18,000 万元｜改造面积 44,600 ㎡｜客房 430 间｜回收期 5.6 年｜内部收益率 17.00%｜定位“国际五星全服务型标杆”｜列入第二批（2027—2029 年）"])
ws.cell(row=r-1, column=1).font = B
r += 1
r = put(ws, r, ["反推：按 20 年等额年金口径，集团 17.00% 对应年现金流约 3,198 万元；5.6 年回收期对应约 3,214 万元。两者自洽，可确认集团采用“改造后年经营现金流 ÷ 改造投资”的简化口径。"])
r += 1
r = put(ws, r, ["本次测算方向一稳态业主经营利润 2,028 万元/年，较集团规划隐含值差 1,170 万元/年，须逐项对账：房量口径（430 对实测在售 402）、房价假设、费用扣减口径、停业期处理。"])
ws.cell(row=r-1, column=1).font = B
r += 1
for line in [
 "【资金盘子影响】若总府走换奢牌方向（27,919—32,061 万元），较集团预留 1.8 亿元超支 9,919—14,061 万元：",
 "　第二批合计由 2.8 亿元升至 3.79—4.21 亿元；六家改造总盘子由 4.08 亿元升至 5.07—5.49 亿元；",
 "　“十五五”刚性资金需求由 7.18—8.18 亿元升至 8.18—9.22 亿元，须集团层面重新平衡六家排序、节奏与筹资。",
 "　反之方向一 14,401 万元，比集团规划值低 3,599 万元，且回收期 7 年落入集团 5-8 年区间，吻合度最高。",
]:
    r = put(ws, r, [line])
r += 1
r = put(ws, r, ["【门槛依据更正】国家层面不存在“回收期不超过 10 年”规定，亦无统一内部收益率数字："])
ws.cell(row=r-1, column=1).font = B
for line in [
 "　《中央企业投资监督管理办法》（国资委令第 34 号，2017-01-07 施行）第七条：投资管理制度由企业制定、董事会审议通过后报国资委；",
 "　第九条：国资委发布负面清单并设定禁止类与特别监管类，负面清单之外由中央企业自主决策，企业须另定更严格版本。",
 "　《建设项目经济评价方法与参数》（第三版）：社会折现率 8%；投资者财务基准收益率由投资者自行确定。",
 "　行业通行参考：酒店项目税后内部收益率 8%—10%、含建设期静态回收期 6—9 年。",
 "　集团口径（《集团改革发展情况汇报材料》投资原则）：回收期控制在 5-8 年；集团六家实测回收期 3.6—7.2 年、内部收益率 6.6%—24.6%。",
]:
    r = put(ws, r, [line])
L("[XLS] 新增 02b 三重口径校准工作表")

# 3d 12 参数与假设 补口径行
ws = wb["12 参数与假设"]
r = ws.max_row + 2
ws.cell(row=r, column=1, value="【口径参数】").font = B; r += 1
for k, v, s in [
 ("集团考核口径","回收期 5-8 年","《集团改革发展情况汇报材料》第四章（一）投资原则"),
 ("集团对总府规划值","18,000 万元／回收期 5.6 年／内部收益率 17.00%","同上，专栏 6 六大核心酒店改造投资效益概览"),
 ("集团六家实测区间","回收期 3.6—7.2 年；内部收益率 6.6%—24.6%","同上，附件 6 未计算租金的五家酒店"),
 ("改造前年均经营现金流","−1,924 万元（业主口径）","国际联号口径测算方法与总府重测 v1.0（2026-11-03），USALI 实测"),
 ("增量口径反事实劣化情景","−5%/年","用于检验不改造情景随设施老化与品牌失分恶化的敏感性"),
 ("行业通行参考","税后内部收益率 8%—10%；含建设期静态回收期 6—9 年","酒店项目可研行业通行基准"),
 ("社会折现率","8%","《建设项目经济评价方法与参数》（第三版）"),
 ("国家层面门槛","无统一内部收益率数字、无回收期年限规定","《中央企业投资监督管理办法》国资委令第 34 号第七条、第九条"),
]:
    r = put(ws, r, [k, v, s])
    ws.cell(row=r-1, column=3).alignment = Alignment(wrap_text=True, vertical="top")
L("[XLS] 12 参数与假设 已补口径参数")

# 3e 13 数据源清单 补录
ws = wb["13 数据源清单"]
r = ws.max_row + 2
ws.cell(row=r, column=1, value="【口径核查补充】").font = B; r += 1
for row in [
 ("国资委投资监管依据","《中央企业投资监督管理办法》（国资委令第 34 号，2017-01-07 施行）：第七条投资管理制度由企业制定、董事会审议通过后报国资委；第九条国资委发布负面清单并设定禁止类与特别监管类，负面清单之外由中央企业自主决策","中华人民共和国司法部 https://www.moj.gov.cn/pub/sfbgw/flfggz/flfggzbmgz/201702/t20170228_145963.html ；成都市国资委 https://gzw.chengdu.gov.cn/cdgzw/c107973/2018-10/25/content_6b93fb02df614dc7880aef1498fbb18a.shtml","2026-11-14 复核","口径二（不存在统一内部收益率数字与回收期年限）"),
 ("财务评价通行参数","《建设项目经济评价方法与参数》（第三版）：社会折现率 8%；投资者财务基准收益率由投资者自行确定","百度百科《社会折现率》；MBA 智库《财务基准收益率》","2026-11-14 复核","折现率 8% 的规范来源"),
 ("集团内部考核口径","《集团改革发展情况汇报材料》（715 定稿）第四章（一）投资原则：投入产出可控，回收期控制在 5-8 年；专栏 6：总府 18,000 万元／44,600 ㎡／430 间／回收期 5.6 年／内部收益率 17.00%；附件 6：六家实测回收期 3.6—7.2 年、内部收益率 6.6%—24.6%，四川宾馆含租金 10.9 年／4.06%；营业现金毛流量＝净利润＋折旧摊销","集团内部文件 715 定稿（01_集团文件\\_report_materials\\715定稿.txt）","2026-11-14 复核","判定基准改为集团 5-8 年；营业现金毛流量定义已确定"),
 ("行业通行参考","酒店项目税后内部收益率 8%—10%、含建设期静态回收期 6—9 年","中撰企业投资咨询《酒店项目可行性报告结论》 https://www.cniplan.com/news/detail/jiudian-keyan-jielun.html","2026-11-14 复核","行业对照基准"),
]:
    r = put(ws, r, list(row))
    for cc in (2,3): ws.cell(row=r-1, column=cc).alignment = Alignment(wrap_text=True, vertical="top")
L("[XLS] 13 数据源清单 已补口径核查来源")

wb.save(XL)
L("XLSX v3.0 %.1f KB | %d sheets" % (os.path.getsize(XL)/1024, len(wb.sheetnames)))
os.remove(XL_OLD)
L("removed xlsx v2.0")
L("DONE")
