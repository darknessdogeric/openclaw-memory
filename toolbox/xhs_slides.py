"""Generate 7 小红书 slides (1080x1440) for the 智驾小蓝灯 topic."""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace\toolbox')
from watermark_tool import protect_output

OUT_DIR = Path(r"D:\B166ER-OpenClaw\workspace\output\xhs_2026-07-16")
OUT_DIR.mkdir(parents=True, exist_ok=True)

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# ===== Common CSS (B166ER 海报风格) =====
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

def render(html_content: str, idx: int):
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>XHS Slide {idx}</title>
<style>{COMMON_CSS}{html_content}</style>
</head>
<body>{html_body}</body>
</html>"""

# ===== Slide definitions =====
slides_data = [
    # 1. 封面
    {
        "type": "cover",
        "html_body": """
<div class="slide">
  <div class="bmark bmark-tl">B166ER</div>
  <div class="pagenum">01 / 07</div>

  <div style="position:absolute; top: 200px; left: 70px; right: 70px; z-index: 5;">
    <div class="tag">商业现象 · 2026</div>
    <h1 style="font-size: 92px; font-weight: 800; line-height: 1.1; margin-top: 60px; letter-spacing: 2px;">
      <span class="gold">30 块</span>蓝灯<br/>
      凭什么给<br/>
      <span class="gold">30 万</span>智驾代言？
    </h1>
    <div style="width: 80px; height: 4px; background: #D4AF37; margin-top: 50px;"></div>
    <div style="font-size: 26px; color: #B8BCC8; margin-top: 30px; font-weight: 300; line-height: 1.5; letter-spacing: 1px;">
      一场「不可见溢价」的<br/>可见化焦虑
    </div>
  </div>

  <div style="position:absolute; bottom: 50px; left: 70px; right: 70px; z-index: 5; display: flex; justify-content: space-between; align-items: flex-end;">
    <div style="font-size: 13px; color: #8A8F9B; letter-spacing: 2px;">ERIC 的 B166ER 出品</div>
    <div style="font-size: 13px; color: #D4AF37; letter-spacing: 2px;">↓ 滑动看深度分析</div>
  </div>
</div>
"""
    },
    # 2. 现象 + 数据
    {
        "type": "phenomenon",
        "html_body": """
<div class="slide">
  <div class="bmark bmark-tl">B166ER</div>
  <div class="pagenum">02 / 07</div>

  <div style="position:absolute; top: 130px; left: 70px; right: 70px; z-index: 5;">
    <div class="sec-title">这 是 个 什 么 现 象 ？</div>
  </div>

  <div style="position:absolute; top: 240px; left: 70px; right: 70px; z-index: 5;">
    <ul style="list-style: none;">
      <li style="font-size: 24px; color: #D8DCE5; line-height: 1.65; margin-bottom: 18px; padding-left: 24px; position: relative; font-weight: 300;">
        <span style="position:absolute; left: 0; top: 14px; width: 8px; height: 2px; background: #D4AF37;"></span>
        2025 Q4 起，新能源车主自费在车上加装<span class="gold">「智驾小蓝灯」</span>
      </li>
      <li style="font-size: 24px; color: #D8DCE5; line-height: 1.65; margin-bottom: 18px; padding-left: 24px; position: relative; font-weight: 300;">
        <span style="position:absolute; left: 0; top: 14px; width: 8px; height: 2px; background: #D4AF37;"></span>
        淘宝 / 拼多多月销 <span class="gold" style="font-weight: 500;">30-50 万单</span>
      </li>
      <li style="font-size: 24px; color: #D8DCE5; line-height: 1.65; margin-bottom: 18px; padding-left: 24px; position: relative; font-weight: 300;">
        <span style="position:absolute; left: 0; top: 14px; width: 8px; height: 2px; background: #D4AF37;"></span>
        价格 <span class="gold" style="font-weight: 500;">30-200 元</span>（vs 整车 20-50 万）
      </li>
      <li style="font-size: 24px; color: #D8DCE5; line-height: 1.65; margin-bottom: 18px; padding-left: 24px; position: relative; font-weight: 300;">
        <span style="position:absolute; left: 0; top: 14px; width: 8px; height: 2px; background: #D4AF37;"></span>
        多地交警开始专项整治 <span style="font-size: 18px; color: #8A8F9B;">（涉嫌模仿特种车辆灯具）</span>
      </li>
      <li style="font-size: 24px; color: #D8DCE5; line-height: 1.65; margin-bottom: 18px; padding-left: 24px; position: relative; font-weight: 300;">
        <span style="position:absolute; left: 0; top: 14px; width: 8px; height: 2px; background: #D4AF37;"></span>
        #小蓝灯 抖音话题播放 <span class="gold" style="font-weight: 500;">1 亿+</span>
      </li>
    </ul>
  </div>

  <div style="position:absolute; bottom: 200px; left: 70px; right: 70px; z-index: 5; padding: 24px 28px; background: rgba(212,175,55,0.06); border-left: 3px solid #D4AF37;">
    <div style="font-size: 18px; color: #B8BCC8; line-height: 1.6; font-weight: 300;">
      一条 <span class="gold" style="font-weight: 500;">30 块</span>的 LED 灯带，被挂在了 <span class="gold" style="font-weight: 500;">30 万</span>的新能源车上。
    </div>
  </div>

  <div class="footer-meta">ERIC 的 B166ER 出品 · 2026.07.16</div>
  <div class="bmark bmark-br">B166ER</div>
</div>
"""
    },
    # 3. 信号真空公式
    {
        "type": "formula",
        "html_body": """
<div class="slide">
  <div class="bmark bmark-tl">B166ER</div>
  <div class="pagenum">03 / 07</div>

  <div style="position:absolute; top: 130px; left: 70px; right: 70px; z-index: 5;">
    <div class="sec-title">背 后 的 本 质</div>
  </div>

  <div style="position:absolute; top: 380px; left: 70px; right: 70px; z-index: 5; text-align: center;">
    <div style="font-size: 26px; color: #B8BCC8; letter-spacing: 3px; margin-bottom: 50px; font-weight: 300;">
      信 号 真 空
    </div>
    <div style="font-size: 56px; font-weight: 700; color: #FFFFFF; letter-spacing: 2px; line-height: 1.3;">
      <span class="gold">高维功能</span> × <span class="gold">低辨识度</span><br/>
      <span style="font-size: 60px;">=</span><br/>
      <span style="color: #D4AF37;">信号真空</span>
    </div>
    <div style="width: 120px; height: 4px; background: #D4AF37; margin: 50px auto 0;"></div>
  </div>

  <div style="position:absolute; bottom: 180px; left: 70px; right: 70px; z-index: 5; padding: 28px 30px; background: rgba(212,175,55,0.08); border: 1px solid #D4AF37; border-radius: 2px;">
    <div style="font-size: 20px; color: #D8DCE5; line-height: 1.7; font-weight: 300; letter-spacing: 0.5px;">
      智驾开了没开，外人根本看不出来。<br/>
      30 万花出去，<span class="gold">只有驾驶者自己知道。</span><br/>
      所以他需要一个符号，替他开口说话。
    </div>
  </div>

  <div class="footer-meta">ERIC 的 B166ER 出品 · 2026.07.16</div>
  <div class="bmark bmark-br">B166ER</div>
</div>
"""
    },
    # 4. 为什么
    {
        "type": "motivation",
        "html_body": """
<div class="slide">
  <div class="bmark bmark-tl">B166ER</div>
  <div class="pagenum">04 / 07</div>

  <div style="position:absolute; top: 130px; left: 70px; right: 70px; z-index: 5;">
    <div class="sec-title">为 什 么 车 主 会 装 ？</div>
  </div>

  <div style="position:absolute; top: 250px; left: 70px; right: 70px; z-index: 5;">
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 18px;">

      <div style="background: rgba(212,175,55,0.06); border-top: 3px solid #D4AF37; padding: 22px 22px 24px;">
        <div style="font-size: 28px; font-weight: 700; color: #D4AF37; margin-bottom: 10px;">显摆</div>
        <div style="font-size: 18px; color: #D8DCE5; line-height: 1.55; font-weight: 300;">"我的车有智驾，你们的车没有"</div>
      </div>

      <div style="background: rgba(212,175,55,0.06); border-top: 3px solid #D4AF37; padding: 22px 22px 24px;">
        <div style="font-size: 28px; font-weight: 700; color: #D4AF37; margin-bottom: 10px;">安全声明</div>
        <div style="font-size: 18px; color: #D8DCE5; line-height: 1.55; font-weight: 300;">"我在自动驾驶，请保持车距"</div>
      </div>

      <div style="background: rgba(212,175,55,0.06); border-top: 3px solid #D4AF37; padding: 22px 22px 24px;">
        <div style="font-size: 28px; font-weight: 700; color: #D4AF37; margin-bottom: 10px;">部落归属</div>
        <div style="font-size: 18px; color: #D8DCE5; line-height: 1.55; font-weight: 300;">"我是 X 鹏 / 理想 / 问界车主"</div>
      </div>

      <div style="background: rgba(212,175,55,0.06); border-top: 3px solid #D4AF37; padding: 22px 22px 24px;">
        <div style="font-size: 28px; font-weight: 700; color: #D4AF37; margin-bottom: 10px;">焦虑抵消</div>
        <div style="font-size: 18px; color: #D8DCE5; line-height: 1.55; font-weight: 300;">"30 万的智驾，要让路人知道我花了这份钱"</div>
      </div>

    </div>
  </div>

  <div style="position:absolute; bottom: 130px; left: 70px; right: 70px; z-index: 5; padding: 22px 26px; background: rgba(212,175,55,0.06); border-left: 3px solid #D4AF37;">
    <div style="font-size: 18px; color: #B8BCC8; line-height: 1.6; font-weight: 300;">
      本质：<span class="gold" style="font-weight: 500;">蓝灯 = 自我证明 = 我没被坑</span>
    </div>
  </div>

  <div class="footer-meta">ERIC 的 B166ER 出品 · 2026.07.16</div>
  <div class="bmark bmark-br">B166ER</div>
</div>
"""
    },
    # 5. 还有谁（受众分层）
    {
        "type": "audience",
        "html_body": """
<div class="slide">
  <div class="bmark bmark-tl">B166ER</div>
  <div class="pagenum">05 / 07</div>

  <div style="position:absolute; top: 130px; left: 70px; right: 70px; z-index: 5;">
    <div class="sec-title">还 有 谁 在 挂 ？</div>
  </div>

  <div style="position:absolute; top: 230px; left: 70px; right: 70px; z-index: 5;">
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px;">

      <div style="background: rgba(255,255,255,0.03); border-top: 3px solid #D4AF37; padding: 20px 18px 22px;">
        <div style="font-size: 11px; color: #6B7280; letter-spacing: 2px; margin-bottom: 8px;">AUDIENCE · 01</div>
        <div style="font-size: 22px; font-weight: 700; color: #FFFFFF; margin-bottom: 8px; letter-spacing: 1px;">真智驾车主</div>
        <div style="font-size: 18px; color: #D4AF37; margin-bottom: 14px; letter-spacing: 1px;">「我有」</div>
        <div style="font-size: 15px; color: #B8BCC8; line-height: 1.6; font-weight: 300; min-height: 70px;">
          花了 20-50 万买智驾<br/>需要自我证明「不亏」
        </div>
        <div style="font-size: 12px; color: #8A8F9B; margin-top: 14px; padding-top: 10px; border-top: 1px dashed rgba(212,175,55,0.3);">
          占比 ~ 60% · 价格 30-200 元
        </div>
      </div>

      <div style="background: rgba(255,255,255,0.03); border-top: 3px solid #D4AF37; padding: 20px 18px 22px;">
        <div style="font-size: 11px; color: #6B7280; letter-spacing: 2px; margin-bottom: 8px;">AUDIENCE · 02</div>
        <div style="font-size: 22px; font-weight: 700; color: #FFFFFF; margin-bottom: 8px; letter-spacing: 1px;">非新能源车主</div>
        <div style="font-size: 18px; color: #D4AF37; margin-bottom: 14px; letter-spacing: 1px;">「我也有」</div>
        <div style="font-size: 15px; color: #B8BCC8; line-height: 1.6; font-weight: 300; min-height: 70px;">
          燃油车 / 老款 / 改装玩家<br/>借光心理，不落伍于时代
        </div>
        <div style="font-size: 12px; color: #8A8F9B; margin-top: 14px; padding-top: 10px; border-top: 1px dashed rgba(212,175,55,0.3);">
          占比 ~ 30% · 价格 15-50 元
        </div>
      </div>

      <div style="background: rgba(255,255,255,0.02); border-top: 3px solid #6B7280; padding: 20px 18px 22px; opacity: 0.92;">
        <div style="font-size: 11px; color: #6B7280; letter-spacing: 2px; margin-bottom: 8px;">AUDIENCE · 03</div>
        <div style="font-size: 22px; font-weight: 700; color: #FFFFFF; margin-bottom: 8px; letter-spacing: 1px;">广告 / 营销方</div>
        <div style="font-size: 18px; color: #D4AF37; margin-bottom: 14px; letter-spacing: 1px;">「我借用这个」</div>
        <div style="font-size: 15px; color: #B8BCC8; line-height: 1.6; font-weight: 300; min-height: 70px;">
          拍摄物料 / 4S 店 / 短视频<br/>挪用符号，获得科技联想
        </div>
        <div style="font-size: 12px; color: #8A8F9B; margin-top: 14px; padding-top: 10px; border-top: 1px dashed rgba(212,175,55,0.3);">
          占比 ~ 10% · 曝光放大 100×
        </div>
      </div>

    </div>
  </div>

  <div style="position:absolute; bottom: 130px; left: 70px; right: 70px; z-index: 5; padding: 20px 24px; background: rgba(212,175,55,0.08); border: 1px solid #D4AF37; border-radius: 2px;">
    <div style="font-size: 17px; color: #D8DCE5; line-height: 1.6; font-weight: 300;">
      当符号开始被<span class="gold" style="font-weight: 500;">非所有者</span>借用、被<span class="gold" style="font-weight: 500;">广告</span>挪用——<br/>
      它就<span class="gold" style="font-weight: 500;">从产品特征升格为文化符号</span>。
    </div>
  </div>

  <div class="footer-meta">ERIC 的 B166ER 出品 · 2026.07.16</div>
  <div class="bmark bmark-br">B166ER</div>
</div>
"""
    },
    # 6. 说明什么问题
    {
        "type": "insights",
        "html_body": """
<div class="slide">
  <div class="bmark bmark-tl">B166ER</div>
  <div class="pagenum">06 / 07</div>

  <div style="position:absolute; top: 130px; left: 70px; right: 70px; z-index: 5;">
    <div class="sec-title">说 明 什 么 问 题 ？</div>
  </div>

  <div style="position:absolute; top: 250px; left: 70px; right: 70px; z-index: 5;">
    <ul style="list-style: none;">
      <li style="font-size: 21px; color: #D4AF37; line-height: 1.6; margin-bottom: 22px; padding: 14px 20px; background: rgba(212,175,55,0.06); border-left: 3px solid #D4AF37; font-weight: 500;">
        <span style="display: inline-block; width: 30px; color: #6B7280;">01</span>
        智能驾驶的"可见化焦虑"：高维功能无法被外部感知
      </li>
      <li style="font-size: 21px; color: #D8DCE5; line-height: 1.6; margin-bottom: 22px; padding-left: 24px; position: relative; font-weight: 300;">
        <span style="position:absolute; left: 0; top: 14px; width: 8px; height: 2px; background: #D4AF37;"></span>
        <span style="display: inline-block; width: 30px; color: #6B7280;">02</span>
        车企品牌建设失误：没人为"智驾"设计可见标识
      </li>
      <li style="font-size: 21px; color: #D8DCE5; line-height: 1.6; margin-bottom: 22px; padding-left: 24px; position: relative; font-weight: 300;">
        <span style="position:absolute; left: 0; top: 14px; width: 8px; height: 2px; background: #D4AF37;"></span>
        <span style="display: inline-block; width: 30px; color: #6B7280;">03</span>
        用户社区运营的天然抓手被忽略
      </li>
      <li style="font-size: 21px; color: #D8DCE5; line-height: 1.6; margin-bottom: 22px; padding-left: 24px; position: relative; font-weight: 300;">
        <span style="position:absolute; left: 0; top: 14px; width: 8px; height: 2px; background: #D4AF37;"></span>
        <span style="display: inline-block; width: 30px; color: #6B7280;">04</span>
        装逼经济进入 micro-signal 时代
      </li>
      <li style="font-size: 21px; color: #D8DCE5; line-height: 1.6; margin-bottom: 22px; padding-left: 24px; position: relative; font-weight: 300;">
        <span style="position:absolute; left: 0; top: 14px; width: 8px; height: 2px; background: #D4AF37;"></span>
        <span style="display: inline-block; width: 30px; color: #6B7280;">05</span>
        监管对新现象的反应滞后
      </li>
    </ul>
  </div>

  <div style="position:absolute; bottom: 110px; left: 70px; right: 70px; z-index: 5; padding: 20px 24px; background: rgba(212,175,55,0.06); border-left: 3px solid #D4AF37;">
    <div style="font-size: 18px; color: #B8BCC8; line-height: 1.6; font-weight: 300;">
      这一切的根因：<span class="gold" style="font-weight: 500;">产品价值无法被外部识别</span>
    </div>
  </div>

  <div class="footer-meta">ERIC 的 B166ER 出品 · 2026.07.16</div>
  <div class="bmark bmark-br">B166ER</div>
</div>
"""
    },
    # 7. 总结 + CTA
    {
        "type": "conclusion",
        "html_body": """
<div class="slide">
  <div class="bmark bmark-tl">B166ER</div>
  <div class="pagenum">07 / 07</div>

  <div style="position:absolute; top: 180px; left: 70px; right: 70px; z-index: 5; text-align: center;">
    <div style="display: inline-block; border: 1.5px solid #D4AF37; color: #D4AF37; padding: 6px 16px; font-size: 13px; letter-spacing: 4px; font-weight: 500;">
      底 层 规 律
    </div>
  </div>

  <div style="position:absolute; top: 280px; left: 70px; right: 70px; z-index: 5; text-align: center;">
    <div style="font-size: 50px; font-weight: 700; color: #D4AF37; line-height: 1.45; letter-spacing: 3px;">
      当产品价值<br/>无法被外部识别<br/>
      <span style="font-size: 56px;">使用者会自发<br/>创造可见符号</span>
    </div>
  </div>

  <div style="position:absolute; top: 740px; left: 70px; right: 70px; z-index: 5; text-align: center;">
    <div style="width: 100px; height: 4px; background: #D4AF37; margin: 0 auto;"></div>
  </div>

  <div style="position:absolute; top: 800px; left: 70px; right: 70px; z-index: 5; text-align: center;">
    <div style="font-size: 32px; color: #FFFFFF; line-height: 1.5; letter-spacing: 2px; font-weight: 500;">
      符号的价值<br/>
      <span style="font-size: 38px;">不在于被发明，而在于被借用</span>
    </div>
  </div>

  <div style="position:absolute; bottom: 240px; left: 70px; right: 70px; z-index: 5; padding: 24px 28px; background: rgba(212,175,55,0.08); border: 1px solid #D4AF37; border-radius: 2px; text-align: center;">
    <div style="font-size: 18px; color: #B8BCC8; line-height: 1.6; font-weight: 300; letter-spacing: 1px;">
      下一个十年的心智之争<br/>
      <span class="gold" style="font-weight: 500;">从定义可见符号开始</span>
    </div>
  </div>

  <div style="position:absolute; bottom: 130px; left: 70px; right: 70px; z-index: 5; text-align: center;">
    <div style="font-size: 22px; color: #D4AF37; font-weight: 600; letter-spacing: 3px; margin-bottom: 14px;">
      评论区告诉我你的答案
    </div>
    <div style="font-size: 14px; color: #8A8F9B; letter-spacing: 2px;">
      关注 B166ER · 每周拆解一个商业现象
    </div>
  </div>

  <div class="bmark bmark-br">B166ER</div>
</div>
"""
    },
]

# Render each slide
for idx, slide in enumerate(slides_data, 1):
    html_path = OUT_DIR / f"slide_{idx:02d}.html"
    png_path = OUT_DIR / f"slide_{idx:02d}.png"
    wm_path = OUT_DIR / f"slide_{idx:02d}_wm.png"

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>XHS Slide {idx}</title>
<style>{COMMON_CSS}
</style>
</head>
<body>
{slide["html_body"]}
</body>
</html>"""

    html_path.write_text(html_content, encoding='utf-8')

    # Render
    r = subprocess.run([
        EDGE, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--force-device-scale-factor=2",
        "--window-size=1080,1440",
        f"--screenshot={png_path}",
        html_path.as_uri(),
    ], capture_output=True, text=True, timeout=60)
    print(f"Slide {idx} render: RC={r.returncode}, size={png_path.stat().st_size if png_path.exists() else 0}")

    # Watermark
    out_wm = protect_output(str(png_path))
    print(f"  Watermarked: {out_wm}")

print("\n=== All 7 slides generated ===")
print(f"Output dir: {OUT_DIR}")
for p in sorted(OUT_DIR.glob("slide_*_wm.png")):
    print(f"  {p.name}: {p.stat().st_size:,} bytes")