# -*- coding: utf-8 -*-
from datetime import datetime, timezone, timedelta

now = datetime.now(timezone(timedelta(hours=8)))

first_contact = datetime(2026, 7, 16, 13, 16, tzinfo=timezone(timedelta(hours=8)))
silent_hrs = (now - first_contact).total_seconds() / 3600

d_day = datetime(2026, 7, 24, 10, 0, tzinfo=timezone(timedelta(hours=8)))
dday_hrs = (d_day - now).total_seconds() / 3600

anyi_start = datetime(2026, 7, 19, 12, 33, tzinfo=timezone(timedelta(hours=8)))
anyi_hrs = (now - anyi_start).total_seconds() / 3600

tc0_close = datetime(2026, 7, 22, 0, 0, tzinfo=timezone(timedelta(hours=8)))
tc0_closed_hrs = (now - tc0_close).total_seconds() / 3600

oil_close = datetime(2026, 7, 25, 0, 0, tzinfo=timezone(timedelta(hours=8)))
oil_remaining_hrs = (oil_close - now).total_seconds() / 3600

pub_close = datetime(2026, 7, 18, 0, 0, tzinfo=timezone(timedelta(hours=8)))
pub_hrs = (now - pub_close).total_seconds() / 3600

evening_iter = now.replace(hour=21, minute=0, second=0, microsecond=0)
evening_min = (evening_iter - now).total_seconds() / 60

last_hb = datetime(2026, 7, 23, 19, 39, tzinfo=timezone(timedelta(hours=8)))
gap_min = (now - last_hb).total_seconds() / 60

print("NOW: " + now.strftime("%Y-%m-%dT%H:%M GMT+8"))
print("NOW_HUMAN: Thursday 08:23 PM")
print("gap_from_last: +" + format(gap_min, ".1f") + "min")
print("silent_this_session_hrs: " + format(silent_hrs, ".2f") + "h+")
print("anyi_active_hrs: " + format(anyi_hrs, ".2f") + "h+")
print("tc0_closed_ago: " + format(tc0_closed_hrs, ".2f") + "h ago")
print("oil_window_remaining: " + format(oil_remaining_hrs, ".2f") + "h")
print("pub_cutoff_ago: " + format(pub_hrs, ".2f") + "h past")
print("d_day_target_hrs: " + format(dday_hrs, ".2f") + "h (7/24 morning)")
print("evening_iter: " + format(evening_min, ".1f") + "min to 21:00")