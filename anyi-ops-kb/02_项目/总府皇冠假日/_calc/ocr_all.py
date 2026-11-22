# -*- coding: utf-8 -*-
"""Driver: OCR every page of the contract via isolated subprocesses (crash-proof + resumable)."""
import io, sys, os, subprocess, time, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

D = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"
OUTDIR = os.path.join(D, "ocr_pages")
LOG = os.path.join(D, "ocr_progress.txt")
PY = r"C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe"
os.makedirs(OUTDIR, exist_ok=True)

log = open(LOG, "w", encoding="utf-8", buffering=1)


def say(s):
    log.write(s + "\n")
    print(s, flush=True)


NPAGES = 49
t0 = time.time()
done = 0
for p in range(1, NPAGES + 1):
    f = os.path.join(OUTDIR, f"p{p:02d}.txt")
    if os.path.exists(f) and os.path.getsize(f) > 0:
        done += 1
        continue
    ok = False
    for attempt in (1, 2):
        try:
            r = subprocess.run([PY, os.path.join(D, "ocr_one.py"), str(p), "200"],
                               capture_output=True, timeout=240)
            if r.returncode == 0 and os.path.exists(f) and os.path.getsize(f) > 0:
                ok = True
                break
            say(f"  p{p} attempt{attempt} rc={r.returncode} err={r.stderr.decode('utf-8','ignore')[:160]}")
        except subprocess.TimeoutExpired:
            say(f"  p{p} attempt{attempt} TIMEOUT")
        except Exception as e:
            say(f"  p{p} attempt{attempt} EXC {type(e).__name__}")
        time.sleep(2)
    if not ok:
        open(f, "w", encoding="utf-8").write(f"[OCR FAILED p{p}]")
    done += 1
    say(f"p{p}/{NPAGES} ok={ok} {time.time()-t0:.0f}s")

# 合并
parts = []
for p in range(1, NPAGES + 1):
    f = os.path.join(OUTDIR, f"p{p:02d}.txt")
    t = open(f, encoding="utf-8").read() if os.path.exists(f) else ""
    parts.append(f"\n===== PAGE {p} =====\n{t}")
MERGED = os.path.join(D, "contract_ocr.txt")
open(MERGED, "w", encoding="utf-8").write("".join(parts))
say(f"DONE {os.path.getsize(MERGED)} chars -> {MERGED}")
