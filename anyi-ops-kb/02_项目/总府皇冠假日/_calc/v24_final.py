# -*- coding: utf-8 -*-
"""v24：修复第五章（五）（六）一致性；Excel 08/10/01 三表按 v21 新模型重算；出 Word v3.0；终检"""
import io, os, sys, re, json, glob, shutil
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v24.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
sys.path.insert(0, os.path.join(KB, "_calc"))
from v22_text import CH5_NEW6

MD = os.path.join(KB, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
t = open(MD, encoding="utf-8").read()

# ══ ① 第五章（五）：表 + 比选结论（替换到 ### （六） 之前）══════════
m = re.search(r"^### （五）品牌方案比选.*?(?=^### （六）)", t, re.M | re.S)
assert m, "未定位第五章（五）"
NEW5 = ("### （五）品牌方案比选\n\n以下比较在第五章第一节情形一假设下成立，并按第九章分档定价口径列示。"
        "**排序同时看收入增量与投资回报两条线，不可只看其一。**\n\n" + CH5_NEW6.rstrip() + "\n\n")
t = t[:m.start()] + NEW5 + t[m.end():]
L("[MD] 第五章（五）表+比选结论已重建")

# ══ ② 第五章（六）方向选择结论：重写 ══════════════════════════════
CH5_SIX = r"""### （六）方向选择结论

**一，以 S1「沿用皇冠 + 公区保留石材 + 不减房」为五星档基准方案推进。** 改造投资 21,313.6 万元为九方案最低，改造后年收入 10,938.7 万元为改造前 6,774.0 万元的 1.61 倍（增量 4,164.7 万元/年），全口径内部收益率 4.60% 高于 3.5% 底线，可保留项节约 4,538.7 万元占改造投资 21.3%。须如实报集团的是：净现值 −6,002.9 万元、集团口径静态回收 10.15 年，均未进入 5 至 8 年参照区间。

**二，S4「洲至奢选 + 公区保留石材」为比价方案。** 收入倍数 2.07、增量 7,235.8 万元/年、全口径内部收益率 4.82%，均略优于 S1；但改造投资 28,190.7 万元、停业 15 个月，集团口径静态回收 9.88 年、净现值 −7,351.4 万元，仍未进入参照区间。

**三，S7B「外部奢牌 + 3 改 2」是唯一在全部判据上成立的方案，但三项前提须先验证。** 收入倍数 5.61、增量 31,229.1 万元/年、全口径内部收益率 11.33%、净现值 +16,916.8 万元、集团口径静态回收 6.11 年（落入区间）。三项前提：顶级设计型价格带（3,000 元）在总府位置可兑现；客房面积经 3 改 2 达到 40 平方米以上；品牌方接受全部改造投入结构。**任一不成立，结论即反转。**

**四，明确否决 S2 减房方案、S3 与 S5 公区拆除重做、S6 与 S8。** S2 收入增量仅 518.5 万元（1.08 倍）而投入不降；S3、S5 改造投入上升而收入不变（净现值 −14,454.7 与 −19,338.6 万元）；S6 净现值 −32,811.6 万元；S8 客房 25.35 平方米低于所有候选奢牌面积门槛。

**五，方案选择最终取决于两个尚未取得的结论。** 一是第三方安全评估对"消防与机电设备现状是否已无法满足经营条件与标准要求"的认定；二是外部奢牌顶级设计型价格带在总府位置的可兑现性。**在这两项结论取得前，本报告的方案比选结论应视为条件性结论。**

"""
m = re.search(r"^### （六）方向选择结论.*?(?=^## 第六章 )", t, re.M | re.S)
if m:
    t = t[:m.start()] + CH5_SIX.rstrip() + "\n\n" + t[m.end():]
    L("[MD] 第五章（六）已重写")
else:
    L("[MISS] 第五章（六）")

open(MD, "w", encoding="utf-8").write(t)
L("MD bytes:", len(t.encode("utf-8")))

# ══ ③ Excel 三表重算 ══
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
V21 = json.load(open(os.path.join(T, "v21.json"), encoding="utf-8"))
BASE = V21["base"]; SCH = {s["key"]: s for s in V21["schemes"]}
NEW = os.path.join(CAL, "总府皇冠改造_可行性研究报告_测算附表_v3.0_2026-11-14.xlsx")
wb = load_workbook(NEW)
THIN = Side(style="thin", color="BFBFBF"); BD = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
BOLD = Font(bold=True); BAD = PatternFill("solid", fgColor="FFC7CE"); OK = PatternFill("solid", fgColor="C6EFCE")
HD = PatternFill("solid", fgColor="D9E2F3")
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
FEAS = {"S1":"基准候选","S2":"否决（收入仅增 8%）","S3":"否决","S4":"比价方案","S5":"否决","S6":"否决",
        "S7":"比价方案","S7B":"唯一全判据成立","S8":"不可行（客房面积不达标）"}
ORD = ("S1","S2","S3","S4","S5","S6","S7","S7B","S8")

# 08 八方案造价总表 → 九方案完整表
del wb["08 八方案造价总表"]
ws = wb.create_sheet("08 八方案造价总表", 7)
ws["A1"] = "九个方案完整造价、收入与回报总表（三段式 × 分档定价）"; ws["A1"].font = Font(bold=True, size=13)
ws["A2"] = "单位：万元。段二机电水电强弱电与品牌无关；判定基准：改造后年收入须高于改造前 6,774.0 万元"
r = 4
r = hd(ws, r, ["方案","品牌标准","公区做法","房量做法","房量（间）","停业月数","段一 停业损失","段二 机电水电强弱电",
               "段三 装修改造","改造投资","项目总资金需求","平均房价（元）","改造后年营业收入","改造前基线","收入增量",
               "收入倍数","全口径内部收益率","全口径净现值","全口径静态回收期","集团口径内部收益率","集团口径静态回收期（年）",
               "增量口径内部收益率","增量口径静态回收期（年）","可保留项节约","可行性"],
        [8,12,10,10,10,9,13,18,14,13,15,12,16,13,13,11,15,14,15,15,17,15,17,13,24])
for k in ORD:
    s = SCH[k]
    b = "**" if k in ("S1","S7B") else ""
    r = put(ws, r, [k, s["brand"], s["pub_mode"], s["room_mode"], s["n_rooms"], s["months"], s["loss"], s["mep"], s["fit"],
                    s["capex"], s["total_need"], s["adr"], s["steady_rev"], round(BASE["total_rev"],1), s["rev_vs_base"], s["rev_ratio"],
                    P(s["irr20"]), s["npv20"], (s["pb20"] or "期内未回收"), P(s["irr_grp"]), (s["pb_grp"] or "不适用"),
                    P(s["irr_inc"]), (s["pb_inc"] or "未回收"), (s.get("retain_saving") if "retain_saving" in s else "不适用"), FEAS[k]],
            ["General"]*25, [None]*23 + [BAD if k in ("S2","S8") else (OK if k=="S7B" else None), None])
r += 1
r = put(ws, r, ["改造前基线（不改造）", "—", "—", "—", BASE["rooms"], "—", "—", "—", "—", "—", "—", BASE["adr"],
                round(BASE["total_rev"],1), "—", "—", 1.00, "—", "—", "—", "—", "—", "—", "—", "—", "业主口径实测"])
ws.cell(row=r-1, column=1).font = BOLD
L("[XLS] 08 总表已重建（9 方案 × 25 列）")

# 10 三口径对照 → 新
del wb["10 三口径对照"]
ws = wb.create_sheet("10 三口径对照", 9)
ws["A1"] = "三口径对照与改造前后收入判据（v3.0 分档定价）"; ws["A1"].font = Font(bold=True, size=13)
ws["A2"] = "口径一 全口径｜口径二 集团口径（改造后年经营现金流÷改造投资）｜口径三 增量口径（相对不改造反事实）"
r = 4
r = hd(ws, r, ["方案","改造投资（万元）","平均房价（元）","改造后年营业收入（万元）","改造前基线（万元）","收入增量（万元）",
               "收入倍数","全口径内部收益率","全口径净现值（万元）","全口径静态回收期","集团口径内部收益率",
               "集团口径静态回收期（年）","增量口径内部收益率","增量口径静态回收期（年）","落入集团 5-8 年区间"],
        [10,15,13,18,16,15,11,15,16,15,15,17,15,17,17])
for k in ORD:
    s = SCH[k]
    inr = (s["pb_grp"] is not None and 5 <= s["pb_grp"] <= 8)
    r = put(ws, r, [k, s["capex"], s["adr"], round(s["steady_rev"],1), round(BASE["total_rev"],1), s["rev_vs_base"], s["rev_ratio"],
                    P(s["irr20"]), s["npv20"], (s["pb20"] or "期内未回收"), P(s["irr_grp"]), (s["pb_grp"] or "不适用"),
                    P(s["irr_inc"]), (s["pb_inc"] or "未回收"), "是" if inr else "否"],
            ["General"]*15, [None]*13 + [OK if inr else BAD, None])
L("[XLS] 10 三口径已重建")

# 01 大数对照表：更新为新数
ws = wb["01 报告大数对照表"]
r = ws.max_row + 2
ws.cell(row=r, column=1, value="【v3.0 更正：分档定价与改造前后收入判据】").font = BOLD
r += 1
r = hd(ws, r, ["报告位置","正文大数","数值","来源表","口径说明"], [30,40,22,22,58])
for row in [
 ("第九章（一）","改造前基线年营业收入","6,774.0 万元","15 分档定价与市场层级","近 24 个月月均 564.5 万元年化"),
 ("第九章（一）","改造前平均房价／出租率","363.99 元／70.78%","15 分档定价与市场层级","2026-09 实测"),
 ("第九章（二）","五星档价位（三档）","620／750／880 元","15 分档定价与市场层级","五星级低、中、高档位"),
 ("第九章（二）","奢华主流带价位","1,500／1,750／2,000 元","15 分档定价与市场层级","瑞吉、华尔道夫、尼依格罗 2026 实测"),
 ("第九章（二）","奢华顶级设计型带价位","3,000 元","15 分档定价与市场层级","居舍 2,000—3,000 元实测"),
 ("第九章（三）","S2 减房收入增量","+518.5 万元（1.08 倍）","08 总表","改房不如不改房的量化形态"),
 ("第九章（三）","S1 收入倍数","1.61 倍（10,938.7 万元）","08 总表","五星档基准"),
 ("第九章（三）","S4 收入倍数","2.07 倍（14,009.8 万元）","08 总表","洲至奢选比价"),
 ("第九章（三）","S7B 收入倍数","5.61 倍（38,003.1 万元）","08 总表","外部奢牌顶级设计型带"),
 ("第九章（三）","S7B 全口径内部收益率／净现值","11.33%／+16,916.8 万元","10 三口径","唯一净现值转正"),
 ("第九章（三）","S7B 集团口径回收期","6.11 年","10 三口径","唯一落入 5-8 年区间"),
 ("第二章（一）","中国酒店总量","40.48 万家／1,979 万间","15 分档定价与市场层级","2026-06"),
 ("第二章（三）","西南／川渝","西南毛利五年首降；重庆 47 万间增速 7.9%","15 分档定价与市场层级","浩华／重庆酒店行业分析"),
 ("第二章（六）","春熙路超高端在营","134 家酒店中超高端仅 3 家","15 分档定价与市场层级","居舍、君悦、尼依格罗"),
 ("第二章（七）","成都奢华两档价格带","1,500-2,000 元／3,000 元以上","15 分档定价与市场层级","2026 实测房价"),
 ("第一章（三）","改房判据","改造后年收入须高于改造前 6,774.0 万元","09 财务评价","贯穿第九章"),
]:
    r = put(ws, r, list(row))
L("[XLS] 01 大数对照表已更新")
wb.save(NEW)
L("XLSX %.1f KB | %d sheets" % (os.path.getsize(NEW)/1024, len(wb.sheetnames)))

# ══ ④ Word v3.0 ══
sys.path.insert(0, r"D:\B166ER-openclaw\workspace\.tmp")
from md2docx_cn import convert
out = os.path.join(REP, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.docx")
convert(MD, out)
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
TMP = os.path.join(T, "_v34.docx")
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
for k in ("1,500", "1,750", "3,000", "19.93", "11.33", "16,916.8", "6,774.0", "518.5", "5.61",
          "40.48 万家", "1,979 万间", "2,000—3,000", "1,180—1,800"):
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
for n in ("总府皇冠改造_可行性研究报告_v2.0_2026-11-14.docx",):
    p = os.path.join(REP, n)
    if os.path.exists(p):
        try:
            os.remove(p); L("removed", n)
        except Exception:
            L("[仍被占用]", n)
L("DONE")
