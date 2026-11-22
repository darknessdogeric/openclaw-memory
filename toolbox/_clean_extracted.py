"""Clean .doc WordDocument stream — extract only Chinese text."""
import olefile, re, os, json

desktop = r'C:\Users\ericz\Desktop'
fname = '关于召开”十五五“发展规划研讨会的预通知(1).doc'
path = os.path.join(desktop, fname)

ole = olefile.OleFileIO(path)

# Stream 1 — summary metadata
print('=== SummaryInformation ===')
try:
    meta = ole.get_metadata()
    for attr in ['title', 'subject', 'author', 'keywords', 'comments', 'last_saved_by']:
        v = getattr(meta, attr, None)
        if v:
            print(f'  {attr}: {v}')
    print(f'  create_time: {meta.create_time}')
    print(f'  last_saved_time: {meta.last_saved_time}')
except Exception as e:
    print(f'  meta error: {e}')

# Stream 2 — WordDocument (text content)
def extract_clean_chinese(raw_bytes):
    """Extract Chinese text using heuristic UTF-16LE decoding + filter."""
    # Word streams store text in UTF-16LE
    try:
        text = raw_bytes.decode('utf-16-le', errors='ignore')
    except:
        text = raw_bytes.decode('gbk', errors='ignore')
    # Strip control chars except newlines
    text = re.sub(r'[\x00-\x08\x0b-\x1f\x7f]', '', text)
    # Extract runs of Chinese + ASCII text
    chunks = re.findall(r'[\u4e00-\u9fff\w\s,。，；：、（）()【】《》!?/．.\\d\\-_+\\.\\:\\-\\/\\(\\)\\[\\]<>a-zA-Z%\\u00b0]+', text)
    return [c.strip() for c in chunks if c.strip() and len(c.strip()) > 1]

# Pull WordDocument stream
word_data = ole.openstream('WordDocument').read()

# Locate the actual text region
# In .doc WordDocument stream: at offset 0x10C (FIB.fcMin) starts
# But simpler: just look for clusters of Chinese characters

# Convert to readable text via UTF-16LE decoding of consecutive Chinese bytes
def smart_decode(b):
    """Try multiple encodings."""
    for enc in ['utf-16-le', 'utf-8', 'gbk']:
        try:
            t = b.decode(enc, errors='ignore')
            t = re.sub(r'[^\u4e00-\u9fff\w\s,。；：、（）()【】《》!?/．.\-:：+\-\d%°a-zA-Z\u201c\u201d\u3000-\u303f\uff00-\uffef]', '', t)
            # Filter short noise
            lines = [l.strip() for l in t.split('\n') if l.strip() and sum(1 for c in l if '\u4e00' <= c <= '\u9fff') > 1]
            return lines
        except:
            continue
    return []

# Look for high-density text regions
results = []
# Method 1: full UTF-16LE decode
try:
    decoded = word_data.decode('utf-16-le', errors='ignore')
    # Now extract only Chinese lines
    cleaned = re.sub(r'[\x00-\x08\x0b-\x1f\x7f]', '\n', decoded)
    lines = cleaned.split('\n')
    last_was_empty = True
    buf = []
    for ln in lines:
        s = ln.strip()
        # Filter out pure noise lines
        chinese_count = sum(1 for c in s if '\u4e00' <= c <= '\u9fff')
        if chinese_count >= 3:
            results.append(s)
        elif chinese_count > 0 and len(s) > 3 and ('年' in s or '月' in s or '日' in s or '亿' in s or '万' in s):
            results.append(s)
except Exception as e:
    print('decode err:', e)

# Write output
out_path = r'D:\B166ER-OpenClaw\workspace\toolbox\_anyu_notice_clean.txt'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('# 安逸集团"十五五"研讨会预通知 - 原始文本清洗输出\n')
    f.write(f'# 源文件: {fname}\n')
    f.write(f'# 大小: {os.path.getsize(path)} bytes\n')
    f.write(f'# 生成: {os.popen("echo %date% %time%").read().strip()}\n\n')
    f.write('--- METADATA ---\n')
    try:
        meta = ole.get_metadata()
        f.write(f'last_modified: {meta.last_saved_time}\n')
        f.write(f'created: {meta.create_time}\n')
    except:
        pass
    f.write('\n--- CONTENT (Chinese lines, ~{count} lines) ---\n'.format(count=len(results)))
    for i, ln in enumerate(results):
        f.write(f'{i:04d} | {ln}\n')

print(f'Cleaned lines: {len(results)}')
print(f'Output: {out_path}')

ole.close()
