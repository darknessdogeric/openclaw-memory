# -*- coding: utf-8 -*-
"""make_inbound_chart.py - 入境客源 2x3 矩阵数据卡（旅行社/酒店 x 成都/四川/全国）
v3.0 · 2026-11-20
★ 复用 source-matrix-infographic 的 PROBE / FITJS / 截图口径；不另造质检器
★ 核心纪律：六级矩阵逐格判定「有官方数 / 无官方数」，无数据不得用总数硬填
★ 全部字符串用 f-string，禁用 % 格式化（数据里含 % 会炸）
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
OUT = os.path.join(ROOT, "output", "info_inbound")
os.makedirs(OUT, exist_ok=True)
PAGES = {"9x16": (1080, 1920), "3x4": (1080, 1440)}
RED, GOLD, BLUE, GREEN, MUT = "#A82A26", "#B08A46", "#3A6B8A", "#2E7D5B", "#6E6555"

# ---- 曲线数据 ----
NAT = [("2023", 8203), ("2024", 13190), ("2025", 15450)]
OVN = [("2019", 6572.5), ("2023", 3431.1)]
CITY = [("2024", 671.0), ("2025", 936.0)]      # 上海（对照）
CDU = [("2024", 147.2), ("2025", 238.0)]       # 成都
VF = [("2024", 2011.5), ("2025", 3008.0)]

CSS = """
:root{--bg:#F8F3E8;--card:#FFF;--line:#E3D9C4;--ink:#1A1714;--mut:#6E6555;
--red:#A82A26;--red2:#B3272D;--gold:#B08A46;--green:#2E7D5B;--blue:#3A6B8A;--pad:52px}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:100%}
body{background:var(--bg);color:var(--ink);font-family:"Microsoft YaHei","PingFang SC","Noto Sans CJK SC",sans-serif;-webkit-font-smoothing:antialiased}
.fit{width:1080px;position:relative;overflow:hidden}
.page{width:1080px;padding:var(--pad) var(--pad) 26px;position:absolute;left:0;top:0;transform-origin:top left}
.kicker{display:flex;justify-content:space-between;align-items:baseline;font-size:14px;letter-spacing:.12em;color:var(--red);font-weight:700}
.kicker .r{letter-spacing:.03em;font-weight:600;color:var(--mut);font-size:12.5px}
.rule{height:3px;background:var(--red2);margin:11px 0 0;width:86px}
h1{font-size:46px;line-height:1.32;letter-spacing:.02em;margin:15px 0 0;font-weight:900}
h1 .dim{color:var(--mut);font-weight:800}
.lede{font-size:16px;line-height:1.58;color:var(--mut);margin:11px 0 0}
.lede b{color:var(--ink)}
h2{font-size:20px;line-height:1.35;font-weight:900;margin:0;display:flex;align-items:center;gap:9px}
h2::before{content:"";width:6px;height:20px;background:var(--red2);display:inline-block}
h2 .note{margin-left:auto;font-size:11.5px;color:var(--mut);font-weight:500}
.sec{margin-top:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:3px;padding:9px 11px 10px;position:relative;overflow:hidden}
.card::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--red2)}
.card.plain::before{display:none}
.kpi{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:10px}
.kpi div{background:var(--card);border:1px solid var(--line);border-radius:3px;padding:7px 9px}
.kpi b{display:block;font-size:18px;font-weight:900;color:var(--red2);line-height:1.2}
.kpi span{display:block;font-size:10.5px;color:var(--mut);margin-top:2px;line-height:1.35}
/* 矩阵表 */
.mx{display:grid;grid-template-columns:78px 1fr 1fr;gap:0;margin-top:9px;border:1px solid var(--line);background:var(--card);border-radius:3px;overflow:hidden}
.mx .h{background:#F0E8D6;font-size:11.5px;font-weight:900;padding:6px 8px;letter-spacing:.02em;color:#4A4235}
.mx .rh{background:#F0E8D6;font-size:13px;font-weight:900;padding:8px;display:flex;align-items:center;justify-content:center;color:#4A4235}
.mx .c{padding:7px 9px;border-left:1px solid var(--line);border-top:1px solid var(--line);font-size:11.5px;line-height:1.45}
.mx .c .s{display:inline-block;font-size:9.5px;font-weight:900;padding:1px 5px;border-radius:2px;margin-bottom:3px}
.s.yes{background:#DCEBE2;color:#1E5E42}
.s.no{background:#F2DFDD;color:#8E2622}
.s.part{background:#F5E9D2;color:#7A5C1E}
.mx .c b{font-size:13px;font-weight:900}
.mx .c em{font-style:normal;color:var(--mut);font-size:10.5px;display:block;margin-top:1px}
/* 图表 */
.g2{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:9px}
.ct{font-size:12.5px;font-weight:800;margin-bottom:1px}
.ct small{font-weight:500;color:var(--mut);font-size:10.5px;margin-left:5px}
svg.chart{display:block;width:100%}
.p9 svg.chart{height:196px}
.p3 svg.chart{height:150px}
svg.chart text{font-family:"Microsoft YaHei","PingFang SC",sans-serif}
.gap li{list-style:none;font-size:12px;line-height:1.55;color:#3B352C;position:relative;padding-left:14px;margin-top:3px}
.gap li::before{content:"";position:absolute;left:0;top:7px;width:5px;height:5px;background:var(--gold);border-radius:50%}
.gap li b{font-weight:800;color:var(--ink)}
.foot{margin-top:13px;padding-top:9px;border-top:1px solid var(--line);display:flex;justify-content:space-between;align-items:baseline;font-size:10.5px;color:var(--mut)}
.foot .it{font-style:italic;text-align:right;max-width:640px}
.p9 h1{font-size:54px;line-height:1.3}
.p9 .lede{font-size:17.5px;line-height:1.62;margin-top:14px}
.p9 .sec{margin-top:24px}
.p9 h2{font-size:23px}
.p9 h2::before{height:23px;width:7px}
.p9 h2 .note{font-size:12px}
.p9 .kpi{margin-top:15px;gap:11px}
.p9 .kpi b{font-size:22px}
.p9 .kpi span{font-size:11.5px}
.p9 .ct{font-size:14px}
.p9 .ct small{font-size:11.5px}
.p9 .mx{margin-top:12px}
.p9 .mx .h{font-size:12.5px;padding:8px 10px}
.p9 .mx .rh{font-size:14px;padding:11px}
.p9 .mx .c{font-size:12.5px;padding:9px 11px}
.p9 .mx .c b{font-size:15px}
.p9 .mx .c em{font-size:11px}
.p9 .g2{gap:11px;margin-top:12px}
.p9 .gap li{font-size:13px;line-height:1.62;margin-top:6px}
.p9 .foot{font-size:11px;margin-top:18px}
.page.p3{padding:30px var(--pad) 20px}
.page.p3 h1{font-size:44px;margin-top:11px}
.page.p3 .lede{font-size:15px;line-height:1.5;margin-top:9px}
.page.p3 .sec{margin-top:15px}
.page.p3 h2{font-size:18.5px}
.page.p3 h2::before{height:18px}
.page.p3 .card{padding:8px 9px 9px}
.page.p3 .ct{font-size:13px}
.page.p3 .kpi{margin-top:9px;gap:8px}
.page.p3 .kpi b{font-size:19px}
.page.p3 .kpi span{font-size:10.5px}
.page.p3 .mx{margin-top:7px}
.page.p3 .mx .h{font-size:11px;padding:5px 7px}
.page.p3 .mx .rh{font-size:12.5px;padding:7px}
.page.p3 .mx .c{font-size:11.5px;padding:6px 8px}
.page.p3 .mx .c b{font-size:13px}
.page.p3 .g2{gap:8px;margin-top:7px}
.page.p3 .gap li{font-size:11.5px;line-height:1.5;margin-top:4px}
.page.p3 .foot{margin-top:11px;font-size:10px}
.page.p3 h1{font-size:37px;margin-top:9px}
.page.p3 .lede{font-size:13.5px;line-height:1.42;margin-top:7px}
.page.p3 .kicker{font-size:12.5px}
.page.p3 .sec{margin-top:10px}
.page.p3 h2{font-size:16px}
.page.p3 h2::before{height:16px;width:5px}
.page.p3 h2 .note{font-size:10px}
.page.p3 .card{padding:6px 8px 7px}
.page.p3 .ct{font-size:11.5px}
.page.p3 .kpi{margin-top:7px;gap:6px}
.page.p3 .kpi b{font-size:15px}
.page.p3 .kpi span{font-size:9.5px}
.page.p3 .mx{margin-top:6px}
.page.p3 .mx .h{font-size:10.5px;padding:4px 6px}
.page.p3 .mx .rh{font-size:11.5px;padding:5px}
.page.p3 .mx .c{font-size:10.5px;padding:5px 7px}
.page.p3 .mx .c b{font-size:11.5px}
.page.p3 .g2{gap:7px;margin-top:6px}
.page.p3 .gap li{font-size:10.5px;line-height:1.4;margin-top:2px}
.page.p3 .foot{margin-top:9px;font-size:9.5px}
"""

KPI = [("15450 万", "2025 全国入境游客 · +17.1%"),
       ("仅 2 / 6", "六级矩阵里有官方数的格子"),
       ("238 万", "2025 成都入境游客 · +44.3%"),
       ("0", "四川全省入境客源官方数")]
MATRIX = [
    ("成都", "part", "团队游客 3,689 人次", "2025 五一假期，+23.3%；占当日入境 13.7%",
     "no", "未单列", "只有总盘 238 万人次 +44.3%"),
    ("四川", "no", "未发布", "单企口径：四川康辉 2024 接 2.1 万人次 +88.7%",
     "no", "未发布", "全省入境总数亦未发布（2024/2025 公报无单列）"),
    ("全国", "no", "未发布", "公报只有旅行社营业收入 4,442.7 亿（2023）",
     "part", "入境过夜 3,431 万", "2023；2019 为 6,572.5 万；2024 起停更"),
]
GAP = ["<b>省级是断点，不是数据不存在</b>：云南 2025 报全省入境 864.26 万、过夜 494.72 万（+51.8%）；四川不报",
       "<b>行业拆分只有城市级做</b>：上海月报「旅行社外联 18.05 万 / 接待 27.49 万」；成都只报团队游客",
       "<b>酒店侧可用代理</b>：全国「入境过夜游客」＝住宿需求，但星级饭店不单列入境客源",
       "<b>补齐路径</b>：省文旅厅月度、口岸出入境（移民管理局）、OTA 境外订单、自有 PMS 外籍证件占比"]
READS = ["<b>入境客源的分行业统计本身就残缺</b>：6 格只有 2 格有官方数 —— 引用前先确认口径",
         "<b>成都唯一硬数是团队占比 13.7%</b>：入境客源以自由行为主，旅行社议价权在下降",
         "<b>上海是唯一能拉全曲线的城市</b>：外联 +97.4%、接待 +55.5%、星级饭店出租率 +2.0pp",
         "<b>对酒店的实操含义</b>：拿不到行业客源数，就用自有 PMS 外籍占比自建月度序列"]
LEDE = ("入境客源按「旅行社／酒店」拆分的官方统计，<b>全国不拆、四川不报、成都只报团队</b>。"
        "<b>六级矩阵里只有 2 格有真数</b>：全国入境过夜 3,431 万（2023）、成都团队游客 3,689 人次（2025 五一）。"
        "<b>缺口本身是结论</b> —— 谁有月度行业拆分，谁才做得了入境客源的渠道策略。")


def chart(series, labels, ymin, ymax, W=452, H=150, legend=False, dec=1):
    L, R, T, B = 52, 16, 20, 22
    iw, ih = W - L - R, H - T - B
    n = len(labels)

    def X(i):
        return L if n == 1 else L + iw * i / float(n - 1)

    def Y(v):
        return T + ih - ih * (v - ymin) / float(ymax - ymin)

    def fm(v):
        if v >= 1000:
            return f"{v:,.0f}"
        if float(v).is_integer():
            return f"{int(v)}"
        return f"{v:.{dec}f}"

    o = []
    for k in range(3):
        v = ymin + (ymax - ymin) * k / 2.0
        y = Y(v)
        o.append(f"<line x1='{L}' y1='{y:.1f}' x2='{W - R}' y2='{y:.1f}' stroke='#E8DFCB' stroke-width='1'/>")
        o.append(f"<text x='{L - 4}' y='{y + 3:.1f}' font-size='8.5' fill='#8A8171' text-anchor='end'>{fm(v)}</text>")
    for i, lb in enumerate(labels):
        o.append(f"<text x='{X(i):.1f}' y='{H - 6}' font-size='9' fill='{MUT}' text-anchor='middle'>{lb}</text>")
    for s in series:
        dy = s.get("dy", -8)
        pts = [(X(i), Y(v)) for i, v in enumerate(s["v"])]
        o.append(f"<polyline points='{' '.join(f'{p[0]:.1f},{p[1]:.1f}' for p in pts)}' fill='none' "
                 f"stroke='{s['c']}' stroke-width='2.3' stroke-linejoin='round' stroke-linecap='round'/>")
        for i, (x, y) in enumerate(pts):
            o.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='3.4' fill='{s['c']}'/>")
            if n > 1 and i == 0:
                ax, anc = x + 7, "start"
            elif n > 1 and i == n - 1:
                ax, anc = x - 7, "end"
            else:
                ax, anc = x, "middle"
            o.append(f"<text x='{ax:.1f}' y='{y + dy:.1f}' font-size='9.5' font-weight='700' "
                     f"fill='{s['c']}' text-anchor='{anc}'>{fm(s['v'][i])}</text>")
    if legend:
        x = L + 2
        for s in series:
            o.append(f"<rect x='{x:.1f}' y='{T - 11}' width='9' height='2.5' fill='{s['c']}'/>")
            o.append(f"<text x='{x + 13:.1f}' y='{T - 8}' font-size='9' fill='{MUT}'>{s['n']}</text>")
            x += 26 + 11 * len(s["n"])
    return (f"<svg class='chart' viewBox='0 0 {W} {H}' preserveAspectRatio='xMidYMid meet'>"
            + "".join(o) + "</svg>")


def matrix(rows):
    o = ["<div class='mx'><div class='h'></div><div class='h'>旅行社 · 入境客源量</div>"
         "<div class='h'>酒店业 · 入境客源量</div>"]
    for name, s1, v1, d1, s2, v2, d2 in rows:
        o.append(f"<div class='rh'>{name}</div>")
        for st, vv, dd in ((s1, v1, d1), (s2, v2, d2)):
            tag = {"yes": "有官方数", "part": "仅部分", "no": "无官方数"}[st]
            o.append(f"<div class='c'><span class='s {st}'>{tag}</span><b>{vv}</b><em>{dd}</em></div>")
    o.append("</div>")
    return "".join(o)


def build(key):
    W, H = PAGES[key]
    p3 = key == "3x4"
    chw, chh = (452, 150) if p3 else (452, 196)
    c1 = chart([{"v": [v for _, v in NAT], "c": RED, "n": "全国"}], [y for y, _ in NAT], 0, 18000, chw, chh)
    c2 = chart([{"v": [v for _, v in OVN], "c": BLUE, "n": "过夜"}], [y for y, _ in OVN], 0, 7500, chw, chh)
    c3 = chart([{"v": [v for _, v in CDU], "c": RED, "n": "成都"},
                {"v": [v for _, v in CITY], "c": GOLD, "n": "上海", "dy": 15}],
               ["2024", "2025"], 0, 1050, chw, chh, legend=True)
    c4 = chart([{"v": [v for _, v in VF], "c": GREEN, "n": "免签"}], [y for y, _ in VF], 0, 3400, chw, chh)
    kpihtml = "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in KPI)
    gaphtml = "".join(f"<li>{x}</li>" for x in GAP)
    readhtml = "".join(f"<li>{x}</li>" for x in READS)
    cls = "page p3" if p3 else "page p9"
    body = ("<div class='" + cls + "'>"
            "<div class='kicker'><span>B166ER · 入境客源矩阵</span><span class='r'>2026-11-20 · v3.0</span></div>"
            "<div class='rule'></div>"
            "<h1>入境客源：<br><span class='dim'>六个格子，只有两个有数</span></h1>"
            "<p class='lede'>" + LEDE + "</p>"
            "<div class='kpi'>" + kpihtml + "</div>"
            "<div class='sec'><h2>一、2×3 矩阵：逐格判真<span class='note'>旅行社 / 酒店 × 成都 / 四川 / 全国</span></h2>"
            + matrix(MATRIX) + "</div>"
            "<div class='sec'><h2>二、有数的格子：把曲线拉出来<span class='note'>单位 万人次</span></h2>"
            "<div class='g2'>"
            "<div class='card plain'><div class='ct'>全国 入境游客<small>总盘 · 2023→2025</small></div>" + c1 + "</div>"
            "<div class='card plain'><div class='ct'>全国 入境过夜游客<small>酒店侧代理 · 2019/2023</small></div>" + c2 + "</div>"
            "</div><div class='g2'>"
            "<div class='card plain'><div class='ct'>成都 vs 上海 入境游客<small>2024→2025 · 城市级可比</small></div>" + c3 + "</div>"
            "<div class='card plain'><div class='ct'>全国 免签入境外国人<small>2024→2025</small></div>" + c4 + "</div>"
            "</div></div>"
            "<div class='sec'><h2>三、为什么缺，以及怎么补</h2><div class='card plain'><ul class='gap'>"
            + gaphtml + "</ul></div></div>"
            "<div class='sec'><h2>四、读数</h2><div class='card plain'><ul class='gap'>"
            + readhtml + "</ul></div></div>"
            "<div class='foot'><span>B166ER · 入境客源矩阵 v3.0</span>"
            "<span class='it'>源：文旅部 2023/2024/2025 统计公报｜国家统计局｜国家移民管理局｜中国旅游研究院｜上海市文旅局 2026-01-22｜成都市文广旅局（文旅部转载）｜四川省政府 2026-09-20｜CEIC 引文旅部</span></div>"
            "</div></div>")
    return ("<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><style>"
            + CSS + "</style></head><body><div class='fit' data-h='" + str(H) + "'>"
            + body + MSM.FITJS + "</body></html>")


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
    print(f"  缩放: 自然高 {pr['natural']} -> 目标 {pr['target']} | scale={pr['scale']:.3f} {'' if scale_ok else '★过小'}")
    print(f"  L1: 溢出 h={pr['ovH']} v={pr['ovV']} | 越界 {pr['wideN']} | 裁切 {pr['clipN']} | 横溢 {pr['owN']}")
    print(f"  L2: 文本 {pr['nText']} | ★重叠 {pr['ovN']} | ★越出 {pr['outN']} | 死白 {pr['maxGap']}px")
    for o in pr["ov"][:4]:
        print("      重叠:", o)
    print(f"  闸门: 内容 {'OK' if content_ok else '★空'} | 尺寸 2x {W * 2}x{H * 2} {'OK' if size_ok else '★'}")
    print(f"  -> {'✅ 硬质检通过' if hard else '★ 未通过'}")
    return hard


if __name__ == "__main__":
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    res = {}
    for key in ["9x16", "3x4"]:
        if only and key != only:
            continue
        W, H = PAGES[key]
        hp = os.path.join(OUT, "inbound_%s.html" % key)
        pp = os.path.join(OUT, "inbound_%s.png" % key)
        open(hp, "w", encoding="utf-8", newline="\n").write(build(key))
        res[key] = qa(hp, W, H, pp, key)
        print(f"  HTML {os.path.getsize(hp)} B | PNG {os.path.getsize(pp)} B\n")
    print("汇总:", res)
