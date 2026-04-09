#!/usr/bin/env python3
"""
酒店收益管理实战检查工具 (Hotel Revenue Management Checklist)
版本: V1.0
创建: 2026-04-03
功能: 酒店收益管理日常工作检查清单
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# ============================================================
# 核心检查模块
# ============================================================

class RevenueChecklist:
    """收益管理日常检查清单"""
    
    def __init__(self, total_rooms: int = 100, baseline_occ: float = 0.70):
        self.total_rooms = total_rooms
        self.baseline_occ = baseline_occ
        self.baseline_adr = 400
    
    def daily_check(self, today_occ: float, today_adr: float,
                   tomorrow_occ: float, tomorrow_adr: float,
                   week_occ: float, week_adr: float,
                   comp_avg_adr: float = 0) -> Dict:
        """
        每日收益检查
        
        参数:
            today_occ: 今日入住率
            today_adr: 今日ADR
            tomorrow_occ: 明日入住率
            tomorrow_adr: 明日ADR
            week_occ: 本周平均入住率
            week_adr: 本周平均ADR
            comp_avg_adr: 竞品平均ADR
        """
        results = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "today": {},
            "tomorrow": {},
            "week": {},
            "alerts": [],
            "actions": []
        }
        
        # 今日检查
        results["today"] = {
            "occ": today_occ,
            "adr": today_adr,
            "revpar": round(today_occ * today_adr, 2),
            "status": self._occ_status(today_occ)
        }
        
        # 明日预测检查
        results["tomorrow"] = {
            "occ": tomorrow_occ,
            "adr": tomorrow_adr,
            "revpar": round(tomorrow_occ * tomorrow_adr, 2),
            "action": self._tomorrow_action(tomorrow_occ, tomorrow_adr)
        }
        
        # 本周趋势
        results["week"] = {
            "avg_occ": week_occ,
            "avg_adr": week_adr,
            "revpar": round(week_occ * week_adr, 2),
            "trend": self._week_trend(week_occ, week_adr)
        }
        
        # 竞品对标
        if comp_avg_adr > 0:
            gap = today_adr - comp_avg_adr
            results["competitor"] = {
                "comp_adr": comp_avg_adr,
                "gap": gap,
                "position": "above" if gap > 0 else "below",
                "action": "可提价" if gap > 20 else ("需优化" if gap < -20 else "保持")
            }
        
        # 生成告警
        self._generate_alerts(results)
        
        # 生成行动建议
        self._generate_actions(results)
        
        return results
    
    def _occ_status(self, occ: float) -> str:
        """入住率状态判断"""
        if occ < 0.5:
            return "🔴 低入住 - 需促销"
        elif occ < 0.7:
            return "🟡 中入住 - 关注渠道"
        elif occ < 0.85:
            return "🟢 正常 - 维护价格"
        elif occ < 0.95:
            return "🟠 高入住 - 可溢价"
        else:
            return "🔴 满房 - 超卖检查"
    
    def _tomorrow_action(self, occ: float, adr: float) -> str:
        """明日行动建议"""
        if occ < 0.5:
            return "启动last-minute促销，提高入住率"
        elif occ < 0.7:
            return "检查渠道，打开OTA促销开关"
        elif occ < 0.85:
            return "维持当前价格，可小幅溢价"
        elif occ < 0.95:
            return "检查升级销售，提升ADR"
        else:
            return "满房，检查超额预订，准备候补"
    
    def _week_trend(self, occ: float, adr: float) -> str:
        """本周趋势"""
        expected_occ = self.baseline_occ
        expected_adr = self.baseline_adr
        
        occ_ratio = occ / expected_occ if expected_occ > 0 else 1
        adr_ratio = adr / expected_adr if expected_adr > 0 else 1
        
        if occ_ratio > 1.1 and adr_ratio > 1.05:
            return "📈 超出预期，超量完成"
        elif occ_ratio > 1.0 and adr_ratio > 1.0:
            return "✅ 符合预期，稳中有升"
        elif occ_ratio < 0.8:
            return "⚠️ 低于预期，需分析原因"
        else:
            return "➡️ 基本符合预期"
    
    def _generate_alerts(self, results: Dict):
        """生成告警"""
        today = results["today"]
        
        if today["occ"] < 0.5:
            results["alerts"].append({
                "level": "red",
                "msg": f"今日入住率{today['occ']:.0%}过低，需立即采取行动"
            })
        elif today["occ"] > 0.95 and today["occ"] < 1.0:
            results["alerts"].append({
                "level": "orange",
                "msg": "明日高入住，需检查超额预订和候补名单"
            })
        
        if "competitor" in results:
            gap = results["competitor"]["gap"]
            if gap < -50:
                results["alerts"].append({
                    "level": "red",
                    "msg": f"ADR落后竞品{abs(gap)}元，需检查定价策略"
                })
    
    def _generate_actions(self, results: Dict):
        """生成行动建议"""
        today_occ = results["today"]["occ"]
        tomorrow_occ = results["tomorrow"]["occ"]
        
        # 即时行动
        if today_occ < 0.6:
            results["actions"].extend([
                "□ 打开OTA促销开关（连住优惠、提前预订优惠）",
                "□ 联系协议客户，主动推销今日可用房",
                "□ 检查OTA房价是否有下调空间"
            ])
        
        if tomorrow_occ < 0.5:
            results["actions"].extend([
                "□ 明日为last-minute促销日",
                "□ 联系团队客户，看能否临时增加预订",
                "□ 考虑下调明日价格吸引walk-in"
            ])
        
        # 常规行动
        results["actions"].extend([
            "□ 检查明日预订进度，对比历史同期",
            "□ 监控竞品价格变化",
            "□ 更新收益管理系统数据"
        ])
    
    def channel_analysis(self, channel_data: List[Dict]) -> Dict:
        """
        渠道分析
        
        channel_data: [
            {"name": "携程", "rooms": 30, "adr": 420, "commission": 0.15},
            {"name": "美团", "rooms": 20, "adr": 380, "commission": 0.12},
            {"name": "官网", "rooms": 15, "adr": 450, "commission": 0.05},
            {"name": "企业协议", "rooms": 25, "adr": 350, "commission": 0.10},
        ]
        """
        total_rooms = sum(c["rooms"] for c in channel_data)
        total_revenue = sum(c["rooms"] * c["adr"] for c in channel_data)
        
        results = {
            "channels": [],
            "summary": {},
            "recommendations": []
        }
        
        for ch in channel_data:
            net_adr = ch["adr"] * (1 - ch["commission"])
            revenue = ch["rooms"] * net_adr
            share = ch["rooms"] / total_rooms if total_rooms > 0 else 0
            
            results["channels"].append({
                "name": ch["name"],
                "rooms": ch["rooms"],
                "adr": ch["adr"],
                "net_adr": round(net_adr, 2),
                "revenue": round(revenue, 2),
                "share": f"{share:.1%}",
                "commission_cost": round(ch["rooms"] * ch["adr"] * ch["commission"], 2)
            })
        
        results["summary"] = {
            "total_rooms": total_rooms,
            "total_revenue": round(total_revenue, 2),
            "avg_adr": round(total_revenue / total_rooms, 2) if total_rooms > 0 else 0,
            "channel_count": len(channel_data)
        }
        
        # 建议
        high_commission = [c for c in results["channels"] if c["adr"] < 400 and c["name"] in ["携程", "美团"]]
        if high_commission:
            results["recommendations"].append(
                f"⚠️ 高佣金渠道（佣金>10%）贡献了{sum(c['rooms'] for c in high_commission)}间夜，需评估是否继续合作"
            )
        
        return results
    
    def pricing_decision(self, base_adr: float, occ: float,
                         comp_adr: float, days_to_arrival: int) -> Dict:
        """
        定价决策辅助
        
        返回建议价格区间
        """
        # 基础价格
        base_price = base_adr
        
        # 入住率调整
        if occ < 0.5:
            occ_adjust = 0.85  # 降价
        elif occ < 0.7:
            occ_adjust = 0.95
        elif occ < 0.85:
            occ_adjust = 1.0
        elif occ < 0.95:
            occ_adjust = 1.15
        else:
            occ_adjust = 1.3
        
        # 竞品调整
        if comp_adr > 0:
            comp_ratio = base_price / comp_adr
            if comp_ratio < 0.85:
                comp_adjust = 1.1  # 我们便宜太多，可以提价
            elif comp_ratio > 1.15:
                comp_adjust = 0.9  # 我们太贵
            else:
                comp_adjust = 1.0
        
        # 时间调整
        if days_to_arrival <= 1:
            time_adjust = 1.2
        elif days_to_arrival <= 3:
            time_adjust = 1.1
        elif days_to_arrival <= 7:
            time_adjust = 1.0
        else:
            time_adjust = 0.95
        
        optimal = base_price * occ_adjust * comp_adjust * time_adjust
        
        return {
            "base_adr": base_adr,
            "optimal_price": round(optimal, 0),
            "price_range": {
                "min": round(optimal * 0.9, 0),
                "max": round(optimal * 1.1, 0)
            },
            "adjustments": {
                "occ": occ_adjust,
                "comp": comp_adjust if comp_adr > 0 else 1.0,
                "time": time_adjust
            },
            "recommendation": f"建议定价 ¥{round(optimal, 0)}（区间 ¥{round(optimal*0.9,0)}-{round(optimal*1.1,0)}）"
        }

# ============================================================
# 酒店收益管理关键指标速查
# ============================================================

REVENUE_KPIS = {
    "ADR": {
        "name": "平均房价",
        "formula": "总客房收入 / 已售客房数",
        "normal_range": "城市酒店 ¥300-800，中端 ¥200-400",
        "action_trigger": "ADR低于竞争对手20元以上"
    },
    "OCC": {
        "name": "入住率",
        "formula": "已售客房数 / 可售客房总数",
        "normal_range": "商务70-85%，度假60-80%",
        "action_trigger": "OCC低于预算5%以上"
    },
    "RevPAR": {
        "name": "每房收益",
        "formula": "ADR × OCC 或 总收入 / 可售客房总数",
        "normal_range": "城市中端 ¥200-400",
        "action_trigger": "RevPAR低于市场均值10%以上"
    },
    "GOP": {
        "name": "经营毛利率",
        "formula": "(总收入 - 经营成本) / 总收入",
        "normal_range": "30-45%",
        "action_trigger": "GOP低于预算3%以上"
    },
    "Porter": {
        "name": "双胞率",
        "formula": "同一房间两个订单 / 总预订数",
        "normal_range": "<2%",
        "action_trigger": "双胞率超过3%"
    }
}

# ============================================================
# 携程/美团/Booking运营检查表
# ============================================================

OTA_CHECKLIST = {
    "携程EBK": [
        "□ 今日价格是否具有竞争力？",
        "□ 挂牌等级是否最新？（特牌/金牌/银牌）",
        "□ 今日可售房量是否准确？",
        "□ 保留房政策是否设置正确？",
        "□ 评价回复率是否>90%？",
        "□ 今日差评是否已处理？",
        "□ 促销活动是否报名（连住/提前订）？"
    ],
    "美团酒店": [
        "□ 今日价格是否低于携程？",
        "□ 酒店星级/钻级是否正确？",
        "□ 今日可售库存是否同步？",
        "□ 美团专属价是否设置？",
        "□ 客人点评是否回复？"
    ],
    "Booking.com": [
        "□ Booking价格是否与国际接轨？",
        "□ 取消政策是否灵活？",
        "□ Genius会员折扣是否参加？",
        "□ 评分数是否>8.0？",
        "□ 照片是否每6个月更新？"
    ],
    "官网/微信": [
        "□ 官网价格是否最优（比OTA低5-10%）？",
        "□ 是否有会员专属价？",
        "□ 是否有官网独享优惠（免费升房）？",
        "□ 微信订阅号是否推送促销？"
    ]
}

# ============================================================
# 主程序
# ============================================================

def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════════╗
║            酒店收益管理实战检查工具 v1.0                   ║
║            Hotel Revenue Management Checklist               ║
╠══════════════════════════════════════════════════════════════╣
║  功能: 每日检查 | 渠道分析 | 定价决策 | OTA检查表           ║
║  核心: ADR × OCC = RevPAR = 每房收益                      ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    print_banner()
    
    print("\n【用法说明】")
    print("本工具提供三种模式：")
    print("1. daily  - 每日收益检查")
    print("2. channel - 渠道分析")
    print("3. pricing - 定价决策")
    print("4. checklist - OTA检查表")
    print()
    print("Python调用示例:")
    print("""
from hotel_revenue_checklist_tool import RevenueChecklist

rc = RevenueChecklist(total_rooms=100, baseline_occ=0.75)

# 每日检查
result = rc.daily_check(
    today_occ=0.78, today_adr=420,
    tomorrow_occ=0.65, tomorrow_adr=400,
    week_occ=0.72, week_adr=410,
    comp_avg_adr=400
)
print(json.dumps(result, indent=2, ensure_ascii=False))

# 定价决策
price = rc.pricing_decision(
    base_adr=400, occ=0.78,
    comp_adr=380, days_to_arrival=3
)
print(price['recommendation'])
    """)

if __name__ == "__main__":
    main()
