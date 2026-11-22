# -*- coding: utf-8 -*-
"""
用 DeepSeek 把月度经济报告改写为 PDF-ready 版本
策略：保留所有数据 + 核心洞察，但精简冗余 + 强化视觉节奏
"""
import os, json, requests, sys
from pathlib import Path

# 配置
DEEPSEEK_KEY = os.environ['DEEPSEEK_API_KEY']
SRC_MD = Path(r"D:\B166ER-OpenClaw\workspace\reports\2026-07-15-6月经济数据全方位解读-官方原文验证版.md")
OUT_MD = Path(r"D:\B166ER-OpenClaw\workspace\reports\2026-07-15-6月经济数据全方位解读-PDF版.md")

src = SRC_MD.read_text(encoding='utf-8')
print(f"源文件: {len(src)} chars / {len(src.encode('utf-8'))//1024} KB")

PROMPT = f"""你是 B166ER —— Eric 的全能型助理。
任务：把下面的 2026 年 6 月/上半年 经济数据报告改写为 **PDF 印刷版**。

# 改写规则（必须严格遵守）

## 1. 内容原则
- **保留所有数据**：表格、百分比、信号灯、正负号都不能改
- **保留核心洞察**：五维因果链（直接/深层/系统/说明/反映/推论）
- **保留五条底层规律 + 四个核心判断 + 一句话总结**
- **保留官方原文链接清单**

## 2. PDF排版优化（与屏幕阅读区别）
- 表格压缩：能合并的合并，能精简的精简
- 长段落拆短：每段 ≤ 4 行
- 删除「emoji信号灯」🟢🟡🔴 等视觉装饰（PDF里用文本即可：✓ / ! / ✗）
- 删除冗余修饰（"❗"、"🔥"重复等）
- **精简冗余表述**：原文"知其然知其所以然"核心思想保留，但描述更紧凑

## 3. 必须新增的「PDF阅读引导」
在开头加一段「**阅读说明**」（200字内）：
- 目标读者：Eric + 自留档
- 阅读时间：15-20分钟
- 核心结论：一行字（房地产断崖 / 消费降级固化 / 高技术独苗）
- 用途：政策窗口预判 + 实战决策连接

## 4. 输出格式
- 直接输出改写后的 Markdown
- 不要解释、不要前言
- 用 >>> 和 <<< 包裹输出
- 标题层级：# (报告标题) / ## (大节) / ### (小节) / #### (细分)
- 表格保持原样（markdown 语法）

# 原始报告

{src}

>>>"""

print("调用 DeepSeek...")
r = requests.post(
    'https://api.deepseek.com/v1/chat/completions',
    headers={'Authorization': f'Bearer {DEEPSEEK_KEY}', 'Content-Type': 'application/json'},
    json={
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'system', 'content': '你是 B166ER，专精宏观经济分析与可视化报告排版的全能助理。'},
            {'role': 'user', 'content': PROMPT},
        ],
        'max_tokens': 8000,
        'temperature': 0.3,
    },
    timeout=120,
)
print(f"status: {r.status_code}")
data = r.json()
if r.status_code != 200:
    print("ERROR:", json.dumps(data, ensure_ascii=False, indent=2)[:2000])
    sys.exit(1)

content = data['choices'][0]['message']['content']
# 提取 >>> 到 <<< 之间
if '>>>' in content:
    content = content.split('>>>', 1)[1]
if '<<<' in content:
    content = content.split('<<<', 1)[0]
content = content.strip()

OUT_MD.write_text(content, encoding='utf-8')
print(f"✅ 已写入: {OUT_MD} ({len(content)} chars / {len(content.encode('utf-8'))//1024} KB)")
print(f"📊 使用 tokens: {data.get('usage', {}).get('total_tokens', '?')}")