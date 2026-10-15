"""
B166ER 原子工具: file_atomic_write
===================================
原子文件写入。先写 .tmp，再 rename。防止 clobber（R-NEW-V2 教训：append 模式被改成 write 直接覆盖历史）。

契约: tools/schemas/file_atomic_write.schema.json
"""
import os
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any


def file_atomic_write(
    path: str,
    content: str,
    encoding: str = "utf-8",
    mode: Optional[int] = None,
    create_dirs: bool = True,
) -> Dict[str, Any]:
    """
    原子写入文件。临时文件 + rename，避免半写状态。

    Args:
        path: 目标文件路径
        content: 要写入的内容
        encoding: 文件编码
        mode: 写入后 chmod (e.g. 0o644)
        create_dirs: 是否自动创建父目录

    Returns:
        {
            "ok": bool,
            "path": str,
            "bytes_written": int,
            "error": str | None,
        }
    """
    p = Path(path)
    try:
        if create_dirs:
            p.parent.mkdir(parents=True, exist_ok=True)

        # 临时文件同目录下，rename 是 atomic（在同 filesystem）
        fd, tmp_path = tempfile.mkstemp(
            dir=str(p.parent),
            prefix=f".{p.name}.",
            suffix=".tmp",
        )
        try:
            with os.fdopen(fd, "w", encoding=encoding) as f:
                f.write(content)
                f.flush()
                os.fsync(f.fileno())  # 强制刷盘
            os.replace(tmp_path, str(p))  # atomic rename
        except Exception:
            # 清理 tmp
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise

        if mode is not None:
            os.chmod(str(p), mode)

        return {
            "ok": True,
            "path": str(p),
            "bytes_written": len(content.encode(encoding)),
            "error": None,
        }
    except Exception as e:
        return {
            "ok": False,
            "path": str(p),
            "bytes_written": 0,
            "error": f"{type(e).__name__}: {str(e)[:200]}",
        }


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        r = file_atomic_write(sys.argv[1], sys.argv[2])
        print(f"ok={r['ok']} bytes={r['bytes_written']} error={r['error']}")
    else:
        print("usage: python file_atomic_write.py <path> <content>")
