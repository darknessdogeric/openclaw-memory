# -*- coding: utf-8 -*-
"""ctc_poster_yijing.py — 传统色意境海报（v1.2）

★ 色源：skills/chinese-traditional-color/references/ctc_colors.json（本书 71 色）
★ 渲染/质检：复用 source-matrix-infographic 的 Playwright 渲染口径 + PROBE 三层质检
★ 字体实况：本机无思源宋体，用华文宋体 STSong（印章用楷体 STKaiti），如实声明不假装
★ 迭代记录（每版都经 L3 视觉核验修缺陷）：
   v1.0 缺陷：朱印压诗句／月不可见／山隐形／底部信息挤／副题悬空／诗句被全角空格扯断
   v1.1 修：落印改按列底定位、诗句改两列、底部信息分层、副题移左下
   v1.2 修：月提亮至 0.16 + 双层光晕；远山提亮、近山压深、加雾带与底部压深
   v1.3 修：★★真正根因 —— svg_scene() 未包 <svg> 根元素，裸 circle/path/rect 在 HTML 中
            全不渲染，这才是"山和月始终看不见"的真因（v1.2 之前的诊断"与背景同色"是误诊）
   v1.4 修：元素全渲染后暴露美学问题 —— 远山改圆浑受雾（不再做色板）、近山改不对称尖脊+脊上积雪、
            月改小只作暗示、副题移至夜空区不再压山
   v1.5 修：月改径向渐变柔晕+无硬边淡盘（三层同心圆叠出"靶心灰盘"感，去硬边）；远山脊线柔化
用法:
    python skills/chinese-traditional-color/scripts/ctc_poster_yijing.py
"""
import io
import os
import sys
import json
import random
import importlib.util

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LIB = os.path.join(ROOT, "skills", "chinese-traditional-color", "references", "ctc_colors.json")
OUT = os.path.join(ROOT, "output", "poster_yijing")
os.makedirs(OUT, exist_ok=True)

_sm = os.path.join(ROOT, "skills", "source-matrix-infographic", "scripts", "make_source_matrix.py")
_spec = importlib.util.spec_from_file_location("_sm", _sm)
MSM = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(MSM)

_lib = json.load(open(LIB, encoding="utf-8"))
_by = {c["name"]: c for c in _lib["colors"]}


def hx(name, fallback):
    c = _by.get(name)
    return (c or {}).get("hex") or fallback


DEEP = hx("漆黑", "#161823")
MID = hx("藏青", "#2e4e7e")
MIST = hx("鸦青", "#424c50")
SNOW = hx("月白", "#d6ecf0")
PAPER = hx("铅白", "#f0f0f4")
GOLD = hx("缃黄", "#f0c239")
SEAL = hx("胭脂红", "#9d2933")

FONT_SONG = "'STSong','SimSun','Noto Serif CJK SC',serif"
FONT_KAI = "'STKaiti','KaiTi','SimKai',serif"
SIZES = {"3x4": (1080, 1440), "9x16": (1080, 1920)}

SEAL_JS = """<script>
(function(){
  var cols=[].slice.call(document.querySelectorAll('.vcol'));
  var s=document.querySelector('.seal');
  if(!cols.length||!s) return;
  var bottom=-1;
  for(var i=0;i<cols.length;i++){var r=cols[i].getBoundingClientRect(); if(r.bottom>bottom) bottom=r.bottom;}
  var sr=s.getBoundingClientRect();
  var want=bottom+20;
  if(sr.top<want){ s.style.top=(want+'px'); }
})();
</script>"""


def svg_scene(w, h, k, rng):
    """山水构造：远山圆浑受雾、近山尖峭不对称、脊上积雪、月只作暗示"""
    o = []
    # ---- 月：径向渐变柔晕 + 无硬边淡盘（宋人画法：月为留白，非实心球） ----
    mx, my, mr = w * 0.275, h * 0.215, w * 0.050
    o.append(f"<defs><radialGradient id='moonGlow' cx='50%' cy='50%' r='50%'>"
             f"<stop offset='0%' stop-color='{PAPER}' stop-opacity='0.16'/>"
             f"<stop offset='34%' stop-color='{PAPER}' stop-opacity='0.07'/>"
             f"<stop offset='62%' stop-color='{PAPER}' stop-opacity='0.025'/>"
             f"<stop offset='100%' stop-color='{PAPER}' stop-opacity='0'/>"
             f"</radialGradient></defs>")
    o.append(f"<circle cx='{mx:.0f}' cy='{my:.0f}' r='{mr*3.4:.0f}' fill='url(#moonGlow)'/>")
    o.append(f"<circle cx='{mx:.0f}' cy='{my:.0f}' r='{mr:.0f}' fill='{PAPER}' opacity='0.075'/>")
    # ---- 远山：圆浑山形、被雾稀释（只比背景亮一点点，不做色板） ----
    base = h * 0.655
    far = (f"M0 {base+50:.0f} C {w*0.10:.0f} {base-70:.0f} {w*0.18:.0f} {base-24:.0f} "
           f"{w*0.29:.0f} {base-78:.0f} C {w*0.40:.0f} {base-118:.0f} {w*0.50:.0f} {base-30:.0f} "
           f"{w*0.61:.0f} {base-72:.0f} C {w*0.72:.0f} {base-108:.0f} {w*0.83:.0f} {base-26:.0f} "
           f"{w} {base-56:.0f}")
    o.append(f"<path d='{far} L {w} {h} L 0 {h} Z' fill='#1d2c48' opacity='0.80'/>")
    o.append(f"<path d='{far} L {w} {h} L 0 {h} Z' fill='{SNOW}' opacity='0.035'/>")
    o.append(f"<path d='{far}' fill='none' stroke='{SNOW}' stroke-width='0.9' opacity='0.18'/>")
    # ---- 雾带：远山脚化开（中式山水关键） ----
    fy = h * 0.715
    o.append(f"<rect x='0' y='{fy:.0f}' width='{w}' height='{h*0.055:.0f}' fill='{SNOW}' opacity='0.045'/>")
    o.append(f"<rect x='0' y='{fy+int(h*0.045):.0f}' width='{w}' height='{h*0.025:.0f}' fill='{SNOW}' opacity='0.022'/>")
    # ---- 近山：不对称尖峭折线（避免等腰三角的折纸感） ----
    b2 = h * 0.80
    pts = [(0.00, 60), (0.09, -58), (0.155, -16), (0.245, -122), (0.315, -40),
           (0.405, -96), (0.485, -20), (0.565, -66), (0.655, -28), (0.745, -108),
           (0.825, -38), (0.915, -74), (1.00, -30)]
    xy = [(w * a, b2 + b) for a, b in pts]
    near = "M" + " L ".join(f"{x:.0f} {y:.0f}" for x, y in xy)
    o.append(f"<path d='{near} L {w} {h} L 0 {h} Z' fill='{DEEP}' opacity='0.99'/>")
    o.append(f"<path d='{near}' fill='none' stroke='{MIST}' stroke-width='1.3' opacity='0.70'/>")
    # 脊上积雪：只给最陡的三段
    for i in (3, 6, 9):
        x1, y1 = xy[i]; x2, y2 = xy[i + 1]
        o.append(f"<line x1='{x1:.0f}' y1='{y1:.0f}' x2='{x2:.0f}' y2='{y2:.0f}' "
                 f"stroke='{SNOW}' stroke-width='2' opacity='0.52' stroke-linecap='round'/>")
    # ---- 底部压深：托住信息区 ----
    o.append(f"<rect x='0' y='{h*0.90:.0f}' width='{w}' height='{h*0.10:.0f}' fill='#0a1120' opacity='0.46'/>")
    # ---- 雪 ----
    for _ in range(140):
        x = rng.uniform(0, w)
        y = rng.uniform(0, h * 0.86)
        if x > w - 310 * k and 200 * k < y < 700 * k:
            continue
        if x < 460 * k and 760 * k < y < 850 * k:
            continue
        r = rng.uniform(0.8, 2.6)
        op = rng.uniform(0.16, 0.82) * (1 - 0.38 * (y / h))
        o.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r:.2f}' fill='{SNOW}' opacity='{op:.2f}'/>")
    return (f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' "
            f"viewBox='0 0 {w} {h}' preserveAspectRatio='none'>" + "".join(o) + "</svg>")


def bmark(x, y, size):
    return (f"<div class='bm' style='left:{x}px;top:{y}px'>"
            f"<span class='bcirc' style='width:{size}px;height:{size}px;border-color:{GOLD};color:{GOLD};"
            f"font-size:{size*0.44:.0f}px'>B</span>"
            f"<span class='btx' style='color:{GOLD};font-size:{size*0.5:.0f}px'>ERIC &amp; B166ER</span></div>")


def build(key):
    w, h = SIZES[key]
    k = h / 1440.0
    rng = random.Random(20261126)
    scene = svg_scene(w, h, k, rng)
    pad = int(64 * k)
    poem_size = int(64 * k)
    colw = int(poem_size * 1.42)
    gapc = int(16 * k)
    poem_top = int(238 * k)
    poem_h = int(poem_size * 5 * 1.08)
    seal_size = int(54 * k)
    seal_x = w - int(96 * k) - colw * 2 - gapc - int(14 * k)
    seal_y = poem_top + poem_h + int(96 * k)
    rule_y = int(1238 * k)
    bm_size = int(28 * k)
    sub_top = int(786 * k)

    css = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:100%}}
body{{background:{DEEP};color:{SNOW};font-family:{FONT_SONG};-webkit-font-smoothing:antialiased}}
.fit{{width:{w}px;position:relative;overflow:hidden}}
.page{{width:{w}px;height:{h}px;position:absolute;left:0;top:0;transform-origin:top left;
 background:linear-gradient(176deg,#090e1b 0%,#0c1324 36%,#16233c 60%,#21334f 80%,#0d1526 100%)}}
.bg{{position:absolute;left:0;top:0;width:{w}px;height:{h}px}}
.vig{{position:absolute;left:0;top:0;width:{w}px;height:{h}px;
 background:radial-gradient(112% 70% at 27% 24%, rgba(214,236,240,.11) 0%, rgba(214,236,240,0) 58%)}}
.bm{{position:absolute;display:flex;align-items:center;gap:{int(9*k)}px;z-index:6}}
.bcirc{{display:inline-flex;align-items:center;justify-content:center;border:1px solid;border-radius:50%;
 font-family:{FONT_SONG};font-weight:700;line-height:1}}
.btx{{font-family:{FONT_SONG};letter-spacing:.06em;white-space:nowrap}}
.vcols{{position:absolute;right:{int(96*k)}px;top:{poem_top}px;display:flex;flex-direction:row-reverse;
 gap:{gapc}px;z-index:4}}
.vcol{{writing-mode:vertical-rl;text-orientation:upright;font-size:{poem_size}px;line-height:1.42;
 letter-spacing:.08em;color:{SNOW};font-weight:500}}
.seal{{position:absolute;left:{seal_x}px;top:{seal_y}px;width:{seal_size}px;height:{seal_size}px;
 background:{SEAL};display:flex;align-items:center;justify-content:center;font-family:{FONT_KAI};
 font-size:{int(30*k)}px;color:#f7efe4;border-radius:2px;transform:rotate(-2deg);
 box-shadow:0 0 0 {int(2*k)}px rgba(158,46,51,.30);z-index:6}}
.kick{{position:absolute;left:{pad}px;top:{int(196*k)}px;font-size:{int(22*k)}px;letter-spacing:.42em;
 color:{GOLD};z-index:4}}
.kick2{{position:absolute;left:{pad}px;top:{int(238*k)}px;font-size:{int(14*k)}px;letter-spacing:.28em;
 color:{SNOW};opacity:.56;z-index:4}}
.sub{{position:absolute;left:{pad}px;top:{sub_top}px;font-size:{int(22*k)}px;letter-spacing:.26em;
 color:{SNOW};opacity:.86;z-index:4}}
.rule{{position:absolute;left:{pad}px;right:{pad}px;top:{rule_y}px;height:1px;z-index:4;
 background:linear-gradient(90deg,rgba(240,194,57,.55) 0%,rgba(240,194,57,.16) 60%,rgba(240,194,57,0) 100%)}}
.src{{position:absolute;left:{pad}px;top:{rule_y+int(22*k)}px;font-size:{int(15*k)}px;letter-spacing:.12em;
 color:{SNOW};opacity:.66;z-index:4}}
.dat{{position:absolute;right:{pad}px;top:{rule_y+int(22*k)}px;font-size:{int(14*k)}px;letter-spacing:.14em;
 color:{SNOW};opacity:.48;text-align:right;z-index:4}}
"""
    body = (
        f"<div class='bg'>{scene}</div><div class='vig'></div>"
        + bmark(pad, pad, bm_size)
        + "<div class='kick'>二十四节气 · 小雪</div>"
        + "<div class='kick2'>二〇二六 · 十一月廿二 — 十二月六</div>"
        + "<div class='vcols'><div class='vcol'>晚来天欲雪</div><div class='vcol'>能饮一杯无</div></div>"
        + "<div class='seal'>雪</div>"
        + "<div class='sub'>一间院子　一炉火　一夜客</div>"
        + "<div class='rule'></div>"
        + "<div class='src'>唐 · 刘长卿《逢雪宿芙蓉山主人》</div>"
        + "<div class='dat'>小雪 · 物候 虹藏不见 / 天气上升地气下降</div>"
        + bmark(w - pad - int(196 * k), h - pad - bm_size, bm_size)
    )
    html = ("<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><style>" + css +
            "</style></head><body><div class='fit' data-h='" + str(h) + "'><div class='page'>" +
            body + "</div></div>" + SEAL_JS + MSM.FITJS + "</body></html>")
    return html, w, h


def qa(html_path, w, h, out_png, key):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=["--disable-gpu", "--font-render-hinting=none"])
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2)
        pg = ctx.new_page()
        pg.goto("file:///" + html_path.replace("\\", "/"), wait_until="networkidle")
        pg.wait_for_timeout(700)
        pr = pg.evaluate(MSM.PROBE)
        pg.screenshot(path=out_png, clip={"x": 0, "y": 0, "width": w, "height": h})
        b.close()
    size_ok = True
    try:
        from PIL import Image
        with Image.open(out_png) as im:
            size_ok = (im.width == w * 2 and im.height == h * 2)
    except Exception:
        pass
    hard = (pr["ovH"] == 0 and pr["ovV"] == 0 and pr["wideN"] == 0 and pr["clipN"] == 0
            and pr["ovN"] == 0 and pr["outN"] == 0 and pr["owN"] == 0 and pr["scale"] >= 0.99
            and pr["nText"] >= 6 and size_ok)
    print(f"=== QA {key} ===")
    print(f"  缩放 {pr['scale']:.3f} | 自然高 {pr['natural']} -> {pr['target']} | 填充 {pr['natural']*100.0/pr['target']:.1f}%")
    print(f"  L1: 溢出 h={pr['ovH']} v={pr['ovV']} | 越界 {pr['wideN']} | 裁切 {pr['clipN']} | 横溢 {pr['owN']}")
    print(f"  L2: 文本 {pr['nText']} | ★重叠 {pr['ovN']} | ★越出 {pr['outN']}")
    for o in pr["ov"][:5]:
        print("      重叠:", o)
    print(f"  闸门: 尺寸 2x {w*2}x{h*2} {'OK' if size_ok else '★'}")
    print(f"  -> {'✅ 通过' if hard else '★ 未通过'}")
    return hard


if __name__ == "__main__":
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    res = {}
    for key in ["3x4", "9x16"]:
        if only and key != only:
            continue
        html, w, h = build(key)
        hp = os.path.join(OUT, "yijing_xiaoxue_%s.html" % key)
        pp = os.path.join(OUT, "yijing_xiaoxue_%s.png" % key)
        open(hp, "w", encoding="utf-8", newline="\n").write(html)
        res[key] = qa(hp, w, h, pp, key)
        print(f"  HTML {os.path.getsize(hp)} B | PNG {os.path.getsize(pp)} B\n")
        from PIL import Image
        with Image.open(pp) as im:
            im = im.convert("RGB"); im.thumbnail((720, 720), Image.LANCZOS)
            im.save(os.path.join(OUT, "_th_%s.jpg" % key), quality=84)
    print("汇总:", res)
