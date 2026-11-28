# -*- coding: utf-8 -*-
"""make_nvda_infographic.py — 黄仁勋 11 天（辞职→复职）9:16 信息图

★ 复用 source-matrix-infographic 的 PROBE / FITJS / 截图口径，不另造质检器
★ 全部字符串用 f-string（数据含 % 会炸，禁用 % 格式化）
★ 口径纪律：涨跌幅分开盘/盘中/收盘三档；目标价分「辞职期前值→辞职期低点」与「复职后」两组，不混用
用法: python skills/source-matrix-infographic/scripts/make_nvda_infographic.py
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
OUT = os.path.join(ROOT, "output", "info_nvda")
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920

RED, GREEN, BLUE, GOLD, MUT = "#B3272D", "#2E7D5B", "#3A6B8A", "#B08A46", "#6E6555"
RED2, GREY = "#8E2622", "#9AA0A6"

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
h1{font-size:50px;line-height:1.3;letter-spacing:.01em;margin:15px 0 0;font-weight:900}
h1 .dim{color:var(--mut);font-weight:800;font-size:42px}
.lede{font-size:16.5px;line-height:1.6;color:var(--mut);margin:12px 0 0}
.lede b{color:var(--ink)}
h2{font-size:21px;line-height:1.35;font-weight:900;margin:0;display:flex;align-items:center;gap:9px}
h2::before{content:"";width:6px;height:21px;background:var(--red);display:inline-block}
h2 .note{margin-left:auto;font-size:11.5px;color:var(--mut);font-weight:500}
.sec{margin-top:18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:3px;padding:10px 12px 11px;position:relative;overflow:hidden}
.card::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--red)}
.card.plain::before{display:none}
.card.gold::before{background:var(--gold)}
.card.blue::before{background:var(--blue)}
.card.green::before{background:var(--green)}
.kpi{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:12px}
.kpi div{background:var(--card);border:1px solid var(--line);border-radius:3px;padding:8px 9px}
.kpi b{display:block;font-size:22px;font-weight:900;line-height:1.15}
.kpi b.up{color:var(--red)}
.kpi b.dn{color:var(--green)}
.kpi b.nt{color:var(--ink)}
.kpi span{display:block;font-size:10.5px;color:var(--mut);margin-top:3px;line-height:1.35}
.ct{font-size:13.5px;font-weight:800}
.ct small{font-weight:500;color:var(--mut);font-size:11px;margin-left:6px}
svg.chart{display:block;width:100%;height:196px}
svg.chart.sm{height:150px}
svg.chart text{font-family:"Microsoft YaHei","PingFang SC",sans-serif}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:9px}
.jd li{list-style:none;font-size:13px;line-height:1.6;color:#3B352C;position:relative;padding-left:15px;margin-top:6px}
.jd li::before{content:"";position:absolute;left:0;top:8px;width:6px;height:6px;background:var(--gold);border-radius:50%}
.jd li b{font-weight:900;color:var(--ink)}
.jd li i{font-style:normal;color:var(--red);font-weight:800}
.tl{position:relative;margin-top:9px;padding-left:15px}
.tl::before{content:"";position:absolute;left:4px;top:5px;bottom:5px;width:2px;background:var(--line)}
.tl .it{position:relative;padding:5px 0 5px 13px}
.tl .it::before{content:"";position:absolute;left:-14px;top:12px;width:9px;height:9px;border-radius:50%;background:var(--red);border:2px solid var(--bg)}
.tl .it .d{font-size:12px;font-weight:900;color:var(--red);letter-spacing:.02em}
.tl .it .x{font-size:12px;color:#3B352C;line-height:1.45;margin-top:1px}
.tl .it .x b{font-weight:800}
.note{font-size:11px;color:var(--mut);line-height:1.5;margin-top:7px}
.note b{color:var(--ink)}
.foot{margin-top:16px;padding-top:10px;border-top:1px solid var(--line);display:flex;justify-content:space-between;align-items:baseline;font-size:10.5px;color:var(--mut)}
.foot .it{font-style:italic;text-align:right;max-width:600px}
"""

# ---------------- 数据（全部已核官方/一手口径） ----------------
PRICE = [("10/6 峰值", 239.24), ("11/11 辞前", 173.73), ("11/12 辞职", 166.19),
         ("11/20 谷底", 125.53), ("11/23 复职", 165.05), ("11/24 次日", 153.76)]

SC_X = ["11/24", "12/3 听证", "Q4 财报", "1 月中"]
SCEN = [
    {"n": "乐观 20%", "v": [153.76, 172.0, 190.0, 200.0], "c": RED, "dy": -8},
    {"n": "基准 55%", "v": [153.76, 160.0, 166.0, 168.0], "c": GOLD, "dy": -9},
    {"n": "悲观 25%", "v": [153.76, 142.0, 130.0, 124.0], "c": GREEN, "dy": 16},
]

# 辞职期投行目标价：前值 → 辞职期低点（不是复职后）
TGT = [("Evercore", 465, 186), ("汇丰", 365, 170), ("Baird", 500, 200),
       ("伯恩斯坦", 400, 200), ("美银", 350, 280), ("BMO", 340, 240),
       ("Stifel", 315, 205), ("瑞银", 300, 240)]

# 11/23 复职日涨幅（收盘口径）
RISE = [("戴尔", 20.46), ("Nebius", 20.28), ("SK海力士", 20.00), ("美光", 19.04),
        ("Marvell", 18.37), ("HPE", 18.09), ("英特尔", 16.34), ("台积电", 14.01),
        ("AMD 对照", 6.85)]

KPI = [("−27.7%", "辞职期最大跌幅 · 7 连跌", "dn"),
       ("+31.48%", "复职日收盘 · 2003 年来最大", "up"),
       ("−1.04%", "复职次日立刻回吐", "dn"),
       ("12/3", "参议院银行委公开听证", "nt")]

JD = [
    "<b>+31.5% 是折价回补，不是基本面重估</b>：仍低于 10/6 峰值 <i>31%</i>；CNBC 直言反弹主要是投资者"
    "「弥补损失」，而非计入新增长 —— 治理折价已修，<b>key-man 折价与监管折价一分未修</b>",
    "<b>真正的变量不在 12/3 一个人身上</b>：沃伦+班克斯推动 Blackwell 对华禁售 ≥18 个月；"
    "沃伦+科顿推动境外芯片加追踪定位功能；<b>SemiAnalysis 已下修 2029/2030 全球 AI 加速器资本开支 41%／40%</b>",
    "<b>三张未交的清单</b>（梅利乌斯）：循环交易合规性、出口合规后续路径、<b>一份真正的继任计划</b> —— "
    "复职一个都没解决；调查未结、SEC 会计问询在途、参院听证 12/10 卢特尼克",
]

TL = [
    ("12/1", "众议院闭门问询 —— <b>黄仁勋</b>"),
    ("12/2", "众议院闭门问询 —— 总法律顾问 <b>Tim Teter</b>"),
    ("12/3 10:00", "参议院银行委员会<b>公开听证</b>：保护美国 AI 优势 · 监督出口管制；沃伦称复职「鲁莽」"),
    ("12/10 暂定", "商务部长<b>卢特尼克</b>接受参院问询"),
    ("2027 财年 Q4 财报", "指引 <b>$1300 亿 ±3%</b>、毛利率 71–72% 能否兑现（管理层动荡期后的第一份成绩单）"),
    ("待定", "独立调查结论（董事会委员会查到底）＋ SEC 会计问询 ＋ 继任人公告"),
]

LED = ("11/8 认错 → 11/12 辞职 → 11/17 董事会公开拒绝 → 11/23 全票复职。"
       "股价用 <b>11 天跌掉 27.7%</b>，再用 <b>1 天涨回 31.5%</b> —— 但 11/24 就回吐 6.8%。"
       "<b>这不是基本面重估，是「关键人折价」被定价、又被撤回。</b>")


# ---------------- 绘图 ----------------
def svg_line(series, labels, ymin, ymax, refs=None, legend=False, W=980, H=196, dec=2):
    L, R, T, B = 60, 72, 26, 26
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
    # ---- 标签先收集，再做去碰撞（纵向推开），最后统一输出 ----
    place = []
    for s in series:
        dy = s.get("dy", -8)
        pts = [(X(i), Y(v)) for i, v in enumerate(s["v"])]
        o.append("<polyline points='" + " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts) +
                 f"' fill='none' stroke='{s['c']}' stroke-width='2.3' stroke-linejoin='round' stroke-linecap='round'/>")
        for i, (x, y) in enumerate(pts):
            o.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='3.6' fill='{s['c']}'/>")
            if n > 1 and i == 0:
                ax, anc = x + 8, "start"
            elif n > 1 and i == n - 1:
                ax, anc = x - 8, "end"
            else:
                ax, anc = x, "middle"
            txt = fm(s["v"][i])
            half = len(txt) * 2.9 + 4
            place.append({"x": ax, "y": y + dy, "t": txt, "a": anc, "c": s["c"], "h": half})
    # 去碰撞：同一竖直带内、纵向间距不足者，向下推开
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


def svg_hbar2(rows, maxv, W=452, H=150):
    o = []
    n = len(rows)
    rh = H / float(n)
    for i, (name, v1, v2) in enumerate(rows):
        y0 = i * rh
        o.append(f"<text x='0' y='{y0 + rh * 0.5 - 1:.1f}' font-size='9.5' fill='{MUT}'>{name}</text>")
        x0 = 66
        bw = W - x0 - 34
        for j, (v, col) in enumerate(((v1, "#C9BCA0"), (v2, RED))):
            w = max(2.0, bw * v / float(maxv))
            yy = y0 + rh * 0.5 - 8 + j * 9
            o.append(f"<rect x='{x0}' y='{yy:.1f}' width='{w:.1f}' height='6.5' rx='1.5' fill='{col}'/>")
            o.append(f"<text x='{x0 + w + 4:.1f}' y='{yy + 6:.1f}' font-size='8.5' "
                     f"fill='{RED2 if j else MUT}'>{v}</text>")
    return (f"<svg class='chart sm' viewBox='0 0 {W} {H}' preserveAspectRatio='xMidYMid meet'>"
            + "".join(o) + "</svg>")


def svg_hbar(rows, W=452, H=150):
    o = []
    n = len(rows)
    rh = H / float(n)
    mx = max(v for _, v in rows)
    for i, (name, v) in enumerate(rows):
        y0 = i * rh
        weak = "对照" in name
        col = GREY if weak else RED
        o.append(f"<text x='0' y='{y0 + rh * 0.5 + 3:.1f}' font-size='9.5' fill='{MUT}'>{name}</text>")
        x0 = 70
        bw = W - x0 - 46
        w = max(2.0, bw * v / float(mx))
        o.append(f"<rect x='{x0}' y='{y0 + rh * 0.5 - 4:.1f}' width='{w:.1f}' height='8' rx='1.5' fill='{col}'/>")
        o.append(f"<text x='{x0 + w + 5:.1f}' y='{y0 + rh * 0.5 + 3.5:.1f}' font-size='8.5' "
                 f"font-weight='700' fill='{GREY if weak else RED}'>+{v:.2f}%</text>")
    return (f"<svg class='chart sm' viewBox='0 0 {W} {H}' preserveAspectRatio='xMidYMid meet'>"
            + "".join(o) + "</svg>")


def build():
    c1 = svg_line([{"v": [v for _, v in PRICE], "c": RED, "n": "NVDA"}],
                  [k for k, _ in PRICE], 100, 260,
                  refs=[(239.24, "10/6 峰值 239.24", GREY), (173.73, "辞前 173.73", GOLD)], dec=2)
    c2 = svg_line(SCEN, SC_X, 100, 260,
                  refs=[(239.24, "10/6 峰值", GREY), (173.73, "辞前 173.73", GOLD)],
                  legend=True, dec=0)
    c3 = svg_hbar2(TGT, 500)
    c4 = svg_hbar(RISE)
    kpi = "".join(f"<div><b class='{c}'>{a}</b><span>{b}</span></div>" for a, b, c in KPI)
    jd = "".join(f"<li>{x}</li>" for x in JD)
    tl = "".join(f"<div class='it'><div class='d'>{d}</div><div class='x'>{x}</div></div>" for d, x in TL)
    body = (
        "<div class='page'>"
        "<div class='kicker'><span>B166ER · 美股 · AI 算力链</span><span class='r'>2026-11-25 · v1.0</span></div>"
        "<div class='rule'></div>"
        "<h1>黄仁勋 11 天<br><span class='dim'>从辞职到复职</span></h1>"
        f"<p class='lede'>{LED}</p>"
        f"<div class='kpi'>{kpi}</div>"

        "<div class='sec'><h2>一、股价：11 天跌掉，再 1 天涨回<span class='note'>收盘价 · 美元</span></h2>"
        f"<div class='card plain'><div class='ct'>NVDA 收盘价轨迹<small>2026/10/6 – 11/24</small></div>{c1}</div>"
        "</div>"

        "<div class='sec'><h2>二、预测：到 2027 年 1 月的三条路径<span class='note'>我的判断 · 非机构预测</span></h2>"
        f"<div class='card gold'><div class='ct'>情景推演<small>锚点：12/3 听证 · Q4 财报</small></div>{c2}"
        "<div class='note'>"
        "<b>乐观 20%</b>：调查提前出结论 + 出口管制路径明确 + 继任计划公布 → 185–210；"
        "<b>基准 55%</b>：听证平淡通过、Q4 $1300 亿兑现 → 150–180；"
        "<b>悲观 25%</b>：听证现新证词 / 调查外溢 / SEC 问询坐实 → 120–140。"
        "<b>注意：三条路径的终点全部低于 10/6 峰值 —— 缺口不靠复职填，靠基本面填。</b></div></div>"
        "</div>"

        "<div class='sec'><h2>三、定价的两张证据<span class='note'>左：辞职期目标价腰斩 ｜ 右：复职日涨幅榜</span></h2>"
        "<div class='g2'>"
        f"<div class='card plain'><div class='ct'>投行目标价：前值 → 辞职期低点<small>美元</small></div>{c3}"
        "<div class='note'>复职后修复：花旗 225→240、StoneX 新给 <b>270</b>、梅利乌斯 220、里昂 255；"
        "共识均值 <b>$232.39</b>（32 买 / 11 持有 / 1 卖出）</div></div>"
        f"<div class='card plain'><div class='ct'>11/23 复职日涨幅<small>收盘口径</small></div>{c4}"
        "<div class='note'>同日：费半 <b>+14.03%</b>、纳指 +6.51%、标普 +4.73%、道指 +3.01%，VIX 36→26。"
        "<b>AMD 仅 +6.85%，明显弱</b> —— 「算力去英伟达化」逻辑阶段性降温</div></div>"
        "</div></div>"

        "<div class='sec'><h2>四、三条判断</h2>"
        f"<div class='card plain'><ul class='jd'>{jd}</ul></div></div>"

        "<div class='sec'><h2>五、接下来的硬节点<span class='note'>12 月三道关</span></h2>"
        f"<div class='card blue'><div class='tl'>{tl}</div></div></div>"

        "<div class='foot'><span>B166ER · 黄仁勋 11 天信息图 v1.0</span>"
        "<span class='it'>源：NVIDIA 官网公告（11/12、11/23）｜SEC 10-Q 与 Q3 FY27 财报（11/17）｜Yahoo Finance / 财华社收盘数据｜"
        "CNBC 11/24｜21 世纪经济报道 / 环球时报 / 同花顺 / 财联社 ｜SemiAnalysis 11/13</span></div>"
        "</div>")
    return ("<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><style>" + CSS +
            "</style></head><body><div class='fit' data-h='1920'>" + body + MSM.FITJS +
            "</body></html>")


def qa(html_path, out_png):
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
    print("=== QA 9x16 ===")
    print(f"  缩放: 自然高 {pr['natural']} -> 目标 {pr['target']} | scale={pr['scale']:.3f} "
          f"{'' if scale_ok else '★过小'} | 填充率 {pr['natural'] * 100.0 / 1920:.1f}%")
    print(f"  L1: 溢出 h={pr['ovH']} v={pr['ovV']} | 越界 {pr['wideN']} | 裁切 {pr['clipN']} | 横溢 {pr['owN']}")
    for c in pr["clip"]:
        print("      裁切:", c)
    print(f"  L2: 文本 {pr['nText']} | ★重叠 {pr['ovN']} | ★越出 {pr['outN']} | 死白 {pr['maxGap']}px")
    for o in pr["ov"][:6]:
        print("      重叠:", o)
    print(f"  闸门: 内容 {'OK' if content_ok else '★空'} | 尺寸 2x {W * 2}x{H * 2} {'OK' if size_ok else '★'}")
    print(f"  -> {'✅ 硬质检通过' if hard else '★ 未通过'}")
    return hard


if __name__ == "__main__":
    hp = os.path.join(OUT, "nvda_jensen_9x16.html")
    pp = os.path.join(OUT, "nvda_jensen_9x16.png")
    open(hp, "w", encoding="utf-8", newline="\n").write(build())
    ok = qa(hp, pp)
    print(f"  HTML {os.path.getsize(hp)} B | PNG {os.path.getsize(pp)} B")
    print("RESULT:", "PASS" if ok else "FAIL")
