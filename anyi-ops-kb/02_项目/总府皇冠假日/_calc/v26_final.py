# -*- coding: utf-8 -*-
"""v26 收官：稳健定位第五章（六）；emoji 清零；表格空白填实；公文版式 Word；终检"""
import io, os, sys, re, json, glob, shutil
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
LOG = open(os.path.join(T, "v26.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
sys.path.insert(0, os.path.join(KB, "_calc"))

MD = os.path.join(KB, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
t = open(MD, encoding="utf-8").read()
L("=== 全部 ## 标题 ===")
for l in t.split("\n"):
    if l.startswith("## "):
        L("   " + l[:60])

# ══ ① 第五章（六）：按章节范围 + 小节标题稳健定位 ══════════════════════
m5 = re.search(r"^## 第五章 .*?(?=^## 第六章 )", t, re.M | re.S)
assert m5, "未定位第五章"
ch5 = t[m5.start():m5.end()]
sub_heads = [l for l in ch5.split("\n") if l.startswith("### ")]
L("第五章小节:", sub_heads)
m6 = re.search(r"^### （六）.*$", ch5, re.M)
CH5_SIX = r"""### （六）方向选择结论

**一，以 S1「沿用皇冠 + 公区保留石材 + 不减房」为五星档基准方案推进。** 改造投资 21,313.6 万元为九方案最低，改造后年收入 10,938.7 万元为改造前 6,774.0 万元的 1.61 倍（增量 4,164.7 万元每年），全口径内部收益率 4.60% 高于 3.5% 底线，可保留项节约 4,538.7 万元占改造投资 21.3%。须如实报集团的是：净现值 −6,002.9 万元、集团口径静态回收 10.15 年，均未进入 5 至 8 年参照区间。

**二，S4「洲至奢选 + 公区保留石材」为比价方案。** 收入倍数 2.07、增量 7,235.8 万元每年、全口径内部收益率 4.82%，均略优于 S1；但改造投资 28,190.7 万元、停业 15 个月，集团口径静态回收 9.88 年、净现值 −7,351.4 万元，仍未进入参照区间。

**三，S7B「外部奢牌 + 3 改 2」是唯一在全部判据上成立的方案，但三项前提须先验证。** 收入倍数 5.61、增量 31,229.1 万元每年、全口径内部收益率 11.33%、净现值 +16,916.8 万元、集团口径静态回收 6.11 年（落入区间）。三项前提：顶级设计型价格带（3,000 元）在总府位置可兑现；客房面积经 3 改 2 达到 40 平方米以上；品牌方接受全部改造投入结构。**任一不成立，结论即反转。**

**四，明确否决 S2 减房方案、S3 与 S5 公区拆除重做、S6 与 S8。** S2 收入增量仅 518.5 万元（1.08 倍）而投入不降；S3、S5 改造投入上升而收入不变（净现值 −14,454.7 与 −19,338.6 万元）；S6 净现值 −32,811.6 万元；S8 客房 25.35 平方米低于所有候选奢牌面积门槛。

**五，方案选择最终取决于两个尚未取得的结论。** 一是第三方安全评估对"消防与机电设备现状是否已无法满足经营条件与标准要求"的认定；二是外部奢牌顶级设计型价格带在总府位置的可兑现性。**在这两项结论取得前，本报告的方案比选结论应视为条件性结论。**

"""
if m6:
    # 从（六）小节到第五章末，整段替换
    ch5n = ch5[:m6.start()] + CH5_SIX.rstrip() + "\n\n"
    L("[MD] 第五章（六）已重写（原标题：%s）" % m6.group(0)[:24])
else:
    ch5n = ch5 + "\n" + CH5_SIX
    L("[MD] 未见（六）小节，已在章末追加")
t = t[:m5.start()] + ch5n + t[m5.end():]

# ══ ② emoji 清零 ══════════════════════════════════════════════════
EMO = "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\u24C2\u2B55]"
n_emo = len(re.findall(EMO, t))
hits = [l[:90] for l in t.split("\n") if re.search(EMO, l)]
for h in hits[:8]:
    L("   emoji行:", h.encode("unicode_escape").decode("ascii"))
t = re.sub(EMO + "+", "", t)
L("[MD] emoji 清除:", n_emo)

# ══ ③ 表格空白填实 ════════════════════════════════════════════════
lines = t.split("\n")
hdr = []; filled = 0; rows_fixed = []
for i, l in enumerate(lines):
    if l.startswith("|"):
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if not hdr and cells and set("".join(cells)) <= set("-: "):
            hdr = cells; continue
        if hdr and len(cells) == len(hdr):
            new = []
            for ci, c in enumerate(cells):
                if c in ("", "—", "-"):
                    col = hdr[ci] if ci < len(hdr) else ""
                    rep = "未公开披露" if ("房量" in col or "数量" in col or "间）" in col or "客房数" in col) else "不适用"
                    new.append(rep); filled += 1
                    rows_fixed.append((i + 1, hdr[ci] if ci < len(hdr) else "", rep))
                else:
                    new.append(c)
            lines[i] = "| " + " | ".join(new) + " |"
        continue
    hdr = []
t = "\n".join(lines)
L("[MD] 表格空白填充:", filled)
for r_ in rows_fixed[:12]:
    L("   L%d 列[%s] -> %s" % r_)

open(MD, "w", encoding="utf-8").write(t)
L("MD bytes:", len(t.encode("utf-8")))

# ══ ④ 公文版式 Word（复用 v17 已验证逻辑，仅换输入输出路径）══════════════
D = os.path.join(KB, "_calc")
src = open(os.path.join(D, "v17_docx.py"), encoding="utf-8").read()
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.md", "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.docx", "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.docx")
open(os.path.join(D, "v17_docx_v3.py"), "w", encoding="utf-8").write(src)
os.system('"%s" "%s" > "%s" 2>&1' % (
    r"C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe",
    os.path.join(D, "v17_docx_v3.py"), os.path.join(T, "v17v3.out")))
lg = os.path.join(T, "v17.log")
if os.path.exists(lg):
    for l in open(lg, encoding="utf-8", errors="replace").read().split("\n"):
        if l.strip():
            L(l.rstrip())
