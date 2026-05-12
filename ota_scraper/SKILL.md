# OTA-Scraper Framework v1.4

## 新能力

### 自适配选择器引擎 (`adaptive.py`)
64个候选选择器覆盖6个字段类型。当平台配置的选择器0命中时自动扫描匹配。
- hotel_list: 17候选 (Booking/Agoda/Expedia/Ctrip/Meituan/通用)
- hotel_name: 13候选 | hotel_price: 10候选
- hotel_score: 10候选 | hotel_reviews: 7候选 | hotel_address: 7候选

### 移动API端点库
9个平台的移动端URL和API端点已收录，移动端通常防护更弱。
- Ctrip: m.ctrip.com/restapi/soa2 端点
- Qunar: touch.qunar.com API
- Meituan: i.meituan.com + ihotel API
- Booking: dml/graphql 端点
- Expedia/Agoda/TripAdvisor: GraphQL端点

### 代理配置
国际OTA网络超时解决方案：设置proxy即可突破

## 已校准平台

| 平台 | 状态 | 提取率 | 字段 |
|------|------|--------|------|
| Booking | ✅ 已校准 | 25-27/页 | 名称✅价格✅评分✅评论✅地址✅ |
| Ctrip | ✅ 已校准 | 15/页 | 名称✅星级✅评分✅评论✅地址✅ID✅ |
| Agoda | 🔧 选择器预配 | 待测试 | (同Booking技术栈) |
| 其余14平台 | 🔧 自适应+预配置 | 待触发 | 64候选自动匹配 |

## 快速使用

```bash
python ota_scraper/run.py booking 北京     # 25家+价格
python ota_scraper/run.py ctrip 上海       # 15家+星级
python ota_scraper/stats.py                # 统计对比报告
```
