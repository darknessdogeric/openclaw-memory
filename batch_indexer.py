# -*- coding: utf-8 -*-
"""
batch_indexer.py - B166ER 知识库批量纳入器 (V2.0, 2026-10-25 重建)

以 scan_files.py 产出的 file_inventory.json 为输入，
把新文件/变更文件增量纳入 .kb_rag.db（复用 kb_rag.py 的分块 + FTS5 写入逻辑）。

用法:
  python batch_indexer.py                # 默认 limit=200
  python batch_indexer.py --limit 200
  python batch_indexer.py --ext .md      # 只纳入指定扩展名
  python batch_indexer.py --dry-run
"""
import os, sys, json, argparse, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
os.environ.setdefault("WORKSPACE", r"D:\B166ER-openclaw\workspace")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")

import kb_rag  # noqa: E402

WORKSPACE = kb_rag.WORKSPACE
INVENTORY = WORKSPACE / "memory" / "file_inventory.json"

# 与 kb_rag.SKIP_DIRS 一致 + 额外排除扫描噪音目录
EXTRA_SKIP = {
    ".backups", ".bak", ".scratch", ".tmp", ".cache", ".claude",
    "skills.bak-20260624-1447", ".archive-20260929", ".git_rebase_backup_20260914_171759",
    "obsidian-vault", "openhuman-eval", "refly-eval", "text-to-cad-extract",
    "open-design-repo", "toolbox", "last30days-skill", ".last30days-skill",
    # anyi/anyi-ops-kb 是 anyi-ops-kb 的近重复副本(1175 vs 1263 文件)，避免双份入库
    "anyi",
}


def load_inventory():
    if not INVENTORY.exists():
        print(f"[!] 清单不存在: {INVENTORY}，请先运行 scan_files.py")
        return []
    with open(INVENTORY, encoding="utf-8") as f:
        return json.load(f)


def rel_to_ws(p: Path):
    try:
        return str(p.relative_to(WORKSPACE))
    except ValueError:
        return None


def skipped(rel):
    parts = set(rel.split("\\"))
    if parts & EXTRA_SKIP:
        return True
    for part in parts:
        if part in kb_rag.SKIP_DIRS:
            return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=200)
    ap.add_argument("--ext", default=None, help="只纳入该扩展名，如 .md")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    inventory = load_inventory()
    if not inventory:
        return 1

    kb_rag.init_db()
    conn = kb_rag.get_db()
    known = {}
    for path, h in conn.execute("SELECT path, hash FROM files"):
        known[path] = h

    print(f"[纳入] 清单 {len(inventory)} 个文件；已索引 {len(known)} 个")

    candidates = []
    for item in inventory:
        rel = item.get("rel") or ""
        if not rel or skipped(rel):
            continue
        if args.ext and item["ext"] != args.ext:
            continue
        p = Path(item["path"])
        if not p.exists():
            continue
        if p.stat().st_size > kb_rag.MAX_FILE_SIZE:
            continue
        if rel in known:
            continue  # 已存在；变更检测在下方
        candidates.append((rel, p))

    # 已存在但内容变更的（hash 不同）
    changed = []
    for item in inventory:
        rel = item.get("rel") or ""
        if not rel or rel not in known or skipped(rel):
            continue
        p = Path(item["path"])
        if not p.exists() or p.stat().st_size > kb_rag.MAX_FILE_SIZE:
            continue
        if args.ext and item["ext"] != args.ext:
            continue
        try:
            if kb_rag.file_hash(p) != known[rel]:
                changed.append((rel, p))
        except Exception:
            pass

    todo = candidates + changed
    # 优先级: .md 优先, 其次按大小降序
    todo.sort(key=lambda x: (0 if x[0].endswith(".md") else 1, -x[1].stat().st_size))
    todo = todo[: args.limit]

    print(f"[纳入] 新增候选 {len(candidates)} / 变更 {len(changed)}；本次处理 {len(todo)} (limit={args.limit})")
    if args.dry_run:
        for rel, p in todo[:20]:
            print(f"   [dry] {rel}")
        conn.close()
        return 0

    t0 = time.time()
    ok, fail, chunks_total = 0, 0, 0
    for i, (rel, p) in enumerate(todo, 1):
        try:
            res = kb_rag.index_file(conn, p, use_vector=False)
            if res and res.get("chunks", 0) > 0:
                ok += 1
                chunks_total += res["chunks"]
            else:
                fail += 1
        except Exception as e:
            fail += 1
            print(f"   [err] {rel}: {e}")
        if i % 25 == 0:
            conn.commit()
    conn.commit()

    fc = conn.execute("SELECT COUNT(*) FROM files").fetchone()[0]
    cc = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    conn.close()

    print(f"[纳入] 完成: 成功 {ok} / 跳过或失败 {fail}；新增分块 {chunks_total}；耗时 {round(time.time()-t0,1)}s")
    print(f"[纳入] 索引库现状: {fc} 文件 / {cc} 分块")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
