# -*- coding: utf-8 -*-
"""收尾：p03 改纯拓扑（消除溢出），p01/p02/p04/p05 补足填充"""
import io, os, re, sys, subprocess
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

MK = r'D:\B166ER-openclaw\workspace\toolbox\_mk_xhs9_v3.py'
t = open(MK, encoding='utf-8').read()

# ---------- p03 改为纯拓扑 ----------
s0 = t.find("P['p03_topo'] = page(")
s1 = t.find("\n\nP['p04_value']", s0)
if s0 < 0 or s1 < 0:
    print('!! p03 定位失败'); sys.exit(1)

P03 = '''P['p03_topo'] = page("P03 · 信息拓扑图", (
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
'''
t = t[:s0] + P03.strip("\n") + t[s1:]
print('p03 已改为纯拓扑')

# ---------- p01 补内容 ----------
OLD1 = """    + "<div class='final'>往下翻：它清了什么 · 四层数据怎么流 · 五步怎么填 · 拿到手怎么开始</div>"
))"""
NEW1 = """    + "<div class='sec'><h2>三步用起来<span class='note'>从今天到明年</span></h2>"
    + g3([(RED, "STEP 01", "填 7 张输入层", "细分市场模板、宴会市场细分、餐饮收入 —— 全表唯一手填源头。"),
          (ORG, "STEP 02", "填部门层与分摊层", "45 张部门表填收入成本人工，8 张分摊表填基数与人数。"),
          (GRN, "STEP 03", "看汇总层", "Total 汇总表、财务关键指标、国资委快报、三大报表自动生成，一个数不许手改。")])
    + "</div>"
    + "<div class='final'>往下翻：它清了什么 · 四层数据怎么流 · 五步怎么填 · 拿到手怎么开始</div>"
))"""
if OLD1 in t:
    t = t.replace(OLD1, NEW1, 1); print('p01 已补内容')
else:
    print('!! p01 锚点未命中')

# ---------- p02 补内容 ----------
OLD2 = """    + note("这六件事都不是设计问题：<b>它们都是数据资产没有归位的表征。</b>\""""
NEW2 = """    + "<div class='sec'><h2>数据资产归位后会发生什么<span class='note'>四个直接变化</span></h2>"
    + g2([(GRN, "变化 01", "编制时间从月级降到周级", "不再搭表、不再对数、不再复制粘贴，只填 7 张输入层。"),
          (GRN, "变化 02", "错误在源头就被拦住", "跨表引用由公式建立，重复填收入会被直接算出来。"),
          (BLU, "变化 03", "集团第一次能横向比店", "统一口径下比较每间可售房收入与营业利润率。"),
          (BLU, "变化 04", "换人也能接着做", "口径写进表与说明，交接即可复用，不依赖个人经验。")])
    + "</div>"
    + note("这六件事都不是设计问题：<b>它们都是数据资产没有归位的表征。</b>\""""
if OLD2 in t:
    t = t.replace(OLD2, NEW2, 1); print('p02 已补内容')
else:
    print('!! p02 锚点未命中')

# ---------- p04 补内容 ----------
OLD4 = """    + "<div class='final'>清掉的是历史数据，留下的是公式链 —— 后者才是能复制、能交接、能跨店复用的资产</div>"
))"""
NEW4 = """    + "<div class='sec'><h2>对三类人最直接<span class='note'>谁拿到的红利最大</span></h2>"
    + g3([(BLU, "集团财务金融部", "口径统一与横向对比", "底座终于有了物理载体，不再靠人工对齐汇总表。"),
          (ORG, "单店财务经理", "不再从零搭表", "重复劳动与跨表对数这两件事直接消失。"),
          (GRN, "酒店总经理", "经营表自己看得懂", "每间可售房收入与人工效率不必再问财务。")])
    + "</div>"
    + "<div class='final'>清掉的是历史数据，留下的是公式链 —— 后者才是能复制、能交接、能跨店复用的资产</div>"
))"""
if OLD4 in t:
    t = t.replace(OLD4, NEW4, 1); print('p04 已补内容')
else:
    print('!! p04 锚点未命中')

# ---------- p05 补内容 ----------
OLD5 = """    + "<div class='final'>十节说明讲清每张表读什么、哪些列能填、为什么顺序不能错 —— 这比模板本身更难得</div>"
))"""
NEW5 = """    + "<div class='sec'><h2>填数边界一张表<span class='note'>22 列，只有 B 至 M 要手填</span></h2>"
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
))"""
if OLD5 in t:
    t = t.replace(OLD5, NEW5, 1); print('p05 已补内容')
else:
    print('!! p05 锚点未命中')

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
