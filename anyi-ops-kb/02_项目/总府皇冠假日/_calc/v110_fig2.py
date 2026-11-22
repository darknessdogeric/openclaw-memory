# -*- coding: utf-8 -*-
"""v110：图2 按 Eric 指示重构——左图改为同级别国际联号对标（洲际体系同城携程挂牌价 vs 总府挂牌价 vs 实际成交 ADR），去掉 1,280 误读线"""
import io, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
FP = os.path.join(KB, "_calc", "v99_figs.py")
s = io.open(FP, encoding="utf-8").read()

# 定位并整段替换 图2 代码块
i = s.index("# ══ 图2 ")
j = s.index("# ══ 图3 ")
new = '''# ══ 图2 市场定位：同级别国际联号对标（携程口径） ══
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.2, 4.4))
# 左图：同属洲际体系在成都的携程挂牌价 vs 总府挂牌价 vs 总府实际成交 ADR
labs = ["温江皇冠\\n39㎡ 位置8.0", "西区皇冠\\n40㎡ 位置8.8", "天府皇冠\\n邻环球中心",
        "总府皇冠（本项目）\\n30㎡ 位置9.4", "总府实际成交 ADR\\n含服务费"]
lo = [698, 675, 730, 728, 412.09]
hi = [1098, 710, 1080, 1268, 412.09]
cl = ["#9DB4C0", "#9DB4C0", "#9DB4C0", C[0], "#A03A2E"]
xs = np.arange(len(labs))
for k in range(len(labs)):
    if hi[k] > lo[k]:
        ax1.bar(k, hi[k] - lo[k], bottom=lo[k], color=cl[k], width=.55)
        ax1.text(k - .30, hi[k] + 30, f"{lo[k]:,}", ha="right", fontsize=8.8, color=INK)
        ax1.text(k + .30, hi[k] + 30, f"{hi[k]:,}", ha="left", fontsize=8.8, color=INK)
    else:
        ax1.bar(k, 60, color=cl[k], width=.55)
        ax1.text(k, lo[k] + 60, f"{lo[k]:,.2f}", ha="center", fontsize=9.4, color=INK, weight="bold")
ax1.set_xticks(xs); ax1.set_xticklabels(labs, fontsize=8.4, color=INK)
ax1.set_ylim(0, 1500); ax1.set_ylabel("元/间晚", fontsize=10, color=MUT)
ax1.set_title("同品牌同城：携程挂牌价基本持平，但总府实际成交仅 412", fontsize=11.2, color=INK, weight="bold")
ax1.grid(axis="y", **GRID); [ax1.spines[x].set_visible(False) for x in ("top", "right")]
ax1.tick_params(colors=MUT, labelsize=9)
ax1.annotate("", xy=(4, 430), xytext=(4, 1180), arrowprops=dict(arrowstyle="<->", color="#A03A2E", lw=1.4))
ax1.text(3.62, 800, "缺口 768 元\\n（协议价与会员价结构）", fontsize=8.6, color="#A03A2E", ha="right", weight="bold")
ax1.text(0.02, .93, "结论：价格带由品牌与商圈决定，资产老旧未被折价；\\n改造的作用是把成交价推回挂牌带，而非抬高挂牌带",
         transform=ax1.transAxes, fontsize=8.4, color="#A03A2E", weight="bold")
# 右图：成都高端价格带阶梯（携程口径）
seg = [("居舍 Upper House", 142, 2000, 3000), ("尼依格罗 Niccolo", 230, 1400, 2800),
       ("瑞吉 St. Regis", 282, 1300, 1700), ("洲至奢选(棕榈泉)", 336, 1588, 2088),
       ("温江皇冠(同品牌对照)", 458, 698, 1098), ("总府皇冠(携程挂牌)", 402, 728, 1268)]
for k, (n, rm, a, b) in enumerate(seg):
    ax2.barh(k, b - a, left=a, color=C[0] if "总府" in n else "#6E93A8", alpha=.9, height=.55)
    ax2.text(a - 55, k, f"{a:,}–{b:,}", va="center", ha="right", fontsize=8.6, color=INK)
    ax2.text(3180, k, f"{n}\\n{rm} 间", va="center", fontsize=8.4, color=MUT)
ax2.axvline(412.09, color="#A03A2E", lw=2.0, ls="--")
ax2.text(430, 5.55, "总府实际成交 ADR 412.09（含服务费）", color="#A03A2E", fontsize=9, weight="bold")
ax2.set_yticks([]); ax2.set_xlim(0, 3400); ax2.invert_yaxis()
ax2.set_xlabel("元/间晚（携程口径挂牌价）", fontsize=10, color=MUT)
ax2.set_title("成都高端价格带阶梯：900 元以上供给不少于 1,632 间", fontsize=11.2, color=INK, weight="bold")
ax2.grid(axis="x", **GRID); [ax2.spines[x].set_visible(False) for x in ("top", "right", "left")]
ax2.tick_params(colors=MUT, labelsize=9)
save(fig, "fig02_市场定位与价格带.png")

'''
s = s[:i] + new + s[j:]
io.open(FP, "w", encoding="utf-8").write(s)
print("图2 已重构")
