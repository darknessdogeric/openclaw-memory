# B166ER GitHub 备份配置指南

## 配置状态

| 步骤 | 状态 | 说明 |
|------|------|------|
| 本地 Git 仓库 | ✅ 已配置 | ~/.openclaw/workspace |
| 远程仓库地址 | ✅ 已配置 | https://github.com/darknessdogeric/openclaw-memory.git |
| GitHub 认证 | ⚠️ 待配置 | 需要创建 Personal Access Token |
| 开机自动同步 | ⚠️ 待配置 | 脚本已创建，需添加快捷方式 |

---

## 第1步：在 GitHub 创建仓库

1. 访问 https://github.com/new
2. 仓库名称: `openclaw-memory`
3. 选择 **Private**（私有仓库）
4. 不要勾选 "Add a README file"（本地已有文件）
5. 点击 **Create repository**

---

## 第2步：创建 Personal Access Token

1. 访问 https://github.com/settings/tokens
2. 点击 **Generate new token (classic)**
3. 填写 Note: `B166ER Git Backup`
4. 过期时间: 选择 **No expiration** 或自定义
5. 权限勾选:
   - ✅ `repo` (完整仓库访问权限)
6. 点击 **Generate token**
7. **立即复制 token**（只会显示一次）

---

## 第3步：配置 Git 认证

### 方式A：Git Credential Manager (推荐)

打开 Git Bash 运行：
```bash
cd ~/.openclaw/workspace
git push -u origin master
```
会弹出窗口要求输入:
- Username: `darknessdogeric`
- Password: 粘贴刚才复制的 Token

### 方式B：直接配置

```bash
git config --global credential.helper manager
cd ~/.openclaw/workspace
git push -u origin master
```

---

## 第4步：设置开机自动同步

打开 PowerShell 运行：
```powershell
C:\B166ER-Backup\create-startup-shortcut.ps1
```

或手动创建快捷方式:
1. 右键 `C:\B166ER-Backup\github-sync.bat`
2. 选择 "创建快捷方式"
3. 将快捷方式移动到: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`

---

## 备份脚本说明

**脚本位置**: `C:\B166ER-Backup\github-sync.bat`

**执行流程**:
1. 添加所有文件变更
2. 自动提交（带时间戳）
3. 推送到 GitHub

**手动运行**: 双击 `github-sync.bat` 即可立即备份

---

## 故障排除

### 推送失败：Authentication failed
- 检查 Token 是否正确
- 检查 Token 是否有 `repo` 权限
- 重新运行 `git push` 重新认证

### 推送失败：repository not found
- 确认 GitHub 上已创建仓库
- 检查远程地址: `git remote -v`
- 如需修改: `git remote set-url origin https://github.com/darknessdogeric/openclaw-memory.git`

---

## 配置完成后测试

```bash
cd ~/.openclaw/workspace
echo "test" >> backup-test.txt
git add -A
git commit -m "测试备份"
git push origin master
```

成功后删除测试文件:
```bash
rm backup-test.txt
git add -A
git commit -m "删除测试文件"
git push origin master
```

---

配置时间: 2026-03-02
GitHub 用户: darknessdogeric
仓库: openclaw-memory
