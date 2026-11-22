"""V8 · KIMI PPT 数据报告蓝灰版 master.

Reproduces Eric's actual production template (used for 2026 H1 economic data 17 frames).
Simulates KIMI PPT mode aesthetic in HTML/CSS so we can render via Edge headless.

Key features:
- 1080x1440 (3:4 standard XHS)
- Deep navy header (#1a2438) + cream body (#f5f3ed)
- White rounded data cards with green/red/black accent numbers
- Black "ranking" blocks with red big data
- Red/yellow risk warning frames
- B166ER watermark + ERIC brand

Usage:
  python v8_kimi_data.py <slides_json> <output_dir>

Where slides_json defines each slide:
  {"kind": "cover", "title": "...", "subtitle": "...", "tag": "官方原文验证版"}
  {"kind": "stats", "kicker": "GDP 上半年累计", "value": "+4.7%", "yoy": "Q2 +4.3% 破下沿", "color": "green|red|black"}
  {"kind": "ranking", "title": "...", "items": [{"name": "...", "value": "..."}]}
  {"kind": "risk", "title": "...", "lines": ["..."]}
  {"kind": "method", "title": "...", "method": "数据→起点→原因→说明→反映问题→推论"}
  {"kind": "outro", "cta": "..."}
"""
import subprocess
import json
import sys
from pathlib import Path
sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace\toolbox')
from watermark_tool import protect_output

# ===== Visual constants (from KIMI PPT export analysis) =====
INK = "#1a2438"          # deep navy header
PAPER = "#f5f3ed"        # cream body
CARD = "#ffffff"         # white data card
ACCENT = "#c8102e"       # red accent
GOLD = "#b08947"         # gold secondary
GREEN = "#16a34a"        # positive
RED = "#dc2626"          # negative
MUTE = "#6b7280"
RULE = "#d6d3c7"

COMMON_CSS = """
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: "Microsoft YaHei", "PingFang SC", "Source Han Sans SC", sans-serif;
    background: #000;
    -webkit-font-smoothing: antialiased;
    color: #0a0a0a;
  }
  .slide {
    width: 1080px;
    height: 1440px;
    position: relative;
    background: #f5f3ed;
    overflow: hidden;
  }
  .top-bar {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 280px;
    background: #1a2438;
    color: #ffffff;
    padding: 80px 70px 50px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .top-bar .tag {
    font-size: 18px;
    letter-spacing: 6px;
    color: #c8102e;
    font-weight: 700;
    text-transform: uppercase;
  }
  .top-bar h1 {
    font-size: 64px;
    font-weight: 900;
    line-height: 1.1;
    color: #ffffff;
    letter-spacing: -0.5px;
  }
  .top-bar h1 .red {
    color: #c8102e;
  }
  .top-bar .source {
    font-size: 16px;
    color: #94a3b8;
    letter-spacing: 3px;
    font-weight: 500;
  }
  .body {
    position: absolute;
    top: 280px; left: 70px; right: 70px; bottom: 70px;
  }
  .data-card {
    background: #ffffff;
    border-radius: 8px;
    padding: 28px 32px;
    border-left: 5px solid #1a2438;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .data-card .label {
    font-size: 18px;
    color: #6b7280;
    letter-spacing: 3px;
    font-weight: 600;
    margin-bottom: 10px;
  }
  .data-card .value {
    font-size: 68px;
    font-weight: 900;
    line-height: 1;
    letter-spacing: -2px;
    margin-bottom: 8px;
  }
  .data-card .value.green { color: #16a34a; }
  .data-card .value.red { color: #dc2626; }
  .data-card .value.black { color: #1a2438; }
  .data-card .yoy {
    font-size: 18px;
    color: #6b7280;
    font-weight: 500;
  }
  .ranking {
    background: #1a2438;
    border-radius: 8px;
    padding: 32px 36px;
    color: #ffffff;
  }
  .ranking .heading {
    font-size: 14px;
    color: #c8102e;
    letter-spacing: 5px;
    font-weight: 700;
    margin-bottom: 18px;
  }
  .ranking .row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 0;
    border-bottom: 1px solid rgba(255,255,255,0.08);
  }
  .ranking .row:last-child { border-bottom: none; }
  .ranking .row .city {
    font-size: 22px;
    font-weight: 600;
    color: #ffffff;
  }
  .ranking .row .val {
    font-size: 22px;
    font-weight: 700;
    color: #c8102e;
    letter-spacing: 0;
  }
  .risk {
    background: #fef2f2;
    border: 2px solid #c8102e;
    border-radius: 8px;
    padding: 24px 28px;
  }
  .risk.yellow {
    background: #fefce8;
    border-color: #b08947;
  }
  .risk .head {
    font-size: 16px;
    color: #c8102e;
    font-weight: 700;
    letter-spacing: 4px;
    margin-bottom: 14px;
  }
  .risk.yellow .head { color: #b08947; }
  .risk .body-text {
    font-size: 20px;
    color: #1a2438;
    line-height: 1.6;
    font-weight: 500;
  }
  .method {
    background: #f5f3ed;
    border: 1.5px solid #1a2438;
    border-radius: 8px;
    padding: 30px 34px;
  }
  .method .label {
    font-size: 14px;
    color: #1a2438;
    letter-spacing: 5px;
    font-weight: 700;
    margin-bottom: 16px;
  }
  .method .formula {
    font-size: 28px;
    font-weight: 600;
    color: #1a2438;
    line-height: 1.5;
    letter-spacing: 2px;
  }
  .footer {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 60px;
    padding: 0 70px;
    border-top: 2px solid #1a2438;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #f5f3ed;
  }
  .footer .by {
    font-size: 13px;
    color: #6b7280;
    letter-spacing: 4px;
    font-weight: 600;
  }
  .footer .b166er {
    font-size: 14px;
    color: #1a2438;
    letter-spacing: 6px;
    font-weight: 800;
  }
"""

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def render_slide(slide, idx, out_dir):
    kind = slide["kind"]
    if kind == "cover":
        body = f"""
        <div class="body">
          <div style="margin-top: 40px;">
            <div style="font-size: 22px; color: #1a2438; font-weight: 700; letter-spacing: 3px;">核心方法论</div>
            <div style="margin-top: 14px; font-size: 26px; color: #1a2438; font-weight: 500; line-height: 1.6;">
              {slide.get("method", "数据 → 起点 → 原因 → 说明 → 反映问题 → 推论")}
            </div>
          </div>
        </div>
        """
        top_bar = f"""
        <div class="top-bar">
          <div class="tag">{slide.get("tag", "官方原文验证版")}</div>
          <h1>{slide["title"]}</h1>
          <div class="source">{slide.get("source", "ERIC & B166ER 出品")}</div>
        </div>
        """
    elif kind == "stats":
        cards_html = ""
        for s in slide["cards"]:
            cards_html += f"""
            <div class="data-card" style="border-left-color: {s.get('accent', '#1a2438')};">
              <div class="label">{s['label']}</div>
              <div class="value {s.get('color', 'black')}">{s['value']}</div>
              <div class="yoy">{s.get('yoy', '')}</div>
            </div>
            """
        top_bar = f"""
        <div class="top-bar">
          <div class="tag">{slide.get("tag", "")}</div>
          <h1>{slide["title"]}</h1>
        </div>
        """
        body = f"""
        <div class="body">
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-top: 24px;">
            {cards_html}
          </div>
        </div>
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
        top_bar = f"""
        <div class="top-bar">
          <div class="tag">{slide.get("tag", "")}</div>
          <h1>{slide["title"]}</h1>
        </div>
        """
        body = f"""
        <div class="body">
          <div class="ranking" style="margin-top: 24px;">
            <div class="heading">{slide.get("heading", "")}</div>
            {rows_html}
          </div>
        </div>
        """
    elif kind == "risk":
        lines_html = "<br/>".join(slide.get("lines", []))
        risk_class = "risk yellow" if slide.get("yellow") else "risk"
        top_bar = f"""
        <div class="top-bar">
          <div class="tag">{slide.get("tag", "")}</div>
          <h1>{slide["title"]}</h1>
        </div>
        """
        body = f"""
        <div class="body">
          <div class="{risk_class}" style="margin-top: 24px;">
            <div class="head">{slide.get("head", "⚠ 风险")}</div>
            <div class="body-text">{lines_html}</div>
          </div>
        </div>
        """
    elif kind == "method":
        top_bar = f"""
        <div class="top-bar">
          <div class="tag">方法论</div>
          <h1>我们的分析框架</h1>
        </div>
        """
        body = f"""
        <div class="body">
          <div class="method" style="margin-top: 40px;">
            <div class="label">5 维认知框架</div>
            <div class="formula">{slide.get("formula", "数据 → 起点 → 原因 → 说明 → 反映问题 → 推论")}</div>
          </div>
        </div>
        """
    elif kind == "outro":
        top_bar = f"""
        <div class="top-bar">
          <div class="tag">ERIC & B166ER</div>
          <h1>{slide["title"]}</h1>
        </div>
        """
        body = f"""
        <div class="body">
          <div style="margin-top: 60px; padding: 40px; background: #1a2438; color: #ffffff; border-radius: 8px; text-align: center;">
            <div style="font-size: 24px; line-height: 1.6; font-weight: 500;">{slide.get("cta", "")}</div>
          </div>
        </div>
        """
    else:
        return None

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>V8 Slide {idx}</title>
<style>{COMMON_CSS}
</style>
</head>
<body>
<div class="slide">
  {top_bar}
  {body}
  <div class="footer">
    <div class="by">{slide.get("by", "ERIC 的 B166ER 出品")}</div>
    <div class="b166er">B166ER · 2026</div>
  </div>
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
        "--window-size=1080,1440",
        f"--screenshot={png_path}",
        html_path.as_uri(),
    ], capture_output=True, text=True, timeout=45)
    print(f"Slide {idx} ({kind}): RC={r.returncode}, size={png_path.stat().st_size if png_path.exists() else 0}")

    out_wm = protect_output(str(png_path))
    print(f"  Watermarked: {out_wm}")
    return out_wm


# ===== Demo: reproduce the 2026 H1 economic data series as proof-of-concept =====
DEMO_SLIDES = [
    {
        "kind": "cover",
        "title": "2026年6月/上半年<br/>经济数据<span class='red'>全方位</span>解读",
        "tag": "官方原文验证版 · B166ER 出品",
        "source": "2026-07-15 · 11 个国统局官方原文",
        "method": "数据 → 起点 → 原因 → 说明 → 反映问题 → 推论",
    },
    {
        "kind": "stats",
        "tag": "01 · 主要指标",
        "title": "上半年宏观核心数据",
        "cards": [
            {"label": "GDP 上半年累计", "value": "+4.7%", "yoy": "Q2 +4.3% 破下沿", "color": "green", "accent": "#16a34a"},
            {"label": "房地产开发投资", "value": "-18.0%", "yoy": "金融链条断裂", "color": "red", "accent": "#dc2626"},
            {"label": "出口（6月美元）", "value": "+27.0%", "yoy": "Q4 或回落至 +5-10%", "color": "green", "accent": "#16a34a"},
            {"label": "高技术制造业（独苗引擎）", "value": "+14.1%", "yoy": "但只占制造业 ~15%", "color": "green", "accent": "#16a34a"},
        ],
    },
    {
        "kind": "ranking",
        "tag": "02 · 区域排名",
        "title": "TOP 6 区域 ADR & 入住率",
        "heading": "TOP 6 区域 · 3 天均值",
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
        "tag": "03 · 全国风险",
        "title": "需要警惕的下行因素",
        "head": "⚠ 全国风险",
        "lines": [
            "南方强降雨带 + 黄河流域高温预警",
            "露天景区 / 夜经济冲击",
            "强降雨场景收入降至 ¥189 亿（-11%）",
        ],
    },
    {
        "kind": "method",
        "title": "5 维认知框架",
        "formula": "数据 → 起点 → 原因 → 说明 → 反映问题 → 推论",
    },
    {
        "kind": "outro",
        "title": "谢谢观看",
        "cta": "评论告诉我：<br/>你还想看哪类经济数据？",
    },
]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: v8_kimi_data.py <output_dir> [slides_json]")
        print("Demo: python v8_kimi_data.py D:\\B166ER-OpenClaw\\workspace\\output\\v8_demo")
        out_dir = Path(r"D:\B166ER-OpenClaw\workspace\output\v8_demo")
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

    print(f"\n=== {len(slides)} slides rendered to {out_dir} ===")