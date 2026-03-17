#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AHL项目文件夹整理工具
扫描、识别重复文件、旧版本，生成整理报告
"""

import os
import hashlib
import json
import re
import sys
from datetime import datetime
from collections import defaultdict
from pathlib import Path
from difflib import SequenceMatcher

# 设置输出编码
sys.stdout.reconfigure(encoding='utf-8')

class AHLFolderOrganizer:
    def __init__(self, target_dir):
        self.target_dir = Path(target_dir)
        self.files_info = []
        self.duplicates = defaultdict(list)
        self.versions = defaultdict(list)
        self.report = {
            'scan_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'target_dir': str(self.target_dir),
            'total_files': 0,
            'total_size': 0,
            'file_types': defaultdict(int),
            'duplicates': {},
            'versions': {},
            'recommendations': []
        }

    def calculate_hash(self, filepath, chunk_size=8192):
        """计算文件MD5哈希"""
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(chunk_size), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            return f"error: {e}"

    def similarity(self, str1, str2):
        """计算两个字符串的相似度"""
        return SequenceMatcher(None, str1, str2).ratio()

    def extract_version(self, filename):
        """从文件名中提取版本号"""
        # 匹配 V1.0, V2.0, v1, v2, 版本1, 版本2 等模式
        patterns = [
            r'[Vv](\d+(?:\.\d+)?)',  # V1.0, v2
            r'版本(\d+(?:\.\d+)?)',  # 版本1.0
            r'第(\d+)版',  # 第1版
            r'V(\d+)_',   # V1_
            r'_(\d+)(?:\.\d+)?_',  # _1.0_
        ]
        
        for pattern in patterns:
            match = re.search(pattern, filename)
            if match:
                return match.group(1)
        return None

    def extract_base_name(self, filename):
        """提取文件基础名（去除版本号）"""
        # 移除版本号相关部分
        base = re.sub(r'[Vv]\d+(?:\.\d+)?', '', filename)
        base = re.sub(r'版本\d+(?:\.\d+)?', '', base)
        base = re.sub(r'第\d+版', '', base)
        base = re.sub(r'_+', '_', base)  # 合并多个下划线
        base = re.sub(r'\s+', ' ', base)  # 合并多个空格
        return base.strip('_ ')

    def scan_files(self):
        """扫描目录下的所有文件"""
        print(f"Scanning directory: {self.target_dir}")
        
        if not self.target_dir.exists():
            print(f"Error: Directory does not exist: {self.target_dir}")
            return False

        for root, dirs, files in os.walk(self.target_dir):
            for filename in files:
                filepath = Path(root) / filename
                try:
                    stat = filepath.stat()
                    file_info = {
                        'path': str(filepath),
                        'name': filename,
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                        'extension': filepath.suffix.lower(),
                        'hash': None,  # 延迟计算
                        'version': self.extract_version(filename),
                        'base_name': self.extract_base_name(filename)
                    }
                    self.files_info.append(file_info)
                    self.report['total_files'] += 1
                    self.report['total_size'] += stat.st_size
                    self.report['file_types'][file_info['extension']] += 1
                except Exception as e:
                    print(f"  Warning: Cannot read file {filepath}: {e}")

        print(f"  Found {self.report['total_files']} files")
        return True

    def find_duplicates(self):
        """识别重复文件"""
        print("\nIdentifying duplicate files...")
        
        # 按大小分组
        size_groups = defaultdict(list)
        for f in self.files_info:
            size_groups[f['size']].append(f)

        # 对相同大小的文件计算哈希
        duplicate_groups = []
        processed = 0
        for size, files in size_groups.items():
            if len(files) > 1:
                hash_groups = defaultdict(list)
                for f in files:
                    f['hash'] = self.calculate_hash(f['path'])
                    processed += 1
                    hash_groups[f['hash']].append(f)
                
                for hash_val, dup_files in hash_groups.items():
                    if len(dup_files) > 1 and not hash_val.startswith('error'):
                        duplicate_groups.append(dup_files)

        # 也检查同名文件（可能内容不同但名字相同）
        name_groups = defaultdict(list)
        for f in self.files_info:
            name_groups[f['name']].append(f)

        same_name_groups = []
        for name, files in name_groups.items():
            if len(files) > 1:
                same_name_groups.append(files)

        self.report['duplicates']['exact'] = [
            [{'path': f['path'], 'name': f['name'], 'size': f['size'], 'modified': f['modified']} 
             for f in group] 
            for group in duplicate_groups
        ]
        
        self.report['duplicates']['same_name'] = [
            [{'path': f['path'], 'name': f['name'], 'size': f['size'], 'modified': f['modified']} 
             for f in group] 
            for group in same_name_groups
        ]

        print(f"  Found {len(duplicate_groups)} groups of exact duplicates")
        print(f"  Found {len(same_name_groups)} groups of same-name files")

    def find_versions(self):
        """识别版本演进关系"""
        print("\nIdentifying version files...")
        
        # 按基础名称分组
        base_groups = defaultdict(list)
        for f in self.files_info:
            if f['version']:
                base_groups[f['base_name']].append(f)

        version_chains = []
        for base_name, files in base_groups.items():
            if len(files) > 1:
                # 按版本号排序
                def version_key(x):
                    try:
                        return float(x['version'])
                    except:
                        return 0
                sorted_files = sorted(files, key=version_key)
                version_chains.append({
                    'base_name': base_name,
                    'versions': [
                        {
                            'version': f['version'],
                            'path': f['path'],
                            'name': f['name'],
                            'modified': f['modified'],
                            'size': f['size']
                        }
                        for f in sorted_files
                    ]
                })

        self.report['versions'] = version_chains
        print(f"  Found {len(version_chains)} groups of version files")

    def generate_recommendations(self):
        """生成归档建议"""
        recommendations = []

        # 重复文件建议
        if self.report['duplicates']['exact']:
            recommendations.append({
                'category': 'Duplicate File Cleanup',
                'priority': 'High',
                'description': f'Found {len(self.report["duplicates"]["exact"])} groups of exact duplicate files',
                'actions': [
                    'Keep the most recently modified file',
                    'Delete other duplicate files',
                    'Or create hard links to save space'
                ]
            })

        if self.report['duplicates']['same_name']:
            recommendations.append({
                'category': 'Same-Name File Check',
                'priority': 'Medium',
                'description': f'Found {len(self.report["duplicates"]["same_name"])} groups of same-name files',
                'actions': [
                    'Check if content is the same',
                    'If different, consider renaming to distinguish',
                    'If same, keep the latest version'
                ]
            })

        # 版本文件建议
        if self.report['versions']:
            total_old_versions = sum(len(v['versions']) - 1 for v in self.report['versions'])
            recommendations.append({
                'category': 'Old Version Archiving',
                'priority': 'Medium',
                'description': f'Found {len(self.report["versions"])} version groups, {total_old_versions} old versions',
                'actions': [
                    'Create "Archive/Old Versions" folder',
                    'Move non-latest versions to archive folder',
                    'Keep latest version in main directory'
                ]
            })

        # 按文件类型建议
        large_extensions = sorted(
            self.report['file_types'].items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        if large_extensions:
            recommendations.append({
                'category': 'File Type Distribution',
                'priority': 'Low',
                'description': f'Main file types: {", ".join([f"{ext}({count})" for ext, count in large_extensions])}',
                'actions': [
                    'Consider organizing by file type',
                    'e.g., Documents/, Images/, Data/, Archive/'
                ]
            })

        # 文件大小建议
        total_size_mb = self.report['total_size'] / (1024 * 1024)
        if total_size_mb > 100:
            recommendations.append({
                'category': 'Large File Management',
                'priority': 'Low',
                'description': f'Total file size: {total_size_mb:.2f} MB',
                'actions': [
                    'Consider compressing old files',
                    'Move rarely used large files to external storage'
                ]
            })

        self.report['recommendations'] = recommendations

    def generate_file_list(self):
        """生成完整文件清单"""
        return [
            {
                'path': f['path'],
                'name': f['name'],
                'size': f['size'],
                'size_human': self.human_readable_size(f['size']),
                'modified': f['modified'],
                'extension': f['extension'],
                'version': f['version']
            }
            for f in sorted(self.files_info, key=lambda x: x['path'])
        ]

    @staticmethod
    def human_readable_size(size_bytes):
        """转换字节为人类可读格式"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} TB"

    def save_reports(self, output_dir):
        """保存报告到文件"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # 1. 完整JSON报告
        json_report = output_path / f'AHL_Organize_Report_{timestamp}.json'
        with open(json_report, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, ensure_ascii=False, indent=2)
        print(f"\n  JSON report saved: {json_report}")

        # 2. 完整文件清单
        file_list = self.generate_file_list()
        list_report = output_path / f'AHL_File_List_{timestamp}.json'
        with open(list_report, 'w', encoding='utf-8') as f:
            json.dump(file_list, f, ensure_ascii=False, indent=2)
        print(f"  File list saved: {list_report}")

        # 3. 可读文本报告
        text_report = output_path / f'AHL_Organize_Report_{timestamp}.txt'
        with open(text_report, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("AHL Project Folder Organization Report\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Scan Time: {self.report['scan_time']}\n")
            f.write(f"Target Directory: {self.report['target_dir']}\n")
            f.write(f"Total Files: {self.report['total_files']}\n")
            f.write(f"Total Size: {self.human_readable_size(self.report['total_size'])}\n\n")

            # 文件类型统计
            f.write("-" * 40 + "\n")
            f.write("File Type Distribution\n")
            f.write("-" * 40 + "\n")
            for ext, count in sorted(self.report['file_types'].items(), key=lambda x: x[1], reverse=True):
                f.write(f"  {ext or '(no extension)'}: {count} files\n")
            f.write("\n")

            # 重复文件
            f.write("-" * 40 + "\n")
            f.write("Duplicate File Analysis\n")
            f.write("-" * 40 + "\n")
            
            if self.report['duplicates']['exact']:
                f.write(f"\n[Exact Duplicates] {len(self.report['duplicates']['exact'])} groups\n")
                for i, group in enumerate(self.report['duplicates']['exact'], 1):
                    f.write(f"\n  Duplicate Group {i}:\n")
                    for f_info in group:
                        f.write(f"    - {f_info['name']}\n")
                        f.write(f"      Path: {f_info['path']}\n")
                        f.write(f"      Size: {self.human_readable_size(f_info['size'])}, Modified: {f_info['modified']}\n")
            else:
                f.write("\nNo exact duplicates found\n")

            if self.report['duplicates']['same_name']:
                f.write(f"\n[Same-Name Files] {len(self.report['duplicates']['same_name'])} groups\n")
                for i, group in enumerate(self.report['duplicates']['same_name'], 1):
                    f.write(f"\n  Same-Name Group {i}: {group[0]['name']}\n")
                    for f_info in group:
                        f.write(f"    - {f_info['path']}\n")
                        f.write(f"      Size: {self.human_readable_size(f_info['size'])}, Modified: {f_info['modified']}\n")

            # 版本演进
            f.write("\n" + "-" * 40 + "\n")
            f.write("Version Evolution Analysis\n")
            f.write("-" * 40 + "\n")
            
            if self.report['versions']:
                f.write(f"\nFound {len(self.report['versions'])} version groups:\n")
                for chain in self.report['versions']:
                    f.write(f"\n  Base Name: {chain['base_name']}\n")
                    f.write(f"  Version Evolution:\n")
                    for v in chain['versions']:
                        f.write(f"    [{v['version']}] {v['name']}\n")
                        f.write(f"      Modified: {v['modified']}, Size: {self.human_readable_size(v['size'])}\n")
            else:
                f.write("\nNo version files found\n")

            # 建议
            f.write("\n" + "=" * 80 + "\n")
            f.write("Archiving Recommendations\n")
            f.write("=" * 80 + "\n")
            
            for rec in self.report['recommendations']:
                f.write(f"\n[{rec['category']}] Priority: {rec['priority']}\n")
                f.write(f"  Description: {rec['description']}\n")
                f.write(f"  Recommended Actions:\n")
                for action in rec['actions']:
                    f.write(f"    - {action}\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("End of Report\n")
            f.write("=" * 80 + "\n")

        print(f"  Text report saved: {text_report}")
        return json_report, list_report, text_report

    def run(self):
        """运行完整扫描流程"""
        print("=" * 60)
        print("AHL Project Folder Organization Tool")
        print("=" * 60)

        # 1. 扫描文件
        if not self.scan_files():
            return False

        # 2. 识别重复
        self.find_duplicates()

        # 3. 识别版本
        self.find_versions()

        # 4. 生成建议
        self.generate_recommendations()

        # 5. 保存报告
        output_dir = self.target_dir / "_Organization_Reports"
        reports = self.save_reports(output_dir)

        print("\n" + "=" * 60)
        print("Scan Complete!")
        print(f"Reports saved to: {output_dir}")
        print("=" * 60)

        return reports


if __name__ == "__main__":
    target_dir = r"C:\Users\Administrator\Desktop\张实项目总控\06-AHL-去中心化旅行平台"
    organizer = AHLFolderOrganizer(target_dir)
    organizer.run()
