# -*- coding: utf-8 -*-
"""v92：v5.0 最终收口
   ① 第一章（四）总体结论重写（消除陈旧数 + 压冗余）
   ② 读数一区间表述修正
   ③ 三分口径合计行填实
   ④ 路径表「性质」列 em-dash 占位改实义（公文转换器将「—」判为空格）
   ⑤ 全表 em-dash 占位兜底替换
   ⑥ 补 DeepSeek「局部改造隐性成本」：OTA 评分冲击、改了一半僵局、顺序倒置返工
   ⑦ 第九章读数一~四压缩，详析留在第五章（五）（消重）
   ⑧ 重新插图 2 / 图 4
   ⑨ Word 重建 + 终检 + 审计 + memory/README"""
import io, os, sys, re, json, glob, subprocess
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v92.log"), "w", encoding="utf-8")
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

base20 = PATHS[0][2]; p5 = PATHS[-1][2]
own_rank = 1 + sum(1 for k in ORDER if B[k]["npv"] > OWN["npv"])
# ① 第一章（四）重写（压冗余：不再复述十二品牌全表，财务结论指向第九章）
CH14 = """### （四）总体结论

**第一，改造的必要性由四份相互独立的证据支撑。** 合规刚性（《消防法》第十三条、第十五条，现状不具备合法经营条件）、人防限制（部分地下层六级人防，竣工资料缺失）、经营失血（部门营业利润率 {gopr}%）、资产定价失位（平均房价 {adr} 元，为商圈 1,280 元的 33.4%，402 间年差额约 1.23 亿元）。四者互相独立，任一成立即构成改造理由。

**第二，★ 品牌选择受房量硬约束，且品牌客房面积要求是比价格更优先的前置条件。** 客房套内总面积 10,192 平方米是刚性的；按各品牌基础房型面积要求反推，可行房量在 {nmin} 至 {nmax} 间之间。**"402 间卖 1,000 元以上"的组合在算术上不成立**——本轮实测修订已印证：洲至奢选基础房由推定 40 平方米订正为实测 45 平方米，房量即由 235 间降至 209 间，净现值相差 45 倍。因此**第一次与品牌方接触即应取得基础房型面积要求的书面答复**。

**第三，品牌档次应与单房投资相匹配。** 基准方案单房投资 {pk01} 万元，按《高星级全服式酒店品牌分级分类》§6.1 落在高端奢华档对应区间，而现行皇冠假日属上高端全服务档。**投资规模与品牌档位之间存在明显错配**：以同等投资承接上高端品牌是能力用不足，承接高端奢华品牌则须放弃现有客源结构与会员体系承接方。

**第四，净现值转正依赖三项可争取的条件，而非理想化假设。** 基准情形（12 个月全停 ＋ 分区滚动、20 年经营期、皇冠续约）净现值 {b20} 万元、内部收益率 {b20irr}%，不成立；延长经营期至 30 年、品牌方承担 30% 改造投入、锦江区补贴 50 万元三项叠加后，净现值 {p5} 万元、内部收益率 {p5irr}%。**其中品牌方分担权重最大。**

**第五，文化价值挖掘与品牌遴选互为条件，而非独立的溢价来源。** 总府街所在街区的历史资源（明代四川都指挥使司"总府"、清光绪五年盐市口官盐店、1926 年智育电影院、2009 年盐市口汉代廊桥遗址、1924 年春熙路开路）构成明确的在地叙事，但**任何价格带都可以做文创，文化本身不产生房价溢价**。其真实作用是与候选品牌标准的契合度、与品牌方谈判时的价值筹码、以及对目标客群的匹配程度。

**第六，集团自有高端品牌路径在模型上优于皇冠续约，位列十二候选品牌中的第 {orank} 位。** 自有品牌路径净现值 {own} 万元、内部收益率 {ownirr}；但该路径缺少全球分销与会员体系，价格认知须从零建立，落地周期长于改造周期。**列为须专项论证的战略备选，不作为推荐方案**，理由详见第五章（八）。

**第七，本报告是决策预研框架，不给出"改不改、改什么、何时改"的结论。** 第三方安全评估结论尚未出具，检测机构对"消防系统与机电系统可分离性"及"是否存在结构层面停业整改触发条件"两项技术结论亦未明确。第五章至第九章的方案比较，均在"须整体改造"假设下成立；第十二章列出需集团定夺的七项事项。

""".format(gopr=N(BASE["gop_rate"]*100,1), adr=N(BASE["adr"]),
           nmin=min(B[k]["n"] for k in ORDER), nmax=max(B[k]["n"] for k in ORDER),
           pk01=N(B["B01"]["per_key_total"],2), b20=M(base20), b20irr=P(PATHS[0][3]),
           p5=M(p5), p5irr=P(PATHS[-1][3]), own=M(OWN["npv"]), ownirr=P(OWN["irr"]), orank=own_rank)
put_between("### （四）总体结论", "## 第二章", CH14, "① 第一章（四）重写")

# ② 读数一区间表述
i = find("**读数一：面积要求是房量的唯一决定因素")
if i >= 0:
    lines[i] = ("**读数一：面积要求是房量的唯一决定因素，房量减少直接吃掉收入基数。** "
                "402 间不变只能容纳上高端全服务档（皇冠假日基础房 25.35 平方米）；"
                "一旦进入规模化奢华及以上档（瑞吉 65 平方米、尼依格罗 50 平方米、康莱德 46 平方米），"
                "房量降至 {nmin} 至 {nmax} 间，**较现状减少 {dmin} 至 {dmax} 间**。"
                "这解释了为什么瑞吉的年营业收入（{rev06} 万元）反而低于皇冠假日（{rev01} 万元）——"
                "**尽管瑞吉实测房价 {adr06} 元是皇冠假定 {adr01} 元的 1.5 倍**。"
                "房价与房量是反向作用，价格提升被房量减少抵消。").format(
        nmin=min(B[k]["n"] for k in ORDER if B[k]["area_th"] > 26),
        nmax=max(B[k]["n"] for k in ORDER if B[k]["area_th"] > 26),
        dmin=402-max(B[k]["n"] for k in ORDER if B[k]["area_th"] > 26),
        dmax=402-min(B[k]["n"] for k in ORDER if B[k]["area_th"] > 26),
        rev06=N(B["B06"]["total_rev"]), rev01=N(B["B01"]["total_rev"]),
        adr06=N(B["B06"]["adr"]), adr01=N(B["B01"]["adr"]))
    L("[OK]   ② 读数一区间表述修正")

# ③ 三分口径合计行填实
i = find("| **合计** | | | | **21,448.5 万元** |")
if i >= 0:
    lines[i] = "| **合计** | 机电设备与隐蔽工程 ＋ 客房改造 ＋ 公区改造 ＋ 其他 | 三口径合并 | 品牌增量仅落在客房与公区两段 | **21,448.5 万元** |"
    L("[OK]   ③ 三分口径合计行填实")
else:
    FAIL.append("③ 合计行"); L("[MISS]", "③ 合计行")

# ④⑤ 表格 em-dash 占位兜底（公文转换器将「—」判为空格）
n_dash = 0
in_tbl = False
for i, l in enumerate(lines):
    if l.startswith("|"):
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        new = []
        for c in cells:
            if c in ("—", "-", ""):
                new.append("不适用"); n_dash += 1
            else:
                new.append(c)
        lines[i] = "| " + " | ".join(new) + " |"
L("[MD] 表格 em-dash 占位替换:", n_dash)

# ④b 路径表性质列改实义
for i, l in enumerate(lines):
    if l.startswith("| 基准 | 12 月全停"):
        lines[i] = "| 基准 | 12 月全停 ＋ 分区滚动 ＋ 20 年 | " + M(base20) + " | 不适用 | " + P(PATHS[0][3]) + " | 本报告基准情形 |"
    elif l.startswith("| P4 | P1＋P2"):
        lines[i] = "| P4 | P1＋P2 | " + M(PATHS[4][2]) + " | " + M(PATHS[4][2]-base20) + " | " + P(PATHS[4][3]) + " | P1 与 P2 叠加 |"
    elif l.startswith("| P5 | P1＋P2＋P3"):
        lines[i] = "| P5 | P1＋P2＋P3 | " + M(PATHS[5][2]) + " | " + M(PATHS[5][2]-base20) + " | " + P(PATHS[5][3]) + " | 三项叠加 |"

# ⑥ DeepSeek：局部改造隐性成本
i = find("### （四）停业方案")
if i >= 0:
    j = i + 1
    while j < len(lines) and not lines[j].startswith("### "):
        j += 1
    ADD = """
#### 4. 局部改造（A 档）的隐性成本必须一并计入比选

在评估结论指向"可局部整改"时，A 档与 C 档的比较不能只比造价，还须计入四项隐性成本，否则会低估 A 档或高估 C 档：

**其一，线上点评与评分的冲击及恢复周期。** 停业或施工期间线上评分与点评量下降，复业后排序与转化率需要时间恢复，恢复期长短随改造范围与停业时长变化。

**其二，"改了一半"的僵局风险。** 局部改造完成后设施水平提升但产品未整体升级，资产既未达到五星标准、又已消耗一次性改造投入与停业成本，二次改造的沉没成本最高。

**其三，★ 施工顺序倒置的返工成本。** 消防管网与机电管线大量共用吊顶与管井空间。**若先单独实施消防改造、后续实施机电更新需再次拆开吊顶，返工成本可能抵消局部改造所节省的停业损失**；同时消防改造须在客房翻新之前完成（喷淋管道与烟感线路须走吊顶内），这使 A 档与 C 档在时序上不是"先小后大"的简单关系。**若最终走向 C 档，先行实施 A 档将造成浪费。**

**其四，两项专项合规的前置性。** 消防验收（住建部令第 58 号第十四条）与公众聚集场所投入使用、营业前消防安全检查（《消防法》第十五条）为复业的法定前提，两者均须整体合格，不存在"局部先行通过"的空间。成都可参照上海松江联合办理机制压缩的是验收环节的行政时间，不是工程工期。

**结论：A 档与 C 档的比较必须以"全生命周期总代价"口径进行，且在消防与机电可分离性未获明确意见前，不得预先锁定 A 档。**

"""
    lines[j:j] = ADD.strip("\n").split("\n") + [""]
    L("[OK]   ⑥ DeepSeek 局部改造隐性成本已补")

# ⑦ 第九章读数一~四压缩（消重：详析留第五章（五））
i = find("**其一，收入规模与房量强相关，与品牌档次弱相关。**")
if i >= 0:
    j = find("### （三）净现值为正的可行路径", i)
    NEW = ("**其一，收入规模与房量强相关，与品牌档次弱相关。** 瑞吉实测房价 {a6} 元、尼依格罗 {a7} 元均高于皇冠假定的 {a1} 元，但因面积门槛分别压至 {n6} 间与 {n7} 间，年营业收入反而低于皇冠的 {r1} 万元。**结论不是\"哪个品牌最贵\"，而是\"哪个组合在算术上成立\"。**\n\n"
           "**其二，前提最弱者净现值最高。** LXR 净现值 {npv12} 万元居首，但其前提是总府路 28 号项目（2023-03 单方官宣、3 年无落地、希尔顿从未官方确认），**在前提核实前该排序不具决策意义**。\n\n"
           "**其三，★ 本轮实测修订后降幅最大的品牌是洲至奢选。** 基础房面积由同档次推定 40 平方米订正为 OTA 实测 45 平方米（标准房 45／尊贵房 52／行政层 54 至 58／套房 106），房量由 235 间降至 {n02} 间，净现值由 +2,787.2 万元降至 {npv02} 万元。**同一品牌在相差 5 平方米的要求下，经济性相差 45 倍——品牌方对基础房型面积的书面确认，是比价格与投资规模更优先的前置条件。**\n\n"
           "**其四，真正可争取的是五项。** 康莱德（{npv03} 万）、柏悦（{npv08} 万）、Sofitel（{npv05} 万）、六善（{npv10} 万）四项空位品牌，加洲至奢选（同集团可换牌，{npv02} 万）；**其中洲至奢选经面积订正后已接近盈亏平衡，须与另外四家并行比较。**\n\n").format(
        a6=N(B["B06"]["adr"]), a7=N(B["B07"]["adr"]), a1=N(B["B01"]["adr"]),
        n6=B["B06"]["n"], n7=B["B07"]["n"], r1=N(B["B01"]["total_rev"]),
        npv12=M(B["B12"]["npv"]), n02=B["B02"]["n"], npv02=M(B["B02"]["npv"]),
        npv03=M(B["B03"]["npv"]), npv08=M(B["B08"]["npv"]), npv05=M(B["B05"]["npv"]), npv10=M(B["B10"]["npv"]))
    lines[i:j] = NEW.strip("\n").split("\n") + [""]
    L("[OK]   ⑦ 第九章读数压缩（消重）")

# ⑧ 重新插图 2 / 图 4
def insert_fig(after_prefix, fname, cap, tag):
    global lines
    i = find(after_prefix)
    if i < 0: FAIL.append(tag); L("[MISS]", tag); return
    j = i + 1
    while j < len(lines) and not lines[j].startswith("### ") and not lines[j].startswith("## "):
        j += 1
    lines[j:j] = ["![{c}](_figs/{f})".format(c=cap, f=fname), ""]
    L("[OK]  ", tag)
insert_fig("### （五）品牌方案比选", "fig02_品牌面积与房量.png", "图 2　品牌客房面积要求 → 总府可行房量（客房套内 10,192 ㎡，移卫耦合折损 8%）", "⑧ 插图2")
insert_fig("### （三）净现值为正的可行路径", "fig04_净现值路径.png", "图 4　净现值转正路径分解（皇冠假日现状续约基准）", "⑧ 插图4")

open(MD5, "w", encoding="utf-8").write("\n".join(lines))
L("")
L("未命中 {0} 处".format(len(FAIL)))
for f in FAIL: L("   MISS:", f)
L("DONE")
