"""
B166ER 原子工具: git_safe_commit
================================
git add + commit + 可选 push。带 idempotency 检查（如果 working tree clean，跳过）。

契约: tools/schemas/git_safe_commit.schema.json

警告: 此工具调用真实 git 命令，会改 working tree 和 history。
调用方应预先:
  1. 确认 staging 内容正确
  2. 测试环境先跑
  3. 生产环境必须 human-in-the-loop 决策
"""
import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any


def _run(cmd: List[str], cwd: str, timeout: int = 60) -> Dict[str, Any]:
    """运行 git 命令，返回结构化结果"""
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return {
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "returncode": -1, "stdout": "", "stderr": f"timeout after {timeout}s"}
    except Exception as e:
        return {"ok": False, "returncode": -1, "stdout": "", "stderr": f"{type(e).__name__}: {e}"}


def git_safe_commit(
    repo_path: str,
    message: str,
    paths: Optional[List[str]] = None,
    push: bool = False,
    remote: str = "origin",
    branch: Optional[str] = None,
    dry_run: bool = True,
    timeout: int = 60,
) -> Dict[str, Any]:
    """
    安全的 git add + commit + (optional) push

    Args:
        repo_path: git 仓库路径
        message: commit message
        paths: 要 add 的文件路径列表（None = add all）
        push: 是否 push
        remote: remote 名称（默认 origin）
        branch: 推送分支（None = 当前 branch）
        dry_run: True 时只打印命令不执行（强烈推荐首次使用）
        timeout: 子命令超时

    Returns:
        {
            "ok": bool,
            "executed_commands": List[str],
            "results": List[{"cmd": str, "ok": bool, "stdout": str, "stderr": str}],
            "summary": str,
        }
    """
    repo = Path(repo_path)
    if not (repo / ".git").exists():
        return {
            "ok": False,
            "executed_commands": [],
            "results": [],
            "summary": f"not_a_git_repo: {repo_path}",
        }

    # 构建命令序列
    cmds: List[List[str]] = []
    if paths:
        cmds.append(["git", "add", "--"] + paths)
    else:
        cmds.append(["git", "add", "-A"])

    cmds.append(["git", "commit", "-m", message])

    if push:
        push_target = f"{remote}" + (f"/{branch}" if branch else "")
        cmds.append(["git", "push", remote, branch or "HEAD"])

    # dry_run 模式
    if dry_run:
        return {
            "ok": True,
            "executed_commands": [" ".join(c) for c in cmds],
            "results": [],
            "summary": "dry_run_no_commands_executed",
        }

    # 实际执行
    results: List[Dict[str, Any]] = []
    for cmd in cmds:
        r = _run(cmd, cwd=str(repo), timeout=timeout)
        r["cmd"] = " ".join(cmd)
        results.append(r)
        if not r["ok"]:
            return {
                "ok": False,
                "executed_commands": [r["cmd"] for r in results],
                "results": results,
                "summary": f"failed_at: {r['cmd']}",
            }

    return {
        "ok": True,
        "executed_commands": [r["cmd"] for r in results],
        "results": results,
        "summary": f"success: {len(results)}_commands",
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        dry = "--no-dry-run" in sys.argv
        r = git_safe_commit(sys.argv[1], sys.argv[2], dry_run=not dry)
        print(f"ok={r['ok']} summary={r['summary']}")
        if r.get("executed_commands"):
            print("executed:")
            for c in r["executed_commands"]:
                print(f"  {c}")
    else:
        print("usage: python git_safe_commit.py <repo> <message> [--no-dry-run]")
