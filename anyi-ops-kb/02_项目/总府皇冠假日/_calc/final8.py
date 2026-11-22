# -*- coding: utf-8 -*-
"""v3.1 收官：修正因引号字符不匹配而残留的判定句 + MD 改名 v3.1 + 出 Word + 修正记录乱码 + 全量终检"""
import io, os, sys, re, glob, shutil
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "final8.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
def esc(s): return str(s).encode("unicode_escape").decode("ascii")

MD_OLD = os.path.join(KB, "总府皇冠改造_立项报告_集团汇报件_v3.0_2026-11-14.md")
MD = os.path.join(KB, "总府皇冠改造_立项报告_集团汇报件_v3.1_2026-11-14.md")
t = open(MD_OLD, encoding="utf-8").read()

# ① 残留判定句（引号兼容正则）
P1 = re.compile(
    r"\*\*结论：按集团自身口径，方向一[“\"']?沿用皇冠 \+ 不减房[”\"']?"
    r"是唯一落入回收期 5-8 年区间的方案，且增量口径内部收益率 19\.93% 高于集团规划值 17\.00%。\*\*"
    r"方向三在增量口径下可达 12\.46%，但回收期 10 年超出集团区间。")
R1 = ("**结论：按集团自身口径（改造后年经营现金流 ÷ 改造投资），方向一“沿用皇冠 + 不减房”是唯一落入回收期 5-8 年区间的方案，"
      "集团口径静态回收期 7.10 年（含首年爬坡 9 年）、集团口径内部收益率 12.48%；增量口径内部收益率 19.93%，高于集团规划值 17.00%。** "
      "方向三集团口径静态回收期 9.19 年、增量口径内部收益率 12.46%，两项均低于方向一。")
t, n = P1.subn(R1, t)
L("[1] 残留判定句替换:", n)

# ② 兜底：任何仍把"增量口径回收期 7 年"与"落入集团 5-8 年"并列的表述
P2 = re.compile(r"增量口径回收期 7 年[^。]{0,20}落入集团 5-8 年区间")
t, n2 = P2.subn("集团口径静态回收期 7.10 年落入集团 5-8 年区间", t)
L("[2] 兜底替换:", n2)

# ③ 全文扫：是否还有把增量口径当集团判定依据的残留
BAD = []
for i, l in enumerate(t.split("\n"), 1):
    s = l.strip()
    if re.search(r"增量口径[^。]{0,40}(落入|符合|达标)", s) and "不含首年爬坡" not in s:
        BAD.append((i, s[:150]))
L("残留可疑行:", len(BAD))
for i, s in BAD:
    L("   L%d | %s" % (i, esc(s)))

# ④ 改名 v3.1
open(MD, "w", encoding="utf-8").write(t)
os.remove(MD_OLD)
L("MD -> v3.1, bytes:", len(t.encode("utf-8")))

# ⑤ 出 Word + 大纲级别
sys.path.insert(0, r"D:\B166ER-openclaw\workspace\.tmp")
from md2docx_cn import convert
out = os.path.join(REP, "总府皇冠改造_立项报告_集团汇报件_v3.1_2026-11-14.docx")
convert(MD, out)
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
TMP = os.path.join(T, "_v31b.docx")
d = Document(out)
def set_outline(p, lvl):
    pPr = p._p.get_or_add_pPr()
    for old in pPr.findall(qn("w:outlineLvl")):
        pPr.remove(old)
    e = OxmlElement("w:outlineLvl"); e.set(qn("w:val"), str(lvl)); pPr.append(e)
cnt = {"0": 0, "1": 0, "2": 0}
for p in d.paragraphs:
    tx = p.text.strip()
    if not tx or len(tx) > 60:
        continue
    if re.match(r"^\d+\. [一二三四五六七八九十]+、", tx):
        continue
    lvl = None
    if tx == "关于总府皇冠假日酒店改造升级工作思路的报告":
        lvl = 0
    elif re.match(r"^[一二三四五六七八九十]+、\S", tx):
        lvl = 1
    elif re.match(r"^（[一二三四五六七八九十]+）", tx):
        lvl = 2
    elif re.match(r"^\d+\.\d+\s", tx):
        lvl = 2
    if lvl is not None:
        set_outline(p, lvl); p.paragraph_format.keep_with_next = True; cnt[str(lvl)] += 1
d.save(TMP); shutil.move(TMP, out)
L("DOCX v3.1 %.1f KB | 大纲 L0=%d L1=%d L2=%d" % (os.path.getsize(out)/1024, cnt["0"], cnt["1"], cnt["2"]))

# ⑥ 终检
d = Document(out)
blank = 0
for ti, tb in enumerate(d.tables, 1):
    for ri, row in enumerate(tb.rows):
        for ci, cell in enumerate(row.cells):
            if cell.text.strip() in ("", "\u2014", "-", "\uff0f", "/"):
                blank += 1
                L("  BLANK 表%d 行%d 列%d" % (ti, ri, ci))
L("docx: 段落 %d / 表格 %d / 空白格 %d" % (len(d.paragraphs), len(d.tables), blank))
EMO = "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\u24C2\u2B55]"
L("emoji:", len(re.findall(EMO, t)), "| ??:", len(re.findall(r"\?\?", t)), "| __:", len(re.findall(r"_{3,}", t)))
for k in ("10 年国资", "10年国资", "10 年门槛", "10年门槛", "国资委 10 年口径", "3.5%", "10 年窗口"):
    c = t.count(k)
    if c:
        L("  [残留]", k, c)
for k in ("19.93%", "12.48%", "7.10 年", "1,186 元", "3,206 万", "42%", "9,919", "14,061", "5-8 年"):
    L("  %-12s %s" % (k, "在" if k in t else "缺"))
bad = [l for l in t.split("\n") if l.startswith("#") and ("|" in l or "**" in l or len(l) > 95)]
L("标题异常:", len(bad))
for b in bad[:5]:
    L("   !", esc(b[:100]))
# 目录与正文一致
m = re.search(r"^## 目录\n", t, re.M)
lines = t[m.end():].split("\n")
start = next((i for i, l in enumerate(lines) if l.startswith("## ")), None)
toc_items = [re.sub(r"^\d+\. ", "", l).strip() for l in lines[:start] if re.match(r"^\d+\. ", l)]
body_items = [l[3:].strip() for l in lines[start:] if l.startswith("## ")]
L("目录与正文一致:", toc_items == body_items, "| 目录", len(toc_items), "正文", len(body_items))
L("章节:", " / ".join(body_items))

# ⑦ 修 corrections.md 乱码
CF = os.path.join(os.environ["USERPROFILE"], "self-improving", "corrections.md")
ct = open(CF, encoding="utf-8").read()
before = ct.count("\ufffd")
ct = ct.replace("**\ufffd⭐", "**⭐").replace("\ufffd⭐", "⭐")
ct = re.sub(r"\ufffd+", "", ct)
open(CF, "w", encoding="utf-8").write(ct)
L("corrections.md 乱码字符: %d -> %d" % (before, ct.count("\ufffd")))

# ⑧ 清理旧版 docx
for n in ("总府皇冠改造_立项报告_集团汇报件_v3.0_2026-11-14.docx",
          "总府皇冠改造_立项报告_集团汇报件_v2.0_2026-11-13.docx",
          "总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.docx"):
    p = os.path.join(REP, n)
    if os.path.exists(p):
        try:
            os.remove(p); L("removed", n)
        except Exception:
            L("[仍被占用]", n)
for f in glob.glob(os.path.join(REP, "~$*")):
    try:
        os.remove(f); L("removed lock", os.path.basename(f))
    except Exception:
        L("[锁文件残留]", os.path.basename(f))

L("\n=== 最终交付 ===")
for f in sorted(glob.glob(os.path.join(REP, "*.docx"))):
    if os.path.basename(f).startswith("~$"):
        continue
    L("  [报告] %-70s %7.1f KB" % (os.path.basename(f).encode("unicode_escape").decode("ascii"), os.path.getsize(f)/1024))
for f in sorted(glob.glob(os.path.join(CAL, "*.xlsx"))):
    L("  [测算] %-70s %7.1f KB" % (os.path.basename(f).encode("unicode_escape").decode("ascii"), os.path.getsize(f)/1024))
L("DONE")
