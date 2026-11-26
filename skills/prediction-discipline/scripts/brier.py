# -*- coding: utf-8 -*-
"""brier.py — 预测台账结算与校准诊断（西尔弗原则二的执行器）

★ 原则二：今天的预测是你以后人生的第一个预测 —— 所以每条预测都要留痕、到期结算。
★ 校准：说 70% 就该有 70% 兑现。Brier 越低越好；可靠性图越贴对角线越诚实。
★ 用法:
    python brier.py --ledger <path.jsonl>              # 结算全部已到期条目
    python brier.py --ledger <path.jsonl> --show-all    # 含未结算
    python brier.py --demo                              # 内置自检样例
"""
import sys, json, os, argparse
from collections import defaultdict

LEDGER_HINT = "ledger: 每行一个 JSON，字段 id/date/question/p/outcome/resolved_date/base_rate/domain"


def load(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln or ln.startswith("#"):
                continue
            rows.append(json.loads(ln))
    return rows


def brier(pairs):
    n = len(pairs)
    if not n:
        return None
    return sum((p - o) ** 2 for p, o in pairs) / n


def murphy(pairs):
    """BS = reliability - resolution + uncertainty（Murphy 1973）"""
    n = len(pairs)
    base = sum(o for _, o in pairs) / n
    bins = defaultdict(list)
    for p, o in pairs:
        bins[min(9, int(p * 10))].append((p, o))
    rel = 0.0
    res = 0.0
    for k, v in bins.items():
        nk = len(v)
        pk = sum(p for p, _ in v) / nk
        ok = sum(o for _, o in v) / nk
        rel += nk / n * (pk - ok) ** 2
        res += nk / n * (ok - base) ** 2
    unc = base * (1 - base)
    return rel, res, unc


def reliability(pairs, bins=10):
    out = []
    d = defaultdict(list)
    for p, o in pairs:
        d[min(bins - 1, int(p * bins))].append((p, o))
    for k in range(bins):
        v = d.get(k, [])
        if not v:
            continue
        mp = sum(p for p, _ in v) / len(v)
        mo = sum(o for _, o in v) / len(v)
        out.append((k, len(v), mp, mo))
    return out


def ascii_reliability(rows, w=34):
    """可靠可靠性图：网格法，不越界"""
    print("  可靠性图（纵轴=实际兑现率，横轴=说出口的概率；点落在对角线上=完美校准）")
    grid = [[" "] * w for _ in range(11)]
    for _, n, mp, mo in rows:
        col = min(w - 1, max(0, int(mp * w)))
        row = 10 - min(10, max(0, int(mo * 11)))
        grid[row][col] = "*"
    print("  +" + "-" * w + "+")
    for r in range(10, -1, -1):
        print("  |" + "".join(grid[r]) + "|  %3d%%" % (r * 10))
    print("  +" + "-" * w + "+")
    print("   " + "".join(("|" if i % 5 == 0 else " ") for i in range(w)))
    print("   0%                              100%")
    print("   （* 落在对角线附近=校准良好；低于对角线=过自信；高于=欠自信）")
    for k, n, mp, mo in rows:
        gap = mo - mp
        tag = "过自信" if gap < -0.05 else ("欠自信" if gap > 0.05 else "准")
        print("   桶 %2d  n=%-3d 说 %.2f 实 %.2f  差 %+.2f  %s" % (k, n, mp, mo, gap, tag))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", type=str, default=None)
    ap.add_argument("--show-all", action="store_true")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()

    if a.demo:
        demo = [(0.2, 0), (0.2, 0), (0.2, 1),
                (0.6, 1), (0.6, 0), (0.6, 1),
                (0.9, 1), (0.9, 1), (0.9, 0)]
        pairs = demo
        print("【自检样例】9 条已结算预测")
        bs = brier(pairs)
        rel, res, unc = murphy(pairs)
        print("  Brier = %.4f（越低越好；恒猜 0.5 且 50/50 则为 0.25）" % bs)
        print("  Murphy 分解：可靠性 %.4f（越低越好）｜分辨力 %.4f（越高越好）｜不确定性 %.4f" % (rel, res, unc))
        print("  校验：%.4f - %.4f + %.4f = %.4f" % (rel, res, unc, rel - res + unc))
        ascii_reliability(reliability(pairs))
        return

    if not a.ledger:
        print("用法：python brier.py --ledger <path.jsonl> [--show-all]")
        print(LEDGER_HINT)
        return
    if not os.path.exists(a.ledger):
        print("台账不存在：%s" % a.ledger)
        return
    rows = load(a.ledger)
    settled = [(r["p"], r["outcome"]) for r in rows if r.get("outcome") is not None]
    pending = [r for r in rows if r.get("outcome") is None]
    print("=" * 76)
    print("预测台账：%s" % a.ledger)
    print("  总条数 %d ｜ 已结算 %d ｜ 待结算 %d" % (len(rows), len(settled), len(pending)))
    print("=" * 76)
    if settled:
        bs = brier(settled)
        rel, res, unc = murphy(settled)
        print("  Brier = %.4f（越低越好）" % bs)
        print("  可靠性 %.4f ｜ 分辨力 %.4f ｜ 不确定性 %.4f" % (rel, res, unc))
        print("  ★ 样本量提醒：n=%d 条的 Brier 噪声很大，只用于自查，不可对外宣称校准水平。" % len(settled))
        print("-" * 76)
        ascii_reliability(reliability(settled))
    else:
        print("  尚无已结算预测 —— 台账不产生分数就不算在跑。")
    if pending:
        print("-" * 76)
        print("  待结算（到期必须回来打分，否则等于没预测）：")
        for r in pending:
            print("   [%s] p=%.2f  到期 %s  %s" % (r.get("id", "?"), r["p"],
                                                  r.get("resolved_date", "?"),
                                                  r.get("question", "")[:44]))
    if a.show_all:
        print("-" * 76)
        print("  全部条目：")
        for r in rows:
            print("   %s | p=%.2f | out=%s | base=%s | %s" % (
                r.get("id", "?"), r["p"], r.get("outcome"), r.get("base_rate"),
                r.get("question", "")[:40]))


if __name__ == "__main__":
    main()
