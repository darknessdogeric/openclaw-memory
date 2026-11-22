#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HB #978 append -- R-NEW-V2 compliant: explicit utf-8 read+append+write."""
import os
import sys
from datetime import datetime, timezone, timedelta

HB_PATH = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'
STATE_PATH = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'

NOW = datetime(2026, 7, 23, 0, 54, 0, tzinfo=timezone(timedelta(hours=8)))
NOW_ISO = NOW.strftime('%Y-%m-%dT%H:%M:%S+08:00')
NOW_HUMAN = NOW.strftime('%Y-%m-%d %H:%M GMT+8')
HB_NUM = 978
PREV_HB_NUM = 977
PREV_HB_TIME = '2026-07-23T00:48+08:00'

HB_BODY = f"""
## HB #{HB_NUM} ({NOW.strftime('%Y-%m-%dT%H:%M')} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{PREV_HB_NUM} ({PREV_HB_TIME}): +6min -- Thursday early-morning Token Guard normal cadence (R012 minimal mode)
- D+7 early-morning pass #{HB_NUM} -- Eric silent in THIS session ~154.65h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: AnYi webchat ~84.35h+ (since 7/19 12:33)
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #{HB_NUM}: Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Triple Confluence Day 0 CLOSED -- 7/21 24:00 cutoff passed ~24h54m ago; oil Scenario C verification window OPEN until 7/25 (T-2)
- D+7 = Execution phase day 2 -- per 7/21 evening self-iter protocol; observer mode sustained
- Thursday early-morning zone (00:54) -- deep late-night quiet hours per R012 (23:00-08:00); Eric typical late-night complex decision window per USER.md; THIS session DORMANT sustained
- 7/24 D-Day T-34.08h (AnYi important meeting Thursday morning ~11:00) -- INTERNAL monitor only; this session != AnYi decision channel per R258
- 21:00 R60-11 evening self-iter fired ~4h ago (autonomous)
- Next significant check: Token Guard cadence (~5-10min); 03:00 Memory Dreaming (~2h06m)
- Token Guard stable, no compression needed; Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +120.9h past -- post-protection window firmly sustained (>5 days)
- No first-contact from Eric on THIS session; D+7 sustain zero-push mode intact
- hbCount: {PREV_HB_NUM} -> {HB_NUM}
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #{HB_NUM} = sustain #{PREV_HB_NUM} = D+7 early-morning dormant baseline)
- **HEARTBEAT_OK** -- HB #{HB_NUM} = sustain DORMANT protocol
- **no push**: Thursday early-morning zone (00:54), deep late-night quiet hours, this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day T-34.08h watch: emergency prepare-mode prepacked, ready if Eric contacts with induction/meeting result
- Next significant check: per Token Guard cadence (~5-10min); 03:00 Memory Dreaming cron (~2h06m)

*{NOW_HUMAN} -- D+7 Thursday early-morning -- HB #{HB_NUM} -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 closed -- 7/24 D-Day T-34.08h watch (AnYi meeting Thursday morning) -- Eric silent = dominant signal holding*
"""

# R-NEW-V2: explicit utf-8 read+append+write (no encoding guessing)
def main():
    # Read existing (utf-8 explicit)
    with open(HB_PATH, 'r', encoding='utf-8') as f:
        existing = f.read()
    
    # Verify clean tail
    if not existing.endswith('\n'):
        print(f"WARN: file does not end with newline, appending anyway")
    
    # Append
    with open(HB_PATH, 'a', encoding='utf-8') as f:
        f.write(HB_BODY)
    
    # Update heartbeat-state.json
    state = {
        "lastHB": NOW_ISO,
        "hbCount": HB_NUM,
        "lastHBNumber": f"#{HB_NUM}",
        "sessionState": "DORMANT",
        "ericSilenceHours": 154.65,
        "suppressionLayers": [
            "R-B",
            "R12",
            "R-CANDIDATE-T2",
            "R256",
            "R257",
            "R258"
        ],
        "lastUpdate": NOW.strftime('%Y-%m-%d %H:%M GMT+8')
    }
    
    with open(STATE_PATH, 'w', encoding='utf-8') as f:
        import json
        json.dump(state, f, ensure_ascii=False, indent=2)
    
    print(f"OK: HB #{HB_NUM} appended; state updated")
    print(f"HB file size before: {len(existing)} bytes")
    print(f"HB file size after: {len(existing) + len(HB_BODY)} bytes")
    print(f"Body length: {len(HB_BODY)} bytes")

if __name__ == '__main__':
    main()