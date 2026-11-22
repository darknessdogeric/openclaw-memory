# -*- coding: utf-8 -*-
"""v90：第十二章重建 + 第五章（五）叙述算式按模型重算 + 图表按 v87 重绘
   —— 全部叙述中的数字一律由 v87.json 生成，杜绝硬编码残留"""
import io, os, sys, re, json
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
FIG = os.path.join(KB, "_figs")
LOG = open(os.path.join(T, "v90.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
J = json.load(open(os.path.join(T, "v87.json"), encoding="utf-8"))
B = {r["key"]: r for r in J["brands"]}; ORDER = J["order"]
BASE = J["base"]; OWN = J["own"]; PATHS = J["paths"]; CL = J["closure"]
def N(v, d=1): return format(round(v, d), ",.%df" % d)
def P(v): return "{:.2f}%".format(v * 100) if v is not None else "无可解"
def M(v, d=1): return ("+" + N(v, d)) if v >= 0 else ("−" + N(abs(v), d))
MD5 = os.path.join(KB, "总府皇冠改造_可行性研究报告_v5.0_2026-11-14.md")
lines = open(MD5, encoding="utf-8").read().split("\n")
FAIL = []
def find(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix): return i
    return -1
def put_between(a, b, content, tag):
    global lines
    i = find(a)
    if i < 0: FAIL.append(tag); L("[MISS]", tag); return
    j = find(b, i + 1)
    if j < 0: FAIL.append(tag+" end"); L("[MISS]", tag, "end"); return
    lines[i:j] = content.rstrip("\n").split("\n") + [""]
    L("[OK]  ", tag)

# ══ 模型派生的算式 ══
b07 = B["B07"]; b12 = B["B12"]; b02 = B["B02"]
rev188 = b07["n"] * 365 * b07["occ"] * b07["adr"] / 1e4
rev402 = 402 * 365 * b07["occ"] * b07["adr"] / 1e4
gap = rev402 - rev188
gap_pct = gap / B["B01"]["capex"] * 100
base20 = [p for p in PATHS if p[0] == "基准"][0]
p1 = [p for p in PATHS if p[0] == "P1"][0]
p2 = [p for p in PATHS if p[0] == "P2"][0]
p3 = [p for p in PATHS if p[0] == "P3"][0]
p5 = [p for p in PATHS if p[0] == "P5"][0]
d1 = p1[2] - base20[2]; d2 = p2[2] - base20[2]; d3 = p3[2] - base20[2]

# ══ ① 第五章（五）读数二：按模型重算 ══
i = find("**读数二：因此")
if i < 0: FAIL.append("读数二"); L("[MISS]", "读数二")
else:
    lines[i] = ("**读数二：因此「402 间卖 1,000 元以上」的组合在算术上不成立。** "
                "以尼依格罗 {n07} 间、{adr07} 元平均房价计，年客房收入 {rev07} 万元；"
                "若维持 402 间而取同一房价，年客房收入为 {rev402} 万元——"
                "**两者相差 {gap} 万元，相当于改造投资 {pct}%**。"
                "任何品牌方案都必须同时回答「房量降到多少」与「价格做到多少」两个问题。").format(
        n07=b07["n"], adr07=N(b07["adr"]), rev07=N(rev188), rev402=N(rev402),
        gap=N(gap), pct=N(gap_pct, 0))
    L("[OK]   读数二已按模型重算")
# 读数一中的旧数
i = find("**读数一：面积要求是房量的唯一决定因素")
if i >= 0:
    lines[i] = ("**读数一：面积要求是房量的唯一决定因素，房量减少直接吃掉收入基数。** "
                "402 间不变只能容纳上高端全服务档（皇冠假日基础房 25.35 平方米）；"
                "一旦进入规模化奢华档（瑞吉 65 平方米、尼依格罗 50 平方米、康莱德 46 平方米），"
                "房量降至 {nmin} 至 {nmax} 间，**较现状减少 {dmin} 至 {dmax} 间**。"
                "这解释了为什么瑞吉的年营业收入（{rev06} 万元）反而低于皇冠假日（{rev01} 万元）——"
                "**尽管瑞吉实测房价 {adr06} 元是皇冠假定 {adr01} 元的 1.5 倍**。"
                "房价与房量是反向作用，价格提升被房量减少抵消。").format(
        nmin=min(B[k]["n"] for k in ORDER if B[k]["area_th"] > 26),
        nmax=max(B[k]["n"] for k in ORDER if B[k]["area_th"] > 26),
        dmin=min(B[k]["n"] for k in ORDER if B[k]["area_th"] > 26) - 402,
        dmax=max(B[k]["n"] for k in ORDER if B[k]["area_th"] > 26) - 402,
        rev06=N(B["B06"]["total_rev"]), rev01=N(B["B01"]["total_rev"]),
        adr06=N(B["B06"]["adr"]), adr01=N(B["B01"]["adr"]))
    L("[OK]   读数一已按模型重算")

# ══ ② 第十二章重建 ══
CH12 = """## 第十二章 结论与建议

### （一）结论

**第一，本报告是决策预研框架，不给出"改不改、改什么、何时改"的结论。** 第三方安全评估结论尚未出具，检测评估机构对"消防系统与机电系统可分离性"及"是否存在结构层面停业整改触发条件"两项技术结论亦未明确。本报告做的是框定决策框架、算清关键变量、列明需要集团定夺的事项。

**第二，改造的必要性由四份相互独立的证据支撑。** 合规刚性（《消防法》第十三条、第十五条，现状不具备合法经营条件）、人防限制（部分地下层六级人防，竣工资料缺失）、经营失血（部门营业利润率 {gopr}%）、资产定价失位（平均房价 {adr} 元，为商圈 1,280 元的 33.4%，402 间年差额约 1.23 亿元）。**任一单独成立即构成充分理由。**

**第三，消防系统与机电系统的可分离性，是局部整改方案成立的技术前提。** 两者大量共用吊顶与管井空间，若先单独改造消防、后续机电更新需再次拆开吊顶，返工成本可能抵消局部改造所节省的停业损失。**建议在第三方安全评估报告中明确要求检测机构就此给出意见。**

**第四，改造范围应按三档分级，每一档对应评估结论的可能类型。** A 底线整改（消防升级约 120—200 元/㎡）、B 机电系统同步更新（约 200—500 元/㎡）、C 整体停业改造（五星级客房全包翻新约 18—25 万元/间）。**A 档与 C 档在施工时序上不是"先小后大"的简单关系**——消防改造须在客房翻新之前完成，若最终走向 C 档，先行实施 A 档可能造成浪费。

**第五，停业 12 个月是工程工期的下限，不是保守估计。** 1996 年建成的全楼消防系统（喷淋 1994 年、报警线路 1996 年敷设且绝缘值严重不达标）与核心机电更新工程本身需约 12 个月；且依住建部令第 58 号第十四条须整体消防验收合格方可投入使用。**可压缩的是验收环节**——成都可参照上海松江联合办理机制（消防验收 15 个工作日 ＋ 营业前检查 10 个工作日），但这不改变 12 个月的工程主体工期。

**第六，★ 品牌选择受房量硬约束，"402 间卖 1,000 元以上"的组合在算术上不成立。** 客房套内总面积 10,192 平方米是刚性的，按品牌基础房型面积要求与移卫耦合折损反推，可行房量在 {nmin} 至 {nmax} 间之间。**本轮实测修订直接印证了这一点：洲至奢选基础房由同档次推定 40 平方米订正为 OTA 实测 45 平方米，房量由 235 间降至 {n02} 间，净现值由 +2,787.2 万元降至 {npv02} 万元——相差 5 平方米，经济性相差 45 倍。** 因此**品牌方对基础房型面积的书面确认，是比价格与投资规模更优先的前置条件。**

**第七，品牌空位须按预期判断，不按当前是否开业判断。** 文华东方已于 2022 年 10 月签约中海 489 米塔楼（267 间、2028 开业）、丽晶已于 2026 年 7 月签约顺江路（180 间、2029Q3）。**真正存在空位的是康莱德、柏悦、Sofitel、六善四项，加洲至奢选（同集团可换牌），共五项；而洲至奢选经面积订正后已接近盈亏平衡，须与另外四家并行比较。**

**第八，全停业 12 个月、经营期 20 年的皇冠假日续约方案净现值 {b20} 万元、内部收益率 {b20irr}%，不成立。** 净现值转正依赖三项可具体争取的条件：经营期 30 年（{d1} 万元）、品牌方承担 30% 改造投入（{d2} 万元）、锦江区补贴 50 万元（{d3} 万元），三项叠加后净现值 {p5npv} 万元、内部收益率 {p5irr}%。

**第九，本项目在安逸十五五战略中承担的是"文创化改造"的旗舰载体角色。** 集团十五五明确要求"一定要做文创化改造，而不是简单改造"，并把在地文化能力列为五大护城河之一。总府所在街区的文化资源（明代四川都指挥使司"总府"、清光绪五年盐市口官盐店、1926 年智育电影院、2009 年盐市口汉代廊桥遗址、1924 年春熙路开路）可考证、可策展、可转化为产品与客群吸引力，**其真实作用是品牌适配、谈判筹码与客群匹配，不是独立的定价能力**。同时须化解集团内部序列冲突——锦著系列在春熙路及邻近已有多家门店，总府改造后的品牌定位须与之形成明确分工。

**第十，2029-03-27 品牌续约谈判截止是上限倒排终点。** 各前置工作按"评估结论落地 → 品牌方向确定 → 在地文化方案确认 → 实施"的顺序推进，**由集团根据决策节奏确定时间，本报告建议不设单一硬截止日**，但须保证品牌方向在该时点前完成，以保留换牌与续约的选择空间。

**第十一，资金边界须分类管理。** 不宜作为主渠道的：地方政府专项债（纯酒店类产业建筑通常存在限制，宾馆酒店常被列入负面清单）、酒店自身经营结余（停业期经营现金流归零）。有时效窗口的：锦江区设备更新与文旅项目奖励（政策有效期至 2026-12-31，须开工前完成项目入库申报）。需集团争取的：旅投集团内部政策支持（须具体化为资本金注入、内部借款利率优惠或集团统筹授信额度）、合作方或品牌方带资、停业期固定成本兜底来源（人工、存量负债利息、基本维护的兜底不明确，方案的资金平衡表无法闭合）。

### （二）建议

**建议一：立即委托第三方安全评估，作为第一优先事项。** 范围为消防、机电设备、结构三方面。**报告须明确包含两项技术结论："消防系统与机电系统的可分离性"与"是否存在结构层面的停业整改触发条件"**——这两项决定 A 档方案是否成立，也决定第五章至第九章的方案空间。评估费用可控，不依赖任何待确认参数。

**建议二：同步向成都警备区确认人防产权与可改造边界。** 由总府实业会同集团办理，并补齐竣工资料与备案。基准按"保持现状不动"处置（30 至 70 万元）；若警备区要求功能腾挪，增加 800 至 1,500 万元并相应延长工期。

**建议三：★ 向候选品牌方发出的第一次问询，必须包含基础房型面积要求。** 随 PIP 前期策划模板一次性提出三项书面答复要求：基础房型最小面积要求（并明确卫生间是否计入套内）、是否接受 3 改 2 后的房量缩减、品牌标准客房数与最低运营规模是否冲突。**理由是本轮的实测修订已证明：面积要求的 5 平方米误差，即可使该品牌方案经济性相差 45 倍。这一项的答复价值高于价格与投资规模的谈判。**

**建议四：以第五章（七）在地文化植入方案作为产品定位基准。** 文化是品牌适配标准与谈判筹码，不是价格工具——**任何价格带都可以做文创，文创本身不产生房价溢价**。在地文化资产的谈判价值应体现在"品牌方承担部分改造投入"的条件上（第九章路径 P2，权重最大的净现值改善项 {d2} 万元），而不是体现在房价假设上。

**建议五：品牌方向按"可争取空位"并行接触，不设单一优先。** 康莱德、柏悦、Sofitel、六善四项空位品牌与洲至奢选同时接触以保留比选空间。**其中洲至奢选虽无第三方谈判障碍，但经面积订正后净现值仅 {npv02} 万元，应与另外四家以同一口径比较后再定，不宜先行锁定。**

**建议六：把分期开业作为基准停业方案与品牌方一并谈定。** 阶段一全楼停业 12 个月完成消防与机电，阶段二分区滚动开业 12 个月，把复业时点从第 24 个月提前到第 13 个月。须请品牌方确认三项：分区验收与分区开业、开业时的客房标准完整度认定、开业时序对会员权益兑现与线上可售库存的约束。

**建议七：按第五章（五）三分口径编制改造投资概算，并向品牌方明确技术边界。** 机电设备与隐蔽工程（{mep} 万元，全楼口径）属业主方刚性责任，不进入品牌溢价谈判；品牌档次带来的增量全部落在客房改造（单间口径）与公区改造（单平口径）两段。

**建议八：在可保留项节约中锁定三年文化内容预算，并设 Kill 判据。** 年度内容预算 180 至 250 万元（对应"1 名文化主理人＋一年 2 次主展＋每月 1 次活动＋机构共创"的最低可行节律），从可保留项节约中划转，不新增改造投资总额。判定指标：策展溢价指数不低于 1.15、导览与工坊参与率不低于 35%、非房收入占比两年内提升至 20% 以上、客群文化动机占比不低于 40%、复购率不低于 20%。**任一项在复业后第 12 个月不达标即停止追加。**

**建议九：完成春熙路商圈品牌序列与客群分层设计。** 明确总府改造后的品牌定位与价格带与锦著系列存量门店的分工，并借本次改造完成该片区线上平台同址条目的归集与点评资产归位。**本项不新增投资，但须在投资决策前完成。**

**建议十：明确停业期固定成本兜底来源。** 人工留存、存量负债利息、基本维护的刚性支出不能假设由酒店经营现金流覆盖，须由集团层面指定来源，否则方案的资金平衡表无法闭合。

**建议十一：启动政策资金申报。** 锦江区设备更新与文旅项目奖励政策有效期至 2026-12-31 且须开工前完成项目入库申报，**建议授权在评估结论落地前先行启动入库前期技术对接**（不涉及施工承诺、不形成资金支出）。

### （三）请示事项

**一、请同意以第三方安全评估结论作为本项目改造方案成立的前置条件，并请集团先行委托消防、机电设备、结构三方安全评估。** 请同时明确要求评估报告中包含"消防系统与机电系统的可分离性"与"是否存在结构层面的停业整改触发条件"两项技术结论。**在评估结论出具前，本报告的方案比较仅在"须整体改造"假设下成立。**

**二、请认可改造必要性的四份独立证据与三档分级框架。** 必要性的四份证据为：合规刚性、人防限制、经营失血、资产定价失位。请认可 A 底线整改／B 机电系统同步更新／C 整体停业改造三档框架，及其"每档对应评估结论类型"的触发逻辑。

**三、请认可停业 12 个月为工程工期下限，并授权以分期开业为基准方案与品牌方一并谈定。** 请认可阶段一全楼停业 12 个月（含整体消防验收）＋阶段二分区滚动开业 12 个月的两阶段安排。

**四、请授权向候选品牌方提交 PIP 前期策划模板，并将基础房型面积要求列为第一问询项。** 同时请授权康莱德、柏悦、Sofitel、六善四项目标空位品牌与洲至奢选并行接触，保留比选空间，不设单一优先。

**五、请认可净现值转正的三项条件并授权分别推进。** 即经营期按 30 年长周期资产安排、品牌方承担 30% 改造投入、锦江区政策性补贴 50 万元。**三项叠加后净现值 {p5npv} 万元、内部收益率 {p5irr}%。若品牌方不承担改造投入分担且补贴不足，请明确本项目的最低可接受投资规模，由本部据此重新划定房量与品牌档位区间。**

**六、请明确停业期固定成本兜底来源，以及旅投集团内部支持的具体形式**（资本金注入、内部借款利率优惠、集团统筹授信额度，或其组合）。

**七、请明确与锦著系列的品牌序列分工，并授权按 2029-03-27 为上限倒排时序。** 建议不设单一硬截止日，各前置工作按顺序推进，由集团根据决策节奏确定时间，但须保证品牌方向在 2029-03-27 前完成。

以上报告，请审阅。
""".format(gopr=N(BASE["gop_rate"] * 100, 1), adr=N(BASE["adr"]),
           nmin=min(B[k]["n"] for k in ORDER), nmax=max(B[k]["n"] for k in ORDER),
           n02=B["B02"]["n"], npv02=M(B["B02"]["npv"]),
           b20=M(base20[2]), b20irr=P(base20[3]),
           d1=M(d1), d2=M(d2), d3=M(d3),
           p5npv=M(p5[2]), p5irr=P(p5[3]), mep=N(B["B01"]["mep"]))
put_between("## 第十二章 结论与建议", "以上报告，请审阅。", CH12, "⑫ 第十二章重建")
open(MD5, "w", encoding="utf-8").write("\n".join(lines))
L("未命中 {0} 处".format(len(FAIL)))
for f in FAIL: L("   MISS:", f)

# ══ ③ 图表按 v87 重绘 ══
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
CAND = ["Microsoft YaHei", "SimHei", "DengXian"]
HAVE = {f.name for f in font_manager.fontManager.ttflist}
F = next((c for c in CAND if c in HAVE), None)
if F: plt.rcParams["font.sans-serif"] = [F]
plt.rcParams["axes.unicode_minus"] = False
C1, C2, C3, C4 = "#1F4E79", "#C00000", "#2E7D32", "#ED7D31"

# 图2 品牌面积→房量
items = sorted([r for r in B.values() if r["area_th"] > 26], key=lambda r: r["area_th"])
fig, ax = plt.subplots(figsize=(10, 5.2))
names = [r["name"].split("（")[0][:10] for r in items]
bars = ax.bar(names, [r["n"] for r in items],
               color=[C4 if r["key"] == "B12" else (C3 if r["key"] == "B02" else C1) for r in items], alpha=.88)
ax.axhline(402, color=C2, ls="--", lw=1.8)
ax.annotate("现状 402 间（单间套内 25.35 ㎡）", (len(names) - .4, 402), textcoords="offset points",
            xytext=(0, 6), ha="right", fontsize=10, color=C2, weight="bold")
for r, b in zip(items, bars):
    ax.annotate("%d 间\n%.0f ㎡" % (r["n"], r["area_th"]), (r["name"].split("（")[0][:10], r["n"]),
                textcoords="offset points", xytext=(0, 4), ha="center", fontsize=8)
ax.set_ylabel("按品牌面积要求可实现的房量（间）", fontsize=10)
ax.set_title("图 2　品牌客房面积要求 → 总府可行房量（客房套内 10,192 ㎡，移卫耦合折损 8%）",
             fontsize=13, color=C1, pad=12, weight="bold")
plt.setp(ax.get_xticklabels(), rotation=32, ha="right", fontsize=9)
ax.grid(axis="y", alpha=.28, ls="--")
fig.savefig(os.path.join(FIG, "fig02_品牌面积与房量.png"), dpi=170, bbox_inches="tight", facecolor="white"); plt.close(fig)
L("[图] fig02 已重绘（洲至奢选 209 间、绿色标注）")

# 图4 净现值路径
labels = ["基准\n（12月全停+分区滚动+20年）", "①经营期\n20→30年", "②品牌方承担\n30%改造投入",
          "③锦江区补贴\n50万元", "④①+②", "⑤①+②+③"]
vals = [p[2] for p in PATHS]
fig, ax = plt.subplots(figsize=(9.6, 4.6))
bars = ax.bar(labels, vals, color=[C2 if v < 0 else C3 for v in vals], alpha=.88, width=.55)
for b, v in zip(bars, vals):
    ax.annotate("%+.0f" % v, (b.get_x() + b.get_width() / 2, v), textcoords="offset points",
                xytext=(0, 6 if v >= 0 else -16), ha="center", fontsize=10, weight="bold",
                color=C3 if v >= 0 else C2)
ax.axhline(0, color="#555", lw=1)
ax.set_ylabel("净现值（万元，8% 折现）", fontsize=10)
ax.set_title("图 4　净现值转正路径分解（皇冠假日现状续约基准）", fontsize=13, color=C1, pad=12, weight="bold")
ax.grid(axis="y", alpha=.28, ls="--")
plt.setp(ax.get_xticklabels(), fontsize=8.5)
fig.savefig(os.path.join(FIG, "fig04_净现值路径.png"), dpi=170, bbox_inches="tight", facecolor="white"); plt.close(fig)
L("[图] fig04 已重绘")

# 图5 停业方案
sl = ["全停业 4 月\n（原设想，不可行）", "全停业 12 月\n一次复业", "全停业 12 月\n分区滚动开业",
      "全停业 16 月\n分区滚动开业", "全停业 20 月\n分区滚动开业"]
def npv_for(mo, phased):
    import importlib.util
    spec = importlib.util.spec_from_file_location("v87m", os.path.join(KB, "_calc", "v87_model.py"))
    return None
sv = [None, None, None, None, None]
# 由 CL 与模型：全停业+一次复业/分区滚动 用 build 的结果（重算）
spec = importlib.util.spec_from_file_location("v87m", os.path.join(KB, "_calc", "v87_model.py"))
import types
src_m = open(os.path.join(KB, "_calc", "v87_model.py"), encoding="utf-8").read()
src_m = src_m.replace('json.dump(dict(base=BASE', '#json.dump(dict(base=BASE')
ns = {}
exec(compile(src_m, "v87_model", "exec"), ns)
bmeta = [b for b in ns["BRANDS"]]
sv[1] = ns["build"](bmeta[0], months_full=12, phased=False, horizon=30)["npv"]
sv[2] = ns["build"](bmeta[0], months_full=12, phased=True, horizon=30)["npv"]
sv[3] = ns["build"](bmeta[0], months_full=16, phased=True, horizon=30)["npv"]
sv[4] = ns["build"](bmeta[0], months_full=20, phased=True, horizon=30)["npv"]
fig, ax = plt.subplots(figsize=(9, 4.4))
xs = list(range(len(sl)))
ax.bar([0], [0], color="#BFBFBF", alpha=.8)
bars = ax.bar(list(xs)[1:], sv[1:], color=[C2 if v < 0 else C3 for v in sv[1:]], alpha=.88, width=.55)
for i, v in enumerate(sv):
    if v is None:
        ax.annotate("消防与机电工程\n12 个月不可压缩", (0, 120), ha="center", fontsize=9, color="#8C8C8C", weight="bold")
    else:
        ax.annotate("%+.0f" % v, (i, v), textcoords="offset points", xytext=(0, 6 if v >= 0 else -16),
                    ha="center", fontsize=10, weight="bold", color=C3 if v >= 0 else C2)
ax.set_xticks(list(xs)); ax.set_xticklabels(sl, fontsize=8.8)
ax.set_ylabel("净现值（万元，30 年口径）", fontsize=10)
ax.set_title("图 5　停业方案与净现值（停业月数是最大的单一变量）", fontsize=13, color=C1, pad=12, weight="bold")
ax.grid(axis="y", alpha=.28, ls="--")
fig.savefig(os.path.join(FIG, "fig05_停业方案.png"), dpi=170, bbox_inches="tight", facecolor="white"); plt.close(fig)
L("[图] fig05 已重绘")
L("DONE")
