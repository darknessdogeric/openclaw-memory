# -*- coding: utf-8 -*-
"""HB #1157 fix: move entry from position 99356 to position 0 (top of file)."""
import io
import sys

HB_PATH = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'

with open(HB_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the misplaced HB #1157 entry
marker = '## HB #1157 (06:02 GMT+8'
idx = content.find(marker)
print(f'#1157 misplaced at position: {idx}')

if idx < 0:
    print('ERROR: HB #1157 not found')
    sys.exit(1)

# The entry ends at the next HB # (e.g., ## HB #1148 or similar) or end-of-file
# Find the next '## HB #' after this one
next_hb_idx = content.find('\n## HB #', idx + 1)
if next_hb_idx < 0:
    # Find the closing '*' line which marks end of decision section
    next_hb_idx = content.find('\n---', idx)
if next_hb_idx < 0:
    # Just take a reasonable amount
    next_hb_idx = idx + 5000  # fallback

# Extract the HB #1157 entry (including leading whitespace/newlines)
# Find the start of the entry block (might have leading newline)
# Backtrack to find the start of the ## heading
entry_start = idx
# Walk back to remove any leading newlines that precede ## HB #1157
while entry_start > 0 and content[entry_start - 1] in ' \t\r\n':
    entry_start -= 1
# Now find the ## start
hash_pos = content.rfind('## HB #1157', 0, idx + 5)
if hash_pos >= 0:
    entry_start = hash_pos

# Find the end (the trailing * line + maybe newlines)
# The entry is the ## block + decision + closing *
# Find the LAST * at the end of the closing line for this entry
# Looking at format: ends with "*... -- this session DORMANT ...*\n\n"
# Find next ## HB # to bound it
end_marker_idx = content.find('## HB #', idx + len('## HB #1157'))
if end_marker_idx < 0:
    # Just keep until end of file
    entry_end = len(content)
else:
    # The end is just before this next ## HB #
    # But we want to keep a single blank line before the next HB
    # Actually, let's just take from entry_start to the position right before the next ## HB #
    entry_end = end_marker_idx
    # Walk back to remove any trailing whitespace before next HB
    while entry_end > entry_start and content[entry_end - 1] in ' \t':
        entry_end -= 1

extracted = content[entry_start:entry_end]
print(f'Extracted length: {len(extracted)}')
print(f'Extracted start: {extracted[:80]}')
print(f'Extracted end: {extracted[-100:]}')

# Remove the misplaced entry from content
new_content_no_1157 = content[:entry_start] + content[entry_end:]

# Now insert at position 0 (very top)
# Make sure new_content starts with the entry followed by a single blank line
final = extracted.strip() + '\n\n' + new_content_no_1157.lstrip('\n')

with open(HB_PATH, 'w', encoding='utf-8') as f:
    f.write(final)

# Verify
with open(HB_PATH, 'r', encoding='utf-8') as f:
    check = f.read()
print(f'After fix - HB #1157 at: {check.find("## HB #1157")}')
print(f'After fix - HB #1156 at: {check.find("## HB #1156")}')
print(f'After fix - first 100 chars: {check[:100]}')