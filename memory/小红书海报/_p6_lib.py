# -*- coding: utf-8 -*-
"""先驱者系列 6 图笔记 - 深空主题库 (重写版, 无密度空隙)"""
import os, sys, base64, random
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT = r"C:\Users\ericz\Desktop\小红书_先驱者系列6图_2026-11-01"
os.makedirs(OUT, exist_ok=True)
HERO_PATH = r"D:\B166ER-openclaw\media\tool-image-generation\pioneer_hero---f0ca0c99-3e0b-41ee-a8a6-22fc4eaaba1c.png"


def hero_b64():
    with open(HERO_PATH, "rb") as f:
        return base64.b64encode(f.read()).decode()


CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;overflow:hidden;position:relative;
 background:radial-gradient(125% 62% at 50% 4%,#1b1f2b 0%,#0c0e15 46%,#06070b 100%);color:#e9e4da;
 font-family:"Noto Sans SC","PingFang SC","Microsoft YaHei",sans-serif}
.wrap{position:relative;z-index:3;width:100%;height:100%;padding:56px 74px 50px 50px;display:flex;flex-direction:column}
.bg{position:absolute;inset:0;z-index:1}
.head{flex:0 0 auto}
.kick{font-size:19px;color:#d8a06a;letter-spacing:4.5px;font-weight:700;margin-bottom:16px}
h1{font-size:64px;font-weight:900;line-height:1.18;letter-spacing:-.6px;font-family:"Noto Serif SC","Songti SC",serif}
h1 .hl{color:#d8a06a}
h2{font-size:48px;font-weight:900;line-height:1.22;font-family:"Noto Serif SC","Songti SC",serif}
h2 .num{font-size:21px;font-weight:900;color:#d8a06a;letter-spacing:2px;display:block;margin-bottom:12px}
.sub{font-size:22px;color:#a8a094;line-height:1.55;margin-top:16px}
.body{flex:1 1 auto;display:flex;flex-direction:column;justify-content:space-between;gap:16px;min-height:0;padding:22px 0}
.foot{flex:0 0 auto;border-top:1px solid rgba(233,228,218,.16);padding-top:18px;margin-top:14px}
.foot .q{font-size:27px;font-weight:800;line-height:1.5}
.foot .q b{color:#d8a06a}
.foot .s{font-size:16px;color:#8e867a;margin-top:12px;line-height:1.65}
.card{background:rgba(255,255,255,.05);border:1px solid rgba(233,228,218,.14);border-radius:8px;padding:28px 26px}
.card.acc{border-color:#d8a06a;border-width:1.5px;background:rgba(216,160,106,.1)}
.card .t{font-size:22px;font-weight:800;color:#e9e4da;margin-bottom:10px;display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.card .t .tag{font-size:13.5px;font-weight:700;color:#a8a094;background:rgba(255,255,255,.08);padding:3px 10px;border-radius:4px;white-space:nowrap;letter-spacing:.5px}
.card.acc .t .tag{background:#d8a06a;color:#14161d}
.card .d{font-size:19px;color:#c3bcb0;line-height:1.72}
.card .d b{color:#f2ede3;font-weight:700}
.card.acc .d b{color:#e8b478}
.g3c{background:rgba(255,255,255,.05);border:1px solid rgba(233,228,218,.14);border-radius:8px;padding:28px 20px}
.g3c.acc{background:rgba(216,160,106,.1);border-color:#d8a06a;border-width:1.5px}
.g3c .k{font-size:13.5px;color:#8e867a;letter-spacing:1.4px;margin-bottom:8px;font-weight:700}
.g3c .v{font-size:34px;font-weight:900;color:#e9e4da;line-height:1.15;margin-bottom:8px}
.g3c.acc .v{color:#e8b478}
.g3c .d{font-size:16.5px;color:#a8a094;line-height:1.62}
.g3c .d b{color:#e9e4da}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.row3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.tl{display:flex;flex-direction:column;gap:20px}
.tlrow{display:flex;gap:16px;align-items:flex-start}
.tlrow .yr{flex:0 0 96px;font-size:25px;font-weight:900;color:#d8a06a;line-height:1.2}
.tlrow .tx{flex:1;border-left:2px solid rgba(216,160,106,.34);padding-left:17px}
.tlrow .tx .h{font-size:20.5px;font-weight:800;color:#e9e4da;margin-bottom:6px}
.tlrow .tx .p{font-size:17px;color:#a8a094;line-height:1.68}
.tlrow .tx .p b{color:#e9e4da}
.tlrow .tx .q{font-size:17.5px;color:#d8a06a;line-height:1.6;margin-top:8px;font-weight:600}
.gate{border-left:3px solid #d8a06a;padding-left:18px}
.gate .gh{font-size:22px;font-weight:800;color:#e9e4da;margin-bottom:8px}
.gate .gp{font-size:17.5px;color:#a8a094;line-height:1.75}
.gate .gp b{color:#d8a06a}
.cmp{display:grid;grid-template-columns:120px 1fr 1fr;gap:18px 18px;align-items:start}
.cmp .ch{font-size:16px;font-weight:800;color:#d8a06a;letter-spacing:.6px}
.cmp .cc{font-size:18px;color:#e9e4da;line-height:1.6;background:rgba(255,255,255,.05);border:1px solid rgba(233,228,218,.13);border-radius:6px;padding:20px 20px}
.cmp .cc.a{background:rgba(216,160,106,.11);border-color:rgba(216,160,106,.5)}
.cmp .cc b{color:#e8b478}
.cmp .c0{font-size:17.5px;color:#8e867a;padding-top:8px}
.plaque{display:flex;flex-direction:column;gap:22px}
.plq{display:flex;gap:15px;align-items:flex-start}
.plq .pn{flex:0 0 36px;height:36px;border-radius:5px;background:#d8a06a;color:#14161d;font-size:17px;font-weight:900;display:flex;align-items:center;justify-content:center}
.plq .pt{font-size:19.5px;color:#c3bcb0;line-height:1.6;padding-top:5px}
.plq .pt b{color:#e9e4da;font-weight:700}
.figw{border:1px solid rgba(233,228,218,.13);border-radius:9px;padding:20px;background:rgba(255,255,255,.035)}
.heroimg{width:100%;border-radius:9px;display:block;border:1px solid rgba(233,228,218,.15)}
.bigline{display:flex;align-items:baseline;gap:14px}
.bigline .n{font-size:58px;font-weight:900;color:#d8a06a;line-height:1}
.bigline .u{font-size:19px;color:#a8a094;line-height:1.5}
.tags{font-size:15px;color:#8e867a;letter-spacing:.3px;line-height:1.6}
.brand{position:absolute;top:13px;right:13px;z-index:9;width:54px;height:54px;border-radius:7px;background:#d8a06a;display:flex;flex-direction:column;align-items:center;justify-content:center}
.brand .bn{font-size:21px;font-weight:900;color:#14161d;line-height:1}
.brand .bl{font-size:6.5px;color:rgba(20,22,29,.85);letter-spacing:1.1px;margin-top:2px;line-height:1}
.wm{position:absolute;bottom:9px;left:50px;z-index:9;font-size:12px;color:#6a6459;letter-spacing:1.4px;font-family:"Courier New",monospace}
"""

CIRCLE = '<circle cx="%.1f" cy="%.1f" r="%.2f" fill="#FFF7E8" opacity="%.2f"/>'


def stars(n=170, seed=1972):
    rnd = random.Random(seed)
    o = []
    for i in range(n):
        x = rnd.uniform(0, 1080)
        y = rnd.uniform(0, 1920)
        r = rnd.uniform(0.5, 2.1)
        op = rnd.uniform(0.12, 0.85)
        o.append(CIRCLE % (x, y, r, op))
    return "".join(o)


def bg_svg():
    return ('<svg class="bg" viewBox="0 0 1080 1920" width="1080" height="1920">' + stars()
            + '<circle cx="840" cy="300" r="240" fill="#d8a06a" opacity="0.05"/>'
            + '<circle cx="840" cy="300" r="150" fill="#e8b478" opacity="0.05"/>'
            + "</svg>")


def page(idx, total, kicker, title_html, sub, body, foot_q="", foot_s=""):
    h = []
    h.append('<div class="wrap">')
    h.append('<div class="head">')
    h.append('<div class="kick">' + kicker + '</div>')
    h.append(title_html)
    if sub:
        h.append('<div class="sub">' + sub + '</div>')
    h.append('</div>')
    h.append('<div class="body">' + body + '</div>')
    h.append('<div class="foot">')
    if foot_q:
        h.append('<div class="q">' + foot_q + '</div>')
    if foot_s:
        h.append('<div class="s">' + foot_s + '</div>')
    h.append('</div></div>')
    h.append('<div class="brand"><div class="bn">B</div><div class="bl">B166ER</div></div>')
    h.append('<div class="wm">先驱者系列 · ' + str(idx) + ' / ' + str(total) + ' &middot; 2026-11-01</div>')
    return ('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><title>' + kicker
            + '</title><style>' + CSS + '</style></head><body>' + bg_svg() + "".join(h) + '</body></html>')
