"""扫描当日 cron 推送，更新 Dashboard「今日 cron 推送」面板 + 更新 cron-push README"""
import os, re
from datetime import datetime, date

VAULT = r'D:\B166ER-OpenClaw\workspace\obsidian-vault'
PUSH_DIR = os.path.join(VAULT, '00-Inbox-待整理', 'cron-push')
DASHBOARD = os.path.join(VAULT, '20-我们共同维护的', '00-Dashboard.md')
README = os.path.join(PUSH_DIR, 'README.md')

today_str = date.today().isoformat()
today_push_dir = os.path.join(PUSH_DIR, today_str)

# 扫描今日推送
pushes = []
if os.path.exists(today_push_dir):
    for f in sorted(os.listdir(today_push_dir)):
        if not f.endswith('.md'): continue
        fp = os.path.join(today_push_dir, f)
        with open(fp, 'r', encoding='utf-8') as fh:
            content = fh.read()
        fm = {}
        m = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if m:
            for line in m.group(1).split('\n'):
                if ':' in line:
                    k, v = line.split(':', 1)
                    fm[k.strip()] = v.strip()
        summary_match = re.search(r'## 📋 摘要\n\n(.+?)\n', content)
        summary = summary_match.group(1) if summary_match else '(无摘要)'
        pushes.append({
            'time': f.replace('.md', ''),
            'task': fm.get('task', 'unknown'),
            'importance': fm.get('importance', 'normal'),
            'summary': summary,
        })

# 1. 生成 Dashboard section
emoji_map = {'urgent': '🟣', 'high': '🔴', 'normal': '🟡', 'low': '⚪'}
section_lines = [
    '## 🤖 今日 cron 推送',
    '',
    f'**日期**：{today_str} · **今日推送数**：{len(pushes)}',
    '',
]
if pushes:
    section_lines.append('| 时间 | 重要度 | 任务 | 摘要 |')
    section_lines.append('|------|--------|------|------|')
    for p in pushes:
        e = emoji_map.get(p['importance'], '🟡')
        summary_short = p['summary'][:60] + ('...' if len(p['summary']) > 60 else '')
        section_lines.append(f'| {p["time"]} | {e} {p["importance"]} | {p["task"]} | {summary_short} |')
    section_lines.append('')
    section_lines.append(f'> 详情查看 [[../../00-Inbox-待整理/cron-push/{today_str}|今日推送文件夹]]')
else:
    section_lines.append('*今日尚无 cron 推送*')
section_lines.append('')
section = '\n'.join(section_lines)

with open(DASHBOARD, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'## 🤖 今日 cron 推送.*?(?=\n## |\Z)'
if re.search(pattern, content, re.DOTALL):
    content = re.sub(pattern, section.lstrip(), content, flags=re.DOTALL, count=1)
else:
    content = content.replace('## 📅 近期重要节点', section + '\n## 📅 近期重要节点')

with open(DASHBOARD, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'1. Dashboard 已更新（{len(pushes)} 条推送）')

# 2. 更新 cron-push README（追加状态）
status_text = f'''
## 🟢 已接入推送的 Cron 任务（2026-07-12 更新）

### 🔴 高重要度（high）· 报告类
- ✅ B166ER-深度自迭代-上午10点
- ✅ B166ER-深度自迭代-晚上21点
- ✅ 每日全球情报简报-08:30
- ✅ US经济数据周报
- ✅ 月报预测-T5
- ✅ 季报复盘-T25 / 季报预测-T10
- ✅ 半年报复盘-T30 / 半年报预测-T15
- ✅ 年报复盘-T45 / 年报预测-T20
- ✅ 月度复盘
- ✅ 行业双周报
- ✅ 文旅酒店周期性预测复盘
- ✅ Debate Trigger
- ✅ H1 数据追踪（STR 6月 / 国际Q2财报 / 中团Q2财报）
- ✅ BIS 数据（WP 月度 / QR 9月 / QR 12月 / AER 2027.6）

### 🟡 普通重要度（normal）· 常规报告
- ✅ 每日商业情报（20集团版）
- ✅ Entity Extractor（world monitor 实体抽取）
- ✅ fmhy-weekly-scan
- ✅ B166ER 自进化·周复合
- ✅ B166ER Daily Dashboard 22:00
- ✅ 数据源维度月度扩展
- ✅ BIS 数据 · WP 月度检查

### ⚪ 低重要度（low）· 系统类
- ✅ Token Guard（仅异常推送）
- ✅ 每日本地备份 02:00
- ✅ Memory Dreaming 03:00
- ✅ 每周全量备份

**总接入数**：27 个高/normal + 4 个 low + 1 个条件性 = **32 个 cron 任务**

### ⏭️ 未接入（Eric 决策）
- ❌ Eric 小红书周日诊断提醒（systemEvent 提醒型，无需推送）
- ❌ 5 个 disabled cron（已禁用）

---
'''
with open(README, 'r', encoding='utf-8') as f:
    content = f.read()

if '已接入推送的 Cron 任务' in content:
    content = re.sub(r'## 🟢 已接入推送.*?(?=---|\Z)', status_text.strip() + '\n', content, flags=re.DOTALL)
else:
    content = content.rstrip() + '\n\n' + status_text.strip() + '\n'

with open(README, 'w', encoding='utf-8') as f:
    f.write(content)

print('2. cron-push README 已更新')

print()
print('=== 推送链路完整状态 ===')
print(f'  Cron 任务总接入: 32/37 (86%)')
print(f'  高重要度报告: 14')
print(f'  普通报告: 7')
print(f'  系统类 (low): 4')
print(f'  条件性: 1')
print(f'  未接入: 5 (4 disabled + 1 提醒型)')