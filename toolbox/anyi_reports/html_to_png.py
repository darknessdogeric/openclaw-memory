r"""
HTML → PNG 渲染器 v1.0 (Playwright 版)
========================================
**替代** 手写 Edge headless / npx 脚本
**依赖** playwright 1.58.0 + Chromium（已装）

用法:
    from anyi_reports.html_to_png import render_html

    # 单张
    render_html('poster.html', 'poster.png', width=1080, height=1440)

    # 批量
    from anyi_reports.html_to_png import render_batch
    render_batch([
        ('poster_1x1.html', 'poster_1x1.png', 1080, 1080),
        ('poster_3x4.html', 'poster_3x4.png', 1080, 1440),
    ])

    # CLI
    python html_to_png.py input.html output.png 1080 1440

参数:
- width/height: CSS 像素（viewport 尺寸 = 截图尺寸）
- scale: 设备像素比（默认 2 = 2x 高清）
- full_page: 是否截长图（默认 False）
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright


def render_html(html_path, png_path, width=1080, height=1440,
                scale=2, full_page=False, wait_ms=1500):
    """
    渲染单个 HTML 为 PNG

    :param html_path: 输入 HTML 路径
    :param png_path: 输出 PNG 路径
    :param width/height: viewport 尺寸（CSS px；PNG 实际 = ×scale）
    :param scale: 设备像素比（2 = 高清）
    :param full_page: True=整页长图；False=视口截图
    :param wait_ms: 等字体/图片加载的毫秒数
    """
    html_path = Path(html_path).resolve()
    png_path = Path(png_path).resolve()
    png_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={'width': width, 'height': height},
            device_scale_factor=scale,
        )
        page.goto(f'file:///{html_path.as_posix()}')
        page.wait_for_timeout(wait_ms)
        if full_page:
            page.screenshot(path=str(png_path), full_page=True)
        else:
            page.screenshot(path=str(png_path),
                            clip={'x': 0, 'y': 0, 'width': width, 'height': height})
        browser.close()

    size = png_path.stat().st_size
    return str(png_path), size


def render_batch(items, scale=2, full_page=False, wait_ms=1500):
    """
    批量渲染（复用同一 browser 实例）

    items: [(html_path, png_path, width, height), ...]
    """
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for html_path, png_path, width, height in items:
            html_path = Path(html_path).resolve()
            png_path = Path(png_path).resolve()
            png_path.parent.mkdir(parents=True, exist_ok=True)
            page = browser.new_page(
                viewport={'width': width, 'height': height},
                device_scale_factor=scale,
            )
            page.goto(f'file:///{html_path.as_posix()}')
            page.wait_for_timeout(wait_ms)
            if full_page:
                page.screenshot(path=str(png_path), full_page=True)
            else:
                page.screenshot(path=str(png_path),
                                clip={'x': 0, 'y': 0, 'width': width, 'height': height})
            page.close()
            results.append((str(png_path), png_path.stat().st_size))
        browser.close()
    return results


def html_to_pdf(html_path, pdf_path, width=1080, height=1440, wait_ms=1500):
    """HTML → PDF（打印级）"""
    html_path = Path(html_path).resolve()
    pdf_path = Path(pdf_path).resolve()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': width, 'height': height})
        page.goto(f'file:///{html_path.as_posix()}')
        page.wait_for_timeout(wait_ms)
        page.pdf(path=str(pdf_path), width=f'{width}px', height=f'{height}px',
                 print_background=True)
        browser.close()
    return str(pdf_path), pdf_path.stat().st_size


if __name__ == '__main__':
    # CLI: python html_to_png.py in.html out.png [width] [height]
    if len(sys.argv) < 3:
        print('用法: python html_to_png.py input.html output.png [width] [height]')
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2]
    w = int(sys.argv[3]) if len(sys.argv) > 3 else 1080
    h = int(sys.argv[4]) if len(sys.argv) > 4 else 1440
    p, size = render_html(inp, out, w, h)
    print(f'[OK] {p}  ({size:,} bytes, {w}x{h} @2x)')
