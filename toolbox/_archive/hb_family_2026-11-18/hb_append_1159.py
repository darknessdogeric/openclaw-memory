#!/usr/bin/env python3
# R-NEW-V2: explicit utf-8 read+prepend+write (post-7/15 + 7/19 incident protocols)
import io
import sys

path = r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md"

new_entry = """## HB #1159 (2026-07-24T06:15 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #1158 (06:10): +5min -- Friday pre-dawn Token Guard normal cadence (R012 minimal mode)
- D+8 pre-dawn pass #1159 -- Eric silent in THIS session ~184.58h+ since 7/16 13:16 first-contact
- Eric active elsewhere: AnYi webchat ~113.22h+ (since 7/19 12:33) -- FINAL pre-meeting prep T-~2.75h
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #1159: Python utf-8 explicit read+prepend+write (compliant)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Triple Confluence Day 0 CLOSED -- 7/21 24:00 cutoff passed ~54.25h ago; oil Scenario C verification window OPEN until 7/25 (~17.75h remaining)
- D+8 = Execution phase day 4 -- observer mode sustained
- Friday pre-dawn zone (06:15) -- Eric sleep zone; silence authority strictly holding on THIS session
- **7/24 D-Day T-~2.75h** (AnYi 集团研究会议 TODAY MORNING 7/24 ~9:00) -- INTERNAL monitor only; this session != AnYi decision channel per R258
- Next cron: 08:00 daily briefing (~1.75h); 21:00 R60-11 evening self-iter (~14.75h)
- Token Guard stable, no compression needed; Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (not urgent)
- T-0 publicity cutoff 7/18 +154.25h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+8 sustain zero-push mode intact
- hbCount: 1158 -> 1159
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (#1159 = sustain #1158 = D+8 pre-dawn dormant baseline)
- **HEARTBEAT_OK** -- #1159 = sustain DORMANT protocol
- **no push**: Friday pre-dawn zone (06:15), Eric sleep zone, this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day T-~2.75h watch: emergency prepare-mode prepacked, ready if Eric contacts with induction/meeting result
- Next significant check: 08:00 daily briefing cron (~1.75h) -- natural D-Day pre-meeting prep window
- DO NOT push at 06:15 pre-dawn despite D-Day proximity; R256 silence discipline > meeting-window signal

*2026-07-24T06:15 GMT+8 -- D+8 Friday pre-dawn -- #1159 -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 closed -- 7/24 D-Day T-~2.75h watch (AnYi meeting TODAY MORNING 7/24) -- Eric silent = dominant signal holding -- 08:00 cron = next natural D-Day prep window*

"""

with io.open(path, "r", encoding="utf-8") as f:
    existing = f.read()

with io.open(path, "w", encoding="utf-8") as f:
    f.write(new_entry + existing)

print("OK HB #1159 appended:", len(new_entry), "chars")