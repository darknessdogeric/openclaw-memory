# -*- coding: utf-8 -*-
"""v109：清除星号 + 数据源清单补携程条目 + 重建全部交付 + 终检"""
import io, os, re, sys, glob, json, subprocess
from docx import Document
from openpyxl import load_workbook
sys.stdout.reconfigure(encoding="utf-8")
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
T = r"D:\B166ER-openclaw\workspace\.tmp"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
PY = r"C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe"
MD = os.path.join(KB, "总府皇冠改造_可行性研究报告_v6.0_2026-11-15.md")

# ── 1. 清除星号 ──
s = io.open(MD, encoding="utf-8").read()
n0 = s.count("\u2605")
s = s.replace("#### 3.2.1 \u2605 ", "#### 3.2.1 ")
s = s.replace("\u2605 ", "").replace("\u2605", "")
io.open(MD, "w", encoding="utf-8").write(s)
print("星号清除：%d -> %d" % (n0, s.count("\u2605")))

# ── 2. 数据源清单补携程条目 ──
ap = os.path.join(KB, "_calc", "v102_attach.py")
lines = io.open(ap, encoding="utf-8").read().split("\n")
idx = [i for i, l in enumerate(lines) if l.strip().startswith('["B-10"')]
assert len(idx) == 1
new = [
 '    ["B-11", "\u643a\u7a0b\u5b98\u65b9\u9875\uff08\u603b\u5e9c\u7687\u51a0\uff0c\u9152\u5e97\u7f16\u53f7 19857058\uff09", "\u8bc4\u5206 4.7\uff08\u8d85\u68d2\uff09\u30018,018 \u6761\u8bc4\u8bba\uff1b\u5206\u9879\uff1a\u536b\u751f 4.8\u3001\u73af\u5883 4.8\u3001\u670d\u52a1 4.8\u3001\u8bbe\u65bd 4.6\uff08\u6700\u4f4e\uff09\uff1b\u6807\u7b7e\uff1a\u6625\u7199\u8def 640 \u7c73\u3001\u592a\u53e4\u91cc 680 \u7c73\u3001IFS 470 \u7c73\u3001\u5929\u5e9c\u5e7f\u573a 1.0 \u516c\u91cc\uff1b\u623f\u578b\u9762\u79ef\uff1a\u6807\u51c6\u623f 30 \u5e73\u65b9\u7c73\u3001\u5957\u623f 50 \u5e73\u65b9\u7c73", "hotels.ctrip.com/map/19857058.html\uff0c2026-11-15 \u8054\u7f51\u590d\u6838", "\u4e3b\u6e90\uff1b\u4e0e\u4e1a\u4e3b\u53f0\u8d26\u7684 402 \u95f4\u3001\u4f4d\u7f6e\u5206\u4ea4\u53c9\u5370\u8bc1"],',
 '    ["B-12", "\u643a\u7a0b\u7cfb\u5206\u9500\u5546\u4e0e\u76f8\u4e92\u5f3a\u8de8\u5e73\u53f0\u6302\u677f\u4ef7\uff08\u603b\u5e9c\u7687\u51a0\u3001\u6e29\u6c5f\u7687\u51a0\uff09", "\u603b\u5e9c\u7687\u51a0\uff1a\u9ad8\u7ea7\u53cc\u5e8a\u623f 728 \u5143\u8d77\u3001\u7687\u51a0\u5957\u623f 50 \u5e73\u65b9\u7c73 1,268 \u5143\u8d77\u3001\u4e2d\u65c5\u6e20\u9053\u6807\u51c6\u623f\u4f18\u60e0\u4ef7 998 \u5143\u3001\u6c38\u5b89\u65c5\u884c\u9ad8\u7ea7\u623f 398 \u5143/\u4eba\uff1b\u6e29\u6c5f\u7687\u51a0\uff1a\u9ad8\u7ea7\u623f 39 \u5e73\u65b9\u7c73 698 \u5143\u8d77\u3001\u6c5f\u666f\u623f 798 \u5143\u8d77\u3001\u884c\u653f\u623f 998 \u5143\u8d77\u3001\u7687\u51a0\u9ad8\u7ea7\u5957\u623f 60 \u5e73\u65b9\u7c73 1,098 \u5143\u8d77", "huixiaoer\u3001huixiaotong\u3001wingontravel\u3001ctscd\uff0c2026-11-15 \u8054\u7f51\u590d\u6838", "\u643a\u7a0b\u53e3\u5f84\u4e3b\u6e90\uff08\u542b\u670d\u52a1\u8d39\uff09\uff1b\u4e0e Agoda \u6700\u4f4e\u4ef7\u6863\u4ea4\u53c9"],',
 '    ["B-13", "\u6d32\u81f3\u5962\u9009\u9152\u5e97\u5b98\u65b9\u95ee\u7b54\uff08\u642d\u914d\u4e0e\u623f\u578b\u9762\u79ef\u6743\u5a01\u53e3\u5f84\uff09", "\u5171\u8bbe 336 \u95f4\u5ba2\u623f\uff0c\u5ba2\u623f\u9762\u79ef 45 \u5e73\u65b9\u7c73\u8d77\uff1b\u6807\u51c6\u623f 45 \u5e73\u65b9\u7c73\u3001\u5e0c\u534e\u7279\u5927\u5e8a\u623f 52 \u5e73\u65b9\u7c73\u3001\u5c0a\u4eab\u623f 58 \u5e73\u65b9\u7c73\u3001\u4eb2\u5b50\u4e3b\u9898\u5957\u623f 106 \u5e73\u65b9\u7c73\u3001\u5927\u4f7f\u5957\u623f 157 \u5e73\u65b9\u7c73\u3001\u603b\u7edf\u5957\u623f 264 \u5e73\u65b9\u7c73", "\u65b0\u534e\u7f51\u8f6c\u8f7d\u9152\u5e97\u5b98\u65b9\u95ee\u7b54\uff082026-11 \u590d\u6838\uff09\uff1b\u643a\u7a0b\u7cfb\u5206\u9500\u5546\u623f\u578b\u9762\u79ef\u4ea4\u53c9\u5370\u8bc1", "\u201c45 \u5e73\u65b9\u7c73\u8d77\u201d\u4e3a\u9152\u5e97\u5b98\u65b9\u53e3\u5f84\uff0c\u975e\u4f30\u7b97\uff1b\u76f4\u63a5\u652f\u6491\u8def\u5f84\u4e8c\u623f\u91cf\u53cd\u63a8"],',
 '    ["B-14", "\u643a\u7a0b\u4e0e\u6210\u4ea4 ADR \u7684\u53e3\u5f84\u533a\u522b\uff08\u672c\u62a5\u544a\u65b9\u6cd5\u8bba\u7ea0\u5173\u952e\uff09", "\u643a\u7a0b\u7cfb\u6302\u677f\u4ef7 680\u20141,268 \u5143\uff0c\u800c\u4e1a\u4e3b\u53f0\u8d26\u5b9e\u9645\u6210\u4ea4 ADR 412.09 \u5143\uff08\u53e3\u5f84 A \u542b 10% \u670d\u52a1\u8d39\uff09\uff0c\u76f8\u5dee 1.65\u20143.08 \u500d\uff1b\u5dee\u989d\u6765\u81ea\u534f\u8bae\u4ef7\u4f53\u7cfb\uff08370\u2014500 \u5143\uff09\u4e0e\u4f1a\u5458\u4ef7\u3001\u4fc3\u9500\u7ed3\u6784", "\u643a\u7a0b\u5b98\u65b9\u9875 + \u4e1a\u4e3b\u53f0\u8d26\u4ea4\u53c9\u9a8c\u7b97", "\u2605 \u672c\u62a5\u544a\u5168\u90e8\u6d4b\u7b97\u4e00\u5f8b\u91c7\u7528\u6210\u4ea4\u53e3\u5f84\uff1bOTA \u6302\u677f\u4ef7\u4ec5\u7528\u4e8e\u5224\u65ad\u4ef7\u683c\u5929\u82b1\u677f\uff0c\u76f4\u63a5\u4ee5\u5176\u63a8\u7b97 ADR \u4f1a\u7cfb\u7edf\u6027\u9ad8\u4f30\u6536\u5165"],',
]
lines[idx[0]+1:idx[0]+1] = new
io.open(ap, "w", encoding="utf-8").write("\n".join(lines))
print("数据源清单已补 B-11 至 B-14")

# ── 3. 重建附件与 Word ──
for script in ("v102_attach.py", "v100_docx.py"):
    r = subprocess.run([PY, os.path.join(KB, "_calc", script)], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=900,
                       env=dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1"))
    print("%s -> rc=%d" % (script, r.returncode))
print(open(os.path.join(T, "v17.log"), encoding="utf-8").read().strip().split("\n")[-1])

# ── 4. 终检 ──
DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v6.0_2026-11-15.docx")
XLSX = os.path.join(CAL, "总府皇冠改造_可行性研究报告_测算附表_v6.0_2026-11-15.xlsx")
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
print()
print("=" * 74); print("=== 最终终检 ==="); print("=" * 74)
print("Word  {0:.1f} KB｜段落 {1}｜表格 {2}｜空白格 {3}｜节 {4}｜图片 {5}｜emoji {6}｜★ {7}".format(
    os.path.getsize(DOCX)/1024, len(d.paragraphs), len(d.tables), blank, len(d.sections),
    nimg, len(re.findall(EMO, alltext)), alltext.count("\u2605")))
print("      目录 {0} 条｜每节页码域 {1}｜横向节 {2}".format(
    len(toc), [x.footer._element.xml.count('w:instr="PAGE"') for x in d.sections],
    sum(1 for x in d.sections if x.page_width > x.page_height)))
wb = load_workbook(XLSX, data_only=True)
print("Excel {0:.1f} KB｜{1} 表".format(os.path.getsize(XLSX)/1024, len(wb.sheetnames)))
print("MD    {0} 字｜图 {1}｜★ {2}".format(len(md), len(re.findall(r"!\[", md)), md.count("\u2605")))
KEY = ["\uff0b3,021", "\u221219,699", "\u221222,862", "\u221224,046", "9.30%", "2.21%", "2.37%", "1.36%",
       "11,066", "21,054", "24,119", "24,340", "9,884", "6,442.73", "5,403.53", "\u2212416.51",
       "60,914.78", "14,382", "60,677", "2,088.85", "10,192", "25.35", "1,280", "416.29", "107.90",
       "43 \u6b21", "0.0017", "2029-09-27", "\u22125,227", "209 \u95f4", "205 \u95f4", "14.69",
       "1,020 \u4ef6", "84.22%", "\u4fdd\u7559\u90e8\u5206\u57fa\u6750", "\u786e\u5b9a\u6027\u65b9\u6848\u610f\u89c1",
       "\u8bf7\u96c6\u56e2\u9009\u62e9\u6267\u884c\u8def\u5f84", "\u5206\u6279\u9a8c\u6536\u4e0d\u53ef\u884c",
       "\u524d\u7f6e\u4ef7\u683c\u9a8c\u8bc1", "3+3", "\u6ca1\u6709\u4e00\u5bb6\u662f\u56fd\u9645\u8054\u53f7",
       # 携程口径新增
       "728 \u5143\u8d77", "1,268 \u5143\u8d77", "698 \u5143\u8d77", "1,588 \u5143\u8d77", "1,098 \u5143\u8d77",
       "30 \u5e73\u65b9\u7c73", "39 \u5e73\u65b9\u7c73", "40 \u5e73\u65b9\u7c73", "45 \u5e73\u65b9\u7c73",
       "8,018 \u6761", "9,495 \u6761", "\u8bbe\u65bd 4.6", "\u5ba2\u623f\u8d28\u7d20\u53ca\u8212\u9002\u5ea6 7.7",
       "1,632 \u95f4", "654 \u95f4", "\u4e0d\u5b58\u5728\u8be5\u72ec\u7acb\u7269\u4e1a", "1,588"]
mw = [k for k in KEY if k not in alltext]; mm = [k for k in KEY if k not in md]
print("关键值（%d 项） Word 缺失: %s" % (len(KEY), mw if mw else "无"))
print("关键值（%d 项） MD   缺失: %s" % (len(KEY), mm if mm else "无"))
print("硬约束: 轻改 {0}｜4.08亿 {1}｜1.8亿 {2}｜不改造 {3}｜四季度 {4}".format(
    md.count("\u8f7b\u6539"), md.count("4.08"), md.count("1.8 \u4ebf"),
    md.count("\u4e0d\u6539\u9020"), md.count("\u56db\u5b63\u5ea6")))
print("桌面根目录总府残留: {0}".format(len(glob.glob(r"C:\Users\ericz\Desktop\*\u603b\u5e9c*"))))
print("DONE")

