import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3, os, sqlite_vec

pkg_path = os.path.dirname(sqlite_vec.__file__)
dll_path = os.path.join(pkg_path, 'vec0.dll')
print(f'DLL: {dll_path}, exists: {os.path.exists(dll_path)}')

conn = sqlite3.connect(':memory:')
conn.enable_load_extension(True)

# Load via PRAGMA directly
try:
    conn.execute(f"PRAGMA load_extension('{dll_path}')")
    print('PRAGMA load_extension: OK')
except Exception as e:
    print(f'PRAGMA error: {e}')

# Try creating table
try:
    conn.execute('CREATE VIRTUAL TABLE t USING vec0(float[3])')
    print('vec0 table: OK')
except Exception as e:
    print(f'vec0 table error: {e}')

# Try sqlite_vec.load
conn2 = sqlite3.connect(':memory:')
try:
    sqlite_vec.load(conn2)
    print('sqlite_vec.load(): OK')
except Exception as e:
    print(f'sqlite_vec.load() error: {type(e).__name__}: {e}')
