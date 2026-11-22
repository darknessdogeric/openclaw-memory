# -*- coding: utf-8 -*-

"""make_topology.py - 自我进化信息拓扑图生成器（可复用 · 单一 SVG 源 · 两版输出）

用法:
    python toolbox/make_topology.py              # 出两版 + 三层质检
    python toolbox/make_topology.py --only 9x16
版式: 3:4 (1080x1440) / 9:16 (1080x1920) 手机竖版
★ 设计纪律:
  1) 模板零 % 格式化（CSS 含大量字面 %）—— 用 @@TOKEN@@ + .replace()
  2) 两版共用同一份 SVG 坐标（3:4 等比缩放），杜绝"两套坐标各自漂移"
  3) 三层质检: L1 盒模型 / L2 SVG 元素级(重叠·越界·压曲线·死白) / L3 视觉核验(人工看缩略图)
"""
import io, sys, os, re, json, glob
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "output", "infra_experience")
os.makedirs(OUT, exist_ok=True)
HOME = os.path.expanduser("~")
SI = os.path.join(HOME, "self-improving")

# ---------------- 单一 SVG 坐标源（已过 QA 与视觉核验） ----------------
SVG_W = 964
SVG_H = 1240
# 版式: 页高 / SVG 容器高 / 缩放 / 标题号 / 正文号 / 卡片号
PAGES = {
  "9x16": dict(page=(1080, 1920), box=1240, scale=1.0,   h1=53, lede=19.5, chipv=20, cardh=20, cardp=15.5),
  "3x4":  dict(page=(1080, 1440), box=826,  scale=0.666, h1=46, lede=18,   chipv=18, cardh=18, cardp=14.5),
}

def _cnt(p):
    return len([f for f in glob.glob(os.path.join(p, "**", "*"), recursive=True) if os.path.isfile(f)])

def load_vals():
    hm = open(os.path.join(SI, "memory.md"), encoding="utf-8").read()
    ct = open(os.path.join(SI, "corrections.md"), encoding="utf-8").read()
    return {
        "DOMAINS": _cnt(os.path.join(SI, "domains")),
        "PROJECTS": _cnt(os.path.join(SI, "projects")),
        "RULES": _cnt(os.path.join(SI, "rules")),
        "ARCHIVE": _cnt(os.path.join(SI, "archive")),
        "EVAL": _cnt(os.path.join(SI, "eval")),
        "TOPICS": len(glob.glob(os.path.join(SI, "rules_*.md"))),
        "MEMLINES": hm.count("\n") + 1,
        "MEMCHARS": len(hm),
        "CORRCHARS": len(ct),
        "RATIO": round(len(ct) / max(len(hm), 1), 1),
    }

TPL = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#0B0908}
body{width:@@PW@@px;height:@@PH@@px;overflow:hidden;position:relative;
 background:
  radial-gradient(1000px 700px at 50% 13%, rgba(212,168,79,.11), transparent 62%),
  linear-gradient(178deg,#17120E 0%,#0B0908 56%,#100C0A 100%);
 font-family:'Noto Sans SC','Microsoft YaHei',sans-serif;color:#F2E9D8}
.grain{position:absolute;inset:0;opacity:.03;pointer-events:none;
 background-image:radial-gradient(circle at 1px 1px, rgba(242,233,216,.9) 1px, transparent 0);background-size:4px 4px}
.wrap{padding:40px 58px 30px 58px;height:100%;display:flex;flex-direction:column;position:relative}
.top{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid rgba(212,168,79,.30);padding-bottom:12px}
.badge{display:flex;align-items:center;gap:12px}
.badge .circle{width:42px;height:42px;border-radius:50%;background:#D4A84F;color:#14100D;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:22px;font-family:Georgia,serif}
.badge .name{font-weight:800;font-size:19px;letter-spacing:1.4px}
.badge .name .x{color:#D4A84F}
.top .chapter{font-size:15px;font-weight:700;letter-spacing:3px;color:#8A7A66;text-align:right;line-height:1.35}
.top .chapter b{color:#D4A84F}
.kicker{font-size:17px;letter-spacing:5px;color:#D4A84F;font-weight:800;margin:18px 0 9px;text-align:center}
h1{font-family:'Noto Serif SC',serif;font-size:@@H1@@px;font-weight:900;line-height:1.2;text-align:center;letter-spacing:2px}
h1 .hl{color:#C8102E}
.lede{font-size:@@LEDE@@px;color:#B7A68F;text-align:center;line-height:1.62;margin:10px 0 0}
.lede b{color:#F2E9D8;font-weight:800}
.lede .g{color:#D4A84F;font-weight:800}
.chips{display:grid;grid-template-columns:repeat(4,1fr);gap:11px;margin:16px 0 2px}
.chip{border:1px solid rgba(212,168,79,.28);border-radius:10px;padding:9px 12px;background:rgba(255,255,255,.024)}
.chip .k{font-size:12.5px;letter-spacing:1.1px;color:#8A7A66;font-weight:700;margin-bottom:4px}
.chip .v{font-size:@@CHIPV@@px;font-weight:800;color:#F2E9D8;line-height:1.2}
.chip .v em{font-style:normal;color:#D4A84F}
.chip .v s{text-decoration:none;color:#C8102E}
.svgbox{width:964px;height:@@BOX@@px;margin:4px auto 0;overflow:hidden;position:relative}
.topo{position:absolute;top:0;left:50%;transform-origin:top left;transform:translateX(-50%) scale(@@SCALE@@);width:964px;height:1240px}
.topo text{font-family:'Noto Sans SC','Microsoft YaHei',sans-serif}
.tn{font-size:22px;font-weight:800;fill:#F2E9D8}
.tn2{font-size:16px;fill:#A2907A}
.tx{font-size:16.5px;fill:#B7A68F}
.tb{font-size:26px;font-weight:800;fill:#E7C378}
.el{font-size:15px;fill:#9A8A76}
.elg{fill:#D4A84F}
.elr{fill:#C8102E;font-weight:700}
.tl{font-size:16.5px;fill:#B7A68F}
.td{font-size:16px;fill:#8A7A66}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:13px;margin:10px 0 0}
.card{border:1px solid rgba(212,168,79,.24);border-radius:12px;padding:14px 16px;background:rgba(255,255,255,.024)}
.card .h{font-size:@@CARDH@@px;font-weight:900;letter-spacing:.6px;margin-bottom:7px;color:#E7C378}
.card p{font-size:@@CARDP@@px;line-height:1.6;color:#A2907A}
.card p b{color:#F2E9D8;font-weight:800}
.card p .r{color:#C8102E;font-weight:700}
.footer{display:flex;justify-content:space-between;align-items:center;border-top:1px solid rgba(212,168,79,.30);padding-top:11px;margin-top:auto}
.footer .credit{font-size:14px;font-weight:700;letter-spacing:1.6px;color:#8A7A66}
.footer .credit .x{color:#D4A84F}
.footer .tag{font-size:12.5px;color:#6E5F4D;letter-spacing:4px}
.footer .circle{width:32px;height:32px;border-radius:50%;background:#D4A84F;color:#14100D;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:17px;font-family:Georgia,serif}
</style></head>
<body>
<div class="grain"></div>
<div class="wrap">
 <div class="top">
  <div class="badge"><div class="circle">B</div><div class="name">ERIC <span class="x">×</span> B166ER</div></div>
  <div class="chapter">认 知 拓 扑 <b>· 01</b></div>
 </div>
 <div class="kicker">SELF-EVOLUTION · 2026-11-17</div>
 <h1>写进记忆 <span class="hl">≠</span> 下次会生效</h1>
 <div class="lede">瓶颈不是存储结构，是<b>缺执行器</b>：记录了 <span class="g">@@CORRCHARS@@</span> 字符教训，行为层只有 <span class="g">@@MEMCHARS@@</span>。<br><b>断的那条边不是「信息存在哪」，是「产出到人眼前」。</b></div>
 <div class="chips">
  <div class="chip"><div class="k">受 损 文 件</div><div class="v"><em>91→88</em> <s>0</s>不可解码</div></div>
  <div class="chip"><div class="k">副 本 删 除</div><div class="v"><em>3</em> 份·849 KB</div></div>
  <div class="chip"><div class="k">孤儿规则补齐</div><div class="v"><em>64</em> 条并入正本</div></div>
  <div class="chip"><div class="k">断 言 状 态</div><div class="v"><em>12/12</em> PASS</div></div>
 </div>
 <div class="svgbox">
 <svg class="topo" viewBox="0 0 964 1240" xmlns="http://www.w3.org/2000/svg">
  <defs>
   <marker id="ag" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#D4A84F" opacity=".72"/></marker>
   <marker id="ar" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#C8102E" opacity=".85"/></marker>
   <linearGradient id="gex" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D4A84F" stop-opacity=".24"/><stop offset="1" stop-color="#D4A84F" stop-opacity=".05"/></linearGradient>
  </defs>
  <g stroke="#D4A84F" stroke-opacity=".42" stroke-width="1.7" fill="none" marker-end="url(#ag)">
   <path d="M300 92 C300 122 250 122 250 158"/>
   <path d="M664 92 C664 122 714 122 714 158"/>
   <path d="M440 208 L524 208"/>
   <path d="M944 208 C944 130 944 54 880 54 L726 54"/>
   <path d="M182 421 L26 421 L26 54 L218 54"/>
   <path d="M482 92 L482 356"/>
   <path d="M482 486 L482 562"/>
   <path d="M482 658 L482 732"/>
   <path d="M482 828 L482 906"/>
  </g>
  <path d="M782 760 C940 764 940 946 L678 946" stroke="#C8102E" stroke-opacity=".82" stroke-width="1.9" stroke-dasharray="6 5" fill="none" marker-end="url(#ar)"/>
  <text class="el" x="192" y="134" text-anchor="end">按上下文</text>
  <text class="el" x="772" y="134" text-anchor="start">按上下文</text>
  <text class="el elg" x="836" y="36" text-anchor="middle">3 次重复→升回 HOT</text>
  <text class="el elg" x="104" y="36" text-anchor="middle">★断言拦截→当场改</text>
  <text class="el" x="496" y="320">每次交付前必跑</text>
  <text class="el" x="496" y="530">产出 eval 记录</text>
  <text class="el" x="496" y="700">状态文件</text>
  <text class="el elg" x="496" y="872">主动推送（已闭合）</text>
  <text class="el elr" x="932" y="712" text-anchor="end">2026-09-22 → 2026-11-17</text>
  <text class="el elr" x="932" y="736" text-anchor="end">56 天空档 · 从不直达</text>
  <rect x="222" y="16" width="500" height="76" rx="12" fill="rgba(212,168,79,.10)" stroke="#D4A84F" stroke-opacity=".64)" stroke-width="1.5"/>
  <text class="tn" x="244" y="49">HOT · memory.md · @@MEMLINES@@ 行</text>
  <text class="tn2" x="244" y="75">常驻 · 行为层 · 只放今天仍成立的事实</text>
  <rect x="20" y="158" width="420" height="120" rx="12" fill="rgba(255,255,255,.03)" stroke="rgba(212,168,79,.34)" stroke-width="1.2"/>
  <text class="tn" x="42" y="191">WARM · 按需加载</text>
  <text class="tx" x="42" y="221">domains @@DOMAINS@@ · projects @@PROJECTS@@</text>
  <text class="tx" x="42" y="246">rules @@RULES@@ · 专题 @@TOPICS@@</text>
  <text class="tx" x="42" y="270">同一主题第 2 次出现即落此层</text>
  <rect x="524" y="158" width="420" height="120" rx="12" fill="rgba(255,255,255,.03)" stroke="rgba(212,168,79,.34)" stroke-width="1.2"/>
  <text class="tn" x="546" y="191">COLD · 显式查询</text>
  <text class="tx" x="546" y="221">archive @@ARCHIVE@@ · eval @@EVAL@@</text>
  <text class="tx" x="546" y="246">未用 30 天→降级 / 90 天→归档</text>
  <text class="tx" x="546" y="270" fill="#C8102E">★ 2026-09-26 曾静默缺席一个月</text>
  <rect x="182" y="356" width="600" height="130" rx="14" fill="url(#gex)" stroke="#D4A84F" stroke-opacity=".80)" stroke-width="2"/>
  <text class="tb" x="204" y="392">★ 执行器层 · 7 个</text>
  <text class="tx" x="204" y="422">selfcheck 12 断言 · skill_router · evolution_scan/watch</text>
  <text class="tx" x="204" y="448">fix_mixed_encoding · 不存内容，只执行断言</text>
  <text class="tx" x="204" y="474">交付前必跑；PASS 才算完成，FAIL 先修或写明豁免</text>
  <rect x="182" y="562" width="600" height="96" rx="12" fill="rgba(255,255,255,.03)" stroke="rgba(212,168,79,.36)" stroke-width="1.2"/>
  <text class="tn" x="204" y="594">产出链 · B166ER-自进化扫描</text>
  <text class="tx" x="204" y="621">每周一 09:00 · script 负载（不调模型）· delivery:none</text>
  <text class="tx" x="204" y="647">写 eval/YYYY-MM-DD.json ＋ .last_scan.json</text>
  <rect x="182" y="732" width="600" height="96" rx="12" fill="rgba(255,255,255,.03)" stroke="rgba(212,168,79,.36)" stroke-width="1.2"/>
  <text class="tn" x="204" y="764">告警链 · B166ER-自进化缺席告警</text>
  <text class="tx" x="204" y="791">每日 08:30 · trigger 零子进程 · agentTurn</text>
  <text class="tx" x="204" y="817">判据：缺席 &gt; 8 天＝漏跑；连续 2 次 red＝有问题没修</text>
  <rect x="272" y="906" width="400" height="82" rx="12" fill="rgba(226,75,60,.11)" stroke="#C8102E" stroke-opacity=".58)" stroke-width="1.4"/>
  <text class="tn" x="294" y="940">Eric 看得见</text>
  <text class="tn2" x="294" y="968">主动推送 · 缺席与失败都会被送到</text>
  <g>
   <text class="tb" x="40" y="1078">断链与闭合 · 时间轴</text>
   <line x1="46" y1="1132" x2="924" y2="1132" stroke="rgba(212,168,79,.30)" stroke-width="1.5"/>
   <circle cx="86" cy="1132" r="6.5" fill="#C8102E"/>
   <circle cx="352" cy="1132" r="6.5" fill="#C8102E"/>
   <circle cx="628" cy="1132" r="7.5" fill="#D4A84F"/>
   <circle cx="880" cy="1132" r="6.5" fill="#D4A84F"/>
   <text class="td" x="86" y="1112" text-anchor="middle">09-22</text>
   <text class="td" x="352" y="1112" text-anchor="middle">10-26</text>
   <text class="td" x="628" y="1112" text-anchor="middle">11-17</text>
   <text class="td" x="880" y="1112" text-anchor="middle">此后</text>
   <text class="tl" x="86" y="1164" text-anchor="middle">最后一次 eval</text>
   <text class="tl" x="352" y="1164" text-anchor="middle">才发现缺席一个月</text>
   <text class="tl" x="628" y="1164" text-anchor="middle">体检·两链建成</text>
   <text class="tl" x="880" y="1164" text-anchor="middle">每周扫描·每日探测</text>
   <text class="td" x="46" y="1212">此前只有「在场检测」：任务跑没跑、跑成没成 —— 没有「缺席检测」，所以它静默了一个月也没人知道</text>
  </g>
 </svg>
 </div>
 <div class="cards">
  <div class="card"><div class="h">记录 ≠ 改变</div>
   <p>纠错日志 <b>@@CORRCHARS@@</b> 字符 vs 行为层 <b>@@MEMCHARS@@</b> ＝ <b>@@RATIO@@ 倍</b>；94 个技能今日路由 <span class="r">0</span> 次。<br>不落成断言，等于没进化。</p></div>
  <div class="card"><div class="h">在场 ≠ 缺席</div>
   <p>只检测「执行时是否正常」，不检测「是否按时执行」。<br><span class="r">断的是「产出到人眼前」那条边</span> —— 跑完了，报告无处可送。</p></div>
  <div class="card"><div class="h">写 ≠ 被想起</div>
   <p>14 条自动化规则我 <b>10-24</b> 就写过，今天<span class="r">逐条重犯</span>。<br>根因不在记性 —— <b>它们不在会被看到的位置</b>。</p></div>
 </div>
 <div class="footer">
  <div class="credit">ERIC <span class="x">×</span> B166ER 共研出品</div>
  <div class="tag">信 息 拓 扑</div>
  <div class="circle">B</div>
 </div>
</div>
</body></html>
"""

def build(V, key):
    P = PAGES[key]
    PW, PH = P["page"]
    tpl = TPL
    for k, v in [("PW", PW), ("PH", PH), ("BOX", P["box"]), ("SCALE", P["scale"]),
                 ("H1", P["h1"]), ("LEDE", P["lede"]), ("CHIPV", P["chipv"]),
                 ("CARDH", P["cardh"]), ("CARDP", P["cardp"])]:
        tpl = tpl.replace("@@%s@@" % k, str(v))
    for k, v in V.items():
        tpl = tpl.replace("@@%s@@" % k, str(v))
    left = re.findall(r"@@[A-Z0-9_]+@@", tpl)
    if left:
        raise SystemExit("未替换占位符: %s" % left)
    return tpl

PROBE = """() => {
  const de=document.documentElement, bd=document.body;
  const R={};
  R.ovH=bd.scrollWidth-de.clientWidth; R.ovV=bd.scrollHeight-de.clientHeight;
  let wide=[]; document.querySelectorAll('*').forEach(e=>{const r=e.getBoundingClientRect();
    if(r.width>0&&(r.left<-1||r.right>de.clientWidth+1)) wide.push((e.className||e.tagName));});
  R.wideN=wide.length; R.wide=wide.slice(0,4);
  let clip=[]; document.querySelectorAll('.card,.chip,.lede').forEach(e=>{
    if(e.scrollHeight-e.clientHeight>3) clip.push((e.className)+':'+(e.textContent||'').slice(0,16));});
  R.clipN=clip.length; R.clip=clip.slice(0,4);
  const ts=[...document.querySelectorAll('svg.topo text')].map(t=>{const r=t.getBoundingClientRect();
    return {x:r.x,y:r.y,w:r.width,h:r.height,t:(t.textContent||'').trim().slice(0,20)};});
  R.nText=ts.length;
  const ov=[]; for(let i=0;i<ts.length;i++)for(let j=i+1;j<ts.length;j++){const a=ts[i],c=ts[j];
    const ix=Math.min(a.x+a.w,c.x+c.w)-Math.max(a.x,c.x), iy=Math.min(a.y+a.h,c.y+c.h)-Math.max(a.y,c.y);
    if(ix>3&&iy>3) ov.push(a.t+' x '+c.t);}
  R.ovN=ov.length; R.ov=ov.slice(0,6);
  const svg=document.querySelector('svg.topo').getBoundingClientRect();
  R.outN=ts.filter(t=>t.x<svg.x-2||t.x+t.w>svg.right+2||t.y<svg.y-2||t.y+t.h>svg.bottom+2).map(t=>t.t).length;
  R.out=ts.filter(t=>t.x<svg.x-2||t.x+t.w>svg.right+2||t.y<svg.y-2||t.y+t.h>svg.bottom+2).map(t=>t.t).slice(0,4);
  // ★ 压曲线检测：不能用 getBBox()(用户单位) 比 getBoundingClientRect()(CSS像素) —— 不同坐标系必误报。
  //   正解：沿路径按长度采样点，把用户坐标换算到客户端坐标，再判是否落在文字盒内。
  const svgEl=document.querySelector('svg.topo');
  const sr=svgEl.getBoundingClientRect();
  const VBW=964, VBH=1240;
  const toClient=(p)=>({x: sr.left + (p.x/VBW)*sr.width, y: sr.top + (p.y/VBH)*sr.height});
  const hp=[];
  for(const path of svgEl.querySelectorAll('path')){
    let len=0; try{len=path.getTotalLength();}catch(e){continue;}
    if(!len) continue;
    const N=160;
    for(let i=0;i<=N;i++){
      let pt; try{pt=path.getPointAtLength(len*i/N);}catch(e){continue;}
      const c=toClient(pt);
      for(const t of ts){
        if(c.x>t.x-2&&c.x<t.x+t.w+2&&c.y>t.y-2&&c.y<t.y+t.h+2){
          if(hp.indexOf(t.t)<0) hp.push(t.t);
          break;
        }
      }
    }
  }
  R.hitPathN=hp.length; R.hitPath=hp.slice(0,6);
  const main=[...document.querySelectorAll('.kicker,h1,.lede,.chips,.svgbox,.cards,.footer')].map(e=>{const r=e.getBoundingClientRect();
    return (e.className||e.tagName).toString().slice(0,9)+':'+Math.round(r.top)+'-'+Math.round(r.bottom);});
  R.main=main;
  let maxGap=0, gp='';
  const boxes=[...document.querySelectorAll('.kicker,h1,.lede,.chips,.svgbox,.cards,.footer')].map(e=>e.getBoundingClientRect()).sort((a,b)=>a.top-b.top);
  for(let i=1;i<boxes.length;i++){const g=boxes[i].top-boxes[i-1].bottom; if(g>maxGap){maxGap=g; gp=(boxes[i-1].className||'')+' -> '+(boxes[i].className||'');}}
  R.maxGap=Math.round(maxGap); R.gapAt=gp;
  return R;
}"""

def qa(html_path, W, H, out_png, tag):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=["--disable-gpu", "--font-render-hinting=none"])
        ctx = b.new_context(viewport={"width": W, "height": H}, device_scale_factor=2)
        pg = ctx.new_page(); pg.goto("file:///" + html_path.replace("\\", "/"), wait_until="networkidle"); pg.wait_for_timeout(900)
        pr = pg.evaluate(PROBE)
        pg.screenshot(path=out_png, clip={"x": 0, "y": 0, "width": W, "height": H})
        b.close()
    hard = (pr["ovH"] == 0 and pr["ovV"] == 0 and pr["wideN"] == 0 and pr["clipN"] == 0
            and pr["ovN"] == 0 and pr["outN"] == 0 and pr["hitPathN"] == 0)
    print("=== QA %s ===" % tag)
    print("  L1 盒模型: 溢出 h=%s v=%s ｜ 越界 %d ｜ 裁切 %d" % (pr["ovH"], pr["ovV"], pr["wideN"], pr["clipN"]))
    for c in pr["clip"]: print("      裁切", c)
    print("  L2 SVG元素级: 文本 %d ｜ ★重叠 %d ｜ ★越出 %d ｜ ★压曲线 %d ｜ 最大死白 %dpx" % (
        pr["nText"], pr["ovN"], pr["outN"], pr["hitPathN"], pr["maxGap"]))
    for o in pr["ov"]: print("      重叠:", o)
    for o in pr["out"]: print("      越出:", o)
    for o in pr["hitPath"]: print("      压曲线:", o)
    print("  版块:", " | ".join(pr["main"]))
    print("  → %s" % ("✅ 硬质检通过（L3 视觉核验待人工）" if hard else "★ 未通过"))
    return hard

if __name__ == "__main__":
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]
    V = load_vals()
    res = {}
    for key in ["9x16", "3x4"]:
        if only and key != only: continue
        P = PAGES[key]
        W, H = P["page"]
        hp = os.path.join(OUT, "self_evolution_topology_%s.html" % key)
        pp = os.path.join(OUT, "self_evolution_topology_%s.png" % key)
        with open(hp, "w", encoding="utf-8", newline="\n") as f:
            f.write(build(V, key))
        ok = qa(hp, W, H, pp, key)
        res[key] = ok
        print("  HTML %d B ｜ PNG %d B" % (os.path.getsize(hp), os.path.getsize(pp)))
        print()
    print("汇总:", json.dumps(res, ensure_ascii=False))
