# -*- coding: utf-8 -*-
"""B166ER: 用 DeepSeek 生成综合报告的 WHY 板块"""
import os, json, requests
from pathlib import Path

DEEPSEEK_KEY = os.environ['DEEPSEEK_API_KEY']
REPORTS_DIR = Path(r'D:\B166ER-OpenClaw\workspace\reports')

# 读所有 6 份报告
reports_text = ""
files = sorted(REPORTS_DIR.glob('2026-07-16-新能源车外挂小蓝灯-*.md'))
for f in files:
    reports_text += f"\n\n===== {f.name} =====\n\n"
    reports_text += f.read_text(encoding='utf-8')

# 限制长度避免超过 token 上限
print(f'6 份报告总字符数: {len(reports_text)}')

PROMPT = f"""你是 B166ER —— Eric 的全能型助理。本任务是基于已有的 6 份子报告，写出综合报告的「WHY 板块」(现象到本质)。

# 任务
基于以下 6 份子报告已经收集的数据和事实，写出 4 个 WHY 假设的完整深度展开 + 综合模型 + 趋势预测。每个假设都要包含 4 个部分：**数据支撑 / 反例与边界 / 置信度 / 与其他假设的关系**。最后给出一个**综合模型**把这些假设融合成一个可解释框架。

# 数据来源（已收集）
{reports_text[:35000]}

# 4 个候选 WHY 假设（来自初步分析）
1. 炫耀动机谱系（Veblen 商品 / 信号理论 / 制度性身份）
2. 替代品经济学（功能 → 装饰，类似车贴/尾翼/拉花）
3. 制度性偷懒（省去合规审批，类似"自建充电桩"灰色地带）
4. AI 时代身份伪造（AI 时代"装 X"的新变种，"我消费故我在"）

# 输出格式（必须遵守）
- 纯 Markdown
- 用 >>> 和 <<< 包裹输出
- 每个假设独立 H3 标题，含 4 个小标题：数据支撑 / 反例与边界 / 置信度 / 与其他假设的关系
- 综合模型独立大段（在 4 个假设之后）
- 未来 12-18 个月预测 3 条
- 风格：**麦肯锡 + 三联生活周刊**（数据 + 人文洞察）

# 写作要求
- 文笔犀利，**有 Eric 想要的人性洞察深度**（Eric 是酒店业老兵，对"消费心理"特别敏感）
- 不空说，每个数据点都引用上面报告里有的事实
- 留意三个 Eric 视角的隐形洞察：
  (a) 中国中产消费心理
  (b) AI 时代身份焦虑  
  (c) 智能驾驶时代的"信号"如何被重新定义
- 不超过 3500 字

# 输出

>>>"""

print("调用 DeepSeek...")
r = requests.post(
    'https://api.deepseek.com/v1/chat/completions',
    headers={'Authorization': f'Bearer {DEEPSEEK_KEY}', 'Content-Type': 'application/json'},
    json={
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'system', 'content': '你是 B166ER，专精消费现象分析与商业洞察的全能助理。请用 Eric 偏好的深度 + 犀利文笔输出。'},
            {'role': 'user', 'content': PROMPT},
        ],
        'max_tokens': 6000,
        'temperature': 0.5,
    },
    timeout=180,
)
print(f'status: {r.status_code}')
data = r.json()
if r.status_code != 200:
    print("ERROR:", json.dumps(data, ensure_ascii=False, indent=2)[:1500])
    import sys
    sys.exit(1)

content = data['choices'][0]['message']['content']
# 提取 >>> 到 <<< 之间
if '>>>' in content:
    content = content.split('>>>', 1)[1]
if '<<<' in content:
    content = content.split('<<<', 1)[0]
content = content.strip()

# 保存
(REPORTS_DIR / '2026-07-16-新能源车外挂小蓝灯-why-raw.md').write_text(content, encoding='utf-8')
print(f'Saved: {len(content)} chars / {len(content.encode("utf-8"))//1024} KB')
print(f'Tokens used: {data.get("usage", {}).get("total_tokens", "?")}')
