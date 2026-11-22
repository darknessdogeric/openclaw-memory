#!/usr/bin/env python3
"""
visual_check.py — 视觉自检成本控制器 (2026-10-25)

背景: 渲染成品后用 view_image 自检, 原图 (2160x3840) 每次 ~11,000 视觉 token,
      且图片进上下文后不退出, 之后每轮都重付 -> 一次海报迭代 4 版 = 33,000 tok。

本工具提供三个降本手段:
  thumb  <img>              生成 <=800px 缩略图 (11,059 -> 1,517 tok, 降 86%)
  sheet  <img1> <img2> ...  多图拼一张对比图 (一次 view 看全部, 省 N-1 次往返)
  probe  <img>              程序化体检: 尺寸/四角底色/非背景占比/内容边界
                             (能替代大部分人眼检查, 0 token)

用法:
  python tools/visual_check.py sheet out/*.png --out _check.png --cols 3
  python tools/visual_check.py thumb a.png --out a_thumb.png --width 800
  python tools/visual_check.py probe a.png
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    from PIL import Image
except ImportError:
    print("[X] 需要 Pillow: pip install pillow")
    raise SystemExit(1)


def cmd_thumb(args):
    src = Path(args.img)
    im = Image.open(src).convert("RGB")
    w0, h0 = im.size
    w = args.width
    h = int(h0 * w / w0)
    out = Path(args.out) if args.out else src.with_name(src.stem + "_thumb.png")
    im.resize((w, h), Image.LANCZOS).save(out)
    t0, t1 = w0 * h0 / 750, w * h / 750
    print(f"OK {out.name}  {w0}x{h0} -> {w}x{h}   tok {t0:,.0f} -> {t1:,.0f} (降 {(1-t1/t0)*100:.0f}%)")
    return 0


def cmd_sheet(args):
    files = [Path(f) for f in args.imgs]
    if not files:
        print("[X] 没有输入图")
        return 1
    cols = args.cols
    cell_w = args.width
    thumbs = []
    for f in files:
        im = Image.open(f).convert("RGB")
        h = int(im.size[1] * cell_w / im.size[0])
        thumbs.append((f.name, im.resize((cell_w, h), Image.LANCZOS)))
    rows = (len(thumbs) + cols - 1) // cols
    row_h = [max(t[1].size[1] for t in thumbs[r * cols:(r + 1) * cols]) for r in range(rows)]
    lab_h = 22
    gap = 8
    W = cols * cell_w + (cols + 1) * gap
    H = sum(row_h) + rows * (lab_h + gap) + gap
    sheet = Image.new("RGB", (W, H), "#1a1a1a")
    from PIL import ImageDraw
    d = ImageDraw.Draw(sheet)
    y = gap
    for r in range(rows):
        x = gap
        for name, t in thumbs[r * cols:(r + 1) * cols]:
            d.text((x + 2, y), name[:46], fill="#dddddd")
            sheet.paste(t, (x, y + lab_h))
            x += cell_w + gap
        y += row_h[r] + lab_h + gap
    out = Path(args.out)
    sheet.save(out)
    # 单张拼接图的 token 远小于 N 张原图
    t_sheet = sheet.size[0] * sheet.size[1] / 750
    t_sep = sum(Image.open(f).size[0] * Image.open(f).size[1] / 750 for f in files)
    print(f"OK {out.name}  {sheet.size}  {len(files)} 张合一")
    print(f"   tok: 分开看 {t_sep:,.0f} -> 合看 {t_sheet:,.0f} (降 {(1-t_sheet/t_sep)*100:.0f}%)")
    return 0


def cmd_probe(args):
    src = Path(args.img)
    im = Image.open(src).convert("RGB")
    w, h = im.size
    print(f"文件 {src.name}  尺寸 {w}x{h}  视觉tok {w*h/750:,.0f}")
    # 四角底色
    corners = {"左上": (4, 4), "右上": (w - 5, 4), "左下": (4, h - 5), "右下": (w - 5, h - 5)}
    bg = im.getpixel(corners["左上"])
    print(f"  底色(左上) {bg}")
    for k, p in corners.items():
        c = im.getpixel(p)
        drift = sum(abs(a - b) for a, b in zip(c, bg))
        print(f"  {k} {c}  偏移 {drift:>4}  {'✅' if drift < 18 else '⚠️ 非纯底色(可能是出血图)'}")
    # 非背景像素占比 (估算内容密度)
    step = max(1, min(w, h) // 160)
    tot = fg = 0
    for yy in range(0, h, step):
        for xx in range(0, w, step):
            tot += 1
            if sum(abs(a - b) for a, b in zip(im.getpixel((xx, yy)), bg)) > 26:
                fg += 1
    pct = fg / max(1, tot) * 100
    print(f"  内容像素占比 {pct:.1f}%")
    if pct < 8:
        print("  ⚠️ 内容过少 -> 可能有大片空白(检查下半页是否空)")
    elif pct > 82:
        print("  ⚠️ 内容过密 -> 可能有溢出/重叠")
    else:
        print("  ✅ 密度正常")
    print(f"  建议: 自检用 800px 缩略 (≈{800*800/750:,.0f} tok) 而非原图 ({w*h/750:,.0f} tok)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("thumb"); t.add_argument("img"); t.add_argument("--out"); t.add_argument("--width", type=int, default=800)
    t.set_defaults(fn=cmd_thumb)
    s = sub.add_parser("sheet"); s.add_argument("imgs", nargs="+"); s.add_argument("--out", default="_check.png")
    s.add_argument("--cols", type=int, default=3); s.add_argument("--width", type=int, default=520)
    s.set_defaults(fn=cmd_sheet)
    p = sub.add_parser("probe"); p.add_argument("img")
    p.set_defaults(fn=cmd_probe)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
