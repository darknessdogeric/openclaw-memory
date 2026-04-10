# 数据获取技能 (Data Acquisition Skill)

## 功能
免费获取酒店行业相关数据，支持：
- 行业新闻采集
- 竞品数据监控
- OTA平台数据
- 政策法规
- 舆情监控

## 工具栈

| 工具 | 用途 | 状态 |
|------|------|------|
| Jina Reader | 网页转markdown | ✅ |
| data_collector.py | 主采集脚本 | ✅ |
| RSS订阅 | 行业更新 | ✅ |

## 使用方法

### 手动采集
```bash
python C:\Users\ericz\.openclaw\data-acquisition\data_collector.py
```

### 采集内容
1. **行业新闻** - 36氪/虎嗅/钛媒体RSS
2. **携程酒店** - 指定城市酒店列表
3. **统计局数据** - 宏观旅游数据
4. **竞品价格** - 全季/亚朵/华住

## 定时任务
- **Cron ID**: 284e4a7e-d9e0-4ac5-adde-9c85dd58c980
- **执行时间**: 每日 8:00 和 20:00
- **状态**: 已启用

## 数据输出
- 位置: `C:\Users\ericz\.openclaw\data-acquisition\data\`
- 格式: JSON
- 命名: `{类型}_{日期}.json`

## 扩展方向
- [ ] 接入更多RSS源
- [ ] 竞品价格自动化对比
- [ ] 微信指数监控
- [ ] 百度指数监控
- [ ] Google Alerts
