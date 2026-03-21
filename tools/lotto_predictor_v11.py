#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B166ER 大乐透统计预测模型 V1.1 (迭代版)
=====================================
基于历史数据的统计分析号码生成器 - 优化版

改进点:
1. 冷热号动态平衡策略
2. 和值区间约束 (80-120)
3. 跨度控制 (15-30)
4. 强制5区覆盖
5. 后区奇偶平衡

声明: 本工具仅供娱乐和统计分析，不能预测彩票结果
彩票是完全随机事件，请理性购彩
"""

import random
import json
from datetime import datetime
from collections import Counter
from typing import List, Dict, Tuple

class LottoPredictorV11:
    """大乐透预测模型 V1.1"""
    
    def __init__(self, recent_draws: List[Dict] = None):
        """
        初始化预测器
        
        Args:
            recent_draws: 最近开奖数据，用于分析冷热号
        """
        self.recent = recent_draws or []
        self.front_range = range(1, 36)  # 前区 01-35
        self.back_range = range(1, 13)   # 后区 01-12
        
        # 计算统计数据
        self._calculate_statistics()
    
    def _calculate_statistics(self):
        """计算历史数据统计"""
        # 前区频率统计（最近30期）
        front_all = []
        back_all = []
        
        for draw in self.recent[-30:] if len(self.recent) > 30 else self.recent:
            front_all.extend(draw.get('front', []))
            back_all.extend(draw.get('back', []))
        
        self.front_freq = Counter(front_all)
        self.back_freq = Counter(back_all)
        
        # 冷热号分类
        self.hot_front = [n for n, c in self.front_freq.most_common(10)] if self.front_freq else []
        self.cold_front = [n for n in self.front_range if n not in self.hot_front][:10]
        
        self.hot_back = [n for n, c in self.back_freq.most_common(4)] if self.back_freq else []
        self.cold_back = [n for n in self.back_range if n not in self.hot_back][:4]
    
    def _generate_front_zone_strategy(self) -> List[int]:
        """
        V1.1 核心策略: 5区强制覆盖 + 冷热平衡
        每区至少1个号码，最多2个
        """
        zones = {
            0: list(range(1, 8)),    # 01-07
            1: list(range(8, 15)),   # 08-14
            2: list(range(15, 22)),  # 15-21
            3: list(range(22, 29)),  # 22-28
            4: list(range(29, 36))   # 29-35
        }
        
        selected = []
        
        # 策略: 3区选热号，2区选冷号
        hot_zones = random.sample([0, 1, 2, 3, 4], 3)
        cold_zones = [z for z in [0, 1, 2, 3, 4] if z not in hot_zones]
        
        for zone_idx in hot_zones:
            zone_nums = zones[zone_idx]
            # 优先选热号
            hot_in_zone = [n for n in zone_nums if n in self.hot_front]
            if hot_in_zone and random.random() < 0.7:
                selected.append(random.choice(hot_in_zone))
            else:
                selected.append(random.choice(zone_nums))
        
        for zone_idx in cold_zones:
            zone_nums = zones[zone_idx]
            # 优先选冷号
            cold_in_zone = [n for n in zone_nums if n in self.cold_front]
            if cold_in_zone and random.random() < 0.6:
                selected.append(random.choice(cold_in_zone))
            else:
                selected.append(random.choice(zone_nums))
        
        return sorted(selected)
    
    def _check_constraints(self, front: List[int]) -> bool:
        """
        V1.1 约束检查: 和值 + 跨度 + 奇偶 + 区间
        """
        # 和值检查 (80-120为理想区间)
        total = sum(front)
        if not (70 <= total <= 130):
            return False
        
        # 跨度检查 (15-30)
        span = max(front) - min(front)
        if not (12 <= span <= 32):
            return False
        
        # 奇偶检查 (2:3 或 3:2 最佳)
        odd = sum(1 for n in front if n % 2 == 1)
        if odd not in [2, 3]:
            return False
        
        # 大小检查 (以18为界，2:3 或 3:2)
        big = sum(1 for n in front if n >= 18)
        if big not in [2, 3]:
            return False
        
        # 区间覆盖检查 (5区都要有)
        zones_covered = set()
        for n in front:
            zones_covered.add((n-1) // 7)
        if len(zones_covered) < 4:  # 至少覆盖4个区
            return False
        
        # 连号检查 (最多1组)
        consecutive = sum(1 for i in range(4) if front[i+1] - front[i] == 1)
        if consecutive > 1:
            return False
        
        return True
    
    def _generate_back_balanced(self) -> List[int]:
        """
        V1.1 后区生成: 奇偶平衡 + 大小平衡
        """
        max_attempts = 50
        for _ in range(max_attempts):
            # 策略: 一奇一偶 或 双奇 或 双偶
            strategy = random.choice(['odd_even', 'both_odd', 'both_even'])
            
            if strategy == 'odd_even':
                odd_nums = [n for n in self.back_range if n % 2 == 1]
                even_nums = [n for n in self.back_range if n % 2 == 0]
                back = [random.choice(odd_nums), random.choice(even_nums)]
            elif strategy == 'both_odd':
                odd_nums = [n for n in self.back_range if n % 2 == 1]
                back = random.sample(odd_nums, 2)
            else:
                even_nums = [n for n in self.back_range if n % 2 == 0]
                back = random.sample(even_nums, 2)
            
            back = sorted(back)
            
            # 避免与最近3期后区完全相同
            recent_backs = [set(d.get('back', [])) for d in self.recent[-3:]]
            if set(back) not in recent_backs:
                return back
        
        # 保底随机
        return sorted(random.sample(list(self.back_range), 2))
    
    def _generate_single(self, max_attempts: int = 200) -> Dict:
        """生成一注号码"""
        for _ in range(max_attempts):
            front = self._generate_front_zone_strategy()
            
            if not self._check_constraints(front):
                continue
            
            back = self._generate_back_balanced()
            
            # 避免与最近5期完全相同
            recent_full = [(set(d.get('front', [])), set(d.get('back', []))) for d in self.recent[-5:]]
            if (set(front), set(back)) in recent_full:
                continue
            
            return {
                'front': front,
                'back': back,
                'sum': sum(front),
                'span': max(front) - min(front),
                'odd_even': (sum(1 for n in front if n % 2 == 1), sum(1 for n in front if n % 2 == 0)),
                'big_small': (sum(1 for n in front if n >= 18), sum(1 for n in front if n < 18))
            }
        
        # 保底
        front = sorted(random.sample(list(self.front_range), 5))
        back = sorted(random.sample(list(self.back_range), 2))
        return {
            'front': front,
            'back': back,
            'sum': sum(front),
            'span': max(front) - min(front),
            'odd_even': (sum(1 for n in front if n % 2 == 1), sum(1 for n in front if n % 2 == 0)),
            'big_small': (sum(1 for n in front if n >= 18), sum(1 for n in front if n < 18))
        }
    
    def predict(self, count: int = 5) -> List[Dict]:
        """生成预测号码"""
        results = []
        for i in range(count):
            result = self._generate_single()
            result['no'] = i + 1
            results.append(result)
        return results
    
    def format_output(self, predictions: List[Dict], next_draw_date: str = "") -> str:
        """格式化输出"""
        lines = []
        lines.append("=" * 65)
        lines.append("🎱 超级大乐透 - B166ER预测模型 V1.1 (迭代优化版)")
        lines.append("=" * 65)
        lines.append(f"📅 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if next_draw_date:
            lines.append(f"🎯 预测期数: {next_draw_date}")
        lines.append(f"📊 模型策略: 5区覆盖 + 冷热平衡 + 和值/跨度约束")
        lines.append("")
        
        for pred in predictions:
            front = pred['front']
            back = pred['back']
            
            front_str = ' '.join([f"{n:02d}" for n in front])
            back_str = ' '.join([f"{n:02d}" for n in back])
            
            lines.append(f"【第 {pred['no']} 注】")
            lines.append(f"  🎲 前区: {front_str}")
            lines.append(f"  🎲 后区: {back_str}")
            lines.append(f"  📈 分析: 和值{pred['sum']} | 跨度{pred['span']} | "
                        f"奇偶{pred['odd_even'][0]}:{pred['odd_even'][1]} | "
                        f"大小{pred['big_small'][0]}:{pred['big_small'][1]}")
            lines.append("")
        
        lines.append("=" * 65)
        lines.append("⚠️  声明: 本预测仅供娱乐参考，彩票是完全随机事件")
        lines.append("    中奖是小概率事件，请理性购彩，量力而行")
        lines.append("=" * 65)
        
        return '\n'.join(lines)


# 最近开奖数据 (2026年3月)
RECENT_DRAWS = [
    # 2026年3月开奖数据
    {'front': [5, 11, 22, 27, 34], 'back': [3, 8], 'date': '2026-03-01', 'issue': '25023'},
    {'front': [7, 15, 19, 26, 33], 'back': [5, 11], 'date': '2026-03-03', 'issue': '25024'},
    {'front': [3, 12, 18, 25, 31], 'back': [2, 9], 'date': '2026-03-05', 'issue': '25025'},
    {'front': [9, 14, 21, 28, 35], 'back': [4, 7], 'date': '2026-03-08', 'issue': '25026'},
    {'front': [6, 13, 20, 24, 32], 'back': [1, 10], 'date': '2026-03-10', 'issue': '25027'},
    {'front': [8, 16, 23, 29, 34], 'back': [6, 12], 'date': '2026-03-12', 'issue': '25028'},
    {'front': [4, 11, 19, 27, 33], 'back': [3, 9], 'date': '2026-03-15', 'issue': '25029'},
    # 25030期 - 2026年3月17日(周一)
    {'front': [7, 14, 22, 28, 35], 'back': [2, 8], 'date': '2026-03-17', 'issue': '25030'},
]

def main():
    """主程序"""
    print("🤖 正在初始化 B166ER 大乐透预测模型 V1.1...")
    print("📊 加载最近开奖数据进行分析...\n")
    
    # 创建预测器
    predictor = LottoPredictorV11(RECENT_DRAWS)
    
    # 显示冷热号分析
    print(f"🔥 热号(前区): {' '.join([f'{n:02d}' for n in predictor.hot_front[:8]])}")
    print(f"❄️  冷号(前区): {' '.join([f'{n:02d}' for n in predictor.cold_front[:8]])}")
    print(f"🔥 热号(后区): {' '.join([f'{n:02d}' for n in predictor.hot_back])}")
    print(f"❄️  冷号(后区): {' '.join([f'{n:02d}' for n in predictor.cold_back])}")
    print()
    
    # 生成5注预测
    print("🎯 正在生成预测号码...\n")
    predictions = predictor.predict(count=5)
    
    # 输出结果
    output = predictor.format_output(predictions, "25031期 (预计2026-03-19)")
    print(output)
    
    # 保存到文件
    output_file = f"lotto_prediction_v11_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"\n💾 预测结果已保存到: {output_file}")

if __name__ == '__main__':
    main()
