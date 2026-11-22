# -*- coding: utf-8 -*-
"""1) 生成器加标签配平修复  2) 渲染器加结构与填充校验（只在 .main 内比对，排除跨容器假阳性）"""
import io, os, re, sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

MK = r'D:\B166ER-openclaw\workspace\toolbox\_mk_xhs9_light.py'
RD = r'D:\B166ER-openclaw\workspace\toolbox\_render_xhs9.py'

# ---------------- 1) 生成器：配平修复 ----------------
t = open(MK, encoding='utf-8').read()

FIX = '''
def balance(html):
    """修 div 标签配平：多余 </div> 删除，缺失 </div> 补齐。返回 (修复后, 说明)"""
    toks = list(re.finditer(r'<div\\b[^>]*>|</div>', html))
    stack = []
    out = []
    last = 0
    extra = []
    for m in toks:
        if m.group(0) != '</div>':
            stack.append(m.start())
        else:
            if stack:
                stack.pop()
            else:
                extra.append(m.start())
    fixed = html
    for s in sorted(extra, reverse=True):
        fixed = fixed[:s] + fixed[s + 6:]
    add = ""
    if stack:
        add = "</div>" * len(stack)
    fixed = fixed + add
    note = ("删多余</div>%d 补缺失</div>%d" % (len(extra), len(stack)))
    return fixed, note


for _k in list(P.keys()):
    _fixed, _note = balance(P[_k])
    if _note != "删多余</div>0 补缺失</div>0":
        P[_k] = _fixed
        print("  配平修复 " + _k + ": " + _note)

'''

ANCH = "for k, v in P.items():\n    open(os.path.join(HTMLD, k + \".html\")"
if ANCH in t:
    if "def balance(html)" not in t:
        t = t.replace(ANCH, FIX + ANCH, 1)
        open(MK, 'w', encoding='utf-8').write(t)
        print('生成器：已加配平修复')
    else:
        print('生成器：配平修复已存在')
else:
    print('!! 生成器锚点未命中')

# ---------------- 2) 渲染器：结构校验 + 仅 .main 内比对 ----------------
r = open(RD, encoding='utf-8').read()

OLD_PROBE_TAIL = """  let ov=0,out=0,wide=0,maxR=-1e9,maxB=-1e9;"""
NEW_PROBE_TAIL = """  const mainEl=document.querySelector('.main');
  const scope=[...mainEl.querySelectorAll('*')].filter(e=>{
    const t=(e.textContent||'').trim(); return t.length>0 && e.children.length===0;});
  let ov=0,out=0,wide=0,maxR=-1e9,maxB=-1e9;"""
if OLD_PROBE_TAIL in r:
    r = r.replace(OLD_PROBE_TAIL, NEW_PROBE_TAIL, 1)
    r = r.replace("  const ps=[...document.querySelectorAll('.poster *')].filter(e=>{",
                  "  const ps=[...document.querySelectorAll('.main *')].filter(e=>{", 1)
    OLD_RET = """  const bs=document.querySelectorAll('.bbig,.bsm').length;"""
    NEW_RET = """  const posterKids=document.querySelector('.poster').children.length;
  const mainH=Math.round(document.querySelector('.main').getBoundingClientRect().height);
  const bs=document.querySelectorAll('.bbig,.bsm').length;"""
    r = r.replace(OLD_RET, NEW_RET, 1)
    r = r.replace("return {n:R.length, ov:ov, out:out, wide:wide, maxR:Math.round(maxR), maxB:Math.round(maxB), bs:bs, bt:bt, fill:fill};",
                  "return {n:R.length, ov:ov, out:out, wide:wide, maxR:Math.round(maxR), maxB:Math.round(maxB), bs:bs, bt:bt, fill:fill, kids:posterKids, mainH:mainH};", 1)
    OLD_GOOD = """                and pr["maxB"] <= 1441 and pr["maxR"] <= 1081 and pr["fill"] >= 88)"""
    NEW_GOOD = """                and pr["maxB"] <= 1441 and pr["maxR"] <= 1081 and pr["fill"] >= 88
                and pr["kids"] == 3 and pr["mainH"] == 1240)"""
    r = r.replace(OLD_GOOD, NEW_GOOD, 1)
    OLD_PR = """              + " B标" + str(pr["bs"]) + " 填充" + str(pr["fill"]) + "% 底" + str(pr["maxB"]))"""
    NEW_PR = """              + " B标" + str(pr["bs"]) + " 填充" + str(pr["fill"]) + "% 底" + str(pr["maxB"])
              + " poster子项" + str(pr["kids"]) + " mainH" + str(pr["mainH"]))"""
    r = r.replace(OLD_PR, NEW_PR, 1)
    open(RD, 'w', encoding='utf-8').write(r)
    print('渲染器：已加结构校验（poster子项=3 / mainH=1240）+ 仅 .main 内比对')
else:
    print('!! 渲染器探针锚点未命中')
