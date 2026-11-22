---
name: image-paradigm-skill
description: |
  图像 / 海报 / 信息图 范式工具集(2026.09.30 整理):
  - 商务风 9:16 信息图 (仿 ERIC 出品)
  - 小红书 3:4 粉色风信息图
  - HTML→图片:Chrome headless 截图(零 API,中文 100% 准确)
  每次产出前调用 templates/ 选范式,然后生成。
triggers:
  - 生成信息图 / 海报 / 封面 / 小红书卡片
  - 商务风 / 极简 / 报告风格
  - 9:16 1080x1920 / 3:4 1080x1440
  - 需要 100% 中文准确(无乱码)
license: internal
---

# 图像 / 海报 范式工具集

## 核心方案(按优先级)

### 1. HTML+CSS → Chrome headless 截图(零 API,100% 中文准确) ⭐ 最优

- **路径**:`toolbox/templates/eric_business_9x16.html`(商务风,9:16)
- **路径**:`toolbox/templates/xiaohongshu_3x4.html`(小红书,3:4)
- **工具调用**(skill: `lh-html-to-image`)
  ```
  "C:\Users\ericz\AppData\Local\Google\Chrome\Application\chrome.exe" --headless=new --disable-gpu --screenshot=output.png --window-size=1080,1920 file:///path/to/template.html
  ```
- **中文字体**(系统已装):
  - `Noto Sans SC`(推荐)/ `Microsoft YaHei` / `SimHei` / `SimSun`
  - Windows: `C:\Windows\Fonts\` 已有
- **优势**:
  - 100% 中文准确(浏览器级渲染)
  - 零 API 成本
  - 像素级精准(可任意 1080x1920 / 3:4 / 16:9)
  - 可在浏览器先预览再截图
- **对比**(经验教训):
  - ❌ `image_generate` LLM 渲染中文 → **经常乱码**(Eric 已验证)
  - ❌ matplotlib 中某些字符偶有 glyph 缺失(警告但可接受)
  - ✅ Chrome headless 截图 = 最稳

### 2. Python matplotlib + 中文字体(无 LLM)
- 适合:程序化数据图 / 自动批处理
- 字体:`Noto Sans SC` / `Microsoft YaHei`
- 缺点:手写式调整繁琐(本次 Eric 风格信息图即用此)
- 优点:不依赖 Chrome,无 GPU

### 3. AI 图像生成(LLM)
- **工具**:`openclaw image_generate`
- **限制**:
  - 中文乱码常见
  - 仅适合纯视觉(无文字需求)
- **不推荐**用于含中文海报/信息图

## 范式库位置

| 文件 | 尺寸 | 用途 |
|------|------|------|
| `toolbox/templates/eric_business_9x16.html` | 1080×1920 | 商务信息图(一句话+三数字+三判断+来源+预测) |
| `toolbox/templates/xiaohongshu_3x4.html` | 1080×1440 | 小红书粉色风格信息图 |
| `toolbox/templates/README.md` | - | 索引 + 已有产出清单 |

## 工作流(下次产出前调用)

```
1. Eric 提供主题与数据
2. 选范式:
   - 商务风报告/双节预测 → eric_business_9x16.html
   - 小红书爆款 → xiaohongshu_3x4.html
3. 复制范式 HTML → 编辑内容(改文字+数字)
4. 保存到 D:\B166ER-OpenClaw\workspace\toolbox\templates\<name>.html
5. 用 lh-html-to-image 截图 → 保存 PNG
6. 复制到 Eric 桌面 + .openclaw/media 归档
```

## 经验(避免重蹈覆辙)

- ❌ 不要再用 `image_generate` 渲染中文(必乱码)
- ✅ 默认用 HTML+CSS + Chrome headless
- ✅ 系统字体足够(Noto Sans SC / SimHei)
- ✅ 1080×1920 是 Eric 默认尺寸(9:16 适合手机)
- ✅ Eric 风格信息图固定结构:
  - 一句话总结(看是X 实则Y 正在Z)
  - 三个数字 + 三个判断 + 来源方法 + 预测矩阵