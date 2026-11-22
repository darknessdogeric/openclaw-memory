# -*- coding: utf-8 -*-
"""小红书多图卡片生成器 · 标准范式 v1.0
来源:综合 nexu-io/card-xiaohongshu(Apache-2.0,8.3K stars) + Eric 反复反馈 + 金轩十文 9 图实战
固定:1080x1440(3:4),flex 纵向,每卡一个核心观点,设计 token 锁定
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright

# ============ 设计 token(整套卡片锁定) ============
# 配色:从 card-design/palettes.md 选一套(暖纸系,适合知识/生活)
TOKEN = {
    'bg': '#FAFAF7',          # 主背景:暖纸白
    'ink': '#1A1A1A',          # 主文字
    'gold': '#D4A574',         # 金色点缀(标题/重要数据)
    'gray': '#6B6B73',         # 副文
    'muted': '#8A8A96',        # 注释/小字
    'border': '#E0DCD0',       # 浅边框
    'card_bg': '#FFFFFF',      # 卡片底
    'highlight': '#9AE8B4',    # 绿色锚点(底部结论)
}

# ============ 标准 4 区段 CSS(经验证稳定) ============
CSS = '''
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body { width:1080px; height:1440px; overflow:hidden;
    font-family:"Microsoft YaHei","PingFang SC","Noto Sans SC",sans-serif;
    background:BG; color:INK; }
  .bg { position:absolute; inset:0; z-index:0;
    background:radial-gradient(ellipse 130% 70% at 50% 8%, #1A2855 0%, #0E1733 55%, #08102A 100%); }
  .glow { position:absolute; width:520px; height:520px; top:8%; left:50%;
    transform:translate(-50%,-50%); border-radius:50%; z-index:0;
    background:radial-gradient(circle, rgba(212,167,116,0.10) 0%, transparent 70%); }

  /* 4 区段 Grid 固定分配 */
  .canvas { position:relative; z-index:1; width:1080px; height:1440px;
    padding: 40px 56px 30px;
    display: grid; grid-template-rows: 70px 150px 1fr 170px; gap: 14px; }

  .seg-header { display:flex; align-items:center; justify-content:space-between; }
  .seg-title { display:flex; flex-direction:column; justify-content:center;
    padding-bottom: 6px; border-bottom: 1px solid rgba(212,167,116,0.30); }
  .seg-body { background:rgba(255,255,255,0.04); border:1px solid rgba(212,167,116,0.20);
    border-radius:10px; padding:18px 20px; overflow:hidden;
    display:flex; flex-direction:column; justify-content: space-evenly; }
  .seg-footer { display:flex; flex-direction:column; justify-content:center; gap:10px;
    padding-top: 10px; border-top: 1.5px solid rgba(212,167,116,0.30); }

  /* 字号(经验证,正文可读 + 不重叠) */
  .tag { color:GOLD; font-size:22px; font-weight:700; letter-spacing:2px; }
  .page-num { color:#4A5078; font-size:20px; font-weight:600; letter-spacing:2px; }
  .line1 { font-size:46px; font-weight:900; color:#F5F2EA; letter-spacing:2px; line-height:1.15; }
  .line2 { font-size:26px; font-weight:700; color:GOLD; letter-spacing:2px; line-height:1.25; margin-top:6px; }

  .footer-line { display:flex; align-items:center; justify-content:space-between; }
  .b-mark { color:GOLD; font-size:22px; font-weight:900; letter-spacing:2px; }
  .b-mark span { color:#5A6088; font-weight:600; margin-left:8px; font-size:16px; letter-spacing:1px; }
  .b-right { color:#4A5078; font-size:16px; letter-spacing:1px; }

  /* footer 大字锚点:画面视觉重心 */
  .footer-summary {
    color:HIGHLIGHT; font-size:26px; font-weight:900; letter-spacing:2px;
    text-align:center; line-height:1.4;
    padding:12px 24px;
    background:linear-gradient(135deg, rgba(154,232,180,0.15), rgba(74,111,165,0.10));
    border:1.5px solid rgba(154,232,180,0.40);
    border-radius:10px;
  }

  /* Block 内元素 */
  .seg-title-text { color:GOLD; font-size:22px; font-weight:800; letter-spacing:1px; line-height:1.3; margin-bottom:8px; }
  .seg-text { color:#C9D4E8; font-size:22px; line-height:1.5; letter-spacing:0.5px; }
  .small { color:#7A86A8; font-size:16px; }
  .hi { color:GOLD; font-weight:700; }

  .conclusion { color:HIGHLIGHT; font-size:20px; font-weight:700; line-height:1.4;
    padding:8px 12px; background:rgba(154,232,180,0.10);
    border-left:3px solid HIGHLIGHT; border-radius:4px; }

  .kpi-row { display:flex; gap:8px; }
  .kpi { flex:1; background:rgba(212,167,116,0.12); border:1px solid rgba(212,167,116,0.30);
    border-radius:6px; padding:12px 8px; text-align:center;
    display:flex; flex-direction:column; justify-content:center; min-height:0; }
  .kpi-num { color:GOLD; font-size:24px; font-weight:900; letter-spacing:1px; line-height:1.1; }
  .kpi-label { color:#9AA5C2; font-size:15px; margin-top:3px; letter-spacing:0.5px; line-height:1.25; }

  table { width:100%; border-collapse:collapse; table-layout:fixed; }
  table th { background:rgba(212,167,116,0.25); color:GOLD;
    font-size:16px; font-weight:700; padding:7px 7px; text-align:left; letter-spacing:0.5px; line-height:1.3; }
  table td { color:#C9D4E8; font-size:17px; padding:7px 7px;
    border-bottom:1px solid rgba(255,255,255,0.06); line-height:1.4; }
  table tr:last-child td { border-bottom:none; }

  .timeline { display:flex; flex-direction:column; gap:6px; }
  .tl-row { display:flex; gap:10px; align-items:center; }
  .tl-year { color:GOLD; font-size:16px; font-weight:900; width:55px; letter-spacing:1px; }
  .tl-bar { flex:1; height:26px; background:rgba(255,255,255,0.05); border-radius:4px;
    position:relative; overflow:hidden; }
  .tl-bar > span { position:absolute; top:0; left:0; bottom:0;
    background:linear-gradient(90deg, GOLD, #E8B84B); border-radius:4px;
    display:flex; align-items:center; padding-left:10px;
    color:#0E1733; font-size:13px; font-weight:800; }

  .compare { display:flex; gap:8px; }
  .compare > div { flex:1; padding:12px 14px; border-radius:6px; }
  .compare .old { background:rgba(180,100,100,0.14); border:1px solid rgba(220,140,140,0.30); }
  .compare .new { background:rgba(100,180,140,0.14); border:1px solid rgba(140,220,170,0.30); }
  .compare h4 { font-size:20px; font-weight:700; letter-spacing:1px; margin-bottom:4px; }
  .compare .old h4 { color:#E89A8A; }
  .compare .new h4 { color:#9AE8B4; }
  .compare p { color:#C9D4E8; font-size:16px; line-height:1.4; letter-spacing:0.5px; }

  .matrix { display:flex; flex-direction:column; gap:4px; }
  .matrix-row { display:flex; gap:5px; align-items:center; }
  .matrix-name { color:#F5F2EA; font-size:17px; font-weight:700; width:135px; letter-spacing:0.5px; }
  .matrix-cells { flex:1; display:flex; gap:5px; }
  .cell { flex:1; padding:7px 4px; border-radius:4px; text-align:center;
    font-size:16px; font-weight:700; letter-spacing:0.5px; line-height:1.3; }
  .cell-h { background:rgba(220,90,90,0.28); color:#F5C2A8; border:1px solid rgba(220,140,120,0.40); }
  .cell-m { background:rgba(220,170,90,0.28); color:#F5DCA8; border:1px solid rgba(220,190,110,0.40); }
  .cell-l { background:rgba(90,200,140,0.28); color:#A8E8C8; border:1px solid rgba(130,220,160,0.40); }
  .cell-hd { background:rgba(255,255,255,0.08); color:#9AA5C2; border:1px solid rgba(255,255,255,0.12); }
'''

# 替换 token 占位符
def apply_token(css):
    return (css
        .replace('BG', TOKEN['bg'])
        .replace('INK', TOKEN['ink'])
        .replace('GOLD', TOKEN['gold'])
        .replace('GRAY', TOKEN['gray'])
        .replace('MUTED', TOKEN['muted'])
        .replace('BORDER', TOKEN['border'])
        .replace('HIGHLIGHT', TOKEN['highlight'])
    )

CSS = apply_token(CSS)

# ============ 卡片模板函数 ============
def make_card(tag, idx, total, l1, l2, body_html, footer_summary, output_path):
    """生成单张卡片 PNG"""
    html = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=1080,height=1440">
<style>{CSS}</style></head>
<body>
<div class="bg"></div><div class="glow"></div>
<div class="canvas">
  <div class="seg-header"><span class="tag">{tag}</span><span class="page-num">{idx}/{total}</span></div>
  <div class="seg-title"><div class="line1">{l1}</div><div class="line2">{l2}</div></div>
  <div class="seg-body">{body_html}</div>
  <div class="seg-footer"><div class="footer-line"><div class="b-mark">B166ER<span>出品 · 2026.10.06</span></div><div class="b-right">金轩十文解读 · 酒店文旅AI</div></div><div class="footer-summary">{footer_summary}</div></div>
</div></body></html>'''

    with sync_playwright() as p:
        browser = p.chromium.launch(
            args=['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage',
                  '--disable-software-rasterizer', '--disable-extensions'])
        ctx = browser.new_context(viewport={'width':1080,'height':1440}, device_scale_factor=1)
        page = ctx.new_page()
        tmp = Path(output_path).with_suffix('.html')
        tmp.write_text(html, encoding='utf-8')
        page.goto(f'file:///{tmp}')
        page.wait_for_load_state('domcontentloaded')
        page.screenshot(path=str(output_path), full_page=False)
        page.close()
        ctx.close()
        browser.close()
        tmp.unlink()
    return output_path


def render_n_cards(cards, output_dir):
    """批量渲染 N 张卡片
    cards: [(tag, l1, l2, body_html, footer_summary), ...]
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for old in output_dir.glob('*.png'):
        old.unlink()
    total = len(cards)
    for i, (tag, l1, l2, body_html, footer_summary) in enumerate(cards):
        out = output_dir / f'card_{i+1:02d}.png'
        make_card(tag, i+1, total, l1, l2, body_html, footer_summary, out)
        print(f'  ✓ {i+1}/{total} {out.name}')
    print(f'完成 -> {output_dir}')
    return output_dir

# ============ 内容段辅助函数 ============
def seg(title, content, conclusion=None):
    """一个内容段:标题 + 内容 [+ 结论]"""
    s = f'<div><div class="seg-title-text">{title}</div>{content}</div>'
    if conclusion:
        s += f'<div class="conclusion">{conclusion}</div>'
    return s

def kpi(items):
    """KPI 行:items=[(数字, 标签), ...]"""
    return '<div class="kpi-row">' + ''.join(
        f'<div class="kpi"><div class="kpi-num">{n}</div><div class="kpi-label">{l}</div></div>'
        for n, l in items
    ) + '</div>'

def table(headers, rows):
    """表格"""
    ths = ''.join(f'<th style="width:{w}">{h}</th>' for h, w in headers)
    trs = ''.join(
        '<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>'
        for row in rows
    )
    return f'<table><tr>{ths}</tr>{trs}</table>'

def timeline(rows):
    """时间线 rows=[(年份, 文字, 百分比), ...]"""
    s = '<div class="timeline">'
    for year, text, pct in rows:
        s += f'<div class="tl-row"><div class="tl-year">{year}</div><div class="tl-bar"><span style="width:{pct}%">{text}</span></div></div>'
    s += '</div>'
    return s

def compare(cols):
    """对比 cols=[(颜色类, 标题, 内容), ...]"""
    items = ''
    for cls, title, content in cols:
        items += f'<div class="{cls}"><h4>{title}</h4><p>{content}</p></div>'
    return f'<div class="compare">{items}</div>'

def matrix(rows):
    """矩阵 rows=[(名称, [(颜色类, 文本), ...]), ...]"""
    s = '<div class="matrix">'
    for name, cells in rows:
        cells_html = ''.join(f'<div class="cell {cls}">{t}</div>' for cls, t in cells)
        s += f'<div class="matrix-row"><div class="matrix-name">{name}</div><div class="matrix-cells">{cells_html}</div></div>'
    s += '</div>'
    return s

# ============ 使用示例 ============
if __name__ == '__main__':
    # 演示:3 张最小卡片
    cards = [
        ('测试 · 封面', '标题 1', '副标题 1',
         seg('段 1', '<div class="seg-text">内容 1</div>'),
         '底部锚点 1'),
        ('测试 · 正文', '标题 2', '副标题 2',
         seg('段 1', kpi([('80%', '覆盖率'), ('7+', '要素'), ('95%', '通过率')])),
         '底部锚点 2'),
        ('测试 · 收尾', '标题 3', '副标题 3',
         seg('段 1', '<div class="seg-text">结论内容</div>'),
         '底部锚点 3'),
    ]
    out = render_n_cards(cards, Path(r'D:/B166ER-OpenClaw/workspace/toolbox/.tmp/card_test'))
    print(f'输出: {out}')
