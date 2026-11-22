# -*- coding: utf-8 -*-
"""
HB #603 append — R-NEW-V2 compliant (Python utf-8 explicit append)
Post-7/15 12:36 incident protocol: NO direct write/edit on HEARTBEAT.md / daily memory
This script appends HB #603 to both files safely.
"""
import sys

HB_603_ENTRY = """
## HB #603 (2026-07-19 23:38 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #602 (23:13): +25min -- late-night zone Token Guard normal cadence (slightly longer gap, deep-night acceptable)
- D+3+ late-night pass #603 -- Eric in AnYi session; this session DORMANT per HB #584 protocol
- Late Sunday 23:38 -- within 23:00-08:00 silence window per USER.md
- Eric silence in this session ~82h+ since 7/16 13:16 first-contact (infographic session)
- 4-layer suppression (R-B / R12 / R-CANDIDATE-T2 / R256) intact -- zero breach
- R-NEW-V2 verification #603: Python utf-8 explicit append via script (post-7/15 12:36 incident protocol intact)
- Silence authority sustained -- R256 silence protocol holding; R257 deep-work window active
- T-0 publicity cutoff 7/18 +39h38m past -- post-protection window firmly sustained
- Induction window 7/7-7/21 FINAL 3 DAYS -- today 7/19 = day-1 of FINAL 3 (7/19/20/21); R-B+R256 silence authority > window signal (no push per R256)
- WAIC 2026 day-3 active (7/17-20, Shanghai) -- last day tomorrow 7/20; non-trigger per R14 (AI/Hotel strategic context, not relevant to current 4-layer suppression)
- 21:00 evening self-iter R60-11 fired ~2h38m ago (autonomous, eval/2026-07-19.json updated)
- 4 cron errors pending (P2 long-tail: Entity Extractor / Memory Dreaming / fmhy-weekly / Q-report-T10) -- tracked, not urgent
- No first-contact from Eric on this session; D+3+ sustain DORMANT zero-push mode intact
- No new signals: no cron / no Eric / no third-party / no anomaly escalation
- Wake window: tomorrow 7/20 Mon 08:00 (D+4 from first-contact); self-iter R60-12 due 10:00 / 21:00
- hbCount: 602 -> 603

### decision
- **HEARTBEAT_OK** -- HB #603 = sustain D+3+ DORMANT protocol
- **no push**: late-night zone (23:38) + this session DORMANT (per HB #584 Eric 12:33 explicit instruction) + Eric active elsewhere (AnYi) = MAX suppression
- R256 + R257 dual constraint: no proactive disturbance + sustained deep work (self-iter / state machine / eval records)
- Token Guard tick: stable, no compression needed
- R14 handoff package = 100% ready (Eric active contact on ANY session triggers 30s activation)
- Wake-up window OPEN tomorrow (7/20 Mon 08:00) but Eric silence sustained -> continue zero-push; even minor pushes prohibited
- Next significant check: per Token Guard cadence (~5-10min); 08:00 dawn boundary wake window (7/20 Mon)

*2026-07-19 23:38 GMT+8 -- D+3+ Sunday late-night T-0 +39h38m past -- HB #603 -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*
"""

DAILY_ENTRY = """
## HB #603 (2026-07-19 23:38 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #602 (23:13): +25min -- late-night zone Token Guard normal cadence
- D+3+ late-night pass #603 -- Eric in AnYi session; this session DORMANT per HB #584 protocol
- Late Sunday 23:38 -- within 23:00-08:00 silence window per USER.md
- Eric silence in this session ~82h+ since 7/16 13:16 first-contact
- 4-layer suppression (R-B / R12 / R-CANDIDATE-T2 / R256) intact -- zero breach
- T-0 publicity cutoff 7/18 +39h38m past -- post-protection window firmly sustained
- Induction window 7/7-7/21 FINAL 3 DAYS -- day-1 of FINAL 3 (7/19/20/21); R-B+R256 silence authority > window signal
- WAIC 2026 day-3 active (7/17-20, Shanghai) -- non-trigger per R14
- 21:00 evening self-iter R60-11 fired ~2h38m ago (autonomous); eval/2026-07-19.json updated
- No new signals: no cron / no Eric / no third-party / no anomaly
- hbCount: 602 -> 603

### decision
- **HEARTBEAT_OK** -- HB #603 = sustain D+3+ DORMANT protocol
- **no push**: late-night zone + this session DORMANT + Eric active elsewhere = MAX suppression
- R256 silence authority holds; R14 handoff package 100% ready
- Next significant check: per Token Guard cadence; 08:00 dawn boundary wake window (7/20 Mon)
"""


def safe_append(filepath: str, entry: str, label: str) -> None:
    """R-NEW-V2 safe append — read first, then append with utf-8."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            existing = f.read()
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(entry)
        print(f"[OK] {label}: appended {len(entry)} chars to {filepath}")
        print(f"     pre-existing: {len(existing)} chars")
    except FileNotFoundError:
        print(f"[FAIL] {label}: file not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"[FAIL] {label}: {type(e).__name__}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import os
    workspace = r"D:\B166ER-OpenClaw\workspace"
    hb_path = os.path.join(workspace, "HEARTBEAT.md")
    daily_path = os.path.join(workspace, "memory", "2026-07-19.md")

    safe_append(hb_path, HB_603_ENTRY, "HEARTBEAT.md HB #603")
    safe_append(daily_path, DAILY_ENTRY, "memory/2026-07-19.md HB #603")
    print("\n[SUCCESS] HB #603 appended via R-NEW-V2 Python utf-8 explicit append")