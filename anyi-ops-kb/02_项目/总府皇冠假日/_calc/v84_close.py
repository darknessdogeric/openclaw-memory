# -*- coding: utf-8 -*-
"""v84：v5.0 收官 —— 补风险 R-22/R-23；清除旧版残留校验词；重建 Word；终检"""
import io, os, sys, re, json, glob, subprocess
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v84.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
MD5 = os.path.join(KB, "总府皇冠改造_可行性研究报告_v5.0_2026-11-14.md")
lines = open(MD5, encoding="utf-8").read().split("\n")
FAIL = []
def find(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix):
            return i
    return -1

# ── ① 风险表补 R-22 / R-23 ──
idx = None
for i in range(len(lines) - 1, -1, -1):
    if re.match(r"^\|\s*R-\d+\s*\|", lines[i]):
        idx = i; break
if idx is None:
    FAIL.append("风险表"); L("[MISS]", "风险表")
else:
    lines[idx + 1:idx + 1] = [
     "| R-22 | 品牌客房面积要求高于本物业承载能力，导致可行房量大幅缩减、收入基数不足 | 高 | 高 | 高 | 瑞吉 65 ㎡、丽晶 60 ㎡ 等要求下房量降至 145—157 间，较现状减少 245—257 间；须以品牌方书面确认的基础房型面积要求为前提，并以三改二后的实际房量重算收入 |",
     "| R-23 | 改造范围未按 A/B/C 三档分级即锁定整体改造，导致不可逆投入 | 中 | 高 | 高 | 建议在第三方安全评估结论出具前，仅推进 A/B 两档可行性论证与成本预留，不启动整体改造的不可逆拆改；待消防与机电可分离性结论明确后再行决策 |",
    ]
    L("[OK]   风险表已补 R-22/R-23")

# ── ② 旧版残留：第五章（七）内的旧表述清理 ──
n = 0
for i, l in enumerate(lines):
    if "轻改" in l and "不是轻改" in l:
        lines[i] = l.replace("不是轻改——轻改（保留主体、局部翻新）", "不是局部翻新——保留主体式翻新")
        n += 1
    elif "轻改" in l:
        lines[i] = l.replace("轻改", "局部翻新")
        n += 1
L("[MD] 轻改表述改写: {0} 处".format(n))
text = "\n".join(lines)

# ── ③ 第五章（七）在地文化：补与品牌适配的关系（用户第 16 条）──
i = text.find("### （七）在地文化价值挖掘")
if i < 0:
    FAIL.append("第五章（七）"); L("[MISS]", "第五章（七）")
else:
    j = text.find("### （八）", i)
    seg = text[i:j]
    ADD = """
**在地文化与品牌遴选的关系，须准确界定三点。**

**其一，文化在本项目中的作用是品牌适配，不是价格工具。** 本报告第九章的十二品牌测算中，平均房价一律取自成都同档次品牌的实测或同档次样本推定，**没有任何一个价格假设来自"加了文化所以能卖更高"**。**任何价格带都可以做文创，文创本身不产生房价溢价**；它能做的是让产品在同价格带中具备可识别性。

**其二，文化是品牌遴选的一条硬标准。** 候选品牌方中，谁能承接总府街的在地叙事（街市与盐、影剧与戏曲、蜀锦与丝路三段母题）、谁的品牌标准允许在地元素进入客房与公区设计，须作为品牌方书面答复事项之一，随 PIP 前期策划文件一并提出（见第五章（五）3）。

**其三，文化是谈判筹码。** 在地文化资产是业主方在本项目品牌谈判中最具独立价值的部分——它是物业自带的、无法由品牌方复制的资产。**这一价值应体现在"品牌方承担部分改造投入"的谈判条件上（第九章路径 P2，权重最大的净现值改善项 +9,873.6 万元），而不是体现在房价假设上。**

**其四，内容投入须有商业机制与判定标准。** 建议年度内容预算 180 至 250 万元（对应"1 名文化主理人＋一年 2 次主展＋每月 1 次活动＋机构共创"的最低可行节律），从可保留项节约中划转，不新增改造投资总额；判定指标为策展溢价指数不低于 1.15、导览与工坊参与率不低于 35%、非房收入占比两年内提升至 20% 以上、客群文化动机占比不低于 40%、复购率不低于 20%，任一项在复业后第 12 个月不达标即停止追加。

"""
    text = text[:i] + seg.rstrip("\n") + "\n\n" + ADD.strip("\n") + "\n\n" + text[j:]
    L("[OK]   第五章（七）补入文化与品牌适配关系")

open(MD5, "w", encoding="utf-8").write(text)
L("[MD] 写入 {0} bytes".format(len(text.encode("utf-8"))))

# ── ④ Word 重建 ──
D = os.path.join(KB, "_calc")
src = open(os.path.join(D, "v17_docx.py"), encoding="utf-8").read()
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.md", "总府皇冠改造_可行性研究报告_v5.0_2026-11-14.md")
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.docx", "总府皇冠改造_可行性研究报告_v5.0_2026-11-14.docx")
open(os.path.join(D, "v17_docx_v5.py"), "w", encoding="utf-8").write(src)
subprocess.run([r"C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe", os.path.join(D, "v17_docx_v5.py")],
               capture_output=True, text=True, encoding="utf-8", errors="replace")
for l in open(os.path.join(T, "v17.log"), encoding="utf-8", errors="replace").read().split("\n"):
    if l.strip(): L(l.rstrip())

# ── ⑤ 终检 ──
from docx import Document as D2
DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v5.0_2026-11-14.docx")
d = D2(DOCX)
paras = [p.text for p in d.paragraphs]
alltext = "\n".join(paras) + "\n" + "\n".join(c.text for tb in d.tables for r in tb.rows for c in r.cells)
blank = sum(1 for tb in d.tables for r in tb.rows for c in r.cells if c.text.strip() in ("", "\u2014", "-", "\uff0f", "/"))
EMO = ("[" + chr(92) + "U0001F300-" + chr(92) + "U0001FAFF" + chr(92) + "U00002600-" + chr(92) + "U000027BF"
       + chr(92) + "U00002B50" + chr(92) + "uFE0F" + chr(92) + "u200D" + chr(92) + "u2764" + chr(92) + "u2B06"
       + chr(92) + "u2B07" + chr(92) + "u2B05" + chr(92) + "u274C" + chr(92) + "u2705" + chr(92) + "u26A0"
       + chr(92) + "u26A1" + chr(92) + "u2139" + chr(92) + "u24C2" + chr(92) + "u2B55]")
L("=== 终检 ===")
L("{0:.1f} KB | 段落 {1} | 表格 {2} | 空白格 {3} | 节 {4}".format(os.path.getsize(DOCX)/1024, len(d.paragraphs), len(d.tables), blank, len(d.sections)))
for i, s in enumerate(d.sections):
    L("   S{0} {1} {2:.0f}x{3:.0f} 页码域{4}".format(i, "横" if s.page_width>s.page_height else "纵", s.page_width.cm, s.page_height.cm, s.footer._element.xml.count('w:instr="PAGE"')))
L("emoji:", len(re.findall(EMO, alltext)))
KEYS = ["427.4","72.55%","6,774.1","4,551.8","15,064.3","+6,499.1","11.55%","8.11%","10,192","31,412.82",
 "11,060.0","14.92","1,147","21,448.5","282 间","230 间","65 ㎡","50 ㎡","文华东方","丽晶","康莱德","柏悦",
 "Sofitel","六善","洲至奢选","LXR","2029-03-27","建设工程消防设计审查验收管理暂行规定","58 号","锦发改发〔2025〕30 号",
 "2026-12-31","可分离性","决策预研","R-22","R-23","策展溢价指数","成都院子","轻改","2,915","10,720"]
miss = [k for k in KEYS if k not in alltext]
L("关键值缺失:", miss if miss else "无（{0} 项全中）".format(len(KEYS)))
for ab in ("ADR","RevPAR","CAPEX","NPV","IRR","GOP"):
    n = len(re.findall(r"\b"+ab+r"\b", alltext))
    if n: L("   ⚠ 英文缩写 {0} ×{1}".format(ab, n))
for o in ("保留石材","2026 年四季度","本报告此前","纠错","唯一全判据成立"):
    if o in alltext: L("   ⚠ 残留: {0}".format(o))
md5 = open(MD5, encoding="utf-8").read()
m = re.search(r"^## 目录\n", md5, re.M)
ls = md5[m.end():].split("\n")
start = next((i for i, l in enumerate(ls) if l.startswith("## ")), None)
toc = [re.sub(r"^\d+\. ", "", l).strip() for l in ls[:start] if re.match(r"^\d+\. ", l)]
bod = [l[3:].strip() for l in ls[start:] if l.startswith("## ")]
L("目录↔正文: {0}（目录 {1} / 正文 {2}）".format(toc == bod, len(toc), len(bod)))
L("章节数:", len(re.findall(r"^## 第", md5, re.M)), "| 图:", len(re.findall(r"!\[", md5)),
  "| 风险条数:", len(re.findall(r"\| R-\d+ \|", md5)))
L("失败:", FAIL)
L("DONE")
