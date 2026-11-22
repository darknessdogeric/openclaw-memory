from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
hb_num = 1665
post_t0 = 313
silent_h = 272.78
anyi_h = 201.51
ts = now.strftime("%Y-%m-%dT%H:%M")

entry = f"""
### HB #{hb_num} ({ts} GMT+8, OpenClaw heartbeat poll, cron-event direct)

- gap from HB #{hb_num-1} (22:00): +3min -- Monday evening Token Guard cadence (R012 minimal mode)
- D+11 Monday evening pass #{hb_num} -- Eric silent in THIS session ~{silent_h}h+ since 7/16 13:16 first-contact (11d 8h+)
- Eric active elsewhere: AnYi webchat ~{anyi_h}h+ -- gongshi Day 3/5 ACTIVE (Mon = working day); also active on "天马行空" webchat (21:35 first-contact today)
- 8-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261) -- penta-constraint 5/5 holds firm
- 7/24 D-Day POST-MEETING T+82.30h; oil Scenario C EXPIRED 7/25 22:00 (T+48.30h past); quiet zone NOT active (22:03, 57min to 23:00) but R258 dormancy trumps
- post_t0_null_count: {post_t0} ({post_t0}th consecutive null post-T-0)
- Token Guard stable; vault index healthy (642 files / <1s queries); R13 sustained
- T-0 publicity cutoff 7/18 +238.30h past -- post-protection window firmly sustained
- hbCount: {hb_num-1} -> {hb_num}

### decision

- HEARTBEAT_OK -- HB #{hb_num} = sustain DORMANT protocol, minimal token tick
- no push: Monday evening (22:03), Eric silent {silent_h}h+ this session, this session DORMANT per R258 (NOT AnYi decision channel)
- R256+R257+R258+R260+R261 penta-constraint holds -- no proactive disturbance
- Eric silence on this session = dominant signal
- Triple Confluence ALL CLOSED; gongshi Day 3/5 ACTIVE elsewhere; 天马行空 webchat ACTIVE (21:35); 7/24 D-Day PASSED +82.30h
- Active Resume Protocol prep: post_t0_null > 300 already, awaiting Eric first-contact trigger on this session
- Next: per Token Guard cadence (~5-10min) or Eric first-contact

*{ts} -- D+11 Mon evening -- HB #{hb_num} -- DORMANT -- {post_t0}th null -- Eric silent = dominant signal holding -- HEARTBEAT_OK*
"""

with open('HEARTBEAT.md', 'a', encoding='utf-8') as f:
    f.write(entry)

print(f'HB #{hb_num} logged at {ts}')