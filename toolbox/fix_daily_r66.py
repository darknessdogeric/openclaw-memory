"""Fix daily note R66 line 444 - precise replacement"""
PATH = 'D:/B166ER-OpenClaw/workspace/memory/2026-08-18.md'

old_line = '| 1 | **平安会议中的"钟部长"**: 会议中介绍为"运营部的钟部长...员工差旅这块的" | 与 MEMORY.md v3.1 "产业发展部 4 人组 = 肖润雨(酒店运营平台岗)" 存在偏差。可能为:①"钟部长"= 肖润雨(口音误听)②"钟部长"= 蒋抒伶(运营管理岗)③ 其他部门同事 ④ Eric 8/13 修正后仍不准确。**不擅自修正,等 Eric 确认** |'

new_line = '| 1 | **平安会议中的"钟部长"**: 会议中介绍为"运营部的钟部长...员工差旅这块的" | ✅ **已澄清 (2026-08-18 19:06 Eric 确认)**: "钟部长" = **钟华**,安逸集团**运管部负责人**("也就是我们所说的大大运营中心")。**非产业发展部 4 人组成员**,属集团原有部门,负责日常运营/TMC/RFP 等 |'

with open(PATH, 'r', encoding='utf-8') as f:
    content = f.read()

if old_line in content:
    content = content.replace(old_line, new_line)
    print('[OK] R66 偏差第 1 条已替换')
else:
    print('[X] NOT FOUND')

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'[OK] Saved')