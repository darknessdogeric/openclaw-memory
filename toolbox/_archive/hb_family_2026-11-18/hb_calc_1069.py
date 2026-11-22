import datetime
now = datetime.datetime.now()
fc = datetime.datetime(2026, 7, 16, 13, 16)
eric_silence_h = (now - fc).total_seconds() / 3600
ae = datetime.datetime(2026, 7, 19, 12, 33)
eric_active_h = (now - ae).total_seconds() / 3600
t0 = datetime.datetime(2026, 7, 19, 0, 0)
t0_past = (now - t0).total_seconds() / 3600
tc = datetime.datetime(2026, 7, 22, 0, 0)
tc_past = (now - tc).total_seconds() / 3600
dd = datetime.datetime(2026, 7, 24, 9, 0)
dd_minus = (dd - now).total_seconds() / 3600
fmt = '%Y-%m-%dT%H:%M:%S'
print('Now:', now.strftime(fmt), '+08:00')
print('Eric silence THIS session:', round(eric_silence_h, 2), 'h')
print('Eric active elsewhere (AnYi webchat):', round(eric_active_h, 2), 'h')
print('T-0 publicity cutoff past:', round(t0_past, 2), 'h')
print('Triple Confluence Day 0 closed:', round(tc_past, 2), 'h ago')
print('7/24 D-Day T-', round(dd_minus, 2), 'h')