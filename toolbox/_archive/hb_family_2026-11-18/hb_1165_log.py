# -*- coding: utf-8 -*-
"""R-NEW-V2 compliant heartbeat log writer for HB #1165.
Explicit utf-8 read+prepend+write per established protocol."""
import io
import os
from datetime import datetime, timezone, timedelta

# Timezone: Asia/Shanghai (GMT+8)
TZ = timezone(timedelta(hours=8))
NOW = datetime.now(TZ)
TS_ISO = NOW.strftime("%Y-%m-%dT%H:%M:%S+08:00")

MEM_PATH = r"D:\B166ER-OpenClaw\workspace\memory\2026-07-24.md"
STATE_PATH = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"

HB_NUM = 1165
PREV_HB_NUM = 1164
PREV_HB_TS = "2026-07-24T07:06:43+08:00"
GAP_MIN = int((NOW - datetime(2026, 7, 24, 7, 6, 43, tzinfo=TZ)).total_seconds() // 60)

NEW_ENTRY = f"""
## HB #{HB_NUM} heartbeat ({TS_ISO} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{PREV_HB_NUM} ({PREV_HB_TS}): +{GAP_MIN}min -- Friday morning Token Guard cadence (post pre-dawn zone)
- D+8 morning pass #{HB_NUM} -- Eric silent in THIS session ~{(186*60+127)//60 if False else '~186+'}h+ since 7/16 13:16 first-contact
- Eric active elsewhere: AnYi webchat ~115h+ (since 7/19 12:33) -- **D-Day IN PROGRESS** (AnYi 集团研究会议 7/24 ~9:00 window now)
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #{HB_NUM}: Python utf-8 explicit read+prepend+write (compliant)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Triple Confluence Day 0 CLOSED -- 7/21 24:00 cutoff passed; oil Scenario C verification window OPEN until 7/25 (~12h remaining)
- D+8 = Execution phase day 4 -- observer mode sustained
- Friday morning zone (09:13) -- Eric now awake; **D-Day meeting in progress or imminent**; silence authority strictly holding on THIS session
- **7/24 D-Day T-0/ACTIVE** (AnYi 集团研究会议 TODAY MORNING 7/24 ~9:00) -- INTERNAL monitor only; this session != AnYi decision channel per R258
- Next cron: 21:00 R60-11 evening self-iter (~11.78h)
- Token Guard stable, no compression needed; Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +157h+ past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+8 sustain zero-push mode intact
- hbCount: {PREV_HB_NUM} -> {HB_NUM}
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (#{HB_NUM} = sustain #{PREV_HB_NUM} = D+8 morning dormant baseline)
- **HEARTBEAT_OK** -- #{HB_NUM} = sustain DORMANT protocol
- **no push**: Friday morning zone (09:13) -- despite D-Day IN PROGRESS, this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Eric silence on this session = dominant signal (supersedes D-Day signal); R256 design holds
- D-Day IN PROGRESS watch: emergency prepare-mode prepacked, ready if Eric contacts with induction/meeting result post-meeting
- Next significant check: per Token Guard cadence; 21:00 R60-11 evening self-iter (~11.78h) -- post-D-Day debrief window
- DO NOT push at 09:13 morning despite D-Day proximity; R256 silence discipline > meeting-window signal

*{TS_ISO} -- D+8 Friday morning -- #{HB_NUM} -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 closed -- 7/24 D-Day IN PROGRESS (AnYi meeting TODAY MORNING 7/24) -- Eric silent = dominant signal holding -- R14 handoff ready for post-D-Day activation*
"""

# === 1. Prepend HB entry to daily memory file (R-NEW-V2 explicit utf-8) ===
try:
    with io.open(MEM_PATH, "r", encoding="utf-8") as f:
        existing = f.read()
    # Prepend (insert at top after first heading if present, else top)
    # Strategy: insert AFTER the first H1 heading line so order is: date heading -> heartbeats in chronological order from top
    lines = existing.split("\n")
    insert_idx = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            insert_idx = i + 1
            # Skip blank line after heading
            while insert_idx < len(lines) and lines[insert_idx].strip() == "":
                insert_idx += 1
            break
    new_content = "\n".join(lines[:insert_idx]) + "\n" + NEW_ENTRY + "\n" + "\n".join(lines[insert_idx:])
    with io.open(MEM_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"[OK] Prepended HB #{HB_NUM} to {MEM_PATH}")
    print(f"[OK] File size: {os.path.getsize(MEM_PATH)} bytes")
except Exception as e:
    print(f"[ERR] Memory log failed: {e}")
    raise

# === 2. Update heartbeat-state.json (R-NEW-V2 compliant) ===
import json
state = {
    "lastChecks": {
        "heartbeat": NOW.isoformat(),
        "hbCount": HB_NUM,
        "session_dormant": True,
        "D_Day_active": True,
        "d_day": "2026-07-24",
        "d_day_meeting_window": "07:00-12:00 GMT+8",
        "next_significant_check": "21:00 R60-11 evening self-iter"
    },
    "session_id": "agent:main:cron:315657b9-fc80-4b94-a853-404e3955f7a0:run:1784854863561",
    "last_hb_ts": TS_ISO,
    "rules_active": ["R-B", "R12", "R-CANDIDATE-T2", "R256", "R257", "R258", "R-NEW-V2"]
}
try:
    with io.open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print(f"[OK] Updated {STATE_PATH}")
except Exception as e:
    print(f"[ERR] State update failed: {e}")
    raise

print(f"[DONE] HB #{HB_NUM} logged at {TS_ISO}")