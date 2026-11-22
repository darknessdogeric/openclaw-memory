"""HB #642 silence duration calculator."""
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
last = datetime(2026, 7, 16, 13, 16, tzinfo=tz)
first_contact = datetime(2026, 7, 19, 12, 36, tzinfo=tz)
t0 = datetime(2026, 7, 18, 0, 0, tzinfo=tz)
induction_end = datetime(2026, 7, 21, 23, 59, tzinfo=tz)

silence_h = (now - last).total_seconds() / 3600
active_h = (now - first_contact).total_seconds() / 3600
t0_past_h = (now - t0).total_seconds() / 3600
induction_close_h = (induction_end - now).total_seconds() / 3600

print(f"now={now.strftime('%Y-%m-%d %H:%M:%S %z')}")
print(f"silence_this_session_h={silence_h:.2f}")
print(f"eric_active_elsewhere_h={active_h:.2f}")
print(f"t0_past_h={t0_past_h:.2f}")
print(f"induction_close_h={induction_close_h:.2f}")
print(f"hb_count=642")
print(f"prev_hb=641 (2026-07-20 12:55:34 GMT+8)")