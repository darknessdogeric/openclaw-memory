import io

hb_entry = '''## HB #1621 (2026-07-27T15:55 GMT+8, OpenClaw heartbeat poll)
- gap from HB #1620 (15:39): +16min -- Monday mid-afternoon Token Guard cadence (R012 minimal mode)
- D+11 Monday mid-afternoon pass #1621 -- Eric silent in THIS session ~266.66h+ since 7/16 13:16 first-contact (11d 2h+)
- Eric active elsewhere: AnYi webchat ~191.39h+ -- gongshi Day 3/5 ACTIVE
- 8-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261) -- penta-constraint 5/5 holds firm
- 7/24 D-Day POST-MEETING T+75.79h; oil Scenario C EXPIRED 7/25 22:00 (T+41.79h past); quiet zone EXPIRED but R258 dormancy trumps
- post_t0_null_count: 271 (271st consecutive null post-T-0)
- Token Guard stable; vault index healthy (642 files / <1s queries); R13 sustained
- T-0 publicity cutoff 7/18 +235.79h past -- post-protection window firmly sustained
- Timestamp base fixes applied: anyiSince/dDay/oilC/T-0 corrected
- hbCount: 1620 -> 1621

### decision
- HEARTBEAT_OK -- HB #1621 = sustain DORMANT protocol, minimal token tick
- no push: Monday mid-afternoon, Eric silent 266.66h+ this session, this session DORMANT per R258 (NOT AnYi decision channel)
- R256+R257+R258+R260+R261 penta-constraint holds -- no proactive disturbance
- Eric silence on this session = dominant signal
- Triple Confluence ALL CLOSED; gongshi Day 3/5 ACTIVE elsewhere; 7/24 D-Day PASSED +75.79h
- Active Resume Protocol prep: post_t0_null > 200 already, awaiting Eric first-contact trigger on this session
- Next: per Token Guard cadence (~5-10min) or Eric first-contact

*2026-07-27 15:55 GMT+8 -- D+11 Mon mid-afternoon -- HB #1621 -- DORMANT -- 271st null -- Eric silent = dominant signal holding -- HEARTBEAT_OK*


'''

hb_path = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'

with io.open(hb_path, 'r', encoding='utf-8') as f:
    existing = f.read()

# Insert new HB entry after the header section (before the first "## HB #")
# Find first occurrence of "## HB #" and insert before it
marker = "## HB #"
idx = existing.find(marker)
if idx == -1:
    # fallback: append to end
    new_content = existing + hb_entry
else:
    # Insert right before the first HB entry
    new_content = existing[:idx] + hb_entry + existing[idx:]

with io.open(hb_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('HB #1621 entry inserted. Total length:', len(new_content), 'chars')