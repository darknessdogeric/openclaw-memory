#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
gen_xhs_h1_overview.py — 酒店行业 2026 H1 全景画像
小红书范式 · 9 张连图 · 1080×1440 (3:4) · DSF=2 (Retina)
基于 xhs_h1_review 风格 (米白底 + 深红 + 深墨蓝 + 金棕 + 翠绿)
数据基线: 2026 H1 中国酒店业 v2.0 (B166ER 8/2 17:15)
"""
import os, sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_h1_overview_2026-08-16")
OUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1440
DSF = 2
DATE = "2026.08.16"
SIG = "ERIC的B166ER出品"


def slide_html(body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><title>H1 2026</title>
<link rel="stylesheet" href="style.css"></head>
<body><div class="layout">
{body}
<div class="bottom-section">
  <div class="signature">
    <span class="left">ERIC · HOTEL · H1 2026</span>
    <span class="center">{SIG}</span>
    <span class="right">{DATE} · v1.0</span>
  </div>
</div>
</div></body></html>
"""


SLIDES = []

# ============= 01 封面: 一句话震撼 =============
SLIDES.append({
    "name": "slide_01",
    "body": """
<div class="status-bar"><span>2026 H1 · HOTEL INDUSTRY · 01 / 09</span><span>ERIC 出品</span></div>
<div class="subtitle-bar"><span class="zh">一句话震撼</span><span class="en">/ THE ONE-LINER · 2026 H1</span></div>
<div class="main-title">看似 <span class="accent">下滑</span><br>实则 <span class="accent-blue">换轨</span><br>正在 <span class="accent-gold">质升</span></div>
<div class="lead">不是衰退 · 是 <span class="accent">高基数</span> + <span class="accent-blue">供给升级</span> + <span class="accent-green">入口换轨</span> 三重叠加。<br>看清真故事,避开 K 型陷阱。</div>
<div class="section">
  <div class="section-title">数据快照 <span class="en">/ SNAPSHOT</span></div>
  <div class="kpi-row">
    <div class="kpi-cell"><div class="label">餐饮收入 H1</div><div class="val">2.83<span style="font-size:30px">万亿</span></div><div class="note">+2.8% 反超商品零售</div></div>
    <div class="kpi-cell"><div class="label">民间投资 H1</div><div class="val dark">-8.5<span style="font-size:30px">%</span></div><div class="note">⚠️ 断崖 · 但头部逆势扩张</div></div>
    <div class="kpi-cell"><div class="label">入境民宿</div><div class="val blue">+60<span style="font-size:30px">%</span></div><div class="note">新疆/山西/贵州 爆发</div></div>
  </div>
</div>
<div class="section">
  <div class="findings-title">3 大反差 <span class="en">/ 3 COUNTER-INTUITIVE</span></div>
  <div class="finding">
    <div class="num">01</div><div class="body">
      <div class="head normal"><span class="accent">"消费降级"是错觉</span></div>
      <div class="text">餐饮 <strong>+2.8%</strong> 反超商品 <strong>+1.1%</strong> · 消费者从"买"转向"体验"。</div>
    </div>
  </div>
  <div class="finding">
    <div class="num">02</div><div class="body">
      <div class="head normal"><span class="accent">民间投资 -8.5% ≠ 酒店萧条</span></div>
      <div class="text">头部连锁逆势扩张 · 华住三线占比 <strong>41%</strong> · 待开业 <strong>54%</strong>。</div>
    </div>
  </div>
  <div class="finding">
    <div class="num">03</div><div class="body">
      <div class="head normal"><span class="accent">入境游"小城化"</span></div>
      <div class="text">新疆/山西/贵州 <strong>+60%</strong> · <span class="em">外资不必争一线</span>。</div>
    </div>
  </div>
</div>
""",
})

# ============= 02 六大数字 =============
SLIDES.append({
    "name": "slide_02",
    "body": """
<div class="status-bar"><span>2026 H1 · 6 KEY NUMBERS · 02 / 09</span><span>ERIC 出品</span></div>
<div class="subtitle-bar"><span class="zh">6 大数字</span><span class="en">/ 6 KEY NUMBERS · NBS + CHAT</span></div>
<div class="main-title">一图<span class="accent">速览</span> H1<br>酒店行业<span class="accent-blue">全景</span></div>
<div class="lead">国家统计局 · STR · 迈点 · 头部财报 —— <span class="accent">90% 已发</span>。</div>
<div class="section">
  <div class="section-title">宏观底盘 <span class="en">/ MACRO BASE</span></div>
  <div class="kpi-row">
    <div class="kpi-cell"><div class="label">社零总额 H1</div><div class="val">24.87<span style="font-size:28px">万亿</span></div><div class="note">+1.3% 弱复苏</div></div>
    <div class="kpi-cell"><div class="label">餐饮收入 H1</div><div class="val">2.83<span style="font-size:28px">万亿</span></div><div class="note">+2.8% ⭐ 反超商品</div></div>
    <div class="kpi-cell"><div class="label">民间投资 H1</div><div class="val dark">-8.5<span style="font-size:30px">%</span></div><div class="note">⛔ 断崖 · 9.1pct</div></div>
  </div>
</div>
<div class="section">
  <div class="section-title">行业指标 <span class="en">/ INDUSTRY METRICS</span></div>
  <div class="kpi-row">
    <div class="kpi-cell"><div class="label">凯悦中国 Q1</div><div class="val blue">+12.4<span style="font-size:28px">%</span></div><div class="note">RevPAR · 国际领跑</div></div>
    <div class="kpi-cell"><div class="label">入境游客民宿</div><div class="val gold">+60<span style="font-size:28px">%</span></div><div class="note">新疆/山西/贵州</div></div>
    <div class="kpi-cell"><div class="label">REITs</div><div class="val">21.51<span style="font-size:28px">亿</span></div><div class="note">远洲酒店 · 7/14</div></div>
  </div>
</div>
<div class="bottom-section">
  <div class="bottom-row">
    <div class="source-block">
      <div class="label">SCOPE <span class="en">范围</span></div>
      <div class="text">2026-01 ~ 2026-06 · L1 国家统计局 + L2 头部财报 + L3 行业报告</div>
    </div>
    <div class="insight-block">
      <div class="label">INSIGHT <span class="en">洞察</span></div>
      <div class="text"><strong>服务</strong>反超<strong>商品</strong> · <strong>高端</strong>领跑<strong>经济</strong> · <strong>头部</strong>逆势<strong>底谷</strong></div>
    </div>
  </div>
</div>
""",
})

# ============= 03 K 型分化 =============
SLIDES.append({
    "name": "slide_03",
    "body": """
<div class="status-bar"><span>2026 H1 · K-SHAPE · 03 / 09</span><span>ERIC 出品</span></div>
<div class="subtitle-bar"><span class="zh">K 型分化</span><span class="en">/ K-SHAPE DIVERGENCE</span></div>
<div class="main-title">不是<span class="accent">衰退</span><br>是<span class="accent-gold">结构</span><span class="accent">分化</span></div>
<div class="lead">同一市场 · 三种命运 · 头部飞天 / 中端承压 / 经济型外资加速退潮。</div>
<div class="section">
  <div class="ks-grid">
    <div class="ks-card up">
      <div class="head">上 · HEAD</div>
      <div class="pct">+12.4%</div>
      <div class="desc">凯悦中国 Q1 RevPAR<br>万豪/洲际 +5.7%<br>亚朵 +47.5%</div>
      <ul>
        <li>奢华 ADR +5~7%</li>
        <li>上海入境 +29.1%</li>
        <li>深圳 RevPAR +12.1%</li>
      </ul>
    </div>
    <div class="ks-card mid">
      <div class="head">中 · MID</div>
      <div class="pct">0~-3%</div>
      <div class="desc">中端 ADR/OCC 弱复苏<br>占 6 月新开 47.8%<br>供给压力最大</div>
      <ul>
        <li>中端 6 月新开 69 家</li>
        <li>中高端 ADR -1~-3%</li>
        <li>连锁化率 41.8%</li>
      </ul>
    </div>
    <div class="ks-card down">
      <div class="head">下 · TAIL</div>
      <div class="pct">-8~-12%</div>
      <div class="desc">经济型外资承压<br>温德姆大中华 -10%<br>民宿中低端 ADR -8%</div>
      <ul>
        <li>国民品牌供给过剩</li>
        <li>北京 RevPAR -64%</li>
        <li>低端个体户 -12%</li>
      </ul>
    </div>
  </div>
</div>
<div class="bottom-section">
  <div class="bottom-row">
    <div class="source-block">
      <div class="label">SOURCE <span class="en">来源</span></div>
      <div class="text">JLL 上海 7/14 · 仲量联行 6 月全国 · 迈点 6 月新开 236 家</div>
    </div>
    <div class="insight-block">
      <div class="label">INSIGHT <span class="en">洞察</span></div>
      <div class="text">结构洗牌 = <strong>国资 + 头部</strong>双垄断 · 头部逆向扩张</div>
    </div>
  </div>
</div>
""",
})

# ============= 04 6 档 × 6 城 =============
SLIDES.append({
    "name": "slide_04",
    "body": """
<div class="status-bar"><span>2026 H1 · 6 TIERS · 04 / 09</span><span>ERIC 出品</span></div>
<div class="subtitle-bar"><span class="zh">6 档酒店分化</span><span class="en">/ 6 TIERS · JUNE YOY</span></div>
<div class="main-title"><span class="accent">奢华</span>一枝独秀<br><span class="accent-blue">中端</span>过剩<span class="accent">承压</span></div>
<div class="lead">6 月全行业 · <span class="accent">奢华独立</span> · <span class="accent-gold">中端供给过剩</span> · <span class="accent">经济型外资重灾区</span></div>
<div class="section">
  <div class="fc-grid">
    <div class="fc-card"><div class="label">奢华 5星</div><div class="row"><span class="from">ADR</span><span class="arrow">→</span><span class="to pos">+5~7%</span></div><div class="row"><span class="from">OCC</span><span class="arrow">→</span><span class="to pos">+2~3pct</span></div><div class="note">丽思/华尔道夫/四季</div></div>
    <div class="fc-card blue"><div class="label">高端 4星</div><div class="row"><span class="from">ADR</span><span class="arrow">→</span><span class="to">+3~5%</span></div><div class="row"><span class="from">RevPAR</span><span class="arrow">→</span><span class="to">+5~8%</span></div><div class="note">万豪/希尔顿/凯悦</div></div>
    <div class="fc-card gold"><div class="label">中高端 准4星</div><div class="row"><span class="from">ADR</span><span class="arrow">→</span><span class="to">-1~-3%</span></div><div class="row"><span class="from">RevPAR</span><span class="arrow">→</span><span class="to">0~+2%</span></div><div class="note">亚朵/锦江都城</div></div>
    <div class="fc-card dark"><div class="label">中端 3星</div><div class="row"><span class="from">ADR</span><span class="arrow">→</span><span class="to">-3~-5%</span></div><div class="row"><span class="from">OCC</span><span class="arrow">→</span><span class="to">+1~3pct</span></div><div class="note">全季/汉庭/如家</div></div>
    <div class="fc-card red"><div class="label">经济型 2星</div><div class="row"><span class="from">ADR</span><span class="arrow">→</span><span class="to">-5~-8%</span></div><div class="row"><span class="from">RevPAR</span><span class="arrow">→</span><span class="to">-5~-8%</span></div><div class="note">7天/锦江之星</div></div>
    <div class="fc-card gold"><div class="label">民宿</div><div class="row"><span class="from">ADR</span><span class="arrow">→</span><span class="to">-8~-10%</span></div><div class="row"><span class="from">OCC</span><span class="arrow">→</span><span class="to pos">+20%+</span></div><div class="note">⛔ 量爆发价崩</div></div>
  </div>
</div>
<div class="bottom-section">
  <div class="bottom-row">
    <div class="source-block">
      <div class="label">SOURCE <span class="en">来源</span></div>
      <div class="text">JLL 上海 7/14 · 仲量联行 6 月全国 · STR 6 月数据 7/22</div>
    </div>
    <div class="insight-block">
      <div class="label">INSIGHT <span class="en">洞察</span></div>
      <div class="text">奢华独立 = <strong>高净值避风港</strong> · 中端是<strong>主战场</strong>也是<strong>修罗场</strong></div>
    </div>
  </div>
</div>
""",
})

# ============= 05 TOP 10 集团矩阵 =============
SLIDES.append({
    "name": "slide_05",
    "body": """
<div class="status-bar"><span>2026 H1 · TOP 10 · 05 / 09</span><span>ERIC 出品</span></div>
<div class="subtitle-bar"><span class="zh">头部集团</span><span class="en">/ TOP 10 · Q1 2026 YOY</span></div>
<div class="main-title"><span class="accent">亚朵</span> yyds<br>头部飞天 <span class="accent-blue">阵型大乱</span></div>
<div class="lead">5 内资 + 5 外资 · 内资 5/5 正增长 · 外资 5/5 正增长 · <span class="accent">但阵型分化巨大</span>。</div>
<div class="section">
  <div class="corp-grid">
    <div class="corp-col">
      <div class="head">内资 5 家 <span style="color:#888;font-size:14px">/ DOMESTIC</span></div>
      <div class="row"><span class="name">亚朵</span><span class="val pos">+47.5%</span></div>
      <div class="row sub">中高端单店模型 + 零售业务</div>
      <div class="row"><span class="name">华住</span><span class="val pos">+11.1%</span></div>
      <div class="row sub">EBITDA +26.7% 增收增利</div>
      <div class="row"><span class="name">锦江</span><span class="val pos">+6.09%</span></div>
      <div class="row sub">Q2 RevPAR -7% 高基数</div>
      <div class="row"><span class="name">首旅</span><span class="val flat">+0.66%</span></div>
      <div class="row sub">如家 OCC 65.9% 经营修复</div>
      <div class="row"><span class="name">君亭</span><span class="val pos">≈+28%</span></div>
      <div class="row sub">中高端拐点信号</div>
    </div>
    <div class="corp-col foreign">
      <div class="head">外资 5 家 <span style="color:#888;font-size:14px">/ FOREIGN</span></div>
      <div class="row"><span class="name">凯悦 H</span><span class="val pos">+12.4%</span></div>
      <div class="row sub">中国区增幅最高</div>
      <div class="row"><span class="name">希尔顿 HLT</span><span class="val pos">+8.98%</span></div>
      <div class="row sub">增速最快</div>
      <div class="row"><span class="name">洲际 IHG</span><span class="val pos">+5.7%</span></div>
      <div class="row sub">外资最大管线 34.3 万间在建</div>
      <div class="row"><span class="name">万豪 MAR</span><span class="val pos">+6%</span></div>
      <div class="row sub">大中华区稳定增长</div>
      <div class="row"><span class="name">⚠️ 温德姆 WH</span><span class="val neg">-10%</span></div>
      <div class="row sub">经济型为主 · 大中华承压</div>
    </div>
  </div>
</div>
<div class="bottom-section">
  <div class="bottom-row">
    <div class="source-block">
      <div class="label">SOURCE <span class="en">来源</span></div>
      <div class="text">头部 Q1 财报 5/15 · 万豪/希尔顿 5/8 · 温德姆 Q2 净利 +17%</div>
    </div>
    <div class="insight-block">
      <div class="label">INSIGHT <span class="en">洞察</span></div>
      <div class="text"><strong>亚朵 > 华住 > 万豪 > 凯悦 > 温德姆</strong> · 增速差距<strong>50pct+</strong></div>
    </div>
  </div>
</div>
""",
})

# ============= 06 4 大反差 / 反直觉 =============
SLIDES.append({
    "name": "slide_06",
    "body": """
<div class="status-bar"><span>2026 H1 · 4 INSIGHTS · 06 / 09</span><span>ERIC 出品</span></div>
<div class="subtitle-bar"><span class="zh">4 大反差</span><span class="en">/ COUNTER-INTUITIVE TRUTHS</span></div>
<div class="main-title">你<span class="accent">没想到</span>的<br>4 件<span class="accent-blue">真事</span></div>
<div class="lead">数据会撒谎 · 直到你<span class="accent">看穿</span>它。</div>
<div class="section">
  <div class="trap-grid">
    <div class="trap-cell">
      <div class="head"><span class="em">❶ 消费降级 是错觉</span></div>
      <div class="vs blue">+2.8%</div>
      <div class="note">餐饮反超商品 · 体验消费成赢家</div>
    </div>
    <div class="trap-cell">
      <div class="head"><span class="em">❷ 民间投资 暴跌 ≠ 酒店萧条</span></div>
      <div class="vs">-8.5%</div>
      <div class="note">头部逆势扩张 · 华住三线占 41%</div>
    </div>
    <div class="trap-cell">
      <div class="head"><span class="em">❸ 入境游 小城化 真趋势</span></div>
      <div class="vs blue">+60%</div>
      <div class="note">新疆 / 山西 / 贵州 · 外资不必争一线</div>
    </div>
    <div class="trap-cell">
      <div class="head"><span class="em">❹ 北京 -64% ≠ 全国恐慌</span></div>
      <div class="vs">-64%</div>
      <div class="note">高位回调 · 一线城市 ≠ 全国代表</div>
    </div>
  </div>
</div>
<div class="bottom-section">
  <div class="bottom-row">
    <div class="source-block">
      <div class="label">SOURCE <span class="en">来源</span></div>
      <div class="text">NBS 7/15 · JLL 7/8 北京 · 途家 7/10 入境游 +60%</div>
    </div>
    <div class="insight-block">
      <div class="label">INSIGHT <span class="en">洞察</span></div>
      <div class="text">看懂 <strong>K 型</strong> = 看懂 <strong>未来 3 年</strong>的酒店业</div>
    </div>
  </div>
</div>
""",
})

# ============= 07 REITs 元年 =============
SLIDES.append({
    "name": "slide_07",
    "body": """
<div class="status-bar"><span>2026 H1 · REITs · 07 / 09</span><span>ERIC 出品</span></div>
<div class="subtitle-bar"><span class="zh">REITs 元年</span><span class="en">/ REITS YEAR · ASSET SECURITIZATION</span></div>
<div class="main-title"><span class="accent">21.51</span><span style="font-size:50px"> 亿</span> + <span class="accent">17.03</span><span style="font-size:50px"> 亿</span><br>= <span class="accent-gold">酒店 REITs 元年</span></div>
<div class="lead">从"运营业务"到"资产金融"<span class="accent"> H2 头部资本运作窗口期打开</span>。</div>
<div class="section">
  <div class="j-grid">
    <div class="j-cell"><div class="when">5月</div><div class="what">REITs 试点扩围至酒店</div></div>
    <div class="j-cell"><div class="when">6/9</div><div class="what">中俄免签正式生效</div></div>
    <div class="j-cell"><div class="when">6/23</div><div class="what">🏆 华安锦江 REIT 通过 (17.03 亿 · 18 城 21 家)</div></div>
    <div class="j-cell"><div class="when">6/25</div><div class="what">仲量联行 + 中伦 联合发布白皮书 (44 页)</div></div>
    <div class="j-cell"><div class="when">7/14</div><div class="what">⭐ 远洲 REIT 通过 (21.51 亿 · 国内完整首单)</div></div>
    <div class="j-cell"><div class="when">Q3-Q4</div><div class="what">8 大二线 + 14 单待发</div></div>
  </div>
</div>
<div class="section">
  <div class="fc-grid">
    <div class="fc-card pos"><div class="label">酒店 REITs</div><div class="row"><span class="from">已发</span><span class="to pos">5 单</span></div><div class="note">华安锦江 + 4 单待发</div></div>
    <div class="fc-card blue"><div class="label">服务式公寓</div><div class="row"><span class="from">REITs</span><span class="to">3 单</span></div><div class="note">雅诗阁 + 华住</div></div>
    <div class="fc-card gold"><div class="label">文旅配套</div><div class="row"><span class="from">REITs</span><span class="to">多单</span></div><div class="note">含 4A/5A 景区</div></div>
    <div class="fc-card dark"><div class="label">合计推进</div><div class="row"><span class="from">仲量联行预计</span><span class="to pos">14 单 / 400 亿</span></div><div class="note">H2 酒店资本运作窗口</div></div>
  </div>
</div>
<div class="bottom-section">
  <div class="bottom-row">
    <div class="source-block">
      <div class="label">SOURCE <span class="en">来源</span></div>
      <div class="text">证监会 6/23 · 上交所 7/14 · 仲量联行 + 中伦 6/25 白皮书</div>
    </div>
    <div class="insight-block">
      <div class="label">INSIGHT <span class="en">洞察</span></div>
      <div class="text">REITs = 酒店从<strong>运营</strong>到<strong>资管</strong> · H2 窗口期</div>
    </div>
  </div>
</div>
""",
})

# ============= 08 CHAT 拐点 =============
SLIDES.append({
    "name": "slide_08",
    "body": """
<div class="status-bar"><span>2026 H1 · CHAT · 08 / 09</span><span>ERIC 出品</span></div>
<div class="subtitle-bar"><span class="zh">景气拐点</span><span class="en">/ CHAT INDEX · TURNING POINT</span></div>
<div class="main-title">从 <span class="accent">-21</span> 升到 <span class="accent-blue">-9</span><br><span class="accent-gold">行业主动调结构</span></div>
<div class="lead">CHA 中国酒店景气指数 · 2026 Q2 环比 <span class="accent">+12 点</span> · 升至近 7 季高位。</div>
<div class="section">
  <div class="timeline-section">
    <div class="section-title">景气曲线 <span class="en">/ CHAT TIMELINE</span></div>
    <div class="timeline-bar-wrap"></div>
    <div class="timeline-marks"><span>2025Q1</span><span>2025Q3</span><span>2026Q1</span><span>2026Q2</span><span>2026?</span></div>
    <div class="timeline-phases">
      <div class="tp dc">深度承压<br><strong>-32</strong></div>
      <div class="tp mb">缓复<br><strong>-15</strong></div>
      <div class="tp fake">谷底<br><strong>-21</strong></div>
      <div class="tp dark">强劲回升<br><strong>-9</strong></div>
      <div class="tp rs">结构性反弹<br><strong>?</strong></div>
    </div>
  </div>
</div>
<div class="section">
  <div class="fc-grid">
    <div class="fc-card blue"><div class="label">2026 Q2 指数</div><div class="row"><span class="from">CHA</span><span class="to">-9</span></div><div class="note">升至近 7 季高位</div></div>
    <div class="fc-card pos"><div class="label">环比变化</div><div class="row"><span class="from">vs Q1</span><span class="to pos">+12 点</span></div><div class="note">谷底反转信号</div></div>
    <div class="fc-card gold"><div class="label">2025 全年签约</div><div class="row"><span class="from">门店</span><span class="to">1,536 家</span></div><div class="note">与 2024 持平</div></div>
    <div class="fc-card red"><div class="label">CORRECTION</div><div class="row"><span class="from">仍为</span><span class="to neg">负向</span></div><div class="note">但环比大幅好转</div></div>
  </div>
</div>
<div class="bottom-section">
  <div class="bottom-row">
    <div class="source-block">
      <div class="label">SOURCE <span class="en">来源</span></div>
      <div class="text">CHA 2026 Q2 报告 7/24 · 连锁化率 41.8% (迈点 6 月)</div>
    </div>
    <div class="insight-block">
      <div class="label">INSIGHT <span class="en">洞察</span></div>
      <div class="text">不是<strong>全面回暖</strong> · 是<strong>主动调结构</strong> · K 型分化加剧</div>
    </div>
  </div>
</div>
""",
})

# ============= 09 H2 三种命运 =============
SLIDES.append({
    "name": "slide_09",
    "body": """
<div class="status-bar"><span>2026 H2 · 3 PATHS · 09 / 09</span><span>ERIC 出品</span></div>
<div class="subtitle-bar"><span class="zh">H2 三种命运</span><span class="en">/ H2 2026 · 3 SCENARIOS</span></div>
<div class="main-title">H2 不是 H1.0<br><span class="accent">3 种命运</span> 3 个<span class="accent-blue">动作</span></div>
<div class="lead">基线 60% / 鹰派 25% / 鸽派 15% · 你赌哪个?</div>
<div class="section">
  <div class="fc-grid">
    <div class="fc-card blue"><div class="label">A · 基线 60%</div><div class="row"><span class="from">H2 行业</span><span class="to pos">+3~5%</span></div><div class="note">头部财报稳健 · K 分化加剧</div></div>
    <div class="fc-card red"><div class="label">B · 鹰派 25%</div><div class="row"><span class="from">H2 OCC</span><span class="to neg">-3~5pct</span></div><div class="note">国资本垄断 · AHL 获窗口</div></div>
    <div class="fc-card pos"><div class="label">C · 鸽派 15%</div><div class="row"><span class="from">H2 行业</span><span class="to pos">+6~8%</span></div><div class="note">财政刺激落地 · 民营回血</div></div>
    <div class="fc-card dark"><div class="label">3 大引擎 (7-8 月)</div><div class="row"><span class="from">避暑 + 七夕 + 入境</span><span class="to pos">↑↑↑</span></div><div class="note">七夕 8/19 情侣酒店 +70%</div></div>
  </div>
</div>
<div class="section">
  <div class="findings-title">3 大风险 <span class="en">/ 3 RISKS</span></div>
  <div class="finding">
    <div class="num">01</div><div class="body"><div class="head">高基数压制</div><div class="text">2025/7 单周 <strong>+29.4%</strong> · H2 增速将明显回落</div></div>
  </div>
  <div class="finding">
    <div class="num">02</div><div class="body"><div class="head">85 号令不确定性</div><div class="text">8/1 施行 · 12 个月过渡 · <span class="em">基线 60% / 鹰派 25% / 鸽派 15%</span></div></div>
  </div>
  <div class="finding">
    <div class="num">03</div><div class="body"><div class="head">民间投资崩塌</div><div class="text"><strong>-8.5%</strong> · 何时止跌 = H2 整体天花板</div></div>
  </div>
</div>
<div class="bottom-section">
  <div class="bottom-row">
    <div class="source-block">
      <div class="label">ONE-LINE <span class="en">一行记住</span></div>
      <div class="text">H1 = 服务反超 + K 分化 + REITs 元年 · H2 关键 = 头部半年报 (8/20-30) + 85 号令执法</div>
    </div>
    <div class="insight-block">
      <div class="label">行动 <span class="en">/ ACT</span></div>
      <div class="text">8/30 等头部半年报 · 9 月补完整版 · 文末 <strong>关注 + 收藏</strong></div>
    </div>
  </div>
</div>
""",
})


def render_slides():
    print(f"开始渲染 {len(SLIDES)} 张 ...\n")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": W, "height": H},
            device_scale_factor=DSF,
            locale="zh-CN",
        )
        for s in SLIDES:
            html_file = OUT_DIR / f"{s['name']}.html"
            png_file = OUT_DIR / f"{s['name']}.png"
            html_file.write_text(slide_html(s["body"]), encoding="utf-8")
            print(f"  - {s['name']}.html -> render")
            page = ctx.new_page()
            page.goto(f"file:///{html_file.as_posix()}", wait_until="networkidle")
            page.wait_for_timeout(900)
            page.screenshot(path=str(png_file), type="png", full_page=False)
            page.close()
            print(f"    OK {png_file.name} ({png_file.stat().st_size:,} B)")
        browser.close()
    print("\n[OK] 9 张 PNG 已渲染")


def add_watermark():
    print("\n开始加水印 ...")
    for s in SLIDES:
        png_path = OUT_DIR / f"{s['name']}.png"
        wm_path = OUT_DIR / f"{s['name']}_wm.png"
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
        margin_x, margin_y = 130, 130
        x = W_img - tw - margin_x
        y = H_img - th - margin_y
        draw.rounded_rectangle(
            [x - 16, y - 8, x + tw + 16, y + th + 8],
            radius=10,
            fill=(26, 31, 58, 200),
        )
        draw.text((x, y), text, fill=(242, 237, 227, 255), font=font)
        final = Image.alpha_composite(img, overlay).convert("RGB")
        final.save(wm_path, "PNG", optimize=True)
        print(f"  [WM] {wm_path.name} ({W_img}x{H_img})")
    print("\n[OK] 9 张水印 PNG 已就绪")


if __name__ == "__main__":
    render_slides()
    add_watermark()
    print(f"\n[DONE] 输出目录: {OUT_DIR}")
