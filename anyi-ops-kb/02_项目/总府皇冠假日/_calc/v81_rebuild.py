# -*- coding: utf-8 -*-
"""v81：直接重建 v5.0 完整 MD（从 v4.0 出发，按序应用全部补丁，不再做增量覆盖）
   顺序：v5.0 基线（v4.0）→ ①轻改对标 ②取消Q4节点 ⑦保留部分基材 ⑤OTA数据 ⑨空位口径
        → 第五章（四）停业方案 /（五）品牌比选 → 第六章（一）三分口径 → 第九章整章 → 第十二章整章
        → 第一章（零）定位 → 第十章（三）补充 → 插图 → 空白格填实 → emoji 清除"""
import io, os, sys, re, json
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
FR = os.path.join(KB, "_calc", "_frag")
LOG = open(os.path.join(T, "v81.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
sys.path.insert(0, os.path.join(KB, "_calc"))
J = json.load(open(os.path.join(T, "v70.json"), encoding="utf-8"))
BR = {r["key"]: r for r in J["brands"]}; ORD = J["order"]
def N(v, d=1): return format(round(v, d), ",.%df" % d)
def P(v): return "{:.2f}%".format(v * 100) if v is not None else "无可解"

MD4 = os.path.join(KB, "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.md")
MD5 = os.path.join(KB, "总府皇冠改造_可行性研究报告_v5.0_2026-11-14.md")
lines = open(MD4, encoding="utf-8").read().split("\n")
FAIL = []
def find(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix):
            return i
    return -1
def find_exact(target, start=0):
    for i in range(start, len(lines)):
        if lines[i] == target:
            return i
    return -1
def setline(i, new, tag):
    if i < 0:
        FAIL.append(tag); L("[MISS]", tag); return
    lines[i] = new; L("[OK]  ", tag)
def put_between(a, b, content, tag):
    global lines
    i = find(a)
    if i < 0:
        FAIL.append(tag); L("[MISS]", tag); return
    j = find(b, i + 1)
    if j < 0:
        FAIL.append(tag + " end"); L("[MISS]", tag, "end"); return
    lines[i:j] = content.rstrip("\n").split("\n") + [""]
    L("[OK]  ", tag)
def read_frag(name, tokens):
    s = open(os.path.join(FR, name), encoding="utf-8").read()
    for k in tokens:
        s = s.replace("{{" + k + "}}", tokens[k])
    if "{{" in s:
        FAIL.append(name + " 占位符")
        L("[MISS]", name, "占位符残留")
    return s

# ── 表格行 ──
brand_rows = []
for k in ORD:
    r = BR[k]
    pc = "{:.0f}".format(r["adr"]) if str(r["price_src"]).startswith("OTA") else "推定"
    brand_rows.append("| {k} | {nm} | {tr} | {ar:.0f} | {n} | {d} | {pc} | {rev} | {nr} | {cx} | {pk} | {npv} | {irr} | {vac} |".format(
        k=k, nm=r["name"], tr=r["tier_cn"], ar=r["area_th"], n=r["n"], d=r["n"] - 402, pc=pc,
        rev=N(r["total_rev"]), nr=N(r["seg"]["fnb"] + r["seg"]["banq"] + r["seg"]["misc"]),
        cx=N(r["capex"]), pk=N(r["per_key_total"], 2), npv=N(r["npv"]), irr=P(r["irr"]), vac=r["vacancy"]))
order_rows = []
for i, k in enumerate(ORD):
    r = BR[k]
    order_rows.append("| {i} | {nm} | {npv} | {irr} | {inc} | {vac} |".format(
        i=i + 1, nm=r["name"], npv=N(r["npv"]), irr=P(r["irr"]), inc=N(r["inc_npv"]), vac=r["vacancy"]))
cost_rows = []
for k in ORD:
    r = BR[k]
    cost_rows.append("| {nm} | {n} | {mep} | {rc} | {rk} | {pc} | {ps} | {ot} | {tot} |".format(
        nm=r["name"], n=r["n"], mep=N(r["mep"]), rc=N(r["room_cost_total"]),
        rk=N(r["room_cost_per_key"], 2), pc=N(r["pub_cost"]),
        ps="{:,.0f}".format(r["pub_per_sqm"] * 10000), ot=N(r["other"]), tot=N(r["capex"])))

# ══ ① 轻改对标 ══
i = find("**其四，改造的单间造价须对标行业价格带。**")
setline(i, """**其四，改造单间造价的比较基准是品牌档次，不是行业轻改造价格。** 本项目是 1996 年建成的在营酒店的**整体改造**，不是轻改——轻改（保留主体、局部翻新）在本物业不可行：消防自动报警主机已全面瘫痪、喷淋系统 1994 年投运、报警线路 1996 年敷设且绝缘值严重不达标、空调主机 1996 年 4 台离心机已运行 30 年，**机电与消防均为整体更换而非局部翻新**。因此比较基准采用《高星级全服式酒店品牌分级分类（仅 5★+）》的**品牌档次单房改造造价带**与本项目实配双基准：

| 档次 | 内部表单房改造带（万元/间） | 本项目对应客房单间 | 位置 |
|---|---|---|---|
| 上高端全服务（皇冠假日、康莱德、费尔蒙） | 20—30 | 14.92 万元 | 带内下沿（保留部分基材所致） |
| 规模化奢华（瑞吉、尼依格罗、柏悦） | 28.8—57.6 | 22.4—38.2 万元 | 带内 |
| 高端奢华（六善、文华东方、丽晶） | 36—50 | 26.0—44.8 万元 | 带内 |
| 超奢华（LXR） | 43—72 | 41.2 万元 | 带内 |

**按品牌档次对标后，本项目各档次的客房单间造价均落在内部表对应档次带之内；唯一越界情形是外部顶奢情景的客房单间 100.32 万元，超超奢华带上限 72 万元每间约 39%——该路径的问题不在房价，而在单房造价失控。**""", "① 轻改对标")

# ══ ② 取消 2026Q4 硬节点 ══
i = find("| R-13 |")
setline(i, "| R-13 | 2029 年品牌窗口错失，改造决策权让渡 | 中 | 高 | 高 | 以 2029-03-27 续约谈判截止为**上限倒排终点**；各前置工作按「评估结论落地→品牌方向确定→文化方案确认→实施」的顺序推进，不设单一硬截止日 |", "②a R-13")
i = find("**四、请明确与锦著系列的品牌序列分工")
setline(i, """**四、请明确与锦著系列的品牌序列分工，并授权按品牌窗口倒排时序。** 请明确总府改造后的品牌定位与价格带与锦著系列存量门店的分工关系；请同意以 2029-03-27 品牌续约谈判截止为**上限倒排终点**，并按「第三方安全评估结论落地 → 品牌方向确定 → 在地文化方案确认 → 实施」的顺序推进各前置工作。**各前置工作的时间由集团根据决策节奏确定，本报告建议不设单一硬截止日，但须保证品牌方向在 2029-03-27 前完成，以保留换牌与续约的选择空间；若评估结论或品牌方向在该时点仍未明确，建议整体决策时点后移并同步重新评估品牌合约处置方案。**""", "②b 请示四")

# ══ ⑦ 保留石材 → 保留部分基材 ══
n_stone = 0
for i, l in enumerate(lines):
    if "保留石材" in l:
        lines[i] = l.replace("保留石材", "保留部分基材"); n_stone += 1
L("[OK]   ⑦ 保留石材→保留部分基材：{0} 行".format(n_stone))
i = find("| R-17 |")
setline(i, "| R-17 | 保留部分基材（石材、木作、吊顶基面）检测不合格 | 中 | 中 | 中 | 改造前完成逐处检测，检测不合格部位局部剔除重做，费用另计 |", "⑦ R-17")

# ══ ⑤ OTA 数据 ══
OTA = [
 ("| 成都尼依格罗 | 九龙仓 | IFS 3 号楼 | 238 间 | 1,191—2,800 元 | 约 40 间 |",
  "| 成都尼依格罗 | 九龙仓 | IFS 3 号楼 | **230 间** | **1,180—1,400 元**（基础房 50 ㎡） | 约 40 间 |"),
 ("| 成都瑞吉 | 万豪 | 太升南路 | 312 间 | 980—2,500 元 | 约 60 间 |",
  "| 成都瑞吉 | 万豪 | 太升南路 | **282 间** | **1,291—1,393 元**（基础房 65 ㎡） | 约 60 间 |"),
 ("| 成都尼依格罗 | 九龙仓 | IFS 3 号楼 | 238 间 | 1,191—2,800 | 已实测 |",
  "| 成都尼依格罗 | 九龙仓 | IFS 3 号楼 | **230 间** | **1,180—1,400**（基础房 50 ㎡） | 已实测 |"),
 ("| 成都瑞吉 | 万豪 | 太升南路 | 312 间 | 980—2,500 | 已实测 |",
  "| 成都瑞吉 | 万豪 | 太升南路 | **282 间** | **1,291—1,393**（基础房 65 ㎡） | 已实测 |"),
 ("| 成都高新丽笙精选 | 锦江丽笙 | 高新区 | 178 间 | 未公开披露 | 不适用 |",
  "| 成都高新丽笙精选 | 锦江丽笙 | 高新区 | 178 间 | 未公开披露（2026-06-16 开业，无稳定成交记录） | 不适用 |"),
 ("| 成都 OAKS（蜀都） | 独立 | 不适用 | 未公开披露 | 已实测（评分 9.6） |",
  "| 成都 OAKS（蜀都） | 独立 | 不适用 | 约 350 欧元起 | 已实测（评分 9.6，507 条点评） |"),
 ("| 成都丽晶 | IHG | 锦江顺江路 | 180 间 | 未公开披露 | 约 180 间 |",
  "| 成都丽晶 | IHG | 锦江顺江路 | 180 间 | 未公开披露 | 约 180 间 | **已签约 2026-07-15** |"),
]
for a, b in OTA:
    i = find_exact(a)
    if i < 0:
        FAIL.append("⑤ " + a[:24]); L("[MISS] ⑤", a[:36]); continue
    lines[i] = b; L("[OK]   ⑤", a[:32])

# ══ ⑨ 空位口径 ══
i = find("**说明：锦江丽笙体系")
setline(i, """**说明：锦江丽笙体系的高新丽笙精选酒店属中高端有限服务品牌，不在《高星级全服式酒店品牌分级分类（仅 5★+）》的 5 星级全服务品牌名单内，本文不将其列入奢华档次样本，仅作为同期新开供给的参照。** 上表中未公开披露房价的项目，均为开业不足一年或尚未开业、缺乏稳定成交记录者，本报告不以任何推算值替代。

**⭐ 关于「品牌空位」的判断口径修正。** 空位不应按「当前是否已在蓉开业」判断，须按**预期**判断，即在项目决策与实施的时点上，该品牌是否已锁定成都核心商圈的物业。修正后的判断如下：

| 品牌 | 2026 年在蓉状态 | 预期判断（决策时点口径） | 依据 |
|---|---|---|---|
| 文华东方 MO | **已签约**（2022-10-20 中海 489 米塔楼，267 间，2028 开业） | **已被占**（且在天府新区，非锦江） | 中海与文华东方管理合同云签约 |
| 丽晶 Regent | **已签约**（2026-07-15 顺江路 D10 望江，180 间，2029Q3） | **已被占**（距本项目约 10 公里） | IHG 与新希望地产签约 |
| 尼依格罗 Niccolo | 在营（IFS 230 间） | 已被占（春熙路正位） | OTA 房型页实测 |
| 瑞吉 St. Regis | 在营（太升南路 282 间） | 已被占 | 携程实测 |
| 费尔蒙 Fairmont | 唯一原物业已转洲至奢选棕榈泉 | 已被占 | 物业已转牌 |
| **洲至奢选 Vignette** | 棕榈泉 335 间在营 | **同集团可换牌，无第三方障碍** | OTA 实测 |
| **康莱德 Conrad** | 未见开业 | **空位** | 全球 51 家、中国 15 家，成都在谈未见落地 |
| **柏悦 Park Hyatt** | 未见开业 | **空位** | 凯悦系，中国 3+ 家 |
| **Sofitel 索菲特** | 未见开业（太和非核心） | **空位** | 雅高系，核心商圈尚无 |
| **六善 Six Senses** | 未见开业 | **空位** | IHG 奢华板块 |
| **LXR** | 总府路 28 号 2023-03 单方官宣，3 年无落地 | **重大空位（待核）** | 希尔顿从未官方确认，权益是否流通属传闻 |

**修正后结论：真正可供本项目争取的高端品牌空位为康莱德、柏悦、Sofitel、六善四项（均未在蓉开业），加洲至奢选（同集团可换牌），共五项；而此前被列为「已被占」的文华东方实为已签约状态，其空位不成立。**""", "⑨ 空位口径")

# ══ 第五章（四）（五）、第六章（一）替换 ══
tok5 = {"BRAND_ROWS": "\n".join(brand_rows), "ORDER_ROWS": "\n".join(order_rows),
        "B3": N(BR["B03"]["npv"]), "B8": N(BR["B08"]["npv"]), "B5": N(BR["B05"]["npv"]),
        "B10": N(BR["B10"]["npv"]), "B2": N(BR["B02"]["npv"])}
put_between("### （四）停业方案", "### （五）品牌方案比选", read_frag("fr_5_4.md", {}), "⑥ 第五章（四）停业方案")
put_between("### （五）品牌方案比选", "### （六）可保留项利用方案", read_frag("fr_5_5.md", tok5), "⑨ 第五章（五）品牌比选")
put_between("### （一）估算基准", "### （二）各品牌方案的改造投资", read_frag("fr_6_1.md", {"COST_ROWS": "\n".join(cost_rows)}), "⑧ 第六章（一）三分口径")

open(MD5, "w", encoding="utf-8").write("\n".join(lines))
L("")
L("阶段一完成，未命中 {0} 处".format(len(FAIL)))
for f in FAIL:
    L("   MISS:", f)
json.dump(dict(fail=FAIL), open(os.path.join(T, "v81_fail.json"), "w", encoding="utf-8"), ensure_ascii=False)
L("DONE")
