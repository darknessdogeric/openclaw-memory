import re
from pathlib import Path

p = Path(r"D:\B166ER-OpenClaw\workspace\memory\2026-08-15.md")
text = p.read_text(encoding="utf-8")

# Remove my wrongly-numbered HB #2 and HB #3 entries (the last two appended)
# Pattern matches from newline + "### HB #2 (" through "HEARTBEAT_OK*"
pattern = re.compile(
    r"\n*### HB #(?:2|3) \(2026-08-15T17:59:42.*?HEARTBEAT_OK\*",
    re.DOTALL
)
new_text, n = pattern.subn("", text)
print(f"Removed {n} bad entries")

# Now also strip trailing whitespace
new_text = new_text.rstrip() + "\n"
p.write_text(new_text, encoding="utf-8")

# Show last 500 chars
print("---LAST 500---")
print(new_text[-500:])