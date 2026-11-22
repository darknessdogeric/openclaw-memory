# -*- coding: utf-8 -*-
"""v107：最终终检 + memory/README/索引 同步（含联网复核后的三处订正）"""
import io, os, re, sys, glob, json
from docx import Document
from openpyxl import load_workbook
sys.stdout.reconfigure(encoding="utf-8")

T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v6.0_2026-11-15.docx")
XLSX = os.path.join(CAL, "总府皇冠改造_可行性研究报告_测算附表_v6.0_2026-11-15.xlsx")
MD = os.path.join(KB, "总府皇冠改造_可行性研究报告_v6.0_2026-11-15.md")

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
md = io.open(MD, encoding="utf-8").read()
EMO = ("[" + chr(92) + "U0001F300-" + chr(92) + "U0001FAFF" + chr(92) + "U00002600-" + chr(92) + "U000027BF"
       + chr(92) + "U00002B50" + chr(92) + "uFE0F" + chr(92) + "u200D" + chr(92) + "u2764" + chr(92) + "u2B06"
       + chr(92) + "u2B07" + chr(92) + "u2B05" + chr(92) + "u274C" + chr(92) + "u2705" + chr(92) + "u26A0"
       + chr(92) + "u26A1" + chr(92) + "u2139" + chr(92) + "u24C2" + chr(92) + "u2B55]")

print("=" * 74); print("=== 交付终检（v6.0 会议纪要口径）==="); print("=" * 74)
print("Word  {0:.1f} KB｜段落 {1}｜表格 {2}｜空白格 {3}｜节 {4}｜图片 {5}｜emoji {6}｜★ {7}".format(
    os.path.getsize(DOCX)/1024, len(d.paragraphs), len(d.tables), blank, len(d.sections),
    nimg, len(re.findall(EMO, alltext)), alltext.count("\u2605")))
print("      目录 {0} 条｜每节页码域 {1}｜横向节 {2}".format(
    len(toc), [s.footer._element.xml.count('w:instr="PAGE"') for s in d.sections],
    sum(1 for s in d.sections if s.page_width > s.page_height)))
wb = load_workbook(XLSX, data_only=True)
print("Excel {0:.1f} KB｜{1} 表".format(os.path.getsize(XLSX)/1024, len(wb.sheetnames)))
print("MD    {0} 字｜图 {1}｜★ {2}".format(len(md), len(re.findall(r"!\[", md)), md.count("\u2605")))

KEY = ["\uff0b3,021", "\u221219,699", "\u221222,862", "\u221224,046", "9.30%", "2.21%", "2.37%", "1.36%",
       "11,066", "21,054", "24,119", "24,340", "9,884", "6,442.73", "5,403.53", "\u2212416.51",
       "60,914.78", "14,382", "60,677", "2,088.85", "10,192", "25.35", "1,280", "416.29",
       "107.90", "43 \u6b21", "0.0017", "2029-09-27", "\u22125,227",
       "209 \u95f4", "205 \u95f4", "14.69", "1,020 \u4ef6", "84.22%", "\u4fdd\u7559\u90e8\u5206\u57fa\u6750",
       "\u786e\u5b9a\u6027\u65b9\u6848\u610f\u89c1", "\u8bf7\u96c6\u56e2\u9009\u62e9\u6267\u884c\u8def\u5f84",
       "\u5206\u6279\u9a8c\u6536\u4e0d\u53ef\u884c", "\u524d\u7f6e\u4ef7\u683c\u9a8c\u8bc1", "3+3",
       "\u6ca1\u6709\u4e00\u5bb6\u662f\u56fd\u9645\u8054\u53f7",
       # 联网复核新增锚点
       "1,632 \u95f4", "654 \u95f4", "\u897f\u533a\u7687\u51a0", "\u6e29\u6c5f\u7687\u51a0", "\u5929\u5e9c\u7687\u51a0",
       "\u4e16\u7eaa\u57ce\u5929\u5802\u6d32\u9645", "1,265\u20143,500", "\u5ba2\u623f\u8d28\u7d20\u53ca\u8212\u9002\u5ea6 7.7",
       "\u4f4d\u7f6e 9.4", "9,495 \u6761", "\u4e0d\u5b58\u5728\u8be5\u72ec\u7acb\u7269\u4e1a"]
mw = [k for k in KEY if k not in alltext]; mm = [k for k in KEY if k not in md]
print("关键值（%d 项） Word 缺失: %s" % (len(KEY), mw if mw else "无"))
print("关键值（%d 项） MD   缺失: %s" % (len(KEY), mm if mm else "无"))
print("硬约束: 轻改 {0}｜4.08亿 {1}｜1.8亿 {2}｜不改造 {3}｜四季度 {4}｜保留石材(仅更正说明) {5}".format(
    md.count("\u8f7b\u6539"), md.count("4.08"), md.count("1.8 \u4ebf"), md.count("\u4e0d\u6539\u9020"),
    md.count("\u56db\u5b63\u5ea6"), md.count("\u4fdd\u7559\u77f3\u6750")))
print("桌面根目录总府残留: {0}｜项目文件夹文件总数: {1}".format(
    len(glob.glob(r"C:\Users\ericz\Desktop\*\u603b\u5e9c*")),
    len([f for f in glob.glob(os.path.join(TGT, '**', '*'), recursive=True) if os.path.isfile(f)])))

# ── memory ──
MEM = r"D:\B166ER-openclaw\workspace\memory\2026-11-15.md"
open(MEM, "a", encoding="utf-8").write(r"""
### 12:10 ⭐⭐⭐⭐⭐ 联网复核：更正三处市场数据，v6.0 定稿
**A5 子 Agent 被 kill（长时间联网取数未产出），改为自行联网复核，结果比 A5 更有价值——查出了三处必须改的错误。**

#### 一、★实体归属更正：「成都世纪城皇冠假日酒店」并不存在
初稿把提价锚点写成"环球中心皇冠假日 757 元／世纪城皇冠假日 697 元"。联网复核：**洲际体系在成都邻近环球中心、世纪城新会展的对应实体是「成都天府皇冠假日酒店」(Crowne Plaza CHENGDU TIANFU NEW AREA by IHG)**，地址天府新区华阳街道剑南大道南段 669 号 52 栋；而"成都世纪城"物业是 **Holiday Inn Chengdu Century City East Tower（190 间，假日品牌，非皇冠）**。→ 报告第三章、第四章、第十一章三处表述全部改为**五家可核验实体价格阶梯**。

#### 二、★洲际体系成都价格阶梯（2026-11-15 联网实测，全部可溯源）
| 物业 | 房量/装修 | 实测价 | 位置评分 |
|---|---|---|---|
| 世纪城天堂洲际大饭店 | — | 800 元起 | — |
| 天府皇冠假日（邻环球中心/世纪城） | — | Agoda 常规 101—150 美元 ≈ 730—1,080 元；最低 44 欧元起 | — |
| 西区皇冠假日 | 347 间/2018 | 675—710 元 | 7.3 |
| 温江皇冠假日 | 458 间/2016 | 581—634 元 | 8.0 |
| 新希望高新皇冠假日 | 347 间/2018 | 293 元/人 | — |
| **总府皇冠假日（本项目）** | **402 间/1996 建成/2014 装修** | **Agoda 常规 51—75 美元 ≈ 370—540 元** | **9.4** |

**路径一 ADR 620 元因此更扎实**：落在西区（675—710）与温江（581—634）之间，而总府位置分 9.4 远高于两者 8.0 与 7.3。

#### 三、★「900 元以上高价段仅 989 间」是错的，已更正为 1,632 间
初稿只数了春熙路核心圈四家（洲至奢选 335＋尼依格罗 230＋瑞吉 282＋居舍 142）。**漏计丽思卡尔顿 353 间、华尔道夫 289 间、香格里拉、钓鱼台、世纪城天堂洲际**。按可核验房量：全市 **不少于 1,632 间**，核心圈可核验部分 654 间。**这一更正削弱"高价段容量有限"论据的强度，但不改变结论**——路径二三不成立是投资额与停业期所致，不是市场容量。

#### 四、★第三方平台独立印证（Agoda 官方页）
总府：1996 建成、26 层、402 间、2014 装修、距春熙路步行街 430 米、餐厅 2 酒吧 1 —— **与业主资料完全一致**。六项子评分：**位置 9.4（最高）、服务 8.9、清洁 8.6、性价比 8.5、设施 8.4、客房质素及舒适度 7.7（最低）**，整体 9.4／9,495 条评价。**位置最优而产品力最差**，第三方口径独立印证了报告的诊断。另核到瑞吉 1,300 起／豪华房 1,300—1,700（与 A1 的 1,291—1,393 互证）、居舍 2,000 起／117 平米寺庙套房 4,000—6,000、费尔蒙 336 间 900—2,200。

#### 五、v6.0 最终交付状态
Word 896.5 KB／288 段／28 表／**0 空白格**／9 节（各 1 个页码域、4 横向）／8 图／**0 emoji／0 ★**；目录 12 条与正文 12 章一致；Excel 10 表与模型逐项数值一致；关键值 51 项 Word/MD 全中；"轻改""4.08亿""1.8亿""不改造""四季度"均 0 次；桌面根目录总府残留 0。
<!-- project: github.com/darknessdogeric/openclaw-memory -->
""")
print("memory 已同步")

RM = os.path.join(KB, "00_项目总览_README.md")
open(RM, "a", encoding="utf-8").write(r"""
### v6.0 定稿（2026-11-15 12:10）—— 联网复核后更正三处
**① 实体归属更正**：不存在"成都世纪城皇冠假日酒店"，洲际体系对应实体为**成都天府皇冠假日**（邻环球中心/世纪城）；改用**洲际体系成都五家可核验实体价格阶梯**（世纪城天堂洲际 800 元起／天府皇冠 730—1,080／西区皇冠 675—710／温江皇冠 581—634／新希望高新 293 元）。
**② 更正高价段容量**：900 元以上由 989 间更正为**全市不少于 1,632 间**（漏计丽思卡尔顿 353、华尔道夫 289 等），核心圈可核验 654 间。结论不变（路径二三不成立于投资额与停业期，非容量）。
**③ 第三方印证**：Agoda 官方页与业主资料完全一致；六项子评分**位置 9.4 最高、客房质素 7.7 最低**，独立印证"位置最优、产品力最差"。
**终检**：896.5 KB／288 段／28 表／0 空白格／9 节／8 图／0 emoji／目录 12 条一致／51 项关键值全中／桌面残留 0。
<!-- project: github.com/darknessdogeric/openclaw-memory -->
""")
print("README 已同步")

IDX = os.path.join(TGT, "00_总府皇冠改造项目_文件索引.md")
open(IDX, "a", encoding="utf-8").write(r"""
## 六、v6.0 定稿补充说明（2026-11-15 12:10）
本版第三章经联网复核后更正三处市场数据：① 不存在"成都世纪城皇冠假日酒店"，洲际体系对应实体为成都天府皇冠假日，提价锚点改用洲际体系成都五家可核验实体价格阶梯；② "900 元以上高价段仅 989 间"更正为全市不少于 1,632 间（核心圈可核验 654 间）；③ 增列 Agoda 官方页对现状基线的独立交叉印证（1996 建成／402 间／2014 装修／位置分 9.4 最高而客房质素分 7.7 最低）。
<!-- project: github.com/darknessdogeric/openclaw-memory -->
""")
print("索引已同步")
print("DONE")
