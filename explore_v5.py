# -*- coding: utf-8 -*-
import subprocess

# Use explicit bytes for folder names
folder_map = {
    b'\xb9\xdc\xc0\xed\xcf\xee\xc4\xbf': 'Manage Projects (Hotel)',
    b'\xd4\xcb\xd3\xaa\xce\xc4\xbc\xfe': 'Operations Files',
    b'\xce\xc2\xbe\xc6\xd5\xb9': 'Hotel Expansion',
    b'\xd6\xd0\xc2\xc3\xbe\xc6\xb5\xea\xcf\xe0\xb9\xd8\xc4\xda\xc8\xdd': 'CTS Hotel Related',
    b'\xd6\xf7\xd2\xaa\xbe\xad\xd3\xaa\xca\xfd\xbe\xdd': 'Main Business Data',
    b'\xd7\xd4\xce\xd2\xb8\xef\xc3\xfc': 'Self Revolution',
    b'\xcf\xe5\xd1\xf4\xb9\xb2\xcf\xed\xb9\xfa\xbc\xca\xce\xc4\xbc\xfe': 'Xiangyang Shared Intl Docs',
    b'\xb8\xf6\xc8\xcb\xca\xc2\xcf\xee\xb1\xa8\xb8\xe6': 'Personal Reports',
    b'\xd0\xc2\xc3\xbd\xcc\xe5': 'New Media',
    b'\xca\xf6\xd6\xb0\xb1\xa8\xb8\xe6': 'Work Reports',
}

print("Testing folder access:")
for gbk_bytes, desc in folder_map.items():
    folder_name = gbk_bytes.decode('gbk')
    cmd = 'dir /ad /b "F:\\' + folder_name + '"'
    result = subprocess.run(['cmd', '/c', cmd], capture_output=True)
    raw = result.stdout
    if raw:
        decoded = raw.decode('gbk', errors='replace').strip()
        print(f"\n{desc} ({gbk_bytes}): EXISTS")
        # Get files
        files_cmd = 'dir /a-d /o-s "F:\\' + folder_name + '"'
        files_result = subprocess.run(['cmd', '/c', files_cmd], capture_output=True)
        files_raw = files_result.stdout
        files_text = files_raw.decode('gbk', errors='replace')
        print(files_text[:500])
    else:
        print(f"\n{desc}: NOT FOUND or EMPTY")
