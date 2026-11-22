# -*- coding: utf-8 -*-
"""v12 收官：删旧结论节、按行补表格占位、修 SWOT 旧值、出 v3.2、终检、清理旧版"""
import io, os, sys, re, json, glob, shutil
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
LOG = open(os.path.join(T, "v12.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
def esc(s): return str(s).encode("unicode_escape").decode("ascii")

MD = os.path.join(KB, "总府皇冠改造_立项报告_集团汇报件_v3.1_2026-11-14.md")
MDN = os.path.join(KB, "总府皇冠改造_立项报告_集团汇报件_v3.2_2026-11-14.md")
t = open(MD, encoding="utf-8").read()

# ══ ① 删除第五章旧的「（六）方向选择结论」══
occ = [m.start() for m in re.finditer(r"^### （六）方向选择结论.*$", t, re.M)]
L("（六）方向选择结论 出现:", len(occ))
if len(occ) >= 2:
    s = occ[1]
    m2 = re.search(r"^(### |## )", t[s + 5:], re.M)
    e = s + 5 + m2.start() if m2 else len(t)
    t = t[:s] + t[e:]
    L("已删除旧（六）节，长度", e - s)

# ══ ② 按行关键词补「—」占位 ══
DASH = re.compile(r"^\|(\s*)—(\s*)\|")
FILL_BY_KW = [
 ("29,171.3 万元，超集团额度", "公区全部重做后产品呈现脱离 1996 年观感，与「国际五星全服务型标杆」定位更接近"),
 ("全口径内部收益率仅 1.35%", "不换牌则无品牌方接受度风险，改造路径与现行合同衔接顺畅"),
 ("39,550.7 万元，超集团额度", "奢牌级公区全量重做，可一次性解决 1996 年公区观感，避免二次投入"),
 ("全口径内部收益率 2.45%，低于 3.5% 底线", "洲至奢选在成都已有落地先例（棕榈泉 336 间，2026-01 开业），品牌执行路径可参照"),
 ("竖井与移卫耦合工程增至 860 万元", "减房后公共区与设备可集中设置，单位面积产出效率提升"),
 ("44,381.3 万元，加停业后总需求", "客房面积与公区标准同时达标，产品完整度最高"),
 ("全口径内部收益率 −2.67%", "房间标准无短板，是唯一同时满足客房面积与公区双标的的路径"),
 ("56,850.9 万元，加停业后总需求", "品牌天花板最高，可为集团争取最高标准的轻资产输出样板"),
 ("全口径内部收益率 −4.08%", "客群天花板最高，长期提价空间最大"),
 ("公区与外立面石材不可保留", "可引入外部投资人与品牌方共担出资"),
]
lines = t.split("\n")
filled = 0
for i, l in enumerate(lines):
    if not DASH.match(l):
        continue
    for kw, txt in FILL_BY_KW:
        if kw in l:
            lines[i] = DASH.sub(lambda m: "| %s |" % txt, l, count=1)
            filled += 1
            L("[FILL]", esc(kw[:26]))
            break
t = "\n".join(lines)
L("补占位数:", filled)

# ══ ③ SWOT O5 ══
OLD_O5 = '**可减少停业损失 6,857 万元、内部收益率 提升 12.0 个百分点**|'
NEW_O5 = '**可缩短停业期以减少停业损失，但须增列独立消防设施 2,800 万元并承担重复拆除与二次搬运，净结果须以 20 年全口径重算**|'
if OLD_O5 in t:
    t = t.replace(OLD_O5, NEW_O5); L("[FIX] SWOT O5")
else:
    L("[MISS] SWOT O5")

# ══ ④ 目录重建 ══
m = re.search(r"^## 目录\n", t, re.M)
if m:
    ls = t[m.end():].split("\n")
    start = next((i for i, l in enumerate(ls) if l.startswith("## ")), None)
    h2s = [l[3:].strip() for l in ls[start:] if l.startswith("## ")]
    toc = "\n".join("%d. %s" % (i + 1, h) for i, h in enumerate(h2s))
    t = t[:m.end()] + toc + "\n\n" + "\n".join(ls[start:])
    L("目录重建:", len(h2s), "条")

open(MDN, "w", encoding="utf-8").write(t)
os.remove(MD)
L("MD -> v3.2, bytes:", len(t.encode("utf-8")))

# ══ ⑤ 出 Word + 大纲 ══
sys.path.insert(0, r"D:\B166ER-openclaw\workspace\.tmp")
from md2docx_cn import convert
out = os.path.join(REP, "总府皇冠改造_立项报告_集团汇报件_v3.2_2026-11-14.docx")
convert(MDN, out)
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
TMP = os.path.join(T, "_v32c.docx")
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
L("DOCX v3.2 %.1f KB | 大纲 L0=%d L1=%d L2=%d" % (os.path.getsize(out)/1024, cnt["0"], cnt["1"], cnt["2"]))

# ══ ⑥ 终检 ══
d = Document(out)
blank = 0
for ti, tb in enumerate(d.tables, 1):
    for ri, row in enumerate(tb.rows):
        for ci, cell in enumerate(row.cells):
            if cell.text.strip() in ("", "\u2014", "-", "\uff0f", "/"):
                blank += 1
                L("  BLANK 表%d 行%d 列%d : %s" % (ti, ri, ci, " || ".join(cell.text.strip()[:24] for cell in row.cells)))
L("docx: 段落 %d / 表格 %d / 空白格 %d" % (len(d.paragraphs), len(d.tables), blank))
EMO = "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\u24C2\u2B55]"
L("emoji:", len(re.findall(EMO, t)), "| ??:", len(re.findall(r"\?\?", t)), "| 单问号:", len(re.findall(r"\?(?=[\d(（])", t)))
L("=== 旧值残留 ===")
for k in ("14,401", "5.37%", "19.93%", "12.48%", "7.10 年", "9,919", "14,061", "27,919", "32,061", "38,784", "20,724"):
    c = t.count(k)
    if c: L("  [旧值]", k, c)
L("=== 关键新值 ===")
for k in ("21,313.6", "31,093.6", "4,538.7", "4.60%", "6.13%", "1,186 元", "11,060", "9,780", "76.2%", "13,040", "28,190.7", "56,850.9"):
    L("  %-12s %s" % (k, "在" if k in t else "缺"))
bad = [l for l in t.split("\n") if l.startswith("#") and ("|" in l or "**" in l or len(l) > 95)]
L("标题异常:", len(bad))
for b in bad[:5]: L("   !", esc(b[:100]))
m = re.search(r"^## 目录\n", t, re.M)
ls = t[m.end():].split("\n")
start = next((i for i, l in enumerate(ls) if l.startswith("## ")), None)
toc_items = [re.sub(r"^\d+\. ", "", l).strip() for l in ls[:start] if re.match(r"^\d+\. ", l)]
body_items = [l[3:].strip() for l in ls[start:] if l.startswith("## ")]
L("目录与正文一致:", toc_items == body_items, "| 目录", len(toc_items), "正文", len(body_items))
L("章节:", " / ".join(body_items))

# ══ ⑦ 清理旧 docx ══
for n in ("总府皇冠改造_立项报告_集团汇报件_v3.1_2026-11-14.docx",
          "总府皇冠改造_立项报告_集团汇报件_v3.0_2026-11-14.docx",
          "总府皇冠改造_立项报告_集团汇报件_v2.0_2026-11-13.docx",
          "总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.docx"):
    p = os.path.join(REP, n)
    if os.path.exists(p):
        try:
            os.remove(p); L("removed", n)
        except Exception:
            L("[仍被 Word 占用]", n)
for f in glob.glob(os.path.join(REP, "~$*")):
    try:
        os.remove(f); L("removed lock", os.path.basename(f))
    except Exception:
        L("[锁文件残留]", os.path.basename(f))
L("\n=== 最终交付 ===")
for f in sorted(glob.glob(os.path.join(REP, "*.docx"))):
    if os.path.basename(f).startswith("~$"): continue
    if not re.search(r"立项报告_集团汇报件|立项方案_数据源清单", f): continue
    L("  [报告] %-68s %7.1f KB" % (os.path.basename(f).encode("unicode_escape").decode("ascii"), os.path.getsize(f)/1024))
for f in sorted(glob.glob(os.path.join(TGT, "测算与中间产物", "*.xlsx"))):
    L("  [测算] %-68s %7.1f KB" % (os.path.basename(f).encode("unicode_escape").decode("ascii"), os.path.getsize(f)/1024))
L("DONE")
