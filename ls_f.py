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

data = wintypes.WIN32_FIND_DATAW()
h = FindFirstFileW('F:/*', ctypes.byref(data))
if h != INVALID_HANDLE_VALUE:
    count = 0
    while True:
        name = data.cFileName
        if name not in ('.', '..'):
            is_dir = bool(data.dwFileAttributes & 0x10)
            suffix = '/ (DIR)' if is_dir else ''
            print(f'{name}{suffix}')
            count += 1
        if not FindNextFileW(h, ctypes.byref(data)):
            break
    FindClose(h)
    print(f'Total: {count}')
else:
    print('FindFirstFileW failed')
