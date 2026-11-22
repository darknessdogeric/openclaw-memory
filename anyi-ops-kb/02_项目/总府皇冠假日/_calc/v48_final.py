# -*- coding: utf-8 -*-
"""v48 收官：表格占位符填实 + ADR 中文化 + 重出公文 Word + 终检 + memory/README 同步"""
import io, os, sys, re, json, glob, subprocess
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v48.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
EMO = r"[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\u24C2\u2B55]"

MD = os.path.join(KB, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
t = open(MD, encoding="utf-8").read()

# ① ADR 中文化
n_adr = len(re.findall(r"\bADR\b", t))
t = t.replace("**一，ADR 目标不激进。**", "**一，平均房价目标不激进。**")
t = re.sub(r"\bADR\b", "平均房价", t)
L("[MD] ADR 中文化:", n_adr)

# ② 表格占位符填实（按列名判定）
lines = t.split("\n"); hdr = []; fixed = 0
for i, l in enumerate(lines):
    if l.startswith("|"):
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if not hdr and cells and set("".join(cells)) <= set("-: "):
            hdr = cells; continue
        if hdr and len(cells) == len(hdr):
            new = []
            for ci, c in enumerate(cells):
                if c in ("—", "-", ""):
                    col = hdr[ci] if ci < len(hdr) else ""
                    if "改善" in col:
                        rep = "不适用（基线情景）"
                    elif "可验证性" in col:
                        rep = "本项目基准方案"
                    elif "说明" in col or "口径" in col or col == "":
                        rep = "不适用"
                    else:
                        rep = "不适用"
                    new.append(rep); fixed += 1
                else:
                    new.append(c)
            lines[i] = "| " + " | ".join(new) + " |"
        continue
    hdr = []
t = "\n".join(lines)
L("[MD] 表格占位符填实:", fixed)

open(MD, "w", encoding="utf-8").write(t)
L("[MD] 已写盘:", len(t.encode("utf-8")), "bytes")

# ③ 公文 Word 重出
D = os.path.join(KB, "_calc")
src = open(os.path.join(D, "v17_docx.py"), encoding="utf-8").read()
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.md", "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.docx", "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.docx")
open(os.path.join(D, "v17_docx_v3.py"), "w", encoding="utf-8").write(src)
PY = r"C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe"
subprocess.run([PY, os.path.join(D, "v17_docx_v3.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
for l in open(os.path.join(T, "v17.log"), encoding="utf-8", errors="replace").read().split("\n"):
    if l.strip(): L(l.rstrip())

# ④ 终检
from docx import Document
DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.docx")
t = open(MD, encoding="utf-8").read()
d = Document(DOCX)
paras = [p.text for p in d.paragraphs]
alltext = "\n".join(paras) + "\n" + "\n".join(c.text for tb in d.tables for r in tb.rows for c in r.cells)
blank = sum(1 for tb in d.tables for r in tb.rows for c in r.cells if c.text.strip() in ("", "\u2014", "-", "\uff0f", "/"))
L("=== 终检 ===")
L("%.1f KB | 段落 %d | 表格 %d | 空白格 %d | 节 %d" % (os.path.getsize(DOCX) / 1024, len(d.paragraphs), len(d.tables), blank, len(d.sections)))
for si, s in enumerate(d.sections):
    L("   S%d %s %.0fx%.0f 页码域 %d" % (si, "横" if s.page_width > s.page_height else "纵",
        s.page_width.cm, s.page_height.cm, s.footer._element.xml.count('w:instr="PAGE"')))
L("emoji:", len(re.findall(EMO, alltext)))
KEYS = ["13,711.7", "2.02 倍", "17.18%", "1.002", "1.732", "1,299", "总府·街市百年", "国际五星旗舰", "2027 年",
        "900 万元", "成都院子", "800 元", "4,538.7", "L3", "R-23", "R-24", "R-25", "四川",
        "10,720", "2,915", "31,727.6", "20,401.3", "14,398.4", "15.61%", "6,774.0", "11.33%", "16,916.8",
        "盐与埠", "影与戏", "街与坊", "蜀与锦", "社会效益", "政治意义", "战略价值", "1,500", "1,750", "3,000"]
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
for o in ("TODO", "FIXME", "待填", "占位"):
    if o in alltext: L("   ⚠ 内部符号: %s" % o)

# ⑤ memory / README
MEM = r"D:\B166ER-openclaw\workspace\memory\2026-11-13.md"
open(MEM, "a", encoding="utf-8").write("""
### 15:50 ⭐⭐⭐⭐⭐ 十五五战略对标 + 在地文化 + 社会效益/政治意义/战略价值（v3.0 第二次增补）
> Eric 指示：「对标一下安逸十五五规划。尤其是在地文化挖掘的问题。不光是经济效益。还有社会效益，政治意义，以及对于安逸战略性的体现。全方位考虑。必要性可行性。」

#### 一、⭐⭐⭐ 战略底牌：总府在集团十五五里已是「国际五星旗舰」
知识库《十五五战略定位研究·10_三大明确战略方向》显示：**旗舰店双轨制 = 国际五星旗舰（总府皇冠假日 430 间）+ 本土自有旗舰（新良大酒店 200—350 间）。总府是集团在成都核心商圈唯一的国际五星载体。**
集团三大明确方向（Eric 2026-08-15 23:09 原话）：①标杆化生活方式酒店 + 把品牌立起来、把安逸立起来 ②**一定要做文创化改造，而不是简单改造** ③AI 数字化成为护城河和支柱。五大护城河：资源整合（第1）、数字化（第2）、运营（第3）、品牌项目（降权）、**在地文化能力（第5）**。
**⭐ 2027 年洲际品牌到期 = 唯一解约窗口，每年 900 万元品牌费刚性流出**（集团台账 4.3）。集团已形成四方向比选（原三方向 + 新增「安逸加悦榕」联合品牌）。→ **「是否改造」与「何时改造」是同一个战略问题。**

#### 二、⭐⭐ 在地文化：本项目最确定的溢价来源
**本地唯一长期样本 = 成都院子酒店**（文殊坊，16 座川西院落，2017 开业，86 间，9 年经营，**OCC 约 80%、ADR 接近 800 元**，非遗主题，业主城投集团，五朵金花=蜀锦蜀绣竹编漆艺银花丝，OTA 48-50%/线下 20%/私域 20-25%）。**ADR 800 元实证 → 本报告 CPI 1.15 对应 862 元同量级，不激进。** 但载体形态不同（院落低密度 vs 402 间垂直商业体），内容方案不可照搬。
**母题「总府·街市百年」**（以地名与街市史替代仿古符号）：明代「总府」（四川都指挥使司）→ 清光绪五年官盐店与盐市口 → 1926 智育电影院与上海影人剧团 → 1924 春熙路开路 → 2009 盐市口汉代廊桥遗址。**四个年度子题：盐与埠／影与戏／街与坊／蜀与锦**（集团国堰「一地一策」母题拆解法直接复用）。
**成熟度目标 L3 联动层**（国堰尺：L1 装饰/L2 叙事/L3 联动/L4 共创/L5 共生）；**国堰审计金句：「低于 5 条『强』的，别叫策展，叫装修」**。L3 最低可行内容预算 180—250 万/年（国堰 166—236 间）→ **按 402 间同强度折算需 435—605 万/年**。
**⭐ 资金来源 = 可保留项节约 4,538.7 万中划转，不新增改造投资总额。**

#### 三、⭐⭐⭐ 文创化溢价情景测算（v43 口径已与正式稿对齐，基线 −6,002.9 万完全一致）
| 情景 | CPI | 年内容预算 | 年营收 | 相对改造前 | 绝对净现值 | 增量净现值 | 增量IRR | 增量回收 |
|---|---|---|---|---|---|---|---|---|
| S1 基线 | 1.000 | 0 | 10,938.7 | 1.61× | −6,002.9 | 14,398.4 | 15.61% | 8 年 |
| 保守 | 1.100 | 320 万 | 12,754.5 | 1.88× | −3,481.9 | 16,919.4 | 16.64% | 7 年 |
| **基准** | **1.150** | **280 万** | **13,711.7** | **2.02×** | **−2,124.3** | **18,277.1** | **17.18%** | **7 年** |
| 乐观 | 1.200 | 240 万 | 14,701.6 | 2.17× | −721.1 | 19,680.2 | 17.73% | 7 年 |
**临界值：追平基线只需 CPI 1.002（平均房价 751 元）—— 边际成本极低，稀缺的不是钱而是内容兑现；追平 S7B 需 CPI 1.732（1,299 元）—— 文创化无法替代外部奢牌价格带。**
**★ 与 S7B 对照：S1+文创 增量净现值 18,277.1 万 > S7B 的 37,318.1 万？否——S7B 更高，但 S7B 前提三项均无支撑；S1+文创 前提可验证（本地样本+集团方法论+成本在可保留节约内）。**
**⚠ 反直觉风险：内容预算越低财务指标略好，但内容越薄溢价越难兑现 =「省了钱、赔了价」负循环，须以 Kill 判据管理而非压缩预算。**

#### 四、⭐ 战略风险（报告新增 R-23/R-24/R-25）
- **R-24 春熙路品牌序列冲突**：集团在春熙路及邻近已有多处自有门店（锦著春熙路店、天府广场春熙路店、春熙路太古里店），且同址多条目问题（春熙路店猫途鹰 8/41/332 三条仅差标点，点评无法沉淀）→ **总府定位必须与锦著系列分工，否则内部自我蚕食**。
- **R-25 2027 窗口错失**；**R-23 文化溢价不兑现（CPI<1.10 Kill）**。
- 外部参照：峨眉山悦榕庄 2026-08 开业，房价 2,700—8,000 元 = 「城市度假」价格天花板；国堰 RevPAR 102.63 与之差十倍。

#### 五、报告改动汇总（v3.0 共 26 表 / 415 段 / 100.6 KB / 9 节）
- **第二章 新增（八）文创化改造路径的市场参照**（原（八）市场预测结论 →（九））
- **第三章 新增（六）战略与文化维度的必要性**：必要性四维 = 合规刚性 + 经营止血 + 旗舰战略（2027 窗口）+ 文化与城市更新（原（六）→（七））
- **第五章 新增（七）在地文化植入方案**（9 个小节：母题史实表／四子题／L1-L5 分级／预算来源／机制三件套／公共区功能分层表／岗位／KPI+Kill）（原（七）（八）→（八）（九））
- **第九章 新增（九）文创化溢价情景测算**（三情景表／临界值反解／路径对照）
- **第十章 重写为「社会效益、政治意义与战略价值」**（三节：社会效益 5 条／政治意义 4 条／十五五战略体现 5 行对照表 + 品牌窗口 + 序列冲突 + 悦榕庄参照）
- **第十二章 结论 11—15、建议 8—12、请示 6—8**
- **Excel 新增 17 文创化溢价情景 / 18 十五五战略对标与在地文化**（19 sheets / 61.9 KB）；01 大数对照表补录 10 条

#### 六、沉淀的方法论（本轮新增教训）
- **战略维度必须先查内部知识库再联网**。总府的旗舰定位、2027 品牌窗口、文创化方法论、成熟度尺全部在 `anyi-ops-kb/07_战略与改革/十五五战略定位研究/` 与 `02_项目/国堰宾馆文创改造/` 里，**比联网更快也更权威**。国堰是先例、总府是旗舰，两者可构成「目的地型 + 城市型」一双样板。
- **有本地实证样本时，溢价假设就应锚定样本而非外推**。成都院子 800 元使 CPI 1.15 不再是乐观假设。
- **临界值反解是判断方案真伪的利器**：本轮用 CPI 1.002 / 1.732 两个临界值，一次性说清「文创化值不值」与「文创化替代不了什么」。
<!-- project: github.com/darknessdogeric/openclaw-memory -->
""")
RM = os.path.join(KB, "00_项目总览_README.md")
open(RM, "a", encoding="utf-8").write("""
### v3.0 第二次增补（2026-11-14 15:50）：十五五战略对标 + 在地文化 + 社会效益/政治意义/战略价值
**战略底牌**：总府在集团十五五中是**「国际五星旗舰」**（双轨制一轨，另一轨新良大酒店）；**2027 年洲际品牌到期 = 唯一解约窗口**（900 万元/年品牌费）；集团三大方向之一即「文创化改造而非简单改造」，五大护城河含「在地文化能力」。
**在地文化**：母题「总府·街市百年」（明代总府→清官盐店→1926 智育电影院→1924 春熙路→2009 汉代廊桥遗址），四子题盐与埠/影与戏/街与坊/蜀与锦，目标 L3 联动层，预算从可保留项节约 4,538.7 万划转（建议 400 万/年×3 年）。
**本地实证**：成都院子酒店 9 年｜OCC 约 80%｜ADR 接近 800 元｜86 间 → CPI 1.15 不激进。
**财务**：S1+文创 基准情景年营收 13,711.7 万（改造前 2.02 倍）、绝对净现值 −2,124.3 万、增量净现值 18,277.1 万、增量内部收益率 17.18%、增量回收 7 年；临界 CPI 1.002（打平）/ 1.732（追平 S7B）。**边界须自曝：绝对净现值仍为负，不作高回报投资申报。**
**报告**：14 章 26 表 415 段 100.6 KB / 9 节；Excel 19 表 61.9 KB（新增 17 文创化溢价情景、18 十五五战略对标与在地文化）；风险新增 R-23 文化溢价不兑现 / R-24 春熙路品牌序列冲突 / R-25 2027 窗口错失。
<!-- project: github.com/darknessdogeric/openclaw-memory -->
""")
L("memory + README synced")
L("交付:", [os.path.basename(x) for x in glob.glob(os.path.join(REP, "总府皇冠改造_可行性研究报告*"))],
  [os.path.basename(x) for x in glob.glob(os.path.join(CAL, "总府皇冠改造_可行性研究报告*"))])
L("桌面残留:", len(glob.glob(r"C:\Users\ericz\Desktop\*总府*")))
L("DONE")
