"""visual_edit.py 服务器 API 端到端测试"""
import json
import sys
import time
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = "http://127.0.0.1:8766"


def get(p, timeout=15):
    with urllib.request.urlopen(B + p, timeout=timeout) as r:
        return r.status, r.read()


def post(p, obj=None, timeout=180):
    data = json.dumps(obj).encode() if obj is not None else b""
    req = urllib.request.Request(B + p, data=data,
                                 headers={"Content-Type": "application/json"},
                                 method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()


fails = 0
try:
    st, body = get("/")
    print(f"  [OK] GET  /            -> {st}, {len(body)} bytes (HTML UI)")

    st, body = get("/api/plan")
    p = json.loads(body)
    n = len(p["slides"])
    print(f"  [OK] GET  /api/plan    -> {st}, {n} 页, title={p.get('title')}")

    st, body = get("/img/5")
    is_png = body[:4] == b"\x89PNG"
    print(f"  [{'OK' if is_png else 'X '}] GET  /img/5       -> {st}, {len(body)} bytes, PNG={is_png}")

    st, body = post("/api/slide/3", {"page_goal": "API 改的第3页结论",
                                     "approved_text_lines": ["API标题", "API要点A"]})
    j = json.loads(body)
    ok = j.get("ok") and j["slide"]["page_goal"] == "API 改的第3页结论"
    if not ok:
        fails += 1
    print(f"  [{'OK' if ok else 'X '}] POST /api/slide/3  -> {st}, ok={j.get('ok')}, "
          f"page_goal={j['slide'].get('page_goal')}")

    st, body = post("/api/rerun/3")
    j = json.loads(body)
    if not j.get("ok"):
        fails += 1
    print(f"  [{'OK' if j.get('ok') else 'X '}] POST /api/rerun/3  -> {st}, ok={j.get('ok')}")
    if j.get("tail"):
        tail = " | ".join(j["tail"].splitlines()[-2:])
        print(f"        tail: {tail[:150]}")

    st, body = post("/api/package")
    j = json.loads(body)
    if not j.get("ok"):
        fails += 1
    print(f"  [{'OK' if j.get('ok') else 'X '}] POST /api/package -> {st}, ok={j.get('ok')}")
    if j.get("tail"):
        print(f"        tail: {j['tail'][:200]}")

except Exception as e:
    print(f"  [X] {type(e).__name__}: {e}")
    fails += 1

print(f"\n失败项: {fails}")
sys.exit(1 if fails else 0)
