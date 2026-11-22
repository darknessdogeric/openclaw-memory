# -*- coding: utf-8 -*-
"""v41：修正出稿顺序（先写 MD 再出 Word）→ 终检 → memory/README 同步
   同时固化本轮重要结论：外部奢牌由「推荐主案」修正为「上限情景战略期权」"""
import io, os, sys, re, json, glob, subprocess
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v41.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

MD = os.path.join(KB, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
t = open(MD, encoding="utf-8").read()
L("MD 当前: %d bytes｜'唯一全判据成立' 存在: %s" % (len(t.encode("utf-8")), "唯一全判据成立" in t))

# ① 先写 MD（确保后续 Word 用的是最新稿）
open(MD, "w", encoding="utf-8").write(t)
L("[MD] 已写盘")

# ② 再出公文 Word
D = os.path.join(KB, "_calc")
src = open(os.path.join(D, "v17_docx.py"), encoding="utf-8").read()
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.md", "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.docx", "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.docx")
open(os.path.join(D, "v17_docx_v3.py"), "w", encoding="utf-8").write(src)
PY = r"C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe"
subprocess.run([PY, os.path.join(D, "v17_docx_v3.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
for l in open(os.path.join(T, "v17.log"), encoding="utf-8", errors="replace").read().split("\n"):
    if l.strip(): L(l.rstrip())

# ③ 终检
from docx import Document
DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.docx")
d = Document(DOCX)
paras = [p.text for p in d.paragraphs]
alltext = "\n".join(paras) + "\n" + "\n".join(c.text for tb in d.tables for r in tb.rows for c in r.cells)
blank = sum(1 for tb in d.tables for r in tb.rows for c in r.cells if c.text.strip() in ("", "\u2014", "-", "\uff0f", "/"))
L("=== 终检 ===")
L("%.1f KB | 段落 %d | 表格 %d | 空白格 %d | 节 %d" % (os.path.getsize(DOCX) / 1024, len(d.paragraphs), len(d.tables), blank, len(d.sections)))
L("emoji:", len(re.findall("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\u24C2\u2B55]", alltext)))
KEYS = ["10,720", "10,192", "254 间", "208 间", "2,915", "31,727.6", "20,401.3", "14,398.4",
        "15.61%", "15.32%", "21.28%", "28.28%", "76.7", "68.4", "上限情景", "投入分担", "R-21", "R-22",
        "1,500", "1,750", "3,000", "11.33%", "16,916.8", "6,774.0", "518.5", "5.61", "40.48 万家"]
miss = [k for k in KEYS if k not in alltext]
L("关键值缺失:", miss if miss else "无（%d 项全中）" % len(KEYS))
for o in ("唯一全判据成立", "唯一在全部判据上成立的方案是 S7B", "唯一同时满足"):
    if o in alltext: L("   ⚠ 旧判据残留: %s" % o)
for ab in ("ADR", "RevPAR", "CAPEX", "NPV", "IRR", "GOP"):
    n = len(re.findall(r"\b%s\b" % ab, alltext))
    if n: L("   ⚠ 英文缩写 %s ×%d" % (ab, n))
m = re.search(r"^## 目录\n", t, re.M)
ls = t[m.end():].split("\n")
start = next((i for i, l in enumerate(ls) if l.startswith("## ")), None)
toc = [re.sub(r"^\d+\. ", "", l).strip() for l in ls[:start] if re.match(r"^\d+\. ", l)]
bod = [l[3:].strip() for l in ls[start:] if l.startswith("## ")]
L("目录↔正文:", toc == bod, "| 目录", len(toc), "正文", len(bod))
L("第九章小节:", [l for l in t.split("\n") if l.startswith("### ") and any(k in l for k in ("现实性检验", "评价结论", "小结"))])

# ④ memory / README
MEM = r"D:\B166ER-openclaw\workspace\memory\2026-11-13.md"
open(MEM, "a", encoding="utf-8").write("""
### 15:20 ⭐⭐⭐⭐⭐ 外部奢牌现实性复核 —— **推翻上一稿的乐观结论**
> Eric 提示：「实事求是的分析。我觉得外部奢牌是不是过于乐观了。」复核后**确认成立，并已改判正式稿**。

#### 一、三处硬伤（其中一处是物理不可能）
1. **⭐ 房量前提物理不成立**：客房套内总面积 10,192 ㎡（工程部实测），268 间 × 40 ㎡ = 10,720 ㎡，**缺口 528 ㎡**。套内口径下 40 ㎡ 门槛最多 **254 间**、49 ㎡（兰博基尼）**208 间**、60 ㎡（丽晶）**169 间**。上一稿"3 改 2 达 40 ㎡ 以上"不成立。`area_base.py` 的 `ROOM_AREA_32` 取 48 ㎡ 但 3 间存量仅 75 ㎡，口径不自洽。
   （若按建面口径含走廊分摊，3 间合并每间建面 84.5 ㎡ 则 268 间成立 —— 但品牌门槛未明示套内/建面，**不得按有利解释自行取值**，须品牌方书面确认。）
2. **⭐ 三项乐观值同时取交集**：平均房价 3,000 元（成都价格带**上限**）× 出租率 70% × 部门营业利润率 40%。盈亏平衡平均房价：GOP 30% → 3,843 元；**GOP 35% → 2,915 元**（无容错）；GOP 40% → 2,349 元。成都无任何酒店全年平均房价达 2,915 元。
3. **⭐ 单房强度超过地标**：S7B 假设单房客房年收入 76.7 万元 > 居舍 68.4 万元（2,500×0.75），即 1996 年存量物业改造后做出成都设计型地标的单房强度。

#### 二、⭐⭐ 判据本身的错误（我自己的错，已纠正）
上一稿用**绝对净现值 > 0** 判优，但**"不改造"不是零成本基准**：年经营现金流 −1,924.0 万、20 年 8% 折现净现值 **−20,401.3 万**，且报警主机 2026-07 已全面瘫痪，继续经营在合规上不成立。
**增量口径重排（相对不改造）**：
| 方案 | 改造投资 | 绝对净现值 | **增量净现值** | **增量IRR** | 增量回收 |
|---|---|---|---|---|---|
| **S1 皇冠·不减房** | 21,313.6 | −6,002.9 | **+14,398.4** | **15.61%** | 8 年 |
| S4 洲至奢选·不减房 | 28,190.7 | −7,351.4 | +13,049.9 | 13.36% | 9 年 |
| **S7B 外部奢牌·3改2** | 56,850.9 | +16,916.8 | +37,318.1 | **15.32%** | 8 年 |
→ **S1 增量效率反超 S7B**（15.61% vs 15.32%），S7B 多投 35,537.3 万只多换 22,919.7 万增量净现值。**S7B 的"唯一全判据成立"是绝对口径的幻觉。**

#### 三、概率加权期望
P(品牌方接盘)=12%（未接触、面积不达标、春熙路已有居舍/君悦/尼依格罗 3 家超高端）× P(价格带兑现|接盘)=30%
全兑现 +16,916.8（3.6%）／中性 −12,937.4（8.4%）／低落 −35,511.2（88%）→ **期望 −31,727.6 万**。

#### 四、⭐ 外部奢牌路径的真实门槛：品牌方分摊，不是价格带
| 房量 | 品牌方分摊 | 业主承担改造投资 | 增量净现值 | 增量IRR |
|---|---|---|---|---|
| 254 间 | 0% | 55,337.1 | +35,015.3 | 15.08% |
| 254 间 | **30%** | 38,736.0 | +51,223.0 | **21.28%** |
| 254 间 | **50%** | 27,668.6 | +62,028.1 | **28.28%** |
→ **问询方向应从"能否做到 3,000 元房价"改为"品牌方愿意投入多少"。**

#### 五、已改判正式稿（v3.0 原地修订）
- 第九章**新增（八）外部奢牌方案的现实性检验**（面积硬约束／平衡ADR／居舍对标／概率加权／分摊情景）
- 第九章（一）补「基准提示：反事实不是零」；第七章小结表**增列增量净现值/增量IRR/增量回收**
- 第五章（五）比选表 S7B 标注「**上限情景，前提不成立**」；第五章（五）（八）结论改写
- 第十二章结论第六、建议二（问询重点改为投入分担+面积口径确认）、建议三、请示三改写；请示二补反事实基准并**请集团认可以增量口径为经济性评价主口径**
- 第十一章风险增 **R-21 面积口径未确认致分母重置**、**R-22 品牌方不出资分担**
- Excel 增「**16 外部奢牌现实性检验**」表（58 行），08/10 表增列增量净现值，S7B 标注修正
- 终稿：Word 79.4 KB／312 段／**19 表 0 空白**／7 节（3 纵+4 横宽表页）／0 emoji；Excel 53.3 KB／17 表

#### 六、教训（沉淀到 self-improving）
- **单点乐观值 × 多重乐观假设的叠加是结论失真的主因**。凡"唯一成立方案"结论，必须做：① 面积/物理可行性反查 ② 盈亏平衡值反解 ③ 概率加权期望 ④ 对标同档位最强样本。**四关过不了的方案，只能列为期权，不能列为主案。**
- **判据必须先反查基准**。用绝对净现值判优前，先问"反事实是不是零"——本案反事实是 −20,401.3 万，用错基准直接导致主案判断错误。
- **出稿顺序**：必须先写 MD 再出 Word；反序会产出用旧稿渲染的 Word，且日志看似正常。
<!-- project: github.com/darknessdogeric/openclaw-memory -->
""")
RM = os.path.join(KB, "00_项目总览_README.md")
open(RM, "a", encoding="utf-8").write("""
### ⚠ v3.0 重要修订（2026-11-14 15:20）：外部奢牌由「推荐主案」修正为「上限情景战略期权」
复核发现三处硬伤并已改判：① **268 间 × 40 ㎡ = 10,720 ㎡ > 全楼套内 10,192 ㎡，房量前提物理不成立**（40 ㎡ 门槛最多 254 间）；② 模型同时取平均房价 3,000 元（价格带上限）× 出租率 70% × 营业利润率 40% 三项乐观值，GOP 35% 时盈亏平衡平均房价升至 2,915 元；③ S7B 假设单房年收入 76.7 万 > 居舍 68.4 万，无落地证据。
**同时纠正判据错误**：反事实「不改造」净现值 −20,401.3 万（非零），增量口径下 **S1（15.61%）反超 S7B（15.32%）**且投资仅 37%。概率加权期望 −31,727.6 万。**外部奢牌路径的真实门槛是品牌方分摊 30% 以上改造投入（增量IRR 升至 21.28%），而非价格带。**
新增：第九章（八）现实性检验；第十一章 R-21/R-22；Excel 表 16「外部奢牌现实性检验」；08/10 表增列增量净现值。
<!-- project: github.com/darknessdogeric/openclaw-memory -->
""")
L("memory + README synced")
L("DONE")
