# -*- coding: utf-8 -*-
"""按集团汇报模板体例重排 + 补全 14 处空白格"""
import io, os, sys, re
T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "govfmt4.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
def esc(s): return s.encode("unicode_escape").decode("ascii")
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
MD = os.path.join(KB, "总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.md")
t = open(MD, encoding="utf-8").read()

# ══════════ 一、补全空白格（按行定位 + 列赋值）══════════
FILLS = [
 ("\u5bbe\u5ba2\u652f\u4ed8\u80fd\u529b", {1: "\u9ad8", 2: "\u4f4e"}),
 ("\u6210\u90fd\u5168\u5e02\u9ad8\u7aef\u9152\u5e97", {2: "\u603b\u5e9c\u73b0\u72b6 RevPAR 257.6 \u5143\uff0c\u4ec5\u4e3a 31%"}),
 ("\u603b\u5e9c\uff08\u73b0\u72b6\uff09", {2: "1996 \u5e74\u5efa\u6210\uff082014 \u5e74\u91cd\u88c5\uff09"}),
 ("Engineering", {1: "\u672a\u5355\u5217"}),
 ("FSMS", {1: "\u672a\u5355\u5217"}),
 ("Overall / \u4e0d\u5408\u89c4\u9879\u6570", {1: "\u672a\u5355\u5217\uff08\u5206\u9879\u6700\u9ad8 95.92%\uff09"}),
 ("\u827a\u672f\u54c1\u4e0e\u5728\u5730\u7b56\u5c55", {3: "\u6cbf\u7528\u7687\u51a0 3.0 \u65e0\u5f3a\u5236\uff1b\u6362\u54c1\u724c\u540e\u6309\u5728\u5730\u6587\u5316\u201c\u4e00\u5e97\u4e00\u7b56\u201d\u6295\u5165"}),
 ("\u5f00\u4e1a\u524d\u8d39\u7528 / \u80fd\u6e90\u8282\u80fd / \u666f\u89c2 / \u50a8\u6cb9", {3: "\u542b pre-opening \u8d39\uff08\u65b9\u5411\u4e09\uff09\u3001\u8282\u80fd\u6539\u9020\u3001\u666f\u89c2\u5ead\u9662\u3001\u50a8\u6cb9\u4e0e\u53d1\u7535\u5408\u89c4"}),
 ("\u5408\u8ba1", {3: "\u65b9\u5411\u4e09\u591a\u51fa\u6362\u724c\u4e13\u9879 2,600 \u4e07\u5143\uff08VI \u5168\u5957 + \u7cfb\u7edf\u91cd\u5efa + \u4f1a\u5458\u8fc7\u6e21 + \u5ba2\u7528\u54c1\u5e03\u8349\uff09"}),
 ("\u4e8c \u6cbf\u7528\u7687\u51a0 + 3 \u6539 2", {6: "\u4e0d\u8fbe\u6807"}),
 ("\u4e09 \u6362\u54c1\u724c + 3 \u6539 2", {6: "\u4e0d\u8fbe\u6807"}),
 ("R-24", {7: "\u6301\u7eed"}),
]
lines = t.split("\n")
filled = 0
for key, cells in FILLS:
    hit = None
    for i, l in enumerate(lines):
        if not l.startswith("|"):
            continue
        parts = l.split("|")
        if len(parts) < 3:
            continue
        if key in parts[1]:
            hit = i; break
    if hit is None:
        L("[MISS]", esc(key)); continue
    parts = lines[hit].split("|")
    for ci, val in cells.items():
        if ci < len(parts):
            parts[ci] = " " + val + " "
    lines[hit] = "|".join(parts)
    filled += 1
    L("[FILL]", esc(key), "->", esc(lines[hit][:120]))
L("filled rows:", filled, "/", len(FILLS))
t = "\n".join(lines)

# ══════════ 二、结论章加"一是/二是/三是/四是"段内分述 ══════════
anchor = "### \uff08\u4e00\uff09\u4e00\u53e5\u8bdd\u7ed3\u8bba"
PROSE = """
\u4e00\u662f\u6539\u9020\u5fc5\u8981\u6027\u6210\u7acb\u3002\u5168\u65b9\u6848\u4e0e\u4e09\u5e74\u54c1\u724c\u65b9\u5ba1\u8ba1\u8bb0\u5f55\u4e92\u76f8\u5370\u8bc1\uff1aIHG \u6807\u51c6\u7b26\u5408\u6027\u7531 2024 \u5e74 95.92% \u964d\u81f3 2026 \u5e74 69.6%\uff0c\u4e0d\u5408\u89c4\u9879\u7531 49 \u9879\u589e\u81f3 80 \u9879\uff1b\u524d\u5385\u5ba2\u8bc9\u4e2d\u8bbe\u65bd\u95ee\u9898\u5360 75.19%\uff0cOTA \u8bc4\u5206\u6263\u5206\u9879\u4e3a\u8bbe\u65bd\u3002\u540c\u65f6\uff0c\u89c4\u5212\u5df2\u5c06\u672c\u9879\u76ee\u5217\u4e3a\u56fd\u5bb6\u4e94\u661f\u5168\u670d\u52a1\u578b\u9152\u5e97\u6807\u6746\u3002

\u4e8c\u662f\u6539\u9020\u53ef\u884c\u6027\u6210\u7acb\u3002\u5ba2\u623f\u51cf\u623f\u81f3 268 \u95f4\u3001\u5957\u5185 40 \u33a1 \u4ee5\u4e0a\u540e\uff0c\u51cf\u623f\u540e\u5efa\u9762 84.5 \u33a1/\u95f4\uff0c\u65e2\u6709\u8d44\u4ea7\u53ef\u652f\u6491\u5b8c\u6574\u4ea7\u54c1\uff1b\u7535\u6c14\u4e3b\u4f9b 6,500KVA\u3001\u5907\u7528 3,250KVA\uff0c\u53d8\u538b\u5668\u4e0e\u53d1\u7535\u7ec4\u66f4\u65b0\u5fc5\u987b\u540c\u65f6\u89c4\u5212\u4e34\u65f6\u4f9b\u7535\u65b9\u6848\u3002

\u4e09\u662f\u505c\u4e1a\u4e0d\u53ef\u907f\uff0c\u4f46\u53ef\u538b\u7f29\u3002\u716c\u706b\u81ea\u52a8\u62a5\u8b66\u7cfb\u7edf\u3001\u55b7\u6dcb\u7ba1\u7f51\u4e0e\u51b7\u6e90\u4e3b\u673a\u4e09\u9879\u5c5e\u5168\u697c\u8054\u52a8\u7684\u786c\u7ea6\u675f\uff0c\u4e00\u6b21\u5168\u505c\u4e1a\u4e3a\u57fa\u51c6\u65b9\u6848\uff0818 \u4e2a\u6708\uff09\uff1b\u5206\u533a\u9a8c\u6536\u9700\u4e3a\u9a8c\u6536\u533a\u589e\u8bbe\u72ec\u7acb\u6d88\u9632\u8bbe\u65bd\uff0c\u53ef\u5c06\u505c\u4e1a\u538b\u7f29\u81f3 10 \u4e2a\u6708\uff0c\u505c\u4e1a\u635f\u5931\u51cf\u5c11\u7ea6 6,900 \u4e07\u5143\u3002

\u56db\u662f\u65b9\u5411\u9009\u62e9\u5df2\u660e\u786e\u3002\u6309\u56fd\u8d44\u59d4 10 \u5e74\u53e3\u5f84\uff08IRR \u5927\u4e8e 3.5%\u3001\u9759\u6001\u4e0e\u52a8\u6001\u56de\u6536\u671f\u5747\u4e0d\u8d85\u8fc7 10 \u5e74\uff09\u590d\u6838\uff0c\u201c\u6cbf\u7528\u7687\u51a0\u3001\u4e0d\u51cf\u623f\u201d\u4e0e\u201c\u6cbf\u7528\u7687\u51a0\u3001\u51cf\u623f\u201d\u5747\u4e0d\u8fbe\u6807\uff1b\u201c\u6362\u54c1\u724c\u3001\u4e0d\u51cf\u623f\u201d\u4e00\u7ec4\u5408\u662f\u552f\u4e00\u8fbe\u6807\u65b9\u6848\uff08IRR 9.58%\u3001\u9759\u6001 7.0 \u5e74\u3001\u52a8\u6001 9.6 \u5e74\uff09\u3002
"""
if anchor in t and "\u4e00\u662f\u6539\u9020\u5fc5\u8981\u6027\u6210\u7acb" not in t:
    t = t.replace(anchor, anchor + "\n" + PROSE, 1)
    L("inserted conclusion prose")
elif "\u4e00\u662f\u6539\u9020\u5fc5\u8981\u6027\u6210\u7acb" in t:
    L("prose already present")
else:
    L("[MISS] anchor for prose")

# 标题改"（讨论稿）"
t = t.replace("# \u5173\u4e8e\u603b\u5e9c\u7687\u51a0\u5047\u65e5\u9152\u5e97\u6539\u9020\u5347\u7ea7\u9879\u76ee\u7684\u53ef\u884c\u6027\u7814\u7a76\u62a5\u544a",
              "# \u603b\u5e9c\u7687\u51a0\u5047\u65e5\u9152\u5e97\u6539\u9020\u5347\u7ea7\u5de5\u4f5c\u601d\u8def\n\n## \uff08\u8ba8\u8bba\u7a3f\uff09", 1)

# ══════════ 三、封面改为「汇报材料汇编」式 + 重建目录 ══════════
i_c = t.find("## \u76ee\u5f55")
i_1 = t.find("## \u4e00\u3001")
assert i_c != -1 and i_1 != -1, (i_c, i_1)
h2s = [l[3:].strip() for l in t.split("\n") if l.startswith("## ") and not l.startswith("## \u76ee\u5f55")]
COVER = """**\u5185\u90e8\u8d44\u6599\u3000\u6ce8\u610f\u4fdd\u5b58**

---

# \u5b89\u9038\u9152\u5e97\u96c6\u56e2\u6709\u9650\u8d23\u4efb\u516c\u53f8

# \u603b\u5e9c\u7687\u51a0\u5047\u65e5\u9152\u5e97\u6539\u9020\u5347\u7ea7\u5de5\u4f5c\u601d\u8def

## \u6c47 \u62a5 \u6750 \u6599

\uff08\u8ba8\u8bba\u7a3f\uff09

2026 \u5e74 11 \u6708

---

## \u76ee\u5f55

"""
toc = "\n".join("%d. %s" % (i + 1, h) for i, h in enumerate(h2s)) + "\n\n---\n\n"
t = COVER + toc + t[i_1:]
open(MD, "w", encoding="utf-8").write(t)
L("MD bytes:", len(t.encode("utf-8")), " 目录条目:", len(h2s))

sys.path.insert(0, r"D:\B166ER-openclaw\workspace\.tmp")
from md2docx_cn import convert
out = os.path.join(REP, "总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.docx")
convert(MD, out)
L("DOCX %.1f KB" % (os.path.getsize(out)/1024))

# 复扫空白格
from docx import Document
d = Document(out)
n = 0
for ti, tb in enumerate(d.tables, 1):
    for ri, row in enumerate(tb.rows):
        for ci, cell in enumerate(row.cells):
            if cell.text.strip() in ("", "\u2014", "-", "\uff0f", "/"):
                n += 1
                L("  REMAIN 表%d 行%d 列%d" % (ti, ri, ci))
L("剩余空白格:", n)
