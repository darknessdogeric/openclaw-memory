import json, os, time
state = {
    "note": "HB #3353; Sat 21:22 weekend-EVENING-quiet-zone (+2h22m past 19:00); R69 Day 23/30; HEARTBEAT_OK; +3min after HB #3352; DORMANT held (1906th consecutive); Eric silent ~30d; AnYi D+23d Sat; no external push",
    "trendradar_rss_through": "2026-08-14",
    "trendradar_health_checked_at": "2026-08-14T18:54:00+08:00",
    "lastHbTime": "2026-08-15T21:22:00+08:00",
    "hbCount": 3353,
    "last_tick_format": "minimal-token-tick",
    "post_t0_null_count": 1906,
    "posture": "DORMANT",
    "session": "cron:315657b9-fc80-4b94-a853-404e3955f7a0",
    "last_update_epoch": 1786800120,
    "workday_zone": "weekend-EVENING-quiet-zone (+2h22m past 19:00)",
    "trendradar_hot_news_through": "2026-08-12",
    "lastHBContext": "Sat 21:22 weekend-EVENING-quiet-zone (+2h22m past 19:00). DORMANT held sustained. HB #3353. R69 Day 23/30. AnYi D+23d Sat. Eric silent ~30d cron. 16-layer suppression holds.",
    "cronSession": "DORMANT",
    "lastDecision": "HEARTBEAT_OK",
    "zone": "weekend-EVENING-quiet-zone (+2h22m past 19:00)",
    "nullCount": 1906,
    "trendradar_health": "healthy v6.10.0",
    "trendradar_rss_fresh": True,
    "anyi_day": 23,
    "r69_silence": "Day 23/30 (expires 2026-08-30)",
    "trendradar_data_through": "2026-08-12",
    "eric_webchat_idle_min": 742
}
tmp = r'D:\B166ER-OpenClaw\workspace\memory\.heartbeat-state.json.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
os.replace(tmp, r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json')
print("state.json updated atomically:", state['hbCount'], "nullCount", state['nullCount'])