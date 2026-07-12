# 酒店收益管理 V5.0 实战实现
## Python代码库 + 模型实现

> 版本: V5.0
> 更新: 2026-04-08
> 定位: 从理论到代码的完整实现

---

## 一、基础指标计算模块

```python
#!/usr/bin/env python3
"""
酒店收益管理基础指标计算
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from typing import List, Dict, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class RoomRevenue:
    """客房收入数据"""
    date: str
    rooms_sold: int
    rooms_available: int
    room_revenue: float
    fbb_revenue: float = 0.0
    other_revenue: float = 0.0
    cogs: float = 0.0  # 成本

class RevenueCalculator:
    """收益管理基础指标计算"""

    @staticmethod
    def occ(rooms_sold: int, rooms_available: int) -> float:
        """入住率"""
        if rooms_available == 0:
            return 0.0
        return rooms_sold / rooms_available * 100

    @staticmethod
    def adr(room_revenue: float, rooms_sold: int) -> float:
        """平均房价"""
        if rooms_sold == 0:
            return 0.0
        return room_revenue / rooms_sold

    @staticmethod
    def revpar(adr: float, occ: float) -> float:
        """RevPAR = ADR × 入住率"""
        return adr * (occ / 100)

    @staticmethod
    def revpar_by_total(rooms_available: int, total_revenue: float) -> float:
        """RevPAR = 总收入 / 可售间夜"""
        if rooms_available == 0:
            return 0.0
        return total_revenue / rooms_available

    @staticmethod
    def gop(revenue: float, controllable_costs: float) -> float:
        """毛营业利润"""
        return revenue - controllable_costs

    @staticmethod
    def gop_percent(revenue: float, gop: float) -> float:
        """GOP%"""
        if revenue == 0:
            return 0.0
        return gop / revenue * 100

    @staticmethod
    def goppar(gop: float, rooms_available: int) -> float:
        """GOPPAR = GOP / 可售间夜"""
        if rooms_available == 0:
            return 0.0
        return gop / rooms_available

    @staticmethod
    def trevpar(total_revenue: float, rooms_available: int) -> float:
        """TRevPAR = 总收入 / 可售间夜"""
        if rooms_available == 0:
            return 0.0
        return total_revenue / rooms_available

    @staticmethod
    def nrevpar(net_room_revenue: float, rooms_available: int) -> float:
        """NRevPAR = 净客房收入 / 可售间夜"""
        if rooms_available == 0:
            return 0.0
        return net_room_revenue / rooms_available

    @staticmethod
    def elasticity(old_price: float, new_price: float,
                  old_demand: float, new_demand: float) -> float:
        """
        价格弹性系数
        Ed = (ΔQ/Q) / (ΔP/P)
        """
        if old_price == 0 or old_demand == 0:
            return 0.0
        q_change = (new_demand - old_demand) / old_demand
        p_change = (new_price - old_price) / old_price
        if p_change == 0:
            return 0.0
        return q_change / p_change

    def calculate_daily(self, data: RoomRevenue) -> Dict:
        """计算单日所有指标"""
        total_revenue = data.room_revenue + data.fbb_revenue + data.other_revenue
        occ = self.occ(data.rooms_sold, data.rooms_available)
        adr = self.adr(data.room_revenue, data.rooms_sold)
        revpar = self.revpar(adr, occ)
        gop = self.gop(total_revenue, data.cogs)
        goppar = self.goppar(gop, data.rooms_available)

        return {
            'date': data.date,
            'occ': round(occ, 2),
            'adr': round(adr, 2),
            'revpar': round(revpar, 2),
            'gop': round(gop, 2),
            'goppar': round(goppar, 2),
            'total_revenue': round(total_revenue, 2)
        }


# 使用示例
calc = RevenueCalculator()

# 测试数据
test_data = RoomRevenue(
    date='2026-04-08',
    rooms_sold=85,
    rooms_available=100,
    room_revenue=42500,
    fbb_revenue=12000,
    other_revenue=3000,
    cogs=28000
)

result = calc.calculate_daily(test_data)
print("=== 单日收益指标 ===")
for k, v in result.items():
    print(f"  {k}: {v}")
```

---

## 二、需求预测模型

### 2.1 指数平滑模型

```python
class ExponentialSmoothing:
    """指数平滑预测"""

    def __init__(self, alpha: float = 0.3):
        self.alpha = alpha  # 平滑系数
        self.level = None

    def fit(self, data: List[float]) -> 'ExponentialSmoothing':
        """初始化"""
        self.level = data[0]
        for i in range(1, len(data)):
            self.level = self.alpha * data[i] + (1 - self.alpha) * self.level
        return self

    def forecast(self, h: int = 1) -> List[float]:
        """预测未来h期"""
        return [self.level] * h


class HoltLinearTrend:
    """Holt线性趋势指数平滑"""

    def __init__(self, alpha: float = 0.3, beta: float = 0.1):
        self.alpha = alpha
        self.beta = beta
        self.level = None
        self.trend = None

    def fit(self, data: List[float]) -> 'HoltLinearTrend':
        """初始化"""
        self.level = data[0]
        self.trend = data[1] - data[0] if len(data) > 1 else 0

        for i in range(1, len(data)):
            prev_level = self.level
            self.level = self.alpha * data[i] + (1 - self.alpha) * (self.level + self.trend)
            self.trend = self.beta * (self.level - prev_level) + (1 - self.beta) * self.trend

        return self

    def forecast(self, h: int = 1) -> List[float]:
        """预测未来h期"""
        return [self.level + (i+1) * self.trend for i in range(h)]


class HoltWinters:
    """Holt-Winters季节性指数平滑"""

    def __init__(self, alpha: float = 0.3, beta: float = 0.1, gamma: float = 0.1,
                 seasonal_period: int = 7):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.s = seasonal_period
        self.level = None
        self.trend = None
        self.seasonal = None

    def fit(self, data: List[float]) -> 'HoltWinters':
        """初始化"""
        n = len(data)
        self.level = sum(data[:self.s]) / self.s
        self.trend = sum(data[self.s:2*self.s]) / self.s - sum(data[:self.s]) / self.s
        self.seasonal = [data[i] / self.level for i in range(self.s)]

        for i in range(self.s, n):
            self.level = self.alpha * (data[i] / self.seasonal[i - self.s]) + \
                        (1 - self.alpha) * (self.level + self.trend)
            self.trend = self.beta * (self.level - (self.level - self.trend)) + \
                        (1 - self.beta) * self.trend
            self.seasonal.append((1 - self.gamma) * self.seasonal[i - self.s] + \
                                 self.gamma * data[i] / self.level)

        return self

    def forecast(self, h: int) -> List[float]:
        """加法模型预测"""
        result = []
        for i in range(h):
            m = i + 1
            y = self.level + m * self.trend + self.seasonal[-(self.s - (m % self.s) + 1) % self.s]
            result.append(y)
        return result
```

### 2.2 ARIMA模型

```python
class SimpleARIMA:
    """
    简化ARIMA实现 (用于教学)
    实际使用建议用 statsmodels.tsa.arima.model.ARIMA
    """

    def __init__(self, p: int = 1, d: int = 1, q: int = 1):
        self.p = p  # AR阶数
        self.d = d  # 差分阶数
        self.q = q  # MA阶数
        self.ar_params = []
        self.ma_params = []
        self.residuals = []

    def difference(self, data: List[float], d: int = 1) -> List[float]:
        """差分"""
        diffed = data.copy()
        for _ in range(d):
            diffed = [diffed[i] - diffed[i-1] for i in range(1, len(diffed))]
        return diffed

    def fit(self, data: List[float]) -> 'SimpleARIMA':
        """
        简化拟合 (实际应使用最大似然估计)
        这里用最小二乘近似
        """
        # 差分
        diffed = self.difference(data, self.d)

        # 简化: 使用最近p个值的平均作为AR部分
        if self.p > 0:
            self.ar_params = [sum(diffed[-(i+1):]) / min(self.p, len(diffed)) for i in range(self.p)]

        return self

    def forecast(self, h: int = 1) -> List[float]:
        """简化预测"""
        last_values = self.ar_params[:self.p] if self.ar_params else [0]
        predictions = []

        for _ in range(h):
            # 简化预测: 用参数加权和
            pred = sum(last_values) / len(last_values) if last_values else 0
            predictions.append(pred)

        return predictions
```

### 2.3 XGBoost预测模型

```python
class XGBoostForecaster:
    """
    XGBoost需求预测
    需要安装: pip install xgboost
    """

    def __init__(self):
        try:
            import xgboost as xgb
            self.xgb = xgb
            self.model = None
        except ImportError:
            self.xgb = None
            print("XGBoost未安装, 请运行: pip install xgboost")

    def create_features(self, df, target_col='demand'):
        """特征工程"""
        import pandas as pd

        # 时间特征
        df['dayofweek'] = df['date'].dt.dayofweek
        df['month'] = df['date'].dt.month
        df['quarter'] = df['date'].dt.quarter
        df['dayofyear'] = df['date'].dt.dayofyear
        df['is_weekend'] = (df['dayofweek'] >= 5).astype(int)

        # 滞后特征
        for lag in [1, 7, 14, 21]:
            df[f'lag_{lag}'] = df[target_col].shift(lag)

        # 滚动特征
        df['rolling_mean_7'] = df[target_col].shift(1).rolling(window=7).mean()
        df['rolling_std_7'] = df[target_col].shift(1).rolling(window=7).std()
        df['rolling_mean_30'] = df[target_col].shift(1).rolling(window=30).mean()

        # 差分特征
        df['diff_1'] = df[target_col].diff(1)
        df['diff_7'] = df[target_col].diff(7)

        return df

    def train(self, df, target_col='demand', feature_cols=None):
        """训练模型"""
        if not self.xgb:
            return None

        if feature_cols is None:
            feature_cols = [c for c in df.columns if c not in [target_col, 'date']]

        # 删除NaN
        train_df = df.dropna()
        X = train_df[feature_cols]
        y = train_df[target_col]

        # 训练
        self.model = self.xgb.XGBRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8
        )
        self.model.fit(X, y)

        return self

    def predict(self, X):
        """预测"""
        if self.model is None:
            return []
        return self.model.predict(X)
```

---

## 三、超额预订模型

```python
import math
from scipy.stats import norm

class OverbookingOptimizer:
    """超额预订优化 (Newsvendor模型)"""

    def __init__(self, capacity: int, avg_noshow_rate: float = 0.05,
                 deny_cost: float = 150.0, overbook_cost: float = 80.0):
        """
        capacity: 房间容量
        avg_noshow_rate: 平均no-show率
        deny_cost: 拒绝成本 (walk-in补偿)
        overbook_cost: 超额成本 (重新预订/升级)
        """
        self.C = capacity
        self.avg_noshow_rate = avg_noshow_rate
        self.Cu = deny_cost   # 低估成本
        self.Co = overbook_cost  # 高估成本

    def critical_ratio(self) -> float:
        """
        Newsvendor临界值
        Cu / (Cu + Co)
        """
        return self.Cu / (self.Cu + self.Co)

    def optimal_overbooking(self, mu: float = None, sigma: float = None) -> int:
        """
        计算最优超额预订量

        mu: 平均no-show数 (默认: capacity × no-show率)
        sigma: no-show标准差 (默认: sqrt(n × p × (1-p)))
        """
        if mu is None:
            mu = self.C * self.avg_noshow_rate
        if sigma is None:
            sigma = math.sqrt(self.C * self.avg_noshow_rate * (1 - self.avg_noshow_rate))

        # 临界比
        cr = self.critical_ratio()

        # 最优超额量 (正态分布近似)
        # x* = mu + sigma × z(cr)
        z = norm.ppf(cr) if cr < 1 else 3.0  # 处理cr=1情况
        x_star = mu + sigma * z

        # 返回相对于容量的超额量
        return max(0, int(round(x_star - self.C)))

    def max_booking(self) -> int:
        """最大可接受预订量"""
        ob = self.optimal_overbooking()
        return self.C + ob

    def expected_revenue(self, booking_limit: int, demand_mean: float,
                        demand_std: float, price: float) -> float:
        """
        计算期望收益
        """
        # 简化计算
        e_demand = demand_mean
        e_denied = max(0, booking_limit - self.C) * self.avg_noshow_rate * price
        e_overbook = max(0, self.C - booking_limit) * self.Co

        return e_demand * price - e_denied - e_overbook

    def print_summary(self):
        """打印分析摘要"""
        ob = self.optimal_overbooking()
        cr = self.critical_ratio()

        print("=== 超额预订分析 ===")
        print(f"  房间容量: {self.C}")
        print(f"  平均no-show率: {self.avg_noshow_rate:.1%}")
        print(f"  拒绝成本: ¥{self.Cu}")
        print(f"  超额成本: ¥{self.Co}")
        print(f"  临界比: {cr:.3f}")
        print(f"  最优超额量: {ob}")
        print(f"  最大预订量: {self.C + ob}")
```

---

## 四、动态定价引擎

```python
class DynamicPricingEngine:
    """动态定价引擎"""

    def __init__(self, base_price: float, cost: float = 0):
        self.base_price = base_price
        self.cost = cost

    def demand_factor(self, booking_progress: float, target_progress: float) -> float:
        """
        需求系数
        booking_progress: 当前预订进度 (0-1)
        target_progress: 目标预订进度
        """
        if target_progress == 0:
            return 1.0
        ratio = booking_progress / target_progress
        if ratio < 0.8:
            return 0.9  # 落后于进度,降价
        elif ratio < 1.0:
            return 1.0
        elif ratio < 1.2:
            return 1.1  # 领先于进度,溢价
        else:
            return 1.2

    def time_factor(self, days_to_arrival: int) -> float:
        """
        时间系数
        距入住天数越近,价格越高
        """
        if days_to_arrival >= 30:
            return 0.85
        elif days_to_arrival >= 14:
            return 0.95
        elif days_to_arrival >= 7:
            return 1.0
        elif days_to_arrival >= 3:
            return 1.15
        else:
            return 1.3

    def competition_factor(self, our_price: float, comp_price: float) -> float:
        """
        竞争系数
        our_price: 本店价格
        comp_price: 竞品价格
        """
        if comp_price == 0:
            return 1.0
        ratio = our_price / comp_price
        if ratio < 0.85:
            return 0.9  # 定价偏低
        elif ratio < 0.95:
            return 1.0
        elif ratio < 1.05:
            return 1.05
        else:
            return 1.1

    def channel_factor(self, channel_commission: float) -> float:
        """
        渠道系数
        渠道佣金率越高,挂牌价越高
        """
        return 1 / (1 - channel_commission)

    def calculate_price(self,
                       booking_progress: float = 0.5,
                       target_progress: float = 0.5,
                       days_to_arrival: int = 14,
                       our_price: float = None,
                       comp_price: float = None,
                       channel_commission: float = 0.15) -> Dict:
        """
        综合计算最优价格
        """
        if our_price is None:
            our_price = self.base_price

        df = self.demand_factor(booking_progress, target_progress)
        tf = self.time_factor(days_to_arrival)
        cf = self.competition_factor(our_price, comp_price or our_price)
        chf = self.channel_factor(channel_commission)

        # 最优价格
        optimal_price = self.base_price * df * tf * cf

        # 净收益 (扣除佣金后)
        net_price = optimal_price * (1 - channel_commission)
        gross_profit = net_price - self.cost

        return {
            'base_price': round(self.base_price, 2),
            'demand_factor': round(df, 3),
            'time_factor': round(tf, 3),
            'competition_factor': round(cf, 3),
            'channel_factor': round(chf, 3),
            'optimal_price': round(optimal_price, 2),
            'net_price': round(net_price, 2),
            'gross_profit': round(gross_profit, 2),
            'markup': round((optimal_price / self.base_price - 1) * 100, 1)
        }

    def pricing_tiers(self, occupancy: float) -> Dict:
        """
        阶梯定价策略
        基于入住率
        """
        if occupancy < 0.4:
            strategy = 'promotion'
            multiplier = 0.85
        elif occupancy < 0.6:
            strategy = 'discount'
            multiplier = 0.92
        elif occupancy < 0.75:
            strategy = 'standard'
            multiplier = 1.0
        elif occupancy < 0.9:
            strategy = 'premium'
            multiplier = 1.15
        else:
            strategy = 'surge'
            multiplier = 1.3

        return {
            'strategy': strategy,
            'multiplier': multiplier,
            'price': round(self.base_price * multiplier, 2),
            'markup_pct': round((multiplier - 1) * 100, 1)
        }
```

---

## 五、渠道优化模型

```python
class ChannelOptimizer:
    """渠道优化"""

    def __init__(self):
        self.channels = {}

    def add_channel(self, name: str, revenue: float, commission: float,
                   cancel_rate: float = 0.1, fixed_cost: float = 0):
        """添加渠道"""
        self.channels[name] = {
            'revenue': revenue,
            'commission': commission,
            'cancel_rate': cancel_rate,
            'fixed_cost': fixed_cost
        }

    def channel_profit(self, name: str) -> float:
        """渠道利润"""
        ch = self.channels[name]
        net = ch['revenue'] * (1 - ch['commission'] - ch['cancel_rate'])
        return net - ch['fixed_cost']

    def channel_roi(self, name: str) -> float:
        """渠道ROI"""
        ch = self.channels[name]
        cost = ch['revenue'] * ch['commission'] + ch['fixed_cost']
        if cost == 0:
            return 0
        return ch['revenue'] / cost

    def channel_score(self, name: str,
                     w_revenue: float = 0.3,
                     w_profit: float = 0.3,
                     w_roi: float = 0.2,
                     w_volume: float = 0.2) -> float:
        """
        渠道综合评分
        """
        ch = self.channels[name]
        revenue_score = ch['revenue'] / 10000  # 归一化
        profit_score = self.channel_profit(name) / 1000
        roi_score = self.channel_roi(name)
        volume_score = ch['revenue'] / 10000  # 简化

        return (w_revenue * revenue_score +
                w_profit * profit_score +
                w_roi * roi_score +
                w_volume * volume_score)

    def optimize_allocation(self, total_rooms: int,
                           min_share: float = 0.1,
                           max_share: float = 0.5) -> Dict:
        """
        线性规划求解最优渠道分配 (简化版)
        实际应用建议用 scipy.optimize.linprog
        """
        results = {}
        total_score = sum(self.channel_score(name) for name in self.channels)

        for name in self.channels:
            score = self.channel_score(name)
            # 按评分比例分配
            share = (score / total_score) if total_score > 0 else 1/len(self.channels)
            share = max(min_share, min(max_share, share))

            results[name] = {
                'share': round(share * 100, 1),
                'rooms': int(total_rooms * share),
                'expected_revenue': self.channels[name]['revenue'] * share,
                'expected_profit': self.channel_profit(name) * share
            }

        return results
```

---

## 六、置换收益分析

```python
class DisplacementAnalyzer:
    """置换收益分析"""

    def __init__(self, upgrade_cost: float = 30, walkin_price: float = 280):
        self.upgrade_cost = upgrade_cost
        self.walkin_price = walkin_price

    def upgrade_decision(self, current_rate: float, upgrade_rate: float,
                        upgrade_prob: float = 0.3) -> Dict:
        """
        Upgrade决策分析

        current_rate: 当前房价
        upgrade_rate: 升级后房价
        upgrade_prob: 升级接受概率
        """
        revenue_diff = upgrade_rate - current_rate
        net_revenue = upgrade_prob * (revenue_diff - self.upgrade_cost)

        return {
            'current_rate': current_rate,
            'upgrade_rate': upgrade_rate,
            'revenue_diff': revenue_diff,
            'upgrade_prob': upgrade_prob,
            'upgrade_cost': self.upgrade_cost,
            'expected_net': round(net_revenue, 2),
            'decision': 'EXECUTE' if net_revenue > 0 else 'REJECT'
        }

    def walkin_decision(self, current_booked: int, capacity: int,
                       walkin_prob: float = 0.5,
                       expected_booking_rate: float = 150) -> Dict:
        """
        Walk-in决策

        current_booked: 当前已预订数
        capacity: 容量
        walkin_prob: walk-in接受概率
        expected_booking_rate: 保留房间的期望未来收入
        """
        available = capacity - current_booked

        if available <= 0:
            return {
                'available_rooms': 0,
                'walkin_offer': None,
                'decision': 'FULL'
            }

        # Walk-in最优报价
        if available / capacity < 0.2:
            markup = 1.3  # 30%溢价
        elif available / capacity < 0.4:
            markup = 1.1
        else:
            markup = 1.0

        walkin_offer = self.walkin_price * markup
        expected_walkin_revenue = walkin_prob * walkin_offer
        expected_future_revenue = expected_booking_rate

        decision = 'ACCEPT' if expected_walkin_revenue > expected_future_revenue else 'REJECT'

        return {
            'available_rooms': available,
            'utilization': f"{current_booked/capacity:.1%}",
            'walkin_prob': walkin_prob,
            'walkin_offer': round(walkin_offer, 2),
            'expected_walkin': round(expected_walkin_revenue, 2),
            'expected_future': round(expected_future_revenue, 2),
            'decision': decision
        }

    def total_displacement_value(self, upgrades: List[Dict],
                                walkins: List[Dict]) -> Dict:
        """总置换收益"""
        total_upgrade = sum(u['expected_net'] for u in upgrades)
        total_walkin = sum(w['expected_walkin'] - w['expected_future']
                          for w in walkins if w['decision'] == 'ACCEPT')

        return {
            'upgrade_value': round(total_upgrade, 2),
            'walkin_value': round(total_walkin, 2),
            'total': round(total_upgrade + total_walkin, 2)
        }
```

---

## 七、预测准确度评估

```python
class ForecastEvaluator:
    """预测评估"""

    @staticmethod
    def mape(actual: List[float], predicted: List[float]) -> float:
        """MAPE: 平均绝对百分比误差"""
        n = len(actual)
        if n == 0:
            return 0
        valid = [(a, p) for a, p in zip(actual, predicted) if a != 0]
        if not valid:
            return 0
        return sum(abs(a - p) / a for a, p in valid) / len(valid) * 100

    @staticmethod
    def mae(actual: List[float], predicted: List[float]) -> float:
        """MAE: 平均绝对误差"""
        if not actual:
            return 0
        return sum(abs(a - p) for a, p in zip(actual, predicted)) / len(actual)

    @staticmethod
    def rmse(actual: List[float], predicted: List[float]) -> float:
        """RMSE: 均方根误差"""
        if not actual:
            return 0
        return math.sqrt(sum((a - p) ** 2 for a, p in zip(actual, predicted)) / len(actual))

    @staticmethod
    def bias(actual: List[float], predicted: List[float]) -> float:
        """Bias: 平均偏差 (预测-实际)"""
        if not actual:
            return 0
        return sum(p - a for a, p in zip(actual, predicted)) / len(actual)

    @staticmethod
    def evaluate(actual: List[float], predicted: List[float]) -> Dict:
        """综合评估"""
        return {
            'MAPE': round(ForecastEvaluator.mape(actual, predicted), 2),
            'MAE': round(ForecastEvaluator.mae(actual, predicted), 2),
            'RMSE': round(ForecastEvaluator.rmse(actual, predicted), 2),
            'Bias': round(ForecastEvaluator.bias(actual, predicted), 2)
        }

    @staticmethod
    def grade(mape: float) -> str:
        """评级"""
        if mape < 5:
            return '优秀'
        elif mape < 10:
            return '良好'
        elif mape < 20:
            return '一般'
        else:
            return '较差'
```

---

## 八、使用示例

```python
if __name__ == '__main__':
    print("=" * 60)
    print("酒店收益管理系统 V5.0 - 使用示例")
    print("=" * 60)

    # 1. 基础指标
    print("\n[1] 基础指标计算")
    calc = RevenueCalculator()
    data = RoomRevenue(
        date='2026-04-08',
        rooms_sold=85,
        rooms_available=100,
        room_revenue=42500,
        fbb_revenue=12000,
        other_revenue=3000,
        cogs=28000
    )
    metrics = calc.calculate_daily(data)
    for k, v in metrics.items():
        print(f"  {k}: {v}")

    # 2. 指数平滑预测
    print("\n[2] 指数平滑预测")
    demand = [70, 75, 72, 78, 80, 85, 88, 82, 86, 90]
    ses = ExponentialSmoothing(alpha=0.3)
    ses.fit(demand)
    forecast = ses.forecast(3)
    print(f"  历史: {demand[-5:]}")
    print(f"  预测: {[round(f, 1) for f in forecast]}")

    # 3. Holt-Winters
    print("\n[3] Holt-Winters季节性预测")
    hw = HoltWinters(alpha=0.3, beta=0.1, gamma=0.2, seasonal_period=7)
    weekly = [60, 75, 85, 90, 85, 70, 55] * 4  # 4周数据
    hw.fit(weekly)
    forecast_hw = hw.forecast(7)
    print(f"  下周预测: {[round(f, 1) for f in forecast_hw]}")

    # 4. 超额预订
    print("\n[4] 超额预订优化")
    ob = OverbookingOptimizer(
        capacity=100,
        avg_noshow_rate=0.05,
        deny_cost=150,
        overbook_cost=80
    )
    ob.print_summary()

    # 5. 动态定价
    print("\n[5] 动态定价")
    pricing = DynamicPricingEngine(base_price=300, cost=80)
    result = pricing.calculate_price(
        booking_progress=0.6,
        target_progress=0.5,
        days_to_arrival=7,
        our_price=300,
        comp_price=320,
        channel_commission=0.15
    )
    for k, v in result.items():
        print(f"  {k}: {v}")

    # 6. 预测评估
    print("\n[6] 预测准确度评估")
    actual = [100, 110, 105, 115]
    predicted = [98, 112, 103, 118]
    eval_result = ForecastEvaluator.evaluate(actual, predicted)
    for k, v in eval_result.items():
        grade = ForecastEvaluator.grade(v) if k == 'MAPE' else ''
        print(f"  {k}: {v} {grade}")

    print("\n" + "=" * 60)
    print("示例完成")
```

---

## 九、依赖安装

```bash
# 核心依赖
pip install numpy pandas scipy

# 机器学习 (可选)
pip install xgboost lightgbm

# 时间序列 (可选)
pip install statsmodels prophet

# 可视化
pip install matplotlib seaborn plotly
```

---

**版本**: V5.0 | **更新**: 2026-04-08 | **作者**: B166ER
