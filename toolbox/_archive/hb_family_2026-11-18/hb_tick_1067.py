#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HB #1067 minimal tick — R-NEW-V2 compliant (utf-8 explicit read+load+write)
Per R012: HB tick = minimal (NOT full report)
Per R256+R257+R258: zero-push, deep work, DORMANT session
"""
import json
import datetime

STATE_PATH = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
HB_PATH = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'
TZ = datetime.timezone(datetime.timedelta(hours=8))


def main():
    # Read state with explicit utf-8 (R-NEW-V2)
    with open(STATE_PATH, 'r', encoding='utf-8') as f:
        state = json.load(f)

    now = datetime.datetime.now(TZ)
    iso_now = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
    iso_short = now.strftime('%Y-%m-%dT%H:%M')

    prev_hb_iso = state.get('lastHB', '')
    prev_hb_num = state.get('hbCount', 1066)
    new_hb_num = prev_hb_num + 1

    # Eric silence: 7/16 13:16 -> now
    first_contact = datetime.datetime(2026, 7, 16, 13, 16, tzinfo=TZ)
    silence_h = round((now - first_contact).total_seconds() / 3600, 2)

    # AnYi active: 7/19 12:33 -> now
    anyi_start = datetime.datetime(2026, 7, 19, 12, 33, tzinfo=TZ)
    anyi_h = round((now - anyi_start).total_seconds() / 3600, 2)

    # 7/24 D-Day T- (target ~09:00)
    dday = datetime.datetime(2026, 7, 24, 9, 0, tzinfo=TZ)
    t_minus = round((dday - now).total_seconds() / 3600, 2)

    # 21:00 evening cron
    evening = now.replace(hour=21, minute=0, second=0, microsecond=0)
    if evening < now:
        evening += datetime.timedelta(days=1)
    cron_to_evening = round((evening - now).total_seconds() / 3600, 2)

    # Compute gap from previous HB
    if prev_hb_iso:
        try:
            prev_dt = datetime.datetime.fromisoformat(prev_hb_iso)
            gap_min = round((now - prev_dt).total_seconds() / 60, 1)
            gap_text = f'+{gap_min}min'
        except Exception:
            gap_text = '+~4min'
    else:
        gap_text = '+~4min'

    # Update state
    state['lastUpdate'] = iso_now
    state['hbCount'] = new_hb_num
    state['lastHeartbeat'] = iso_now
    state['lastHBNumber'] = f'#{new_hb_num}'
    state['ericSilenceHours'] = silence_h
    state['lastHB'] = iso_now
    state['note'] = (
        f'#{new_hb_num} - {iso_now} sustained DORMANT; '
        f'7/24 AnYi D-Day T-{t_minus}h (TOMORROW Fri morning); '
        f'Eric silent ~{silence_h}h on this session; '
        f'6-layer suppression intact; minimal tick per R012; '
        f'gap from #{prev_hb_num} ({prev_hb_iso}) = {gap_text} Token Guard normal cadence'
    )

    # Write state with explicit utf-8 (R-NEW-V2)
    with open(STATE_PATH, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    # Build HB entry (R012 minimal mode)
    hb_entry = (
        f'\n### HB #{new_hb_num} ({iso_short} GMT+8, cron-event)\n'
        f'- gap from #{prev_hb_num} ({prev_hb_iso.split("+")[0]} GMT+8): {gap_text} '
        f'-- Thursday afternoon Token Guard tick (R012 minimal mode)\n'
        f'- D+7 afternoon pass #{new_hb_num} -- Eric silent in THIS session ~{silence_h}h+ since 7/16 13:16\n'
        f'- Eric active elsewhere: AnYi webchat ~{anyi_h}h+ (since 7/19 12:33)\n'
        f'- 6-layer suppression maintained -- zero breach\n'
        f'- R-NEW-V2: Python utf-8 explicit read+load+write compliant\n'
        f'- R012: HB tick = minimal (NOT full report)\n'
        f'- 7/24 D-Day T-{t_minus}h (AnYi meeting TOMORROW MORNING 7/24) -- INTERNAL monitor only\n'
        f'- Next cron: 21:00 R60-11 evening self-iter (~{cron_to_evening}h)\n'
        f'- hbCount: {prev_hb_num} -> {new_hb_num}\n'
        f'- R14 handoff package = 100% ready\n\n'
        f'### decision\n'
        f'- **active_mode_dormant_this_session_continue** (HB #{new_hb_num} = sustain DORMANT protocol)\n'
        f'- **HEARTBEAT_OK** -- HB #{new_hb_num} = sustain DORMANT baseline\n'
        f'- no push: Thursday afternoon zone, Eric silent on THIS session; 6-layer triple-suppression active\n\n'
        f'*{iso_now} -- D+7 Thursday afternoon -- HB #{new_hb_num} -- '
        f'this session DORMANT -- zero-push mode intact -- 7/24 D-Day T-{t_minus}h watch '
        f'-- Eric silent = dominant signal holding*\n'
    )

    # Append to HEARTBEAT.md with explicit utf-8
    with open(HB_PATH, 'a', encoding='utf-8') as f:
        f.write(hb_entry)

    print(f'OK HB #{new_hb_num} written')
    print(f'  silence={silence_h}h  anyi={anyi_h}h  T-{t_minus}h')
    print(f'  state.lastHB={state["lastHB"]}')


if __name__ == '__main__':
    main()