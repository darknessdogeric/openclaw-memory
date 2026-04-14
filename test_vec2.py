import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3, os, sqlite_vec

ext_path = sqlite_vec.loadable_path()
print(f'Extension path: {ext_path}')

# Try load_extension function
conn = sqlite3.connect(':memory:')
conn.enable_load_extension(True)
try:
    result = conn.execute("SELECT load_extension(?)", (ext_path,)).fetchone()
    print(f'load_extension() result: {result}')
    # Try to create vec0 table
    conn.execute('CREATE VIRTUAL TABLE t USING vec0(float[3])')
    print('vec0 table: OK')
except Exception as e:
    print(f'Error: {type(e).__name__}: {e}')
