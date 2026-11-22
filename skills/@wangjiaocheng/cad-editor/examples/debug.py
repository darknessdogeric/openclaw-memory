with open(r'D:\B166ER-OpenClaw\workspace\skills\@wangjiaocheng\cad-editor\examples\build_sichuan_hotel_1f.py', 'rb') as f:
    lines = f.read().split(b'\n')
print('Line 117 raw bytes:')
print(lines[116])
print()
b = lines[116]
for i, byte in enumerate(b):
    if byte > 127:
        ch = chr(byte) if byte < 128 else '?'
        print(f'pos {i}: byte {byte:02x} char {ch}')