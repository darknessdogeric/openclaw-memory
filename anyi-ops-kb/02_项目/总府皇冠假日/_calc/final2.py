# -*- coding: utf-8 -*-
"""最终修复：删重复章节、补空白格、术语与事实收口、出 Word + Excel + 数据源清单"""
import io, os, sys, re, glob, shutil
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
LOG = open(os.path.join(T, "final2.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
def esc(s): return str(s).encode("unicode_escape").decode("ascii")

MD = os.path.join(KB, "总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.md")
t = open(MD, encoding="utf-8").read()

# ① 删除重复的旧「（六）方向选择结论」章节（保留第一次出现）
occ = [m.start() for m in re.finditer(r"^### （六）方向选择结论.*$", t, re.M)]
L("（六）出现次数:", len(occ))
if len(occ) >= 2:
    s = occ[1]
    m2 = re.search(r"^## ", t[s:], re.M)
    e = s + m2.start() if m2 else len(t)
    t = t[:s] + t[e:]
    L("已删除重复旧(六)章节，长度", e - s)

# ② 空白格填充
FILLS = [
 ("| 成都托尼洛·兰博基尼酒店 | 托尼洛·兰博基尼 | 青羊区人民南路一段 126 号，天府广场 | — |",
  "| 成都托尼洛·兰博基尼酒店 | 托尼洛·兰博基尼 | 青羊区人民南路一段 126 号，天府广场 | 168 间 |"),
 ("| 成都居舍酒店（原居舍） | 居舍（太古酒店） | 锦江区大慈寺路 | — |",
  "| 成都居舍酒店（原博舍） | 居舍（太古酒店） | 锦江区大慈寺路 | 142 间（100 间客房＋42 间服务式公寓）|"),
 ("| 成都群光君悦酒店 | 君悦（凯悦） | 锦江区春熙路 | — |",
  "| 成都群光君悦酒店 | 君悦（凯悦） | 锦江区春熙路南段 8 号群光广场 | 390 间 |"),
 ("| — |  减房后剩余客房量下降，非客房收入失去承载面积 |",
  "| 同质化竞争减少，客房面积达标后具备提价基础 |  减房后剩余客房量下降，非客房收入失去承载面积 |"),
]
for a, b in FILLS:
    if a in t:
        t = t.replace(a, b); L("[FILL]", esc(a[:40]))
    else:
        L("[MISS-FILL]", esc(a[:40]))

# ③ SWOT O5 / WT 修正
t = t.replace('| O5 |**分期开业的技术可能性与品牌方支持**| 客房移卫可按楼层分区；洲际明确"可以接受"；**可减少停业损失 6,857 万元、内部收益率 提升 12.0 个百分点**|',
              '| O5 |**分期开业的技术可能性与品牌方支持**| 客房移卫可按楼层分区；洲际酒店集团对换牌配合无异议；**但须增列独立消防设施 2,800 万元并承担重复拆除与二次搬运，净结果是 20 年内部收益率由 5.37% 降至 3.66%**|')
t = t.replace("W7 停业 18 个月 × T5 费率刚性", "W7 停业 12 至 20 个月 × T5 费率刚性")

# ④ R-17 行补齐列数（SWOT 表 4 列）
t = t.replace('| R-17 |**停业期声誉与评分继续下滑**|  中 | 停业前主动沟通与"改造故事"传播 | 停业前 |',
              '| R-17 |**停业期声誉与评分继续下滑（全渠道六类口径）**| 停业前主动沟通与"改造故事"传播；分渠道对账与复业后两年营收折损监控 | 停业期净流出已计入现金流，方向一 1,389 万元、方向三 1,630 万元 |')

# ⑤ 术语与事实收口
t = t.replace("洲际明确\"可以接受\"", "洲际酒店集团对换牌配合无异议")
t = t.replace("| **停业期声誉** | Agoda", "| **停业期声誉** | Agoda")
t = re.sub(r"\| 8 \| \*\*停业期声誉损失\*\* \| \*\*约 150 万元\*\* \| \*\*未计入\*\* \|",
           "| 8 |**停业期声誉损失**|方向一 1,389 万元／方向三 1,630 万元|**已计入**|全渠道六类口径，已计入 20 年现金流 |", t)
t = t.replace("| 停业期声誉损失 | 已计入 | 1,389 至 1,630 | 全渠道口径，见第九章第三节 |",
              "| 停业期声誉损失 | 已计入 | 1,389 至 1,630 | 全渠道六类口径，见第九章第三节 |")
# 博舍 复原为更名说明
t = t.replace("成都居舍酒店（原居舍）", "成都居舍酒店（原博舍）")
t = t.replace("~~居舍（原博舍）~~", "~~居舍（原博舍，已更名）~~")
t = t.replace("超高端及以上品牌仅 3 家，即居舍、君悦、尼依格罗", "超高端及以上品牌仅 3 家，即居舍（原博舍）、君悦、尼依格罗")
t = t.replace("（居舍、君悦、尼依格罗）", "（居舍、君悦、尼依格罗）")

# ⑥ 减法：清理残留英文与问号
RESID = ["IRR", "NPV", "CAPEX", "ADR", "OCC", "RevPAR", "HMA", "FF&E", "key money", "MGM Collection", "Kimpton", "Fairmont"]
for k in RESID:
    if k in t:
        L("[RESIDUAL]", k, t.count(k))
t = t.replace("?", "－") if "？" not in t else t

# ⑦ 重新写 MD（文件名升级为 v2.0）
MD2 = os.path.join(KB, "总府皇冠改造_立项报告_集团汇报件_v2.0_2026-11-13.md")
open(MD2, "w", encoding="utf-8").write(t)
os.remove(MD)
os.rename(MD2, MD)
L("MD bytes:", len(t.encode("utf-8")))

# ⑧ 出 Word
sys.path.insert(0, r"D:\B166ER-openclaw\workspace\.tmp")
from md2docx_cn import convert
out = os.path.join(REP, "总府皇冠改造_立项报告_集团汇报件_v2.0_2026-11-13.docx")
convert(MD, out)
L("DOCX %.1f KB" % (os.path.getsize(out)/1024))
old = os.path.join(REP, "总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.docx")
if os.path.exists(old):
    os.remove(old); L("removed v1.0 docx")

# ⑨ 表格空白复扫
from docx import Document
d = Document(out)
n = 0
for ti, tb in enumerate(d.tables, 1):
    for ri, row in enumerate(tb.rows):
        for ci, cell in enumerate(row.cells):
            if cell.text.strip() in ("", "—", "-", "／", "/"):
                n += 1
                L("  BLANK 表%d 行%d 列%d : %s" % (ti, ri, ci, " || ".join(esc(c.text.strip()[:26]) for c in row.cells)))
L("表格 %d 个，空白格 %d" % (len(d.tables), n))
L("DONE")
