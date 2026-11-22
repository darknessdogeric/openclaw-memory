# -*- coding: utf-8 -*-
"""按《立项报告》范式合并：源B(公文版可行性研究报告·十一章骨架+目录+公文要素) + 源A(整体方案报告·最新数字)"""
import io, os, sys, re
T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "merge.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
BF = "总府皇冠改造_可行性研究报告_公文版_v1.0_2026-11-09.md"
AF = "总府皇冠改造_整体方案报告_v1.0_2026-11-13.md"
OUTF = "总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.md"

EMOJI = "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\u24C2\u2B55]"

def clean(t):
    t = re.sub(EMOJI + "+", "", t)
    t = re.sub(r"[ \t]+\n", "\n", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    t = t.replace("**——**", "——")
    t = re.sub(r"\*\*[ \t]+", "**", t)
    t = re.sub(r"[ \t]+\*\*", "**", t)
    t = re.sub(r"\*\*[ \t]*\*\*", "", t)
    return t

def parse(path):
    t = clean(open(path, encoding="utf-8").read())
    chaps = []; cur_ch = None; cur_bl = None
    for l in t.split("\n"):
        if l.startswith("## "):
            cur_ch = {"title": l[3:].strip(), "blocks": [], "raw": []}
            chaps.append(cur_ch); cur_bl = None; continue
        if l.startswith("### "):
            cur_bl = {"title": l[4:].strip(), "body": []}
            cur_ch["blocks"].append(cur_bl); continue
        if cur_bl is not None:
            cur_bl["body"].append(l)
        elif cur_ch is not None:
            cur_ch["raw"].append(l)
    return chaps, t

BC, BT = parse(os.path.join(KB, BF))
AC, AT = parse(os.path.join(KB, AF))
def find_c(cs, key):
    for c in cs:
        if key in c["title"]:
            return c
    return None

b1 = find_c(BC, "一、立项依据")
b2 = find_c(BC, "二、市场调研")
b3 = find_c(BC, "三、改造必要性")
b4 = find_c(BC, "四、改造可行性")
b5 = find_c(BC, "五、改造方案比选")
b6 = find_c(BC, "六、投资构成")
b7 = find_c(BC, "七、资金来源")
b8 = find_c(BC, "八、SWOT")
b9 = find_c(BC, "九、经济测算")
b10 = find_c(BC, "十、风险分析")
b11 = find_c(BC, "十一、结论与建议")
a1 = find_c(AC, "一、结论与建议")
a2 = find_c(AC, "二、立项依据")
a3 = find_c(AC, "三、停业方案论证")
a5 = find_c(AC, "五、投资构成")
a6 = find_c(AC, "六、经济测算")
a7 = find_c(AC, "七、四个方向")
a10 = find_c(AC, "十、风险与应对")
L("B chapters:", [c["title"][:16] for c in BC])
L("B block counts:", {c["title"][:14]: len(c["blocks"]) for c in BC})
L("A block counts:", {c["title"][:14]: len(c["blocks"]) for c in AC})

# ── 源B 的文首（目录之前）与文尾 ──
lines = BT.split("\n")
i_c = next(i for i, l in enumerate(lines) if l.startswith("## 目录"))
i_1 = next(i for i, l in enumerate(lines) if l.startswith("## 一、"))
HEAD = "\n".join(lines[:i_c]).rstrip()
i_tail = next(i for i, l in enumerate(lines) if i > i_1 and (l.startswith("附件") or l.startswith("**附件") or l.startswith("抄送")))
TAIL = "\n".join(lines[i_tail:]).rstrip()
L("HEAD lines:", i_c, " TAIL from:", i_tail)
L("TAIL preview:", TAIL[:180].replace("\n", " | "))

CN = "\u96f6\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341"
def cn(n):
    return CN[n] if n <= 10 else str(n)
def strip_num(t):
    return re.sub(r"^\(?\d+(\.\d+)?\)?[\.、\uff09]?\s*", "", t).strip()
def strip_cn(t):
    return re.sub(r"^\uff08[^\uff09]+\uff09\s*", "", t).strip()

def emit(bl, lvl, num):
    t = strip_cn(strip_num(bl["title"]))
    head = ("### \uff08%s\uff09%s" % (cn(num), t)) if lvl == 3 else ("#### %d. %s" % (num, t))
    return head + "\n\n" + "\n".join(bl["body"]).strip("\n")

PLAN = [
 ("\u4e00\u3001\u7acb\u9879\u4f9d\u636e\u4e0e\u9879\u76ee\u6982\u8ff0", [
   ("B", b1, [0]), ("B", b1, [1]), ("B", b1, [2]), ("B", b1, [3])]),
 ("\u4e8c\u3001\u5e02\u573a\u8c03\u7814", [
   ("B", b2, list(range(len(b2["blocks"]))))]),
 ("\u4e09\u3001\u6539\u9020\u5fc5\u8981\u6027", [
   ("B", b3, list(range(len(b3["blocks"]))))]),
 ("\u56db\u3001\u6539\u9020\u53ef\u884c\u6027", [
   ("B", b4, [0]),
   ("A", a3, [0,1,2]),
   ("B", b4, [2]), ("B", b4, [3]), ("B", b4, [4]), ("B", b4, [5]), ("B", b4, [6])]),
 ("\u4e94\u3001\u6539\u9020\u65b9\u6848\u6bd4\u9009\u4e0e\u54c1\u724c\u9009\u62e9", [
   ("B", b5, [0]), ("B", b5, [1]), ("B", b5, [3]),
   ("A", a7, [2]), ("A", a7, [0]), ("A", a7, [1])]),
 ("\u516d\u3001\u6295\u8d44\u6784\u6210\u4e0e\u9690\u6027\u6210\u672c\u4e13\u9879", [
   ("A", a5, [0,1]), ("B", b6, [1]), ("B", b6, [2])]),
 ("\u4e03\u3001\u8d44\u91d1\u6765\u6e90\u4e0e\u5408\u4f5c\u6a21\u5f0f\u65b9\u5411", [
   ("B", b7, list(range(len(b7["blocks"]))))]),
 ("\u516b\u3001SWOT \u5206\u6790", [
   ("B", b8, list(range(len(b8["blocks"]))))]),
 ("\u4e5d\u3001\u7ecf\u6d4e\u6d4b\u7b97\u7ed3\u679c", [
   ("A", a6, list(range(len(a6["blocks"]))))]),
 ("\u5341\u3001\u98ce\u9669\u5206\u6790\u4e0e\u5e94\u5bf9", [
   ("A", a10, []), ("B", b10, [0,1])]),
 ("\u5341\u4e00\u3001\u7ed3\u8bba\u4e0e\u5efa\u8bae", [
   ("A", a1, [0,1,2])]),
]

OUT = []
TOC = []
for ctitle, groups in PLAN:
    OUT.append("## " + ctitle)
    TOC.append(ctitle)
    n = 0
    for src, ch, idxs in groups:
        blocks = ch["blocks"]
        if not blocks:
            n += 1
            OUT.append("### \uff08%s\uff09\u98ce\u9669\u6e05\u5355" % cn(n))
            OUT.append("\n".join(ch["raw"]).strip("\n"))
            continue
        for i in idxs:
            n += 1
            OUT.append(emit(blocks[i], 3, n))

TOC_BLOCK = "## \u76ee\u5f55\n\n" + "\n".join(
    ["%d. %s" % (i + 1, t) for i, t in enumerate(TOC)]) + "\n"

final = HEAD + "\n\n" + TOC_BLOCK + "\n\n" + "\n\n".join(OUT) + "\n\n" + TAIL
MD = os.path.join(KB, OUTF)
open(MD, "w", encoding="utf-8").write(final)
L("MD bytes:", len(final.encode("utf-8")), "emoji:", len(re.findall(EMOJI, final)))
bad = [l for l in final.split("\n") if l.startswith("#") and ("|" in l or "**" in l or len(l) > 95)]
L("heading issues:", len(bad))
for b in bad[:6]:
    L("  !", b[:110])
L("H2:", len([l for l in final.split("\n") if l.startswith("## ")]),
  "H3:", len([l for l in final.split("\n") if l.startswith("### ")]),
  "H4:", len([l for l in final.split("\n") if l.startswith("#### ")]))

sys.path.insert(0, r"D:\B166ER-openclaw\workspace\.tmp")
from md2docx_cn import convert
out = os.path.join(REP, "总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.docx")
convert(MD, out)
L("DOCX %.1f KB" % (os.path.getsize(out)/1024))
L("DONE")
