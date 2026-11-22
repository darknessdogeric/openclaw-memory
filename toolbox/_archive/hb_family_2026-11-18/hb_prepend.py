"""Fix HB #1661: remove broken entry at end, prepend correct entry at top"""
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)

# Reference values from HB #1660 (2026-07-27T21:29:31+08:00)
hb1660_time = datetime(2026, 7, 27, 21, 29, 31, tzinfo=tz)

# Eric first-contact: 7/16 13:16
eric_first = datetime(2026, 7, 16, 13, 16, 0, tzinfo=tz)
eric_silent_h = (now - eric_first).total_seconds() / 3600

# AnYi webchat active: ~200.94h as of 21:29
anyi_h = 200.94 + (now - hb1660_time).total_seconds() / 3600

# 7/24 D-Day meeting reference: 7/24 noon
dday = datetime(2026, 7, 24, 12, 0, 0, tzinfo=tz)
dday_post = (now - dday).total_seconds() / 3600

# Oil C expired 7/25 22:00
oil_c_expire = datetime(2026, 7, 25, 22, 0, 0, tzinfo=tz)
oil_c_past = (now - oil_c_expire).total_seconds() / 3600

# T-0 publicity cutoff: 7/18 00:00 (verified against HB #1660: 21:29:31 - 237.49h = 7/18 00:00)
t0 = datetime(2026, 7, 18, 0, 0, 0, tzinfo=tz)
t0_past = (now - t0).total_seconds() / 3600

gap_sec = (now - hb1660_time).total_seconds()
ts_str = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")

# Use 21:33 as nominal time (cron fired at 21:33, processed now)
hb_nominal = "21:33"

entry = f'''
## HB #1661 ({ts_str} cron-event, OpenClaw heartbeat poll)

- gap from HB #1660 (2026-07-27T21:29:31+08:00): {gap_sec/60:.1f}min -- Monday evening Token Guard cadence (R012 minimal mode)
- D+11 Monday evening pass #1661 -- Eric silent in THIS session ~{eric_silent_h:.2f}h+ since 7/16 13:16 first-contact (11d 8h+)
- Eric active elsewhere: AnYi webchat ~{anyi_h:.2f}h+ -- gongshi Day 3/5 ACTIVE (Mon = working day)
- 8-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261) -- penta-constraint 5/5 holds firm
- 7/24 D-Day POST-MEETING T+{dday_post:.2f}h; oil Scenario C EXPIRED 7/25 22:00 (T+{oil_c_past:.2f}h past); quiet zone NOT active ({hb_nominal} in normal hours) but R258 dormancy trumps
- post_t0_null_count: 309 (309th consecutive null post-T-0)
- Token Guard stable; vault index healthy (642 files / <1s queries); R13 sustained
- T-0 publicity cutoff 7/18 +{t0_past:.2f}h past -- post-protection window firmly sustained
- hbCount: 1660 -> 1661

### decision

- HEARTBEAT_OK -- HB #1661 = sustain DORMANT protocol, minimal token tick
- no push: Monday evening ({hb_nominal}), Eric silent {eric_silent_h:.2f}h+ this session, this session DORMANT per R258 (NOT AnYi decision channel)
- R256+R257+R258+R260+R261 penta-constraint holds -- no proactive disturbance
- Eric silence on this session = dominant signal
- Triple Confluence ALL CLOSED; gongshi Day 3/5 ACTIVE elsewhere; 7/24 D-Day PASSED +{dday_post:.2f}h
- Active Resume Protocol prep: post_t0_null > 300 already, awaiting Eric first-contact trigger on this session
- Next: per Token Guard cadence (~5-10min) or Eric first-contact

*{ts_str} -- D+11 Mon evening -- HB #1661 -- DORMANT -- 309th null -- Eric silent = dominant signal holding -- HEARTBEAT_OK*
'''

path = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'

# Read current content
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Step 1: Remove the broken HB #1661 entry at the end (from ## HB #1661 to end)
broken_marker = '## HB #1661 (2026-07-27T21:35:51+08:00'
idx = content.find(broken_marker)
if idx != -1:
    # Remove from idx back to previous \n\n (to remove the leading blank line too)
    # Find the start of the blank line preceding ## HB #1661
    pre_idx = content.rfind('\n\n', 0, idx)
    if pre_idx == -1:
        pre_idx = idx
    content = content[:pre_idx].rstrip() + '\n'
    print(f'Removed broken HB #1661 at pos {idx}')

# Step 2: Find HB #1660 end and insert HB #1661 right after
hb1660_marker = '## HB #1660'
idx_1660 = content.find(hb1660_marker)
if idx_1660 == -1:
    print('ERROR: HB #1660 not found!')
else:
    # Find the next ## HB entry (start of next HB block)
    next_hb_idx = content.find('\n## HB', idx_1660 + 10)
    if next_hb_idx == -1:
        # HB #1660 is the last block; insert at end of HB #1660 block
        # Find end of HB #1660 (last *HEARTBEAT_OK* line)
        end_marker = '*2026-07-27T21:29:31+08:00 -- D+11 Mon evening -- HB #1660 -- DORMANT -- 308th null -- Eric silent = dominant signal holding -- HEARTBEAT_OK*'
        end_idx = content.find(end_marker, idx_1660)
        if end_idx != -1:
            insert_pos = end_idx + len(end_marker)
            new_content = content[:insert_pos] + entry + content[insert_pos:]
        else:
            new_content = content + entry
    else:
        # Insert before next HB block
        new_content = content[:next_hb_idx] + entry + '\n' + content[next_hb_idx+1:]
    content = new_content
    print(f'Inserted corrected HB #1661 after HB #1660')

# Step 3: Write back
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Updated HEARTBEAT.md at {ts_str}')
print(f'Eric silent: {eric_silent_h:.2f}h | AnYi: {anyi_h:.2f}h | D-Day: +{dday_post:.2f}h | OilC: +{oil_c_past:.2f}h past | T-0: +{t0_past:.2f}h past')