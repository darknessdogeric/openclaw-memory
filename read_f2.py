import os, ctypes
from ctypes import wintypes
import pdfplumber

kernel32 = ctypes.windll.kernel32
INVALID_HANDLE_VALUE = -1
FindFirstFileW = kernel32.FindFirstFileW
FindFirstFileW.argtypes = [wintypes.LPCWSTR, ctypes.POINTER(wintypes.WIN32_FIND_DATAW)]
FindFirstFileW.restype = wintypes.HANDLE
FindNextFileW = kernel32.FindNextFileW
FindNextFileW.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.WIN32_FIND_DATAW)]
FindNextFileW.restype = wintypes.BOOL
FindClose = kernel32.FindClose
FindClose.argtypes = [wintypes.HANDLE]

def listdir(path):
    data = wintypes.WIN32_FIND_DATAW()
    h = FindFirstFileW(path + '/*', ctypes.byref(data))
    results = []
    if h != INVALID_HANDLE_VALUE:
        while True:
            name = data.cFileName
            if name not in ('.', '..'):
                is_dir = bool(data.dwFileAttributes & 0x10)
                results.append((name, is_dir))
            if not FindNextFileW(h, ctypes.byref(data)):
                break
        FindClose(h)
    return results

def find_files(root, patterns, extensions=None):
    results = []
    stack = [root]
    while stack:
        current = stack.pop()
        try:
            items = listdir(current)
        except:
            continue
        for name, is_dir in items:
            full = os.path.join(current, name)
            if is_dir:
                stack.append(full)
            else:
                for p in patterns:
                    if p in name:
                        if extensions is None or any(name.lower().endswith(ext) for ext in extensions):
                            try:
                                sz = os.path.getsize(full)
                                results.append((full, name, sz))
                            except:
                                pass
                        break
    return results

# Find key files in F:/
bases = [
    'F:/重点项目',
    'F:/运营文件', 
    'F:/行业资料文件夹',
    'F:/自我革命',
    'F:/商贸提案',
    'F:/商贸文件',
]

all_files = []
for base in bases:
    if os.path.exists(base):
        found = find_files(base, ['中国旅游', '中旅', '至拓', '至胜', '亚朵', 'IP', '文创'], ['.pdf', '.docx'])
        all_files.extend(found)

# Sort by size descending
all_files.sort(key=lambda x: x[2], reverse=True)

print(f'Found {len(all_files)} key files:')
for full, name, sz in all_files[:15]:
    print(f'{sz//1024:>6}KB  {name}')

# Read the most important ones
print('\n=== Reading TOP 3 documents ===\n')

for full, name, sz in all_files[:3]:
    if not full.endswith('.pdf') or sz > 20*1024*1024:
        print(f'Skipping {name} (too large or not PDF)')
        continue
    try:
        print(f'=== {name} ({sz//1024}KB) ===')
        with pdfplumber.open(full) as pdf:
            print(f'Pages: {len(pdf.pages)}')
            text = ''
            for page in pdf.pages[:8]:
                t = page.extract_text()
                if t:
                    text += t + '\n'
        # Print first 3000 chars
        print(text[:3000])
        print('\n---END---\n')
    except Exception as e:
        print(f'Error reading {name}: {e}\n')
