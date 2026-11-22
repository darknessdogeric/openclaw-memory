# -*- coding: utf-8 -*-
"""小红书 9 图 v2 · 酒店经营预算模板（空白模板）产品介绍
范式：浅色信息拓扑图（参照 Eric 留存参考 业务拓扑图 v1.3）
配色：白底 + 砖红 CA1D39 / 橙 E1820D / 黄 FFD90D / 绿 277549 / 蓝 257DD4 / 灰 A3A3A3
结构：每张均以「层级色条 + 色块 + 流向箭头 + 图例」组织；P03 为完整数据流向拓扑（主视觉）
B 标：R30 左上大 B + 右下小 B，写法 ERIC & B166ER
"""
import io, os, re, sys

OUT = r'C:\Users\ericz\Desktop\产业发展部\外部相关资料\全面预算管理\小红书9图_预算模板'
HTMLD = os.path.join(OUT, "html")
os.makedirs(HTMLD, exist_ok=True)

RED, ORG, YEL, GRN, BLU, GRY = "#CA1D39", "#E1820D", "#FFD90D", "#277549", "#257DD4", "#A3A3A3"
RED_L, YEL_L, GRN_L, BLU_L = "#F6DBDF", "#FBF3D6", "#DDE9E2", "#DEEAF7"

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1440px}
body{background:#FFFFFF;color:#1A1A1A;font-family:"Microsoft YaHei","PingFang SC","Noto Sans CJK SC",sans-serif;-webkit-font-smoothing:antialiased}
.poster{width:1080px;height:1440px;position:relative;overflow:hidden;display:grid;grid-template-rows:112px 1fr 88px;background:#FCFBF9}
.top{padding:22px 44px 0;display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #1A1A1A;margin:0 44px}
.brand{display:flex;align-items:center;gap:11px}
.bbig{width:56px;height:56px;border-radius:50%;background:#CA1D39;color:#fff;font-size:27px;font-weight:900;display:flex;align-items:center;justify-content:center}
.btxt{font-size:18px;font-weight:900;letter-spacing:.05em;color:#1A1A1A}
.meta{font-size:12.5px;font-weight:800;letter-spacing:.16em;color:#7A7A7A}
.main{padding:20px 44px 14px;display:flex;flex-direction:column;min-height:0}
.kicker{display:inline-flex;align-items:center;gap:8px;font-size:15px;font-weight:900;letter-spacing:.14em;color:#CA1D39}
.kicker::before{content:"";width:8px;height:8px;background:#CA1D39;border-radius:50%}
h1{font-size:52px;line-height:1.34;font-weight:900;letter-spacing:-.01em;margin:10px 0 0;color:#111}
h1 em{font-style:normal;color:#CA1D39}
h1 .w{color:#8A8A8A}
.lede{font-size:16.5px;line-height:1.62;color:#5C5C5C;margin:10px 0 0}
.lede b{color:#1A1A1A}
h2{font-size:23px;line-height:1.3;font-weight:900;margin:0;display:flex;align-items:center;gap:9px;color:#1A1A1A}
h2::before{content:"";width:7px;height:23px;background:#CA1D39;border-radius:2px}
h2 .note{margin-left:auto;font-size:12.5px;color:#7A7A7A;font-weight:600}
.sec{margin-top:16px;min-height:0}
/* ===== 拓扑组件 ===== */
.tl{display:grid;grid-template-columns:62px 1fr;align-items:stretch}
.tlb{writing-mode:vertical-rl;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;
 font-size:13px;font-weight:900;letter-spacing:.08em;color:#fff;padding:8px 3px;border-radius:5px 0 0 5px}
.tlb .en{font-size:10px;font-weight:700;opacity:.9;letter-spacing:.12em;margin-top:6px}
.tln{border:1px solid #E3E3E3;border-left:none;border-radius:0 5px 5px 0;background:#fff;padding:10px 12px;display:flex;flex-direction:column;gap:7px}
.tlrow{display:grid;gap:8px}
.blk{border-radius:5px;padding:9px 12px;color:#fff;min-width:0}
.blk .t{font-size:15px;font-weight:800;line-height:1.26}
.blk .d{font-size:12px;line-height:1.4;opacity:.94;margin-top:3px}
.blk .d b{font-weight:800}
.blk.dark{color:#1A1A1A}
.blk.out{border:1px solid #E3E3E3;color:#3A3A3A;background:#fff}
.blk.out .t{color:#1A1A1A}
.tarrow{height:15px;position:relative}
.tarrow::before{content:"";position:absolute;left:66px;top:0;width:2px;height:10px;background:#C9C9C9}
.tarrow::after{content:"";position:absolute;left:62px;top:9px;border-left:5px solid transparent;border-right:5px solid transparent;border-top:7px solid #C9C9C9}
.tnote{background:#FAEBD9;border:1px solid #E8C88C;border-radius:5px;padding:9px 11px;font-size:11.5px;line-height:1.5;color:#6B5320}
.tnote b{color:#8A3B1E}
.legend{display:flex;flex-wrap:wrap;gap:10px 14px;margin-top:9px;align-items:center}
.legend span{font-size:12px;color:#5C5C5C;display:flex;align-items:center;gap:5px}
.legend i{width:12px;height:12px;border-radius:3px;display:inline-block}
.kpi{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin-top:12px}
.kpi div{border:1px solid #E3E3E3;border-radius:6px;padding:10px 12px;background:#fff}
.kpi b{display:block;font-size:29px;font-weight:900;color:#CA1D39;line-height:1.1}
.kpi span{display:block;font-size:12.5px;color:#6B6B6B;margin-top:5px;line-height:1.35}
.chain{display:grid;grid-template-columns:1fr 26px 1fr 26px 1fr 26px 1fr;align-items:stretch;margin-top:12px}
.chain .cnode{border-radius:6px;padding:12px 13px;color:#fff}
.chain .cnode .n{font-size:12px;font-weight:900;opacity:.9;letter-spacing:.1em}
.chain .cnode .t{font-size:16px;font-weight:900;line-height:1.3;margin-top:5px}
.chain .cnode .d{font-size:12px;line-height:1.42;opacity:.94;margin-top:5px}
.chain .carrow{align-self:center;position:relative;height:16px}
.chain .carrow::before{content:"";position:absolute;left:4px;top:0;width:14px;height:2px;background:#C9C9C9}
.chain .carrow::after{content:"";position:absolute;left:16px;top:-4px;border-left:7px solid #C9C9C9;border-top:5px solid transparent;border-bottom:5px solid transparent}
.chain .cfoot{grid-column:1/8;display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:9px}
.chain .cfoot div{border:1px solid #E3E3E3;border-radius:5px;padding:8px 10px;font-size:12px;color:#5C5C5C;line-height:1.4}
.chain .cfoot div b{color:#CA1D39;font-weight:900}
.note{background:#FAEBD9;border:1px solid #E8C88C;border-left:5px solid #E1820D;border-radius:5px;padding:13px 15px;margin-top:12px;font-size:15.5px;line-height:1.6;color:#6B5320}
.note b{color:#8A3B1E;font-weight:900}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:12px}
.grid5{display:grid;grid-template-columns:repeat(5,1fr);gap:9px;margin-top:12px}
.vcard{border:1px solid #E3E3E3;border-radius:6px;padding:12px 13px;background:#fff;border-top:5px solid #277549}
.vcard .l{font-size:11.5px;font-weight:900;letter-spacing:.12em;color:#277549}
.vcard .t{font-size:16.5px;font-weight:900;color:#1A1A1A;margin-top:5px;line-height:1.3}
.vcard .d{font-size:13px;color:#6B6B6B;margin-top:6px;line-height:1.48}
.vcard .n{font-size:13px;font-weight:900;color:#277549;margin-top:6px}
.ins{border:1px solid #E3E3E3;border-radius:6px;padding:12px 14px;background:#fff;display:grid;grid-template-columns:44px 1fr;gap:12px;align-items:start}
.ins .q{font-size:19px;font-weight:900;color:#CA1D39;line-height:1.25}
.ins .t{font-size:16px;font-weight:800;color:#1A1A1A;line-height:1.36}
.ins .d{font-size:13px;color:#6B6B6B;line-height:1.45;margin-top:3px}
.final{background:#DDE9E2;border:1px solid #9CC4AE;border-radius:6px;padding:14px 16px;margin-top:13px;text-align:center;font-size:19px;font-weight:900;color:#1A5C3B;line-height:1.4}
.cta{display:grid;grid-template-columns:1.6fr 1fr;gap:11px;margin-top:13px}
.cta .big{background:#CA1D39;color:#fff;border-radius:6px;font-size:25px;font-weight:900;display:flex;align-items:center;justify-content:center;text-align:center;padding:16px 10px;line-height:1.28}
.cta .sm{border:1px solid #C9C9C9;border-radius:6px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:12px 8px;text-align:center}
.cta .sm .l{font-size:11px;letter-spacing:.14em;color:#8A8A8A;font-weight:800}
.cta .sm .v{font-size:22px;font-weight:900;color:#1A1A1A;margin-top:5px}
.bottom{padding:0 44px;border-top:2px solid #1A1A1A;margin:0 44px;display:flex;justify-content:space-between;align-items:center}
.stamp{font-size:12px;font-weight:800;letter-spacing:.14em;color:#7A7A7A}
.by{display:flex;align-items:center;gap:8px;font-size:13.5px;font-weight:900;letter-spacing:.04em;color:#3A3A3A}
.bsm{width:28px;height:28px;border-radius:50%;background:#CA1D39;color:#fff;font-size:13px;font-weight:900;display:flex;align-items:center;justify-content:center}
"""

BTOP = "<div class='brand'><span class='bbig'>B</span><span class='btxt'>ERIC &amp; B166ER</span></div>"
BBOT = "<div class='by'><span class='bsm'>B</span>ERIC &amp; B166ER</div>"


def _balance_one(frag):
    """单个块内补齐缺失的 </div>（补在块末）"""
    depth = 0
    extra = []
    for m in re.finditer(r'<div\b[^>]*>|</div>', frag):
        if m.group(0) != '</div>':
            depth += 1
        else:
            if depth > 0:
                depth -= 1
            else:
                extra.append(m.start())
    fixed = frag
    for s in sorted(extra, reverse=True):
        fixed = fixed[:s] + fixed[s + 6:]
    if depth > 0:
        fixed = fixed + "</div>" * depth
    return fixed


def _split_top(frag):
    """把 main 内容按顶层 div 切块，每块自平衡后再拼回"""
    spans = []
    depth = 0
    start = 0
    for m in re.finditer(r'<div\b[^>]*>|</div>', frag):
        if m.group(0) != '</div>':
            if depth == 0:
                start = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                spans.append((start, m.end()))
    if not spans:
        return frag
    out = [frag[:spans[0][0]]]
    for s, e in spans:
        out.append(_balance_one(frag[s:e]))
    out.append(frag[spans[-1][1]:])
    return "".join(out)


def page(meta, main):
    return ("<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><title>" + meta + "</title><style>"
            + CSS + "</style></head><body><div class='poster'>"
            + "<div class='top'>" + BTOP + "<div class='meta'>" + meta + "</div></div>"
            + "<div class='main'>" + main + "</div>"
            + "<div class='bottom'><div class='stamp'>酒店 · 财务 · 工具</div>" + BBOT + "</div>"
            + "</div></body></html>")


def blk(color, t, d, dark=False, extra=""):
    cls = "blk dark" if dark else "blk"
    st = " style='background:" + color + "'" if color else ""
    return ("<div class='" + cls + "'" + st + "><div class='t'>" + t + "</div>"
            + ("<div class='d'>" + d + "</div>" if d else "") + "</div>")


def side(cols, note_html, body_html, note_color="#FAEBD9", note_border="#E8C88C"):
    """左窄说明 + 右主体，两栏 grid"""
    return ("<div style='display:grid;grid-template-columns:" + cols
            + ";gap:12px;align-items:start'>"
            + "<div class='tnote' style='background:" + note_color + ";border:1px solid " + note_border
            + ";border-radius:5px;padding:10px 12px;font-size:12.5px;line-height:1.55;color:#6B5320'>"
            + note_html + "</div>"
            + "<div>" + body_html + "</div></div>")


def mini(items, cols=2):
    o = ["<div class='tlrow' style='grid-template-columns:repeat(" + str(cols) + ",1fr)'>"]
    for c, l, t2, d in items:
        o.append("<div class='blk' style='background:" + c + "'><div class='t'>" + l + "</div><div class='d'>" + t2 + "</div></div>")
    o.append("</div>")
    return "".join(o)

def layer(label, en, color, body):
    return ("<div class='tl'><div class='tlb' style='background:" + color + "'>" + label
            + "<span class='en'>" + en + "</span></div><div class='tln'>" + body + "</div></div>")


def arrow():
    return "<div class='tarrow'></div>"


def legend(items):
    o = ["<div class='legend'>"]
    for c, t in items:
        o.append("<span><i style='background:" + c + "'></i>" + t + "</span>")
    o.append("</div>")
    return "".join(o)


def kpis(items):
    return ("<div class='kpi'>" + "".join("<div><b>" + a + "</b><span>" + b + "</span></div>" for a, b in items) + "</div>")


P = {}

# ---------- P01 封面：总览拓扑 ----------
P['p01_cover'] = page("P01 · 封面", (
    "<div class='kicker'>集团酒店经营预算 · 空白模板 V1.0</div>"
    "<h1>71 张表 18618 条公式<br><span class='w'>一台</span><em>空白预算引擎</em></h1>"
    "<p class='lede'>把集团酒店经营预算，从<b>带着一家酒店历史数据的旧表</b>，改成<b>任何一家店都能重算的空白模型</b>。"
    "公式链、行号索引、批注与跨表引用关系全部保留，硬编码经营数据全部清空。</p>"
    + kpis([("71", "工作表"), ("18,618", "条公式，一条未删"), ("4 层", "数据流向"), ("0", "残留历史数据")])
    + "<div class='sec'><h2>信息拓扑总览<span class='note'>输入 → 部门 → 分摊 → 汇总 → 谁用</span></h2>"
    + "<div class='tl'><div class='tlb' style='background:#1A1A1A'>资产底座<span class='en'>TEMPLATE</span></div>"
    "<div class='tln'>" + blk("#1A1A1A", "酒店经营预算模板（空白模板）v1.0",
                              "71 张工作表 · 18,618 条计算公式 · 0.8 MB · 打开即重算 · 3 个外部链接处理方式写明")
    + "</div></div>"
    + arrow()
    + "<div class='tl'><div class='tlb' style='background:#CA1D39'>四层结构<span class='en'>4 LAYERS</span></div>"
    "<div class='tln'><div class='tlrow' style='grid-template-columns:repeat(4,1fr)'>"
    + blk(RED, "输入层 · 7 张", "细分市场与档位月度数据<br>唯一手填源头")
    + blk(ORG, "部门层 · 45 张", "一月至十二月的<br>收入、成本与人工行")
    + blk(GRN, "分摊层 · 8 张", "分摊基数与人数<br>其余公式分摊")
    + blk(YEL, "汇总层 · 8＋3 张", "全部公式生成<br>不得手工修改", dark=True)
    + "</div></div></div>"
    + arrow()
    + "<div class='tl'><div class='tlb' style='background:#257DD4'>谁在用<span class='en'>5 USERS</span></div>"
    "<div class='tln'><div class='tlrow' style='grid-template-columns:repeat(5,1fr)'>"
    + blk(BLU, "集团财务金融部", "口径统一与横向对比")
    + blk(BLU, "单店财务经理", "不再从零搭表")
    + blk(BLU, "酒店总经理", "看得懂经营表")
    + blk(BLU, "运营与收益", "单房产出自动成表")
    + blk(BLU, "新开业项目组", "直接套模板")
    + "</div></div></div>"
    + legend([(RED, "输入层 · 唯一手填源头"), (ORG, "部门层 · 填收入成本人工"),
              (GRN, "分摊层 · 填基数与人数"), (YEL, "汇总层 · 全自动"), (BLU, "使用者")])
    + "</div>"
    + "<div class='final'>往下翻：它清了什么 · 它保住了什么 · 四层数据怎么流 · 你要怎么填</div>"
))

# ---------- P02 痛点链 ----------
P['p02_painpoints'] = page("P02 · 痛点", (
    "<h2>预算编制最贵的不是时间<span class='note'>是返工</span></h2>"
    "<div class='chain'>"
    "<div class='cnode' style='background:#A3A3A3'><div class='n'>STEP 01</div><div class='t'>旧模板带着<br>一家店的历史数据</div>"
    "<div class='d'>换个店套不上，改一次错一年。<b>40,616 处硬编码</b>成了谁都不敢动的地雷。</div></div>"
    "<div class='carrow'></div>"
    "<div class='cnode' style='background:#CA1D39'><div class='n'>STEP 02</div><div class='t'>跨表复制手写<br>数字对不上</div>"
    "<div class='d'>餐饮收入本该来自餐饮部，却又填了一遍。<b>一处填错，64 张表跟着错。</b></div></div>"
    "<div class='carrow'></div>"
    "<div class='cnode' style='background:#E1820D'><div class='n'>STEP 03</div><div class='t'>各店口径不一<br>集团没法比</div>"
    "<div class='d'>出租率、每间可售房收入、人工口径各写各的，<b>汇总表靠人工对齐</b>。</div></div>"
    "<div class='carrow'></div>"
    "<div class='cnode' style='background:#FFD90D;color:#1A1A1A'><div class='n'>STEP 04</div><div class='t'>年份写死在<br>公式里</div>"
    "<div class='d'>每到新的一年就重做一遍，<b>复制粘贴当研发</b>；改年份还会误伤行号索引。</div></div>"
    "<div class='cfoot'>"
    "<div><b>40,616</b> 处硬编码清空</div>"
    "<div><b>276</b> 处伪装成公式的数据清空</div>"
    "<div><b>64</b> 张表由公式带出</div>"
    "<div><b>5</b> 年每年重做一遍</div>"
    "</div></div>"
    "<div class='note'>这四件事的共同点是：<b>它们都不是设计问题，是数据资产没有归位。</b>"
    "模板里真正值钱的是公式链和口径，而它被历史数据压在下面看不见。</div>"
))

# ---------- P03 主视觉：完整数据流向拓扑 ----------
P['p03_topo'] = page("P03 · 信息拓扑图", (
    "<h2>四层数据流向拓扑<span class='note'>从填数到出表，只有一条路</span></h2>"
    + side("236px",
           "<b>清洗结果</b><br>硬编码清空 <b>40,616</b> 处<br>伪装公式清空 <b>276</b> 处<br>"
           "公式保留 <b>18,618</b> 条<br>缓存值剥离 <b>18,603</b> 处<br>行号索引保留 <b>274</b> 个<br>批注保留 <b>29</b> 张表",
           layer("L1 输入层", "7 TABLES", RED,
                 blk(RED, "细分市场与餐饮收入 7 张",
                     "细分市场模板、宴会市场细分及收入分析、餐饮收入、Rooms Segments 市场细分、Banquet Segment 宴会市场细分")
                 + "<div style='font-size:12.5px;color:#8A3B1E;background:#F6DBDF;border-radius:4px;padding:7px 10px'>"
                   "<b>填：</b>各细分市场及档位的月度数据 —— 全表唯一手填源头</div>")
           + arrow()
           + layer("L2 部门层", "45 TABLES", ORG,
                   blk(ORG, "房务 · 前厅 · 客房 · 行政楼层 · 餐饮与十一个餐厅 · 宴会 · 市场销售 · 采购 · 行政 · 人力 · 工程",
                       "共 45 张标准部门损益表，统一 22 列结构")
                   + "<div style='font-size:12.5px;color:#8A3B1E;background:#FAEBD9;border-radius:4px;padding:7px 10px'>"
                     "<b>填：</b>一月至十二月的收入、成本与人工行 —— 收入只填最底层一次，部门之间不得重复填</div>")
           + arrow()
           + layer("L3 分摊层", "8 TABLES", GRN,
                   blk(GRN, "餐饮间接费用 · 人工成本及员工人数 · 员餐分摊 · 洗衣房分摊 · 主营业务成本下人工 · 管理费用下人工 · 非经营性费用",
                       "把公共成本按业务真实动因摊到各部门")
                   + "<div style='font-size:12.5px;color:#1A5C3B;background:#DDE9E2;border-radius:4px;padding:7px 10px'>"
                     "<b>填：</b>分摊基数与人数 —— 其余全部由公式分摊</div>")
           + arrow()
           + layer("L4 汇总层", "8 + 3 TABLES", YEL,
                   blk(YEL, "Total 酒店汇总表 · 财务关键指标 · 国资委快报 · 客房餐饮部门利润率 · 餐饮部收入结构分解 · 利润表 · 资产负债表 · 现金流量表",
                       "全部由公式生成", dark=True)
                   + "<div style='font-size:12.5px;color:#6B5320;background:#FBF3D6;border-radius:4px;padding:7px 10px'>"
                     "<b>不填：</b>任何一个数值都不许手改 —— 手改即失效</div>")
           + arrow()
           + layer("L5 谁在用", "5 USERS", BLU,
                   mini([(BLU, "集团财务", "口径与横向对比"), (BLU, "单店财务", "编制不再搭表"),
                         (BLU, "总经理", "读经营表"), (BLU, "运营收益", "单房产出"), (BLU, "新开业", "直接套用")], 5)))
    + legend([(RED, "输入层 · 唯一手填源头"), (ORG, "部门层 · 填收入成本人工"),
              (GRN, "分摊层 · 填基数与人数"), (YEL, "汇总层 · 全自动"), (BLU, "使用者")])
    + "<div class='sec'><h2>四张关键表怎么读<span class='note'>读表也是方法的一部分</span></h2>"
    + g2([("#CA1D39", "TOTAL 汇总表", "以万元计。C 列为本年预算，D 列为上一版本预算，E 与 F 列为同比额与同比率，G 列为上年预测，H 与 I 列为同比额与同比率，J 列为上年预算。", "#CA1D39"),
          ("#E1820D", "财务关键指标", "以万元计。C 列本年预算，D 列上年预测，E 与 F 列为增减额与增减率，G 列历史基准年实际。出租率、人均指标全部自动取自损益表汇总表。", "#E1820D"),
          ("#277549", "利润表与现金流量表", "以元计。C 列为上年九月末，D 列为上年十月至十二月预估，E 列为上年全年预计，F 列起为本年逐月数据，需按月填写。", "#277549"),
          ("#257DD4", "资产负债表", "以元计。H3 单元格标注对标来源为港中旅财报 01 表，D4 单元格标注已核对；期初、期末余额与科目行次须补充填写。", "#257DD4")])
    + "</div>"
    + "<div class='final'>先看这张拓扑再动手：填数只在 L1、L2、L3 三层发生，L4 永远不要碰</div>"
))

E.setdefault('p02_painpoints', "")
E['p02_painpoints'] += (
    "<div class='sec'><h2>数据资产归位后会发生什么<span class='note'>四个直接变化</span></h2>"
    + g2([("#277549", "变化 01", "编制时间从月级降到周级", "不再搭表、不再对数、不再复制粘贴，只填 7 张输入层。"),
          ("#277549", "变化 02", "错误在源头就被拦住", "跨表引用由公式建立，重复填收入会被直接算出来。"),
          ("#257DD4", "变化 03", "集团第一次能横向比店", "统一口径下比较每间可售房收入与营业利润率。"),
          ("#257DD4", "变化 04", "换人也能接着做", "口径写进表与说明，交接即可复用，不依赖个人经验。")])
    + "</div>"
)

E.setdefault('p06_quotes', "")
E['p06_quotes'] += (
    "<div class='sec'><h2>三条最容易踩的坑<span class='note'>说明书已提前标注</span></h2>"
    + g3([("#CA1D39", "坑 01", "先看汇总层再回头找", "要自下而上排查：输入层 → 部门层 → 分摊层 → 汇总层。"),
          ("#E1820D", "坑 02", "以为没数据是文件坏了", "打开后大量为零或空白是正常的：B 至 M 未填时公式自然算为零。"),
          ("#277549", "坑 03", "把年份和行号一起替换", "A 列是行号索引，只替换 XXXX 系列偏移量，A 列不动。")])
    + "</div>"
)

for _k in list(P.keys()):
    _st = _check_structure(P[_k])
    if _st != "poster直接子元素=3(应为3)":
        print("  !! 结构异常 " + _k + ": " + _st)

for k, v in P.items():
    open(os.path.join(HTMLD, k + ".html"), "w", encoding="utf-8", newline="\n").write(v)

BAD = ["微信", "加微信", "加我", "扫码", "扫一扫", "二维码", "支付宝", "抖音", "微博", "私域", "引流", "企业开票", "1对 1", "1对1"]
hits = [(k, b) for k, v in P.items() for b in BAD if b in v]
print("HTML written:", len(P))
print("R29 forbidden:", hits if hits else "none")
