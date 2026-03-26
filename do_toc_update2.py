with open('C:/Users/ericz/.openclaw/workspace/memory/hotel-industry-knowledge-base.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find line range for 4.7.4 through 4.7.7
start_line = None
end_line = None
for i, line in enumerate(lines):
    if '     - 4.7.4 [营' in line:
        start_line = i
        print(f'Found 4.7.4 at line {i}: {line.rstrip()[:60]}')
    if '     - 4.8 [第' in line:
        end_line = i
        print(f'Found 4.8 at line {i}: {line.rstrip()[:60]}')
    if '     - 4.7.7 [工' in line:
        print(f'Found 4.7.7 at line {i}: {line.rstrip()[:60]}')
    if '   - 4.8 [第' in line:
        end_line = i
        print(f'Found 4.8 (3space) at line {i}: {line.rstrip()[:60]}')

print(f'Final: start_line={start_line}, end_line={end_line}')
