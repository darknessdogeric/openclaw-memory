# -*- coding: utf-8 -*-
"""make_source_matrix.py - B166ER 全部信源矩阵信息图生成器

用法:
    python toolbox/make_source_matrix.py              # 出两版 + 三层质检
    python toolbox/make_source_matrix.py --only 9x16

设计纪律:
  1) 模板零 % 格式化（CSS 含大量字面 %）—— 用 @@TOKEN@@ + .replace()
  2) 两版共用同一份数据与同一套 CSS 变量，3:4 只改版式开关
  3) 三层质检: L1 盒模型 / L2 元素级(重叠·越界·裁切·横向溢出·死白) / L3 视觉核验
  4) 文字直接写中文，不手写 HTML 实体码（手写实体码会把"国庆"写成"国带"）

★ 数据全部来自官方排查总表原文，不自算比率（自算会踩口径陷阱）
"""
import io, sys, os, re, json

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
import sm_parse as SP
import sm_srcrows as SR

RES_CLS = {"取得": "sg", "仅摘要": "sy", "未取得": "sr", "付费终端": "sp",
            "反爬硬挡": "sk", "主体存疑": "sgray"}

OUT = os.path.join(ROOT, "output", "info_source_matrix")
DATA = os.path.join(ROOT, "skills", "source-matrix-infographic", "data")
TPL = os.path.join(DATA, "tpl.html")
CSSF = os.path.join(DATA, "tpl.css")
os.makedirs(OUT, exist_ok=True)

PAGES = {"9x16": (1080, 1920), "3x4": (1080, 1440)}
DOTS = {"U0001F7E2U0001F7E2": "#2E7D5B", "U0001F7E1U0001F7E1": "#C08A1E",
        "U0001F7E0U0001F7E0": "#D07A3A", "U0001F534U0001F534": "#B04A42"}

# 自适应缩放：内容超高时整体缩到刚好装进目标框，并暴露 scale 供闸门检查
FITJS = """<script>
(function(){
  var fit=document.querySelector('.fit'), pg=document.querySelector('.page');
  var target=parseInt(fit.getAttribute('data-h'),10)||1920;
  var natural=pg.getBoundingClientRect().height;
  var s=Math.min(1, target/natural);
  pg.style.transform='scale('+s+')';
  fit.style.height=target+'px';
  window.__scale=s; window.__natural=Math.round(natural); window.__target=target;
})();
</script>"""

PROBE = r"""() => {
  const de=document.documentElement, bd=document.body, R={};
  R.scale=window.__scale||1; R.natural=window.__natural||0; R.target=window.__target||0;
  R.ovH=bd.scrollWidth-de.clientWidth; R.ovV=bd.scrollHeight-de.clientHeight;
  let wide=[]; document.querySelectorAll('.page *').forEach(e=>{const r=e.getBoundingClientRect();
    if(r.width>0&&(r.left<-1||r.right>de.clientWidth+1)) wide.push((e.className||e.tagName).toString().slice(0,14));});
  R.wideN=wide.length; R.wide=wide.slice(0,5);
  let clip=[]; document.querySelectorAll('.card,.note-box,.stack,.tdef').forEach(e=>{
    if(e.scrollHeight-e.clientHeight>3) clip.push((e.className||'')+':'+(e.textContent||'').slice(0,18));});
  R.clipN=clip.length; R.clip=clip.slice(0,5);
  let ow=[]; document.querySelectorAll('.page *').forEach(e=>{
    if(e.scrollWidth-e.clientWidth>3) ow.push((e.className||e.tagName).toString().slice(0,14)+':'+e.textContent.trim().slice(0,12));});
  R.owN=ow.length; R.ow=ow.slice(0,5);
  // ★ 逐行矩形：用 Range.getClientRects()，避免内联元素跨行时并集矩形造成假重叠
  const rng=document.createRange();
  const items=[];
  const walk=document.createTreeWalker(document.querySelector('.page'),NodeFilter.SHOW_TEXT);
  let n;
  while((n=walk.nextNode())){
    if(!n.nodeValue.trim()) continue;
    const el=n.parentElement; if(!el) continue;
    let rects=[];
    try{rng.selectNodeContents(n); rects=[...rng.getClientRects()];}catch(e){continue;}
    for(const r of rects){ if(r.width<1||r.height<1) continue;
      items.push({el:el,x:r.x,y:r.y,w:r.width,h:r.height,
        t:n.nodeValue.trim().slice(0,14),c:(el.className||el.tagName).toString().slice(0,12)}); }
  }
  const ov=[];
  for(let i=0;i<items.length;i++)for(let j=i+1;j<items.length;j++){
    const a=items[i],b=items[j];
    if(a.el===b.el) continue;
    const ix=Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x), iy=Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y);
    if(ix>2&&iy>2) ov.push(a.t+' x '+b.t+' ['+a.c+'/'+b.c+']');}
  R.ovN=ov.length; R.ov=ov.slice(0,8); R.nText=items.length;
  const fb=document.querySelector('.fit').getBoundingClientRect();
  R.outN=items.filter(t=>t.x<fb.x-2||t.x+t.w>fb.right+2||t.y<fb.y-2||t.y+t.h>fb.bottom+2).length;
  R.out=items.filter(t=>t.x<fb.x-2||t.x+t.w>fb.right+2||t.y<fb.y-2||t.y+t.h>fb.bottom+2).map(t=>t.t).slice(0,5);
  const boxes=[...document.querySelectorAll('.rule,h1,.lede,.sec,.rounds,.grid,.note-box,.foot,.kicker')].map(e=>({c:e.className,r:e.getBoundingClientRect()})).sort((a,b)=>a.r.top-b.r.top);
  let mg=0,ga=''; for(let i=1;i<boxes.length;i++){const g=boxes[i].r.top-boxes[i-1].r.bottom;
    if(g>mg){mg=g;ga=boxes[i-1].c+' -> '+boxes[i].c;}}
  R.maxGap=Math.round(mg); R.gapAt=ga;
  R.secs=[];
  document.querySelectorAll('.page > *').forEach(e=>{const r=e.getBoundingClientRect();
    R.secs.push((e.className||e.tagName).toString().slice(0,8)+':'+Math.round(r.height));});
  return R;
}"""


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(D, key):
    ajn = {c["code"]: c["n"] for c in D["h79_cats"]}
    rows79 = SR.parse_src_rows(SP.rd(SP.F_H79))
    pc79 = SR.per_class_rate(rows79)

    def card(c, extra="", gold=False):
        lst = rows79.get(c["code"], [])
        lines = ""
        for r in SR.picks(lst, 2):
            lines += ("<em class='" + RES_CLS.get(r["res"], "sgray") + "'>●</em>"
                      + esc(r["name"]) + "<br>")
        return ("<div class='card" + (" klm" if gold else "") + "'><span class='badge'>" + esc(c["code"]) + "</span>"
                "<div class='cname'>" + esc(c["name"]) + "</div>"
                "<div class='cspec'>" + esc(c["spec"]) + extra + "</div>"
                "<div class='clist'>" + lines + "</div></div>")

    def stack(seg, title, sub):
        tot = sum(s["n"] for s in seg) or 1
        h = ""
        for s in seg:
            w = s["n"] * 100.0 / tot
            h += ("<div style='width:%.4f%%;background:%s'>%s</div>"
                  % (w, s["color"], (str(s["n"]) if w > 9 else "")))
        lg = ""
        for s in seg:
            lg += ("<span class='lg'><s style='background:%s'></s><b>%s</b> %d | %d%%</span>"
                   % (s["color"], esc(s["name"]), s["n"], s["pct"]))
        return ("<div class='rlabel'>" + title + "<small>" + sub + "</small></div>"
                "<div class='stack'>" + h + "</div><div class='legend'>" + lg + "</div>")

    tiers = ""
    for r in D["conf"]:
        d = DOTS.get(r[0][:4], "#9AA0A6")
        tiers += ("<div class='tier'><span class='dot' style='background:%s'></span>"
                  "<div class='tname'>" + esc(r[1]) + "<small>" + esc(r[0]) + "</small></div>"
                  "<div class='tdef'>" + esc(r[2]) + "<br><em>门控：</em>" + esc(r[3]) + "</div></div>")
    sop = ""
    for r in D["sop"]:
        sop += ("<div class='tier'><span class='dot' style='background:#8A6BB1'></span>"
                "<div class='tname'>" + esc(r[0]) + "<small>" + esc(r[1]) + "</small></div>"
                "<div class='tdef'>" + esc(r[2]) + "</div></div>")
    gap = ""
    for r in D["gap"]:
        if len(r) >= 4:
            gap += ("<li><b>" + esc(r[0]) + "</b> ｜ " + esc(r[1]) + " ｜ " + esc(r[2]) + " ｜ " + esc(r[3]) + "</li>")
    cname = {}
    for c in D["cats_aj"] + D["cats_klm"] + D.get("cats_n", []):
        cname[c["code"]] = c["name"]
    hit = ""
    for code in sorted(pc79):
        p = pc79[code]
        hit += ("<div class='hit'><b>" + esc(code) + "</b><span class='k'>" + esc(cname.get(code, "")) +
                "</span><span class='bar'><i style='width:%d%%'></i></span>"
                "<span class='v'>取得 %d/%d</span></div>" % (p["rate"], p["hit"], p["total"]))
    ajhtml = "".join(card(c, ("　·　%d 源" % ajn[c["code"]] if c["code"] in ajn else ""))
                     for c in D["cats_aj"])
    klmhtml = "".join(card(c, "", True) for c in D["cats_klm"])
    nhtml = "".join(card(c, "", True) for c in D.get("cats_n", []))
    h79 = SP.bars(D["h79"])
    gq = SP.bars(D["gq"])

    _nsrc = 0
    for _c in D.get("cats_n", []):
        _m = re.search(r"(\d+)\s*源", _c.get("spec", ""))
        if _m:
            _nsrc += int(_m.group(1))
    head = ("14 类 · 79 ＋ %d 源" % _nsrc) if _nsrc else "13 类 × 79 源"
    lede = ("这不是信源清单，是<b>「这些类真能拿到什么」的账</b>。"
            "同一份 79 源名单，<b>国庆轮</b>与<b>Q3/Q4 轮</b>各打一遍："
            "<b>上市集团 9/10、新增的 K/L/M 三类各 5/6 最易穿透</b>；"
            "<b>本土数据 0/3、审计银行 0/8 完全打不动</b>。"
            "四条取数规则保证拿不到时明说「推算」。<br>"
            "<b>新增 N 类｜奢华 · 顶奢 · 奢华精品（6 子域 · %d 源）</b> —— 它与五星级/商务的口径完全不同，"
            "混着取数必然出错，故单列。" % _nsrc)
    html = open(TPL, encoding="utf-8").read()
    css = open(CSSF, encoding="utf-8").read()
    W, H = PAGES[key]
    repl = {
        "@@CSS@@": css,
        "@@FIT@@": "<div class='fit' data-h='%d'>" % H,
        "@@CLS@@": "p9" if key == "9x16" else "p3",
        "@@HEADLINE@@": head,
        "@@LEDE@@": lede,
        "@@AJ@@": ajhtml,
        "@@KLM@@": klmhtml,
        "@@N@@": nhtml,
        "@@TIERS@@": tiers,
        "@@SOP@@": sop,
        "@@H79@@": stack(h79, "2026-11-10 Q3/Q4 月度轮",
                        "共 79 源 · 2026 Q3 财报、Q3/Q4 景气与经营报告、10 月报告"),
        "@@GQ@@": stack(gq, "2026-10-11 国庆专项轮",
                       "共 79 源 · 2026 国庆公开报告与数据"),
        "@@HIT@@": hit,
        "@@GAP@@": gap,
        "@@JS@@": FITJS,
    }
    for k, v in repl.items():
        html = html.replace(k, v)
    return html


def qa(html_path, W, H, out_png, tag):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=["--disable-gpu", "--font-render-hinting=none"])
        ctx = b.new_context(viewport={"width": W, "height": H}, device_scale_factor=2)
        pg = ctx.new_page()
        pg.goto("file:///" + html_path.replace("\\", "/"), wait_until="networkidle")
        pg.wait_for_timeout(700)
        pr = pg.evaluate(PROBE)
        pg.screenshot(path=out_png, clip={"x": 0, "y": 0, "width": W, "height": H})
        b.close()
    scale_ok = pr["scale"] >= 0.82
    content_ok = pr["nText"] >= 120
    size_ok = True
    try:
        from PIL import Image
        with Image.open(out_png) as im:
            size_ok = (im.width == W * 2 and im.height == H * 2)
    except Exception:
        pass
    hard = (pr["ovH"] == 0 and pr["ovV"] == 0 and pr["wideN"] == 0 and pr["clipN"] == 0
            and pr["ovN"] == 0 and pr["outN"] == 0 and pr["owN"] == 0 and scale_ok
            and content_ok and size_ok)
    print("  内容闸门: 文本 %d(需>=120) %s ｜ 尺寸 2x=%dx%d %s"
          % (pr["nText"], "OK" if content_ok else "★空图", W * 2, H * 2, "OK" if size_ok else "★尺寸不符"))
    print("=== QA %s ===" % tag)
    print("  缩放: 内容自然高 %d → 目标 %d ｜ scale=%.3f %s"
          % (pr["natural"], pr["target"], pr["scale"], "" if scale_ok else "★过小(<0.82,不可读)"))
    print("  L1 盒模型: 溢出 h=%s v=%s | 越界 %d | 裁切 %d | 文本横向溢出 %d"
          % (pr["ovH"], pr["ovV"], pr["wideN"], pr["clipN"], pr["owN"]))
    for c in pr["clip"]:
        print("      裁切:", c)
    for o in pr["ow"]:
        print("      溢出:", o)
    print("  L2 元素级: 文本 %d | ★重叠 %d | ★越出 %d | 最大死白 %dpx"
          % (pr["nText"], pr["ovN"], pr["outN"], pr["maxGap"]))
    for o in pr["ov"]:
        print("      重叠:", o)
    for o in pr["out"]:
        print("      越出:", o)
    print("  死白最大间隙:", pr["maxGap"], "px @", pr["gapAt"])
    print("  区块高:", " ".join(pr.get("secs", [])))
    print("  -> %s" % ("✅ 硬质检通过（L3 视觉核验待人工）" if hard else "★ 未通过"))
    return hard


if __name__ == "__main__":
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]
    D = SP.load()
    print("载入: A-J %d 类 | KLM %d 类 | N %d 类 | 79轮统计 %d | 国庆统计 %d | 逐类命中 %d | 缺口 %d"
          % (len(D["cats_aj"]), len(D["cats_klm"]), len(D.get("cats_n", [])),
             len(D["h79"]), len(D["gq"]), len(D["gq_cats"]), len(D["gap"])))
    # ★ 数据闸门：空内容也���全过质检（无重叠无越界）—— 必须先验内容非空，否则是绿灯假象
    if (len(D["cats_aj"]) < 10 or len(D["cats_klm"]) < 3 or len(D["h79"]) < 5
            or len(D["gq_cats"]) < 10 or len(D.get("cats_n", [])) < 1):
        print("★ 数据不足（源文件缺失或解析失败），拒绝出图：%s" %
              {k: len(D[k]) for k in ("cats_aj", "cats_klm", "h79", "gq", "gq_cats", "gap")})
        raise SystemExit(2)
    res = {}
    for key in ["9x16", "3x4"]:
        if only and key != only:
            continue
        W, H = PAGES[key]
        hp = os.path.join(OUT, "source_matrix_%s.html" % key)
        pp = os.path.join(OUT, "source_matrix_%s.png" % key)
        open(hp, "w", encoding="utf-8", newline="\n").write(build(D, key))
        ok = qa(hp, W, H, pp, key)
        res[key] = ok
        print("  HTML %d B | PNG %d B" % (os.path.getsize(hp), os.path.getsize(pp)))
        print()
    print("汇总:", json.dumps(res, ensure_ascii=False))
