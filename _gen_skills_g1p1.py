#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

def skill_block(skill_id, name, description, group_tag, input_schema, output_schema, prompt, dependencies, metrics, python_framework):
    b = []
    b.append(f"### {skill_id} {name}\n")
    b.append(f"**功能描述**: {description}\n")
    b.append("\n")
    b.append("```yaml\n")
    b.append(f"SKILL-ID: {skill_id}\n")
    b.append(f"name: {name}\n")
    b.append(f"group: {group_tag}\n")
    b.append("```\n")
    b.append("\n")
    b.append("**INPUT（输入Schema）**:\n")
    b.append("```json\n")
    b.append(input_schema)
    b.append("\n```\n")
    b.append("\n")
    b.append("**OUTPUT（输出Schema）**:\n")
    b.append("```json\n")
    b.append(output_schema)
    b.append("\n```\n")
    b.append("\n")
    b.append("**PROMPT（执行指导）**:\n")
    b.append("```\n")
    b.append(prompt)
    b.append("\n```\n")
    b.append("\n")
    b.append("**依赖项（dependencies）**:\n")
    for d in dependencies:
        b.append(f"- {d}\n")
    b.append("\n")
    b.append("**性能指标（metrics）**:\n")
    for m in metrics:
        b.append(f"- {m}\n")
    b.append("\n")
    b.append("**Python实现框架**:\n")
    b.append("```python\n")
    b.append(python_framework)
    b.append("\n```\n")
    b.append("\n")
    b.append("---\n")
    return "".join(b)

output_path = r'C:\Users\ericz\.openclaw\workspace\docs\收益管理AGENT-SKILL体系-V1.0.md'

# Read existing
with open(output_path, 'r', encoding='utf-8') as f:
    existing = f.read()

lines = [existing]

# ===== GROUP 1: DATA =====
lines.append("## 第一组：数据采集SKILL（4个）\n")

# RM-DATA-001
lines.append(skill_block(
    "RM-DATA-001", "PMS订单数据拉取",
    "从酒店PMS系统拉取历史订单数据，支持Opera/SAP/Flysht等主流PMS",
    "data_collection",
    """{
  "hotel_id": "string",
  "start_date": "date",
  "end_date": "date",
  "room_types": ["string"],
  "channels": ["string"],
  "rate_codes": ["string"],
  "fields": ["string"]
}""",
    """{
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
}""",
    """# ROLE: 数据工程师
# TASK: 从PMS系统拉取酒店订单历史数据
# REQUIREMENTS:
1. 连接PMS API，根据hotel_config识别PMS类型（Opera/SAP/Flysht/自定义）
2. 按日期/房型/渠道/价格码多维度筛选拉取
3. 数据脱敏处理：guest_name仅返回姓氏+脱敏字符（如"张**"）
4. ADR自动计算：room_revenue / occupied_rooms
5. 返回records数组+统计摘要+fetch_time_ms
6. 异常处理：PMS连接失败/数据超限/字段不匹配""",
    ["PMS_API_KEY", "hotel_config", "PMS_CONNECTION_POOL"],
    ["响应时间 < 5s", "数据完整率 > 99%", "脱敏合规率 100%"],
    """import requests
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
        }"""
))

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(''.join(lines))

print("Group 1 Part 1 saved")
