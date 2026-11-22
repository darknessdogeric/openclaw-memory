# -*- coding: utf-8 -*-
"""小红书 9 图 · 酒店经营预算模板（空白模板）产品介绍
范式：GS 酒店朋友圈 v2 参考（暗蓝黑底 + 金橙强调 + 圆角卡片 + 高密度）
第 6 张用信息拓扑图语言（层级色条 + 实心色块 + 流向箭头 + 图例）
B 标：R30 严格左上(大) + 右下(小)，写法 ERIC & B166ER
"""
import io, os, re, sys, time, subprocess, shutil

WS = r'D:\B166ER-openclaw\workspace'
OUT = os.path.join(r'C:\Users\ericz\Desktop\产业发展部\外部相关资料\全面预算管理', '小红书9图_预算模板')
HTMLD = os.path.join(OUT, 'html')
PNGD = os.path.join(OUT, 'png')
os.makedirs(HTMLD, exist_ok=True)
os.makedirs(PNGD, exist_ok=True)
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1440px}
body{background:#0F1424;font-family:"Microsoft YaHei","PingFang SC","Noto Sans CJK SC",sans-serif;-webkit-font-smoothing:antialiased;color:#fff}
.poster{width:1080px;height:1440px;position:relative;overflow:hidden;display:grid;grid-template-rows:132px 1fr 104px;
background:radial-gradient(1200px 700px at 78% -8%,#1E2742 0%,#141A2E 46%,#0F1424 100%)}
.top{padding:30px 52px 0;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid rgba(255,255,255,.12);margin:0 52px}
.brand{display:flex;align-items:center;gap:12px}
.bbig{width:66px;height:66px;border-radius:50%;background:#E0A94A;color:#141A2E;font-size:32px;font-weight:900;display:flex;align-items:center;justify-content:center;letter-spacing:-.02em}
.btxt{font-size:19px;font-weight:800;letter-spacing:.06em;color:#E8ECF7}
.meta{font-size:13px;font-weight:700;letter-spacing:.18em;color:#7F89A6}
.main{padding:20px 52px 16px;display:flex;flex-direction:column;justify-content:space-between;min-height:0}
.kicker{display:inline-flex;align-items:center;gap:9px;font-size:16px;font-weight:800;letter-spacing:.16em;color:#E0A94A}
.kicker::before{content:"";width:9px;height:9px;background:#E0A94A;border-radius:50%}
h1{font-size:60px;line-height:1.38;font-weight:900;letter-spacing:-.01em;margin:12px 0 0}
h1 em{font-style:normal;color:#E0A94A}
h1 .w{color:#9AA3BC}
.lede{font-size:17.5px;line-height:1.66;color:#A7B0C8;margin:11px 0 0}
.lede b{color:#E8ECF7}
h2{font-size:25px;line-height:1.32;font-weight:900;margin:0;display:flex;align-items:center;gap:10px;color:#fff}
h2::before{content:"";width:8px;height:25px;background:#E0A94A;border-radius:2px}
h2 .note{margin-left:auto;font-size:13px;color:#7F89A6;font-weight:600}
.sec{margin-top:22px;min-height:0}
.rule{height:1px;background:rgba(255,255,255,.10);margin:14px 0 0}
.kpi{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:14px}
.kpi div{background:#232B45;border:1px solid rgba(255,255,255,.10);border-radius:8px;padding:12px 13px}
.kpi b{display:block;font-size:33px;font-weight:900;color:#E0A94A;line-height:1.1;letter-spacing:-.01em}
.kpi span{display:block;font-size:13.5px;color:#9AA3BC;margin-top:6px;line-height:1.4}
.cards{display:flex;flex-direction:column;gap:11px;margin-top:13px}
.card{background:#232B45;border:1px solid rgba(255,255,255,.09);border-radius:8px;padding:13px 16px;display:grid;grid-template-columns:50px 1fr;gap:14px;align-items:start}
.card .n{font-size:23px;font-weight:900;color:#E0A94A;line-height:1.25}
.card .t{font-size:21px;font-weight:800;color:#fff;line-height:1.32}
.card .d{font-size:15px;color:#9AA3BC;line-height:1.5;margin-top:4px}
.card .d b{color:#C8D0E4;font-weight:700}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:12px}
.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin-top:12px}
.tile{background:#232B45;border:1px solid rgba(255,255,255,.09);border-radius:8px;padding:14px 14px}
.tile .l{font-size:13px;font-weight:800;letter-spacing:.12em;color:#E0A94A}
.tile .v{font-size:18px;font-weight:800;color:#fff;margin-top:7px;line-height:1.32}
.tile .d{font-size:14px;color:#9AA3BC;margin-top:6px;line-height:1.48}
.tile.green{background:#17332C;border-color:#2A5348}
.tile.green .l{color:#6FCBA6}
.tile.red{background:#33212A;border-color:#5A3540}
.tile.red .l{color:#E58A96}
.tile.blue{background:#1A2E4A;border-color:#2C4A72}
.tile.blue .l{color:#7FB2E8}
.list{margin-top:13px;display:flex;flex-direction:column;gap:10px}
.li{background:#232B45;border:1px solid rgba(255,255,255,.09);border-radius:8px;padding:14px 16px;font-size:16px;line-height:1.58;color:#A7B0C8}
.li b{color:#fff;font-weight:800}
.li .q{color:#E0A94A;font-weight:900}
.lead{background:#1B2340;border:1px solid rgba(224,169,74,.34);border-left:5px solid #E0A94A;border-radius:8px;padding:17px 19px;margin-top:13px}
.lead p{font-size:19px;line-height:1.64;color:#C8D0E4}
.lead p+p{margin-top:9px}
.lead p b{color:#fff;font-weight:900}
.lead .hl{color:#E0A94A;font-weight:900}
.final{background:#17332C;border:1px solid #2A5348;border-radius:8px;padding:15px 18px;margin-top:13px;text-align:center;font-size:20px;font-weight:900;color:#6FCBA6;line-height:1.4}
.cta{display:grid;grid-template-columns:1.6fr 1fr;gap:12px;margin-top:13px}
.cta .big{background:#E0A94A;color:#141A2E;border-radius:8px;font-size:27px;font-weight:900;display:flex;align-items:center;justify-content:center;text-align:center;padding:16px 10px;line-height:1.26}
.cta .sm{border:1px solid rgba(255,255,255,.22);border-radius:8px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:12px 8px;text-align:center}
.cta .sm .l{font-size:11.5px;letter-spacing:.14em;color:#7F89A6;font-weight:800}
.cta .sm .v{font-size:23px;font-weight:900;color:#fff;margin-top:5px}
.bottom{padding:0 52px;border-top:1px solid rgba(255,255,255,.12);margin:0 52px;display:flex;justify-content:space-between;align-items:center}
.stamp{font-size:12.5px;font-weight:800;letter-spacing:.16em;color:#6E7899}
.by{display:flex;align-items:center;gap:9px;font-size:14px;font-weight:800;letter-spacing:.05em;color:#C8D0E4}
.bsm{width:32px;height:32px;border-radius:50%;background:#E0A94A;color:#141A2E;font-size:15px;font-weight:900;display:flex;align-items:center;justify-content:center}
/* ===== 拓扑图（P06）===== */
.topo{display:grid;grid-template-columns:74px 1fr;gap:0;margin-top:13px}
.lrow{display:grid;grid-template-rows:1fr;align-items:stretch}
.lbar{border-radius:6px;display:flex;align-items:center;justify-content:center;text-align:center;font-size:13px;font-weight:900;letter-spacing:.06em;line-height:1.35;padding:8px 4px;writing-mode:vertical-rl}
.lbar .en{font-size:11px;font-weight:700;opacity:.85;letter-spacing:.14em;margin-top:6px}
.lnodes{display:flex;flex-direction:column;gap:7px;padding-left:12px}
.node{background:#2A3450;border-radius:6px;padding:9px 12px;border-left:4px solid #E0A94A}
.node .nt{font-size:16px;font-weight:800;color:#fff}
.node .nd{font-size:12.5px;color:#9AA3BC;margin-top:2px;line-height:1.4}
.node .nf{font-size:11.5px;color:#E0A94A;font-weight:800;margin-top:3px}
.arrow{height:16px;margin-left:12px;position:relative}
.arrow::before{content:"";position:absolute;left:0;top:0;width:2px;height:11px;background:rgba(224,169,74,.55)}
.arrow::after{content:"";position:absolute;left:-4px;top:10px;border-left:5px solid transparent;border-right:5px solid transparent;border-top:7px solid rgba(224,169,74,.75)}
.legend{display:flex;flex-wrap:wrap;gap:8px;margin-top:11px}
.legend span{font-size:12px;color:#A7B0C8;display:flex;align-items:center;gap:6px}
.legend i{width:13px;height:13px;border-radius:3px;display:inline-block}
"""

BTOP = '<div class="brand"><span class="bbig">B</span><span class="btxt">ERIC &amp; B166ER</span></div>'
BBOT = '<div class="by"><span class="bsm">B</span>ERIC &amp; B166ER</div>'


def page(meta, main):
    return ("<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><title>" + meta + "</title><style>"
            + CSS + "</style></head><body><div class='poster'>"
            + "<div class='top'>" + BTOP + "<div class='meta'>" + meta + "</div></div>"
            + "<div class='main'>" + main + "</div>"
            + "<div class='bottom'><div class='stamp'>酒店 · 财务 · 工具</div>" + BBOT + "</div>"
            + "</div></body></html>")


def cards(items):
    o = ["<div class='cards'>"]
    for n, t, d in items:
        o.append("<div class='card'><div class='n'>" + n + "</div><div><div class='t'>" + t + "</div><div class='d'>" + d + "</div></div></div>")
    o.append("</div>")
    return "".join(o)


def kpis(items):
    return ("<div class='kpi'>" + "".join("<div><b>" + a + "</b><span>" + b + "</span></div>" for a, b in items) + "</div>")


def tiles(cols, items):
    o = ["<div class='g" + str(cols) + "'>"]
    for cls, l, v, d in items:
        o.append("<div class='tile " + cls + "'><div class='l'>" + l + "</div><div class='v'>" + v + "</div><div class='d'>" + d + "</div></div>")
    o.append("</div>")
    return "".join(o)


def lis(items):
    return "<div class='list'>" + "".join("<div class='li'>" + x + "</div>" for x in items) + "</div>"


P = {}

P['p01_cover'] = page("P01 · 封面", (
    "<div class='kicker'>集团酒店经营预算 · 空白模板 V1.0</div>"
    "<h1>71 张表<br><span class='w'>18618 条公式</span><br>一台<span class='em'>空白预算引擎</span></h1>"
    "<p class='lede'>把集团酒店经营预算从<b>带一家酒店历史数据的旧表</b>，改成<b>任何一家店都能重算的空白模型</b>。"
    "公式链、行号索引、批注、跨表引用关系全部保留，硬编码经营数据全部清空。</p>"
    + kpis([("71", "工作表（输入 7／部门 45／分摊 8／汇总 8／三表 3）"), ("18,618", "计算公式，一条未删"), ("4 层", "数据流向：输入→部门→分摊→汇总"), ("0", "残留的历史经营数据")])
    + "<div class='rule'></div>"
    + "<div class='final'>往下翻：它清了什么 · 它保住了什么 · 你要怎么填</div>"
    + "<div class='cta'><div class='big'>九张图讲完<br>一台空白的预算引擎</div>"
    "<div class='sm'><div class='l'>GET</div><div class='v'>评论区扣 1</div></div></div>"
))

P['p02_painpoints'] = page("P02 · 痛点", (
    "<h2>预算编制最贵的不是时间<span class='note'>是返工</span></h2>"
    + cards([
        ("01", "旧模板带着一家酒店的历史数据", "换个店套不上，改一次错一年；<b>40,616 处硬编码</b>成了谁都不敢动的地雷。"),
        ("02", "跨表复制手写，数字对不上", "餐饮收入该来自餐饮部，却又填了一遍；<b>一处填错，64 张表跟着错</b>。"),
        ("03", "各店口径不一，集团没法比", "出租率、每间可售房收入、人工口径各写各的，<b>汇总表靠人工对齐</b>。"),
        ("04", "年份写死在公式里", "每到新的一年就重做一遍，<b>复制粘贴当研发</b>；改年份还会误伤行号索引。"),
    ])
    + "<div class='lead'><p>这四件事的共同点是：<span class='hl'>它们都不是设计问题，是数据资产没有归位</span>。"
    "模板里真正值钱的是公式链和口径，而它被历史数据压在下面看不见。</p></div>"
))

P['p03_value'] = page("P03 · 价值", (
    "<h2>清掉数据，模型才算数<span class='note'>七个变化</span></h2>"
    + tiles(2, [
        ("", "01", "数据归零，模型归位", "40,616 处硬编码、276 处伪装成公式的数据一并清空，A 列以外无残留。"),
        ("", "02", "一条数据链，四层贯通", "输入→部门→分摊→汇总，改最底层一次，全表联动重算。"),
        ("", "03", "年份参数化", "XXXX／XXXX-1／XXXX-4 偏移量写法，换目标年度只替换、不重建。"),
        ("", "04", "口径写进表里", "40 余张部门损益表共用同一套 22 列结构，A 列中英对照说明已建好。"),
        ("green", "05", "填数边界清晰", "B 至 M 手填，其余全部系统带出；汇总层八个表禁止手改。"),
        ("green", "06", "批注与索引留痕", "29 张表批注完成去数据化，274 个行号索引原样保留。"),
        ("green", "07", "打开即重算", "18,603 处公式缓存值已剥离；3 个外部链接已给三种处理方式。"),
    ])
))

P['p04_audience'] = page("P04 · 给谁用", (
    "<h2>五类人会立刻感觉到差别<span class='note'>谁该拿走这份模板</span></h2>"
    + cards([
        ("01", "集团财务金融部", "口径统一与横向对比的底座；<b>国资委快报</b>与财务关键指标自动生成。"),
        ("02", "单店财务经理", "不再从零搭表；<b>细分市场填完，部门表带出，汇总表自动落</b>。"),
        ("03", "酒店总经理", "看得懂经营表；<b>每间可售房收入、出租率、人均指标</b>不必再问财务。"),
        ("04", "运营与收益团队", "人工成本按人数分摊到部门，<b>人工效率与单房产出自动成表</b>。"),
        ("05", "新开业项目组", "直接套模板，<b>不用重建历史列</b>；先填一家店也能带出全店口径。"),
    ])
    + "<div class='lead'><p>它同时是一份<b>培训教材</b>：<span class='hl'>十节说明</span>讲清每张表读什么、"
    "哪些列能填、为什么顺序不能错，新人照着填就不会填错。</p></div>"
))

P['p05_chapters'] = page("P05 · 结构", (
    "<h2>模板怎么用：十节讲清<span class='note'>附工作表一览 71 张</span></h2>"
    + tiles(2, [
        ("", "01", "基本情况与清洗说明", "71 张表、18,618 条公式、计量单位与跨表核对口径。"),
        ("", "02", "四层结构与职责", "输入层填数、部门层填数、分摊层填基数、汇总层全自动。"),
        ("", "03", "标准部门损益表列结构", "第 1 行表名、第 2 行列组并含三个年度区、第 3 行月份。"),
        ("", "04", "跨表引用与填写边界", "收入只填最底层一次，部门之间不得重复填。"),
        ("", "05", "五步填写顺序", "市场细分 → 部门收入成本人工 → 分摊基数 → 核对三表 → 核对汇总。"),
        ("", "06", "各表读法要点", "Total 汇总表、财务关键指标、利润表与现金流量表、资产负债表。"),
        ("", "07", "年度参数规则", "XXXX 为本年，XXXX-4 为历史基准年，即实际数所在列。"),
        ("", "08", "外部链接处理", "3 个外部工作簿引用：重新指向或彻底断开，两条路径写明。"),
        ("", "09", "数据清洗清单", "清了什么、留了什么、留痕在哪，逐项可查。"),
        ("", "10", "使用注意事项与常见问题", "不改列、不改 A 列、不手改汇总表；六类高频问题解答。"),
    ])
))

P['p06_topo'] = page("P06 · 信息拓扑图", (
    "<h2>四层数据流向拓扑<span class='note'>从填数到出表，只有一条路</span></h2>"
    "<div class='topo'>"
    "<div class='lrow'><div class='lbar' style='background:#1A2E4A;color:#7FB2E8'>L1 输入层<span class='en'>7 TABLES</span></div></div>"
    "<div class='lnodes'>"
    "<div class='node' style='border-left-color:#7FB2E8'><div class='nt'>输入层 · 7 张</div><div class='nd'>细分市场模板、宴会市场细分及收入分析、餐饮收入、Rooms Segments 市场细分、Banquet Segment 宴会市场细分</div><div class='nf'>填：各细分市场与档位的月度数据 —— 全表唯一源头</div></div>"
    "</div></div>"
    "<div class='arrow'></div>"
    "<div class='topo'>"
    "<div class='lrow'><div class='lbar' style='background:#4A3410;color:#E0A94A'>L2 部门层<span class='en'>45 TABLES</span></div></div>"
    "<div class='lnodes'>"
    "<div class='node' style='border-left-color:#E0A94A'><div class='nt'>部门层 · 45 张</div><div class='nd'>房务部、前厅部、客房部、行政楼层、餐饮部与十一个餐厅、宴会、市场销售、采购部、行政部、人力资源部、工程维修等</div><div class='nf'>填：一月至十二月的收入、成本与人工行 —— 收入只填最底层一次</div></div>"
    "</div></div>"
    "<div class='arrow'></div>"
    "<div class='topo'>"
    "<div class='lrow'><div class='lbar' style='background:#17332C;color:#6FCBA6'>L3 分摊层<span class='en'>8 TABLES</span></div></div>"
    "<div class='lnodes'>"
    "<div class='node' style='border-left-color:#6FCBA6'><div class='nt'>分摊层 · 8 张</div><div class='nd'>餐饮间接费用、人工成本及员工人数、员餐分摊、洗衣房分摊、主营业务成本下人工、管理费用下人工、非经营性费用</div><div class='nf'>填：分摊基数与人数 —— 其余全部由公式分摊</div></div>"
    "</div></div>"
    "<div class='arrow'></div>"
    "<div class='topo'>"
    "<div class='lrow'><div class='lbar' style='background:#33212A;color:#E58A96'>L4 汇总层<span class='en'>8 + 3 TABLES</span></div></div>"
    "<div class='lnodes'>"
    "<div class='node' style='border-left-color:#E58A96'><div class='nt'>汇总层 · 8 张 ＋ 财务三表 · 3 张</div><div class='nd'>Total 酒店汇总表、财务关键指标、Flash Report 国资委快报、客房餐饮部门利润率、利润表、资产负债表、现金流量表</div><div class='nf'>全公式生成 —— 不得手工修改任何数值</div></div>"
    "</div></div>"
    "</div>"
    "<div class='legend'><span><i style='background:#1A2E4A'></i>输入层 · 唯一手填源头</span>"
    "<span><i style='background:#4A3410'></i>部门层 · 填收入成本人工</span>"
    "<span><i style='background:#17332C'></i>分摊层 · 填基数与人数</span>"
    "<span><i style='background:#33212A'></i>汇总层 · 全自动</span></div>"
    + kpis([("22", "标准部门损益表列结构"), ("7", "张表是真正手填源头"), ("18,618", "条公式串起全链"), ("64", "张表由公式带出")])
))

P['p07_quotes'] = page("P07 · 关键洞察", (
    "<h2>五句想清楚就不一样的話<span class='note'>来自清洗与使用过程</span></h2>"
    + lis([
        "<span class='q'>「模板不是用来抄的，是用来算的。」</span>　清空历史数据之后，公式链才第一次露出它的样子。",
        "<span class='q'>「真正的数据源只有 7 张表，其余 64 张都是公式。」</span>　填错源头，全盘皆错；这也是为什么填写顺序不能颠倒。",
        "<span class='q'>「在汇总层改一个数，整份预算就不可信了。」</span>　汇总层的手工修改，是最贵也最隐蔽的错误。",
        "<span class='q'>「年份写死一次，明年重做一次。」</span>　参数化不是偷懒，是把重复劳动一次性归零。",
        "<span class='q'>「口径不统一的汇总表，比没有汇总表更危险。」</span>　可比的底线是对齐，不是加总。",
    ])
    + "<div class='lead'><p>这五条共同指向一件事：<span class='hl'>数据资产要归位，模型才有价值</span>。"
    "这也是为什么这份交付是「模板＋使用说明」两份，而不是一份空表。</p></div>"
))

P['p08_delivery'] = page("P08 · 交付物", (
    "<h2>三份东西，直接可用<span class='note'>已随附</span></h2>"
    + tiles(1, [
        ("blue", "DELIVERABLE 01", "附件5 酒店经营预算模板-汇总版（空白模板）v1.0.xlsx",
         "71 张工作表 · 18,618 条公式 · 4 层数据流向 · 0.8 MB · 打开即重算 · 3 个外部链接处理方式写明。"),
        ("", "DELIVERABLE 02", "附件5 酒店经营预算模板（空白模板）v1.0_使用说明.docx",
         "十节正文 · 71 张工作表一览（名称／层级／填数说明）· 22 列填写要求表 · 六类常见问题解答。"),
        ("green", "DELIVERABLE 03", "配套可执行件",
         "参数化年度替换规则 · 3 个外部链接处理指引 · 29 张表批注清单（已去数据化）· 清洗前后对照。"),
    ])
    + "<div class='lead'><p>清洗结果同样可查：<b>硬编码清空 40,616 处</b>、伪装公式清空 <b>276 处</b>、"
    "公式缓存值剥离 <b>18,603 处</b>、行号索引保留 <b>274 个</b>、批注保留 <b>29 张表</b>。</p></div>"
))

P['p09_cta'] = page("P09 · 行动", (
    "<h2>三个动作<span class='note'>拿走就能用</span></h2>"
    + cards([
        ("A", "集团向：纳入标准动作", "把这份空白模板写进年度预算编制流程，<b>停止各店自建表</b>；口径统一从源头做。"),
        ("B", "行业向：把方法做成产品", "「空白模板＋使用说明＋参数化＋清洗 SOP」是一整套可复制的方法，<b>同业也需要</b>。"),
        ("C", "自留：清洗流程固化", "40616→0 的这套清洗与校验流程已沉淀，<b>换一个项目即可复用</b>。"),
    ])
    + "<div class='lead'><p>如果你正在做下一年的预算：<span class='hl'>先填 7 张输入层表，再往下走</span>。"
    "顺序错了，后面 64 张表的数字都不作数。</p></div>"
    + "<div class='cta'><div class='big'>评论区扣 1<br>私信领取完整工作表一览</div>"
    "<div class='sm'><div class='l'>SAVE</div><div class='v'>先收藏</div></div></div>"
    + "<div class='final'>结论：真正的资产不是那张表，是那 18618 条还在的公式</div>"
))

# ---------- 写 HTML ----------
for k, v in P.items():
    open(os.path.join(HTMLD, k + ".html"), "w", encoding="utf-8", newline="\n").write(v)
print("HTML written:", len(P), "files")

# ---------- R29 合规检查 ----------
BAD = ["微信", "加微信", "加我", "扫码", "扫一扫", "二维码", "支付宝", "抖音", "微博", "私域", "引流", "企业开票", "1对 1", "1对1"]
hits = []
for k, v in P.items():
    for b in BAD:
        if b in v:
            hits.append((k, b))
print("R29 forbidden words:", hits if hits else "none")

# ---------- 渲染交给 _render_xhs9.py（Playwright 管线） ----------
print("HTML done. R29 forbidden words:", hits if hits else "none")
print("渲染请执行: python toolbox/_render_xhs9.py")
