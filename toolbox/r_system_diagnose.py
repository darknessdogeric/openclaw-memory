#!/usr/bin/env python3
"""R体系诊断脚本 - 深度迭代前置分析"""
import re, os, collections

path = os.path.expanduser("~/self-improving/rules.md")
text = open(path, encoding="utf-8", errors="replace").read()
lines = text.splitlines()

print(f"=== 文件概览 ===")
print(f"总行数: {len(lines)}")
print(f"总字节: {len(text.encode('utf-8'))}")

# 提取所有 R 编号（标题级别，行首 R 开头）
rule_headers = re.findall(r'^#{1,4}\s*(R[\d\-]+)', text, re.M)
rule_mentions = re.findall(r'\bR[\d]{2,3}\b', text)

print(f"\n=== 规则标题（标题级）数量 ===")
print(f"标题级 R 编号: {len(rule_headers)} 个")

# 统计每个编号出现的标题次数
cnt = collections.Counter(rule_headers)
dups = {k: v for k, v in cnt.items() if v > 1}
print(f"\n=== 标题级重复编号 (ID 冲突) ===")
if dups:
    for k, v in sorted(dups.items()):
        print(f"  {k}: 出现 {v} 次")
else:
    print("  无")

# 全文中 R 编号提及次数（识别"幽灵规则"，被引用但无定义）
mention_cnt = collections.Counter(re.findall(r'\bR\d{2,3}\b', text))
defined = set(re.findall(r'^#{1,4}\s*(R\d{2,3})', text, re.M))
defined_full = set()
for d in defined:
    defined_full.add(d)
# 也识别 "R12"/"R48" 这类
all_defined = set()
for m in re.finditer(r'^#{1,4}\s*(R\d{2,3}(?:-\d+)?)', text, re.M):
    base = m.group(1).split('-')[0]
    all_defined.add(base)

ghost = sorted([k for k in mention_cnt if k not in all_defined and int(k[1:]) >= 40])
print(f"\n=== 被提及但可能无独立定义的编号（前30）===")
print("  " + ", ".join(ghost[:30]))

# 检测编码损坏（mojibake 字符）
mojibake = re.findall(r'[\ufffd]', text)
print(f"\n=== 编码损坏检测 ===")
print(f"  U+FFFD 替换字符: {len(mojibake)} 个")
# 检测常见乱码模式（GBK 解码错误的特征）
bad_chars = re.findall(r'[\u00c0-\u00ff]{3,}', text)
print(f"  疑似 GBK 乱码片段: {len(bad_chars)} 个")

# 按主题粗略分类统计（关键词）
themes = {
    "沉默期/静默": r'沉默|静默|DORMANT',
    "cron/运行时": r'cron|isolated|运行时',
    "报告/交付": r'月报|报告|交付|PDF|简报',
    "信息图/视觉": r'信息图|视觉|徽章|badge|海报',
    "AHL": r'AHL',
    "安逸/AnYi": r'安逸|AnYi',
    "自媒体/合规": r'小红书|自媒体|xhs|合规',
    "数据估算/投资": r'估算|投资|数据可信',
    "工具调用/PowerShell": r'PowerShell|工具调用|write 工具',
    "自我改进/元规则": r'候选|转化|自迭代|自我改进',
}
print(f"\n=== 主题分布（按关键词命中标题）===")
for theme, pat in themes.items():
    hits = sum(1 for h in rule_headers if re.search(pat, text[text.find(h):text.find(h)+200] or ""))
    # 简化：按整行
    c = 0
    for line in lines:
        if re.match(r'^#{1,4}\s*R', line) and re.search(pat, line):
            c += 1
    print(f"  {theme}: {c} 条")
