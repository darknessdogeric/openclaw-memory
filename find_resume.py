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

# Search in multiple locations
for base in ['C:/Users/ericz', 'C:/Users/ericz/Documents', 'C:/Users/ericz/Desktop']:
    if not os.path.exists(base):
        continue
    print(f'\n=== {base} ===')
    try:
        items = listdir(base)
        for name, is_dir in sorted(items)[:30]:
            if is_dir:
                print(f'  [DIR]  {name}')
            else:
                try:
                    print(f'         {name}')
                except:
                    pass
    except:
        pass
