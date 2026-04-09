# Multi-OTA 价格采集 · 快速执行卡

## 一句话命令

**携程单平台** → 用chrome-devtools导航 → image工具解析

**多平台均价** → 按此卡顺序执行

---

## 标准工作流（多平台）

### Step 1: 搜索酒店（各平台）

| 平台 | 搜索URL格式 | 示例 |
|------|-----------|------|
| 携程 | `hotels.ctrip.com/hotels/list/?cityName=城市&cityId=ID` | 大理/滁州 |
| 美团 | `meituan.com/s/城市+酒店名` | meituan.com/s/滁州+君家 |
| 去哪儿 | `qunar.com/site/oneshot/城市/酒店名.htm` | — |
| 飞猪 | `fliggy.com/hotel/城市/酒店名` | — |

### Step 2: 截图每个平台

```
chrome-devtools → navigate_page(URL) → wait → take_screenshot → 保存
```

### Step 3: AI解析（image工具）

对每张截图调用：
```
prompt: "你是酒店价格分析师。请提取所有房间名称和价格。
排除：套房/家庭房/亲子房/行政房/复式Loft/别墅
纳入：高级房/豪华房/单间/标间/大床房/双床房
返回JSON数组格式。"
```

### Step 4: 数据汇总（手填或脚本）

```python
platform_results = [
    {"platform": "ctrip", "adr": 298, "rooms": 3},
    {"platform": "meituan", "adr": 285, "rooms": 2},
    {"platform": "qunar", "adr": 292, "rooms": 2},
]
```

### Step 5: 计算加权ADR

```
python multi_ota_crawler.py <酒店名> [城市]
```

---

## OCC估算表

| 城市等级 | 5钻/五星 | 4钻/四星 | 3钻/三星 | 2钻以下 |
|---------|---------|---------|---------|---------|
| 一线城市 | 80% | 75% | 70% | 65% |
| 二线城市 | 75% | 70% | 65% | 60% |
| 三线城市 | 70% | 65% | 60% | 55% |

> 默认：二线城市 4钻 = 70%

---

## 标准房判定（优先级）

1. **有关键词** → 纳：高级/豪华/单间/标间
2. **无关键词** → 看原始库存最大2种
3. **无法判断** → 主观（主理人判断）

**排除**：套房/家庭房/亲子房/行政房/复式Loft/别墅

---

## 输出格式

```json
{
  "hotel_name": "酒店名",
  "weighted_adr": 298.5,
  "simple_adr": 291.7,
  "occ_estimate": 0.70,
  "revpar_estimate": 209,
  "confidence": "high",
  "sources": [
    {"platform": "ctrip", "adr": 305, "weight": 0.4},
    {"platform": "meituan", "adr": 285, "weight": 0.3},
    {"platform": "qunar", "adr": 292, "weight": 0.2}
  ]
}
```

---

## 已知携程cityId

| 城市 | cityId | URL |
|------|--------|-----|
| 大理 | 36 | hotels.ctrip.com/hotels/list/?cityName=大理&cityId=36 |
| 滁州 | 214 | hotels.ctrip.com/hotels/list/?cityName=滁州&cityId=214 |
| 重庆 | 4 | hotels.ctrip.com/hotels/list/?cityName=重庆&cityId=4 |
| 乐山 | 36 | (同大理，需搜索确认) |
| 成都 | 28 | hotels.ctrip.com/hotels/list/?cityName=成都&cityId=28 |

> 未知城市：去 https://hotels.ctrip.com/jiudian/ 查找

---

## 执行检查清单

```
[ ] 确认酒店在每个OTA平台都有
[ ] 截图保存到 skills/multi-ota-price-tool/output/
[ ] image工具分析每个截图
[ ] 提取标准房价格（排除特殊房型）
[ ] 还原真实裸收益 (挂牌价 - 优惠) × 0.85
[ ] 计算各平台ADR均值
[ ] 估算OCC（城市等级 + 酒店档次）
[ ] 计算加权ADR + RevPAR
[ ] 输出结构化报告
```

---

**文件位置**: `skills/multi-ota-price-tool/`
