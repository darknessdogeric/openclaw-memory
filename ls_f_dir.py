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

base = 'F:'
for dir_name in ['重点项目', '运营文件', '行业资料文件夹', '商贸提案']:
    dir_path = base + '/' + dir_name
    print(f'\n=== {dir_name} ===')
    if not os.path.exists(dir_path):
        print('  (does not exist)')
        continue
    items = listdir(dir_path)
    print(f'  {len(items)} items')
    for name, is_dir in sorted(items, key=lambda x: x[0])[:10]:
        if is_dir:
            sub = listdir(dir_path + '/' + name)
            print(f'  [DIR]  {name}/ ({len(sub)} sub-items)')
        else:
            try:
                full = os.path.join(dir_path, name)
                sz = os.path.getsize(full)
                print(f'  {sz//1024:>6}KB  {name}')
            except:
                print(f'  ???KB  {name}')
    if len(items) > 10:
        print(f'  ... and {len(items)-10} more')
