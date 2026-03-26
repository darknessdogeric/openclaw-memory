import subprocess

result = subprocess.run(['cmd', '/c', 'dir F: /ad /b'], capture_output=True)
output = result.stdout.decode('utf-8', errors='replace')
folders = [f.strip() for f in output.strip().split('\r\n') if f.strip()]

with open('C:/Users/ericz/Desktop/folders_list.txt', 'w', encoding='utf-8') as f:
    for folder in folders:
        f.write(folder + '\n')

print(f'Found {len(folders)} folders')
