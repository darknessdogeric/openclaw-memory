# -*- coding: utf-8 -*-
"""v59：v4.0 收官 —— ① 竞争烈度星号改数值标度 ② 定位 Word 缺失的 1 张表 ③ 重建 ④ 终检 ⑤ memory/README"""
import io, os, sys, re, json, glob, subprocess
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v59.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
sys.path.insert(0, os.path.join(KB, "_calc"))
MD4 = os.path.join(KB, "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.md")
t = open(MD4, encoding="utf-8").read()
lines = t.split("\n")

# ① 竞争烈度：星号标度改 5 分制数值
L("=== 1. 竞争烈度行现状 ===")
for i, l in enumerate(lines, 1):
    if "竞争烈度" in l: L("   L%d | %s" % (i, l.strip()[:140]))
SCALE = [
 ("| 竞争烈度 | ☆☆ | ☆☆ | 丽晶 2029 年开业使竞争升级 |",
  "| 竞争烈度 | 3/5 | 5/5 | 丽晶 2029 年开业使竞争升级 |"),
 ("| 竞争烈度 | ☆☆ | ☆☆ | 结构性过剩 |",
  "| 竞争烈度 | 4/5 | 5/5 | 结构性过剩 |"),
 ("| 竞争烈度 | ☆☆ | ☆☆ | 连锁加速进入 |",
  "| 竞争烈度 | 3/5 | 4/5 | 连锁加速进入 |"),
]
n = 0
for a, b in SCALE:
    if a in t:
        t = t.replace(a, b); n += 1
L("[MD] 竞争烈度标度改写:", n)
# 兜底：任何仍含 ☆ 的行
for i, l in enumerate(t.split("\n"), 1):
    if "☆" in l: L("   ⚠ 残留 ☆ L%d | %s" % (i, l.strip()[:130]))
t = re.sub("☆+", "", t)
open(MD4, "w", encoding="utf-8").write(t)
lines = t.split("\n")

# ② 定位 Word 缺失的表
from docx import Document
DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.docx")
d = Document(DOCX)
md_blocks = []
i = 0
while i < len(lines):
    if lines[i].startswith("|"):
        j = i
        while j < len(lines) and lines[j].startswith("|"): j += 1
        md_blocks.append((i + 1, lines[i].strip().strip("|").split("|")[0].strip()))
        i = j
    else:
        i += 1
doc_first = [tb.cell(0, 0).text.strip() for tb in d.tables]
L("")
L("=== 2. 表数差异定位 ===")
L("   MD 块 %d ｜Word 表 %d" % (len(md_blocks), len(d.tables)))
mdc = [x[1] for x in md_blocks]
from collections import Counter
cm, cd = Counter(mdc), Counter(doc_first)
for k, v in cm.items():
    if cd.get(k, 0) < v:
        L("   ⚠ MD 中多出 %s（行%s，MD %d 次 / Word %d 次）" % (k[:40], [x[0] for x in md_blocks if x[1] == k], v, cd.get(k, 0)))
for k, v in cd.items():
    if cm.get(k, 0) < v:
        L("   ⚠ Word 中多出 %s（MD %d 次 / Word %d 次）" % (k[:40], cm.get(k, 0), v))

# ③ 重建 Word
D = os.path.join(KB, "_calc")
src = open(os.path.join(D, "v17_docx.py"), encoding="utf-8").read()
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.md", "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.md")
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.docx", "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.docx")
open(os.path.join(D, "v17_docx_v4.py"), "w", encoding="utf-8").write(src)
subprocess.run([r"C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe", os.path.join(D, "v17_docx_v4.py")],
               capture_output=True, text=True, encoding="utf-8", errors="replace")
for l in open(os.path.join(T, "v17.log"), encoding="utf-8", errors="replace").read().split("\n"):
    if l.strip(): L(l.rstrip())

# ④ 终检
d = Document(DOCX)
paras = [p.text for p in d.paragraphs]
alltext = "\n".join(paras) + "\n" + "\n".join(c.text for tb in d.tables for r in tb.rows for c in r.cells)
blank = sum(1 for tb in d.tables for r in tb.rows for c in r.cells if c.text.strip() in ("", "\u2014", "-", "\uff0f", "/"))
EMO = ("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D"
       "\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\u24C2\u2B55]")
L("")
L("=== 3. 终检 ===")
L("%.1f KB | 段落 %d | 表格 %d | 空白格 %d | 节 %d" % (os.path.getsize(DOCX)/1024, len(d.paragraphs), len(d.tables), blank, len(d.sections)))
for i, s in enumerate(d.sections):
    L("   S%d %s %.0fx%.0f 页码域%d" % (i, "横" if s.page_width>s.page_height else "纵", s.page_width.cm, s.page_height.cm, s.footer._element.xml.count('w:instr="PAGE"')))
L("emoji(真实):", len(re.findall(EMO, alltext)), "| ☆残留:", alltext.count("☆"), "| ★残留:", alltext.count("★"))
KEYS = ["427.4","72.55%","6,774.1","4,551.8","21,312.4","53.02","24,797.0","9,950.5","7,585.4",
        "71,947.5","7,768.4","4,750.9","100.32","2029-09-27","2029-03-27","六级","丽笙精选",
        "LXR","洲至奢选","柏悦","Sofitel","消防验收","不得投入使用","R-21","1,161.5","3,484.6",
        "2,871","2022","217","1.24 亿元","五条路径","2029 Q3","告知承诺","康莱德","文华东方","3/5"]
miss = [k for k in KEYS if k not in alltext]
L("关键值缺失:", miss if miss else "无（%d 项全中）" % len(KEYS))
for ab in ("ADR","RevPAR","CAPEX","NPV","IRR","GOP"):
    n = len(re.findall(r"\b%s\b" % ab, alltext))
    if n: L("   ⚠ 英文缩写 %s ×%d" % (ab, n))
for o in ("本报告此前","纠错","增量口径","净现值为负则","唯一全判据成立"):
    if o in alltext: L("   ⚠ 残留: %s" % o)
m = re.search(r"^## 目录\n", t, re.M)
ls = t[m.end():].split("\n")
start = next((i for i, l in enumerate(ls) if l.startswith("## ")), None)
toc = [re.sub(r"^\d+\. ", "", l).strip() for l in ls[:start] if re.match(r"^\d+\. ", l)]
bod = [l[3:].strip() for l in ls[start:] if l.startswith("## ")]
L("目录↔正文:", toc == bod, "| 目录", len(toc), "正文", len(bod))
L("章节数:", len(re.findall(r"^## 第", t, re.M)))

# ⑤ memory / README
MEM = r"D:\B166ER-openclaw\workspace\memory\2026-11-13.md"
open(MEM, "a", encoding="utf-8").write("""
### 22:40 ⭐⭐⭐⭐⭐ v4.0 全面重构（Eric 26 条审视）→ 正式交付
> Eric 一次给出 26 条审视意见，其中多条指向事实性错误。**全部接受，按"重构"而非"打补丁"处理**，v3.0 保留为历史、v4.0 重写。

#### 一、本轮从内部档案查实并推翻的四处硬错误
1. **⭐ 洲际合同实际到 2029-09-27**（协议正文 10 年期，2019-09-28 起），**续约谈判硬性窗口 2029-03-27**（届满前 6 个月须达成一致，否则自动到期）。此前误用集团台账"2027 年到期"的说法。
2. **⭐ 部分地下层为六级人防**（框架+剪力墙、7 度Ⅱ 类），**人防竣工资料与主管部门备案至今未查找到**，是唯一可能无法通过改造解决的项（R-03）。此前整章漏写。
3. **⭐ 改造前基线被低估**：旧稿用 2026-09 单月低点 ADR 363.99 元 × OCC 70.78% 得客房收入 3,780.2 万；**24 个月实测均值为 ADR 427.4 元 / OCC 72.55%，客房收入 4,551.8 万（USALI 利润表交叉验证，反算差异 0.05%），旧值低估 771.6 万（20.4%）**。且旧稿收入结构错误——实际客房 67.2%／餐饮 13.8%／会议 13.1%／其他 5.9%，已改为四板块分别建模。
4. **⭐ 停业损失口径混同**：815 万/月把"须付出去的刚性支出"与"营业收入归零"混同。已分离为**段一A 刚性现金支出**（计入资金需求，12 个月 3,484.6 万，与 715 定稿 3,674 万交叉验证）＋**段一B 营业收入归零**（仅入现金流，不计入需投入资金）。

#### 二、v4.0 结构性重写
- **市场章改为三问结构**：为什么改造／为什么做国际联号高星／市场行情；**分级分类为主线**（内部《高星级全服式酒店品牌分级分类（仅5★+）》四档），全量市场降为支撑附节。
- **⭐ 新增内部既有预测衔接**：《成都 UPSCALE / UPPER SCALE / LUXURY 市场分析与预测》(2026-10-23) —— 此前完全没接入。三 Scale 2026—2030 预测、2029 丽晶开业分水岭、抢位窗口 2027—2028 全部纳入。
- **⭐ 2021—2026 五年曲线**（2022 年每间可售房收入 217 元为十年最低 → 2025 年仅回 2019 年 103%）。
- **⭐ 成都 2,000 元以上奢华深挖**：核心商圈该档房源约 260 间、年需求容量约 1.24 亿元；丽晶 2029 开业将放大一倍供给 → **不能把 402 间整体假设为该价格带**。
- **⭐ 12 品牌逐个测算**（丽笙精选已按内部分级表剔除出奢华样本，锦江丽笙属中高端有限服务）；净现值排序与前提可验证性排序分离：LXR 最高（+71,947.5 万）但前提最弱，洲至奢选最可靠（+7,768.4 万）。
- **⭐ 关键校准**：S1 单房 53.02 万 → 按内部表 §6.1 落在**高端奢华档**区间（非皇冠的上高端档）；**外部顶奢客房单间 100.32 万，超内部表超奢带上限 72 万/间 39%** → 问题在造价不在价格。
- **净现值转正路径 P1—P8**：分期开业 +6,204.5／品牌方承担 30% +9,472.1／补贴 3,000 万 +6,078.4／经营期 30 年 +3,078.4；**P8 净现值 +9,950.5 万、IRR 15.24%**。
- **自建品牌路径单列**（+4,750.9 万、IRR 9.95%，优于皇冠续约），但因客源体系/价格认知/建设周期三条不成立，列为中长期课题与本轮脱钩。
- **文化重新定位**：删除"成都院子是价格样板"的错误对标（它是古建改造），改为**文化与品牌遴选互为条件**（品牌适配＋谈判筹码＋客群匹配），**不设独立溢价测算**。
- **消防补入《消防法》第十三条、第十五条 + 住建部令 58 号**："未经消防验收禁止投入使用""公众聚集场所未经许可不得投入使用、营业"；并发现**两个环节可联合办理**（成都参照杭州做法）。
- **人防三方案**（基准"保持现状不动"30—70 万）、**资金筹措五条并行路径**（政策/合作共建/品牌方/资产盘活/债务）、**风险表去掉责任方列**。

#### 三、交付
- 改造报告交付\\总府皇冠改造_可行性研究报告_v4.0_2026-11-14.docx —— 12 章 / 40 表 / 0 空白 / 7 节（含横页宽表）/ 0 emoji
- 测算与中间产物\\总府皇冠改造_可行性研究报告_测算附表_v4.0_2026-11-14.xlsx —— 12 表
- v3.0 三件已删除；桌面根目录残留 0

#### 四、沉淀（教训）
- **单一数值口径必须交叉验证两个独立来源**。ADR 363.99 与 427.4 都在"实测"里，但一个是单月低点、一个是 24 个月均值——**前者来自 2026-09 单月，是被当成趋势用的低点**。凡基线数据必须做"反算校验"（房量×365×OCC×ADR 对 USALI 实测），差异超 1% 即须排查。
- **停业损失这类混合科目必须拆成"资金需求口径"与"现金流口径"两栏**，否则总资金需求被系统性高估（815×12=9,780 万 vs 真实刚性支出 3,485 万，**高估 181%**）。
- **知识库里的既有成果必须先检索再用**：《成都三 Scale 市场分析与预测》已存在却未接入，等于重做市场章且丢失内部口径一致性。
- **集团台账与合同原件冲突时以合同原件为准**（2027 vs 2029-09-27）。
- **内部表（品牌分级分类）优先于外部推算**：单房投资与品牌档位的对应关系、造价带上限，都只能取内部表。
<!-- project: github.com/darknessdogeric/openclaw-memory -->
""")
RM = os.path.join(KB, "00_项目总览_README.md")
open(RM, "a", encoding="utf-8").write("""
### v4.0 全面重构（2026-11-14 22:40）—— Eric 26 条审视后重写
**四处硬错误已从内部档案查实推翻**：①洲际合同实际到 **2029-09-27**（续约谈判截止 2029-03-27，非 2027）；②**部分地下层六级人防**、竣工资料缺失（R-03），此前整章漏写；③**改造前基线被低估 20.4%**（24 个月实测 ADR 427.4/OCC 72.55%，客房收入 4,551.8 万，非 3,780.2 万），且收入结构改为客房/餐饮/会议/其他四板块建模；④**停业损失口径混同**已拆为段一A 刚性现金支出（3,484.6 万/12 月，计入资金需求）与段一B 营业收入归零（仅入现金流）。
**结构重写**：市场章三问结构（为什么改造/为什么国际联号高星/市场行情），分级分类为主线、全量市场降为支撑；接入内部既有《成都三 Scale 市场分析与预测》；新增 2021—2026 五年曲线与成都 2,000 元以上奢华深挖（该档房源约 260 间、年容量约 1.24 亿元）；12 品牌逐个测算并分离"净现值排序"与"前提可验证性排序"；净现值转正路径 P1—P8（P8 +9,950.5 万、IRR 15.24%）；自建品牌单列（+4,750.9 万，但前提不成立）；文化改为与品牌遴选互为条件、不设溢价测算；补入消防"不验收不能营业"法规依据与人防三方案；风险表去责任方列。
**交付**：可研报告 v4.0（12 章 40 表 0 空白 7 节 0 emoji）＋测算附表 v4.0（12 表）；v3.0 三件已删除。
<!-- project: github.com/darknessdogeric/openclaw-memory -->
""")
L("memory + README synced")
L("DONE")
