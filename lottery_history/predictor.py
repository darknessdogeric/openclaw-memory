"""
B166ER 统一彩票预测引擎 V1.0
支持: 大乐透 (DLT) + 双色球 (SSQ)
自迭代: 预测→复盘→权重更新
"""
import csv
import json
import os
import sys
import random
from collections import Counter, defaultdict
from datetime import datetime
from typing import Any

sys.stdout.reconfigure(encoding='utf-8')

# ── 彩票规则 ──
RULES = {
    'dlt': {
        'name': '大乐透',
        'front_pool': 35, 'front_count': 5,
        'back_pool': 12, 'back_count': 2,
        'csv': 'dlt_history.csv',
    },
    'ssq': {
        'name': '双色球',
        'front_pool': 33, 'front_count': 6,  # 红球
        'back_pool': 16, 'back_count': 1,     # 蓝球
        'csv': 'ssq_history.csv',
    },
}

DIR = os.path.dirname(__file__)
PREDICTIONS_FILE = os.path.join(DIR, 'predictions_log.json')
EVOLUTION_FILE = os.path.join(DIR, 'evolution_log.md')


# ═══════════════════════════════════════════
#  数据加载
# ═══════════════════════════════════════════

def load_history(lottery_type: str) -> list[dict]:
    """加载历史开奖数据"""
    csv_path = os.path.join(DIR, RULES[lottery_type]['csv'])
    if not os.path.exists(csv_path):
        return []
    with open(csv_path, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


# ═══════════════════════════════════════════
#  统计分析
# ═══════════════════════════════════════════

class LotteryAnalyzer:
    """彩票统计分析器"""

    def __init__(self, lottery_type: str):
        self.lt = lottery_type
        self.rule = RULES[lottery_type]
        self.history = load_history(lottery_type)
        self.fp = self.rule['front_pool']
        self.fc = self.rule['front_count']
        self.bp = self.rule['back_pool']
        self.bc = self.rule['back_count']

    @property
    def total_issues(self) -> int:
        return len(self.history)

    @property
    def latest_issue(self) -> str:
        return self.history[-1]['issue'] if self.history else 'N/A'

    def get_front_numbers(self, row: dict) -> list[int]:
        """提取前区/红球号码"""
        if self.lt == 'dlt':
            return [int(row[f'front_{i}']) for i in range(1, 6)]
        else:
            return [int(row[f'r{i}']) for i in range(1, 7)]

    def get_back_numbers(self, row: dict) -> list[int]:
        """提取后区/蓝球号码"""
        if self.lt == 'dlt':
            return [int(row[f'back_{i}']) for i in range(1, 3)]
        else:
            return [int(row['b1'])]

    # ── 频次分析 ──

    def frequency(self, n_recent: int = 50, zone: str = 'front') -> Counter:
        """最近N期的号码频次"""
        counter = Counter()
        recent = self.history[-n_recent:] if len(self.history) > n_recent else self.history
        for row in recent:
            if zone == 'front':
                counter.update(self.get_front_numbers(row))
            else:
                counter.update(self.get_back_numbers(row))
        return counter

    def hot_numbers(self, n_recent: int = 30, top_k: int = 10) -> list[int]:
        """热号: 近期出现次数最多的号码"""
        freq = self.frequency(n_recent, 'front')
        return [n for n, _ in freq.most_common(top_k)]

    def cold_numbers(self, n_recent: int = 30, bottom_k: int = 10) -> list[int]:
        """冷号: 近期出现次数最少的号码"""
        freq = self.frequency(n_recent, 'front')
        all_nums = set(range(1, self.fp + 1))
        appeared = set(freq.keys())
        never = all_nums - appeared
        result = list(never)
        # 补齐: 从低频中取
        sorted_asc = sorted(freq.items(), key=lambda x: x[1])
        for n, _ in sorted_asc:
            if len(result) >= bottom_k:
                break
            if n not in result:
                result.append(n)
        return result[:bottom_k]

    # ── 遗漏分析 ──

    def gap_analysis(self, zone: str = 'front') -> dict[int, int]:
        """各号码距离上一次出现的期数（遗漏值）"""
        pool = self.fp if zone == 'front' else self.bp
        gaps = {}
        for num in range(1, pool + 1):
            gap = 0
            for row in reversed(self.history):
                nums = self.get_front_numbers(row) if zone == 'front' else self.get_back_numbers(row)
                if num in nums:
                    break
                gap += 1
            gaps[num] = gap
        return gaps

    def top_missing(self, zone: str = 'front', top_k: int = 10) -> list[tuple[int, int]]:
        """遗漏值最大的号码"""
        gaps = self.gap_analysis(zone)
        return sorted(gaps.items(), key=lambda x: -x[1])[:top_k]

    # ── 奇偶比 ──

    def odd_even_ratio(self, n_recent: int = 50) -> Counter:
        """最近N期的奇偶比分布"""
        counter = Counter()
        recent = self.history[-n_recent:] if len(self.history) > n_recent else self.history
        for row in recent:
            nums = self.get_front_numbers(row)
            odds = sum(1 for n in nums if n % 2 == 1)
            evens = len(nums) - odds
            counter[f'{odds}:{evens}'] += 1
        return counter

    # ── 区间分布 ──

    def zone_distribution(self, n_recent: int = 50) -> dict[str, Counter]:
        """三个区间的频次分布"""
        zone_size = self.fp // 3
        zones = {'zone1': range(1, zone_size + 1),
                 'zone2': range(zone_size + 1, zone_size * 2 + 1),
                 'zone3': range(zone_size * 2 + 1, self.fp + 1)}
        zone_count = Counter()
        recent = self.history[-n_recent:] if len(self.history) > n_recent else self.history
        for row in recent:
            nums = self.get_front_numbers(row)
            for n in nums:
                for zname, zrange in zones.items():
                    if n in zrange:
                        zone_count[zname] += 1
        return {zname: zone_count[zname] for zname in zones}

    # ── 连号分析 ──

    def consecutive_stats(self, n_recent: int = 50) -> dict:
        """连号出现频率"""
        total = 0
        consecutive_count = 0
        recent = self.history[-n_recent:] if len(self.history) > n_recent else self.history
        for row in recent:
            nums = sorted(self.get_front_numbers(row))
            for i in range(len(nums) - 1):
                if nums[i + 1] - nums[i] == 1:
                    consecutive_count += 1
            total += 1
        return {
            'consecutive_draws': consecutive_count,
            'total_draws': total,
            'rate': consecutive_count / total if total > 0 else 0,
        }

    # ── 和值分析 ──

    def sum_stats(self, n_recent: int = 50) -> dict:
        """和值统计"""
        sums = []
        recent = self.history[-n_recent:] if len(self.history) > n_recent else self.history
        for row in recent:
            nums = self.get_front_numbers(row)
            sums.append(sum(nums))
        if not sums:
            return {}
        return {
            'min': min(sums),
            'max': max(sums),
            'avg': sum(sums) / len(sums),
            'median': sorted(sums)[len(sums) // 2],
        }

    # ── 综合报告 ──

    def full_report(self) -> dict[str, Any]:
        """生成完整统计分析报告"""
        return {
            'lottery': self.rule['name'],
            'total_issues': self.total_issues,
            'latest_issue': self.latest_issue,
            'latest_date': self.history[-1].get('date', '') if self.history else '',
            'front_hot_30': self.hot_numbers(30, 10),
            'front_cold_30': self.cold_numbers(30, 10),
            'front_gaps': dict(self.top_missing('front', 10)),
            'front_odd_even': dict(self.odd_even_ratio(50)),
            'front_zones': self.zone_distribution(50),
            'front_consecutive': self.consecutive_stats(50),
            'front_sum': self.sum_stats(50),
            'back_freq': dict(self.frequency(30, 'back').most_common()),
            'back_gaps': dict(self.top_missing('back', 5)),
        }


# ═══════════════════════════════════════════
#  预测引擎
# ═══════════════════════════════════════════

class LotteryPredictor:
    """统一预测引擎"""

    def __init__(self, lottery_type: str):
        self.lt = lottery_type
        self.analyzer = LotteryAnalyzer(lottery_type)
        self.rule = self.analyzer.rule

    def score_number(self, num: int, report: dict) -> float:
        """综合评分一个号码（前区/红球）"""
        score = 0.0

        # 热号加分
        hot = report['front_hot_30']
        if num in hot:
            pos = hot.index(num)
            score += (len(hot) - pos) / len(hot) * 3.0  # 越热分越高

        # 冷号补分（遗漏回补）
        gaps = report['front_gaps']
        gap = gaps.get(str(num), 0)
        if gap > 10:
            score += min(gap / 20, 2.0)  # 遗漏越久，回补概率越大

        # 区间平衡加分
        zone_size = self.rule['front_pool'] // 3
        if num <= zone_size:
            zone = 'zone1'
        elif num <= zone_size * 2:
            zone = 'zone2'
        else:
            zone = 'zone3'
        zones = report['front_zones']
        total_zone = sum(zones.values())
        if total_zone > 0:
            zone_ratio = zones.get(zone, 0) / total_zone
            # 区间占比越高，该区号码越值得选
            score += zone_ratio * 2.0

        return score

    def score_back_number(self, num: int, report: dict) -> float:
        """综合评分后区/蓝球"""
        score = 0.0
        bf = report['back_freq']
        # 热度加分
        if str(num) in bf:
            score += bf[str(num)] * 0.5
        # 遗漏加分
        bg = report['back_gaps']
        gap = bg.get(str(num), 0)
        if gap > 8:
            score += min(gap / 10, 2.0)
        return score

    def generate_candidates(self, k: int = 100) -> list[tuple[list[int], list[int], float]]:
        """生成K个候选组合并评分"""
        report = self.analyzer.full_report()
        front_scores = {n: self.score_number(n, report) for n in range(1, self.rule['front_pool'] + 1)}
        back_scores = {n: self.score_back_number(n, report) for n in range(1, self.rule['back_pool'] + 1)}

        candidates = []
        for _ in range(k * 5):  # 多生成一些再筛选
            # 加权随机选前区 (最低权重1.0防止choices报错)
            f_weights = [max(front_scores.get(n, 0), 1.0) for n in range(1, self.rule['front_pool'] + 1)]
            front = sorted(random.choices(
                range(1, self.rule['front_pool'] + 1),
                weights=f_weights,
                k=self.rule['front_count']
            ))
            if len(set(front)) < self.rule['front_count']:
                continue

            # 加权随机选后区 (最低权重1.0)
            b_weights = [max(back_scores.get(n, 0), 1.0) for n in range(1, self.rule['back_pool'] + 1)]
            back = sorted(random.choices(
                range(1, self.rule['back_pool'] + 1),
                weights=b_weights,
                k=self.rule['back_count']
            ))
            if len(set(back)) < self.rule['back_count']:
                continue

            # 计算总分
            f_score = sum(front_scores.get(n, 0) for n in front)
            b_score = sum(back_scores.get(n, 0) for n in back)
            total = f_score + b_score

            candidates.append((front, back, total))

        # 去重+排序
        seen = set()
        unique = []
        for f, b, s in sorted(candidates, key=lambda x: -x[2]):
            key = f'{f}|{b}'
            if key not in seen:
                seen.add(key)
                unique.append((f, b, s))
            if len(unique) >= k:
                break

        return unique

    def predict(self, n_bets: int = 5) -> dict:
        """出预测结果：n_bets 注"""
        report = self.analyzer.full_report()
        candidates = self.generate_candidates(200)

        bets = []
        for i, (front, back, score) in enumerate(candidates[:n_bets]):
            bets.append({
                'scheme': i + 1,
                'front': front,
                'back': back,
                'score': round(score, 2),
            })

        prediction = {
            'lottery': self.rule['name'],
            'type': self.lt,
            'predicted_at': datetime.now().isoformat(),
            'total_issues': self.analyzer.total_issues,
            'latest_issue': self.analyzer.latest_issue,
            'n_bets': n_bets,
            'bets': bets,
            'stats_snapshot': {
                'front_hot_30': report['front_hot_30'][:10],
                'front_cold_30': report['front_cold_30'][:10],
                'front_odd_even_top3': dict(sorted(
                    report['front_odd_even'].items(),
                    key=lambda x: -x[1]
                )[:3]),
                'front_gaps_top5': {str(k): v for k, v in report['front_gaps'].items()},
                'back_freq_top5': dict(sorted(
                    report['back_freq'].items(),
                    key=lambda x: -x[1]
                )[:5]),
            },
        }

        # 保存预测记录
        self._save_prediction(prediction)

        return prediction

    def _save_prediction(self, pred: dict) -> None:
        """保存预测到日志"""
        preds = []
        if os.path.exists(PREDICTIONS_FILE):
            with open(PREDICTIONS_FILE, 'r', encoding='utf-8') as f:
                preds = json.load(f)
        preds.append(pred)
        with open(PREDICTIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(preds, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════
#  复盘 & 自迭代
# ═══════════════════════════════════════════

def review_prediction(lottery_type: str, actual_issue: str) -> dict | None:
    """将最新预测与实际开奖对比，更新进化日志"""
    rule = RULES[lottery_type]
    history = load_history(lottery_type)

    # 找到实际开奖数据
    actual = None
    for row in reversed(history):
        if row['issue'] == actual_issue:
            actual = row
            break
    if actual is None:
        print(f'[REVIEW] 未找到 {actual_issue} 期开奖数据')
        return None

    # 找到该期的预测
    if not os.path.exists(PREDICTIONS_FILE):
        print('[REVIEW] 无预测记录')
        return None
    with open(PREDICTIONS_FILE, 'r', encoding='utf-8') as f:
        preds = json.load(f)

    analyzer = LotteryAnalyzer(lottery_type)
    actual_front = analyzer.get_front_numbers(actual)
    actual_back = analyzer.get_back_numbers(actual)

    # 对比每个方案的命中
    results = []
    for pred in preds:
        if pred['type'] != lottery_type:
            continue
        for bet in pred.get('bets', []):
            f_hits = len(set(bet['front']) & set(actual_front))
            b_hits = len(set(bet['back']) & set(actual_back))
            results.append({
                'issue': actual_issue,
                'scheme': bet['scheme'],
                'predicted_at': pred['predicted_at'],
                'front_hits': f_hits,
                'back_hits': b_hits,
                'front': bet['front'],
                'back': bet['back'],
            })

    if not results:
        print(f'[REVIEW] 未找到 {lottery_type} {actual_issue} 期的预测')
        return None

    # 找最佳方案
    best = max(results, key=lambda x: (x['front_hits'], x['back_hits']))

    # 写入进化日志
    review = {
        'lottery': rule['name'],
        'issue': actual_issue,
        'date': actual.get('date', ''),
        'actual_front': actual_front,
        'actual_back': actual_back,
        'total_schemes': len(results),
        'best': best,
        'all_results': results,
        'reviewed_at': datetime.now().isoformat(),
    }

    _log_evolution(review)

    return review


def _log_evolution(review: dict) -> None:
    """追加进化日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    lines = [
        f'\n## {review["lottery"]} {review["issue"]}期复盘 ({timestamp})',
        f'',
        f'- 开奖号码: {" ".join(str(n).zfill(2) for n in review["actual_front"])}',
        f'  {" ".join(str(n).zfill(2) for n in review["actual_back"])}' if review["lottery"] == "大乐透" else f'  {str(review["actual_back"][0]).zfill(2)}',
        f'- 总方案数: {review["total_schemes"]}',
        f'- 最佳方案: 方案{review["best"]["scheme"]} — 前区{review["best"]["front_hits"]}个 + 后区{review["best"]["back_hits"]}个',
        f'- 最佳号码: 前区{review["best"]["front"]} | 后区{review["best"]["back"]}',
        f'',
        f'### 命中详情',
    ]

    for r in sorted(review['all_results'], key=lambda x: (-x['front_hits'], -x['back_hits'])):
        lines.append(f'- 方案{r["scheme"]}: 前区{r["front_hits"]}+后区{r["back_hits"]} '
                     f'({" ".join(str(n).zfill(2) for n in r["front"])})')

    lines.append('')
    lines.append('### 进化信号')
    lines.append(f'- 前区命中率: {review["best"]["front_hits"]}/{RULES[review["lottery"].lower() if review["lottery"]=="大乐透" else "ssq"]["front_count"]}')
    lines.append(f'- 后区命中率: {review["best"]["back_hits"]}/{RULES[review["lottery"].lower() if review["lottery"]=="大乐透" else "ssq"]["back_count"]}')
    lines.append('')

    # 简单进化建议
    if review['best']['front_hits'] == 0:
        lines.append('⚠️ 前区全灭 — 检查热号/遗漏权重是否需要调整')
    if review['best']['front_hits'] <= 1:
        lines.append('🟡 前区命中偏低 — 考虑扩大热号窗口或增加冷号回补权重')
    if review['best']['back_hits'] == 0:
        lines.append('⚠️ 后区全灭 — 后区随机性强，需要更多候选')

    with open(EVOLUTION_FILE, 'a', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


# ═══════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════

def main():
    import argparse
    ap = argparse.ArgumentParser(description='B166ER 统一彩票预测引擎')
    ap.add_argument('type', choices=['dlt', 'ssq'], help='彩票类型')
    ap.add_argument('--predict', '-p', type=int, default=0, metavar='N', help='出N注预测')
    ap.add_argument('--review', '-r', type=str, default='', metavar='ISSUE', help='复盘指定期号')
    ap.add_argument('--report', action='store_true', help='输出统计报告')
    ap.add_argument('--bets', '-b', type=int, default=5, help='预测注数(默认5)')
    args = ap.parse_args()

    if args.predict:
        predictor = LotteryPredictor(args.type)
        result = predictor.predict(args.predict or args.bets)

        # 格式化输出
        print(f'\n{"="*60}')
        print(f'  {result["lottery"]} 预测方案')
        print(f'  基于: {result["total_issues"]}期历史数据')
        print(f'  最新: {result["latest_issue"]}期')
        print(f'  时间: {result["predicted_at"][:19]}')
        print(f'{"="*60}')

        for bet in result['bets']:
            f_str = ' '.join(str(n).zfill(2) for n in bet['front'])
            b_str = ' '.join(str(n).zfill(2) for n in bet['back'])
            print(f'\n  方案{bet["scheme"]} (评分: {bet["score"]:.2f})')
            print(f'    前区: {f_str}')
            print(f'    后区: {b_str}')

        print(f'\n{"-"*60}')
        print(f'  热号TOP10: {result["stats_snapshot"]["front_hot_30"]}')
        print(f'  冷号TOP10: {result["stats_snapshot"]["front_cold_30"]}')
        print(f'  遗漏TOP5: {list(result["stats_snapshot"]["front_gaps_top5"].items())[:5]}')
        print(f'  后区频次: {result["stats_snapshot"]["back_freq_top5"]}')
        print(f'{"="*60}\n')

    elif args.review:
        result = review_prediction(args.type, args.review)
        if result:
            print(f'\n复盘完成: {result["lottery"]} {result["issue"]}期')
            print(f'实际: {" ".join(str(n).zfill(2) for n in result["actual_front"])} | {" ".join(str(n).zfill(2) for n in result["actual_back"])}')
            print(f'最佳: 方案{result["best"]["scheme"]} (前{result["best"]["front_hits"]}+后{result["best"]["back_hits"]})')

    elif args.report:
        analyzer = LotteryAnalyzer(args.type)
        report = analyzer.full_report()
        print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
