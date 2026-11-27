# -*- coding: utf-8 -*-
"""模型成本台账（对应《企业级AgentOS架构设计与工程实践》第 4 章 4.8「成本记录」）。

原则：不要等到账单来了才���现问题。
每条记录必须含：谁花的、干了什么、产出了什么（价值标记）、token 数。

价值标记 value: "productive"（有到期结算/有交付物）| "empty"（空跑：无到期无产出）
空跑率是本工具的核心指标 —— 自动化最烧钱的地方不是干活，是每天空跑。

用法：
  python cost_ledger.py add --actor B166ER --task "台账结算" --tokens 678145 \
      --value productive --note "结算3条预测"
  python cost_ledger.py ingest --path data/model_cost_ledger.jsonl \
      --from-runs data/automation_runs.json
  python cost_ledger.py report --path data/model_cost_ledger.jsonl
  python cost_ledger.py review --path data/model_cost_ledger.jsonl
"""
import io, sys, os, json, argparse, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DEFAULT = os.path.join(ROOT, "data", "model_cost_ledger.jsonl")

FIELDS = ("ts", "actor", "task", "tokens", "value", "note")


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


def save(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def cmd_add(a):
    rows = load(a.path)
    rec = {
        "ts": now(),
        "actor": a.actor,
        "task": a.task,
        "tokens": int(a.tokens),
        "value": a.value,
        "note": a.note or "",
    }
    for k in FIELDS:
        if k not in rec:
            raise SystemExit("缺字段: " + k)
    if rec["value"] not in ("productive", "empty"):
        raise SystemExit("value 只能是 productive 或 empty")
    rows.append(rec)
    save(a.path, rows)
    print("已记账 %s ｜ tokens=%d ｜ %s" % (a.task, rec["tokens"], rec["value"]))
    return 0


def cmd_ingest(a):
    """从 automations runs 导出的 json 批量入账。"""
    if not os.path.exists(a.runs):
        raise SystemExit("找不到 runs 文件: " + a.runs)
    data = json.load(open(a.runs, encoding="utf-8"))
    entries = data.get("entries") if isinstance(data, dict) else data
    if not entries:
        print("runs 文件无条目")
        return 0
    rows = load(a.path)
    have = {(r.get("ts"), r.get("task"), r.get("tokens")) for r in rows}
    n = 0
    for e in entries:
        usage = e.get("usage") or {}
        tok = int(usage.get("total_tokens") or 0)
        if not tok:
            continue
        ts = datetime.datetime.fromtimestamp(e.get("runAtMs", 0) / 1000.0).isoformat(timespec="seconds")
        summ = (e.get("summary") or "").strip()
        # 空跑判定：summary 表示无到期/无产出
        empty = any(k in summ for k in ("无到期", "不结算", "无产出", "no due", "nothing"))
        task = e.get("jobName") or "automation"
        key = (ts, task, tok)
        if key in have:
            continue
        rows.append({"ts": ts, "actor": "automation", "task": task,
                     "tokens": tok, "value": "empty" if empty else "productive",
                     "note": summ[:200]})
        have.add(key)
        n += 1
    save(a.path, rows)
    print("入账 %d 条（跳过重复 %d）" % (n, len(entries) - n))
    return 0


def cmd_report(a):
    rows = load(a.path)
    if not rows:
        print("台账为空:", a.path)
        return 0
    total = sum(r["tokens"] for r in rows)
    empt = [r for r in rows if r.get("value") == "empty"]
    prod = [r for r in rows if r.get("value") == "productive"]
    e_tok = sum(r["tokens"] for r in empt)
    p_tok = sum(r["tokens"] for r in prod)
    print("=" * 70)
    print("模型成本台账 · 记录 %d 条" % len(rows))
    print("=" * 70)
    print("总 token            : %s" % format(total, ","))
    print("生产性 token        : %s  (%d 条)" % (format(p_tok, ","), len(prod)))
    print("空跑 token          : %s  (%d 条)" % (format(e_tok, ","), len(empt)))
    print("空跑率（按 token）  : %.1f%%" % (100.0 * e_tok / total if total else 0))
    print("空跑率（按条数）    : %.1f%%" % (100.0 * len(empt) / len(rows)))
    if prod:
        print("单条产出均值 token  : %s" % format(int(p_tok / len(prod)), ","))
    if empt:
        print("单次空跑均值 token  : %s" % format(int(e_tok / len(empt)), ","))
    print("")
    print("--- 按任务聚合（token 降序 前 12）---")
    agg = {}
    for r in rows:
        k = r.get("task", "?")
        agg.setdefault(k, [0, 0, 0])
        agg[k][0] += r["tokens"]
        agg[k][1] += 1
        if r.get("value") == "empty":
            agg[k][2] += 1
    for k, (t, n, e) in sorted(agg.items(), key=lambda x: -x[1][0])[:12]:
        print("  %12s  %4d 条  空跑 %4d  %s" % (format(t, ","), n, e, k[:44]))
    print("")
    print("说明：token 非金额。金额换算取决于 provider 计价与缓存策略，此处不做假设。")
    return 0


def cmd_review(a):
    """按第 4 章 4.10「模型网关接入业务前要检查什么」做一条复盘建议。"""
    rows = load(a.path)
    if not rows:
        print("台账为空")
        return 0
    total = sum(r["tokens"] for r in rows)
    empt = [r for r in rows if r.get("value") == "empty"]
    e_tok = sum(r["tokens"] for r in empt)
    rate = 100.0 * e_tok / total if total else 0
    print("★ 成本复盘")
    if rate >= 60:
        print("  空跑率 %.1f%% —— 偏高。建议：把周期任务改为**按到期事件触发**（一次性节点），" % rate)
        print("  而不是每天固定跑。净效果：空跑归零，成本降 %.0f%%。" % rate)
    elif rate >= 30:
        print("  空跑率 %.1f%% —— 中等。建议：核对任务触发条件是否可再收紧（错峰/按需）。" % rate)
    else:
        print("  空跑率 %.1f%% —— 健康。保持当前触发策略。" % rate)
    big = sorted(rows, key=lambda r: -r["tokens"])[:3]
    print("")
    print("--- 最贵的 3 条 ---")
    for r in big:
        print("  %12s  %s  %s" % (format(r["tokens"], ","), r.get("value"), r.get("task", "")[:50]))
    print("")
    print("★ 提醒（4.8）：fallback 与降级必须记录，否则账单来时无法归因。")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default=DEFAULT)
    sub = ap.add_subparsers(dest="cmd")
    s1 = sub.add_parser("add")
    s1.add_argument("--actor", required=True)
    s1.add_argument("--task", required=True)
    s1.add_argument("--tokens", required=True)
    s1.add_argument("--value", default="productive")
    s1.add_argument("--note", default="")
    s1.set_defaults(func=cmd_add)
    s2 = sub.add_parser("ingest")
    s2.add_argument("--from-runs", dest="runs", required=True)
    s2.set_defaults(func=cmd_ingest)
    s3 = sub.add_parser("report")
    s3.set_defaults(func=cmd_report)
    s4 = sub.add_parser("review")
    s4.set_defaults(func=cmd_review)
    a = ap.parse_args()
    if not a.cmd:
        a.func = cmd_report
    sys.exit(a.func(a) or 0)


if __name__ == "__main__":
    main()
