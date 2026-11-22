# -*- coding: utf-8 -*-
import io, os, sys, json
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
  const R=ps.map(e=>({e,r:e.getBoundingClientRect(),t:e.textContent.trim().slice(0,30),
    cls:e.className||e.tagName}));
  const out=[];
  for(let i=0;i<R.length;i++) for(let j=i+1;j<R.length;j++){
    const a=R[i].r,b=R[j].r;
    const ix=Math.min(a.right,b.right)-Math.max(a.left,b.left);
    const iy=Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top);
    if(ix>1.2&&iy>1.2) out.push([R[i].t,R[i].cls,R[j].t,R[j].cls,
      Math.round(a.left),Math.round(a.top),Math.round(a.right),Math.round(a.bottom),
      Math.round(b.left),Math.round(b.top),Math.round(b.right),Math.round(b.bottom)]);
  }
  return out;
}"""

with sync_playwright() as pw:
    b = pw.chromium.launch(args=["--disable-gpu", "--font-render-hinting=none"])
    ctx = b.new_context(viewport={"width": 1080, "height": 1440}, device_scale_factor=1)
    for k in ("p01_cover", "p08_delivery"):
        pg = ctx.new_page()
        pg.goto("file:///" + os.path.join(HTMLD, k + ".html").replace("\\", "/"), wait_until="networkidle")
        pg.wait_for_timeout(350)
        res = pg.evaluate(PROBE)
        print("=== " + k + " 重叠 " + str(len(res)) + " 对 ===")
        for r in res:
            print("   A[%s|%s] x=%d y=%d r=%d b=%d" % (r[0], r[1], r[4], r[5], r[6], r[7]))
            print("   B[%s|%s] x=%d y=%d r=%d b=%d" % (r[2], r[3], r[8], r[9], r[10], r[11]))
        pg.close()
    b.close()
