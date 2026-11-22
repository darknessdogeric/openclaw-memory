"""GEO topic · V4 麦肯锡 9 张小红书图.

Content: 智驾小蓝灯后第二篇 — GEO 是否是过渡期噪音？

Slide structure:
  01 cover        - 封面（Executive Briefing）
  02 phenomenon   - GEO 是什么 + 产业链现状
  03 data         - 搜狐实证数据（0.01% → 11.2%）
  04 nature       - 污染路径（从曝光位到 AI 思维方式）
  05 essence      - Eric 5 观点 = 信息污染 5 个面
  06 rebuttal     - GEO 的辩护 + 压力测试
  07 alternative  - Agent-Native 范式
  08 action       - 对 Eric 的 3 条建议
  09 takeaway     - 收口金句
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace\toolbox')
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(r"D:\B166ER-OpenClaw\workspace\output\geo_2026-07-16")
OUT_DIR.mkdir(parents=True, exist_ok=True)

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# ===== V4 麦肯锡 master CSS (full version, from xhs_mckinsey.py) =====
COMMON_CSS = """
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: "Helvetica Neue", "Source Han Serif SC", "Noto Serif CJK SC", "PingFang SC", "Microsoft YaHei", sans-serif;
    background: #FFFFFF;
    -webkit-font-smoothing: antialiased;
    color: #0A2540;
  }
  .slide {
    width: 1080px;
    height: 1440px;
    position: relative;
    background: #FFFFFF;
    overflow: hidden;
    padding: 0;
  }
  .masthead {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 80px;
    padding: 0 50px;
    border-bottom: 3px solid #0A2540;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #FFFFFF;
    z-index: 20;
  }
  .masthead .brand { font-size: 16px; font-weight: 700; letter-spacing: 6px; color: #0A2540; }
  .masthead .date { font-size: 13px; color: #5A6B7D; letter-spacing: 3px; font-family: "Helvetica Neue", Arial, sans-serif; }
  .footer {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 60px;
    padding: 0 50px;
    border-top: 3px solid #0A2540;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #FFFFFF;
    z-index: 20;
  }
  .footer .source { font-size: 12px; color: #5A6B7D; letter-spacing: 3px; font-family: "Helvetica Neue", Arial, sans-serif; }
  .footer .page { font-size: 13px; font-weight: 700; color: #0A2540; letter-spacing: 4px; }
  .content {
    position: absolute;
    top: 100px; left: 40px; right: 40px; bottom: 80px;
    z-index: 5;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .eyebrow {
    font-size: 16px;
    color: #C8102E;
    letter-spacing: 6px;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 12px;
    font-family: "Helvetica Neue", Arial, sans-serif;
  }
  h1 { font-size: 88px; font-weight: 700; line-height: 1.1; color: #0A2540; letter-spacing: -0.5px; }
  h2 { font-size: 56px; font-weight: 700; line-height: 1.12; color: #0A2540; letter-spacing: -0.3px; margin-bottom: 18px; }
  .red { color: #C8102E; }
  .gray { color: #5A6B7D; }
  .accent-bar { width: 80px; height: 6px; background: #C8102E; }
  .body-text { font-size: 28px; color: #2A3A4D; line-height: 1.6; font-weight: 400; }
  .body-text .hl { background: linear-gradient(transparent 60%, #FFE08A 60%); font-weight: 600; padding: 0 2px; }
  .pullquote {
    border-top: 5px solid #0A2540;
    border-bottom: 5px solid #0A2540;
    padding: 32px 0;
    font-size: 36px;
    font-weight: 500;
    color: #0A2540;
    line-height: 1.45;
    font-style: italic;
  }
  .data-callout {
    background: #F2F4F7;
    border-left: 8px solid #0A2540;
    padding: 32px 36px;
  }
  .data-callout .label {
    font-size: 15px;
    color: #5A6B7D;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 12px;
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-weight: 700;
  }
  .data-callout .value {
    font-size: 78px;
    font-weight: 700;
    color: #0A2540;
    line-height: 1;
    letter-spacing: -1px;
    font-family: "Helvetica Neue", Arial, sans-serif;
  }
  .data-callout .unit { font-size: 24px; color: #5A6B7D; font-weight: 400; margin-left: 8px; }
  .data-callout .note { font-size: 19px; color: #5A6B7D; margin-top: 18px; line-height: 1.5; }
  table.editorial { width: 100%; border-collapse: collapse; font-family: "Helvetica Neue", Arial, sans-serif; }
  table.editorial th {
    background: #0A2540;
    color: #FFFFFF;
    font-size: 15px;
    font-weight: 700;
    text-align: left;
    padding: 18px 22px;
    letter-spacing: 3px;
    text-transform: uppercase;
  }
  table.editorial td {
    padding: 24px 22px;
    border-bottom: 1px solid #E5E8EC;
    font-size: 23px;
    color: #0A2540;
  }
  table.editorial td:first-child { font-weight: 700; }
  table.editorial tr:last-child td { border-bottom: 4px solid #0A2540; }
  ol.editorial { list-style: none; counter-reset: li; }
  ol.editorial li {
    font-size: 28px;
    color: #2A3A4D;
    line-height: 1.5;
    margin-bottom: 30px;
    padding-left: 80px;
    position: relative;
  }
  ol.editorial li::before {
    content: counter(li, decimal-leading-zero);
    counter-increment: li;
    position: absolute;
    left: 0; top: 8px;
    font-size: 24px;
    font-weight: 700;
    color: #C8102E;
    letter-spacing: 2px;
    font-family: "Helvetica Neue", Arial, sans-serif;
    width: 64px;
    border-bottom: 3px solid #C8102E;
    padding-bottom: 6px;
  }
  .three-col { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 26px; }
  .col { border-top: 5px solid #0A2540; padding: 24px 0 4px; }
  .col.muted { border-top-color: #94A2B0; }
  .col .col-num { font-size: 14px; color: #94A2B0; letter-spacing: 3px; margin-bottom: 12px; font-family: "Helvetica Neue", Arial, sans-serif; font-weight: 700; }
  .col .col-title { font-size: 30px; font-weight: 700; color: #0A2540; margin-bottom: 10px; letter-spacing: -0.2px; }
  .col .col-keyword { font-size: 21px; color: #C8102E; margin-bottom: 18px; font-weight: 600; font-style: italic; }
  .col .col-body { font-size: 20px; color: #2A3A4D; line-height: 1.55; min-height: 80px; }
  .col .col-stat { font-size: 14px; color: #5A6B7D; margin-top: 18px; padding-top: 14px; border-top: 1px dashed #94A2B0; font-family: "Helvetica Neue", Arial, sans-serif; }
  .dark-callout {
    background: #0A2540;
    color: #FFFFFF;
    padding: 36px 42px;
  }
  .dark-callout .label { font-size: 14px; color: #C8102E; letter-spacing: 5px; font-weight: 700; margin-bottom: 18px; font-family: "Helvetica Neue", Arial, sans-serif; }
  .dark-callout .body { font-size: 28px; line-height: 1.55; color: #FFFFFF; font-weight: 400; }
  .dark-callout .body .red-text { color: #C8102E; font-weight: 700; }
"""


def render(idx, body_html):
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>GEO Slide {idx}</title>
<style>{COMMON_CSS}
</style>
</head>
<body>
<div class="slide">
  <div class="masthead">
    <div class="brand">B166ER · 商业内参</div>
    <div class="date">2026.07.16 · ISSUE NO.002</div>
  </div>
  <div class="content">{body_html}</div>
  <div class="footer">
    <div class="source">SOURCE: B166ER · GEO 现象观察</div>
    <div class="page">{idx:02d} / 09</div>
  </div>
</div>
</body>
</html>"""
    html_path = OUT_DIR / f"slide_{idx:02d}.html"
    png_path = OUT_DIR / f"slide_{idx:02d}.png"
    wm_path = OUT_DIR / f"slide_{idx:02d}_wm.png"
    html_path.write_text(html, encoding='utf-8')

    r = subprocess.run([
        EDGE, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--force-device-scale-factor=2",
        "--window-size=1080,1440",
        f"--screenshot={png_path}",
        html_path.as_uri(),
    ], capture_output=True, text=True, timeout=45)
    print(f"Slide {idx}: RC={r.returncode}, size={png_path.stat().st_size if png_path.exists() else 0}")
    return png_path


def pil_watermark(png_path):
    p = Path(png_path)
    wm = p.with_name(p.stem + '_wm.png')
    img = Image.open(p).convert("RGBA")
    w, h = img.size
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 22)
        font_tiny = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 18)
        font_big = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 70)
    except Exception:
        font = ImageFont.load_default()
        font_tiny = font
        font_big = font
    # Top-left: smaller, won't crowd masthead
    draw.rectangle([(0, 0), (200, 50)], fill=(10, 37, 64, 200))
    draw.text((16, 14), "B166ER · GEO", fill=(255, 255, 255, 255), font=font)
    # Bottom-right: integrated into footer area (below page number line)
    # slide footer is 60px high (top border at h-60), so watermark sits at h-30
    # but page number text is at ~h-30 baseline
    # Place B166ER text on the BOTTOM edge (last 30px), centered-right
    draw.text((w-220, h-30), "© B166ER · 2026.07.16", fill=(10, 37, 64, 240), font=font_tiny)
    # Center diagonal watermark (very faint)
    wm_text = "B166ER · 2026.07.16"
    bbox = draw.textbbox((0, 0), wm_text, font=font_big)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    txt_img = Image.new("RGBA", (tw + 40, th + 40), (0, 0, 0, 0))
    txt_draw = ImageDraw.Draw(txt_img)
    txt_draw.text((20, 20), wm_text, fill=(200, 200, 200, 40), font=font_big)
    txt_img = txt_img.rotate(-22, expand=True)
    overlay.paste(txt_img, ((w - txt_img.size[0]) // 2, (h - txt_img.size[1]) // 2), txt_img)
    out = Image.alpha_composite(img, overlay).convert("RGB")
    out.save(wm, "PNG", optimize=True)
    return wm


# ===== Slide bodies =====
SLIDE_01 = """
<div>
  <div class="eyebrow">EXECUTIVE BRIEFING · 摘要</div>
  <h1>GEO：<span class="red">过渡期噪音</span>，<br/>还是未来？</h1>
  <div class="accent-bar"></div>
</div>
<div style="font-size: 30px; color: #2A3A4D; line-height: 1.55; font-style: italic; font-weight: 400;">
  一场关于「AI 时代信息污染」的<br/>五维深度解构
</div>
<div class="hr" style="height: 2px; background: #0A2540; margin: 0;"></div>
<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 30px;">
  <div>
    <div style="font-size: 14px; color: #5A6B7D; letter-spacing: 4px; margin-bottom: 12px; font-weight: 700;">SECTOR</div>
    <div style="font-size: 24px; color: #0A2540; font-weight: 700;">AI / 内容</div>
  </div>
  <div>
    <div style="font-size: 14px; color: #5A6B7D; letter-spacing: 4px; margin-bottom: 12px; font-weight: 700;">CLAIM</div>
    <div style="font-size: 24px; color: #0A2540; font-weight: 700;">过渡期噪音</div>
  </div>
  <div>
    <div style="font-size: 14px; color: #5A6B7D; letter-spacing: 4px; margin-bottom: 12px; font-weight: 700;">NEXT</div>
    <div style="font-size: 24px; color: #C8102E; font-weight: 700;">Agent-Native</div>
  </div>
</div>
"""

SLIDE_02 = """
<div>
  <div class="eyebrow">01 · THE PHENOMENON</div>
  <h2>GEO 是什么</h2>
</div>
<div class="body-text" style="margin-bottom: 24px;">
  <span class="hl">GEO (Generative Engine Optimization)</span> — 把 SEO 的"博弈对象从搜索引擎换成 LLM"。2023 由 Princeton + IIT Delhi 提出，论文验证 9 种优化策略可提升 AI 引用率 <span class="hl">22-41%</span>。
</div>
<div class="three-col">
  <div class="col">
    <div class="col-num">TYPE · 01</div>
    <div class="col-title">内容农场 2.0</div>
    <div class="col-keyword">批量伪测评</div>
    <div class="col-body">AI 批量生产"XX 最佳 10 大"<br/>伪测评 + 多平台铺发</div>
  </div>
  <div class="col">
    <div class="col-num">TYPE · 02</div>
    <div class="col-title">伪权威注入</div>
    <div class="col-keyword">伪造引用源</div>
    <div class="col-body">伪造行业报告 + 白皮书<br/>+ 真实地名/链接混入</div>
  </div>
  <div class="col">
    <div class="col-num">TYPE · 03</div>
    <div class="col-title">私域推流</div>
    <div class="col-keyword">制造"流行度"</div>
    <div class="col-body">自媒体矩阵推同一内容<br/>给 LLM 制造"主流信号"</div>
  </div>
</div>
<div style="font-size: 22px; color: #2A3A4D; font-style: italic; border-left: 5px solid #C8102E; padding-left: 18px; line-height: 1.55;">
  <strong style="color: #0A2540; font-style: normal;">2026 现状：</strong>中国 GEO 服务商已超 200 家，客单价 ¥3000-50000/月。
</div>
"""

SLIDE_03 = """
<div>
  <div class="eyebrow">02 · THE EVIDENCE</div>
  <h2>污染的非线性放大</h2>
</div>
<div class="data-callout">
  <div class="label">SOURCE · 搜狐《长安街知事》2026-03-17</div>
  <div class="value">0.01%<span class="unit">虚假文本 → +11.2% 有害输出</span></div>
  <div class="note">当训练数据集中仅有 <strong style="color: #0A2540;">0.01%</strong> 的虚假文本时，模型输出的有害内容会增加 <strong style="color: #C8102E;">11.2%</strong>；即使是 <strong style="color: #0A2540;">0.001%</strong> 的虚假文本，有害输出也上升 <strong style="color: #C8102E;">7.2%</strong>。</div>
</div>
<div class="pullquote" style="margin: 24px 0; padding: 24px 0;">
  「当 GEO 乱象蔓延，大模型很可能在<br/><strong style="color: #C8102E;">被污染数据的回音壁</strong>中不断再生产，<br/>最终导致互联网内容生态劣化。」
</div>
<div style="font-size: 22px; color: #5A6B7D; line-height: 1.6; font-style: italic;">
  来源：搜狐《AI 污染，细思极恐》（2026-03-17）· 引用 Princeton 2023 论文实测数据
</div>
"""

SLIDE_04 = """
<div>
  <div class="eyebrow">03 · THE MECHANISM</div>
  <h2>污染路径：从曝光位到思维方式</h2>
</div>
<table class="editorial">
  <thead>
    <tr><th style="width: 22%;">时代</th><th style="width: 32%;">博弈对象</th><th style="width: 46%;">用户识别能力</th></tr>
  </thead>
  <tbody>
    <tr><td>Web 1.0</td><td>编辑推荐位</td><td>能识别"这是编辑"</td></tr>
    <tr><td>Web 2.0</td><td>SEO 搜索结果</td><td>能识别"这是广告"</td></tr>
    <tr><td>Web 3.0</td><td>KOL / 社交推荐</td><td>难识别，需判断 KOL 公信力</td></tr>
    <tr><td class="red">Web 4.0</td><td class="red">LLM 直接回答</td><td class="red" style="font-weight: 700;">用户：<strong>无法识别"这是污染"</strong></td></tr>
  </tbody>
</table>
<div class="dark-callout" style="margin-top: 24px;">
  <div class="label">KEY MECHANISM</div>
  <div class="body">
    GEO 从 AI 的 <span class="red-text">"思维方式"</span> 入手，试图扭曲整个模型的信息生产链路。<br/>
    <strong>商业操纵</strong>以 "AI 总结后的建议" / "AI 推荐的答案" / "AI 整理出的共识" 等形态出现。
  </div>
</div>
"""

SLIDE_05 = """
<div>
  <div class="eyebrow">04 · THE ESSENCE</div>
  <h2>信息污染的 5 个面</h2>
</div>
<ol class="editorial">
  <li><span class="red" style="font-weight: 700;">数据层面</span> · 0.01% 假信息放大 11.2% 伤害 — 非线性污染</li>
  <li><span class="red" style="font-weight: 700;">工具层面</span> · 搜索权重 = Web 2.0 思路套到 AI 上 — 范式滞后</li>
  <li><span class="red" style="font-weight: 700;">能力层面</span> · 让 AI 退化为"加引用的搜索框" — 能力错配</li>
  <li><span class="red" style="font-weight: 700;">用户层面</span> · 用户失去辨识能力 — 信息差扩大</li>
  <li><span class="red" style="font-weight: 700;">范式层面</span> · 终局是 Agent-Native，不是 GEO — 范式跃迁</li>
</ol>
<div class="dark-callout" style="margin-top: 16px;">
  <div class="label">CORE · 底层规律</div>
  <div class="body" style="font-size: 26px;">
    AI 时代的信息污染 = 让 AI 偏离<span class="red-text">用户真实需求匹配</span>的所有行为。
  </div>
</div>
"""

SLIDE_06 = """
<div>
  <div class="eyebrow">05 · THE REBUTTAL</div>
  <h2>GEO 的辩护 · 压力测试</h2>
</div>
<table class="editorial">
  <thead>
    <tr><th style="width: 32%;">反方观点</th><th style="width: 68%;">我的回应</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>"任何媒介都有博弈，<br/>GEO 是必经阶段"</td>
      <td>AI 时代是<strong>决策代理化</strong>，污染杠杆比搜索时代大 <strong style="color: #C8102E;">10 倍</strong></td>
    </tr>
    <tr>
      <td>"监管会跟上"</td>
      <td>LLM 黑箱 + 训练数据滚动更新，<strong>法律永远滞后 2-3 年</strong></td>
    </tr>
    <tr>
      <td>"技术会自净"<br/>（LLM 反污染过滤层）</td>
      <td>LLM 厂商没有动力自净：<br/><strong style="color: #C8102E;">"显得有用"比"显得真实"更利于留存</strong></td>
    </tr>
  </tbody>
</table>
<div class="data-callout" style="margin-top: 16px;">
  <div class="label">CONCLUSION</div>
  <div class="value" style="font-size: 50px;">GEO = 过渡期噪音<span class="unit">（不是终局）</span></div>
</div>
"""

SLIDE_07 = """
<div>
  <div class="eyebrow">06 · THE FUTURE</div>
  <h2>替代范式：Agent-Native</h2>
</div>
<div class="three-col">
  <div class="col">
    <div class="col-num">PHASE · 01</div>
    <div class="col-title">Real-time Agent</div>
    <div class="col-keyword">持续观察</div>
    <div class="col-body">AI 持续观察用户日历<br/>消费、社交信号<br/>主动推送（不等 GEO 污染）</div>
    <div class="col-stat">范式：信任资本累积</div>
  </div>
  <div class="col">
    <div class="col-num">PHASE · 02</div>
    <div class="col-title">Value-Aligned</div>
    <div class="col-keyword">真实匹配</div>
    <div class="col-body">商家声明真实定位<br/>AI 找最匹配价值取向的<br/>不需要 GEO 包装</div>
    <div class="col-stat">范式：真实性即最高权重</div>
  </div>
  <div class="col muted">
    <div class="col-num">PHASE · 03</div>
    <div class="col-title">Outcome Pricing</div>
    <div class="col-keyword">按结果付费</div>
    <div class="col-body">AI 推荐后实际成交<br/>不再买"AI 引用率"<br/>直接消灭 GEO 商业模式</div>
    <div class="col-stat">范式：结果导向</div>
  </div>
</div>
<div class="dark-callout" style="margin-top: 24px;">
  <div class="label">AHL · AGENT-NATIVE TRAVEL</div>
  <div class="body" style="font-size: 24px;">
    <span class="red-text">AHL</span> 不做 GEO，我们做 Agent-Native 旅行基础设施。<br/>
    这是和市面上所有竞品的根本差异化。
  </div>
</div>
"""

SLIDE_08 = """
<div>
  <div class="eyebrow">07 · THE ACTION</div>
  <h2>三条行动建议</h2>
</div>
<ol class="editorial">
  <li><span class="red" style="font-weight: 700;">内容定位</span> · 做"反 GEO"内容 — 教文旅从业者识别陷阱。2026 中文互联网几乎没人占。</li>
  <li><span class="red" style="font-weight: 700;">AHL 叙事升级</span> · 官网第一页写"我们不做 GEO" — 拉开和所有竞品距离。</li>
  <li><span class="red" style="font-weight: 700;">个人 IP 占位</span> · 持续输出"AI 信息污染"系列 — 你是中文互联网第一代"反 GEO"思想家。</li>
</ol>
<div class="dark-callout" style="margin-top: 16px; background: #0A2540;">
  <div style="font-size: 14px; color: #C8102E; letter-spacing: 5px; font-weight: 700; margin-bottom: 14px;">TIMING · 时间窗口</div>
  <div style="font-size: 26px; color: #FFFFFF; line-height: 1.5;">
    Eric 在这个时点的判断 = <span style="color: #C8102E; font-weight: 700;">2026 中文互联网最前瞻的 GEO 批评之一</span>。
  </div>
</div>
"""

SLIDE_09 = """
<div>
  <div class="eyebrow">08 · THE TAKEAWAY</div>
  <h2 style="font-size: 50px;">最终结论</h2>
</div>
<div class="dark-callout">
  <div class="label">CORE LAW · 底层规律</div>
  <div class="body" style="font-size: 34px;">
    当产品价值无法被外部识别<br/>
    使用者会自发创造可见符号
  </div>
</div>
<div style="font-size: 32px; color: #0A2540; line-height: 1.5; font-weight: 500; margin: 20px 0;">
  <span class="red" style="font-style: italic;">未来属于</span>，<br/>
  不属于 <span style="text-decoration: line-through; color: #94A2B0;">GEO</span>，<br/>
  而属于 <span class="red" style="font-weight: 700;">Agent-Native</span>。
</div>
<div class="gray-callout">
  <div class="label" style="font-size: 14px; color: #5A6B7D; letter-spacing: 4px; font-weight: 700; margin-bottom: 10px; text-transform: uppercase;">DISCUSSION · 互动</div>
  <div style="font-size: 22px; color: #0A2540; line-height: 1.55; font-weight: 500;">
    GEO 之后，你认为下一个过渡期噪音会是什么？<br/>
    <span style="color: #5A6B7D; font-size: 18px;">评论区聊聊。关注 B166ER，每周拆解一个商业现象。</span>
  </div>
</div>
"""

BODIES = [SLIDE_01, SLIDE_02, SLIDE_03, SLIDE_04, SLIDE_05, SLIDE_06, SLIDE_07, SLIDE_08, SLIDE_09]

print(f"Rendering {len(BODIES)} slides...")
for idx, body in enumerate(BODIES, 1):
    png = render(idx, body)
    wm = pil_watermark(png)
    print(f"  Watermarked: {wm.name} ({wm.stat().st_size:,} bytes)")

print(f"\n=== {len(BODIES)} GEO slides rendered to {OUT_DIR} ===")