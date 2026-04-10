#!/usr/bin/env python3
"""
酒店收益管理综合工具 (Hotel Revenue Management Tool)
版本: V1.0
创建: 2026-04-03
功能: ADR估算/OCC预测/动态定价/竞品分析
"""

import json
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

# ============================================================
# 核心数据模型
# ============================================================

@dataclass
class RoomType:
    """房型"""
    name: str
    total_rooms: int
    base_adr: float
    rack_rate: float

@dataclass
class ChannelData:
    """渠道数据"""
    channel: str           # ota/wechat/official
    adr: float             # 净价
    volume_ratio: float    # 间夜占比
    commission_rate: float # 佣金率

@dataclass
class MarketEvent:
    """市场事件"""
    date: str
    name: str
    impact: float          # 影响系数 (>1涨价, <1跌价)
    days_affected: int = 3

# ============================================================
# ADR反推模型
# ============================================================

class ADREstimator:
    """
    ADR反推模型
    功能: 从OTA展示价反推酒店真实ADR
    
    公式: 真实ADR = Σ(渠道占比 × 渠道净价格)
    折扣率: 经济型80%/中端75%/高端70%/奢华65%
    """
    
    DISCOUNT_RATES = {
        "budget": 0.80,    # 经济型
        "midscale": 0.75,  # 中端
        " upscale": 0.70,  # 高端
        "luxury": 0.65     # 奢华
    }
    
    def __init__(self, hotel_class: str = "midscale"):
        self.hotel_class = hotel_class
        self.discount = self.DISCOUNT_RATES.get(hotel_class, 0.75)
    
    def ota_to_net(self, ota_price: float, commission_rate: float = 0.15) -> float:
        """OTA展示价 → 净价格"""
        return ota_price * (1 - commission_rate)
    
    def rack_to_net(self, rack_rate: float) -> float:
        """挂牌价 → 净价格"""
        return rack_rate * self.discount
    
    def estimate_real_adr(self, channels: List[ChannelData]) -> float:
        """
        综合多渠道估算真实ADR
        
        channels: List[ChannelData] - 各渠道数据
        """
        total_adr = 0.0
        
        for ch in channels:
            # 计算净价格
            if ch.channel == "ota":
                net_price = self.ota_to_net(ch.adr)
            elif ch.channel == "official":
                net_price = ch.adr
            else:  # wechat/private
                net_price = ch.adr
            
            # 加权求和
            total_adr += net_price * ch.volume_ratio
        
        return round(total_adr, 2)
    
    def print_analysis(self, channels: List[ChannelData]):
        """打印分析报告"""
        print(f"\n{'='*60}")
        print(f"ADR反推分析报告")
        print(f"{'='*60}")
        print(f"酒店档次: {self.hotel_class}")
        print(f"折扣率: {self.discount:.0%}")
        print()
        
        print("【渠道明细】")
        total_volume = 0
        weighted_adr = 0.0
        
        for ch in channels:
            if ch.channel == "ota":
                net = self.ota_to_net(ch.adr)
            else:
                net = ch.adr
            
            volume_adr = net * ch.volume_ratio
            total_volume += ch.volume_ratio
            weighted_adr += volume_adr
            
            print(f"  {ch.channel:10s} | 展示价: ¥{ch.adr:>6.0f} | 净价: ¥{net:>6.0f} | 占比: {ch.volume_ratio:>5.1%}")
        
        real_adr = self.estimate_real_adr(channels)
        print()
        print(f"【估算结果】")
        print(f"  加权真实ADR: ¥{real_adr:.2f}")
        print(f"  渠道贡献占比: {total_volume:.1%}")

# ============================================================
# OCC估算模型
# ============================================================

class OCCEstimator:
    """
    入住率(OCC)估算模型
    功能: 基于多信号加权估算酒店入住率
    
    公式: OCC = Σ(信号权重 × 信号OCC) × 0.75 + 基线OCC × 0.25
    
    公开信源:
    - OTA库存状态（可售房间数）
    - 微信订房进度
    - 官网直销数据
    - 市场事件（展会/节假日/天气）
    """
    
    def __init__(self, baseline_occ: float = 0.70):
        self.baseline_occ = baseline_occ
    
    def estimate_from_ota(self, total_rooms: int, 
                         available_rooms: int,
                         trend_factor: float = 1.0) -> float:
        """
        基于OTA库存估算OCC
        
        total_rooms: 总房间数
        available_rooms: 可售房间数
        trend_factor: 趋势因子（>1表示上涨趋势）
        """
        if available_rooms >= total_rooms:
            return 0.0
        
        raw_occ = (total_rooms - available_rooms) / total_rooms
        adjusted_occ = raw_occ * trend_factor
        
        return min(0.95, max(0, adjusted_occ))
    
    def estimate_from_booking_progress(self, total_rooms: int,
                                      booked_rooms: int,
                                      days_to_arrival: int,
                                      historical_pickup_rate: float = 0.3) -> float:
        """
        基于预订进度估算OCC
        
        booked_rooms: 已预订房间数
        days_to_arrival: 距入住天数
        historical_pickup_rate: 历史取消率/未到率
        """
        # 预计最终入住 = 当前预订 + 预计增量
        expected_final = booked_rooms + (days_to_arrival * historical_pickup_rate * total_rooms)
        expected_final = min(expected_final, total_rooms)
        
        return expected_final / total_rooms
    
    def estimate_with_events(self, base_occ: float,
                           events: List[MarketEvent],
                           target_date: str) -> float:
        """
        结合市场事件调整OCC估算
        
        events: 市场事件列表
        target_date: 目标日期
        """
        adjusted_occ = base_occ
        
        for event in events:
            if event.date == target_date:
                adjusted_occ *= event.impact
        
        return min(0.98, adjusted_occ)
    
    def weighted_estimate(self, signals: Dict[str, Tuple[float, float]]) -> float:
        """
        多信号加权估算
        
        signals: Dict[str, Tuple[occ, weight]]
        例: {"ota": (0.75, 0.4), "wechat": (0.70, 0.3), "event": (0.80, 0.3)}
        """
        total_weight = 0.0
        weighted_sum = 0.0
        
        for source, (occ, weight) in signals.items():
            weighted_sum += occ * weight
            total_weight += weight
        
        if total_weight == 0:
            return self.baseline_occ
        
        # 混合基线
        signal_avg = weighted_sum / total_weight
        final_occ = signal_avg * 0.75 + self.baseline_occ * 0.25
        
        return round(final_occ, 4)
    
    def print_analysis(self, signals: Dict[str, Tuple[float, float]]):
        """打印分析报告"""
        print(f"\n{'='*60}")
        print(f"OCC入住率估算报告")
        print(f"{'='*60}")
        print(f"基线OCC: {self.baseline_occ:.1%}")
        print()
        
        print("【信号明细】")
        for source, (occ, weight) in signals.items():
            print(f"  {source:15s} | OCC: {occ:.1%} | 权重: {weight:.1%}")
        
        final = self.weighted_estimate(signals)
        print()
        print(f"【估算结果】")
        print(f"  综合OCC: {final:.1%}")
        print(f"  预计间夜: {int(final * 100)} 间（假设100间）")

# ============================================================
# 动态定价模型
# ============================================================

class DynamicPricing:
    """
    动态定价模型
    功能: 基于需求系数/竞争系数/时间系数计算最优房价
    
    最优价格 = 基础ADR × 需求系数 × 竞争系数 × 时间系数 × 事件系数
    """
    
    def __init__(self, base_adr: float = 500):
        self.base_adr = base_adr
    
    def demand_factor(self, occ: float, target_occ: float = 0.75) -> float:
        """
        需求系数
        occ: 当前估算入住率
        target_occ: 目标入住率
        """
        if occ < target_occ:
            # 低于目标，稍微降价
            ratio = occ / target_occ
            return 0.85 + 0.15 * ratio
        else:
            # 高于目标，溢价
            ratio = occ / target_occ
            return min(1.5, 1.0 + 0.5 * (ratio - 1))
    
    def competition_factor(self, our_adr: float, comp_adr: float) -> float:
        """
        竞争系数
        our_adr: 我方ADR
        comp_adr: 竞品ADR
        """
        if comp_adr == 0:
            return 1.0
        
        ratio = our_adr / comp_adr
        
        # 我们比竞品便宜 → 可以提价
        if ratio < 0.9:
            return 1.1
        # 我们比竞品贵很多 → 需要降价
        elif ratio > 1.2:
            return 0.9
        else:
            return 1.0
    
    def time_factor(self, days_to_arrival: int) -> float:
        """
        时间系数
        days_to_arrival: 距入住天数
        """
        if days_to_arrival <= 1:
            return 1.3   # 当天高价
        elif days_to_arrival <= 3:
            return 1.15
        elif days_to_arrival <= 7:
            return 1.0
        elif days_to_arrival <= 14:
            return 0.95
        else:
            return 0.9   # 提前预订优惠
    
    def event_factor(self, event: MarketEvent) -> float:
        """事件系数"""
        return event.impact if event else 1.0
    
    def calculate_optimal_price(self,
                                base_adr: float,
                                occ: float,
                                comp_adr: float = 0,
                                days_to_arrival: int = 7,
                                event: MarketEvent = None) -> Dict:
        """计算最优价格"""
        d_factor = self.demand_factor(occ)
        c_factor = self.competition_factor(base_adr, comp_adr) if comp_adr else 1.0
        t_factor = self.time_factor(days_to_arrival)
        e_factor = self.event_factor(event)
        
        optimal = base_adr * d_factor * c_factor * t_factor * e_factor
        
        return {
            "base_adr": base_adr,
            "optimal_price": round(optimal, 0),
            "demand_factor": round(d_factor, 3),
            "competition_factor": round(c_factor, 3),
            "time_factor": round(t_factor, 3),
            "event_factor": round(e_factor, 3),
            "price_range": {
                "min": round(optimal * 0.85, 0),
                "max": round(optimal * 1.15, 0)
            }
        }
    
    def print_pricing(self, result: Dict):
        """打印定价报告"""
        print(f"\n{'='*60}")
        print(f"动态定价分析报告")
        print(f"{'='*60}")
        print(f"基础ADR: ¥{result['base_adr']:.0f}")
        print()
        
        print("【系数明细】")
        print(f"  需求系数: {result['demand_factor']:.3f}")
        print(f"  竞争系数: {result['competition_factor']:.3f}")
        print(f"  时间系数: {result['time_factor']:.3f}")
        print(f"  事件系数: {result['event_factor']:.3f}")
        
        print()
        print(f"【定价结果】")
        print(f"  最优价格: ¥{result['optimal_price']:.0f}")
        print(f"  价格区间: ¥{result['price_range']['min']:.0f} - ¥{result['price_range']['max']:.0f}")

# ============================================================
# 竞品分析工具
# ============================================================

class CompetitorAnalysis:
    """竞品分析"""
    
    def __init__(self):
        self.competitors = []
    
    def add_competitor(self, name: str, adr: float, occ: float, 
                       rating: float, revpar: float):
        """添加竞品"""
        self.competitors.append({
            "name": name,
            "adr": adr,
            "occ": occ,
            "rating": rating,
            "revpar": revpar
        })
    
    def compare(self, our_adr: float, our_occ: float) -> Dict:
        """与竞品对比"""
        if not self.competitors:
            return {"message": "没有竞品数据"}
        
        avg_adr = sum(c["adr"] for c in self.competitors) / len(self.competitors)
        avg_occ = sum(c["occ"] for c in self.competitors) / len(self.competitors)
        avg_revpar = sum(c["revpar"] for c in self.competitors) / len(self.competitors)
        
        our_revpar = our_adr * our_occ
        
        return {
            "our_adr": our_adr,
            "our_occ": our_occ,
            "our_revpar": our_revpar,
            "comp_avg_adr": round(avg_adr, 2),
            "comp_avg_occ": round(avg_occ, 4),
            "comp_avg_revpar": round(avg_revpar, 2),
            "adr_position": "above" if our_adr > avg_adr else "below",
            "revpar_position": "above" if our_revpar > avg_revpar else "below",
            "gap": round(our_revpar - avg_revpar, 2)
        }
    
    def print_analysis(self, our_adr: float, our_occ: float):
        """打印竞品分析"""
        result = self.compare(our_adr, our_occ)
        
        print(f"\n{'='*60}")
        print(f"竞品对比分析报告")
        print(f"{'='*60}")
        
        print("\n【竞品明细】")
        for c in self.competitors:
            print(f"  {c['name']}: ADR ¥{c['adr']:.0f} | OCC {c['occ']:.1%} | RevPAR ¥{c['revpar']:.0f} | 评分 {c['rating']}")
        
        print("\n【我方数据】")
        print(f"  ADR ¥{result['our_adr']:.0f} | OCC {result['our_occ']:.1%} | RevPAR ¥{result['our_revpar']:.0f}")
        
        print("\n【市场均值】")
        print(f"  ADR ¥{result['comp_avg_adr']:.0f} | OCC {result['comp_avg_occ']:.1%} | RevPAR ¥{result['comp_avg_revpar']:.0f}")
        
        print("\n【定位判断】")
        print(f"  ADR定位: {'高于均值' if result['adr_position'] == 'above' else '低于均值'}")
        print(f"  RevPAR差距: ¥{result['gap']:.0f} ({'领先' if result['gap'] > 0 else '落后'})")

# ============================================================
# 主程序
# ============================================================

def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════════╗
║            酒店收益管理综合工具 v1.0                          ║
║            Hotel Revenue Management Tool                     ║
╠══════════════════════════════════════════════════════════════╣
║  功能: ADR反推 | OCC估算 | 动态定价 | 竞品分析              ║
║  核心: 收益管理三角 (ADR × OCC = RevPAR)                    ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def demo():
    """演示模式"""
    print("\n【ADR反推演示】")
    channels = [
        ChannelData("ota", 450, 0.5, 0.15),
        ChannelData("wechat", 380, 0.2, 0.05),
        ChannelData("official", 420, 0.3, 0.0)
    ]
    adr_est = ADREstimator("midscale")
    adr_est.print_analysis(channels)
    
    print("\n【OCC估算演示】")
    signals = {
        "OTA库存": (0.78, 0.40),
        "微信预订": (0.72, 0.25),
        "官网直销": (0.68, 0.20),
        "市场事件": (0.85, 0.15)
    }
    occ_est = OCCEstimator(baseline_occ=0.70)
    occ_est.print_analysis(signals)
    
    print("\n【动态定价演示】")
    pricing = DynamicPricing(base_adr=500)
    result = pricing.calculate_optimal_price(
        base_adr=500,
        occ=0.78,
        comp_adr=480,
        days_to_arrival=3,
        event=MarketEvent("2026-04-04", "清明假期", 1.2)
    )
    pricing.print_pricing(result)
    
    print("\n【竞品分析演示】")
    comp = CompetitorAnalysis()
    comp.add_competitor("全季酒店", 420, 0.82, 4.6, 344)
    comp.add_competitor("亚朵酒店", 480, 0.75, 4.7, 360)
    comp.add_competitor("桔子酒店", 400, 0.78, 4.5, 312)
    comp.print_analysis(our_adr=450, our_occ=0.76)

def main():
    print_banner()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "demo":
            demo()
        elif command == "adr":
            # ADR计算
            print("\n请输入OTA展示价和佣金率（逗号分隔）:")
            try:
                price, commission = input("> ").split(",")
                price = float(price.strip())
                commission = float(commission.strip())
                
                est = ADREstimator()
                net = est.ota_to_net(price, commission)
                print(f"净价格: ¥{net:.2f}")
            except ValueError:
                print("输入格式错误，请输入: 价格,佣金率")
        elif command == "occ":
            # OCC计算
            print("\n请输入 (总房间,已售房间,趋势因子)：")
            try:
                total, sold, trend = input("> ").split(",")
                total = int(total.strip())
                sold = int(sold.strip())
                trend = float(trend.strip())
                
                est = OCCEstimator()
                occ = est.estimate_from_ota(total, sold, trend)
                print(f"估算OCC: {occ:.1%}")
            except ValueError:
                print("输入格式错误")
        elif command == "help":
            print("""
用法:
  python hotel_revenue_tool.py          # 显示此帮助
  python hotel_revenue_tool.py demo    # 运行演示
  python hotel_revenue_tool.py adr     # ADR计算
  python hotel_revenue_tool.py occ     # OCC估算
  python hotel_revenue_tool.py help    # 显示帮助

命令说明:
  demo   - 运行完整演示（ADR+OCC+定价+竞品）
  adr    - 从OTA价反推真实ADR
  occ    - 从OTA库存估算入住率
  pricing - 动态定价计算
  comp   - 竞品对比分析
            """)
        else:
            print(f"未知命令: {command}")
    else:
        demo()

if __name__ == "__main__":
    main()
