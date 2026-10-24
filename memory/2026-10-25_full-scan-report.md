# B166ER 全盘扫描与自动纳入报告

> 生成时间: 2026-10-25 03:58:05（自动脚本 full_scan_run.py）
> 执行方式: `python full_scan_run.py`（确定性五段流水线）

## 一、执行结果

| 阶段 | 结果 | 耗时 |
|------|------|------|
| 扫描 | OK | 2.8s |
| 纳入 | OK | 1.1s |
| 索引统计 | OK | 1.8s |
| 路由登记 | OK | 0.2s |

## 二、关键指标

- scanned_files: 39680
- scanned_bytes: 0
- indexed_this_run: 30
- index_failed: 0
- index_files: 1901
- index_chunks: 114234
- index_kb: 34270
- last_indexed: 2026-10-25
- vector_engine: ✅ model2vec 256维
- kb_rag_ok: True
- kb_candidates: 168
- already_routed: 168
- new_routes_needed: 0
- routing_status: OK

## 三、结论

- 路由表闭环完成，无待登记条目。
- 索引库可用（1901 文件 / 114234 分块）。
- 向量引擎: ✅ model2vec 256维

---

> 路由登记唯一事实源: `skills/knowledge-base/routing-index.md`（`kb_routing_table.py --apply` 生成）。
> 注意：`kb_router.py` 已于 2026-07-11 删除，不存在。
