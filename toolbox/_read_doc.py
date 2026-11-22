"""Read old-format .doc via olefile + UTF-16 string scan."""
import olefile, re, os

desktop = r'C:\Users\ericz\Desktop'
fname = '关于召开\u201d十五五\u201c发展规划研讨会的预通知(1).doc'
path = os.path.join(desktop, fname)

print('PATH:', path)
print('SIZE:', os.path.getsize(path), 'bytes')

ole = olefile.OleFileIO(path)
print('\n=== OLE streams ===')
for s in ole.listdir():
    print(' ', '/'.join(s))

# Read all named streams that may contain text
print('\n=== Stream contents (UTF-16 + UTF-8 scan) ===')
candidates = ['WordDocument', 'Text', 'BodyText', '0Table', '1Table']
for name in candidates:
    try:
        if ole.exists(name):
            data = ole.openstream(name).read()
            print(f'\n--- {name} ({len(data)} bytes) ---')
            # Try UTF-16LE
            try:
                txt16 = data.decode('utf-16-le', errors='ignore')
                # clean control chars
                clean = re.sub(r'[\x00-\x08\x0b-\x1f\x7f]', '', txt16)
                # remove runs of empty
                clean = re.sub(r'\s{3,}', '\n', clean)
                lines = [l.strip() for l in clean.split('\n') if l.strip()]
                for ln in lines:
                    if len(ln) > 1:
                        print(f'  | {ln}')
            except Exception as e:
                print(f'  UTF-16 err: {e}')
    except Exception as e:
        print(f'  {name} err: {e}')

ole.close()
