# -*- coding: utf-8 -*-
"""总装：替换章节 + 修正事实 + 术语中文化 + 出 Word + 数据源清单"""
import io, os, sys, re, glob, shutil
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
LOG = open(os.path.join(T, "assemble.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
sys.path.insert(0, os.path.join(KB, "_calc"))
from new_chapters import CH2, CH6, CH9
from new_blocks import CH4_D, CH5_D, CH11, HEAD_FINAL, TAIL_FINAL

MD = os.path.join(KB, "总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.md")
t = open(MD, encoding="utf-8").read()

# ══ 工具：按 H2 标题替换整章 ══
def replace_chapter(text, title_prefix, new_body):
    m = re.search(r"^## " + re.escape(title_prefix) + r".*$", text, re.M)
    if not m:
        L("[MISS chapter]", title_prefix); return text
    start = m.start()
    m2 = re.search(r"^## ", text[m.end():], re.M)
    end = m.end() + m2.start() if m2 else len(text)
    L("[CH replaced]", title_prefix, "len", end - start)
    return text[:start] + new_body.rstrip() + "\n\n" + text[end:]

def replace_sub(text, chapter_prefix, sub_head, new_body):
    m = re.search(r"^## " + re.escape(chapter_prefix) + r".*$", text, re.M)
    if not m:
        L("[MISS chapter for sub]", chapter_prefix); return text
    ch_start = m.start()
    m2 = re.search(r"^## ", text[m.end():], re.M)
    ch_end = m.end() + m2.start() if m2 else len(text)
    ch = text[ch_start:ch_end]
    sm = re.search(r"^### " + re.escape(sub_head) + r".*$", ch, re.M)
    if not sm:
        L("[MISS sub]", chapter_prefix, "|", sub_head); return text
    s_start = sm.start()
    m3 = re.search(r"^### ", ch[sm.end():], re.M)
    s_end = sm.end() + m3.start() if m3 else len(ch)
    L("[SUB replaced]", chapter_prefix, "|", sub_head)
    return text[:ch_start] + ch[:s_start] + new_body.rstrip() + "\n\n" + ch[s_end:] + text[ch_end:]

# ① 章节替换
t = replace_chapter(t, "二、市场调研", CH2)
t = replace_sub(t, "四、改造可行性", "（四）两种停业方案的经济差异", CH4_D)
t = replace_sub(t, "五、改造方案比选与品牌选择", "（五）逐方向优劣", CH5_D)
t = replace_chapter(t, "六、投资构成与隐性成本专项", CH6)
t = replace_chapter(t, "九、经济测算结果", CH9)
t = replace_chapter(t, "十一、结论与建议", CH11)

# ② 事实修正：博舍→居舍
n_boshe = t.count("博舍")
t = t.replace("博舍", "居舍")
L("博舍→居舍:", n_boshe)

# ③ 品牌落地状态修正（联网复核新事实）
OLD_BRAND = """| 傲途格 Autograph | 万豪 | 无项目 |  门槛最低、专收编有故事的历史物业 |
| ~~洲至奢选~~ | IHG |  已开业 |  排除 |
| ~~丽晶~~ | IHG |  已签约 |  排除 |
| ~~文华东方~~ | MO |  2028 开业 |  排除 |
| ~~瑰丽/凯宾斯基~~ | 雅高系 |  在营 |  排除 |"""
NEW_BRAND = """| 傲途格 Autograph | 万豪 | 无项目 |  门槛最低、专收编有故事的历史物业 |
| ~~洲至奢选~~ | 洲际酒店集团 |  已在营（棕榈泉 336 间，2026 年翻新） |  排除 |
| ~~丽晶~~ | 洲际酒店集团 |  已签约（2026-07-15，计划 2029Q3 开业） |  排除 |
| ~~费尔蒙~~ | 雅高／费尔蒙 |  **已在营**（成都棕榈泉费尔蒙，2016 开业，2026 翻新） |  排除 |
| ~~托尼洛·兰博基尼~~ | 独立奢华 |  **2026-03-28 天府广场开业**（西南首家，总投约 24 亿元） |  排除 |
| ~~丽笙精选~~ | 锦江丽笙 |  **2026-06-16 中国—欧洲中心开业**（西南首家，178 间） |  排除 |
| ~~文华东方~~ | 半岛集团 |  2028 开业 |  排除 |
| ~~瑰丽／凯宾斯基~~ | 雅高系 |  在营 |  排除 |
| ~~居舍（原博舍）~~ | 太古酒店 |  在营（2025-10 已更名居舍） |  排除 |"""
if OLD_BRAND in t:
    t = t.replace(OLD_BRAND, NEW_BRAND); L("[OK] 品牌候选表修正")
else:
    L("[MISS] 品牌候选表")

# ④ 声誉：单平台→全渠道
REP_OLD_1 = "| 停业期声誉 | Agoda 评分由 9.4 降至 7.6 | 停业前主动沟通与\"改造故事\"传播； 评分传导 ADR，5 分制 +1 分 ≈ ADR +11.2% |"
REP_NEW_1 = "| 停业期声誉（全渠道口径） | 复业后第 1 年营收折损 8.5%、第 2 年 3.0%、一次性渠道重建 1.2%，合计相当于稳态年营收的 12.7% | 分六类渠道测算：国内在线旅行社平台 42%、国际在线旅行社 18%、品牌会员 14%、协议客户与商旅 16%、旅行社与团队 5%、会议婚宴与本地 5%（详见第九章第三节） |"
if REP_OLD_1 in t:
    t = t.replace(REP_OLD_1, REP_NEW_1); L("[OK] 声誉行 1")
else:
    L("[MISS] 声誉行 1")

REP_OLD_2 = "| 8 |**停业期声誉损失**|**约 150 万元**|**未计入**| Agoda 评分由 9.4 降至 7.6；网评 +0.1 相当于 900–1,000 间夜/年 |"
REP_NEW_2 = "| 8 |**停业期声誉损失**|方向一 1,389 万元／方向三 1,630 万元|**已计入**|全渠道六类口径；体现为复业后两年营收折损与一次性渠道重建费用，已计入 20 年现金流 |"
if REP_OLD_2 in t:
    t = t.replace(REP_OLD_2, REP_NEW_2); L("[OK] 声誉行 2")
else:
    L("[MISS] 声誉行 2")

t = t.replace("| 停业期声誉与评分继续下滑 |  中 | 停业前主动沟通与\"改造故事\"传播 | 停业前 |",
              "| 停业期声誉与评分继续下滑（全渠道） |  中 | 停业前主动沟通与\"改造故事\"传播；分渠道对账 | 停业前 |")
t = t.replace("| 停业期声誉与评分继续下滑（Agoda 由 9.4 降至 7.6） |**高**| 中 | 中 | 停业前主动沟通与\"改造故事\"传播；网评 +0.1 相当于 900–1,000 间夜/年 | 酒店运营 | 停业前 |",
              "| 停业期声誉与评分继续下滑（全渠道六类口径） |**高**| 中 | 中 | 停业前主动沟通与\"改造故事\"传播；分渠道对账与复业后两年营收折损监控 | 酒店运营 | 停业前 |")

# ⑤ 十五五：刚性→参照
t = t.replace("| **集团\"十五五\"规划**| 总府列为六家改造项目之一；\"继续以国际品牌委托经营模式运营\"；2030 年营业现金毛流量约 2,500 万元、利润总额亏损控制在约 300 万元 |**项目时间表与经营目标由规划给定，非项目自选**|",
              "| **集团\"十五五\"规划**| 总府列为六家改造项目之一；\"继续以国际品牌委托经营模式运营\"；2030 年营业现金毛流量约 2,500 万元、利润总额亏损控制在约 300 万元 |**规划作为决策参照与目标指引，不构成时间与方式的硬性约束；本报告测算按工程量与品牌标准独立推导，两者不一致时以工程与市场事实为准**|")
t = t.replace("| 规划与政策 | 安逸酒店集团\"十五五\"规划修订稿 OCR 全文及权威要点；",
              "| 规划与政策 | 安逸酒店集团\"十五五\"规划修订稿 OCR 全文及权威要点（作为参照依据，非硬约束）；")
t = t.replace("| S7 |  集团层面政策与任务支撑 | 十五五规划列为六家改造项目之一；旗舰标杆打造行动；旗舰旗舰物业区位 |",
              "| S7 |  集团层面政策与任务支撑 | 十五五规划列为六家改造项目之一（参照依据，非时间硬约束）；旗舰标杆打造行动；旗舰旗舰物业区位 |")
t = t.replace("（五）财务可行性\n\n>**详见第九部分及附件 2 三个方向全维度经济测算表",
              "（五）财务可行性\n\n>**详见第九部分及附件 1 细项概算表 v2.0")
t = t.replace("> 中性情景 20 年口径结论：方向二 IRR**9.49%**、NPV**+2,944 万元**、静态回收期**9.7 年**。",
              "> 中性情景 20 年口径结论见第九章第三节；四个方向的 10 年国资考核口径结果见第九章第四节。")
t = t.replace("> **须同时注意：按国资委 10 年口径复核，三个方向在\"一次全停业\"下均不达标（详见第九部分第四节）；分项说明见结论部分第 4 条。**",
              "> **须同时注意：按国资委 10 年口径复核，四个方向在\"一次全停业\"下均不达标（详见第九章第四节）；成因与应对见第十一章结论部分第四、五条。**")
t = t.replace("| **5.1** | **规划与政策** | **15** | 安逸酒店集团十五五规划修订稿 OCR 全文与权威要点 | 刚性：项目时间表、改造路径与经营目标由规划给定 |",
              "| **5.1** | **规划与政策** | **15** | 安逸酒店集团十五五规划修订稿 OCR 全文与权威要点 | 参照：规划给出目标指引，实际时点与方式按工程与市场条件确定 |")

# ⑥ 术语中文化
TERMS = [
 ("CAPEX", "改造投资"), ("NPV", "净现值"), ("ADR", "平均房价"), ("OCC", "出租率"),
 ("RevPAR", "每间可售房收入"), ("GOP 率", "部门营业利润率"), ("业主 GOP", "业主部门营业利润"),
 ("HMA", "酒店管理公司"), ("FF&E", "家具装置设备"), ("PIP", "周期性翻新改造"),
 ("key money", "品牌入场投资"), ("MICE", "会议与会展"), ("USALI", "酒店业统一会计制度"),
 ("CRS/CRM", "中央预订系统与客户关系管理系统"), ("FLS", "品牌方服务标准"),
]
for a, b in TERMS:
    c = t.count(a)
    t = t.replace(a, b)
    if c: L("[TERM]", a, "->", b, c)
# IRR 逐个（避免误伤）
c_irr = len(re.findall(r"\bIRR\b", t))
t = re.sub(r"\bIRR\b", "内部收益率", t)
L("[TERM] IRR -> 内部收益率", c_irr)
# VI 视觉识别
t = t.replace("VI 替换", "视觉识别系统替换").replace("品牌专项（VI 全套）", "品牌专项（视觉识别系统全套）")
t = t.replace("VI 全套", "视觉识别系统全套").replace("会员身份与积分不可继承", "会员身份与积分不可继承")
t = t.replace("系统、VI 全部延续", "系统、视觉识别系统全部延续")
# OTA → 在线旅行社平台（保留首次全称）
t = t.replace("OTA 评分扣分项", "在线旅行社平台评分扣分项").replace("OTA 依赖度", "在线旅行社平台依赖度")
t = t.replace("OTA 佣金", "在线旅行社平台佣金").replace("OTA 渠道", "在线旅行社平台渠道")
t = t.replace("OTA 平台", "在线旅行社平台").replace("OTA 口径", "在线旅行社平台口径")
t = t.replace("Agoda", "Agoda（安可达）")
t = t.replace("MGM Collection", "MGM 精选系列").replace("MGM 精选系列", "MGM 精选系列")
t = t.replace("Kimpton", "金普顿").replace("Fairmont", "费尔蒙")
t = t.replace("Autograph", "傲途格").replace("Niccolo", "尼依格罗")
t = t.replace("Radisson Collection", "丽笙精选").replace("The Temple House", "居舍")
t = t.replace("Upper House", "居舍")
t = t.replace("IHG Connect", "洲际酒店集团智能客控系统")
t = t.replace("IHG", "洲际酒店集团")
t = t.replace("MO", "半岛集团")
t = t.replace("LRA", "长住客房").replace("FIT", "协议客户")
t = t.replace("R-25", "R-25")
t = t.replace("STR 三档竞争组", "行业统计机构三档竞争组")
t = t.replace("STR 竞争组", "行业统计机构竞争组")
t = t.replace("（STR）", "（行业统计机构）")
t = t.replace("STR ", "行业统计机构 ")
t = t.replace("STR口径", "行业统计机构口径")
t = t.replace("B2 发电机房", "地下二层发电机房")
t = t.replace("B1F", "地下一层").replace("B2F", "地下二层").replace("1F", "首层").replace("4F", "四层").replace("2F", "二层").replace("3F", "三层")
t = t.replace("21F", "二十一层").replace("5#", "五号").replace("6#", "六号")

# ⑦ 目录重建
m = re.search(r"^## 目录\n", t, re.M)
if m:
    body = t[m.end():]
    h2s = [l[3:].strip() for l in body.split("\n") if l.startswith("## ") and l[3:].strip() != "目录"]
    toc = "\n".join("%d. %s" % (i + 1, h) for i, h in enumerate(h2s))
    t = t[:m.end()] + toc + "\n\n" + body[len(toc) + 2:] if False else t
    # 精确重建
    j = body.find("\n\n", 0)
    # 找到目录后第一个非空块结束
    k = 0
    lines = body.split("\n")
    idx = 0
    for i, l in enumerate(lines):
        if l.strip() == "" and i > 0 and any(x.strip() for x in lines[:i]):
            idx = i; break
    rest = "\n".join(lines[idx + 1:])
    t = t[:m.end()] + toc + "\n\n" + rest
    L("TOC rebuilt:", len(h2s), "entries")

# ⑧ 文首文尾
i_head = t.find("**内部资料")
i_body = t.find("## 一、")
if i_head != -1 and i_body != -1:
    t = HEAD_FINAL + t[i_body:]
    L("[OK] 文首替换")
i_tail = t.find("## 附件说明")
if i_tail != -1:
    t = t[:i_tail] + TAIL_FINAL
    L("[OK] 文尾替换")

# ⑨ emoji 清除
EMO = "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\u24C2\u2B55]"
t = re.sub(EMO + "+", "", t)
t = re.sub(r"[ \t]+\n", "\n", t)
t = re.sub(r"\n{3,}", "\n\n", t)
t = t.replace("**——**", "——")
t = re.sub(r"\*\*[ \t]+", "**", t)
t = re.sub(r"[ \t]+\*\*", "**", t)
t = re.sub(r"\*\*[ \t]*\*\*", "", t)
t = t.replace("??", "").replace("??", "")
t = re.sub(r"\|\s*\|\s*\|", "| | |", t)

open(MD, "w", encoding="utf-8").write(t)
L("MD bytes:", len(t.encode("utf-8")), "emoji:", len(re.findall(EMO, t)))
bad = [l for l in t.split("\n") if l.startswith("#") and ("|" in l or "**" in l or len(l) > 95)]
L("heading issues:", len(bad))
for b in bad[:8]: L("  !", b.encode("unicode_escape").decode("ascii")[:110])
# 残留英文缩写扫描
for k in ("IRR", "NPV", "CAPEX", "ADR", "RevPAR", "HMA", "FF&E", "key money", "Agoda"):
    if k in t: L("[RESIDUAL-EN]", k, t.count(k))

sys.path.insert(0, r"D:\B166ER-openclaw\workspace\.tmp")
from md2docx_cn import convert
out = os.path.join(REP, "总府皇冠改造_立项报告_集团汇报件_v2.0_2026-11-13.docx")
convert(MD, out)
L("DOCX %.1f KB" % (os.path.getsize(out)/1024))

# 表格空白扫描
from docx import Document
d = Document(out)
n = 0
for ti, tb in enumerate(d.tables, 1):
    for ri, row in enumerate(tb.rows):
        for ci, cell in enumerate(row.cells):
            if cell.text.strip() in ("", "—", "-", "／", "/"):
                n += 1
                L("  BLANK 表%d 行%d 列%d : %s" % (ti, ri, ci, " || ".join(c.text.strip()[:22] for c in row.cells)))
L("表格 %d 个，空白格 %d" % (len(d.tables), n))
L("DONE")
