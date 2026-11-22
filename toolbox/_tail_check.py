import sys
path = r"D:\B166ER-OpenClaw\workspace\memory\2026-07-16.md"
with open(path, 'rb') as f:
    data = f.read()
print(f"Length: {len(data)} bytes")
print(f"Last 200 bytes (repr): {data[-200:].decode('utf-8', errors='replace')}")
print(f"Ends with newline: {data.endswith(b'\\n')}")
print(f"Last char (hex): {data[-1]:02x}")