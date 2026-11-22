# -*- coding: utf-8 -*-
"""生物层面的危险 · 小红书多图研报笔记 6 图 (geo_v4 纯白规格, 现象观察类)"""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BOX = Path(r"D:\B166ER-openclaw\workspace\toolbox")
_g = (BOX / "geo_v4_mckinsey.py").read_text(encoding="utf-8")
COMMON_CSS = _g.split('COMMON_CSS = """', 1)[1].split('"""', 1)[0]

OUT_DIR = r"D:\B166ER-openclaw\workspace\output\xhs_bio_2026-11-01"
TOTAL = 6
ISSUE = "2026.11.01 · ISSUE NO.001"
SOURCE = "SOURCE: B166ER · 演化机制观察"

SLIDE_01 = """
<div>
  <div class="eyebrow">EXECUTIVE BRIEFING · 摘要</div>
  <h1>生物层面的<br/><span class="red">危险</span>在哪里</h1>
  <div class="accent-bar"></div>
  <div style="font-size: 28px; color: #5A6B7D; margin-top: 26px; font-style: italic; line-height: 1.55;">
    人类（以及大多数社会性哺乳动物）的动机系统、社会行为、意义建构，<br/>
    是在漫长的稀缺与竞争环境中进化出来的。
  </div>
</div>
<div class="data-callout">
  <div class="label">WHEN THE FUEL RUNS OUT</div>
  <div class="value">4</div>
  <div class="note">四个塌陷：动机塌陷 / 社会病理放大 / 繁殖与代际传递受挫 / 意义真空</div>
</div>
<div class="three-col">
  <div class="col">
    <div class="col-num">01 · 进化背景</div>
    <div class="col-title">稀缺与竞争</div>
    <div class="col-body">生存压力、地位竞争、资源不确定，长期塑造了我们的行为系统。</div>
    <div class="col-stat">不是设计，是筛选</div>
  </div>
  <div class="col">
    <div class="col-num">02 · 生理机制</div>
    <div class="col-title">三条回路</div>
    <div class="col-body">多巴胺奖励回路 · 催产素信任机制 · 皮质醇压力反应。</div>
    <div class="col-stat">外加地位与合作策略</div>
  </div>
  <div class="col muted">
    <div class="col-num">03 · 触发点</div>
    <div class="col-title">极大满足</div>
    <div class="col-body">基本需求几乎无成本满足、生存焦虑大幅消退。</div>
    <div class="col-stat">核心燃料开始失效</div>
  </div>
</div>
"""

SLIDE_02 = """
<div>
  <div class="eyebrow">01 · THE PHENOMENON</div>
  <h2>我们不是被设计成<br/>在丰裕中生活的</h2>
  <div class="accent-bar"></div>
</div>
<div class="body-text">
  生存压力、地位竞争、资源不确定，长期塑造了我们的多巴胺奖励回路、催产素信任机制、皮质醇压力反应，以及复杂的地位与合作策略。
</div>
<table class="editorial">
  <tr><th>机制</th><th>在稀缺中扮演的角色</th><th>在丰裕中变成</th></tr>
  <tr><td>多巴胺<br/>奖励回路</td><td>驱动延迟满足与长期投入</td><td>动机塌陷 —— 转向即时快感</td></tr>
  <tr><td>催产素<br/>信任机制</td><td>让合作与结群得以维系</td><td>关系退化为圈层与身份竞争</td></tr>
  <tr><td>皮质醇<br/>压力反应</td><td>威胁之下动员资源</td><td>长期压力与焦虑</td></tr>
  <tr><td>地位与<br/>合作策略</td><td>在竞争中排序与结盟</td><td>纯零和的符号竞争</td></tr>
</table>
<div style="border-left: 8px solid #C8102E; padding: 24px 30px; background: #FDF3F4;">
  <div style="font-size: 26px; color: #0A2540; line-height: 1.55;">
    同一套机制，在极端稀缺下是<b>适应力</b>；在极大满足下，反而变成<b>负担</b>。
  </div>
</div>
"""

SLIDE_03 = """
<div>
  <div class="eyebrow">02 · THE FRAMEWORK</div>
  <h2>当物质条件接近<span class="red">「极大满足」</span><br/>核心燃料开始失效</h2>
  <div class="accent-bar"></div>
</div>
<div class="body-text">
  基本需求几乎无成本地被满足、生存焦虑大幅消退时 —— 原先驱动行为的核心燃料开始失效。
</div>
<div class="data-callout">
  <div class="label">WHAT WAS REMOVED</div>
  <div class="value">0</div>
  <div class="note">剩余的稀缺压力 —— 而驱动系统仍按匮乏期的方式运行。抽掉的不是资源，是燃料本身。</div>
</div>
<div class="pullquote">
  匮乏期塑造出来的行为系统，不会因为条件变好而自动切换到另一种模式。
</div>
<div class="dark-callout">
  <div class="label">KEY INSIGHT</div>
  <div class="body">
    这不是道德问题，也不是分配问题 —— 是<span class="red-text">生物层面</span>的时滞问题：<br/>
    造物的环境已经变了，被造出来的东西还没变。
  </div>
</div>
"""

SLIDE_04 = """
<div>
  <div class="eyebrow">03 · THE FOUR FAILURES</div>
  <h2>燃料失效后的<br/><span class="red">四个塌陷</span></h2>
  <div class="accent-bar"></div>
</div>
<table class="editorial">
  <tr><th>塌陷</th><th>机制</th><th>表现</th></tr>
  <tr><td>动机塌陷</td><td>努力、延迟满足、长期规划的进化价值下降</td><td>转向即时快感、低投入娱乐，或者彻底退缩</td></tr>
  <tr><td>社会病理放大</td><td>地位竞争从争夺生存资源转向纯零和符号竞争</td><td>身份、话语权、审美优越感 —— 更尖锐，也更虚无</td></tr>
  <tr><td>繁殖与代际传递受挫</td><td>生育意愿与育儿能力崩溃</td><td>Universe 25 的鼠群；现实高福利社会的低生育率</td></tr>
  <tr><td>意义真空</td><td>必须自己生成「为什么活」的答案</td><td>焦虑、抑郁、成瘾或意识形态狂热</td></tr>
</table>
<div class="pullquote">
  绝大多数人并没有现成的精神资源去填补这个真空 —— 于是容易陷入焦虑、抑郁、成瘾或意识形态狂热。
</div>
"""

SLIDE_05 = """
<div>
  <div class="eyebrow">04 · THE IMPLICATION</div>
  <h2>稀缺不只是残忍<br/>它还是<span class="red">秩序</span></h2>
  <div class="accent-bar"></div>
</div>
<ol class="editorial">
  <li>稀缺塑造的机制<b>不会因为条件变好而消失</b> —— 多巴胺、催产素、皮质醇是按匮乏环境被筛选出来的。</li>
  <li>燃料失效<b>不会自动带来升维</b> —— 没有稀缺这根脚手架，系统失去的是可预期的行为约束。</li>
  <li>繁殖与代际传递是<b>最先崩的一环</b> —— Universe 25 里鼠群停止繁殖；现实中的低生育率是同一逻辑的现代表现。</li>
</ol>
<div class="dark-callout">
  <div class="label">UNDERLYING CAUSE</div>
  <div class="body">
    稀缺是残酷的，但它也是人类行为秩序的<b>重要脚手架</b>。<br/>
    彻底抽掉这根脚手架，系统<b>不一定会自动升维</b>，更可能先经历失稳甚至坍塌。
  </div>
</div>
"""

SLIDE_06 = """
<div>
  <div class="eyebrow">05 · THE TAKEAWAY</div>
  <h2>抽掉脚手架之后<br/>剩下的<span class="red">不会自动升级</span></h2>
  <div class="accent-bar"></div>
</div>
<div class="dark-callout">
  <div class="label">CORE LAW</div>
  <div class="body">
    稀缺是残酷的，但它也是人类行为秩序的<b>重要脚手架</b>。<br/>
    脚手架拆掉之后，剩下的结构<span class="red-text">不会自动升级</span> ——<br/>
    它只会在原地失稳，甚至坍塌。
  </div>
</div>
<div class="pullquote">
  所以真正的问题不是「消除稀缺」，<br/>
  而是「在消除稀缺的同时，用什么替代它提供约束」。
</div>
<div style="background: #F2F4F7; padding: 26px 32px;">
  <div style="font-size: 15px; color: #5A6B7D; letter-spacing: 4px; margin-bottom: 10px;">FORWARD LOOK</div>
  <div style="font-size: 26px; color: #0A2540; line-height: 1.55;">
    演化心理学 · 行为经济学 · 稀缺心理学<br/>
    从「造物环境」看「被造出来的东西」，而不是从道德劝诫看它。
  </div>
</div>
<div style="font-size: 21px; color: #5A6B7D; line-height: 1.6;">
  <span style="color: #C8102E; font-weight: 700;">DISCUSSION</span>
  如果你正在设计一个「让所有人都不再稀缺」的方案 —— 这本笔记是写给你的。
</div>
"""

SLIDES = [SLIDE_01, SLIDE_02, SLIDE_03, SLIDE_04, SLIDE_05, SLIDE_06]
