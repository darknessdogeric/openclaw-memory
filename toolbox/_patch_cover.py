# -*- coding: utf-8 -*-
"""新增标题封面 p00_title，并重排 P01–P10 序号"""
import io, os, re, sys, subprocess
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

MK = r'D:\B166ER-openclaw\workspace\toolbox\_mk_xhs9_v3.py'
t = open(MK, encoding='utf-8').read()

TITLE_P = '''P['p00_title'] = page("P01 · 标题封面", (
    "<div class='kicker'>集团酒店经营预算 · 空白模板 V1.0</div>"
    "<h1 style='font-size:84px;line-height:1.18;margin-top:18px'>酒店经营<br>预算模板<br><em>空白模板 v1.0</em></h1>"
    "<p class='lede' style='font-size:19px;max-width:900px'>把集团酒店经营预算，从<b>带着一家酒店历史数据的旧表</b>，"
    "改成<b>任何一家店都能重算的空白模型</b>。<br>公式链、行号索引、批注与跨表引用关系全部保留，硬编码经营数据全部清空。</p>"
    + "<div class='sec'><h2>四个数字<span class='note'>这套模板的全部家当</span></h2>"
    + kpis([("71", "张工作表"), ("18,618", "条计算公式，一条未删"), ("4", "层数据流向"), ("0", "处残留历史数据")])
    + "</div>"
    + "<div class='sec'><h2>一张图看懂怎么跑<span class='note'>填数只在前三层发生</span></h2>"
    + "<div style='display:grid;grid-template-columns:repeat(4,1fr);gap:8px'>"
    + blk(RED, "输入层", "7 张 · 唯一手填源头")
    + blk(ORG, "部门层", "45 张 · 收入成本人工")
    + blk(GRN, "分摊层", "8 张 · 基数与人数")
    + blk(YEL, "汇总层", "8＋3 张 · 全自动", dark=True)
    + "</div>"
    + "<div style='display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:6px'>"
    + "<div style='font-size:12.5px;color:#7A7A7A;text-align:center'>细分市场与餐饮收入</div>"
    + "<div style='font-size:12.5px;color:#7A7A7A;text-align:center'>房务·餐饮·宴会·销售等</div>"
    + "<div style='font-size:12.5px;color:#7A7A7A;text-align:center'>餐饮间接费·人工·洗衣</div>"
    + "<div style='font-size:12.5px;color:#7A7A7A;text-align:center'>三表·快报·关键指标</div>"
    + "</div>"
    + legend([(RED, "输入层"), (ORG, "部门层"), (GRN, "分摊层"), (YEL, "汇总层")])
    + "</div>"
    + note("<b>汇总层一个数都不许手改。</b>改最底层一次，全表联动重算 —— 这就是它和旧模板的全部差别。")
    + "<div class='cta'><div class='big'>九张图讲完<br>一台空白的预算引擎</div>"
    "<div class='sm'><div class='l'>GET</div><div class='v'>评论区扣 1</div></div></div>"
))

'''

ANCH = "P['p01_cover'] = page("
if "P['p00_title']" not in t:
    if ANCH in t:
        t = t.replace(ANCH, TITLE_P + ANCH, 1)
        print('标题封面已插入')
    else:
        print('!! 插入锚点未命中'); sys.exit(1)

# ---- 序号重排 ----
RENUM = '''
_REN = [('p00_title', 'P01 · 标题封面'), ('p01_cover', 'P02 · 信息拓扑总览'),
        ('p02_painpoints', 'P03 · 痛点'), ('p03_topo', 'P04 · 信息拓扑图'),
        ('p04_value', 'P05 · 价值'), ('p05_audience', 'P06 · 给谁用'),
        ('p06_quotes', 'P07 · 关键洞察'), ('p07_delivery', 'P08 · 交付物'),
        ('p08_action', 'P09 · 行动'), ('p09_summary', 'P10 · 全景')]
for _k, _m in _REN:
    if _k in P:
        P[_k] = re.sub(r'<div class=.meta.>[^<]*</div>',
                       "<div class='meta'>" + _m + "</div>", P[_k], count=1)

'''
ANCH2 = "BAD = [\"微信\""
if "_REN = [" not in t:
    if ANCH2 in t:
        t = t.replace(ANCH2, RENUM + ANCH2, 1)
        print('序号重排已加')
    else:
        print('!! 重排锚点未命中'); sys.exit(1)

open(MK, 'w', encoding='utf-8').write(t)
print('写入完成')

r = subprocess.run([sys.executable, MK], capture_output=True, text=True, encoding='utf-8', errors='replace')
print(r.stdout[-600:])
if r.stderr:
    print('STDERR:', r.stderr[-400:])
RD = r'D:\B166ER-openclaw\workspace\toolbox\_render_xhs9.py'
r2 = subprocess.run([sys.executable, RD], capture_output=True, text=True, encoding='utf-8', errors='replace')
print(r2.stdout)
if r2.stderr:
    print('STDERR:', r2.stderr[-400:])
