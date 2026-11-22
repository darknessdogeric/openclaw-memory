# -*- coding: utf-8 -*-
import io, os, sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from playwright.sync_api import sync_playwright

OUT = r'C:\Users\ericz\Desktop\产业发展部\外部相关资料\全面预算管理\小红书9图_预算模板'
HTMLD = os.path.join(OUT, "html")

PROBE = """() => {
  const ps=[...document.querySelectorAll('.poster *')].filter(e=>{
    const t=(e.textContent||'').trim(); return t.length>0 && e.children.length===0;});
  const R=[];
  for(const e of ps){
    const disp=getComputedStyle(e).display;
    const tx=e.textContent.trim().slice(0,26), cls=e.className||e.tagName;
    if(disp==='inline'||disp==='inline-block'||disp==='inline-flex'){
      const rg=document.createRange(); rg.selectNodeContents(e);
      for(const r of rg.getClientRects()) if(r.width>0.5&&r.height>0.5) R.push({r,t:tx,cls:cls});
    } else R.push({r:e.getBoundingClientRect(),t:tx,cls:cls});
  }
  const ovs=[];
  for(let i=0;i<R.length;i++) for(let j=i+1;j<R.length;j++){
    const a=R[i].r,b=R[j].r;
    const ix=Math.min(a.right,b.right)-Math.max(a.left,b.left);
    const iy=Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top);
    if(ix>1.2&&iy>1.2) ovs.push([R[i].t,R[i].cls,R[j].t,R[j].cls,
      Math.round(a.left),Math.round(a.top),Math.round(a.right),Math.round(a.bottom),
      Math.round(b.left),Math.round(b.top),Math.round(b.right),Math.round(b.bottom)]);
  }
  const main=document.querySelector('.main'); const mr=main.getBoundingClientRect();
  let mb=0; for(const e of main.querySelectorAll('*')){const r=e.getBoundingClientRect(); if(r.height>0.5) mb=Math.max(mb,r.bottom);}
  const lastChild=main.lastElementChild; const lr=lastChild.getBoundingClientRect();
  return {ovs:ovs, fill:Math.round((mb-mr.top)/mr.height*100), mainH:Math.round(mr.height),
          contentH:Math.round(mb-mr.top), lastTag:lastChild.className, lastBottom:Math.round(lr.bottom)};
}"""

KEYS = sorted(os.path.splitext(os.path.basename(p))[0] for p in __import__('glob').glob(os.path.join(HTMLD, "*.html")))
with sync_playwright() as pw:
    b = pw.chromium.launch(args=["--disable-gpu", "--font-render-hinting=none"])
    ctx = b.new_context(viewport={"width": 1080, "height": 1440}, device_scale_factor=1)
    for k in KEYS:
        pg = ctx.new_page()
        pg.goto("file:///" + os.path.join(HTMLD, k + ".html").replace("\\", "/"), wait_until="networkidle")
        pg.wait_for_timeout(300)
        pr = pg.evaluate(PROBE)
        need = 88 - pr["fill"]
        print("%-16s fill %3d%%  内容高 %4d / 可用 %4d  缺 %4dpx  末块 %s" %
              (k, pr["fill"], pr["contentH"], pr["mainH"], max(0, int(need)), pr["lastTag"]))
        for o in pr["ovs"][:4]:
            print("      OV A[%s|%s] x%d y%d r%d b%d  B[%s|%s] x%d y%d r%d b%d" %
                  (o[0], o[1], o[4], o[5], o[6], o[7], o[2], o[3], o[8], o[9], o[10], o[11]))
        pg.close()
    b.close()
