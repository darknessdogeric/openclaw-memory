# -*- coding: utf-8 -*-
"""regression_to_mean.py — 回归均值检验（西尔弗《信号与噪声》第四章·棒球）

★ 核心命题：挑出「极端差」的那批人去做干预，下次他们自然变好 —— 这不是干预的功劳。
★ E[z2|z1] = r · z1（r = 两次测量的相关性）
★ 用法:
    python regression_to_mean.py --r 0.6 --z1 -2
    python regression_to_mean.py --r 0.6 --series 0.5,1.2,1.8,2.4
    python regression_to_mean.py --r 0.6 --series 0.5,1.2,1.8,2.4 --n 200
"""
import sys, argparse, math


def expect(r, z1):
    z2 = r * z1
    print("=" * 72)
    print("回归均值推演：可靠性 r=%.3g ｜ 首次标准化分 z1=%+.3g" % (r, z1))
    print("  E[z2|z1] = r × z1 = %.3g × (%+.3g) = %+.3g" % (r, z1, z2))
    print("  → 期望「自发」改善 = %.3g 个标准差" % abs(z2 - z1))
    print("-" * 72)
    print("  ★ 判定：如果你只对最差的一批做了干预、且没有对照组，")
    print("    那么上面这个改善幅度，**不需要任何干预也会出现**。")
    print("    要证明干预有效，必须有：① 同样差的对照组 ② 或把基线分数作为协变量回归")
    print("    ③ 或多次基线测量提升信度 ④ 或同时看「最好的一批」是否等量下滑")
    return z2


def from_series(r, series, n=200):
    xs = series[:-1]
    ys = series[1:]
    m = len(xs)
    mx = sum(xs) / m
    my = sum(ys) / m
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    rhat = num / den if den else float("nan")
    print("=" * 72)
    print("由观测序列估算可靠性 r = %.3f（m=%d 对）" % (rhat, m))
    print("  序列:", ", ".join("%.2f" % v for v in series))
    print("-" * 72)
    z1 = (series[-1] - mx) / (math.sqrt(sum((x - mx) ** 2 for x in xs) / m) or 1)
    print("  最后一次相对基线均值偏离约 %+.2f 个标准差" % z1)
    z2 = rhat * z1
    print("  下一轮期望值 %+.2f 个标准差（自发回归 %.2f 个标准差）" % (z2, abs(z2 - z1)))
    print("-" * 72)
    print("  ★ 阈值口径：若此前按「低于 %.2f」筛人干预，下一轮均值会自然回到 %.2f 附近。"
          % (my + z1 * (math.sqrt(sum((x - mx) ** 2 for x in xs) / m) or 1), my))
    print("    没有对照组，就会把回归均值误记成「我们的方案有效」。")
    print("  ★ 样本量提醒：m=%d 对观测估 r 的噪声很大，结论应写成「不足以判定」，不是「有效」。" % m)
    return rhat


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--r", type=float, default=0.6)
    ap.add_argument("--z1", type=float, default=-2.0)
    ap.add_argument("--series", type=str, default=None)
    ap.add_argument("--n", type=int, default=200)
    a = ap.parse_args()
    if a.series:
        s = [float(x) for x in a.series.split(",")]
        from_series(a.r, s, a.n)
    else:
        expect(a.r, a.z1)


if __name__ == "__main__":
    main()
