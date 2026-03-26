import os, ctypes
from ctypes import wintypes

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

# Try to find PDF/DOCX files in home that look like resumes
print('Searching for resume-like files...')
for root, dirs, files in os.walk('C:/Users/ericz'):
    # Skip system folders
    if any(x in root for x in ['AppData', '.cache', '.config', '.claude', '.ssh', '.vscode', 'Application Data', 'Cookies']):
        continue
    for f in files:
        lower = f.lower()
        if any(k in lower for k in ['resume', 'cv', 'jianli', '简历', '履历', '个人简历', '张实', 'zhangshi', 'ericzhang']):
            if f.endswith(('.pdf', '.docx', '.doc')):
                full = os.path.join(root, f)
                sz = os.path.getsize(full)
                print(f'{sz//1024:>6}KB  {full}')

# Also list desktop more carefully
print('\nDesktop contents (all non-dirs):')
desktop = 'C:/Users/ericz/Desktop'
items = listdir(desktop)
for name, is_dir in sorted(items):
    if not is_dir:
        full = os.path.join(desktop, name)
        try:
            sz = os.path.getsize(full)
            print(f'  {sz//1024:>6}KB  {name}')
        except:
            print(f'       ???  {name}')
