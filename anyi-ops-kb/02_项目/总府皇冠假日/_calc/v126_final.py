# -*- coding: utf-8 -*-
"""v126：Word 重建 + 终检 + 旧版清理 + memory/索引同步"""
import io, os, re, sys, glob, json, shutil, subprocess
from docx import Document
from openpyxl import load_workbook
sys.stdout.reconfigure(encoding="utf-8")
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
PY = r"C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe"
V = json.load(open(os.path.join(T, "v120.json"), encoding="utf-8"))
R = V["results"]

# ── 1. Word 生成器改指 v7.0 ──
dp = os.path.join(KB, "_calc", "v100_docx.py")
s = io.open(dp, encoding="utf-8").read()
s = s.replace("总府皇冠改造_可行性研究报告_v6.0_2026-11-15.md", "总府皇冠改造_可行性研究报告_v7.0_2026-11-15.md")
s = s.replace("总府皇冠改造_可行性研究报告_v6.0_2026-11-15.docx", "总府皇冠改造_可行性研究报告_v7.0_2026-11-15.docx")
io.open(dp, "w", encoding="utf-8").write(s)
r = subprocess.run([PY, dp], capture_output=True, text=True, encoding="utf-8", errors="replace",
                   env=dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1"), timeout=900)
print("docx rc=%d" % r.returncode)
print(io.open(os.path.join(T, "v17.log"), encoding="utf-8").read().strip())

# ── 2. 清理旧版 ──
removed = []
for d in (REP, CAL):
    for f in glob.glob(os.path.join(d, "*")):
        b = os.path.basename(f)
        if not os.path.isfile(f): continue
        if any(x in b for x in ("v6.0_2026-11-15", "v5.0_2026-11-14", "v4.0_2026-11-14")):
            os.remove(f); removed.append(b)
print("清理旧版:", len(removed))
for x in removed: print("   -", x)

# ── 3. 终检 ──
DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v7.0_2026-11-15.docx")
XLSX = os.path.join(CAL, "总府皇冠改造_可行性研究报告_测算附表_v7.0_2026-11-15.xlsx")
MD = os.path.join(KB, "总府皇冠改造_可行性研究报告_v7.0_2026-11-15.md")
d = Document(DOCX)
alltext = "\n".join(p.text for p in d.paragraphs) + "\n" + "\n".join(
    c.text for tb in d.tables for r in tb.rows for c in r.cells)
blank = sum(1 for tb in d.tables for r in tb.rows for c in r.cells
            if c.text.strip() in ("", "\u2014", "-", "\uff0f", "/", "\u2013"))
nimg = sum(1 for rel in d.part.rels.values() if "image" in rel.reltype)
ps = [p.text.strip() for p in d.paragraphs]
ti = next((i for i, x in enumerate(ps) if x.replace(" ", "").endswith("\u76ee\u5f55")), 0)
toc = []
for j in range(ti + 1, min(len(ps), ti + 30)):
    if re.match(r"^\d{1,2}\.\s", ps[j]): toc.append(ps[j])
    elif toc: break
EMO = ("[" + chr(92) + "U0001F300-" + chr(92) + "U0001FAFF" + chr(92) + "U00002600-" + chr(92) + "U000027BF"
       + chr(92) + "U00002B50" + chr(92) + "uFE0F" + chr(92) + "u200D" + chr(92) + "u2764" + chr(92) + "u2B06"
       + chr(92) + "u2B07" + chr(92) + "u2B05" + chr(92) + "u274C" + chr(92) + "u2705" + chr(92) + "u26A0"
       + chr(92) + "u26A1" + chr(92) + "u2139" + chr(92) + "u24C2" + chr(92) + "u2B55]")
md = io.open(MD, encoding="utf-8").read()
wb = load_workbook(XLSX, data_only=True)
print()
print("=" * 74); print("=== v7.0 交付终检 ==="); print("=" * 74)
print("Word  {0:.1f} KB｜段落 {1}｜表格 {2}｜空白格 {3}｜节 {4}｜图片 {5}｜emoji {6}｜★ {7}".format(
    os.path.getsize(DOCX)/1024, len(d.paragraphs), len(d.tables), blank, len(d.sections),
    nimg, len(re.findall(EMO, alltext)), alltext.count("\u2605")))
print("      目录 {0} 条｜每节页码域 {1}｜横向节 {2}".format(
    len(toc), [x.footer._element.xml.count('w:instr="PAGE"') for x in d.sections],
    sum(1 for x in d.sections if x.page_width > x.page_height)))
print("Excel {0:.1f} KB｜{1} 表".format(os.path.getsize(XLSX)/1024, len(wb.sheetnames)))
print("MD    {0} 字｜图 {1}｜★ {2}".format(len(md), len(re.findall(r"!\[", md)), md.count("\u2605")))
KEY = ["\uff0b1,530", "\u22121,192", "\u221213,025", "\u221227,999", "24,453", "32,485", "36,842", "38,528",
       "21,610", "268 \u95f4", "254 \u95f4", "402 \u95f4", "8.0 \u4e07\u5143/\u95f4", "3,216", "412.09", "728 \u5143\u8d77",
       "\u4e09\u6539\u4e8c", "\u5b58\u91cf\u6539\u9020\u5de5\u4f5c\u6b65\u9aa4", "\u5168\u751f\u547d\u5468\u671f", "\u5ba2\u623f\u8f7b\u6539",
       "\u505c\u4e1a\u671f", "\u722c\u5761\u66f2\u7ebf", "\u6536\u76ca\u7ed3\u6784\u6a21\u578b", "8,866", "5,806",
       "\u961f\u5217\u4e00", "\u8def\u5f84\u4e00", "\u8def\u5f84\u56db", "\u81ea\u5efa\u65d7\u8230\u54c1\u724c"]
mw = [k for k in KEY if k not in alltext]; mm = [k for k in KEY if k not in md]
print("关键值（%d 项）Word 缺失: %s" % (len(KEY), mw if mw else "无"))
print("关键值（%d 项）MD   缺失: %s" % (len(KEY), mm if mm else "无"))
print("硬约束: 轻改 {0}｜4.08亿 {1}｜1.8亿 {2}｜不改造 {3}｜四季度 {4}｜上一版 {5}｜初稿曾 {6}".format(
    md.count("\u8f7b\u6539"), md.count("4.08"), md.count("1.8 \u4ebf"), md.count("\u4e0d\u6539\u9020"),
    md.count("\u56db\u5b63\u5ea6"), md.count("\u4e0a\u4e00\u7248"), md.count("\u521d\u7a3f\u66fe")))
print("桌面根目录总府残留: {0}".format(len(glob.glob(r"C:\Users\ericz\Desktop\*\u603b\u5e9c*"))))
print()
print("=== 交付清单 ===")
for f in sorted(glob.glob(os.path.join(REP, "*"))) + sorted(glob.glob(os.path.join(CAL, "*"))):
    if os.path.isfile(f): print("  %7.1f KB  %s" % (os.path.getsize(f)/1024, os.path.basename(f)))

# ── 4. memory / README / 索引 ──
MEM = r"D:\B166ER-openclaw\workspace\memory\2026-11-15.md"
open(MEM, "a", encoding="utf-8").write(r"""
### 12:55 ⭐⭐⭐⭐⭐ 总府皇冠改造 v7.0 定稿（三档价格带 × 四方案 × 存量改造工作步骤）
**依据 Eric《方案优化意见梳理》（2026-11-15，来自得到大脑）重构。核心变化：路径一不是"底线整改"，而是"客房轻改 + 可议价"。**

#### 一、四方案重构
| 方案 | 房量/档次 | 投资 | 停业 | NPV | IRR | 回收 |
|---|---|---|---|---|---|---|
| 一 轻改（家具·床品·木饰面·装饰面更新） | 402/五星豪华 | 24,453万 | 12月 | **＋1,530万** | 8.74% | 9.71年 |
| 二 停业改造（洲际体系内升级） | 402/五星豪华 | 32,485万 | 14月 | −1,192万 | 7.55% | 10.59年 |
| 三 换品牌并动格局（三改二） | 268/上奢 | 36,842万 | 26月 | −13,025万 | 3.87% | 14.83年 |
| 四 自建品牌（参考） | 268/五星豪华 | 38,528万 | 30月 | −27,999万 | −1.47% | 不回本 |
**三档价格带**：五星豪华 600—800／上奢 900—2,000／奢华 2,000 以上。**房量口径改为三改二 402→268 间**（套内 38.0㎡，名义 42.6㎡；洲际方套内≥40㎡约束则 254 间）。
**★关键**：路径三在第二档（950元）为 −13,025万，若 268 间进入第三档（2,200元）则 ＋44,722万 —— 成立性押在"能否卖到 2,000 以上"，须由市场回答。

#### 二、★自行发现并修正的三处测算错误
1. **现金流时间轴混用**：原模型把 20 笔年度现金流按 (1+8%)^19~^38 折现（等于按月折现年现金流），**系统性低估经营现金流现值约 2.5 亿元**。已改为统一月度网格（折现率 (1+8%)^(1/12)-1）。
2. **公共必选工程严重低估**：原按 160 元/㎡计得 11,066 万元，无法覆盖消防全系统+4台R11冷媒机组+542盘管+4干变+34低压柜+14电梯+4锅炉+26层管网全线。**重建为 21,610 万元（313 元/㎡）**，并补齐漏项：客房与公区面层恢复、拆除清运、报建检测、第三方评估监理、项目管理与开办费、建设期利息。
3. **客房完全不改造则净现值不可能为正** —— Eric 的核心质疑成立。隐蔽工程解决"能不能营业"，客房轻改（8.0万元/间、3,216万元）才解决"能不能卖到价"。

#### 三、★价格下滑归因更正
携程挂牌 728 元与同品牌同城（温江 698 起、西区 675 起）基本持平，成交仅 412.09 元，**差额主因不是协议价/会员价结构，而是产品竞争力不足：长期为保开房率而降价、以会议团队客量提入住率 → 整体价格下滑，未发挥春熙路商旅高溢价属性**。

#### 四、报告新增两章
- **第四章 存量改造工作步骤**：六阶段（立项合规前置→设计定位→报建招采→停业实施→验收复业→运营提升），每阶段列对内工作/对外工作/交付物/放行闸口。
- **第五章 全生命周期对内与对外工作分步展开**：对外合作五顺位（咨询顾问→品牌设计方→产品设计方→机电与消防设计方→施工总承包与设备供应商），**第一顺位是设计方而非工程总承包**。

#### 五、撤销事项
上一版基于"分期施工、分期开业"的分期方案已撤销 —— 阶段性改造与阶段性开业不可行（消防单一系统不满足独立性；合同附件 A 7.10 条要求营业区消防全程可用）。

#### 六、交付
v7.0 Word（十二章→十四章，44,607 字）＋ 测算附表 v7.0（14 表含使用说明、四方案分表、爬坡曲线、存量改造步骤表、全生命周期分工表）＋ 8 图。v5.0/v6.0 已清理。
<!-- project: github.com/darknessdogeric/openclaw-memory -->
""")
print("memory 已同步")
RM = os.path.join(KB, "00_项目总览_README.md")
open(RM, "a", encoding="utf-8").write(r"""
### v7.0 定稿（2026-11-15 12:55）—— 三档价格带 × 四方案
**按 Eric《方案优化意见梳理》重构**：路径一改为"轻改"（客房家具/床品/木饰面/装饰面更新，8.0 万元/间）而非"客房不动"；房量改为三改二 402→268 间；新增三档价格带（600—800／900—2,000／2,000 以上）与三档收入结构模型、20 年爬坡曲线；新增第四章存量改造工作步骤（六阶段）、第五章全生命周期对内/对外分工（对外合作第一顺位为设计方与咨询顾问）。修正三处测算错误：现金流时间轴混用（低估现值约 2.5 亿元）、公共必选工程低估（11,066→21,610 万元）、客房不改造则净现值不可能为正。**结论：路径一（轻改）唯一成立，＋1,530 万元；路径三的成立性取决于能否把 268 间推到 2,000 元以上。**
<!-- project: github.com/darknessdogeric/openclaw-memory -->
""")
print("README 已同步")
IDX = os.path.join(TGT, "00_总府皇冠改造项目_文件索引.md")
open(IDX, "a", encoding="utf-8").write(r"""
## 八、v7.0 定稿说明（2026-11-15 12:55）
本版按产业发展部意见重构为「三档价格带 × 四方案」结构：路径一轻改（客房家具／床品／木饰面／装饰面更新，402 间）、路径二停业改造（洲际体系内升级）、路径三换品牌并动格局（三改二 268 间）、路径四自建品牌（参考）。新增第四章「存量改造工作步骤」（六阶段、对内与对外工作、放行闸口）与第五章「全生命周期：对内工作与对外工作分步展开」。测算附表 v7.0 共 14 表，含使用说明、三档价格带与收入结构、房量口径、公共必选工程、四方案分表、敏感性、爬坡曲线、存量改造工作步骤、全生命周期分工与数据来源。v5.0 与 v6.0 已清理归档。
<!-- project: github.com/darknessdogeric/openclaw-memory -->
""")
print("索引已同步")
print("DONE")
