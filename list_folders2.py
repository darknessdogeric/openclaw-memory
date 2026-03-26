import subprocess
import os

result = subprocess.run(['cmd', '/c', 'dir F: /ad /b'], capture_output=True)
output = result.stdout.decode('utf-8', errors='replace')
folders = [f.strip() for f in output.strip().split('\r\n') if f.strip()]

# Print raw bytes
with open('C:/Users/ericz/.openclaw/workspace/folders_raw.txt', 'wb') as f:
    f.write(result.stdout)

# Print decoded
with open('C:/Users/ericz/.openclaw/workspace/folders_decoded.txt', 'w', encoding='utf-8') as f:
    for folder in folders:
        f.write(folder + '\n')

print('Done')
