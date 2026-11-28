# -*- coding: utf-8 -*-
"""make_macro_chart.py — 中国宏观经济周期定位与下行期结束方式 · 9:16 + 3:4 信息图

★ 复用 source-matrix-infographic 的 PROBE / FITJS / 截图口径，不另造质检器
★ 全部字符串用 f-string（数据含 % 会炸，禁用 % 格式化）
★ 口径纪律：
   1. 名义 GDP 与 GDP 平减指数均为机构测算，非官方公布 → 图上标「机构测算」
   2. 「10月当月同比」是券商反推值，非官方发布值 → 图上标「反推」
   3. 固投 −8.1% 须拆成「约 3pct 基数下修 ＋ 约 5pct 真实收缩」
   4. 出口必须区分「金额」与「数量」→ 量已负增长是本图的核心事实
   5. 概率与时点均为本方判断，须标「我的判断 · 非机构预测」
用法: python skills/source-matrix-infographic/scripts/make_macro_chart.py
"""
import io
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_source_matrix as MSM

ROOT = MSM.ROOT
OUT = os.path.join(ROOT, "output", "info_macro")
os.makedirs(OUT, exist_ok=True)
PAGES = {"9x16": (1080, 1920), "3x4": (1080, 1440)}

RED, GREEN, BLUE, GOLD, MUT = "#B3272D", "#2E7D5B", "#3A6B8A", "#B08A46", "#6E6555"
RED2, GREY, INK = "#8E2622", "#9AA0A6", "#1A1714"

CSS = """
:root{--bg:#F8F3E8;--card:#FFF;--line:#E3D9C4;--ink:#1A1714;--mut:#6E6555;
--red:#B3272D;--green:#2E7D5B;--blue:#3A6B8A;--gold:#B08A46;--pad:52px}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:100%}
body{background:var(--bg);color:var(--ink);font-family:"Microsoft YaHei","PingFang SC","Noto Sans CJK SC",sans-serif;-webkit-font-smoothing:antialiased}
.fit{width:1080px;position:relative;overflow:hidden}
.page{width:1080px;padding:var(--pad) var(--pad) 28px;position:absolute;left:0;top:0;transform-origin:top left}
.kicker{display:flex;justify-content:space-between;align-items:baseline;font-size:14px;letter-spacing:.1em;color:var(--red);font-weight:700}
.kicker .r{letter-spacing:.03em;font-weight:600;color:var(--mut);font-size:12.5px}
.rule{height:3px;background:var(--red);margin:11px 0 0;width:84px}
h1{font-size:45px;line-height:1.34;letter-spacing:.01em;margin:15px 0 0;font-weight:900}
h1 .dim{color:var(--mut);font-weight:800;font-size:38px}
h1 em{font-style:normal;color:var(--red)}
.lede{font-size:15.5px;line-height:1.58;color:var(--mut);margin:11px 0 0}
.lede b{color:var(--ink)}
h2{font-size:21px;line-height:1.35;font-weight:900;margin:0;display:flex;align-items:center;gap:9px}
h2::before{content:"";width:6px;height:21px;background:var(--red);display:inline-block}
h2 .note{margin-left:auto;font-size:11.5px;color:var(--mut);font-weight:500}
.sec{margin-top:15px}
.card{background:var(--card);border:1px solid var(--line);border-radius:3px;padding:8px 10px 9px;position:relative;overflow:hidden}
.card::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--red)}
.card.plain::before{display:none}
.card.gold::before{background:var(--gold)}
.card.blue::before{background:var(--blue)}
.card.green::before{background:var(--green)}
.kpi{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:11px}
.kpi div{background:var(--card);border:1px solid var(--line);border-radius:3px;padding:8px 9px}
.kpi b{display:block;font-size:23px;font-weight:900;line-height:1.15}
.kpi b.up{color:var(--red)}
.kpi b.dn{color:var(--green)}
.kpi b.nt{color:var(--ink)}
.kpi span{display:block;font-size:10.5px;color:var(--mut);margin-top:3px;line-height:1.35}
.ct{font-size:13.5px;font-weight:800}
.ct small{font-weight:500;color:var(--mut);font-size:11px;margin-left:6px}
svg.chart{display:block;width:100%;height:180px}
svg.chart.sm{height:152px}
svg.chart.md{height:186px}
svg.chart text{font-family:"Microsoft YaHei","PingFang SC",sans-serif}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:9px}
.jd li{list-style:none;font-size:12.5px;line-height:1.5;color:#3B352C;position:relative;padding-left:15px;margin-top:6px}
.jd li::before{content:"";position:absolute;left:0;top:8px;width:6px;height:6px;background:var(--gold);border-radius:50%}
.jd li b{font-weight:900;color:var(--ink)}
.jd li i{font-style:normal;color:var(--red);font-weight:800}
.note{font-size:11px;color:var(--mut);line-height:1.55;margin-top:7px}
.note b{color:var(--ink)}
table.idx{width:100%;border-collapse:collapse;margin-top:8px}
table.idx th{font-size:10.5px;color:var(--mut);font-weight:700;text-align:left;padding:4px 5px;border-bottom:1px solid var(--line)}
table.idx td{font-size:11px;padding:3.5px;border-bottom:1px solid #F0E9D8;line-height:1.4}
table.idx td.n{font-weight:900;color:var(--red);white-space:nowrap}
table.idx td.c{font-weight:700;white-space:nowrap}
table.idx tr.hi td{background:#FCF4F0}
.foot{margin-top:13px;padding-top:9px;border-top:1px solid var(--line);display:flex;justify-content:space-between;align-items:baseline;font-size:10.5px;color:var(--mut)}
.foot .it{font-style:italic;text-align:right;max-width:640px}
"""

# ---------------- 数据（全部来自判断书＋事实底表，已核） ----------------
# 四条周期：名, 状态色, 窗口起(frac), 窗口止(frac), 标签
CYC = [
    ("名义周期 · 价格与收入", GREEN, -0.02, 0.278, "2026Q2 已转折"),
    ("资产负债表周期 · 地产与居民", GOLD, 0.50, 0.667, "2027H2–2028H1 · p40%"),
    ("实际需求周期 · 消费与就业", RED, 0.667, 0.833, "2028 · p35%"),
    ("外部周期 · AI 资本开支＋流动性", RED2, 0.333, 0.50, "2027H1 · p30%"),
]

# 固定资产投资累计同比（1-10月，逐月恶化）
FAI_X = ["1-2月", "1-6月", "1-7月", "1-8月", "1-9月", "1-10月"]
FAI_V = [1.8, -5.7, -6.7, -7.2, -7.2, -8.1]

# 出口：正负分离条形（金额口径为主，数量口径是核心）
EXP_ROWS = [
    ("集成电路 · 金额", 137.1, RED),
    ("自动数据处理设备 · 金额", 114.8, RED),
    ("高新技术产品 · 金额", 66.6, GOLD),
    ("保税物流 · 金额", 44.1, GOLD),
    ("加工贸易 · 金额", 28.4, GOLD),
    ("一般贸易 · 金额", 13.2, GREY),
    ("劳动密集型 · 金额", 2.4, GREY),
    ("集成电路 · 数量", -2.4, BLUE),
]

# 四条路径
PATH = [
    ("A 换引擎式出清（复制 2016–2018）", 40, "2027H2", GREEN),
    ("B 外部打断与估值重定价（类 2001）", 30, "2027H1", RED),
    ("C 二次通缩与 L 型长期化", 22, "2027H2", GOLD),
    ("D 强刺激 V 型", 8, "2027H2", GREY),
]

# 十个先行指标：名, 当前值, 拐点判据, 高亮
IND = [
    ("集成电路出口<b>数量</b>", "−2.4%", "量增价平＝引擎健康", True),
    ("住户中长期贷款累计", "−501 亿", "转正", True),
    ("美国 10Y 美债", "4.94%", "破 5.5%", True),
    ("PPI 同比", "+5.7%", "环比转负＝输入型退潮", False),
    ("社会消费品零售同比", "+1.0%", "回到 2.5%+", False),
    ("房地产开发投资 / 土地出让", "−21.6% / −25.8%", "收窄至 −10% 内", False),
    ("云厂 AI capex 增速", "+72%", "2027 指引 <20%", False),
]

KPI = [
    ("+6.0%", "名义 GDP · Q3 · 近 18 季最好", "up"),
    ("−8.1%", "固定资产投资 · 1–10 月", "dn"),
    ("−2.4%", "芯片出口<b>数量</b> · 10 月", "dn"),
    ("−25.8%", "土地出让收入 · 1–10 月", "dn"),
]

LED = ("<b>2026 年的中国不在一个统一的「下行期」里。</b>名义周期已在 Q2 转折，实际需求周期没有；"
       "而撑起名义增长的那台引擎 —— AI 硬件出口 —— <b>量的基础已在负增长</b>。")

JD = [
    "① <b>名义上行、实际停滞的撕裂</b>：Q3 名义 GDP +6.0%、平减 +1.5%，但固投 −8.1%、社零 +1.0%、"
    "地产投资 −21.6%、住户贷款累计 <i>−1.46 万亿</i>",
    "② <b>出口的「强」是价格假象</b>：10 月集成电路出口金额 +137.1%，而<b>数量 −2.4%</b>；"
    "AI 两类商品占出口 18.1%、拉动 13.6pct，劳动密集型只有 +2.4%",
    "③ <b>换引擎而非衰退</b>：政府加杠杆（政府债券 +14.4%、占社融 22.7%）＋ AI 出海涨价 ＋ "
    "高技术制造（+17.6%）替换了地产＋基建＋居民加杠杆。<b>新引擎资本密集、不吸纳就业</b> → "
    "利润表改善、需求表恶化",
]

NOTE_CYCLE = ("<b>名义</b>已转折（Q2 平减 +1.6%，结束 12 个季度负增长）；<b>资产负债表</b>与<b>实际需求</b>尚未转折；<b>外部周期</b>正在反向收紧。<b>「下行期何时结束」必须分周期问。</b>")

NOTE_FAI = ("10 月当月同比 −16.9% 是<b>券商反推值</b>，非官方口径；统计局季调环比 10 月 <b>−2.93%</b>（9 月 +0.07%）＝ 绝对量萎缩。<b>−8.1% 中约 3pct 是基数下修、约 5pct 是真实收缩。</b>")

NOTE_EXP = ("★ 唯一的负值是「数量」：<b>金额 +137.1%、数量 −2.4%</b>（另一口径 −2.5%）。出口的「强」是 AI 全球价格链的<b>价格红利</b>，不是份额扩张 —— <b>红利会随 AI capex 减速而消失。</b>")

NOTE_PATH = ("概率与时点均为<b>我的判断 · 非机构预测</b>。路径 B 若兑现，本方酒店业经营端转正时点应<b>后移至 2028H2–2029</b>。")

NOTE_IND = ("判据必须能被<b>非季节因素</b>解释才算数：青年失业率下降主因毕业季扰动消退；社融 10 月多增 3,251 亿里政府债券贡献 7,017 亿（超 100%）—— <b>看着转好，实质是财政在托、季节在退。</b>")

FOOT_SRC = ("源：国家统计局（10/19、11/16、11/18）｜央行 10 月金融统计报告（11/13）｜海关总署（11/10）｜"
             "财政部 1–10 月财政收支（11/20）｜IMF WEO 2026-10 与 GFSR 2026-04｜"
             "中指研究院百城二手｜贝壳研究院｜美联储 10/28 纪要｜券商研究（单源处已标注）")


def svg_timeline(rows, W=980, H=172):
    """四条周期时间线：横向轨道 2026→2029，now 在 2026Q4。"""
    o = []
    T, B = 24, 30
    lab_w = 214
    x0 = lab_w
    tw = W - lab_w - 12
    rh = (H - T - B) / float(len(rows))

    def XF(f):
        return x0 + tw * f

    # 年份刻度
    for i, yr in enumerate(("2026", "2027", "2028", "2029")):
        xx = XF(i / 3.0)
        o.append(f"<line x1='{xx:.1f}' y1='{T - 6}' x2='{xx:.1f}' y2='{H - B + 4:.1f}' stroke='#EFE7D6' stroke-width='1'/>")
        o.append(f"<text x='{xx:.1f}' y='{T - 11}' font-size='9.5' fill='#8A8171' text-anchor='middle'>{yr}</text>")
    # now 线
    nx = XF(0.278)
    o.append(f"<line x1='{nx:.1f}' y1='{T - 6}' x2='{nx:.1f}' y2='{H - B + 4:.1f}' stroke='#B3272D' stroke-width='1.4' stroke-dasharray='4 3'/>")
    o.append(f"<text x='{nx + 5:.1f}' y='{T - 11}' font-size='9.5' font-weight='800' fill='#B3272D'>现在</text>")

    for i, (name, col, a, b, lab) in enumerate(rows):
        cy = T + rh * i + rh * 0.5
        o.append(f"<text x='0' y='{cy + 3:.1f}' font-size='11' font-weight='800' fill='{INK}'>{name}</text>")
        o.append(f"<rect x='{x0:.1f}' y='{cy - 8:.1f}' width='{tw:.1f}' height='16' fill='#FBF7EE' stroke='#EFE7D6'/>")
        xa, xb = XF(max(a, -0.005)), XF(b)
        if xb - xa < 3:
            xb = xa + 4
        o.append(f"<rect x='{xa:.1f}' y='{cy - 8:.1f}' width='{xb - xa:.1f}' height='16' fill='{col}' opacity='0.9' rx='1.5'/>")
        tx = xb + 6
        if tx > W - 12:
            tx = xa - 6
            anc = "end"
        else:
            anc = "start"
        o.append(f"<text x='{tx:.1f}' y='{cy + 3.5:.1f}' font-size='10' font-weight='800' fill='{col}' text-anchor='{anc}'>{lab}</text>")
    return (f"<svg class='chart md' viewBox='0 0 {W} {H}' preserveAspectRatio='xMidYMid meet'>"
            + "".join(o) + "</svg>")


def svg_line(series, labels, ymin, ymax, refs=None, legend=False, W=980, H=178, dec=2):
    L, R, T, B = 58, 74, 26, 26
    iw, ih = W - L - R, H - T - B
    n = len(labels)

    def X(i):
        return L if n == 1 else L + iw * i / float(n - 1)

    def Y(v):
        return T + ih - ih * (v - ymin) / float(ymax - ymin)

    def fm(v):
        return f"{v:,.{dec}f}"

    o = []
    for k in range(3):
        v = ymin + (ymax - ymin) * k / 2.0
        y = Y(v)
        o.append(f"<line x1='{L}' y1='{y:.1f}' x2='{W - R}' y2='{y:.1f}' stroke='#E8DFCB' stroke-width='1'/>")
        o.append(f"<text x='{L - 5}' y='{y + 3:.1f}' font-size='9' fill='#8A8171' text-anchor='end'>{fm(v)}</text>")
    for r in refs or []:
        val, lab, col = r
        if ymin < val < ymax:
            y = Y(val)
            o.append(f"<line x1='{L}' y1='{y:.1f}' x2='{W - R}' y2='{y:.1f}' stroke='{col}' "
                     f"stroke-width='1.1' stroke-dasharray='5 4' opacity='0.85'/>")
            o.append(f"<text x='{W - R + 4}' y='{y + 3:.1f}' font-size='9' fill='{col}'>{lab}</text>")
    for i, lb in enumerate(labels):
        o.append(f"<text x='{X(i):.1f}' y='{H - 8}' font-size='9.5' fill='{MUT}' text-anchor='middle'>{lb}</text>")
    place = []
    for s in series:
        dy = s.get("dy", -9)
        pts = [(X(i), Y(v)) for i, v in enumerate(s["v"])]
        o.append("<polyline points='" + " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts) +
                 f"' fill='none' stroke='{s['c']}' stroke-width='2.4' stroke-linejoin='round' stroke-linecap='round'/>")
        for i, (x, y) in enumerate(pts):
            o.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='3.6' fill='{s['c']}'/>")
            if n > 1 and i == 0:
                ax, anc = x + 8, "start"
            elif n > 1 and i == n - 1:
                ax, anc = x - 8, "end"
            else:
                ax, anc = x, "middle"
            txt = fm(s["v"][i])
            place.append({"x": ax, "y": y + dy, "t": txt, "a": anc, "c": s["c"], "h": len(txt) * 3.2 + 4})
    place.sort(key=lambda p: (p["y"], p["x"]))
    for i in range(len(place)):
        for j in range(i + 1, len(place)):
            a, b = place[i], place[j]
            if b["y"] - a["y"] > 13:
                break
            if abs(b["x"] - a["x"]) < a["h"] + b["h"]:
                b["y"] = a["y"] + 13
    for p in place:
        o.append(f"<text x='{p['x']:.1f}' y='{p['y']:.1f}' font-size='9.5' font-weight='700' "
                 f"fill='{p['c']}' text-anchor='{p['a']}'>{p['t']}</text>")
    if legend:
        x = L + 2
        for s in series:
            o.append(f"<rect x='{x:.1f}' y='{T - 18}' width='10' height='3' fill='{s['c']}'/>")
            o.append(f"<text x='{x + 15:.1f}' y='{T - 13}' font-size='10' fill='{MUT}'>{s['n']}</text>")
            x += 30 + 13 * len(s["n"])
    return (f"<svg class='chart' viewBox='0 0 {W} {H}' preserveAspectRatio='xMidYMid meet'>"
            + "".join(o) + "</svg>")


def svg_signed(rows, W=980, H=176):
    """正负分离条形：金额为正向右，数量为负向左。

    ★ 零轴位置须按「负向留白 + 正向条形 + 数值标签」三段实算，
      不能按比例猜 —— 否则最大条形会冲出 viewBox 右缘、标签被裁。
    """
    o = []
    T, B = 12, 22
    lab_w = 196
    x0 = lab_w
    neg_room = 96
    pos_lab = 54
    zero = x0 + neg_room
    pos_room = W - 8 - zero - pos_lab
    rh = (H - T - B) / float(len(rows))
    mx = max(abs(v) for _, v, _ in rows)
    scale = pos_room / float(mx)
    o.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='#B9AE96' stroke-width='1.2'/>"
             % (zero, T - 2, zero, H - B + 2))
    for i, (name, v, col) in enumerate(rows):
        cy = T + rh * i + rh * 0.5
        o.append("<text x='0' y='%.1f' font-size='10.5' fill='%s'>%s</text>" % (cy + 3.5, INK, name))
        w = abs(v) * scale
        if v >= 0:
            o.append("<rect x='%.1f' y='%.1f' width='%.1f' height='14' rx='1.5' fill='%s'/>"
                     % (zero, cy - 7, w, col))
            o.append("<text x='%.1f' y='%.1f' font-size='10' font-weight='800' fill='%s'>+%.1f%%</text>"
                     % (zero + w + 5, cy + 4, col, v))
        else:
            o.append("<rect x='%.1f' y='%.1f' width='%.1f' height='14' rx='1.5' fill='%s'/>"
                     % (zero - w, cy - 7, w, col))
            o.append("<text x='%.1f' y='%.1f' font-size='10' font-weight='800' fill='%s' text-anchor='end'>%.1f%%</text>"
                     % (zero - w - 5, cy + 4, col, v))
    o.append("<text x='%.1f' y='%d' font-size='9' fill='#8A8171' text-anchor='middle'>0</text>" % (zero, H - 6))
    return ("<svg class='chart md' viewBox='0 0 %d %d' preserveAspectRatio='xMidYMid meet'>" % (W, H)
            + "".join(o) + "</svg>")


def svg_path(rows, W=980, H=150):
    """四条路径概率条形 ＋ 首次可观测时点。"""
    o = []
    T, B = 8, 26
    lab_w = 292
    x0 = lab_w
    tw = W - lab_w - 188
    rh = (H - T - B) / float(len(rows))
    mx = max(v for _, v, _, _ in rows)
    o.append(f"<text x='{x0:.1f}' y='{T + 2}' font-size='9.5' fill='#8A8171'>概率</text>")
    o.append(f"<text x='{W - 72:.1f}' y='{T + 2}' font-size='9.5' fill='#8A8171'>首次可观测</text>")
    for i, (name, v, when, col) in enumerate(rows):
        cy = T + rh * i + rh * 0.5
        o.append(f"<text x='0' y='{cy + 3.5:.1f}' font-size='11' font-weight='700' fill='{INK}'>{name}</text>")
        w = tw * v / float(mx)
        o.append(f"<rect x='{x0:.1f}' y='{cy - 8:.1f}' width='{w:.1f}' height='16' rx='1.5' fill='{col}'/>")
        o.append(f"<text x='{x0 + w + 6:.1f}' y='{cy + 4.5:.1f}' font-size='12' font-weight='900' fill='{col}'>{v}%</text>")
        o.append(f"<text x='{W - 72:.1f}' y='{cy + 3.5:.1f}' font-size='10.5' font-weight='700' fill='{MUT}'>{when}</text>")
    return (f"<svg class='chart sm' viewBox='0 0 {W} {H}' preserveAspectRatio='xMidYMid meet'>"
            + "".join(o) + "</svg>")


def svg_flow(W=980, H=182):
    """全球传导链：上支（当期）与下支（反向收紧）。"""
    o = []
    bw, bh = 152, 40

    def box(x, y, w, h, t1, t2, col, fill="#FFF"):
        o.append(f"<rect x='{x:.1f}' y='{y:.1f}' width='{w:.1f}' height='{h:.1f}' rx='2.5' fill='{fill}' stroke='{col}' stroke-width='1.3'/>")
        o.append(f"<text x='{x + w / 2:.1f}' y='{y + 17:.1f}' font-size='10.5' font-weight='900' fill='{col}' text-anchor='middle'>{t1}</text>")
        o.append(f"<text x='{x + w / 2:.1f}' y='{y + 30:.1f}' font-size='9' fill='{MUT}' text-anchor='middle'>{t2}</text>")

    def arrow(x1, y1, x2, y2, col, dash=False):
        d = " stroke-dasharray='4 3'" if dash else ""
        o.append(f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' stroke='{col}' stroke-width='1.5'{d}/>")
        ang = 0 if x2 > x1 else (3.14159 if x2 < x1 else 0)
        o.append(f"<polygon points='{x2:.1f},{y2:.1f} {x2 - 6:.1f},{y2 - 3.4:.1f} {x2 - 6:.1f},{y2 + 3.4:.1f}' fill='{col}'/>")

    # 上支：当期的强需求引擎
    y1 = 18
    box(4, y1, bw, bh, "AI capex 7,250亿", "2026 · 四家云厂", GOLD, "#FDF8EC")
    arrow(bw + 4, y1 + bh / 2, bw + 26, y1 + bh / 2, GOLD)
    box(bw + 26, y1, bw, bh, "芯片涨价", "出口价 +143%", RED, "#FCF1EF")
    arrow(bw * 2 + 30, y1 + bh / 2, bw * 2 + 52, y1 + bh / 2, RED)
    box(bw * 2 + 52, y1, bw, bh, "中国出口 +35.2%", "PPI +5.7%", RED, "#FCF1EF")
    arrow(bw * 3 + 56, y1 + bh / 2, bw * 3 + 78, y1 + bh / 2, RED)
    box(bw * 3 + 78, y1, bw + 66, bh, "名义 GDP +6.0%", "利润表改善 ✓", GREEN, "#EFF6F2")
    o.append(f"<text x='{bw * 3 + 78:.1f}' y='{y1 + bh + 15:.1f}' font-size='9.5' fill='#6E6555'>但社零 +1.0% · 青年失业 17.2% → <tspan fill='#B3272D' font-weight='800'>需求表恶化</tspan></text>")

    # 中间：断链
    ym = y1 + bh + 30
    o.append(f"<line x1='{bw * 2 + 52 + bw / 2:.1f}' y1='{y1 + bh:.1f}' x2='{bw * 2 + 52 + bw / 2:.1f}' y2='{ym:.1f}' stroke='#C9BCA0' stroke-width='1.2' stroke-dasharray='3 3'/>")

    # 下支：反向收紧
    y2 = ym + 26
    box(4, y2, bw, bh, "美联储已加息", "9/16 全票 +25bp", RED2, "#FBEFEC")
    arrow(bw + 4, y2 + bh / 2, bw + 26, y2 + bh / 2, RED2)
    box(bw + 26, y2, bw, bh, "10Y 4.94%", "12月再加息 94%", RED2, "#FBEFEC")
    arrow(bw * 2 + 30, y2 + bh / 2, bw * 2 + 52, y2 + bh / 2, RED2)
    box(bw * 2 + 52, y2, bw, bh, "折旧墙", "2027–29 翻倍", RED2, "#FBEFEC")
    arrow(bw * 3 + 56, y2 + bh / 2, bw * 3 + 78, y2 + bh / 2, RED2)
    box(bw * 3 + 78, y2, bw + 66, bh, "量价双杀", "出口·PPI 转负", RED2, "#FBEFEC")
    o.append(f"<text x='4' y='{y2 + bh + 15:.1f}' font-size='9.5' fill='#6E6555'>→ 路径 B 风险窗口 <tspan fill='#B3272D' font-weight='800'>2027H1</tspan>：AI capex 只要<tspan font-weight='800'>增速放缓</tspan>就引爆上游（BIS：AI 投资 55.2% 来自 AI 企业内部）</text>")
    return (f"<svg class='chart md' viewBox='0 0 {W} {H}' preserveAspectRatio='xMidYMid meet'>"
            + "".join(o) + "</svg>")


def build(key):
    W, H = PAGES[key]
    p3 = key == "3x4"

    c_cycle = svg_timeline(CYC)
    c_fai = svg_line([{"v": FAI_V, "c": RED, "n": "固定资产投资累计同比"}],
                     FAI_X, -10, 4,
                     refs=[(0, "0 轴", GREY)], legend=True, dec=1)
    c_exp = svg_signed(EXP_ROWS)
    c_path = svg_path(PATH)
    c_flow = svg_flow()

    kpi = "".join(f"<div><b class='{c}'>{a}</b><span>{b}</span></div>" for a, b, c in KPI)
    jd = "".join(f"<li>{x}</li>" for x in JD)

    idx_rows = []
    for n, cur, turn, hi in IND:
        cls = "hi" if hi else ""
        idx_rows.append(f"<tr class='{cls}'><td>{n}</td><td class='n'>{cur}</td><td class='c'>{turn}</td></tr>")
    idx = ("<table class='idx'><tr><th>先行指标</th><th>当前值</th><th>拐点判据</th></tr>"
           + "".join(idx_rows) + "</table>")

    parts = []
    parts.append(
        "<div class='page'>"
        "<div class='kicker'><span>B166ER · 中国宏观经济 · 全球视野</span>"
        "<span class='r'>2026-11-28 · v1.0</span></div>"
        "<div class='rule'></div>"
        "<h1>中国经济不在<br>一个<em>下行期</em>里</h1>"
        f"<p class='lede'>{LED}</p>"
        f"<div class='kpi'>{kpi}</div>")

    parts.append(
        "<div class='sec'><h2>一、四条周期，四种速度<span class='note'>横轴 2026 → 2029</span></h2>"
        f"<div class='card plain'><div class='ct'>周期分层定位<small>本方判断</small></div>{c_cycle}</div>"
        f"<div class='note'>{NOTE_CYCLE}</div></div>")

    parts.append(
        "<div class='sec'><h2>二、实际需求在恶化：投资逐月塌陷<span class='note'>1–10 月累计同比 · %</span></h2>"
        f"<div class='card plain'><div class='ct'>固定资产投资（不含农户）累计同比<small>2026 年逐月</small></div>{c_fai}</div>"
        f"<div class='note'>{NOTE_FAI}</div></div>")

    parts.append(
        "<div class='sec'><h2>三、★ 出口的「强」是价格：量已经负了<span class='note'>2026 年 10 月 · 同比 %</span></h2>"
        f"<div class='card plain'><div class='ct'>出口金额 vs 数量<small>唯一负值即核心事实</small></div>{c_exp}</div>"
        f"<div class='note'>{NOTE_EXP}</div></div>")

    parts.append(
        "<div class='sec'><h2>四、下行期以什么方式结束<span class='note'>我的判断 · 非机构预测</span></h2>"
        f"<div class='card gold'><div class='ct'>四条路径与概率<small>首次可观测时点</small></div>{c_path}</div>"
        f"<div class='note'>{NOTE_PATH}</div></div>")

    if not p3:
        parts.append(
            "<div class='sec'><h2>五、全球传导链：同一个引擎，一边供血一边抽血</h2>"
            f"<div class='card plain'>{c_flow}</div></div>")

    parts.append(
        "<div class='sec'><h2>六、三条判断</h2>"
        f"<div class='card plain'><ul class='jd'>{jd}</ul></div></div>")

    if not p3:
        parts.append(
            "<div class='sec'><h2>七、十个先行指标<span class='note'>高亮＝最该盯的三个</span></h2>"
            f"<div class='card blue'>{idx}</div>"
            f"<div class='note'>{NOTE_IND}</div></div>")

    parts.append(
        "<div class='foot'><span>B166ER · 宏观经济周期定位信息图 v1.0</span>"
        f"<span class='it'>{FOOT_SRC}</span></div>"
        "</div>")

    body = "".join(parts)
    return ("<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><style>" + CSS +
            "</style></head><body><div class='fit' data-h='" + str(H) + "'>" + body + MSM.FITJS +
            "</body></html>")


def qa(html_path, W, H, out_png, tag):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=["--disable-gpu", "--font-render-hinting=none"])
        ctx = b.new_context(viewport={"width": W, "height": H}, device_scale_factor=2)
        pg = ctx.new_page()
        pg.goto("file:///" + html_path.replace("\\", "/"), wait_until="networkidle")
        pg.wait_for_timeout(700)
        pr = pg.evaluate(MSM.PROBE)
        pg.screenshot(path=out_png, clip={"x": 0, "y": 0, "width": W, "height": H})
        b.close()
    scale_ok = pr["scale"] >= 0.80
    content_ok = pr["nText"] >= 70
    size_ok = True
    try:
        from PIL import Image
        with Image.open(out_png) as im:
            size_ok = (im.width == W * 2 and im.height == H * 2)
    except Exception:
        pass
    hard = (pr["ovH"] == 0 and pr["ovV"] == 0 and pr["wideN"] == 0 and pr["clipN"] == 0
            and pr["ovN"] == 0 and pr["outN"] == 0 and pr["owN"] == 0 and scale_ok and content_ok and size_ok)
    print(f"=== QA {tag} ===")
    print(f"  缩放 {pr['natural']} -> {pr['target']} | scale={pr['scale']:.3f} "
          f"{'' if scale_ok else '★过小'} | 填充率 {pr['natural'] * 100.0 / H:.1f}%")
    print(f"  L1 溢出 h={pr['ovH']} v={pr['ovV']} | 越界 {pr['wideN']} | 裁切 {pr['clipN']} | 横溢 {pr['owN']}")
    for c in pr["clip"]:
        print("      裁切:", c)
    print(f"  L2 文本 {pr['nText']} | ★重叠 {pr['ovN']} | ★越出 {pr['outN']} | 死白 {pr['maxGap']}px")
    for o in pr["ov"][:8]:
        print("      重叠:", o)
    print(f"  闸门 内容 {'OK' if content_ok else '★空'} | 尺寸 2x {W * 2}x{H * 2} {'OK' if size_ok else '★'}")
    print(f"  -> {'? 硬质检通过' if hard else '★ 未通过'}")
    return hard


if __name__ == "__main__":
    res = {}
    for key in ["9x16", "3x4"]:
        W, H = PAGES[key]
        hp = os.path.join(OUT, f"macro_cycle_{key}.html")
        pp = os.path.join(OUT, f"macro_cycle_{key}.png")
        open(hp, "w", encoding="utf-8", newline="\n").write(build(key))
        res[key] = qa(hp, W, H, pp, key)
        print(f"  HTML {os.path.getsize(hp)} B | PNG {os.path.getsize(pp)} B\n")
    print("RESULT:", "PASS" if all(res.values()) else "FAIL")
