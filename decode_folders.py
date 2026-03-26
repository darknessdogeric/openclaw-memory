import subprocess

result = subprocess.run(['cmd', '/c', 'dir F: /ad /b'], capture_output=True)
raw_bytes = result.stdout

# GBK decode
text = raw_bytes.decode('gbk', errors='replace')
lines = [l.strip() for l in text.strip().split('\r\n') if l.strip()]

# Write properly decoded output
with open('C:/Users/ericz/.openclaw/workspace/folders_decoded.txt', 'w', encoding='utf-8') as f:
    for line in lines:
        f.write(line + '\n')

print(f"Decoded {len(lines)} folders")
for i, line in enumerate(lines):
    print(f"{i+1}. {line}")
