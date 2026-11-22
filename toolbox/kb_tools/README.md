# B166ER KB 工具链 — README

> **位置**: `D:\B166ER-OpenClaw\workspace\toolbox\kb_tools\`
> **作者**: B166ER
> **版本**: v1.0 · 2026-09-18

---

## 🎯 工具链目标

**解决 Eric 8:33 提的"知识库融合纠错并沉淀 + 随时调用"**:
- ✅ **融合**:自动识别同名多版本
- ✅ **纠错**:自动修订 R66 遗留虚构内容
- ✅ **沉淀**:自动维护 KB 总览索引(MOC)
- ✅ **调用**:14,740 块语义索引,<1 秒响应

---

## 📦 工具清单(6 个 + README)

### 1. `kb_scanner.py` — KB 扫描器

**功能**:扫描所有 .md 文件,提取元数据,发现问题。

```bash
cd D:\B166ER-OpenClaw\workspace\toolbox\kb_tools
python kb_scanner.py
```

**输出**:
- `scan_report.json` — 完整元数据 + 问题清单
- `KB_MOC.md` — KB 总览索引(自动生成)

**检测项**:
- ✅ 0 字节文件
- ✅ 多版本冲突(同名 vX.Y)
- ✅ 关键词冲突(R66 已清理关键词残留)
- ✅ TODO/FIXME 标记

---

### 2. `kb_maintenance.py` — 自动维护器

**功能**:基于扫描报告,执行维护操作。

```bash
python kb_maintenance.py
```

**执行**:
- ✅ 删除 0 字节文件
- ✅ 生成 KB_MOC.md
- ✅ 报告未归档旧版本
- ✅ 分析关键词冲突

---

### 3. `kb_auto_r66.py` — R66 修订工具(批量清理虚构)

**功能**:检测并清理虚构内容(阿联酋/UAE/本奥米尔/350亿授信 等)。

```bash
# Dry-run(只报告不修改)
python kb_auto_r66.py

# Apply(实际修改)
python kb_auto_r66.py apply
```

**策略**:
- 保留 R66 修订日志(标记本身应保留)
- 替换虚构事实为 `[R66已清理]`
- 表格行:替换关键词
- 段落行:整行替换

---

### 4. `kb_auto_archive.py` — 旧版本归档工具

**功能**:将同名旧版本移到 `_归档_/` 子目录,只保留最新。

```bash
python kb_auto_archive.py       # Dry-run
python kb_auto_archive.py apply  # 实际归档
```

---

### 5. `kb_semantic_search.py` — 语义检索器

**功能**:基于 sentence-transformers 的本地语义检索(无需网络)。

```bash
# 首次索引(7-8 分钟,一次性)
python kb_semantic_search.py index

# 搜索(返回 top-5)
python kb_semantic_search.py search "你的问题"

# 统计
python kb_semantic_search.py stats
```

**索引数据**:
- 总文档块:**15,299**(增量索引后)
- 索引大小:21 MB(embeddings.npz 21 MB + docs.pkl 17 MB)
- 模型:sentence-transformers/all-MiniLM-L6-v2(已下载,90MB)
- 维度:384

**实测召回率**(用 Eric 最近 5 个问题测试):
| 查询 | Top-1 命中 | 评分 |
|------|-----------|------|
| 中国酒店行业 数据来源 STR PMS OTA | 05_8大数据源报告 | 0.715 ✅ |
| 巴蜀文化主题酒店 1244 在地文化 | 培训PPT03 | 0.712 ✅ |
| 花园宾馆改造 一店一品一主题 KPI | 花园宾馆项目方案 | 0.689 ✅ |
| 地方国资酒店集团集体发牌 | CHANGELOG.md | 0.644 ⚠️ |
| 安逸集团1244战略 轻重分离 | AHL 内部预审稿 | 0.624 ⚠️ |

**5/5 命中相关领域**,3/5 完美命中。

---

### 6. `kb_index_incremental.py` — 增量索引器 ⭐

**功能**:只索引新增/修改的文件,避免全量重建(7 分钟 → 2 分钟)。

```bash
# 检查变化
python kb_index_incremental.py

# 实际增量索引
python kb_index_incremental.py apply
```

**原理**:
1. 扫描 KB 所有 .md,计算 SHA256
2. 对比已有索引,识别新增/修改/删除
3. 只对变化的文件生成 embeddings
4. 合并到现有 embeddings.npz

**性能**:
- 全量重建:7-8 分钟
- **增量索引**(60 个变化文件):**~2 分钟**

---

## 🔄 工具链执行流程(标准动作)

```
Eric 任何问题
  ↓
1. 先 search("...")  → 找 5 个最相关片段
2. 基于知识基础回答
3. 工作产出 → toolbox/.tmp/<日期>_<任务>/
4. 完成 → 归档到 anyi-ops-kb / universal-kb
5. 归档后 → 跑 kb_scanner.py 检查一致性
6. 发现问题 → 跑 kb_auto_r66.py / kb_auto_archive.py
7. KB 显著变化 → 重建 kb_semantic_search.py 索引
```

---

## 📊 工具链成果(自迭代 v3.0)

| 维度 | 初始 | 当前 | 变化 |
|------|------|------|------|
| 0 字节文件 | 1 | 0 | -1 |
| 关键词冲突(虚构) | 85 | 0(真实残留) | **-85** |
| 多版本冲突 | 11 | 0 | **-11** |
| 语义索引 | 0 | 14,740 块 | **+14,740** |
| KB MOC 总览 | 无 | 76 KB | **+76 KB** |

---

## ⚠️ 已知限制

1. **英文模型对中文召回率有上限** — 准确率约 60-70%
2. **全量索引耗时长** — 7 分钟(需改进为增量索引)
3. **PowerShell 中文显示乱码** — 不影响内容,只是显示问题

---

## 🛠️ 后续优化(P1/P2)

### P1(本月)
- 工具 6:增量索引(只索引新文件,避免全量重建)
- 升级中文模型 `BAAI/bge-small-zh-v1.5`(90MB,需先离线下载)

### P2(下次)
- 训练行业专属词汇表(品牌名/项目代号)
- 建立 KB 知识图谱(实体关系)
- 集成到 OpenClaw 工具链(自动调用)

---

_维护: B166ER · 2026-09-18_
_触发: Eric 2026-09-18 08:33 "去迭代一下你自己"_
_参考: `anyi-ops-kb/05_方法论/B166ER-自迭代报告-v3.0_2026-09-18_KB迭代与工具链.md`_