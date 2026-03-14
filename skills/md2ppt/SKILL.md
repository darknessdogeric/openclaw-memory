# MD2PPT Converter Skill
## Markdown转PPT路演工具

**技能名称**: MD2PPT Converter  
**版本**: 1.0  
**创建日期**: 2026-03-04  
**用途**: 将Markdown文档转换为路演演示PPT

---

## 功能说明

本技能可以将AHL项目文档（Markdown格式）自动转换为专业的PowerPoint演示文稿，适用于：
- 政府申请路演
- 投资人路演
- 团队内部分享
- 客户演示

## 安装要求

**依赖库**:
```bash
pip install python-pptx Pillow
```

## 使用方法

### 方法一：命令行直接运行
```bash
python C:\Users\Administrator\.openclaw\skills\md2ppt\md2ppt.py
```

### 方法二：在Python中调用
```python
from md2ppt import MD2PPTConverter

converter = MD2PPTConverter()
converter.convert_markdown(
    md_file='文档.md',
    output_file='演示.pptx',
    presentation_title='演示标题'
)
```

### 方法三：批量转换
脚本会自动转换以下文件：
- 政府申请说明书 → 政府申请路演.pptx
- 商业计划书 → 投资人路演.pptx
- 顶层设计总纲 → 顶层设计路演.pptx

## PPT设计规范

**视觉风格**:
- 主色调: AHL蓝 (#1A5490)
- 强调色: 橙色 (#FF7F27)
- 布局: 16:9宽屏
- 字体: 微软雅黑

**页面类型**:
1. 标题页 - 项目名称+副标题
2. 章节分隔页 - 全页背景+大标题
3. 内容页 - 标题+要点列表
4. 双栏页 - 对比展示
5. 结束页 - 感谢+联系方式

## 转换效果

**支持元素**:
- ✅ 标题层级 (H1-H4)
- ✅ 列表项 (有序/无序)
- ✅ 文本段落
- ✅ 章节自动分页
- ⚠️ 表格 (转为文本)
- ⚠️ 图片 (需手动添加)

## 输出位置

生成的PPT文件保存在：
```
C:\Users\Administrator\Desktop\项目说明书\
```

## 使用建议

1. **政府申请**: 使用 "AHL路演-政府申请.pptx"
2. **投资人路演**: 使用 "AHL路演-投资人BP.pptx"
3. **顶层设计**: 使用 "AHL路演-顶层设计.pptx"

## 手动优化建议

自动生成的PPT建议手动优化：
- 添加项目Logo
- 插入架构图/流程图
- 调整关键页面动画
- 添加演讲者备注

## 故障排除

**问题1**: 中文显示异常  
**解决**: 确保系统安装了微软雅黑字体

**问题2**: 转换失败  
**解决**: 检查Markdown文件编码为UTF-8

---

**维护者**: B166ER  
**更新日期**: 2026-03-04
