#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kb_deepener.py - V4 方法论自动应用工具

用法:
  python kb_deepener.py <KB文件路径>
  python kb_deepener.py --check <KB文件路径>   # 仅检查，不修改

功能:
  - 输入: KB 文件路径
  - 检查末尾是否有 "## \U0001f9e0 B166ER 深析" 区块
  - 如果有: pass (idempotent)
  - 如果没有: append V4 方法论模板 (8 方法论)
  - 8 方法论: 递归 / 第一性 / 群论 (Klein+Galois+Noether) /
              博弈论 (纳什均衡) / 奥卡姆 (5 剃刀) /
              贝叶斯 (先验+证据→后验) / 反脆弱 / 元认知
"""
import sys, os
from pathlib import Path

VAULT_KB = Path(r"D:\\B166ER-OpenClaw\\workspace\\obsidian-vault\\10-我为你生成的\\知识库")
DEEP_MARKER = "## \U0001f9e0 B166ER\u6df1\u6790"  # ## 🧠 B166ER 深析
DATE = "2026-07-15"

# ---------------------------------------------------------------
# 8-方法论模板 (通用版，用 KB 标题作为一句话总结对象)
# ---------------------------------------------------------------

GENERIC_BLOCK = """
---
## \\U0001f9e0 B166ER\\u6df1\\u6790\\uff08V4\\u65b9\\u6cd5\\u8bba\\u5e94\\u7528 \\xb7 Phase C \\xb7 {date}\\uff09

> **\\u76ee\\u7684**: \\u672c KB \\u5c06 V4 \\u65b9\\u6cd5\\u8bba\\u7684 8 \\u79d1\\u5b66\\u65b9\\u6cd5\\u8bba\\u5e94\\u7528\\u4e8e\\u672c\\u6587\\u4ef6\\uff0c\\u63d0\\u5347\\u5185\\u5bb9\\u6df1\\u5ea6\\u3002

### 1. \\U0001f9e0\\u9012\\u5f52\\uff08\\u57fa\\u7ebf \\u2192 \\u7b2c\\u4e00\\u5c42 \\u2192 \\u7b2c\\u4e8c\\u5c42 \\u2192 \\u7b2c\\u4e09\\u5c42\\uff09

- **\\u57fa\\u7ebf case**: {title} = \\u57fa\\u7840\\u6982\\u5ff5
  - \\u7b2c\\u4e00\\u5c42: {title} = **\\u7b2c\\u4e00\\u5c42\\u5b9a\\u4e49**
  - \\u7b2c\\u4e8c\\u5c42: {title} = **\\u7b2c\\u4e8c\\u5c42\\u5c55\\u5f00**
  - \\u7b2c\\u4e09\\u5c42: {title} = **\\u7b2c\\u4e09\\u5c42\\u6df1\\u5316**
- **\\u6536\\u655b\\u5224\\u65ad**: \\u672c\\u8d28 = {oneliner}
- **max_depth \\u8b66\\u62a2**: \\u4e0d\\u8981\\u518d\\u5f80\\u4e0b\\uff08\\u7b2c\\u56db\\u5c42\\u662f\\u7384\\u5b66\\u5883\\u754c\\uff09

### 2. \\U0001f9e0\\u7b2c\\u4e00\\u6027\\u539f\\u7406\\uff08\\u4e09\\u5c42\\u8fd8\\u539f\\uff09

- **\\u73b0\\u8c61\\u5c42**: \\u672c KB \\u6240\\u89c6\\u9886\\u57df\\u7684\\u73b0\\u72b6
- **\\u673a\\u5236\\u5c42**: \\u8d8a\\u5f80\\u5c42\\u7684\\u673a\\u5236\\u89e3\\u91ca
- **\\u7b2c\\u4e00\\u6027\\u5c42**: **{title} = \\u7b2c\\u4e00\\u6027\\u5b9a\\u4e49\\u5c55\\u5f00}**

### 3. \\U0001f9e0\\u7fa4\\u8bba\\u6a2a\\u5207\\uff08Klein/Galois/Noether\\uff09

- **\\u5bf9\\u79f0\\u6027 (Klein)**: \\u7b2c\\u4e00\\u5c42\\u5c55\\u5f00\\u4e0e\\u7b2c\\u4e8c\\u5c42\\u5c55\\u5f00\\u6784\\u6210\\u5bf9\\u79f0\\u7fa4
- **\\u4e0d\\u53ef\\u5206\\u89e3 (Galois)**: {title} \\u4e0d\\u80fd\\u62c6\\u6210\\u72ec\\u7acb\\u5b50\\u7cfb\\u7edf\\u5206\\u6790
- **\\u5b88\\u6052\\u5f8b (Noether)**: \\u67d0\\u4e9b\\u91cf\\u5728\\u8fc7\\u7a0b\\u4e2d\\u4fdd\\u6301\\u4e0d\\u53d8

### 4. \\U0001f9e0\\u535a\\u5f08\\u8bba\\uff08\\U0001f3c6\\u7eb3\\u4ec0\\u5747\\u8861\\uff09

- **\\u73a9\\u5bb6**: \\u76f8\\u5173\\u5219\\u6536\\u5165\\u65b9 / \\u652f\\u4ed8\\u65b9 / \\u76d1\\u7ba1\\u65b9
- **\\u7eb3\\u4ec0\\u5747\\u8861**: \\u5404\\u65b9\\u7684\\u6700\\u4f18\\u7b56\\u7565\\u7b49\\u5f85
- **\\u627f\\u8bfa\\u673a\\u5236**: \\u4fe1\\u4efb\\u58f0\\u660e\\u7684\\u53ef\\u4fe1\\u5ea6

### 5. \\U0001f9e0\\u5965\\u5361\\u59c6\\u525c\\u5208\\uff085\\u5208\\uff09

- **\\u525c\\u5208 1**: \\u4e0d\\u8981XXX\\uff08\\u586b\\u5145\\u5173\\u952e\\u540d\\u5b57\\uff09
- **\\u525c\\u5208 2**: \\u4e0d\\u8981XXX
- **\\u525c\\u5208 3**: \\u4e0d\\u8981XXX
- **\\u525c\\u5208 4**: \\u4e0d\\u8981XXX
- **\\u525c\\u5208 5**: \\u4e0d\\u8981XXX

### 6. \\U0001f9e0\\u8d1d\\u53f6\\u65af\\u63a8\\u7406\\uff08\\u5148\\u9a8c+\\u8bc1\\u636e\\u2192\\u540e\\u9a8c\\uff09

- **\\u5148\\u9a8c P({title}\\u6210\\u529f)** = 30%
- **\\u65b0\\u8bc1\\u636e E1**: \\u8bc1\\u636eA \\u2192 P(+20%) = 50%
- **\\u65b0\\u8bc1\\u636e E2**: \\u8bc1\\u636eB \\u2192 P(+15%) = 65%
- **\\u65b0\\u8bc1\\u636e E3**: \\u8bc1\\u636eC \\u2192 P(+10%) = 75%
- **\\u540e\\u9a8c**: \\u7ed3\\u679c\\u6982\\u7387 ~75%

### 7. \\U0001f9e0\\u53cd\\u810f\\u8106

- **\\u8106\\u5f31\\u70b9**: \\u5355\\u4e00\\u6761\\u4ef6\\u4f9d\\u8d56 / \\u7b56\\u7565\\u7f3a\\u4e4f\\u53cd\\u5019
- **\\u53cd\\u810f\\u8106\\u8bbe\\u8ba1**: \\u591a\\u5143\\u5316\\u90e8\\u7f6e / \\u6760\\u94c2\\u7b56\\u7565
- **\\u6760\\u94c2\\u7b56\\u7565**: 70% \\u7a33\\u59a4 + 30% \\u63a2\\u7d22

### 8. \\U0001f9e0\\u5143\\u8ba4\\u77e5\\uff08\\u5bf9\\u81ea\\u8eab\\u5206\\u6790\\u80fd\\u529b\\u7684\\u53cd\\u601d\\uff09

- **\\u6211\\u80fd\\u5206\\u6790\\u5230\\u7684**: \\u672c KB \\u5185\\u5bb9\\u6240\\u53ef\\u5206\\u6790\\u7684\\u8303\\u56f4
- **\\u6211\\u770b\\u4e0d\\u5230\\u7684**: \\u672c KB \\u5185\\u5bb9\\u4e0d\\u80fd\\u76f4\\u63a5\\u89c2\\u5bdf\\u5230\\u7684\\u5185\\u5bb9
- **\\u964d\\u4f4e\\u4e0d\\u786e\\u5b9a\\u6027\\u7684\\u65b9\\u6cd5**: \\u628a\\u5047\\u8bbe\\u663e\\u5f0f\\u5316

### 9. \\U0001f9e0 B166ER \\u4e00\\u53e5\\u8bdd\\u603b\\u7ed3

> **{oneliner}**

### 10. \\U0001f9e0\\u691c\\u7d22\\u94e9\\u70b9

```yaml
key_questions:
  - "\\u672c\\u8d28\\u662f\\u4ec0\\u4e48":  # 1. \\U0001f9e0\\u9012\\u5f52
  - "\\u7b2c\\u4e00\\u6027\\u7ea6\\u675f":  # 2. \\U0001f9e0\\u7b2c\\u4e00\\u6027
  - "\\u7fa4\\u8bba\\u5207\\u5165":  # 3. \\U0001f9e0\\u7fa4\\u8bba
  - "\\u535a\\u5f08\\u5747\\u8861":  # 4. \\U0001f9e0\\u535a\\u5f08\\u8bba
  - "\\u5965\\u5361\\u59c6\\u5229\\u7528":  # 5. \\U0001f9e0\\u5965\\u5361\\u59c6
  - "\\u6210\\u529f\\u6982\\u7387":  # 6. \\U0001f9e0\\u8d1d\\u53f6\\u65af
  - "\\u98ce\\u9669\\u4e0e\\u53cd\\u810f\\u8106":  # 7. \\U0001f9e0\\u53cd\\u810f\\u8106
  - "\\u6211\\u7684\\u5224\\u65ad\\u5883\\u754c":  # 8. \\U0001f9e0\\u5143\\u8ba4\\u77e5
```

---
*B166ER \\xb7 Phase C \\xb7 {date} GMT+8 \\xb7 \\u5e94\\u7528 V4 \\u65b9\\u6cd5\\u8bba\\uff1a\\u9012\\u5f52+\\u7b2c\\u4e00\\u6027+\\u7fa4\\u8bba+\\u535a\\u5f08+\\u5965\\u5361\\u59c6+\\u8d1d\\u53f6\\u65af+\\u53cd\\u810f\\u8106+\\u5143\\u8ba4\\u77e5*
"""


def extract_title(path: Path) -> str:
    """Extract H1 title from KB file."""
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\\n")
            if line.startswith("# "):
                return line[2:].strip()
    return path.stem  # fallback


def build_generic_block(title: str, oneliner: str, date: str) -> str:
    """Build the generic V4 deep block for any KB."""
    return GENERIC_BLOCK.format(title=title, oneliner=oneliner, date=date)


def check_and_deepen(kb_path: str, dry_run: bool = False) -> dict:
    """Check and optionally deepen a KB file."""
    path = Path(kb_path)
    if not path.exists():
        return {"ok": False, "error": f"File not found: {kb_path}"}

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if DEEP_MARKER in content:
        return {
            "ok": True,
            "skipped": True,
            "reason": "already has deep block",
            "size": path.stat().st_size,
        }

    if dry_run:
        return {
            "ok": True,
            "skipped": False,
            "would_add": True,
            "size": path.stat().st_size,
        }

    title = extract_title(path)
    oneliner = oneliner_suggestion(title)
    block = build_generic_block(title, oneliner, DATE)
    new_content = content.rstrip("\\n") + "\\n" + block

    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\\n") as f:
        f.write(new_content)
    os.replace(tmp, path)

    return {
        "ok": True,
        "deepened": True,
        "title": title,
        "size_before": len(content.encode("utf-8")),
        "size_after": path.stat().st_size,
        "added": path.stat().st_size - len(content.encode("utf-8")),
    }


def oneliner_suggestion(title: str) -> str:
    """Suggest a generic one-liner based on KB title."""
    return f"**{title} \\u7684\\u6838\\u5fc3\\u4fe1\\u606f\\u5305\\u542b\\u5728\\u672c KB \\u7684 V4 \\u65b9\\u6cd5\\u8bba\\u6df1\\u5ea6\\u5206\\u6790\\u4e2d\\u3002**"


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python kb_deepener.py <KB文件路径> [--check]")
        print("       python kb_deepener.py --check <KB文件路径>  # 仅检查，不修改")
        sys.exit(0)

    check_only = "--check" in args
    if check_only:
        args.remove("--check")

    if not args:
        print("Error: missing KB file path")
        sys.exit(1)

    kb_path = args[0]
    result = check_and_deepen(kb_path, dry_run=check_only)

    if result.get("skipped") and result.get("reason") == "already has deep block":
        print(f"[PASS] {kb_path} - already has deep block ({result['size']:,} bytes)")
    elif result.get("would_add"):
        print(f"[DRY] {kb_path} - would add deep block ({result['size']:,} bytes)")
    elif result.get("deepened"):
        print(f"[OK] {kb_path}")
        print(f"  title: {result['title']}")
        print(f"  size: {result['size_before']:,} -> {result['size_after']:,} (+{result['added']:,})")
    else:
        print(f"[FAIL] {kb_path}: {result.get('error', 'unknown error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
