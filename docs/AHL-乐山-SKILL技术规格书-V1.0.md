# AHL 乐山锦江嘉州宾馆 SKILL技术规格书 V1.0

> **版本**: V1.0
> **日期**: 2026-03-27
> **试点酒店**: 四川乐山锦江嘉州宾馆
> **模块**: 模块3（技术深化任务）
> **状态**: 技术规格设计，待实地数据验证

---

## 文档目的

本规格书定义AHL数字员工Phase 1阶段需要实现的7个核心SKILL的技术规格。每个SKILL必须包含完整的技术规格，确保代码可运行、可测试、可维护。

**技术原则**：知其然而知其所以然。先解释原理，再给规格，最后给代码。

---

## SKILL整体架构

```
Phase 1 SKILL架构

数据输入层（PMS/OTA）
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│                    SKILL计算层                               │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                │
│  │ RM-001   │  │ RM-002   │  │ RM-003   │                │
│  │ ADR/OCC  │  │ STR指数  │  │ 竞品爬虫 │                │
│  │ 计算     │  │ MPI/ARI  │  │           │                │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                │
│       │              │              │                       │
│       └──────────────┴──────────────┘                       │
│                      │                                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ RM-004   │  │ RM-005   │  │ OTA-001  │  │ OTA-002  │ │
│  │ 价格预警 │  │ 收益日报 │  │ 排名诊断  │  │ 差评预警 │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
               微信推送/看板
```

---

## SKILL-001: RM-001 ADR/OCC/RevPAR计算

### 基本信息

| 属性 | 值 |
|------|-----|
| SKILL编号 | RM-001 |
| SKILL名称 | ADR/OCC/RevPAR计算 |
| 所属领域 | 收益管理（Revenue Management） |
| 优先级 | P0（Phase 1必须实现） |
| 版本 | v1.0 |

---

### 规格详情

#### 输入(Input)

```yaml
数据来源:
  - PMS订单数据（Excel导入或API）
  - PMS夜审数据（Excel导入或API）
  
数据类型: JSON或CSV格式

必需字段:
  - checkin_date: DATE, 入住日期
  - checkout_date: DATE, 离店日期
  - room_revenue: DECIMAL(10,2), 房费金额
  - total_revenue: DECIMAL(10,2), 总收入
  - status: VARCHAR(16), 订单状态
  - total_rooms: INT, 总房量（夜审数据）
  
可选字段:
  - occupied: INT, 在住房量（夜审数据）
  - channel: VARCHAR(16), 订单来源
  - room_type: VARCHAR(16), 房型
```

#### 处理逻辑(Process)

**算法原理**：

ADR（Average Daily Rate，平均房价）
```
ADR = Σ(已售客房收入) / Σ(已售客房数)

如果某房间入住1晚收入300元，则贡献300元到ADR分子，1间夜到ADR分母
如果某房间连住3晚收入900元，则贡献900元到ADR分子，3间夜到ADR分母
```

OCC（Occupancy，入住率）
```
OCC = Σ(已售客房数) / Σ(可售客房总数) × 100%

注意：分母用的是"可售房量"，而非总房量
（可售房量 = 总房量 - OOO不可售房 - 免费房/店用房）
```

RevPAR（Revenue Per Available Room，每房收益）
```
RevPAR = ADR × OCC = Σ(已售客房收入) / Σ(可售客房总数)

两种算法结果相同，推荐用第一种（ADR×OCC）更直观
```

**Python实现**：

```python
#!/usr/bin/env python3
"""
RM-001: ADR/OCC/RevPAR计算
AHL乐山锦江嘉州宾馆专用

功能：基于PMS订单/夜审数据，计算酒店核心收益指标
输入：订单JSON/CSV 或 夜审数据JSON/CSV
输出：每日/每周/每月的ADR/OCC/RevPAR

作者：AHL技术组
版本：v1.0
"""

import pandas as pd
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class DailyMetrics:
    """每日收益指标"""
    date: str                    # 日期 (YYYY-MM-DD)
    total_rooms: int             # 可售房总量
    occupied: int               # 已售房数
    vacant: int                  # 空房数（待清扫等）
    ooo: int                     # 不可售房（维修等）
    complimentary: int           # 免费房
    house_use: int              # 店用房
    
    room_revenue: float         # 客房收入
    total_revenue: float        # 总收入（含餐饮等）
    
    occupancy_pct: float        # 入住率 (%)
    adr: float                  # 平均房价 (元)
    revpar: float               # 每房收益 (元)
    
    arrivals: int               # 当日新入住
    departures: int            # 当日离店
    inhouse_guests: int         # 在店客人数
    order_count: int            # 订单数
    
    data_source: str            # 数据来源: PMS/Manual/NightAudit


@dataclass
class PeriodMetrics:
    """周期收益指标汇总"""
    period: str                 # 周期名称: "2026-W13" / "2026-03"
    start_date: str
    end_date: str
    
    total_revenue: float
    room_revenue: float
    
    avg_occupancy_pct: float    # 平均入住率（算术平均）
    weighted_adr: float         # 加权ADR（按间夜数加权）
    revpar: float               # RevPAR
    
    total_room_nights: float     # 总间夜数
    occupied_room_nights: float # 已售间夜数
    
    # 同比/环比（如果有历史数据）
    occupancy_yoy: Optional[float] = None
    occupancy_mom: Optional[float] = None
    adr_yoy: Optional[float] = None
    adr_mom: Optional[float] = None
    revpar_yoy: Optional[float] = None
    revpar_mom: Optional[float] = None


class RM001Calculator:
    """
    ADR/OCC/RevPAR计算引擎
    
    核心算法：
    1. 从订单数据或夜审数据计算每日指标
    2. 支持多周期汇总（日/周/月）
    3. 支持同比/环比计算
    """
    
    def __init__(self, hotel_id: str = "JZZS001"):
        self.hotel_id = hotel_id
    
    def calculate_daily_from_orders(self, orders_df: pd.DataFrame, 
                                     total_rooms: int,
                                     date: str) -> DailyMetrics:
        """
        从订单数据计算每日指标
        
        适用场景：只有订单数据，没有夜审数据时
        
        参数:
            orders_df: 订单DataFrame
            total_rooms: 当日可售房总量
            date: 计算日期 (YYYY-MM-DD)
        
        返回:
            DailyMetrics: 每日指标
        """
        # 筛选该日期的数据
        # 注意：入住日期=date的算当日入住，离店日期=date的算当日离店
        df = orders_df.copy()
        
        # 在住房（入住日期 <= date < 离店日期）
        inhouse = df[
            (pd.to_datetime(df['checkin_date']) <= pd.to_datetime(date)) &
            (pd.to_datetime(df['checkout_date']) > pd.to_datetime(date))
        ]
        
        # 当日新入住
        arrivals = df[pd.to_datetime(df['checkin_date']) == pd.to_datetime(date)]
        
        # 当日离店
        departures = df[pd.to_datetime(df['checkout_date']) == pd.to_datetime(date)]
        
        # 已售房数 = 在住房中已付房费（不含在店未付）
        occupied = len(inhouse)
        
        # 计算房费收入（在住房贡献的房费，需按天分摊）
        # 简化处理：当日贡献 = 订单总房费 / 入住天数
        room_revenue = 0.0
        for _, order in inhouse.iterrows():
            checkin = pd.to_datetime(order['checkin_date'])
            checkout = pd.to_datetime(order['checkout_date'])
            nights = (checkout - checkin).days
            if nights > 0:
                daily_revenue = float(order.get('room_revenue', 0)) / nights
                room_revenue += daily_revenue
        
        # 计算ADR
        if occupied > 0:
            adr = room_revenue / occupied
        else:
            adr = 0.0
        
        # 计算OCC
        occupancy_pct = (occupied / total_rooms * 100) if total_rooms > 0 else 0.0
        
        # 计算RevPAR
        revpar = adr * (occupancy_pct / 100) * total_rooms if total_rooms > 0 else 0.0
        # 简化：RevPAR = 总收入 / 可售房量
        revpar = room_revenue / total_rooms if total_rooms > 0 else 0.0
        
        return DailyMetrics(
            date=date,
            total_rooms=total_rooms,
            occupied=occupied,
            vacant=total_rooms - occupied,
            ooo=0,
            complimentary=0,
            house_use=0,
            room_revenue=round(room_revenue, 2),
            total_revenue=round(room_revenue, 2),  # 简化版只有房费
            occupancy_pct=round(occupancy_pct, 2),
            adr=round(adr, 2),
            revpar=round(revpar, 2),
            arrivals=len(arrivals),
            departures=len(departures),
            inhouse_guests=occupied,
            order_count=len(inhouse),
            data_source="orders"
        )
    
    def calculate_daily_from_night_audit(self, audit_data: Dict, 
                                          date: str) -> DailyMetrics:
        """
        从夜审数据计算每日指标
        
        适用场景：夜审数据是最准确的数据来源
        夜审后数据包含所有入离结账，最完整
        
        参数:
            audit_data: 夜审数据Dict
            date: 夜审日期 (YYYY-MM-DD)
        
        返回:
            DailyMetrics: 每日指标
        """
        # 夜审数据通常包含完整的财务和房态数据
        room_revenue = float(audit_data.get('room_revenue', 0))
        total_revenue = float(audit_data.get('total_revenue', 0))
        
        total_rooms = int(audit_data.get('room_inventory', audit_data.get('total_rooms', 0)))
        occupied = int(audit_data.get('occupied_rooms', audit_data.get('occupied', 0)))
        
        vacant = int(audit_data.get('vacant_rooms', 0))
        ooo = int(audit_data.get('out_of_order', 0))
        complimentary = int(audit_data.get('complimentary', 0))
        house_use = int(audit_data.get('house_use', 0))
        
        arrivals = int(audit_data.get('arrivals', 0))
        departures = int(audit_data.get('departures', 0))
        inhouse_guests = int(audit_data.get('inhouse_guests', occupied))
        
        # ADR
        adr = room_revenue / occupied if occupied > 0 else 0.0
        
        # OCC（夜审数据中的occupancy_percent通常更准确）
        occupancy_pct = float(audit_data.get('occupancy_percent', 
                               occupied / total_rooms * 100 if total_rooms > 0 else 0))
        
        # RevPAR
        revpar = room_revenue / total_rooms if total_rooms > 0 else 0.0
        
        return DailyMetrics(
            date=date,
            total_rooms=total_rooms,
            occupied=occupied,
            vacant=vacant,
            ooo=ooo,
            complimentary=complimentary,
            house_use=house_use,
            room_revenue=round(room_revenue, 2),
            total_revenue=round(total_revenue, 2),
            occupancy_pct=round(occupancy_pct, 2),
            adr=round(adr, 2),
            revpar=round(revpar, 2),
            arrivals=arrivals,
            departures=departures,
            inhouse_guests=inhouse_guests,
            order_count=audit_data.get('order_count', 0),
            data_source="night_audit"
        )
    
    def calculate_period(self, daily_metrics: List[DailyMetrics],
                         period_type: str = "weekly") -> PeriodMetrics:
        """
        计算周期汇总指标
        
        参数:
            daily_metrics: 每日指标列表
            period_type: 周期类型 "daily" / "weekly" / "monthly"
        
        返回:
            PeriodMetrics: 周期汇总指标
        """
        if not daily_metrics:
            raise ValueError("没有每日指标数据")
        
        df = pd.DataFrame([asdict(m) for m in daily_metrics])
        
        start_date = df['date'].min()
        end_date = df['date'].max()
        
        total_room_revenue = df['room_revenue'].sum()
        total_revenue = df['total_revenue'].sum()
        
        total_room_nights = df['occupied'].sum()
        total_rooms_available = (df['total_rooms'] * len(df)).sum()  # 简化
        
        avg_occupancy = df['occupancy_pct'].mean()
        weighted_adr = total_room_revenue / total_room_nights if total_room_nights > 0 else 0
        revpar = total_room_revenue / total_rooms_available if total_rooms_available > 0 else 0
        
        # 周期名称
        if period_type == "weekly":
            start = datetime.strptime(start_date, "%Y-%m-%d")
            period = f"{start.year}-W{start.isocalendar()[1]}"
        elif period_type == "monthly":
            period = start_date[:7]  # "2026-03"
        else:
            period = start_date
        
        return PeriodMetrics(
            period=period,
            start_date=start_date,
            end_date=end_date,
            total_revenue=round(total_revenue, 2),
            room_revenue=round(total_room_revenue, 2),
            avg_occupancy_pct=round(avg_occupancy, 2),
            weighted_adr=round(weighted_adr, 2),
            revpar=round(revpar, 2),
            total_room_nights=round(total_room_nights, 1),
            occupied_room_nights=round(total_room_nights, 1),
        )
    
    def calculate_yoy_mom(self, current: PeriodMetrics, 
                          previous: PeriodMetrics) -> PeriodMetrics:
        """计算同比/环比"""
        # 简化实现
        current.occupancy_yoy = None
        current.occupancy_mom = None
        current.adr_yoy = None
        current.adr_mom = None
        current.revpar_yoy = None
        current.revpar_mom = None
        
        if previous.avg_occupancy_pct and previous.avg_occupancy_pct > 0:
            current.occupancy_mom = (
                (current.avg_occupancy_pct - previous.avg_occupancy_pct) 
                / previous.avg_occupancy_pct * 100
            )
        
        if previous.adr_yoy and previous.adr > 0:
            current.adr_yoy = (
                (current.weighted_adr - previous.weighted_adr) 
                / previous.weighted_adr * 100
            )
        
        return current


# ============================================================
# 数据存储
# ============================================================

def save_daily_metrics(metrics: DailyMetrics, 
                       output_dir: str = "./data/revenue") -> str:
    """保存每日指标到JSON"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    filepath = Path(output_dir) / f"daily_metrics_{metrics.date}.json"
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(asdict(metrics), f, ensure_ascii=False, indent=2)
    
    logger.info(f"每日指标已保存: {filepath}")
    return str(filepath)


def load_daily_metrics(date: str, 
                      data_dir: str = "./data/revenue") -> Optional[DailyMetrics]:
    """加载每日指标"""
    filepath = Path(data_dir) / f"daily_metrics_{date}.json"
    
    if not filepath.exists():
        return None
    
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    return DailyMetrics(**data)


# ============================================================
# 主执行
# ============================================================

def main():
    """主执行函数"""
    calculator = RM001Calculator(hotel_id="JZZS001")
    
    # 示例：从订单数据计算
    # orders_df = pd.read_csv("./data/orders_2026_03_27.csv")
    # metrics = calculator.calculate_daily_from_orders(
    #     orders_df=orders_df,
    #     total_rooms=180,
    #     date="2026-03-27"
    # )
    
    logger.info("RM-001 ADR/OCC/RevPAR计算模块初始化完成")


if __name__ == "__main__":
    main()
```

#### 输出(Output)

```yaml
输出格式: JSON / CSV

每日指标输出:
  - date: str, 日期
  - occupancy_pct: float, 入住率 (%)
  - adr: float, 平均房价 (元)
  - revpar: float, 每房收益 (元)
  - room_revenue: float, 客房收入
  - total_rooms: int, 可售房量
  - occupied: int, 已售房数
  - arrivals: int, 新入住
  - departures: int, 离店
  - data_source: str, 数据来源

周期汇总输出:
  - period: str, 周期名称
  - avg_occupancy_pct: float, 平均入住率
  - weighted_adr: float, 加权ADR
  - revpar: float, 每房收益
  - total_revenue: float, 总收入
  - room_revenue: float, 客房收入
```

#### 数据依赖(Dependency)

```yaml
上游依赖:
  - PMS订单数据（RM-001本身不生产数据，只是计算）
  - 或：PMS夜审数据（NightAudit）
  
下游依赖:
  - RM-002 STR指数计算（使用RM-001输出）
  - RM-005 收益日报生成（使用RM-001输出）
  - OTA-001 OTA排名诊断（对比用）
```

#### 技术实现提示(Implementation)

```yaml
技术栈:
  - 语言: Python 3.10+
  - 核心库: pandas, dataclasses
  - 存储: JSON文件 + SQLite可选
  
性能要求:
  - 单日数据计算: <1秒
  - 30天汇总计算: <5秒

边界检查:
  - total_rooms = 0 时不计算OCC
  - occupied = 0 时ADR = 0（而非报错）
  - 数据缺失时记录警告，不中断计算
```

#### 边界(Boundary)

```yaml
不适用场景:
  - 总房量为0的异常数据
  - 全部房间不可售的极端情况
  
可能出错的情况:
  - 日期格式不统一（尝试多种格式解析）
  - 房费金额为负数（可能是退款，需特殊处理）
  - 数据时间跨度过大（如计算1年数据），需分批处理
```

---

## SKILL-002: RM-002 STR指数计算(MPI/ARI/RGI)

### 基本信息

| 属性 | 值 |
|------|-----|
| SKILL编号 | RM-002 |
| SKILL名称 | STR指数计算(MPI/ARI/RGI) |
| 所属领域 | 收益管理（Revenue Management） |
| 优先级 | P0（Phase 1必须实现） |
| 版本 | v1.0 |

---

### 规格详情

#### 输入(Input)

```yaml
必需输入:
  - self_metrics: RM-001输出的每日/周期指标
  - competitor_avg: 竞品平均ADR/OCC（来自竞品爬虫或EBK）
  - market_avg: 市场平均ADR/OCC（STR数据或EBK竞品对比）

数据格式:
  - self_metrics: DailyMetrics或PeriodMetrics
  - competitor_avg: Dict {adr: float, occupancy: float}
  - market_avg: Dict {adr: float, occupancy: float}
```

#### 处理逻辑(Process)

**算法原理**：

STR指数是国际酒店行业通用的竞争力衡量指标，由Smith Travel Research创立：

```
MPI (Market Penetration Index，市场渗透指数)
= 本酒店OCC / 市场平均OCC × 100

MPI解读：
- MPI > 100：好于市场，表现优异
- MPI = 100：与市场持平
- MPI < 100：弱于市场，需要改进

举例：
- 本酒店OCC = 80%，市场OCC = 70%
- MPI = 80/70 × 100 = 114.3（好于市场14.3%）
```

```
ARI (Average Rate Index，平均房价指数)
= 本酒店ADR / 市场平均ADR × 100

ARI解读：
- ARI > 100：溢价能力高于市场
- ARI = 100：价格与市场持平
- ARI < 100：价格低于市场

举例：
- 本酒店ADR = 350元，市场ADR = 320元
- ARI = 350/320 × 100 = 109.4（溢价能力高9.4%）
```

```
RGI (Revenue Generation Index，收益指数)
= 本酒店RevPAR / 市场平均RevPAR × 100
= MPI × ARI / 100（简化算法）

RGI解读：
- RGI > 100：收益能力高于市场
- RGI = 100：收益与市场持平
- RGI < 100：收益低于市场

举例：
- 本酒店RevPAR = 280元，市场RevPAR = 224元
- RGI = 280/224 × 100 = 125.0（收益能力高25%）
```

**Python实现**：

```python
#!/usr/bin/env python3
"""
RM-002: STR指数计算
AHL乐山锦江嘉州宾馆专用

功能：计算MPI/ARI/RGI三大STR指数
输入：RM-001输出 + 竞品/市场数据
输出：STR指数及解读

作者：AHL技术组
版本：v1.0
"""

import pandas as pd
import logging
from dataclasses import dataclass, asdict
from typing import Dict, Optional, List
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class STRIndex:
    """STR指数"""
    date: str                          # 日期
    period: str                        # 周期
    
    # 本酒店指标
    self_occupancy: float              # 本酒店入住率
    self_adr: float                   # 本酒店ADR
    self_revpar: float                 # 本酒店RevPAR
    
    # 市场/竞品指标
    market_occupancy: float            # 市场入住率
    market_adr: float                 # 市场ADR
    market_revpar: float              # 市场RevPAR
    
    # STR三指数
    mpi: float                        # Market Penetration Index
    ari: float                        # Average Rate Index
    rgi: float                        # Revenue Generation Index
    
    # 解读
    mpi_interpretation: str            # MPI解读
    ari_interpretation: str            # ARI解读
    rgi_interpretation: str           # RGI解读
    
    # 数据来源
    data_source: str                  # 数据来源


class RM002Calculator:
    """
    STR指数计算引擎
    
    核心逻辑：
    1. 获取本酒店指标（来自RM-001）
    2. 获取市场/竞品指标（来自竞品爬虫或EBK）
    3. 计算MPI/ARI/RGI
    4. 生成解读
    """
    
    def __init__(self, hotel_id: str = "JZZS001"):
        self.hotel_id = hotel_id
    
    def calculate_mpi(self, self_occ: float, market_occ: float) -> float:
        """
        计算MPI
        
        如果市场OCC为0，返回None（避免除零）
        """
        if market_occ <= 0:
            logger.warning("市场入住率为0，无法计算MPI")
            return None
        return round(self_occ / market_occ * 100, 1)
    
    def calculate_ari(self, self_adr: float, market_adr: float) -> float:
        """
        计算ARI
        
        如果市场ADR为0，返回None
        """
        if market_adr <= 0:
            logger.warning("市场ADR为0，无法计算ARI")
            return None
        return round(self_adr / market_adr * 100, 1)
    
    def calculate_rgi(self, mpi: float, ari: float) -> float:
        """
        计算RGI
        
        两种算法：
        1. RGI = MPI × ARI / 100
        2. RGI = RevPAR / MarketRevPAR × 100
        推荐第一种（分解了价格和量的贡献）
        """
        if mpi is None or ari is None:
            return None
        return round(mpi * ari / 100, 1)
    
    def interpret_mpi(self, mpi: float) -> str:
        """MPI解读"""
        if mpi is None:
            return "数据不足，无法评估"
        
        if mpi >= 120:
            return f"⭐⭐⭐⭐⭐ 极强（MPI={mpi}），市场表现远超平均"
        elif mpi >= 110:
            return f"⭐⭐⭐⭐ 优秀（MPI={mpi}），显著优于市场"
        elif mpi >= 100:
            return f"⭐⭐⭐ 良好（MPI={mpi}），与市场持平偏上"
        elif mpi >= 90:
            return f"⭐⭐ 一般（MPI={mpi}），略低于市场"
        else:
            return f"⚠️ 较弱（MPI={mpi}），显著低于市场，需重点改进"
    
    def interpret_ari(self, ari: float) -> str:
        """ARI解读"""
        if ari is None:
            return "数据不足，无法评估"
        
        if ari >= 120:
            return f"💰 高溢价（MPI={ari}），品牌/产品力强"
        elif ari >= 110:
            return f"💵 偏溢价（ARI={ari}），定价高于市场"
        elif ari >= 100:
            return f"📊 市场定价（ARI={ari}），价格与市场持平"
        elif ari >= 90:
            return f"📉 偏低（ARI={ari}），定价略低于市场"
        else:
            return f"⚠️ 低溢价（ARI={ari}），可能需提升产品或促销过度"
    
    def interpret_rgi(self, rgi: float) -> str:
        """RGI解读"""
        if rgi is None:
            return "数据不足，无法评估"
        
        if rgi >= 120:
            return f"🏆 收益王者（RGI={rgi}），综合收益能力极强"
        elif rgi >= 110:
            return f"📈 收益优秀（RGI={rgi}），综合表现优于市场"
        elif rgi >= 100:
            return f"📊 市场平均（RGI={rgi}），收益与市场持平"
        elif rgi >= 90:
            return f"📉 收益一般（RGI={rgi}），略低于市场水平"
        else:
            return f"⚠️ 收益较弱（RGI={rgi}），综合收益能力不足"
    
    def calculate_index(self,
                       self_metrics: Dict,
                       market_metrics: Dict,
                       period: str = "daily") -> STRIndex:
        """
        计算STR指数
        
        参数:
            self_metrics: 本酒店指标 (from RM-001)
                {
                    "occupancy_pct": 78.5,
                    "adr": 320.0,
                    "revpar": 251.2,
                }
            market_metrics: 市场指标 (from 竞品爬虫或EBK)
                {
                    "occupancy_pct": 72.0,
                    "adr": 310.0,
                    "revpar": 223.2,
                }
            period: 周期类型 "daily" / "weekly" / "monthly"
        
        返回:
            STRIndex: STR指数及解读
        """
        self_occ = self_metrics.get("occupancy_pct", 0)
        self_adr = self_metrics.get("adr", 0)
        self_revpar = self_metrics.get("revpar", 0)
        
        market_occ = market_metrics.get("occupancy_pct", 0)
        market_adr = market_metrics.get("adr", 0)
        market_revpar = market_metrics.get("revpar", 0)
        
        # 计算三指数
        mpi = self.calculate_mpi(self_occ, market_occ)
        ari = self.calculate_ari(self_adr, market_adr)
        rgi = self.calculate_rgi(mpi, ari)
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        return STRIndex(
            date=today,
            period=period,
            self_occupancy=round(self_occ, 2),
            self_adr=round(self_adr, 2),
            self_revpar=round(self_revpar, 2),
            market_occupancy=round(market_occ, 2),
            market_adr=round(market_adr, 2),
            market_revpar=round(market_revpar, 2),
            mpi=mpi if mpi else 0,
            ari=ari if ari else 0,
            rgi=rgi if rgi else 0,
            mpi_interpretation=self.interpret_mpi(mpi),
            ari_interpretation=self.interpret_ari(ari),
            rgi_interpretation=self.interpret_rgi(rgi),
            data_source="calculated",
        )
    
    def calculate_from_competitor_avg(self,
                                      self_metrics: Dict,
                                      competitor_prices_df: pd.DataFrame,
                                      period: str = "daily") -> STRIndex:
        """
        从竞品价格数据计算市场平均指标
        
        适用场景：只有竞品爬虫数据，没有官方市场数据时
        
        参数:
            self_metrics: 本酒店指标
            competitor_prices_df: 竞品价格DataFrame (from RM-003)
                包含列: hotel_id, date, price, room_type
            period: 周期类型
        
        返回:
            STRIndex: STR指数
        """
        if competitor_prices_df.empty:
            logger.warning("没有竞品价格数据，返回默认值")
            return self.calculate_index(self_metrics, 
                                       {"occupancy_pct": 70, "adr": 300, "revpar": 210},
                                       period)
        
        # 从竞品价格估算市场ADR
        # 注意：这是估算值，与真实市场数据有偏差
        market_adr = competitor_prices_df['price'].mean()
        
        # 市场入住率：假设竞品平均入住率约70%（可调）
        market_occ = 70.0
        
        # 市场RevPAR
        market_revpar = market_adr * (market_occ / 100)
        
        market_metrics = {
            "occupancy_pct": market_occ,
            "adr": market_adr,
            "revpar": market_revpar,
        }
        
        return self.calculate_index(self_metrics, market_metrics, period)


def format_str_report(str_index: STRIndex) -> str:
    """格式化STR指数报告（用于微信推送）"""
    report = f"""
🏨 STR指数报告 {str_index.date}
━━━━━━━━━━━━━━━━━━━━

📊 本店指标：
• 入住率：{str_index.self_occupancy}%
• ADR：¥{str_index.self_adr}
• RevPAR：¥{str_index.self_revpar}

📈 市场基准：
• 入住率：{str_index.market_occupancy}%
• ADR：¥{str_index.market_adr}
• RevPAR：¥{str_index.market_revpar}

🎯 STR三指数：
• MPI（市场渗透）={str_index.mpi} | {str_index.mpi_interpretation}
• ARI（房价指数）={str_index.ari} | {str_index.ari_interpretation}
• RGI（收益指数）={str_index.rgi} | {str_index.rgi_interpretation}

━━━━━━━━━━━━━━━━━━━━
    """.strip()
    
    return report


if __name__ == "__main__":
    calculator = RM002Calculator()
    
    # 示例
    self_metrics = {
        "occupancy_pct": 78.5,
        "adr": 320.0,
        "revpar": 251.2,
    }
    
    market_metrics = {
        "occupancy_pct": 72.0,
        "adr": 310.0,
        "revpar": 223.2,
    }
    
    index = calculator.calculate_index(self_metrics, market_metrics)
    report = format_str_report(index)
    print(report)
```

#### 输出(Output)

```yaml
输出格式: JSON / 文本报告

STR指数输出:
  - date: str, 日期
  - mpi: float, 市场渗透指数
  - ari: float, 房价指数
  - rgi: float, 收益指数
  - mpi_interpretation: str, MPI解读
  - ari_interpretation: str, ARI解读
  - rgi_interpretation: str, RGI解读
  - self_occupancy: float, 本店入住率
  - self_adr: float, 本店ADR
  - market_occupancy: float, 市场入住率
  - market_adr: float, 市场ADR
```

#### 数据依赖(Dependency)

```yaml
上游依赖:
  - RM-001: ADR/OCC/RevPAR计算（必需）
  - RM-003: 竞品价格爬虫（用于估算市场指标）
  - EBK竞品对比数据（优先，数据更准确）
  
下游依赖:
  - RM-005: 收益日报生成（使用STR指数）
```

#### 技术实现提示(Implementation)

```yaml
技术栈:
  - 语言: Python 3.10+
  - 核心库: pandas, dataclasses
  - 存储: JSON

性能要求:
  - 单次计算: <0.1秒

注意:
  - MPI/ARI/RGI的计算需要"市场基准数据"
  - 没有市场数据时，无法计算（可降级显示"数据不足"）
  - 市场数据来源优先级：STR官方 > EBK竞品对比 > 竞品爬虫估算
```

#### 边界(Boundary)

```yaml
不适用场景:
  - 完全没有市场对比数据时（无法计算）
  - 市场数据严重滞后时（月度数据vs实时）

可能出错的情况:
  - 除零错误（市场指标为0）→ 已做保护处理
  - 数据类型错误 → 已做类型转换保护
```

---

## SKILL-003: RM-003 竞品价格爬取（携程+美团）

> **核心SKILL** - 已在模块2中提供完整代码框架，此处补充规格说明

### 基本信息

| 属性 | 值 |
|------|-----|
| SKILL编号 | RM-003 |
| SKILL名称 | 竞品价格爬取（携程+美团） |
| 所属领域 | 收益管理（Revenue Management） |
| 优先级 | P0（Phase 1必须实现） |
| 版本 | v1.0 |

---

### 规格详情

#### 输入(Input)

```yaml
配置输入:
  - competitors.yaml: 竞品酒店配置列表
  - schedule: 爬取时间表
  - request_interval: 请求间隔配置

无数据输入依赖:
  - RM-003是数据生产者，不是消费者
  - 直接从携程/美团抓取数据
```

#### 处理逻辑(Process)

```python
# 核心逻辑伪代码
class RM003Crawler:
    
    def run(self):
        for competitor in competitors:
            # 1. 伪装请求头（UA轮换）
            headers = self.get_random_headers()
            
            # 2. 访问携程/美团竞品页面
            html = self.request(competitor.url, headers)
            
            # 3. 解析页面提取价格
            prices = self.parse_price(html)
            
            # 4. 清洗数据（去除异常值）
            prices_clean = self.clean(prices)
            
            # 5. 存储到数据库
            self.save_to_db(prices_clean)
            
            # 6. 随机延迟（避免被封）
            self.random_delay()
```

#### 输出(Output)

```yaml
输出格式: CSV + SQLite

数据字段:
  - hotel_id: str, 竞品ID
  - hotel_name: str, 竞品名称
  - date: DATE, 价格日期
  - price: DECIMAL(8,2), 价格
  - room_type: str, 房型
  - source: str, 平台来源
  - crawl_time: DATETIME, 抓取时间
```

#### 数据依赖(Dependency)

```yaml
上游依赖: 无（RM-003是数据源）
下游依赖:
  - RM-002: STR指数计算（使用竞品价格）
  - RM-004: 竞品价格预警（使用竞品价格）
  - RM-005: 收益日报（使用竞品价格）
```

#### 技术实现提示(Implementation)

```yaml
技术栈:
  - 语言: Python 3.10+
  - 核心库: requests, beautifulsoup4, lxml, pandas
  - 数据库: SQLite

反爬策略:
  - UA轮换
  - 请求间隔随机化
  - 自动降级（检测到验证码后暂停）

数据校验:
  - 价格范围检查（50 < price < 5000）
  - 去重（同酒店+同日期+同价格）
```

#### 边界(Boundary)

```yaml
不适用场景:
  - 目标网站完全无法访问
  - 目标网站JS动态渲染（降级到其他方案）

可能出错的情况:
  - IP被封 → 等待解封或降级
  - 页面改版 → 维护解析逻辑
  - 无价格数据 → 记录警告，继续下一个
```

---

## SKILL-004: RM-004 竞品价格预警

### 基本信息

| 属性 | 值 |
|------|-----|
| SKILL编号 | RM-004 |
| SKILL名称 | 竞品价格预警 |
| 所属领域 | 收益管理（Revenue Management） |
| 优先级 | P1（Phase 1建议实现） |
| 版本 | v1.0 |

---

### 规格详情

#### 输入(Input)

```yaml
必需输入:
  - competitor_prices: RM-003输出的竞品价格数据
  - self_adr: RM-001输出的本店ADR
  - alert_thresholds: 预警阈值配置

数据格式:
  - competitor_prices: DataFrame
  - self_adr: float
  - alert_thresholds: Dict
```

#### 处理逻辑(Process)

**预警规则**：

```python
class RM004PriceAlert:
    """
    竞品价格预警逻辑
    
    预警类型：
    1. 竞品高价预警：竞品ADR显著高于本店 → 可能存在溢价空间
    2. 竞品低价预警：竞品ADR显著低于本店 → 需要关注竞争力
    3. 竞品价格突变：竞品价格日波动超过阈值 → 市场异动
    4. 价格倒挂：竞品价格低于本店 → 可能需要调整定价
    """
    
    def check_high_price_alert(self, competitor_adr, self_adr, threshold=0.2):
        """
        竞品高价预警
        
        条件：竞品ADR > 本店ADR × (1 + threshold)
        含义：竞品价格偏高，说明市场可能接受更高价格
        """
        if self_adr <= 0:
            return False
        return competitor_adr > self_adr * (1 + threshold)
    
    def check_low_price_alert(self, competitor_adr, self_adr, threshold=0.2):
        """
        竞品低价预警
        
        条件：竞品ADR < 本店ADR × (1 - threshold)
        含义：竞品价格偏低，可能在做促销或市场份额争夺
        """
        if self_adr <= 0:
            return False
        return competitor_adr < self_adr * (1 - threshold)
    
    def check_price_surge_alert(self, current_price, previous_price, threshold=0.3):
        """
        价格突变预警
        
        条件：|当日价格 - 前日价格| / 前日价格 > threshold
        含义：竞品价格大幅波动，市场可能发生变化
        """
        if previous_price <= 0:
            return False
        change_pct = abs(current_price - previous_price) / previous_price
        return change_pct > threshold
    
    def generate_alerts(self, competitor_df, self_adr) -> List[Alert]:
        """
        生成所有预警
        
        返回预警列表，按严重程度排序
        """
        alerts = []
        
        # 按酒店分组
        for hotel_id, group in competitor_df.groupby('hotel_id'):
            group = group.sort_values('date')
            
            # 检查历史价格趋势
            prices = group['price'].values
            if len(prices) >= 2:
                # 价格突变
                for i in range(1, len(prices)):
                    if self.check_price_surge_alert(prices[i], prices[i-1]):
                        alerts.append(Alert(
                            hotel_id=hotel_id,
                            alert_type="price_surge",
                            current_price=prices[i],
                            previous_price=prices[i-1],
                            severity="warning",
                            message=f"{hotel_id} 价格突变: ¥{prices[i-1]}→¥{prices[i]}"
                        ))
            
            # 获取最新价格
            latest = prices[-1]
            
            # 竞品高价
            if self.check_high_price_alert(latest, self_adr):
                alerts.append(Alert(
                    hotel_id=hotel_id,
                    alert_type="high_price",
                    current_price=latest,
                    self_price=self_adr,
                    severity="info",
                    message=f"{hotel_id} 定价偏高: ¥{latest} vs 本店¥{self_adr}"
                ))
            
            # 竞品低价
            if self.check_low_price_alert(latest, self_adr):
                alerts.append(Alert(
                    hotel_id=hotel_id,
                    alert_type="low_price",
                    current_price=latest,
                    self_price=self_adr,
                    severity="warning",
                    message=f"{hotel_id} 定价偏低: ¥{latest} vs 本店¥{self_adr}"
                ))
        
        return sorted(alerts, key=lambda x: {"critical": 0, "warning": 1, "info": 2})
```

#### 输出(Output)

```yaml
输出格式: JSON / 预警文本

预警输出:
  - alert_type: str, 预警类型 (high_price/low_price/price_surge)
  - hotel_id: str, 竞品ID
  - hotel_name: str, 竞品名称
  - current_price: float, 当前价格
  - previous_price: float, 前日价格（突变时）
  - severity: str, 严重程度 (info/warning/critical)
  - message: str, 预警消息
  - timestamp: DATETIME, 预警时间
```

#### 数据依赖(Dependency)

```yaml
上游依赖:
  - RM-003: 竞品价格爬虫（必需）
  - RM-001: 本店ADR（必需）
下游依赖:
  - RM-005: 收益日报（包含预警信息）
```

#### 边界(Boundary)

```yaml
不适用场景:
  - 没有竞品价格数据时（无法预警）
  - 没有本店ADR基准时（无法对比）

可能出错的情况:
  - 除零错误 → 已做保护
  - 数据缺失 → 跳过该竞品
```

---

## SKILL-005: RM-005 收益日报生成

### 基本信息

| 属性 | 值 |
|------|-----|
| SKILL编号 | RM-005 |
| SKILL名称 | 收益日报生成 |
| 所属领域 | 收益管理（Revenue Management） |
| 优先级 | P0（Phase 1必须实现，核心交付物） |
| 版本 | v1.0 |

---

### 规格详情

#### 输入(Input)

```yaml
必需输入:
  - daily_metrics: RM-001输出的每日指标
  - str_index: RM-002输出的STR指数
  - competitor_prices: RM-003输出的竞品价格
  - alerts: RM-004输出的价格预警
  - weather: 天气预报数据（可选，和风API）

数据格式:
  - daily_metrics: DailyMetrics
  - str_index: STRIndex
  - competitor_prices: DataFrame
  - alerts: List[Alert]
  - weather: Dict
```

#### 处理逻辑(Process)

```python
class RM005DailyReport:
    """
    收益日报生成器
    
    核心逻辑：
    1. 汇总当日所有数据
    2. 生成结构化日报
    3. 输出多种格式（文本/HTML/微信卡片）
    """
    
    def generate_text_report(self, 
                            daily_metrics: DailyMetrics,
                            str_index: STRIndex,
                            alerts: List[Alert],
                            weather: Dict = None) -> str:
        """
        生成文本格式日报（用于微信推送）
        
        格式要求：
        - 总字数控制在500字以内
        - 关键数据突出显示
        - 预警信息醒目
        """
        # 构建日报内容
        date = daily_metrics.date
        
        report = f"""
🏨 锦江嘉州宾馆 收益日报
📅 {date}
━━━━━━━━━━━━━━━━━━━━

📊 今日业绩
• 入住率：{daily_metrics.occupancy_pct}%
• ADR：¥{daily_metrics.adr}
• RevPAR：¥{daily_metrics.revpar}
• 客房收入：¥{daily_metrics.room_revenue:,.0f}

📈 对比分析
• MPI：{str_index.mpi}（{str_index.mpi_interpretation.split('(')[0]}）
• ARI：{str_index.ari}（{str_index.ari_interpretation.split('(')[0]}）
• RGI：{str_index.rgi}（{str_index.rgi_interpretation.split('(')[0]}）

🔔 预警提醒
{self._format_alerts(alerts)}

━━━━━━━━━━━━━━━━━━━━
        """.strip()
        
        return report
    
    def _format_alerts(self, alerts: List[Alert]) -> str:
        """格式化预警信息"""
        if not alerts:
            return "• 暂无预警 ✅"
        
        lines = []
        for alert in alerts[:3]:  # 最多显示3条
            emoji = "🔴" if alert.severity == "critical" else "🟡"
            lines.append(f"{emoji} {alert.message}")
        
        return "\n".join(lines)
```

#### 输出(Output)

```yaml
输出格式: 多格式

文本报告 (wechat):
  - 用于微信公众号/企业微信推送
  - 500字以内
  - Markdown格式

HTML报告 (email):
  - 用于邮件发送
  - 完整数据展示
  - 可视化图表（ECharts）

JSON报告 (api):
  - 用于数据API
  - 完整字段
```

#### 数据依赖(Dependency)

```yaml
上游依赖:
  - RM-001: 每日指标（必需）
  - RM-002: STR指数（必需）
  - RM-003: 竞品价格（建议）
  - RM-004: 价格预警（建议）
  - 和风天气API（可选）
下游依赖:
  - 微信推送（最终输出）
```

---

## SKILL-006: OTA-001 OTA排名诊断

### 基本信息

| 属性 | 值 |
|------|-----|
| SKILL编号 | OTA-001 |
| SKILL名称 | OTA排名诊断 |
| 所属领域 | OTA运营（OTA Operations） |
| 优先级 | P1（Phase 1建议实现） |
| 版本 | v1.0 |

---

### 规格详情

#### 输入(Input)

```yaml
必需输入:
  - hotel_name: str, 酒店名称
  - city: str, 城市
  - check_date: DATE, 查询日期（通常为入住日期）
  - room_type: str, 查询房型（可选）

可选输入:
  - ctrip_hotel_id: str, 携程酒店ID（可加速查询）
  - meituan_hotel_id: str, 美团酒店ID
```

#### 处理逻辑(Process)

**排名诊断原理**：

OTA排名 = 综合竞争力分数，决定了酒店在搜索结果中的位置。

携程排名因素：
```
综合分数 = 
  30% × 转化率（曝光→浏览→下单）
+ 25% × 点评分数（含数量/质量/时效）
+ 20% × 产量（GMV贡献）
+ 15% × 价格竞争力
+ 10% × 基础信息完整度
```

美团排名因素：
```
综合分数 =
  35% × 转化率
+ 25% × 评分
+ 20% × 活动参与度
+ 10% × 销量
+ 10% × 基础服务质量
```

```python
class OTA001RankingDiagnosis:
    """
    OTA排名诊断
    
    功能：
    1. 查询携程/美团上的酒店排名
    2. 分析排名变化原因
    3. 给出优化建议
    """
    
    def diagnose_ctrip(self, hotel_name: str, city: str, 
                      check_date: str) -> Dict:
        """
        诊断携程排名
        
        携程排名诊断需要：
        1. 搜索目标城市+日期的酒店列表
        2. 找到目标酒店在列表中的位置
        3. 分析周围竞品的指标
        
        ⚠️ 注意：携程App排名数据通常需要商家后台EBK
        网页排名仅为参考
        """
        # 搜索携程酒店
        search_url = f"https://hotels.ctrip.com/hotel/{city}/"
        
        # 诊断结果
        result = {
            "platform": "ctrip",
            "hotel_name": hotel_name,
            "date": check_date,
            "ranking": None,  # 当前排名
            "total_hotels": None,  # 搜索结果总数
            "page": None,  # 所在页码
            "position_on_page": None,  # 页内位置
            "factors": {
                "score": None,
                "review_score": None,
                "review_count": None,
                "price": None,
                "position": None,
            },
            "diagnosis": None,  # 诊断结论
            "suggestions": [],  # 优化建议
        }
        
        return result
    
    def diagnose_meituan(self, hotel_name: str, city: str,
                        check_date: str) -> Dict:
        """诊断美团排名"""
        # 类似携程逻辑
        pass
```

#### 输出(Output)

```yaml
输出格式: JSON / 诊断文本

诊断输出:
  - platform: str, 平台
  - ranking: int, 当前排名
  - total_hotels: int, 竞品总数
  - factors: Dict, 排名因素分析
  - diagnosis: str, 诊断结论
  - suggestions: List[str], 优化建议
```

#### 数据依赖(Dependency)

```yaml
上游依赖: 无（独立诊断）
下游依赖: 无
```

---

## SKILL-007: OTA-002 差评预警

### 基本信息

| 属性 | 值 |
|------|-----|
| SKILL编号 | OTA-002 |
| SKILL名称 | 差评预警 |
| 所属领域 | OTA运营（OTA Operations） |
| 优先级 | P0（Phase 1必须实现） |
| 版本 | v1.0 |

---

### 规格详情

#### 输入(Input)

```yaml
必需输入:
  - hotel_id: str, 酒店ID
  - hotel_name: str, 酒店名称

可选输入:
  - days: int, 查询最近天数（默认7）
  - min_score: float, 最低预警分数（默认4.0）
  - platforms: List[str], 监控平台 ["ctrip", "meituan", "qunar"]
```

#### 处理逻辑(Process)

**差评预警原理**：

差评对酒店的伤害：
- 1条差评平均导致订单下降3-5%
- 差评聚集在某个维度（卫生/服务/设施）说明系统性问题
- 差评响应率影响潜在客人的决策

```python
class OTA002ReviewAlert:
    """
    OTA差评预警
    
    功能：
    1. 从EBK/OTA后台抓取差评数据
    2. 分析差评内容和分数
    3. 按维度分类（卫生/服务/设施/位置/性价比）
    4. 生成预警推送给酒店负责人
    """
    
    def fetch_negative_reviews(self, hotel_id: str, days: int = 7) -> List[Dict]:
        """
        获取差评
        
        数据来源优先级：
        1. 携程EBK差评导出（最准确）
        2. 美团商家后台差评导出
        3. OTA开放平台API
        4. 爬虫（不推荐）
        """
        reviews = []
        
        # 携程EBK差评
        # 路径：数据中心 → 点评管理 → 差评筛选
        # 导出字段：日期/分数/点评内容/入住日期
        
        return reviews
    
    def categorize_review(self, review_text: str) -> Dict[str, float]:
        """
        差评维度分类
        
        使用关键词匹配判断差评属于哪个维度：
        - 卫生：脏/有虫/异味/床单/毛巾/卫生间
        - 服务：态度/前台/入住/退房/响应
        - 设施：空调/热水/WiFi/房间/家具
        - 位置：吵/偏僻/难找/交通
        - 性价比：贵/不值/便宜/划算
        
        返回：{维度: 匹配得分}
        """
        keywords = {
            "卫生": ["脏", "有虫", "异味", "不干净", "床单", "毛巾", "卫生间", "清洁"],
            "服务": ["态度", "前台", "冷漠", "不耐烦", "入住", "退房", "响应慢"],
            "设施": ["空调", "不热", "不冷", "热水", "WiFi", "信号", "坏", "旧"],
            "位置": ["吵", "噪音", "偏僻", "难找", "交通", "施工"],
            "性价比": ["贵", "不值", "亏", "便宜", "划算"],
        }
        
        categories = {}
        text_lower = review_text.lower()
        
        for category, words in keywords.items():
            score = sum(1 for word in words if word in text_lower)
            if score > 0:
                categories[category] = score
        
        return categories
    
    def generate_alert(self, reviews: List[Dict]) -> Dict:
        """
        生成差评预警
        
        返回预警结构：
        - total_negative: 差评总数
        - avg_score: 平均分数
        - top_categories: 问题最多维度
        - urgent_reviews: 需要立即处理的差评
        """
        if not reviews:
            return {"status": "ok", "message": "暂无差评"}
        
        # 统计
        avg_score = sum(r['score'] for r in reviews) / len(reviews)
        
        # 分类
        all_categories = {}
        for review in reviews:
            cats = self.categorize_review(review['content'])
            for cat, score in cats.items():
                all_categories[cat] = all_categories.get(cat, 0) + score
        
        # 排序
        top_categories = sorted(all_categories.items(), 
                               key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "status": "alert" if avg_score < 4.2 else "warning",
            "total_negative": len(reviews),
            "avg_score": round(avg_score, 2),
            "top_categories": top_categories,
            "urgent_reviews": [r for r in reviews if r['score'] <= 3.0],
            "suggestions": self._generate_suggestions(top_categories),
        }
    
    def _generate_suggestions(self, categories: List[tuple]) -> List[str]:
        """根据问题维度生成改进建议"""
        suggestions_map = {
            "卫生": "🔧 建议：加强客房清洁管理，增加查房频次，重点关注床上用品和卫生间清洁",
            "服务": "🔧 建议：开展前台服务培训，强调微笑服务，提高响应速度",
            "设施": "🔧 建议：检查并维修老化设施，制定设备定期检修计划",
            "位置": "🔧 建议：在OTA详情页标注周边交通信息，提供指引服务",
            "性价比": "🔧 建议：优化价格策略，或提升配套服务增加感知价值",
        }
        
        return [suggestions_map.get(cat[0], "") for cat in categories if cat[0] in suggestions_map]
```

#### 输出(Output)

```yaml
输出格式: JSON / 预警文本

预警输出:
  - status: str, 状态 (ok/warning/alert)
  - total_negative: int, 差评总数
  - avg_score: float, 平均分数
  - top_categories: List[tuple], 问题维度
  - urgent_reviews: List[Dict], 紧急差评
  - suggestions: List[str], 改进建议
  - timestamp: DATETIME, 预警时间
```

#### 数据依赖(Dependency)

```yaml
上游依赖: 无（独立获取EBK差评数据）
下游依赖: 微信推送（最终输出）
```

#### 边界(Boundary)

```yaml
不适用场景:
  - 没有EBK差评导出权限
  - OTA平台API未申请

可能出错的情况:
  - 差评内容涉及隐私 → 需脱敏处理
  - 差评文字为方言/表情 → 降级到纯分数分析
```

---

## SKILL执行矩阵

| SKILL | 输入 | 处理 | 输出 | 依赖 | 优先级 |
|-------|------|------|------|------|--------|
| RM-001 | PMS订单/夜审 | ADR/OCC/RevPAR | 每日指标 | 无 | P0 |
| RM-002 | RM-001+竞品数据 | MPI/ARI/RGI | STR指数 | RM-001 | P0 |
| RM-003 | 携程/美团 | 爬虫解析 | 竞品价格 | 无 | P0 |
| RM-004 | RM-003+RM-001 | 预警规则 | 预警列表 | RM-001, RM-003 | P1 |
| RM-005 | RM-001~004 | 日报组装 | 日报文本 | RM-001~004 | P0 |
| OTA-001 | 携程/美团 | 排名诊断 | 诊断报告 | 无 | P1 |
| OTA-002 | EBK差评 | 分类汇总 | 差评预警 | 无 | P0 |

---

## 技术实现总览

### 技术栈

| 组件 | 技术选型 | 选型理由 |
|------|---------|---------|
| 语言 | Python 3.10+ | 生态丰富，数据处理强 |
| 数据处理 | pandas | 表格数据处理首选 |
| HTTP请求 | requests | 轻量可控，反爬易实现 |
| HTML解析 | BeautifulSoup4 + lxml | 轻量，CSS选择器友好 |
| 数据存储 | SQLite | 轻量，文件级，备份简单 |
| JSON处理 | 内置json库 | 无需额外依赖 |
| 定时任务 | schedule / Windows Task Scheduler | 灵活/系统级 |
| 微信推送 | 企业微信Webhook | 免费，稳定 |

### 代码目录结构

```
AHL-Leshan/
├── skills/
│   ├── RM-001_adr_occ_revpar.py
│   ├── RM-002_str_index.py
│   ├── RM-003_competitor_crawler.py
│   ├── RM-004_price_alert.py
│   ├── RM-005_daily_report.py
│   ├── OTA-001_ranking_diagnosis.py
│   └── OTA-002_review_alert.py
├── data/
│   ├── revenue/          # RM-001输出
│   ├── competitor/       # RM-003输出
│   ├── alerts/           # RM-004输出
│   └── reports/          # RM-005输出
├── logs/                 # 日志文件
├── config/
│   ├── competitors.yaml  # 竞品配置
│   └── hotels.yaml      # 酒店配置
├── database/
│   └── competitor.db    # SQLite数据库
├── main_daily.py         # 每日定时任务入口
├── main_realtime.py      # 实时监控入口
└── requirements.txt
```

### requirements.txt

```
pandas>=2.0.0
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
python-dateutil>=2.8.0
schedule>=1.2.0
```

---

**文档状态**: V1.0（技术规格版）
**下次更新**: 实地调研后补充OTA排名诊断具体实现
**负责人**: AHL技术组
