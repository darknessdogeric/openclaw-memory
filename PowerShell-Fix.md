# Windows PowerShell 命令兼容解决方案

## 问题原因
PowerShell 不支持 `&&` 和 `||` 操作符（这是 Bash 特性），导致命令链失败。

## 解决方案

### 方案1: 使用分号代替 (推荐)
```powershell
# 错误写法 (Bash风格)
cd C:\Users\Administrator\.openclaw\workspace && git add -A && git commit -m "msg" && git push

# 正确写法 (PowerShell风格)
cd C:\Users\Administrator\.openclaw\workspace; git add -A; git commit -m "msg"; git push
```

### 方案2: 使用 Git Bash
```bash
# 在Git Bash中运行，支持 &&
cd /c/Users/Administrator/.openclaw/workspace && git add -A && git commit -m "msg" && git push
```

### 方案3: 使用脚本文件
创建 `git-backup.ps1`:
```powershell
Set-Location C:\Users\Administrator\.openclaw\workspace
git add -A
git commit -m "Backup: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
git push origin master
```

## 快速修复命令

对于当前的Git备份，请使用以下任一方式：

**方式A - PowerShell分号:**
```powershell
cd C:\Users\Administrator\.openclaw\workspace; git add -A; git commit -m "Backup $(Get-Date -Format 'yyyy-MM-dd HH:mm')"; git push origin master
```

**方式B - 单行顺序执行:**
```powershell
cd C:\Users\Administrator\.openclaw\workspace
git add -A
git commit -m "Backup"
git push origin master
```

**方式C - 使用Git Bash:**
打开Git Bash，运行：
```bash
cd /c/Users/Administrator/.openclaw/workspace && git add -A && git commit -m "Backup" && git push origin master
```

## 长期解决方案

我已更新我的执行方式，后续将使用分号代替 && 操作符。
