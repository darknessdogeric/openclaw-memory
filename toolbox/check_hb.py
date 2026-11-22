import json
with open('memory/heartbeat-state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)
print(f"Current hbCount: {state['hbCount']}")
print(f"Current heartbeat: {state['lastChecks']['heartbeat']}")
