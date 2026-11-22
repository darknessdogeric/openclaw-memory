"""B166ER heartbeat tick — minimal stdout for cron pipelines."""
import json, time
from datetime import datetime, timezone, timedelta

ts = int(time.time())
shanghai = datetime.fromtimestamp(ts, tz=timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M GMT+8")
print(f"ts={ts}")
print(f"shanghai={shanghai}")
