#!/usr/bin/env python3
"""full_repair.py - 完整修复：SQLite + Skill system
Eric 2026-09-06 23:42 选 A：Step 1-3 全做
"""
import os
import sqlite3
import shutil
import subprocess
import json
from datetime import datetime

USER = os.environ.get('USERPROFILE')
TS = datetime.now().strftime('%Y%m%d_%H%M%S')

print('=' * 60)
print('完整修复 (Step 1-3) - 2026-09-06 23:42')
print('=' * 60)

# ============================================
# Step 0: 杀所有 node 进程 (gateway + watcher)
# ============================================
print('\n[Step 0] 杀所有 node 进程...')
result = subprocess.run(['powershell', '-NoProfile', '-Command',
    'Get-Process -Name node -ErrorAction SilentlyContinue | ForEach-Object { Write-Host "kill $($_.Id)"; Stop-Process -Id $_.Id -Force }'],
    capture_output=True, text=True, timeout=20)
print(f'  杀进程输出: {result.stdout.strip()[:200]}')

# 等 5 秒
import time
time.sleep(5)

# 确认进程已停
result = subprocess.run(['powershell', '-NoProfile', '-Command',
    '(Get-Process -Name node -ErrorAction SilentlyContinue).Count'],
    capture_output=True, text=True)
remaining = result.stdout.strip()
print(f'  剩余 node 进程: {remaining}')

# ============================================
# Step 1: SQLite 完整重建 + auto_checkpoint scheduled task
# ============================================
print('\n[Step 1] SQLite 完整重建...')
DBS = [
    os.path.join(USER, '.openclaw', 'state', 'openclaw.sqlite'),
    os.path.join(USER, '.openclaw', 'agents', 'main', 'agent', 'openclaw-agent.sqlite'),
    os.path.join(USER, '.openclaw', 'agents', 'anyi', 'agent', 'openclaw-agent.sqlite'),
    os.path.join(USER, '.openclaw', 'agents', 'coder', 'agent', 'openclaw-agent.sqlite'),
]

for db in DBS:
    if not os.path.exists(db):
        continue
    name = os.path.relpath(db, USER)
    print(f'\n  → {name}')

    # 备份
    bak = f'{db}.rebuild-{TS}'
    shutil.copy2(db, bak)
    for s in ['-wal', '-shm']:
        if os.path.exists(db + s):
            shutil.copy2(db + s, bak + s)
            try:
                os.remove(db + s)
            except:
                pass

    # dump
    dump = f'{db}.dump-{TS}.sql'
    try:
        src = sqlite3.connect(db, timeout=10)
        with open(dump, 'w', encoding='utf-8') as f:
            for line in src.iterdump():
                f.write(f'{line}\n')
        src.close()
        print(f'    dump: {os.path.getsize(dump)/1e6:.1f} MB')
    except Exception as e:
        print(f'    ❌ dump 失败: {e}')
        continue

    # 删原 DB
    try:
        os.remove(db)
    except Exception as e:
        print(f'    ⚠️ 删 DB 失败: {e}')

    # 重建
    try:
        new = sqlite3.connect(db)
        with open(dump, 'r', encoding='utf-8') as f:
            new.executescript(f.read())
        new.execute('PRAGMA wal_checkpoint(TRUNCATE);')
        new.execute('VACUUM;')  # 真空回收
        new.close()
        new_size = os.path.getsize(db) / 1e6
        verify = sqlite3.connect(db, timeout=5).execute('PRAGMA integrity_check;').fetchone()[0]
        print(f'    ✅ 重建: {new_size:.1f} MB, integrity={verify}')
    except Exception as e:
        print(f'    ❌ 重建失败: {e}')
    finally:
        if os.path.exists(dump):
            os.remove(dump)

# ============================================
# Step 2: 装 scheduled task (auto_checkpoint)
# ============================================
print('\n[Step 2] 装 auto_checkpoint scheduled task...')
workspace = r'D:\B166ER-OpenClaw\workspace'
script_path = os.path.join(workspace, 'toolbox', 'auto_checkpoint.py')
task_name = 'OpenClaw AutoCheckpoint'
ps_cmd = f'''
$action = New-ScheduledTaskAction -Execute "python" -Argument "{script_path}"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName "{task_name}" -Action $action -Trigger $trigger -Settings $settings -Force | Out-String
'''
result = subprocess.run(['powershell', '-NoProfile', '-Command', ps_cmd],
    capture_output=True, text=True, timeout=30)
print(f'  注册结果: {result.stdout.strip()[:200]}')
if result.returncode != 0:
    print(f'  错误: {result.stderr.strip()[:200]}')

# 立即跑一次
print('\n  立即跑一次 auto_checkpoint.py...')
subprocess.run(['python', script_path], timeout=30)

# ============================================
# Step 3a: 修 9 个活的 SKILL.md description
# ============================================
print('\n[Step 3a] 修 9 个 SKILL.md description...')
SKILLS_NEEDING_DESC = [
    ('~/.openclaw/skills/aesthetic-judgment/SKILL.md', 'aesthetic-judgment',
     'aesthetic-judgment: 评估设计、文案、视觉作品的美学质量（形式/意境/气韵/留白等），用于 Eric 个人审美决策'),
    ('~/.openclaw/skills/douyin-auto/SKILL.md', 'douyin-auto',
     'douyin-auto: 抖音本地生活+新媒体自动化运营，1.2亿 GMV 闭环，Eric 在中旅21年率先提出'),
    ('~/.openclaw/skills/pricing-strategy/SKILL.md', 'pricing-strategy',
     'pricing-strategy: 收益管理 + 动态定价 + 渠道价格策略（酒店/RFP/电商通用）'),
    ('workspace/skills/cost-governor/SKILL.md', 'cost-governor',
     'cost-governor: 项目成本管控 + 现金流预警 + 投资回收期跟踪'),
    ('workspace/skills/hotel-feasibility-report/SKILL.md', 'hotel-feasibility-report',
     'hotel-feasibility-report: 酒店项目可行性研究报告（含 IRR/RevPAR/OCC 五维分析）'),
    ('workspace/skills/music-aesthetic-judgment/SKILL.md', 'music-aesthetic-judgment',
     'music-aesthetic-judgment: Eric 音乐收藏美学分析（542 首歌曲 5 维审美判断）'),
    ('workspace/skills/skill-vetter/SKILL.md', 'skill-vetter',
     'skill-vetter: OpenClaw skill 质量审核（description/frontmatter/completeness 检查）'),
]

for path_template, name, desc in SKILLS_NEEDING_DESC:
    path = path_template.replace('~', USER).replace('workspace/', workspace + '\\')
    if not os.path.exists(path):
        print(f'  ⚠️ {path} 不存在')
        continue
    # 读前 5 行
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # 检查是否已有 description
    if content.startswith('---') and 'description:' in content[:300]:
        print(f'  ✓ {name}: 已有 description')
        continue
    # 注入 frontmatter
    new_content = f'---\ndescription: {desc}\n---\n\n' + content
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'  ✅ {name}: 已加 description')

# ============================================
# Step 3b: 解决 6 个 skill 冲突
# ============================================
print('\n[Step 3b] 解决 skill 冲突...')
# 默认策略: 保留 workspace/skills 下的 (新版本), 删除 ~/.openclaw/skills 下的 (旧版本)
# 但 Eric 没拍板，先列出冲突让 Eric 看

CONFLICTS = [
    ('chrome-live-session',
     '~/.openclaw/skills/chrome-live-session',
     '~/.openclaw/skills/chrome-for-agents/skills/chrome-live-session',
     '保留 ~/.openclaw/skills/chrome-live-session (顶层), 删 chrome-for-agents 下重复'),
    ('web-access',
     '~/.openclaw/skills/web-access',
     '~/.openclaw/skills/web-access-new',
     '保留 web-access-new (新版本), 重命名 web-access 为 web-access-old 或删除'),
    ('agent-reach',
     '~/.openclaw/skills/agent-reach',
     'workspace/.agents/skills/agent-reach',
     '保留 workspace 下 (项目级), 删 ~/.openclaw 下 (全局旧版)'),
    ('document-pdf',
     'workspace/.agents/skills/document-pdf',
     'workspace/skills/document-pdf',
     '保留 workspace/.agents/skills 下 (新版本), 删 workspace/skills 下旧版'),
    ('scrapling-official',
     'workspace/.agents/skills/scrapling-official',
     'workspace/skills/scrapling-official',
     '保留 workspace/.agents/skills 下 (新版本), 删 workspace/skills 下旧版'),
    ('business-intelligence',
     'workspace/.agents/skills/business-intelligence',
     'workspace/skills/business-intelligence',
     '保留 workspace/.agents/skills 下 (新版本), 删 workspace/skills 下旧版'),
]

for name, p1, p2, action in CONFLICTS:
    print(f'  [{name}]')
    print(f'    A: {p1}')
    print(f'    B: {p2}')
    print(f'    建议: {action}')

# ============================================
# Step 4: 启动 gateway
# ============================================
print('\n[Step 4] 等 gateway 自动重启...')
time.sleep(10)
result = subprocess.run(['powershell', '-NoProfile', '-Command',
    '(Get-Process -Name node -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match "openclaw" }).Id'],
    capture_output=True, text=True)
pids = [int(p.strip()) for p in result.stdout.strip().split('\n') if p.strip().isdigit()]
print(f'  当前 gateway PID: {pids}')

if not pids:
    print('  gateway 没自动重启，尝试手动启动...')
    # 找 openclaw CLI
    cli_path = os.path.join(USER, 'AppData', 'Roaming', 'npm', 'openclaw.cmd')
    if os.path.exists(cli_path):
        subprocess.Popen(['start', 'cmd', '/c', cli_path, 'gateway', 'run'],
                       shell=True)

print('\n' + '=' * 60)
print('Step 1-3 已执行')
print('=' * 60)
print('\n下一步:')
print('1. Eric 测试发文字消息看是否还有 malformed')
print('2. 如果冲突 skill 默认方案可接受，我执行删除')
print('3. 观察 30 分钟看 WAL 是否稳定 (auto_checkpoint 已装)')