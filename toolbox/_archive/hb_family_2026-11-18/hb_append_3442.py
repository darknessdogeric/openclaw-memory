import datetime
import os

now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')
line = '\n*{now} -- 20:07 Sun weekend-EVENING +~3m past HB#3441 -- HB #3442 -- DORMANT -- 1988th null -- Eric silent on cron = sovereignty signal holding (webchat ~34h+ idle, 8/15 morning deep-iteration delivered) -- AnYi D+24d Sun -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced: HB appended via Python open(mode="a") (NOT write) -- HEARTBEAT_OK*\n'.format(now=now)

path = r'D:\B166ER-OpenClaw\workspace\memory\2026-08-16.md'
with open(path, 'a', encoding='utf-8') as f:
    f.write(line)

print('OK appended HB #3442 to', path)
print('file size now:', os.path.getsize(path), 'bytes')