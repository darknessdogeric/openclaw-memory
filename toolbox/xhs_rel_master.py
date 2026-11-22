# -*- coding: utf-8 -*-
"""关系经济落幕 · 小红书多图研报笔记 9 图 (geo_v4 纯白规格, 现象观察类)"""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BOX = Path(r"D:\B166ER-openclaw\workspace\toolbox")
_g = (BOX / "geo_v4_mckinsey.py").read_text(encoding="utf-8")
COMMON_CSS = _g.split('COMMON_CSS = """', 1)[1].split('"""', 1)[0]

OUT_DIR = r"D:\B166ER-openclaw\workspace\output\xhs_rel_2026-11-01"
TOTAL = 9
ISSUE = "2026.11.01 · ISSUE NO.001"
SOURCE = "SOURCE: B166ER · 关系与新经济观察"

SLIDE_01 = """
<div>
  <div class="eyebrow">EXECUTIVE BRIEFING · 摘要</div>
  <h1>关系经济<br/><span class="red">正在落幕</span></h1>
  <div class="accent-bar"></div>
  <div style="font-size: 28px; color: #5A6B7D; margin-top: 26px; font-style: italic; line-height: 1.55;">
    当技术迭代周期被压缩到几个月，<br/>
    人情 —— 这张最后的底牌 —— 就失效了。
  </div>
</div>
<div class="data-callout">
  <div class="label">WHEN THE CYCLE COMPRESSES</div>
  <div class="value">4-6<span class="unit">个月 · 大模型迭代周期</span></div>
  <div class="note">架构切换已从 18 个月压缩到 6 个月。替代方案的刷新速度，决定了旧解法的折旧速度。</div>
</div>
<div class="three-col">
  <div class="col">
    <div class="col-num">01 · 旧解法</div>
    <div class="col-title">靠人</div>
    <div class="col-body">信任来自人，信息藏在人手里，扩张靠人脉。</div>
    <div class="col-stat">关系经济</div>
  </div>
  <div class="col">
    <div class="col-num">02 · 新解法</div>
    <div class="col-title">靠标准</div>
    <div class="col-body">信任写进代码，验证由系统完成，扩张靠边际成本。</div>
    <div class="col-stat">新经济关系</div>
  </div>
  <div class="col muted">
    <div class="col-num">03 · 净结果</div>
    <div class="col-title">关系只剩成本</div>
    <div class="col-body">协调成本被技术打到零的同时，关系创造的价值也归零。</div>
    <div class="col-stat">单向碾压</div>
  </div>
</div>
"""

SLIDE_02 = """
<div>
  <div class="eyebrow">01 · THE PHENOMENON</div>
  <h2>它不是坏习惯<br/>是<span class="red">前技术时代的最优解</span></h2>
  <div class="accent-bar"></div>
</div>
<div class="body-text">
  在不确定性无法被定价的世界里，关系是最便宜的协调装置。它的全部价值来自一句话 —— <b>我无法验证你，所以我信你</b>。
</div>
<table class="editorial">
  <tr><th>维度</th><th>关系经济的做法</th><th>它真正的功能</th></tr>
  <tr><td>信任来源</td><td>找熟人、找担保人</td><td>用关系替代验证</td></tr>
  <tr><td>信息位置</td><td>信息藏在人情与暗示里</td><td>把隐性信息锁死在关系里</td></tr>
  <tr><td>扩张方式</td><td>复制人脉与身位</td><td>把网络当资本来放大</td></tr>
  <tr><td>组织形态</td><td>公司是关系网的容器</td><td>让关系可以被继承与调度</td></tr>
</table>
<div class="pullquote">
  关系经济从来不是道德问题，是<b>信息技术的时滞问题</b>。
</div>
<div style="border-left: 8px solid #C8102E; padding: 24px 30px; background: #FDF3F4;">
  <div style="font-size: 26px; color: #0A2540; line-height: 1.55;">
    它在一个<b>无法验证</b>的世界里是最优解 —— 用一个无法验证的世界继续运行，必然被碾压。
  </div>
</div>
"""

SLIDE_03 = """
<div>
  <div class="eyebrow">02 · THE CORE PROBLEM</div>
  <h2>两条腿同时踩断<br/>关系<span class="red">不再是最优解</span></h2>
  <div class="accent-bar"></div>
</div>
<div class="body-text">
  一边是技术迭代时间被指数级压缩，另一边是信任与验证被基础设施接管。两件事各自都足以让关系经济失去存在理由。
</div>
<div class="three-col">
  <div class="col">
    <div class="col-num">01 · 时间压缩</div>
    <div class="col-title">迭代周期 4-6 个月</div>
    <div class="col-body">架构切换从 18 个月压到 6 个月。靠人维系的关系，需要时间才能沉淀成习惯 —— 而替代方案每几个月就刷新一次。</div>
    <div class="col-stat">旧解法跑不到下一代</div>
  </div>
  <div class="col">
    <div class="col-num">02 · 信任基础设施</div>
    <div class="col-title">验证比信任便宜</div>
    <div class="col-body">条件支付把资金释放与履约条件绑定；平台评级把信誉变成可查询、可比价的记录。</div>
    <div class="col-stat">担保被规则替代</div>
  </div>
  <div class="col">
    <div class="col-num">03 · 组织被替代</div>
    <div class="col-title">一人公司 36.3%</div>
    <div class="col-body">2026 年新设公司中由单个人创立的比重。AI Agent 让一个人跑通原本需要一整家公司的流程。</div>
    <div class="col-stat">公司不再是关系的容器</div>
  </div>
</div>
<div class="data-callout">
  <div class="label">THE ASYMMETRY</div>
  <div class="value">18 &rarr; 6</div>
  <div class="note">架构切换周期的压缩（单位：月）。技术每快一倍，旧关系资产的折旧期就短一半。</div>
</div>
"""

SLIDE_04 = """
<div>
  <div class="eyebrow">03 · THE MECHANISM</div>
  <h2>信任正在从<span class="red">人身上</span><br/>转移到<span class="red">代码里</span></h2>
  <div class="accent-bar"></div>
</div>
<table class="editorial">
  <tr><th>旧信任</th><th>新信任</th><th>关键变化</th></tr>
  <tr><td>口头承诺 + 人情担保</td><td>条件支付 + 履约绑定</td><td>资金释放与履约条件绑定，验证即时可查</td></tr>
  <tr><td>找熟人打听</td><td>平台评级与信用记录</td><td>信誉成为可查询、可比价的资产</td></tr>
  <tr><td>靠关系压价</td><td>算法与供需直连</td><td>议价权交给数据，不再交给人情</td></tr>
  <tr><td>凭感觉判断对方</td><td>Agent 编排与自动执行</td><td>判断从人的经验变成系统的规则</td></tr>
</table>
<div class="pullquote">
  互联网的价值链正在从「流量分发」转向「任务解决」—— 入口不再属于人，属于 Agent。
</div>
<div class="dark-callout">
  <div class="label">KEY INSIGHT</div>
  <div class="body">
    不是人变得不重要了，是<span class="red-text">「验证一个人」这件事的成本归零了</span>。<br/>
    关系曾经是验证的替代品；现在验证本身变便宜，关系的剩余价值就归零，<br/>
    剩下的只有维系成本 —— 这就是它看起来<b>愚昧</b>的全部原因。
  </div>
</div>
"""

SLIDE_05 = """
<div>
  <div class="eyebrow">04 · THE RISE</div>
  <h2>新经济体的<span class="red">四个形态</span></h2>
  <div class="accent-bar"></div>
</div>
<div class="three-col">
  <div class="col">
    <div class="col-num">01 · 一人公司</div>
    <div class="col-title">36.3%</div>
    <div class="col-body">2026 年新设公司中由单个人创立的比重（2019 年 23.7%，六年增长 53%）。AI Agent 让一个人跑通采购、运营、销售、客服。</div>
    <div class="col-stat">新华网 · 2026.07</div>
  </div>
  <div class="col">
    <div class="col-num">02 · 平台化个体</div>
    <div class="col-title">+14.7%</div>
    <div class="col-body">2025 年平台网店经营的个体工商户同比增速。线上线下融合，不再依赖渠道与关系网，直接对接需求。</div>
    <div class="col-stat">存量个体的形态升级</div>
  </div>
  <div class="col">
    <div class="col-num">03 · AI 原生组织</div>
    <div class="col-title">数字员工</div>
    <div class="col-body">AI 从工具进化为可感知、规划、执行、反思的自主数字员工，并开始重构业务流程本身。</div>
    <div class="col-stat">组织边界外扩</div>
  </div>
</div>
<div class="data-callout">
  <div class="label">THE NEW BASE</div>
  <div class="value">1.6<span class="unit">亿户 · 2025 年新设个体工商户</div>
  <div class="note">其中「新经济、新业态、新模式、新动能」个体工商户 4010 万户，连续五年增长；存活三年以上 8420 万户，占 65.8%。</div>
</div>
"""

SLIDE_06 = """
<div>
  <div class="eyebrow">05 · THE DISAPPEARANCE</div>
  <h2>正在消失的<span class="red">四类东西</span></h2>
  <div class="accent-bar"></div>
</div>
<table class="editorial">
  <tr><th>旧实体</th><th>为什么活不下去</th><th>替代它的是什么</th></tr>
  <tr><td>二级批发代理</td><td>终端需求直接拉货，层级不再必要</td><td>推式转拉式的扁平供应链</td></tr>
  <tr><td>熟人融资中介</td><td>信用可查，评分与抵押替代担保</td><td>数据化风控</td></tr>
  <tr><td>关系型渠道商</td><td>平台与算法直连，流量不再靠身位</td><td>平台化供给</td></tr>
  <tr><td>人情型担保</td><td>法律责任与执行成本被写进规则</td><td>可执行合约 + 条件支付</td></tr>
</table>
<div class="pullquote">
  旧经济体不是被攻击，是被<b>绕过</b>。
</div>
<div style="border-left: 8px solid #C8102E; padding: 24px 30px; background: #FDF3F4;">
  <div style="font-size: 26px; color: #0A2540; line-height: 1.55;">
    它们没有犯错，只是<b>失去了存在理由</b> —— 而失去理由，比犯错更彻底。
  </div>
</div>
"""

SLIDE_07 = """
<div>
  <div class="eyebrow">06 · THE CONTRAST</div>
  <h2>四个维度上<br/>这是一场<span class="red">单向碾压</span></h2>
  <div class="accent-bar"></div>
</div>
<table class="editorial">
  <tr><th>维度</th><th>关系经济</th><th>新经济关系</th><th>结果</th></tr>
  <tr><td>信任来源</td><td>人</td><td>系统与代码</td><td>不可验证的一方出局</td></tr>
  <tr><td>决策依据</td><td>人情与暗示</td><td>数据与模型</td><td>经验不再构成优势</td></tr>
  <tr><td>扩张速度</td><td>一个人际网络的速度</td><td>边际成本趋零</td><td>规模效应反转</td></tr>
  <tr><td>退出成本</td><td>关系带不走，资产随人走</td><td>代码与数据可迁移</td><td>组织本身成为负担</td></tr>
</table>
<div class="dark-callout">
  <div class="label">WHY IT CANNOT FIGHT BACK</div>
  <div class="body">
    旧关系的四个优势维度，被技术逐一替换。<br/>
    更关键的是，它<b>没有还手能力</b> —— 因为它的全部优势，<br/>
    都建立在「对方无法被验证」这件事上。
  </div>
</div>
"""

SLIDE_08 = """
<div>
  <div class="eyebrow">07 · THE TREND</div>
  <h2>落幕不是一天<br/>是<span class="red">三段</span></h2>
  <div class="accent-bar"></div>
</div>
<ol class="editorial">
  <li><b>替代期</b> —— 新形态先在边缘长出来，旧关系仍在主干。平台网店个体户同比 +14.7%、「四新」个体户 4010 万户连续五年增长，都是这个阶段的表征。</li>
  <li><b>挤压期</b> —— 新形态成本低于旧形态，价格战开始。渠道扁平化推式转拉式，层级被一层层削掉。</li>
  <li><b>清算期</b> —— 旧实体不是倒闭，是不再被需要。存活个体户里，靠关系的那部分先被挤出。</li>
</ol>
<div class="data-callout">
  <div class="label">THE DEPRECIATION CLOCK</div>
  <div class="value">4-6<span class="unit">个月 · 一代关系资产的折旧期</div>
  <div class="note">技术迭代周期每压缩一次，清算期就提前一段。依赖关系建立的资产，其有效期正在以「迭代周期」为单位缩短。</div>
</div>
"""

SLIDE_09 = """
<div>
  <div class="eyebrow">08 · THE TAKEAWAY</div>
  <h2>关系不会消失<br/>它只会<span class="red">只剩成本</span></h2>
  <div class="accent-bar"></div>
</div>
<div class="dark-callout">
  <div class="label">CORE LAW</div>
  <div class="body">
    关系的价值 ＝ 它节省的验证成本 － 它自身的维系成本。<br/>
    当验证成本被技术打到零，关系的净价值<span class="red-text">只剩负数</span>。
  </div>
</div>
<div class="pullquote">
  曾经稀缺的是「可靠的人」；<br/>
  现在稀缺的是「<b>可验证的系统</b>」。
</div>
<div style="background: #F2F4F7; padding: 26px 32px;">
  <div style="font-size: 15px; color: #5A6B7D; letter-spacing: 4px; margin-bottom: 10px;">FORWARD LOOK</div>
  <div style="font-size: 26px; color: #0A2540; line-height: 1.55;">
    交易成本经济学 · 演化生物学 · 平台经济学 · AI Agent<br/>
    从「关系的收益」看「关系的成本」，是一个新范式。
  </div>
</div>
<div style="font-size: 21px; color: #5A6B7D; line-height: 1.6;">
  <span style="color: #C8102E; font-weight: 700;">DISCUSSION</span>
  如果你的生意建立在关系上 —— 这本笔记是提醒你：关系的折旧期，比你以为的短得多。
</div>
"""

SLIDES = [SLIDE_01, SLIDE_02, SLIDE_03, SLIDE_04, SLIDE_05, SLIDE_06, SLIDE_07, SLIDE_08, SLIDE_09]
