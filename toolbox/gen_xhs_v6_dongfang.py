#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书多图笔记 - 「酒店退款，钱到底在谁那里？」
V6 东方气韵实战版模板（米黄纸底 + 暖褐 + 朱红 + 金边 + 圆形B标 + 居中 + 高密度）
输出: 6 张 3:4 竖版 1080x1440 -> scale2 = 2160x2880
"""
import os, subprocess

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
OUT_DIR = r"D:\B166ER-OpenClaw\workspace\xhs_ota_refund_v6"
HTML_DIR = os.path.join(OUT_DIR, "html")
PNG_DIR = os.path.join(OUT_DIR, "png")
os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(PNG_DIR, exist_ok=True)

W, H = 1080, 1440

# V6 东方气韵配色
PAPER_TOP = "#f8edd6"
PAPER_BOT = "#ead7ab"
INK = "#231610"        # 深褐黑
INK2 = "#5c4630"       # 中褐
ACCENT = "#c8102e"     # 朱红
GOLD = "#b0893c"       # 金边
CARD = "#fffdf6"       # 白底卡
CARD_BORDER = "#d9c69a"

CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:#231610}}
body{{
  width:{W}px;height:{H}px;
  background:linear-gradient(168deg,{PAPER_TOP} 0%,{PAPER_BOT} 100%);
  font-family:'Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif;
  color:{INK};overflow:hidden;position:relative;
}}
/* 四角金边 L */
.corner{{position:absolute;width:34px;height:34px;border:3px solid {GOLD};opacity:.55}}
.tl{{top:34px;left:34px;border-right:none;border-bottom:none}}
.tr{{top:34px;right:34px;border-left:none;border-bottom:none}}
.bl{{bottom:34px;left:34px;border-right:none;border-top:none}}
.br{{bottom:34px;right:34px;border-left:none;border-top:none}}

.wrap{{
  padding:64px 70px 56px 70px;
  height:100%;display:flex;flex-direction:column;
}}
/* 顶部 B标 */
.top{{
  display:flex;justify-content:space-between;align-items:center;
  border-bottom:2px solid {INK};padding-bottom:16px;
}}
.badge{{display:flex;align-items:center;gap:14px}}
.badge .circle{{
  width:50px;height:50px;border-radius:50%;
  background:{INK};color:{PAPER_TOP};
  display:flex;align-items:center;justify-content:center;
  font-weight:900;font-size:26px;font-family:'Georgia',serif;
}}
.badge .name{{font-weight:900;font-size:21px;letter-spacing:1px;line-height:1.2}}
.badge .name .x{{color:{ACCENT}}}
.top .chapter{{
  font-size:19px;font-weight:700;letter-spacing:2px;color:{INK2};
  text-align:right;line-height:1.3;
}}
.top .chapter b{{color:{ACCENT}}}

/* 主体居中 */
.main{{flex:1;display:flex;flex-direction:column;justify-content:center;text-align:center}}
.kicker{{
  font-size:22px;letter-spacing:5px;color:{ACCENT};font-weight:800;
  margin-bottom:22px;
}}
.kicker::before,.kicker::after{{content:"";display:inline-block;width:44px;height:3px;background:{ACCENT};vertical-align:middle;margin:0 16px}}
h1{{
  font-size:72px;font-weight:900;line-height:1.28;letter-spacing:1px;
  color:{INK};margin-bottom:22px;
}}
h1 .hl{{color:{ACCENT}}}
.lede{{
  font-size:28px;color:{INK2};line-height:1.65;font-weight:500;
  max-width:840px;margin:0 auto;
}}
.lede b{{color:{INK}}}

/* 白底圆角数据卡 */
.card{{
  background:{CARD};border:2px solid {CARD_BORDER};border-radius:18px;
  padding:28px 36px;margin:20px auto 0 auto;
  max-width:880px;text-align:center;
  box-shadow:0 4px 0 rgba(35,22,16,.06);
}}
.card p{{font-size:28px;line-height:1.7;color:{INK};margin-bottom:12px}}
.card p:last-child{{margin-bottom:0}}
.card .dim{{color:{INK2}}}
.card .em{{color:{ACCENT};font-weight:800}}
.card .big{{font-size:44px;font-weight:900;color:{ACCENT};line-height:1.2;letter-spacing:-1px}}

/* 黑榜（深褐底 + 米白字 + 朱红数字） */
.dark{{
  background:{INK};color:{PAPER_TOP};border:none;
  border-radius:18px;padding:28px 36px;
}}
.dark p{{color:{PAPER_TOP}}}
.dark .em{{color:#ffd7a8}}
.dark .big{{color:{ACCENT}}}

/* 对比双卡 */
.vs{{display:flex;gap:18px;margin-top:20px;justify-content:center}}
.vs .box{{
  flex:1;max-width:430px;border-radius:16px;padding:24px 22px;
  background:{CARD};border:2px solid {CARD_BORDER};text-align:center;
}}
.vs .box.dark{{background:{INK};border-color:{INK}}}
.vs .head{{font-size:22px;font-weight:900;letter-spacing:2px;margin-bottom:14px}}
.vs .head.good{{color:#0a5a3c}}
.vs .head.bad{{color:{ACCENT}}}
.vs .box p{{font-size:26px;line-height:1.6;color:{INK}}}
.vs .box.dark p{{color:{PAPER_TOP}}}
.vs .box .em{{color:{ACCENT};font-weight:800}}

/* 流程行 */
.flow{{margin-top:20px;display:flex;flex-direction:column;gap:12px}}
.flow .row{{
  background:{CARD};border:2px solid {CARD_BORDER};border-radius:14px;
  padding:18px 26px;font-size:26px;line-height:1.5;text-align:center;
}}
.flow .row .n{{color:{ACCENT};font-weight:900;margin-right:10px}}
.flow .row .who{{color:{ACCENT};font-weight:800}}

/* 底部 B标 */
.footer{{
  border-top:2px solid {INK};padding-top:16px;
  display:flex;justify-content:space-between;align-items:center;
}}
.footer .credit{{
  font-size:19px;font-weight:800;letter-spacing:1px;color:{INK};
}}
.footer .credit .x{{color:{ACCENT}}}
.footer .tag{{
  font-size:17px;color:{INK2};letter-spacing:2px;font-weight:600;
}}
.footer .circle{{
  width:44px;height:44px;border-radius:50%;
  background:{INK};color:{PAPER_TOP};
  display:flex;align-items:center;justify-content:center;
  font-weight:900;font-size:22px;font-family:'Georgia',serif;
}}
"""

def render(chapter, kicker, title_html, body_html, credit="ERIC & B166ER 共研出品", tag=""):
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body>
<div class="corner tl"></div><div class="corner tr"></div>
<div class="corner bl"></div><div class="corner br"></div>
<div class="wrap">
  <div class="top">
    <div class="badge"><div class="circle">B</div><div class="name">ERIC <span class="x">×</span> B166ER</div></div>
    <div class="chapter">{chapter}</div>
  </div>
  <div class="main">
    <div class="kicker">{kicker}</div>
    <h1>{title_html}</h1>
    {body_html}
  </div>
  <div class="footer">
    <div class="credit">ERIC <span class="x">×</span> B166ER 共研出品</div>
    <div class="tag">{tag}</div>
    <div class="circle">B</div>
  </div>
</div>
</body></html>"""

def shot(idx):
    hp = os.path.join(HTML_DIR, f"{idx}.html")
    pp = os.path.join(PNG_DIR, f"{idx}.png")
    with open(hp, "w", encoding="utf-8") as f:
        pass  # 占位，下面单独写
    url = "file:///" + hp.replace("\\", "/")
    r = subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        f"--screenshot={pp}", f"--window-size={W},{H}",
                        "--force-device-scale-factor=2", url],
                       capture_output=True, text=True, timeout=60)
    return os.path.exists(pp), pp

def gen(idx, html):
    hp = os.path.join(HTML_DIR, f"{idx}.html")
    with open(hp, "w", encoding="utf-8") as f:
        f.write(html)
    pp = os.path.join(PNG_DIR, f"{idx}.png")
    url = "file:///" + hp.replace("\\", "/")
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--screenshot={pp}", f"--window-size={W},{H}",
                    "--force-device-scale-factor=2", url],
                   capture_output=True, text=True, timeout=60)
    ok = os.path.exists(pp)
    print(f"[{idx}] {'OK' if ok else 'FAIL'}")
    return ok

# ============ 图 1 · 封面 ============
gen(1, render(
    chapter="酒店行业真相 · 第 01 期<br><b>P01</b>",
    kicker="中间商零风险套利",
    title_html="酒店退款，<br>钱到底在<span class='hl'>谁那里</span>？",
    body_html="""<div class="lede">客人要退、酒店退不了、OTA 装无辜——<br>每个酒店人都经历过的<b>「踢皮球」</b>。</div>
<div class="card"><p class="em">往下滑，一层层撕开真相。</p></div>""",
    tag="OTA · 渠道真相"
))

# ============ 图 2 · 场景 + 合同真相 ============
gen(2, render(
    chapter="P02 · 现象与合同",
    kicker="退款踢皮球",
    title_html="皮球，<br>到底<span class='hl'>卡在哪</span>？",
    body_html="""<div class="flow">
<div class="row"><span class="who">客人</span>：我要退款，找酒店</div>
<div class="row"><span class="who">酒店</span>：你是 OTA 订的，找 OTA</div>
<div class="row"><span class="who">OTA</span>：得酒店同意，我才能退</div>
</div>
<div class="card"><p><span class="em">真相①</span> 酒店签的是 OTA，不是客人</p>
<p class="dim"><span class="em">真相②</span> 「最晚取消时间」18:00/20:00 过时作废，<br>本为防渠道「占房倒卖」</p></div>""",
    tag="合同主体 · 错位"
))

# ============ 图 3 · 钱在途 + 责任转嫁 ============
gen(3, render(
    chapter="P03 · 资金与责任",
    kicker="钱停中台 · 责任甩两端",
    title_html="钱，<br>到底在<span class='hl'>谁手里</span>？",
    body_html="""<div class="flow">
<div class="row"><span class="n">①</span>客人下单 → 钱进 <span class="who">OTA</span> → 根本没到酒店</div>
<div class="row"><span class="n">②</span>过时未入住 → 订单自动作废（交易已取消）</div>
</div>
<div class="card"><p><span class="em">酒店同意退</span> → OTA「名正言顺」退<br><span class="dim">（钱本来就在它手里）</span></p></div>
<div class="card dark"><p><span class="em">酒店拒绝退</span> → OTA 甩锅：<br>「是酒店不退，我也没办法」</p></div>""",
    tag="资金在途 · 责任转嫁"
))

# ============ 图 4 · 本质 + 数据 ============
gen(4, render(
    chapter="P04 · 看清本质",
    kicker="零风险套利",
    title_html="这不是退款问题，<br>是<span class='hl'>零风险套利</span>",
    body_html="""<div class="vs">
<div class="box"><div class="head good">钱停中台</div><p>中间环节：<br><span class="em">全部得利</span> + 责任豁免</p></div>
<div class="box dark"><div class="head bad">风险甩两端</div><p>酒店 / 客人：<br><span class="em">全部风险</span> + 全部责任</p></div>
</div>
<div class="card"><p><span class="big">21.8%</span> OTA 取消率 vs <span class="big">10.6%</span> 直销</p>
<p class="dim"><span class="em">80%</span> 携程毛利率 vs <span class="em">-320 亿</span> 2024 酒店行业亏损</p></div>""",
    tag="钱在谁那里，谁就免了责"
))

# ============ 图 5 · 延展 + 规律 ============
gen(5, render(
    chapter="P05 · 举一反三",
    kicker="同一逻辑 · 换了不同的皮",
    title_html="这种怪相，<br><span class='hl'>无处不在</span>",
    body_html="""<div class="flow">
<div class="row">外卖 · 网约车 · 电商 · 长租公寓 · 预付费卡</div>
</div>
<div class="card dark"><p><span class="em">谁握着在途资金，谁就握着话语权；</span><br><span class="em">谁被甩了责任，谁就是最后的风险承担者。</span></p></div>
<div class="card"><p><span class="big">51.79 亿</span> 携程因垄断被罚没</p>
<p class="dim">反垄断史上最高 <span class="em">7.5%</span> 比例 · 投诉解决率仅 <span class="em">49.44%</span></p></div>""",
    tag="底层规律 · 从不骗人"
))

# ============ 图 6 · 破局 + 金句 ============
gen(6, render(
    chapter="P06 · 破局",
    kicker="把客人变成自己的人",
    title_html="酒店人，<br>怎么<span class='hl'>破</span>？",
    body_html="""<div class="card"><p><span class="em">私域 · 会员 · 直销</span>，才是真正属于自己的客源。</p></div>
<div class="vs">
<div class="box"><div class="head good">华住</div><p>直销 <span class="em">87%</span><br>会员间夜 <span class="em">74%</span></p></div>
<div class="box"><div class="head good">国际对标</div><p>万豪 Bonvoy <span class="em">1.8亿</span><br>希尔顿 Honors <span class="em">1.5亿</span></p></div>
</div>
<div class="card dark"><p class="em">把 OTA 客源压在 20% 以下，<br>才有资格谈「议价」。</p></div>""",
    tag="别把命脉，交给别人"
))

print(f"\n完成，输出: {PNG_DIR}")
