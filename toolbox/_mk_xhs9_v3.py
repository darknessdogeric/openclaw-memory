# -*- coding: utf-8 -*-
"""小红书 9 图 v3（最终）· 浅色信息拓扑范式
CSS 从 _mk_xhs9_light.py 抽取复用；9 张全部由平衡 helper 构建；内容量按满版设计
"""
import io, os, re, sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

WS = r'D:\B166ER-openclaw\workspace'
SRC = os.path.join(WS, 'toolbox', '_mk_xhs9_light.py')
OUT = r'C:\Users\ericz\Desktop\产业发展部\外部相关资料\全面预算管理\小红书9图_预算模板'
HTMLD = os.path.join(OUT, "html")
os.makedirs(HTMLD, exist_ok=True)

_s = open(SRC, encoding='utf-8').read()
CSS = _s.split('CSS = """', 1)[1].split('"""', 1)[0]

RED, ORG, YEL, GRN, BLU, GRY, BLK = "#CA1D39", "#E1820D", "#FFD90D", "#277549", "#257DD4", "#A3A3A3", "#1A1A1A"

BTOP = "<div class='brand'><span class='bbig'>B</span><span class='btxt'>ERIC &amp; B166ER</span></div>"
BBOT = "<div class='by'><span class='bsm'>B</span>ERIC &amp; B166ER</div>"


# ---------------- 平衡 helper ----------------
def blk(color, t, d="", dark=False):
    st = " style='background:" + color + "'"
    cls = "blk dark" if dark else "blk"
    o = "<div class='" + cls + "'" + st + "><div class='t'>" + t + "</div>"
    if d:
        o += "<div class='d'>" + d + "</div>"
    return o + "</div>"


def mini(items, cols=2):
    o = ["<div class='tlrow' style='grid-template-columns:repeat(" + str(cols) + ",1fr)'>"]
    for it in items:
        c = it[0]
        t = it[1]
        d = it[2] if len(it) > 2 else ""
        o.append(blk(c, t, d))
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


def note(html, color="#FAEBD9", border="#E8C88C"):
    return ("<div class='note' style='background:" + color + ";border-color:" + border
            + ";border-left-color:" + border + "'>" + html + "</div>")


def kpis(items):
    return ("<div class='kpi'>" + "".join("<div><b>" + a + "</b><span>" + b + "</span></div>" for a, b in items) + "</div>")


def vcard(*a):
    color = a[0]
    if len(a) >= 5:
        l, t, d, ex = a[1], a[2], a[3], a[4]
        d = d + "<br>" + ex
    elif len(a) == 4:
        l, t, d = a[1], a[2], a[3]
    elif len(a) == 3:
        l, t, d = '', a[1], a[2]
    else:
        l, t, d = '', a[1], ''
    o = ("<div class='vcard' style='border-top-color:" + color + "'>")
    if l:
        o += "<div class='l'>" + l + "</div>"
    o += "<div class='t'>" + t + "</div><div class='d'>" + d + "</div></div>"
    return o


def g2(items):
    return "<div class='grid2'>" + "".join(vcard(*x) for x in items) + "</div>"


def g3(items):
    return "<div class='grid3'>" + "".join(vcard(*x) for x in items) + "</div>"


def g5(items):
    return "<div class='grid5'>" + "".join(vcard(*x) for x in items) + "</div>"


def side(cols, note_html, body_html):
    return ("<div style='display:grid;grid-template-columns:" + cols + ";gap:12px;align-items:start'>"
            + "<div class='tnote' style='background:#FAEBD9;border:1px solid #E8C88C;border-radius:5px;padding:10px 12px;"
              "font-size:12.5px;line-height:1.55;color:#6B5320'>" + note_html + "</div>"
            + "<div>" + body_html + "</div></div>")


def ins(n, t, d):
    return ("<div class='ins'><div class='q'>" + n + "</div><div><div class='t'>" + t
            + "</div><div class='d'>" + d + "</div></div></div>")


def page(meta, main):
    return ("<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><title>" + meta + "</title><style>"
            + CSS + "</style></head><body><div class='poster'>"
            + "<div class='top'>" + BTOP + "<div class='meta'>" + meta + "</div></div>"
            + "<div class='main'>" + main + "</div>"
            + "<div class='bottom'><div class='stamp'>酒店 · 财务 · 工具</div>" + BBOT + "</div>"
            + "</div></body></html>")


P = {}

P['p00_title'] = page("P01 · 标题封面", (
    "<div class='kicker'>集团全面预算管理 · 空白模板 V1.0</div>"
    "<h1 style='font-size:84px;line-height:1.18;margin-top:18px'>酒店全面<br>预算管理工具<br><em>空白模板 v1.0</em></h1>"
    "<p class='lede' style='font-size:19px;max-width:900px'>把集团酒店全面预算，从<b>带着一家酒店历史数据的旧表</b>，"
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

P['p01_cover'] = page("P01 · 封面", (
    "<div class='kicker'>集团酒店经营预算 · 空白模板 V1.0</div>"
    "<h1>71 张表 18618 条公式<br><span class='w'>一台</span><em>空白预算引擎</em></h1>"
    "<p class='lede'>把集团酒店全面预算，从<b>带着一家酒店历史数据的旧表</b>，改成<b>任何一家店都能重算的空白模型</b>。"
    "公式链、行号索引、批注与跨表引用关系全部保留，硬编码经营数据全部清空。</p>"
    + kpis([("71", "工作表"), ("18,618", "条公式，一条未删"), ("4 层", "数据流向"), ("0", "残留历史数据")])
    + "<div class='sec'><h2>信息拓扑总览<span class='note'>输入 → 部门 → 分摊 → 汇总 → 谁用</span></h2>"
    + layer("资产底座", "TEMPLATE", BLK,
            blk(BLK, "酒店经营预算模板（空白模板）v1.0",
                "71 张工作表 · 18,618 条计算公式 · 0.8 MB · 打开即重算 · 3 个外部链接处理方式写明"))
    + arrow()
    + layer("四层结构", "4 LAYERS", RED,
            mini([(RED, "输入层 · 7 张", "细分市场与档位月度数据，唯一手填源头"),
                  (ORG, "部门层 · 45 张", "一月至十二月的收入、成本与人工行"),
                  (GRN, "分摊层 · 8 张", "分摊基数与人数，其余公式分摊"),
                  (YEL, "汇总层 · 8＋3 张", "全部公式生成，不得手工修改")], 4))
    + arrow()
    + layer("谁在用", "5 USERS", BLU,
            mini([(BLU, "集团财务金融部", "口径统一与横向对比"), (BLU, "单店财务经理", "不再从零搭表"),
                  (BLU, "酒店总经理", "看得懂经营表"), (BLU, "运营与收益", "单房产出自动成表"),
                  (BLU, "新开业项目组", "直接套模板")], 5))
    + legend([(RED, "输入层 · 唯一手填源头"), (ORG, "部门层 · 填收入成本人工"),
              (GRN, "分摊层 · 填基数与人数"), (YEL, "汇总层 · 全自动"), (BLU, "使用者")])
    + "</div>"
    + "<div class='sec'><h2>三步用起来<span class='note'>从今天到明年</span></h2>"
    + g3([(RED, "STEP 01", "填 7 张输入层", "细分市场模板、宴会市场细分、餐饮收入 —— 全表唯一手填源头。"),
          (ORG, "STEP 02", "填部门层与分摊层", "45 张部门表填收入成本人工，8 张分摊表填基数与人数。"),
          (GRN, "STEP 03", "看汇总层", "Total 汇总表、财务关键指标、国资委快报、三大报表自动生成，一个数不许手改。")])
    + "</div>"
    + "<div class='final'>往下翻：它清了什么 · 四层数据怎么流 · 五步怎么填 · 拿到手怎么开始</div>"
))

P['p02_painpoints'] = page("P02 · 痛点", (
    "<h2>预算编制最贵的不是时间<span class='note'>是返工</span></h2>"
    + "<div class='chain'>"
    + blk(GRY, "<div class='n'>STEP 01</div><div class='t'>旧模板带着一家店的历史数据</div>"
              "<div class='d'>换个店套不上，改一次错一年。<b>40,616 处硬编码</b>成了谁都不敢动的地雷。</div>")
    + "<div class='carrow'></div>"
    + blk(RED, "<div class='n'>STEP 02</div><div class='t'>跨表复制手写，数字对不上</div>"
              "<div class='d'>餐饮收入本该来自餐饮部，却又填了一遍。<b>一处填错，64 张表跟着错。</b></div>")
    + "<div class='carrow'></div>"
    + blk(ORG, "<div class='n'>STEP 03</div><div class='t'>各店口径不一，集团没法比</div>"
              "<div class='d'>出租率、每间可售房收入、人工口径各写各的，<b>汇总表靠人工对齐</b>。</div>")
    + "<div class='carrow'></div>"
    + blk(YEL, "<div class='n'>STEP 04</div><div class='t'>年份写死在公式里</div>"
              "<div class='d'>每到新的一年就重做一遍，<b>复制粘贴当研发</b>；改年份还会误伤行号索引。</div>", dark=True)
    + "</div>"
    + "<div class='sec'><h2>返工成本最后落在哪<span class='note'>六个可见后果</span></h2>"
    + g3([(RED, "01", "跨表错误无人察觉", "餐饮收入重复填一遍，汇总时才发现，此时 64 张表已全部重算。"),
          (RED, "02", "集团比不了店", "各店口径不同，汇总表靠人工对齐，越汇总越不放心。"),
          (ORG, "03", "每年重做一遍", "年份写死在公式里，改一次全表替换，还容易误伤行号索引。"),
          (ORG, "04", "新人不敢动", "历史数据满表都是地雷，没人知道哪个格能改、哪个不能改。"),
          (GRN, "05", "口径靠口口相传", "没有写下来的口径规则，换个人做就换一种算法。"),
          (GRN, "06", "预算与实际脱节", "编制一套、考核另一套，差异说不清是经营问题还是口径问题。")])
    + "</div>"
    + "<div class='sec'><h2>共同根因<span class='note'>四个问题同源</span></h2>"
    + layer("根因", "ROOT CAUSE", BLK,
            mini([(BLK, "数据资产压在结构下面", "真正值钱的是 18,618 条公式与跨表引用关系，但被历史数据盖住看不见。"),
                  (BLK, "口径没有写进表里", "规则活在人的脑子里，没进表，就无法被复用、被交接、被审计。"),
                  (GRY, "填数边界没有标定", "哪些格能填、哪些格是公式，没有硬边界，所以不敢动。"),
                  (GRY, "变更没有参数化", "年份、链接、外部依赖都写死，每次变更都靠人手。")], 2))
    + "</div>"
    + "<div class='sec'><h2>数据资产归位后会发生什么<span class='note'>四个直接变化</span></h2>"
    + g2([(GRN, "变化 01", "编制时间从月级降到周级", "不再搭表、不再对数、不再复制粘贴，只填 7 张输入层。"),
          (GRN, "变化 02", "错误在源头就被拦住", "跨表引用由公式建立，重复填收入会被直接算出来。"),
          (BLU, "变化 03", "集团第一次能横向比店", "统一口径下比较每间可售房收入与营业利润率。"),
          (BLU, "变化 04", "换人也能接着做", "口径写进表与说明，交接即可复用，不依赖个人经验。")])
    + "</div>"
    + note("这六件事都不是设计问题：<b>它们都是数据资产没有归位的表征。</b>"
           "清空历史数据、保留公式链、把口径写进表里、给每个格标明填与不填 —— 这四步做完，上面六条同时消失。")
))

P['p03_topo'] = page("P03 · 信息拓扑图", (
    "<h2>四层数据流向拓扑<span class='note'>从填数到出表，只有一条路</span></h2>"
    + layer("L1 输入层", "7 TABLES", RED,
            blk(RED, "细分市场与餐饮收入 7 张",
                "细分市场模板、宴会市场细分及收入分析、餐饮收入、Rooms Segments 市场细分、Banquet Segment 宴会市场细分")
            + "<div style='font-size:13px;color:#8A3B1E;background:#F6DBDF;border-radius:4px;padding:8px 11px'>"
              "<b>填：</b>各细分市场及档位的月度数据 —— 全表唯一手填源头</div>")
    + arrow()
    + layer("L2 部门层", "45 TABLES", ORG,
            blk(ORG, "房务 · 前厅 · 客房 · 行政楼层 · 餐饮与十一个餐厅 · 宴会 · 市场销售 · 采购 · 行政 · 人力 · 工程",
                "共 45 张标准部门损益表，统一 22 列结构")
            + "<div style='font-size:13px;color:#8A3B1E;background:#FAEBD9;border-radius:4px;padding:8px 11px'>"
              "<b>填：</b>一月至十二月的收入、成本与人工行 —— 收入只填最底层一次，部门之间不得重复填</div>")
    + arrow()
    + layer("L3 分摊层", "8 TABLES", GRN,
            blk(GRN, "餐饮间接费用 · 人工成本及员工人数 · 员餐分摊 · 洗衣房分摊 · 主营业务成本下人工 · 管理费用下人工 · 非经营性费用",
                "把公共成本按业务真实动因摊到各部门")
            + "<div style='font-size:13px;color:#1A5C3B;background:#DDE9E2;border-radius:4px;padding:8px 11px'>"
              "<b>填：</b>分摊基数与人数 —— 其余全部由公式分摊</div>")
    + arrow()
    + layer("L4 汇总层", "8 + 3 TABLES", YEL,
            blk(YEL, "Total 酒店汇总表 · 财务关键指标 · 国资委快报 · 客房餐饮部门利润率 · 餐饮部收入结构分解 · 利润表 · 资产负债表 · 现金流量表",
                "全部由公式生成", dark=True)
            + "<div style='font-size:13px;color:#6B5320;background:#FBF3D6;border-radius:4px;padding:8px 11px'>"
              "<b>不填：</b>任何一个数值都不许手改 —— 手改即失效</div>")
    + arrow()
    + layer("L5 谁在用", "5 USERS", BLU,
            mini([(BLU, "集团财务", "口径与横向对比"), (BLU, "单店财务", "编制不再搭表"),
                  (BLU, "总经理", "读经营表"), (BLU, "运营收益", "单房产出"), (BLU, "新开业", "直接套用")], 5))
    + legend([(RED, "输入层 · 唯一手填源头"), (ORG, "部门层 · 填收入成本人工"),
              (GRN, "分摊层 · 填基数与人数"), (YEL, "汇总层 · 全自动"), (BLU, "使用者")])
    + "<div class='sec'><h2>清洗之后留下的东西<span class='note'>逐项可追溯</span></h2>"
    + g3([(RED, "清空", "40,616 处", "硬编码经营数据，A 列以外无残留"),
          (RED, "清空", "276 处", "伪装成公式的数据"),
          (RED, "剥离", "18,603 处", "公式缓存值，打开即自动重算"),
          (GRN, "保留", "18,618 条", "计算公式，一条未删"),
          (GRN, "保留", "274 个", "行号索引，A 列不得改动"),
          (GRN, "保留", "29 张表", "批注，已完成去数据化")])
    + "</div>"
    + "<div class='final'>填数只在 L1、L2、L3 三层发生，L4 永远不要碰</div>"
))

P['p04_value'] = page("P04 · 价值", (
    "<h2>清掉数据，模型才算数<span class='note'>七个变化</span></h2>"
    + g2([(RED, "01", "数据归零，模型归位", "40,616 处硬编码、276 处伪装成公式的数据一并清空，A 列以外无残留。"),
          (RED, "02", "一条数据链，四层贯通", "输入 → 部门 → 分摊 → 汇总，改最底层一次，全表联动重算。"),
          (ORG, "03", "年份参数化", "XXXX／XXXX-1／XXXX-4 偏移量写法，换目标年度只替换、不重建。"),
          (ORG, "04", "口径写进表里", "40 余张部门损益表共用同一套 22 列结构，A 列中英对照说明已建好。"),
          (GRN, "05", "填数边界清晰", "B 至 M 手填，其余系统带出；汇总层八个表禁止手改。"),
          (GRN, "06", "批注与索引留痕", "29 张表批注完成去数据化，274 个行号索引原样保留。"),
          (BLU, "07", "打开即重算", "18,603 处公式缓存值已剥离；3 个外部链接已给三种处理方式。"),
          (BLK, "结果", "口径统一，横向可比", "集团第一次能拿同一把尺子比所有店：出租率、每间可售房收入、营业利润率，全部自动成表。")])
    + "<div class='sec'><h2>能换来的东西<span class='note'>可量化的部分</span></h2>"
    + g3([(RED, "01", "横向比店第一次成立", "同一把尺子量所有店：出租率、每间可售房收入、营业利润率，自动成表。"),
          (RED, "02", "编制周期显著缩短", "不再从零搭表，填完 7 张输入层，部门与汇总自动带出。"),
          (ORG, "03", "错误在源头暴露", "跨表引用由公式建立，重复填收入会被公式直接看出来。"),
          (ORG, "04", "口径不再靠口传", "22 列结构与填写要求写进使用说明，交接即可复用。"),
          (GRN, "05", "年度切换零成本", "改一处参数，全表跟随，不用逐表替换。"),
          (GRN, "06", "复核有据可查", "29 张表批注保留并去数据化，逐项可追溯。")])
    + "</div>"
    + "<div class='sec'><h2>对三类人最直接<span class='note'>谁拿到的红利最大</span></h2>"
    + g3([(BLU, "集团财务金融部", "口径统一与横向对比", "底座终于有了物理载体，不再靠人工对齐汇总表。"),
          (ORG, "单店财务经理", "不再从零搭表", "重复劳动与跨表对数这两件事直接消失。"),
          (GRN, "酒店总经理", "经营表自己看得懂", "每间可售房收入与人工效率不必再问财务。")])
    + "</div>"
    + "<div class='final'>清掉的是历史数据，留下的是公式链 —— 后者才是能复制、能交接、能跨店复用的资产</div>"
))

P['p05_audience'] = page("P05 · 给谁用", (
    "<h2>五类人会立刻感觉到差别<span class='note'>谁该拿走这份模板</span></h2>"
    + g5([(BLU, "01", "集团财务金融部", "口径统一与横向对比的底座；国资委快报与财务关键指标自动生成。"),
          (ORG, "02", "单店财务经理", "不再从零搭表；细分市场填完，部门表带出，汇总表自动落。"),
          (GRN, "03", "酒店总经理", "看得懂经营表；每间可售房收入、出租率、人均指标不必再问财务。"),
          (RED, "04", "运营与收益团队", "人工成本按人数分摊到部门，人工效率与单房产出自动成表。"),
          (GRY, "05", "新开业项目组", "直接套模板，不用重建历史列；先填一家店也能带出全店口径。")])
    + "<div class='sec'><h2>三个最常见场景<span class='note'>上手即用</span></h2>"
    + g3([(RED, "SCENARIO 01", "明年预算从零编",
           "下载模板 → 改年份参数 → 填 7 张输入层 → 部门层填数 → 汇总自动出。全程不碰历史数据。"),
          (ORG, "SCENARIO 02", "新店开业第一次做预算",
           "直接套模板；先填一家店的输入层与部门表，汇总表会带出全店口径，未填部分为零。"),
          (GRN, "SCENARIO 03", "集团要横向比一遍店",
           "用 Total 汇总表与财务关键指标，统一口径下比较每间可售房收入与营业利润率。")])
    + "</div>"
    + "<div class='sec'><h2>三个上手难点<span class='note'>说明书已提前解决</span></h2>"
    + g3([(RED, "难点 01", "不知道哪些格能填",
            "22 列结构已标明：A 列说明不填、B 至 M 手填、N 至 V 系统带出与计算。"),
          (ORG, "难点 02", "填完数字不对",
            "填写顺序固定五步，且须自下而上排查：输入层 → 部门层 → 分摊层 → 汇总层。"),
          (GRN, "难点 03", "换了年份不会改",
            "XXXX 为本年、XXXX-1 为上年、XXXX-4 为历史基准年，逐表替换且不得动 A 列。")])
    + "</div>"
    + "<div class='sec'><h2>它同时是一份培训教材<span class='note'>十节讲清怎么用</span></h2>"
    + layer("使用说明", "10 SECTIONS", BLK,
            mini([(BLK, "① 基本情况与清洗", "71 张表、18,618 条公式、计量单位"),
                  (BLK, "② 四层结构与职责", "哪层填数、哪层全自动"),
                  (BLK, "③ 22 列结构", "A 列说明、B 至 M 手填"),
                  (BLK, "④ 跨表引用边界", "收入只填最底层一次"),
                  (BLK, "⑤ 五步填写顺序", "顺序错全盘错"),
                  (GRY, "⑥ 各表读法", "Total／关键指标／三表"),
                  (GRY, "⑦ 年度参数规则", "XXXX 偏移量含义"),
                  (GRY, "⑧ 外部链接处理", "重新指向或彻底断开"),
                  (GRY, "⑨ 数据清洗清单", "清了什么、留了什么"),
                  (GRY, "⑩ 注意事项与常见问题", "六类高频问题解答")], 5))
    + "</div>"
    + "<div class='sec'><h2>填数边界一张表<span class='note'>22 列，只有 B 至 M 要手填</span></h2>"
    + layer("列结构", "22 COLUMNS", BLK,
            mini([(BLK, "A　项目说明", "中英文对照，已建好，不填"),
                  (BLK, "B 至 M　十二月", "本年预算，重点填写"),
                  (GRY, "N　全年合计", "系统自动汇总"),
                  (GRY, "O / P　上年实际与预测", "系统带出"),
                  (GRY, "Q　实际加预测", "系统自动计算"),
                  (GRY, "R / S　差异额与差异率", "系统自动计算"),
                  (GRY, "T　历史基准年实际", "系统带出"),
                  (GRY, "U / V　差异额与差异率", "系统自动计算")], 4))
    + "</div>"
    + "<div class='final'>十节说明讲清每张表读什么、哪些列能填、为什么顺序不能错 —— 这比模板本身更难得</div>"
))

P['p06_quotes'] = page("P06 · 关键洞察", (
    "<h2>五句想清楚就不一样的話<span class='note'>来自清洗与使用过程</span></h2>"
    + "<div style='display:flex;flex-direction:column;gap:9px;margin-top:12px'>"
    + ins("01", "「模板不是用来抄的，是用来算的。」", "清空历史数据之后，公式链才第一次露出它的样子。")
    + ins("02", "「真正的数据源只有 7 张表，其余 64 张都是公式。」", "填错源头，全盘皆错；这也是为什么填写顺序不能颠倒。")
    + ins("03", "「在汇总层改一个数，整份预算就不可信了。」", "汇总层的手工修改，是最贵也最隐蔽的错误。")
    + ins("04", "「年份写死一次，明年重做一次。」", "参数化不是偷懒，是把重复劳动一次性归零。")
    + ins("05", "「口径不统一的汇总表，比没有汇总表更危险。」", "可比的底线是对齐，不是加总。")
    + "</div>"
    + "<div class='sec'><h2>五条洞察各指向一个动作<span class='note'>从想到到做到</span></h2>"
    + g3([(RED, "洞察 01 → 动作", "先清数据再谈编制", "把历史数据清空，模型才第一次可用；否则所有讨论都在讨论别人的数。"),
          (RED, "洞察 02 → 动作", "只认 7 张输入层", "其余 64 张都是公式，改它们等于改结论；从源头改一次即可。"),
          (ORG, "洞察 03 → 动作", "汇总层只读不算", "把手工改数的机会彻底关掉，差异才有解释空间。"),
          (ORG, "洞察 04 → 动作", "年份一年一改一次", "参数化替换是十分钟的活，不要拖成一星期的重做。"),
          (GRN, "洞察 05 → 动作", "口径先对齐再汇总", "先统一口径再加总，否则汇总得越快错得越深。"),
          (GRN, "洞察 06 → 动作", "把口径写下来", "口径写进表与说明，才能被复用、被交接、被审计。")])
    + "</div>"
    + "<div class='sec'><h2>三个最容易踩的坑<span class='note'>说明书已提前标注</span></h2>"
    + g3([(RED, "坑 01", "先看汇总层再回头找", "要自下而上排查：输入层 → 部门层 → 分摊层 → 汇总层。"),
          (ORG, "坑 02", "以为没数据是文件坏了", "打开后大量为零或空白是正常的：B 至 M 未填时公式自然算为零。"),
          (GRN, "坑 03", "把年份和行号一起替换", "A 列是行号索引，只替换 XXXX 系列偏移量，A 列不动。")])
    + "</div>"
    + "<div class='final'>这六条共同指向一件事：数据资产要归位，模型才有价值 —— 所以交付是「模板 + 使用说明」两份，不是一份空表</div>"
))

P['p07_delivery'] = page("P07 · 交付物", (
    "<h2>三份东西，直接可用<span class='note'>已随附</span></h2>"
    + layer("交付件", "3 ITEMS", BLU,
            mini([(BLU, "DELIVERABLE 01　附件5 酒店经营预算模板-汇总版（空白模板）v1.0.xlsx",
                   "71 张工作表 · 18,618 条公式 · 4 层数据流向 · 0.8 MB · 打开即重算 · 3 个外部链接处理方式写明"),
                  (BLU, "DELIVERABLE 02　附件5 酒店经营预算模板（空白模板）v1.0_使用说明.docx",
                   "十节正文 · 71 张工作表一览（名称／层级／填数说明）· 22 列填写要求表 · 六类常见问题解答"),
                  (GRN, "DELIVERABLE 03　配套可执行件",
                   "参数化年度替换规则 · 3 个外部链接处理指引 · 29 张表批注清单（已去数据化）· 清洗前后对照")], 1))
    + "<div class='sec'><h2>清洗结果同样可查<span class='note'>逐项可追溯</span></h2>"
    + g3([(RED, "清空", "40,616", "处硬编码经营数据，A 列以外无残留"),
          (RED, "清空", "276", "处伪装成公式的数据"),
          (RED, "剥离", "18,603", "处公式缓存值，打开即自动重算"),
          (GRN, "保留", "18,618", "条计算公式，一条未删"),
          (GRN, "保留", "274", "个行号索引，A 列不得改动"),
          (GRN, "保留", "29", "张表批注，已完成去数据化")])
    + "</div>"
    + "<div class='sec'><h2>拿到手怎么开始<span class='note'>三步</span></h2>"
    + g3([(RED, "STEP 01", "改年份参数", "逐表把 XXXX 替换为目标年，并调整 XXXX-1、XXXX-4 等偏移量；A 列行号索引不得一并替换。"),
          (ORG, "STEP 02", "处理外部链接", "打开若提示更新链接，选不更新；再按需重新指向源工作簿或彻底断开。"),
          (GRN, "STEP 03", "填 7 张输入层", "按五步顺序推进：输入层 → 部门层 → 分摊层 → 核对三表 → 核对汇总。")])
    + "</div>"
    + "<div class='sec'><h2>四条注意事项<span class='note'>说明书第九、十节</span></h2>"
    + g2([(RED, "注意 01", "不得删除列、不得拆分合并单元格", "18,618 条公式依赖既定位置，改位置即改结果。"),
          (RED, "注意 02", "不得修改 A 列", "A 列是 274 个行号索引，是排查错误的坐标。"),
          (ORG, "注意 03", "汇总表不得手工改数值", "汇总层八张表全部自动生成，手改即失效。"),
          (ORG, "注意 04", "注意计量单位不统一", "财务三表以元计，其余汇总表以万元计，跨表核对时须换算。")])
    + "</div>"
    + "<div class='final'>真正的资产不是那张表，是那 18,618 条还在的公式</div>"
))

P['p08_action'] = page("P08 · 行动", (
    "<h2>三个动作<span class='note'>拿走就能用</span></h2>"
    + layer("三步走", "3 ACTIONS", ORG,
            mini([(ORG, "A　集团向：纳入标准动作", "把这份空白模板写进年度预算编制流程，停止各店自建表；口径统一从源头做。"),
                  (GRN, "B　行业向：把方法做成产品", "「空白模板 + 使用说明 + 参数化 + 清洗 SOP」是一整套可复制的方法，同业也需要。"),
                  (BLU, "C　自留：清洗流程固化", "40616 → 0 的这套清洗与校验流程已沉淀，换一个项目即可复用。")], 3))
    + "<div class='sec'><h2>三层分工<span class='note'>谁做什么</span></h2>"
    + g3([(BLK, "集团本部", "定口径与标准", "统一指标定义与模板版本；不介入单店填数，只管口径与规则。"),
          (ORG, "单店与项目公司", "填数与复核", "按五步顺序完成 L1 至 L3 的填数，并在 L4 层复核结果。"),
          (GRN, "产业发展部", "维护模板与培训", "模板版本管理、使用说明更新、新店培训与口径答疑。")])
    + "</div>"
    + "<div class='sec'><h2>时间表<span class='note'>三步走</span></h2>"
    + g3([(RED, "近期", "模板定版与发布", "完成年份参数化与外部链接处理，发布统一版本与使用说明。"),
          (ORG, "中期", "全口径推行", "各店停止自建表，集团汇总口径统一到这套模板。"),
          (GRN, "远期", "沉淀为产品", "把清洗与校验流程固化，与标准产品包一并对外输出。")])
    + "</div>"
    + "<div class='sec'><h2>四个提醒<span class='note'>别踩这些坑</span></h2>"
    + g2([(RED, "提醒 01", "不要在汇总层改数", "这是最贵也最隐蔽的错误。"),
          (RED, "提醒 02", "不要跳过输入层", "7 张表不填，后面全部为零，不是错，是没数据。"),
          (ORG, "提醒 03", "不要改 A 列", "行号索引是排查坐标。"),
          (ORG, "提醒 04", "不要先看汇总层", "要自下而上排查，否则永远找不到源头。")])
    + "</div>"
    + note("如果你正在做下一年的预算：<b>先填 7 张输入层表，再往下走。</b>顺序错了，后面 64 张表的数字都不作数。")
    + "<div class='cta'><div class='big'>评论区扣 1<br>私信领取完整工作表一览</div>"
    "<div class='sm'><div class='l'>SAVE</div><div class='v'>先收藏</div></div></div>"
))

P['p09_summary'] = page("P09 · 全景", (
    "<h2>一张图收尾<span class='note'>这套模板到底改变了什么</span></h2>"
    + layer("改前", "BEFORE", GRY,
            mini([(GRY, "带着一家店的历史数据", "40,616 处硬编码，谁都不敢动"),
                  (GRY, "跨表手写、一处错全盘错", "口径散在每个人的 Excel 里"),
                  (GRY, "年份写死，每年重做一遍", "复制粘贴当研发")], 3))
    + arrow()
    + layer("改后", "AFTER", RED,
            mini([(RED, "数据归零，模型归位", "18,618 条公式全链路贯通"),
                  (GRN, "四层分工，口径统一", "输入 7 张 → 部门 45 → 分摊 8 → 汇总 11"),
                  (BLU, "参数化年份，可复制", "口径卡与产品包可移交他人复用")], 3))
    + "<div class='sec'><h2>四个使用建议<span class='note'>上手前先记住</span></h2>"
    + g2([(RED, "建议 01", "只填三层", "L1 输入、L2 部门、L3 分摊；L4 汇总永远只读。"),
          (RED, "建议 02", "按顺序走", "五步顺序不可颠倒，自下而上排查。"),
          (ORG, "建议 03", "先改参数再填数", "年份与外部链接先处理，避免返工。"),
          (ORG, "建议 04", "口径问题问说明", "十节说明已覆盖六类高频问题。")])
    + "</div>"
    + "<div class='sec'><h2>四个提醒<span class='note'>别踩这些坑</span></h2>"
    + g2([(RED, "提醒 01", "不要在汇总层改数", "这是最贵也最隐蔽的错误。"),
          (RED, "提醒 02", "不要跳过输入层", "7 张表不填，后面全部为零，不是错，是没数据。"),
          (ORG, "提醒 03", "不要改 A 列", "行号索引是排查坐标。"),
          (ORG, "提醒 04", "不要先看汇总层", "要自下而上排查，否则永远找不到源头。")])
    + "</div>"
    + legend([(GRY, "改前 · 数据资产被压住"), (RED, "改后 · 模型归位"), (GRN, "改后 · 口径统一"), (BLU, "改后 · 可复制")])
    + "<div class='final'>真正的资产不是那张表，是那 18,618 条还在的公式 —— 模板可以被复制，公式链复制一次就长期有效</div>"
    + "<div class='cta'><div class='big'>评论区扣 1<br>私信领取完整工作表一览</div>"
    "<div class='sm'><div class='l'>SAVE</div><div class='v'>先收藏</div></div></div>"
))


_REN = [('p00_title', 'P01 · 标题封面'), ('p01_cover', 'P02 · 信息拓扑总览'),
        ('p02_painpoints', 'P03 · 痛点'), ('p03_topo', 'P04 · 信息拓扑图'),
        ('p04_value', 'P05 · 价值'), ('p05_audience', 'P06 · 给谁用'),
        ('p06_quotes', 'P07 · 关键洞察'), ('p07_delivery', 'P08 · 交付物'),
        ('p08_action', 'P09 · 行动'), ('p09_summary', 'P10 · 全景')]
for _k, _m in _REN:
    if _k in P:
        P[_k] = re.sub(r'<div class=.meta.>[^<]*</div>',
                       "<div class='meta'>" + _m + "</div>", P[_k], count=1)

BAD = ["微信", "加微信", "加我", "扫码", "扫一扫", "二维码", "支付宝", "抖音", "微博", "私域", "引流", "企业开票", "1对 1", "1对1"]
hits = [(k, b) for k, v in P.items() for b in BAD if b in v]
for k, v in P.items():
    o = len(re.findall(r'<div\b', v))
    c = len(re.findall(r'</div>', v))
    if o != c:
        print("  !! 标签不配平 " + k + ": 开" + str(o) + " 闭" + str(c))
    open(os.path.join(HTMLD, k + ".html"), "w", encoding="utf-8", newline="\n").write(v)
print("HTML written:", len(P))
print("R29 forbidden:", hits if hits else "none")
