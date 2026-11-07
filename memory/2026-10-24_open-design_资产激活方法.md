# 记忆: open-design 资产激活方法 (2026-10-24)

> **触发**: Eric 问"VI/导视导览/LOGO/色系/海报"→ 发现已装 `open-design` skill 声称 150+ 品牌库但本地克隆缺失
> **核心难题**: 仓库 `nexu-io/open-design` = **3.56 GB / 103,635 star**，常规 `git clone` 会卡死（试了 2 次，0 文件）

## 结论: 不要克隆, 用 GitHub API 精准拉

```powershell
# ❌ 会卡死 (3.5GB)
git clone --depth 1 https://github.com/nexu-io/open-design $HOME\.open-design-skill\repo
git clone --filter=blob:none --no-checkout --depth 1 ...   # 仍慢, 树对象太大

# ✅ API 列举 + raw 直连下载 (只下需要的)
```

**已落地路径**: `C:\Users\ericz\.open-design-skill\repo\`

| 目录 | 内容 | 体积 | 拉取方式 |
|------|------|------|---------|
| `design-systems/` | **152 个品牌 DESIGN.md** (Apple/Airbnb/BMW/Bugatti/Binance/Claude/Canva/Cisco…) | 1,672 KB | API 列目录 → raw 拉 `design-systems/<slug>/DESIGN.md` |
| `design-templates/` | **116 个渲染模板** (deck/prototype/email/audio…，含 html-ppt 系列) | 2,037 KB | API 递归 + 扩展名过滤 |
| `craft/` | **13 个通用方法论** (color / typography / typography-hierarchy / anti-ai-slop / accessibility-baseline / laws-of-ux / animation-discipline / rtl-and-bidi / state-coverage / form-validation / FUTURE_SECTIONS) | 110 KB | API 递归 |
| `skills/` | 169 个功能 skill (stub 形式, 指向 upstream) | 未拉 | ⚠️ GitHub API 限流 + 这些是 stub 需另拷 upstream, 优先级低 |

## 关键坑

1. **GitHub API 60 次/小时未认证限流** → 触发 403 `API rate limit exceeded`。
   - 兜底: `raw.githubusercontent.com` **不限流**，只要知道路径就能直连
   - 目录名未知时: 一次 Contents API 拿全部 slug，之后全走 raw
2. **真实路径是 `design-templates/`，不是 `templates/`**（`templates/` 只有 1 目录 2 文件，是另一回事）
3. **`craft/` 才是方法论**（色系/字体/无障碍/反 AI 味/UX 法则），不在 `skills/` 里
4. 验证方式: `node scripts/list-design-systems.mjs` / `list-design-templates.mjs` / `list-craft.mjs`

## 为什么值得 (对 Eric)

`craft/color.md` 里的规则正好命中 Eric 反复强调的东西：
- 中性色占 **70–90%** 像素
- 强调色**每屏最多 2 处**（"AI 生成 UI 最大可读性杀手就是 accent 滥用"）
- 正文对比度 **≥ 4.5:1**（作为门禁不是目标）
- 单一强调色，**不许自创第二强调色**

`craft/typography.md` + `typography-hierarchy.md` = 字体与字阶的通用契约，叠在任意 DESIGN.md 之上。

152 个品牌 DESIGN.md = 现成的 VI 参照系（可直接给品牌做"对标 Airbnb 的色板/字阶"这类活）。
