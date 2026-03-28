# 收益管理 AGENT SKILL体系 V1.0

> **版本**: V1.0  
> **日期**: 2026-03-26  
> **定位**: 收益管理场景的最小可执行SKILL单元，可独立调用或组合编排  
> **范围**: 数据采集 / 指标计算 / 预测模型 / 定价决策 / 库存管理 / 竞品分析 / 分析报表  
> **SKILL总数**: 51个  

---

## 概述

### 设计理念

收益管理SKILL体系将酒店收益管理全链路拆解为**51个最小可执行单元**。每个SKILL：
- 有明确输入/输出（JSON Schema）
- 有完整prompt指导LLM执行
- 可独立调用，也可组合使用
- 包含Python实现框架参考

**底层逻辑**：如果收益管理是一个工厂，那么数据是原料，指标是质检标准，预测是需求探测器，定价是定价引擎，库存是仓储调度，竞品分析是市场雷达，报表是管理驾驶舱。

### SKILL分类总览

| 组别 | SKILL数量 | 核心功能 |
|------|-----------|----------|
| 第一组：数据采集 | 4个 | PMS/OTA/竞品/外部数据拉取 |
| 第二组：指标计算 | 13个 | ADR/OCC/RevPAR/STR指数/渠道分析/房型分析 |
| 第三组：预测模型 | 8个 | 需求预测/展会影响/取消率/No-show预测 |
| 第四组：定价决策 | 10个 | 基准/动态/事件/早鸟/渠道差异化定价 |
| 第五组：库存管理 | 6个 | 可售/配额/超售/升舱/预警/保留房 |
| 第六组：竞品分析 | 5个 | 价格监控/动态预警/周报/Benchmark/活动监控 |
| 第七组：分析报表 | 6个 | 日报/周报/月报/预算vs实际/渠道/预测准确率 |
| **合计** | **51个** | |

---

## 第一组：数据采集SKILL（4个）

### RM-DATA-001 PMS订单数据拉取
**功能描述**: 从酒店PMS系统拉取历史订单数据，支持Opera/SAP/Flysht等主流PMS

```yaml
SKILL-ID: RM-DATA-001
name: PMS订单数据拉取
group: data_collection
```

**INPUT（输入Schema）**:
```json
{
  "hotel_id": "string",
  "start_date": "date",
  "end_date": "date",
  "room_types": ["string"],
  "channels": ["string"],
  "rate_codes": ["string"],
  "fields": ["string"]
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "hotel_id": "string",
  "date_range": {"start": "date", "end": "date"},
  "records": [
    {
      "reservation_id": "string",
      "arrival_date": "date",
      "departure_date": "date",
      "room_type": "string",
      "channel": "string",
      "rate_code": "string",
      "room_revenue": "float",
      "adr": "float",
      "los": "int",
      "guest_name_masked": "string"
    }
  ],
  "count": "int",
  "total_revenue": "float",
  "fetch_time_ms": "int"
}
```

**PROMPT（执行指导）**:
```
# ROLE: 数据工程师
# TASK: 从PMS系统拉取酒店订单历史数据
# REQUIREMENTS:
1. 连接PMS API，根据hotel_config识别PMS类型（Opera/SAP/Flysht/自定义）
2. 按日期/房型/渠道/价格码多维度筛选拉取
3. 数据脱敏处理：guest_name仅返回姓氏+脱敏字符（如"张**"）
4. ADR自动计算：room_revenue / occupied_rooms
5. 返回records数组+统计摘要+fetch_time_ms
6. 异常处理：PMS连接失败/数据超限/字段不匹配
```

**依赖项（dependencies）**:
- PMS_API_KEY
- hotel_config
- PMS_CONNECTION_POOL

**性能指标（metrics）**:
- 响应时间 < 5s
- 数据完整率 > 99%
- 脱敏合规率 100%

**Python实现框架**:
```python
import requests
from datetime import datetime

class PMSDataFetcher:
    def __init__(self, api_key, hotel_config):
        self.api_key = api_key
        self.config = hotel_config
        self.pms_type = hotel_config.get('pms_type', 'opera')

    def fetch_orders(self, hotel_id, start_date, end_date,
                     room_types=None, channels=None, rate_codes=None, fields=None):
        pms_api = self.config['pms_api_endpoint']
        headers = {'Authorization': f'Bearer {self.api_key}'}
        params = {
            'hotel_id': hotel_id, 'start': start_date, 'end': end_date,
            'room_types': ','.join(room_types) if room_types else '',
            'channels': ','.join(channels) if channels else ''
        }
        response = requests.get(f'{pms_api}/reservations',
                                params=params, headers=headers, timeout=10)
        raw_data = response.json()['reservations']
        records = []
        for r in raw_data:
            record = {
                'reservation_id': r['confirmation_no'],
                'arrival_date': r['arrival'], 'departure_date': r['departure'],
                'room_type': r['room_type'], 'channel': r['source_code'],
                'rate_code': r['rate_code'], 'room_revenue': float(r['room_revenue']),
                'adr': float(r['room_revenue']) / r['no_of_rooms'],
                'guest_name_masked': r['guest_name'][:1] + '**'
            }
            if fields:
                record = {k: v for k, v in record.items() if k in fields}
            records.append(record)
        return {
            'status': 'success', 'hotel_id': hotel_id,
            'records': records, 'count': len(records),
            'total_revenue': sum(r['room_revenue'] for r in records)
        }
```

---

### RM-DATA-002 OTA订单同步
**功能描述**: 从携程/美团/飞猪同步OTA订单数据，包含订单状态/取消/改期信息

```yaml
SKILL-ID: RM-DATA-002
name: OTA订单同步
group: data_collection
```

**INPUT（输入Schema）**:
```json
{
  "hotel_id": "string",
  "platforms": ["ctrip", "meituan", "fliggy"],
  "start_date": "date",
  "end_date": "date",
  "include_cancelled": "boolean"
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "platforms": {"ctrip": "int", "meituan": "int", "fliggy": "int"},
  "records": [
    {
      "platform": "string",
      "order_id": "string",
      "hotel_id": "string",
      "room_type": "string",
      "checkin": "date",
      "checkout": "date",
      "guest_name_masked": "string",
      "total_amount": "float",
      "commission": "float",
      "status": "confirmed|cancelled|modified",
      "booked_at": "datetime"
    }
  ],
  "total_count": "int",
  "total_revenue": "float",
  "sync_timestamp": "datetime"
}
```

**PROMPT（执行指导）**:
```
# ROLE: OTA数据工程师
# TASK: 从各大OTA平台同步订单数据
# REQUIREMENTS:
1. 遍历指定OTA平台（携程/美团/飞猪），调用各平台开放API
2. 处理分页：单次请求≤500条，超出自动翻页
3. 状态映射：OTA状态码 → 统一状态（confirmed/cancelled/modified）
4. 佣金计算：从API获取commission字段，无则按平台标准佣金率估算
5. 脱敏处理：guest_name_masked = 姓氏 + '**'
6. 合并去重：同一订单多平台出现，以最早预订平台为准
7. 异常处理：单平台失败不影响其他平台，记录error_platforms
```

**依赖项（dependencies）**:
- OTA_API_KEYS
- hotel_ota_credentials
- commission_rates

**性能指标（metrics）**:
- 响应时间 < 10s（3平台并行）
- 数据完整率 > 98%
- 支持增量同步

**Python实现框架**:
```python
import asyncio
import aiohttp
from datetime import datetime

class OTAOrderSyncer:
    def __init__(self, api_keys, credentials):
        self.api_keys = api_keys

    async def sync_all(self, hotel_id, platforms, start_date, end_date,
                       include_cancelled=True):
        tasks = [self._sync_platform(hotel_id, p, start_date, end_date,
                                     include_cancelled) for p in platforms]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        all_records = []
        platform_counts = {}
        errors = {}
        for p, result in zip(platforms, results):
            if isinstance(result, Exception):
                errors[p] = str(result)
            else:
                all_records.extend(result['records'])
                platform_counts[p] = result['count']
        return {
            'status': 'success' if not errors else 'partial_success',
            'platforms': platform_counts,
            'records': all_records,
            'total_count': len(all_records),
            'total_revenue': sum(r['total_amount'] for r in all_records),
            'error_platforms': errors,
            'sync_timestamp': datetime.now().isoformat()
        }
```

---

### RM-DATA-003 竞品价格爬取
**功能描述**: 从OTA平台爬取竞品酒店实时房价，支持携程/美团/去哪儿/Booking

```yaml
SKILL-ID: RM-DATA-003
name: 竞品价格爬取
group: data_collection
```

**INPUT（输入Schema）**:
```json
{
  "competitor_ids": ["string"],
  "room_types": ["string"],
  "checkin_date": "date",
  "checkout_date": "date",
  "platforms": ["string"]
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "scrape_timestamp": "datetime",
  "competitors": [
    {
      "competitor_id": "string",
      "hotel_name": "string",
      "room_types": [
        {
          "room_type": "string",
          "platforms": [
            {
              "platform": "string",
              "price": "float",
              "discount": "float",
              "availability": "int"
            }
          ],
          "lowest_price": "float",
          "avg_price": "float"
        }
      ]
    }
  ]
}
```

**PROMPT（执行指导）**:
```
# ROLE: 市场数据工程师
# TASK: 爬取竞品酒店实时房价数据
# REQUIREMENTS:
1. 使用playwright/selenium访问OTA搜索页，模拟真实用户行为
2. 反爬处理：随机User-Agent/请求间隔/Session切换
3. 数据提取：房型名/价格/折扣/可售数/原价的全量提取
4. 异常处理：单竞品失败不影响整体，记录failed_competitors
5. 数据校验：价格偏离市场价>50%触发人工复核
6. 增量更新：对比上次数据，仅返回变化记录
```

**依赖项（dependencies）**:
- playwright_cli
- 竞品hotel_id_mapping
- anti_bot_config

**性能指标（metrics）**:
- 爬取成功率 > 95%
- 数据时效性 < 5min
- 反爬屏蔽率 < 5%

**Python实现框架**:
```python
from playwright.sync_api import sync_playwright
import time
import random

class CompetitorPriceScraper:
    def __init__(self, competitor_mapping, anti_bot_config):
        self.competitor_mapping = competitor_mapping
        self.anti_bot = anti_bot_config

    def scrape(self, competitor_ids, room_types, checkin, checkout, platforms):
        results = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True,
                user_agent=random.choice(self.anti_bot['user_agents']))
            for comp_id in competitor_ids:
                try:
                    page = browser.new_page()
                    url = self._build_url(comp_id, checkin, checkout)
                    page.goto(url, timeout=30000)
                    time.sleep(random.uniform(2, 5))
                    rooms = self._extract_rooms(page, room_types, platforms)
                    results.append({'competitor_id': comp_id, 'rooms': rooms})
                    page.close()
                except Exception as e:
                    results.append({'competitor_id': comp_id, 'error': str(e)})
            browser.close()
        return {'status': 'success', 'competitors': results}
```

---

### RM-DATA-004 外部数据接入
**功能描述**: 接入天气/展会/节假日/宏观经济数据，为预测模型提供外部特征

```yaml
SKILL-ID: RM-DATA-004
name: 外部数据接入
group: data_collection
```

**INPUT（输入Schema）**:
```json
{
  "city_code": "string",
  "start_date": "date",
  "end_date": "date",
  "data_types": ["weather", "holiday", "event", "flight", "macro"]
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "city_code": "string",
  "date_range": {"start": "date", "end": "date"},
  "data": {
    "weather": [
      {"date": "date", "temp_high": "int", "temp_low": "int",
       "condition": "string", "rain_prob": "float"}
    ],
    "holidays": [
      {"date": "date", "name": "string", "days": "int"}
    ],
    "events": [
      {"date": "date", "event_name": "string", "venue": "string"}
    ]
  }
}
```

**PROMPT（执行指导）**:
```
# ROLE: 数据工程师
# TASK: 接入外部宏观数据（天气/展会/节假日/经济指标）
# REQUIREMENTS:
1. 天气数据：从Open-Meteo/WeatherAPI获取每日最高/最低温度/降雨概率
2. 节假日数据：从中国节假日API/日历API获取法定节假日+传统节日
3. 展会数据：从城市会展局API/大众点评活动API获取展会信息
4. 事件影响标注：展会按规模分级（国际级/国家级/省级），影响系数0.3~1.5
5. 节假日效应：分节前/节中/节后，影响系数和持续天数标注
```

**依赖项（dependencies）**:
- weather_api_key
- holiday_api
- event_api

**性能指标（metrics）**:
- 响应时间 < 3s
- 数据覆盖完整率 > 99%
- 支持T+0和T+7预测

**Python实现框架**:
```python
import requests

class ExternalDataLoader:
    ENDPOINTS = {
        'weather': 'https://api.open-meteo.com/v1/forecast',
        'holiday': 'https://api.apih.cn/v1/holiday'
    }

    def load(self, city_code, start_date, end_date, data_types):
        result = {'status': 'success', 'data': {}}
        if 'weather' in data_types:
            result['data']['weather'] = self._fetch_weather(city_code, start_date, end_date)
        if 'holiday' in data_types:
            result['data']['holidays'] = self._fetch_holidays(start_date, end_date)
        return result

    def _fetch_weather(self, city_code, start, end):
        params = {'latitude': city_code, 'longitude': city_code,
                  'daily': 'temperature_2m_max,temperature_2m_min,precipitation_probability',
                  'start_date': start, 'end_date': end}
        r = requests.get(self.ENDPOINTS['weather'], params=params, timeout=10)
        data = r.json()['daily']
        return [{'date': d, 'temp_high': data['temperature_2m_max'][i],
                 'temp_low': data['temperature_2m_min'][i]}
                for i, d in enumerate(data['time'])]
```

---

## 第二组：指标计算SKILL（13个）

### 核心指标类（5个）

### RM-CALC-001 ADR计算
**功能描述**: 计算平均客房价（Average Daily Rate）：已售客房收入÷已售客房数

```yaml
SKILL-ID: RM-CALC-001
name: ADR计算
group: metrics_calculation
```

**INPUT（输入Schema）**:
```json
{
  "room_revenue": "float",
  "occupied_rooms": "int",
  "by_channel": "boolean",
  "by_room_type": "boolean"
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "adr": "float",
  "by_channel": [
    {"channel": "string", "adr": "float", "occupied_rooms": "int", "revenue": "float"}
  ],
  "by_room_type": [
    {"room_type": "string", "adr": "float", "occupied_rooms": "int", "revenue": "float"}
  ]
}
```

**PROMPT（执行指导）**:
```
# ROLE: 收益分析师
# TASK: 计算平均客房价（ADR）
# FORMULA: ADR = Σ(room_revenue) / Σ(occupied_rooms)
# REQUIREMENTS:
1. 基本计算：总收入÷总已售间夜
2. 渠道分解：按channel分组计算各渠道ADR
3. 房型分解：按room_type分组计算各房型ADR
4. ADR天花板检测：若某房型ADR超出当地市场均价200%+，输出警告
5. 历史对比：返回同比（vs上周同期）/环比（vs上期）变化
6. 注意：仅计算付费用客房，团体免房/员工房不计入分子分母
```

**依赖项（dependencies）**:
- RM-DATA-001（订单数据）

**性能指标（metrics）**:
- 计算精度: 分以下四舍五入
- 单次计算时间 < 100ms
- 支持最多365天跨度

**Python实现框架**:
```python
import pandas as pd

class ADRCalculator:
    def calculate(self, orders_df, by_channel=False, by_room_type=False):
        paid = orders_df[~orders_df['rate_code'].isin(['COMP', 'STAFF'])]
        total_revenue = paid['room_revenue'].sum()
        total_rooms = paid['rooms_sold'].sum()
        result = {
            'status': 'success',
            'adr': round(total_revenue / total_rooms, 2) if total_rooms > 0 else 0
        }
        if by_channel:
            result['by_channel'] = paid.groupby('channel').apply(
                lambda x: pd.Series({'adr': round(x['room_revenue'].sum() / x['rooms_sold'].sum(), 2)})
            ).reset_index().to_dict('records')
        return result
```

---

### RM-CALC-002 OCC计算
**功能描述**: 计算客房入住率（Occupancy）：已售客房数÷可售客房数×100%

```yaml
SKILL-ID: RM-CALC-002
name: OCC计算
group: metrics_calculation
```

**INPUT（输入Schema）**:
```json
{
  "occupied_rooms": "int",
  "available_rooms": "int",
  "by_date": "boolean",
  "by_room_type": "boolean"
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "occ_percent": "float",
  "occ_decimal": "float",
  "occupied_rooms": "int",
  "available_rooms": "int"
}
```

**PROMPT（执行指导）**:
```
# ROLE: 收益分析师
# TASK: 计算客房入住率（OCC）
# FORMULA: OCC = occupied_rooms / available_rooms × 100%
# REQUIREMENTS:
1. 基础计算：已售间夜÷可售间夜×100%
2. OCC预警：>100%触发超售审查，<30%触发低价预警
3. 可售房数计算：总房间数 - 维修房 - 长住房 - 保留房
4. 历史对比：返回同比/环比OCC变化
```

**依赖项（dependencies）**:
- RM-INV-001（可售库存）

**性能指标（metrics）**:
- 精度: 0.01%
- 支持日期/房型双维度分解
- OCC>100%异常检测

**Python实现框架**:
```python
class OCCCalculator:
    def calculate(self, occupied_rooms, available_rooms):
        if available_rooms == 0:
            return {'status': 'error', 'message': 'available_rooms cannot be zero'}
        occ_decimal = occupied_rooms / available_rooms
        result = {
            'status': 'success',
            'occ_percent': round(occ_decimal * 100, 2),
            'occ_decimal': round(occ_decimal, 4),
            'occupied_rooms': occupied_rooms,
            'available_rooms': available_rooms,
            'warnings': []
        }
        if occ_decimal > 1.0:
            result['warnings'].append('OCC > 100%, possible overbooking')
        if occ_decimal < 0.30:
            result['warnings'].append('OCC < 30%, low demand alert')
        return result
```

---

### RM-CALC-003 RevPAR计算
**功能描述**: 计算每可用客房收入（Revenue Per Available Room）：ADR×OCC或总收入÷可售房

```yaml
SKILL-ID: RM-CALC-003
name: RevPAR计算
group: metrics_calculation
```

**INPUT（输入Schema）**:
```json
{
  "total_room_revenue": "float",
  "total_available_rooms": "int",
  "adr": "float",
  "occ_percent": "float"
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "revpar": "float",
  "calculation_method": "adr_x_occ | revenue_divided",
  "adr": "float",
  "occ_percent": "float"
}
```

**PROMPT（执行指导）**:
```
# ROLE: 收益分析师
# TASK: 计算每可用客房收入（RevPAR）
# FORMULA: RevPAR = ADR × OCC = 总收入 ÷ 可售间夜总数
# REQUIREMENTS:
1. 双公式验证：ADR×OCC和总收入÷可售房两种算法交叉验证
2. 支持多种期间：日/周/月/自定义
3. RevPAR分解：RevPAR = MPI × 市场竞争指数 / 100
4. 同比/环比：与上周同期/上月同期/去年同月对比
```

**依赖项（dependencies）**:
- RM-CALC-001（ADR）
- RM-CALC-002（OCC）

**性能指标（metrics）**:
- 精度: 分以下四舍五入
- 双公式验证一致性
- 同比/环比计算

**Python实现框架**:
```python
class RevPARCalculator:
    def calculate(self, total_room_revenue=None, total_available_rooms=None,
                  adr=None, occ_percent=None):
        if adr is not None and occ_percent is not None:
            revpar = adr * (occ_percent / 100)
            method = 'adr_x_occ'
        elif total_room_revenue is not None and total_available_rooms is not None:
            revpar = total_room_revenue / total_available_rooms if total_available_rooms > 0 else 0
            method = 'revenue_divided'
        else:
            return {'status': 'error', 'message': 'insufficient inputs'}
        return {
            'status': 'success',
            'revpar': round(revpar, 2),
            'calculation_method': method
        }
```

---

### RM-CALC-004 GOPPAR计算
**功能描述**: 计算每可用客房经营利润（GOP Per Available Room）：GOP÷可售房

```yaml
SKILL-ID: RM-CALC-004
name: GOPPAR计算
group: metrics_calculation
```

**INPUT（输入Schema）**:
```json
{
  "gop": "float",
  "available_rooms": "int",
  "period_days": "int"
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "goppar": "float",
  "gop": "float",
  "available_rooms": "int",
  "period_days": "int",
  "gop_margin": "float",
  "vs_budget": {"goppar_diff": "float", "percent_diff": "float"}
}
```

**PROMPT（执行指导）**:
```
# ROLE: 收益分析师
# TASK: 计算每可用客房经营利润（GOPPAR）
# FORMULA: GOPPAR = GOP / available_rooms
# REQUIREMENTS:
1. GOP = 客房收入 + 餐饮收入 + 其他收入 - 运营成本
2. GOPPAR = GOP / 可售间夜总数（不是已售间夜）
3. 周期支持：日/周/月/年化GOPPAR
4. vs预算：与预算GOPPAR对比，计算偏差金额和百分比
```

**依赖项（dependencies）**:
- PMS_financial_data
- RM-CALC-003（RevPAR）

**性能指标（metrics）**:
- 支持日/周/月/年化
- GOPPAR偏差分析
- 成本归因分析

**Python实现框架**:
```python
class GOPPARCalculator:
    def calculate(self, gop, available_rooms, period_days=1):
        goppar = gop / available_rooms if available_rooms > 0 else 0
        return {
            'status': 'success',
            'goppar': round(goppar, 2),
            'gop': round(gop, 2),
            'available_rooms': available_rooms,
            'period_days': period_days,
            'daily_goppar': round(goppar, 2),
            'monthly_goppar': round(goppar * 30, 2),
            'annualized_goppar': round(goppar * 365, 2)
        }
```

---

### RM-CALC-005 RevPAR变化率计算
**功能描述**: 计算RevPAR同比/环比变化率，识别趋势

```yaml
SKILL-ID: RM-CALC-005
name: RevPAR变化率计算
group: metrics_calculation
```

**INPUT（输入Schema）**:
```json
{
  "current_revpar": "float",
  "prior_revpar": "float",
  "comparison_type": "wow|yoy|mom|dod"
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "current_revpar": "float",
  "prior_revpar": "float",
  "change_absolute": "float",
  "change_percent": "float",
  "direction": "up|down|flat",
  "comparison_type": "string",
  "interpretation": "string"
}
```

**PROMPT（执行指导）**:
```
# ROLE: 收益分析师
# TASK: 计算RevPAR变化率
# FORMULA: 变化率 = (当前 - 基准) / 基准 × 100%
# REQUIREMENTS:
1. 变化率计算：百分比和绝对值双维度
2. 方向判断：>0为上升，<0为下降，=0为持平（阈值±0.5%为持平）
3. 市场解读：
   - +5%以上：强势增长
   - +0~5%：温和增长
   - ±0.5%以内：基本持平
   - -5%~0：轻微下滑
   - <-5%：显著下滑
```

**依赖项（dependencies）**:
- RM-CALC-003（RevPAR基准值）

**性能指标（metrics）**:
- 精度: 0.01%
- 支持4种对比类型
- 季节性调整选项

**Python实现框架**:
```python
class RevPARChangeCalculator:
    THRESHOLDS = {'strong_up': 5, 'flat': 0.5, 'strong_down': -5}

    def calculate(self, current_revpar, prior_revpar, comparison_type='yoy'):
        if prior_revpar == 0:
            return {'status': 'error', 'message': 'prior_revpar cannot be zero'}
        change_pct = ((current_revpar - prior_revpar) / prior_revpar) * 100
        change_abs = current_revpar - prior_revpar
        direction = 'up' if change_pct > self.THRESHOLDS['flat'] else \
                    'down' if change_pct < -self.THRESHOLDS['flat'] else 'flat'
        return {
            'status': 'success',
            'change_absolute': round(change_abs, 2),
            'change_percent': round(change_pct, 2),
            'direction': direction,
            'comparison_type': comparison_type
        }
```

---

### STR指数类（3个）

### RM-CALC-006 MPI计算
**功能描述**: 计算市场渗透指数（Market Penetration Index）：酒店ADR÷市场ADR×100

```yaml
SKILL-ID: RM-CALC-006
name: MPI计算
group: metrics_calculation
```

**INPUT（输入Schema）**:
```json
{
  "hotel_adr": "float",
  "market_adr": "float",
  "period": {"start": "date", "end": "date"}
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "mpi": "float",
  "hotel_adr": "float",
  "market_adr": "float",
  "performance": "above_avg|at_avg|below_avg",
  "interpretation": "string"
}
```

**PROMPT（执行指导）**:
```
# ROLE: 收益分析师
# TASK: 计算市场渗透指数（MPI - Market Penetration Index）
# FORMULA: MPI = hotel_adr / market_adr × 100
# REQUIREMENTS:
1. MPI = 100：酒店定价与市场平均水平一致
2. MPI > 100（如110）：酒店定价高于市场，表示溢价能力强或定位高端
3. MPI < 100（如90）：酒店定价低于市场，可能需要提价或调整定位
4. MPI分层：
   - MPI > 115：强势溢价（红色警戒）
   - MPI 100~115：高于平均（绿色健康）
   - MPI 85~100：低于平均（黄色预警）
   - MPI < 85：显著低于市场（红色预警）
```

**依赖项（dependencies）**:
- RM-CALC-001（ADR）
- RM-COMP-004（市场Benchmark）

**性能指标（metrics）**:
- 精度: 0.1
- 支持日/周/月MPI
- STR标准对标

**Python实现框架**:
```python
class MPICalculator:
    def calculate(self, hotel_adr, market_adr, period=None):
        if market_adr == 0:
            return {'status': 'error', 'message': 'market_adr cannot be zero'}
        mpi = (hotel_adr / market_adr) * 100
        if mpi > 115:
            perf, interp = 'above_avg_strong', '强势溢价，需关注客源流失风险'
        elif mpi > 100:
            perf, interp = 'above_avg', '高于市场平均，定价策略健康'
        elif mpi > 85:
            perf, interp = 'below_avg', '低于市场平均，建议价格优化'
        else:
            perf, interp = 'below_avg_significant', '显著低于市场，需立即审视定价策略'
        return {
            'status': 'success',
            'mpi': round(mpi, 1),
            'performance': perf,
            'interpretation': interp
        }
```

---

### RM-CALC-007 ARI计算
**功能描述**: 计算平均房价指数（Average Rate Index）：酒店ADR÷市场ADR（同入住率层级）×100

```yaml
SKILL-ID: RM-CALC-007
name: ARI计算
group: metrics_calculation
```

**INPUT（输入Schema）**:
```json
{
  "hotel_adr": "float",
  "market_adr_same_occ": "float",
  "period": {"start": "date", "end": "date"}
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "ari": "float",
  "hotel_adr": "float",
  "market_adr_same_occ": "float",
  "performance": "string",
  "recommendation": "string"
}
```

**PROMPT（执行指导）**:
```
# ROLE: 收益分析师
# TASK: 计算平均房价指数（ARI - Average Rate Index）
# FORMULA: ARI = hotel_adr / market_adr_same_occ_level × 100
# REQUIREMENTS:
1. ARI关键：与MPI不同，ARI在相同入住率水平下对比，排除OCC影响
2. ARI = 100：与竞品同OCC下ADR一致
3. ARI > 100：酒店在同OCC下能收取更高房价（定价效率高）
4. ARI < 100：酒店在同OCC下定价偏低（可能低估品牌价值）
```

**依赖项（dependencies）**:
- RM-CALC-001（ADR）
- RM-CALC-002（OCC）
- RM-COMP-004（市场Benchmark）

**性能指标（metrics）**:
- 精度: 0.1
- 同OCC层级对比
- 定价效率评估

**Python实现框架**:
```python
class ARICalculator:
    def calculate(self, hotel_adr, market_adr_same_occ, period=None):
        if market_adr_same_occ == 0:
            return {'status': 'error', 'message': 'market_adr_same_occ cannot be zero'}
        ari = (hotel_adr / market_adr_same_occ) * 100
        if ari > 110:
            perf, rec = 'strong_rate_premium', '高定价效率，建议维持并观察竞品反应'
        elif ari > 95:
            perf, rec = 'at_par', '定价合理，与竞品基本一致'
        else:
            perf, rec = 'below_par', '同OCC下定价偏低，可考虑小幅提价'
        return {
            'status': 'success',
            'ari': round(ari, 1),
            'performance': perf,
            'recommendation': rec
        }
```

---

### RM-CALC-008 RGI计算
**功能描述**: 计算收入产生指数（Revenue Generated Index）：酒店RevPAR÷市场RevPAR×100

```yaml
SKILL-ID: RM-CALC-008
name: RGI计算
group: metrics_calculation
```

**INPUT（输入Schema）**:
```json
{
  "hotel_revpar": "float",
  "market_revpar": "float",
  "period": {"start": "date", "end": "date"}
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "rgi": "float",
  "hotel_revpar": "float",
  "market_revpar": "float",
  "performance": "above_avg|at_avg|below_avg"
}
```

**PROMPT（执行指导）**:
```
# ROLE: 收益分析师
# TASK: 计算收入产生指数（RGI - Revenue Generated Index）
# FORMULA: RGI = hotel_RevPAR / market_RevPAR × 100
# REQUIREMENTS:
1. RGI = 100：酒店与市场整体收入效率一致
2. RGI = MPI × (OCC_hotel / OCC_market) / 100（分解验证）
3. 三指数综合解读（MPI/ARI/RGI）：
   - MPI↑ + ARI↑ + RGI↑：量价齐升，最强态势
   - MPI↑ + ARI↓：放量减价，低价抢量
   - MPI↓ + ARI↑：缩量溢价，高冷定位
   - MPI↓ + ARI↓：量价齐跌，最弱态势
4. RGI分层：>110强势/95~110健康/<95预警
```

**依赖项（dependencies）**:
- RM-CALC-003（RevPAR）
- RM-CALC-006（MPI）
- RM-CALC-007（ARI）

**性能指标（metrics）**:
- 精度: 0.1
- 三指数联合解读
- RGI趋势追踪

**Python实现框架**:
```python
class RGICalculator:
    def calculate(self, hotel_revpar, market_revpar, period=None):
        if market_revpar == 0:
            return {'status': 'error', 'message': 'market_revpar cannot be zero'}
        rgi = (hotel_revpar / market_revpar) * 100
        perf = 'strong' if rgi > 110 else 'healthy' if rgi > 95 else 'weak'
        return {
            'status': 'success',
            'rgi': round(rgi, 1),
            'hotel_revpar': round(hotel_revpar, 2),
            'market_revpar': round(market_revpar, 2),
            'performance': perf
        }
```

---

### 渠道分析类（3个）

### RM-CALC-009 渠道ADR对比
**功能描述**: 横向对比各预订渠道的ADR表现，识别高效/低效渠道

```yaml
SKILL-ID: RM-CALC-009
name: 渠道ADR对比
group: metrics_calculation
```

**INPUT（输入Schema）**:
```json
{
  "orders": [
    {"channel": "string", "room_revenue": "float", "rooms_sold": "int"}
  ],
  "compare_types": ["channel", "platform", "rate_code"]
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "overall_adr": "float",
  "by_dimension": [
    {
      "dimension": "string",
      "value": "string",
      "adr": "float",
      "rooms_sold": "int",
      "revenue": "float",
      "adr_vs_overall_pct": "float",
      "rank": "int"
    }
  ],
  "top_channel": "string",
  "worst_channel": "string"
}
```

**PROMPT（执行指导）**:
```
# ROLE: 收益分析师
# TASK: 各渠道ADR横向对比
# REQUIREMENTS:
1. 渠道ADR = 某渠道收入÷某渠道已售间夜
2. vs总体ADR：各渠道ADR与总体ADR对比，计算偏离百分比
3. 排名：按ADR降序排名
4. 渠道分组：直销/OTA/协议/团队
5. 异常检测：某渠道ADR < 总体ADR 30%+，标记为低价渠道
6. 佣金效率：OTA渠道需同时考虑佣金成本，计算净ADR
```

**依赖项（dependencies）**:
- RM-DATA-001（订单数据）
- RM-DATA-002（OTA数据）

**性能指标（metrics）**:
- 支持3种维度对比
- 佣金后净ADR计算
- 渠道效率排名

**Python实现框架**:
```python
class ChannelADRComparator:
    def compare(self, orders, compare_types=['channel']):
        import pandas as pd
        df = pd.DataFrame(orders)
        overall_adr = df['room_revenue'].sum() / df['rooms_sold'].sum()
        results = []
        for dim in compare_types:
            grouped = df.groupby(dim).agg(
                adr=('room_revenue', lambda x: x.sum() / df.loc[x.index, 'rooms_sold'].sum()),
                rooms_sold=('rooms_sold', 'sum'),
                revenue=('room_revenue', 'sum')
            ).reset_index()
            grouped['adr_vs_overall_pct'] = ((grouped['adr'] / overall_adr) - 1) * 100
            grouped['dimension'] = dim
            grouped = grouped.sort_values('adr', ascending=False)
            grouped['rank'] = range(1, len(grouped) + 1)
            results.extend(grouped.to_dict('records'))
        top = results[0] if results else None
        worst = results[-1] if results else None
        return {
            'status': 'success',
            'overall_adr': round(overall_adr, 2),
            'by_dimension': results,
            'top_channel': top['value'] if top else None,
            'worst_channel': worst['value'] if worst else None
        }
```

---

### RM-CALC-010 渠道贡献度分析
**功能描述**: 计算各渠道收入/间夜占比，识别核心渠道与长尾渠道

```yaml
SKILL-ID: RM-CALC-010
name: 渠道贡献度分析
group: metrics_calculation
```

**INPUT（输入Schema）**:
```json
{
  "orders": [{"channel": "string", "room_revenue": "float", "rooms_sold": "int"}],
  "grouping": "channel|platform|rate_code"
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "total_revenue": "float",
  "total_rooms": "int",
  "contribution": [
    {
      "group": "string",
      "revenue": "float",
      "rooms": "int",
      "revenue_pct": "float",
      "rooms_pct": "float",
      "adr": "float",
      "revenue_vs_rooms_pct_diff": "float"
    }
  ],
  "top3_revenue_pct": "float",
  "channel_concentration": "hhi"
}
```

**PROMPT（执行指导）**:
```
# ROLE: 收益分析师
# TASK: 分析各渠道对收入的贡献度
# REQUIREMENTS:
1. 渠道分组：直销/OTA/协议/团队
2. 核心指标：收入占比、间夜占比、ADR
3. revenue_vs_rooms_pct_diff > 0：该渠道用少量间夜贡献了大量收入（高效）
4. TOP3占比：CR3 > 70% = 高度依赖风险，CR3 < 40% = 渠道分散健康
5. HHI指数：赫芬达尔-赫希曼指数，>2500高度集中，<1500分散健康
```

**依赖项（dependencies）**:
- RM-DATA-001（订单数据）

**性能指标（metrics）**:
- HHI渠道集中度计算
- CR3 Top3占比
- 高效/低效渠道识别

**Python实现框架**:
```python
class ChannelContributionAnalyzer:
    def analyze(self, orders, grouping='channel'):
        import pandas as pd
        df = pd.DataFrame(orders)
        total_revenue = df['room_revenue'].sum()
        total_rooms = df['rooms_sold'].sum()
        grouped = df.groupby(grouping).agg(
            revenue=('room_revenue', 'sum'),
            rooms=('rooms_sold', 'sum')
        ).reset_index()
        grouped['revenue_pct'] = (grouped['revenue'] / total_revenue) * 100
        grouped['rooms_pct'] = (grouped['rooms'] / total_rooms) * 100
        hhi = (grouped['revenue_pct'] ** 2).sum()
        top3_pct = grouped.nlargest(3, 'revenue')['revenue_pct'].sum()
        return {
            'status': 'success',
            'total_revenue': round(total_revenue, 2),
            'contribution': grouped.to_dict('records'),
            'top3_revenue_pct': round(top3_pct, 2),
            'channel_concentration': {'hhi': round(hhi, 1)}
        }
```

---

### RM-CALC-011 渠道ROI计算
**功能描述**: 计算各渠道的投资回报率：渠道净收入÷渠道成本（佣金+促销）

```yaml
SKILL-ID: RM-CALC-011
name: 渠道ROI计算
group: metrics_calculation
```

**INPUT（输入Schema）**:
```json
{
  "channel_data": [
    {
      "channel": "string",
      "gross_revenue": "float",
      "commission_pct": "float",
      "promotion_cost": "float",
      "rooms_sold": "int"
    }
  ]
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "channels": [
    {
      "channel": "string",
      "gross_revenue": "float",
      "commission": "float",
      "net_revenue": "float",
      "total_cost": "float",
      "roi": "float",
      "roi_percent": "float",
      "rank": "int"
    }
  ],
  "best_roi_channel": "string",
  "worst_roi_channel": "string",
  "portfolio_roi": "float"
}
```

**PROMPT（执行指导）**:
```
# ROLE: 收益分析师
# TASK: 计算各渠道投资回报率（ROI）
# REQUIREMENTS:
1. 佣金 = gross_revenue × commission_pct
2. 净收入 = gross_revenue - 佣金 - 促销成本
3. ROI = (净收入 - 总成本) / 总成本 × 100%
4. 净ADR = 净收入 / rooms_sold
5. 渠道排序：按ROI降序
6. 战略建议：
   - 高ROI渠道：增加配额，优化转化率
   - 低ROI渠道：降低佣金率或减少配额
   - 负ROI渠道：立即重新谈判或暂停合作
```

**依赖项（dependencies）**:
- RM-CALC-009（渠道ADR）
- OTA_commission_rates

**性能指标（metrics）**:
- 精度: 0.01%
- ROI排名
- 负ROI预警

**Python实现框架**:
```python
class ChannelROICalculator:
    def calculate(self, channel_data):
        results = []
        for ch in channel_data:
            gross = ch['gross_revenue']
            comm = gross * ch['commission_pct']
            promo = ch['promotion_cost']
            total_cost = comm + promo
            net = gross - total_cost
            roi = ((net - total_cost) / total_cost * 100) if total_cost > 0 else 0
            results.append({
                **ch,
                'commission': round(comm, 2),
                'net_revenue': round(net, 2),
                'total_cost': round(total_cost, 2),
                'roi': round(roi, 2),
                'rank': 0
            })
        results.sort(key=lambda x: x['roi'], reverse=True)
        for i, r in enumerate(results):
            r['rank'] = i + 1
        return {
            'status': 'success',
            'channels': results,
            'best_roi_channel': results[0]['channel'] if results else None,
            'worst_roi_channel': results[-1]['channel'] if results else None
        }
```

---

### 房型分析类（2个）

### RM-CALC-012 房型贡献度分析
**功能描述**: 计算各房型收入占比，识别核心/利润/流量房型

```yaml
SKILL-ID: RM-CALC-012
name: 房型贡献度分析
group: metrics_calculation
```

**INPUT（输入Schema）**:
```json
{
  "orders": [{"room_type": "string", "room_revenue": "float", "rooms_sold": "int"}],
  "room_config": {
    "room_type": "string",
    "cost_per_room": "float",
    "rack_rate": "float"
  }
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "total_revenue": "float",
  "by_room_type": [
    {
      "room_type": "string",
      "revenue": "float",
      "rooms_sold": "int",
      "revenue_pct": "float",
      "rooms_pct": "float",
      "adr": "float",
      "type": "core|profit|traffic"
    }
  ],
  "core_room_types": ["string"],
  "traffic_room_types": ["string"],
  "profit_room_types": ["string"]
}
```

**PROMPT（执行指导）**:
```
# ROLE: 收益分析师
# TASK: 分析各房型对收入的贡献度
# REQUIREMENTS:
1. 基础指标：收入/间夜/ADR/占比
2. 房型分类（基于二维矩阵）：
   - 核心房型：收入占比TOP20%，量价双高
   - 利润房型：ADR高（>平均ADR 20%+），贡献毛利高
   - 流量房型：间夜占比高（>30%），ADR低，拉动OCC
3. 贡献毛利：room_revenue - (rooms_sold × cost_per_room)
```

**依赖项（dependencies）**:
- RM-DATA-001（订单数据）
- room_cost_config

**性能指标（metrics）**:
- 房型四象限分类
- 贡献毛利计算
- 房型组合建议

**Python实现框架**:
```python
class RoomTypeContributionAnalyzer:
    def analyze(self, orders, room_config=None):
        import pandas as pd
        df = pd.DataFrame(orders)
        total_revenue = df['room_revenue'].sum()
        total_rooms = df['rooms_sold'].sum()
        avg_adr = total_revenue / total_rooms if total_rooms > 0 else 0
        grouped = df.groupby('room_type').agg(
            revenue=('room_revenue', 'sum'),
            rooms_sold=('rooms_sold', 'sum')
        ).reset_index()
        grouped['revenue_pct'] = grouped['revenue'] / total_revenue * 100
        grouped['rooms_pct'] = grouped['rooms_sold'] / total_rooms * 100
        grouped['adr'] = grouped['revenue'] / grouped['rooms_sold']
        grouped['type'] = grouped.apply(
            lambda r: 'profit' if r['adr'] > avg_adr * 1.2 else
                      'traffic' if r['rooms_pct'] > 30 else 'core', axis=1)
        return {
            'status': 'success',
            'by_room_type': grouped.to_dict('records'),
            'core_room_types': grouped[grouped['type']=='core']['room_type'].tolist(),
            'traffic_room_types': grouped[grouped['type']=='traffic']['room_type'].tolist(),
            'profit_room_types': grouped[grouped['type']=='profit']['room_type'].tolist()
        }
```

---

### RM-CALC-013 房型OCC矩阵
**功能描述**: 构建房型×日期的入住率矩阵，识别房型销售节奏

```yaml
SKILL-ID: RM-CALC-013
name: 房型OCC矩阵
group: metrics_calculation
```

**INPUT（输入Schema）**:
```json
{
  "date_range": {"start": "date", "end": "date"},
  "room_types": ["string"],
  "orders": [
    {"room_type": "string", "arrival_date": "date", "departure_date": "date",
     "rooms_sold": "int"}
  ],
  "available_inventory": {
    "room_type": "string",
    "daily_available": "int"
  }
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "matrix": [
    {
      "date": "date",
      "by_room_type": {
        "room_type": {"occupied": "int", "available": "int", "occ_pct": "float"}
      },
      "total_occ_pct": "float"
    }
  ],
  "summary": {
    "best_selling_room_type": "string",
    "worst_selling_room_type": "string",
    "highest_occ_date": "date",
    "lowest_occ_date": "date"
  }
}
```

**PROMPT（执行指导）**:
```
# ROLE: 收益分析师
# TASK: 构建房型×日期的OCC矩阵
# REQUIREMENTS:
1. 矩阵构建：日期行 × 房型列，每格=该日该房型OCC%
2. 贡献分解：每个间夜按入住日期计入当日该房型
3. 汇总分析：最好卖房型/最难卖房型/高峰日/OCC洼地日
4. 热力图数据：返回RGB值或hex色码，用于前端可视化
```

**依赖项（dependencies）**:
- RM-DATA-001（订单数据）
- RM-INV-001（可售库存）

**性能指标（metrics）**:
- 矩阵完整性检查
- 热力图数据输出
- 销售节奏分析

**Python实现框架**:
```python
class RoomTypeOCCMatrix:
    def build(self, date_range, room_types, orders, available_inventory):
        from datetime import datetime, timedelta
        import pandas as pd
        start = datetime.strptime(date_range['start'], '%Y-%m-%d')
        end = datetime.strptime(date_range['end'], '%Y-%m-%d')
        dates = [(start + timedelta(days=i)).strftime('%Y-%m-%d')
                 for i in range((end - start).days + 1)]
        occ_dict = {}
        for _, row in pd.DataFrame(orders).iterrows():
            arr = datetime.strptime(row['arrival_date'], '%Y-%m-%d')
            dep = datetime.strptime(row['departure_date'], '%Y-%m-%d')
            for d in dates:
                d_dt = datetime.strptime(d, '%Y-%m-%d')
                if arr <= d_dt < dep:
                    key = (d, row['room_type'])
                    occ_dict[key] = occ_dict.get(key, 0) + row['rooms_sold']
        matrix = []
        for d in dates:
            row = {'date': d, 'by_room_type': {}, 'total_occupied': 0, 'total_available': 0}
            for rt in room_types:
                occ = occ_dict.get((d, rt), 0)
                avail = available_inventory.get(rt, {}).get('daily_available', 0)
                occ_pct = (occ / avail * 100) if avail > 0 else 0
                row['by_room_type'][rt] = {'occupied': occ, 'available': avail, 'occ_pct': round(occ_pct, 1)}
                row['total_occupied'] += occ
                row['total_available'] += avail
            row['total_occ_pct'] = round((row['total_occupied'] / row['total_available'] * 100)
                                         if row['total_available'] > 0 else 0, 1)
            matrix.append(row)
        return {'status': 'success', 'matrix': matrix}
```

---

## 第三组：预测模型SKILL（8个）

### RM-PRED-001 短期需求预测（7天）
**功能描述**: 使用Holt-Winters三次指数平滑预测未来7天每日需求（间夜量）

```yaml
SKILL-ID: RM-PRED-001
name: 短期需求预测（7天）
group: prediction_model
```

**INPUT（输入Schema）**:
```json
{
  "historical_orders": [{"date": "date", "rooms_sold": "int", "adr": "float"}],
  "forecast_days": "int",
  "seasonality_period": "int",
  "confidence_level": "float"
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "model": "Holt-Winters",
  "forecast": [
    {"date": "date", "predicted_rooms": "float", "lower_ci": "float", "upper_ci": "float"}
  ],
  "total_forecast_rooms": "float",
  "demand_level": "low|medium|high|very_high"
}
```

**PROMPT（执行指导）**:
```
# ROLE: 数据科学家
# TASK: 使用Holt-Winters模型预测未来7天短期需求
# REQUIREMENTS:
1. 算法选择：Holt-Winters三次指数平滑（加法/乘法季节性自动选择）
2. 季节性周期：周季节性（7天），自动检测
3. 趋势+季节+残差分解，确保可解释性
4. 置信区间：输出80%和95%置信区间，支持风险决策
5. 需求分级：very_high(OCC>90%), high(80~90%), medium(50~80%), low(<50%)
6. 模型评估：MAPE < 15%为可接受
```

**依赖项（dependencies）**:
- RM-DATA-001（历史订单）
- RM-DATA-004（节假日数据）

**性能指标（metrics）**:
- MAPE < 15%
- 支持7~14天预测
- 置信区间输出
- 节假日自适应

**Python实现框架**:
```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pandas as pd

class ShortTermDemandForecaster:
    def __init__(self, seasonality_period=7):
        self.seasonality_period = seasonality_period

    def forecast(self, historical_orders, forecast_days=7, confidence_level=0.95):
        df = pd.DataFrame(historical_orders).set_index('date')['rooms_sold']
        df.index = pd.to_datetime(df.index)
        df = df.asfreq('D', fill_value=0)
        model = ExponentialSmoothing(
            df, trend='add', seasonal='add' if len(df) > 14 else None,
            seasonal_periods=self.seasonality_period
        )
        fitted = model.fit(optimized=True)
        forecast_result = fitted.get_forecast(forecast_days)
        pred = forecast_result.predicted_mean
        conf_int = forecast_result.conf_int(alpha=1-confidence_level)
        avg_occ = df.mean()
        demand_level = 'very_high' if pred.mean() / avg_occ > 1.2 else \
                       'high' if pred.mean() / avg_occ > 1.0 else \
                       'medium' if pred.mean() / avg_occ > 0.6 else 'low'
        return {
            'status': 'success',
            'model': 'Holt-Winters',
            'forecast': [
                {'date': str(pred.index[i].date()),
                 'predicted_rooms': round(pred.iloc[i], 1),
                 'lower_ci': round(conf_int.iloc[i, 0], 1),
                 'upper_ci': round(conf_int.iloc[i, 1], 1)}
                for i in range(len(pred))
            ],
            'demand_level': demand_level
        }
```

---

### RM-PRED-002 中期需求预测（30天）
**功能描述**: 使用SARIMA模型预测未来30天需求，支持趋势+季节性+外部变量

```yaml
SKILL-ID: RM-PRED-002
name: 中期需求预测（30天）
group: prediction_model
```

**INPUT（输入Schema）**:
```json
{
  "historical_orders": [{"date": "date", "rooms_sold": "int"}],
  "forecast_days": "int",
  "external_vars": [{"name": "string", "values": [{"date": "date", "value": "float"}]}]
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "model": "SARIMA",
  "forecast": [{"date": "date", "predicted_rooms": "float"}],
  "weekly_breakdown": [{"week": "string", "total_rooms": "float"}]
}
```

**PROMPT（执行指导）**:
```
# ROLE: 数据科学家
# TASK: 使用SARIMA模型预测未来30天中期需求
# REQUIREMENTS:
1. SARIMA参数自动选择：AIC/BIC最优定阶
2. 周季节性（7天）+ 月季节性（30天）双周期
3. 外部变量支持：气温/展会/节假日作为外生变量
4. 周度分解：30天=4周+2天，输出每周总量
5. MAPE评估：<20%为可接受（中期预测精度低于短期）
```

**依赖项（dependencies）**:
- RM-DATA-001（历史订单）
- RM-DATA-004（外部数据）

**性能指标（metrics）**:
- MAPE < 20%
- 周度分解输出
- 外部变量支持

**Python实现框架**:
```python
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pandas as pd

class MediumTermDemandForecaster:
    def forecast(self, historical_orders, forecast_days=30, external_vars=None):
        df = pd.DataFrame(historical_orders).set_index('date')
        df.index = pd.to_datetime(df.index)
        y = df['rooms_sold'].asfreq('D', fill_value=0)
        exog = None
        if external_vars:
            exog_df = pd.DataFrame(external_vars[0]['values']).set_index('date')
            exog = exog_df.reindex(y.index).fillna(0)
        model = SARIMAX(y, exog=exog, order=(1,1,1),
                        seasonal_order=(1,1,1,7), enforce_stationarity=False)
        fitted = model.fit(disp=False)
        forecast = fitted.get_forecast(forecast_days)
        return {
            'status': 'success',
            'model': 'SARIMA',
            'forecast': [{'date': str(forecast.predicted_mean.index[i].date()),
                          'predicted_rooms': round(forecast.predicted_mean.iloc[i], 1)}
                         for i in range(len(forecast.predicted_mean))]
        }
```

---

### RM-PRED-003 节假日需求预测
**功能描述**: 使用Facebook Prophet模型预测节假日期间需求，自动识别节假日效应

```yaml
SKILL-ID: RM-PRED-003
name: 节假日需求预测
group: prediction_model
```

**INPUT（输入Schema）**:
```json
{
  "historical_orders": [{"date": "date", "rooms_sold": "int"}],
  "holidays": [{"date": "date", "name": "string", "days": "int"}],
  "forecast_days": "int",
  "country": "CN"
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "model": "Prophet",
  "forecast": [{"date": "date", "predicted": "float", "effect": "string"}],
  "holiday_impact": [{"holiday_name": "string", "uplift_vs_normal": "float"}]
}
```

**PROMPT（执行指导）**:
```
# ROLE: 数据科学家
# TASK: 使用Prophet模型预测节假日期间需求
# REQUIREMENTS:
1. Prophet节假日效应：自动建模节前/节中/节后的需求曲线
2. 中国节假日：春节/国庆/五一/端午/中秋/清明（自动内置）
3. 节前效应：通常节前7天开始上升，节前3天达到高峰
4. 节后效应：假期结束后7~14天可能还有溢出
5. 需求提升计算：节假日日均需求 vs 平日日均需求，计算uplift%
```

**依赖项（dependencies）**:
- RM-DATA-001（历史节假日数据）
- RM-DATA-004（节假日数据）

**性能指标（metrics）**:
- 节假日效应量化
- 节前/节中/节后分解
- 定价溢价建议

**Python实现框架**:
```python
from prophet import Prophet
import pandas as pd

class HolidayDemandForecaster:
    def forecast(self, historical_orders, holidays, forecast_days=30, country='CN'):
        df = pd.DataFrame(historical_orders)
        df.columns = ['ds', 'y']
        df['ds'] = pd.to_datetime(df['ds'])
        m = Prophet(holidays=holidays, holidays_mode='multiplicative',
                   seasonality_mode='multiplicative')
        m.add_country_holidays(country_name=country)
        m.fit(df)
        future = m.make_future_dataframe(periods=forecast_days)
        forecast = m.predict(future)
        return {
            'status': 'success',
            'model': 'Prophet',
            'forecast': forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(forecast_days).to_dict('records')
        }
```

---

### RM-PRED-004 展会影响预测
**功能描述**: 评估展会期间对酒店需求的影响，计算展会效应系数

```yaml
SKILL-ID: RM-PRED-004
name: 展会影响预测
group: prediction_model
```

**INPUT（输入Schema）**:
```json
{
  "event": {
    "event_name": "string",
    "venue": "string",
    "start_date": "date",
    "end_date": "date",
    "expected_attendance": "int",
    "category": "international|national|regional|local"
  },
  "historical_with_similar_events": [{"date": "date", "rooms_sold": "int"}],
  "city_room_inventory": "int"
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "event_name": "string",
  "impact_analysis": {
    "event_rooms_demand": "float",
    "city_wide_occ_uplift": "float",
    "peak_day_demand": "float"
  },
  "pricing_recommendation": {
    "adr_premium_min": "float",
    "adr_premium_max": "float"
  }
}
```

**PROMPT（执行指导）**:
```
# ROLE: 收益策略师
# TASK: 预测展会对酒店需求的影响并给出定价策略
# REQUIREMENTS:
1. 历史展会效应：同类展会（同等规模/城市）的历史间夜增量
2. 城市供需分析：展会期间全市OCC提升数据（参考STR竞品数据）
3. 展会贡献估算：hotel_market_share × city_event_demand = hotel_event_demand
4. 分类影响系数：
   - 国际级展会：需求+60~120%，溢价0.5~1倍
   - 国家级：需求+30~60%，溢价0.3~0.5倍
   - 省级：需求+15~30%，溢价0.15~0.3倍
```

**依赖项（dependencies）**:
- RM-DATA-004（展会数据）
- historical_event_data

**性能指标（metrics）**:
- 展会贡献需求量化
- 溢价定价区间
- 风险识别

**Python实现框架**:
```python
class EventImpactPredictor:
    IMPACT_COEFFICIENTS = {
        'international': {'demand_uplift': (0.6, 1.2), 'adr_premium': (0.5, 1.0)},
        'national': {'demand_uplift': (0.3, 0.6), 'adr_premium': (0.3, 0.5)},
        'regional': {'demand_uplift': (0.15, 0.3), 'adr_premium': (0.15, 0.3)}
    }

    def predict(self, event, historical_events, city_inventory):
        category = event['category']
        coeff = self.IMPACT_COEFFICIENTS.get(category, self.IMPACT_COEFFICIENTS['regional'])
        attendance = event['expected_attendance']
        city_demand_uplift = (attendance / 1000) * 0.1
        hotel_demand = city_demand_uplift * 0.05
        duration = (pd.to_datetime(event['end_date']) - pd.to_datetime(event['start_date'])).days + 1
        peak_demand = hotel_demand * 1.5
        city_occ_uplift = (hotel_demand * duration) / city_inventory * 100
        return {
            'status': 'success',
            'event_name': event['event_name'],
            'impact_analysis': {
                'event_rooms_demand': round(hotel_demand * duration, 0),
                'city_wide_occ_uplift': round(city_occ_uplift, 1),
                'peak_day_demand': round(peak_demand, 0)
            },
            'pricing_recommendation': {
                'adr_premium_min': coeff['adr_premium'][0],
                'adr_premium_max': coeff['adr_premium'][1]
            }
        }
```

---

### RM-PRED-005 渠道需求预测
**功能描述**: 预测各渠道未来需求间夜量，指导渠道配额分配

```yaml
SKILL-ID: RM-PRED-005
name: 渠道需求预测
group: prediction_model
```

**INPUT（输入Schema）**:
```json
{
  "channel": "string",
  "historical_orders": [{"date": "date", "rooms_sold": "int"}],
  "forecast_period": {"start": "date", "end": "date"}
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "channel": "string",
  "forecast": [{"date": "date", "predicted_rooms": "float"}],
  "total_forecast_rooms": "float",
  "quota_recommendation": {"recommended_allocation": "float"}
}
```

**PROMPT（执行指导）**:
```
# ROLE: 数据科学家
# TASK: 预测特定渠道的未来需求
# REQUIREMENTS:
1. 模型选择：随机森林/XGBoost分类+回归联合预测
2. 特征工程：lead_time + day_of_week +节假日+ 竞品价格+ ADR差异
3. 输出：每日预测间夜 + ADR预测 + 收入预测
4. 渠道特征：OTA vs 官网 vs 协议，lead_time分布差异巨大
```

**依赖项（dependencies）**:
- RM-DATA-001（历史订单）
- RM-DATA-004（外部数据）

**性能指标（metrics）**:
- MAPE < 20%
- 渠道特征提取
- 配额建议输出

**Python实现框架**:
```python
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

class ChannelDemandForecaster:
    def forecast(self, channel, historical_orders, forecast_period, feature_vars):
        df = pd.DataFrame([o for o in historical_orders if o['channel'] == channel])
        if len(df) < 30:
            return {'status': 'error', 'message': 'insufficient data for channel'}
        X = df[feature_vars]
        y = df['rooms_sold']
        model = RandomForestRegressor(n_estimators=100).fit(X, y)
        future_features = self._build_features(forecast_period, channel)
        pred = model.predict(future_features)
        return {
            'status': 'success',
            'channel': channel,
            'total_forecast_rooms': round(pred.sum(), 1)
        }
```

---

### RM-PRED-006 提前期需求预测
**功能描述**: 基于贝叶斯方法预测不同提前期段的预订概率，优化早鸟/晚鸟定价

```yaml
SKILL-ID: RM-PRED-006
name: 提前期需求预测
group: prediction_model
```

**INPUT（输入Schema）**:
```json
{
  "booking_history": [{"lead_time": "int", "rooms_booked": "int"}],
  "target_date": "date",
  "current_bookings": "int",
  "current_adr": "float",
  "total_inventory": "int"
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "lead_time_buckets": [
    {"bucket": "string", "historical_probability": "float", "predicted_bookings": "float"}
  ],
  "optimal_early_bird_discount": "float",
  "optimal_last_minute_premium": "float"
}
```

**PROMPT（执行指导）**:
```
# ROLE: 收益策略师
# TASK: 基于贝叶斯模型预测不同提前期预订行为
# REQUIREMENTS:
1. 先验分布：基于历史同类型日期构建lead_time分布
2. 后验更新：随着当前预订数据更新需求预测
3. 预订分段概率：90天+(5~10%), 60~89天(10~15%), 30~59天(25~35%), 14~29天(25~30%), <14天(15~25%)
4. 定价联动：早鸟折扣 = f(当前OCC预测, 距入住天数), 晚鸟溢价 = f(剩余库存, 距入住天数)
```

**依赖项（dependencies）**:
- RM-DATA-001（预订历史）

**性能指标（metrics）**:
- 概率精度±5%
- 早鸟/晚鸟联动定价
- 动态更新

**Python实现框架**:
```python
from scipy import stats
import numpy as np

class LeadTimeDemandForecaster:
    LEAD_BUCKETS = ['90+days', '60-89days', '30-59days', '14-29days', '7-13days', '3-6days', '1-2days']

    def forecast(self, booking_history, target_date, current_bookings, total_inventory):
        hist_lens = [b['lead_time'] for b in booking_history]
        lead_dist = stats.gamma.fit(hist_lens, floc=0)
        buckets = []
        bounds = [(90, 999), (60, 89), (30, 59), (14, 29), (7, 13), (3, 6), (1, 2)]
        total_bookings = sum(b['rooms_booked'] for b in booking_history)
        for (low, high), bucket_name in zip(bounds, self.LEAD_BUCKETS):
            count = sum(b['rooms_booked'] for b in booking_history if low <= b['lead_time'] <= high)
            prob = count / total_bookings if total_bookings > 0 else 0.1
            predicted = prob * total_inventory
            buckets.append({'bucket': bucket_name, 'historical_probability': round(prob, 3)})
        current_occ = current_bookings / total_inventory if total_inventory > 0 else 0
        early_discount = max(0, (0.9 - current_occ) * 0.5)
        late_premium = current_occ * 0.3 if current_occ > 0.7 else 0
        return {
            'status': 'success',
            'lead_time_buckets': buckets,
            'optimal_early_bird_discount': round(early_discount, 2),
            'optimal_last_minute_premium': round(late_premium, 2)
        }
```

---

### RM-PRED-007 取消率预测
**功能描述**: 预测不同类型订单的取消概率，支持担保定价和超售决策

```yaml
SKILL-ID: RM-PRED-007
name: 取消率预测
group: prediction_model
```

**INPUT（输入Schema）**:
```json
{
  "reservation_data": [
    {"reservation_id": "string", "lead_time": "int", "channel": "string",
     "was_cancelled": "int"}
  ],
  "target_reservation": {"lead_time": "int", "channel": "string", "adr": "float"}
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "cancellation_probability": "float",
  "risk_level": "low|medium|high|critical",
  "recommended_actions": {
    "require_guarantee": "boolean",
    "guarantee_type": "string"
  }
}
```

**PROMPT（执行指导）**:
```
# ROLE: 收益策略师
# TASK: 预测订单取消概率并给出管控建议
# REQUIREMENTS:
1. 逻辑回归模型：P(取消) = sigmoid(β0 + Σβi×xi)
2. 关键特征：lead_time（越长越高）+ channel（OTA高于直销）+ 节假日（低于平日）+ ADR（高价高于低价）+ 会员等级
3. 风险分级：low(P<10%), medium(10~25%), high(25~50%), critical(P>50%)
4. 管控策略：high+要求担保，critical收取首晚房费或不允许取消
```

**依赖项（dependencies）**:
- RM-DATA-001（历史预订）

**性能指标（metrics）**:
- AUC > 0.75
- 风险分级输出
- 担保策略建议

**Python实现框架**:
```python
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import pandas as pd

class CancellationPredictor:
    def predict(self, reservation_data, target_reservation):
        df = pd.DataFrame(reservation_data)
        feature_cols = ['lead_time', 'adr']
        X = df[feature_cols]
        y = df['was_cancelled']
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        model = LogisticRegression().fit(X_scaled, y)
        X_new = scaler.transform([[target_reservation[f] for f in feature_cols]])
        prob = model.predict_proba(X_new)[0, 1]
        risk = 'critical' if prob > 0.5 else 'high' if prob > 0.25 else \
               'medium' if prob > 0.1 else 'low'
        return {
            'status': 'success',
            'cancellation_probability': round(prob, 3),
            'risk_level': risk,
            'recommended_actions': {
                'require_guarantee': prob > 0.25,
                'guarantee_type': 'credit_card' if prob > 0.4 else None
            }
        }
```

---

### RM-PRED-008 No-show率预测
**功能描述**: 使用泊松回归预测No-show率，支撑超售数量决策

```yaml
SKILL-ID: RM-PRED-008
name: No-show率预测
group: prediction_model
```

**INPUT（输入Schema）**:
```json
{
  "noshhow_data": [{"date": "date", "reservations": "int", "noshhows": "int"}],
  "target_date": "date",
  "current_reservations": "int"
}
```

**OUTPUT（输出Schema）**:
```json
{
  "status": "success|error",
  "predicted_noshhow_rate": "float",
  "predicted_noshhow_count": "float",
  "expected_arrivals": "int",
  "oversell_recommendation": {
    "oversell_count": "int",
    "risk_level": "low|medium|high"
  }
}
```

**PROMPT（执行指导）**:
```
# ROLE: 收益策略师
# TASK: 预测No-show率并给出超售建议
# REQUIREMENTS:
1. 泊松回归：No-show数量 ~ Poisson(λ)
2. 历史No-show基准：行业均值3~8%，OTA约5~10%，官网约2~5%
3. 关键驱动因素：无担保+3~5%，长lead_time每多30天+1~2%，ADR低No-show略高
4. 超售计算：期望超售收益 = oversell_count × probability_of_fullhouse × ADR
5. 风险控制：超售数不超过当前预订5%
```

**依赖项（dependencies）**:
- RM-DATA-001（历史No-show数据）

**性能指标（metrics）**:
- No-show率MAPE < 20%
- 超售收益/成本分析
- 风险控制

**Python实现框架**:
```python
from scipy import stats
import numpy as np

class NoShowPredictor:
    def predict(self, noshow_data, target_date, current_reservations):
        df = pd.DataFrame(noshow_data)
        df['noshhow_rate'] = df['noshhows'] / df['reservations']
        avg_rate = df['noshhow_rate'].mean()
        predicted_rate = min(0.15, max(0.02, avg_rate))
        predicted_noshhows = current_reservations * predicted_rate
        expected_arrivals = current_reservations - predicted_noshhows
        oversell_count = int(current_reservations * 0.03)
        risk = 'low' if oversell_count <= 3 else 'medium' if oversell_count <= 5 else 'high'
        return {
            'status': 'success',
            'predicted_noshhow_rate': round(predicted_rate, 3),
            'predicted_noshhow_count': round(predicted_noshhows, 1),
            'expected_arrivals': int(expected_arrivals),
            'oversell_recommendation': {
                'oversell_count': oversell_count,
                'risk_level': risk
            }
        }
```
