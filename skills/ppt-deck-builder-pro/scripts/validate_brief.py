#!/usr/bin/env python3
"""
validate_brief.py — PPT 前置契约校验器 (Brief Contract v1.0)

用法:
    python scripts/validate_brief.py <plan.json>

退出码:
    0 = 全部通过, 可以进入生成阶段
    1 = 有未通过项, 禁止生成
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

VALID_PRESETS = {
    "startup_roadshow", "corporate_pro", "dark_blue_business", "light_consulting",
    "minimal_white", "gradient_modern", "elegant_chinese", "data_viz_pro",
    "creative_playful", "luxury_premium", "green_nature", "whiteboard_handdrawn",
    "custom",
}

AUDIENCE_FIELDS = ["who", "knows", "wants", "action"]

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("plan", help="plan json path")
    args = ap.parse_args()

    path = Path(args.plan)
    if not path.exists():
        print(f"[X] plan 不存在: {path}")
        return 1
    try:
        plan = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[X] plan 解析失败: {e}")
        return 1

    brief = plan.get("brief")
    if not isinstance(brief, dict):
        check("brief 块存在", False, "plan 顶层缺少 brief 对象 —— 必须先锁定 5 个参数")
        brief = {}

    # ① 页数
    total = brief.get("total_slides")
    if not isinstance(total, int) or total <= 0:
        check("① 页数已定", False, "brief.total_slides 缺失或非正整数 (默认 10)")
    else:
        if total < 5:
            check("① 页数已定", False, f"{total} 页过少, 建议 ≥5 或合并需求")
        elif total > 25:
            check("① 页数已定", False, f"{total} 页过多, 建议 ≤25 或拆成多份")
        else:
            check("① 页数已定", True, f"{total} 页")

    # ② 风格
    preset = brief.get("style_preset")
    if not preset:
        check("② 风格已定", False, "brief.style_preset 缺失 (不接受文字描述, 必须是 12 套具名之一)")
    elif preset not in VALID_PRESETS:
        check("② 风格已定", False, f"未知 preset '{preset}', 合法值见 references/template-selector.md")
    else:
        check("② 风格已定", True, preset)

    # ③ 听众
    aud = brief.get("audience")
    if not isinstance(aud, dict):
        check("③ 听众四项齐全", False, "brief.audience 缺失 (who/knows/wants/action)")
    else:
        missing = [f for f in AUDIENCE_FIELDS if not str(aud.get(f, "")).strip()]
        if missing:
            check("③ 听众四项齐全", False, f"缺: {', '.join(missing)}")
        else:
            check("③ 听众四项齐全", True, f"who={str(aud['who'])[:20]}")

    # ④ 必含章节
    secs = brief.get("required_sections")
    if not isinstance(secs, list) or len(secs) < 3:
        check("④ 必含章节 ≥3", False, f"required_sections 只有 {len(secs) if isinstance(secs, list) else 0} 项, 需 ≥3")
    else:
        bad = [s.get("name", "?") for s in secs if not str(s.get("conclusion", "")).strip()]
        if bad:
            check("④ 必含章节 ≥3", False, f"以下章节缺唯一结论: {', '.join(map(str, bad))}")
        else:
            sum_slides = sum(int(s.get("slides", 0) or 0) for s in secs)
            drift = abs(sum_slides - total) if isinstance(total, int) else 0
            if isinstance(total, int) and drift > max(1, total * 0.3):
                check("④ 必含章节 ≥3", False,
                      f"章节页数合计 {sum_slides} 与总页数 {total} 偏差过大 (>{max(1, total*0.3):.0f})")
            else:
                check("④ 必含章节 ≥3", True, f"{len(secs)} 章节 / 合计 {sum_slides} 页")

    # ⑤ 数据源
    ds = brief.get("data_sources")
    if not isinstance(ds, list) or not ds:
        check("⑤ 数据源 ≥1", False, "brief.data_sources 缺失 (内部/公开/联网/文档/示意)")
    else:
        bad = [d.get("type", "?") for d in ds if not str(d.get("where", "")).strip()]
        if bad:
            check("⑤ 数据源 ≥1", False, f"以下数据源缺来源位置: {', '.join(map(str, bad))}")
        else:
            check("⑤ 数据源 ≥1", True, f"{len(ds)} 项")

    # ⑥ 显式约束
    cons = brief.get("explicit_constraints")
    if not isinstance(cons, list) or not cons:
        check("⑥ 显式约束 ≥1", False, "brief.explicit_constraints 缺失 (至少写清合规/边界)")
    else:
        check("⑥ 显式约束 ≥1", True, f"{len(cons)} 条")

    # ⑦ 成功判据
    sc = str(brief.get("success_check", "")).strip()
    if not sc:
        check("⑦ 成功判据可验证", False, "brief.success_check 缺失 (必须是可判定的表述)")
    else:
        vague = [w for w in ("讲清楚", "做好", "漂亮", "专业", "有质感") if w in sc]
        if vague:
            check("⑦ 成功判据可验证", False, f"含不可判定词: {', '.join(vague)}")
        else:
            check("⑦ 成功判据可验证", True, sc[:40])

    # 输出
    print("=" * 66)
    print("BRIEF CONTRACT 校验  (Brief Contract v1.0)")
    print("=" * 66)
    for name, ok, detail in results:
        print(f"  [{'OK ' if ok else 'X  '}] {name:22} {detail}")
    passed = sum(1 for _, ok, _ in results if ok)
    print("-" * 66)
    print(f"  通过 {passed}/{len(results)}")
    if passed == len(results):
        print("  ✅ 可以进入生成阶段")
        return 0
    print("  ❌ 有未通过项 —— 回到提问, 不要开始生成")
    print("\n  提问模板见 references/brief-contract.md 第 3 节")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
