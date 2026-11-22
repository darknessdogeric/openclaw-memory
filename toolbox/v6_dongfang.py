"""V6 · 东方气韵 master — Eric's primary production visual.

Reproduces the V6 aesthetic used for:
  - Eric 审美基因图鉴 9x16
  - 端午酒店预测 T-2 终稿 9x16
  - 全国端午酒店预测 9x16

Key features:
  - 9:16 (1080x1920) portrait
  - Cream gradient (#f5e8c8 → #e8d4a8)
  - Vermilion accent (#c8102e / #d62828)
  - Deep black + gold trim
  - ERIC & B166ER black rounded logo (top-left)
  - B166ER red square (bottom-right)
  - Black "ranking" block with red big data
  - Vermilion high-impact bar at the bottom
  - White rounded data cards

Slide types:
  - cover: 标题 + 副标 + 数据预言
  - hero: 大数据主推
  - stats: 数据卡矩阵
  - ranking: 黑榜（区域/品牌/品类）
  - risk: 风险警示（黄底）
  - tactic: 关键判断
  - outro: 收口金句
"""
import subprocess
import json
import sys
from pathlib import Path
sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace\toolbox')
from watermark_tool import protect_output

# ===== Visual constants (extracted from V6 production samples) =====
PAPER_TOP = "#f5e8c8"
PAPER_BOT = "#e8d4a8"
ACCENT = "#c8102e"          # vermilion (primary)
DARK_RED = "#9b0e1f"        # deeper red
INK = "#0a0a0a"             # near-black
MUTE = "#5a4a30"            # warm gray
GOLD = "#a07d3c"            # gold trim
GREEN = "#16a34a"
WARM_WHITE = "#faf6ed"

COMMON_CSS = """
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: "Source Han Sans SC", "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
    background: #000;
    -webkit-font-smoothing: antialiased;
    color: #0a0a0a;
  }
  .slide {
    width: 1080px;
    height: 1920px;
    position: relative;
    background: linear-gradient(180deg, #f5e8c8 0%, #e8d4a8 100%);
    overflow: hidden;
  }

  /* ERIC & B166ER logo top-left (black rounded) */
  .logo-tl {
    position: absolute;
    top: 50px; left: 50px;
    background: #0a0a0a;
    color: #faf6ed;
    border-radius: 50px;
    padding: 14px 24px 14px 18px;
    display: flex;
    align-items: center;
    gap: 14px;
    z-index: 20;
  }
  .logo-tl .e-mark {
    width: 36px; height: 36px;
    background: #c8102e;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #faf6ed;
    font-family: "Cormorant Garamond", "Times New Roman", serif;
    font-size: 24px;
    font-weight: 700;
    font-style: italic;
  }
  .logo-tl .label {
    font-size: 11px;
    letter-spacing: 4px;
    color: #faf6ed;
    line-height: 1.3;
    font-weight: 600;
  }
  .logo-tl .label .small { font-size: 9px; letter-spacing: 2px; color: #c8a86e; }

  /* Top-center eyebrow */
  .eyebrow {
    position: absolute;
    top: 130px; left: 50px; right: 50px;
    text-align: center;
    z-index: 5;
  }
  .eyebrow .en {
    font-size: 22px;
    letter-spacing: 8px;
    color: #9b0e1f;
    font-weight: 700;
    font-family: "Cormorant Garamond", "Times New Roman", serif;
  }
  .eyebrow .dot { color: #c8102e; }

  /* B166ER red square bottom-right */
  .b166er-br {
    position: absolute;
    bottom: 50px; right: 50px;
    background: #0a0a0a;
    color: #faf6ed;
    padding: 18px 24px;
    border-radius: 4px;
    z-index: 20;
    text-align: right;
  }
  .b166er-br .big {
    font-size: 24px;
    letter-spacing: 6px;
    font-weight: 800;
    color: #faf6ed;
  }
  .b166er-br .est {
    font-size: 9px;
    letter-spacing: 3px;
    color: #c8a86e;
    margin-top: 4px;
  }
  .b166er-br .red-dot {
    display: inline-block;
    width: 8px; height: 8px;
    background: #c8102e;
    margin-right: 6px;
    vertical-align: middle;
  }

  /* Main title */
  .title-block {
    text-align: center;
    margin: 60px 50px 30px;
  }
  .title-block h1 {
    font-size: 110px;
    font-weight: 900;
    line-height: 1.0;
    color: #0a0a0a;
    letter-spacing: -2px;
    margin-bottom: 16px;
  }
  .title-block h1 .red {
    color: #c8102e;
  }
  .title-block .sub {
    font-size: 32px;
    color: #5a4a30;
    font-weight: 400;
    letter-spacing: 2px;
  }

  /* Hero card (big prediction) */
  .hero-card {
    margin: 50px 60px;
    padding: 50px 40px;
    border: 2.5px solid #c8102e;
    border-radius: 8px;
    background: rgba(255,255,255,0.4);
    text-align: center;
  }
  .hero-card .label {
    font-size: 24px;
    color: #9b0e1f;
    letter-spacing: 6px;
    font-weight: 700;
    margin-bottom: 16px;
  }
  .hero-card .big {
    font-size: 200px;
    font-weight: 900;
    color: #0a0a0a;
    line-height: 0.9;
    letter-spacing: -6px;
    margin: 16px 0;
  }
  .hero-card .big .unit {
    font-size: 80px;
    color: #c8102e;
    margin-left: 4px;
  }
  .hero-card .delta {
    font-size: 28px;
    color: #16a34a;
    font-weight: 700;
    margin-bottom: 14px;
  }
  .hero-card .ref {
    font-size: 18px;
    color: #5a4a30;
    font-weight: 400;
    letter-spacing: 2px;
  }

  /* Data cards (white rounded) */
  .stats-grid {
    margin: 40px 60px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }
  .stat-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 30px 28px;
    text-align: left;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  }
  .stat-card .label {
    font-size: 18px;
    color: #9b0e1f;
    letter-spacing: 3px;
    font-weight: 700;
    margin-bottom: 12px;
  }
  .stat-card .value {
    font-size: 60px;
    font-weight: 900;
    line-height: 1;
    letter-spacing: -2px;
    margin-bottom: 8px;
    color: #0a0a0a;
  }
  .stat-card .value.green { color: #16a34a; }
  .stat-card .value.red { color: #c8102e; }
  .stat-card .yoy {
    font-size: 18px;
    color: #16a34a;
    font-weight: 600;
  }
  .stat-card .yoy.red { color: #c8102e; }

  /* Black ranking block */
  .ranking {
    margin: 40px 60px;
    background: #0a0a0a;
    border-radius: 12px;
    padding: 36px 40px;
    color: #faf6ed;
  }
  .ranking .heading {
    font-size: 16px;
    color: #c8102e;
    letter-spacing: 6px;
    font-weight: 700;
    margin-bottom: 22px;
    text-transform: uppercase;
  }
  .ranking .row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 0;
    border-bottom: 1px solid rgba(255,255,255,0.1);
  }
  .ranking .row:last-child { border-bottom: none; }
  .ranking .city {
    font-size: 24px;
    font-weight: 600;
    color: #faf6ed;
  }
  .ranking .val {
    font-size: 22px;
    font-weight: 700;
    color: #c8102e;
    letter-spacing: 0.5px;
  }

  /* Risk (yellow) */
  .risk {
    margin: 40px 60px;
    background: #fef9e7;
    border: 2px solid #c8102e;
    border-radius: 8px;
    padding: 32px 36px;
  }
  .risk .head {
    font-size: 18px;
    color: #c8102e;
    font-weight: 700;
    letter-spacing: 5px;
    margin-bottom: 14px;
  }
  .risk .body-text {
    font-size: 22px;
    color: #0a0a0a;
    line-height: 1.6;
    font-weight: 500;
  }

  /* Vermilion high-impact bar (bottom call-out) */
  .impact-bar {
    margin: 30px 60px 0;
    background: linear-gradient(90deg, #c8102e 0%, #9b0e1f 100%);
    border-radius: 6px;
    padding: 28px 36px;
    color: #faf6ed;
  }
  .impact-bar .quote {
    font-size: 26px;
    font-weight: 700;
    line-height: 1.55;
    color: #faf6ed;
    letter-spacing: 1px;
  }

  /* Footer bottom-left */
  .footer-bl {
    position: absolute;
    bottom: 50px; left: 50px;
    font-size: 13px;
    color: #5a4a30;
    letter-spacing: 4px;
    font-weight: 600;
    line-height: 1.5;
    z-index: 20;
  }
"""

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def header_html(slide):
    en = slide.get("eyebrow_en", "DRAGON BOAT FESTIVAL · 2026")
    return f"""
    <div class="logo-tl">
      <div class="e-mark">E</div>
      <div class="label">ERIC & B166ER<span class="small">出品</span></div>
    </div>
    <div class="eyebrow">
      <div class="en">{en}</div>
    </div>
    """


def footer_html(slide):
    return f"""
    <div class="footer-bl">
      {slide.get("footer_left", "ERIC 的 B166ER 出品 · 2026")}
    </div>
    <div class="b166er-br">
      <div class="big"><span class="red-dot"></span>B166ER</div>
      <div class="est">EST. 2026 · 主人AI · ERIC</div>
    </div>
    """


def render_slide(slide, idx, out_dir):
    kind = slide["kind"]

    if kind == "cover":
        body = f"""
        {header_html(slide)}
        <div class="title-block">
          <h1>{slide["title_1"]}<br/><span class="red">{slide["title_red"]}</span></h1>
          <div class="sub">{slide.get("subtitle", "")}</div>
        </div>
        <div class="hero-card">
          <div class="label">{slide.get("hero_label", "全国总预测")}</div>
          <div class="big">{slide["hero_value"]}<span class="unit">{slide.get("hero_unit", "")}</span></div>
          <div class="delta">{slide.get("hero_delta", "")}</div>
          <div class="ref">{slide.get("hero_ref", "")}</div>
        </div>
        {footer_html(slide)}
        """

    elif kind == "stats":
        cards_html = ""
        for c in slide["cards"]:
            color_class = c.get("color", "black")
            yoy_class = "red" if c.get("yoy_color", "") == "red" else ""
            cards_html += f"""
            <div class="stat-card">
              <div class="label">{c['label']}</div>
              <div class="value {color_class}">{c['value']}</div>
              <div class="yoy {yoy_class}">{c.get('yoy', '')}</div>
            </div>
            """
        body = f"""
        {header_html(slide)}
        <div class="title-block">
          <h1>{slide['title']}</h1>
        </div>
        <div class="stats-grid">
          {cards_html}
        </div>
        {footer_html(slide)}
        """

    elif kind == "ranking":
        rows_html = ""
        for item in slide["items"]:
            rows_html += f"""
            <div class="row">
              <div class="city">{item['name']}</div>
              <div class="val">{item['value']}</div>
            </div>
            """
        body = f"""
        {header_html(slide)}
        <div class="title-block">
          <h1>{slide['title']}</h1>
        </div>
        <div class="ranking">
          <div class="heading">{slide.get('heading', '')}</div>
          {rows_html}
        </div>
        {footer_html(slide)}
        """

    elif kind == "risk":
        body = f"""
        {header_html(slide)}
        <div class="title-block">
          <h1>{slide['title']}</h1>
        </div>
        <div class="risk">
          <div class="head">{slide.get('head', '⚠ 最大风险')}</div>
          <div class="body-text">{slide.get('body', '')}</div>
        </div>
        {footer_html(slide)}
        """

    elif kind == "tactic":
        body = f"""
        {header_html(slide)}
        <div class="title-block">
          <h1>{slide['title']}</h1>
          <div class="sub">{slide.get('subtitle', '')}</div>
        </div>
        <div class="impact-bar">
          <div class="quote">{slide.get('quote', '')}</div>
        </div>
        {footer_html(slide)}
        """

    elif kind == "outro":
        body = f"""
        {header_html(slide)}
        <div class="title-block">
          <h1>{slide['title']}</h1>
          <div class="sub">{slide.get('subtitle', '')}</div>
        </div>
        <div class="impact-bar" style="margin-top: 200px;">
          <div class="quote">{slide.get('quote', '')}</div>
        </div>
        {footer_html(slide)}
        """

    else:
        return None

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>V6 Slide {idx}</title>
<style>{COMMON_CSS}
</style>
</head>
<body>
<div class="slide">
  {body}
</div>
</body>
</html>"""

    html_path = out_dir / f"slide_{idx:02d}.html"
    png_path = out_dir / f"slide_{idx:02d}.png"
    wm_path = out_dir / f"slide_{idx:02d}_wm.png"

    html_path.write_text(html, encoding='utf-8')

    r = subprocess.run([
        EDGE, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--force-device-scale-factor=2",
        "--window-size=1080,1920",
        f"--screenshot={png_path}",
        html_path.as_uri(),
    ], capture_output=True, text=True, timeout=45)
    print(f"Slide {idx} ({kind}): RC={r.returncode}, size={png_path.stat().st_size if png_path.exists() else 0}")

    out_wm = _pil_watermark(str(png_path))
    print(f"  Watermarked: {out_wm}")
    return out_wm


def _pil_watermark(png_path: str) -> str:
    """PIL visual watermark (replaces blind_watermark lib that hangs)."""
    from PIL import Image, ImageDraw, ImageFont
    p = Path(png_path)
    wm = p.with_name(p.stem + '_wm.png')
    img = Image.open(p).convert("RGBA")
    w, h = img.size
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    # Top-right B166ER small mark
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 28)
        font_small = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 22)
    except Exception:
        font = ImageFont.load_default()
        font_small = font
    # top-left small
    draw.rectangle([(0, 0), (250, 60)], fill=(10, 10, 10, 200))
    draw.text((20, 18), "B166ER · V6", fill=(250, 246, 237, 255), font=font_small)
    # bottom-left small
    draw.rectangle([(0, h-60), (250, h)], fill=(10, 10, 10, 200))
    draw.text((20, h-44), "© B166ER 2026", fill=(200, 168, 110, 255), font=font_small)
    # center diagonal watermark (very faint)
    big_font = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 80) if Path(r"C:\Windows\Fonts\msyhbd.ttc").exists() else font
    wm_text = "B166ER & ERIC"
    bbox = draw.textbbox((0, 0), wm_text, font=big_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    txt_img = Image.new("RGBA", (tw + 40, th + 40), (0, 0, 0, 0))
    txt_draw = ImageDraw.Draw(txt_img)
    txt_draw.text((20, 20), wm_text, fill=(200, 168, 110, 50), font=big_font)
    txt_img = txt_img.rotate(-22, expand=True)
    tx = (w - txt_img.size[0]) // 2
    ty = (h - txt_img.size[1]) // 2
    overlay.paste(txt_img, (tx, ty), txt_img)
    out = Image.alpha_composite(img, overlay).convert("RGB")
    out.save(wm, "PNG", optimize=True)
    return str(wm)


# ===== Demo: reproduce 全国端午预测 =====
DEMO_SLIDES = [
    {
        "kind": "cover",
        "title_1": "全国端午",
        "title_red": "酒店",
        "subtitle": "6/19 - 6/21 · 21 城 · 全网预测",
        "eyebrow_en": "DRAGON BOAT FESTIVAL · 2026",
        "hero_label": "全国酒店总收入预测",
        "hero_value": "¥213",
        "hero_unit": "亿",
        "hero_delta": "↑ 6.2% vs 2025 端午",
        "hero_ref": "基准场景：3 天合计",
    },
    {
        "kind": "stats",
        "title": "入住率 & 房价 · 核心指标",
        "cards": [
            {"label": "日均入住率", "value": "68%", "yoy": "+3.5 ppts 全国", "color": "black"},
            {"label": "日均房价 (ADR)", "value": "¥452", "yoy": "+2.8% YoY", "color": "black"},
            {"label": "RevPAR", "value": "¥307", "yoy": "+8.1% YoY", "color": "green"},
            {"label": "间夜数", "value": "4,712万", "yoy": "+5.5% 全国", "color": "green"},
        ],
    },
    {
        "kind": "ranking",
        "title": "TOP 6 区域 · ADR & 入住率",
        "heading": "TOP 6 区域 ADR & 入住率（3 天均值）",
        "items": [
            {"name": "长三角（沪宁苏杭）", "value": "ADR ¥618 · OCC 75%"},
            {"name": "京津冀（北京/天津）", "value": "ADR ¥558 · OCC 72%"},
            {"name": "珠三角（广深）", "value": "ADR ¥535 · OCC 74%"},
            {"name": "西南（成都/重庆/丽江）", "value": "ADR ¥438 · OCC 72%"},
            {"name": "中部（武汉/长沙/郑州）", "value": "ADR ¥342 · OCC 65%"},
            {"name": "西北（西安/兰州）", "value": "ADR ¥298 · OCC 58%"},
        ],
    },
    {
        "kind": "risk",
        "title": "需要警惕的下行因素",
        "head": "⚠ 全国风险",
        "body": "南方强降雨带 + 黄河流域高温预警 — 露天景区 / 夜经济冲击，强降雨场景收入降至 ¥189 亿（-11%）。",
    },
    {
        "kind": "outro",
        "title": "预测终稿",
        "subtitle": "基准场景 · 21 城 STR 数据",
        "quote": "6/19-6/21 全国酒店总收入 ¥213 亿 · ↑ 6.2%<br/>数据源：26 源 + 迈点 MBI + Amex GBT + 21 城 STR",
    },
]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        out_dir = Path(r"D:\B166ER-OpenClaw\workspace\output\v6_demo")
    else:
        out_dir = Path(sys.argv[1])

    out_dir.mkdir(parents=True, exist_ok=True)

    if len(sys.argv) > 2:
        slides_json = Path(sys.argv[2])
        slides = json.loads(slides_json.read_text(encoding='utf-8'))
    else:
        slides = DEMO_SLIDES

    for idx, slide in enumerate(slides, 1):
        render_slide(slide, idx, out_dir)

    print(f"\n=== {len(slides)} V6 slides rendered to {out_dir} ===")