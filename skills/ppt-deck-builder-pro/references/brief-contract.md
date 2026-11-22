# Brief Contract — PPT 制作前置契约 (v1.0)

> **来源**: 逆向 Kimi PPT 官方帮助文档 (`kimi.com/help/ppt/ppt-overview`) 得出
> **核心发现**: Kimi 的提示词**不是自由发挥**, 而是显式参数:
>   "我做一份从AGENT入门到进阶的PPT，**适合非技术背景的产品经理**，**15页左右**，**包含痛点、解决方案、核心功能、定价**"
> **落地**: 本 skill 在生成前**必须先锁定这 5 个参数**, 否则不许进入生成阶段

---

## 0. 为什么要有这个契约

| | 无契约 | 有契约 (本文件) |
|--|--------|---------------|
| 返工原因 | "不是我要的风格" / "页数太多" / "受众不对" | 首次就锁定 |
| 责任归属 | 含糊 | 参数先定, 变更需显式说明 |
| 可复用 | 每次重讲 | brief 是资产, 可存可复用 |

**Kimi 官方对比表自证**: 传统 PPT「依赖模板或设计能力 / 需自己撰写文案 / 数小时至数天」
→ Kimi PPT「AI 自动匹配配色排版图表 / AI 自动研究撰写结构化 / 几分钟」
**它把人的负担从"怎么做"移到了"要什么"。** 契约就是"要什么"的结构化。

---

## 1. 五个必填参数

### ① 页数 (`total_slides`)
- **默认值**: 10
- **规则**: 少于 5 页 → 合并；多于 25 页 → 拆成多份（一次 20 页封顶）
- **Kimi 原例**: "10 页 PPT" / "15 页左右" / "20 页图文并茂的汇报PPT"

### ② 风格 (`style_preset`)
- **默认值**: `corporate_pro`
- **可选值**: 见 `references/template-selector.md` 的 12 套
- **规则**: **一套 deck 只允许一个主风格**；确需破例时, 必须在该页 `style_notes` 写明理由
- **Kimi 原例**: "商业风格" / "突出增长趋势"

### ③ 目标听众 (`audience`)
- **必填, 不给默认值** —— 这是最容易被跳过、也最致命的一项
- **必写四项**: `who` (谁) / `knows` (已知什么) / `wants` (要什么结论) / `action` (看完要做什么)
- **反例**: "领导" —— 太模糊
- **正例**: "投委会成员; 已知我们的业务盘子; 要决定是否追加 3000 万; 要当场批"

### ④ 必含章节 (`required_sections`)
- **必填, 至少 3 项**
- **每项写清**: 章节名 + 这一页要传达的**唯一结论** + 预计页数
- **规则**: 章节顺序 = 阅读路径; 章节之间不重复结论
- **Kimi 原例**: "包含痛点、解决方案、核心功能、定价" / "包含竞争格局、技术路线、政策背景"

### ⑤ 数据源 (`data_sources`)
- **必填, 至少 1 项**
- **每项写清**: 来源类型 + 具体位置 + 可信度
- **类型**: 内部数据 / 公开研究 / 联网检索 / 用户提供文档 / 示意数据
- **规则**: **示意数据必须显式标注**, 不得让读者误认为真实数据
- **Kimi 官方强调**: "引用的文献与数据均经过真实信息源核验, 确保 PPT 内容与事实、有据可循"

---

## 2. brief 的 JSON 结构

```json
{
  "brief": {
    "total_slides": 10,
    "style_preset": "corporate_pro",
    "audience": {
      "who": "投委会 5 位委员",
      "knows": "我们的存量业务盘子与去年增长曲线",
      "wants": "判断是否追加 3000 万投 AHL",
      "action": "当场给出是否追加的明确结论"
    },
    "required_sections": [
      {"name": "行业为什么现在", "conclusion": "窗口期只剩 12 个月", "slides": 2},
      {"name": "我们凭什么", "conclusion": "唯一同时握有协议层与场景的团队", "slides": 3},
      {"name": "要多少钱", "conclusion": "3000 万换 6 年期 1244 独家协议层", "slides": 2}
    ],
    "data_sources": [
      {"type": "internal", "where": "安逸集团 167 家酒店 2025 年经营台账", "confidence": "🟢🟢 一手"},
      {"type": "web", "where": "厚海数据平台 MSI 2026 Q3", "confidence": "🟡🟡 多源"}
    ],
    "explicit_constraints": [
      "不出现安逸集团未公开的内部数据",
      "所有预测标注区间而非单点"
    ],
    "success_check": "委员看完后能复述'为什么是现在、为什么是我们、要多少'"
  }
}
```

---

## 3. 生成前校验清单 (硬门禁)

生成任何一页之前, 逐条自查:

```
□ 页数已定, 且与章节页数之和一致 (允许 ±1 页余量)
□ 风格已定, 且是 12 套具名 preset 之一 (不接受"有质感一点"这种描述)
□ 听众四项齐全 (who / knows / wants / action)
□ 必含章节 ≥3, 每项都有唯一结论
□ 数据源 ≥1, 示意数据已标注
□ explicit_constraints 已写 (至少 1 条, 尤其是合规边界)
□ success_check 可被验证 (不是"讲清楚"这种不可判定的表述)
```

**任一项缺失 → 回到提问, 不进入生成。**

### 提问模板 (一次问完, 不挤牙膏)

```
做这份 PPT 前, 我需要锁定 5 件事 (不回这几项我只能猜, 返工率很高):

1) 页数: 多少页? (默认 10; 超 20 页建议拆两份)
2) 风格: 12 套里选一个 —— 
   corporate_pro 企业提案 / startup_roadshow 融资路演 / light_consulting 咨询报告 /
   data_viz_pro 数据分析 / gradient_modern 科技发布 / elegant_chinese 国风文化 /
   whiteboard_handdrawn 培训讲解 / luxury_premium 高端VIP / minimal_white 极简 /
   dark_blue_business 客户演示 / green_nature 环保可持续 / creative_playful 创意教育
3) 听众: 谁看? 他们已经知道什么? 想得出什么结论? 看完要做什么?
4) 必含章节: 至少 3 个, 每个要传达的唯一结论是什么? 各占几页?
5) 数据源: 数据从哪来? 哪些是要联网查的? 哪些是示意 (会标注)?
```

---

## 4. brief 与 plan 的关系

```
brief (要什么)  ──生成──▶  slides[].page_goal / content / approved_text_lines
                              │
                              ├── page_type          ← 页面类型 (cover/path/diagnostic/...)
                              ├── reading_path       ← 阅读路径
                              ├── native_structure_lock  ← 页面结构锁定
                              ├── qa_focus           ← 本页验收点
                              └── prompt_override    ← 最终提示词
```

**规则**: `brief` 定方向, `plan` 定每一页。**任何页面级修改都不得违反 brief 的 ①②③④⑤。**
若用户中途改需求, **先改 brief 再改 plan**, 否则会出现"风格统一但页数对不上"这类不一致。

---

## 5. 与现有 references 的关系

| brief 参数 | 落地时查 |
|-----------|---------|
| ② 风格 | `references/style-presets.md` / `references/template-selector.md` |
| ③ 听众 | `references/audience-and-goals.md` |
| ④ 章节 | `references/story-patterns.md` / `references/page-types.md` |
| ⑤ 数据源 | `references/chart-selection.md` / `references/data-slide-patterns.md` |
| 页面级 | `references/layout-patterns.md` / `references/prompt-rules.md` |
| 验收 | `references/qa-checklist.md` |

---

## 6. 校验脚本

```bash
python scripts/validate_brief.py <plan.json>
```

逐条打印上面 7 个勾选项的通过/失败, 失败项给出修复建议。**生成前必跑。**

---

**版本**: v1.0
**来源**: 逆向 Kimi PPT 官方文档 (`kimi.com/help/ppt/ppt-overview`, 抓取时间 2026-10-21)
**适用**: `ppt-deck-builder-pro` 全部生成路径
