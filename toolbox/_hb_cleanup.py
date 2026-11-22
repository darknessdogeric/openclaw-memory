"""Remove spurious HB entry."""
import pathlib, re

WORKSPACE = pathlib.Path(r"D:\B166ER-OpenClaw\workspace")
HEARTBEAT = WORKSPACE / "HEARTBEAT.md"

text = HEARTBEAT.read_text(encoding="utf-8")

# Find HB #615 entry (the spurious one)
pattern = r"\n## HB #615 \(.*?\n\*2026-07-19 17:30.*?\n\*"
m = re.search(pattern, text, re.DOTALL)
if m:
    new_text = text.replace(m.group(0), "\n")
    HEARTBEAT.write_text(new_text, encoding="utf-8")
    print("OK: removed HB #615")
else:
    # Try simpler split
    parts = text.split("\n## HB #615 (")
    if len(parts) == 2:
        # Keep only the part before
        head = parts[0]
        # Re-find the next HB entry
        after = parts[1]
        # Find the next "## HB #" in after
        next_hb_match = re.search(r"\n## HB #\d+", after)
        if next_hb_match:
            cleaned_after = after[next_hb_match.start():]
            new_text = head + "\n" + cleaned_after
        else:
            new_text = head.rstrip() + "\n"
        HEARTBEAT.write_text(new_text, encoding="utf-8")
        print("OK: removed HB #615 (fallback method)")
    else:
        print("NO HB #615 found to remove")
