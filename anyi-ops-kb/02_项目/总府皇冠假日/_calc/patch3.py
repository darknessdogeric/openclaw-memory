# -*- coding: utf-8 -*-
"""v3.0 改稿：撤回虚构的“10年国资门槛”，改为三重口径 + 集团715定稿对照"""
import io, os, sys, re, glob
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
LOG = open(os.path.join(T, "patch3.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
def esc(s): return str(s).encode("unicode_escape").decode("ascii")
sys.path.insert(0, os.path.join(KB, "_calc"))
from new_chapters import CH9
from new_calib import CH9_MOUTH, CH9_CALIB, CH9_CONC, CH5_NEW, CH11_NEW

MD = os.path.join(KB, "总府皇冠改造_立项报告_集团汇报件_v2.0_2026-11-13.md")
MD3 = os.path.join(KB, "总府皇冠改造_立项报告_集团汇报件_v3.0_2026-11-14.md")
t = open(MD, encoding="utf-8").read()

# ── 拆 CH9_CALIB 为三节 ──
i5 = CH9_CALIB.find("### （五）")
i6 = CH9_CALIB.find("### （六）")
CAL4 = CH9_CALIB[:i5].rstrip()
CAL5 = CH9_CALIB[i5:i6].rstrip()
CAL6 = CH9_CALIB[i6:].rstrip()
CONC = CH9_CONC.replace("### （八）本章结论", "### （九）本章结论")

# ── 旧第九章的 (二)(三)(五停业)(六敏感性) 保留 ──
def chapter(text, prefix):
    m = re.search(r"^## " + re.escape(prefix) + r".*$", text, re.M)
    if not m: return None
    s = m.start()
    m2 = re.search(r"^## ", text[m.end():], re.M)
    e = m.end() + m2.start() if m2 else len(text)
    return text[s:e]
def sub(text, prefix, head):
    ch = chapter(text, prefix)
    if not ch: return None
    m = re.search(r"^### " + re.escape(head) + r".*$", ch, re.M)
    if not m: return None
    s = m.start()
    m2 = re.search(r"^### ", ch[m.end():], re.M)
    e = m.end() + m2.start() if m2 else len(ch)
    return ch[s:e]

old9 = chapter(t, "九、经济测算结果")
assert old9, "未找到第九章"
o2 = sub(old9, "九、经济测算结果", "（二）收入与盈利能力")
o3 = sub(old9, "九、经济测算结果", "（三）业主现金流与项目回报（20 年财务评价口径）")
o5 = sub(old9, "九、经济测算结果", "（五）停业方案的经济差异（20 年财务评价口径，不计停业期内部收益率）")
o6 = sub(old9, "九、经济测算结果", "（六）敏感性")
L("保留节:", bool(o2), bool(o3), bool(o5), bool(o6))
# 敏感性标题改序号
if o6: o6b = o6.replace("### （六）敏感性", "### （八）敏感性")
else: o6b = ""
if o5: o5b = o5.replace("### （五）停业方案的经济差异", "### （七）停业方案的经济差异")
else: o5b = ""

NEW9 = ("## 九、经济测算结果\n\n" + CH9_MOUTH + "\n\n" + (o2 or "") + "\n\n" + (o3 or "") + "\n\n"
        + CAL4 + "\n\n" + CAL5 + "\n\n" + CAL6 + "\n\n" + (o5b or "") + "\n\n" + (o6b or "") + "\n\n" + CONC)
t = t.replace(old9, NEW9)
L("第九章已替换")

# ── 第五章 (五)(六) 整体替换 ──
ch5 = chapter(t, "五、改造方案比选与品牌选择")
assert ch5, "未找到第五章"
i = ch5.find("### （五）逐方向优劣")
if i != -1:
    tail_new = CH5_NEW + "\n"
    ch5n = ch5[:i] + tail_new
    t = t.replace(ch5, ch5n)
    L("第五章已替换")

# ── 第十一章 替换 ──
ch11 = chapter(t, "十一、结论与建议")
assert ch11, "未找到第十一章"
t = t.replace(ch11, CH11_NEW.rstrip() + "\n\n")
L("第十一章已替换")

# ── 全文散点口径修正 ──
FIX = [
 ("四个方向的 10 年国资考核口径结果见第九章第四节。",
  "四个方向在三重口径下的对照结果见第九章第四节。"),
 (">**须同时注意：按国资委 10 年口径复核，三个方向在\"一次全停业\"下均不达标（详见第九章第四节）；分项说明见结论部分第 4 条。**",
  ">**须同时注意：内部收益率须按三套口径分别列示，详见第九章第四节；全口径下四个方向净现值均为负，成因与应对见结论部分第六条。**"),
 ("以下比较详见第九章第五节。", "以下比较详见第九章第七节。"),
 ("| 停业期声誉（全渠道口径） | 复业后第 1 年营收折损 8.5%、第 2 年 3.0%、一次性渠道重建 1.2%，合计相当于稳态年营收的 12.7% | 分六类渠道测算：国内在线旅行社平台 42%、国际在线旅行社 18%、品牌会员 14%、协议客户与商旅 16%、旅行社与团队 5%、会议婚宴与本地 5%（详见第九章第三节） |",
  "| 停业期声誉（全渠道口径） | 复业后第 1 年营收折损 8.5%、第 2 年 3.0%、一次性渠道重建 1.2%，合计相当于稳态年营收的 12.7% | 分六类渠道测算：国内在线旅行社平台 42%、国际在线旅行社 18%、品牌会员 14%、协议客户与商旅 16%、旅行社与团队 5%、会议婚宴与本地 5%（详见附件细项概算表 v2.0） |"),
 ("| **集团\"十五五\"规划**| 总府列为六家改造项目之一；\"继续以国际品牌委托经营模式运营\"；2030 年营业现金毛流量约 2,500 万元、利润总额亏损控制在约 300 万元 |**规划作为决策参照与目标指引，不构成时间与方式的硬性约束；本报告测算按工程量与品牌标准独立推导，两者不一致时以工程与市场事实为准**|",
  "| **集团\"十五五\"规划**| 总府列为六家改造项目之一；改造投资 1.8 亿元、回收期 5.6 年、内部收益率 17.00%；第二批（2027—2029 年）；\"营业现金毛流量\"定义为净利润加折旧摊销 |**规划作为决策参照与目标指引，不构成时间与方式的硬性约束；本报告测算按工程量与品牌标准独立推导，两者不一致时以工程与市场事实为准。**回收期与内部收益率口径见第九章第五节|"),
 ("会计口径，与国资\"营业现金毛流量\"统计口径相关",
  "建议采用集团《改革发展情况汇报材料》附件 6 口径：营业现金毛流量为净利润加折旧摊销"),
 ("| 停业期声誉损失 | 已计入 | 1,389 至 1,630 | 全渠道六类口径，见第九章第三节 |",
  "| 停业期声誉损失 | 已计入 | 1,389 至 1,630 | 全渠道六类口径，见附件细项概算表 v2.0 |"),
]
for a, b in FIX:
    if a in t:
        t = t.replace(a, b); L("[FIX]", esc(a[:34]))
    else:
        L("[MISS]", esc(a[:34]))

# ── 附件说明：更新口径描述 ──
t = t.replace("（2026 年 11 月 13 日，13 个工作表：口径说明、方向总览、客房改造分项、公共区域分项、投资构成明细、停业期现金流、20 年现金流、10 年国资口径复核、声誉损失分渠道、敏感性分析、停业方案对比、逐月现金流、数据源与口径）",
              "（2026 年 11 月 14 日，26 个工作表：口径说明、方向总览、客房改造分项、公共区域分项、投资构成明细、停业期现金流、20 年现金流、三重口径校准与集团 715 定稿对照、声誉损失分渠道、敏感性分析、停业方案对比、逐月现金流、停业损失构成、参数与假设、数据源清单）")

# ── 残留检查 ──
L("\n=== 残留检查 ===")
for k in ("10 年国资", "10年国资", "国资委 10 年", "国资 10 年", "10 年门槛", "10年门槛",
          "10 年考核口径", "10 年窗口", "回收期不超过 10"):
    c = t.count(k)
    if c: L("  [残留]", k, c)
for k in ("19.93%", "12.48%", "3,198", "5-8 年", "回收期 7 年", "1.8 亿元", "超支",
          "34 号令", "第五节", "第九章第七节"):
    L("  %-14s %s" % (k, "在" if k in t else "缺"))

open(MD3, "w", encoding="utf-8").write(t)
os.remove(MD)
os.rename(MD3, MD)
L("\nMD bytes:", len(t.encode("utf-8")))

sys.path.insert(0, r"D:\B166ER-openclaw\workspace\.tmp")
from md2docx_cn import convert
out = os.path.join(REP, "总府皇冠改造_立项报告_集团汇报件_v3.0_2026-11-14.docx")
convert(MD, out)
L("DOCX %.1f KB" % (os.path.getsize(out)/1024))
old = os.path.join(REP, "总府皇冠改造_立项报告_集团汇报件_v2.0_2026-11-13.docx")
if os.path.exists(old):
    try: os.remove(old); L("removed v2.0")
    except Exception as e: L("SKIP(locked) v2.0")

from docx import Document
d = Document(out)
n = 0
for ti, tb in enumerate(d.tables, 1):
    for ri, row in enumerate(tb.rows):
        for ci, cell in enumerate(row.cells):
            if cell.text.strip() in ("", "\u2014", "-", "\uff0f", "/"):
                n += 1
                L("  BLANK 表%d 行%d 列%d : %s" % (ti, ri, ci, " || ".join(esc(c.text.strip()[:26]) for c in row.cells)))
L("表格 %d，空白格 %d" % (len(d.tables), n))
L("DONE")
