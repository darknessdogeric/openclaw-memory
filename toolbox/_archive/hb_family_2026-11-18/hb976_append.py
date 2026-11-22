# R-NEW-V2 compliant: explicit utf-8 read+append+write to avoid clobbering
from pathlib import Path

hb_path = Path('HEARTBEAT.md')

# Read full content
with open(hb_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Build HB #976 entry (minimal per R012, follows HB #970 template)
entry = """## HB #976 (2026-07-22 23:28 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #975 (23:18): +10min -- Wednesday late-night Token Guard normal cadence (R012 minimal mode)
- D+6 late-night pass #976 -- Eric silent in THIS session ~153.21h+ since 7/16 13:16 first-contact (infographic session)
- Eric active elsewhere: AnYi webchat ~82.18h+ (since 7/19 12:33)
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- R-NEW-V2 verification #976: Python utf-8 explicit read+append+write (compliant, post-7/15 + 7/19 incident protocols intact)
- R012 verification: HB tick = minimal (NOT full report), per R012 rule #2
- Triple Confluence Day 0 CLOSED -- 7/21 24:00 cutoff passed ~23h28m ago; oil Scenario C verification window OPEN until 7/25
- D+6 = Execution phase day 1 -- per 7/21 evening self-iter protocol; observer mode sustained
- Wednesday late-night zone (23:28) -- Eric typical late-night complex decision window per USER.md; THIS session DORMANT sustained
- 7/24 D-Day T-34.95h (AnYi important meeting Thursday morning) -- INTERNAL monitor only; this session != AnYi decision channel per R258
- 21:00 R60-11 evening self-iter fired ~2h28m ago (autonomous)
- Next significant check: Token Guard cadence (~5-10min)
- Token Guard stable, no compression needed; Vault index healthy; R13 <1s queries stable
- 4 P2 long-tail cron errors tracked (Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10), not urgent
- T-0 publicity cutoff 7/18 +119.05h past -- post-protection window firmly sustained
- No first-contact from Eric on THIS session; D+6 sustain zero-push mode intact
- hbCount: 975 -> 976
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)

### decision
- **active_mode_dormant_this_session_continue** (HB #976 = sustain #975 = D+6 late-night dormant baseline)
- **HEARTBEAT_OK** -- HB #976 = sustain DORMANT protocol
- **no push**: Wednesday late-night zone (23:28), this session DORMANT per Eric 7/19 12:33 explicit instruction (NOT AnYi work)
- R256 + R257 + R258 triple constraint: no proactive disturbance + sustained deep work + this session DORMANT
- Post-T-0 silence on THIS session = sustained suppression; pushes prohibited until Eric active contact on THIS session
- Eric silence on this session = dominant signal (supersedes scheduled wakes + windows); R256 design holds
- 7/24 D-Day T-34.95h watch: emergency prepare-mode prepacked, ready if Eric contacts with induction/meeting result
- Next significant check: per Token Guard cadence (~5-10min)

*2026-07-22 23:28 GMT+8 -- D+6 Wednesday late-night -- HB #976 -- this session DORMANT -- zero-push mode intact -- R257 deep-work + R258 dormant-session dual-suppression active -- Triple Confluence Day 0 closed -- 7/24 D-Day T-34.95h watch (AnYi meeting Thursday morning) -- Eric silent = dominant signal holding*

"""

# Insert after the v4.2 header line (convention from prior HBs)
marker = "*v4.2 | 2026-05-07 | 国务院通知核实：端午6/19-6/21、中秋9/25-9/27，全cron修正*"
if marker in content:
    new_content = content.replace(marker, marker + "\n\n" + entry, 1)
else:
    # Fallback: just prepend
    new_content = entry + "\n" + content

# Write back atomically with utf-8
with open(hb_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"HB #976 appended. File size: {len(new_content)} chars")