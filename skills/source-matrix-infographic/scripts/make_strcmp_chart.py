# -*- coding: utf-8 -*-
"""make_strcmp_chart.py - B166ER 与 STR 的行业级对照（同一批问题，两种解法）
v3.0 · 2026-11-21
★ 复用 source-matrix-infographic 的 PROBE / FITJS / 截图口径；不另造质检器
★ 全部字符串用 f-string，禁用 % 格式化
★ v3.0：主体是 B166ER 与 STR 两个数据能力供给方，站在行业层面比较异同；
  不出现任何单一酒店企业的内部内容，结论落在可执行分工而非优劣评判
★ 版权纪律：数据商讲义仅内部使用；本卡只呈现能力对照与维度覆盖，不出现其图表与逐点数据
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
OUT = os.path.join(ROOT, "output", "info_strcmp")
os.makedirs(OUT, exist_ok=True)
PAGES = {"9x16": (1080, 1920), "3x4": (1080, 1440)}
RED, GOLD, BLUE, GREEN, MUT = "#A82A26", "#B08A46", "#3A6B8A", "#2E7D5B", "#6E6555"

CSS = """
:root{--bg:#F8F3E8;--card:#FFF;--line:#E3D9C4;--ink:#1A1714;--mut:#6E6555;
--red:#A82A26;--red2:#B3272D;--gold:#B08A46;--green:#2E7D5B;--blue:#3A6B8A;--purple:#6A5A9E;--pad:50px}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:100%}
body{background:var(--bg);color:var(--ink);font-family:"Microsoft YaHei","PingFang SC","Noto Sans CJK SC",sans-serif;-webkit-font-smoothing:antialiased}
.fit{width:1080px;position:relative;overflow:hidden}
.page{width:1080px;padding:var(--pad) var(--pad) 26px;position:absolute;left:0;top:0;transform-origin:top left}
.kicker{display:flex;justify-content:space-between;align-items:baseline;font-size:15px;letter-spacing:.1em;color:var(--red);font-weight:700}
.kicker .r{letter-spacing:.03em;font-weight:600;color:var(--mut);font-size:13px}
.rule{height:4px;background:var(--red2);margin:12px 0 0;width:96px}
h1{font-size:52px;line-height:1.38;letter-spacing:.01em;margin:16px 0 0;font-weight:900}
h1 .dim{color:var(--mut);font-weight:800}
h1 .b{color:var(--red2)}
.lede{font-size:18px;line-height:1.64;color:var(--mut);margin:13px 0 0}
.lede b{color:var(--ink)}
h2{font-size:23px;line-height:1.34;font-weight:900;margin:0;display:flex;align-items:center;gap:10px}
h2::before{content:"";width:7px;height:23px;background:var(--red2);display:inline-block}
h2 .note{margin-left:auto;font-size:12px;color:var(--mut);font-weight:500}
.sec{margin-top:26px}
.card{background:var(--card);border:1px solid var(--line);border-radius:3px;padding:11px 13px 12px;position:relative;overflow:hidden}
.card::before{content:"";position:absolute;left:0;top:0;bottom:0;width:5px;background:var(--red2)}
.card.plain::before{display:none}
.kpi{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin-top:12px}
.kpi div{background:var(--card);border:1px solid var(--line);border-radius:3px;padding:9px 11px}
.kpi b{display:block;font-size:22px;font-weight:900;line-height:1.2}
.kpi span{display:block;font-size:11.5px;color:var(--mut);margin-top:3px;line-height:1.35}
.kpi .a b{color:var(--red2)}
.kpi .b b{color:var(--blue)}
/* 两栏标题 */
.heads{display:grid;grid-template-columns:repeat(2,1fr);gap:9px;margin-top:12px}
.hd{border:1px solid var(--line);border-radius:3px;padding:8px 12px;background:var(--card);display:flex;align-items:baseline;gap:8px}
.hd .nm{font-size:18px;font-weight:900}
.hd .mt{font-size:12px;color:var(--mut);font-weight:600}
.hd.str{background:#F3F0F8;border-color:#DCD5EC}
.hd.str .nm{color:var(--purple)}
.hd.b16{background:#FBF3EE;border-color:#EEDACB}
.hd.b16 .nm{color:var(--red2)}
/* 对照矩阵 3 列 */
.cmp{display:grid;grid-template-columns:112px 1fr 1fr;margin-top:11px;border:1px solid var(--line);background:var(--card);border-radius:3px;overflow:hidden}
.cmp .h{background:#F0E8D6;font-size:14px;font-weight:900;padding:9px 11px;letter-spacing:.02em;color:#4A4235}
.cmp .h.s{background:#EDE9F5;color:#463A86}
.cmp .h.b{background:#F6E8DF;color:#8E2622}
.cmp .rh{background:#F0E8D6;font-size:14.5px;font-weight:900;padding:11px;color:#4A4235;line-height:1.3;display:flex;align-items:center}
.cmp .c{padding:10px 11px;border-left:1px solid var(--line);border-top:1px solid var(--line);font-size:13px;line-height:1.5;color:#3B352C;min-width:0;overflow-wrap:anywhere;word-break:break-word}
.cmp .c b{font-weight:800;color:var(--ink)}
.cmp .c.s{background:#FBFAFD}
.cmp .c.b{background:#FDFBF8}
.gap li{list-style:none;font-size:13.5px;line-height:1.58;color:#3B352C;position:relative;padding-left:16px;margin-top:7px}
.gap li::before{content:"";position:absolute;left:0;top:8px;width:6px;height:6px;background:var(--gold);border-radius:50%}
.gap li b{font-weight:800;color:var(--ink)}
.gap.same li::before{background:var(--green)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:11px}
.bigread{background:#FBF8F1;border:1px solid var(--line);border-left:6px solid var(--red2);border-radius:3px;padding:15px 17px;margin-top:10px}
.bigread p{font-size:17.5px;line-height:1.66;color:#3B352C}
.bigread p+p{margin-top:9px}
.bigread p b{font-weight:900;color:var(--ink)}
.bigread .hl{color:var(--red2);font-weight:900}
.foot{margin-top:20px;padding-top:10px;border-top:1px solid var(--line);display:flex;justify-content:space-between;align-items:baseline;font-size:11.5px;color:var(--mut)}
.foot .it{font-style:italic;text-align:right;max-width:640px;line-height:1.5}
.p9 h1{font-size:60px;line-height:1.38}
.p9 .lede{font-size:19.5px;line-height:1.66;margin-top:16px}
.p9 .sec{margin-top:30px}
.p9 h2{font-size:26px}
.p9 h2::before{height:26px;width:8px}
.p9 h2 .note{font-size:13px}
.p9 .kpi{margin-top:16px;gap:11px}
.p9 .kpi b{font-size:24px}
.p9 .kpi span{font-size:12px}
.p9 .heads{margin-top:14px}
.p9 .hd{padding:9px 13px}
.p9 .hd .nm{font-size:19px}
.p9 .hd .mt{font-size:12.5px}
.p9 .cmp{margin-top:13px}
.p9 .cmp .h{font-size:15px;padding:10px 12px}
.p9 .cmp .rh{font-size:15px;padding:12px 11px}
.p9 .cmp .c{font-size:13.5px;padding:11px 12px}
.p9 .gap li{font-size:14.5px;line-height:1.6;margin-top:8px}
.p9 .two{gap:11px;margin-top:12px}
.p9 .bigread{padding:17px 19px}
.p9 .bigread p{font-size:19px;line-height:1.68}
.p9 .bigread p+p{margin-top:10px}
.p9 .foot{font-size:12px;margin-top:24px}
.page.p3{padding:26px var(--pad) 18px}
.page.p3 h1{font-size:42px;margin-top:12px}
.page.p3 .lede{font-size:15.5px;line-height:1.52;margin-top:10px}
.page.p3 .sec{margin-top:19px}
.page.p3 h2{font-size:20px}
.page.p3 h2::before{height:20px}
.page.p3 .card{padding:8px 9px 9px}
.page.p3 .kpi{margin-top:9px;gap:8px}
.page.p3 .kpi b{font-size:18px}
.page.p3 .kpi span{font-size:10.5px}
.page.p3 .heads{margin-top:10px;gap:8px}
.page.p3 .hd{padding:7px 10px}
.page.p3 .hd .nm{font-size:15px}
.page.p3 .hd .mt{font-size:10.5px}
.page.p3 .cmp{margin-top:9px}
.page.p3 .cmp .h{font-size:11.5px;padding:6px 8px}
.page.p3 .cmp .rh{font-size:12.5px;padding:8px}
.page.p3 .cmp .c{font-size:11.5px;padding:8px}
.page.p3 .gap li{font-size:12px;line-height:1.5;margin-top:5px}
.page.p3 .two{gap:8px;margin-top:9px}
.page.p3 .bigread{padding:12px 14px;margin-top:9px}
.page.p3 .bigread p{font-size:14px;line-height:1.54}
.page.p3 .bigread p+p{margin-top:7px}
.page.p3 .foot{margin-top:14px;font-size:10px}
"""

KPI = [("a", "79 源 · 13 类", "B166ER 矩阵信源规模"),
       ("a", "46 项 · 9 组", "B166ER 区域市场维度体系"),
       ("b", "41 年 · 260 万间", "STR 样本量与积累"),
       ("b", "51 市场 · 186 次级", "STR 覆盖颗粒度")]

SAME = [
    "<b>回答的是同一批问题</b>：市场在哪、客人是谁、我们的店赚不赚钱、资产值多少——四层问题，谁都躲不开。",
    "<b>都承认单一来源不可靠</b>：一个靠样本与竞争群做校准，一个靠多源交叉与置信度门控，底层是同一条纪律。",
    "<b>都要求口径先于结论</b>：可售间夜、统计区间、竞争群、竞品口径必须写明，否则数字没有可比性。",
    "<b>都把数据当资产而非装饰</b>：不用不产生价值，用错比没有更危险——口径错了，后面全错。",
]

CMP_HEAD = ["对照维度", "STR · 数据商模式", "B166ER · 矩阵模式"]
CMP = [
    ("覆盖层级", "市场层为主：41 年、260 多万间客房、51 市场、186 次级、12 项指标",
     "四层兼顾：市场（30 省／8 强城市／5 大区域／18 区域／4 层级）、客群（8 类客群）、单店（竞对逐个数据＋竞争群＋三指数＋SWOT）、资产（四层定价／REITs／交易案例／抵押与再融资）"),
    ("信源构成", "单一数据商内部采集，样本口径稳定、规模与历史不可复制",
     "79 源 13 类多源交叉：协会、官方统计、国际与国内研究、OTA、上市集团财报、研报、资本与不动产、审计与银行、财经媒体、本土数据"),
    ("颗粒度与口径归属", "分类与颗粒度由数据商定义（市场分类为北美口径，次级市场为商务出行口径）",
     "口径自定：业态×客群×档次×数字化成熟度×绿色化×智能化六维 38 类，可按在地资源与业主诉求重新切分"),
    ("交付形态", "订阅式标准产品：数据接口、逐月序列、Pipeline、在手预订与预测",
     "按任务交付结论件：对标分析、测算模型、改造与定价方案、投资与退出路径、口径卡与竞争群锁定"),
    ("更新节奏", "年度与半年度，发布会式更新",
     "按周；单月可出多版报告、战略判断与测算件"),
    ("可复制性", "复制＝再买一份订阅，边际成本由商业条款决定",
     "复制＝把方法与标准交付出去：口径卡、竞争群、报告范式、判分与校验规则可移交"),
    ("各自的盲区", "长序列与未来在手预订为其独占；单店真实成交价、业主合同、资产公允值无供给",
     "逐月连续序列是自身唯一结构性缺口；其余靠交叉补，但需持续投入维护信源与规则"),
]

SPLIT = [
    "<b>买 STR 的部分</b>：多年长序列、市场层年度基准、全国与跨市场排名、未来在手预订——这些是数据资产，不是方法，推理换不来。",
    "<b>必须自建的部分</b>：单店层与资产层（行业无标准供给）、客群细分基准、按在地资源重新切分、业主与合同侧信息。",
    "<b>交叉的部分</b>：市场层关键结论至少三个独立信源指向一致才敢对外，单源数据仅作内部参考。",
    "<b>纪律部分</b>：每个数据点标注来源、口径、统计区间与置信度；推算必须写明方法与不确定性。",
]

READ = [
    "<b>不是二选一</b>：长序列与未来预订买得到，单店结构与资产真实价值买不到——两者是分工，不是优劣。",
    "<b>先定维度，再定供给</b>：先把要回答的问题与层级列清，再决定买什么、爬什么、自建什么。",
    "<b>缺口即价值</b>：行业没人给的维度，正是自建能形成壁垒的地方。",
    "<b>口径是最贵的资产</b>：口径写错一次，后面所有结论都要推翻重来——这比缺数据更危险。",
]

LEDE = ("酒店经营要回答四层问题：<b>市场、客群、单店、资产</b>。行业里两种典型解法——"
        "<b>STR 是订阅数据商</b>：41 年积累、260 多万间客房、51 个市场，样本与口径由它定义；"
        "<b>B166ER 是矩阵能力</b>：79 源 13 类、46 项维度、4 档置信度门控，逐点可溯、口径自定。"
        "<b>两者回答同一批问题，差别在方法与覆盖面——不是替代关系，是分工。</b>")


def heads():
    o = ["<div class='heads'>"]
    o.append("<div class='hd str'><span class='nm'>STR</span><span class='mt'>数据商模式 · 订阅 · 口径由它定义</span></div>")
    o.append("<div class='hd b16'><span class='nm'>B166ER</span><span class='mt'>矩阵模式 · 自建 · 口径自定</span></div>")
    o.append("</div>")
    return "".join(o)


def matrix():
    o = ["<div class='cmp'><div class='h'></div>"]
    for h in CMP_HEAD[1:]:
        cls = "s" if "STR" in h else "b"
        o.append(f"<div class='h {cls}'>{h}</div>")
    for name, s, b in CMP:
        o.append(f"<div class='rh'>{name}</div>")
        o.append(f"<div class='c s'>{s}</div>")
        o.append(f"<div class='c b'>{b}</div>")
    o.append("</div>")
    return "".join(o)


def build(key):
    W, H = PAGES[key]
    p3 = key == "3x4"
    kpihtml = "".join(f"<div class='{c}'><b>{a}</b><span>{b}</span></div>" for c, a, b in KPI)
    samehtml = "".join(f"<li>{x}</li>" for x in SAME)
    splithtml = "".join(f"<li>{x}</li>" for x in SPLIT)
    readhtml = "".join(f"<li>{x}</li>" for x in READ)
    cls = "page p3" if p3 else "page p9"
    body = ("<div class='" + cls + "'>"
            "<div class='kicker'><span>ERIC &amp; B166ER · 数据能力对照</span><span class='r'>2026-11-21 · v3.0</span></div>"
            "<div class='rule'></div>"
            "<h1>同一批问题，<br><span class='dim'>两种</span><span class='b'>解法</span></h1>"
            "<p class='lede'>" + LEDE + "</p>"
            "<div class='kpi'>" + kpihtml + "</div>"
            "<div class='sec'><h2>一、同：四条共同的底座</h2><div class='card plain'><ul class='gap same'>"
            + samehtml + "</ul></div></div>"
            "<div class='sec'><h2>二、异：七个维度上的差别</h2>"
            + heads() + matrix() + "</div>"
            "<div class='sec'><h2>三、怎么分工</h2><div class='two'>"
            "<div class='card'><ul class='gap'>" + splithtml + "</ul></div>"
            "<div class='bigread'><ul class='gap'>" + readhtml + "</ul></div>"
            "</div></div>"
            "<div class='foot'><span>ERIC &amp; B166ER · 数据能力对照 v3.0</span>"
            "<span class='it'>数据供给格局为行业公开信息之归纳；具体数据商讲义仅内部使用，不得转载、引用或对外发布。</span></div>"
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
    fill = pr["natural"] / float(H)
    print(f"=== QA {tag} ===")
    print(f"  缩放: 自然高 {pr['natural']} -> 目标 {pr['target']} | scale={pr['scale']:.3f} | 填充率 {fill * 100:.1f}%")
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
        hp = os.path.join(OUT, "strcmp_%s.html" % key)
        pp = os.path.join(OUT, "strcmp_%s.png" % key)
        open(hp, "w", encoding="utf-8", newline="\n").write(build(key))
        res[key] = qa(hp, W, H, pp, key)
        print(f"  HTML {os.path.getsize(hp)} B | PNG {os.path.getsize(pp)} B\n")
    print("汇总:", res)
