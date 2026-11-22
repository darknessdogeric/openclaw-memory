---
name: ppt-visual-editor
description: PPT 在线可视化编辑器 — 图片网格预览 + 点页改 + 单页重跑 + 一键重打包。让 deck 制作从"生成后靠记忆判断哪页差"变成"看着图改哪页"。触发：改PPT / 调PPT / 预览PPT / 这页不好 / 重新生成第N页 / PPT可视化编辑 / visual edit deck / 重打包 / contact sheet。适用于 ppt-deck-builder-pro / super-ppt / 任何"plan.json → slide-XX.png → pptx"管线。
version: 1.0.0
author: B166ER (逆向 Kimi PPT 在线可视化编辑 + 复用 ppt-deck-builder-pro 管线)
license: MIT-0
metadata:
  version: "1.0.0"
  category: ppt
  related_skills: [ppt-deck-builder-pro, super-ppt, officecli]
---

# PPT 在线可视化编辑器 (Visual Editor)

> **逆向来源**: Kimi PPT 官方文档明确写「PPT 生成后可以点击预览，并在线修改，支持用户手动自定义」——
> 这是 Kimi 相对传统 PPT 工具的**唯一结构性优势**，也是我们此前唯一落后的一项。
> **实现思路**: 不重建管线，复用 `ppt-deck-builder-pro` 已有四件套，只补中间那层「看得见、改得动」的界面。

---

## 一、它解决什么

| | 生成即交付 (此前) | 本编辑器 |
|--|-----------------|---------|
| 怎么知道哪页差 | 靠记忆 + 翻 PNG 文件夹 | **网格总览，一眼看完** |
| 改一页 | 改 plan JSON → 手敲命令重跑 | **网页上改字段 → 点按钮重跑** |
| 改完看效果 | 手动看文件 | **浏览器自动刷新** |
| 重新打包 | 手敲 package 命令 | **点一下** |

---

## 二、零新依赖的复用关系

```
ppt-deck-builder-pro/
├── ../ppt-deck-builder-pro/scripts/generate_from_plan.py      ← 批量生成
├── ../ppt-deck-builder-pro/scripts/rerun_single_page.sh       ← 单页重跑   ★
├── ../ppt-deck-builder-pro/scripts/package_image_deck.sh      ← 打包 pptx  ★
├── ../ppt-deck-builder-pro/scripts/build_contact_sheet.py     ← 联系表总览  ★
└── ../ppt-deck-builder-pro/assets/slide_plan_template.json    ← 中间数据结构 ★

        ┌──────────── 本 skill 补的这一层 ────────────┐
        │  grid.png / page-XX.png  →  浏览器网格预览    │
        │  点页 → 编辑该页字段 → 重跑 → 刷新          │
        └─────────────────────────────────────────────┘
```

**可选增强**: `officecli watch <file.pptx>` 可对最终 pptx 起 live preview 服务器；
`officecli view <file.pptx> html` 出 HTML 预览（中文正常）。
本 skill 主线走**图片级**预览，因为我们的管线本来就是图片打包制。

---

## 三、快速上手

```bash
# 1. 生成 deck (已有流程)
bash ../ppt-deck-builder-pro/scripts/generate_from_plan.py --plan plan.json --outdir out/ --max-workers 3

# 2. 启动可视化编辑器
python <ppt-visual-editor>/scripts/visual_edit.py serve \
    --plan plan.json --images-dir out/ --port 8765
# → 浏览器打开 http://127.0.0.1:8765

# 3. 在网页上: 点页 → 改「本页结论 / 可见文字 / 提示词」→ 点「重跑此页」
#    → 页面自动刷新显示新图

# 4. 全部满意后点「重新打包 PPTX」
```

---

## 四、网页上能改什么

| 字段 | plan 里的键 | 作用 | 典型改法 |
|------|------------|------|---------|
| **本页结论** | `slides[].page_goal` | 这一页要让观众记住的一句话 | 改结论 → 页面标题与内容随之变 |
| **可见文字** | `slides[].approved_text_lines` | 页面上真正要出现的字 | 精简 / 换措辞 / 改数字 |
| **页面标题** | `slides[].content` | 页标题 | 与可见文字第一行对应 |
| **文字区说明** | `slides[].text_regions` | 文字放在哪 | 避免文字压图 / 越界 |
| **提示词覆盖** | `slides[].prompt_override` | 完全手写本页提示词 | 前面都不行时的兜底 |
| **页面类型** | `slides[].page_type` | cover/path/diagnostic/... | 排版不对时换类型 |
| **阅读路径** | `slides[].reading_path` | top to bottom / left to right | 视觉顺序不对时改 |

**改动即时写回 plan.json**，所以「网页上改的」= 「plan 里改的」，两条路径永远一致。

---

## 五、命令

```bash
# 启动预览+编辑服务
visual_edit.py serve --plan plan.json --images-dir out/ [--port 8765] [--host 127.0.0.1]

# 只建索引 (不开服务), 输出每页状态表
visual_edit.py index --plan plan.json --images-dir out/

# 列出所有被改过的页 (对比 plan 的 mtime 与图片 mtime)
visual_edit.py status --plan plan.json --images-dir out/

# 命令行直接改一页并重跑 (给自动化/脚本用)
visual_edit.py patch --plan plan.json --images-dir out/ --slide 5 \
    --set page_goal="新的本页结论" \
    --set approved_text_lines='["标题","要点1","要点2"]' \
    --rerun
```

---

## 六、工作流规范（从 Kimi 逆向来的纪律）

1. **先看总览再动手** —— 打开网页第一件事是看网格, 不要凭 plan 猜
2. **一次只改一页** —— 改完立刻看效果, 避免多页同时改导致风格漂移
3. **先改 brief, 再改页** —— 若某页反复改不好, 多半是 brief 里的「必含章节」或「听众」定错了
4. **改完必须重打包** —— 只重跑了图没重打包, 交付的 pptx 还是旧的
5. **看联系表** —— `build_contact_sheet.py` 出的总览图是终检手段, 改完跑一次

---

## 七、已知限制

1. **重跑依赖图像 provider 可用** —— provider 挂了会重跑失败, 脚本会保留旧图并提示
2. **Windows 需 Git Bash** —— `rerun_single_page.sh` / `package_image_deck.sh` 是 bash 脚本;
   脚本会自动探测 `D:\Git\usr\bin\bash.exe`
3. **不检测外部改动** —— 网页外的 plan 改动需重启服务才会刷新
4. **只改内容, 不改设计** —— 设计层的调整仍要改 `style_preset` 或整份模板重跑

---

## 八、相关文件

- 编排器: `<skill>/scripts/visual_edit.py`
- 管线件: `ppt-deck-builder-pro/scripts/{generate_from_plan,rerun_single_page,package_image_deck,build_contact_sheet}.*`
- 中间结构: `ppt-deck-builder-pro/../ppt-deck-builder-pro/assets/slide_plan_template.json`
- 输入契约: `ppt-deck-builder-pro/../ppt-deck-builder-pro/references/brief-contract.md`
- 场景模板: `ppt-deck-builder-pro/../ppt-deck-builder-pro/assets/scenarios/*.json` (6 个)
- 逆向依据: `anyi-ops-kb/00_方法论/Kimi_PPT能力逆向分析_v1.0_2026-10-21.md`
