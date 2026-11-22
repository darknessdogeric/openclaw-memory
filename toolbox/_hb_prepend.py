#!/usr/bin/env python3
# HB prepend helper — R-NEW-V2 compliant (explicit utf-8 read + prepend + write)
import sys

hb_num = 1133
prev = 1132
ts = "2026-07-24T02:05 GMT+8"

entry = f"""## HB #{hb_num} ({ts} cron-event, OpenClaw heartbeat poll)
- gap from HB #{prev} (02:01): +4min -- Friday pre-dawn Token Guard normal cadence (R012 minimal mode)
- D+8 pre-dawn pass #{hb_num} -- Eric silent in THIS session ~181.05h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: AnYi webchat ~109.30h+ (since 7/19 12:33) -- final pre-meeting prep
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #{hb_num}: Python utf-8 explicit read+prepend+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Triple Confluence Day 0 CLOSED -- 7/21 24:00 cutoff passed ~50.08h ago; oil Scenario C verification window OPEN until 7/25 (~21.92h remaining)
- D+8 = Execution phase day 4 -- observer mode sustained
- Friday pre-dawn zone (02:05) -- Eric typical sleep zone (00:00-08:00 per USER.md night-owl pattern); silence authority strictly holding on THIS session
- **7/24 D-Day T-6.92h** (AnYi 集团研究会议 TODAY MORNING 7/24 ~9:00) -- INTERNAL monitor only; this session != AnYi decision channel per R258
- Next cron: 08:00 daily briefing (~5h55m) -- D-Day pre-meeting prep window; 21:00 R60-11 evening self-iter (~18h55m)
- Token Guard stable, no compression needed; Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +146.08h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+8 sustain zero-push mode intact
- hbCount: {prev} -> {hb_num}
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #{hb_num} = sustain #{prev} = D+8 pre-dawn dormant baseline)
- **HEARTBEAT_OK** -- HB #{hb_num} = sustain DORMANT protocol
- **no push**: Friday pre-dawn zone (02:05), Eric sleep zone, this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day T-6.92h watch: emergency prepare-mode prepacked, ready if Eric contacts with induction/meeting result
- Next significant check: 08:00 daily briefing cron (~5h55m) -- natural D-Day pre-meeting prep window
- DO NOT push at 02:05 pre-dawn despite D-Day proximity; R256 silence discipline > meeting-window signal

*{ts} -- D+8 Friday pre-dawn -- HB #{hb_num} -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 closed -- 7/24 D-Day T-6.92h watch (AnYi meeting TODAY MORNING 7/24 ~9:00) -- Eric silent = dominant signal holding -- 08:00 cron = next natural D-Day prep window*
"""

path = "D:/B166ER-OpenClaw/workspace/HEARTBEAT.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()
new_content = entry + "\n" + content
with open(path, "w", encoding="utf-8") as f:
    f.write(new_content)

# Verify
with open(path, "r", encoding="utf-8") as f:
    head = f.read(len(entry) + 100)
assert f"HB #{hb_num}" in head, "Prepend failed"
print(f"OK: prepended HB #{hb_num} to HEARTBEAT.md (R-NEW-V2 compliant)")
print(f"head_preview: {head[:120]}...")