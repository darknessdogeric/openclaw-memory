# -*- coding: utf-8 -*-
"""v34 收官：重生成公文 Word（页码域已修复）＋ 全面终检 ＋ 交付确认"""
import io, os, sys, re, json, glob, shutil, subprocess
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v34.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

# ① 重建 v3 版转换脚本（继承已修复的 v17）
D = os.path.join(KB, "_calc")
src = open(os.path.join(D, "v17_docx.py"), encoding="utf-8").read()
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.md", "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.docx", "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.docx")
open(os.path.join(D, "v17_docx_v3.py"), "w", encoding="utf-8").write(src)
PY = r"C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe"
subprocess.run([PY, os.path.join(D, "v17_docx_v3.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
lg = os.path.join(T, "v17.log")
for l in open(lg, encoding="utf-8", errors="replace").read().split("\n"):
    if l.strip(): L(l.rstrip())

# ② 全面终检
from docx import Document
DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.docx")
MD = os.path.join(KB, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
md = open(MD, encoding="utf-8").read()
d = Document(DOCX)
paras = [p.text for p in d.paragraphs]
alltext = "\n".join(paras) + "\n" + "\n".join(c.text for tb in d.tables for r in tb.rows for c in r.cells)

L("=== 一、公文版式 ===")
L("文件 %.1f KB | 段落 %d | 表格 %d | 节 %d" % (os.path.getsize(DOCX) / 1024, len(d.paragraphs), len(d.tables), len(d.sections)))
blank = sum(1 for tb in d.tables for r in tb.rows for c in r.cells if c.text.strip() in ("", "\u2014", "-", "\uff0f", "/"))
L("空白格: %d" % blank)
for i, s in enumerate(d.sections):
    L("   S%d %s %.0fx%.0f | 页码域数 %d" % (i, "横" if s.page_width > s.page_height else "纵",
        s.page_width.cm, s.page_height.cm, s.footer._element.xml.count("w:instr=\"PAGE\"")))
L("红头/发文机关: %s | 发文字号: %s | 主送: %s" % (
    "有" if any("安逸酒店集团有限责任公司" == p.strip() for p in paras) else "无",
    "有" if any("安逸产发〔2026〕" in p for p in paras) else "无",
    "有" if any("主送" in p for p in paras) else "无"))
L("目录: %s | 请示事项: %s | 落款: %s" % (
    "有" if any(p.strip() in ("目 录", "目录") for p in paras) else "无",
    "有" if any("请示事项" in p for p in paras) else "无",
    "有" if any("以上报告，请审阅" in p for p in paras) else "无"))
emo = len(re.findall("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\u24C2\u2B55]", alltext))
L("emoji: %d" % emo)
for ab in ("ADR", "RevPAR", "CAPEX", "NPV", "IRR", "GOP"):
    n = len(re.findall(r"\b%s\b" % ab, alltext))
    if n: L("   ⚠ 英文缩写 %s ×%d" % (ab, n))
for o in ("6.13%", "2.45%", "−2.67%", "−4.08%", "1.8 亿元", "4.08 亿", "六家", "待填", "TODO"):
    if o in alltext: L("   ⚠ 残留: %s" % o)

L("=== 二、章节与目录 ===")
chs = [p.strip() for p in paras if re.match(r"^第[一二三四五六七八九十]+章", p.strip())]
uniq = []
for c in chs:
    if c not in uniq: uniq.append(c)
L("章标题 %d（去重）:" % len(uniq))
for c in uniq: L("   %s" % c)
m = re.search(r"^## 目录\n", md, re.M)
ls = md[m.end():].split("\n")
start = next((i for i, l in enumerate(ls) if l.startswith("## ")), None)
toc = [re.sub(r"^\d+\. ", "", l).strip() for l in ls[:start] if re.match(r"^\d+\. ", l)]
bod = [l[3:].strip() for l in ls[start:] if l.startswith("## ")]
L("MD 目录↔正文: %s（目录 %d / 正文 %d）" % (toc == bod, len(toc), len(bod)))

L("=== 三、关键数据命中 ===")
KEYS = ["1,500", "1,750", "3,000", "11.33%", "16,916.8", "6,774.0", "518.5", "5.61", "31,229.1",
        "38,003.1", "22,168.5", "14,009.8", "10,938.7", "7,292.5", "9,339.9", "33,252.7",
        "40.48 万家", "1,979 万间", "2,000—3,000", "1,180—1,800", "736.66", "4,602.96",
        "21,313.6", "31,093.6", "4,538.7", "11,060", "S7B", "134 家", "3,000 元"]
miss = [k for k in KEYS if k not in alltext]
L("缺失: %s" % (miss if miss else "无（%d 项全中）" % len(KEYS)))

L("=== 四、Excel 附表 ===")
from openpyxl import load_workbook
XL = os.path.join(CAL, "总府皇冠改造_可行性研究报告_测算附表_v3.0_2026-11-14.xlsx")
wb = load_workbook(XL)
L("%.1f KB | %d sheets" % (os.path.getsize(XL) / 1024, len(wb.sheetnames)))
ws8 = wb["08 九方案造价总表"]
L("08 行 %d 列 %d" % (ws8.max_row, ws8.max_column))
ws15 = wb["15 分档定价与市场层级"]
L("15 行 %d 列 %d" % (ws15.max_row, ws15.max_column))

L("=== 五、交付清单 ===")
for p in sorted(glob.glob(os.path.join(REP, "总府皇冠改造_可行性研究报告*"))) + sorted(glob.glob(os.path.join(CAL, "总府皇冠改造_可行性研究报告*"))):
    L("  %6.1f KB  %s" % (os.path.getsize(p) / 1024, os.path.basename(p)))
L("桌面根目录总府残留: %d" % len(glob.glob(r"C:\Users\ericz\Desktop\*总府*")))
L("DONE")
