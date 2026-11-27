# -*- coding: utf-8 -*-
"""任务级 Trace 与审计事件分离记账（对应《企业级AgentOS架构设计与工程实践》第 8 章）。

核心纪律（8.5）：Trace 与 AuditEvent 必须分开。
  Trace       —— 发生了什么、耗时多少、状态如何（性能归因用）
  AuditEvent  —— 谁授权、影响了谁、何时、对哪类范围（权限追溯用）

混在一起，就既做不了性能归因，也做不了权限追溯。

用法：
  # 记录一个 span（任务级）
  python trace_log.py span --task 国堰审计 --step signal_audit --status ok --ms 820
  # 记录审计事件（授权/影响面）
  python trace_log.py audit --actor B166ER --action 口径对齐 --impact 5 --scope 知识库+桌面
  # 记录一次失败事故并回灌到回归集（8.12 事故回灌）
  python trace_log.py incident --task 自检 --symptom "三份自检并发争树" --fix "改为单份运行"
  # 查看
  python trace_log.py report
  python trace_log.py regressions
"""
import io, sys, os, json, argparse, datetime, uuid

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TRACE = os.path.join(ROOT, "data", "task_trace.jsonl")
AUDIT = os.path.join(ROOT, "data", "audit_events.jsonl")
REGRESS = os.path.join(ROOT, "data", "regression_cases.jsonl")


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def load(path):
    if not os.path.exists(path):
        return []
    out = []
    for ln in open(path, encoding="utf-8"):
        ln = ln.strip()
        if ln:
            try:
                out.append(json.loads(ln))
            except Exception:
                continue
    return out


def append(path, rec):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def cmd_span(a):
    rec = {"ts": now(), "trace_id": a.trace_id or uuid.uuid4().hex[:12],
           "task": a.task, "step": a.step, "status": a.status,
           "ms": int(a.ms) if a.ms else None,
           "detail": a.detail or ""}
    append(TRACE, rec)
    print("span  %-10s %-22s %-8s %s ms" % (rec["task"][:10], rec["step"][:22],
                                            rec["status"], rec["ms"] if rec["ms"] is not None else "-"))
    return 0


def cmd_audit(a):
    rec = {"ts": now(), "event_id": uuid.uuid4().hex[:12],
           "actor": a.actor, "action": a.action, "impact": int(a.impact or 0),
           "scope": a.scope or "", "decision": a.decision or "",
           "note": a.note or ""}
    append(AUDIT, rec)
    print("audit %-12s %-24s 影响面 %s  范围 %s" % (
        rec["actor"], rec["action"][:24], rec["impact"], rec["scope"]))
    return 0


def cmd_incident(a):
    rec = {"ts": now(), "case_id": uuid.uuid4().hex[:8],
           "task": a.task, "symptom": a.symptom, "fix": a.fix,
           "class": a.klass or "执行", "regression": True}
    append(REGRESS, rec)
    print("incident 已回灌 %s ｜ %s" % (rec["case_id"], rec["symptom"][:50]))
    return 0


def cmd_report(a):
    tr = load(TRACE)
    au = load(AUDIT)
    rg = load(REGRESS)
    print("=" * 72)
    print("任务级 Trace 与审计事件（两者分账，不混记）")
    print("=" * 72)
    print("")
    print("--- Trace（性能归因用）：%d 条 ---" % len(tr))
    agg = {}
    for r in tr:
        k = r.get("task", "?")
        a = agg.setdefault(k, [0, 0, 0])
        a[0] += 1
        a[1] += r.get("ms") or 0
        if r.get("status") == "fail":
            a[2] += 1
    for k, (n, ms, f) in sorted(agg.items(), key=lambda x: -x[1][1])[:12]:
        print("  %-30s %3d span  合计 %6d ms  失败 %d" % (k[:30], n, ms, f))
    if tr:
        tot = sum(r.get("ms") or 0 for r in tr)
        fails = len([r for r in tr if r.get("status") == "fail"])
        print("  合计耗时 %d ms ｜ 失败 span %d ｜ 失败率 %.1f%%" % (
            tot, fails, 100.0 * fails / len(tr)))
    print("")
    print("--- AuditEvent（权限追溯用）：%d 条 ---" % len(au))
    byactor = {}
    for r in au:
        byactor.setdefault(r.get("actor", "?"), [0, 0])
        byactor[r["actor"]][0] += 1
        byactor[r["actor"]][1] += int(r.get("impact") or 0)
    for k, (n, imp) in sorted(byactor.items(), key=lambda x: -x[1][1])[:12]:
        print("  %-16s %3d 次  累计影响面 %s" % (k[:16], n, imp))
    print("")
    print("--- 事故回灌回归集：%d 条 ---" % len(rg))
    for r in rg[-5:]:
        print("  [%s] %s ｜ 归因 %s" % (r.get("class"), r.get("symptom", "")[:44], r.get("fix", "")[:36]))
    print("")
    print("纪律：Trace 回答「发生了什么」，AuditEvent 回答「谁授权、影响了谁」。")
    print("      两者分开，才能既做性能归因，也做权限追溯。")
    return 0


def cmd_regressions(a):
    rg = load(REGRESS)
    if not rg:
        print("回归集为空:", REGRESS)
        return 0
    print("回归集 %d 条（每次修复都应回灌一条，否则同类错误会复发）" % len(rg))
    for r in rg:
        print("  [%s][%s] %s" % (r.get("class", "?"), r.get("case_id", "?"), r.get("symptom", "")))
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    s1 = sub.add_parser("span")
    s1.add_argument("--task", required=True)
    s1.add_argument("--step", required=True)
    s1.add_argument("--status", default="ok")
    s1.add_argument("--ms", default=None)
    s1.add_argument("--trace-id", dest="trace_id", default=None)
    s1.add_argument("--detail", default="")
    s1.set_defaults(func=cmd_span)
    s2 = sub.add_parser("audit")
    s2.add_argument("--actor", required=True)
    s2.add_argument("--action", required=True)
    s2.add_argument("--impact", default=0)
    s2.add_argument("--scope", default="")
    s2.add_argument("--decision", default="")
    s2.add_argument("--note", default="")
    s2.set_defaults(func=cmd_audit)
    s3 = sub.add_parser("incident")
    s3.add_argument("--task", required=True)
    s3.add_argument("--symptom", required=True)
    s3.add_argument("--fix", required=True)
    s3.add_argument("--class", dest="klass", default="")
    s3.set_defaults(func=cmd_incident)
    s4 = sub.add_parser("report")
    s4.set_defaults(func=cmd_report)
    s5 = sub.add_parser("regressions")
    s5.set_defaults(func=cmd_regressions)
    a = ap.parse_args()
    if not a.cmd:
        a.func = cmd_report
    sys.exit(a.func(a) or 0)


if __name__ == "__main__":
    main()
