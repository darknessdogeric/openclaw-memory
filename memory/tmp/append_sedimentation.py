import json

# 1. append prediction to tomorrow.jsonl
pred = {
  'date': '2026-08-23',
  'predictor': 'B166ER 深度自迭代晚间',
  'confidence': 'high',
  'predictions': [
    {'type': 'Eric活动', 'value': '周一上班日，核心动作=联系刘宇钦 (80%)', 'reason': '8/22 重大校准发现直接上级=刘宇钦；三大能力汇报v1.0待审阅；R69倒计时7天'},
    {'type': 'B166ER角色', 'value': '继续DORMANT守夜 + standby (R67/R68/R69)', 'reason': 'R69 Day 23/30；无Eric召唤=无主动；守夜合规'},
    {'type': '安逸内部', 'value': '三大能力汇报v1.0审阅反馈 + 月底董事长调研汇报三件套', 'reason': '方法论v3.0+治理结构v1.2+能力汇报v1.0已就绪，等Eric反馈迭代'},
    {'type': 'AHL', 'value': '商业计划书v4待启动 + 边缘推理TCO方案', 'reason': 'Nvidia涨价>15%强化边缘推理优先判断；等Eric触发R14 handoff'},
    {'type': '全球市场', 'value': '8/24 美制裁伊朗窗口 + WTI $78-83区间', 'reason': '霍尔木兹威胁压制下跌，需求疲软压制上涨；美加贸易战9/8前无转机'}
  ],
  'created_at': '2026-08-23T21:00:00+08:00',
  'cron_trigger': '1abe7c29-24c1-4be8-8362-3554c6249c91'
}
with open('memory/predictions/tomorrow.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(pred, ensure_ascii=False) + '\n')

# 2. append industry event to industry-events.jsonl
ev = {
  'date': '2026-08-23',
  'event': '伊朗封锁霍尔木兹威胁 + 美加贸易战破裂 + 巴拿马运河限流 + Nvidia AI服务器涨价>15%',
  'sources': ['B166ER每日情报简报 8/23', 'Bloomberg', 'SCMP'],
  'impact': 'high',
  'ahl_relevance': '供应链成本上行传导酒店运营成本；Nvidia涨价强化AHL边缘推理优先；美元松动=跨境资产配置窗口',
  'category': 'geopolitical',
  'level': 'P1',
  'logged_at': '2026-08-23T21:00:00+08:00'
}
with open('memory/industry-events.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(ev, ensure_ascii=False) + '\n')

print('OK: prediction + industry event appended')
