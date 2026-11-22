"""
1. 检查 cron 数据库，列出所有任务和它们的 OBSIDIAN-PUSH 状态
2. 重启 Obsidian
3. 打开 Dashboard
4. 截图
"""
import os, subprocess, time, urllib.parse, json, re

OBSIDIAN = r'D:\obsidian\Obsidian.exe'
VAULT = r'D:\B166ER-OpenClaw\workspace\obsidian-vault'
CRON_DB = r'C:\Users\ericz\.openclaw\state\openclaw.sqlite'

# 1. 直接读 cron 数据库
print('=' * 60)
print('1. 检查所有 cron 任务接入状态')
print('=' * 60)

import sqlite3
conn = sqlite3.connect(CRON_DB)
cur = conn.cursor()
cur.execute('SELECT id, name, enabled, description, next_run_at_ms FROM jobs ORDER BY id')
jobs = cur.fetchall()
conn.close()

obsidian_jobs = []
non_obsidian_jobs = []
for job_id, name, enabled, desc, next_run in jobs:
    desc = desc or ''
    is_obsidian = '[OBSIDIAN-PUSH' in desc or 'OBSIDIAN-PUSH' in name.upper()
    status = '🟢 ON' if enabled else '⚪ OFF'
    push_marker = '✅' if is_obsidian else '❌'
    line = f'  {push_marker} {status} {name}'
    print(line)
    if is_obsidian:
        obsidian_jobs.append(name)
    else:
        non_obsidian_jobs.append(name)

print()
print(f'已接入 Obsidian 推送: {len(obsidian_jobs)}/{len(jobs)}')

if non_obsidian_jobs:
    print()
    print('未接入的任务:')
    for name in non_obsidian_jobs:
        print(f'  - {name}')

# 2. 重启 Obsidian
print()
print('=' * 60)
print('2. 重启 Obsidian')
print('=' * 60)

# 杀进程
subprocess.run('powershell -NoProfile -Command "Stop-Process -Name Obsidian -Force -ErrorAction SilentlyContinue"',
               capture_output=True, encoding='gbk', errors='ignore', timeout=10)
time.sleep(3)

# 删 lockfile
for lf in [r'C:\Users\ericz\AppData\Roaming\obsidian\lockfile',
           r'C:\Users\ericz\AppData\Roaming\Obsidian\lockfile']:
    if os.path.exists(lf):
        os.remove(lf)
        print(f'  删 lockfile: {lf}')

# 启动
subprocess.Popen([OBSIDIAN])
print('  Obsidian 已启动')
time.sleep(8)

# 3. 打开 Dashboard
print()
print('=' * 60)
print('3. 打开 Dashboard')
print('=' * 60)

uri = 'obsidian://open?path=' + urllib.parse.quote(VAULT + r'\20-我们共同维护的\00-Dashboard.md')
subprocess.run(['cmd', '/c', 'start', '', uri], shell=False, timeout=10)
time.sleep(3)

# 4. 切前台 + 截图
print()
print('=' * 60)
print('4. 切前台 + 截图')
print('=' * 60)

ps_focus = '''powershell -NoProfile -Command "
Add-Type @\\"
using System;
using System.Runtime.InteropServices;
public class W {
  [DllImport(\\"user32.dll\\")] public static extern bool SetForegroundWindow(IntPtr hWnd);
}
\\"@
$proc = Get-Process Obsidian | Where-Object MainWindowTitle | Select-Object -First 1
[W]::SetForegroundWindow($proc.MainWindowHandle) | Out-Null
Write-Output $proc.Id $proc.MainWindowTitle
"'''
r = subprocess.run(ps_focus, capture_output=True, encoding='gbk', errors='ignore', timeout=15)
print('  focus:', r.stdout.strip())

time.sleep(2)

ps_ss = 'powershell -NoProfile -Command "Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing; $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds; $bmp = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height; $gfx = [System.Drawing.Graphics]::FromImage($bmp); $gfx.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size); $bmp.Save(\\"D:\\B166ER-OpenClaw\\workspace\\obsidian-vault\\screenshot-final-v3.png\\"); Write-Output OK"'
subprocess.run(ps_ss, capture_output=True, encoding='gbk', errors='ignore', timeout=15)

ss = os.path.join(VAULT, 'screenshot-final-v3.png')
if os.path.exists(ss):
    print(f'  截图: {os.path.getsize(ss):,} B')
else:
    print('  截图: 失败')

print()
print('=' * 60)
print('完成')
print('=' * 60)