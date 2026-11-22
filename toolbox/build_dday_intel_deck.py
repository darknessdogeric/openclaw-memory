"""
build_dday_intel_deck.py — Real B166ER artifact using OfficeCLI
Builds: D-day 等待期情报协议 v1.0 (5 slides)

This is the FIRST production deliverable from the OfficeCLI integration.
Output: D:\OfficeCLI-test\b166er_outputs\dday_intel_protocol_v1.pptx
"""

import sys
sys.path.insert(0, r"D:\B166ER-OpenClaw\workspace\toolbox")
from officecli_skill import build_pptx, verify_pptx
import json
from pathlib import Path


OUTPUT_DIR = Path(r"D:\OfficeCLI-test\b166er_outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT = OUTPUT_DIR / "dday_intel_protocol_v1.pptx"


slides = [
    # Slide 1: Cover
    {
        "title": "D-day 等待期情报协议",
        "background": "0A0E27",  # deep navy (B166ER V3 Brutalist dark)
        "subtitle": "安逸集团产业发展部部长 · 任命公示期 T+1~T+12",
        "shapes": [
            {"text": "v1.0  |  2026-07-14  |  Eric / 张实", "x": "2cm", "y": "12cm",
             "size": 14, "color": "888888", "bold": False},
            {"text": "B166ER 出品 · officecli v1.0.135", "x": "2cm", "y": "13cm",
             "size": 12, "color": "555555"},
        ],
    },
    # Slide 2: 时间窗口
    {
        "title": "时间窗口 T+1 ~ T+12",
        "background": "FFFFFF",
        "shapes": [
            {"text": "今天 (T+1) = 7/14 周二", "x": "2cm", "y": "4.5cm", "size": 22, "bold": True},
            {"text": "内部通知窗口: T+1 ~ T+7 (7/14 ~ 7/20)", "x": "2cm", "y": "6cm", "size": 20},
            {"text": "  · 任前谈话 / 集团 OA / 党委组织部电话", "x": "2.5cm", "y": "7cm", "size": 16, "color": "555555"},
            {"text": "  · 任何一次接听 = 流程启动确认", "x": "2.5cm", "y": "8cm", "size": 16, "color": "555555"},
            {"text": "公示期: T+5 ~ T+12 (7/18 ~ 7/25)", "x": "2cm", "y": "9.5cm", "size": 20},
            {"text": "  · 集团内部 OA / 工会 / 党群工作部", "x": "2.5cm", "y": "10.5cm", "size": 16, "color": "555555"},
            {"text": "正式任命公告: T+12 ~ T+14 (7/25 ~ 7/27)", "x": "2cm", "y": "12cm", "size": 20, "bold": True},
        ],
    },
    # Slide 3: 三方信号监控
    {
        "title": "三方信号监控清单",
        "background": "F5F5F0",
        "shapes": [
            {"text": "通道 1 — 电话 (最高优先级)", "x": "2cm", "y": "4cm", "size": 20, "bold": True, "color": "C8102E"},
            {"text": "  · 17760348653 (主号) — 接听任何陌生号段 028/0289", "x": "2.5cm", "y": "5cm", "size": 16},
            {"text": "  · 028-86755566 四川省旅游投资集团 (核实后接)", "x": "2.5cm", "y": "6cm", "size": 16},
            {"text": "通道 2 — 短信 / 微信", "x": "2cm", "y": "7.5cm", "size": 20, "bold": True, "color": "C8102E"},
            {"text": "  · 集团内部 OA 短信 / 微信加好友申请", "x": "2.5cm", "y": "8.5cm", "size": 16},
            {"text": "  · 任何\"任前\"\"考察\"\"公示\"关键词 = 立即响应", "x": "2.5cm", "y": "9.5cm", "size": 16},
            {"text": "通道 3 — 集团 OA 系统", "x": "2cm", "y": "11cm", "size": 20, "bold": True, "color": "C8102E"},
            {"text": "  · 未注册账号 = 默认流程中", "x": "2.5cm", "y": "12cm", "size": 16},
            {"text": "  · 收到注册邀请 = 接近任命落地", "x": "2.5cm", "y": "13cm", "size": 16},
        ],
    },
    # Slide 4: 7个决策触发器
    {
        "title": "7 个决策触发器",
        "background": "FFFAF0",
        "shapes": [
            {"text": "触发 1: 接到\"任前谈话\"电话", "x": "2cm", "y": "3.5cm", "size": 18, "bold": True},
            {"text": "  → 立即确认时间地点, 准备 1244 战略 1 页摘要", "x": "2.5cm", "y": "4.3cm", "size": 14, "color": "555555"},
            {"text": "触发 2: 收到 OA 注册邀请", "x": "2cm", "y": "5.3cm", "size": 18, "bold": True},
            {"text": "  → 当天完成注册, 24h 内查看 OA 待办", "x": "2.5cm", "y": "6.1cm", "size": 14, "color": "555555"},
            {"text": "触发 3: 集团 HR 直接联系", "x": "2cm", "y": "7.1cm", "size": 18, "bold": True},
            {"text": "  → 索要任命文件, 启动报到 SOP 草案", "x": "2.5cm", "y": "7.9cm", "size": 14, "color": "555555"},
            {"text": "触发 4: 公示在集团内网可见", "x": "2cm", "y": "8.9cm", "size": 18, "bold": True},
            {"text": "  → 截图存档, 通知核心圈 (李源 / 陈思序)", "x": "2.5cm", "y": "9.7cm", "size": 14, "color": "555555"},
            {"text": "触发 5: 收到原单位 (襄阳共享维景) 任何函件", "x": "2cm", "y": "10.7cm", "size": 18, "bold": True},
            {"text": "  → 启动离职 SOP, 同步推进 CTG 交接", "x": "2.5cm", "y": "11.5cm", "size": 14, "color": "555555"},
            {"text": "触发 6: T+12 仍无任何信号", "x": "2cm", "y": "12.5cm", "size": 18, "bold": True, "color": "C8102E"},
            {"text": "  → 主动联系引荐人 / HR, 走 soft 路径核实", "x": "2.5cm", "y": "13.3cm", "size": 14, "color": "C8102E"},
            {"text": "触发 7: 收到非集团陌生邀约 (同期多家国企挖人)", "x": "2cm", "y": "14.3cm", "size": 18, "bold": True},
            {"text": "  → 暂缓所有外部洽谈, 全力等安逸", "x": "2.5cm", "y": "15.1cm", "size": 14, "color": "555555"},
        ],
    },
    # Slide 5: 行动SOP
    {
        "title": "行动 SOP · 每晚 22:00 自检",
        "background": "FFFFFF",
        "shapes": [
            {"text": "每日 22:00 三问自检 (3 分钟)", "x": "2cm", "y": "4cm", "size": 20, "bold": True, "color": "0A0E27"},
            {"text": "Q1: 今天有无任一通道的信号?", "x": "2.5cm", "y": "5cm", "size": 16},
            {"text": "Q2: 我是否已对最新信号做出 24h 响应?", "x": "2.5cm", "y": "5.8cm", "size": 16},
            {"text": "Q3: 当前 T+N, 是否触发主动联系?", "x": "2.5cm", "y": "6.6cm", "size": 16},
            {"text": "", "x": "2cm", "y": "7.6cm", "size": 14},
            {"text": "B166ER 自动监控", "x": "2cm", "y": "8.5cm", "size": 20, "bold": True, "color": "C8102E"},
            {"text": "  · 每日 22:30 自检推送 (R-CANDIDATE-T2 sharp eval)", "x": "2.5cm", "y": "9.3cm", "size": 16},
            {"text": "  · T+5 主动联系提醒 (若仍无信号)", "x": "2.5cm", "y": "10.1cm", "size": 16},
            {"text": "  · T+12 升级路径建议 (若无信号)", "x": "2.5cm", "y": "10.9cm", "size": 16},
            {"text": "", "x": "2cm", "y": "11.9cm", "size": 14},
            {"text": "联系人 (优先级降序)", "x": "2cm", "y": "12.5cm", "size": 20, "bold": True, "color": "0A0E27"},
            {"text": "  1. 集团 HR (待记)  2. 组织部 (待记)  3. 引荐人 (待记)", "x": "2.5cm", "y": "13.3cm", "size": 14, "color": "555555"},
        ],
    },
]


print("=" * 70)
print("Building D-day 等待期情报协议 v1.0")
print(f"Output: {OUTPUT}")
print("=" * 70)

result = build_pptx(str(OUTPUT), slides, verify=True)

print()
print(f"Build OK: {result['ok']}")
print(f"Total steps: {len(result['log']['steps'])}")
print(f"Errors: {len(result['log']['errors'])}")
for e in result['log']['errors'][:5]:
    print(f"  ! {e}")

if result.get('verify', {}).get('ok'):
    v = result['verify']
    print()
    print("✅ Verification (via python-pptx, bypasses officecli Chinese view bug):")
    print(f"   Size: {v['size_bytes']:,} bytes")
    print(f"   Slides: {v['slide_count']}")
    print(f"   Dimensions: {v['slide_width_emu']} × {v['slide_height_emu']} EMU")
    for slide in v['slides']:
        title_shape = next((s for s in slide['shapes'] if s.get('text')), None)
        title = title_shape['text'][:50] if title_shape else '(no text)'
        text_count = sum(1 for s in slide['shapes'] if s.get('type') == 'text')
        print(f"   Slide {slide['index']}: {text_count} text shapes | title='{title}...'")
else:
    print()
    print(f"❌ Verification failed: {result.get('verify', {}).get('error')}")

print()
print("=" * 70)
print(f"File: {OUTPUT}")
print("=" * 70)