# -*- coding: utf-8 -*-
"""Playwright 渲染 9 张 + 自检（尺寸／B标／重叠溢出）"""
import io, os, sys, time
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from playwright.sync_api import sync_playwright

OUT = r'C:\Users\ericz\Desktop\产业发展部\外部相关资料\全面预算管理\小红书9图_预算模板'
HTMLD = os.path.join(OUT, "html")
PNGD = os.path.join(OUT, "png")
os.makedirs(PNGD, exist_ok=True)

import glob as _glob
KEYS = sorted(os.path.splitext(os.path.basename(p))[0] for p in _glob.glob(os.path.join(HTMLD, "*.html")))
print("渲染清单:", KEYS)

PROBE = """() => {
  const ps=[...document.querySelectorAll('.main *')].filter(e=>{
    const t=(e.textContent||'').trim(); return t.length>0 && e.children.length===0;});
  const R=[];
  for(const e of ps){
    const disp=getComputedStyle(e).display;
    const cls=e.className||e.tagName;
    const tx=e.textContent.trim().slice(0,30);
    if(disp==='inline'||disp==='inline-block'||disp==='inline-flex'){
      const rg=document.createRange(); rg.selectNodeContents(e);
      for(const r of rg.getClientRects()){
        if(r.width>0.5&&r.height>0.5) R.push({r,t:tx,cls:cls});
      }
    } else {
      R.push({r:e.getBoundingClientRect(),t:tx,cls:cls});
    }
  }
  const mainEl=document.querySelector('.main');
  const scope=[...mainEl.querySelectorAll('*')].filter(e=>{
    const t=(e.textContent||'').trim(); return t.length>0 && e.children.length===0;});
  let ov=0,out=0,wide=0,maxR=-1e9,maxB=-1e9;
  for(const x of R){
    const r=x.r;
    if(r.right>maxR)maxR=r.right; if(r.bottom>maxB)maxB=r.bottom;
    if(r.left<-0.6||r.top<-0.6||r.right>1080.6||r.bottom>1440.6) out++;
    if(r.width>1080) wide++;
  }
  for(let i=0;i<R.length;i++) for(let j=i+1;j<R.length;j++){
    const a=R[i].r,b=R[j].r;
    const ix=Math.min(a.right,b.right)-Math.max(a.left,b.left);
    const iy=Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top);
    if(ix>1.2&&iy>1.2) ov++;
  }
  const posterKids=document.querySelector('.poster').children.length;
  const mainH=Math.round(document.querySelector('.main').getBoundingClientRect().height);
  const bs=document.querySelectorAll('.bbig,.bsm').length;
  const bt=document.body.innerText.includes('ERIC & B166ER');
  const main=document.querySelector('.main');
  const mr=main.getBoundingClientRect();
  let mb=0;
  for(const e of main.querySelectorAll('*')){const r=e.getBoundingClientRect(); if(r.height>0.5) mb=Math.max(mb,r.bottom);}
  const fill=Math.round((mb-mr.top)/(mr.height)*100);
  return {n:R.length, ov:ov, out:out, wide:wide, maxR:Math.round(maxR), maxB:Math.round(maxB), bs:bs, bt:bt, fill:fill, kids:posterKids, mainH:mainH};
}"""

ok_all = True
with sync_playwright() as pw:
    b = pw.chromium.launch(args=["--disable-gpu", "--font-render-hinting=none"])
    ctx = b.new_context(viewport={"width": 1080, "height": 1440}, device_scale_factor=2)
    for k in KEYS:
        hp = os.path.join(HTMLD, k + ".html")
        pp = os.path.join(PNGD, k + ".png")
        if os.path.exists(pp):
            os.remove(pp)
        pg = ctx.new_page()
        pg.goto("file:///" + hp.replace("\\", "/"), wait_until="networkidle")
        pg.wait_for_timeout(450)
        pr = pg.evaluate(PROBE)
        pg.screenshot(path=pp, clip={"x": 0, "y": 0, "width": 1080, "height": 1440})
        pg.close()
        sz = os.path.getsize(pp) // 1024 if os.path.exists(pp) else 0
        from PIL import Image
        with Image.open(pp) as im:
            wh = im.size
        good = (sz >= 40 and pr["ov"] == 0 and pr["out"] == 0 and pr["wide"] == 0
                and pr["bs"] == 2 and pr["bt"] and wh == (2160, 2880)
                and pr["maxB"] <= 1441 and pr["maxR"] <= 1081 and pr["fill"] >= 88
                and pr["kids"] == 3 and pr["mainH"] == 1240)
        ok_all = ok_all and good
        print(("  OK   " if good else "  CHECK") + k + "  " + str(sz) + " KB  " + str(wh)
              + "  文本" + str(pr["n"]) + " 重叠" + str(pr["ov"]) + " 越界" + str(pr["out"])
              + " B标" + str(pr["bs"]) + " 填充" + str(pr["fill"]) + "% 底" + str(pr["maxB"])
              + " poster子项" + str(pr["kids"]) + " mainH" + str(pr["mainH"]))
    b.close()
print("ALL:", "PASS" if ok_all else "NEEDS FIX")
