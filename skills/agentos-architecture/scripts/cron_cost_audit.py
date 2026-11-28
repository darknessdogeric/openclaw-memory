# -*- coding: utf-8 -*-
"""自动作业触发频率体检（配套《企业级AgentOS架构设计与工程实践》第 4 章 4.8「成本记录」）。

第 4 章那句话说得很直白：**不要等到账单来了才发现问题**。
本文把"账单"换算成"年触发次数"——因为 Agent 任务的成本几乎全在 token 上，
而 token 消耗的最直接驱动量就是**触发次数**。

判据（可调）：
  高频（≥ 每日）   → 必须说明它为什么需要这么频繁；无理由则应改为按事件触发
  中频（每周~每月） → 核对产出周期与触发周期是否一致
  低频（≤ 每季）   → 基本无问题

用法：
  python cron_cost_audit.py                 # 人类可读报告
  python cron_cost_audit.py --json          # 机器可读
  python cron_cost_audit.py --min-annual 100  # 只看年触发 ≥ 100 次的
"""
import io, sys, os, json, subprocess, argparse

CLI = r"C:\Users\ericz\AppData\Roaming\npm\openclaw.cmd"

# 高频作业的白名单：name 片段 -> 为什么它需要这么频繁
WHITELIST = {
    "自进化缺席告警": "每日扫描自进化状态文件，漏跑即失去告警意义；属别的工作线，未授权不改",
}


def cron_annual(expr):
    """返回 (年触发次数, 频率标签)。cron 五段：分 时 日 月 周。"""
    parts = (expr or "").split()
    if len(parts) != 5:
        return None, "未知"
    mi, hr, dom, mon, dow = parts

    def count(field, lo, hi):
        if field == "*":
            return hi - lo + 1
        if "/" in field:
            try:
                step = int(field.split("/")[1])
            except Exception:
                return 1
            return max(1, (hi - lo) // step + 1)
        vals = []
        for part in field.split(","):
            if "-" in part:
                a, b = part.split("-")
                try:
                    vals.extend(range(int(a), int(b) + 1))
                except Exception:
                    pass
            else:
                try:
                    vals.append(int(part))
                except Exception:
                    pass
        return max(1, len(vals))

    m = count(mi, 0, 59)
    h = count(hr, 0, 23)
    d = count(dom, 1, 31)
    mo = count(mon, 1, 12)
    dw = count(dow, 0, 7)
    dom_all = dom == "*"
    dow_all = dow == "*"
    if dom_all and dow_all:
        # 日与星期均通配 -> 每天
        per_year = m * h * 365
    elif dom_all:
        # 日通配、星期指定 -> 每周该星期几（一年 52 周，不是 12 个月！）
        per_year = m * h * dw * 52
    elif dow_all:
        # 星期通配、日指定 -> 每月该几天
        per_year = m * h * d * mo
    else:
        # 日与星期均指定 -> 一年约一两次
        per_year = max(1, m * h * dw)
    # 标签由次数反推，不由分支决定 —— 否则「次数」与「标签」会各说各话
    if per_year >= 300:
        kind = "每日"
    elif per_year >= 45:
        kind = "每周"
    elif per_year >= 12:
        kind = "按月"
    else:
        kind = "按年"
    return per_year, kind


def load_jobs():
    if not os.path.exists(CLI):
        return None, "openclaw CLI 不存在: " + CLI
    try:
        r = subprocess.run([CLI, "cron", "list", "--json"],
                           capture_output=True, timeout=120)
        raw = r.stdout.decode("utf-8", "replace")
        return json.loads(raw).get("jobs", []), None
    except Exception as e:
        return None, "读取失败: %s" % str(e)[:100]


def audit(min_annual=0):
    jobs, err = load_jobs()
    if err:
        return {"error": err, "rows": []}
    rows = []
    for j in jobs:
        sch = j.get("schedule") or {}
        if not j.get("enabled"):
            continue
        if sch.get("kind") != "cron":
            continue
        per_year, kind = cron_annual(sch.get("expr"))
        if per_year is None:
            continue
        name = j.get("name") or ""
        wl = None
        for k, why in WHITELIST.items():
            if k in name:
                wl = why
                break
        if per_year >= 365:
            verdict = "高频" + ("（已备案）" if wl else " ★需复核")
        elif per_year >= 52:
            verdict = "中频"
        elif per_year >= 4:
            verdict = "低频"
        else:
            verdict = "极低频"
        rows.append({"name": name, "expr": sch.get("expr"), "annual": per_year,
                     "kind": kind, "verdict": verdict, "whitelist": wl,
                     "nextRunAt": j.get("nextRunAt"),
                     "lastRunAt": j.get("lastRunAt"),
                     "lastDurationMs": j.get("lastDurationMs"),
                     "id": j.get("id")})
    rows.sort(key=lambda r: -r["annual"])
    return {"error": None, "rows": [r for r in rows if r["annual"] >= min_annual],
            "all_count": len(rows)}


def render(res):
    L = []
    L.append("=" * 76)
    L.append("自动作业触发频率体检 · 成本前置视角")
    L.append("依据《企业级AgentOS架构设计与工程实践》4.8「不要等到账单来了才发现问题」")
    L.append("=" * 76)
    if res.get("error"):
        L.append("★ " + res["error"])
        return "\n".join(L)
    L.append("")
    L.append("  年触发     频率      作业")
    for r in res["rows"]:
        L.append("  %8d  %-9s %s" % (r["annual"], r["kind"], r["name"][:46]))
        L.append("              %s" % r["expr"])
        if r["whitelist"]:
            L.append("              └ 备案：%s" % r["whitelist"])
        elif r["verdict"].endswith("★需复核"):
            L.append("              └ ★ 每日触发却无备案理由 —— 应改为按事件触发")
    L.append("")
    L.append("判据：≥每日 须有备案理由；每周~每月 核对产出周期；≤每季 基本无问题。")
    L.append("说明：年次数为按 cron 五段估算；token 消耗与触发次数正相关，但具体金额取决于")
    L.append("      上下文长度与 provider 计价，本工具不做金额假设。")
    return "\n".join(L)


SELFTEST = [
    # (表达式, 期望年次数, 期望标签)
    ("0 9 * * *", 365, "每日"),
    ("30 8 * * *", 365, "每日"),
    ("0 9 * * 1", 52, "每周"),
    ("0 10 10 * *", 12, "按月"),
    ("0 9 31 12 *", 1, "按年"),
    ("*/15 * * * *", 365 * 96, "每日"),
    ("0 0 1,15 * *", 24, "按月"),
]


def selftest():
    """判定逻辑必须经已知答案验证 —— 否则全绿也可能是假绿。"""
    bad = []
    for expr, want_n, want_k in SELFTEST:
        got_n, got_k = cron_annual(expr)
        ok = (got_n == want_n and got_k == want_k)
        if not ok:
            bad.append("%s 期望(%s,%s) 实际(%s,%s)" % (expr, want_n, want_k, got_n, got_k))
        print("  %s %-16s 期望 %5d/%-4s  实际 %5d/%-4s" % (
            "OK " if ok else "★错", expr, want_n, want_k, got_n, got_k))
    if bad:
        print("判定逻辑自测失败: %d 例" % len(bad))
        for b in bad:
            print("   " + b)
        return 1
    print("判定逻辑自测: 全部正确")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--min-annual", type=int, default=0)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    res = audit(a.min_annual)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(render(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
