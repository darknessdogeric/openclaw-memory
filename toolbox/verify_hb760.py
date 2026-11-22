import json
with open('memory/heartbeat-state.json', 'r', encoding='utf-8') as f:
    s = json.load(f)
print('=== STATE FILE ===')
print('  hbCount:', s['hbCount'])
print('  silence:', s['silenceDuration_h'], 'h+ (global+session)')
print('  anyi:', s['ericActiveElsewhere_h'], 'h+')
print('  mode:', s['mode'])
print('  lastHB:', s['lastHB'])
with open('HEARTBEAT.md', 'r', encoding='utf-8') as f:
    h = f.read()
idx = h.rfind('## HB #760')
hb760 = h[idx:]
print()
print('=== HB #760 ENTRY VERIFICATION ===')
print('  Contains 120.75 (correct):', '120.75' in hb760)
print('  Contains 49.47 (correct):', '49.47' in hb760)
print('  Contains 691.75 (should be False):', '691.75' in hb760)
print('  Contains 135.13 (should be False):', '135.13' in hb760)
print('  Entry length:', len(hb760), 'chars')