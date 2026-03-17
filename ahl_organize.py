import os
import shutil
import json
from datetime import datetime
from pathlib import Path

# 配置
BASE_DIR = Path("C:/Users/Administrator/Desktop/张实项目总控/05-AHL-去中心化旅行平台")
ARCHIVE_DIR = BASE_DIR / "00-归档管理"
REPORT_DIR = ARCHIVE_DIR / "整理报告"

# 档案分类映射
CATEGORY_MAP = {
    "顶层设计": ["顶层设计", "架构方案", "产品清单", "协议"],
    "商业融资": ["商业计划书", "融资", "投资人", "取费标准", "说明书"],
    "产品技术": ["SKILL", "AGENT", "SOP", "产品方案", "技术"],
    "运营实施": ["苏州", "大理", "PP&SOP", "运营"],
    "市场品牌": ["市场", "竞品", "品牌", "营销"],
    "数据知识": ["知识库", "数据框架", "向量"],
    "工具脚本": [".py", "CLI", "脚本", "工具"],
}

# 版本模式
VERSION_PATTERNS = ["V1.0", "V2.0", "V3.0", "V4.0", "V5.0", "V0.", "-V1.", "-V2.", "-V3.", "-V4.", "-V5."]

def scan_files():
    """扫描所有文件"""
    files = []
    for root, dirs, filenames in os.walk(BASE_DIR):
        # 跳过归档管理目录（避免重复处理）
        if "00-归档管理" in root:
            continue
        for filename in filenames:
            filepath = Path(root) / filename
            stat = filepath.stat()
            files.append({
                "path": str(filepath),
                "name": filename,
                "size": stat.st_size,
                "mtime": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "ext": filepath.suffix.lower()
            })
    return files

def find_duplicates(files):
    """查找重复文件"""
    # 按文件名+大小分组
    name_size_map = {}
    for f in files:
        key = f"{f['name']}_{f['size']}"
        if key not in name_size_map:
            name_size_map[key] = []
        name_size_map[key].append(f)
    
    # 找出重复组
    duplicates = {k: v for k, v in name_size_map.items() if len(v) > 1}
    return duplicates

def find_temp_files(files):
    """查找临时文件"""
    temp_patterns = ["~$", ".tmp", ".temp", ".bak", ".old"]
    temp_files = []
    for f in files:
        if any(f['name'].startswith(p) or f['name'].endswith(p) for p in temp_patterns):
            temp_files.append(f)
    return temp_files

def classify_file(filename):
    """根据文件名分类"""
    filename_lower = filename.lower()
    for category, keywords in CATEGORY_MAP.items():
        if any(kw.lower() in filename_lower for kw in keywords):
            return category
    return "其他"

def has_version(filename):
    """检查文件名是否包含版本号"""
    return any(v in filename for v in VERSION_PATTERNS)

def generate_report(files, duplicates, temp_files):
    """生成整理报告"""
    report = {
        "整理日期": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "总文件数": len(files),
        "总大小_MB": round(sum(f['size'] for f in files) / (1024*1024), 2),
        "重复文件组": len(duplicates),
        "临时文件数": len(temp_files),
        "分类统计": {},
        "重复详情": duplicates,
        "临时文件": temp_files
    }
    
    # 分类统计
    for f in files:
        cat = classify_file(f['name'])
        if cat not in report["分类统计"]:
            report["分类统计"][cat] = {"count": 0, "size": 0}
        report["分类统计"][cat]["count"] += 1
        report["分类统计"][cat]["size"] += f['size']
    
    return report

def create_directory_structure():
    """创建档案目录结构"""
    dirs = [
        "00-归档管理/整理报告",
        "01-顶层设计/当前版本",
        "01-顶层设计/历史版本",
        "02-商业融资/当前版本",
        "02-商业融资/历史版本",
        "03-产品技术/当前版本",
        "03-产品技术/历史版本",
        "04-运营实施/苏州酒管公司项目",
        "04-运营实施/大理0号实验室",
        "04-运营实施/PP&SOP知识库",
        "05-市场品牌",
        "06-数据与知识库",
        "07-工具与脚本",
        "99-归档资料/废弃方案",
        "99-归档资料/暂停项目",
        "99-归档资料/临时文件"
    ]
    
    for d in dirs:
        (BASE_DIR / d).mkdir(parents=True, exist_ok=True)
    
    print(f"[DONE] 已创建 {len(dirs)} 个目录")

def main():
    print("[SCAN] 开始扫描AHL项目文件夹...")
    
    # 1. 扫描文件
    files = scan_files()
    print(f"[INFO] 发现 {len(files)} 个文件")
    
    # 2. 查找重复
    duplicates = find_duplicates(files)
    print(f"[INFO] 发现 {len(duplicates)} 组重复文件")
    
    # 3. 查找临时文件
    temp_files = find_temp_files(files)
    print(f"[INFO] 发现 {len(temp_files)} 个临时文件")
    
    # 4. 创建目录结构
    print("[INFO] 创建档案目录结构...")
    create_directory_structure()
    
    # 5. 生成报告
    report = generate_report(files, duplicates, temp_files)
    
    # 保存报告
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_file = REPORT_DIR / f"AHL_整理报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n[DONE] 整理报告已保存: {report_file}")
    
    # 输出摘要
    print("\n" + "="*50)
    print("整理摘要")
    print("="*50)
    print(f"总文件数: {report['总文件数']}")
    print(f"总大小: {report['总大小_MB']} MB")
    print(f"重复文件组: {report['重复文件组']}")
    print(f"临时文件: {report['临时文件数']}")
    print("\n分类统计:")
    for cat, stats in report['分类统计'].items():
        size_mb = round(stats['size'] / (1024*1024), 2)
        print(f"  {cat}: {stats['count']}个文件 ({size_mb} MB)")
    
    # 输出重复文件详情
    if duplicates:
        print("\n重复文件详情:")
        for key, dup_files in list(duplicates.items())[:5]:  # 只显示前5组
            print(f"\n  文件: {dup_files[0]['name']}")
            for f in dup_files:
                print(f"    - {f['path']}")
    
    return report

if __name__ == "__main__":
    main()
