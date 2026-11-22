#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vault_safe_run.py - 强制隔离的 vault 操作接口

用途:
  所有 vault 重 IO 操作必须通过本接口，禁止在主会话直接调用。
  这是 R13 (vault 重 IO 必须走子会话) 的技术执行层。

安全检查:
  - sys.argv[1] 必须等于 'main' 才能执行
  - 否则报错并拒绝执行

使用方式:
  # 主会话不直接调用 (会报错)
  python vault_safe_run.py foo  -> ERROR

  # 通过子会话调用
  python vault_safe_run.py main -> OK (执行主逻辑)

  # 实际使用时通过 spawn/subagent 机制调用
  # openclaw gateway spawn -- python vault_safe_run.py main <command> <args...>
"""
import sys

REQUIRED_ARG = "main"

def main():
    if len(sys.argv) < 2 or sys.argv[1] != REQUIRED_ARG:
        print(
            "ERROR: vault_safe_run.py must be called from a sub-session.",
            file=sys.stderr,
        )
        print(
            "禁止在主会话直接调用 vault_safe_run.py。",
            file=sys.stderr,
        )
        print(
            "所有 vault 重 IO 操作必须通过子会话/spawn 机制调用。",
            file=sys.stderr,
        )
        print(
            "R13: vault 重 IO 必须走子会话。",
            file=sys.stderr,
        )
        print(
            f"Received argv: {sys.argv!r}",
            file=sys.stderr,
        )
        sys.exit(1)

    # 授权调用 - 执行主逻辑 (占位)
    print("[vault_safe_run.py] 主会话授权验证通过。")
    print(f"[vault_safe_run.py] 执行命令: {sys.argv[2:]}")

    # ---- 这里是占位逻辑 ----
    # 实际使用中，这里会替换为真正的 vault 操作：
    # - vault_sync.py update
    # - kb_deepener.py <path>
    # - 任何其他 vault 重 IO 操作
    # ------------------------

    print("[vault_safe_run.py] 操作完成 (占位模式)。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
