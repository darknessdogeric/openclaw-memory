#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
gen_2026_summer_xhs_v3.py - V3 Swiss Modern 海报 V3.1
- 燕麦白 + 黑白灰商务 (Swiss Modern / 麦肯锡)
- B166ER B 标规范: 左上 + 右下
- 9 张 1080×1440 (玉帝视角 通用受众版)
- Eric 个人项目(安逸/AHL/医养/167家) 完全不提
- 外资酒店集团样本加入 p08
- p09 改成 "入境获客手段清单" 为小红书个人售卖引流
- 没有价格字样
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
import subprocess

OUT_DIR = Path(r"C:/Users/ericz/Desktop/新媒体产品线/2026暑期对冲9图-v3.0/XHS-output")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ========== 共用 CSS (V3 范式·严格布局统一) ==========
CSS = """
<style>
:root{
  --bg:#f4f1ec;--bg2:#ffffff;
  --ink:#1a1a1a;--ink2:#4a4a4a;
  --grid:#d6d6d6;--red:#d62828;--blue:#003049;
  --mute:#8a8a8a;--gold:#b08947;
  --safe-top:60px;--safe-bot:60px;
  --hpad:80px
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#1a1a1a}
body{font-family:'Inter','Noto Sans SC',sans-serif;background:#1a1a1a;
  display:flex;justify-content:center;align-items:center;min-height:100vh;color:var(--ink)}
.poster{
  width:1080px;min-height:1440px;height:1440px;background:var(--bg);color:var(--ink);
  position:relative;overflow:hidden;
  display:flex;flex-direction:column;
  padding:var(--safe-top) var(--hpad) var(--safe-bot) var(--hpad)
}
.grid{
  position:absolute;top:0;left:var(--hpad);right:var(--hpad);bottom:0;
  background-image:linear-gradient(to right,var(--grid) 1px,transparent 1px);
  background-size:76.6px 100%;opacity:.4;pointer-events:none;z-index:1
}
/* 顶部统一 - top fixed 56px */
.top{
  height:56px;
  padding-bottom:20px;border-bottom:2px solid var(--ink);
  display:grid;grid-template-columns:1fr 1fr;align-items:end;
  position:relative;z-index:2
}
.brand{font-family:'IBM Plex Mono',monospace;font-size:16px;font-weight:500;
  letter-spacing:.16em;text-transform:uppercase;color:var(--ink)}
.meta{font-family:'IBM Plex Mono',monospace;font-size:16px;color:var(--mute);
  letter-spacing:.1em;text-align:right}
/* 中段统一 - main flex auto 自适应, 内部所有元素压缩 */
.main{
  flex:1 1 auto;min-height:0;display:flex;flex-direction:column;position:relative;z-index:2;
  padding-top:24px
}
/* 底部统一 - bottom fixed 90px */
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
/* 统一元素 */
.kicker{font-family:'IBM Plex Mono',monospace;font-size:18px;color:var(--red);
  letter-spacing:.32em;text-transform:uppercase;font-weight:600;
  display:flex;align-items:center;gap:14px;margin-bottom:24px}
.kicker::before{content:"";width:48px;height:2px;background:var(--red);display:inline-block}
h1{font-family:'Noto Sans SC','Inter',sans-serif;font-size:110px;font-weight:900;
  line-height:1.02;letter-spacing:-.04em;color:var(--ink);margin-bottom:14px}
h1 em{color:var(--red);font-family:'Cormorant Garamond',serif;font-weight:600;
  font-style:italic;font-size:.7em;letter-spacing:-.01em}
h2{font-family:'Noto Sans SC',sans-serif;font-size:48px;font-weight:900;
  color:var(--ink);line-height:1.18;letter-spacing:-.02em}
h3{font-family:'Noto Sans SC',sans-serif;font-size:24px;font-weight:900;
  color:var(--ink);line-height:1.25;letter-spacing:-.01em;margin-bottom:8px;
  white-space:nowrap}
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

# ========== 9 张内容 ==========

PAGES = []

# 01 封面 - 玉帝视角·5 年冷热
PAGES.append({
    "name": "p01_cover",
    "title": "玉帝视角",
    "title_em": "看 2026 暑期",
    "subtitle_meta": "VOL.01 · 5-YEAR OVERVIEW",
    "kicker": "A · 玉帝视角",
    "body": """
<div class="lede">看清全貌 · 不被噪音带节奏。<br>用 9 张图说清一个问题: <em style="color:var(--red);font-weight:700;font-style:normal">今年的冷,会持续还是反转?</em></div>

<div style="display:grid;grid-template-columns:1fr 1px 1fr 1px 1fr;border-top:2px solid var(--ink);border-bottom:2px solid var(--ink);padding:42px 0">
  <div style="padding:0 18px;text-align:center">
    <div class="num" style="font-size:88px;color:var(--ink);line-height:1">10<span style="font-size:32px;color:var(--mute);font-style:italic">年</span></div>
    <div class="mono" style="margin-top:10px">DURATION</div>
    <div style="font-size:15px;color:var(--ink);margin-top:8px;font-weight:600;font-family:'Noto Sans SC'">十年缓冲</div>
  </div>
  <div class="divider-v" style="height:120px;align-self:center"></div>
  <div style="padding:0 18px;text-align:center">
    <div class="num" style="font-size:88px;color:var(--red);line-height:1">+30<span style="font-size:32px;color:var(--mute);font-style:italic">%</span></div>
    <div class="mono" style="margin-top:10px">INBOUND</div>
    <div style="font-size:15px;color:var(--ink);margin-top:8px;font-weight:600;font-family:'Noto Sans SC'">半年入境</div>
  </div>
  <div class="divider-v" style="height:120px;align-self:center"></div>
  <div style="padding:0 18px;text-align:center">
    <div class="num" style="font-size:88px;color:var(--ink);line-height:1">5<span style="font-size:32px;color:var(--mute);font-style:italic">年</span></div>
    <div class="mono" style="margin-top:10px">STRATEGY</div>
    <div style="font-size:15px;color:var(--ink);margin-top:8px;font-weight:600;font-family:'Noto Sans SC'">顶层规划</div>
  </div>
</div>

<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:42px">
  <div style="padding:20px 16px;border:2px solid var(--ink);text-align:center">
    <div class="mono" style="color:var(--ink);font-weight:700">01 · 冷数据</div>
    <div style="font-family:'IBM Plex Mono';font-size:11px;color:var(--mute);margin-top:6px;letter-spacing:.18em">COLD DATA</div>
  </div>
  <div style="padding:20px 16px;background:var(--red);color:#fff;text-align:center">
    <div class="mono" style="color:#fff;font-weight:700">02 · 硬数据</div>
    <div style="font-family:'IBM Plex Mono';font-size:11px;opacity:.85;margin-top:6px;letter-spacing:.18em">INBOUND</div>
  </div>
  <div style="padding:20px 16px;border:2px solid var(--ink);text-align:center">
    <div class="mono" style="color:var(--ink);font-weight:700">03 · 行动</div>
    <div style="font-family:'IBM Plex Mono';font-size:11px;color:var(--mute);margin-top:6px;letter-spacing:.18em">ACTION</div>
  </div>
</div>
""",
    "bottom_left": "V3 范式 · B166ER",
    "bottom_right": "2026.07.14 · 玉帝视角",
})

# 02 全网在议论什么
PAGES.append({
    "name": "p02_agenda",
    "title": "全网",
    "title_em": "在讨论什么",
    "subtitle_meta": "P02 · 3 CONTRADICTIONS",
    "kicker": "B · THE CONTRADICTION",
    "body": """
<div class="lede">看似矛盾的 3 个判断,实则同一格局。<br>玉帝视角:这是三个时间切片,不是三种结论。</div>

<div class="divider-h"></div>

<div style="display:grid;grid-template-columns:auto 1fr;gap:24px;padding:32px 0;border-bottom:1px solid var(--grid);align-items:start">
  <div class="num" style="font-size:84px;color:var(--red);min-width:96px;line-height:1">01</div>
  <div>
    <h3>今年暑期确实冷</h3>
    <p class="body" style="margin-top:8px">中小单体酒店'有客流不盈利'。锦江全服务型酒店 RevPAR 同比 -10.8%。这是事实,不是叙事。</p>
  </div>
</div>

<div style="display:grid;grid-template-columns:auto 1fr;gap:24px;padding:32px 0;border-bottom:1px solid var(--grid);align-items:start">
  <div class="num" style="font-size:84px;color:var(--ink);min-width:96px;line-height:1">02</div>
  <div>
    <h3>有人说 是 5 年里最好的一年</h3>
    <p class="body" style="margin-top:8px">这个说法在酒店圈被广泛讨论,但缺少数据验证。单纯的判断不是事实,要看支撑是什么。</p>
  </div>
</div>

<div style="display:grid;grid-template-columns:auto 1fr;gap:24px;padding:32px 0;align-items:start">
  <div class="num" style="font-size:84px;color:var(--ink);min-width:96px;line-height:1">03</div>
  <div>
    <h3>中央 7 月发了 5 年规划</h3>
    <p class="body" style="margin-top:8px">国函〔2026〕61 号 · 旅游强国 十五五 规划。一次性输出 11 个 2030 量化目标,大提入境 1.9 亿人次。</p>
  </div>
</div>

<div class="divider-h" style="margin-top:32px"></div>
<div style="text-align:center;padding-top:24px">
  <span style="font-family:'Noto Sans SC',sans-serif;font-size:24px;font-weight:600;color:var(--ink)">-- 时间切片 不是 矛盾结论 --</span>
</div>
""",
    "bottom_left": "P02 / 09",
    "bottom_right": "玉帝视角",
})

# 03 国内冷数据 (含外资) - 4 数据一排
PAGES.append({
    "name": "p03_cold",
    "title": "国内",
    "title_em": "都冷",
    "subtitle_meta": "P03 · 2 外资 · 2 内资",
    "kicker": "C · COLD DATA",
    "body": """
<div class="lede">内资外资都冷,只是冷法不同。<br>玉帝视角先看冷的成色 -- 5 组关键数据。</div>

<div class="divider-h"></div>

<div style="display:grid;grid-template-columns:1fr 1px 1fr 1px 1fr 1px 1fr;border-top:none;border-bottom:2px solid var(--ink)">
  <div style="padding:48px 16px 36px 0;border-right:1px solid var(--grid);overflow:hidden">
    <div class="num" style="font-size:72px;color:var(--red);line-height:.85;margin-bottom:14px;letter-spacing:-.04em">-10.8<span style="font-size:26px;color:var(--mute);font-style:italic">%</span></div>
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px">
      <span style="background:var(--red);color:#fff;font-family:'IBM Plex Mono';font-size:10px;padding:4px 9px;letter-spacing:.2em;font-weight:700">内资</span>
    </div>
    <h3 style="font-size:20px;line-height:1.2;white-space:nowrap;overflow:hidden">锦江 全服务型</h3>
    <p style="font-family:'Noto Sans SC';font-size:14px;color:var(--ink2);margin-top:6px;line-height:1.4">RevPAR 2024</p>
  </div>
  <div class="divider-v" style="align-self:center"></div>
  <div style="padding:48px 16px 36px 16px;border-right:1px solid var(--grid);overflow:hidden">
    <div class="num" style="font-size:72px;color:var(--red);line-height:.85;margin-bottom:14px;letter-spacing:-.04em">-8.4<span style="font-size:26px;color:var(--mute);font-style:italic">%</span></div>
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px">
      <span style="background:var(--blue);color:#fff;font-family:'IBM Plex Mono';font-size:10px;padding:4px 9px;letter-spacing:.2em;font-weight:700">外资</span>
    </div>
    <h3 style="font-size:20px;line-height:1.2;white-space:nowrap;overflow:hidden">万豪 大中华</h3>
    <p style="font-family:'Noto Sans SC';font-size:14px;color:var(--ink2);margin-top:6px;line-height:1.4">RevPAR Q3 2024</p>
  </div>
  <div class="divider-v" style="align-self:center"></div>
  <div style="padding:48px 16px 36px 16px;border-right:1px solid var(--grid);overflow:hidden">
    <div class="num" style="font-size:72px;color:var(--red);line-height:.85;margin-bottom:14px;letter-spacing:-.04em">-6.77<span style="font-size:26px;color:var(--mute);font-style:italic">%</span></div>
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px">
      <span style="background:var(--red);color:#fff;font-family:'IBM Plex Mono';font-size:10px;padding:4px 9px;letter-spacing:.2em;font-weight:700">内资</span>
    </div>
    <h3 style="font-size:20px;line-height:1.2;white-space:nowrap;overflow:hidden">亚朵</h3>
    <p style="font-family:'Noto Sans SC';font-size:14px;color:var(--ink2);margin-top:6px;line-height:1.4">RevPAR · 2年下行</p>
  </div>
  <div class="divider-v" style="align-self:center"></div>
  <div style="padding:48px 0 36px 16px;overflow:hidden">
    <div class="num" style="font-size:72px;color:var(--red);line-height:.85;margin-bottom:14px;letter-spacing:-.04em">-10.3<span style="font-size:26px;color:var(--mute);font-style:italic">%</span></div>
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px">
      <span style="background:var(--blue);color:#fff;font-family:'IBM Plex Mono';font-size:10px;padding:4px 9px;letter-spacing:.2em;font-weight:700">外资</span>
    </div>
    <h3 style="font-size:20px;line-height:1.2;white-space:nowrap;overflow:hidden">洲际 IHG</h3>
    <p style="font-family:'Noto Sans SC';font-size:14px;color:var(--ink2);margin-top:6px;line-height:1.4">RevPAR Q3 大中华</p>
  </div>
</div>
""",
    "bottom_left": "数据 · 锦江/亚朵/万豪/IHG 2024 业绩",
    "bottom_right": "玉帝视角 P03 / 09",
})

# 04 入境飞起 (4 大时间序列 - 极简版, 不溢出)
PAGES.append({
    "name": "p04_inbound",
    "title": "入境",
    "title_em": "真火",
    "subtitle_meta": "P04 · 4 TIME POINTS",
    "kicker": "D · INBOUND DATA",
    "body": """
<div class="lede">5 年唯一两位数高增赛道。<br>玉帝视角:看火的真实性。</div>

<div class="divider-h"></div>

<div style="display:grid;grid-template-columns:1fr 1px 1fr;border-top:none;border-bottom:1px solid var(--ink)">
  <div style="padding:32px 20px 32px 0;border-right:1px solid var(--grid);display:flex;flex-direction:column">
    <div class="mono" style="color:var(--mute);margin-bottom:10px">2026 Q1</div>
    <div class="num" style="font-size:76px;color:var(--ink);line-height:.9;letter-spacing:-.04em;margin-bottom:12px">+22.3<span style="font-size:26px;color:var(--mute);font-style:italic">%</span></div>
    <p style="font-family:'Noto Sans SC';font-size:16px;color:var(--ink);font-weight:600;margin-bottom:2px">出入境外国人</p>
    <p class="body-sm">2133 万人次</p>
  </div>
  <div style="padding:32px 0 32px 20px;display:flex;flex-direction:column">
    <div class="mono" style="color:var(--red);margin-bottom:10px">Q1 · 免签</div>
    <div class="num" style="font-size:76px;color:var(--red);line-height:.9;letter-spacing:-.04em;margin-bottom:12px">+29.3<span style="font-size:26px;color:var(--mute);font-style:italic">%</span></div>
    <p style="font-family:'Noto Sans SC';font-size:16px;color:var(--ink);font-weight:600;margin-bottom:2px">免签入境</p>
    <p class="body-sm">831.5 万人次</p>
  </div>
</div>

<div style="display:grid;grid-template-columns:1fr 1px 1fr;border-bottom:2px solid var(--ink)">
  <div style="padding:32px 20px 32px 0;border-right:1px solid var(--grid);display:flex;flex-direction:column">
    <div class="mono" style="color:var(--red);margin-bottom:10px">H1 · 免签累计</div>
    <div class="num" style="font-size:76px;color:var(--red);line-height:.9;letter-spacing:-.04em;margin-bottom:12px">+30.6<span style="font-size:26px;color:var(--mute);font-style:italic">%</span></div>
    <p style="font-family:'Noto Sans SC';font-size:16px;color:var(--ink);font-weight:600;margin-bottom:2px">免签外国人</p>
    <p class="body-sm">1781.5 万人次</p>
  </div>
  <div style="padding:32px 0 32px 20px;display:flex;flex-direction:column">
    <div class="mono" style="color:var(--red);margin-bottom:10px">2025 · 入境花费</div>
    <div class="num" style="font-size:76px;color:var(--red);line-height:.9;letter-spacing:-.04em;margin-bottom:12px">+39.2<span style="font-size:26px;color:var(--mute);font-style:italic">%</span></div>
    <p style="font-family:'Noto Sans SC';font-size:16px;color:var(--ink);font-weight:600;margin-bottom:2px">入境消费</p>
    <p class="body-sm">1311 亿美元</p>
  </div>
</div>

<div style="margin-top:20px;text-align:center;padding:0 28px">
  <div style="font-family:'Noto Sans SC',sans-serif;font-size:18px;font-weight:600;color:var(--ink);line-height:1.4">花费增速 <em style="color:var(--red);font-family:'Cormorant Garamond',serif;font-weight:700;font-style:italic;font-size:1.2em">10.8%</em> &gt; 人次增速 <em style="color:var(--red);font-family:'Cormorant Garamond',serif;font-weight:700;font-style:italic;font-size:1.2em">7.6%</em> · 消费升级 &gt; 流量升级</div>
</div>
""",
    "bottom_left": "数据 · 国家移民管理局",
    "bottom_right": "玉帝视角 P04 / 09",
})

# 05 5 年规划对齐
PAGES.append({
    "name": "p05_plan",
    "title": "5 年",
    "title_em": "顶层纲领",
    "subtitle_meta": "P05 · 国函〔2026〕61",
    "kicker": "E · 5-YEAR PLAN",
    "body": """
<div class="lede">中央发文,旅游强国首次入五年规划。<br>玉帝视角将 9 个关键数字摆开。</div>

<div class="divider-h"></div>

<div style="display:grid;grid-template-columns:1fr 1px 1fr 1px 1fr 1px 1fr;border-bottom:2px solid var(--ink)">
  <div style="padding:32px 0;text-align:center;border-right:none">
    <div class="num" style="font-size:64px;color:var(--ink);line-height:1">83<span style="font-size:22px;color:var(--mute);font-style:italic">亿</span></div>
    <div class="mono" style="margin-top:10px">2030 国内</div>
  </div>
  <div class="divider-v" style="height:90px;align-self:center"></div>
  <div style="padding:32px 0;text-align:center">
    <div class="num" style="font-size:64px;color:var(--ink);line-height:1">7.7<span style="font-size:22px;color:var(--mute);font-style:italic">万亿</span></div>
    <div class="mono" style="margin-top:10px">国内花费</div>
  </div>
  <div class="divider-v" style="height:90px;align-self:center"></div>
  <div style="padding:32px 0;text-align:center">
    <div class="num" style="font-size:64px;color:var(--red);line-height:1">1.9<span style="font-size:22px;color:var(--mute);font-style:italic">亿</span></div>
    <div class="mono" style="color:var(--red);margin-top:10px">2030 入境</div>
  </div>
  <div class="divider-v" style="height:90px;align-self:center"></div>
  <div style="padding:32px 0;text-align:center">
    <div class="num" style="font-size:64px;color:var(--red);line-height:1">1500<span style="font-size:22px;color:var(--mute);font-style:italic">亿</span></div>
    <div class="mono" style="color:var(--red);margin-top:10px">入境花费$</div>
  </div>
</div>

<div style="display:grid;grid-template-columns:repeat(4,1fr);border-top:2px solid var(--ink);border-bottom:2px solid var(--ink);padding:32px 0">
  <div style="text-align:center;border-right:1px solid var(--grid)">
    <div class="num" style="font-size:48px;color:var(--ink)">88</div>
    <div class="mono" style="margin-top:8px">CITIES</div>
  </div>
  <div style="text-align:center;border-right:1px solid var(--grid)">
    <div class="num" style="font-size:48px;color:var(--ink)">11</div>
    <div class="mono" style="margin-top:8px">PROJECTS</div>
  </div>
  <div style="text-align:center;border-right:1px solid var(--grid)">
    <div class="num" style="font-size:48px;color:var(--ink)">9</div>
    <div class="mono" style="margin-top:8px">GUARANTEES</div>
  </div>
  <div style="text-align:center">
    <div class="num" style="font-size:48px;color:var(--ink)">3</div>
    <div class="mono" style="margin-top:8px">FUTURES</div>
  </div>
</div>
""",
    "bottom_left": "数据 · 国务院公报",
    "bottom_right": "玉帝视角 P05 / 09",
})

# 06 入境对冲还是战略? 第一性原理
PAGES.append({
    "name": "p06_first",
    "title": "对冲",
    "title_em": "还是战略",
    "subtitle_meta": "P06 · 3 LAYERS",
    "kicker": "F · FIRST PRINCIPLES",
    "body": """
<div class="lede">3 层还原:从现象到本质。<br>玉帝视角揭穿 5 个"不是对冲"的理由。</div>

<div class="divider-h"></div>

<div style="display:grid;grid-template-columns:auto 1fr;gap:24px;padding:24px 0;border-bottom:1px solid var(--grid);align-items:center">
  <div class="num" style="font-size:96px;color:var(--mute);min-width:120px;line-height:1">1</div>
  <div>
    <div class="mono" style="margin-bottom:8px">PHENOMENON</div>
    <h3 style="font-size:24px">今年暑期冷 + 中央大提入境</h3>
  </div>
</div>

<div style="display:grid;grid-template-columns:auto 1fr;gap:24px;padding:24px 0;border-bottom:1px solid var(--grid);align-items:center">
  <div class="num" style="font-size:96px;color:var(--ink);min-width:120px;line-height:1">2</div>
  <div>
    <div class="mono" style="margin-bottom:8px">MECHANISM</div>
    <h3 style="font-size:24px">国内卷化 + 入境起飞 同时出现</h3>
  </div>
</div>

<div style="display:grid;grid-template-columns:auto 1fr;gap:24px;padding:24px 0;border-bottom:2px solid var(--ink);align-items:center">
  <div class="num" style="font-size:96px;color:var(--red);min-width:120px;line-height:1">3</div>
  <div>
    <div class="mono" style="margin-bottom:8px">ESSENCE</div>
    <h3 style="font-size:24px">中国 出口立国 → 消费+服务+出海</h3>
  </div>
</div>

<div style="margin-top:32px;background:var(--ink);color:#fff;padding:28px 32px">
  <div class="mono" style="font-size:12px;color:#aaa;letter-spacing:.18em;margin-bottom:12px">5 REASONS · 不是短期对冲</div>
  <div style="font-family:'Noto Sans SC',sans-serif;font-size:18px;line-height:1.7">
    <span style="color:#fff;font-weight:700">1</span> 入境政策始于 2023,显著早于今年暑期<br>
    <span style="color:#fff;font-weight:700">2</span> 5 年 2026-2030 规划,不止一年<br>
    <span style="color:#fff;font-weight:700">3</span> 对美博弈 + 文化输出,超出经济范畴<br>
    <span style="color:#fff;font-weight:700">4</span> CAGR 10.8% 是战略目标,不是应急<br>
    <span style="color:#fff;font-weight:700">5</span> 玉帝:不止 看飞 还要 造飞
  </div>
</div>
""",
    "bottom_left": "5 角度论证 · 多源验证",
    "bottom_right": "玉帝视角 P06 / 09",
})

# 07 5 年时间线全景
PAGES.append({
    "name": "p07_timeline",
    "title": "5 年",
    "title_em": "全景时间线",
    "subtitle_meta": "P07 · 4 NODES",
    "kicker": "G · 5 YEAR HORIZON",
    "body": """
<div class="lede">把 5 年切割成 4 个关键节点。<br>玉帝视角:每个节点都有可识别的政策信号。</div>

<div style="position:relative;padding:36px 0;border-top:2px solid var(--ink);border-bottom:2px solid var(--ink)">
  <div style="position:absolute;left:0;right:0;top:50%;height:2px;background:var(--ink)"></div>

  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;position:relative;z-index:2">
    <div style="text-align:center">
      <div style="width:36px;height:36px;background:var(--red);border:3px solid var(--bg);border-radius:50%;margin:0 auto 14px"></div>
      <div class="num" style="font-size:44px;color:var(--red);line-height:1;margin-bottom:8px">2026</div>
      <div style="font-family:'Noto Sans SC';font-size:15px;font-weight:700;color:var(--ink);margin-bottom:4px">政策密集</div>
      <div style="font-family:'Noto Sans SC';font-size:14px;color:var(--mute)">入境起飞</div>
    </div>
    <div style="text-align:center">
      <div style="width:36px;height:36px;background:var(--gold);border:3px solid var(--bg);border-radius:50%;margin:0 auto 14px"></div>
      <div class="num" style="font-size:44px;color:var(--gold);line-height:1;margin-bottom:8px">2027</div>
      <div style="font-family:'Noto Sans SC';font-size:15px;font-weight:700;color:var(--ink);margin-bottom:4px">AI 分水岭</div>
      <div style="font-family:'Noto Sans SC';font-size:14px;color:var(--mute)">入境 1.85 亿</div>
    </div>
    <div style="text-align:center">
      <div style="width:36px;height:36px;background:var(--gold);border:3px solid var(--bg);border-radius:50%;margin:0 auto 14px"></div>
      <div class="num" style="font-size:44px;color:var(--gold);line-height:1;margin-bottom:8px">2028</div>
      <div style="font-family:'Noto Sans SC';font-size:15px;font-weight:700;color:var(--ink);margin-bottom:4px">规划中段</div>
      <div style="font-family:'Noto Sans SC';font-size:14px;color:var(--mute)">AI 改造完成</div>
    </div>
    <div style="text-align:center">
      <div style="width:36px;height:36px;background:var(--ink);border:3px solid var(--bg);border-radius:50%;margin:0 auto 14px"></div>
      <div class="num" style="font-size:44px;color:var(--ink);line-height:1;margin-bottom:8px">2030</div>
      <div style="font-family:'Noto Sans SC';font-size:15px;font-weight:700;color:var(--ink);margin-bottom:4px">规划收官</div>
      <div style="font-family:'Noto Sans SC';font-size:14px;color:var(--mute)">验证决策</div>
    </div>
  </div>
</div>

<div style="margin-top:28px;display:grid;grid-template-columns:1fr 1px 1fr 1px 1fr;align-items:center;padding:28px 0;border-top:2px solid var(--ink);border-bottom:2px solid var(--ink)">
  <div style="padding:0 18px;text-align:center">
    <div class="num" style="font-size:56px;color:var(--ink);line-height:1">23<span style="font-size:20px;color:var(--mute);font-style:italic">亿</span></div>
    <div class="mono" style="margin-top:6px">DOMESTIC +</div>
  </div>
  <div class="divider-v" style="height:80px;align-self:center"></div>
  <div style="padding:0 18px;text-align:center">
    <div class="num" style="font-size:56px;color:var(--red);line-height:1">5800<span style="font-size:20px;color:var(--mute);font-style:italic">万</span></div>
    <div class="mono" style="color:var(--red);margin-top:6px">INBOUND +</div>
  </div>
  <div class="divider-v" style="height:80px;align-self:center"></div>
  <div style="padding:0 18px;text-align:center">
    <div class="num" style="font-size:56px;color:var(--ink);line-height:1">$4300<span style="font-size:20px;color:var(--mute);font-style:italic">亿</span></div>
    <div class="mono" style="margin-top:6px">入境消费 +</div>
  </div>
</div>
""",
    "bottom_left": "玉帝视角 · 全景对齐",
    "bottom_right": "玉帝视角 P07 / 09",
})

# 08 8 类酒店不同命运 (含外资) - 6 类全覆盖
PAGES.append({
    "name": "p08_matrix",
    "title": "8 类",
    "title_em": "不同命运",
    "subtitle_meta": "P08 · 8 TYPES",
    "kicker": "H · TYPE MATRIX",
    "body": """
<div class="lede">不是所有酒店都冷。玉帝视角分类:含外资品牌,共 8 类命运。</div>

<div class="divider-h"></div>

<table style="width:100%;border-collapse:collapse">
<thead>
<tr style="border-bottom:2px solid var(--ink);background:var(--bg)">
  <th class="mono" style="text-align:left;padding:14px 10px;font-size:12px;color:var(--mute);font-weight:600">CATEGORY</th>
  <th class="mono" style="text-align:center;padding:14px 8px;font-size:12px;color:var(--mute);font-weight:600">NOW</th>
  <th class="mono" style="text-align:center;padding:14px 8px;font-size:12px;color:var(--mute);font-weight:600">5Y</th>
  <th style="padding:14px 8px"></th>
</tr>
</thead>
<tbody>

<!-- 国内 -->
<tr style="border-bottom:1px solid var(--grid)">
  <td style="padding:14px 10px">
    <div style="font-family:'Noto Sans SC';font-size:18px;font-weight:900;color:var(--ink)">经济型</div>
    <div style="font-family:'IBM Plex Mono';font-size:11px;color:var(--mute);margin-top:2px;letter-spacing:.12em">如家 · 汉庭</div>
  </td>
  <td class="num" style="text-align:center;padding:14px 8px;color:var(--red);font-size:26px;font-weight:700">-</td>
  <td class="num" style="text-align:center;padding:14px 8px;color:var(--red);font-size:26px;font-weight:700">- -</td>
  <td style="padding:14px 8px;font-family:'Noto Sans SC';font-size:14px;color:var(--ink2)">ADR 难提 · 加盟下沉</td>
</tr>

<tr style="border-bottom:1px solid var(--grid)">
  <td style="padding:14px 10px">
    <div style="font-family:'Noto Sans SC';font-size:18px;font-weight:900;color:var(--ink)">中端</div>
    <div style="font-family:'IBM Plex Mono';font-size:11px;color:var(--mute);margin-top:2px;letter-spacing:.12em">亚朵 · 桔子 · 全季</div>
  </td>
  <td class="num" style="text-align:center;padding:14px 8px;color:var(--red);font-size:26px;font-weight:700">~</td>
  <td class="num" style="text-align:center;padding:14px 8px;color:var(--red);font-size:26px;font-weight:700">~</td>
  <td style="padding:14px 8px;font-family:'Noto Sans SC';font-size:14px;color:var(--ink2)">AI 改造决定胜负</td>
</tr>

<tr style="border-bottom:1px solid var(--grid)">
  <td style="padding:14px 10px">
    <div style="font-family:'Noto Sans SC';font-size:18px;font-weight:900;color:var(--ink)">高端</div>
    <div style="font-family:'IBM Plex Mono';font-size:11px;color:var(--mute);margin-top:2px;letter-spacing:.12em">锦江 · 华住 · 首旅</div>
  </td>
  <td class="num" style="text-align:center;padding:14px 8px;color:var(--gold);font-size:26px;font-weight:700">~</td>
  <td class="num" style="text-align:center;padding:14px 8px;color:var(--gold);font-size:26px;font-weight:700">+</td>
  <td style="padding:14px 8px;font-family:'Noto Sans SC';font-size:14px;color:var(--ink2)">场景化 + 文化 IP</td>
</tr>

<!-- 外资 -->
<tr style="border-bottom:1px solid var(--grid);background:rgba(208,40,40,.04)">
  <td style="padding:14px 10px">
    <div style="font-family:'Noto Sans SC';font-size:18px;font-weight:900;color:var(--ink)">外资 · 国际品牌</div>
    <div style="font-family:'IBM Plex Mono';font-size:11px;color:var(--red);margin-top:2px;letter-spacing:.12em">万豪 · 希尔顿 · 雅高 · 凯悦 · IHG</div>
  </td>
  <td class="num" style="text-align:center;padding:14px 8px;color:var(--ink);font-size:26px;font-weight:700">+</td>
  <td class="num" style="text-align:center;padding:14px 8px;color:var(--red);font-size:26px;font-weight:700">+ + +</td>
  <td style="padding:14px 8px;font-family:'Noto Sans SC';font-size:14px;color:var(--red);font-weight:700">入境政策的天然赢家</td>
</tr>

<tr style="border-bottom:1px solid var(--grid)">
  <td style="padding:14px 10px">
    <div style="font-family:'Noto Sans SC';font-size:18px;font-weight:900;color:var(--ink)">外资 · 中端精选</div>
    <div style="font-family:'IBM Plex Mono';font-size:11px;color:var(--mute);margin-top:2px;letter-spacing:.12em">希尔顿欢朋 · 雅高美居 · IHG智选</div>
  </td>
  <td class="num" style="text-align:center;padding:14px 8px;color:var(--gold);font-size:26px;font-weight:700">+</td>
  <td class="num" style="text-align:center;padding:14px 8px;color:var(--red);font-size:26px;font-weight:700">+ +</td>
  <td style="padding:14px 8px;font-family:'Noto Sans SC';font-size:14px;color:var(--ink2)">外籍客首选 · 增量红利</td>
</tr>

<tr style="border-bottom:1px solid var(--grid)">
  <td style="padding:14px 10px">
    <div style="font-family:'Noto Sans SC';font-size:18px;font-weight:900;color:var(--ink)">外资 · 单体精品</div>
    <div style="font-family:'IBM Plex Mono';font-size:11px;color:var(--mute);margin-top:2px;letter-spacing:.12em">Six Senses · Aman · 1 Hotels</div>
  </td>
  <td class="num" style="text-align:center;padding:14px 8px;color:var(--gold);font-size:26px;font-weight:700">+ +</td>
  <td class="num" style="text-align:center;padding:14px 8px;color:var(--red);font-size:26px;font-weight:700">+ + +</td>
  <td style="padding:14px 8px;font-family:'Noto Sans SC';font-size:14px;color:var(--ink2)">国际化标签 · 入境首选</td>
</tr>

<!-- 度假 + 入境接待 -->
<tr style="border-bottom:1px solid var(--grid)">
  <td style="padding:14px 10px">
    <div style="font-family:'Noto Sans SC';font-size:18px;font-weight:900;color:var(--ink)">度假资源型</div>
    <div style="font-family:'IBM Plex Mono';font-size:11px;color:var(--mute);margin-top:2px;letter-spacing:.12em">青城山 · 稻城 · 九寨沟</div>
  </td>
  <td class="num" style="text-align:center;padding:14px 8px;color:var(--gold);font-size:26px;font-weight:700">+</td>
  <td class="num" style="text-align:center;padding:14px 8px;color:var(--gold);font-size:26px;font-weight:700">+ +</td>
  <td style="padding:14px 8px;font-family:'Noto Sans SC';font-size:14px;color:var(--ink2)">稳定溢价 · 政策加成</td>
</tr>

<tr>
  <td style="padding:14px 10px;background:var(--red);color:#fff">
    <div style="font-family:'Noto Sans SC';font-size:18px;font-weight:900">入境接待</div>
    <div style="font-family:'IBM Plex Mono';font-size:11px;opacity:.9;margin-top:2px;letter-spacing:.12em">所有品牌 · 入境定位</div>
  </td>
  <td class="num" style="text-align:center;padding:14px 8px;background:var(--red);color:#fff;font-size:26px;font-weight:700">+</td>
  <td class="num" style="text-align:center;padding:14px 8px;background:var(--red);color:#fff;font-size:26px;font-weight:700">+ + +</td>
  <td style="padding:14px 8px;background:var(--red);color:#fff;font-family:'Noto Sans SC';font-size:14px;font-weight:700">5 年唯一高确定性</td>
</tr>

</tbody>
</table>
""",
    "bottom_left": "矩阵分类 · 玉帝视角",
    "bottom_right": "玉帝视角 P08 / 09",
})

# 09 入境获客手段 (3 列 grid 紧凑版 - 不溢出)
PAGES.append({
    "name": "p09_tactics",
    "title": "9 种",
    "title_em": "入境获客",
    "subtitle_meta": "P09 · 9 TACTICS · ENGAGE",
    "kicker": "I · HOW TO GET INBOUND",
    "body": """
<div class="lede">5 年窗口已经打开。<br>玉帝视角:9 种手段,选 1-2 个做透就够。</div>

<div style="display:grid;grid-template-columns:1fr 1px 1fr 1px 1fr;border-top:2px solid var(--ink);border-bottom:2px solid var(--ink);">
  <div style="padding:24px 12px 24px 0;border-right:1px solid var(--grid);display:flex;flex-direction:column;gap:6px">
    <div style="display:flex;align-items:flex-end;gap:10px">
      <div class="num" style="font-size:36px;color:var(--red);line-height:1">01</div>
      <div style="background:var(--red);color:#fff;font-family:'IBM Plex Mono';font-size:9px;padding:3px 7px;letter-spacing:.2em;font-weight:700;align-self:center">OTA</div>
    </div>
    <h3 style="font-size:17px;font-weight:900;line-height:1.25">加入国际 OTA</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.5;margin-top:4px">Booking/Agoda/Expedia/Trip.com</p>
  </div>
  <div class="divider-v"></div>
  <div style="padding:24px 12px;display:flex;flex-direction:column;gap:6px">
    <div style="display:flex;align-items:flex-end;gap:10px">
      <div class="num" style="font-size:36px;color:var(--red);line-height:1">02</div>
      <div style="background:var(--red);color:#fff;font-family:'IBM Plex Mono';font-size:9px;padding:3px 7px;letter-spacing:.2em;font-weight:700;align-self:center">官网</div>
    </div>
    <h3 style="font-size:17px;font-weight:900;line-height:1.25">官网邮件多语种</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.5;margin-top:4px">EN/JP/KO 至少 3 语</p>
  </div>
  <div class="divider-v"></div>
  <div style="padding:24px 0 24px 12px;border-right:none;display:flex;flex-direction:column;gap:6px;border-right:0">
    <div style="display:flex;align-items:flex-end;gap:10px">
      <div class="num" style="font-size:36px;color:var(--red);line-height:1">03</div>
      <div style="background:var(--red);color:#fff;font-family:'IBM Plex Mono';font-size:9px;padding:3px 7px;letter-spacing:.2em;font-weight:700;align-self:center">导览</div>
    </div>
    <h3 style="font-size:17px;font-weight:900;line-height:1.25">外文导览 + 标识</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.5;margin-top:4px">Google Maps/餐厅/服务点</p>
  </div>
</div>

<div style="display:grid;grid-template-columns:1fr 1px 1fr 1px 1fr;border-bottom:2px solid var(--ink)">
  <div style="padding:24px 12px 24px 0;border-right:1px solid var(--grid);display:flex;flex-direction:column;gap:6px">
    <div style="display:flex;align-items:flex-end;gap:10px">
      <div class="num" style="font-size:36px;color:var(--red);line-height:1">04</div>
      <div style="background:var(--red);color:#fff;font-family:'IBM Plex Mono';font-size:9px;padding:3px 7px;letter-spacing:.2em;font-weight:700;align-self:center">支付</div>
    </div>
    <h3 style="font-size:17px;font-weight:900;line-height:1.25">信用卡 + 离境退税</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.5;margin-top:4px">Visa/Master/银联<br>+ 即买即退</p>
  </div>
  <div class="divider-v"></div>
  <div style="padding:24px 12px;display:flex;flex-direction:column;gap:6px">
    <div style="display:flex;align-items:flex-end;gap:10px">
      <div class="num" style="font-size:36px;color:var(--red);line-height:1">05</div>
      <div style="background:var(--red);color:#fff;font-family:'IBM Plex Mono';font-size:9px;padding:3px 7px;letter-spacing:.2em;font-weight:700;align-self:center">渠道</div>
    </div>
    <h3 style="font-size:17px;font-weight:900;line-height:1.25">国际游客渠道</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.5;margin-top:4px">TMC/海外社/<br>学校交换项目</p>
  </div>
  <div class="divider-v"></div>
  <div style="padding:24px 0 24px 12px;border-right:0;display:flex;flex-direction:column;gap:6px">
    <div style="display:flex;align-items:flex-end;gap:10px">
      <div class="num" style="font-size:36px;color:var(--ink);line-height:1">06</div>
      <div style="background:var(--ink);color:#fff;font-family:'IBM Plex Mono';font-size:9px;padding:3px 7px;letter-spacing:.2em;font-weight:700;align-self:center">社媒</div>
    </div>
    <h3 style="font-size:17px;font-weight:900;line-height:1.25">海外社媒运营</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.5;margin-top:4px">Instagram/YouTube/<br>Google Maps</p>
  </div>
</div>

<div style="display:grid;grid-template-columns:1fr 1px 1fr 1px 1fr;border-bottom:2px solid var(--ink)">
  <div style="padding:24px 12px 24px 0;border-right:1px solid var(--grid);display:flex;flex-direction:column;gap:6px">
    <div style="display:flex;align-items:flex-end;gap:10px">
      <div class="num" style="font-size:36px;color:var(--ink);line-height:1">07</div>
      <div style="background:var(--ink);color:#fff;font-family:'IBM Plex Mono';font-size:9px;padding:3px 7px;letter-spacing:.2em;font-weight:700;align-self:center">签证</div>
    </div>
    <h3 style="font-size:17px;font-weight:900;line-height:1.25">签证便利化对接</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.5;margin-top:4px">240 小时过境<br>+ 免签城市申报</p>
  </div>
  <div class="divider-v"></div>
  <div style="padding:24px 12px;display:flex;flex-direction:column;gap:6px">
    <div style="display:flex;align-items:flex-end;gap:10px">
      <div class="num" style="font-size:36px;color:var(--ink);line-height:1">08</div>
      <div style="background:var(--ink);color:#fff;font-family:'IBM Plex Mono';font-size:9px;padding:3px 7px;letter-spacing:.2em;font-weight:700;align-self:center">服务</div>
    </div>
    <h3 style="font-size:17px;font-weight:900;line-height:1.25">国际客服务标准化</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.5;margin-top:4px">24h 多语客服<br>+ 紧急响应</p>
  </div>
  <div class="divider-v"></div>
  <div style="padding:24px 0 24px 12px;border-right:0;display:flex;flex-direction:column;gap:6px">
    <div style="display:flex;align-items:flex-end;gap:10px">
      <div class="num" style="font-size:36px;color:var(--ink);line-height:1">09</div>
      <div style="background:var(--ink);color:#fff;font-family:'IBM Plex Mono';font-size:9px;padding:3px 7px;letter-spacing:.2em;font-weight:700;align-self:center">申报</div>
    </div>
    <h3 style="font-size:17px;font-weight:900;line-height:1.25">政策窗口主动申报</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.5;margin-top:4px">智慧旅游基金<br>+ 文创专项</p>
  </div>
</div>

<div style="margin-top:24px;background:var(--red);color:#fff;padding:18px 24px;display:flex;justify-content:space-between;align-items:center">
  <div style="font-family:'IBM Plex Mono';font-size:12px;letter-spacing:.32em;font-weight:600;opacity:.85">ENGAGE</div>
  <div style="font-family:'Noto Sans SC',sans-serif;font-size:18px;font-weight:900;letter-spacing:.04em;text-align:center;flex:1;padding:0 18px">你在哪个阶段? <span style="display:inline-block;width:8px;height:8px;background:#fff;border-radius:50%;vertical-align:middle"></span> 评论区 1-9 · 我来诊断</div>
  <div style="font-family:'IBM Plex Mono';font-size:11px;letter-spacing:.18em;font-weight:600">DM OPEN</div>
</div>
""",
    "bottom_left": "P09 / 09 · 行动清单",
    "bottom_right": "2026.07.14 · 玉帝视角",
})

# ========== HTML 生成 ==========

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


# ========== 主流程 ==========

if __name__ == "__main__":
    print(f"开始生成 {len(PAGES)} 张 (V3.1 均匀布局+外资+获客清单)...")

    # 1. 写所有 HTML
    for i, page in enumerate(PAGES, 1):
        html = build_html(page, i, len(PAGES))
        html_path = OUT_DIR / f"{i:02d}_{page['name']}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  ✅ HTML [{i:02d}/{len(PAGES):02d}] {html_path.name}")

    print("\n✅ HTML 写完,等待用 Playwright 渲染...")
    print(f"输出目录: {OUT_DIR}")
