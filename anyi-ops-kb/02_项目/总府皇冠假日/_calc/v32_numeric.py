# -*- coding: utf-8 -*-
"""v32：数值归一化一致性比对（消除千分位/负号/小数位伪差异）+ 页脚页码域核查 + 真差异修复"""
import io, os, sys, re, json, glob, unicodedata
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v32.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

MD = os.path.join(KB, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.docx")
XLSX = os.path.join(CAL, "总府皇冠改造_可行性研究报告_测算附表_v3.0_2026-11-14.xlsx")

def nums(text):
    """抽取文本中全部数字，归一化为 float 集合（去千分位、统一负号、去尾零）"""
    t = text.replace("\u2212", "-").replace("\u2013", "-").replace("\u2014", "-")
    t = t.replace(",", "")
    out = set()
    for m in re.finditer(r"-?\d+(?:\.\d+)?", t):
        try:
            v = float(m.group(0))
            out.add(round(v, 4))
        except Exception:
            pass
    return out

md = open(MD, encoding="utf-8").read()
mdn = nums(md)
from docx import Document
d = Document(DOCX)
doct = "\n".join(p.text for p in d.paragraphs) + "\n" + "\n".join(c.text for tb in d.tables for r in tb.rows for c in r.cells)
don = nums(doct)

from openpyxl import load_workbook
wb = load_workbook(XLSX)

def check(ws, name, r0, cols, label):
    bad = []
    for rr in range(r0, ws.max_row + 1):
        k = ws.cell(row=rr, column=1).value
        if not (isinstance(k, str) and k.startswith("S")): continue
        for cn, ci in cols:
            v = ws.cell(row=rr, column=ci).value
            if v is None or isinstance(v, str): continue
            f = float(v)
            if abs(f) < 1e-9: continue
            cands = {round(f, 4), round(abs(f), 4)}
            if abs(f) < 1:  # 比率类
                cands |= {round(f * 100, 4), round(abs(f) * 100, 4)}
                cands |= {round(f * 100, 2), round(abs(f) * 100, 2)}
            if round(abs(f) * 100, 4) == round(f * 100, 4): pass
            hit_m = bool(cands & mdn); hit_d = bool(cands & don)
            if not (hit_m and hit_d):
                bad.append((k, cn, v, hit_m, hit_d))
    L("%s 不一致: %d" % (label, len(bad)))
    for b in bad: L("   ⚠ %s %s=%r md=%s doc=%s" % b)
    return bad

ws8 = wb["08 九方案造价总表"]
COLS8 = [("改造投资", 10), ("总资金需求", 11), ("平均房价", 12), ("改造后收入", 13), ("收入增量", 15),
         ("收入倍数", 16), ("全口径IRR", 17), ("净现值", 18), ("集团口径IRR", 20), ("集团回收期", 21)]
b8 = check(ws8, "08 九方案总表", 5, COLS8, "正文↔Excel 08")

ws10 = wb["10 三口径对照"]
COLS10 = [("改造投资", 2), ("平均房价", 3), ("改造后收入", 4), ("收入增量", 6), ("收入倍数", 7),
          ("全口径IRR", 8), ("净现值", 9), ("集团口径IRR", 11), ("集团回收期", 12)]
b10 = check(ws10, "10 三口径", 5, COLS10, "正文↔Excel 10")

# 15 表：分档定价与市场
ws15 = wb["15 分档定价与市场层级"]
L("=== 15 表关键值抽查 ===")
for rr in range(1, ws15.max_row + 1):
    a = ws15.cell(row=rr, column=1).value
    b = ws15.cell(row=rr, column=2).value
    if a in ("五星级", "五星至奢华之间", "奢华（主流带）", "奢华（顶级设计型带）"):
        vals = str(ws15.cell(row=rr, column=3).value)
        for v in re.findall(r"\d+", vals):
            ok = float(v) in mdn
            L("   档次 %s 取值 %s → %s" % (a, v, "在正文" if ok else "⚠缺"))

# 页脚页码域
L("=== 页脚核查 ===")
for si, s in enumerate(d.sections):
    fx = s.footer._element.xml
    has_p = "PAGE" in fx
    # 抽取页脚可见文本
    vis = " ".join(p.text for p in s.footer.paragraphs)
    # 域结果数
    instr = re.findall(r"<w:instrText[^>]*>([^<]*)</w:instrText>", fx)
    L("   S%d 页码域:%s 指令:%s 可见:%r" % (si, has_p, instr, vis[:50]))
L("fldChar 总数:", d.element.xml.count("fldChar") + sum(s.footer._element.xml.count("fldChar") for s in d.sections))
L("DONE")
