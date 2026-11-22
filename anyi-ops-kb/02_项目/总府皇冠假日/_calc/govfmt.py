# -*- coding: utf-8 -*-
"""整体方案报告 -> 公文范式 · 修正版 2（修 \s 吞换行导致标题粘连）"""
import io, os, sys, re
T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "govfmt.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
SRC = os.path.join(KB, "总府皇冠改造_整体方案报告_v1.0_2026-11-13.md")
MD  = os.path.join(KB, "总府皇冠改造_整体方案报告_公文版_v1.0_2026-11-13.md")

src = open(SRC, encoding="utf-8").read()
L("source bytes:", len(src.encode("utf-8")))

# 1) 去 emoji（非 raw 字符串，\U 才生效）
EMOJI = "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\u24C2\u2B55]"
n0 = len(re.findall(EMOJI, src))
src = re.sub(EMOJI + "+", "", src)
L("emoji:", n0, "->", len(re.findall(EMOJI, src)))

# 2) 清理（只用 [ \t]，绝不跨行）
src = re.sub(r"[ \t]+\n", "\n", src)
src = re.sub(r"\n{3,}", "\n\n", src)
src = src.replace("**——**", "——")
src = re.sub(r"\*\*[ \t]+", "**", src)
src = re.sub(r"[ \t]+\*\*", "**", src)
src = re.sub(r"\*\*[ \t]*\*\*", "", src)

# 3) 拆正文
body = []
started = False
for l in src.split("\n"):
    if not started:
        if l.startswith("## 一、结论与建议"):
            started = True
        else:
            continue
    body.append(l)
body = "\n".join(body).strip()

# 4) 标题层级公文化（每节重新编号）
def cn(n):
    return "\u96f6\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341"[n] if n <= 10 else str(n)
sub = 0
out = []
for l in body.split("\n"):
    if l.startswith("## "):
        sub = 0
        out.append(l); continue
    m3 = re.match(r"^### (\d+)\.(\d+)[ \t]*(.*)$", l)
    m4 = re.match(r"^#### (\d+)\.(\d+)[ \t]*(.*)$", l)
    if m3:
        sub += 1
        out.append("### \uff08%s\uff09%s" % (cn(sub), m3.group(3).strip()))
        continue
    if m4:
        out.append("#### %d. %s" % (sub, m4.group(3).strip()))
        continue
    out.append(l)
body = "\n".join(out)

# 5) 标题完整性自检
bad = [l for l in body.split("\n") if l.startswith("#") and ("|" in l or "**" in l or len(l) > 90)]
L("heading integrity issues:", len(bad))
for b in bad[:6]:
    L("  !", b[:110])
L("H2 count:", len([l for l in body.split("\n") if l.startswith("## ")]),
  " H3 count:", len([l for l in body.split("\n") if l.startswith("### ")]),
  " H4 count:", len([l for l in body.split("\n") if l.startswith("#### ")]))

HEAD = """**\u5185\u90e8\u8d44\u6599\u3000\u6ce8\u610f\u4fdd\u5bc6**\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u4efd\u53f7\uff1a000001

# \u5b89\u9038\u9152\u5e97\u96c6\u56e2\u6587\u4ef6

**\u5b89\u9038\u4ea7\u53d1\u30142026\u3015\u603b\u5e9c\u6539\u9020\u65b9\u6848\u7b2c 001 \u53f7**

\u7b7e\u53d1\u4eba\uff1a

# \u5173\u4e8e\u603b\u5e9c\u7687\u51a0\u5047\u65e5\u9152\u5e97\u6539\u9020\u5347\u7ea7\u6574\u4f53\u65b9\u6848\u7684\u62a5\u544a

\u4e3b\u9001\uff1a\u5b89\u9038\u9152\u5e97\u96c6\u56e2\u51b3\u7b56\u5c42\u3002

\u5404\u6709\u5173\u5355\u4f4d\uff1a

"""

TAIL = """
\u7279\u6b64\u62a5\u544a\u3002

## \u9644\u4ef6\u8bf4\u660e

1. \u300a\u603b\u5e9c\u7687\u51a0\u6539\u9020_\u7acb\u9879\u65b9\u6848_\u7ec6\u9879\u6982\u7b97\u8868\u300b\uff082026 \u5e74 11 \u6708 13 \u65e5\uff0c12 \u4e2a\u5de5\u4f5c\u8868\uff09
2. \u300a\u603b\u5e9c\u7687\u51a0\u6539\u9020_\u53ef\u884c\u6027\u7814\u7a76\u62a5\u544a\uff08\u516c\u6587\u7248\uff09\u300b\uff082026 \u5e74 11 \u6708 9 \u65e5\uff09
3. \u300a\u603b\u5e9c\u7687\u51a0\u6539\u9020_\u7b2c\u4e8c\u6279\u6b21\u8d44\u6599\u5438\u6536\u4e0e\u7ed3\u8bba\u4fee\u8ba2\u62a5\u544a\u300b\uff082026 \u5e74 11 \u6708 10 \u65e5\uff09
4. \u300a\u603b\u5e9c\u7687\u51a0\u6539\u9020_\u7efc\u5408\u6539\u9020\u62a5\u544a\u300b\u7b2c\u4e00\u81f3\u5341\u4e00\u6b21\u90e8\u5206

## \u6284\u9001

\u56db\u5ddd\u603b\u5e9c\u5b9e\u4e1a\u6709\u9650\u516c\u53f8\uff0c\u96c6\u56e2\u8d22\u52a1\u90e8\uff0c\u96c6\u56e2\u5de5\u7a0b\u90e8\uff0c\u96c6\u56e2\u603b\u7ecf\u7406\u529e\u516c\u5ba4\uff0c\u96c6\u56e2\u6cd5\u5f8b\u5408\u89c4\u90e8\u3002

\u56db\u5ddd\u5bbe\u9986\u96c6\u56e2\uff08\u5b89\u9038\u9152\u5e97\u96c6\u56e2\uff09\u4ea7\u4e1a\u53d1\u5c55\u90e8\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u2026 \u5e74 11 \u6708 13 \u65e5

\u5370\u53d1\u673a\u5173\uff1a\u56db\u5ddd\u5bbe\u9986\u96c6\u56e2\uff08\u5b89\u9038\u9152\u5e97\u96c6\u56e2\uff09\u4ea7\u4e1a\u53d1\u5c55\u90e8\u3000\u3000\u3000\u5370\u53d1\u65e5\u671f\uff1a2026 \u5e74 11 \u6708 13 \u65e5
"""

final = HEAD + body + TAIL
open(MD, "w", encoding="utf-8").write(final)
L("MD", len(final.encode("utf-8")), "bytes")
L("final emoji:", len(re.findall(EMOJI, final)))

sys.path.insert(0, r"D:\B166ER-openclaw\workspace\.tmp")
from md2docx_cn import convert
out = os.path.join(REP, "总府皇冠改造_整体方案报告_公文版_v1.0_2026-11-13.docx")
convert(MD, out)
L("DOCX %.1f KB" % (os.path.getsize(out)/1024))

MEM = r"D:\B166ER-openclaw\workspace\memory\2026-11-13.md"
t2 = open(MEM, encoding="utf-8").read()
t2 = t2.replace("\uff08\u9996\u6b21\u8f6c\u6362\u56e0 raw string \u4e2d \\U \u672a\u751f\u6548\u800c\u9057\u6f0f\uff0c\u5df2\u4fee\u6b63\u91cd\u51fa\uff09",
 "\uff08\u4fee\u6b63\u4e24\u6b21\uff1a\u2460 raw string \u4e2d \\U \u672a\u751f\u6548 \u2192 emoji \u672a\u5220\u6389\uff1b\u2461 \u6e05\u7406\u6b63\u5219\u7528\u7684 \\s \u541e\u6389\u6362\u884c\uff0c\u5bfc\u81f4\u6807\u9898\u4e0e\u6b63\u6587\u7c98\u8fde\u3001\u5c0f\u8282\u4e22\u5931\uff1b\u5df2\u4fee\u6b63\u91cd\u51fa\uff09")
open(MEM, "w", encoding="utf-8").write(t2)
L("DONE")
