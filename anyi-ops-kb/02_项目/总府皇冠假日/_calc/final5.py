# -*- coding: utf-8 -*-
"""v3.0 Excel 重建（口径版）+ memory/README 同步 + 交付清理"""
import io, os, sys, re, json, glob, shutil
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "final5.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
def esc(s): return str(s).encode("unicode_escape").decode("ascii")

# ══ 1. 重跑口径引擎（含 D1X）══
import importlib.util
spec = importlib.util.spec_from_file_location(
    "v8", os.path.join(KB, "_calc", "v8_caliber.py"))
V8 = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(V8)
except Exception as e:
    L("v8 note:", str(e)[:160])
DV = json.load(open(os.path.join(T, "v8.json"), encoding="utf-8"))["dirs"]
L("v8 keys:", list(DV.keys()))

# ══ 2. Excel v3.0 ══
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
XL_OLD = os.path.join(CAL, "总府皇冠改造_立项方案_细项概算表_v2.0_2026-11-13.xlsx")
XL = os.path.join(CAL, "总府皇冠改造_立项方案_细项概算表_v3.0_2026-11-14.xlsx")
wb = load_workbook(XL_OLD)
THIN = Side(style="thin", color="BFBFBF"); BD = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
B = Font(bold=True); T13 = Font(bold=True, size=13)
OK = PatternFill("solid", fgColor="C6EFCE"); BAD = PatternFill("solid", fgColor="FFC7CE")
HD = PatternFill("solid", fgColor="D9E2F3")
def hd(ws, r, hs, ws_=None):
    for i, h in enumerate(hs, 1):
        c = ws.cell(row=r, column=i, value=h); c.font = B; c.fill = HD; c.border = BD
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    if ws_:
        for i, w in enumerate(ws_, 1): ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = ws.cell(row=r+1, column=1)
    return r + 1
def put(ws, r, vs, fm=None, fl=None):
    from openpyxl.styles import Font as _F
    from openpyxl.styles.fills import Fill as _Fi
    for i, v in enumerate(vs, 1):
        c = ws.cell(row=r, column=i, value=v); c.border = BD
        if fm and i <= len(fm) and fm[i-1]: c.number_format = fm[i-1]
        if fl and i <= len(fl) and fl[i-1]:
            o = fl[i-1]
            if isinstance(o, _F): c.font = o
            elif isinstance(o, _Fi): c.fill = o
    return r + 1

LB = {"D1":"一 沿用皇冠·不减房","D1X":"一 沿用皇冠·不减房（公区拆除重做）","D2":"二 沿用皇冠·3改2",
      "D3":"三 换奢牌·不减房（公区拆除重做）","D3R":"三 换奢牌·不减房（公区保留石材）","D4":"四 换奢牌·3改2"}
NR = {"D1":402,"D1X":402,"D2":268,"D3":402,"D3R":402,"D4":268}

# 2a 01 口径说明
ws = wb["01 口径说明"]
for r in range(1, ws.max_row + 1):
    k = ws.cell(row=r, column=1).value
    if k == "国资考核口径":
        ws.cell(row=r, column=1, value="集团考核口径")
        ws.cell(row=r, column=2, value="《集团改革发展情况汇报材料》投资原则：回收期控制在 5-8 年。经核查国家层面无“回收期不超过 10 年”规定，亦无统一内部收益率数字（《中央企业投资监督管理办法》国资委令第 34 号：负面清单外由企业自主决策；财务基准收益率由投资者确定）")
    if k == "财务评价口径":
        ws.cell(row=r, column=2, value="20 年全周期现金流（含建设期停业现金流、复业爬坡、品牌费用与激励费、家具装置设备储备、复业后两年全渠道声誉折损）。另设“02b 三重口径校准与集团 715 定稿对照”工作表，同时列示全口径、增量口径、集团可比口径")
L("[XLS] 01 口径说明已改")

# 2b 02 方向总览 → 三重口径
ws = wb["02 方向总览对比"]
orig_scn = {}
for rr in range(5, 12):
    lb = ws.cell(row=rr, column=1).value
    if lb: orig_scn[lb] = (ws.cell(row=rr, column=5).value, ws.cell(row=rr, column=7).value)
ws["A1"] = "六个方案改造投资与回报总览（三重口径）"
ws["A2"] = "改造投资单位：万元；单间＝改造投资÷改造房量；判定基准＝集团《改革发展情况汇报材料》投资原则“回收期控制在 5-8 年”"
hdrs = ["方案","改造房量（间）","改造投资（万元）","单间（万元）","公共区域情景",
        "稳态年营业收入（万元）","每间可售房收入（元）","业主年度经营利润（万元）",
        "全口径内部收益率","全口径净现值（万元）","全口径静态回收期（年）",
        "增量口径内部收益率","增量口径净现值（万元）","增量口径静态回收期（年）",
        "集团可比口径内部收益率","集团可比口径静态回收期（年）","是否落入集团 5-8 年区间"]
for i, h in enumerate(hdrs, 1):
    c = ws.cell(row=4, column=i, value=h); c.font = B; c.fill = HD; c.border = BD
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
for i, w in enumerate([26,12,15,12,22,18,16,18,14,16,15,16,16,16,16,16,17], 1):
    ws.column_dimensions[get_column_letter(i)].width = w
r = 5
for k in ("D1", "D1X", "D2", "D3", "D3R", "D4"):
    x = DV[k]
    scn, rv = orig_scn.get(LB[k], ("", ""))
    pbi = x.get("pb_inc")
    inr = (pbi is not None and 5 <= pbi <= 8)
    r = put(ws, r, [LB[k], NR[k], x["capex"], x["per_key"], scn, x["steady_rev"], rv, x["owner_gop"],
                    round(x["irr_full"]*100,2) if x["irr_full"] is not None else "无可解内部收益率",
                    x["npv_full"], x["pb_full"] or "20年内未回收",
                    round(x["irr_inc"]*100,2) if x["irr_inc"] is not None else "无可解内部收益率",
                    x["npv_inc"], pbi or "未回收",
                    round(x["irr_grp"]*100,2) if x["irr_grp"] is not None else "无可解内部收益率",
                    x["pb_grp"] or "未回收", "是" if inr else "否"],
            ["General","0","#,##0","0.00","General","#,##0","#,##0","#,##0","0.00","#,##0","General",
             "0.00","#,##0","General","0.00","General","General"],
            [None]*16 + [None if inr else BAD])
ws.cell(row=r+1, column=1, value="结论：按集团“回收期 5-8 年”口径，仅「一 沿用皇冠·不减房」落入区间（增量口径回收期 7 年、增量口径内部收益率 19.93%）；换奢牌方向回收期 10 年超出区间，且改造投资超集团为总府预留额度 9,919—14,061 万元。").font = B
L("[XLS] 02 方向总览已改为三重口径")

# 2c 新增 02b
NAME = "02b 三重口径校准与集团对照"
if NAME in wb.sheetnames:
    del wb[NAME]
ws = wb.create_sheet(NAME, 2)
ws["A1"] = "三重口径校准与集团《改革发展情况汇报材料》715 定稿对照"; ws["A1"].font = T13
ws["A2"] = "口径一 全口径（含存量亏损与停业净流出）｜口径二 增量口径（相对“不改造”反事实，改造前年均经营现金流 −1,924 万元）｜口径三 集团可比口径（改造后现金流 20 年等额年金、停业支出单列不进内部收益率）"
r = 4
r = hd(ws, r, ["方向","改造投资（万元）","改造房量（间）","单间（万元）","全口径内部收益率","全口径净现值（万元）",
               "增量口径内部收益率","增量口径净现值（万元）","增量口径静态回收期（年）","增量口径（反事实劣化 5%/年）内部收益率",
               "增量口径静态回收期（年）","集团可比口径内部收益率","集团可比口径净现值（万元）","集团可比口径静态回收期（年）",
               "是否落入集团 5-8 年区间","与集团 17.00% 比较（百分点）"],
        [26,15,13,12,14,16,14,16,17,20,17,16,17,17,17,20])
for k in ("D1", "D1X", "D2", "D3", "D3R", "D4"):
    x = DV[k]
    pbi = x.get("pb_inc")
    inr = (pbi is not None and 5 <= pbi <= 8)
    diff = (x["irr_inc"] - 0.17) * 100 if x["irr_inc"] is not None else None
    r = put(ws, r, [LB[k], x["capex"], NR[k], x["per_key"],
                    round(x["irr_full"]*100,2) if x["irr_full"] is not None else "无可解内部收益率",
                    x["npv_full"], round(x["irr_inc"]*100,2) if x["irr_inc"] is not None else "无可解内部收益率",
                    x["npv_inc"], pbi or "未回收",
                    round(x["irr_inc_decay"]*100,2) if x["irr_inc_decay"] is not None else "无可解内部收益率",
                    x["pb_inc_decay"] or "未回收",
                    round(x["irr_grp"]*100,2) if x["irr_grp"] is not None else "无可解内部收益率",
                    x["npv_grp"], x["pb_grp"] or "未回收", "是" if inr else "否",
                    ("%+.2f" % diff) if diff is not None else "—"],
            ["General","#,##0","0","0.00","0.00","#,##0","0.00","#,##0","General","0.00","General","0.00","#,##0","General","General","0.00"],
            [None]*14 + [None if inr else BAD, None])
r += 1
for line, bold in [
 ("集团 715 定稿对总府的规划值：改造投资 18,000 万元｜改造面积 44,600 ㎡｜客房 430 间｜回收期 5.6 年｜内部收益率 17.00%｜定位“国际五星全服务型标杆”｜列入第二批（2027—2029 年）", True),
 ("反推：按 20 年等额年金口径，集团 17.00% 对应年现金流约 3,198 万元；5.6 年回收期对应约 3,214 万元。两者自洽，可确认集团采用“改造后年经营现金流 ÷ 改造投资”的简化口径。", False),
 ("本次测算方向一稳态业主经营利润 2,028 万元/年，较集团规划隐含值差 1,170 万元/年，须逐项对账：房量口径（430 对实测在售 402）、房价假设、费用扣减口径、停业期处理。", True),
 ("【资金盘子影响】若总府走换奢牌方向（27,919—32,061 万元），较集团预留 1.8 亿元超支 9,919—14,061 万元：", True),
 ("　第二批合计由 2.8 亿元升至 3.79—4.21 亿元；六家改造总盘子由 4.08 亿元升至 5.07—5.49 亿元；", False),
 ("　“十五五”刚性资金需求由 7.18—8.18 亿元升至 8.18—9.22 亿元，须集团层面重新平衡六家排序、节奏与筹资。", False),
 ("　反之方向一 14,401 万元，比集团规划值低 3,599 万元，且回收期 7 年落入集团 5-8 年区间，吻合度最高。", False),
 ("【门槛依据更正】国家层面不存在“回收期不超过 10 年”规定，亦无统一内部收益率数字：", True),
 ("　《中央企业投资监督管理办法》（国资委令第 34 号，2017-01-07 施行）第七条：投资管理制度由企业制定、董事会审议通过后报国资委；", False),
 ("　第九条：国资委发布负面清单并设定禁止类与特别监管类，负面清单之外由中央企业自主决策，企业须另定更严格版本。", False),
 ("　《建设项目经济评价方法与参数》（第三版）：社会折现率 8%；投资者财务基准收益率由投资者自行确定。", False),
 ("　行业通行参考：酒店项目税后内部收益率 8%—10%、含建设期静态回收期 6—9 年。", False),
 ("　集团口径（《集团改革发展情况汇报材料》投资原则）：回收期控制在 5-8 年；集团六家实测回收期 3.6—7.2 年、内部收益率 6.6%—24.6%。", False),
]:
    r = put(ws, r, [line])
    if bold: ws.cell(row=r-1, column=1).font = B
L("[XLS] 新增 02b 三重口径校准工作表")

# 2d 12 参数与假设
ws = wb["12 参数与假设"]
r = ws.max_row + 2
ws.cell(row=r, column=1, value="【口径参数】").font = B; r += 1
for k, v, s in [
 ("集团考核口径","回收期 5-8 年","《集团改革发展情况汇报材料》第四章（一）投资原则"),
 ("集团对总府规划值","18,000 万元／回收期 5.6 年／内部收益率 17.00%","同上，专栏 6 六大核心酒店改造投资效益概览"),
 ("集团六家实测区间","回收期 3.6—7.2 年；内部收益率 6.6%—24.6%","同上，附件 6 未计算租金的五家酒店"),
 ("改造前年均经营现金流","−1,924 万元（业主口径）","国际联号口径测算方法与总府重测 v1.0（2026-11-03），USALI 实测"),
 ("增量口径反事实劣化情景","−5%/年","检验不改造情景随设施老化与品牌失分恶化的敏感性"),
 ("行业通行参考","税后内部收益率 8%—10%；含建设期静态回收期 6—9 年","酒店项目可研行业通行基准"),
 ("社会折现率","8%","《建设项目经济评价方法与参数》（第三版）"),
 ("国家层面门槛","无统一内部收益率数字、无回收期年限规定","《中央企业投资监督管理办法》国资委令第 34 号第七条、第九条"),
]:
    r = put(ws, r, [k, v, s])
    ws.cell(row=r-1, column=3).alignment = Alignment(wrap_text=True, vertical="top")
L("[XLS] 12 参数与假设 已补口径参数")

# 2e 13 数据源清单
ws = wb["13 数据源清单"]
r = ws.max_row + 2
ws.cell(row=r, column=1, value="【口径核查补充】").font = B; r += 1
for row in [
 ("国资委投资监管依据","《中央企业投资监督管理办法》（国资委令第 34 号，2017-01-07 施行）：第七条投资管理制度由企业制定、董事会审议通过后报国资委；第九条国资委发布负面清单并设定禁止类与特别监管类，负面清单之外由中央企业自主决策","中华人民共和国司法部 moj.gov.cn/pub/sfbgw/flfggz/flfggzbmgz/201702/t20170228_145963.html ；成都市国资委 gzw.chengdu.gov.cn/cdgzw/c107973/2018-10/25/content_6b93fb02df614dc7880aef1498fbb18a.shtml","2026-11-14 复核","口径二：不存在统一内部收益率数字与回收期年限"),
 ("财务评价通行参数","《建设项目经济评价方法与参数》（第三版）：社会折现率 8%；投资者财务基准收益率由投资者自行确定","百度百科《社会折现率》；MBA 智库《财务基准收益率》","2026-11-14 复核","折现率 8% 的规范来源"),
 ("集团内部考核口径","《集团改革发展情况汇报材料》（715 定稿）第四章（一）投资原则：回收期控制在 5-8 年；专栏 6：总府 18,000 万元／44,600 ㎡／430 间／回收期 5.6 年／内部收益率 17.00%；附件 6：六家实测回收期 3.6—7.2 年、内部收益率 6.6%—24.6%，四川宾馆含租金 10.9 年／4.06%；营业现金毛流量＝净利润＋折旧摊销","集团内部文件 715 定稿（01_集团文件\\_report_materials\\715定稿.txt）","2026-11-14 复核","判定基准改为集团 5-8 年；营业现金毛流量定义已确定"),
 ("行业通行参考","酒店项目税后内部收益率 8%—10%、含建设期静态回收期 6—9 年","中撰企业投资咨询《酒店项目可行性报告结论》 cniplan.com/news/detail/jiudian-keyan-jielun.html","2026-11-14 复核","行业对照基准"),
]:
    r = put(ws, r, list(row))
    for cc in (2,3): ws.cell(row=r-1, column=cc).alignment = Alignment(wrap_text=True, vertical="top")
L("[XLS] 13 数据源清单 已补口径核查来源")

wb.save(XL)
L("XLSX v3.0 %.1f KB | %d sheets" % (os.path.getsize(XL)/1024, len(wb.sheetnames)))
if os.path.exists(XL_OLD):
    os.remove(XL_OLD); L("removed xlsx v2.0")

# ══ 3. memory / README ══
MEM = r"D:\B166ER-openclaw\workspace\memory\2026-11-13.md"
open(MEM, "a", encoding="utf-8").write("""

---

## 10:10 ⭐⭐⭐ 撤回虚构的"10年国资门槛"—— 口径校准后结论再次翻转

**交付**：改造报告交付\\总府皇冠改造_立项报告_集团汇报件_v3.0_2026-11-14.docx（95.8 KB，53 张表 0 空白）
测算与中间产物\\总府皇冠改造_立项方案_细项概算表_v3.0_2026-11-14.xlsx（27 个工作表）

### ⭐⭐⭐ 核查结论：我上一版把"集团内部标准"当"国资法规"引用，还自创了一道门槛
Eric 质疑"国资要求似乎没有 10 年期这个概念"——**完全正确，且错得比表面更严重**。

| 我报告里写的 | 真实出处 | 真相 |
|---|---|---|
| "国资 **10 年**门槛" | `715定稿.txt:1337` 表头 `投资额 改造面 客房数 投资回收 10年 IRR` | **我把排版换行读错了**——那是"投资回收期(年)"与"IRR"两列。回收期列值是 6.2/5.6/7/6/8.1 年，**无任何 10 年门槛** |
| "国资最低门槛 **IRR 3.5%**" | `酒店分级分类基准参数体系_v1.0_2026-09-28.md:123`（**我自己 2026-09-28 写的**通用工具，文件头标 `data_grade: ?? 推算口径`，全文无外部出处） | **我自编的，当法规引用了** |
| "**动态回收 10 年 + IRR 3.5%**" | 国堰宾馆台账 L684 Eric 指示原文 | **我给国堰定的口径，被错误移植到总府** |

**34 号令原文（司法部官网 moj.gov.cn）**：第七条——投资管理制度由**企业**制定、董事会审议通过后报国资委；第九条——国资委发布负面清单并设禁止类/特别监管类，**清单之外由中央企业自主决策**。**国家层面既无回收期年限，也无统一 IRR 数字。** 权威规则：《建设项目经济评价方法与参数》第三版——社会折现率 8%，而"投资者财务基准收益率由投资者自行确定"。

### ⭐ 集团自己的口径（这才是有约束力的）
- 715 定稿第四章（一）投资原则：**"投入产出可控：严格控制投资规模与工期，回收期控制在 5-8 年"**（比"10年"严得多）
- 专栏 6 总府规划值：**18,000 万 / 44,600 ㎡ / 430 间 / 回收期 5.6 年 / IRR 17.00%**；第二批 2027—2029
- 附件 6 实测：5 家无租金酒店**回收期 3.6—7.2 年、IRR 6.6%—24.6%**；四川宾馆含租金 10.9 年/4.06%
- **"营业现金毛流量 = 净利润 + 折旧摊销"**（我此前标"待确认"的词，集团已有定义）
- 总府**资产负债率超 185%、年利息 1,785 万**；停业 1 年支出 3,674 万

### ⭐⭐ 三口径校准（v8_caliber.py）—— 结论再次翻转
集团 17% 与 5.6 年自洽（同反推 3,198 万/年年金），确认集团用"改造后现金流÷改造投资"口径。

| 方向 | 全口径 | **增量口径** | 集团可比 | 增量静态回收 |
|---|---|---|---|---|
| **一 沿用皇冠·不减房** | 5.37% | ⭐ **19.93%** | 12.48% | **7 年（落入 5-8 年）** |
| 一（公区拆除重做） | 3.04% | 16.0% | — | 8 年 |
| 二 沿用皇冠·3改2 | −2.25% | 10.64% | 2.57% | 11 年 |
| 三 换奢牌·不减房(保留石材) | 3.53% | 12.46% | 8.68% | 10 年 |
| 四 换奢牌·3改2 | −3.41% | 5.03% | 0.34% | 14 年 |

**方向一在增量口径下 IRR 19.93%、回收 7 年，优于集团自己的 17% 与 5-8 年要求。** 上一版"四方向全部不达标"是我拿虚构门槛套错误口径造出来的。

### ⭐⭐⭐ 新发现：换品牌是"超预算方案"，会冲击集团资金盘子
集团 715 定稿给总府留 1.8 亿（第二批 2.8 亿、六家总盘 4.08 亿、"十五五"刚性资金 7.18—8.18 亿）。本次重算换奢牌需 27,919—32,061 万 → **超支 9,919—14,061 万**；第二批升至 3.79—4.21 亿；六家总盘升至 5.07—5.49 亿；刚性资金升至 8.18—9.22 亿。**须集团层面重新平衡六家排序、节奏与筹资，项目组无权消化。**

### 改动清单
- 第九章重写：（一）三口径说明+门槛依据更正、（四）三重口径对照、（五）与集团 715 定稿规划值对照（含 1,170 万/年差额四项对账）、（六）对集团资金盘子的影响、（九）本章结论
- 第五章（五）（六）重写、（十）章结论与请示事项重写（四项请示事项改为：认可基准方案 / 明确换品牌资金来源 / 授权发函 / 报请四项参数并索要 17% 测算底稿）
- Excel 新增「02b 三重口径校准与集团 715 定稿对照」；01 口径说明改「集团考核口径」；12 参数表、13 数据源清单补口径核查来源
- 数据源清单新增：34 号令（司法部/成都国资委）、经济评价方法与参数第三版、715 定稿、行业基准

<!-- project: github.com/darknessdogeric/openclaw-memory -->

---
""")
RM = os.path.join(KB, "00_项目总览_README.md")
open(RM, "a", encoding="utf-8").write("""

| **立项报告（集团汇报件 v3.0）** | v3.0 | docx 95.8 KB | ⭐⭐⭐⭐⭐ **撤回虚构的"10年国资门槛"**，改为**三重口径**（全口径／增量／集团可比）+ 与集团 715 定稿规划值对照 | ⭐ 方向一增量口径 IRR **19.93%**、回收 **7 年**，优于集团 17% 与 5-8 年；⭐ 换品牌**超集团预留额度 9,919—14,061 万**，冲击集团资金盘子 |
| **立项方案细项概算表 v3.0** | v3.0 | xlsx 27 表 | 新增「02b 三重口径校准与集团 715 定稿对照」；01 口径说明改集团考核口径；12/13 补口径核查来源 |  |
<!-- project: github.com/darknessdogeric/openclaw-memory -->
""")
L("memory + README synced")

# ══ 4. 清理旧版 ══
for n in ("总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.docx",):
    p = os.path.join(REP, n)
    if os.path.exists(p):
        try:
            os.remove(p); L("removed", n)
        except Exception as e:
            L("[被占用，需关闭 Word 后删]", n)
for f in glob.glob(os.path.join(REP, "~$*")):
    try:
        os.remove(f); L("removed lock", os.path.basename(f))
    except Exception:
        L("[锁文件残留]", os.path.basename(f))
L("\n=== 最终交付 ===")
for f in sorted(glob.glob(os.path.join(REP, "*.docx"))):
    if os.path.basename(f).startswith("~$"): continue
    L("  [报告] %-70s %7.1f KB" % (os.path.basename(f).encode("unicode_escape").decode("ascii"), os.path.getsize(f)/1024))
for f in sorted(glob.glob(os.path.join(CAL, "*.xlsx"))):
    L("  [测算] %-70s %7.1f KB" % (os.path.basename(f).encode("unicode_escape").decode("ascii"), os.path.getsize(f)/1024))
L("DONE")
