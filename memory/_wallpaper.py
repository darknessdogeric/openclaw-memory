# -*- coding: utf-8 -*-
"""早安桌面壁纸 - 行星黎明"""
import os, sys, math, random, datetime
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT = r"C:\Users\ericz\Desktop\早安壁纸_行星黎明_2026-11-02.png"
W, H = 1280, 720

rnd = random.Random(1102)
stars = []
for i in range(220):
    x = rnd.uniform(0, W)
    y = rnd.uniform(0, H * 0.62)
    fade = max(0.0, 1.0 - (y / (H * 0.62)) ** 1.5)
    r = rnd.uniform(0.4, 1.5)
    op = rnd.uniform(0.10, 0.80) * fade
    stars.append('<circle cx="%.1f" cy="%.1f" r="%.2f" fill="#FFF6E6" opacity="%.2f"/>' % (x, y, r, op))
# 少量亮星带十字光芒
big = []
for _ in range(7):
    x = rnd.uniform(40, W - 40)
    y = rnd.uniform(20, H * 0.40)
    s = rnd.uniform(1.6, 2.4)
    big.append('<g opacity="%.2f"><circle cx="%.1f" cy="%.1f" r="%.1f" fill="#FFFFFF"/>'
               '<path d="M%.1f %.1f L%.1f %.1f M%.1f %.1f L%.1f %.1f" stroke="#FFF6E6" stroke-width="0.7"/>'
               '</g>' % (rnd.uniform(0.45, 0.85), x, y, s,
                        x - 7, y, x + 7, y, x, y - 7, x, y + 7))

dt = datetime.date(2026, 11, 2)
wd = "星期" + "一二三四五六日"[dt.weekday()]

SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#04060D"/>
      <stop offset="30%"  stop-color="#0A0E1D"/>
      <stop offset="52%"  stop-color="#151833"/>
      <stop offset="70%"  stop-color="#2B2540"/>
      <stop offset="84%"  stop-color="#5A3630"/>
      <stop offset="95%"  stop-color="#A6642C"/>
      <stop offset="100%" stop-color="#E0A45C"/>
    </linearGradient>
    <radialGradient id="sun" cx="63%" cy="82%" r="46%">
      <stop offset="0%"   stop-color="#FFF0CE" stop-opacity="0.98"/>
      <stop offset="22%"  stop-color="#FFC684" stop-opacity="0.62"/>
      <stop offset="50%"  stop-color="#E08A3E" stop-opacity="0.26"/>
      <stop offset="100%" stop-color="#B4622A" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="planet" x1="0" y1="0" x2="0.35" y2="1">
      <stop offset="0%"   stop-color="#14172A"/>
      <stop offset="40%"  stop-color="#0A0C16"/>
      <stop offset="100%" stop-color="#05060C"/>
    </linearGradient>
    <linearGradient id="rim" x1="0.08" y1="0.05" x2="0.95" y2="0.95">
      <stop offset="0%"   stop-color="#FFF3D6" stop-opacity="0.95"/>
      <stop offset="28%"  stop-color="#FFC07A" stop-opacity="0.75"/>
      <stop offset="62%"  stop-color="#D97C3C" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#7A3E1C" stop-opacity="0.12"/>
    </linearGradient>
    <radialGradient id="vign" cx="50%" cy="42%" r="78%">
      <stop offset="55%"  stop-color="#000000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.55"/>
    </radialGradient>
    <filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="9"/>
    </filter>
    <filter id="soft2" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="22"/>
    </filter>
  </defs>

  <rect width="1280" height="720" fill="url(#sky)"/>
  <g>__STARS__</g>
  <g>__BIG__</g>

  <rect width="1280" height="720" fill="url(#sun)"/>

  <!-- 大气辉光（在行星之后被遮住下半） -->
  <circle cx="792" cy="1010" r="404" fill="none" stroke="#FFB870" stroke-width="26" opacity="0.26" filter="url(#soft2)"/>
  <circle cx="792" cy="1010" r="404" fill="none" stroke="#FFD9A0" stroke-width="8"  opacity="0.42" filter="url(#soft)"/>

  <!-- 行星本体 -->
  <circle cx="792" cy="1010" r="404" fill="url(#planet)"/>
  <circle cx="792" cy="1010" r="404" fill="none" stroke="url(#rim)" stroke-width="3.2"/>
  <circle cx="792" cy="1010" r="404" fill="none" stroke="#FFC98C" stroke-width="10" opacity="0.30" filter="url(#soft)"/>

  <!-- 地表微光 -->
  <ellipse cx="640" cy="690" rx="300" ry="90" fill="#8A4E1E" opacity="0.10" filter="url(#soft2)"/>

  <rect width="1280" height="720" fill="url(#vign)"/>

  <!-- 文案 -->
  <g>
    <rect x="92" y="252" width="86" height="4" fill="#D8A06A"/>
    <text x="92" y="352" font-family="Noto Serif SC, Songti SC, serif" font-size="96" font-weight="700"
          fill="#F4EFE5" letter-spacing="12">早安</text>
    <text x="96" y="404" font-family="Noto Sans SC, PingFang SC, Microsoft YaHei, sans-serif"
          font-size="23" fill="#BDB5A8" letter-spacing="4.5">不必先有答案，再出发。</text>
  </g>

  <!-- 页脚 -->
  <text x="92" y="664" font-family="Noto Sans SC, PingFang SC, Microsoft YaHei, sans-serif"
        font-size="14" fill="#7E7668" letter-spacing="3">B166ER · __DATE__ · __WD__</text>
  <text x="1188" y="664" text-anchor="end" font-family="Noto Sans SC, PingFang SC, Microsoft YaHei, sans-serif"
        font-size="14" fill="#6A6357" letter-spacing="3">第 15 格 · 深空边缘</text>
</svg>
"""

SVG = SVG.replace("__STARS__", "".join(stars)).replace("__BIG__", "".join(big))
SVG = SVG.replace("__DATE__", "2026.11.02").replace("__WD__", wd)

HTML = ('<!DOCTYPE html><html><head><meta charset="utf-8"><style>'
        'html,body{margin:0;padding:0;background:#04060D;width:1280px;height:720px;overflow:hidden}'
        'svg{display:block}</style></head><body>' + SVG + '</body></html>')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
    pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
    pg.set_content(HTML, wait_until="load")
    pg.wait_for_timeout(700)
    pg.screenshot(path=OUT, full_page=False, omit_background=False, timeout=25000)
    pg.close()
    b.close()

from PIL import Image
im = Image.open(OUT)
print("OK", OUT)
print("  size:", im.size, " ratio 1:%.3f" % (im.size[1] / im.size[0]))
print("  bytes:", os.path.getsize(OUT))
