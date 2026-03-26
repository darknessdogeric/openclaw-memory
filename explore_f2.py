import os

# Get full F:\ drive listing
drive = 'F:/'
try:
    items = os.listdir(drive)
    print('F:/ root items:')
    for item in sorted(items):
        path = os.path.join(drive, item)
        if os.path.isdir(path):
            try:
                count = len(os.listdir(path))
                print(f'  [DIR]  {item}/ ({count} items)')
            except:
                print(f'  [DIR]  {item}/')
        else:
            sz = os.path.getsize(path)
            print(f'  [FILE] {item} ({sz//1024}KB)')
except Exception as e:
    print(f'Error: {e}')
