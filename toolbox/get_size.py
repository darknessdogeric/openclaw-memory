import os
import sys
total = 0
count = 0
for root, dirs, files in os.walk(sys.argv[1]):
    for f in files:
        try:
            fp = os.path.join(root, f)
            sz = os.path.getsize(fp)
            total += sz
            count += 1
        except OSError:
            pass
print(f"Total: {total:,} bytes ({total/1024/1024:.2f} MB), {count} files")
