"""验证最终交付包结构 + 文件大小"""
import os
import sys

PKG_DIR = r"D:\B166ER-OpenClaw\workspace\outputs\酒管公司供应链工程-交付包-v1.0"


def fmt_size(size):
    if size < 1024:
        return f"{size:,} B"
    elif size < 1024 * 1024:
        return f"{size/1024:.1f} KB"
    else:
        return f"{size/(1024*1024):.2f} MB"


def walk_and_report(root_dir):
    print(f"\n{'='*80}")
    print(f"  交付包结构：{root_dir}")
    print(f"{'='*80}\n")
    
    total_size = 0
    file_count = 0
    pdf_count = 0
    png_count = 0
    
    # 树形展示
    for item in sorted(os.listdir(root_dir)):
        full = os.path.join(root_dir, item)
        if os.path.isdir(full):
            print(f"[DIR] {item}/")
            sub_files = sorted(os.listdir(full))
            for sub in sub_files:
                sub_full = os.path.join(full, sub)
                if os.path.isfile(sub_full):
                    size = os.path.getsize(sub_full)
                    total_size += size
                    file_count += 1
                    ext = os.path.splitext(sub)[1].lower()
                    if ext == ".pdf":
                        pdf_count += 1
                        emoji = "[PDF]"
                    elif ext == ".png":
                        png_count += 1
                        emoji = "[PNG]"
                    elif ext == ".md":
                        emoji = "[MD ]"
                    elif ext == ".html":
                        emoji = "[HTM]"
                    elif ext == ".txt":
                        emoji = "[TXT]"
                    else:
                        emoji = "[???]"
                    rel = os.path.relpath(sub_full, root_dir)
                    print(f"   {emoji} {sub}  ({fmt_size(size)})")
        elif os.path.isfile(full):
            size = os.path.getsize(full)
            total_size += size
            file_count += 1
            ext = os.path.splitext(item)[1].lower()
            if ext == ".pdf":
                pdf_count += 1
                emoji = "[PDF]"
            elif ext == ".png":
                png_count += 1
                emoji = "[PNG]"
            elif ext == ".md":
                emoji = "[MD ]"
            elif ext == ".txt":
                emoji = "[TXT]"
            else:
                emoji = "[???]"
            print(f"{emoji} {item}  ({fmt_size(size)})")
    
    print(f"\n{'='*80}")
    print(f"  Statistics")
    print(f"{'='*80}")
    print(f"  Total files: {file_count}")
    print(f"  PDFs: {pdf_count} (13 chapter + 1 comprehensive + 1 tools)")
    print(f"  PNGs: {png_count} (1x + 2x retina)")
    print(f"  Total size: {fmt_size(total_size)}")
    print()


def main():
    if not os.path.exists(PKG_DIR):
        print(f"ERROR: Directory not found: {PKG_DIR}")
        sys.exit(1)
    walk_and_report(PKG_DIR)
    
    # 验证关键文件存在
    print(f"\n{'='*80}")
    print(f"  Key Files Validation")
    print(f"{'='*80}\n")
    key_files = [
        "B166ER-品牌标.png",
        "README.md",
        "05-网盘说明.txt",
        "01-综合主报告-酒管公司供应链工程全维度体系-v1.0.pdf",
        "03-工具清单-供应链数字化工具矩阵-v1.0.pdf",
        "02-分章节PDFs",
        "04-思维导图",
    ]
    for kf in key_files:
        full = os.path.join(PKG_DIR, kf)
        if os.path.exists(full):
            if os.path.isdir(full):
                cnt = len(os.listdir(full))
                print(f"  [OK] {kf}/ ({cnt} items)")
            else:
                size = os.path.getsize(full)
                print(f"  [OK] {kf} ({fmt_size(size)})")
        else:
            print(f"  [MISSING] {kf}")


if __name__ == "__main__":
    main()