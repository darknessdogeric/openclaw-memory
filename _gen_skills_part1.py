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

lines = []

# ===== HEADER =====
lines.append("# 收益管理 AGENT SKILL体系 V1.0\n")
lines.append("> **版本**: V1.0  \n")
lines.append("> **日期**: 2026-03-26  \n")
lines.append("> **定位**: 收益管理场景的最小可执行SKILL单元，可独立调用或组合编排  \n")
lines.append("> **范围**: 数据采集 / 指标计算 / 预测模型 / 定价决策 / 库存管理 / 竞品分析 / 分析报表  \n")
lines.append("> **SKILL总数**: 51个  \n")
lines.append("\n---\n")

# ===== OVERVIEW =====
lines.append("## 概述\n")
lines.append("### 设计理念\n")
lines.append("收益管理SKILL体系将酒店收益管理全链路拆解为**51个最小可执行单元**。每个SKILL：\n")
lines.append("- 有明确输入/输出（JSON Schema）\n")
lines.append("- 有完整prompt指导LLM执行\n")
lines.append("- 可独立调用，也可组合使用\n")
lines.append("- 包含Python实现框架参考\n")
lines.append("\n")
lines.append("**底层逻辑**：如果收益管理是一个工厂，那么数据是原料，指标是质检标准，预测是需求探测器，定价是定价引擎，库存是仓储调度，竞品分析是市场雷达，报表是管理驾驶舱。\n")
lines.append("\n")
lines.append("### SKILL分类总览\n")
lines.append("\n")
lines.append("| 组别 | SKILL数量 | 核心功能 |\n")
lines.append("|------|-----------|----------|\n")
lines.append("| 第一组：数据采集 | 4个 | PMS/OTA/竞品/外部数据拉取 |\n")
lines.append("| 第二组：指标计算 | 13个 | ADR/OCC/RevPAR/STR指数/渠道分析/房型分析 |\n")
lines.append("| 第三组：预测模型 | 8个 | 需求预测/展会影响/取消率/No-show预测 |\n")
lines.append("| 第四组：定价决策 | 10个 | 基准/动态/事件/早鸟/渠道差异化定价 |\n")
lines.append("| 第五组：库存管理 | 6个 | 可售/配额/超售/升舱/预警/保留房 |\n")
lines.append("| 第六组：竞品分析 | 5个 | 价格监控/动态预警/周报/Benchmark/活动监控 |\n")
lines.append("| 第七组：分析报表 | 6个 | 日报/周报/月报/预算vs实际/渠道/预测准确率 |\n")
lines.append("| **合计** | **51个** | |\n")
lines.append("\n")
lines.append("---\n")

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(''.join(lines))

print("Header saved")
