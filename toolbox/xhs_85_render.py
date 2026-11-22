"""民政部85号令 × 酒店行业 — 小红书6图生成
基于 xhs_slides.py 模板（B166ER 深黑+金色商参风）
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace\toolbox')
from watermark_tool import protect_output

OUT_DIR = Path(r"D:\B166ER-OpenClaw\workspace\output\xhs_85_2026-08-01")
OUT_DIR.mkdir(parents=True, exist_ok=True)

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# ===== Common CSS (B166ER 商参风格 - 深黑+金色) =====
COMMON_CSS = """
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", "Heiti SC", "Noto Sans CJK SC", sans-serif;
    background: #000;
    -webkit-font-smoothing: antialiased;
  }
  .slide {
    width: 1080px;
    height: 1440px;
    position: relative;
    background:
      radial-gradient(circle at 88% 8%, rgba(212,175,55,0.14) 0%, transparent 42%),
      radial-gradient(circle at 8% 92%, rgba(212,175,55,0.08) 0%, transparent 38%),
      linear-gradient(160deg, #0A0E1A 0%, #141B2D 55%, #0A0E1A 100%);
    color: #FFFFFF;
    overflow: hidden;
    padding: 90px 70px;
  }
  .slide::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
      linear-gradient(rgba(212,175,55,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(212,175,55,0.03) 1px, transparent 1px);
    background-size: 80px 80px;
    pointer-events: none;
  }
  .bmark {
    position: absolute;
    font-size: 14px;
    color: #D4AF37;
    letter-spacing: 5px;
    font-weight: 700;
    z-index: 10;
  }
  .bmark-tl { top: 45px; left: 60px; }
  .bmark-br { bottom: 45px; right: 60px; }
  .pagenum {
    position: absolute;
    top: 50px;
    right: 60px;
    font-size: 14px;
    color: #8A8F9B;
    letter-spacing: 3px;
    z-index: 10;
    font-weight: 500;
  }
  .tag {
    display: inline-block;
    border: 1.5px solid #D4AF37;
    color: #D4AF37;
    padding: 6px 16px;
    font-size: 13px;
    letter-spacing: 4px;
    font-weight: 500;
  }
  .sec-title {
    font-size: 30px;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: 3px;
    padding-bottom: 6px;
    border-bottom: 2px solid #D4AF37;
    margin-bottom: 36px;
  }
  .gold { color: #D4AF37; }
  .footer-meta {
    position: absolute;
    bottom: 50px;
    left: 70px;
    font-size: 11px;
    color: #6B7280;
    letter-spacing: 2px;
  }
"""

# ===== Slide definitions =====
slides_data = [
    # 1. 封面
    {
        "type": "cover",
        "html_body": """
<div class="slide">
  <div class="bmark bmark-tl">B166ER</div>
  <div class="pagenum">01 / 06</div>

  <div style="position:absolute; top: 200px; left: 70px; right: 70px; z-index: 5;">
    <div class="tag">政策解读 · 2026.08.01</div>
    <h1 style="font-size: 84px; font-weight: 800; line-height: 1.12; margin-top: 50px; letter-spacing: 2px;">
      酒店行业<br/><span class="gold">地震！</span>
    </h1>
    <div style="width: 80px; height: 4px; background: #D4AF37; margin-top: 50px;"></div>
    <div style="font-size: 26px; color: #B8BCC8; margin-top: 30px; font-weight: 300; line-height: 1.5; letter-spacing: 1px;">
      民政部 85 号令<br/>
      <span class="gold" style="font-weight: 600;">今天施行</span> · 12 个月大洗牌开始
    </div>
  </div>

  <div style="position:absolute; bottom: 130px; left: 70px; right: 70px; z-index: 5; padding: 24px 28px; background: rgba(212,175,55,0.06); border-left: 3px solid #D4AF37;">
    <div style="font-size: 20px; color: #D8DCE5; line-height: 1.6; font-weight: 300;">
      "XX酒店研究院""促进会""中心"——<br/>
      <span class="gold" style="font-weight: 500;">要没了。</span>
    </div>
  </div>

  <div style="position:absolute; bottom: 50px; left: 70px; right: 70px; z-index: 5; display: flex; justify-content: space-between; align-items: flex-end;">
    <div style="font-size: 13px; color: #8A8F9B; letter-spacing: 2px;">ERIC 的 B166ER 出品</div>
    <div style="font-size: 13px; color: #D4AF37; letter-spacing: 2px;">→ 滑动看深度分析</div>
  </div>
</div>
"""
    },
    # 2. 政策一张看懂
    {
        "type": "policy",
        "html_body": """
<div class="slide">
  <div class="bmark bmark-tl">B166ER</div>
  <div class="pagenum">02 / 06</div>

  <div style="position:absolute; top: 130px; left: 70px; right: 70px; z-index: 5;">
    <div class="sec-title">一张图看懂 85 号令</div>
  </div>

  <!-- 时间轴 -->
  <div style="position:absolute; top: 220px; left: 70px; right: 70px; z-index: 5;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
      <div style="font-size: 16px; color: #D4AF37; font-weight: 600; letter-spacing: 2px;">2026.08.01</div>
      <div style="flex: 1; height: 2px; background: linear-gradient(90deg, #D4AF37 0%, #B8BCC8 100%); margin: 0 18px; position: relative;">
        <div style="position: absolute; left: 0; top: -4px; width: 10px; height: 10px; background: #D4AF37; border-radius: 50%;"></div>
        <div style="position: absolute; right: 0; top: -4px; width: 10px; height: 10px; background: #B8BCC8; border-radius: 50%;"></div>
      </div>
      <div style="font-size: 16px; color: #B8BCC8; font-weight: 600; letter-spacing: 2px;">2027.08.01</div>
    </div>
    <div style="display: flex; justify-content: space-between; font-size: 13px; color: #8A8F9B; letter-spacing: 1px;">
      <div>施行</div>
      <div>12 个月过渡期截止</div>
    </div>
  </div>

  <!-- 4禁1禁 -->
  <div style="position:absolute; top: 360px; left: 70px; right: 70px; z-index: 5;">
    <div style="font-size: 18px; color: #D4AF37; font-weight: 600; letter-spacing: 2px; margin-bottom: 18px;">4 类禁设分支机构 ❌</div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
      <div style="background: rgba(212,175,55,0.06); border-left: 3px solid #D4AF37; padding: 14px 18px; font-size: 16px; color: #D8DCE5; font-weight: 300;">地域性分支机构</div>
      <div style="background: rgba(212,175,55,0.06); border-left: 3px solid #D4AF37; padding: 14px 18px; font-size: 16px; color: #D8DCE5; font-weight: 300;">姓氏宗亲分支机构</div>
      <div style="background: rgba(212,175,55,0.06); border-left: 3px solid #D4AF37; padding: 14px 18px; font-size: 16px; color: #D8DCE5; font-weight: 300;">会员明显重合</div>
      <div style="background: rgba(212,175,55,0.06); border-left: 3px solid #D4AF37; padding: 14px 18px; font-size: 16px; color: #D8DCE5; font-weight: 300;">业务高度相似</div>
    </div>
  </div>

  <!-- 命名禁令 -->
  <div style="position:absolute; top: 700px; left: 70px; right: 70px; z-index: 5;">
    <div style="font-size: 18px; color: #D4AF37; font-weight: 600; letter-spacing: 2px; margin-bottom: 14px;">1 个命名禁令 ❌</div>
    <div style="background: rgba(255,255,255,0.03); padding: 18px 22px; font-size: 22px; color: #FFFFFF; font-weight: 500; letter-spacing: 1px; margin-bottom: 14px; text-decoration: line-through; text-decoration-color: #D4AF37;">
      中心 · 联盟 · 研究会 · 促进会 · 研究院
    </div>
    <div style="font-size: 18px; color: #D4AF37; font-weight: 600; letter-spacing: 2px; margin-bottom: 14px;">✅ 只能叫</div>
    <div style="background: rgba(212,175,55,0.10); padding: 18px 22px; font-size: 22px; color: #D4AF37; font-weight: 600; letter-spacing: 1px; border: 1px solid #D4AF37;">
      分会 · 专业委员会 · 工作委员会 · 专家委员会 · 技术委员会
    </div>
  </div>

  <div class="footer-meta">ERIC 的 B166ER 出品 · 2026.08.01</div>
  <div class="bmark bmark-br">B166ER</div>
</div>
"""
    },
    # 3. 4层冲击传导链
    {
        "type": "impact",
        "html_body": """
<div class="slide">
  <div class="bmark bmark-tl">B166ER</div>
  <div class="pagenum">03 / 06</div>

  <div style="position:absolute; top: 130px; left: 70px; right: 70px; z-index: 5;">
    <div class="sec-title">酒店行业的 4 层传导冲击</div>
  </div>

  <!-- 漏斗 -->
  <div style="position:absolute; top: 260px; left: 70px; right: 70px; z-index: 5;">
    <!-- 第1层 -->
    <div style="display: flex; align-items: center; margin-bottom: 14px;">
      <div style="width: 60px; height: 60px; background: #D4AF37; color: #0A0E1A; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: 800; flex-shrink: 0;">01</div>
      <div style="flex: 1; margin-left: 16px; background: rgba(212,175,55,0.08); padding: 16px 22px; border-left: 3px solid #D4AF37;">
        <div style="font-size: 18px; color: #D4AF37; font-weight: 600; letter-spacing: 1px; margin-bottom: 4px;">协会端</div>
        <div style="font-size: 17px; color: #D8DCE5; font-weight: 300; line-height: 1.5;">存量 "XX 酒店研究院 / 中心" 强制改名 / 撤销</div>
      </div>
    </div>

    <!-- 第2层 -->
    <div style="display: flex; align-items: center; margin: 0 30px; margin-bottom: 14px;">
      <div style="width: 60px; height: 60px; background: rgba(212,175,55,0.7); color: #0A0E1A; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: 800; flex-shrink: 0;">02</div>
      <div style="flex: 1; margin-left: 16px; background: rgba(212,175,55,0.06); padding: 16px 22px; border-left: 3px solid rgba(212,175,55,0.7);">
        <div style="font-size: 18px; color: #D4AF37; font-weight: 600; letter-spacing: 1px; margin-bottom: 4px;">业务端</div>
        <div style="font-size: 17px; color: #D8DCE5; font-weight: 300; line-height: 1.5;">培训 / 评奖 / 发榜主体合规性重审</div>
      </div>
    </div>

    <!-- 第3层 -->
    <div style="display: flex; align-items: center; margin: 0 60px; margin-bottom: 14px;">
      <div style="width: 60px; height: 60px; background: rgba(212,175,55,0.5); color: #0A0E1A; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: 800; flex-shrink: 0;">03</div>
      <div style="flex: 1; margin-left: 16px; background: rgba(212,175,55,0.05); padding: 16px 22px; border-left: 3px solid rgba(212,175,55,0.5);">
        <div style="font-size: 18px; color: #D4AF37; font-weight: 600; letter-spacing: 1px; margin-bottom: 4px;">集团端</div>
        <div style="font-size: 17px; color: #D8DCE5; font-weight: 300; line-height: 1.5;">酒店集团冠名研究机构资质清退</div>
      </div>
    </div>

    <!-- 第4层 -->
    <div style="display: flex; align-items: center; margin: 0 90px;">
      <div style="width: 60px; height: 60px; background: rgba(212,175,55,0.3); color: #0A0E1A; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: 800; flex-shrink: 0;">04</div>
      <div style="flex: 1; margin-left: 16px; background: rgba(212,175,55,0.04); padding: 16px 22px; border-left: 3px solid rgba(212,175,55,0.3);">
        <div style="font-size: 18px; color: #D4AF37; font-weight: 600; letter-spacing: 1px; margin-bottom: 4px;">话语权端</div>
        <div style="font-size: 17px; color: #D8DCE5; font-weight: 300; line-height: 1.5;">头部合规智库集中度 ↑</div>
      </div>
    </div>
  </div>

  <!-- 底部洞察 -->
  <div style="position:absolute; bottom: 130px; left: 70px; right: 70px; z-index: 5; padding: 20px 24px; background: rgba(212,175,55,0.08); border: 1px solid #D4AF37; border-radius: 2px;">
    <div style="font-size: 17px; color: #D8DCE5; line-height: 1.6; font-weight: 300; letter-spacing: 0.5px;">
      <span class="gold" style="font-weight: 500;">本质：</span>"挂靠型智库"时代终结，行业研究供给收缩 → 头部集中
    </div>
  </div>

  <div class="footer-meta">ERIC 的 B166ER 出品 · 2026.08.01</div>
  <div class="bmark bmark-br">B166ER</div>
</div>
"""
    },
    # 4. 5个新机会
    {
        "type": "opportunity",
        "html_body": """
<div class="slide">
  <div class="bmark bmark-tl">B166ER</div>
  <div class="pagenum">04 / 06</div>

  <div style="position:absolute; top: 130px; left: 70px; right: 70px; z-index: 5;">
    <div class="sec-title">5 个新机会正在诞生</div>
  </div>

  <!-- 5卡片网格 (上3下2) -->
  <div style="position:absolute; top: 240px; left: 70px; right: 70px; z-index: 5;">
    <!-- 上排3卡 -->
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; margin-bottom: 14px;">
      <div style="background: rgba(212,175,55,0.08); border-top: 3px solid #D4AF37; padding: 22px 18px;">
        <div style="font-size: 36px; font-weight: 800; color: #D4AF37; line-height: 1; margin-bottom: 12px;">01</div>
        <div style="font-size: 19px; color: #FFFFFF; font-weight: 600; margin-bottom: 8px; letter-spacing: 1px;">改名咨询</div>
        <div style="font-size: 14px; color: #B8BCC8; line-height: 1.55; font-weight: 300;">品牌重塑<br/>12 个月窗口期</div>
      </div>
      <div style="background: rgba(212,175,55,0.08); border-top: 3px solid #D4AF37; padding: 22px 18px;">
        <div style="font-size: 36px; font-weight: 800; color: #D4AF37; line-height: 1; margin-bottom: 12px;">02</div>
        <div style="font-size: 19px; color: #FFFFFF; font-weight: 600; margin-bottom: 8px; letter-spacing: 1px;">独立法人化</div>
        <div style="font-size: 14px; color: #B8BCC8; line-height: 1.55; font-weight: 300;">法律服务<br/>牌照属性</div>
      </div>
      <div style="background: rgba(212,175,55,0.08); border-top: 3px solid #D4AF37; padding: 22px 18px;">
        <div style="font-size: 36px; font-weight: 800; color: #D4AF37; line-height: 1; margin-bottom: 12px;">03</div>
        <div style="font-size: 19px; color: #FFFFFF; font-weight: 600; margin-bottom: 8px; letter-spacing: 1px;">专家委员会</div>
        <div style="font-size: 14px; color: #B8BCC8; line-height: 1.55; font-weight: 300;">新质生产力智库<br/>政策鼓励</div>
      </div>
    </div>

    <!-- 下排2卡 -->
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
      <div style="background: rgba(212,175,55,0.08); border-top: 3px solid #D4AF37; padding: 22px 18px;">
        <div style="font-size: 36px; font-weight: 800; color: #D4AF37; line-height: 1; margin-bottom: 12px;">04</div>
        <div style="font-size: 19px; color: #FFFFFF; font-weight: 600; margin-bottom: 8px; letter-spacing: 1px;">资产收购</div>
        <div style="font-size: 14px; color: #B8BCC8; line-height: 1.55; font-weight: 300;">野鸡研究院 IP / 数据<br/>抄底窗口</div>
      </div>
      <div style="background: rgba(212,175,55,0.08); border-top: 3px solid #D4AF37; padding: 22px 18px;">
        <div style="font-size: 36px; font-weight: 800; color: #D4AF37; line-height: 1; margin-bottom: 12px;">05</div>
        <div style="font-size: 19px; color: #FFFFFF; font-weight: 600; margin-bottom: 8px; letter-spacing: 1px;">协会话语权</div>
        <div style="font-size: 14px; color: #B8BCC8; line-height: 1.55; font-weight: 300;">总秘书处集中<br/>长期红利</div>
      </div>
    </div>
  </div>

  <!-- 底部金句 -->
  <div style="position:absolute; bottom: 130px; left: 70px; right: 70px; z-index: 5; padding: 20px 24px; background: rgba(212,175,55,0.08); border: 1px solid #D4AF37; border-radius: 2px;">
    <div style="font-size: 17px; color: #D8DCE5; line-height: 1.6; font-weight: 300; letter-spacing: 0.5px;">
      <span class="gold" style="font-weight: 500;">先行者窗口期：</span>12 个月 = 改名 / 收购 / 站队 的战略选择期
    </div>
  </div>

  <div class="footer-meta">ERIC 的 B166ER 出品 · 2026.08.01</div>
  <div class="bmark bmark-br">B166ER</div>
</div>
"""
    },
    # 5. 12个月行动清单
    {
        "type": "timeline",
        "html_body": """
<div class="slide">
  <div class="bmark bmark-tl">B166ER</div>
  <div class="pagenum">05 / 06</div>

  <div style="position:absolute; top: 130px; left: 70px; right: 70px; z-index: 5;">
    <div class="sec-title">12 个月行动清单</div>
  </div>

  <!-- 时间线 -->
  <div style="position:absolute; top: 240px; left: 100px; right: 100px; z-index: 5;">
    <!-- 中线 -->
    <div style="position: absolute; left: 50%; top: 0; bottom: 0; width: 2px; background: linear-gradient(180deg, #D4AF37 0%, #6B7280 100%); transform: translateX(-50%);"></div>

    <!-- Q3 2026 -->
    <div style="display: flex; align-items: center; margin-bottom: 36px; position: relative;">
      <div style="width: 50%; text-align: right; padding-right: 32px;">
        <div style="font-size: 16px; color: #D4AF37; font-weight: 600; letter-spacing: 2px; margin-bottom: 4px;">Q3 2026</div>
        <div style="font-size: 13px; color: #8A8F9B; letter-spacing: 1px;">现在 — 9 月</div>
      </div>
      <div style="position: absolute; left: 50%; transform: translateX(-50%); width: 24px; height: 24px; background: #D4AF37; border-radius: 50%; border: 4px solid #0A0E1A; z-index: 2;"></div>
      <div style="width: 50%; padding-left: 32px;">
        <div style="font-size: 19px; color: #FFFFFF; font-weight: 600; letter-spacing: 1px;">摸底 + 决策</div>
        <div style="font-size: 14px; color: #B8BCC8; line-height: 1.5; font-weight: 300; margin-top: 4px;">分支机构清单 / 内部立项</div>
      </div>
    </div>

    <!-- Q4 2026 -->
    <div style="display: flex; align-items: center; margin-bottom: 36px; position: relative;">
      <div style="width: 50%; text-align: right; padding-right: 32px;">
        <div style="font-size: 19px; color: #FFFFFF; font-weight: 600; letter-spacing: 1px;">方案 + 章程</div>
        <div style="font-size: 14px; color: #B8BCC8; line-height: 1.5; font-weight: 300; margin-top: 4px;">保留 / 改名 / 撤销 / 独立</div>
      </div>
      <div style="position: absolute; left: 50%; transform: translateX(-50%); width: 24px; height: 24px; background: rgba(212,175,55,0.8); border-radius: 50%; border: 4px solid #0A0E1A; z-index: 2;"></div>
      <div style="width: 50%; padding-left: 32px;">
        <div style="font-size: 16px; color: rgba(212,175,55,0.9); font-weight: 600; letter-spacing: 2px; margin-bottom: 4px;">Q4 2026</div>
        <div style="font-size: 13px; color: #8A8F9B; letter-spacing: 1px;">10 — 12 月</div>
      </div>
    </div>

    <!-- Q1 2027 -->
    <div style="display: flex; align-items: center; margin-bottom: 36px; position: relative;">
      <div style="width: 50%; text-align: right; padding-right: 32px;">
        <div style="font-size: 16px; color: rgba(212,175,55,0.8); font-weight: 600; letter-spacing: 2px; margin-bottom: 4px;">Q1 2027</div>
        <div style="font-size: 13px; color: #8A8F9B; letter-spacing: 1px;">1 — 3 月</div>
      </div>
      <div style="position: absolute; left: 50%; transform: translateX(-50%); width: 24px; height: 24px; background: rgba(212,175,55,0.7); border-radius: 50%; border: 4px solid #0A0E1A; z-index: 2;"></div>
      <div style="width: 50%; padding-left: 32px;">
        <div style="font-size: 19px; color: #FFFFFF; font-weight: 600; letter-spacing: 1px;">新架构注册</div>
        <div style="font-size: 14px; color: #B8BCC8; line-height: 1.5; font-weight: 300; margin-top: 4px;">独立法人化 / 理事会表决</div>
      </div>
    </div>

    <!-- Q2 2027 -->
    <div style="display: flex; align-items: center; margin-bottom: 36px; position: relative;">
      <div style="width: 50%; text-align: right; padding-right: 32px;">
        <div style="font-size: 19px; color: #FFFFFF; font-weight: 600; letter-spacing: 1px;">品牌切换</div>
        <div style="font-size: 14px; color: #B8BCC8; line-height: 1.5; font-weight: 300; margin-top: 4px;">资产转移 / 人员安置</div>
      </div>
      <div style="position: absolute; left: 50%; transform: translateX(-50%); width: 24px; height: 24px; background: rgba(212,175,55,0.5); border-radius: 50%; border: 4px solid #0A0E1A; z-index: 2;"></div>
      <div style="width: 50%; padding-left: 32px;">
        <div style="font-size: 16px; color: rgba(212,175,55,0.6); font-weight: 600; letter-spacing: 2px; margin-bottom: 4px;">Q2 2027</div>
        <div style="font-size: 13px; color: #8A8F9B; letter-spacing: 1px;">4 — 6 月</div>
      </div>
    </div>

    <!-- Q3 2027 截止 -->
    <div style="display: flex; align-items: center; position: relative;">
      <div style="width: 50%; text-align: right; padding-right: 32px;">
        <div style="font-size: 16px; color: #6B7280; font-weight: 600; letter-spacing: 2px; margin-bottom: 4px;">Q3 2027</div>
        <div style="font-size: 13px; color: #8A8F9B; letter-spacing: 1px;">7 — 8 月</div>
      </div>
      <div style="position: absolute; left: 50%; transform: translateX(-50%); width: 28px; height: 28px; background: #6B7280; border-radius: 50%; border: 4px solid #0A0E1A; z-index: 2; display: flex; align-items: center; justify-content: center; font-size: 14px; color: #0A0E1A; font-weight: 800;">!</div>
      <div style="width: 50%; padding-left: 32px;">
        <div style="font-size: 19px; color: #FFFFFF; font-weight: 600; letter-spacing: 1px;">合规完成</div>
        <div style="font-size: 14px; color: #D4AF37; line-height: 1.5; font-weight: 500; margin-top: 4px;">截止 2027.08.01</div>
      </div>
    </div>
  </div>

  <div class="footer-meta">ERIC 的 B166ER 出品 · 2026.08.01</div>
  <div class="bmark bmark-br">B166ER</div>
</div>
"""
    },
    # 6. 互动页
    {
        "type": "interactive",
        "html_body": """
<div class="slide">
  <div class="bmark bmark-tl">B166ER</div>
  <div class="pagenum">06 / 06</div>

  <div style="position:absolute; top: 180px; left: 70px; right: 70px; z-index: 5; text-align: center;">
    <div style="display: inline-block; border: 1.5px solid #D4AF37; color: #D4AF37; padding: 6px 16px; font-size: 13px; letter-spacing: 4px; font-weight: 500;">
      评论区见
    </div>
  </div>

  <div style="position:absolute; top: 260px; left: 70px; right: 70px; z-index: 5; text-align: center;">
    <div style="font-size: 52px; font-weight: 700; color: #FFFFFF; line-height: 1.3; letter-spacing: 2px;">
      你是哪类？<br/>
      <span class="gold">对号入座</span>
    </div>
  </div>

  <!-- 5个角色卡片 -->
  <div style="position:absolute; top: 480px; left: 70px; right: 70px; z-index: 5;">
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
      <div style="background: rgba(212,175,55,0.08); border-left: 3px solid #D4AF37; padding: 16px 20px; display: flex; align-items: center;">
        <div style="font-size: 32px; color: #D4AF37; font-weight: 800; margin-right: 14px; flex-shrink: 0;">A</div>
        <div>
          <div style="font-size: 17px; color: #FFFFFF; font-weight: 600; margin-bottom: 3px;">协会负责人</div>
          <div style="font-size: 13px; color: #B8BCC8; font-weight: 300;">必须立刻行动</div>
        </div>
      </div>
      <div style="background: rgba(212,175,55,0.08); border-left: 3px solid #D4AF37; padding: 16px 20px; display: flex; align-items: center;">
        <div style="font-size: 32px; color: #D4AF37; font-weight: 800; margin-right: 14px; flex-shrink: 0;">B</div>
        <div>
          <div style="font-size: 17px; color: #FFFFFF; font-weight: 600; margin-bottom: 3px;">酒店集团</div>
          <div style="font-size: 13px; color: #B8BCC8; font-weight: 300;">看冠名机构</div>
        </div>
      </div>
    </div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
      <div style="background: rgba(212,175,55,0.08); border-left: 3px solid #D4AF37; padding: 16px 20px; display: flex; align-items: center;">
        <div style="font-size: 32px; color: #D4AF37; font-weight: 800; margin-right: 14px; flex-shrink: 0;">C</div>
        <div>
          <div style="font-size: 17px; color: #FFFFFF; font-weight: 600; margin-bottom: 3px;">行业智库</div>
          <div style="font-size: 13px; color: #B8BCC8; font-weight: 300;">合规路径重估</div>
        </div>
      </div>
      <div style="background: rgba(212,175,55,0.08); border-left: 3px solid #D4AF37; padding: 16px 20px; display: flex; align-items: center;">
        <div style="font-size: 32px; color: #D4AF37; font-weight: 800; margin-right: 14px; flex-shrink: 0;">D</div>
        <div>
          <div style="font-size: 17px; color: #FFFFFF; font-weight: 600; margin-bottom: 3px;">投资人</div>
          <div style="font-size: 13px; color: #B8BCC8; font-weight: 300;">机会在哪</div>
        </div>
      </div>
    </div>

    <div style="background: rgba(212,175,55,0.04); border-left: 3px solid rgba(212,175,55,0.4); padding: 16px 20px; display: flex; align-items: center; opacity: 0.85;">
      <div style="font-size: 32px; color: #6B7280; font-weight: 800; margin-right: 14px; flex-shrink: 0;">E</div>
      <div>
        <div style="font-size: 17px; color: #B8BCC8; font-weight: 500; margin-bottom: 3px;">旁观者</div>
        <div style="font-size: 13px; color: #8A8F9B; font-weight: 300;">吃瓜学习</div>
      </div>
    </div>
  </div>

  <div style="position:absolute; bottom: 110px; left: 70px; right: 70px; z-index: 5; text-align: center;">
    <div style="font-size: 20px; color: #D4AF37; font-weight: 600; letter-spacing: 3px; margin-bottom: 8px;">
      👇 评论区告诉我
    </div>
    <div style="font-size: 13px; color: #8A8F9B; letter-spacing: 2px;">
      关注 B166ER · 每周拆解一个商业现象
    </div>
  </div>

  <div class="bmark bmark-br">B166ER</div>
</div>
"""
    },
]

# Render each slide
print(f"Output directory: {OUT_DIR}")
print(f"Rendering {len(slides_data)} slides at 1080x1440 (Retina 2x)...")

for idx, slide in enumerate(slides_data, 1):
    html_path = OUT_DIR / f"slide_{idx:02d}.html"
    png_path = OUT_DIR / f"slide_{idx:02d}.png"

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>XHS 85号令 Slide {idx}</title>
<style>{COMMON_CSS}
</style>
</head>
<body>
{slide["html_body"]}
</body>
</html>"""

    html_path.write_text(html_content, encoding='utf-8')

    # Render via Edge headless
    r = subprocess.run([
        EDGE, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--force-device-scale-factor=2",
        "--window-size=1080,1440",
        f"--screenshot={png_path}",
        html_path.as_uri(),
    ], capture_output=True, text=True, timeout=60)
    
    rc = r.returncode
    size = png_path.stat().st_size if png_path.exists() else 0
    print(f"  Slide {idx}/{len(slides_data)}: RC={rc}, PNG={size:,} bytes")

    # Watermark (R12 规则：所有视觉产出必须水印)
    if png_path.exists() and size > 0:
        try:
            wm_out = protect_output(str(png_path))
            print(f"    Watermark: {Path(wm_out).name}")
        except Exception as e:
            print(f"    Watermark FAILED: {e}")

print("\n=== All slides rendered + watermarked ===")
print(f"\nOutput files:")
for p in sorted(OUT_DIR.glob("slide_*.png")):
    print(f"  {p.name}: {p.stat().st_size:,} bytes")
