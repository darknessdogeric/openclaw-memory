"""Append minimal HB #861 log entry to today's memory file (R-NEW-V2 compliant)."""
from datetime import datetime, timezone, timedelta

tz_china = timezone(timedelta(hours=8))
now = datetime.now(tz_china)

log_entry = """
*HB #861 路 2026-07-22 04:58 GMT+8 路 鍛ㄎ窞鍛ㄦ棭鏅╀紤鐣?鏈細璇濇矇榛?zero-push 路 01:00 鏃╂櫄鏅氶棿 cron 瓒呰繃 23h58m 銆?2:00/04:00 deep-night cron 瓒呰繃 閮ㄧ讲瀹屽�銆?3:00: 宸查€氳繃銆?1:00 鍏ㄩ棬 CRON 瀹屾垚銆?HB 璁℃暣浣撴瀯瀹岀編 + 闆跺閿欒薄 = 鏃犵揣鎬?
""".format()

# R-NEW-V2: explicit utf-8 read+append+write
filepath = 'memory/2026-07-22.md'
with open(filepath, 'a', encoding='utf-8') as f:
    f.write(log_entry)

print('HB #861 log entry appended to {}'.format(filepath))