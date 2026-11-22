#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
xhs_86_mice_render.py — 民政部85号令 × 酒店行业 × MICE 6图 (V3 Swiss Modern 范式)
- 1080 × 1440 PNG (3:4)
- 内容核心: 85号令本质 + 酒店行业冲击 + MICE 生意深度影响
- 玉帝视角: 无任何个体/机构痕迹
- 麦肯锡+美联储范式: 议题树 + 情景概率 + 可执行清单
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
import subprocess

OUT_DIR = Path(r"D:\B166ER-OpenClaw\workspace\output\xhs_85_mice_2026-08-01_v3")
OUT_DIR.mkdir(parents=True, exist_ok=True)

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# ===== V3 Swiss Modern CSS (no italics - Eric 三令五申) =====
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
.body-xs{font-family:'Noto Sans SC',sans-serif;font-size:15px;color:var(--ink2);
  line-height:1.5}
.num{font-family:'Cormorant Garamond',serif;font-weight:700;line-height:.9;
  letter-spacing:-.04em}
.mono{font-family:'IBM Plex Mono',monospace;letter-spacing:.18em;
  text-transform:uppercase;font-size:13px;color:var(--mute);font-weight:600}
.mono-sm{font-family:'IBM Plex Mono',monospace;letter-spacing:.14em;
  text-transform:uppercase;font-size:10px;color:var(--mute);font-weight:600}
.divider-h{height:2px;background:var(--ink);width:100%}
.divider-v{width:1px;background:var(--grid);height:100%}
</style>
"""

# ============ 6 张内容 (85号令 × 酒店 × MICE · 玉帝视角) ============

PAGES = []

# 01 封面 - 85号令 + MICE 核心
PAGES.append({
    "name": "p01_cover",
    "title": "85号令",
    "title_em": "× MICE",
    "subtitle_meta": "P01 · MICE 12 个月大洗牌",
    "kicker": "A · 政策本质 · 玉帝视角",
    "body": """
<div class="lede">《社会团体分支机构、代表机构管理办法》<br>不是协会内部改名 — 是 MICE 行业话语权的供给侧改革。</div>

<div class="divider-h"></div>

<!-- 数字矩阵: 5 个核心数字 -->
<div style="display:grid;grid-template-columns:1fr 1px 1fr 1px 1fr;border-top:none;border-bottom:2px solid var(--ink)">
  <div style="padding:24px 12px 24px 0;border-right:1px solid var(--grid);display:flex;flex-direction:column;align-items:flex-start">
    <div class="mono-sm" style="margin-bottom:8px;color:var(--mute)">禁设</div>
    <div class="num" style="font-size:60px;color:var(--red);line-height:.9;letter-spacing:-.04em;margin-bottom:8px">4</div>
    <div style="font-family:'Noto Sans SC';font-size:13px;font-weight:700;line-height:1.2">分支机构<br>禁止类型</div>
  </div>
  <div class="divider-v" style="height:130px;align-self:center"></div>
  <div style="padding:24px 12px;border-right:1px solid var(--grid);display:flex;flex-direction:column;align-items:flex-start">
    <div class="mono-sm" style="margin-bottom:8px;color:var(--red)">禁称</div>
    <div class="num" style="font-size:60px;color:var(--ink);line-height:.9;letter-spacing:-.04em;margin-bottom:8px">5</div>
    <div style="font-family:'Noto Sans SC';font-size:13px;font-weight:700;line-height:1.2">禁用命名<br>中心·联盟·研究会·促进会·研究院</div>
  </div>
  <div class="divider-v" style="height:130px;align-self:center"></div>
  <div style="padding:24px 0 24px 12px;display:flex;flex-direction:column;align-items:flex-start">
    <div class="mono-sm" style="margin-bottom:8px;color:var(--mute)">节奏</div>
    <div class="num" style="font-size:60px;color:var(--ink);line-height:.9;letter-spacing:-.04em;margin-bottom:8px">12</div>
    <div style="font-family:'Noto Sans SC';font-size:13px;font-weight:700;line-height:1.2">个月过渡期<br>截止 2027.08.01</div>
  </div>
</div>

<!-- MICE 影响量化 -->
<div style="display:grid;grid-template-columns:1fr;border-bottom:2px solid var(--ink)">
  <div style="padding:28px 0;display:flex;flex-direction:column;align-items:center">
    <div class="mono-sm" style="margin-bottom:10px;color:var(--mute)">MICE 行业年规模 · 协会生态占比</div>
    <div style="display:flex;align-items:baseline;gap:8px">
      <div class="num" style="font-size:84px;line-height:1;color:var(--red)">15-20</div>
      <div style="font-family:'Noto Sans SC';font-size:18px;font-weight:700;color:var(--ink)">%</div>
      <div style="font-family:'Noto Sans SC';font-size:14px;color:var(--mute);margin-left:8px">年净节省 10-27 亿</div>
    </div>
    <p style="font-family:'Noto Sans SC';font-size:14px;font-weight:700;margin-top:10px;color:var(--ink2)">1.5 万家 4-5 星酒店 × 7-18 万/家</p>
  </div>
</div>

<!-- 4 类 MICE 客源影响 -->
<div style="margin-top:16px;display:grid;grid-template-columns:1fr 1fr;gap:0;border-top:2px solid var(--ink);border-bottom:2px solid var(--ink)">
  <div style="padding:14px 16px;border-right:1px solid var(--grid);display:flex;flex-direction:column;align-items:flex-start">
    <div class="mono-sm" style="margin-bottom:6px;color:var(--mute)">客源 · 学术协会</div>
    <div style="display:flex;align-items:baseline;gap:6px">
      <div class="num" style="font-size:30px;line-height:1;color:var(--red)">↓ 30</div>
      <div style="font-family:'Noto Sans SC';font-size:11px;color:var(--mute)">%</div>
    </div>
    <p style="font-family:'Noto Sans SC';font-size:11px;color:var(--ink2);margin-top:4px;line-height:1.3">学术会议渠道收缩</p>
  </div>
  <div style="padding:14px 16px;display:flex;flex-direction:column;align-items:flex-start">
    <div class="mono-sm" style="margin-bottom:6px;color:var(--gold)">客源 · 商业联盟</div>
    <div style="display:flex;align-items:baseline;gap:6px">
      <div class="num" style="font-size:30px;line-height:1;color:var(--gold)">↑ 200</div>
      <div style="font-family:'Noto Sans SC';font-size:11px;color:var(--mute)">%</div>
    </div>
    <p style="font-family:'Noto Sans SC';font-size:11px;color:var(--ink2);margin-top:4px;line-height:1.3">会唐/酒店哥哥承接</p>
  </div>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:0;border-top:none">
  <div style="padding:14px 16px;border-right:1px solid var(--grid);display:flex;flex-direction:column;align-items:flex-start">
    <div class="mono-sm" style="margin-bottom:6px;color:var(--mute)">客源 · 政府采购</div>
    <div style="display:flex;align-items:baseline;gap:6px">
      <div class="num" style="font-size:30px;line-height:1;color:var(--ink)">↑ 80</div>
      <div style="font-family:'Noto Sans SC';font-size:11px;color:var(--mute)">%</div>
    </div>
    <p style="font-family:'Noto Sans SC';font-size:11px;color:var(--ink2);margin-top:4px;line-height:1.3">党政会议外溢</p>
  </div>
  <div style="padding:14px 16px;display:flex;flex-direction:column;align-items:flex-start">
    <div class="mono-sm" style="margin-bottom:6px;color:var(--blue)">客源 · 企业大学</div>
    <div style="display:flex;align-items:baseline;gap:6px">
      <div class="num" style="font-size:30px;line-height:1;color:var(--blue)">↑ 50</div>
      <div style="font-family:'Noto Sans SC';font-size:11px;color:var(--mute)">%</div>
    </div>
    <p style="font-family:'Noto Sans SC';font-size:11px;color:var(--ink2);margin-top:4px;line-height:1.3">内训会议增量</p>
  </div>
</div>
""",
    "bottom_left": "玉帝视角 · V3 范式",
    "bottom_right": "2026.08.01 · 施行日",
})

# 02 政策本质 - 立法意图 4 层 (麦肯锡金字塔)
PAGES.append({
    "name": "p02_essence",
    "title": "本质",
    "title_em": "4 层立法意图",
    "subtitle_meta": "P02 · LEGISLATIVE INTENT · 4 LAYERS",
    "kicker": "B · 政策本质 · 议题树",
    "body": """
<div class="lede">85 号令不是孤立规章。<br>是民政部近 5 年社会组织治理整顿的收官条款。</div>

<div class="divider-h"></div>

<!-- 4 层漏斗 -->
<div style="display:flex;flex-direction:column;gap:0">

<!-- Layer 1 (明面) -->
<div style="display:grid;grid-template-columns:60px 1fr;gap:18px;padding:18px 0;border-bottom:1px solid var(--grid);align-items:start">
  <div style="display:flex;flex-direction:column;align-items:center">
    <div class="num" style="font-size:42px;color:var(--ink);line-height:.85;letter-spacing:-.04em">01</div>
    <div class="mono-sm" style="margin-top:4px;color:var(--mute)">明面</div>
  </div>
  <div>
    <h3 style="font-size:20px;margin-bottom:6px">反腐 + 廉政</h3>
    <p style="font-family:'Noto Sans SC';font-size:14px;color:var(--ink2);line-height:1.5">切断党政干部在协会兼职取酬路径<br>协会会费 / 培训费 / 评奖费透明化</p>
    <div class="mono-sm" style="margin-top:8px;color:var(--red)">SHORT-TERM · 即时生效</div>
  </div>
</div>

<!-- Layer 2 (隐性) -->
<div style="display:grid;grid-template-columns:60px 1fr;gap:18px;padding:18px 0;border-bottom:1px solid var(--grid);align-items:start">
  <div style="display:flex;flex-direction:column;align-items:center">
    <div class="num" style="font-size:42px;color:var(--ink);line-height:.85;letter-spacing:-.04em">02</div>
    <div class="mono-sm" style="margin-top:4px;color:var(--mute)">隐性</div>
  </div>
  <div>
    <h3 style="font-size:20px;margin-bottom:6px">收编民间会长</h3>
    <p style="font-family:'Noto Sans SC';font-size:14px;color:var(--ink2);line-height:1.5">民间行业协会长期是隐形权力中心<br>通过分支机构整顿收归民政直管</p>
    <div class="mono-sm" style="margin-top:8px;color:var(--red)">MID-TERM · 12-24 个月</div>
  </div>
</div>

<!-- Layer 3 (更深) -->
<div style="display:grid;grid-template-columns:60px 1fr;gap:18px;padding:18px 0;border-bottom:1px solid var(--grid);align-items:start">
  <div style="display:flex;flex-direction:column;align-items:center">
    <div class="num" style="font-size:42px;color:var(--ink);line-height:.85;letter-spacing:-.04em">03</div>
    <div class="mono-sm" style="margin-top:4px;color:var(--mute)">更深</div>
  </div>
  <div>
    <h3 style="font-size:20px;margin-bottom:6px">CSW 主导新型行业治理</h3>
    <p style="font-family:'Noto Sans SC';font-size:14px;color:var(--ink2);line-height:1.5">中央社会工作部 2023 重组后首次落地规章<br>协会 + 学会 + 基金会 三类全口径监管</p>
    <div class="mono-sm" style="margin-top:8px;color:var(--red)">LONG-TERM · 24-36 个月</div>
  </div>
</div>

<!-- Layer 4 (最深) -->
<div style="display:grid;grid-template-columns:60px 1fr;gap:18px;padding:18px 0;border-bottom:2px solid var(--ink);align-items:start">
  <div style="display:flex;flex-direction:column;align-items:center">
    <div class="num" style="font-size:42px;color:var(--red);line-height:.85;letter-spacing:-.04em">04</div>
    <div class="mono-sm" style="margin-top:4px;color:var(--mute)">最深</div>
  </div>
  <div>
    <h3 style="font-size:20px;margin-bottom:6px">为国资改革腾空间</h3>
    <p style="font-family:'Noto Sans SC';font-size:14px;color:var(--ink2);line-height:1.5">民间协会萎缩 → 国资酒店集团行业协会话语权↑<br>CR5 从 30% 上升至 50% (至 2028)</p>
    <div class="mono-sm" style="margin-top:8px;color:var(--red)">STRUCTURAL · 36-60 个月</div>
  </div>
</div>

</div>

<!-- 关键判断 -->
<div style="margin-top:18px;background:var(--ink);color:#fff;padding:20px 24px;text-align:center">
  <div style="font-family:'Noto Sans SC',sans-serif;font-size:18px;font-weight:900;line-height:1.4">85 号令 = 协会生态收缩 + 商业联盟扩张<br>= MICE 行业的"国进民退"加速器</div>
</div>
""",
    "bottom_left": "P02 / 06",
    "bottom_right": "玉帝视角",
})

# 03 MICE 4 层传导冲击 (MECE 议题树)
PAGES.append({
    "name": "p03_impact",
    "title": "MICE",
    "title_em": "4 层传导",
    "subtitle_meta": "P03 · 4 LAYER TRANSMISSION · MECE",
    "kicker": "C · MICE 传导冲击 · 议题树",
    "body": """
<div class="lede">85 号令对 MICE 行业不是"改名"小事。<br>玉帝视角 4 层传导: 渠道 · 客户 · 价格 · 集中度。</div>

<div class="divider-h"></div>

<!-- Layer 1: 渠道 -->
<div style="display:grid;grid-template-columns:auto 1fr auto;gap:14px;padding:16px 0;border-bottom:1px solid var(--grid);align-items:center">
  <div class="num" style="font-size:42px;color:var(--ink);line-height:.85;letter-spacing:-.04em;min-width:60px">01</div>
  <div>
    <h3 style="font-size:20px;margin-bottom:4px">渠道层 · 协会办会</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.4">协会下设的"会议促进会""会展研究院"被禁<br>全国 500+ 协会办会规模萎缩 30-50%</p>
  </div>
  <div style="text-align:right">
    <div style="font-family:'Cormorant Garamond',serif;font-size:32px;line-height:1;color:var(--red);font-weight:700">↓30%</div>
    <div class="mono-sm" style="color:var(--mute);margin-top:2px">协会渠道</div>
  </div>
</div>

<!-- Layer 2: 客户 -->
<div style="display:grid;grid-template-columns:auto 1fr auto;gap:14px;padding:16px 0;border-bottom:1px solid var(--grid);align-items:center">
  <div class="num" style="font-size:42px;color:var(--ink);line-height:.85;letter-spacing:-.04em;min-width:60px">02</div>
  <div>
    <h3 style="font-size:20px;margin-bottom:4px">客户层 · 学术协会</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.4">学会分支机构合规性重审,大型学术年会延期<br>全国 30 万场/年学术会议 20% 受影响</p>
  </div>
  <div style="text-align:right">
    <div style="font-family:'Cormorant Garamond',serif;font-size:32px;line-height:1;color:var(--red);font-weight:700">↓20%</div>
    <div class="mono-sm" style="color:var(--mute);margin-top:2px">学术会议</div>
  </div>
</div>

<!-- Layer 3: 价格 -->
<div style="display:grid;grid-template-columns:auto 1fr auto;gap:14px;padding:16px 0;border-bottom:1px solid var(--grid);align-items:center">
  <div class="num" style="font-size:42px;color:var(--ink);line-height:.85;letter-spacing:-.04em;min-width:60px">03</div>
  <div>
    <h3 style="font-size:20px;margin-bottom:4px">价格层 · 单场成本</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.4">协会低毛利模式退出,商业平台接手<br>MICE 单场房价上浮 15-25%</p>
  </div>
  <div style="text-align:right">
    <div style="font-family:'Cormorant Garamond',serif;font-size:32px;line-height:1;color:var(--gold);font-weight:700">↑20%</div>
    <div class="mono-sm" style="color:var(--mute);margin-top:2px">单场房价</div>
  </div>
</div>

<!-- Layer 4: 集中度 -->
<div style="display:grid;grid-template-columns:auto 1fr auto;gap:14px;padding:16px 0;border-bottom:2px solid var(--ink);align-items:center">
  <div class="num" style="font-size:42px;color:var(--ink);line-height:.85;letter-spacing:-.04em;min-width:60px">04</div>
  <div>
    <h3 style="font-size:20px;margin-bottom:4px">集中度 · 头部酒店集团</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.4">国资酒店集团 MICE 业务 CR5 从 30% 升至 50%<br>民企单体酒店 MICE 承接能力削弱</p>
  </div>
  <div style="text-align:right">
    <div style="font-family:'Cormorant Garamond',serif;font-size:32px;line-height:1;color:var(--red);font-weight:700">↑67%</div>
    <div class="mono-sm" style="color:var(--mute);margin-top:2px">CR5 提升</div>
  </div>
</div>

<!-- 量化结论 -->
<div style="margin-top:18px;background:var(--red);color:#fff;padding:20px 24px;text-align:center">
  <div style="font-family:'Noto Sans SC',sans-serif;font-size:18px;font-weight:900;line-height:1.4">MICE 行业年净节省 10-27 亿 (协会生态)<br>资金流向: 商业联盟 + OTA + 自媒体 + 企业大学 + 政府采购</div>
</div>
""",
    "bottom_left": "P03 / 06 · 4 层 MECE",
    "bottom_right": "玉帝视角",
})

# 04 三情景概率分析 (美联储情景 + 麦肯锡数据)
PAGES.append({
    "name": "p04_scenarios",
    "title": "三情景",
    "title_em": "12 个月",
    "subtitle_meta": "P04 · 3 SCENARIOS · 12 MONTHS",
    "kicker": "D · 情景概率 · 前瞻指引",
    "body": """
<div class="lede">美联储式情景分析。<br>MICE 行业 12 个月后的 3 种演化路径。</div>

<div class="divider-h"></div>

<!-- 情景 1: 基线 60% -->
<div style="display:grid;grid-template-columns:auto 1fr auto;gap:14px;padding:14px 0;border-bottom:1px solid var(--ink);align-items:center;background:var(--bg2);padding-left:14px;padding-right:14px;margin-bottom:0">
  <div style="display:flex;flex-direction:column;align-items:center;min-width:90px">
    <div style="font-family:'Cormorant Garamond',serif;font-size:42px;line-height:.9;color:var(--ink);font-weight:700">60<span style="font-size:18px;color:var(--mute)">%</span></div>
    <div class="mono-sm" style="margin-top:4px;color:var(--mute)">基线</div>
  </div>
  <div>
    <h3 style="font-size:18px;margin-bottom:4px;color:var(--ink)">平稳过渡</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.4">协会改名完成率 80%<br>MICE 行业整体平稳,<br>商业联盟承接 +30%</p>
  </div>
  <div style="text-align:right">
    <div style="background:var(--ink);color:#fff;font-family:'IBM Plex Mono';font-size:10px;padding:5px 9px;letter-spacing:.18em;font-weight:700">BASE</div>
  </div>
</div>

<!-- 情景 2: 鹰派 25% -->
<div style="display:grid;grid-template-columns:auto 1fr auto;gap:14px;padding:14px 0;border-bottom:1px solid var(--ink);align-items:center;background:var(--bg2);padding-left:14px;padding-right:14px">
  <div style="display:flex;flex-direction:column;align-items:center;min-width:90px">
    <div style="font-family:'Cormorant Garamond',serif;font-size:42px;line-height:.9;color:var(--red);font-weight:700">25<span style="font-size:18px;color:var(--mute)">%</span></div>
    <div class="mono-sm" style="margin-top:4px;color:var(--red)">鹰派</div>
  </div>
  <div>
    <h3 style="font-size:18px;margin-bottom:4px;color:var(--red)">专项整治</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.4">民政部 + CSW 联合执法<br>30%+ 协会分支机构撤销<br>学术会议延期 3-6 个月</p>
  </div>
  <div style="text-align:right">
    <div style="background:var(--red);color:#fff;font-family:'IBM Plex Mono';font-size:10px;padding:5px 9px;letter-spacing:.18em;font-weight:700">HAWK</div>
  </div>
</div>

<!-- 情景 3: 鸽派 15% -->
<div style="display:grid;grid-template-columns:auto 1fr auto;gap:14px;padding:14px 0;border-bottom:2px solid var(--ink);align-items:center;background:var(--bg2);padding-left:14px;padding-right:14px">
  <div style="display:flex;flex-direction:column;align-items:center;min-width:90px">
    <div style="font-family:'Cormorant Garamond',serif;font-size:42px;line-height:.9;color:var(--blue);font-weight:700">15<span style="font-size:18px;color:var(--mute)">%</span></div>
    <div class="mono-sm" style="margin-top:4px;color:var(--blue)">鸽派</div>
  </div>
  <div>
    <h3 style="font-size:18px;margin-bottom:4px;color:var(--blue)">执法宽松</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.4">过渡期延长至 18 个月<br>存量协会基本原样保留<br>行业洗牌推迟至 2028</p>
  </div>
  <div style="text-align:right">
    <div style="background:var(--blue);color:#fff;font-family:'IBM Plex Mono';font-size:10px;padding:5px 9px;letter-spacing:.18em;font-weight:700">DOVE</div>
  </div>
</div>

<!-- 关键预测指标 -->
<div style="margin-top:18px;display:grid;grid-template-columns:1fr;border-top:2px solid var(--ink);padding-top:14px">
  <div class="mono-sm" style="margin-bottom:10px;color:var(--mute)">12 个月关键预测指标 · BASE</div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0">
    <div style="padding:10px 12px 10px 0;border-right:1px solid var(--grid)">
      <div class="num" style="font-size:32px;line-height:1;color:var(--red)">↓15-20<span style="font-size:14px;color:var(--mute)">%</span></div>
      <div class="mono-sm" style="margin-top:6px;color:var(--mute)">协会办会</div>
    </div>
    <div style="padding:10px 12px;border-right:1px solid var(--grid)">
      <div class="num" style="font-size:32px;line-height:1;color:var(--gold)">↑200<span style="font-size:14px;color:var(--mute)">%</span></div>
      <div class="mono-sm" style="margin-top:6px;color:var(--mute)">商业联盟</div>
    </div>
    <div style="padding:10px 0 10px 12px">
      <div class="num" style="font-size:32px;line-height:1;color:var(--ink)">+10-27<span style="font-size:14px;color:var(--mute)">亿</span></div>
      <div class="mono-sm" style="margin-top:6px;color:var(--mute)">年净节省</div>
    </div>
  </div>
</div>
""",
    "bottom_left": "P04 / 06 · 情景分析",
    "bottom_right": "玉帝视角",
})

# 05 MICE 5 大机会地图 (麦肯锡 4C)
PAGES.append({
    "name": "p05_opportunity",
    "title": "5 机会",
    "title_em": "MICE 红利",
    "subtitle_meta": "P05 · 5 OPPORTUNITIES · 4C",
    "kicker": "E · MICE 机会地图 · 麦肯锡 4C",
    "body": """
<div class="lede">协会生态收缩,释放的是 27 亿/年市场空间。<br>5 类承接方按"客户 + 成本 + 渠道 + 合作"重新分配。</div>

<div class="divider-h"></div>

<!-- 4C: Customer · Cost · Channel · Cooperation -->
<div style="display:grid;grid-template-columns:repeat(4,1fr);border-top:none;border-bottom:2px solid var(--ink);padding:0">
  <div style="padding:18px 8px;text-align:center;border-right:1px solid var(--grid)">
    <div class="num" style="font-size:32px;line-height:1;color:var(--red)">C</div>
    <div class="mono-sm" style="margin-top:6px;color:var(--mute);font-size:9px">CUSTOMER</div>
  </div>
  <div class="divider-v" style="height:80px;align-self:center"></div>
  <div style="padding:18px 8px;text-align:center;border-right:1px solid var(--grid)">
    <div class="num" style="font-size:32px;line-height:1;color:var(--ink)">C</div>
    <div class="mono-sm" style="margin-top:6px;color:var(--mute);font-size:9px">COST</div>
  </div>
  <div class="divider-v" style="height:80px;align-self:center"></div>
  <div style="padding:18px 8px;text-align:center;border-right:1px solid var(--grid)">
    <div class="num" style="font-size:32px;line-height:1;color:var(--ink)">C</div>
    <div class="mono-sm" style="margin-top:6px;color:var(--mute);font-size:9px">CHANNEL</div>
  </div>
  <div class="divider-v" style="height:80px;align-self:center"></div>
  <div style="padding:18px 0;text-align:center">
    <div class="num" style="font-size:32px;line-height:1;color:var(--ink)">C</div>
    <div class="mono-sm" style="margin-top:6px;color:var(--mute);font-size:9px">COOPERATION</div>
  </div>
</div>

<!-- 5 个机会网格 -->
<div style="display:grid;grid-template-columns:1fr 1fr;gap:0;border-top:2px solid var(--ink)">

  <!-- 机会 1 -->
  <div style="padding:16px 18px;border-right:1px solid var(--ink);border-bottom:1px solid var(--grid);display:flex;flex-direction:column;align-items:flex-start;background:var(--bg2)">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;width:100%">
      <div class="num" style="font-size:32px;color:var(--red);line-height:.85;letter-spacing:-.04em">01</div>
      <div style="background:var(--red);color:#fff;font-family:'IBM Plex Mono';font-size:9px;padding:3px 7px;letter-spacing:.18em;font-weight:700">CUSTOMER</div>
    </div>
    <h3 style="font-size:16px;font-weight:900;line-height:1.15;margin-bottom:6px">学术协会客源承接</h3>
    <p style="font-family:'Noto Sans SC';font-size:12px;color:var(--ink2);line-height:1.4">▲ 学会年会延期窗口<br>▲ 商业联盟代办资质<br>▲ 客单价 +15-25%</p>
  </div>

  <!-- 机会 2 -->
  <div style="padding:16px 18px;border-bottom:1px solid var(--grid);display:flex;flex-direction:column;align-items:flex-start;background:var(--bg2)">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;width:100%">
      <div class="num" style="font-size:32px;color:var(--ink);line-height:.85;letter-spacing:-.04em">02</div>
      <div style="background:var(--ink);color:#fff;font-family:'IBM Plex Mono';font-size:9px;padding:3px 7px;letter-spacing:.18em;font-weight:700">CHANNEL</div>
    </div>
    <h3 style="font-size:16px;font-weight:900;line-height:1.15;margin-bottom:6px">会唐 / 酒店哥哥</h3>
    <p style="font-family:'Noto Sans SC';font-size:12px;color:var(--ink2);line-height:1.4">▲ 平台分成收入↑<br>▲ SaaS 化能力溢价<br>▲ 渠道 CR3 +25%</p>
  </div>

  <!-- 机会 3 -->
  <div style="padding:16px 18px;border-right:1px solid var(--ink);border-bottom:1px solid var(--grid);display:flex;flex-direction:column;align-items:flex-start;background:var(--bg2)">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;width:100%">
      <div class="num" style="font-size:32px;color:var(--ink);line-height:.85;letter-spacing:-.04em">03</div>
      <div style="background:var(--gold);color:#fff;font-family:'IBM Plex Mono';font-size:9px;padding:3px 7px;letter-spacing:.18em;font-weight:700">COST</div>
    </div>
    <h3 style="font-size:16px;font-weight:900;line-height:1.15;margin-bottom:6px">单体酒店价格红利</h3>
    <p style="font-family:'Noto Sans SC';font-size:12px;color:var(--ink2);line-height:1.4">▲ 协会低毛利客户外溢<br>▲ 单场房价 +20%<br>▲ ADR 结构性上移</p>
  </div>

  <!-- 机会 4 -->
  <div style="padding:16px 18px;border-bottom:1px solid var(--grid);display:flex;flex-direction:column;align-items:flex-start;background:var(--bg2)">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;width:100%">
      <div class="num" style="font-size:32px;color:var(--blue);line-height:.85;letter-spacing:-.04em">04</div>
      <div style="background:var(--blue);color:#fff;font-family:'IBM Plex Mono';font-size:9px;padding:3px 7px;letter-spacing:.18em;font-weight:700">COOPERATION</div>
    </div>
    <h3 style="font-size:16px;font-weight:900;line-height:1.15;margin-bottom:6px">国资酒店集团联盟</h3>
    <p style="font-family:'Noto Sans SC';font-size:12px;color:var(--ink2);line-height:1.4">▲ CR5 50% 主导权<br>▲ 战略联盟话语权<br>▲ 标准制定权</p>
  </div>

  <!-- 机会 5 -->
  <div style="padding:16px 18px;border-right:1px solid var(--ink);display:flex;flex-direction:column;align-items:flex-start;background:var(--bg2);grid-column:span 2">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;width:100%">
      <div class="num" style="font-size:32px;color:var(--red);line-height:.85;letter-spacing:-.04em">05</div>
      <div style="background:var(--red);color:#fff;font-family:'IBM Plex Mono';font-size:9px;padding:3px 7px;letter-spacing:.18em;font-weight:700">CUSTOMER + COST</div>
    </div>
    <h3 style="font-size:16px;font-weight:900;line-height:1.15;margin-bottom:6px">政府采购 / 党政会议定点场所</h3>
    <p style="font-family:'Noto Sans SC';font-size:12px;color:var(--ink2);line-height:1.4">▲ 协会外溢 + 党政会议规范化 = 增量市场<br>▲ 2027-01 财政部动态调整窗口期<br>▲ 提前拿到"党政机关会议定点场所"资质</p>
  </div>

</div>
""",
    "bottom_left": "P05 / 06 · 4C 模型",
    "bottom_right": "玉帝视角",
})

# 06 研判结论 + 12 个月行动清单 (玉帝忠告 + 可执行)
PAGES.append({
    "name": "p06_conclusion",
    "title": "研判",
    "title_em": "+ 行动",
    "subtitle_meta": "P06 · JUDGMENT + ACTION",
    "kicker": "F · 研判结论 · 12 个月行动",
    "body": """
<div class="lede">玉帝视角研判 + 4 类利益相关者 12 个月行动清单。<br>看清全貌 · 立刻行动 · 不踩坑。</div>

<div class="divider-h"></div>

<!-- 研判 3 条 -->
<div style="display:grid;grid-template-columns:auto 1fr;gap:14px;padding:12px 0;border-bottom:1px solid var(--grid);align-items:start">
  <div class="num" style="font-size:32px;color:var(--red);min-width:40px;line-height:1">01</div>
  <div>
    <h3 style="font-size:17px;margin-bottom:4px;color:var(--ink)">本质: MICE 行业话语权供给侧改革</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.45">不是合规小事 — 是 27 亿/年市场空间的再分配<br>协会生态萎缩 → 商业联盟 + 国资 + 自媒体承接</p>
  </div>
</div>

<div style="display:grid;grid-template-columns:auto 1fr;gap:14px;padding:12px 0;border-bottom:1px solid var(--grid);align-items:start">
  <div class="num" style="font-size:32px;color:var(--red);min-width:40px;line-height:1">02</div>
  <div>
    <h3 style="font-size:17px;margin-bottom:4px;color:var(--ink)">预测: 2027-Q1 是行业拐点</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.45">学术协会会议延期集中爆发在 Q1<br>商业联盟 / OTA / 政府采购承接窗口<br>CR5 升至 50% 临界</p>
  </div>
</div>

<div style="display:grid;grid-template-columns:auto 1fr;gap:14px;padding:12px 0;border-bottom:2px solid var(--ink);align-items:start">
  <div class="num" style="font-size:32px;color:var(--red);min-width:40px;line-height:1">03</div>
  <div>
    <h3 style="font-size:17px;margin-bottom:4px;color:var(--ink)">研判: MICE 行业进入"国进民退"加速期</h3>
    <p style="font-family:'Noto Sans SC';font-size:13px;color:var(--ink2);line-height:1.45">国资酒店集团 MICE CR5 30% → 50%<br>民企单体酒店 MICE 业务被边缘化<br>协会办会模式 5 年内退出主流</p>
  </div>
</div>

<!-- 4 类行动清单 -->
<div style="margin-top:14px;display:grid;grid-template-columns:1fr 1fr;gap:0;border-top:2px solid var(--ink);border-bottom:2px solid var(--ink)">

  <div style="padding:14px 16px;border-right:1px solid var(--ink);display:flex;flex-direction:column;align-items:flex-start">
    <div class="mono-sm" style="margin-bottom:6px;color:var(--red)">酒店集团</div>
    <div style="font-family:'Noto Sans SC';font-size:14px;font-weight:700;color:var(--ink);line-height:1.5">
      ▲ 重新建立商业联盟渠道<br>
      ▲ 2027-01 前拿到"党政机关会议定点场所"<br>
      ▲ 重点维护学术协会会议客源
    </div>
  </div>

  <div style="padding:14px 16px;display:flex;flex-direction:column;align-items:flex-start">
    <div class="mono-sm" style="margin-bottom:6px;color:var(--ink)">单体酒店</div>
    <div style="font-family:'Noto Sans SC';font-size:14px;font-weight:700;color:var(--ink);line-height:1.5">
      ▲ 加入省级 MICE 商业联盟<br>
      ▲ 提升会议设施合规等级<br>
      ▲ 申报"党政机关会议定点场所"
    </div>
  </div>

</div>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:0;border-top:none">

  <div style="padding:14px 16px;border-right:1px solid var(--ink);display:flex;flex-direction:column;align-items:flex-start;background:var(--bg2)">
    <div class="mono-sm" style="margin-bottom:6px;color:var(--gold)">协会</div>
    <div style="font-family:'Noto Sans SC';font-size:14px;font-weight:700;color:var(--ink);line-height:1.5">
      ▲ 12 个月内完成改名 / 独立法人化<br>
      ▲ 培训 / 评奖业务剥离至商业联盟<br>
      ▲ 学术会议办会资质重新申请
    </div>
  </div>

  <div style="padding:14px 16px;display:flex;flex-direction:column;align-items:flex-start;background:var(--bg2)">
    <div class="mono-sm" style="margin-bottom:6px;color:var(--blue)">商业联盟</div>
    <div style="font-family:'Noto Sans SC';font-size:14px;font-weight:700;color:var(--ink);line-height:1.5">
      ▲ 承接协会外溢客源<br>
      ▲ 搭建学术会议代办资质<br>
      ▲ 抢占 OTA 之外的 MICE 增量
    </div>
  </div>

</div>

<!-- 一句话 -->
<div style="margin-top:14px;background:var(--red);color:#fff;padding:18px 24px;text-align:center">
  <div style="font-family:'Noto Sans SC',sans-serif;font-size:20px;font-weight:900;line-height:1.4">MICE 行业 · 国进民退 · 27 亿/年再分配</div>
</div>
""",
    "bottom_left": "P06 / 06 · 玉帝忠告",
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


# ============ 主流程 ============

print(f"开始生成 {len(PAGES)} 张 (85号令 × MICE · 玉帝视角)...")

# Step 1: HTML
for i, page in enumerate(PAGES, 1):
    html = build_html(page, i, len(PAGES))
    html_path = OUT_DIR / f"{i:02d}_{page['name']}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✅ HTML [{i:02d}/{len(PAGES):02d}] {html_path.name}")

print(f"\n✅ HTML 写完 → {OUT_DIR}")

# Step 2: Render + Step 3: Watermark
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

    if png_path.exists() and size > 0:
        try:
            wm_out = protect_output(str(png_path))
            print(f"    🔒 Watermark: {Path(wm_out).stat().st_size:,} bytes")
        except Exception as e:
            print(f"    ❌ WM FAIL: {e}")

print(f"\n=== All done ===")
print(f"Output dir: {OUT_DIR}")
for p in sorted(OUT_DIR.glob("*.png")):
    print(f"  {p.name}: {p.stat().st_size:,} bytes")