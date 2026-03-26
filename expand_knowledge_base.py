# This script will find insertion points and expand the 5 key topics

with open('C:/Users/ericz/.openclaw/workspace/memory/hotel-industry-knowledge-base.md', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Find insertion points
def find_insert_before(target_marker):
    for i, line in enumerate(lines):
        if target_marker in line and line.startswith('### '):
            return i
    return None

# Find CRM insertion point (before 4.7.2)
# Find where 4.7.1.4 CRM数据指标体系 ends
crm_end_idx = None
for i, line in enumerate(lines):
    if '4.7.2' in line and '直客预订' in line and '##' in line:
        crm_end_idx = i
        break

print(f'CRM insertion point (4.7.2 section start): line {crm_end_idx}')

# Find booking section insertion point (before 4.7.3)
booking_end_idx = None
for i, line in enumerate(lines):
    if '4.7.3' in line and '私域运营' in line and '##' in line:
        booking_end_idx = i
        break

print(f'Booking insertion point (4.7.3 section start): line {booking_end_idx}')

# Find private domain insertion point (before 4.7.4 OTA)
priv_end_idx = None
for i, line in enumerate(lines):
    if '4.7.4' in line and 'OTA' in line and '##' in line:
        priv_end_idx = i
        break

print(f'Private domain insertion point (4.7.4 section start): line {priv_end_idx}')

# Find OTA section - end of 4.7.4
ota_end_idx = None
for i, line in enumerate(lines):
    if '4.7.5' in line and '营销工具' in line and '##' in line:
        ota_end_idx = i
        break

print(f'OTA end point (4.7.5 section start): line {ota_end_idx}')
