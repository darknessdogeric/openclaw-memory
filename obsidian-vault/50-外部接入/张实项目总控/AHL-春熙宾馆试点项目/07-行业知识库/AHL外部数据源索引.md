# AHL 外部数据源索引

**版本**: V1.0
**日期**: 2026-04-18
**编制**: B166ER
**用途**: AHL智能运营系统外部数据对接参考

---

## 一、数据源分类总览

```
AHL外部数据源
├── 🌤️ 天气数据（最高优先级）
├── 📊 经济与消费数据
├── 🏨 旅游与酒店行业数据
├── 🔍 搜索热度数据
├── 🗓️ 日历与事件数据
└── 📍 地理与交通数据
```

---

## 二、天气数据（⭐⭐⭐⭐⭐ 最高优先）

### 2.1 Open-Meteo

**类型**：免费开源天气API，无需注册
**API地址**：https://open-meteo.com/
**覆盖**：全球任意经纬度
**数据频率**：每小时/每日

| 接口 | 说明 | 酒店场景用途 |
|------|------|-------------|
| hourly (温度/降水/云量) | 每小时预报 | 短期入住率预测 |
| daily (最高/最低/降雨概率) | 每日预报 | 7-14天收益预测 |
| historical_weather | 历史天气 | 同比分析基准 |

**API调用示例**：
```
https://api.open-meteo.com/v1/forecast?
    latitude=30.6587&longitude=104.0668  (成都)
    &hourly=temperature_2m,precipitation,cloudcover
    &daily=temperature_2m_max,temperature_2m_min,precipitation_probability
    &forecast_days=14
```

**数据字段**：
- `temperature_2m` — 温度（影响旅游/出行意愿）
- `precipitation` — 降水量（雨天=低入住率）
- `cloudcover` — 云量（影响拍照/景区体验）
- `precipitation_probability` — 降雨概率（客人决策参考）

**酒店场景映射**：
| 天气条件 | 入住率影响 | 价格策略 |
|---------|-----------|---------|
| 晴天+高温 | +10-15% | 可溢价 |
| 雨天 | -5-10% | 促销降价 |
| 暴雨/台风 | -20-30% | 大幅促销或关房 |
| 阴天凉爽 | +5% | 维持或小幅下调 |

---

### 2.2 Visual Crossing

**类型**：免费天气API（每天1000次调用）
**API地址**：https://www.visualcrossing.com/weather-api
**特点**：历史数据+预报数据合一

---

### 2.3 WorldWeatherOnline

**类型**：付费/免费混合
**API地址**：https://www.worldweatheronline.com/
**免费额度**：每月500次
**特点**：提供旅游指数、紫外线指数等

---

## 三、经济与消费数据（⭐⭐⭐ 高优先）

### 3.1 Google Trends

**类型**：搜索热度数据
**地址**：https://trends.google.com/
**API**：Google Trends API (Pytrends库)

| 搜索词 | 酒店场景用途 |
|--------|-------------|
| "成都酒店" | 实时需求热度 |
| "春熙路附近酒店" | 区域需求监控 |
| "成都旅游" | 季节性需求预测 |
| "酒店优惠券" | 促销效果评估 |

**Pytrends调用示例**：
```python
from pytrends.request import TrendReq
pytrends = TrendReq(hl='zh-CN', tz=360)
pytrends.build_payload(kw_list=['成都酒店'], timeframe='today 3-m')
data = pytrends.interest_over_time()
```

---

### 3.2 World Bank Open Data

**类型**：全球发展指标
**地址**：https://data.worldbank.org/
**API**：https://api.worldbank.org/v2/

| 指标 | 酒店场景用途 |
|------|-------------|
| GDP per capita | 消费能力评估 |
| International tourism | 出入境趋势 |
| Consumer price index | 通胀影响定价 |

---

### 3.3 UN Trade Statistics

**类型**：国际贸易与旅游数据
**地址**：https://unstats.un.org/unsd/
**用途**：出入境旅游统计

---

## 四、旅游与酒店行业数据（⭐⭐⭐ 中优先）

### 4.1 UN Tourism Statistics

**类型**：全球旅游业统计
**地址**：https://www.unwto.org/
**免费数据**：
- 全球旅游趋势
- 各国出入境人数
- 旅游收入统计

---

### 4.2 STR (Smith Travel Research)

**类型**：酒店行业数据（需付费）
**地址**：https://str.com/
**数据**：
- 酒店入住率平均值
- 平均房价
- RevPAR指数

**注意**：基础报告有时免费发布

---

### 4.3 中国旅游研究院

**类型**：中国旅游数据
**地址**：https://www.cta-web.org.cn/
**数据**：
- 国内旅游人数
- 旅游收入
- 假期旅游报告

---

### 4.4 国家统计局

**类型**：中国宏观数据
**地址**：https://data.stats.gov.cn/
**酒店相关数据**：
- 限额以上住宿业营业额
- 消费者信心指数
- 城镇人口可支配收入

---

## 五、搜索热度数据（⭐⭐⭐⭐ 高优先）

### 5.1 百度指数

**类型**：中国市场搜索热度
**地址**：https://index.baidu.com/
**数据**：
- 关键词搜索趋势
- 人群画像（年龄/地域）
- 相关词热度

**酒店相关词**：
| 关键词 | 用途 |
|--------|------|
| 成都酒店 | 区域需求监控 |
| 春熙路酒店 | 精准竞品监控 |
| 成都旅游攻略 | 出行需求预判 |

---

### 5.2 微信指数

**类型**：微信生态热度
**地址**：微信搜一搜→微信指数
**用途**：私域流量监控

---

## 六、日历与事件数据（⭐⭐⭐⭐ 高优先）

### 6.1 中国法定节假日

**数据来源**：国务院每年发布节假日安排

| 节日 | 通常时间 | 入住率峰值 |
|------|---------|-----------|
| 春节 | 大年三十→初六 | 95%+ |
| 清明 | 4月初3天 | 85%+ |
| 五一 | 5月1-5天 | 90%+ |
| 端午 | 6月3天 | 80%+ |
| 中秋+国庆 | 10月1-7天 | 95%+ |
| 元旦 | 1月1-3天 | 85%+ |

**提前量**：节假日价格调整需提前14-30天

---

### 6.2 糖酒会/展会日历

**数据来源**：成都市博览局官网

| 展会 | 时间 | 入住率影响 |
|------|------|-----------|
| 成都糖酒会 | 3月/11月 | +30-50% |
| 西博会 | 9-10月 | +20-30% |
| China运动用品展 | 待查 | +10-20% |

---

### 6.3 大运会/演唱会等事件

**监控方式**：
- 成都本地宝公众号
- 大麦网演出日历
- 微博热搜

---

## 七、地理与交通数据（⭐⭐ 辅助）

### 7.1 高德地图/百度地图

**数据**：
- 酒店周边配套（餐饮/景点/交通）
- 实时交通拥堵指数
- 地铁/公交可达性

**用途**：
- 酒店位置评分
- 竞品辐射范围分析

---

## 八、数据接入优先级排序

### 第一优先级（立即可接入）

| 数据源 | 接入方式 | AGENT模块 | 工作量 |
|--------|---------|----------|--------|
| **Open-Meteo天气** | API | 收益管理-预测 | 2小时 |
| **糖酒会/节假日** | 本地日历表 | 收益管理-事件 | 1小时 |

### 第二优先级（后续迭代）

| 数据源 | 接入方式 | AGENT模块 | 工作量 |
|--------|---------|----------|--------|
| **百度指数** | API | 竞品分析-需求监控 | 4小时 |
| **Google Trends** | Pytrends | 竞品分析-需求监控 | 4小时 |

### 第三优先级（价值验证后）

| 数据源 | 接入方式 | AGENT模块 | 工作量 |
|--------|---------|----------|--------|
| 国家统计局 | API | 收益管理-宏观特征 | 8小时 |
| UN Tourism | CSV下载 | 收益管理-行业基准 | 8小时 |

---

## 九、API对接技术规范

### 9.1 标准调用模式

```python
class ExternalDataConnector:
    """外部数据连接器基类"""
    
    def fetch(self, **kwargs):
        """获取数据，子类实现"""
        raise NotImplementedError
    
    def parse(self, raw_data):
        """解析数据，子类实现"""
        raise NotImplementedError
    
    def to_features(self, parsed_data):
        """转换为AGENT可用特征"""
        raise NotImplementedError


class WeatherConnector(ExternalDataConnector):
    """天气数据连接器"""
    
    def __init__(self, lat, lon):
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        self.params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,precipitation,cloudcover",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability",
            "forecast_days": 14,
            "timezone": "Asia/Shanghai"
        }
    
    def to_features(self, data):
        """转换为收益预测特征"""
        return {
            "rain_probability": data["daily"]["precipitation_probability"][0],
            "avg_temperature": (data["daily"]["temperature_2m_max"][0] + 
                               data["daily"]["temperature_2m_min"][0]) / 2,
            "is_weekend": data["is_weekend"],  # 需结合日历
            "upcoming_holiday": data["days_to_holiday"]
        }
```

### 9.2 缓存策略

| 数据类型 | 缓存频率 | 缓存时长 | 更新方式 |
|---------|---------|---------|---------|
| 天气预报 | 每6小时 | 6小时 | 自动轮询 |
| 节假日数据 | 一次性 | 全年 | 每年更新 |
| 百度指数 | 每日 | 24小时 | 每日抓取 |
| 经济指标 | 每月 | 月度 | 定期拉取 |

---

## 十、数据源文档位置

| 数据源 | 官方文档 |
|--------|---------|
| Open-Meteo | https://open-meteo.com/en/docs |
| Google Trends | https://developers.google.com/trends |
| World Bank API | https://datahelpdesk.worldbank.org/ |
| 国家统计局 | https://data.stats.gov.cn/api/ |

---

**文档版本**: V1.0
**编制**: B166ER
**最后更新**: 2026-04-18


---

## 🔗 相关笔记

- [[AHL 平台 MOC]]
- [[酒店行业 MOC]]
- [[B166ER 知识库 MOC]]

*该区块由 B166ER 自动注入 (2026-07-28) — 关键词匹配*
