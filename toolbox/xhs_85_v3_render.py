#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
xhs_85_v3_render.py — 民政部85号令 × 酒店行业 6图 (V3 Swiss Modern 范式)
- 1080 × 1440 PNG (3:4)
- B166ER V3 Swiss Modern 范式: 燕麦白 + 黑红 + 网格 + IBM Plex Mono
- B标: 左上 B166ER / N/6 + 底部红点 ERIC的B166ER出品
- 沿用 gen_xhs_6grid_hotel.py 全部 CSS + 布局规范
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
import subprocess

# 沿用 gen_xhs_6grid_hotel.py 的 OUT_DIR 风格
OUT_DIR = Path(r"D:\B166ER-OpenClaw\workspace\output\xhs_85_2026-08-01_v3")
OUT_DIR.mkdir(parents=True, exist_ok=True)

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# ===== V3 Swiss Modern CSS (与 gen_xhs_6grid_hotel.py 完全一致) =====
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

# ============ 6 张内容（85号令主题） ============

PAGES = []

# 01 封面 - 85号令 + 4禁1禁 + 12个月
PAGES.append({
    "name": "p01_cover",
    "title": "85号令",
    "title_em": "今天施行",
    "subtitle_meta": "P01 · 4 + 1 + 12 · TODAY",
    "kicker": "A · 看懂全貌",
    "body": """
<div class="lede">《社会团体分支机构、代表机构管理办法》<br>酒店行业的"挂靠型智库"时代,今天终止。</div>

<div class="divider-h"></div>

<div style="display:grid;grid-template-columns:1fr 1px 1fr 1px 1fr;border-top:none;border-bottom:2px solid var(--ink)">
  <div style="padding:28px 16px 28px 0;border-right:1px solid var(--grid);display:flex;flex-direction:column;align-items:flex-start">
    <div class="mono" style="margin-bottom:10px;color:var(--mute);font-size:11px">禁设 · 4 类</div>
    <div class="num" style="font-size:64px;color:var(--red);line-height:.9;letter-spacing:-.04em;margin-bottom:10px">4</div>
    <h3 style="font-size:18px;line-height:1.2">分支机构禁止</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.4;margin-top:6px">地域性 / 宗亲 / 会员重合 / 业务重叠</p>
  </div>
  <div class="divider-v" style="height:140px;align-self:center"></div>
  <div style="padding:28px 16px;border-right:1px solid var(--grid);display:flex;flex-direction:column;align-items:flex-start">
    <div class="mono" style="margin-bottom:10px;color:var(--red);font-size:11px">禁称 · 5 类</div>
    <div class="num" style="font-size:64px;color:var(--ink);line-height:.9;letter-spacing:-.04em;margin-bottom:10px">5</div>
    <h3 style="font-size:18px;line-height:1.2">命名禁止</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.4;margin-top:6px">中心 / 联盟 / 研究会 / 促进会 / 研究院</p>
  </div>
  <div class="divider-v" style="height:140px;align-self:center"></div>
  <div style="padding:28px 0 28px 16px;display:flex;flex-direction:column;align-items:flex-start">
    <div class="mono" style="margin-bottom:10px;color:var(--mute);font-size:11px">节奏 · 12 月</div>
    <div class="num" style="font-size:64px;color:var(--ink);line-height:.9;letter-spacing:-.04em;margin-bottom:10px">12</div>
    <h3 style="font-size:18px;line-height:1.2">过渡期</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.4;margin-top:6px">截止 2027.08.01<br>全部合规</p>
  </div>
</div>

<div style="margin-top:18px;background:var(--ink);color:#fff;padding:20px 24px;text-align:center">
  <div style="font-family:'Noto Sans SC',sans-serif;font-size:20px;font-weight:900;line-height:1.4">4 类酒店人适用<br><span style="font-size:14px;font-weight:500;letter-spacing:.08em;margin-top:6px;display:inline-block">协会 · 酒店集团 · 智库 · 投资人</span></div>
</div>
""",
    "bottom_left": "玉帝视角 · V3 范式",
    "bottom_right": "2026.08.01 · 4 类酒店人",
})

# 02 政策骨架 - 4禁 + 5禁称 + 5允许 + 12月
PAGES.append({
    "name": "p02_skeleton",
    "title": "骨架",
    "title_em": "完整条款",
    "subtitle_meta": "P02 · 4 + 5 + 5 + 12",
    "kicker": "B · 政策骨架",
    "body": """
<div class="lede">85 号令核心条款 4 维拆解。<br>禁设 · 禁称 · 允许 · 节奏,一项不漏。</div>

<div class="divider-h"></div>

<!-- 4 类禁设 -->
<div style="display:grid;grid-template-columns:repeat(4,1fr);border-top:none;border-bottom:2px solid var(--ink);padding:0">
  <div style="padding:24px 8px 24px 0;text-align:center;border-right:1px solid var(--grid)">
    <div class="num" style="font-size:48px;line-height:1;color:var(--red)">4</div>
    <div class="mono" style="margin-top:8px;color:var(--red);font-size:9px">禁设类</div>
    <p style="font-family:'Noto Sans SC';font-size:12px;font-weight:700;margin-top:6px">分支机构</p>
  </div>
  <div class="divider-v" style="height:100px;align-self:center"></div>
  <div style="padding:24px 8px 24px 0;text-align:center;border-right:1px solid var(--grid)">
    <div class="num" style="font-size:48px;line-height:1;color:var(--red)">5</div>
    <div class="mono" style="margin-top:8px;color:var(--red);font-size:9px">禁称类</div>
    <p style="font-family:'Noto Sans SC';font-size:12px;font-weight:700;margin-top:6px">命名禁用</p>
  </div>
  <div class="divider-v" style="height:100px;align-self:center"></div>
  <div style="padding:24px 0 24px 0;text-align:center;border-right:1px solid var(--grid)">
    <div class="num" style="font-size:48px;line-height:1;color:var(--ink)">5</div>
    <div class="mono" style="margin-top:8px;color:var(--ink);font-size:9px">允许类</div>
    <p style="font-family:'Noto Sans SC';font-size:12px;font-weight:700;margin-top:6px">合规命名</p>
  </div>
  <div class="divider-v" style="height:100px;align-self:center"></div>
  <div style="padding:24px 0 24px 0;text-align:center">
    <div class="num" style="font-size:48px;line-height:1;color:var(--ink)">12</div>
    <div class="mono" style="margin-top:8px;color:var(--ink);font-size:9px">MONTHS</div>
    <p style="font-family:'Noto Sans SC';font-size:12px;font-weight:700;margin-top:6px">整改过渡</p>
  </div>
</div>

<!-- 详细列表 -->
<div style="margin-top:16px;display:grid;grid-template-columns:1fr 1fr;gap:14px">

  <div style="background:var(--bg2);padding:14px 18px;border-left:4px solid var(--red)">
    <div class="mono" style="font-size:10px;color:var(--red);margin-bottom:8px">❌ 禁设 · 4 类分支机构</div>
    <p style="font-family:'Noto Sans SC';font-size:14px;line-height:1.65;color:var(--ink);font-weight:500">
      地域性 · 姓氏宗亲 ·<br>会员明显重合 ·<br>名称/业务高度相似
    </p>
  </div>

  <div style="background:var(--bg2);padding:14px 18px;border-left:4px solid var(--red)">
    <div class="mono" style="font-size:10px;color:var(--red);margin-bottom:8px">❌ 禁称 · 5 类命名</div>
    <p style="font-family:'Noto Sans SC';font-size:14px;line-height:1.65;color:var(--ink);font-weight:500">
      中心 · 联盟 · 研究会 ·<br>促进会 · 研究院
    </p>
  </div>

  <div style="background:var(--bg2);padding:14px 18px;border-left:4px solid var(--ink)">
    <div class="mono" style="font-size:10px;color:var(--ink);margin-bottom:8px">✅ 允许 · 5 类合规命名</div>
    <p style="font-family:'Noto Sans SC';font-size:14px;line-height:1.65;color:var(--ink);font-weight:500">
      分会 · 专业委员会 ·<br>工作委员会 ·<br>专家委员会 · 技术委员会
    </p>
  </div>

  <div style="background:var(--bg2);padding:14px 18px;border-left:4px solid var(--ink)">
    <div class="mono" style="font-size:10px;color:var(--ink);margin-bottom:8px">⏰ 节奏 · 12 个月</div>
    <p style="font-family:'Noto Sans SC';font-size:14px;line-height:1.65;color:var(--ink);font-weight:500">
      施行 2026.08.01<br>截止 2027.08.01<br>全面合规
    </p>
  </div>

</div>

<div style="margin-top:18px;background:var(--ink);color:#fff;padding:16px 24px;text-align:center">
  <div style="font-family:'Noto Sans SC',sans-serif;font-size:18px;font-weight:900;line-height:1.4">中国 / 中华 / 全国 / 国家 字样 同样禁用<br>分支机构不能开设银行账户</div>
</div>
""",
    "bottom_left": "P02 / 06",
    "bottom_right": "玉帝视角",
})

# 03 4 类酒店人对照 - 麦肯锡 2x2 矩阵
PAGES.append({
    "name": "p03_audience",
    "title": "4 类",
    "title_em": "酒店人",
    "subtitle_meta": "P03 · 4 HOTEL PEOPLE · 2x2 MATRIX",
    "kicker": "C · 谁该看 · 麦肯锡矩阵",
    "body": """
<div class="lede">所有酒店人都能读,但动作不同。<br>玉帝视角按 紧迫度 + 资源 切成 4 类。</div>

<!-- 4 行 1 列布局 (避免象限高度不平衡) -->
<div style="display:flex;flex-direction:column;border:2px solid var(--ink)">
  <!-- 01 协会负责人 -->
  <div style="padding:18px 24px;background:var(--bg2);border-bottom:1px solid var(--ink);display:grid;grid-template-columns:auto 1fr;gap:24px;align-items:start">
    <div style="display:flex;flex-direction:column;align-items:center;gap:6px;min-width:120px">
      <div class="num" style="font-size:56px;color:var(--ink);line-height:.85;letter-spacing:-.04em">01</div>
      <div style="background:var(--ink);color:#fff;font-family:'IBM Plex Mono';font-size:11px;padding:4px 10px;letter-spacing:.2em;font-weight:700;white-space:nowrap">立刻行动</div>
    </div>
    <div>
      <h3 style="font-size:22px;font-weight:900;line-height:1.15;margin-bottom:6px">协会负责人</h3>
      <div style="font-family:'IBM Plex Mono';font-size:10px;color:var(--mute);letter-spacing:.16em;margin-bottom:10px;text-transform:uppercase;font-weight:600">FOCUS · 摸底 + 方案 + 章程</div>
      <div style="font-family:'Noto Sans SC';font-size:14px;color:var(--ink);font-weight:700;line-height:1.5">▲ 分支机构清单 &nbsp; ▲ 改名/撤销/独立法人化 &nbsp; ▲ 12 个月硬约束</div>
    </div>
  </div>
  <!-- 02 投资人 -->
  <div style="padding:18px 24px;background:var(--bg2);border-bottom:1px solid var(--ink);display:grid;grid-template-columns:auto 1fr;gap:24px;align-items:start">
    <div style="display:flex;flex-direction:column;align-items:center;gap:6px;min-width:120px">
      <div class="num" style="font-size:56px;color:var(--gold);line-height:.85;letter-spacing:-.04em">02</div>
      <div style="background:var(--gold);color:#fff;font-family:'IBM Plex Mono';font-size:11px;padding:4px 10px;letter-spacing:.2em;font-weight:700;white-space:nowrap">抄底机会</div>
    </div>
    <div>
      <h3 style="font-size:22px;font-weight:900;line-height:1.15;margin-bottom:6px">投资人</h3>
      <div style="font-family:'IBM Plex Mono';font-size:10px;color:var(--mute);letter-spacing:.16em;margin-bottom:10px;text-transform:uppercase;font-weight:600">FOCUS · 资产收购 + 牌照</div>
      <div style="font-family:'Noto Sans SC';font-size:14px;color:var(--ink);font-weight:700;line-height:1.5">▲ 野鸡 IP / 数据 &nbsp; ▲ 12 个月窗口期 &nbsp; ▲ 话语权重排</div>
    </div>
  </div>
  <!-- 03 酒店集团 -->
  <div style="padding:18px 24px;background:var(--bg2);border-bottom:1px solid var(--ink);display:grid;grid-template-columns:auto 1fr;gap:24px;align-items:start">
    <div style="display:flex;flex-direction:column;align-items:center;gap:6px;min-width:120px">
      <div class="num" style="font-size:56px;color:var(--red);line-height:.85;letter-spacing:-.04em">03</div>
      <div style="background:var(--red);color:#fff;font-family:'IBM Plex Mono';font-size:11px;padding:4px 10px;letter-spacing:.2em;font-weight:700;white-space:nowrap">必须评估</div>
    </div>
    <div>
      <h3 style="font-size:22px;font-weight:900;line-height:1.15;margin-bottom:6px">酒店集团</h3>
      <div style="font-family:'IBM Plex Mono';font-size:10px;color:var(--mute);letter-spacing:.16em;margin-bottom:10px;text-transform:uppercase;font-weight:600">FOCUS · 冠名研究 + 合规</div>
      <div style="font-family:'Noto Sans SC';font-size:14px;color:var(--ink);font-weight:700;line-height:1.5">▲ 冠名清退 &nbsp; ▲ 品牌瘦下来 &nbsp; ▲ 合规成本前置</div>
    </div>
  </div>
  <!-- 04 行业智库 -->
  <div style="padding:18px 24px;background:var(--bg2);display:grid;grid-template-columns:auto 1fr;gap:24px;align-items:start">
    <div style="display:flex;flex-direction:column;align-items:center;gap:6px;min-width:120px">
      <div class="num" style="font-size:56px;color:var(--blue);line-height:.85;letter-spacing:-.04em">04</div>
      <div style="background:var(--blue);color:#fff;font-family:'IBM Plex Mono';font-size:11px;padding:4px 10px;letter-spacing:.2em;font-weight:700;white-space:nowrap">路径重估</div>
    </div>
    <div>
      <h3 style="font-size:22px;font-weight:900;line-height:1.15;margin-bottom:6px">行业智库</h3>
      <div style="font-family:'IBM Plex Mono';font-size:10px;color:var(--mute);letter-spacing:.16em;margin-bottom:10px;text-transform:uppercase;font-weight:600">FOCUS · 改名 / 独立 / 退出</div>
      <div style="font-family:'Noto Sans SC';font-size:14px;color:var(--ink);font-weight:700;line-height:1.5">▲ 4 路径选 1 &nbsp; ▲ 头部集中度↑ &nbsp; ▲ 议价上行</div>
    </div>
  </div>
</div>
""",
    "bottom_left": "P03 / 06 · 2x2 矩阵",
    "bottom_right": "玉帝视角",
})

# 04 12个月关键数据对比
PAGES.append({
    "name": "p04_data",
    "title": "数据",
    "title_em": "对比",
    "subtitle_meta": "P04 · 4 METRICS · 12 MONTHS",
    "kicker": "D · 数字趋势",
    "body": """
<div class="lede">今天 → 12 个月后的 4 个关键对比。<br>行业研究供给收缩是基线情景。</div>

<div class="divider-h"></div>

<table style="width:100%;border-collapse:collapse">
<thead>
<tr style="border-bottom:2px solid var(--ink);background:var(--bg)">
  <th class="mono" style="text-align:left;padding:14px 8px;font-size:11px;color:var(--mute);font-weight:600">指标</th>
  <th class="mono" style="text-align:center;padding:14px 8px;font-size:11px;color:var(--mute);font-weight:600">今天</th>
  <th class="mono" style="text-align:center;padding:14px 8px;font-size:11px;color:var(--red);font-weight:600">12 个月后</th>
  <th class="mono" style="text-align:center;padding:14px 8px;font-size:11px;color:var(--mute);font-weight:600">变化</th>
</tr>
</thead>
<tbody>
<tr style="border-bottom:1px solid var(--grid)">
  <td style="padding:18px 8px;font-family:'Noto Sans SC';font-size:18px;font-weight:900;color:var(--ink)">挂靠型智库</td>
  <td class="num" style="text-align:center;padding:18px 8px;font-size:24px;color:var(--ink2)">~500+</td>
  <td class="num" style="text-align:center;padding:18px 8px;font-size:26px;color:var(--ink);font-weight:700">-30%</td>
  <td class="num" style="text-align:center;padding:18px 8px;font-size:24px;color:var(--red);font-weight:700">↓</td>
</tr>
<tr style="border-bottom:1px solid var(--grid)">
  <td style="padding:18px 8px;font-family:'Noto Sans SC';font-size:18px;font-weight:900;color:var(--ink)">独立法人智库</td>
  <td class="num" style="text-align:center;padding:18px 8px;font-size:24px;color:var(--ink2)">~50</td>
  <td class="num" style="text-align:center;padding:18px 8px;font-size:26px;color:var(--ink);font-weight:700">+200</td>
  <td class="num" style="text-align:center;padding:18px 8px;font-size:24px;color:var(--gold);font-weight:700">↑</td>
</tr>
<tr style="border-bottom:1px solid var(--grid)">
  <td style="padding:18px 8px;font-family:'Noto Sans SC';font-size:18px;font-weight:900;color:var(--ink)">行业研究供给</td>
  <td class="num" style="text-align:center;padding:18px 8px;font-size:24px;color:var(--ink2)">100%</td>
  <td class="num" style="text-align:center;padding:18px 8px;font-size:26px;color:var(--red);font-weight:700">85%</td>
  <td class="num" style="text-align:center;padding:18px 8px;font-size:24px;color:var(--red);font-weight:700">↓</td>
</tr>
<tr>
  <td style="padding:18px 8px;font-family:'Noto Sans SC';font-size:18px;font-weight:900;color:var(--red)">头部智库议价</td>
  <td class="num" style="text-align:center;padding:18px 8px;font-size:24px;color:var(--ink2)">基准</td>
  <td class="num" style="text-align:center;padding:18px 8px;font-size:26px;color:var(--red);font-weight:700">+30%</td>
  <td class="num" style="text-align:center;padding:18px 8px;font-size:26px;color:var(--red);font-weight:700">↑</td>
</tr>
</tbody>
</table>

<div style="margin-top:20px;background:var(--ink);color:#fff;padding:18px 24px;text-align:center">
  <div style="font-family:'Noto Sans SC',sans-serif;font-size:18px;font-weight:900;line-height:1.4">行业研究供给收缩 <em style="color:var(--red);font-family:'Cormorant Garamond',serif;font-size:1.2em">15%</em><br>= 头部智库议价能力 +30%</div>
</div>
""",
    "bottom_left": "P04 / 06",
    "bottom_right": "数据 · 基线情景 60%",
})

# 05 12 个月行动清单（5 类人）
PAGES.append({
    "name": "p05_actions",
    "title": "12 个月",
    "title_em": "行动节奏",
    "subtitle_meta": "P05 · 5 × 4 PHASES",
    "kicker": "E · 行动清单",
    "body": """
<div class="lede">玉帝视角:看清全貌是不够的,要立刻动。<br>4 阶段 × 5 类人,12 个月节奏表。</div>

<div class="divider-h"></div>

<table style="width:100%;border-collapse:collapse">
<thead>
<tr style="border-bottom:2px solid var(--ink);background:var(--bg)">
  <th class="mono" style="text-align:left;padding:12px 6px;font-size:10px;color:var(--mute);font-weight:600">角色</th>
  <th class="mono" style="text-align:center;padding:12px 6px;font-size:10px;color:var(--red);font-weight:600">Q3 2026</th>
  <th class="mono" style="text-align:center;padding:12px 6px;font-size:10px;color:var(--mute);font-weight:600">Q4 2026</th>
  <th class="mono" style="text-align:center;padding:12px 6px;font-size:10px;color:var(--mute);font-weight:600">Q1 2027</th>
  <th class="mono" style="text-align:center;padding:12px 6px;font-size:10px;color:var(--ink);font-weight:600">Q2-Q3</th>
</tr>
</thead>
<tbody>
<tr style="border-bottom:1px solid var(--grid)">
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:15px;font-weight:900;color:var(--ink)">协会</td>
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:13px;text-align:center;color:var(--red);font-weight:700">摸底</td>
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:13px;text-align:center;color:var(--ink)">方案</td>
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:13px;text-align:center;color:var(--ink)">注册</td>
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:13px;text-align:center;color:var(--ink);font-weight:700">合规</td>
</tr>
<tr style="border-bottom:1px solid var(--grid)">
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:15px;font-weight:900;color:var(--ink)">酒店集团</td>
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:13px;text-align:center;color:var(--red);font-weight:700">清查</td>
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:13px;text-align:center;color:var(--ink)">评估</td>
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:13px;text-align:center;color:var(--ink)">决策</td>
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:13px;text-align:center;color:var(--ink);font-weight:700">执行</td>
</tr>
<tr style="border-bottom:1px solid var(--grid)">
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:15px;font-weight:900;color:var(--ink)">智库</td>
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:13px;text-align:center;color:var(--red);font-weight:700">重估</td>
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:13px;text-align:center;color:var(--ink)">客户沟通</td>
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:13px;text-align:center;color:var(--ink)">转型</td>
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:13px;text-align:center;color:var(--ink);font-weight:700">受益</td>
</tr>
<tr style="border-bottom:1px solid var(--grid)">
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:15px;font-weight:900;color:var(--ink)">投资人</td>
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:13px;text-align:center;color:var(--red);font-weight:700">扫描</td>
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:13px;text-align:center;color:var(--ink)">估值</td>
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:13px;text-align:center;color:var(--ink)">抄底</td>
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:13px;text-align:center;color:var(--ink);font-weight:700">整合</td>
</tr>
<tr>
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:15px;font-weight:900;color:var(--ink)">旁观者</td>
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:13px;text-align:center;color:var(--mute)">观察</td>
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:13px;text-align:center;color:var(--mute)">学习</td>
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:13px;text-align:center;color:var(--mute)">站队</td>
  <td style="padding:14px 6px;font-family:'Noto Sans SC';font-size:13px;text-align:center;color:var(--mute)">评估</td>
</tr>
</tbody>
</table>

<div style="margin-top:18px;text-align:center;background:var(--ink);color:#fff;padding:14px 24px">
  <div style="font-family:'Noto Sans SC',sans-serif;font-size:18px;font-weight:900;line-height:1.4">Q3 立刻做 · Q4 方案 · Q1 注册 · Q2-Q3 合规</div>
</div>
""",
    "bottom_left": "P05 / 06",
    "bottom_right": "玉帝视角",
})

# 06 终 - 5 大盲区 + 一句话
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
    <h3 style="font-size:18px;margin-bottom:4px">不要忽视"挂靠依赖症"</h3>
    <p style="font-family:'Noto Sans SC';font-size:15px;color:var(--ink2);line-height:1.5">协会下"研究院"看似合规,实则没有独立法人。12 个月后失效。</p>
  </div>
</div>

<div style="display:grid;grid-template-columns:auto 1fr;gap:18px;padding:14px 0;border-bottom:1px solid var(--grid);align-items:start">
  <div class="num" style="font-size:36px;color:var(--red);min-width:50px;line-height:1">02</div>
  <div>
    <h3 style="font-size:18px;margin-bottom:4px">不要低估合规成本</h3>
    <p style="font-family:'Noto Sans SC';font-size:15px;color:var(--ink2);line-height:1.5">独立法人化 = 500 万起 + 人员。改名不是零成本。</p>
  </div>
</div>

<div style="display:grid;grid-template-columns:auto 1fr;gap:18px;padding:14px 0;border-bottom:1px solid var(--grid);align-items:start">
  <div class="num" style="font-size:36px;color:var(--red);min-width:50px;line-height:1">03</div>
  <div>
    <h3 style="font-size:18px;margin-bottom:4px">不要错过"专家委员会"新形态</h3>
    <p style="font-family:'Noto Sans SC';font-size:15px;color:var(--ink2);line-height:1.5">AI / 绿色 / ESG / 银发 × 委员会 = 政策鼓励 + 供给真空。</p>
  </div>
</div>

<div style="display:grid;grid-template-columns:auto 1fr;gap:18px;padding:14px 0;border-bottom:1px solid var(--grid);align-items:start">
  <div class="num" style="font-size:36px;color:var(--red);min-width:50px;line-height:1">04</div>
  <div>
    <h3 style="font-size:18px;margin-bottom:4px">不要把"过渡期"当"宽限期"</h3>
    <p style="font-family:'Noto Sans SC';font-size:15px;color:var(--ink2);line-height:1.5">12 个月 = 硬截止日。Q3 摸底晚 1 周,Q4 方案全乱。</p>
  </div>
</div>

<div style="display:grid;grid-template-columns:auto 1fr;gap:18px;padding:14px 0;border-bottom:2px solid var(--ink);align-items:start">
  <div class="num" style="font-size:36px;color:var(--red);min-width:50px;line-height:1">05</div>
  <div>
    <h3 style="font-size:18px;margin-bottom:4px">不要忽视"老兵价值"</h3>
    <p style="font-family:'Noto Sans SC';font-size:15px;color:var(--ink2);line-height:1.5">新规不会替你做研究。数据/客户关系/IP,人才是真护城河。</p>
  </div>
</div>

<div style="margin-top:24px;background:var(--red);color:#fff;padding:24px 28px;text-align:center">
  <div class="mono" style="font-size:12px;letter-spacing:.32em;margin-bottom:12px;opacity:.85">玉帝视角 · 一句话</div>
  <div style="font-family:'Noto Sans SC',sans-serif;font-size:24px;font-weight:900;line-height:1.4">看清全貌 · 立刻行动 · 不踩坑</div>
</div>
""",
    "bottom_left": "P06 / 06 · 完结",
    "bottom_right": "2026.08.01 · 玉帝视角",
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


# ============ 主流程：生成 HTML + 渲染 PNG + 水印 ============

print(f"开始生成 {len(PAGES)} 张 (V3 Swiss Modern 范式)...")

# Step 1: 写 HTML
for i, page in enumerate(PAGES, 1):
    html = build_html(page, i, len(PAGES))
    html_path = OUT_DIR / f"{i:02d}_{page['name']}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✅ HTML [{i:02d}/{len(PAGES):02d}] {html_path.name}")

print(f"\n✅ HTML 写完 → {OUT_DIR}")

# Step 2: 渲染 PNG (1080×1440, Retina 2x)
print(f"\n开始渲染 PNG (1080×1440, Retina 2x)...")
sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace\toolbox')
from watermark_tool import protect_output

for i, page in enumerate(PAGES, 1):
    html_path = OUT_DIR / f"{i:02d}_{page['name']}.html"
    png_path = OUT_DIR / f"{i:02d}_{page['name']}.png"

    r = subprocess.run([
        EDGE, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--force-device-scale-factor=2",
        "--window-size=1080,1440",
        f"--screenshot={png_path}",
        html_path.as_uri(),
    ], capture_output=True, text=True, timeout=60)
    
    rc = r.returncode
    size = png_path.stat().st_size if png_path.exists() else 0
    print(f"  📸 Render [{i:02d}/{len(PAGES):02d}] RC={rc}, PNG={size:,} bytes")

    # Step 3: 水印
    if png_path.exists() and size > 0:
        try:
            wm_out = protect_output(str(png_path))
            print(f"    🔒 Watermark: {Path(wm_out).name}")
        except Exception as e:
            print(f"    ❌ Watermark FAILED: {e}")

print(f"\n=== All done ===")
print(f"\nOutput dir: {OUT_DIR}")
for p in sorted(OUT_DIR.glob("*.png")):
    print(f"  {p.name}: {p.stat().st_size:,} bytes")