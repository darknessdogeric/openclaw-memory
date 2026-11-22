"""Step 3: Test OfficeCLI with 5-page Chinese PPT."""
import subprocess, os, json, sys

OC = r"D:\OfficeCLI-test\officecli.exe"
TEST_DIR = r"D:\OfficeCLI-test"
PPTX = os.path.join(TEST_DIR, "test_demo.pptx")
LOG = []

def run(cmd, **kw):
    print(f"\n$ {' '.join(cmd)}")
    sys.stdout.flush()
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=120,
            **kw
        )
        out = (result.stdout or '').strip()
        err = (result.stderr or '').strip()
        rc = result.returncode
        print(f"RC={rc}")
        if out: print(f"STDOUT ({len(out)}): {out[:500]}")
        if err: print(f"STDERR ({len(err)}): {err[:500]}")
        LOG.append({"cmd": ' '.join(cmd), "rc": rc, "stdout_len": len(out), "stderr_len": len(err)})
        return result
    except subprocess.TimeoutExpired as e:
        print(f"TIMEOUT: {e}")
        LOG.append({"cmd": ' '.join(cmd), "rc": "TIMEOUT"})
        return None
    except Exception as e:
        print(f"ERROR: {e}")
        LOG.append({"cmd": ' '.join(cmd), "rc": "ERROR", "err": str(e)})
        return None

# Clean slate
for f in [PPTX, PPTX + ".part"]:
    if os.path.exists(f):
        os.remove(f)

print("=== Test 1: create ===")
r = run([OC, "create", PPTX])
created = os.path.exists(PPTX)
print(f"PPTX exists: {created}")
if created:
    print(f"Size: {os.path.getsize(PPTX)} bytes")

print("\n=== Test 2: add slide x 5 with Chinese titles ===")
titles = [
    "酒店供应链管理手册",
    "采购成本下降 25%",
    "供应商分级管理",
    "应急采购 SOP",
    "¥99 整套 13章节",
]
for i, t in enumerate(titles, 1):
    print(f"\n--- Slide {i}: {t} ---")
    r = run([OC, "add", PPTX, "/", "--type", "slide", "--prop", f"title={t}"])

print("\n=== Test 3: view outline ===")
r = run([OC, "view", PPTX, "outline"])

print("\n=== Test 4: view html ===")
r = run([OC, "view", PPTX, "html"])

# Check files
print("\n=== Files in test dir ===")
for f in os.listdir(TEST_DIR):
    full = os.path.join(TEST_DIR, f)
    if os.path.isfile(full):
        print(f"  {f}: {os.path.getsize(full):,} bytes")

# Save log
with open(r"D:\B166ER-OpenClaw\workspace\toolbox\officecli_stage1\test_log.json", 'w', encoding='utf-8') as f:
    json.dump(LOG, f, ensure_ascii=False, indent=2)

print("\nLog saved to test_log.json")
