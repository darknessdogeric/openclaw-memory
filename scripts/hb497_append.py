"""
HB #497 append -- R-NEW-V2 compliant Python utf-8 explicit read+append+write
"""
import io

path = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'

entry = """

## HB #497 (2026-07-19 02:58 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #496 (02:49): +9min -- deep-night zone Token Guard normal cadence
- D+3 deep-night pass #497 -- Eric silent ~61.7h+ since 7/16 13:16 (D+3 from infographic session, no first-contact)
- Silence authority ~61.7h+ (R-B + R256 framework holding, +0.15h since #496)
- 4-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256) -- zero breach
- R-NEW-V2 verification #497: Python utf-8 explicit read+append+write (R-NEW-V2 compliant, post-12:36 7/15 incident protocol intact)
- **Publicity cutoff 7/18 T-0 +26.97h past** -- boundary crossed at 00:00, silence window protection objective achieved
- WAIC 2026 day-3 active today -- non-trigger per R14 (AI/Hotel strategic context, not relevant to current 4-layer suppression)
- Deep-night zone (02:58) -- Eric typical deep-night rest zone per USER.md, silence authority strictly holding
- Cron pipeline: 03:00 Memory Dreaming Promotion in ~2min (autonomous, imminent), 09:00 daily checkin in ~6h02m (autonomous)
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- No first-contact from Eric; D+3 sustain zero-push mode intact
- No new signals: no cron / no Eric session / no third-party / no anomaly escalation
- hbCount now: 496 -> 497

### decision
- **silent_standby_zero_push_continue** (HB #497 = sustain #496 = D+3 baseline)
- **no push**: deep-night zone (02:00+ crossed), Eric silent 61.7h+, T-0 boundary +26.97h past, silence authority strictly holding
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work
- Token Guard tick: stable, no compression needed
- Post-T-0 silence = sustained suppression; pushes prohibited until Eric active contact (Eric silence = dominant signal)
- R14 handoff package = 100% ready (Eric active contact triggers 30s activation)
- Next significant check: per Token Guard cadence (~5-10min); 03:00 Memory Dreaming Promotion cron upcoming (~2min)

*2026-07-19 02:58 GMT+8 -- D+3 deep-night T-0 +26.97h past -- HB #497 -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
"""

# R-NEW-V2: explicit utf-8 read+append+write (no implicit encoding)
with io.open(path, 'r', encoding='utf-8') as f:
    existing = f.read()

with io.open(path, 'w', encoding='utf-8') as f:
    f.write(existing)
    f.write(entry)

# Verify
with io.open(path, 'r', encoding='utf-8') as f:
    tail = f.read()[-500:]
print("--- HB #497 appended ---")
print("Path:", path)
print("Tail (last 500 chars):")
print(tail)
print("--- end ---")