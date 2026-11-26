# -*- coding: utf-8 -*-
"""base_rate.py — 基率陷阱、贝叶斯更新、效应稀释（西尔弗《信号与噪声》核心工具）

★ 本书最反直觉的一条：命中率高 ≠ 准确。基础率低时，再高的灵敏度也救不了你。
★ 用法:
    python base_rate.py screen --prevalence 0.01 --sens 0.99 --spec 0.99
    python base_rate.py bayes --prior 0.2 --lr 3.0
    python base_rate.py odds --prior 0.2 --sens 0.9 --spec 0.8
    python base_rate.py discovery --prevalence 0.001 --sens 0.9 --spec 0.9
    python base_rate.py dilute --coverage 0.08 --effect 0.25      # 效应稀释（酒店经营归因）
    python base_rate.py dilute --coverage 0.08 --effect 0.25 --baseline 0.46
"""
import sys, argparse


def screen(prevalence, sens, spec, n=10000):
    prev, se, sp = prevalence, sens, spec
    tp = n * prev * se
    fn = n * prev * (1 - se)
    fp = n * (1 - prev) * (1 - sp)
    tn = n * (1 - prev) * sp
    ppv = tp / (tp + fp) if (tp + fp) else 0.0
    npv = tn / (tn + fn) if (tn + fn) else 0.0
    print("=" * 74)
    print("筛查/检测情景：基础率 %.4g ｜ 灵敏度 %.4g ｜ 特异度 %.4g ｜ 样本 %d" % (prev, se, sp, n))
    print("-" * 74)
    print("  真阳性 %8.0f   假阴性 %8.0f" % (tp, fn))
    print("  假阳性 %8.0f   真阴性 %8.0f" % (fp, tn))
    print("-" * 74)
    print("  阳性预测值 PPV（阳性里真的是患者的比例）= %.2f%%" % (ppv * 100))
    print("  阴性预测值 NPV                              = %.2f%%" % (npv * 100))
    print("-" * 74)
    print("  ★ 只报「灵敏度 %.0f%%」不报基础率 = 拿 %.0f%% 的假阳性换来的"
          % (se * 100, (1 - sp) * 100))
    print("    命中率 %.1f%%，但阳性里只有 %.1f%% 是真的。" % (se * 100, ppv * 100))
    if prev < 0.02:
        print("  ★ 基础率低于 2%：稀有事件 + 高灵敏度的经典陷阱 ——")
        print("    「被噪声牵着鼻子走」就发生在这里。")
    same = (1 - prev) * sp
    print("  ★ 未检测人群里「本来就健康」的比例 = %.2f%%" % (same * 100))
    print("    检测的代价：把 %.2f%% 的健康者判成有病，与漏掉 %.2f%% 的病人比一比，"
          % ((1 - sp) * 100, (1 - se) * 100))
    print("    —— 这就是成本权衡，不是「谁更准」。")
    return ppv


def bayes(prior, lr):
    post_odds = prior / (1 - prior) * lr
    post = post_odds / (1 + post_odds)
    print("=" * 74)
    print("贝叶斯更新：先验 %.4g ｜ 似然比 LR %.4g" % (prior, lr))
    print("  先验赔率 %.4f  ×  LR %.4f  =  后验赔率 %.4f" % (prior / (1 - prior), lr, post_odds))
    print("  后验概率 = %.2f%%" % (post * 100))
    print("-" * 74)
    print("  ★ 似然比才是可迁移的量：换基础率就重算后验，结论不必重推。")
    print("    书里说：赌客靠似然比思考，不靠绝对概率。")
    return post


def odds(prior, sens, spec):
    lr = sens / (1 - spec)
    post_odds = prior / (1 - prior) * lr
    post = post_odds / (1 + post_odds)
    print("=" * 74)
    print("由灵敏度/特异度构造似然比：LR = %.4g / %.4g = %.4f" % (sens, 1 - spec, lr))
    print("先验 %.4g -> 后验 %.2f%%" % (prior, post * 100))
    return post


def discovery(prevalence, sens, spec):
    n = 100000
    tp = n * prevalence * sens
    fp = n * (1 - prevalence) * (1 - spec)
    print("=" * 74)
    print("发现率 / 漏检权衡（药物筛选式：基础率越低越难）")
    print("  样本 %d ｜ 基础率 %.4g ｜ 灵敏度 %.4g ｜ 特异度 %.4g" % (n, prevalence, sens, spec))
    print("  真阳性 %7.0f ｜ 假阳性 %7.0f" % (tp, fp))
    print("  → 每找到一个真的，要误 %.1f 个" % (fp / tp if tp else float("inf")))
    print("-" * 74)
    print("  ★ 书里的处方：预测不是为了「找到全部」，而是为了「让损失最小」。")
    print("    代价不对称时阈值就该移动 —— 漏报贵就压阈值，误报贵就抬阈值。")
    return fp / tp if tp else float("inf")


def dilute(coverage, effect, baseline=None):
    """效应稀释：定向动作只能作用于被覆盖的那部分人，整体贡献有上限。"""
    print("=" * 74)
    print("效应稀释（经营归因的基率约束）")
    print("  覆盖率（动作触达客群占比）= %.2f%%" % (coverage * 100))
    print("  组内效应（被触达客群的相对提升）= %.2f%%" % (effect * 100))
    print("-" * 74)
    overall = coverage * effect
    print("  ★ 整体效应上限 = 覆盖率 × 组内效应 = %.4f × %.4g = %.4g = %.2f%%"
          % (coverage, effect, overall, overall * 100))
    if baseline is not None:
        print("  折算到整体基数 %.4g → 绝对提升上限 %.4g（%.2f%% × %.2f%%）"
              % (baseline, overall * baseline, overall * 100, baseline * 100))
    print("-" * 74)
    print("  ★ 所以：若你观察到整体提升明显大于 %.2f%%，" % (overall * 100))
    print("    那它**不可能**只由这次动作解释 —— 要么覆盖了更多人，要么有别的驱动，")
    print("    要么「提升」本身是噪声或回归均值（用 regression_to_mean.py 查）。")
    print("  ★ 反过来：若整体提升只有 %.2f%%，而你宣称是定向动作的功劳，" % (overall * 100))
    print("    那也可能是把别处的噪声算到了它头上。")
    return overall


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["screen", "bayes", "odds", "discovery", "dilute"])
    ap.add_argument("--prevalence", type=float, default=0.01)
    ap.add_argument("--sens", type=float, default=0.99)
    ap.add_argument("--spec", type=float, default=0.99)
    ap.add_argument("--prior", type=float, default=0.2)
    ap.add_argument("--lr", type=float, default=3.0)
    ap.add_argument("--n", type=int, default=10000)
    ap.add_argument("--coverage", type=float, default=0.08)
    ap.add_argument("--effect", type=float, default=0.25)
    ap.add_argument("--baseline", type=float, default=None)
    a = ap.parse_args()
    if a.mode == "screen":
        screen(a.prevalence, a.sens, a.spec, a.n)
    elif a.mode == "bayes":
        bayes(a.prior, a.lr)
    elif a.mode == "odds":
        odds(a.prior, a.sens, a.spec)
    elif a.mode == "discovery":
        discovery(a.prevalence, a.sens, a.spec)
    else:
        dilute(a.coverage, a.effect, a.baseline)


if __name__ == "__main__":
    main()
