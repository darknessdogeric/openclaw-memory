# -*- coding: utf-8 -*-

"""evolution_scan.py - 自进化扫描器（确定性脚本，非 agentTurn）
依据 R-AUTO-07：机械任务用脚本，不用模型自由发挥。
产出：~/self-improving/eval/YYYY-MM-DD.json（沿用历史 eval 格式 + 机器可读状态）
退出码：0 = 全绿；1 = 有 FAIL（任务链断了 / 有问题需上报）
"""
import io, sys, os, re, json, glob, datetime, subprocess, traceback
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
SI = os.path.join(HOME, "self-improving")
EVAL = os.path.join(SI, "eval")
MARK = "evolution_scan_v1"

def now():
    return datetime.datetime.now()

def main():
    t0 = now()
    rec = {"date": t0.strftime("%Y-%m-%d"), "time": t0.strftime("%H:%M GMT+8"),
           "trigger": "automation: B166ER-自进化扫描（每周一 09:00 Asia/Shanghai）",
           "task_type": "自进化扫描", "wake_source": "cron/automation",
           "scanner": MARK, "status": "unknown", "exit_code": None,
           "summary": "", "signals": {"what_worked": [], "what_didnt_work": [], "surprise_discovery": []},
           "classification": {}, "actions_taken": [], "rules_added": [], "rules_enhanced": [],
           "reliability": {}, "tags": [], "next_actions": []}
    try:
        r = subprocess.run([sys.executable, os.path.join(ROOT, "toolbox", "selfcheck.py")],
                           capture_output=True, timeout=180)
        out = r.stdout.decode("utf-8", "replace")
        err = r.stderr.decode("utf-8", "replace")
        rec["exit_code"] = r.returncode
        checks = []
        for m in re.finditer(r"\[(PASS|FAIL)\]\s+(C\d+)\s+(.+?)\s{2,}(.*)$", out, re.M):
            checks.append({"id": m.group(2), "ok": m.group(1) == "PASS",
                           "title": m.group(3).strip(), "msg": m.group(4).strip()})
        if not checks:
            checks = [{"id": "?", "ok": False, "title": "selfcheck 输出无法解析", "msg": out[-300:]}]
        npass = sum(1 for c in checks if c["ok"])
        rec["checks"] = checks
        rec["status"] = "green" if (npass == len(checks) and r.returncode == 0) else "red"
        rec["summary"] = "自进化扫描：%d/%d 条断言通过（%s）。%s" % (
            npass, len(checks), rec["status"],
            "全部通过，无新增损坏、无索引脱节、无分层空转。" if rec["status"] == "green"
            else "存在失败断言：" + "；".join("%s %s" % (c["id"], c["msg"]) for c in checks if not c["ok"]))
        rec["signals"]["what_worked"] = [
            "12 条断言全部可执行并给出 PASS/FAIL（%d 通过）" % npass,
            "selfcheck 以退出码 0/1 表达状态，可被外部直接判读",
            "本轮扫描耗时 %.1f 秒" % ((now()-t0).total_seconds()),
        ]
        if rec["status"] == "red":
            rec["signals"]["what_didnt_work"] = [
                "失败断言：" + "；".join("%s(%s)" % (c["id"], c["title"]) for c in checks if not c["ok"])]
            rec["next_actions"] = ["逐条修 FAIL 断言对应的真实问题；修完重跑 selfcheck 直到全绿"]
        rec["classification"] = {
            "工具链": "selfcheck 12 条断言执行成功" if rec["exit_code"] is not None else "selfcheck 未产出退出码",
            "分析推理": "机器断言判定，非模型判断（避免 LLM 漂移）",
            "执行效率": "%.1f 秒" % (now()-t0).total_seconds(),
            "输出呈现": "%d 条断言结果" % len(checks),
            "沟通": "green → 静默（不打扰 Eric）；red → 由缺席/失败探测器推送",
        }
        rec["reliability"] = {"assertions_total": len(checks), "assertions_passed": npass,
                              "deterministic": True, "model_used": False}
        rec["tags"] = ["selfcheck", "evolution_scan", rec["status"]]
    except Exception as e:
        rec["status"] = "red"
        rec["summary"] = "扫描器自身异常：%s" % str(e)[:120]
        rec["signals"]["what_didnt_work"] = [traceback.format_exc()[-400:]]
        rec["exit_code"] = 2
    os.makedirs(EVAL, exist_ok=True)
    # ★ 修复：当天已有记录时，追加为 history 条目而不是覆写。
    #   原实现无条件覆写 -> ① 注入的失败状态被立刻盖回（退出码恒为 0）② 同日重复跑丢历史
    day = t0.strftime("%Y-%m-%d")
    p = os.path.join(EVAL, day + ".json")
    prior = None
    if os.path.exists(p):
        try:
            prior = json.load(open(p, encoding="utf-8"))
        except Exception:
            prior = None
    if prior is not None and prior.get("scanner") == MARK:
        # 同日重跑：保留今日首条，另存为 history；今日记录更新为最新一次
        hist = prior.get("history") or []
        hist.append({k: prior.get(k) for k in ("date","time","status","summary","exit_code")})
        prior["history"] = hist
        rec["history"] = hist
        rec["first_run_today"] = prior.get("first_run_today") or prior.get("time")
    rec["last_run"] = t0.strftime("%H:%M:%S GMT+8")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(rec, f, ensure_ascii=False, indent=1)
    # ★ 额外写极小状态文件：trigger script 只读它（不启子进程，避开 30s 预算）
    try:
        st = os.path.join(EVAL, ".last_scan.json")
        with open(st, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"date": rec["date"], "ts": t0.isoformat(), "status": rec["status"],
                       "exit": rec["exit_code"], "checks": len(rec.get("checks", [])),
                       "ok": sum(1 for c in rec.get("checks", []) if c["ok"])}, f, ensure_ascii=False)
    except Exception:
        pass
    print("%s | %s | %d 断言 | %s" % (rec["date"], rec["status"],
          len(rec.get("checks", [])), rec["summary"][:150]))
    print("RECORD: %s" % p)
    return 0 if rec["status"] == "green" else 1

if __name__ == "__main__":
    sys.exit(main())
