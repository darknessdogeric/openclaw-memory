"""
Append HB #1127 entry to memory/2026-07-24.md (R-NEW-V2 compliant).
"""
import sys

MEM_PATH = r'D:\B166ER-OpenClaw\workspace\memory\2026-07-24.md'

NEW_ENTRY = """
## HB #1127 heartbeat (2026-07-24 00:59)
- Friday pre-dawn zone (00:59), Eric sleep zone, this session DORMANT
- D+8 = Execution phase day 4 -- observer mode sustained
- 7/24 D-Day T-8.02h watch: AnYi meeting TODAY MORNING 7/24 (T-~8h from typical 09:00 start)
- Triple Confluence Day 0 CLOSED (oil Scenario C verification window OPEN until 7/25 ~23h remaining)
- 6-layer suppression maintained (R-B / R12 / R-CANDIDATE-T2 / R256 / R257 / R258) -- zero breach
- Eric silent in THIS session ~179.72h+ since 7/16 13:16; active elsewhere (AnYi webchat) ~108.50h+
- R14 handoff package = 100% ready
- Decision: HEARTBEAT_OK / no push / this session DORMANT
"""

def main():
    # utf-8-sig read (handle BOM if present)
    with open(MEM_PATH, 'r', encoding='utf-8-sig', newline='') as f:
        existing = f.read()
    
    # Pre-state check
    assert 'HB #1123' in existing, "Pre-state check failed: HB #1123 missing"
    
    # Append
    new_content = existing + NEW_ENTRY
    
    with open(MEM_PATH, 'w', encoding='utf-8', newline='') as f:
        f.write(new_content)
    
    # Verify
    with open(MEM_PATH, 'r', encoding='utf-8-sig') as f:
        verify = f.read()
    
    if 'HB #1127' in verify and verify.endswith('DORMANT\n'):
        print('OK: HB #1127 appended to memory/2026-07-24.md')
        print(f'File size: {len(verify)} bytes')
    else:
        print('FAIL: post-write verification failed')
        print(f'Ends with: {verify[-50:]!r}')
        sys.exit(1)

if __name__ == '__main__':
    main()