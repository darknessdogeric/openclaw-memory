# -*- coding: utf-8 -*-
"""Fix duplicate HB #578 by renumbering the 12:20 entry to HB #579."""
import json
from datetime import datetime, timezone, timedelta

hb_file = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'
state_file = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'

with open(hb_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the duplicate block by timestamp marker "12:20"
# The added block: "## HB #578 (2026-07-19 12:20 ..." through "*... 12:20 ...*"
marker_start = "## HB #578 (2026-07-19 12:20"
start_idx = content.rfind(marker_start)
if start_idx < 0:
    print('NOT_FOUND')
else:
    # Renumber this entry's #578 -> #579 (only in the duplicate block)
    # Get the entire block
    block_end = content.rfind('*2026-07-19 12:20')
    # End of "*...HB #578...*\n"
    block = content[start_idx:block_end + len('*2026-07-19 12:20 GMT+8 -- D+3 Sunday-noon T-0 +36.34h past -- HB #578 -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*')]

    # Renumber: heading, decision line, hbCount line, trailing star
    fixed = block.replace('HB #578 (2026-07-19 12:20', 'HB #579 (2026-07-19 12:20')
    fixed = fixed.replace('HB #578 = sustain #577', 'HB #579 = sustain #578')
    fixed = fixed.replace('hbCount: 577 -> 578', 'hbCount: 578 -> 579')
    fixed = fixed.replace('-- HB #578 -- zero-push mode intact', '-- HB #579 -- zero-push mode intact')

    new_content = content[:start_idx] + fixed + content[block_end + len('*2026-07-19 12:20 GMT+8 -- D+3 Sunday-noon T-0 +36.34h past -- HB #578 -- zero-push mode intact -- silence protocol holding -- R257 deep-work window active*'):]

    with open(hb_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    # Update state to hbCount=579, lastHB=579
    with open(state_file, 'r', encoding='utf-8-sig') as f:
        state = json.load(f)

    state['hbCount'] = 579
    state['lastHB'] = 579

    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    print(f'Renumbered entry. Old block length: {len(block)}, new: {len(fixed)}')
    print(f'Replacements made: heading + decision + hbCount + trailing star')
    print(f'State updated: hbCount=579, lastHB=579')
