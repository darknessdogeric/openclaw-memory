"""2026 H1 中国酒店行业全景状态报告 · 小红书 12 图
R34 麦肯锡 + 美联储 + 摩根 风格
1080×1440 (3:4)
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
  .content {
    position: absolute;
    top: 130px; left: 70px; right: 70px; bottom: 130px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .eyebrow {
    font-size: 14px;
    letter-spacing: 6px;
    color: #C8102E;
    font-weight: 700;
    margin-bottom: 16px;
  }
  h1 {
    font-size: 88px;
    font-weight: 800;
    line-height: 1.1;
    color: #0A2540;
    letter-spacing: 4px;
    margin-bottom: 16px;
  }
  h1 .accent { color: #C8102E; }
  h2 {
    font-size: 56px;
    font-weight: 800;
    line-height: 1.2;
    color: #0A2540;
    letter-spacing: 3px;
    margin-bottom: 24px;
  }
  .body-text {
    font-size: 28px;
    line-height: 1.7;
    color: #2D3F5A;
    letter-spacing: 1px;
    font-weight: 400;
  }
  .body-text strong { color: #C8102E; font-weight: 700; }
  .body-text em { font-style: italic; color: #0A2540; font-weight: 600; }
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
  .data-callout {
    text-align: center;
    padding: 30px 0;
    margin: 24px 0;
  }
  .data-callout .value {
    font-size: 180px;
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
  .del-vs {
    font-size: 36px;
    line-height: 1.7;
    color: #0A2540;
    margin: 24px 0;
    text-align: center;
    font-weight: 600;
    letter-spacing: 3px;
  }
  .del-vs .old { text-decoration: line-through; color: #8A8F9B; margin-right: 16px; }
  .del-vs .new { color: #C8102E; font-weight: 800; margin-left: 16px; }
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
  .kpi-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin: 20px 0;
  }
  .kpi-cell {
    padding: 18px 14px;
    background: #FFFFFF;
    border-left: 4px solid #C8102E;
  }
  .kpi-cell .kpi-label {
    font-size: 14px;
    color: #8A8F9B;
    letter-spacing: 2px;
    font-weight: 600;
    margin-bottom: 4px;
  }
  .kpi-cell .kpi-val {
    font-size: 28px;
    font-weight: 900;
    color: #0A2540;
    letter-spacing: 1px;
    line-height: 1.1;
  }
  .kpi-cell .kpi-val .up { color: #2E7D32; }
  .kpi-cell .kpi-val .dn { color: #C8102E; }
  .kpi-cell .kpi-sub {
    font-size: 16px;
    color: #5A6578;
    margin-top: 4px;
    letter-spacing: 1px;
  }
"""

# ===========================================================================
# SLIDE 01 — 封面
# ===========================================================================
SLIDE_01 = """
  <div>
    <div class="eyebrow">EXECUTIVE BRIEFING · 2026.08.22</div>
    <h1>2026 H1<br>中国酒店<br><span class="accent">全景状态</span></h1>
  </div>
  <div>
    <div class="formula">
      <div class="f-text">供给<span class="eq">·</span>需求<span class="eq">·</span>格局</div>
      <div class="f-sub">REVPAR 同比转正的拐点半年</div>
    </div>
    <div class="red-bar">
      <div class="bar-text">
        <strong>9 大维度</strong> + <strong>58 信源框架</strong> + <strong>置信度标注</strong>
      </div>
    </div>
  </div>
"""

# ===========================================================================
# SLIDE 02 — 一句话总结
# ===========================================================================
SLIDE_02 = """
  <div>
    <div class="eyebrow">00 · THE HEADLINE</div>
    <h2>RevPAR 转正的<br>拐点半年</h2>
  </div>
  <div>
    <div class="pull-quote">
      量已回 · 价初稳 · 供给出清 · 格局向头部收敛
    </div>
    <div class="red-bar">
      <div class="bar-text">
        短看<strong>入境 + 暑期弹性</strong><br>
        中看<strong>中高端内卷胜负</strong><br>
        长看<strong>人口结构换仓</strong>
      </div>
    </div>
  </div>
"""

# ===========================================================================
# SLIDE 03 — 宏观基本面
# ===========================================================================
SLIDE_03 = """
  <div>
    <div class="eyebrow">01 · THE MACRO</div>
    <h2>供给出清后半场<br>+ 需求 K 型分化</h2>
  </div>
  <div>
    <table class="editorial">
      <tr><td>存量客房</td><td><strong>~1,750-1,800 万间</strong> · +2~3% · 增速放缓</td></tr>
      <tr><td>存量门店</td><td><strong>~36-37 万家</strong> · 单体持续出清</td></tr>
      <tr><td>国内出游</td><td>恢复性增长 · <strong>+8~12%</strong></td></tr>
      <tr><td>入境游</td><td>免签扩容 · <strong>+25~35%</strong> · ★ 高置信</td></tr>
      <tr><td colspan="2" class="concl">供给增速首次降到需求增速之下</td></tr>
    </table>
    <div class="red-bar">
      <div class="bar-text">
        <strong>ADR 修复</strong>慢于 <strong>OCC</strong> · 量先回 价滞后
      </div>
    </div>
  </div>
"""

# ===========================================================================
# SLIDE 04 — 运营06 维
# ===========================================================================
SLIDE_04 = """
  <div>
    <div class="eyebrow">02 · THE OPERATIONS</div>
    <h2>运营 06 维<br>RevPAR ★ 关键拐点</h2>
  </div>
  <div>
    <div class="kpi-grid">
      <div class="kpi-cell">
        <div class="kpi-label">OCC · 入住率</div>
        <div class="kpi-val"><span class="up">62-65%</span></div>
        <div class="kpi-sub">+1.5~2.5pct · 量先回</div>
      </div>
      <div class="kpi-cell">
        <div class="kpi-label">ADR · 平均房价</div>
        <div class="kpi-val"><span class="up">¥295-315</span></div>
        <div class="kpi-sub">-1%~+2% · 转正临界点</div>
      </div>
      <div class="kpi-cell">
        <div class="kpi-label">RevPAR · 每间可售房收入</div>
        <div class="kpi-val"><span class="up">¥188-200</span></div>
        <div class="kpi-sub">+2~4% · ★ 拐点</div>
      </div>
      <div class="kpi-cell">
        <div class="kpi-label">OTA 占比</div>
        <div class="kpi-val"><span>28-32%</span></div>
        <div class="kpi-sub">持平微升 · 头部直销防守</div>
      </div>
    </div>
    <div class="pull-quote">
      结束连续 6~8 季度同比下滑<br>
      <strong>★ 关键拐点信号</strong>
    </div>
  </div>
"""

# ===========================================================================
# SLIDE 05 — 档次 K 型
# ===========================================================================
SLIDE_05 = """
  <div>
    <div class="eyebrow">03 · THE TIERS</div>
    <h2>档次 04 维<br>K 型分化定型</h2>
  </div>
  <div>
    <table class="editorial">
      <tr><td>奢华</td><td><strong>≥¥1,200</strong> · 高端商务疲软 / 度假奢华坚挺</td></tr>
      <tr><td>高档</td><td><strong>¥600-1,200</strong> · <strong>最承压</strong> · RevPAR -2~-4%</td></tr>
      <tr><td>中高端</td><td><strong>¥400-600</strong> · 主战场 · 最卷 · RevPAR +1~3%</td></tr>
      <tr><td>中端</td><td><strong>¥200-400</strong> · 稳定基本盘 · RevPAR +2~4%</td></tr>
      <tr><td>经济</td><td><strong>¥100-200</strong> · 单体加速出清 · 连锁品牌逆势收割</td></tr>
      <tr><td colspan="2" class="concl">亚朵 / 桔子水晶 / 丽呈 · 扩张最猛</td></tr>
    </table>
  </div>
"""

# ===========================================================================
# SLIDE 06 — 地理 03 维
# ===========================================================================
SLIDE_06 = """
  <div>
    <div class="eyebrow">04 · THE GEOGRAPHY</div>
    <h2>地理 03 维<br>下沉红利验证期</h2>
  </div>
  <div>
    <div class="audience-grid">
      <div class="aud-cell">
        <div class="aud-num">L2</div>
        <div class="aud-name">一线 / 新一线</div>
        <div class="aud-desc">供给最密<br>价格战最烈<br>RevPAR 修复最慢</div>
      </div>
      <div class="aud-cell">
        <div class="aud-num">L3</div>
        <div class="aud-name">县 域</div>
        <div class="aud-desc">连锁化率仅 ~30%<br>★ 新签约 55-60% 落三线及以下</div>
      </div>
      <div class="aud-cell">
        <div class="aud-num">Q4</div>
        <div class="aud-name">景区 / 商圈</div>
        <div class="aud-desc">三亚 / 大理 / 阿勒泰<br>ADR 韧性最强<br>冰雪+避暑双季</div>
      </div>
    </div>
    <div class="forward-look">
      入境口岸城市（上海 / 成都 / 西安）外宾间夜占比回升至 <strong>2019 年 80-90%</strong> 水平
    </div>
  </div>
"""

# ===========================================================================
# SLIDE 07 — 客群 05 维
# ===========================================================================
SLIDE_07 = """
  <div>
    <div class="eyebrow">05 · THE CUSTOMERS</div>
    <h2>客群 05 维<br>结构换血</h2>
  </div>
  <div>
    <table class="editorial">
      <tr><td>亲 子</td><td><strong>25-30%</strong> ↓ 人口结构传导开始显性化</td></tr>
      <tr><td>商 务</td><td>20-25% 弱修复 · 差标下移 · 中端受益</td></tr>
      <tr><td>Z 世代</td><td><strong>10-15% ↑</strong> 演唱会 / 赛事跟着行程走 · 酒店+内容</td></tr>
      <tr><td>银 发</td><td><strong>10-15% ↑↑</strong> 候鸟康养 · 错峰长住 · ★ 最确定增量</td></tr>
      <tr><td>情 侣</td><td>10-15% 平 · 电竞房 / 影音房产品化</td></tr>
      <tr><td>MICE</td><td>5-10% 修复中 · 会奖回流二线</td></tr>
      <tr><td colspan="2" class="concl">银发 · 唯一确定性十年增量</td></tr>
    </table>
  </div>
"""

# ===========================================================================
# SLIDE 08 — 竞争格局
# ===========================================================================
SLIDE_08 = """
  <div>
    <div class="eyebrow">06 · THE COMPETITION</div>
    <h2>竞争格局<br>TOP10 集中度 60% → 70%</h2>
  </div>
  <div>
    <table class="editorial">
      <tr><td>华住</td><td>HTHT · 门店冲 12,000+ · RevPAR 同比转正 · <最稳></td></tr>
      <tr><td>锦江</td><td>600754 · 品牌整合收官 · CRS 统一 · 规模第一</td></tr>
      <tr><td>首旅</td><td>600258 · 如家焕新 + 中高端补课 · 稳健偏慢</td></tr>
      <tr><td>亚朵</td><td>ATAT · <估值锚> · 零售 GMV 或超酒店主业增速</td></tr>
      <tr><td>格林</td><td>2005.HK · 深耕下沉 · 平稳</td></tr>
      <tr><td>国际</td><td>全线押注中端特许经营 · 希尔顿欢朋 / 美居 / 快捷季</td></tr>
      <tr><td colspan="2" class="concl">连锁化率 ~42-45% → 60% 目标 · 集中度向 70% 推进</td></tr>
    </table>
  </div>
"""

# ===========================================================================
# SLIDE 09 — 政策与资本
# ===========================================================================
SLIDE_09 = """
  <div>
    <div class="eyebrow">07 · POLICY &amp; CAPITAL</div>
    <h2>政策与资本<br>08 维</h2>
  </div>
  <div>
    <div class="dark-callout">
      <div class="dc-title">KEY POLICY</div>
      <div class="dc-body">
        <strong>消费 REITs 扩容</strong><br>
        酒店资产纳入试点预期升温<br>
        重资产退出通道打开
      </div>
    </div>
    <ol class="editorial">
      <li><strong>入境便利化</strong> · 免签国扩围 + 支付友好化 · 利好高档/奢华</li>
      <li><strong>银发经济</strong>顶层设计 · 康养酒店 / 旅居产品获政策背书</li>
      <li><strong>消防合规</strong> · 单体小酒店合规成本上升 → 加速连锁化</li>
    </ol>
  </div>
"""

# ===========================================================================
# SLIDE 10 — 人口结构
# ===========================================================================
SLIDE_10 = """
  <div>
    <div class="eyebrow">08 · THE DEMOGRAPH · · · · 五星必修</div>
    <h2>人口结构 09 维<br>最深的暗流</h2>
  </div>
  <div>
    <div class="data-callout">
      <div class="value">-66%</div>
      <div class="unit">2025 新生儿 vs 2016 峰值</div>
    </div>
    <div class="red-bar">
      <div class="bar-text">
        亲子红利进入 <strong>5-8 年倒计时</strong><br>
        学龄人口 -9.6% · 暑期亲子总盘子结构性收缩
      </div>
    </div>
    <div class="pull-quote">
      老龄化加速 · 银发旅居<br>
      <strong>唯一确定性十年增量</strong>
    </div>
  </div>
"""

# ===========================================================================
# SLIDE 11 — 风险
# ===========================================================================
SLIDE_11 = """
  <div>
    <div class="eyebrow">09 · THE RISK</div>
    <h2>风险提示</h2>
  </div>
  <div>
    <div class="dark-callout">
      <div class="dc-title">DOWNSIDE</div>
      <div class="dc-body">
        宏观消费力若 <strong>二次走弱</strong><br>
        ADR 转正可能推迟至 <strong>2026 H2</strong>
      </div>
    </div>
    <div class="forward-look">
      以上推演待 <strong>8 月各集团 Q2 财报</strong>验证 · 口径声明：默认 T1 同比 (2026 H1 vs 2025 H1) · 58 信源框架推演 · 标注置信度 (★高 / ◐中 / ○低)
    </div>
    <div class="red-bar">
      <div class="bar-text">
        实盘请以 <strong>STR / 迈点 / 上市集团 Q2 财报</strong> 交叉校准
      </div>
    </div>
  </div>
"""

# ===========================================================================
# SLIDE 12 — 收口 CTA
# ===========================================================================
SLIDE_12 = """
  <div>
    <div class="eyebrow">10 · THE TAKEAWAY</div>
    <h2>一句话总结<br>2026 H1 酒店业</h2>
  </div>
  <div>
    <div class="core-law">
      <div class="cl-eyebrow">CORE LAW · 核心法则</div>
      <div class="cl-title">RevPAR <strong>同比转正</strong><br>拐点半年 · 量已回 · 价初稳</div>
    </div>
    <div class="forward-look">
      完整版<strong>酒店业深度研究档案</strong><br>
      含档次 04 维深度 + 头部 10 家对比表 + REITs 政策追踪<br>
      评论区留言 <strong>'酒店报告'</strong> · 我发您
    </div>
  </div>
"""