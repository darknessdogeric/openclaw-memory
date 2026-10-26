# KB 每周维护报告

> 生成时间: 2026-10-26 10:39:20（自动）
> 执行方式: `python toolbox/kb_tools/kb_weekly_run.py`（确定性三段流水线）

## 执行结果

| 阶段 | 结果 | 耗时 |
|------|------|------|
| 扫描 | OK | |
| 维护 | OK | |
| 路由 | OK | |

## 关键指标

- scanned_files: 913
- empty_files: 0
- multi_versions: 9
- conflict_keywords: 4
- advisory_terms: 40
- todos: 0
- placeholder_terms: 18
- kb_candidates: 1285
- already_routed: 1285
- new_routes_needed: 0
- routing_status: OK
- moc_bytes: 128862

## 结论

- 路由表闭环完成，无待登记条目。
- 无 0 字节文件需要清理。
- 有 9 组多版本冲突需人工判定（脚本不自动合并）。
