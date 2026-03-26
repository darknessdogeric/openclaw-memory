# -*- coding: utf-8 -*-
import subprocess

# Folder name in GBK
folder_name = '管理项目'
folder_name_gbk = folder_name.encode('gbk')
print('Folder name:', folder_name)
print('Folder name GBK bytes:', folder_name_gbk)

# Run dir command
cmd = 'dir /ad /b "' + folder_name + '"'
print('Cmd:', cmd)

result = subprocess.run(['cmd', '/c', cmd], capture_output=True)
raw = result.stdout
print('Raw output length:', len(raw))
print('Raw first 100 bytes:', raw[:100])

# Decode as GBK
text = raw.decode('gbk', errors='replace')
print('\nDecoded output:')
print(text)
