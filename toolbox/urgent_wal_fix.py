#!/usr/bin/env python3
"""Urgent WAL fix - try short connections with quick checkpoint"""
import sqlite3, os, sys, time

db = os.path.expanduser('~/.openclaw/state/openclaw.sqlite')
wal = db + '-wal'
shm = db + '-shm'

def main():
    print(f"DB: {db}")
    print(f"  size: {os.path.getsize(db)//1024} KB")
    print(f"  wal: {os.path.getsize(wal)//1024} KB")
    print(f"  shm: {os.path.getsize(shm)//1024} KB")
    print()
    
    # Quick integrity check first
    try:
        conn = sqlite3.connect(db, timeout=5)
        cur = conn.cursor()
        cur.execute('PRAGMA quick_check')
        print(f'Quick check: {cur.fetchone()}')
        conn.close()
    except Exception as e:
        print(f'Quick check FAILED: {e}')
        return
    
    # Try TRUNCATE checkpoint (short connection)
    print('\n=== Trying TRUNCATE checkpoint ===')
    for attempt in range(8):
        try:
            conn = sqlite3.connect(db, timeout=3)
            cur = conn.cursor()
            cur.execute('PRAGMA wal_checkpoint(TRUNCATE)')
            result = cur.fetchone()
            conn.close()
            status = 'OK' if result[0] == 0 else f'BUSY (in_wal={result[1]}, checkpointed={result[2]})'
            print(f'Attempt {attempt+1}: {status}')
            if result[0] == 0:
                print('  CHECKPOINT SUCCESS!')
                break
        except Exception as e:
            print(f'Attempt {attempt+1}: ERROR - {e}')
        time.sleep(1)
    
    print()
    print(f"=== File sizes after fix ===")
    print(f"  DB: {os.path.getsize(db)//1024} KB")
    print(f"  WAL: {os.path.getsize(wal)//1024} KB")
    print(f"  SHM: {os.path.getsize(shm)//1024} KB")

if __name__ == '__main__':
    main()