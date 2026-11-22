# -*- coding: utf-8 -*-
"""Verify HEARTBEAT.md integrity post HB #932 append."""
with open(r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md", 'r', encoding='utf-8') as f:
    content = f.read()

checks = {
    'HB #932 footer': '2026-07-22T16:30 GMT+8 -- D+6 Wednesday afternoon -- HB #932' in content,
    'HB #932 header': '## HB #932 (2026-07-22T16:30 GMT+8 cron-event' in content,
    'HB #914 still present': '## HB #914 (2026-07-22T13:40 GMT+8 cron-event' in content,
    'Triple Confluence Day 0 CLOSED': 'Triple Confluence Day 0 CLOSED' in content,
    'Triple Confluence Day +1 post-window': 'Triple Confluence Day +1 post-window passive' in content,
}
print('=== HEARTBEAT.md integrity check ===')
for k, v in checks.items():
    status = 'OK  ' if v else 'FAIL'
    print('  [' + status + '] ' + k)
print('Total HB # entries: ' + str(content.count('## HB #')))