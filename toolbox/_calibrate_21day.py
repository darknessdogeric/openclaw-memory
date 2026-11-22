"""Calibrate the 21-day plan from '主导/主动设计' to '观察+收集' tone."""
import os

path = r'D:\B166ER-OpenClaw\workspace\obsidian-vault\50-外部接入\02-安逸集团知识库-20260720\安逸-个人21天融入计划.md'
with open(path, encoding='utf-8') as f:
    content = f.read()

calibrations = [
    ('主导某项改革方案设计', '协助某项改革方案讨论'),
    ('主导某项改革落地', '协助某项改革推进'),
    ('主持 1 次跨部门协调会议', '参加 1 次跨部门协调会议'),
    ('AHL / 数字化建议', 'AHL/数字化内部素材（暂不提案）'),
    ('产业发展部年度工作计划 V1.0', '产业发展部年度工作计划 V0.5 草稿（主动权在领导）'),
    ('个人产业洞察', '个人产业观察笔记'),
    ('完成 13+ 家酒店走访（每家 1 天实地看）', '接触部分核心酒店（节奏按合规边界）'),
    ('完成集团数字化现状全景摸底', '了解集团数字化现状（信息收集为主）'),
    ('1 次重大会议发言（不主动请缨，等待机会）', '1 次会议记笔记（不主动发言，等待合适机会）'),
    ('5 个主动可贡献的具体动作', '5 个可观察的问题（注意不出头）'),
]
n_changes = 0
log = []
for old, new in calibrations:
    if old in content:
        content = content.replace(old, new)
        n_changes += 1
        log.append(f'  [CHANGE] {old[:30]}... -> {new[:30]}...')

# Update last_modified
old_marker = '2026-07-20 18:30 GMT+8（互联补完 v2 — Eric 架构指令）'
new_marker = '2026-07-20 18:32 GMT+8（互联补完 v2 + 21 天计划校准：观察+收集而非主导）'
if old_marker in content:
    content = content.replace(old_marker, new_marker)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'=== Calibration Report ===')
print(f'Changes applied: {n_changes} / {len(calibrations)}')
for l in log:
    print(l)
