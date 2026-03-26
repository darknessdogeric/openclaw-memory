import subprocess

result = subprocess.run(['cmd', '/c', 'dir F: /ad /b'], capture_output=True)
raw_bytes = result.stdout

# Try to detect encoding
# First few bytes tell us the encoding
first_line = raw_bytes.split(b'\r\n')[1] if len(raw_bytes.split(b'\r\n')) > 1 else b''
print(f"First folder name bytes: {first_line[:20]}")

# The bytes like \xc4\xea are GBK for 年 (0xc4 0xea)
# But in UTF-8, Chinese chars are 3-4 bytes
# Let's try GBK first
try:
    text = raw_bytes.decode('gbk')
    print("GBK decode works!")
    print(text)
except:
    print("GBK failed")

# Also try to decode line by line
lines = raw_bytes.split(b'\r\n')
print(f"\nTotal folders: {len([l for l in lines if l])}")
