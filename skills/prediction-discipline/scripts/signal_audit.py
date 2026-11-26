# -*- coding: utf-8 -*-
"""signal_audit.py — 「这是信号还是噪声」判决器（西尔弗全书工具箱的可执行化）

★ 审一条结论会不会被证伪：先查多重比较，再查基率，再查效应量与样本量，
  再查过拟合，最后给出「该怎么说才诚实」的口径改写。
★ 用法:
    python signal_audit.py --tests 40 --alpha 0.05 --effect 0.3 --sd 1.0 --n 30 --prevalence 0.01
    python signal_audit.py --tests 1 --alpha 0.05 --effect 0.3 --sd 1.0 --n 30
"""
import sys, argparse, math

RED, YEL, GRN, DIM = "【红】", "【黄】", "【绿】", "　"


def holm_bonferroni(tests, alpha):
    thr = alpha / tests
    exp_fp = tests * alpha
    return thr, exp_fp


def power_two_sample(effect, sd, n, alpha=0.05):
    se = sd * math.sqrt(2.0 / n)
    z_a = 1.96
    z_b = 0.84
    pw = (abs(effect) / se - z_a) / z_b
    return max(0.0, pw)   # 负值夹到 0：样本量根本不足以检出该效应，不是「负检验力」


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tests", type=int, default=1, help="检验了多少个假设（多重比较数）")
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--effect", type=float, default=0.0, help="效应量（标准差单位）")
    ap.add_argument("--sd", type=float, default=1.0)
    ap.add_argument("--n", type=int, default=30, help="每组样本量")
    ap.add_argument("--prevalence", type=float, default=None, help="事件基础率（若结论是「检出/命中」）")
    ap.add_argument("--in-sample", action="store_true", help="是否用了同一批数据既找规律又验证")
    ap.add_argument("--narrative", type=str, default="", help="原始结论表述")
    a = ap.parse_args()

    print("=" * 78)
    print("信号 / 噪声判决器")
    if a.narrative:
        print("  原始结论：%s" % a.narrative)
    print("=" * 78)

    flags = []

    # 1) 多重比较
    thr, exp_fp = holm_bonferroni(a.tests, a.alpha)
    if a.tests > 1:
        sev = RED if a.tests >= 10 else YEL
        print("%s 多重比较：试了 %d 个假设" % (sev, a.tests))
        print("%s   单个假设阈值应从 %.3g 收紧到 %.4g（Holm/Bonferroni）" % (DIM, a.alpha, thr))
        print("%s   按 %.3g 的名义阈值，至少会出现 %.1f 个假阳性" % (DIM, a.alpha, exp_fp))
        flags.append("多重比较未校正" if a.tests >= 10 else "轻微多重比较风险")
    else:
        print("%s 多重比较：只检验了 1 个假设，无此风险" % GRN)

    # 2) 效应量与样本量
    if a.effect:
        pw = power_two_sample(a.effect, a.sd, a.n, a.alpha)
        sev = RED if pw < 0.5 else (YEL if pw < 0.8 else GRN)
        extra = ""
        if abs(a.effect) / (a.sd * math.sqrt(2.0 / a.n)) < 1.96:
            extra = "（样本量根本不足以检出该效应，检验力按 0 计）"
        print("%s 检验力：效应量 %.2f 个标准差 ｜ 每组 n=%d → 检验力约 %.0f%% %s" % (sev, a.effect, a.n, pw * 100, extra))
        if pw < 0.8:
            flags.append("样本量不足（检验力 %.0f%% < 80%%，阴性结果不可解释）" % (pw * 100))
        if abs(a.effect) < 0.2:
            flags.append("效应量很小（%.2f SD），即便显著也难有经营意义" % a.effect)

    # 3) 基率
    if a.prevalence is not None:
        sev = RED if a.prevalence < 0.05 else GRN
        print("%s 基率：事件基础率 %.4g" % (sev, a.prevalence))
        if a.prevalence < 0.02:
            flags.append("稀有事件：结论多半来自基率而非真信号，须报 PPV 而非命中率")
        else:
            print("%s   基础率够高，命中率不至于被基率吃掉" % DIM)

    # 4) 过拟合 / 样本外
    if a.in_sample:
        print("%s 过拟合风险：同一批数据既用来找规律又用来验证 —— 这是书里明说的失败模式" % RED)
        flags.append("非样本内验证（in-sample），无法排除过拟合")
    else:
        print("%s 验证方式：声明为样本外/留出验证" % GRN)

    print("-" * 78)
    if flags:
        print("结论：%s **不能按现在的说法当信号用** —— 有 %d 个待处理问题：" % (RED, len(flags)))
        for i, f in enumerate(flags, 1):
            print("   %d) %s" % (i, f))
    else:
        print("结论：%s 未发现结构性降级理由，可按信号处理（仍须带概率与置信区间）" % GRN)
    print("-" * 78)
    print("诚实口径改写模板：")
    print("  弱：「X 显著提升」→ 强：「在 %d 次检验、基础率 %.4g 的条件下，效应量约 %.2f SD，"
          % (a.tests, a.prevalence if a.prevalence is not None else 0, a.effect))
    print("        检验力约 %.0f%%，仍不足以排除噪声」" % (power_two_sample(a.effect, a.sd, a.n) * 100 if a.effect else 0))
    print("  ★ 书里的原则一：用概率方式思考 —— 每次下结论都写成「以 P 概率、在此区间内」。")
    return flags


if __name__ == "__main__":
    main()
