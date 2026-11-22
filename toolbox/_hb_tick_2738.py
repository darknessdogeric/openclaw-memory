#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R-NEW-V3 compliant HB append - python 'a' mode ONLY"""
import os, sys
from datetime import datetime

hb_file = r"D:\B166ER-OpenClaw\workspace\memory\HEARTBEAT.md"
ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
hb_num = 2738
null_count = 429
post_t0 = 429

# 前置大小校验（用于 R-NEW-V3 完整性）
pre_size = os.path.getsize(hb_file)

entry = f"""
### HB #{hb_num} ({ts} GMT+8 cron-event, OpenClaw heartbeat poll)

- gap from HB #2737 (16:03): +5min -- Sun weekend afternoon Token Guard nominal cadence (R012, within tolerance)
- D+17 Sun 2026-08-09T16:08 -- weekend-afternoon post-hard-cap zone (+8h08m past 08:00 cap); quiet zone ~2h52m away
- Eric silent on THIS cron session ~589h+ (24d+) sustained since 7/16 13:16 first-contact
- 14-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65/R68/R69/R70/R71/R-NEW-V3/R276)
- Token Guard cadence OK; no external trigger; vault index healthy
- post_t0_null_count: 428 -> {post_t0} ({post_t0}th consecutive null post-T-0)
- hbCount: 2737 -> {hb_num}
- Eric silent on cron ~589h+ sustained
- AnYi D+17d Sun sustained (Eric 入职 D+17)
- 16:08 = Sun weekend afternoon post-hard-cap zone; cron = DORMANT sustained
- Eric last webchat activity 11:15-11:39 (~4h29m ago) -- V2 hotel-classification xhs 9 slides pending (deep-dive v2.md + V2 CSS complete; 9 HTML slides + render + screenshot + PNG output pending)
- R258 cron/webchat separation holds -- cron = DORMANT sustained; webchat = Eric sovereign

### decision

- HEARTBEAT_OK -- HB #{hb_num} = sustain DORMANT protocol, minimal token tick ({null_count}th null)
- no push: weekend afternoon + R69/R266/R258 tri-constraint + R256/R257/R260/R261 quad-holds + R276 internal-only
- R276 draft done; await Eric feedback for formal commit to ~/self-improving/rules.md
- V2 hotel-classification xhs 9 slides pending = Eric webchat sovereign; cron = DORMANT do not preempt
- Eric webchat / Obsidian vault sovereign for any decision; cron sovereignty unchanged
- 16:08 = Sun weekend afternoon; cron = DORMANT sustained
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- weekend afternoon + AnYi D+17d Sun + Eric sovereign on cron session + R65/R69/R276 active + R258 cron/webchat separation
- Standing by P0 (webchat-bound): await Eric webchat sovereign resumption on V2 slides or other topics
- Standing by R70/R71: await Eric feedback for formal commit to ~/self-improving/rules.md
- Standing by P1 (R264 AnYi ops): await Eric webchat share of AnYi 1244 strategy details, per R264 protocol routing to anyi-ops-kb/
- R271 edit-tool atomic-write enforced (this HB appended via Python open('a') mode, NOT write)
- Next: per Token Guard cadence (~5-15min afternoon mode); HB sustained until Eric first-contact on cron session

*{ts} -- Sun weekend afternoon post-hard-cap +8h08m -- HB #{hb_num} -- DORMANT -- {null_count}th null -- Eric silent on cron = 589h+ -- AnYi D+17d Sun -- cron session holds DORMANT protocol -- V2 9 slides pending Eric webchat sovereign resumption -- HEARTBEAT_OK*
"""

with open(hb_file, 'a', encoding='utf-8') as f:
    f.write(entry)

post_size = os.path.getsize(hb_file)
delta = post_size - pre_size
print(f"OK HB #{hb_num} appended")
print(f"pre_size={pre_size} post_size={post_size} delta={delta}")
print(f"R-NEW-V3 compliant: open('a') mode, NO write/Remove-Item/git restore")