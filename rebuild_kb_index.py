"""
重建知识库语义索引
目标：将knowledge-base文件（memory/*.md）纳入语义搜索
"""
import sys, os
sys.path.insert(0, 'C:/Users/ericz/.openclaw/workspace')

from local_semantic_search import index_memory_files
import glob

# 确认memory目录下有哪些kb文件
memory_dir = 'C:/Users/ericz/.openclaw/workspace/memory'
kb_files = glob.glob(os.path.join(memory_dir, '*.md'))
print(f"Knowledge base files found: {len(kb_files)}")
for f in sorted(kb_files):
    size = os.path.getsize(f)
    name = os.path.basename(f)
    print(f"  {name} ({size}B)")

print(f"\nTotal: {len(kb_files)} files")
print("\nRe-indexing...")
index_memory_files()
print("Done.")
