"""Second-round calibration: clean up Week 1 'active' items in 21-day plan."""
import os

path = r'D:\B166ER-OpenClaw\workspace\obsidian-vault\50-外部接入\02-安逸集团知识库-20260720\安逸-个人21天融入计划.md'
with open(path, encoding='utf-8') as f:
    content = f.read()

v2_calibrations = [
    # Eric 自己录音 — 不要自动整理
    ('19:00 整理会议纪要', '[Eric 自行录音，集团禁止第三方整理]'),
    ('整理完整的会议纪要', '[Eric 自己会整理录音为笔记]'),
    # "完整画一遍'个人战略地图'" — 不是个人主导动作
    ('完整画一遍"个人战略地图"', '私下草稿"个人观察笔记"（不出门）'),
    # "列出个人战略地图 V2.0" 同上
    ('列出"个人战略地图 V2.0"', '私下更新"观察笔记"（不主动对外）'),
    # Week 1 阶段的"个人可贡献"还是有点不谨慎
    ('3 个"个人可贡献"的具体动作', '3 个不主动建议，但私下想清楚的问题'),
    # Day 4 的 notebook — 还是 Eric 自己的事
    ('准备笔记本（13 家酒店速记 + 关键术语速查）', '[Eric 自备] 笔记本（13 家酒店速记 + 关键术语速查）'),
    # "Day 5 全程参与" 保持
    # "22:00 前睡觉" 保持
]
n_changes = 0
log = []
for old, new in v2_calibrations:
    if old in content:
        content = content.replace(old, new, 1)  # 只替换第一个
        n_changes += 1
        log.append(f'  [OK] {old[:30]}... -> {new[:40]}...')
    else:
        log.append(f'  [--] {old[:30]}... not found')

# Update timestamp
old_marker = '18:32 GMT+8（互联补完 v2 + 21 天计划校准'
new_marker = '18:35 GMT+8（互联补完 v2 + 21 天计划二轮校准：Eric 自己录音整理）'
if old_marker in content:
    content = content.replace(old_marker, new_marker)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('=== V2 Calibration Report ===')
print(f'Changes: {n_changes} / {len(v2_calibrations)}')
for l in log:
    print(l)
