#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AHL项目文件夹整理脚本 - 完整版
功能：扫描、清理临时文件、处理重复文件、分类移动文件、版本管理
"""

import os
import shutil
import re
import json
import sys
from datetime import datetime
from collections import defaultdict
from pathlib import Path

# 设置编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 目标目录 - 修正为06-AHL
TARGET_DIR = r"C:\Users\Administrator\Desktop\张实项目总控\06-AHL-去中心化旅行平台"

# 分类规则：关键词 -> 目标目录
CLASSIFICATION_RULES = [
    ("顶层设计", "01-顶层设计/当前版本/"),
    ("架构", "01-顶层设计/当前版本/"),
    ("产品清单", "01-顶层设计/当前版本/"),
    ("商业计划书", "02-商业融资/当前版本/"),
    ("融资", "02-商业融资/当前版本/"),
    ("投资人", "02-商业融资/当前版本/"),
    ("BP", "02-商业融资/当前版本/"),
    ("SKILL", "03-产品技术/当前版本/"),
    ("AGENT", "03-产品技术/当前版本/"),
    ("SOP", "03-产品技术/当前版本/"),
    ("产品方案", "03-产品技术/当前版本/"),
    ("苏州", "04-运营实施/苏州酒管公司项目/"),
    ("大理", "04-运营实施/大理0号实验室/"),
    ("PP", "04-运营实施/PP&SOP知识库/"),
    ("市场", "05-市场品牌/"),
    ("竞品", "05-市场品牌/"),
    ("品牌", "05-市场品牌/"),
    ("数据", "06-数据与知识库/"),
]

# 脚本/工具文件扩展名
SCRIPT_EXTENSIONS = ['.py', '.js', '.sh', '.bat', '.ps1', '.vbs']

class AHLFolderOrganizer:
    def __init__(self, target_dir):
        self.target_dir = target_dir
        self.report = {
            "scan_time": datetime.now().isoformat(),
            "target_dir": target_dir,
            "deleted_temp_files": [],
            "duplicate_files_handled": [],
            "moved_files": [],
            "version_handled": [],
            "errors": [],
            "final_structure": {}
        }
        self.all_files = []
        
    def log(self, message):
        """安全打印日志"""
        try:
            print(message)
        except:
            try:
                print(message.encode('gbk', errors='replace').decode('gbk', errors='replace'))
            except:
                pass
        
    def scan_all_files(self):
        """扫描所有文件（包括子目录）"""
        self.log("=" * 80)
        self.log("[扫描] 正在扫描目录...")
        self.log(f"目标: {self.target_dir}")
        self.all_files = []
        
        for root, dirs, files in os.walk(self.target_dir):
            # 跳过报告文件和特定目录
            if '整理报告' in root or '99-归档管理' in root:
                continue
                
            for file in files:
                # 跳过报告文件
                if file.startswith('整理报告_') or file.startswith('AHL_整理报告_'):
                    continue
                    
                file_path = os.path.join(root, file)
                try:
                    stat = os.stat(file_path)
                    self.all_files.append({
                        "path": file_path,
                        "name": file,
                        "size": stat.st_size,
                        "mtime": stat.st_mtime,
                        "mtime_str": datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                        "relative_path": os.path.relpath(file_path, self.target_dir)
                    })
                except Exception as e:
                    self.report["errors"].append(f"扫描文件出错 {file_path}: {str(e)}")
        
        self.log(f"[扫描] 找到 {len(self.all_files)} 个文件")
        for f in self.all_files[:20]:  # 显示前20个文件
            self.log(f"  - {f['relative_path']}")
        if len(self.all_files) > 20:
            self.log(f"  ... 还有 {len(self.all_files) - 20} 个文件")
        return self.all_files
    
    def delete_temp_files(self):
        """删除所有~$开头的Office临时文件"""
        self.log("\n" + "=" * 80)
        self.log("[清理] 正在删除临时文件...")
        temp_files = [f for f in self.all_files if f["name"].startswith("~$")]
        
        for file_info in temp_files:
            try:
                os.remove(file_info["path"])
                self.report["deleted_temp_files"].append({
                    "path": file_info["path"],
                    "name": file_info["name"],
                    "size": file_info["size"]
                })
                self.log(f"  删除: {file_info['name']}")
            except Exception as e:
                self.report["errors"].append(f"删除临时文件失败 {file_info['path']}: {str(e)}")
        
        # 从all_files中移除已删除的文件
        self.all_files = [f for f in self.all_files if not f["name"].startswith("~$")]
        self.log(f"[清理] 共删除 {len(temp_files)} 个临时文件")
        return len(temp_files)
    
    def find_duplicate_files(self):
        """查找重复文件（基于文件名，忽略大小写和版本号）"""
        self.log("\n" + "=" * 80)
        self.log("[查重] 正在查找重复文件...")
        
        # 按文件名分组（忽略扩展名和版本号）
        file_groups = defaultdict(list)
        
        for file_info in self.all_files:
            name = file_info["name"]
            # 提取基础名称（去掉版本号如V1.0, V2.0等）
            base_name = re.sub(r'[_\-]?[vV]\d+(\.\d+)?', '', name)
            base_name = re.sub(r'\.(docx?|pdf|xlsx?|pptx?|txt|md|json)$', '', base_name, flags=re.IGNORECASE)
            base_name = base_name.lower().strip()
            
            if base_name and len(base_name) > 2:  # 避免太短的名称
                file_groups[base_name].append(file_info)
        
        # 找出有重复的文件组（排除报告文件）
        duplicates = {k: v for k, v in file_groups.items() if len(v) > 1}
        self.log(f"[查重] 找到 {len(duplicates)} 组重复文件")
        for k, v in duplicates.items():
            self.log(f"  组 '{k}': {len(v)} 个文件")
            for f in v:
                self.log(f"    - {f['name']} ({f['mtime_str']})")
        return duplicates
    
    def handle_duplicate_files(self, duplicates):
        """处理重复文件，保留最新版本"""
        self.log("\n" + "=" * 80)
        self.log("[去重] 正在处理重复文件...")
        
        deleted_paths = []
        for base_name, files in duplicates.items():
            # 按修改时间排序，最新的在前
            files_sorted = sorted(files, key=lambda x: x["mtime"], reverse=True)
            
            # 保留最新的，删除其他的
            keep_file = files_sorted[0]
            delete_files = files_sorted[1:]
            
            self.log(f"  保留最新: {keep_file['name']} ({keep_file['mtime_str']})")
            
            for del_file in delete_files:
                try:
                    os.remove(del_file["path"])
                    self.report["duplicate_files_handled"].append({
                        "kept": keep_file["path"],
                        "deleted": del_file["path"],
                        "reason": f"保留最新版本 ({keep_file['mtime_str']} vs {del_file['mtime_str']})"
                    })
                    deleted_paths.append(del_file["path"])
                    self.log(f"    删除旧版: {del_file['name']} ({del_file['mtime_str']})")
                except Exception as e:
                    self.report["errors"].append(f"删除重复文件失败 {del_file['path']}: {str(e)}")
        
        # 从all_files中移除已删除的文件
        self.all_files = [f for f in self.all_files if f["path"] not in deleted_paths]
        self.log(f"[去重] 共处理 {len(duplicates)} 组重复文件")
    
    def extract_version_info(self, filename):
        """从文件名中提取版本信息"""
        version_match = re.search(r'[vV](\d+(?:\.\d+)?)', filename)
        if version_match:
            return version_match.group(1)
        return None
    
    def classify_file(self, file_info):
        """根据文件名关键词分类文件"""
        filename = file_info["name"]
        filename_lower = filename.lower()
        
        # 检查是否是脚本/工具文件
        ext = os.path.splitext(filename)[1].lower()
        if ext in SCRIPT_EXTENSIONS or "脚本" in filename or "工具" in filename:
            return "07-工具与脚本/"
        
        # 根据关键词匹配
        for keyword, target_dir in CLASSIFICATION_RULES:
            if keyword.lower() in filename_lower:
                return target_dir
        
        return None
    
    def move_files(self):
        """移动文件到对应分类目录"""
        self.log("\n" + "=" * 80)
        self.log("[分类] 正在分类移动文件...")
        
        # 创建必要的目录
        dirs_to_create = [
            "01-顶层设计/当前版本/",
            "01-顶层设计/历史版本/",
            "02-商业融资/当前版本/",
            "02-商业融资/历史版本/",
            "03-产品技术/当前版本/",
            "03-产品技术/历史版本/",
            "04-运营实施/苏州酒管公司项目/",
            "04-运营实施/大理0号实验室/",
            "04-运营实施/PP&SOP知识库/",
            "05-市场品牌/",
            "06-数据与知识库/",
            "07-工具与脚本/",
            "99-归档管理/整理报告/",
        ]
        
        for dir_path in dirs_to_create:
            full_path = os.path.join(self.target_dir, dir_path)
            os.makedirs(full_path, exist_ok=True)
        
        self.log("[分类] 已创建分类目录")
        
        # 按基础名称分组，处理版本
        file_groups = defaultdict(list)
        for file_info in self.all_files:
            filename = file_info["name"]
            # 提取基础名称（去掉版本号）
            base_name = re.sub(r'[_\-]?[vV]\d+(\.\d+)?', '', filename)
            base_name = re.sub(r'\.(docx?|pdf|xlsx?|pptx?|txt|md|json)$', '', base_name, flags=re.IGNORECASE)
            base_name = base_name.lower().strip()
            if base_name:
                file_groups[base_name].append(file_info)
        
        # 移动文件
        moved_count = 0
        for base_name, files in file_groups.items():
            # 按修改时间排序，最新的在前
            files_sorted = sorted(files, key=lambda x: x["mtime"], reverse=True)
            
            for idx, file_info in enumerate(files_sorted):
                version = self.extract_version_info(file_info["name"])
                target_subdir = self.classify_file(file_info)
                
                if target_subdir:
                    # 判断是放入当前版本还是历史版本
                    if idx == 0:
                        # 最新版本放入当前版本
                        dest_dir = target_subdir
                    else:
                        # 旧版本放入历史版本
                        dest_dir = target_subdir.replace("当前版本/", "历史版本/")
                    
                    dest_path = os.path.join(self.target_dir, dest_dir, file_info["name"])
                    
                    # 如果已经在目标位置，跳过
                    if os.path.normpath(file_info["path"]) == os.path.normpath(dest_path):
                        continue
                    
                    # 如果目标位置已存在同名文件，添加序号
                    counter = 1
                    original_dest = dest_path
                    while os.path.exists(dest_path):
                        name, ext = os.path.splitext(original_dest)
                        dest_path = f"{name}_{counter}{ext}"
                        counter += 1
                    
                    try:
                        shutil.move(file_info["path"], dest_path)
                        self.report["moved_files"].append({
                            "from": file_info["path"],
                            "to": dest_path,
                            "category": dest_dir,
                            "is_latest": idx == 0,
                            "version": version
                        })
                        self.log(f"  移动: {file_info['name']} -> {dest_dir}")
                        moved_count += 1
                    except Exception as e:
                        self.report["errors"].append(f"移动文件失败 {file_info['path']}: {str(e)}")
        
        self.log(f"[分类] 共移动 {moved_count} 个文件")
        return moved_count
    
    def generate_final_structure(self):
        """生成最终目录结构"""
        self.log("\n" + "=" * 80)
        self.log("[结构] 正在生成最终目录结构...")
        
        structure = {}
        for root, dirs, files in os.walk(self.target_dir):
            # 跳过报告文件
            files = [f for f in files if not f.startswith('整理报告_') and not f.startswith('AHL_整理报告_')]
            
            # 计算相对路径
            rel_path = os.path.relpath(root, self.target_dir)
            if rel_path == '.':
                rel_path = ''
            
            # 只记录有文件的目录
            if files:
                structure[rel_path] = {
                    "files": files,
                    "file_count": len(files)
                }
        
        self.report["final_structure"] = structure
        return structure
    
    def save_report(self):
        """保存报告到文件"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 保存JSON报告
        report_path = os.path.join(self.target_dir, "99-归档管理", "整理报告", f"AHL_整理报告_{timestamp}.json")
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(self.report, f, ensure_ascii=False, indent=2)
            self.log(f"\n[报告] JSON报告已保存: {report_path}")
        except Exception as e:
            self.log(f"[警告] 保存JSON报告失败: {str(e)}")
        
        # 生成文本报告
        txt_report_path = os.path.join(self.target_dir, "99-归档管理", "整理报告", f"AHL_整理报告_{timestamp}.txt")
        try:
            with open(txt_report_path, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("AHL项目文件夹整理报告\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"扫描时间: {self.report['scan_time']}\n")
                f.write(f"目标目录: {self.report['target_dir']}\n\n")
                
                f.write("-" * 80 + "\n")
                f.write(f"1. 删除的临时文件 ({len(self.report['deleted_temp_files'])} 个)\n")
                f.write("-" * 80 + "\n")
                for item in self.report['deleted_temp_files']:
                    f.write(f"   - {item['name']} ({item['size']} bytes)\n")
                
                f.write("\n" + "-" * 80 + "\n")
                f.write(f"2. 处理的重复文件 ({len(self.report['duplicate_files_handled'])} 组)\n")
                f.write("-" * 80 + "\n")
                for item in self.report['duplicate_files_handled']:
                    f.write(f"   保留: {os.path.basename(item['kept'])}\n")
                    f.write(f"   删除: {os.path.basename(item['deleted'])}\n")
                    f.write(f"   原因: {item['reason']}\n\n")
                
                f.write("\n" + "-" * 80 + "\n")
                f.write(f"3. 移动的文件 ({len(self.report['moved_files'])} 个)\n")
                f.write("-" * 80 + "\n")
                for item in self.report['moved_files']:
                    f.write(f"   {os.path.basename(item['from'])}\n")
                    f.write(f"      -> {item['category']}\n")
                    f.write(f"      (最新版本: {'是' if item['is_latest'] else '否'})\n\n")
                
                f.write("\n" + "-" * 80 + "\n")
                f.write("4. 最终目录结构\n")
                f.write("-" * 80 + "\n")
                for dir_path, info in sorted(self.report['final_structure'].items()):
                    f.write(f"\n[{dir_path}] ({info['file_count']} 个文件)\n")
                    for fname in info['files']:
                        f.write(f"   - {fname}\n")
                
                if self.report['errors']:
                    f.write("\n" + "-" * 80 + "\n")
                    f.write(f"5. 错误 ({len(self.report['errors'])} 个)\n")
                    f.write("-" * 80 + "\n")
                    for err in self.report['errors']:
                        f.write(f"   ! {err}\n")
                
                f.write("\n" + "=" * 80 + "\n")
                f.write("整理完成\n")
                f.write("=" * 80 + "\n")
            
            self.log(f"[报告] 文本报告已保存: {txt_report_path}")
        except Exception as e:
            self.log(f"[警告] 保存文本报告失败: {str(e)}")
    
    def run(self):
        """执行完整的整理流程"""
        self.log("\n" + "=" * 80)
        self.log("AHL项目文件夹整理工具")
        self.log("=" * 80)
        self.log(f"目标目录: {self.target_dir}")
        
        # 1. 扫描所有文件
        self.scan_all_files()
        
        if len(self.all_files) == 0:
            self.log("\n[警告] 没有找到需要整理的文件")
            return
        
        # 2. 删除临时文件
        self.delete_temp_files()
        
        # 3. 处理重复文件
        duplicates = self.find_duplicate_files()
        if duplicates:
            self.handle_duplicate_files(duplicates)
        
        # 4. 分类移动文件
        self.move_files()
        
        # 5. 生成最终目录结构
        self.generate_final_structure()
        
        # 6. 保存报告
        self.save_report()
        
        self.log("\n" + "=" * 80)
        self.log("整理完成!")
        self.log("=" * 80)
        self.log(f"删除临时文件: {len(self.report['deleted_temp_files'])} 个")
        self.log(f"处理重复文件: {len(self.report['duplicate_files_handled'])} 组")
        self.log(f"移动文件: {len(self.report['moved_files'])} 个")
        self.log(f"错误: {len(self.report['errors'])} 个")


if __name__ == "__main__":
    organizer = AHLFolderOrganizer(TARGET_DIR)
    organizer.run()
