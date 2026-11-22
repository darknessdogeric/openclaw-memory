#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
gen_xhs_6grid_hotel.py — 玉帝视角酒店业深度解读 6 图图文(小红书通用受众版)
- 1080 × 1440 PNG (小红书最佳)
- B166ER V3 Swiss Modern 范式 (燕麦白 + 黑红 + 网格)
- B标: 左上 B166ER / N/6 + 底部红点 ERIC的B166ER出品
- 6 张: 封面 + 5 张核心内容
- 4 类受众通用: 酒店投资人 / 酒店经营者 / 酒管公司 / 单体酒店
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
import subprocess

OUT_DIR = Path(r"C:/Users/ericz/Desktop/小红书产品线/2026十五五酒店业6图-v1.0/XHS-output")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# V3 B166ER Swiss Modern 范式
CSS = """
<style>
:root{
  --bg:#f4f1ec;--bg2:#ffffff;
  --ink:#1a1a1a;--ink2:#4a4a4a;
  --grid:#d6d6d6;--red:#d62828;--blue:#003049;
  --mute:#8a8a8a;--gold:#b08947
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#1a1a1a}
body{font-family:'Inter','Noto Sans SC',sans-serif;background:#1a1a1a;
  display:flex;justify-content:center;align-items:center;min-height:100vh;color:var(--ink)}
.poster{
  width:1080px;min-height:1440px;height:1440px;background:var(--bg);color:var(--ink);
  position:relative;overflow:hidden;
  display:flex;flex-direction:column;
  padding:60px 80px 60px 80px
}
.grid{
  position:absolute;top:0;left:80px;right:80px;bottom:0;
  background-image:linear-gradient(to right,var(--grid) 1px,transparent 1px);
  background-size:76.6px 100%;opacity:.4;pointer-events:none;z-index:1
}
.top{
  height:56px;padding-bottom:20px;border-bottom:2px solid var(--ink);
  display:grid;grid-template-columns:1fr 1fr;align-items:end;
  position:relative;z-index:2
}
.brand{font-family:'IBM Plex Mono',monospace;font-size:16px;font-weight:500;
  letter-spacing:.16em;text-transform:uppercase;color:var(--ink)}
.meta{font-family:'IBM Plex Mono',monospace;font-size:16px;color:var(--mute);
  letter-spacing:.1em;text-align:right}
.main{
  flex:1 1 auto;min-height:0;display:flex;flex-direction:column;position:relative;z-index:2;
  padding-top:24px
}
.bottom{
  height:56px;padding-top:20px;border-top:2px solid var(--ink);
  display:grid;grid-template-columns:1fr auto 1fr;align-items:center;
  position:relative;z-index:2
}
.bottom .left{font-family:'IBM Plex Mono',monospace;font-size:15px;
  color:var(--ink);letter-spacing:.12em;font-weight:500}
.bottom .right{font-family:'IBM Plex Mono',monospace;font-size:15px;
  color:var(--mute);letter-spacing:.1em;text-align:right}
.by{font-family:'Noto Sans SC',sans-serif;font-size:20px;font-weight:700;
  color:var(--ink);letter-spacing:.04em;display:flex;align-items:center;
  gap:12px;justify-self:center}
.by .dot{width:10px;height:10px;background:var(--red);display:inline-block;flex-shrink:0}
.kicker{font-family:'IBM Plex Mono',monospace;font-size:18px;color:var(--red);
  letter-spacing:.32em;text-transform:uppercase;font-weight:600;
  display:flex;align-items:center;gap:14px;margin-bottom:24px}
.kicker::before{content:"";width:48px;height:2px;background:var(--red);display:inline-block}
h1{font-family:'Noto Sans SC','Inter',sans-serif;font-size:110px;font-weight:900;
  line-height:1.02;letter-spacing:-.04em;color:var(--ink);margin-bottom:14px}
h1 em{color:var(--red);font-family:'Cormorant Garamond',serif;font-weight:600;
  font-size:.7em;letter-spacing:-.01em}
h3{font-family:'Noto Sans SC',sans-serif;font-size:24px;font-weight:900;
  color:var(--ink);line-height:1.25;letter-spacing:-.01em;margin-bottom:8px;
  white-space:nowrap;overflow:hidden}
.lede{font-family:'Noto Sans SC',sans-serif;font-size:22px;color:var(--ink2);
  line-height:1.4;max-width:760px;font-weight:400;margin-bottom:20px}
.body{font-family:'Noto Sans SC',sans-serif;font-size:20px;color:var(--ink2);
  line-height:1.6}
.body-sm{font-family:'Noto Sans SC',sans-serif;font-size:18px;color:var(--ink2);
  line-height:1.55}
.num{font-family:'Cormorant Garamond',serif;font-weight:700;line-height:.9;
  letter-spacing:-.04em}
.mono{font-family:'IBM Plex Mono',monospace;letter-spacing:.18em;
  text-transform:uppercase;font-size:13px;color:var(--mute);font-weight:600}
.divider-h{height:2px;background:var(--ink);width:100%}
.divider-v{width:1px;background:var(--grid);height:100%}
</style>
"""

# ============ 6 张内容 ============

PAGES = []

# 01 封面 - 玉帝视角 + 6 不变量
PAGES.append({
    "name": "p01_cover",
    "title": "玉帝视角",
    "title_em": "酒店业 5 年",
    "subtitle_meta": "P01 · 6 IMMUTABLES",
    "kicker": "A · 看懂全貌",
    "body": """
<div class="lede">政策从经济议题升级为国家战略。<br>看清全貌 · 不被噪音带节奏。</div>

<div class="divider-h"></div>

<div style="display:grid;grid-template-columns:1fr 1px 1fr;border-top:none;border-bottom:2px solid var(--ink)">
  <div style="padding:42px 20px 42px 0;border-right:1px solid var(--grid);display:flex;flex-direction:column">
    <div class="mono" style="margin-bottom:14px;color:var(--mute)">不变项 01</div>
    <div class="num" style="font-size:60px;color:var(--red);line-height:.9;letter-spacing:-.04em;margin-bottom:14px">+7.6<span style="font-size:24px;color:var(--mute)">%</span></div>
    <h3 style="font-size:20px">入境人次 5 年 CAGR</h3>
    <p class="body-sm">5 年唯一高确定性赛道</p>
  </div>
  <div style="padding:42px 20px 42px 0;border-right:1px solid var(--grid);display:flex;flex-direction:column">
  </div>
</div>

<div style="display:grid;grid-template-columns:1fr;border-bottom:2px solid var(--ink)">
  <div style="padding:32px 20px;border-right:1px solid var(--grid);display:flex;flex-direction:column">
    <div class="mono" style="margin-bottom:10px;color:var(--red)">不变项 02</div>
    <div class="num" style="font-size:60px;color:var(--ink);line-height:.9;letter-spacing:-.04em;margin-bottom:14px">+10.8<span style="font-size:24px;color:var(--mute)">%</span></div>
    <h3 style="font-size:20px">入境花费 5 年 CAGR</h3>
    <p class="body-sm">消费升级 &gt; 流量升级</p>
  </div>
</div>

<div style="margin-top:24px;display:grid;grid-template-columns:1fr 1px 1fr 1px 1fr 1px 1fr;border-top:2px solid var(--ink);border-bottom:2px solid var(--ink);padding:0">
  <div style="padding:18px 0;text-align:center;border-right:1px solid var(--grid)">
    <div class="num" style="font-size:36px;line-height:1">83<span style="font-size:14px;color:var(--mute)">亿</span></div>
    <div class="mono" style="margin-top:4px;font-size:9px">国内 2030</div>
  </div>
  <div class="divider-v" style="height:80px;align-self:center"></div>
  <div style="padding:18px 0;text-align:center;border-right:1px solid var(--grid)">
    <div class="num" style="font-size:36px;line-height:1">7.7<span style="font-size:14px;color:var(--mute)">万亿</span></div>
    <div class="mono" style="margin-top:4px;font-size:9px">国内花费</div>
  </div>
  <div class="divider-v" style="height:80px;align-self:center"></div>
  <div style="padding:18px 0;text-align:center;border-right:1px solid var(--grid)">
    <div class="num" style="font-size:36px;color:var(--red);line-height:1">1.9<span style="font-size:14px;color:var(--mute)">亿</span></div>
    <div class="mono" style="color:var(--red);margin-top:4px;font-size:9px">2030 入境</div>
  </div>
  <div class="divider-v" style="height:80px;align-self:center"></div>
  <div style="padding:18px 0;text-align:center">
    <div class="num" style="font-size:36px;color:var(--red);line-height:1">$1500<span style="font-size:14px;color:var(--mute)">亿</span></div>
    <div class="mono" style="color:var(--red);margin-top:4px;font-size:9px">入境花费</div>
  </div>
</div>

<div style="margin-top:24px;text-align:center;font-family:'Noto Sans SC',sans-serif;font-size:20px;font-weight:600;color:var(--ink)">
  4 类酒店人适用: <span style="display:inline-block;padding:6px 14px;border:2px solid var(--ink);margin:0 4px;font-weight:700">投资人</span> <span style="display:inline-block;padding:6px 14px;border:2px solid var(--ink);margin:0 4px;font-weight:700">经营者</span> <span style="display:inline-block;padding:6px 14px;border:2px solid var(--ink);margin:0 4px;font-weight:700">酒管</span> <span style="display:inline-block;padding:6px 14px;border:2px solid var(--ink);margin:0 4px;font-weight:700">单体</span>
</div>
""",
    "bottom_left": "玉帝视角 · V3 范式",
    "bottom_right": "2026.07.15 · 全受众",
})

# 02 政策骨架 - 11+4+3+88+3+8+11+9
PAGES.append({
    "name": "p02_skeleton",
    "title": "5 年",
    "title_em": "顶层纲领",
    "subtitle_meta": "P02 · 11 + 4 + 88",
    "kicker": "B · 政策骨架",
    "body": """
<div class="lede">国函〔2026〕61 号。<br>11 个数字线索,完整还原顶层纲领。</div>

<div class="divider-h"></div>

<div style="display:grid;grid-template-columns:repeat(3,1fr);border-top:none;border-bottom:2px solid var(--ink);padding:0">
  <div style="padding:32px 14px 32px 0;text-align:center;border-right:1px solid var(--grid)">
    <div class="num" style="font-size:64px;line-height:1;color:var(--ink)">11</div>
    <div class="mono" style="margin-top:10px;color:var(--mute)">PRINCIPLES</div>
    <p style="font-family:'Noto Sans SC';font-size:14px;font-weight:700;margin-top:8px">根本遵循</p>
  </div>
  <div class="divider-v" style="height:120px;align-self:center"></div>
  <div style="padding:32px 14px;border-right:1px solid var(--grid);text-align:center">
    <div class="num" style="font-size:64px;line-height:1;color:var(--red)">4</div>
    <div class="mono" style="margin-top:10px;color:var(--red)">2030 GOALS</div>
    <p style="font-family:'Noto Sans SC';font-size:14px;font-weight:700;margin-top:8px">量化目标</p>
  </div>
  <div class="divider-v" style="height:120px;align-self:center"></div>
  <div style="padding:32px 0 32px 14px;text-align:center">
    <div class="num" style="font-size:64px;line-height:1;color:var(--red)">3</div>
    <div class="mono" style="margin-top:10px;color:var(--red)">SPATIAL</div>
    <p style="font-family:'Noto Sans SC';font-size:14px;font-weight:700;margin-top:8px">空间布局</p>
  </div>
</div>

<div style="display:grid;grid-template-columns:1fr;border-bottom:2px solid var(--ink);padding:0">
  <div style="padding:32px 0;display:flex;flex-direction:column;align-items:center">
    <div class="num" style="font-size:96px;line-height:1">88</div>
    <div class="mono" style="margin-top:14px">CITIES · 32 枢纽 + 33 重点 + 23 特色</div>
    <p style="font-family:'Noto Sans SC';font-size:14px;font-weight:700;margin-top:8px;color:var(--ink2)">5 年资源向这 88 城倾斜</p>
  </div>
</div>

<div style="display:grid;grid-template-columns:repeat(4,1fr);border-top:2px solid var(--ink);padding:32px 0;border-bottom:2px solid var(--ink)">
  <div style="padding:0 12px;text-align:center;border-right:1px solid var(--grid)">
    <div class="num" style="font-size:36px">3</div>
    <div class="mono" style="margin-top:6px;font-size:10px">动能 智能化/绿色/融合</div>
  </div>
  <div style="padding:0 12px;text-align:center;border-right:1px solid var(--grid)">
    <div class="num" style="font-size:36px">8</div>
    <div class="mono" style="margin-top:6px;font-size:10px">重点任务</div>
  </div>
  <div style="padding:0 12px;text-align:center;border-right:1px solid var(--grid)">
    <div class="num" style="font-size:36px;color:var(--red)">11</div>
    <div class="mono" style="margin-top:6px;color:var(--red);font-size:10px">专项工程</div>
  </div>
  <div style="padding:0 12px;text-align:center">
    <div class="num" style="font-size:36px">9</div>
    <div class="mono" style="margin-top:6px;font-size:10px">保障体系</div>
  </div>
</div>

<div style="margin-top:24px;background:var(--ink);color:#fff;padding:18px 24px;text-align:center">
  <div style="font-family:'Noto Sans SC',sans-serif;font-size:18px;font-weight:900;line-height:1.4">11 个专项工程 = 万亿级政策池<br>主动申报者拿走 50%+</div>
</div>
""",
    "bottom_left": "P02 / 06",
    "bottom_right": "玉帝视角",
})

# 03 4 类酒店人对照 - 麦肯锡 2x2 矩阵图(V7 改进:布局清晰+4 色对比)
PAGES.append({
    "name": "p03_audience",
    "title": "4 类",
    "title_em": "酒店人",
    "subtitle_meta": "P03 · 4 HOTEL PEOPLE · 2x2 MATRIX",
    "kicker": "C · 谁该看 · 麦肯锡矩阵",
    "body": """
<div class="lede">所有酒店人都能读,但动作不同。<br>玉帝视角按 资源 + 风险 切成 4 象限。</div>

<!-- Y 轴标题 (顶部) -->
<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:6px">
  <div style="text-align:right;padding-right:18px">
    <div style="font-family:'IBM Plex Mono';font-size:11px;color:var(--mute);letter-spacing:.32em;text-transform:uppercase;font-weight:700">资源充足</div>
  </div>
  <div style="text-align:left;padding-left:18px">
    <div style="font-family:'IBM Plex Mono';font-size:11px;color:var(--mute);letter-spacing:.32em;text-transform:uppercase;font-weight:700">资源有限</div>
  </div>
</div>

<!-- 象限标签 -->
<div style="display:grid;grid-template-columns:1fr 1fr;gap:0;margin-bottom:4px">
  <div style="text-align:right;padding-right:14px">
    <div style="font-family:'IBM Plex Mono';font-size:10px;color:var(--red);letter-spacing:.18em;font-weight:600;text-transform:uppercase">高 决 策 风 险 ⟵</div>
  </div>
  <div style="text-align:left;padding-left:14px">
    <div style="font-family:'IBM Plex Mono';font-size:10px;color:var(--blue);letter-spacing:.18em;font-weight:600;text-transform:uppercase">⟶ 低 决 策 风 险</div>
  </div>
</div>

<!-- 4 象限主图 -->
<div style="display:grid;grid-template-columns:1fr 1px 1fr;gap:0;border:2px solid var(--ink)">
  <!-- 第 1 象限: 资源充足 + 高风险 - 酒管 -->
  <div style="padding:36px 28px;background:var(--bg2);border-right:1px solid var(--ink);display:flex;flex-direction:column;align-items:flex-start;min-height:280px">
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:14px;width:100%">
      <div class="num" style="font-size:80px;color:var(--ink);line-height:.85;letter-spacing:-.04em">01</div>
      <div style="background:var(--ink);color:#fff;font-family:'IBM Plex Mono';font-size:12px;padding:6px 12px;letter-spacing:.2em;font-weight:700">集团公司</div>
    </div>
    <h3 style="font-size:28px;font-weight:900;line-height:1.2;margin-bottom:14px">酒管公司 / 集团</h3>
    <div style="font-family:'IBM Plex Mono';font-size:11px;color:var(--mute);letter-spacing:.18em;margin-bottom:14px;text-transform:uppercase;font-weight:600">FOCUS · 6 战略 + 4 调整</div>
    <div style="font-family:'Noto Sans SC';font-size:17px;color:var(--ink);font-weight:700;line-height:1.5;margin-top:auto">
      ▲ 品牌矩阵<br>
      ▲ 集群化扩张<br>
      ▲ IP 轻资产
    </div>
  </div>
  <!-- 第 2 象限: 资源充足 + 低风险 - 投资人 -->
  <div style="padding:36px 28px;background:var(--bg2);display:flex;flex-direction:column;align-items:flex-start;min-height:280px">
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:14px;width:100%">
      <div class="num" style="font-size:80px;color:var(--gold);line-height:.85;letter-spacing:-.04em">02</div>
      <div style="background:var(--gold);color:#fff;font-family:'IBM Plex Mono';font-size:12px;padding:6px 12px;letter-spacing:.2em;font-weight:700">资本方</div>
    </div>
    <h3 style="font-size:28px;font-weight:900;line-height:1.2;margin-bottom:14px">酒店投资人</h3>
    <div style="font-family:'IBM Plex Mono';font-size:11px;color:var(--mute);letter-spacing:.18em;margin-bottom:14px;text-transform:uppercase;font-weight:600">FOCUS · 10 类型 + 6 原则</div>
    <div style="font-family:'Noto Sans SC';font-size:17px;color:var(--ink);font-weight:700;line-height:1.5;margin-top:auto">
      ▲ 5 年回报路径<br>
      ▲ 资本敏感度<br>
      ▲ 88 城市对冲
    </div>
  </div>
</div>

<div style="display:grid;grid-template-columns:1fr 1px 1fr;gap:0;border:2px solid var(--ink);border-top:none">
  <!-- 第 3 象限: 资源有限 + 高风险 - 单体 -->
  <div style="padding:36px 28px;background:var(--bg2);border-right:1px solid var(--ink);display:flex;flex-direction:column;align-items:flex-start;min-height:280px">
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:14px;width:100%">
      <div class="num" style="font-size:80px;color:var(--red);line-height:.85;letter-spacing:-.04em">03</div>
      <div style="background:var(--red);color:#fff;font-family:'IBM Plex Mono';font-size:12px;padding:6px 12px;letter-spacing:.2em;font-weight:700">风险高</div>
    </div>
    <h3 style="font-size:28px;font-weight:900;line-height:1.2;margin-bottom:14px">单体酒店 (差异)</h3>
    <div style="font-family:'IBM Plex Mono';font-size:11px;color:var(--mute);letter-spacing:.18em;margin-bottom:14px;text-transform:uppercase;font-weight:600">FOCUS · 8 突围 + 5 微行动</div>
    <div style="font-family:'Noto Sans SC';font-size:17px;color:var(--ink);font-weight:700;line-height:1.5;margin-top:auto">
      ▲ 8 突围(差异化)<br>
      ▲ 5 微行动(小预算)<br>
      ▲ 申报能力 = 隐形回报
    </div>
  </div>
  <!-- 第 4 象限: 资源有限 + 低风险 - 经营者 -->
  <div style="padding:36px 28px;background:var(--bg2);display:flex;flex-direction:column;align-items:flex-start;min-height:280px">
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:14px;width:100%">
      <div class="num" style="font-size:80px;color:var(--blue);line-height:.85;letter-spacing:-.04em">04</div>
      <div style="background:var(--blue);color:#fff;font-family:'IBM Plex Mono';font-size:12px;padding:6px 12px;letter-spacing:.2em;font-weight:700">日常稳</div>
    </div>
    <h3 style="font-size:28px;font-weight:900;line-height:1.2;margin-bottom:14px">酒店经营者</h3>
    <div style="font-family:'IBM Plex Mono';font-size:11px;color:var(--mute);letter-spacing:.18em;margin-bottom:14px;text-transform:uppercase;font-weight:600">FOCUS · 4 调整 + 9 动作</div>
    <div style="font-family:'Noto Sans SC';font-size:17px;color:var(--ink);font-weight:700;line-height:1.5;margin-top:auto">
      ▲ 卖体验而非房间<br>
      ▲ AI 改造(2027 关键)<br>
      ▲ 私域沉淀
    </div>
  </div>
</div>

<!-- 对角说明 -->
<div style="margin-top:14px;text-align:center;padding:8px;font-family:'IBM Plex Mono';font-size:11px;color:var(--mute);letter-spacing:.18em;text-transform:uppercase">
  ✦ 对角策略 → 高资源高风险选 战略扩张 ↔ 低资源低风险选 日常运营 ✦
</div>
""",
    "bottom_left": "P03 / 06 · 2x2 矩阵",
    "bottom_right": "玉帝视角",
})

# 04 关键数据对比 2024 vs 2030
PAGES.append({
    "name": "p04_data",
    "title": "数据",
    "title_em": "对比",
    "subtitle_meta": "P04 · 4 METRICS · 5 YEARS",
    "kicker": "D · 数字趋势",
    "body": """
<div class="lede">2024 → 2030 的 5 年趋势对比。<br>入境游 CAGR 10.8% — 5 年最高增速。</div>

<div class="divider-h"></div>

<table style="width:100%;border-collapse:collapse">
<thead>
<tr style="border-bottom:2px solid var(--ink);background:var(--bg)">
  <th class="mono" style="text-align:left;padding:14px 8px;font-size:12px;color:var(--mute);font-weight:600">指标</th>
  <th class="mono" style="text-align:center;padding:14px 8px;font-size:12px;color:var(--mute);font-weight:600">2024</th>
  <th class="mono" style="text-align:center;padding:14px 8px;font-size:12px;color:var(--red);font-weight:600">2030</th>
  <th class="mono" style="text-align:center;padding:14px 8px;font-size:12px;color:var(--mute);font-weight:600">CAGR</th>
</tr>
</thead>
<tbody>
<tr style="border-bottom:1px solid var(--grid)">
  <td style="padding:18px 8px;font-family:'Noto Sans SC';font-size:18px;font-weight:900;color:var(--ink)">国内人次</td>
  <td class="num" style="text-align:center;padding:18px 8px;font-size:24px;color:var(--ink2)">~60 亿</td>
  <td class="num" style="text-align:center;padding:18px 8px;font-size:26px;color:var(--ink);font-weight:700">83 亿</td>
  <td class="num" style="text-align:center;padding:18px 8px;font-size:24px;color:var(--gold);font-weight:700">+6.7%</td>
</tr>
<tr style="border-bottom:1px solid var(--grid)">
  <td style="padding:18px 8px;font-family:'Noto Sans SC';font-size:18px;font-weight:900;color:var(--ink)">国内花费</td>
  <td class="num" style="text-align:center;padding:18px 8px;font-size:24px;color:var(--ink2)">~5.7 万亿</td>
  <td class="num" style="text-align:center;padding:18px 8px;font-size:26px;color:var(--ink);font-weight:700">7.7 万亿</td>
  <td class="num" style="text-align:center;padding:18px 8px;font-size:24px;color:var(--gold);font-weight:700">+6.2%</td>
</tr>
<tr style="border-bottom:1px solid var(--grid)">
  <td style="padding:18px 8px;font-family:'Noto Sans SC';font-size:18px;font-weight:900;color:var(--ink)">入境人次</td>
  <td class="num" style="text-align:center;padding:18px 8px;font-size:24px;color:var(--ink2)">~1.32 亿</td>
  <td class="num" style="text-align:center;padding:18px 8px;font-size:26px;color:var(--red);font-weight:700">1.9 亿</td>
  <td class="num" style="text-align:center;padding:18px 8px;font-size:24px;color:var(--red);font-weight:700">+7.6%</td>
</tr>
<tr>
  <td style="padding:18px 8px;font-family:'Noto Sans SC';font-size:18px;font-weight:900;color:var(--red)">入境花费</td>
  <td class="num" style="text-align:center;padding:18px 8px;font-size:24px;color:var(--ink2)">~$800 亿</td>
  <td class="num" style="text-align:center;padding:18px 8px;font-size:26px;color:var(--red);font-weight:700">$1500 亿</td>
  <td class="num" style="text-align:center;padding:18px 8px;font-size:26px;color:var(--red);font-weight:700">+10.8%</td>
</tr>
</tbody>
</table>

<div style="margin-top:20px;background:var(--ink);color:#fff;padding:18px 24px;text-align:center">
  <div style="font-family:'Noto Sans SC',sans-serif;font-size:18px;font-weight:900;line-height:1.4">入境花费 CAGR <em style="color:var(--red);font-family:'Cormorant Garamond',serif;font-size:1.2em">10.8%</em><br>= 5 年最高增速</div>
</div>
""",
    "bottom_left": "P04 / 06",
    "bottom_right": "数据 · 文旅部 / 国家移民管理局",
})

# 05 9 经营动作 + 4 调整 (核心动作清单)
PAGES.append({
    "name": "p05_actions",
    "title": "9 动作",
    "title_em": "立即可做",
    "subtitle_meta": "P05 · 9 ACTIONS",
    "kicker": "E · 行动清单",
    "body": """
<div class="lede">玉帝视角:看清全貌是不够的,要立刻动。<br>9 个低成本/高回报的动作,分阶段做。</div>

<div class="divider-h"></div>

<div style="display:grid;grid-template-columns:1fr 1px 1fr 1px 1fr;border-top:none;border-bottom:2px solid var(--ink)">
  <div style="padding:20px 12px 20px 0;border-right:1px solid var(--grid);display:flex;flex-direction:column;gap:6px">
    <div style="display:flex;align-items:flex-end;gap:8px">
      <div class="num" style="font-size:32px;color:var(--red);line-height:1">01</div>
      <div class="mono" style="color:var(--mute);font-size:9px;letter-spacing:.15em">基础</div>
    </div>
    <h3 style="font-size:18px">多语官网</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.4">EN / JP / KO<br>5-30K</p>
  </div>
  <div class="divider-v"></div>
  <div style="padding:20px 12px;border-right:1px solid var(--grid);display:flex;flex-direction:column;gap:6px">
    <div style="display:flex;align-items:flex-end;gap:8px">
      <div class="num" style="font-size:32px;color:var(--red);line-height:1">02</div>
      <div class="mono" style="color:var(--mute);font-size:9px;letter-spacing:.15em">基础</div>
    </div>
    <h3 style="font-size:18px">国际 OTA</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.4">Booking/Agoda<br>5-15% 佣金</p>
  </div>
  <div class="divider-v"></div>
  <div style="padding:20px 12px 20px 0;border-right:0;display:flex;flex-direction:column;gap:6px">
    <div style="display:flex;align-items:flex-end;gap:8px">
      <div class="num" style="font-size:32px;color:var(--red);line-height:1">03</div>
      <div class="mono" style="color:var(--mute);font-size:9px;letter-spacing:.15em">基础</div>
    </div>
    <h3 style="font-size:18px">支付退税</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.4">Visa/Master<br>+ 即买即退</p>
  </div>
</div>

<div style="display:grid;grid-template-columns:1fr 1px 1fr 1px 1fr;border-top:none;border-bottom:2px solid var(--ink)">
  <div style="padding:20px 12px 20px 0;border-right:1px solid var(--grid);display:flex;flex-direction:column;gap:6px">
    <div style="display:flex;align-items:flex-end;gap:8px">
      <div class="num" style="font-size:32px;color:var(--ink);line-height:1">04</div>
      <div class="mono" style="color:var(--mute);font-size:9px;letter-spacing:.15em">中级</div>
    </div>
    <h3 style="font-size:18px">私域沉淀</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.4">微信/小程序<br>复购 +25%</p>
  </div>
  <div class="divider-v"></div>
  <div style="padding:20px 12px;border-right:1px solid var(--grid);display:flex;flex-direction:column;gap:6px">
    <div style="display:flex;align-items:flex-end;gap:8px">
      <div class="num" style="font-size:32px;color:var(--ink);line-height:1">05</div>
      <div class="mono" style="color:var(--mute);font-size:9px;letter-spacing:.15em">中级</div>
    </div>
    <h3 style="font-size:18px">AI 智能化</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.4">客服+运营+营销<br>人力 -25%</p>
  </div>
  <div class="divider-v"></div>
  <div style="padding:20px 12px 20px 0;border-right:0;display:flex;flex-direction:column;gap:6px">
    <div style="display:flex;align-items:flex-end;gap:8px">
      <div class="num" style="font-size:32px;color:var(--red);line-height:1">06</div>
      <div class="mono" style="color:var(--red);font-size:9px;letter-spacing:.15em">高级</div>
    </div>
    <h3 style="font-size:18px">政策申报</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.4">专项基金<br>5-500 万</p>
  </div>
</div>

<div style="display:grid;grid-template-columns:1fr 1px 1fr 1px 1fr;border-top:none;border-bottom:2px solid var(--ink)">
  <div style="padding:20px 12px 20px 0;border-right:1px solid var(--grid);display:flex;flex-direction:column;gap:6px">
    <div style="display:flex;align-items:flex-end;gap:8px">
      <div class="num" style="font-size:32px;color:var(--ink);line-height:1">07</div>
      <div class="mono" style="color:var(--mute);font-size:9px;letter-spacing:.15em">中级</div>
    </div>
    <h3 style="font-size:18px">外文导览</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.4">标识 + 菜单<br>满意度 +20%</p>
  </div>
  <div class="divider-v"></div>
  <div style="padding:20px 12px;border-right:1px solid var(--grid);display:flex;flex-direction:column;gap:6px">
    <div style="display:flex;align-items:flex-end;gap:8px">
      <div class="num" style="font-size:32px;color:var(--ink);line-height:1">08</div>
      <div class="mono" style="color:var(--mute);font-size:9px;letter-spacing:.15em">高级</div>
    </div>
    <h3 style="font-size:18px">差异化主题</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.4">文化/精品/目的地<br>ADR +15-30%</p>
  </div>
  <div class="divider-v"></div>
  <div style="padding:20px 12px 20px 0;border-right:0;display:flex;flex-direction:column;gap:6px">
    <div style="display:flex;align-items:flex-end;gap:8px">
      <div class="num" style="font-size:32px;color:var(--ink);line-height:1">09</div>
      <div class="mono" style="color:var(--mute);font-size:9px;letter-spacing:.15em">高级</div>
    </div>
    <h3 style="font-size:18px">联盟/集群</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.4">行业协会+城市联盟<br>政策对接</p>
  </div>
</div>

<div style="margin-top:18px;text-align:center;background:var(--ink);color:#fff;padding:14px 24px">
  <div style="font-family:'Noto Sans SC',sans-serif;font-size:18px;font-weight:900;line-height:1.4">基础 3 动作立即做 · 中级 3 季度推 · 高级 3 年节奏</div>
</div>
""",
    "bottom_left": "P05 / 06",
    "bottom_right": "玉帝视角",
})

# 06 终 - 5 大盲区警示 + 一句话
PAGES.append({
    "name": "p06_closing",
    "title": "5 盲区",
    "title_em": "与总结",
    "subtitle_meta": "P06 · 5 BLIND SPOTS",
    "kicker": "F · 玉帝忠告",
    "body": """
<div class="lede">看清全貌是基础,不踩坑是关键。<br>玉帝视角 5 大盲区警示。</div>

<div class="divider-h"></div>

<div style="display:grid;grid-template-columns:auto 1fr;gap:18px;padding:14px 0;border-bottom:1px solid var(--grid);align-items:start">
  <div class="num" style="font-size:36px;color:var(--red);min-width:50px;line-height:1">01</div>
  <div>
    <h3 style="font-size:18px;margin-bottom:4px">不要把赌注压在政策上</h3>
    <p style="font-family:'Noto Sans SC';font-size:15px;color:var(--ink2);line-height:1.5">多数文旅基金落地率 &lt; 60%。政策是加分项,不是生存项。</p>
  </div>
</div>

<div style="display:grid;grid-template-columns:auto 1fr;gap:18px;padding:14px 0;border-bottom:1px solid var(--grid);align-items:start">
  <div class="num" style="font-size:36px;color:var(--red);min-width:50px;line-height:1">02</div>
  <div>
    <h3 style="font-size:18px;margin-bottom:4px">不要忽视"老兵价值"</h3>
    <p style="font-family:'Noto Sans SC';font-size:15px;color:var(--ink2);line-height:1.5">AI 不能替代熟手店长,数据不能替代客户关系。</p>
  </div>
</div>

<div style="display:grid;grid-template-columns:auto 1fr;gap:18px;padding:14px 0;border-bottom:1px solid var(--grid);align-items:start">
  <div class="num" style="font-size:36px;color:var(--red);min-width:50px;line-height:1">03</div>
  <div>
    <h3 style="font-size:18px;margin-bottom:4px">不要把"政策红利"当"市场红利"</h3>
    <p style="font-family:'Noto Sans SC';font-size:15px;color:var(--ink2);line-height:1.5">政策创造 5 年窗口,不创造 10 年基本面。需要长期能力做底。</p>
  </div>
</div>

<div style="display:grid;grid-template-columns:auto 1fr;gap:18px;padding:14px 0;border-bottom:1px solid var(--grid);align-items:start">
  <div class="num" style="font-size:36px;color:var(--red);min-width:50px;line-height:1">04</div>
  <div>
    <h3 style="font-size:18px;margin-bottom:4px">不要让"声音"取代"判断"</h3>
    <p style="font-family:'Noto Sans SC';font-size:15px;color:var(--ink2);line-height:1.5">一致预期往往是滞后指标。反共识机会反而更好。</p>
  </div>
</div>

<div style="display:grid;grid-template-columns:auto 1fr;gap:18px;padding:14px 0;border-bottom:2px solid var(--ink);align-items:start">
  <div class="num" style="font-size:36px;color:var(--red);min-width:50px;line-height:1">05</div>
  <div>
    <h3 style="font-size:18px;margin-bottom:4px">不要把 5 年规划当"倒计时"</h3>
    <p style="font-family:'Noto Sans SC';font-size:15px;color:var(--ink2);line-height:1.5">把 5 年当成"节奏",而非"倒计时"。每年评估,每季度调整。</p>
  </div>
</div>

<div style="margin-top:24px;background:var(--red);color:#fff;padding:24px 28px;text-align:center">
  <div class="mono" style="font-size:12px;letter-spacing:.32em;margin-bottom:12px;opacity:.85">玉帝视角 · 一句话</div>
  <div style="font-family:'Noto Sans SC',sans-serif;font-size:24px;font-weight:900;line-height:1.4">看清全貌 · 不被噪音带节奏</div>
</div>
""",
    "bottom_left": "P06 / 06 · 完结",
    "bottom_right": "2026.07.15 · 玉帝视角",
})

# ============ HTML 生成 ============

def build_html(page, idx, total):
    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Noto+Serif+SC:wght@400;600;700;900&family=Inter:wght@200;300;400;500;700;900&family=Noto+Sans+SC:wght@300;400;500;700;900&family=IBM+Plex+Mono:wght@400;500;700&display=swap" rel="stylesheet">{CSS}</head><body>
<div class="poster">
  <div class="grid"></div>
  <div class="top">
    <div class="brand">B166ER / {idx:02d} / {total}</div>
    <div class="meta">{page['subtitle_meta']}</div>
  </div>
  <div class="main">
    <div class="kicker">{page['kicker']}</div>
    <h1>{page['title']}<br><em>{page['title_em']}</em></h1>
    {page['body']}
  </div>
  <div class="bottom">
    <div class="left">{page['bottom_left']}</div>
    <div class="by"><span class="dot"></span>ERIC的B166ER出品</div>
    <div class="right">{page['bottom_right']}</div>
  </div>
</div>
</body></html>"""


# ============ 主流程 ============

if __name__ == "__main__":
    print(f"开始生成 {len(PAGES)} 张 (6 图小红书 V3 范式)...")

    for i, page in enumerate(PAGES, 1):
        html = build_html(page, i, len(PAGES))
        html_path = OUT_DIR / f"{i:02d}_{page['name']}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  ✅ HTML [{i:02d}/{len(PAGES):02d}] {html_path.name}")

    print(f"\n✅ HTML 写完 → {OUT_DIR}")
