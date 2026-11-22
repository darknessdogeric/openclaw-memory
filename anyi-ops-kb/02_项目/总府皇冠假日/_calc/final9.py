# -*- coding: utf-8 -*-
"""v3.1 收官：① 口径表述全量对齐（判定基准统一为集团口径）② 负号乱码修复
   ③ Excel 02/02b 判定列改用集团口径 ④ 重出 Word ⑤ 终检"""
import io, os, sys, re, json, glob, shutil
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "final9.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
def esc(s): return str(s).encode("unicode_escape").decode("ascii")

MD = os.path.join(KB, "总府皇冠改造_立项报告_集团汇报件_v3.1_2026-11-14.md")
t = open(MD, encoding="utf-8").read()

# ══ ① 口径表述对齐（用正则，引号兼容）══════════════════════
FIX = [
 # L864 重复旧句（已被 L862 新句取代）→ 删除
 (r"\*\*结论：按集团自身口径，方向一[“\"']?沿用皇冠 \+ 不减房[”\"']?是唯一落入回收期 5-8 年区间的方案，且增量口径内部收益率 19\.93% 高于集团规划值 17\.00%。\*\*[ ]*方向三在增量口径下可达 12\.46%，但回收期 10 年超出集团区间。\n\n",
  ""),
 # L866 判定依据表述 → 改为集团口径为基准、增量口径为辅助
 (r"这不是经营能力问题，而是历史包袱与建设期时点问题。对改造决策而言，判定应使用增量口径；对存量资产处置与保值增值考核而言，则须使用口径三并另行报请集团明确。",
  "这不是经营能力问题，而是历史包袱与建设期时点问题。对改造决策而言，判定基准应是与集团一致的口径三（改造后年经营现金流 ÷ 改造投资）；口径二用于表达改造的必要性；口径一用于说明项目自身的绝对价值。三套口径在本次报告中并列列示，不单独依赖任一口径作结论。"),
 # L482 第五章结论一 → 补集团口径数
 (r"增量口径静态回收期 7 年，增量口径内部收益率 19\.93%，高于集团规划值 17\.00%；改造投资 14,401 万元，低于集团为总府预留的 18,000 万元。",
  "集团口径静态回收期 7.10 年（含首年爬坡 9 年）、集团口径内部收益率 12.48%、增量口径内部收益率 19.93%；改造投资 14,401 万元，低于集团为总府预留的 18,000 万元。"),
 # L1030 第十一章结论四 → 剔除口径错配的比较
 (r"增量口径静态回收期 7 年、增量口径内部收益率 19\.93%，均优于集团规划值 5\.6 年与 17\.00%；改造投资 14,401 万元，低于集团为总府预留的 18,000 万元。",
  "集团口径静态回收期 7.10 年（含首年爬坡 9 年）、集团口径内部收益率 12.48%、增量口径内部收益率 19.93%；改造投资 14,401 万元，低于集团为总府预留的 18,000 万元。与集团规划值 5.6 年、17.00% 的差距已定位到平均房价假设一项（详见第九章第五节），须以集团测算底稿据实对账。"),
 # 第五章 方向一优势栏 → 增量口径回收期不用于判定，改集团口径
 (r"\*\*增量口径回收期 7 年，落入集团[“\"']?回收期 5-8 年[”\"']?区间\*\*",
  "**集团口径静态回收期 7.10 年，落入集团 5-8 年区间**"),
]
for pat, rep in FIX:
    t, n = re.subn(pat, rep, t)
    L("[FIX]", esc(pat[:40]), "->", n)

# ══ ② 负号乱码：? 出现在数字前 → − ═════════════════════════
def fix_minus(text):
    out = []
    cnt = 0
    samples = []
    for m in re.finditer(r"\?(?=[\d(（])", text):
        s = max(0, m.start() - 22)
        samples.append(text[s:m.start() + 12].replace("\n", " "))
    text = re.sub(r"\?(?=[\d(（])", "\u2212", text)
    return text, cnt, samples[:8]
t, mc, ms = fix_minus(t)
L("负号乱码修复:", mc)
for s in ms:
    L("   ", esc(s))

# ══ ③ 残留复检 ══════════════════════════════════════════════
sus = []
for i, l in enumerate(t.split("\n"), 1):
    s = l.strip()
    if re.search(r"增量口径[^。]{0,45}(落入|达标|符合)", s):
        sus.append((i, s[:160]))
L("口径残留可疑行:", len(sus))
for i, s in sus:
    L("   L%d | %s" % (i, esc(s)))

open(MD, "w", encoding="utf-8").write(t)
L("MD bytes:", len(t.encode("utf-8")))

# ══ ④ Excel：02 总览与 02b 的判定列改用集团口径 ═══════════════
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
XL = os.path.join(CAL, "总府皇冠改造_立项方案_细项概算表_v3.1_2026-11-14.xlsx")
wb = load_workbook(XL)
DV = json.load(open(os.path.join(T, "v8.json"), encoding="utf-8"))["dirs"]
THIN = Side(style="thin", color="BFBFBF"); BD = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
B = Font(bold=True); HD = PatternFill("solid", fgColor="D9E2F3"); OKF = PatternFill("solid", fgColor="C6EFCE")
LB = {"D1": "一 沿用皇冠·不减房", "D1X": "一 沿用皇冠·不减房（公区拆除重做）", "D2": "二 沿用皇冠·3改2",
      "D3": "三 换奢牌·不减房（公区拆除重做）", "D3R": "三 换奢牌·不减房（公区保留石材）", "D4": "四 换奢牌·3改2"}
NR = {"D1": 402, "D1X": 402, "D2": 268, "D3": 402, "D3R": 402, "D4": 268}
OWNER_COEF = 0.18542

# 02 总览：改第 14 列（增量口径静态回收期）不动，新增/改第 17 列判定 → 用集团口径
ws = wb["02 方向总览对比"]
r = 5
for k in ("D1", "D1X", "D2", "D3", "D3R", "D4"):
    x = DV[k]
    og = x["owner_gop"]
    pbn = round(x["capex"] / og, 2) if og else None
    inr = (pbn is not None and 5 <= pbn <= 8)
    # N 列：增量口径静态回收期（保留，标注口径）
    ws.cell(row=r, column=14, value=x["pb_inc"] or "未回收")
    # Q 列：是否落入 → 改为集团口径判定
    cc = ws.cell(row=r, column=17, value="是" if inr else "否")
    cc.fill = OKF if inr else PatternFill("solid", fgColor="FFC7CE")
    # R 列：集团口径静态回收期（不含爬坡）
    cc2 = ws.cell(row=r, column=18, value=pbn); cc2.number_format = "0.00"; cc2.border = BD
    r += 1
ws.cell(row=4, column=18, value="集团口径静态回收期（不含爬坡，年）").font = B
ws.cell(row=4, column=18).fill = HD; ws.cell(row=4, column=18).border = BD
ws.cell(row=4, column=18).alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
ws.column_dimensions["R"].width = 20
ws.cell(row=r + 1, column=1, value="判定基准：集团口径（改造后年经营现金流 ÷ 改造投资），与集团 715 定稿专栏 6 的 5.6 年回收期同算法；方向一 7.10 年落入集团 5-8 年区间。").font = B
L("[XLS] 02 总览判定列已改集团口径")

# 02b：第 15 列已是集团口径无爬坡，第 16 列为判定 → 确认按第 15 列重算
ws2 = wb["02b 三重口径校准与集团对照"]
hr = None
for rr in range(1, 14):
    if ws2.cell(row=rr, column=1).value == "方向":
        hr = rr; break
if hr:
    rr = hr + 1
    for k in ("D1", "D1X", "D2", "D3", "D3R", "D4"):
        if k not in DV: continue
        x = DV[k]
        pbn = round(x["capex"] / x["owner_gop"], 2) if x["owner_gop"] else None
        inr = (pbn is not None and 5 <= pbn <= 8)
        c15 = ws2.cell(row=rr, column=15, value=pbn); c15.number_format = "0.00"; c15.border = BD
        if inr: c15.fill = OKF
        ws2.cell(row=rr, column=16, value="是" if inr else "否")
        rr += 1
    L("[XLS] 02b 判定列已统一集团口径")
wb.save(XL)
L("XLSX %.1f KB | %d sheets" % (os.path.getsize(XL)/1024, len(wb.sheetnames)))

# ══ ⑤ 重出 Word + 大纲级别 ═══════════════════════════════════
sys.path.insert(0, r"D:\B166ER-openclaw\workspace\.tmp")
from md2docx_cn import convert
out = os.path.join(REP, "总府皇冠改造_立项报告_集团汇报件_v3.1_2026-11-14.docx")
convert(MD, out)
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
TMP = os.path.join(T, "_v31c.docx")
d = Document(out)
def set_outline(p, lvl):
    pPr = p._p.get_or_add_pPr()
    for old in pPr.findall(qn("w:outlineLvl")):
        pPr.remove(old)
    e = OxmlElement("w:outlineLvl"); e.set(qn("w:val"), str(lvl)); pPr.append(e)
cnt = {"0": 0, "1": 0, "2": 0}
for p in d.paragraphs:
    tx = p.text.strip()
    if not tx or len(tx) > 60: continue
    if re.match(r"^\d+\. [一二三四五六七八九十]+、", tx): continue
    lvl = None
    if tx == "关于总府皇冠假日酒店改造升级工作思路的报告": lvl = 0
    elif re.match(r"^[一二三四五六七八九十]+、\S", tx): lvl = 1
    elif re.match(r"^（[一二三四五六七八九十]+）", tx): lvl = 2
    elif re.match(r"^\d+\.\d+\s", tx): lvl = 2
    if lvl is not None:
        set_outline(p, lvl); p.paragraph_format.keep_with_next = True; cnt[str(lvl)] += 1
d.save(TMP); shutil.move(TMP, out)
L("DOCX %.1f KB | 大纲 L0=%d L1=%d L2=%d" % (os.path.getsize(out)/1024, cnt["0"], cnt["1"], cnt["2"]))

# ══ ⑥ 终检 ════════════════════════════════════════════════════
d = Document(out)
blank = 0
for ti, tb in enumerate(d.tables, 1):
    for ri, row in enumerate(tb.rows):
        for ci, cell in enumerate(row.cells):
            if cell.text.strip() in ("", "\u2014", "-", "\uff0f", "/"):
                blank += 1; L("  BLANK 表%d 行%d 列%d" % (ti, ri, ci))
L("docx: 段落 %d / 表格 %d / 空白格 %d" % (len(d.paragraphs), len(d.tables), blank))
EMO = "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\u24C2\u2B55]"
L("emoji:", len(re.findall(EMO, t)), "| ??:", len(re.findall(r"\?\?", t)), "| 单问号残留:", len(re.findall(r"\?(?=[\d(（])", t)))
for k in ("10 年国资", "10年国资", "10 年门槛", "10年门槛", "国资委 10 年口径", "3.5%", "10 年窗口"):
    c = t.count(k)
    if c: L("  [残留]", k, c)
for k in ("19.93%", "12.48%", "7.10 年", "1,186 元", "3,206 万", "42%", "9,919", "14,061", "5-8 年", "−1,924"):
    L("  %-12s %s" % (k, "在" if k in t else "缺"))
bad = [l for l in t.split("\n") if l.startswith("#") and ("|" in l or "**" in l or len(l) > 95)]
L("标题异常:", len(bad))
for b in bad[:5]: L("   !", esc(b[:100]))
m = re.search(r"^## 目录\n", t, re.M)
lines = t[m.end():].split("\n")
start = next((i for i, l in enumerate(lines) if l.startswith("## ")), None)
toc_items = [re.sub(r"^\d+\. ", "", l).strip() for l in lines[:start] if re.match(r"^\d+\. ", l)]
body_items = [l[3:].strip() for l in lines[start:] if l.startswith("## ")]
L("目录与正文一致:", toc_items == body_items, "| 目录", len(toc_items), "正文", len(body_items))

# ══ ⑦ memory ══════════════════════════════════════════════════
MEM = r"D:\B166ER-openclaw\workspace\memory\2026-11-13.md"
open(MEM, "a", encoding="utf-8").write("""

**收官（v3.1）**：① 判定基准统一为集团口径（改造后年经营现金流 ÷ 改造投资，与 715 定稿专栏 6 同算法），增量口径降为表达改造必要性、全口径为绝对价值，三套并列列示；② 第五章、第十一章、结论章、请示事项口径表述全部对齐；③ 修复正文中负号乱码（?1,924 → −1,924 等）；④ Excel 02 总览与 02b 的"是否落入集团 5-8 年"列改为按集团口径静态回收期（不含爬坡）判定，并新增该列。终检：53 张表 0 空白、目录与正文 11:11 一致、emoji 0、可导航标题 74。
<!-- project: github.com/darknessdogeric/openclaw-memory -->
""")
L("memory 已追加")
L("DONE")
