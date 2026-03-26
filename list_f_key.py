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

def listdir_w(path):
    data = wintypes.WIN32_FIND_DATAW()
    h = FindFirstFileW(path, ctypes.byref(data))
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

def walkdir(path):
    stack = [path]
    while stack:
        current = stack.pop()
        items = listdir_w(current + '/*')
        for name, is_dir in items:
            full = current + '/' + name
            yield full, name, is_dir
            if is_dir:
                stack.append(full)

def find_files_w(root, extensions=None):
    results = []
    for full, name, is_dir in walkdir(root):
        if not is_dir:
            for ext in (extensions or []):
                if name.lower().endswith(ext):
                    try:
                        sz = os.path.getsize(full)
                        results.append((full, name, sz))
                    except:
                        pass
                    break
    return results

# Find all PDFs in F:/ using Windows API for listing
print('Finding all PDFs in F:/ ...')
pdfs = []
for full, name, is_dir in walkdir('F:/'):
    if not is_dir and name.lower().endswith('.pdf'):
        try:
            sz = os.path.getsize(full)
            pdfs.append((full, name, sz))
        except:
            pass

pdfs.sort(key=lambda x: x[2], reverse=True)
print(f'Found {len(pdfs)} PDF files')
for full, name, sz in pdfs[:20]:
    print(f'{sz//1024:>6}KB  {name}')

# Try to read the largest PDFs
print('\n=== Reading key documents ===\n')

for full, name, sz in pdfs[:10]:
    if sz < 500*1024:  # Skip files > 500KB for quick reading
        continue
    try:
        print(f'=== {name} ({sz//1024}KB) ===')
        with pdfplumber.open(full) as pdf:
            pages = len(pdf.pages)
            print(f'Pages: {pages}')
            text = ''
            for page in pdf.pages[:5]:
                t = page.extract_text()
                if t:
                    text += t + '\n'
        print(text[:1500])
        print('...\n')
    except Exception as e:
        print(f'Error: {e}\n')
