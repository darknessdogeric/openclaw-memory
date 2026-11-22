#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
gen_time_travel.py — 单图信息美图 · 时间穿越物理学深度解析
基于 biji.com/5JwRyLwpNQ9Ry 笔记内容
小红书范式 · 9:16 全屏 1080×1920 · DSF=2 (Retina)
米白底 + 深红/墨蓝/金棕/翠绿
v2.0 — 修复 Q5/Q6 截断 + 字号优化
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_time_travel_2026-08-16")
OUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920
DSF = 2
DATE = "2026.08.16"
SIG = "ERIC的B166ER出品"

# 自定义 CSS 覆盖 — 9:16 模式优化
EXTRA_CSS = """
<style>
html, body {
  width: 1080px !important;
  height: auto !important;
  min-height: 1920px !important;
  max-height: none !important;
  overflow: visible !important;
}
.layout {
  width: 1080px !important;
  height: auto !important;
  min-height: 1920px !important;
  max-height: none !important;
  padding: 40px 70px 30px;
  gap: 14px;
  overflow: visible !important;
}
.findings-title { font-size: 24px; }
.finding { padding: 14px 0; gap: 16px; }
.finding .num { font-size: 48px; width: 60px; }
.finding .head { font-size: 22px; margin-bottom: 5px; }
.finding .text { font-size: 18px; line-height: 1.5; }
.kpi-row { padding: 0; }
.kpi-cell { padding: 22px 14px; min-height: 180px; }
.kpi-cell .label { font-size: 18px; }
.kpi-cell .val { font-size: 70px; }
.kpi-cell .note { font-size: 16px; }
.main-title { font-size: 96px; margin-bottom: 12px; }
.lead { font-size: 23px; line-height: 1.4; padding-left: 18px; }
.status-bar { font-size: 14px; padding-bottom: 10px; }
.subtitle-bar { font-size: 20px; }
.section-title { font-size: 21px; }
.bottom-section { gap: 8px; }
.signature { padding-top: 8px; font-size: 12px; }
.insight-block .text { font-size: 22px; }
.source-block .text { font-size: 15px; }
</style>
"""

HTML = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><title>时间穿越物理学</title>
<link rel="stylesheet" href="style.css">
""" + EXTRA_CSS + """
</head>
<body><div class="layout">

  <!-- 顶部状态条 -->
  <div class="status-bar">
    <span>PHYSICS · TIME TRAVEL · DEEP DIVE</span>
    <span>@ERIC 出品</span>
  </div>

  <!-- 副标签 -->
  <div class="subtitle-bar">
    <span class="zh">时间穿越物理学</span>
    <span class="en">/ ENERGY WALL · ALCUBIERRE · 6 DEEP QUESTIONS</span>
  </div>

  <!-- 主标题 -->
  <div class="main-title">
    从 <span class="accent">能量壁垒</span><br>
    到 <span class="accent-blue">阿库别瑞</span><br>
    答 <span class="accent-gold">6 个</span>核心问题
  </div>

  <!-- 摘要钩子 -->
  <div class="lead">
    改写历史要 <span class="accent">大爆炸级能量</span>?
    <br>看完这 6 Q&A · <span class="accent-blue">物理学的 6 堵墙</span>。
  </div>

  <!-- KPI: 3 个关键数字 -->
  <div class="section">
    <div class="section-title">关键数字 <span class="en">/ KEY NUMBERS · 数量级跨度 42 阶</span></div>
    <div class="kpi-row">
      <div class="kpi-cell">
        <div class="label">改写历史所需</div>
        <div class="val">10<span style="font-size:28px">⁸⁰</span></div>
        <div class="note">焦耳 · 大爆炸量级</div>
      </div>
      <div class="kpi-cell">
        <div class="label">人体时空环</div>
        <div class="val dark">10<span style="font-size:28px">⁴¹</span></div>
        <div class="note">焦耳 · 木星质量级</div>
      </div>
      <div class="kpi-cell">
        <div class="label">降级幅度</div>
        <div class="val blue">42<span style="font-size:28px">阶</span></div>
        <div class="note">仍有 2 堵墙 · 不可逾越</div>
      </div>
    </div>
  </div>

  <!-- 6 个 Q&A 卡 -->
  <div class="section">
    <div class="findings-title">6 大问题 <span class="en">/ 6 DEEP QUESTIONS</span></div>

    <div class="finding">
      <div class="num">Q1</div>
      <div class="body">
        <div class="head normal"><span class="accent">改写历史要多少能量?</span></div>
        <div class="text">单一宇宙假设下需要 <strong>10⁸⁰ 焦耳</strong>(大爆炸初始总能量)。但有两条规避路径:<span class="em">诺维科夫自洽 / 量子多世界劈裂</span>。</div>
      </div>
    </div>

    <div class="finding">
      <div class="num">Q2</div>
      <div class="body">
        <div class="head normal"><span class="accent">量子坍缩能零能耗穿越吗?</span></div>
        <div class="text"><span class="em">不能</span> · 撞上 3 堵墙:退相干 / 观测者悖论 / <strong>幺正性铁律</strong>(只能分支 · 不能修改)。</div>
      </div>
    </div>

    <div class="finding">
      <div class="num">Q3</div>
      <div class="body">
        <div class="head normal"><span class="accent">黑洞信息悖论推翻因果律?</span></div>
        <div class="text"><span class="em">不能</span> · 光锥因果律独立于信息守恒 · <strong>光锥 ≈ 黑洞视界</strong>(零超曲面)。</div>
      </div>
    </div>

    <div class="finding">
      <div class="num">Q4</div>
      <div class="body">
        <div class="head normal"><span class="accent">只改局部光锥 · 能量能降级?</span></div>
        <div class="text">能 · 人体时空环 ≈ <strong>10⁴¹ 焦耳</strong>(降 42 阶)。但有 2 堵墙:引力场长程性 / 量子纠缠非局域性。</div>
      </div>
    </div>

    <div class="finding">
      <div class="num">Q5</div>
      <div class="body">
        <div class="head normal"><span class="accent">阿库别瑞引擎能时空旅行?</span></div>
        <div class="text"><span class="em">数学自洽 · 物理不可行</span> · 前压空间 + 后膨胀 = 曲速泡 · 燃料 = 木星质量级 <strong>奇异物质</strong>。</div>
      </div>
    </div>

    <div class="finding">
      <div class="num">Q6</div>
      <div class="body">
        <div class="head normal"><span class="accent">最后一道坎在哪?</span></div>
        <div class="text"><span class="em">观测者无法控制曲速泡</span>(前沿与内部无因果联系) · 抵达前 <strong>无法停下或转向</strong>。</div>
      </div>
    </div>
  </div>

  <!-- 底部 + 签名 -->
  <div class="bottom-section">
    <div class="bottom-row">
      <div class="source-block">
        <div class="label">SOURCE <span class="en">来源</span></div>
        <div class="text">biji.com / 5JwRyLwpNQ9Ry · DeepSeek 深度对话总结</div>
      </div>
      <div class="insight-block">
        <div class="label">INSIGHT <span class="en">洞察</span></div>
        <div class="text"><strong>物理</strong>守护<strong>因果</strong> · <span class="em">穿越 = 数学可能 · 物理不可能</span></div>
      </div>
    </div>
    <div class="signature">
      <span class="left">ERIC · PHYSICS · 9:16 DEEP DIVE</span>
      <span class="center">""" + SIG + """</span>
      <span class="right">""" + DATE + """ · v2.0</span>
    </div>
  </div>

</div></body></html>
"""

# 写 HTML
html_path = OUT_DIR / "slide_01.html"
html_path.write_text(HTML, encoding="utf-8")
print(f"[HTML] saved: {html_path}")

# 渲染
print("\n[RENDER] 1080x1920 start ...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(
        viewport={"width": W, "height": H},
        device_scale_factor=DSF,
        locale="zh-CN",
    )
    page = ctx.new_page()
    page.goto(f"file:///{html_path.as_posix()}", wait_until="networkidle")
    page.wait_for_timeout(900)
    png_path = OUT_DIR / "slide_01.png"
    page.screenshot(path=str(png_path), type="png", full_page=False)
    print(f"  [OK] {png_path.name} ({png_path.stat().st_size:,} B)")
    browser.close()

# 水印
print("\n[WATERMARK] start ...")
img = Image.open(png_path).convert("RGBA")
W_img, H_img = img.size
overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)
text = "(c) ERIC B166ER / 2026.08.16"
font_size = max(int(W * 0.013 * DSF), 13 * DSF)
try:
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
except Exception:
    font = ImageFont.load_default()
bbox = draw.textbbox((0, 0), text, font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
margin_x, margin_y = 130, 200
x = W_img - tw - margin_x
y = H_img - th - margin_y
draw.rounded_rectangle(
    [x - 16, y - 8, x + tw + 16, y + th + 8],
    radius=10,
    fill=(26, 31, 58, 200),
)
draw.text((x, y), text, fill=(242, 237, 227, 255), font=font)
final = Image.alpha_composite(img, overlay).convert("RGB")
wm_path = OUT_DIR / "slide_01_wm.png"
final.save(wm_path, "PNG", optimize=True)
print(f"  [WM] {wm_path.name} ({W_img}x{H_img})")

print(f"\n[DONE] 输出目录: {OUT_DIR}")