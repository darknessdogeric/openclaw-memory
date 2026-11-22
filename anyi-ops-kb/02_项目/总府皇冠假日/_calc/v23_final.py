# -*- coding: utf-8 -*-
"""v23 修正：动态定位比选结论块与风险表末行；重建 Excel 附表 v3.0；出 Word v3.0；终检"""
import io, os, sys, re, json, glob, shutil
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v23.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
sys.path.insert(0, os.path.join(KB, "_calc"))
from v22_text import CH5_NEW6

MD = os.path.join(KB, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
t = open(MD, encoding="utf-8").read()

# ① 比选结论：动态定位
m = re.search(r"\*\*比选结论[：:]?\*\*.*?(?=\n### （六）)", t, re.S)
if m:
    t = t[:m.start()] + CH5_NEW6.rstrip() + "\n" + t[m.end():]
    L("[FIX] 比选结论已替换")
else:
    L("[MISS] 比选结论")
    for i, l in enumerate(t.split("\n"), 1):
        if "比选结论" in l:
            L("   实际 L%d | %s" % (i, l[:120]))

# ② 风险表末行动态追加
lines = t.split("\n")
idx = None
for i in range(len(lines) - 1, -1, -1):
    if re.match(r"^\|\s*R-\d+\s*\|", lines[i]):
        idx = i; break
if idx is not None:
    RISK_NEW = ("| R-19 | 改造后收入未达预期（价格带低于假设或出租率不及预期） | 高 | 高 | 高 | 分档定价下 S4 与 S1 的收入敏感性差异达 1.28 倍（14,009.8 对 10,938.7 万元），须在投资决策前完成品牌方定价意见验证 | 产业发展部 |",
                "| R-20 | 顶级设计型价格带无法在总府位置兑现 | 中 | 高 | 高 | 以品牌方定价意见与可比第三方成交数据双重验证；不能验证则该路径不成立，退回 S1 | 产业发展部 |")
    lines.insert(idx + 1, RISK_NEW[0])
    lines.insert(idx + 2, RISK_NEW[1])
    t = "\n".join(lines)
    L("[FIX] 风险表末行 L%d 已追加 R-19/R-20" % (idx + 1))
else:
    L("[MISS] 风险表 R 行")

open(MD, "w", encoding="utf-8").write(t)
L("MD bytes:", len(t.encode("utf-8")))

# ══════════ Excel 附表 v3.0 ══════════
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
V21 = json.load(open(os.path.join(T, "v21.json"), encoding="utf-8"))
BASE = V21["base"]; SCH = {s["key"]: s for s in V21["schemes"]}; TIER = V21["tier"]
OLD = os.path.join(CAL, "总府皇冠改造_可行性研究报告_测算附表_v2.0_2026-11-14.xlsx")
NEW = os.path.join(CAL, "总府皇冠改造_可行性研究报告_测算附表_v3.0_2026-11-14.xlsx")
wb = load_workbook(OLD)
THIN = Side(style="thin", color="BFBFBF"); BD = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
BOLD = Font(bold=True); T13 = Font(bold=True, size=13)
BAD = PatternFill("solid", fgColor="FFC7CE"); OK = PatternFill("solid", fgColor="C6EFCE"); HD = PatternFill("solid", fgColor="D9E2F3")
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
def N(v, d=1): return format(round(v, d), ",.%df" % d)
def P(v): return ("%.2f%%" % (v * 100)) if v is not None else "无可解内部收益率"

# 新增 15 分档定价与市场层级
if "15 分档定价与市场层级" in wb.sheetnames:
    del wb["15 分档定价与市场层级"]
ws = wb.create_sheet("15 分档定价与市场层级")
ws["A1"] = "分档定价体系与七级市场层级数据"; ws["A1"].font = T13
ws["A2"] = "定价按品牌档次取值；市场数据自中国→西南→川渝→四川→成都→春熙路→成都国际联号五星及奢华逐层收窄"
r = 4
r = put(ws, r, ["【一】改造前基线（实测，不改造）"]); ws.cell(row=r-1, column=1).font = BOLD
r = hd(ws, r, ["指标","数值","单位","来源"], [26, 18, 12, 76])
for k, v, u, s in [
 ("在售房量", BASE["rooms"], "间", "工程部《房间分布表》"),
 ("平均房价", BASE["adr"], "元/间夜", "2026-09 实测（24 个月区间内最低点）"),
 ("出租率", round(BASE["occ"] * 100, 2), "%", "24 个月实测"),
 ("客房年收入", round(BASE["rooms_rev"], 1), "万元", "402 × 365 × 70.78% × 363.99"),
 ("总营业收入", round(BASE["total_rev"], 1), "万元", "近 24 个月月均 564.5 万元年化"),
 ("业主经营现金流", BASE["owner_cf"], "万元/年", "业主口径实测（负值，即持续失血）"),
 ("非房/客房收入比", round(BASE["nonroom_ratio"], 3), "倍", "由上两项推出"),
]:
    r = put(ws, r, [k, v, u, s], ["General", "#,##0.00", "General", "General"])
r += 1
r = put(ws, r, ["【二】分档定价体系（本次更正核心）"]); ws.cell(row=r-1, column=1).font = BOLD
r = hd(ws, r, ["档次","品牌","取值（元/间/晚）","依据"], [22, 30, 22, 84])
for br, t_ in TIER.items():
    r = put(ws, r, [t_["tier"], br, "／".join(str(int(x)) for x in t_["adr"]), t_["adr_note"]],
            ["General", "General", "General", "General"])
r += 1
r = put(ws, r, ["【三】成都核心商圈在营与在建项目实际房价带（2026 实测）"]); ws.cell(row=r-1, column=1).font = BOLD
r = hd(ws, r, ["项目","品牌","房量","状态与时间","房价带（元/间/晚）"], [24, 26, 24, 34, 26])
for row in [
 ("成都居舍酒店","居舍（太古酒店）","142 间（100 客房+42 服务式公寓）","2015 开业；2025-10 由博舍更名居舍","2,000—3,000"),
 ("成都尼依格罗酒店","尼依格罗（九龙仓）","238 间，40—200 ㎡","2015 开业","1,180—1,800"),
 ("成都瑞吉酒店","瑞吉（凯悦）","—","在营","1,500—2,000"),
 ("成都华尔道夫酒店","华尔道夫（希尔顿）","289 间","2017-07 开业","1,400—1,800"),
 ("成都群光君悦酒店","君悦（凯悦）","390 间","2016 开业，2026 十周年","核心区五星"),
 ("成都洲至奢选酒店","洲至奢选（洲际）","335 间","2026 开业（原费尔蒙）","约 900 起（$127）"),
 ("成都高新丽笙精选酒店","丽笙精选（锦江丽笙）","178 间","2026-06-16 开业，西南首家","奢华档"),
 ("成都托尼洛·兰博基尼酒店","托尼洛·兰博基尼","168 间，49 ㎡ 起","2026-03-28 开业，西南首家，总投约 24 亿元","顶级"),
 ("成都丽晶酒店","丽晶（洲际）","180 间全大户型","2026-07-15 签约，计划 2029Q3 开业","顶奢"),
]:
    r = put(ws, r, list(row))
r += 1
r = put(ws, r, ["【四】七级市场层级数据"]); ws.cell(row=r-1, column=1).font = BOLD
r = hd(ws, r, ["层级","关键数据","来源"], [20, 78, 44])
for a, b, c in [
 ("中国","全国酒店 40.48 万家／客房 1,979 万间（2026-06）；分档次客房占比 经济 54.46%／中档 22.48%／高档 15.40%／豪华 7.65%；连锁化率 41.80%→42.5%；2026H1 全国 ADR 292 元／OCC 73.8%／RevPAR 215.5 元；RevPAR 不足 200 元的存量酒店占比超 40%","《2026 中国酒店市场发展报告》《2026 中国酒店投资白皮书》"),
 ("中国","新增供给中来自老旧物业翻新占 75%—80%；2026Q2 翻新与品牌转换项目 265 个／45,733 间，品牌转换占 92%；存量改造市场规模破 4,500 亿元；房龄超 8 年酒店逾 11 万家，未来三年 73.2 万间客房进入 15 年更新周期","《2026 中国酒店投资白皮书》"),
 ("中国","⭐ 改造价格三档：轻改 1.5—2 万元/间、中改 2—4 万元/间、重改 5 万元/间（单间造价校验基准）","《2026 中国酒店投资白皮书》"),
 ("中国","单体酒店 2026H1 接待人次 +18% 但营收 −4.7%、房价跌超 20%；连锁单房收益溢价 18%—25%、会员复购 35% 对 15%；成都每年 15%—18% 单体换手，约一半关门或改长租","《2026 中国酒店规模》"),
 ("西南","西南区域酒店经营毛利已出现五年来的首次下滑","浩华《2026 中国酒店投资展望》（经《2026 中国酒店市场发展报告》引用）"),
 ("川渝","成都全市酒店客房约 36.2 万间（另口径 2025 年 9,615 家／47.9 万间）；重庆 47 万间、年均增速 7.9%；重庆五大国际集团 37 品牌 97 家（77 开业／19 在建）；重庆 2024 五星 ADR 736.66 元、RevPAR 548.87 元","《成都酒店行业分析》《重庆酒店行业分析》《新店扎堆、收益分化，成渝商圈酒店进入残酷存量博弈》"),
 ("四川","2026 国庆全省 908 家 A 级景区接待 4,602.96 万人次（+0.85%）、旅游花费 340.87 亿元；2026 春节前六天累计超 4,200 万人次","国际在线四川／四川经济日报／四川省文旅厅"),
 ("成都","2026Q1 入境客源同比 +100%；2026H1 新开中档以上客房约 1.1 万间；在建及筹建 127 个／约 28 万间客房，规模全国第一","《2026 中国酒店市场发展报告》《过于热闹的成都酒店，还有押注的必要吗？》"),
 ("成都","2025 年高端及中高端平均 OCC 67.5%（+1.3pct），但 RevPAR 仅恢复至 2019 年同期 103%、增幅由双位数降至 3.8%；核心商圈甲级商业体内优质酒店物业资本化率压至 4.5%—5%","STR／戴德梁行（经《2026 中国酒店市场发展报告》引用）"),
 ("春熙路","时尚活力区 5.02 平方公里、5 街道 18 社区、一核两轴三区；春熙路至太古里约 1.5 平方公里 134 家酒店，超高端及以上仅 3 家（居舍、君悦、尼依格罗）；以全市 0.34% 土地面积承载 23% 高端酒店签约量","成都市人民政府《春熙路时尚活力区》；Directrix 准聚监测（经《2026 中国酒店市场发展报告》引用）；澎润洞察"),
]:
    r = put(ws, r, [a, b, c])
wb.save(NEW)
L("XLSX v3.0 %.1f KB | %d sheets" % (os.path.getsize(NEW)/1024, len(wb.sheetnames)))
os.remove(OLD); L("removed 附表 v2.0")

# 02 总览表：改为三重口径 + 收入列
ws = wb["02 方向总览对比"]
ws["A1"] = "九个方案完整造价与回报总表（三段式 × 分档定价）"
ws["A2"] = "单位：万元。段二机电水电强弱电与品牌无关；判定基准：改造后年收入须高于改造前 6,774.0 万元"
hr = None
for rr in range(1, 8):
    if ws.cell(row=rr, column=1).value == "方案":
        hr = rr; break
hdrs = ["方案","品牌标准","公区做法","房量做法","房量（间）","停业月数","段一 停业损失","段二 机电水电强弱电","段三 装修改造",
        "改造投资","项目总资金需求","平均房价（元）","改造后年营业收入","改造前基线","收入增量","收入倍数",
        "全口径内部收益率","全口径净现值","全口径静态回收期","集团口径内部收益率","集团口径静态回收期（年）","增量口径内部收益率","增量口径静态回收期（年）","可行性"]
for i, h in enumerate(hdrs, 1):
    c = ws.cell(row=hr, column=i, value=h); c.font = BOLD; c.fill = HD; c.border = BD
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.column_dimensions[get_column_letter(i)].width = 13 if i > 9 else 15
FEAS = {"S1":"基准候选","S2":"否决（收入仅增 8%）","S3":"否决","S4":"比价方案","S5":"否决","S6":"否决",
        "S7":"比价方案","S7B":"唯一全判据成立","S8":"不可行（客房面积不达标）"}
r = hr + 1
for k in ("S1","S2","S3","S4","S5","S6","S7","S7B","S8"):
    s = SCH[k]
    b = "**" if k in ("S1","S7B") else ""
    inr = (s["pb_inc"] is not None)
    vals = [k, s["brand"], s["pub_mode"], s["room_mode"], s["n_rooms"], s["months"], s["loss"], s["mep"], s["fit"],
            s["capex"], s["total_need"], s["adr"], s["steady_rev"], BASE["total_rev"], s["rev_vs_base"], s["rev_ratio"],
            P(s["irr20"]), s["npv20"], (s["pb20"] or "期内未回收"), P(s["irr_grp"]), (s["pb_grp"] or "不适用"),
            P(s["irr_inc"]), (s["pb_inc"] or "未回收"), FEAS[k]]
    r = put(ws, r, vals, ["General"]*24, [None]*23 + [BAD if k in ("S2","S8") else (OK if k == "S7B" else None)])
wb.save(NEW)
L("[XLS] 02 总览已改三重口径 + 收入列（9 行）")

# ══════════ Word v3.0 ══════════
sys.path.insert(0, r"D:\B166ER-openclaw\workspace\.tmp")
from md2docx_cn import convert
out = os.path.join(REP, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.docx")
convert(MD, out)
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
TMP = os.path.join(T, "_v33.docx")
d = Document(out)
def set_outline(p, lvl):
    pPr = p._p.get_or_add_pPr()
    for old in pPr.findall(qn("w:outlineLvl")):
        pPr.remove(old)
    e = OxmlElement("w:outlineLvl"); e.set(qn("w:val"), str(lvl)); pPr.append(e)
cnt = {"0":0,"1":0,"2":0}
for p in d.paragraphs:
    tx = p.text.strip()
    if not tx or len(tx) > 60: continue
    if re.match(r"^\d+\. [一二三四五六七八九十]+、", tx): continue
    lvl = None
    if tx == "关于总府皇冠假日酒店改造升级项目可行性研究报告": lvl = 0
    elif re.match(r"^[一二三四五六七八九十]+、\S", tx): lvl = 1
    elif re.match(r"^（[一二三四五六七八九十]+）", tx): lvl = 2
    elif re.match(r"^\d+\.\d+\s", tx): lvl = 2
    if lvl is not None:
        set_outline(p, lvl); p.paragraph_format.keep_with_next = True; cnt[str(lvl)] += 1
d.save(TMP); shutil.move(TMP, out)
L("DOCX v3.0 %.1f KB | 大纲 L0=%d L1=%d L2=%d" % (os.path.getsize(out)/1024, cnt["0"], cnt["1"], cnt["2"]))
d = Document(out)
blank = sum(1 for tb in d.tables for r in tb.rows for c in r.cells if c.text.strip() in ("", "\u2014", "-", "\uff0f", "/"))
L("docx: 段落 %d / 表格 %d / 空白格 %d / 节 %d" % (len(d.paragraphs), len(d.tables), blank, len(d.sections)))
EMO = "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\u24C2\u2B55]"
L("emoji:", len(re.findall(EMO, t)), "| ??:", len(re.findall(r"\?\?", t)))
for k in ("620", "880", "1,500", "1,750", "3,000", "19.93", "11.33", "16,916.8", "6,774.0", "518.5", "5.61", "40.48 万家", "1,979 万间"):
    L("  %-14s %s" % (k, "在" if k in t else "缺"))
bad = [l for l in t.split("\n") if l.startswith("#") and ("|" in l or "**" in l or len(l) > 95)]
L("标题异常:", len(bad))
for b in bad[:5]: L("   !", b[:100])
m = re.search(r"^## 目录\n", t, re.M)
ls = t[m.end():].split("\n")
start = next((i for i, l in enumerate(ls) if l.startswith("## ")), None)
toc = [re.sub(r"^\d+\. ", "", l).strip() for l in ls[:start] if re.match(r"^\d+\. ", l)]
bod = [l[3:].strip() for l in ls[start:] if l.startswith("## ")]
L("目录与正文一致:", toc == bod, "| 目录", len(toc), "正文", len(bod))
# 旧版清理
for n in ("总府皇冠改造_可行性研究报告_v2.0_2026-11-14.docx",):
    p = os.path.join(REP, n)
    if os.path.exists(p):
        try:
            os.remove(p); L("removed", n)
        except Exception:
            L("[仍被占用]", n)
L("DONE")
