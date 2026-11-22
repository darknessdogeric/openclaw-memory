import json

predictions = [
    {
        "date": "2026-07-26",
        "topic": "US_Iran",
        "label": "暂停-反转窗口",
        "trump_action": "7/25下令暂停空袭伊朗,结束13天连续打击",
        "israel_action": "内塔尼亚胡7/28访美递交伊朗核情报",
        "scenario_prob": {"baseline_pause_persist": 0.60, "escalation_resume": 0.30, "breakthrough": 0.25},
        "oil_target": "WTI 85-92区间震荡;暂停持续则下沿82-85,重启打击则跳涨至100+",
        "confidence": 0.72,
        "source": "B166ER综合判断 2026-07-26"
    },
    {
        "date": "2026-07-26",
        "WTI_close": 89.31,
        "Brent_close": 96.78,
        "direction": "周累计暴涨后技术性回调",
        "weekly_WTI": "+8.27%",
        "weekly_Brent": "+9.85%",
        "China_retail_gas": "7/31预计上调超0.7元/升",
        "trigger": "特朗普暂停空袭+OPEC+8/2会议增产预期",
        "upside_target": "WTI 100+ 若7/28以方情报推动美重启打击",
        "downside_risk": "WTI 78-80 若谈判实质突破",
        "confidence": 0.75,
        "source": "qq.com/腾讯证券 7/26"
    },
    {
        "date": "2026-07-26",
        "model": "DeepSeek V4 满血版",
        "release_window": "预计7/28-7/30发布",
        "performance": "逼近Claude Opus 4.8",
        "Agent_capability": "明显跃升+3D场景生成/SVG渲染提升",
        "pricing": "七分之一国际竞品价格+峰谷定价机制",
        "params_V4Pro": "总参1.6万亿/激活490亿(MoE)",
        "direction": "AHL边际成本再降20-30%",
        "action": "V4发布后48h评估在AHL多Agent架构中的角色",
        "confidence": 0.78,
        "source": "qq.com 7/20-7/26"
    },
    {
        "date": "2026-07-26",
        "Shanghai_Composite": "3800点保卫战",
        "close_7_24": "3814.20 (-1.61%)",
        "volume_7_24": "19312亿 (时隔多月跌破2万亿)",
        "down_stocks": 4900,
        "baseline": "3800点短期支撑有效,需观察量能配合",
        "downside": "若跌破3760进入技术性回调",
        "upside": "半导体设备逆势+3.18% 提供结构性机会",
        "Fed_FOMC_7_29_30": "维持利率不变概率85.6%,9月加息25bp概率53.5%",
        "confidence": 0.70,
        "source": "东方财富/国际金融要情 7/24-7/26"
    },
    {
        "date": "2026-07-26",
        "Hotel_REITs": "双轨期确立",
        "inter_institutional": "远洲集团21.51亿(上交所过审,首单完整走完流程)",
        "public_offering": "华安锦江17.03亿(证监会通过6/23)",
        "dist_rate": "5.05%(华安锦江2026净现金流分派率)",
        "Implication_for_AnYi": "酒店资产证券化窗口期持续→1244战略退出渠道验证",
        "next_window": "2027-2028年是酒店REITs密集发行期",
        "confidence": 0.82,
        "source": "观点网/中证报 7/14-7/26"
    }
]

with open(r"D:\B166ER-OpenClaw\workspace\memory\predictions\macro.jsonl", "a", encoding="utf-8") as f:
    for p in predictions:
        f.write(json.dumps(p, ensure_ascii=False) + "\n")

print(f"Appended {len(predictions)} predictions")