# -*- coding: utf-8 -*-
"""v3.0 最终收尾：补录四川省与国家级依据（报告正文 + 数据源清单 docx + Excel）"""
import io, os, sys, re
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "final6.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
def esc(s): return str(s).encode("unicode_escape").decode("ascii")

MD = os.path.join(KB, "总府皇冠改造_立项报告_集团汇报件_v3.0_2026-11-14.md")
t = open(MD, encoding="utf-8").read()

# ══ 1. 报告第九章第一节：补省级依据 ══
OLD = "对总府具有实际约束力的是集团内部口径"
NEW = ("省级层面同构。《四川省属国有企业投资监督管理办法（试行）》第五条明确省国资委制定省属企业投资项目负面清单并分类监管，"
       "第八条明确企业投资管理制度应经董事会审议通过后书面报告省国资委，第十一条明确分户确认主业、培育业务及非主业投资比例；"
       "该办法强调提高资本回报与严控非主业投资，但同样未设定任何统一的内部收益率数字或投资回收期年限。"
       "该办法另配套监督检查要点、审查事项及红线清单、投资项目请示报告材料清单。\n\n"
       "对总府具有实际约束力的是集团内部口径")
if OLD in t and "四川省属国有企业投资监督管理办法" not in t:
    t = t.replace(OLD, NEW, 1)
    L("[MD] 已补四川省办法依据")
else:
    L("[MD] 四川省依据", "已存在" if "四川省属国有企业投资监督管理办法" in t else "锚点缺失")

# 出 Word
sys.path.insert(0, r"D:\B166ER-openclaw\workspace\.tmp")
from md2docx_cn import convert
out = os.path.join(REP, "总府皇冠改造_立项报告_集团汇报件_v3.0_2026-11-14.docx")
convert(MD, out)
L("DOCX %.1f KB" % (os.path.getsize(out)/1024))

# 重新设大纲级别
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
TMP = os.path.join(T, "_v3_nav2.docx")
d = Document(out)
def set_outline(p, lvl):
    pPr = p._p.get_or_add_pPr()
    for old in pPr.findall(qn("w:outlineLvl")):
        pPr.remove(old)
    e = OxmlElement("w:outlineLvl"); e.set(qn("w:val"), str(lvl)); pPr.append(e)
cnt = {"0": 0, "1": 0, "2": 0}
for p in d.paragraphs:
    tx = p.text.strip()
    if not tx or len(tx) > 60:
        continue
    if re.match(r"^\d+\. [一二三四五六七八九十]+、", tx):
        continue
    lvl = None
    if tx == "关于总府皇冠假日酒店改造升级工作思路的报告":
        lvl = 0
    elif re.match(r"^[一二三四五六七八九十]+、\S", tx):
        lvl = 1
    elif re.match(r"^（[一二三四五六七八九十]+）", tx):
        lvl = 2
    elif re.match(r"^\d+\.\d+\s", tx):
        lvl = 2
    if lvl is not None:
        set_outline(p, lvl); p.paragraph_format.keep_with_next = True; cnt[str(lvl)] += 1
d.save(TMP)
import shutil; shutil.move(TMP, out)
L("大纲级别 L0=%d L1=%d L2=%d" % (cnt["0"], cnt["1"], cnt["2"]))

d = Document(out)
blank = 0
for ti, tb in enumerate(d.tables, 1):
    for ri, row in enumerate(tb.rows):
        for ci, cell in enumerate(row.cells):
            if cell.text.strip() in ("", "\u2014", "-", "\uff0f", "/"):
                blank += 1
                L("  BLANK 表%d 行%d 列%d" % (ti, ri, ci))
L("docx: 段落 %d / 表格 %d / 空白格 %d" % (len(d.paragraphs), len(d.tables), blank))

# ══ 2. 数据源清单 docx 追加 4 条 ══
DS = os.path.join(REP, "总府皇冠改造_立项方案_数据源清单_v1.0_2026-11-13.docx")
if os.path.exists(DS):
    from docx.shared import Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn as _qn
    dd = Document(DS)
    tb = dd.tables[0]
    NEWROWS = [
     ("国家及行业政策依据（投资监管）",
      "《中央企业投资监督管理办法》（国资委令第 34 号，2017-01-07 施行）第七条：企业投资管理制度应经董事会审议通过后报国资委；第九条：国资委发布中央企业投资项目负面清单并设定禁止类与特别监管类，负面清单之外的投资项目由中央企业自主决策，企业应在国资委负面清单基础上制定本企业更为严格具体的负面清单",
      "中华人民共和国司法部 moj.gov.cn/pub/sfbgw/flfggz/flfggzbmgz/201702/t20170228_145963.html；成都市国资委 gzw.chengdu.gov.cn/cdgzw/c107973/2018-10/25/content_6b93fb02df614dc7880aef1498fbb18a.shtml",
      "2026-11-14 复核",
      "口径依据：国家层面不设统一内部收益率数字、不设投资回收期年限"),
     ("省级投资监管依据",
      "《四川省属国有企业投资监督管理办法（试行）》第五条：省国资委制定省属企业投资项目负面清单并分类监管；第八条：企业投资管理制度应经董事会审议通过后书面报告省国资委；第十一条：分户确认、动态管理企业主业、培育业务及非主业投资比例。该办法强调提高资本回报、严控非主业投资，未设定统一内部收益率数字或回收期年限。另配套监督检查要点、审查事项及红线清单、投资项目请示（报告）材料清单",
      "四川省国资委 gzw.sc.gov.cn/scsgzw/CU230403/2017/12/19/5418945fa1a64fc4a9834239c892cd48.shtml；四川省政府 sc.gov.cn；知政策网 zhizhengce.com",
      "2026-11-14 复核",
      "口径依据：省级层面同构，仍无统一收益率门槛"),
     ("财务评价通行参数",
      "《建设项目经济评价方法与参数》（第三版）：社会折现率规定为 8%，供各类建设项目评价时统一采用；投资者财务基准收益率由投资者自行确定（一般为其最低可接受收益率加行业与项目投资风险报酬率）",
      "百度百科《社会折现率》；MBA 智库《财务基准收益率》",
      "2026-11-14 复核",
      "折现率 8% 的规范来源；财务基准收益率由投资者确定"),
     ("集团内部考核口径与总府规划值",
      "《集团改革发展情况汇报材料》（715 定稿）第四章（一）投资原则：投入产出可控，回收期控制在 5-8 年；专栏 6：总府皇冠假日酒店改造投资 18,000 万元、改造面积 44,600 ㎡、客房 430 间、回收期 5.6 年、内部收益率 17.00%，列入第二批（2027—2029 年）；附件 6：六家改造酒店营业现金毛流量＝净利润＋折旧摊销，未计算租金的五家回收期 3.6—7.2 年、内部收益率 6.6%—24.6%，四川宾馆含市场化租金回收期 10.9 年、内部收益率 4.06%；另记总府资产负债率超 185%、年利息支出约 1,785 万元",
      "集团内部文件 715 定稿（anyi-ops-kb\\01_集团文件\\_report_materials\\715定稿.txt）",
      "2026-11-14 复核",
      "判定基准改为集团 5-8 年；营业现金毛流量定义已确定；总府规划值对照基准"),
     ("行业通行参考",
      "酒店项目税后内部收益率应高于行业基准收益率（通常 8%—10%），含建设期静态投资回收期宜控制在 6—9 年；财务净现值按基准折现率 8% 计算须大于零",
      "中撰企业投资咨询《酒店项目可行性报告结论》 cniplan.com/news/detail/jiudian-keyan-jielun.html",
      "2026-11-14 复核",
      "行业对照基准"),
    ]
    for row in NEWROWS:
        cells = tb.add_row().cells
        for j, v in enumerate(row):
            cells[j].text = ""
            p = cells[j].paragraphs[0]
            if j in (0, 3):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(v); r.font.size = Pt(9); r.font.name = "仿宋"
            r._element.rPr.rFonts.set(_qn("w:eastAsia"), "仿宋")
    dd.save(DS)
    L("数据源清单追加 5 条 -> %d 条, %.1f KB" % (len(tb.rows) - 1, os.path.getsize(DS) / 1024))

# ══ 3. Excel 13 表补录 ══
XL = os.path.join(CAL, "总府皇冠改造_立项方案_细项概算表_v3.0_2026-11-14.xlsx")
if os.path.exists(XL):
    from openpyxl import load_workbook
    from openpyxl.styles import Font, Alignment, Border, Side
    wb = load_workbook(XL)
    ws = wb["13 数据源清单"]
    r = ws.max_row + 1
    B = Font(bold=True)
    THIN = Side(style="thin", color="BFBFBF"); BD = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
    def put(ws, r, vs):
        for i, v in enumerate(vs, 1):
            c = ws.cell(row=r, column=i, value=v); c.border = BD
        return r + 1
    for row in NEWROWS:
        r = put(ws, r, list(row))
        for cc in (2, 3):
            ws.cell(row=r - 1, column=cc).alignment = Alignment(wrap_text=True, vertical="top")
    ws.cell(row=r, column=1, value="【口径核查结论】国家与省级层面均无“投资回收期不超过 10 年”规定、无统一内部收益率数字；有约束力的是集团“回收期 5-8 年”内部口径。此前版本所称“国资委 10 年门槛”系编制方误读集团材料表头所致，已在 v3.0 中撤回。").font = B
    wb.save(XL)
    L("Excel 13 表已补录, %.1f KB" % (os.path.getsize(XL) / 1024))

# ══ 4. memory ══
MEM = r"D:\B166ER-openclaw\workspace\memory\2026-11-13.md"
open(MEM, "a", encoding="utf-8").write("""

**补充（2026-11-14 上午）**：省级依据亦已核实 ——《四川省属国有企业投资监督管理办法（试行）》第五条省国资委制定负面清单分类监管、第八条企业投资制度经董事会审议后书面报省国资委、第十一条分户确认主业与培育业务比例；**同样无统一内部收益率数字、无回收期年限规定**。国家与省级结构一致，结论闭环。数据源清单已补录 5 条（34 号令、四川办法、经济评价方法与参数第三版、集团 715 定稿口径、行业通行基准）。
<!-- project: github.com/darknessdogeric/openclaw-memory -->
""")
L("memory 追加完成")
L("DONE")
