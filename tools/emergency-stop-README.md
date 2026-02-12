# B166ER 紧急停止按钮 - 安装说明

> 创建时间: 2026-02-12  
> 位置: `tools/emergency-stop-README.md`

---

## 🛑 三种停止方案

为你创建了 **3种** 紧急停止方式，可根据需要选择：

---

## 方案 1: 浏览器用户脚本 (推荐)

**效果**: 在 OpenClaw Web UI (localhost:3000) 右上角添加红色停止按钮

### 安装步骤

1. **安装 Tampermonkey 扩展**
   - Chrome/Edge: [Chrome Web Store](https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo)
   - Firefox: [Firefox Add-ons](https://addons.mozilla.org/firefox/addon/tampermonkey/)

2. **安装脚本**
   - 打开文件 `tools/b166er-stop-button.user.js`
   - 复制全部内容
   - 点击 Tampermonkey 图标 → "创建新脚本"
   - 粘贴内容并保存 (Ctrl+S)

3. **使用**
   - 访问 http://localhost:3000
   - 右上角会出现红色 ⏹ 停止按钮
   - 快捷键: **Ctrl+Shift+S**

### 特点
- ✅ 最优雅的方式，集成在 Web UI 中
- ✅ 一键停止，无需切换窗口
- ✅ 有视觉反馈和通知
- ⚠️ 需要安装浏览器扩展

---

## 方案 2: 独立停止页面

**效果**: 独立的 HTML 页面，美观的紧急停止按钮

### 使用方法

1. **桌面快捷方式**
   - 已创建: `桌面/B166ER-Emergency-Stop.lnk`
   - 双击打开停止页面
   - 点击大红按钮停止

2. **或直接打开文件**
   - 文件: `tools/emergency-stop.html`
   - 用浏览器打开即可

### 特点
- ✅ 无需安装任何扩展
- ✅ 视觉效果最佳（动画、渐变）
- ✅ 可跨设备使用（手机、平板）
- ⚠️ 需要切换到浏览器窗口

---

## 方案 3: 批处理脚本

**效果**: 双击强制终止 OpenClaw 进程

### 使用方法

1. **桌面快捷方式**
   - 已创建: `桌面/B166ER-Stop-Batch.lnk`
   - 双击运行

2. **或右键管理员运行**
   - 文件: `tools/emergency-stop.bat`
   - 右键 → "以管理员身份运行"

### 特点
- ✅ 最彻底，强制终止进程
- ✅ 可处理卡死、无响应情况
- ✅ 无需浏览器
- ⚠️ 无法保存进行中的工作
- ⚠️ 可能需要管理员权限

---

## 🎯 使用建议

| 场景 | 推荐方案 |
|------|----------|
| 日常使用 | 方案 1 (用户脚本) |
| 快速停止 | 方案 2 (停止页面) |
| 卡死/无响应 | 方案 3 (批处理) |
| 手机/平板 | 方案 2 (停止页面) |

---

## 🔧 快捷键速查

| 快捷键 | 功能 |
|--------|------|
| **Ctrl + Shift + S** | 触发停止 (方案1和2) |
| **Alt + F4** | 关闭当前窗口 |
| **Ctrl + C** | 在终端中中断 (如果焦点在终端) |

---

## 📝 文件清单

```
tools/
├── emergency-stop.html           # 方案2: 独立停止页面
├── emergency-stop.bat            # 方案3: 批处理脚本
├── b166er-stop-button.user.js    # 方案1: 用户脚本
└── emergency-stop-README.md      # 本说明文件

桌面/
├── B166ER-Emergency-Stop.lnk     # 方案2快捷方式
└── B166ER-Stop-Batch.lnk         # 方案3快捷方式
```

---

## ⚠️ 注意事项

1. **停止是立即的**
   - 正在进行的任务会被中断
   - 未保存的工作可能丢失
   - 建议先等待任务自然完成

2. **批处理方案是强制的**
   - 相当于"拔电源"
   - 只有在其他方案无效时使用

3. **权限问题**
   - 如果停止失败，尝试以管理员身份运行
   - 批处理方案可能需要管理员权限

---

## 🔄 更新

如需更新停止按钮功能，重新运行相关命令或替换文件即可。

---

**有任何问题随时告诉我！**
