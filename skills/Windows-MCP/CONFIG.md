# Windows-MCP 配置指南

## 安装状态
✅ **已安装** - windows-mcp 0.6.9

## 基本信息
- **名称**: Windows-MCP
- **版本**: 0.6.9
- **功能**: Windows系统自动化MCP服务器
- **位置**: `C:\Users\Administrator\.openclaw\workspace\skills\Windows-MCP`

## 核心功能

### 1. 文件系统操作
- 文件导航
- 文件读写
- 目录操作

### 2. 应用程序控制
- 打开应用
- 控制窗口
- 模拟用户输入

### 3. UI自动化
- UI元素交互
- 鼠标/键盘操作
- 截图

### 4. 浏览器自动化
- DOM模式
- 网页内容提取
- 浏览器控制

### 5. QA测试
- 自动化测试
- 状态捕获
- 测试报告

## 使用方法

### 启动MCP服务器
```bash
windows-mcp --transport stdio
```

### 可用传输方式
- `stdio` - 标准输入输出（默认）
- `sse` - Server-Sent Events
- `streamable-http` - HTTP流

### 配置示例
```json
{
  "mcpServers": {
    "windows-mcp": {
      "command": "windows-mcp",
      "args": ["--transport", "stdio"]
    }
  }
}
```

## 依赖项
- Python 3.13+
- comtypes
- dxcam
- fastmcp
- pywin32
- psutil
- pillow

## 注意事项
1. 需要Windows 7/8/10/11系统
2. 首次启动可能需要安装依赖
3. 部分功能需要管理员权限
4. 默认语言为英语，其他语言可能需要禁用App-Tool

## 使用场景
- 自动化Windows任务
- 文件管理自动化
- 应用程序控制
- UI测试
- 浏览器自动化

## 相关链接
- GitHub: https://github.com/CursorTouch/Windows-MCP
- PyPI: https://pypi.org/project/windows-mcp/
- 文档: https://windowsmcp.io/
