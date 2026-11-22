"""HB #676 time delta calculator"""
import datetime

now = datetime.datetime.now()
eric_last = datetime.datetime(2026, 7, 16, 13, 16)
anyi_first = datetime.datetime(2026, 7, 19, 12, 33)
induction_end = datetime.datetime(2026, 7, 21, 23, 59, 59)
evening_iter = now.replace(hour=21, minute=0, second=0, microsecond=0)
if evening_iter < now:
    evening_iter += datetime.timedelta(days=1)
t0_cutoff = datetime.datetime(2026, 7, 18, 0, 0, 0)
hb_prev = datetime.datetime(2026, 7, 20, 18, 35, 50)

print(f'Now: {now.strftime("%Y-%m-%dT%H:%M:%S GMT+8")}')
print(f'gap from HB #675 (18:35): +{round((now - hb_prev).total_seconds()/60, 1)}min')
print(f'Eric silent THIS session h: {round((now - eric_last).total_seconds()/3600, 2)}')
print(f'Eric active AnYi h: {round((now - anyi_first).total_seconds()/3600, 2)}')
print(f'Induction window remaining h: {round((induction_end - now).total_seconds()/3600, 2)}')
print(f'21:00 R60-12 evening h: {round((evening_iter - now).total_seconds()/3600, 2)}')
print(f'T-0 +h past: {round((now - t0_cutoff).total_seconds()/3600, 2)}')