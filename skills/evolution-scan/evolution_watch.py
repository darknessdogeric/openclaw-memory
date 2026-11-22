# -*- coding: utf-8 -*-

"""evolution_watch.py - 自进化扫描缺席/失败探测器（automation trigger 脚本）
依据 R-AUTO-09：产出链之外，必须有一条独立路径校验"是否按时来了"。
本脚本只读、只吐 JSON：{"fire": bool, "message": str, "state": {...}}
不写文件、不跑模型、毫秒级。
"""
import io, sys, os, re, json, glob, datetime
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
HOME = os.path.expanduser("~")
EVAL = os.path.join(HOME, "self-improving", "eval")
MARK = "evolution_scan_v1"
MAX_AGE_DAYS = 9          # 每周一跑 → 允许 9 天（跨两次）
FAIL_STREAK = 2           # 连续 2 次 red 才报（避免偶发噪声）

def main():
    today = datetime.datetime.now()
    recs = []
    for p in sorted(glob.glob(os.path.join(EVAL, "*.json"))):
        b = os.path.basename(p)
        if not re.match(r"^\d{4}-\d{2}-\d{2}\.json$", b):
            continue
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if d.get("scanner") != MARK:
            continue
        try:
            dd = datetime.datetime.strptime(d.get("date", ""), "%Y-%m-%d")
        except Exception:
            continue
        recs.append((dd, d.get("status", "unknown"), p))
    recs.sort(key=lambda x: x[0], reverse=True)
    state = {"last_seen": recs[0][0].strftime("%Y-%m-%d") if recs else None,
             "last_status": recs[0][1] if recs else None,
             "seen": len(recs),
             "fail_streak": 0}
    if not recs:
        # 首次运行：建立基线，不误报（尚无记录不等于缺席）
        print(json.dumps({"fire": False, "message": "", "state": state}, ensure_ascii=False))
        return 0
    latest = recs[0]
    age = (today.date() - latest[0].date()).days
    state["age_days"] = age
    # 连续 red 计数
    streak = 0
    for dd, st, p in recs:
        if st == "red":
            streak += 1
        else:
            break
    state["fail_streak"] = streak
    reasons = []
    if age > MAX_AGE_DAYS:
        reasons.append("自进化扫描已缺席 %d 天（阈值 %d 天，最后一次 %s）" % (age, MAX_AGE_DAYS, latest[0].strftime("%Y-%m-%d")))
    if streak >= FAIL_STREAK:
        reasons.append("自进化扫描连续 %d 次未全绿（最近记录 %s）" % (streak, latest[0].strftime("%Y-%m-%d")))
    if reasons:
        msg = ("【自进化链路告警】" + "；".join(reasons) +
               "。\n产出链存在但未被检测 —— 请检查 B166ER-自进化扫描 automation 是否仍在运行、"
               "以及 ~/self-improving/eval/ 是否仍能落盘。\n"
               "处置：先跑 `python toolbox/selfcheck.py` 看是否有 FAIL 断言；若有，按断言逐条修。")
        print(json.dumps({"fire": True, "message": msg, "state": state}, ensure_ascii=False))
    else:
        print(json.dumps({"fire": False, "message": "", "state": state}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    sys.exit(main())
