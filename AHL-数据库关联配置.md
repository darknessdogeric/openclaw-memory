# B166ER与AHL数据库关联配置

## 数据库位置
**主路径**: `D:\AHL-Database\`

## 快捷访问路径

### 国际酒店集团
- 万豪: `D:\AHL-Database\01-国际酒店集团\01-万豪集团\`
- 希尔顿: `D:\AHL-Database\01-国际酒店集团\02-希尔顿集团\`
- 洲际: `D:\AHL-Database\01-国际酒店集团\03-洲际集团\`
- 雅高: `D:\AHL-Database\01-国际酒店集团\04-雅高集团\`
- 凯悦: `D:\AHL-Database\01-国际酒店集团\05-凯悦集团\`

### 国内酒店集团
- 华住: `D:\AHL-Database\02-国内酒店集团\01-华住集团\`
- 锦江: `D:\AHL-Database\02-国内酒店集团\02-锦江集团\`
- 首旅: `D:\AHL-Database\02-国内酒店集团\03-首旅集团\`

### 精品酒店
- 亚朵: `D:\AHL-Database\03-精品酒店\01-亚朵\`
- 花间堂: `D:\AHL-Database\03-精品酒店\02-花间堂\`

### 标准规范
- 国家标准: `D:\AHL-Database\04-民宿标准\01-国家标准\`
- 行业标准: `D:\AHL-Database\05-行业标准\`

### 个人资料
- 张实资料库: `D:\AHL-Database\06-张实个人资料库\`

## 调用指令

当张实将资料放入D盘后，使用以下方式调用：

```python
# 读取资料
read(file_path="D:\\AHL-Database\\[路径]\\[文件名]")

# 保存资料
write(file_path="D:\\AHL-Database\\[路径]\\[文件名]", content="...")

# 列目录
exec(command="ls D:\\AHL-Database\\[路径]")
```

## 工作流程

1. 张实收集资料 → 放入D盘对应文件夹
2. 通知B166ER: "资料已放入D盘，请分析"
3. B166ER读取 → 分析整理 → 生成标准版
4. 输出成果 → 保存回D盘或Workspace

## 注意事项

- 读取前确认文件存在
- 处理PDF时使用doc-reader skill
- 整理后的标准版保存到Workspace做Git备份
