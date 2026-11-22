# -*- coding: utf-8 -*-
"""v30 终稿收口：英文缩写中文化；重出公文 Word；Excel 英文化清理；全面终检"""
import io, os, sys, re, json, glob, shutil
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v30.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

MD = os.path.join(KB, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
t = open(MD, encoding="utf-8").read()

# ① 英文缩写中文化
REP_MAP = [
 ("重庆 2024 年五星 ADR 736.66 元", "重庆 2024 年五星级平均房价 736.66 元"),
 ("每间可售房收入（RevPAR）", "每间可售房收入"),
 ("RevPAR 不足 200 元", "每间可售房收入不足 200 元"),
 ("RevPAR", "每间可售房收入"),
 ("ADR", "平均房价"),
 ("CAPEX", "改造投资"),
 ("NPV", "净现值"),
 ("IRR", "内部收益率"),
 ("GOP率", "部门营业利润率"),
 ("GOP", "部门营业利润率"),
]
for a, b in REP_MAP:
    n = t.count(a)
    if n: t = t.replace(a, b); L("[MD] %-28s -> %-14s ×%d" % (a[:28], b[:14], n))
open(MD, "w", encoding="utf-8").write(t)
left = [w for w in ("ADR", "RevPAR", "CAPEX", "NPV", "IRR", "GOP") if re.search(r"\b%s\b" % w, t)]
L("[MD] 残留英文缩写:", left if left else "无")

# ② Excel 英文化清理
from openpyxl import load_workbook
XL = os.path.join(CAL, "总府皇冠改造_可行性研究报告_测算附表_v3.0_2026-11-14.xlsx")
wb = load_workbook(XL)
cnt = 0
for nm in wb.sheetnames:
    ws = wb[nm]
    for rr in ws.iter_rows():
        for c in rr:
            if isinstance(c.value, str):
                v = c.value
                for a, b in (("RevPAR", "每间可售房收入"), ("ADR", "平均房价"), ("CAPEX", "改造投资"),
                             ("NPV", "净现值"), ("IRR", "内部收益率"), ("GOP", "部门营业利润率")):
                    if a in v: v = v.replace(a, b); cnt += 1
                if v != c.value: c.value = v
L("[XLS] 英文缩写替换:", cnt)
# Sheet 名英文化
for nm in list(wb.sheetnames):
    if nm == "08 八方案造价总表":
        wb[nm].title = "08 九方案造价总表"
wb.save(XL)
L("[XLS] sheets:", wb.sheetnames)

# ③ 重出公文 Word（直接调用，不经 os.system）
import subprocess
PY = r"C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe"
r = subprocess.run([PY, os.path.join(KB, "_calc", "v17_docx_v3.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
lg = os.path.join(T, "v17.log")
if os.path.exists(lg):
    for l in open(lg, encoding="utf-8", errors="replace").read().split("\n"):
        if l.strip(): L(l.rstrip())

# ④ 全面终检
DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.docx")
L("=== Word 终检 ===")
L("存在:", os.path.exists(DOCX), "| %.1f KB" % (os.path.getsize(DOCX) / 1024))
from docx import Document
d = Document(DOCX)
paras = [p.text for p in d.paragraphs]
alltext = "\n".join(paras) + "\n" + "\n".join(c.text for tb in d.tables for r in tb.rows for c in r.cells)
blank = sum(1 for tb in d.tables for r in tb.rows for c in r.cells if c.text.strip() in ("", "\u2014", "-", "\uff0f", "/"))
L("段落 %d / 表格 %d / 空白格 %d / 节 %d" % (len(d.paragraphs), len(d.tables), blank, len(d.sections)))
orient = []
for i, s in enumerate(d.sections):
    orient.append("S%d:%s %.0fx%.0f" % (i, "横" if s.page_width > s.page_height else "纵", s.page_width.cm, s.page_height.cm))
L("页面:", " | ".join(orient))
xml = d.element.xml
L("目录域 TOC:", "TOC" in xml, "| 页码域 PAGE:", "PAGE" in xml, "| 字体设定:", "仿宋" in xml or "方正" in xml)
EMO = "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\u24C2\u2B55]"
L("emoji:", len(re.findall(EMO, alltext)))
KEYS = ["1,500", "1,750", "3,000", "11.33", "16,916.8", "6,774.0", "518.5", "5.61", "31,229.1",
        "40.48 万家", "1,979 万间", "2,000—3,000", "1,180—1,800", "736.66", "4,602.96",
        "21,313.6", "31,093.6", "4,538.7", "S7B", "38,003.1", "22,168.5", "14,009.8", "10,938.7"]
miss = [k for k in KEYS if k not in alltext]
L("关键数字缺失:", miss if miss else "无（全部命中）")
chs = [p.strip() for p in paras if re.match(r"^第[一二三四五六七八九十]+章", p.strip())]
L("章节数:", len(chs))
for ab in ("ADR", "RevPAR", "CAPEX", "NPV", "IRR", "GOP"):
    n = len(re.findall(r"\b%s\b" % ab, alltext))
    if n: L("   ⚠ Word 英文缩写 %s × %d" % (ab, n))
for o in ("6.13%", "2.45%", "−2.67%", "−4.08%", "1.8 亿元", "4.08 亿", "六家"):
    if o in alltext: L("   ⚠ 旧数/参照系:", o)
L("=== Word 终检完成 ===")

# ⑤ 清理旧版 + 桌面残留
for p in (os.path.join(REP, "总府皇冠改造_可行性研究报告_v2.0_2026-11-14.docx"),):
    if os.path.exists(p):
        try: os.remove(p); L("removed", os.path.basename(p))
        except Exception as e: L("[仍被占用]", os.path.basename(p))
L("桌面根目录总府残留:", len(glob.glob(r"C:\Users\ericz\Desktop\*总府*")))
L("交付目录 Word:", [os.path.basename(x) for x in glob.glob(os.path.join(REP, "总府皇冠改造_可行性研究报告*.docx"))])
L("测算目录 XLSX:", [os.path.basename(x) for x in glob.glob(os.path.join(CAL, "总府皇冠改造_可行性研究报告*.xlsx"))])
L("DONE")
