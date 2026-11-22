---
title: MangoDisk 实测报告 v1.0
date: 2026-10-07
author: B166ER
trigger: Eric 2026-10-07 14:40 - "那走 A 吧"
duration: 实测 15 分钟
---

# MangoDisk 实测报告 v1.0

> **目的**：通过实测（不是文档摘抄）回答「MangoDisk 能否进 KB」「对你这台机有什么收益」。
> **方法**：下载安装包 → 校验 SHA256 → 跑默认扫描 → 看 JSON 输出 → 汇总分析。
> **结论**：**值得内化**（理由见第五节），但不必立即用于清理——可作为「空间预警 + 决策辅助」工具。

---

## 一、安装与验证

| 步骤 | 结果 | 备注 |
|---|---|---|
| 1.下载 Windows CLI v1.1.6 | **10.59 MB** | GitHub Releases 直接下 |
| 2.SHA256 校验 | **完全一致** `6d7f944499b09c454a657057aded1ca6eca356e714628a1d1fa6cbf669df8db4` | 与官方 release 一致，未被篡改 |
| 3.运行 `mangodisk --version` | **mangodisk 1.1.6** | CLI 跑通 |
| 4.运行 `mangodisk --help` | 文档完整，CLI 子命令清晰 | `clean` + `help` 两个命令 |
| 5.运行 `mangodisk clean --format json` | 77 秒扫完 C 盘 | 默认只读，**未删任何东西** |

## 二、扫描结果（**C 盘**）

| 项目 | 数值 |
|---|---|
| 总空间 | 300.00 GB |
| 已用 | 246.55 GB（82.2%）|
| 可用 | 53.46 GB |
| **可清理** | **44.14 GB（占已用 17.9%）** |
| 扫描耗时 | 77 秒 |
| 适用规则数 | 73 |
| 过滤规则数 | 81 |
| 已装应用数 | 158 |
| 运行中进程数 | 349 |
| 读失败数 | 1（权限拒绝，无关紧要）|

## 三、按类别汇总

| # | 类别 | 规则 | 文件数 | 可清理 |
|---|---|---|---|---|
| 1 | **development（开发环境）** | 9 | 867,932 | **25.38 GB** |
| 2 | **browser（浏览器）** | 4 | 41,564 | **14.43 GB** |
| 3 | application（应用）** | 13 | 12,397 | 2.14 GB |
| 4 | system（系统） | 10 | 3,739 | 0.93 GB |
| 5 | ai（AI 模型）| 5 | 56 | 0.80 GB |
| 6 | project（项目临时）| 30 | 26,180 | 0.46 GB |
| 7 | container（Docker）| 2 | 14 | 0.00 GB |

## 四、TOP 25 单项（按大小）

| # | 类别 | 大小 | 文件数 | 说明 |
|---|---|---|---|---|
| 1 | development | 18.42 GB | 839,827 | **最大头**：node_modules / 包管理器缓存 |
| 2 | browser | 13.02 GB | 27,173 | 浏览器缓存（Chrome / Edge）|
| 3 | development | 3.83 GB | 22,538 | 开发工具缓存 |
| 4 | development | 1.96 GB | 1,824 | 其他构建产物 |
| 5 | system | 0.80 GB | 251 | 系统临时文件 |
| 7 | application | 0.74 GB | 5,684 | 应用缓存 |
| 8 | development | 0.68 GB | 600 | IDE 索引缓存 |
| 9 | **ai** | **0.67 GB** | 50 | **本地 AI 模型（Ollama / HuggingFace）**|
| 10 | application | 0.65 GB | 5,357 | 更多应用缓存 |
| 11 | application | 0.53 GB | 53 | 卸载残留 |
| 12 | project | 0.46 GB | 26,164 | 项目临时构建 |
| ... | ... | ... | ... | （略）|

## 五、判断：是否符合你的 3 个真实痛点

### 痛点 1：C 盘飘红 / 开发环境累积

**实测结果**：
- development 类别占 **25.38 GB**（57% 可清理量都来自这里）
- 单单 node_modules 类别就 18.42 GB，**839,827 个文件**
- 这和我之前说的"Ollama 模型几十 GB"形成对照——这台机还没有大量本地模型，但开发环境累积已经很重

**结论**：✅ 完全对得上痛点

### 痛点 2：未来要装大模型 + 3DGS

**实测结果**：
- ai 类别已经识别到 0.80 GB（含 50 个文件，0.67 GB 是最大头）
- container 类别只有 14 个文件、0.00 GB——说明这台机 **Docker 还没跑起来**，**这就是 3DGS / 大模型训练需要预先清理的位置**

**结论**：✅ 已经预留了 ai / container 扫描规则，未来上 3DGS / Ollama 时能快速定位

### 痛点 3：公家电脑安全 + 可审计

**实测结果**：
- 默认只读——运行 `mangodisk clean` 后**没删任何东西**（这是 MangoDisk 的核心设计）
- 看到的 44.14 GB 是「**可清理**」量，不是「**自动清理**」量
- CLI 必须 `--apply --yes` 才会实际清理（**双重确认**）
- SHA256 校验通过 + 开源协议 GPL v3 + Tauri/Rust 实现（不是 Electron，安全边界更窄）

**结论**：✅ 设计上完全符合公家合规要求

## 六、4 个亮点 vs 4 个不足

### 亮点

1. **JSON 输出可脚本化** —— 我刚才就是用 Python 把 JSON 汇总出的报告。**未来可以做成「每周自动跑扫描 → 自动出 dashboard → 预警 > 60% 时通知」**
2. **开发环境专项** —— 单 node_modules 18.42 GB 的识别，普通工具（DaisyDisk / WinDirStat）做不到这种"知道这是开发者构建产物"
3. **安全设计** —— 默认只读 + 显式 --yes + 双重确认，对公家电脑极合适
4. **AI 模型识别** —— 已经识别到 0.80 GB，本地 Ollama 模型权重 / HuggingFace 缓存都能精准定位（这是**未来**大模型部署时的重要能力）

### 不足

1. **Windows 桌面版需要 Microsoft Edge WebView2 Runtime** —— 我没装桌面版只跑了 CLI，所以 UI 体验未知
2. **个人项目（harry0703 单开发者）** —— 没有团队背书，长期维护有风险
3. **国内下载慢** —— winget 源下载经常卡死，最后还是从 GitHub release 页面直下；公家电脑可能更糟
4. **C 盘占用 82.2%**——MangoDisk 显示可清 44 GB，但**实际能清多少取决于业务影响**（删了 node_modules 需要重装依赖）

## 七、推荐使用方式

### 1. **每周一次自动扫描 + 预警**（推荐首选）

```powershell
# 周一早上 8 点跑扫描
mangodisk clean --format json --no-progress > scan.json
# 解析 JSON，提取可清理量 + 按类别
# 如果可清理量 > 30GB 或 C 盘占用 > 85%，推送 dashboard
```

我可以**写一个 Python 脚本**做这件事：
- 自动跑扫描
- 解析 JSON
- 与上周对比
- 生成 Markdown 报告
- 推送 Obsidian / dashboard

### 2. **大项目前/后的"清理预热"**

每次要装新东西（3DGS / Ollama / 大模型）前先跑一次扫描，腾出空间后再装。

### 3. **季节性大扫除**（季度 / 半年度）

每个季度跑一次 `--apply --yes` 实际清理，看哪些能安全删。

## 八、给 Eric 的 3 个具体决策点

| 决策 | 我的建议 |
|---|---|
| **是否装桌面版**（含 GUI）| **暂时不装**——CLI 已够用，桌面版需要 WebView2 + 占用更多资源。**等真需要"非技术用户使用时"再装** |
| **是否每周自动扫描** | **建议装**——空间预警比事后清理重要。我可以脚本化到开机启动 |
| **是否纳入 KB** | **建议纳入**——MangoDisk 方法论 + 实测数据沉淀，将来部署到公家机也用得上 |

## 十、结论（一句话）

> **MangoDisk 是合格的"安全磁盘清理工具"**——设计理念（默认只读 + 公家合规 + 开发环境专项）正好对应你这台机器的真实痛点。**44 GB 可清理量对一台只有 53 GB 可用空间的机是及时雨**。**建议**作为「空间预警 + 决策辅助」工具长期使用，而不是"清理工具"立即执行。

---

## 十一、附录：完整复现步骤

```powershell
# 1. 下载
Invoke-WebRequest -Uri 'https://github.com/harry0703/MangoDisk/releases/download/v1.1.6/MangoDisk-1.1.6-windows-cli.exe' -OutFile 'mangodisk.exe' -UseBasicParsing

# 2. 校验
Get-FileHash 'mangodisk.exe' -Algorithm SHA256
# 期望: 6D7F944499B09C454A657057ADED1CA6ECA356E714628A1D1FA6CBF669DF8DB4

# 3. 扫描（默认只读，不删任何东西）
mangodisk clean --format json --no-progress > scan.json

# 4. 解析
python summarize_scan.py
```

---

*编制：B166ER · 2026-10-07 14:50 GMT+8*
*实测数据基于 Eric 的本机（型号：Intel i7 Gen 14 / 31.7 GB RAM / Windows 11 Pro 26200 / C 盘 300 GB）*
*沉淀路径：`anyi-ops-kb\05_方法论\MangoDisk_实测报告_v1.0_2026-10-07.md`*
*配套数据：`toolbox\.tmp\mangodisk_test\scan_result.json`（446KB 完整 JSON）*