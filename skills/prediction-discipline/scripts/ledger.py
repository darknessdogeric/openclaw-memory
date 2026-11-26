# -*- coding: utf-8 -*-
"""ledger.py — 预测台账（西尔弗原则二：今天的预测是你以后人生的第一个预测）

★ 每条预测都必须：问题可证伪 ｜ 给出概率 ｜ 写明基率 ｜ 写明结算日 ｜ 到期回来打分
★ 没有结算日的预测 = 不可证伪的断言 = 不算预测
★ 用法:
    python ledger.py add --q "问题" --p 0.55 --base-rate 0.40 --resolve 2027-01-15 --domain market --note "依据"
    python ledger.py settle --id 2026-11-26-01 --outcome 1 --note "实际：..."
    python ledger.py pending
    python ledger.py list
    python ledger.py score
    python ledger.py --path <file>   # 换台账路径
"""
import io, os, sys, json, argparse, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "..", "..", "data", "prediction_ledger.jsonl")
DEFAULT = os.path.abspath(DEFAULT)


def now_id():
    return datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")


def read(path):
    rows = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for ln in f:
                ln = ln.strip()
                if not ln or ln.startswith("#"):
                    continue
                rows.append(json.loads(ln))
    return rows


def write(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def cmd_add(a, path):
    rows = read(path)
    if not (0 < a.p < 1):
        print("★ 概率必须开区间，(0,1)；'一定会'/'绝不会'不是预测。"); return
    if not a.resolve:
        print("★ 必须给结算日（--resolve）。没有结算日的问题不可证伪。"); return
    if a.base_rate is None:
        print("★ 未填基率（--base-rate）。基率是判断'信号还是噪声'的锚；确实不知道就写 0 并在 note 说明。")
    r = {"id": a.id or now_id(), "date": datetime.date.today().isoformat(),
         "question": a.q, "p": a.p, "outcome": None, "resolved_date": a.resolve,
         "base_rate": a.base_rate, "domain": a.domain, "note": a.note or ""}
    rows.append(r)
    write(path, rows)
    print("已登记 [%s] p=%.2f ｜ 到期 %s ｜ %s" % (r["id"], r["p"], r["resolved_date"], r["question"][:56]))
    print("  台账：%s（累计 %d 条）" % (path, len(rows)))


def cmd_settle(a, path):
    rows = read(path)
    hit = 0
    for r in rows:
        if r.get("id") == a.id:
            r["outcome"] = a.outcome
            r["settled_date"] = datetime.date.today().isoformat()
            if a.note:
                r["settled_note"] = a.note
            hit += 1
    if not hit:
        print("★ 未找到 id=%s" % a.id); return
    write(path, rows)
    print("已结算 [%s] outcome=%s" % (a.id, a.outcome))


def cmd_pending(path):
    rows = read(path)
    pend = [r for r in rows if r.get("outcome") is None]
    print("待结算 %d 条" % len(pend))
    today = datetime.date.today().isoformat()
    for r in sorted(pend, key=lambda x: x.get("resolved_date", "9999")):
        due = r.get("resolved_date", "?")
        flag = " ★已到期" if due != "?" and due <= today else ""
        print("  [%s] p=%.2f 到期 %s%s  %s" % (r.get("id"), r["p"], due, flag, r.get("question", "")[:48]))


def cmd_list(path):
    rows = read(path)
    print("台账 %s ｜ 共 %d 条" % (path, len(rows)))
    for r in rows:
        print("  %s | p=%.2f | out=%s | base=%s | 到期 %s | %s" % (
            r.get("id"), r["p"], r.get("outcome"), r.get("base_rate"),
            r.get("resolved_date"), r.get("question", "")[:40]))


def cmd_score(path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("brier", os.path.join(HERE, "brier.py"))
    B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
    rows = read(path)
    settled = [(r["p"], r["outcome"]) for r in rows if r.get("outcome") is not None]
    if not settled:
        print("尚无已结算预测 —— 台账不产生分数就不算在跑。"); return
    bs = B.brier(settled)
    rel, res, unc = B.murphy(settled)
    print("已结算 %d 条 ｜ Brier %.4f ｜ 可靠性 %.4f ｜ 分辨力 %.4f ｜ 不确定性 %.4f"
          % (len(settled), bs, rel, res, unc))
    print("★ n=%d 样本极小，仅用于自查，不对外宣称校准水平。" % len(settled))
    B.ascii_reliability(B.reliability(settled))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["add", "settle", "pending", "list", "score"])
    ap.add_argument("--path", default=DEFAULT)
    ap.add_argument("--id", default=None)
    ap.add_argument("--q", default="")
    ap.add_argument("--p", type=float, default=0.5)
    ap.add_argument("--base-rate", type=float, default=None)
    ap.add_argument("--resolve", default=None)
    ap.add_argument("--domain", default="general")
    ap.add_argument("--note", default=None)
    ap.add_argument("--outcome", type=int, default=None)
    a = ap.parse_args()
    path = os.path.abspath(a.path)
    if a.cmd == "add":
        cmd_add(a, path)
    elif a.cmd == "settle":
        cmd_settle(a, path)
    elif a.cmd == "pending":
        cmd_pending(path)
    elif a.cmd == "list":
        cmd_list(path)
    else:
        cmd_score(path)


if __name__ == "__main__":
    main()
