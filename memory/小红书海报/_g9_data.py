# -*- coding: utf-8 -*-
"""9图内容 v2 — 酒店分级分类 全维度覆盖"""

PAGES = []

PAGES.append(dict(
  kicker="HOTEL GRADING & CLASSIFICATION · 9 图",
  title='酒店分级分类<br>一张图看懂 <span class="hl">6 套语言</span>同时在说话',
  sub="政府国标 · 国别体系 · 集团分级 · 品牌层级 · 数据机构 · 渠道与消费者<br>再加一个最常被混谈的：信用评级",
  body="""<div class="card acc">
  <div class="t">这 6 套语言，没有一套能翻译成另一套</div>
  <div class="stack" style="margin-top:10px">
    <div class="tier"><div class="no">1</div><div class="tx"><div class="h">政府 / 国标</div>
      <div class="p">中国大陆 GB/T 14308 · 港澳台各一套 · 唯一有法律效力的一套</div></div></div>
    <div class="tier"><div class="no">2</div><div class="tx"><div class="h">国别体系</div>
      <div class="p">法国 5 类 + Palace · 英国 4 星 · 美国 5 星 · 日本无国标 · 印度 OYO</div></div></div>
    <div class="tier"><div class="no">3</div><div class="tx"><div class="h">集团分级</div>
      <div class="p">华住 · 锦江 · 首旅 · 亚朵 · 雅高 · 万豪 —— 各画各的档位线</div></div></div>
    <div class="tier"><div class="no">4</div><div class="tx"><div class="h">集团内品牌层级</div>
      <div class="p">希尔顿 6 档 · IHG 4 档 · 万豪 / 凯悦 / 雅高各有自己的阶梯</div></div></div>
    <div class="tier"><div class="no">5</div><div class="tx"><div class="h">数据机构分级</div>
      <div class="p">STR Brand Scale · 米其林 · Forbes —— 按数据口径，不按行政</div></div></div>
    <div class="tier"><div class="no">6</div><div class="tx"><div class="h">渠道商与消费者</div>
      <div class="p">携程特牌金牌 · 飞猪钻级 · 途家优选严选臻选 · TripAdvisor 气泡</div></div></div>
  </div>
</div>
<div class="card soft">
  <div class="t">还有一个常被混进来的</div>
  <div class="d"><b>信用评级</b>（S&amp;P Global / Fitch）评的是酒店集团的<b>还债能力</b>，不是酒店好不好住。<br>2025-03-31 标普把米其林长期评级从 A- 上调到 A —— 这是公司信用，不是酒店星级。</div>
</div>""",
  foot_q="这期讲清 <b>6 套语言 + 1 个伪相关</b>",
  foot_s="GB/T 14308-2023 · 中国饭店协会 · HKTB · 澳门旅游局 · 台湾观光局 · Atout France · STR · 米其林 · Forbes · 携程/飞猪/途家/同程/美团 · TripAdvisor"
))

PAGES.append(dict(
  kicker="00 · 为什么这事比想的复杂",
  title='消费者选酒店，<br>实际只过 <span class="hl">三道关</span>',
  sub="每道关背后都站着一套互不通约的分级语言 —— 这就是行业最拧巴的地方",
  body="""<div class="card acc">
  <div class="t">第一关 · 预算档位<span class="tag">我在哪个价格带</span></div>
  <div class="d">要判断一家酒店"贵不贵、值不值"。<br>依据可以是 <b>星级</b>（政府/国别）、<b>集团档次线</b>、<b>STR Brand Scale</b>、<b>携程特牌金牌</b> —— 四种语言可能给出四个答案。</div>
</div>
<div class="card">
  <div class="t">第二关 · 品牌认知<span class="tag">我认哪个牌子</span></div>
  <div class="d">同一个集团里，<b>希尔顿</b>（欢朋→康莱德→希尔顿）、<b>IHG</b>（假日→智选→假日精选）各自是一条阶梯。<br>消费者认的是<b>品牌层级</b>，不是国家的五颗星。</div>
</div>
<div class="card">
  <div class="t">第三关 · 口碑确认<span class="tag">别人怎么说</span></div>
  <div class="d">看 <b>TripAdvisor 气泡</b>（现已改为四舍五入到 0.1）、<b>Booking</b> 评分、<b>携程/美团</b> 分档评价 —— 全是<b>消费端数据</b>，与前面的行政标准毫无关系。</div>
</div>
<div class="card soft">
  <div class="d" style="font-size:18.5px;color:#1c1917">所以"这家酒店是什么档次"这个问题，<b>行业里从来没有唯一答案</b>。<br>能回答的只有两类人：<b>出标准的人</b>，和<b>懂多套标准的人</b>。</div>
</div>""",
))

PAGES.append(dict(
  kicker="01 · 层级一 · 政府与国标（大陆）",
  title='唯一有法律效力的一套：<br><span class="hl">GB/T 14308</span>',
  sub="很多人记成 21030 —— 正确的是 14308",
  body="""<div class="tl">
  <div class="tlrow"><div class="yr">1993</div><div class="tx">
    <div class="h">首版《旅游饭店星级划分》</div>
    <div class="p">五星制建立，硬件标准为主：建筑面积、设备、装修。</div></div></div>
  <div class="tlrow"><div class="yr">2001<br>2003</div><div class="tx">
    <div class="h">两次修订</div>
    <div class="p">补齐细分业态，调整星级门槛与服务项目。</div></div></div>
  <div class="tlrow"><div class="yr">2010 版</div><div class="tx">
    <div class="h">GB/T 14308-2010（2011-01 实施）</div>
    <div class="p">长期使用的版本，行业习惯称"国标"。</div></div></div>
  <div class="tlrow"><div class="yr">2023 版</div><div class="tx">
    <div class="h">GB/T 14308-2023（2024-03-01 实施）</div>
    <div class="p">四个方向：<b>新发展理念 · 实用 · 减轻企业负担 · 科学评价方法</b>，强化服务质量监管。</div></div></div>
</div>
<div class="card acc">
  <div class="t">协会在同一张表上补位</div>
  <div class="kv"><span class="k">一星</span><span class="v a">900 – 1000 分</span></div>
  <div class="kv"><span class="k">二星</span><span class="v a">800 – 900 分</span></div>
  <div class="kv"><span class="k">三星</span><span class="v a">700 – 800 分</span></div>
  <div class="d" style="margin-top:9px">中国饭店协会 · 另有 T/CHA 030-2023《住宿服务质量分级与"领航者"评价要求》。</div>
</div>
<div class="card soft">
  <div class="t">但中间夹着一个空白</div>
  <div class="d">精品民宿、非标生活方式酒店、单一主题住宿 —— <b>星级体系装不下，协会分级又不等于品牌等级</b>。</div>
</div>""",
))

PAGES.append(dict(
  kicker="01 · 层级一 · 港澳台三地",
  title='同一片中文市场，<br><span class="hl">三套评级逻辑</span>',
  sub="这是最容易被跳过、也最能说明问题的部分",
  body="""<div class="row2">
  <div class="card">
    <div class="t">香港<span class="tag">不透明</span></div>
    <div class="d">香港旅游发展局（HKTB）评级，<b>四类</b>：<br>甲级高价酒店（≈5–6 星）· 乙级高价（≈4 星）· 中价 · 旅客宾馆<br><br>五项指标：设施 · 位置 · 员工与客房比 · 实际房价 · 客源结构<br><br><b>名单不公开</b> —— 只通知个别酒店。</div>
  </div>
  <div class="card">
    <div class="t">澳门<span class="tag">官方定期评</span></div>
    <div class="d">特区政府旅游局评定，<b>五类</b>：<br>五星豪华 · 五星 · 四星 · 三星 · 二星<br>公寓另分三星 / 二星<br><br>依据设施与服务<b>定期更新</b>。<br>2016 年为 74 家酒店 + 31 家公寓。</div>
  </div>
</div>
<div class="card acc">
  <div class="t">台湾<span class="tag">申报 + 专家评</span></div>
  <div class="d">交通部观光局（体系参考美国 AAA），<b>六级</b>：一至五星 + <b>卓越五星级</b>。<br>
  评核五项：住宿品质 · 服务 · 清洁 · 安全 · 卫生<br>
  须提交：营业许可证 · 保险单 · 安全检查报告<br>
  由专任专家评定，不定期检视调整。</div>
</div>
<div class="card soft">
  <div class="d" style="font-size:18px;color:#1c1917">三句话记住：<b>香港 = 不透明</b>｜<b>澳门 = 官方定期评</b>｜<b>台湾 = 申报 + 专家评</b></div>
</div>""",
))

PAGES.append(dict(
  kicker="02 · 层级二 · 集团分级",
  title='集团自己画档位线，<br><span class="hl">四家中国巨头四种打法</span>',
  sub="集团分级决定了一个品牌被放进哪个价格带，也决定了它跟业主怎么分账",
  body="""<div class="row2">
  <div class="card"><div class="t">华住<span class="tag">全谱系</span></div>
    <div class="d">覆盖<b>经济到高端最广</b>；核心城市高流量<b>直营</b> + 特许标准化输出，结构均衡。<br>汉庭 → 全季 → 桔子 → 高端线，一条完整阶梯。</div></div>
  <div class="card"><div class="t">锦江<span class="tag">全服务偏重</span></div>
    <div class="d">全服务酒店占比高，带来<b>效率瓶颈</b>：单店产出与规模不匹配。<br>旗下 12 万+ 间客房，是国内规模第一。</div></div>
  <div class="card"><div class="t">亚朵<span class="tag">中高端商旅</span></div>
    <div class="d">聚焦<b>中高端商旅</b>；产品迭代提升溢价，<b>零售业务</b>拉高非房费收入，单店收入结构更健康。</div></div>
  <div class="card"><div class="t">首旅如家<span class="tag">存量深耕</span></div>
    <div class="d">依托如家系的存量基础做规模；2026H1 直营 RevPAR 290.10 元 <b>+3.89%</b>、净利 <b>+54.04%</b> —— 存量效率改善的样本。</div></div>
</div>
<div class="card acc">
  <div class="t">国际集团也各画各的</div>
  <div class="d">万豪（St. Regis / Ritz-Carlton 起）· 希尔顿（6 档）· IHG（4 档）· 雅高（Raffles 起）· 凯悦（生活方式与在地文化）· 温德姆 · 万豪中国。<br><b>同一个"高端"，每家的起点都不一样</b> —— 这就是集团分级与行政星级对不上的原因。</div>
</div>
<div class="card soft">
  <div class="d">业主最关心的是另一件事：<b>集团把品牌放哪个价格带，决定了它跟业主怎么谈管理费、怎么分客源渠道</b>。</div>
</div>""",
))

PAGES.append(dict(
  kicker="03 · 层级三 · 集团内品牌层级",
  title='消费者真正认的<br><span class="hl">是这条阶梯</span>',
  sub="同一个集团内部，自己切一刀：从入门到顶奢，每一档住着完全不同的人",
  body="""<div class="card">
  <div class="t">希尔顿 · 6 档<span class="tag">最细的一套</span></div>
  <div class="d">Luxury（Waldorf Astoria · Conrad · Curio）· Upper Upscale（Canopy · Signia · Hilton）· Upscale（DoubleTree · Tapestry · <b>希尔顿花园</b>）· Upper Midscale（Hampton · Home2）· Midscale（Tru）· Select（Courtyard · Fairfield by Marriott）</div>
</div>
<div class="card">
  <div class="t">IHG · 4 档</div>
  <div class="d">Luxury &amp; Lifestyle（洲际 · Kimpton · Regent）· Premium（Westin · Renaissance · Le Méridien）· Select（Aloft · AC Hotels · Moxy）· Mainstream（<b>假日酒店</b> · Holiday Inn Express）</div>
</div>
<div class="row3">
  <div class="g3c"><div class="k">MARRIOTT</div><div class="v">Luxury</div>
    <div class="d">St. Regis · The Ritz-Carlton<br>下设 <b>Classic</b> 与 <b>Distinctive</b> 两个子类 —— 同一档里再切一刀。</div></div>
  <div class="g3c"><div class="k">HYATT</div><div class="v">生活方式</div>
    <div class="d">Park Hyatt · Andaz<br>强调<b>设计感与在地文化</b>，不按传统奢华分。</div></div>
  <div class="g3c acc"><div class="k">ACCOR</div><div class="v">双头</div>
    <div class="d">Raffles · Banyan Tree<br>从<b>传统奢华</b>一路到<b>生活方式奢华</b>。</div></div>
</div>
<div class="card soft">
  <div class="d">规律：<b>越老的集团越按硬件分档，越年轻的越按生活方式分档</b>。这是品牌层级与行政星级永远对不上的根源。</div>
</div>""",
))

PAGES.append(dict(
  kicker="04 · 层级四 · 数据机构分级",
  title='不看你几颗星，<br>看你 <span class="hl">ADR 在哪一档</span>',
  sub="STR 的 Brand Scale 是全球最通行的商业口径 —— 它按数据分，不按行政分",
  body="""<div class="card acc">
  <div class="t">STR Brand Scale · 按上年全系统平均 ADR 分 6 档</div>
  <div class="d" style="margin-top:8px">Luxury → Upper Upscale → Upscale → Upper Midscale → Midscale → Economy<br>独立物业单列（Independent），与加盟体系分开。</div>
</div>
<div class="card">
  <div class="t">STR 的另两个口径</div>
  <div class="kv"><span class="k">Class</span><span class="v">给独立物业按地区定档</span></div>
  <div class="kv"><span class="k">STAR Report</span><span class="v">OCC / ADR / RevPAR 对标竞争组</span></div>
  <div class="d" style="margin-top:9px">投资者和业主真正在用的是这一套 —— <b>有竞争组、有同口径、有时间序列</b>，星级反而不是。</div>
</div>
<div class="row2">
  <div class="card"><div class="t">米其林指南<span class="tag">1–3 星 + 钥匙</span></div>
    <div class="d">评的是<b>餐饮与住宿体验</b>：食材品质 · 厨师技巧 · 料理个性 · 物有所值 · 一致性。<br>餐厅用星或餐盘符号，酒店用钥匙（2024 推出）。</div></div>
  <div class="card"><div class="t">Forbes Travel Guide<span class="tag">5 星</span></div>
    <div class="d">独立于星级体系的另一套 5 星评估，与米其林口径不同、<b>不可互换</b>。<br>日本无国家酒店星级制，这套就承担了阶梯功能。</div></div>
</div>
<div class="card soft" style="border-color:#a05f26;border-width:1.5px;background:#fdfaf4">
  <div class="t">别把这两个混成一件事</div>
  <div class="d"><b>STR / 米其林 / Forbes 评的是酒店</b>；<b>S&amp;P Global / Fitch 评的是集团能不能还债</b>。<br>2025-03-31 标普把米其林长期评级从 A- 上调至 A、展望稳定 —— 那是公司信用，不是酒店星级。</div>
</div>""",
))

PAGES.append(dict(
  kicker="05 · 层级五 · 渠道商与消费者",
  title='你最终看到的那层分级，<br><span class="hl">是平台定的</span>',
  sub="离消费者最近的一套语言，却几乎从不出现在行业报告里",
  body="""<div class="row2">
  <div class="card"><div class="t">携程<span class="tag">特牌 / 金牌 / 无牌</span></div>
    <div class="d">对商家的标签体系，直接影响<b>流量与定价策略</b>。</div></div>
  <div class="card"><div class="t">飞猪<span class="tag">钻级</span></div>
    <div class="d">按<b>钻</b>分档的商家分级。</div></div>
  <div class="card"><div class="t">途家<span class="tag">优选 / 严选 / 臻选</span></div>
    <div class="d">民宿侧的<b>三层</b>筛选体系。</div></div>
  <div class="card"><div class="t">同程 / 美团<span class="tag">月评 / 运营评估</span></div>
    <div class="d">同程<b>每月</b>评估；美团是综合<b>运营评估体系</b>。</div></div>
</div>
<div class="card acc">
  <div class="t">消费者端 · TripAdvisor 气泡评分</div>
  <div class="d">已改为<b>四舍五入到 0.1</b>（3.8 / 4.2）而不再取 0.5 整（3.0 / 4.5）；<b>计算方法不变，只影响显示值、不影响排名</b>。另有 Travelers' Choice Awards。</div>
</div>
<div class="card soft">
  <div class="t">一个正在发生的变量</div>
  <div class="d">这些平台正因<b>营销与定价算法</b>可能构成不公平行为，被市场监管机构调查。<br>渠道分级一旦被动摇，商户侧的曝光与定价会立刻重排。</div>
</div>""",
))

PAGES.append(dict(
  kicker="06 · 存量时代怎么办",
  title='分级分类的真问题，<br>从来不是<span class="hl">几颗星</span>',
  sub="而是存量时代，怎么给「没有星、也不想被当没星」的资产一个坐标",
  body="""<div class="card acc">
  <div class="t">三个正在失效的假设</div>
  <div class="d"><b>① 星级评的是"新建时什么样"</b> —— 存量改造、换牌、业态重组之后，这套语言直接失效。<br><b>② 消费端与行政端脱节</b> —— 消费者按"有没有星"决策，业主按"哪个牌子"决策，两套语言各说各话。<br><b>③ 集团分级对外不可见</b> —— 真正决定档位线的那条线，是集团内部画的。</div>
</div>
<div class="row2">
  <div class="card"><div class="t">可能的解法一<span class="tag">维度化</span></div>
    <div class="d">从一条线变一张网：<b>等级 × 品类 × 品质</b>。<br>用 <b>可归因的经营数据</b>（RevPAR / 单店产出 / 复购）而非建筑与装修，给存量资产定坐标。</div></div>
  <div class="card"><div class="t">可能的解法二<span class="tag">多标签</span></div>
    <div class="d">承认一个酒店同时是"中高端""康养""文化主题""宠物友好"。<br>用<b>标签组</b>替代单颗星，让非标与精品第一次进入可比坐标。</div></div>
</div>
<div class="card">
  <div class="t">真正的分水岭</div>
  <div class="d" style="font-size:18px;color:#1c1917">谁先定义新坐标，谁就定义下一轮酒店业的<b>定价权</b> —— 不是定义星级，是定义"什么值得被多付钱"。</div>
</div>""",
))