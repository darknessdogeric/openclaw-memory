"""AHL · 小红书 12 图 · R34 麦肯锡 + 美联储 + 摩根 风格重制版
完全按 R34 规则定稿：白底 + 深蓝 #0A2540 + 红 #C8102E + 思源宋体 + 大量留白
封面 + 5 段内容 + 收口 节奏（这里扩到 7 张精炼版，避免信息过载）
"""
# ===========================================================================
# COMMON_CSS (R34 V4 字号体系已验证)
# ===========================================================================
COMMON_CSS = """
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: "Source Han Serif SC", "Noto Serif CJK SC", "Songti SC", "SimSun", serif;
    background: #F5F1E8;
    -webkit-font-smoothing: antialiased;
    color: #0A2540;
  }
  .slide {
    width: 1080px;
    height: 1440px;
    position: relative;
    background: #F5F1E8;
    overflow: hidden;
    padding: 90px 70px;
  }
  /* 顶部 masthead */
  .masthead {
    position: absolute;
    top: 50px; left: 70px; right: 70px;
    display: flex; justify-content: space-between; align-items: center;
    font-size: 14px;
    letter-spacing: 4px;
    color: #0A2540;
    font-weight: 700;
  }
  .masthead .brand { font-weight: 800; }
  .masthead .meta { color: #8A8F9B; letter-spacing: 3px; font-weight: 500; }
  .masthead-rule {
    position: absolute;
    top: 88px; left: 70px; right: 70px;
    border-top: 1px solid #0A2540;
  }
  /* 底部 footer */
  .footer {
    position: absolute;
    bottom: 50px; left: 70px; right: 70px;
    display: flex; justify-content: space-between; align-items: flex-end;
    font-size: 12px;
    color: #8A8F9B;
    letter-spacing: 2px;
  }
  .footer-rule {
    position: absolute;
    bottom: 88px; left: 70px; right: 70px;
    border-top: 1px solid #D6CFC0;
  }
  .footer .source { font-weight: 500; }
  .footer .version { font-size: 10px; color: #C8102E; font-weight: 700; letter-spacing: 3px; }
  .footer .page { font-size: 18px; color: #0A2540; font-weight: 700; letter-spacing: 2px; }
  /* 内容区 */
  .content {
    position: absolute;
    top: 130px; left: 70px; right: 70px; bottom: 130px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  /* eyebrow */
  .eyebrow {
    font-size: 14px;
    letter-spacing: 6px;
    color: #C8102E;
    font-weight: 700;
    margin-bottom: 16px;
  }
  /* h1 */
  h1 {
    font-size: 88px;
    font-weight: 800;
    line-height: 1.1;
    color: #0A2540;
    letter-spacing: 4px;
    margin-bottom: 16px;
  }
  h1 .accent { color: #C8102E; }
  /* h2 */
  h2 {
    font-size: 56px;
    font-weight: 800;
    line-height: 1.2;
    color: #0A2540;
    letter-spacing: 3px;
    margin-bottom: 24px;
  }
  /* 正文 */
  .body-text {
    font-size: 28px;
    line-height: 1.7;
    color: #2D3F5A;
    letter-spacing: 1px;
    font-weight: 400;
  }
  .body-text strong { color: #C8102E; font-weight: 700; }
  .body-text em { font-style: italic; color: #0A2540; font-weight: 600; }
  /* pull quote */
  .pull-quote {
    font-size: 36px;
    line-height: 1.5;
    color: #0A2540;
    font-style: italic;
    font-weight: 500;
    padding: 32px 0;
    border-top: 2px solid #C8102E;
    border-bottom: 2px solid #C8102E;
    letter-spacing: 2px;
    margin: 32px 0;
  }
  /* data callout */
  .data-callout {
    text-align: center;
    padding: 30px 0;
    margin: 24px 0;
  }
  .data-callout .value {
    font-size: 200px;
    font-weight: 900;
    color: #C8102E;
    line-height: 1;
    letter-spacing: 4px;
  }
  .data-callout .unit {
    font-size: 28px;
    color: #0A2540;
    letter-spacing: 4px;
    margin-top: 8px;
    font-weight: 600;
  }
  /* 红条批注 */
  .red-bar {
    border-left: 6px solid #C8102E;
    padding: 16px 24px;
    margin: 20px 0;
    background: rgba(200, 16, 46, 0.04);
  }
  .red-bar .bar-text {
    font-size: 24px;
    line-height: 1.6;
    color: #0A2540;
    font-weight: 500;
  }
  .red-bar .bar-text strong { color: #C8102E; font-weight: 800; }
  /* 表格 */
  table.editorial {
    width: 100%;
    border-collapse: collapse;
    margin: 24px 0;
  }
  table.editorial td {
    padding: 14px 0;
    font-size: 24px;
    color: #0A2540;
    border-bottom: 1px solid #D6CFC0;
    letter-spacing: 1px;
    vertical-align: top;
  }
  table.editorial td:first-child {
    font-weight: 800;
    color: #C8102E;
    width: 80px;
  }
  table.editorial td.concl {
    color: #8A8F9B;
    font-style: italic;
    text-align: right;
    border-bottom: none;
    padding-top: 28px;
  }
  /* 黑底 callout */
  .dark-callout {
    background: #0A2540;
    color: #F5F1E8;
    padding: 40px 36px;
    margin: 24px 0;
    border-radius: 0;
  }
  .dark-callout .dc-title {
    font-size: 16px;
    letter-spacing: 6px;
    color: #C8102E;
    font-weight: 800;
    margin-bottom: 16px;
  }
  .dark-callout .dc-body {
    font-size: 28px;
    line-height: 1.6;
    color: #F5F1E8;
    font-weight: 500;
  }
  .dark-callout .dc-body strong { color: #C8102E; }
  /* 三栏 audience */
  .audience-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 20px;
    margin: 24px 0;
  }
  .aud-cell {
    padding: 24px 18px;
    background: #FFFFFF;
    border: 1px solid #D6CFC0;
  }
  .aud-cell .aud-num {
    font-size: 36px;
    font-weight: 900;
    color: #C8102E;
    margin-bottom: 8px;
    letter-spacing: 2px;
  }
  .aud-cell .aud-name {
    font-size: 22px;
    font-weight: 700;
    color: #0A2540;
    margin-bottom: 6px;
    letter-spacing: 2px;
  }
  .aud-cell .aud-desc {
    font-size: 18px;
    line-height: 1.5;
    color: #5A6578;
    letter-spacing: 1px;
  }
  /* 编号列表 */
  ol.editorial {
    counter-reset: editorial;
    list-style: none;
    margin: 24px 0;
    padding: 0;
  }
  ol.editorial li {
    counter-increment: editorial;
    padding: 18px 0 18px 70px;
    position: relative;
    border-bottom: 1px solid #D6CFC0;
    font-size: 26px;
    line-height: 1.5;
    color: #0A2540;
  }
  ol.editorial li:last-child { border-bottom: none; }
  ol.editorial li::before {
    content: counter(editorial, decimal-leading-zero);
    position: absolute;
    left: 0; top: 18px;
    font-size: 32px;
    font-weight: 900;
    color: #C8102E;
    letter-spacing: 2px;
  }
  ol.editorial li strong { color: #C8102E; font-weight: 800; }
  /* CTA black */
  .core-law {
    background: #0A2540;
    color: #F5F1E8;
    padding: 50px 40px;
    text-align: center;
    margin: 32px 0;
  }
  .core-law .cl-eyebrow {
    font-size: 14px;
    letter-spacing: 6px;
    color: #C8102E;
    font-weight: 700;
    margin-bottom: 20px;
  }
  .core-law .cl-title {
    font-size: 48px;
    line-height: 1.4;
    color: #F5F1E8;
    font-weight: 800;
    letter-spacing: 4px;
  }
  .core-law .cl-title strong { color: #C8102E; }
  /* 删除线对比 */
  .del-vs {
    font-size: 36px;
    line-height: 1.7;
    color: #0A2540;
    margin: 24px 0;
    text-align: center;
    font-weight: 600;
    letter-spacing: 3px;
  }
  .del-vs .old {
    text-decoration: line-through;
    color: #8A8F9B;
    margin-right: 16px;
  }
  .del-vs .new {
    color: #C8102E;
    font-weight: 800;
    margin-left: 16px;
  }
  /* FORWARD LOOK */
  .forward-look {
    font-size: 22px;
    line-height: 1.7;
    color: #5A6578;
    font-style: italic;
    padding: 20px 24px;
    border-left: 3px solid #0A2540;
    margin: 20px 0;
    letter-spacing: 1px;
  }
  /* 公式 */
  .formula {
    text-align: center;
    padding: 36px 0;
    margin: 24px 0;
  }
  .formula .f-text {
    font-size: 72px;
    font-weight: 800;
    letter-spacing: 4px;
    color: #0A2540;
    line-height: 1.1;
    white-space: nowrap;
  }
  .formula .f-text .eq { color: #C8102E; margin: 0 20px; font-weight: 900; }
  .formula .f-sub {
    font-size: 18px;
    color: #8A8F9B;
    letter-spacing: 6px;
    margin-top: 16px;
    font-weight: 500;
  }
"""

# ===========================================================================
# SLIDE 01 — 封面
# ===========================================================================
SLIDE_01 = """
  <div>
    <div class="eyebrow">EXECUTIVE BRIEFING · 2026.08.22</div>
    <h1>酒店业的<br><span class="accent">AI 革命</span></h1>
    <div class="body-text" style="margin-top: 24px;">
      AHL 同构双矩阵范式 · 范式四阶 · TOKEN 经济
    </div>
  </div>
  <div>
    <div class="formula">
      <div class="f-text">单店<span class="eq">＝</span>集团<span class="eq">＝</span>文旅</div>
      <div class="f-sub">FRACTAL ARCHITECTURE · 同一种解法</div>
    </div>
    <div class="red-bar">
      <div class="bar-text">
        <strong>3 个失败方案</strong> + <strong>1 个真正的答案</strong> + <strong>5 个支撑</strong>
      </div>
    </div>
  </div>
"""

# ===========================================================================
# SLIDE 02 — 现象 / 痛点
# ===========================================================================
SLIDE_02 = """
  <div>
    <div class="eyebrow">01 · THE PHENOMENON</div>
    <h2>酒店行业<br>卡在哪里？</h2>
  </div>
  <div>
    <table class="editorial">
      <tr><td>01</td><td><strong>头部集团</strong> 重资产·规模大·效率低·创新慢</td></tr>
      <tr><td>02</td><td><strong>单体酒店</strong> 缺流量·缺数据·缺 AI 能力</td></tr>
      <tr><td>03</td><td><strong>AI 浪潮</strong> DeepSeek / 豆包帮不了酒店本身</td></tr>
      <tr><td>04</td><td><strong>抽水经济</strong> OTA 抽佣 15-25%，价值被中介拿走</td></tr>
      <tr><td colspan="2" class="concl">∴ 酒店需要怎样的 AI 能力？</td></tr>
    </table>
  </div>
"""

# ===========================================================================
# SLIDE 03 — 失败方案 / 真正的答案
# ===========================================================================
SLIDE_03 = """
  <div>
    <div class="eyebrow">02 · THE FAILURES</div>
    <h2>3 个失败方案<br>+ 1 个真正的答案</h2>
  </div>
  <div>
    <div class="del-vs">
      <span class="old">App</span>
      <span class="old">SaaS</span>
      <span class="old">AI 入口</span>
    </div>
    <div class="data-callout">
      <div class="value">双</div>
      <div class="unit">AGENT 矩阵范式 · 真正的答案</div>
    </div>
    <div class="pull-quote">
      客人 Agent ↔ 商家 Agent 直接握手<br>
      AHL 只做<em>协议层</em>，不做撮合
    </div>
  </div>
"""

# ===========================================================================
# SLIDE 04 — 范式四阶
# ===========================================================================
SLIDE_04 = """
  <div>
    <div class="eyebrow">03 · THE FRAMEWORK</div>
    <h2>范式四阶<br>价值锚一路迁移</h2>
  </div>
  <div>
    <table class="editorial">
      <tr><td>1</td><td><strong>货架经济</strong> · 价值锚：位置 · 抽水者：房东</td></tr>
      <tr><td>2</td><td><strong>匹配经济</strong> · 价值锚：算法 · 抽水者：OTA</td></tr>
      <tr><td>3</td><td><strong>直接经济</strong> · 价值锚：协议 · 抽水者：无</td></tr>
      <tr><td>4</td><td><strong>TOKEN 经济</strong> · 价值锚：算力 · AHL 在此</td></tr>
      <tr><td colspan="2" class="concl">位置 → 算法 → 协议 → 算力</td></tr>
    </table>
    <div class="red-bar">
      <div class="bar-text">
        AHL = <strong>协议层</strong> + <strong>TOKEN 计量器</strong>
      </div>
    </div>
  </div>
"""

# ===========================================================================
# SLIDE 05 — TOKEN = *** 时代的电费
# ===========================================================================
SLIDE_05 = """
  <div>
    <div class="eyebrow">04 · THE TOKEN ANALOGY</div>
    <h2>TOKEN 是<br>Agent 时代的电费</h2>
  </div>
  <div>
    <table class="editorial">
      <tr><td>成本</td><td>电费（度） ⇄ TOKEN（算力）</td></tr>
      <tr><td>基建</td><td>电网 ⇄ AHL 协议层</td></tr>
      <tr><td>计量</td><td>电表 ⇄ 握手计量器</td></tr>
      <tr><td>支撑</td><td>工业经济 ⇄ Agent 经济</td></tr>
      <tr><td colspan="2" class="concl">1 次握手 = X TOKEN · 1 TOKEN = ***</td></tr>
    </table>
    <div class="pull-quote">
      电网不生产产品，电网收电费。<br>
      AHL 不撮合交易，AHL 收 TOKEN。
    </div>
  </div>
"""

# ===========================================================================
# SLIDE 06 — 同构分形架构
# ===========================================================================
SLIDE_06 = """
  <div>
    <div class="eyebrow">05 · THE ARCHITECTURE</div>
    <h2>同构分形架构<br>三层 · 同一种解法</h2>
  </div>
  <div>
    <div class="audience-grid">
      <div class="aud-cell">
        <div class="aud-num">H</div>
        <div class="aud-name">单 店</div>
        <div class="aud-desc">本店 + 周边<br>完整闭环</div>
      </div>
      <div class="aud-cell">
        <div class="aud-num">G</div>
        <div class="aud-name">集 团</div>
        <div class="aud-desc">N 家店 + 联盟<br>完整闭环</div>
      </div>
      <div class="aud-cell">
        <div class="aud-num">C</div>
        <div class="aud-name">文 旅</div>
        <div class="aud-desc">全产业 Agent 网<br>完整闭环</div>
      </div>
    </div>
    <div class="dark-callout">
      <div class="dc-title">KEY INSIGHT</div>
      <div class="dc-body">
        <strong>同构</strong> 三层结构完全相同<br>
        <strong>自完备</strong> 每层独立可运营<br>
        <strong>可嵌套</strong> 大层包含小层
      </div>
    </div>
  </div>
"""

# ===========================================================================
# SLIDE 07 — 收口 / CTA
# ===========================================================================
SLIDE_07 = """
  <div>
    <div class="eyebrow">06 · THE TAKEAWAY</div>
    <h2>一张协议<br>三层适用<br>TOKEN 贯穿</h2>
  </div>
  <div>
    <div class="core-law">
      <div class="cl-eyebrow">CORE LAW · 核心法则</div>
      <div class="cl-title">AHL = <strong>Agent 时代的协议层 + TOKEN 计量器</strong></div>
    </div>
    <div class="forward-look">
      <strong>招早期试点客户 5-10 家</strong>（集团 / 文旅优先）<br>
      需要完整版商业计划书<br>
      评论区留言 <strong>'BP'</strong> · 我发您
    </div>
  </div>
"""
