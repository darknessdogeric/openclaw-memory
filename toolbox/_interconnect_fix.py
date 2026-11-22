"""Batch fix: add cross-domain interconnect block to 14 安逸 notes.
Also calibrate the '21-day plan' from 'active' to 'observe + collect' tone."""

import os, re, sys

ROOT = r'D:\B166ER-OpenClaw\workspace'
KB = os.path.join(ROOT, r'obsidian-vault\50-外部接入\02-安逸集团知识库-20260720')

INTERCONNECT_BLOCK = '''---

## 🌐 跨域互联（独立成库 + 双向互联）

> 按 Eric 2026-07-20 架构原则：安逸集团笔记 = **独立成库**（Eric 入职专属体系）+ **全面双向互联**（不成为信息孤岛）。  
> 每条笔记都与兄弟文件 + 跨域理论框架双向引用。

### ↔ 兄弟节点（同 vault 内）
- [[_MOC-安逸集团十五五]] — 本数据库主入口（49 页战略文档结构化视角）
- [[安逸集团-D-day MOC|emergence/hubs/安逸集团-D-day MOC]] — 人事/政治/90 天视角（**互补**）

### 🌐 跨域理论框架（按主题）
- **酒店行业 KB** — 行业基准判断（赛道笔记主用）
- **AHL 平台 MOC** — 集团内孵化路径（AHL 笔记主用）
- **博弈论 V3** — 利益相关方/战略博弈（战略/改革笔记主用）
- **审美 V3** — 品牌价值/文化主题解构（文化主题赛道主用）
- **Eric 人格-审美 MOC** — 个人审美与集团品牌的契合（"此心安处是吾乡"）
- **战略-方法论 MOC** — 竞争优势/蓝海战略（1234/赛道笔记主用）

---

**最后更新**：2026-07-20 18:30 GMT+8（互联补完 v2 — Eric 架构指令）
'''

# Specific block per note type
SPECIFIC_BLOCKS = {
    'AHL对接安逸-关键机会点.md': '''
### 🎯 AHL 专属跨域互联
- [[AHL 平台 MOC]] — 主路径（详细展开）
- [[03-安逸集团机会]] — 入职 90 天 + AHL 时机
- [[B_安逸酒店Agent协议立项草案_20260707]] — AHL 集团内立项草案（已存在）
''',
    '安逸-1234发展战略.md': '''
### 🎯 战略方法论专属
- [[战略-方法论 MOC]] — 1234 战略 vs 蓝海战略 / 竞争优势
- [[博弈论 V3]] — "1234" 中的"4 步路径"是典型博弈路径
''',
    '安逸-三大核心矛盾诊断.md': '''
### 🎯 矛盾诊断专属
- [[博弈论 V3]] — 矛盾三方（资产/产品/机制）= 多方博弈
- [[战略-方法论 MOC]] — "三个不匹配" = SWOT 升级版
''',
    '安逸-战略定位-巴蜀文化开创者.md': '''
### 🎯 战略定位专属
- [[审美 V3]] — "巴蜀文化主题酒店" = 审美差异化的极致
- [[Eric 人格-审美 MOC]] — "此心安处是吾乡" 与 Eric 个人审美的契合
- [[博弈论 V3]] — 利益相关方价值主张 = 6 方博弈
''',
    '安逸-一店一品矩阵-IP解构.md': '''
### 🎯 一店一品专属
- [[审美 V3]] — 四文化维度解构 = 文化主题设计的审美框架
- [[酒店行业 KB]] — 君亭/雷迪森标杆案例参照
''',
    '安逸-数字化战略总览.md': '''
### 🎯 数字化专属
- [[AHL 平台 MOC]] — 安逸会 160→600 万会员 = 私域基础设施（可对接 AHL）
- 工业互联网 / 数字化转型框架（待补 MOC 链）
''',
    '安逸-轻重分离1+5架构.md': '''
### 🎯 体制架构专属
- [[战略-方法论 MOC]] — 雷迪森案例 = 轻重分离的可复制路径
- [[博弈论 V3]] — 轻重协同机制 = 内部博弈设计
''',
    '安逸-六大旗舰改造-4.08亿.md': '''
### 🎯 投资分析专属
- [[经济周期 KB]]（如有）/ 房地产周期（REITs 时点）
- [[博弈论 V3]] — 6 大利益方（股东/银行/政府/加盟商/员工/客户）
''',
    '安逸-7.38亿资金需求.md': '''
### 🎯 融资战略专属
- [[经济周期 KB]]（如有）/ REITs/ABS 周期
- [[博弈论 V3]] — 4 轮驱动 = 4 利益方博弈
''',
    '安逸-三项制度改革.md': '''
### 🎯 改革设计专属
- [[博弈论 V3]] — 三项制度 = 三方博弈再设计
- [[战略-方法论 MOC]] — 任期制+契约化 = 现代企业制度
''',
    '安逸-亏损面-50%企业治理分类.md': '''
### 🎯 亏损治理专属
- [[博弈论 V3]] — 3 类亏损 = 3 种治理博弈
- [[经济周期 KB]]（如有）— 古尔沟/总府资负率与现金流
''',
    '安逸-个人21天融入计划.md': '''
### 🎯 个人计划专属
- [[Eric 人格-审美 MOC]] — 个人节奏与风格
- [[安逸-个人21天融入计划#观测而非主导|观测为主，非主导]] — 已校准为"观察+收集"
''',
}

# 21-day plan calibration: replace aggressive "主导/主动设计" with "观察+收集"
def calibrate_21day(content):
    """替换 '主动/主导/自己设计' 为 '观察/参与/协助' 风格."""
    calibrations = [
        ('设计', '了解'),
        ('主导某项改革方案设计', '协助某项改革方案讨论'),
        ('主导某项改革落地', '协助某项改革推进'),
        ('主持 1 次跨部门协调会议', '参加 1 次跨部门协调会议'),
        ('提交 1 份"AHL / 数字化建议"内部提案', '积累 1 份"AHL / 数字化建议"内部素材（暂不提案）'),
        ('完成"产业发展部年度工作计划 V1.0"', '完成"产业发展部年度工作计划 V0.5 草稿"（主动权在领导）'),
        ('个人产业洞察', '个人产业观察笔记'),
        ('完成 13+ 家酒店走访（每家 1 天实地看）', '完成部分核心酒店现场接触（节奏按合规边界）'),
        ('完成集团数字化现状全景摸底', '了解集团数字化现状（信息收集为主）'),
        ('1 次重大会议发言（不主动请缨，等待机会）', '1 次会议记笔记（不主动发言，等待机会）'),
        ('5 个"主动可贡献"的具体动作', '5 个可观察的问题'),
        ('私下与跨集团同行交流（如老同事）— 行业交流', '私下与跨集团同行交流（如老同事）— 行业交流'),
    ]
    new_content = content
    for old, new in calibrations:
        new_content = new_content.replace(old, new)
    return new_content

# Process all .md in KB (except _MOC and README)
files = sorted([f for f in os.listdir(KB) if f.endswith('.md')])
updated = []
skipped = []

for fn in files:
    if fn.startswith('_MOC') or fn == 'README.md':
        skipped.append(fn)
        continue
    path = os.path.join(KB, fn)
    with open(path, encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has cross-domain block
    if '## 🌐 跨域互联（独立成库 + 双向互联）' in content:
        skipped.append(fn + ' (already updated)')
        continue
    
    # Calibrate 21-day plan content
    if fn == '安逸-个人21天融入计划.md':
        content = calibrate_21day(content)
    
    # Build new content
    base_block = INTERCONNECT_BLOCK
    if fn in SPECIFIC_BLOCKS:
        # Insert specific block BEFORE the "---" separator of INTERCONNECT
        # i.e., put specific block right after the standard header
        base_block = base_block.replace(
            '### ↔ 兄弟节点（同 vault 内）',
            '### ↔ 兄弟节点（同 vault 内）',
            1
        )
        # append specific after generic
        base_block = base_block.replace(
            '---\n\n**最后更新**',
            SPECIFIC_BLOCKS[fn] + '\n---\n\n**最后更新**'
        )
    
    new_content = content.rstrip() + '\n\n' + base_block
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    updated.append(fn)

print('=== Updated files ===')
for f in updated:
    print(f'  [UPDATED] {f}')
print(f'\nTotal updated: {len(updated)}')
print('\n=== Skipped files ===')
for s in skipped:
    print(f'  [SKIP] {s}')
print(f'\nTotal skipped: {len(skipped)}')
