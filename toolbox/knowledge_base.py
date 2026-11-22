# -*- coding: utf-8 -*-
"""
knowledge_base.py — Compatibility shim for `from knowledge_base import B166ERKnowledgeBase`

历史:
  - 早期 auto-indexer (Cron 8d8930ef + 652a1957) 使用 from knowledge_base import B166ERKnowledgeBase
  - 当前 KB 基础设施已重写为 kb_tools/ 工具链 (kb_scanner / kb_maintenance / kb_semantic_search / kb_index_incremental)
  - knowledge_base.py 源文件丢失,但 .pyc 缓存仍在
  - 旧 .pyc 在 Python 3.14 + 当前架构下不兼容

本 shim 作用:
  - 提供 B166ERKnowledgeBase 类 (满足旧 import 路径)
  - 将 index_file / scan / search 等操作 路由 到 kb_tools/ 实际模块
  - 让旧 cron 任务能继续运行,不报错

作者: B166ER · 2026-10-08
"""
import os
import sys
from pathlib import Path

WORKSPACE = Path(r'D:\B166ER-OpenClaw\workspace')
KB_TOOLS = WORKSPACE / 'toolbox' / 'kb_tools'

# 把 kb_tools 加进 sys.path
if str(KB_TOOLS) not in sys.path:
    sys.path.insert(0, str(KB_TOOLS))

# 重新导出 kb_semantic_search 的核心功能
try:
    from kb_semantic_search import (
        chunk_text,
        collect_documents,
        build_index,
        search as _search,
        stats,
    )
    _HAS_SEMANTIC = True
except Exception as _e:
    _HAS_SEMANTIC = False
    _IMPORT_ERR = _e

# 2026-10-26 修复:kb_index_incremental 导出的是 check()/apply(),不是 build_index()
#   → 旧 import 恒失败 → _HAS_INCREMENTAL 恒为 False
#   → index_file() 静默降级为「全量重建」(60k+ 块,约 30 分钟),周更任务实际跑不动
try:
    from kb_index_incremental import apply as _incremental_apply
    _HAS_INCREMENTAL = True
except Exception:
    _HAS_INCREMENTAL = False

_META_FILE = WORKSPACE / 'toolbox' / 'kb_tools' / 'index' / 'index_meta.json'


def _index_meta() -> dict:
    """读取索引元数据(总块数等),用于计算本次增量数"""
    try:
        import json
        raw = _META_FILE.read_text(encoding='utf-8')
        return json.loads(raw)
    except Exception:
        return {}


class B166ERKnowledgeBase:
    """
    兼容旧 API 的 KB 入口类
    所有方法路由到 kb_tools/ 实际模块
    """
    def __init__(self, workspace: str | None = None):
        self.workspace = Path(workspace) if workspace else WORKSPACE
        self.kb_tools = self.workspace / 'toolbox' / 'kb_tools'
        self.kb_dirs = [self.workspace / 'universal-kb', self.workspace / 'anyi-ops-kb']
        self.memory_dir = self.workspace / 'memory'
        self.index_dir = self.kb_tools / 'index'

    def scan(self):
        """扫描 KB,返回文档列表(等价于 kb_semantic_search.collect_documents)"""
        if _HAS_SEMANTIC:
            return collect_documents()
        raise RuntimeError(f'kb_semantic_search not importable: {_IMPORT_ERR}')

    def index_file(self, filepath: str, tags: list | None = None):
        """
        对单文件做增量索引(添加到现有索引)
        旧 API:index_file(filepath, tags=['auto-updated'])
        """
        fp = Path(filepath)
        if not fp.is_absolute():
            fp = self.workspace / filepath
        if not fp.exists():
            return {'ok': False, 'error': f'file not found: {fp}'}

        if _HAS_INCREMENTAL:
            try:
                before = _index_meta()
                _incremental_apply()
                after = _index_meta()
                added = after.get('total_chunks', 0) - before.get('total_chunks', 0)
                # tags 由旧 API 传入,底层索引器无标签概念 → 记录到元数据备查
                if tags:
                    after['last_index_tags'] = list(tags)
                    after['last_indexed_at'] = after.get('updated_at', '')
                    try:
                        import json
                        _META_FILE.write_text(
                            json.dumps(after, ensure_ascii=False, indent=2), encoding='utf-8')
                    except Exception:
                        pass
                return {'ok': True, 'indexed': added,
                        'total_chunks': after.get('total_chunks'),
                        'path': str(fp), 'tags': list(tags or [])}
            except Exception as e:
                return {'ok': False, 'error': str(e)}

        # 降级:全量重建
        if _HAS_SEMANTIC:
            try:
                n = build_index()
                return {'ok': True, 'indexed': n, 'path': str(fp), 'note': 'full rebuild'}
            except Exception as e:
                return {'ok': False, 'error': str(e)}
        return {'ok': False, 'error': 'no indexer available'}

    def index_all(self, full_rebuild: bool = False):
        """全量或增量索引"""
        if full_rebuild and _HAS_SEMANTIC:
            n = build_index()
            return {'ok': True, 'chunks': n, 'mode': 'full'}
        if _HAS_INCREMENTAL:
            _incremental_apply()
            meta = _index_meta()
            return {'ok': True, 'chunks': meta.get('total_chunks'),
                    'updated_at': meta.get('updated_at'), 'mode': 'incremental'}
        return {'ok': False, 'error': 'no indexer available'}

    def search(self, query: str, top_k: int = 5):
        if _HAS_SEMANTIC:
            return _search(query, top_k=top_k)
        raise RuntimeError(f'kb_semantic_search not importable: {_IMPORT_ERR}')

    def stats(self):
        if _HAS_SEMANTIC:
            return stats()
        return None


# 一些旧脚本可能直接调用的函数
def index_file(filepath: str, tags: list | None = None):
    return B166ERKnowledgeBase().index_file(filepath, tags)


def search(query: str, top_k: int = 5):
    return B166ERKnowledgeBase().search(query, top_k)


def scan():
    return B166ERKnowledgeBase().scan()


# 兼容旧 .pyc 缓存中可能调用的其它符号
def get_status():
    return {
        'workspace': str(WORKSPACE),
        'kb_tools': str(KB_TOOLS),
        'kb_tools_exists': KB_TOOLS.exists(),
        'semantic_search_available': _HAS_SEMANTIC,
        'incremental_available': _HAS_INCREMENTAL,
        'index_dir_exists': (KB_TOOLS / 'index').exists(),
    }


if __name__ == '__main__':
    import json
    print(json.dumps(get_status(), ensure_ascii=False, indent=2))