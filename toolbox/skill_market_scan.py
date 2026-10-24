# -*- coding: utf-8 -*-
r"""
B166ER-技能市场扫描 v1.3 —— 确定性扫描器（替代 agentTurn，根治 timeout）

根因与修复对照：
  A. clawhub 是 .ps1 → 用 npm 的 clawhub.cmd shim
  B. clawhub search 输出是纯文本（非 JSON）→ 正则解析 "name  desc  (score)"
  C. 泛查询词 + 大 limit → 向量检索卡 20s+ → 只用 2 个精准词 / limit 5 / 15s 硬超时
  D. 任务原 cd 到 C 盘空壳目录 → 写死真实工作区 D:\B166ER-OpenClaw\workspace
  E. **Windows 管道死锁**：.cmd→cmd.exe→node.exe 孙进程持有 stdout 管道，
     subprocess.communicate() 超时后仍永久阻塞 → 改用「临时文件承接 stdout +
     taskkill /T 杀整棵进程树」，保证调用必然在 timeout 内返回
"""
import sys, os, re, json, subprocess, tempfile, time, datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WS = Path(r'D:\B166ER-OpenClaw\workspace')
SKILLS = WS / 'skills'
MEMO = WS / 'memory' / 'B166ER-skill-upgrade-checklist.md'
SHIM = Path(os.environ.get('APPDATA', '')) / 'npm' / 'clawhub.cmd'
LOG = WS / '.tmp' / 'skill_scan_last.json'

TOTAL_BUDGET = 200
CLAWHUB_TIMEOUT = 15
GIT_TIMEOUT = 20
MAX_GIT = 8
QUERIES = ['hotel', 'travel']

t0 = time.time()
def left():
    return TOTAL_BUDGET - (time.time() - t0)

NEWPROC = getattr(subprocess, 'CREATE_NEW_PROCESS_GROUP', 0)

def kill_tree(pid):
    subprocess.run(['taskkill', '/PID', str(pid), '/T', '/F'],
                   capture_output=True, shell=False)

def run(cmd, timeout):
    """文件承接 stdout + 超时杀整棵进程树 —— 绝不因孙进程持句柄而死锁"""
    try:
        with tempfile.TemporaryFile('w+b') as tf:
            try:
                p = subprocess.Popen(cmd, stdout=tf, stderr=subprocess.STDOUT,
                                     stdin=subprocess.DEVNULL,
                                     creationflags=NEWPROC)
            except Exception as e:
                return -2, '', str(e)
            try:
                p.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                kill_tree(p.pid)
                try:
                    p.wait(timeout=8)
                except Exception:
                    pass
                return -1, '', 'TIMEOUT'
            tf.seek(0)
            out = tf.read().decode('utf-8', 'replace')
            return p.returncode, out, ''
    except Exception as e:
        return -2, '', str(e)

LINE_RE = re.compile(r'^(?P<name>[^\s]+)\s{2,}(?P<desc>.*?)\s{2,}\((?P<score>[\d.]+)\)\s*$')

def parse_market(text):
    out, seen = [], set()
    for line in (text or '').splitlines():
        line = line.rstrip()
        if not line or line.startswith('-'):
            continue
        m = LINE_RE.match(line)
        if m and m.group('name') not in seen:
            seen.add(m.group('name'))
            out.append({'name': m.group('name'),
                        'desc': m.group('desc').strip()[:100],
                        'score': m.group('score')})
    return out

# ---------- 1. 市场扫描 ----------
market, cli_ok, q_stat = [], False, []
if SHIM.exists():
    for q in QUERIES:
        if left() < 45:
            break
        st = time.time()
        rc, o, e = run([str(SHIM), 'search', q, '--limit', '5'], CLAWHUB_TIMEOUT)
        dt = round(time.time() - st, 1)
        q_stat.append({'q': q, 'rc': rc, 'sec': dt})
        if rc == 0:
            cli_ok = True
            for it in parse_market(o):
                if it['name'] not in {m['name'] for m in market}:
                    market.append(it)
else:
    print('!! clawhub.cmd 不存在：', SHIM)

# ---------- 2. 本地清单 ----------
local_dirs, local_skill_md = [], set()
if SKILLS.exists():
    for d in SKILLS.iterdir():
        if d.is_dir() and not d.name.startswith('.'):
            local_dirs.append(d.name)
            if (d / 'SKILL.md').exists():
                local_skill_md.add(d.name)
local_dirs.sort()
local_names = set(local_dirs)
new_market = [m for m in market if m['name'] not in local_names]

# ---------- 3. git 更新（三分类，失败也给出可行动原因）----------
# 2026-10-25 修正：旧版 `git pull --ff-only` 失败只报 err，无行动价值。
#   evolver: main...origin/main [ahead 115, behind 149]  → 分叉，--ff-only 必然失败
#   wewrite: fetching ref refs/tags/v3.6.1 failed: reference already exists → 标签冲突
# 新版：fetch --no-tags（绕开标签冲突）→ 读 ahead/behind → 分类
#   ① uptodate  已是最新
#   ② updated  远端有新提交且可快进 → merge --ff-only（安全自动完成）
#   ③ diverged 本地有未推提交且远端也有新提交 → 需人工 rebase/merge，脚本绝不自动改写
#   ④ failed   网络/权限/其它 → 留待下轮
git_updated, git_diverged, git_failed, git_uptodate = [], [], [], []
cands = [d for d in (SKILLS.iterdir() if SKILLS.exists() else [])
         if d.is_dir() and (d / '.git').exists()][:MAX_GIT]
for d in cands:
    if left() < 30:
        break
    # 3.1 fetch（--no-tags 避免本地/远端同名标签冲突）
    rc, o, e = run(['git', '-C', str(d), 'fetch', '--prune', '--no-tags', 'origin'], GIT_TIMEOUT)
    if rc == -1:
        git_failed.append('{}(timeout)'.format(d.name))
        continue
    if rc != 0:
        reason = 'timeout' if rc == -1 else ('missing' if rc == -2 else
                  (e.strip().splitlines()[-1][:40] if e.strip() else 'err'))
        git_failed.append('{}({})'.format(d.name, reason))
        continue
    # 3.2 读 ahead/behind
    rc2, o2, e2 = run(['git', '-C', str(d), 'rev-list', '--left-right', '--count', 'HEAD...@{u}'], 60)
    ahead = behind = None
    if rc2 == 0:
        parts = (o2 or '').split()
        if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
            ahead, behind = int(parts[0]), int(parts[1])
    if ahead is None:
        git_failed.append('{}(no-upstream)'.format(d.name))
        continue
    if behind == 0:
        git_uptodate.append(d.name)
        continue
    if ahead > 0:
        # 分叉：本地有未推提交，绝不自动改写历史
        git_diverged.append('{}(ahead {},behind {})'.format(d.name, ahead, behind))
        continue
    # 3.3 仅在可快进时自动 merge
    rc3, o3, e3 = run(['git', '-C', str(d), 'merge', '--ff-only', '@{u}'], GIT_TIMEOUT)
    if rc3 == 0:
        git_updated.append(d.name)
    else:
        reason = 'timeout' if rc3 == -1 else (
            (e3.strip().splitlines()[-1][:40] if (e3 or '').strip() else 'err'))
        git_failed.append('{}({})'.format(d.name, reason))

# ---------- 4. 写清单 + 结构化日志 ----------
MEMO.parent.mkdir(parents=True, exist_ok=True)
ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
q_line = ', '.join('{}={}s(rc{})'.format(x['q'], x['sec'], x['rc']) for x in q_stat)
L = ['\n---\n\n## 技能市场扫描 · {}\n'.format(ts),
     '- 用时 {:.0f}s / 预算 {}s（clawhub CLI {}）\n'.format(
         time.time() - t0, TOTAL_BUDGET, '可用' if cli_ok else '不可用'),
     '- 检索词与耗时：' + q_line + '\n',
     '- 市场去重后 {} 条；本地技能 {} 个（SKILL.md {} 个）\n'.format(
         len(market), len(local_dirs), len(local_skill_md)),
     '- 市场有本地无：{} 个\n'.format(len(new_market)),
     '\n### 新技能候选\n']
if new_market:
    for m in new_market:
        L.append('- **{}** (score {}) — {}\n'.format(m['name'], m['score'], m['desc']))
else:
    L.append('- 无（市场返回项均已安装）\n')
L.append('\n### git 更新结果\n- 已更新 {} 个：{}\n'.format(
    len(git_updated), ', '.join(git_updated) if git_updated else '—'))
L.append('- 已是最新 {} 个：{}\n'.format(
    len(git_uptodate), ', '.join(git_uptodate) if git_uptodate else '—'))
L.append('- 需人工处理（分支分叉，脚本不自动改写）{} 个：{}\n'.format(
    len(git_diverged), ', '.join(git_diverged) if git_diverged else '—'))
L.append('- 失败（网络/权限等）{} 个：{}\n'.format(
    len(git_failed), ', '.join(git_failed) if git_failed else '—'))
with open(MEMO, 'a', encoding='utf-8') as f:
    f.writelines(L)

result = {'ts': ts, 'sec': round(time.time() - t0, 1), 'cli_ok': cli_ok,
          'queries': q_stat, 'market_n': len(market), 'local_n': len(local_dirs),
          'skill_md_n': len(local_skill_md), 'new': new_market,
          'git_ok': git_updated, 'git_uptodate': git_uptodate,
          'git_diverged': git_diverged, 'git_fail': git_failed}
LOG.parent.mkdir(parents=True, exist_ok=True)
LOG.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')

print('=== B166ER 技能市场扫描完成 ===')
print('用时 {}s / 预算 {}s｜clawhub CLI {}'.format(
    result['sec'], TOTAL_BUDGET, '可用' if cli_ok else '不可用'))
print('查询耗时：' + ' | '.join('{}={}s'.format(x['q'], x['sec']) for x in q_stat))
print('市场去重 {} 条｜本地技能 {} 个（SKILL.md {}）'.format(
    len(market), len(local_dirs), len(local_skill_md)))
print('新技能候选：' + (', '.join(m['name'] for m in new_market) if new_market else '无'))
print('git 更新: 已更新 {}｜已最新 {}｜需人工(分叉) {}｜失败 {}'.format(
    len(git_updated), len(git_uptodate), len(git_diverged), len(git_failed)))
print('清单：{}｜日志：{}'.format(MEMO, LOG))
