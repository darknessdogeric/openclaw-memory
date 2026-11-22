# -*- coding: utf-8 -*-
"""先驱者 6 图 - Playwright 渲染 + geo_v4 原版 PIL 水印"""
import sys
from pathlib import Path
sys.path.insert(0, r"D:\B166ER-openclaw\workspace\toolbox")
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright
import xhs_pioneer as M

OUT = M.OUT_DIR
TOTAL = M.TOTAL


def page_html(idx, body_html):
    return ('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">'
            '<title>先驱者 Slide ' + str(idx) + '</title><style>' + M.COMMON_CSS + '</style></head><body>'
            '<div class="slide">'
            '<div class="masthead"><div class="brand">B166ER · 商业内参</div>'
            '<div class="date">' + M.ISSUE + '</div></div>'
            '<div class="content">' + body_html + '</div>'
            '<div class="footer"><div class="source">' + M.SOURCE + '</div>'
            '<div class="page">' + ("%02d / %02d" % (idx, TOTAL)) + '</div></div>'
            '</div></body></html>')


def pil_watermark(png_path):
    p = Path(png_path)
    wm = p.with_name(p.stem + "_wm.png")
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
    draw.rectangle([(0, 50), (200, 100)], fill=(10, 37, 64, 200))
    draw.text((16, 64), "B166ER · GEO", fill=(255, 255, 255, 255), font=font)
    draw.text((w - 220, h - 34), "© B166ER · 2026.11.01", fill=(10, 37, 64, 240), font=font_tiny)
    wm_text = "B166ER · 2026.11.01"
    bbox = draw.textbbox((0, 0), wm_text, font=font_big)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    txt_img = Image.new("RGBA", (tw + 40, th + 40), (0, 0, 0, 0))
    td = ImageDraw.Draw(txt_img)
    td.text((20, 20), wm_text, fill=(200, 200, 200, 40), font=font_big)
    txt_img = txt_img.rotate(-22, expand=True)
    overlay.paste(txt_img, ((w - txt_img.size[0]) // 2, (h - txt_img.size[1]) // 2), txt_img)
    out = Image.alpha_composite(img, overlay).convert("RGB")
    out.save(wm, "PNG", optimize=True)
    return wm


CHECK = """() => {
  const issues = [];
  const R = (e) => e.getBoundingClientRect();
  const tx = (e) => (e.textContent || '').trim();
  document.querySelectorAll('.content *').forEach(el => {
    if (el.children.length === 0 && tx(el)) {
      if (el.scrollWidth > el.clientWidth + 2)
        issues.push('文字溢出: ' + (el.className||el.tagName) + ' :: ' + tx(el).slice(0,20));
    }
  });
  const c = document.querySelector('.content');
  if (c) {
    const cr = R(c);
    document.querySelectorAll('.content > *').forEach(el => {
      const r = R(el);
      if (r.bottom > cr.bottom + 2)
        issues.push('内容溢出content: ' + (el.className||el.tagName) + ' 超' + Math.round(r.bottom - cr.bottom) + 'px');
      if (r.right > cr.right + 2 || r.left < cr.left - 2)
        issues.push('内容出血: ' + (el.className||el.tagName));
    });
  }
  const mh = document.querySelector('.masthead'), ft = document.querySelector('.footer');
  if (mh && ft) {
    const mr = R(mh), fr = R(ft);
    document.querySelectorAll('.content *').forEach(el => {
      if (!tx(el) || el.children.length) return;
      const r = R(el);
      if (r.top < mr.bottom - 2) issues.push('压masthead: ' + tx(el).slice(0,16));
      if (r.bottom > fr.top + 2) issues.push('压footer: ' + tx(el).slice(0,16));
    });
  }
  return issues;
}"""


def main():
    print("CSS chars:", len(M.COMMON_CSS))
    bad = 0
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
        for i, body in enumerate(M.SLIDES, 1):
            html = page_html(i, body)
            hp = OUT / ("slide_%02d.html" % i)
            hp.write_text(html, encoding="utf-8")
            pg = b.new_page(viewport={"width": 1080, "height": 1440}, device_scale_factor=2)
            pg.set_content(html, wait_until="domcontentloaded")
            pg.wait_for_timeout(350)
            iss = pg.evaluate(CHECK)
            pp = OUT / ("slide_%02d.png" % i)
            pg.screenshot(path=str(pp), full_page=False, omit_background=False, timeout=25000)
            pg.close()
            w = pil_watermark(pp)
            if iss:
                bad += 1
            print("Slide %02d  %s  %d B  wm %d B  %s" % (i, "OK  " if not iss else "WARN", pp.stat().st_size, w.stat().st_size, "" if not iss else "| " + " ; ".join(iss[:4])))
        b.close()
    print("=== DONE ===", OUT, "| pages with issues:", bad)


main()
