# -*- coding: utf-8 -*-
"""重写 p03/p05/p09 为平衡结构（只用 helper）+ 补足 p02/p05/p06/p09 填充"""
import io, os, re, sys, subprocess
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

MK = r'D:\B166ER-openclaw\workspace\toolbox\_mk_xhs9_light.py'
t = open(MK, encoding='utf-8').read()

# ---------- 1) 新增 helper：两栏（左说明 + 右主体）、四张小卡 ----------
HELPERS = '''
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

'''
ANCH_HELP = "def layer(label, en, color, body):"
if "_def side(" not in t:
    t = t.replace(ANCH_HELP, HELPERS.strip("\n") + "\n\n" + ANCH_HELP, 1)
    print('helper 已加：side() / mini()')

# ---------- 2) 替换 p03 ----------
P03_NEW = '''P['p03_topo'] = page("P03 · 信息拓扑图", (
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
'''

# ---------- 3) 替换 p05 ----------
P05_NEW = '''P['p05_audience'] = page("P05 · 给谁用", (
    "<h2>五类人会立刻感觉到差别<span class='note'>谁该拿走这份模板</span></h2>"
    + g5([("#257DD4", "01", "集团财务金融部", "口径统一与横向对比的底座；国资委快报与财务关键指标自动生成。", "读：L4 汇总层"),
          ("#E1820D", "02", "单店财务经理", "不再从零搭表；细分市场填完，部门表带出，汇总表自动落。", "填：L1 + L2"),
          ("#277549", "03", "酒店总经理", "看得懂经营表；每间可售房收入、出租率、人均指标不必再问财务。", "读：Total 汇总表"),
          ("#CA1D39", "04", "运营与收益团队", "人工成本按人数分摊到部门，人工效率与单房产出自动成表。", "填：L3 分摊层"),
          ("#A3A3A3", "05", "新开业项目组", "直接套模板，不用重建历史列；先填一家店也能带出全店口径。", "填：L1 起步")])
    + "<div class='sec'><h2>三个最常见场景<span class='note'>上手即用</span></h2>"
    + g3([("#CA1D39", "SCENARIO 01", "明年预算从零编",
           "下载模板 → 改年份参数 → 填 7 张输入层 → 部门层填数 → 汇总自动出。全程不碰历史数据。"),
          ("#E1820D", "SCENARIO 02", "新店开业第一次做预算",
           "直接套模板；先填一家店的输入层与部门表，汇总表会带出全店口径，未填部分为零。"),
          ("#277549", "SCENARIO 03", "集团要横向比一遍店",
           "用 Total 汇总表与财务关键指标，统一口径下比较每间可售房收入与营业利润率。")])
    + "</div>"
    + "<div class='sec'><h2>三个上手难点<span class='note'>说明书已提前解决</span></h2>"
    + g3([("#CA1D39", "难点 01", "不知道哪些格能填",
            "22 列结构已标明：A 列说明不填、B 至 M 手填、N 至 V 系统带出与计算。"),
           ("#E1820D", "难点 02", "填完数字不对",
            "填写顺序固定五步，且须自下而上排查：输入层 → 部门层 → 分摊层 → 汇总层。"),
           ("#277549", "难点 03", "换了年份不会改",
            "XXXX 为本年、XXXX-1 为上年、XXXX-4 为历史基准年，逐表替换且不得动 A 列。")])
    + "</div>"
    + "<div class='sec'><h2>它同时是一份培训教材<span class='note'>十节讲清怎么用</span></h2>"
    + layer("使用说明", "10 SECTIONS", "#1A1A1A",
            mini([("#1A1A1A", "① 基本情况与清洗", "71 张表、18,618 条公式、计量单位"),
                  ("#1A1A1A", "② 四层结构与职责", "哪层填数、哪层全自动"),
                  ("#1A1A1A", "③ 22 列结构", "A 列说明、B 至 M 手填"),
                  ("#1A1A1A", "④ 跨表引用边界", "收入只填最底层一次"),
                  ("#1A1A1A", "⑤ 五步填写顺序", "顺序错全盘错"),
                  ("#5A5A5A", "⑥ 各表读法", "Total／关键指标／三表"),
                  ("#5A5A5A", "⑦ 年度参数规则", "XXXX 偏移量含义"),
                  ("#5A5A5A", "⑧ 外部链接处理", "重新指向或彻底断开"),
                  ("#5A5A5A", "⑨ 数据清洗清单", "清了什么、留了什么"),
                  ("#5A5A5A", "⑩ 注意事项与常见问题", "六类高频问题解答")], 5))
    + "</div>"
    + "<div class='final'>十节说明讲清每张表读什么、哪些列能填、为什么顺序不能错 —— 这比模板本身更难得</div>"
))
'''

# ---------- 4) 替换 p09 ----------
P09_NEW = '''P['p09_summary'] = page("P09 · 全景", (
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
    + g2([("#CA1D39", "建议 01", "只填三层", "L1 输入、L2 部门、L3 分摊；L4 汇总永远只读。"),
          ("#CA1D39", "建议 02", "按顺序走", "五步顺序不可颠倒，自下而上排查。"),
          ("#E1820D", "建议 03", "先改参数再填数", "年份与外部链接先处理，避免返工。"),
          ("#E1820D", "建议 04", "口径问题问说明", "十节说明已覆盖六类高频问题。")])
    + "</div>"
    + "<div class='sec'><h2>四个提醒<span class='note'>别踩这些坑</span></h2>"
    + g2([("#CA1D39", "提醒 01", "不要在汇总层改数", "这是最贵也最隐蔽的错误。"),
          ("#CA1D39", "提醒 02", "不要跳过输入层", "7 张表不填，后面全部为零，不是错，是没数据。"),
          ("#E1820D", "提醒 03", "不要改 A 列", "行号索引是排查坐标。"),
          ("#E1820D", "提醒 04", "不要先看汇总层", "要自下而上排查，否则永远找不到源头。")])
    + "</div>"
    + legend([(GRY, "改前 · 数据资产被压住"), (RED, "改后 · 模型归位"), (GRN, "改后 · 口径统一"), (BLU, "改后 · 可复制")])
    + "<div class='final'>真正的资产不是那张表，是那 18,618 条还在的公式 —— 模板可以被复制，公式链复制一次就长期有效</div>"
    + "<div class='cta'><div class='big'>评论区扣 1<br>私信领取完整工作表一览</div>"
    "<div class='sm'><div class='l'>SAVE</div><div class='v'>先收藏</div></div></div>"
))
'''

for key, new in (("p03_topo", P03_NEW), ("p05_audience", P05_NEW), ("p09_summary", P09_NEW)):
    s0 = t.find("P['%s'] = page(" % key)
    if s0 < 0:
        print('!! 未找到 ' + key); continue
    s1 = t.find("\n\nP['", s0)
    if s1 < 0:
        s1 = t.find("\n\nfor _k in list(P.keys()):", s0)
    t = t[:s0] + new.strip("\n") + t[s1:]
    print('已重写 ' + key)

# ---------- 5) 给 p02 / p06 补填充 ----------
EXTRA_ADD = '''
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
'''
ANCH_E = "\nfor _k in list(P.keys()):"
if "E.setdefault('p02_painpoints'" not in t:
    t = t.replace(ANCH_E, EXTRA_ADD + ANCH_E, 1)
    print('已加 p02 / p06 补充区块')

open(MK, 'w', encoding='utf-8').write(t)
print('写入完成')

r = subprocess.run([sys.executable, MK], capture_output=True, text=True, encoding='utf-8', errors='replace')
print(r.stdout[-1200:])
if r.stderr:
    print('STDERR:', r.stderr[-600:])

RD = r'D:\B166ER-openclaw\workspace\toolbox\_render_xhs9.py'
r2 = subprocess.run([sys.executable, RD], capture_output=True, text=True, encoding='utf-8', errors='replace')
print(r2.stdout)
if r2.stderr:
    print('STDERR:', r2.stderr[-600:])
