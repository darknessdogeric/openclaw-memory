# -*- coding: utf-8 -*-
"""B166ER integration index (no emojis for PowerShell compat)"""
from pathlib import Path
import re

OUT_DIR = Path('reports')
files = sorted(OUT_DIR.glob('2026-07-16-新能源车外挂小蓝灯-*.md'))

reports = {}
for f in files:
    content = f.read_text(encoding='utf-8')
    fm = re.findall(r'(\w+):\s*(.*)', content[:600])
    fm_dict = dict(fm)
    headings = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
    reports[f.name] = {
        'fm': fm_dict,
        'chars': len(content),
        'size_kb': len(content.encode('utf-8'))//1024,
        'headings_count': len(headings),
        'tables_count': content.count('|---'),
    }

def extract_tldr(content):
    lines = content.split('\n')
    tldr_lines = []
    in_tldr = False
    for line in lines[:200]:
        if any(kw in line for kw in ['TL;DR', '执行摘要', '核心结论', '核心发现', '一句话核心结论']):
            in_tldr = True
            continue
        if in_tldr:
            if line.strip().startswith('##'):
                break
            clean = line.strip()
            if clean and clean != '|':
                tldr_lines.append(clean)
    return '\n'.join(tldr_lines[:30])

output = []
output.append('---')
output.append('author: B166ER (主会话)')
output.append('audience: Eric')
output.append('status: active')
output.append('created: 2026-07-16 12:25 GMT+8')
output.append('type: 数据集成索引 / Phase 2 完整数据图')
output.append('topic: 新能源车外挂小蓝灯 6 份报告集成索引')
output.append('parent: reports/2026-07-16-新能源车外挂小蓝灯-全网扒数据.md')
output.append('---')
output.append('')
output.append('# Phase 2 数据集成索引')
output.append('')
output.append('> Eric 11:31 提醒: 所有电商和新媒体平台都要去看。')
output.append('> 本次响应: 3 个并发 sub-agent 在 11:33-12:15 完成所有数据采集。')
output.append('> 下一阶段: Eric 决定是否跳到 WHY 分析。')
output.append('')

output.append('## 6 份报告文件位置 + 体量')
output.append('')
output.append('| 序 | 文件名 | 大小 | 角色 |')
output.append('|----|--------|------|------|')
output.append('| 0 | 2026-07-16-新能源车外挂小蓝灯-全网扒数据.md | 18 KB | Phase 1 速报(您最初的问题) |')
output.append('| 1 | 2026-07-16-新能源车外挂小蓝灯-电商平台全覆盖.md | 35 KB | 9 电商全平台数据 |')
output.append('| 2 | 2026-07-16-新能源车外挂小蓝灯-新媒体平台全覆盖.md | 54 KB | 10 新媒体全平台数据 |')
output.append('| 3 | 2026-07-16-新能源车外挂小蓝灯-海外参考.md | 12 KB | 欧美同类 + 销量 |')
output.append('| 4 | 2026-07-16-新能源车外挂小蓝灯-法规深度.md | 23 KB | 国标 + 工信部 + 公安部 |')
output.append('| 5 | 2026-07-16-新能源车外挂小蓝灯-评论解码.md | 21 KB | 4 派→8 子态度 + 5 原话 |')
output.append('')
output.append('总数据量: 约 163 KB / 6 份 markdown / ~102 次独立搜索 + 14 个详情页抓取')
output.append('')

output.append('## 核心数据汇总 (来自子任务 TL;DR)')
output.append('')

for f in files:
    content = f.read_text(encoding='utf-8')
    if '全网扒数据' in f.name:
        continue
    output.append(f'### {f.name}')
    output.append('```')
    output.append(extract_tldr(content))
    output.append('```')
    output.append('')

output.append('## 数据完整性自评 (各子任务的诚实声明)')
output.append('')
output.append('| 维度 | 覆盖度 | 关键说明 |')
output.append('|------|-------|---------|')
output.append('| 淘宝 | 部分 | 抓到 Top 商品 + 价格 |')
output.append('| **拼多多** | 受限 | 必须 App 端 + 第三方分析 |')
output.append('| 京东 | 全 | 排行榜 + 商品详情页双验证 |')
output.append('| 1688 | 全 | 工厂价清楚 |')
output.append('| 抖店 | 部分 | 抖音内嵌商品分批抓 |')
output.append('| 小红书商城 | 部分 | 笔记挂车 + 商品页双路径 |')
output.append('| 闲鱼 | 全 | 二手数据可见 |')
output.append('| 苏宁/得物 | 全 | 商品较少(非主战场) |')
output.append('| 抖音 | 部分 | 反爬拦了部分细节,Tavily+第三方补 |')
output.append('| 小红书 | 关键 | 笔记数 + 评论情感分析做透 |')
output.append('| B站/微博/知乎/快手 | 全 | Tavily + 公开榜单 |')
output.append('| 公众号 | 全 | 搜狗微信 + 第三方爬虫 |')
output.append('| 视频号/头条/贴吧 | 全 | 公开数据 |')
output.append('| Amazon/eBay | 全 | 确认无"假 ADB 灯"细分品类 |')
output.append('| TikTok Shop | 全 | 同类 LED 改装 2.09 万单/月 |')
output.append('| Reddit/X | 全 | 欧美车主的态度分裂 (没有装X) |')
output.append('')

output.append('## 关键合规警报 (来自法规深度)')
output.append('')
output.append('**一句话**: 当前"外挂小蓝灯"处于法规灰色地带 - 交警暂未明确执法但公安部已经点名"智驾神器"为打击对象。')
output.append('')
output.append('边界:')
output.append('- 不违法: 装一个不接车机的小蓝灯 (目前无明确条款)')
output.append('- 临界违法: 装蓝光 + 故意误导 → 可能构成"误导其他道路参与者"')
output.append('- 明确违法: 生产销售"智驾神器"等干扰产品 (公安部已点名)')
output.append('- 责任人: 现行执法案例 = 0, 但警告先例已多起')
output.append('')

output.append('## 评论解码 4 派 → 8 子态度 (来自评论解码)')
output.append('')
output.append('| 大类 | 子态度 | 占比 | 核心动机 |')
output.append('|------|--------|------|---------|')
output.append('| 真香 A | 装X炫耀 | ~13% | 让人看到我有智驾 |')
output.append('| 真香 B | 实用 | ~10% | 夜间提示 + 装饰 |')
output.append('| 中立 A | 无所谓 | ~13% | 装不装都行 |')
output.append('| 中立 B | 跟随 | ~10% | 大家都装 |')
output.append('| 中立 C | 从众 | ~7% | 看销量榜第几名 |')
output.append('| 批判 A | 道德 | ~5% | 装X不诚实 |')
output.append('| 批判 B | 安全 | ~5% | 误导他人出事 |')
output.append('| 批判 C | 审美 | ~5% | 太浮夸不喜欢 |')
output.append('')
output.append('**5 条最具代表性的评论原话**已经在 `评论解码.md` 末尾段,Eric 您要的"消费偏好奇怪"直接证据。')
output.append('')

output.append('## 准备进入 WHY 阶段 - 4 个候选方向')
output.append('')
output.append('基于已齐数据的 4 个 WHY 假设:')
output.append('')
output.append('1. **炫耀动机谱系** (Veblen商品 → 信号理论 → 制度性身份)')
output.append('   数据支撑: 真香A 13% 装X炫耀')
output.append('2. **替代品经济学** (从功能性 → 装饰性, 类似车贴/尾翼)')
output.append('   数据支撑: 价格带宽 ¥30-1388 = 50 倍跨度')
output.append('3. **制度性偷懒** (省去合规流程, 类似汽车拉花)')
output.append('   数据支撑: 小鹏 15377 名老车主众筹')
output.append('4. **AI 时代身份伪造** (花小钱假装"会 AI", 装X 的 AI 时代变种)')
output.append('   数据支撑: 评论原话 + 法规缺位 + 行业渗透 67%')
output.append('')
output.append('**Eric, 您挑哪个方向展开? 或者全部跑?**')
output.append('')

output.append('## 仍有的数据缺口 (透明声明)')
output.append('')
output.append('| # | 缺口 | 备注 |')
output.append('|---|------|------|')
output.append('| 1 | 拼多多 App 内完整数据 | 显式声明受限,已用第三方补 |')
output.append('| 2 | 抖音商城实时销量 | 内嵌商品 + 第三方分析已补 |')
output.append('| 3 | 小红书商城实时销量 | 笔记数 + 评论情感做透了 |')
output.append('| 4 | 实际"假灯车主"占比 | 无公开统计,靠评论 + 销量反推 |')
output.append('| 5 | 海外执法案例 | 暂无 |')
output.append('')

output.append('---')
output.append('')
output.append('*数据集成完成 · 6 份报告 + 1 索引已落地 · 等 Eric 决定方向。*')

(OUT_DIR / '2026-07-16-新能源车外挂小蓝灯-DATA-INDEX.md').write_text('\n'.join(output), encoding='utf-8')
print('OK')
print('Index:', OUT_DIR / '2026-07-16-新能源车外挂小蓝灯-DATA-INDEX.md')
print('size_bytes:', (OUT_DIR / '2026-07-16-新能源车外挂小蓝灯-DATA-INDEX.md').stat().st_size)
