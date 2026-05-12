# Markdown转PDF技能

## 技能名称
**MD2PDF Converter** - Markdown转PDF转换器

## 安装说明

### 前置要求
1. Python 3.8+ (已安装)
2. wkhtmltopdf (需要下载安装)

### 安装步骤

#### 步骤1: 安装wkhtmltopdf (仅首次)
1. 访问: https://wkhtmltopdf.org/downloads.html
2. 下载: wkhtmltopdf for Windows (64-bit)
3. 安装: 使用默认设置安装

#### 步骤2: 验证安装
```bash
# 检查是否安装成功
"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" --version
```

## 使用方法

### 方法一: 双击运行 (推荐)
直接双击运行: `转换MD为PDF.bat`

### 方法二: 命令行运行
```bash
cd "C:\Users\Administrator\Desktop\张实项目总控\06-AHL-去中心化旅行平台"
python md_to_pdf.py
```

### 方法三: 转换指定文件
```bash
python md_to_pdf.py 文件名.md
```

## 功能特性

✅ 支持中文完美显示  
✅ 自动表格美化  
✅ 代码块高亮  
✅ 目录生成  
✅ 页眉页脚  
✅ A4纸张格式  

## 输出效果

转换后的PDF具有以下特点:
- 专业商务风格
- 清晰的层级结构
- 美观的表格和代码块
- 适合打印和分享

## 故障排除

### 问题1: "未找到wkhtmltopdf"
**解决**: 安装wkhtmltopdf并确保路径正确

### 问题2: 中文显示为方框
**解决**: 安装中文字体 (Microsoft YaHei, SimHei)

### 问题3: 转换失败
**解决**: 检查MD文件编码是否为UTF-8

## 更新日志

- v1.0 (2026-03-04): 初始版本，支持基本转换功能

## 维护信息

- 创建者: B166ER
- 创建日期: 2026-03-04
- 适用项目: AHL去中心化旅行平台
