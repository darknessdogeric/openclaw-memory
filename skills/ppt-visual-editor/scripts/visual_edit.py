#!/usr/bin/env python3
"""
visual_edit.py — PPT 在线可视化编辑器 (编排器)

管线 (全部复用 ppt-deck-builder-pro, 零新依赖):
    plan.json  ──┬─> slide-XX.png  (网格预览)
                 └─> 字段编辑 ──> 写回 plan.json ──> rerun_single_page.sh ──> 刷新

子命令:
    serve   启动预览+编辑服务器
    index   只建索引, 打印每页状态表
    status  列出被改过的页
    patch   命令行改一页 (可选 --rerun)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── 定位 ppt-deck-builder-pro 的 scripts 目录 ──
BASH_CANDIDATES = [
    r"D:\Git\usr\bin\bash.exe",
    r"C:\Program Files\Git\bin\bash.exe",
    "/usr/bin/bash", "/bin/bash",
]


def find_deck_skill() -> Path | None:
    """定位 ppt-deck-builder-pro 目录"""
    cands = [
        Path(r"D:\B166ER-openclaw\workspace\skills\ppt-deck-builder-pro"),
        Path(__file__).resolve().parent.parent.parent / "ppt-deck-builder-pro",
        Path.home() / ".openclaw" / "skills" / "ppt-deck-builder-pro",
    ]
    for c in cands:
        if (c / "scripts" / "rerun_single_page.sh").exists():
            return c
    return None


def find_bash() -> str | None:
    for b in BASH_CANDIDATES:
        if Path(b).exists():
            return b
    w = shutil.which("bash")
    return w


DECK = find_deck_skill()
BASH = find_bash()
WORKER = os.environ.get("B166ER_VISUAL_WORKER")  # 供并行测试注入


def slide_no(i: int) -> str:
    return f"{i:02d}"


def img_path(images_dir: Path, n: int) -> Path:
    for pat in (f"slide-{slide_no(n)}.*", f"slide_{slide_no(n)}.*", f"slide-{n}.*", f"slide_{n}..*"):
        hits = sorted(images_dir.glob(pat))
        if hits:
            return hits[0]
    return images_dir / f"slide-{slide_no(n)}.png"


def load_plan(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_plan(path: Path, plan: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def find_slide(plan: dict, n: int) -> dict | None:
    for s in plan.get("slides", []):
        if int(s.get("slide_number", 0)) == n:
            return s
    return None


# ══════════════════════════════════════════════════════════
# 核心: 重跑一页
# ══════════════════════════════════════════════════════════
def rerun_one(plan_path: Path, images_dir: Path, n: int,
              resolution: str = "4k", aspect: str = "16:9",
              provider: str | None = None,
              provider_command: str | None = None,
              provider_options: list[str] | None = None,
              timeout: int = 900) -> tuple[bool, str]:
    """重跑单页。
    ⚠️ 必须透传 provider: rerun_single_page.sh 不会自动继承 plan 里的 image_provider,
       若不传, 会回落到 plan 的 provider (真实 API), 导致重跑失败。
       provider 额外参数走 rerun_single_page.sh 的位置 6+ (追加给 generate_from_plan.py)
    """
    if DECK is None or BASH is None:
        return False, "找不到 ppt-deck-builder-pro 或 bash"
    script = DECK / "scripts" / "rerun_single_page.sh"
    cmd = [BASH, str(script), str(plan_path), str(images_dir), str(n), resolution, aspect]
    if provider:
        cmd += ["--provider", provider]
    if provider_command:
        cmd += ["--provider-command", provider_command]
    for po in (provider_options or []):
        cmd += ["--provider-option", po]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        out = (p.stdout or "") + (p.stderr or "")
        ok = p.returncode == 0
        tail = "\n".join(out.strip().splitlines()[-5:]) if out.strip() else "(无输出)"
        return ok, tail
    except subprocess.TimeoutExpired:
        return False, f"重跑超时 (> {timeout}s)"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def package(plan_path: Path, images_dir: Path, out_pptx: Path, timeout: int = 600) -> tuple[bool, str]:
    if DECK is None or BASH is None:
        return False, "找不到 ppt-deck-builder-pro 或 bash"
    script = DECK / "scripts" / "package_image_deck.sh"
    cmd = [BASH, str(script), str(images_dir), str(out_pptx), str(plan_path)]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        out = (p.stdout or "") + (p.stderr or "")
        return p.returncode == 0, ("\n".join(out.strip().splitlines()[-4:]) if out.strip() else "OK")
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


# ══════════════════════════════════════════════════════════
# 前端
# ══════════════════════════════════════════════════════════
PAGE = r"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PPT 可视化编辑器</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:#11151d;color:#e6e8ec;display:flex;height:100vh;overflow:hidden}
#grid{flex:1;overflow:auto;padding:18px}
#side{width:420px;background:#171c26;border-left:1px solid #262d3a;display:flex;flex-direction:column}
#grid h1{font-size:15px;color:#8a93a5;font-weight:600;padding:0 0 12px;letter-spacing:1px}
.cell{display:inline-block;width:320px;margin:0 12px 14px 0;vertical-align:top;cursor:pointer;border:2px solid transparent;border-radius:8px;overflow:hidden;position:relative;background:#0c0f14}
.cell:hover{border-color:#3d7ef0}
.cell.sel{border-color:#f0a93d}
.cell .no{position:absolute;left:0;top:0;background:rgba(0,0,0,.72);color:#ffd;padding:2px 8px;font-size:12px;font-weight:700}
.cell .tag{position:absolute;right:0;top:0;background:rgba(240,169,61,.9);color:#111;padding:2px 7px;font-size:11px;font-weight:700}
.cell img{width:100%;display:block}
.cell .meta{padding:5px 8px;font-size:12px;color:#8a93a5}
#side h2{font-size:16px;padding:14px 16px;border-bottom:1px solid #262d3a;display:flex;justify-content:space-between;align-items:center}
#side .body{flex:1;overflow:auto;padding:14px 16px}
label{display:block;font-size:12px;color:#8a93a5;margin:12px 0 4px;letter-spacing:.5px}
input,textarea{width:100%;background:#0e1219;border:1px solid #2b3340;color:#e6e8ec;border-radius:6px;padding:8px;font-family:inherit;font-size:13px}
textarea{min-height:76px;resize:vertical;line-height:1.5}
.btns{padding:12px 16px;border-top:1px solid #262d3a;display:flex;gap:8px;flex-wrap:wrap}
button{flex:1;min-width:120px;background:#3d7ef0;border:0;color:#fff;padding:10px;border-radius:6px;font-size:13px;font-weight:700;cursor:pointer;font-family:inherit}
button:hover{background:#5a92f5}
button.amber{background:#f0a93d;color:#111}
button.amber:hover{background:#ffbe5c}
button:disabled{opacity:.45;cursor:not-allowed}
#msg{padding:9px 16px;font-size:12px;background:#0e1219;color:#8a93a5;min-height:34px;border-top:1px solid #262d3a;white-space:pre-wrap}
.ok{color:#6fd08c}.err{color:#ef7676}.warn{color:#f0c14b}
</style></head><body>
<div id="grid"><h1 id="title">载入中…</h1><div id="cells"></div></div>
<div id="side">
  <h2><span id="stitle">选择一页</span><span style="font-size:11px;color:#8a93a5" id="sno"></span></h2>
  <div class="body" id="sbody">
    <p style="color:#8a93a5;font-size:13px;line-height:1.7">点左侧任意一页开始编辑。<br><br>
    可改：本页结论 / 可见文字 / 标题 / 文字区 / 提示词覆盖 / 页面类型 / 阅读路径。<br>
    改完点「重跑此页」，图片会自动刷新。</p>
  </div>
  <div class="btns">
    <button class="amber" id="btnRerun" disabled>重跑此页</button>
    <button id="btnPkg" disabled>重新打包 PPTX</button>
  </div>
  <div id="msg">就绪</div>
</div>
<script>
let PLAN=null, CUR=null;
const F=["page_goal","content","page_type","reading_path","text_regions","approved_text_lines","prompt_override"];
const LBL={page_goal:"本页结论 (一句话)",content:"页面标题",page_type:"页面类型",reading_path:"阅读路径",
  text_regions:"文字区说明 (每行一个)",approved_text_lines:"可见文字 (每行一个)",prompt_override:"提示词覆盖 (完全手写)"};
const TYPES=["cover","agenda","path","diagnostic","comparison","cards","matrix","data","chart","dashboard","conclusion"];

function esc(s){return String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));}
function arr(v){return Array.isArray(v)?v.join("\n"):String(v??"");}

async function boot(){
  const r=await fetch("/api/plan");
  PLAN=await r.json();
  document.getElementById("title").textContent=`${PLAN.title||"deck"} · ${PLAN.total_slides||PLAN.slides.length} 页 · ${PLAN.style_preset||""}`;
  render();
}

function render(){
  const c=document.getElementById("cells"); c.innerHTML="";
  for(const s of PLAN.slides){
    const n=s.slide_number;
    const d=document.createElement("div");
    d.className="cell"; d.id="cell-"+n;
    const dirty=s.__dirty?"<span class='tag'>已改</span>":"";
    d.innerHTML=`<span class="no">${n}</span>${dirty}<img src="/img/${n}?t=${Date.now()}" onerror="this.style.opacity=.2">
      <div class="meta">${esc(s.page_type||"")} · ${esc((s.content||"").slice(0,22))}</div>`;
    d.onclick=()=>sel(n);
    c.appendChild(d);
  }
}

function sel(n){
  CUR=n; const s=PLAN.slides.find(x=>x.slide_number===n); if(!s)return;
  document.querySelectorAll(".cell").forEach(e=>e.classList.remove("sel"));
  const cell=document.getElementById("cell-"+n); if(cell)cell.classList.add("sel");
  document.getElementById("stitle").textContent="编辑第 "+n+" 页";
  document.getElementById("sno").textContent=s.page_type||"";
  let h="";
  for(const f of F){
    const isArr=["text_regions","approved_text_lines"].includes(f);
    h+=`<label>${LBL[f]}</label>`;
    if(f==="page_type"){
      h+=`<select id="f-page_type">`+TYPES.map(t=>`<option ${t===s.page_type?"selected":""}>${t}</option>`).join("")+`</select>`;
    } else if(isArr){
      h+=`<textarea id="f-${f}">${esc(arr(s[f]))}</textarea>`;
    } else {
      h+=`<input id="f-${f}" value="${esc(s[f]??"")}">`;
    }
  }
  document.getElementById("sbody").innerHTML=h;
  document.getElementById("btnRerun").disabled=false;
  document.getElementById("btnPkg").disabled=false;
}

function collect(){
  const s=PLAN.slides.find(x=>x.slide_number===CUR); if(!s)return null;
  const o={};
  for(const f of F){
    const el=document.getElementById("f-"+f); if(!el)continue;
    if(f==="text_regions"||f==="approved_text_lines"){
      o[f]=el.value.split("\n").map(x=>x.trim()).filter(Boolean);
    } else o[f]=el.value;
  }
  return o;
}

async function save(){
  const o=collect(); if(!o)return;
  const r=await fetch("/api/slide/"+CUR,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(o)});
  const j=await r.json();
  if(j.ok){const s=PLAN.slides.find(x=>x.slide_number===CUR);Object.assign(s,j.slide);s.__dirty=true;render();
    msg("已保存到 plan.json","ok");}
  else msg("保存失败: "+j.error,"err");
}

async function rerun(){
  if(CUR==null)return;
  await save();
  msg(`正在重跑第 ${CUR} 页… 请稍候（可能需要 30-120 秒）`,"warn");
  document.getElementById("btnRerun").disabled=true;
  const r=await fetch("/api/rerun/"+CUR,{method:"POST"});
  const j=await r.json();
  document.getElementById("btnRerun").disabled=false;
  if(j.ok){msg("重跑完成 ✓\n"+(j.tail||""),"ok");setTimeout(render,300);}
  else msg("重跑失败:\n"+(j.tail||j.error),"err");
}

async function pkg(){
  msg("正在打包 PPTX…","warn");
  const r=await fetch("/api/package",{method:"POST"});
  const j=await r.json();
  if(j.ok)msg("打包完成 ✓\n"+(j.tail||""),"ok"); else msg("打包失败:\n"+(j.tail||j.error),"err");
}

function msg(t,cls=""){const m=document.getElementById("msg");m.className=cls;m.textContent=t;}
document.getElementById("btnRerun").onclick=rerun;
document.getElementById("btnPkg").onclick=pkg;
boot();
</script></body></html>"""


# ══════════════════════════════════════════════════════════
# 服务器
# ══════════════════════════════════════════════════════════
def make_handler(plan_path: Path, images_dir: Path, out_pptx: Path,
                 lock: threading.Lock, resolution: str, aspect: str,
                 provider: str | None = None,
                 provider_command: str | None = None,
                 provider_options: list[str] | None = None):
    plan = load_plan(plan_path)

    class H(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *a):
            pass

        def _send(self, code, body, ctype="text/html; charset=utf-8"):
            if isinstance(body, str):
                body = body.encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            p = urlparse(self.path).path
            if p == "/":
                return self._send(200, PAGE)
            if p == "/api/plan":
                with lock:
                    return self._send(200, json.dumps(plan, ensure_ascii=False),
                                      "application/json; charset=utf-8")
            if p.startswith("/img/"):
                n = int(re.sub(r"\D", "", p.split("/")[-1]) or 0)
                f = img_path(images_dir, n)
                if f.exists():
                    ctype = "image/png" if f.suffix.lower() == ".png" else "image/jpeg"
                    return self._send(200, f.read_bytes(), ctype)
                return self._send(404, b"not found", "text/plain")
            return self._send(404, b"not found", "text/plain")

        def do_POST(self):
            n = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(n).decode("utf-8") if n else "{}"
            p = urlparse(self.path).path

            if p.startswith("/api/slide/"):
                sn = int(p.rsplit("/", 1)[-1])
                try:
                    patch = json.loads(raw)
                except Exception as e:
                    return self._send(400, json.dumps({"ok": False, "error": str(e)}),
                                      "application/json; charset=utf-8")
                with lock:
                    s = find_slide(plan, sn)
                    if not s:
                        return self._send(404, json.dumps({"ok": False, "error": "页不存在"}),
                                          "application/json; charset=utf-8")
                    s.update(patch)
                    save_plan(plan_path, plan)
                    return self._send(200, json.dumps({"ok": True, "slide": s}, ensure_ascii=False),
                                      "application/json; charset=utf-8")

            if p.startswith("/api/rerun/"):
                sn = int(p.rsplit("/", 1)[-1])
                ok, tail = rerun_one(plan_path, images_dir, sn, resolution, aspect,
                                     provider, provider_command, provider_options)
                return self._send(200, json.dumps({"ok": ok, "tail": tail}, ensure_ascii=False),
                                  "application/json; charset=utf-8")

            if p == "/api/package":
                ok, tail = package(plan_path, images_dir, out_pptx)
                return self._send(200, json.dumps({"ok": ok, "tail": tail}, ensure_ascii=False),
                                  "application/json; charset=utf-8")

            return self._send(404, b"not found", "text/plain")

    return H


def cmd_serve(args):
    plan_path = Path(args.plan).resolve()
    images_dir = Path(args.images_dir).resolve()
    out_pptx = Path(args.out_pptx).resolve() if args.out_pptx else plan_path.with_suffix(".pptx")
    images_dir.mkdir(parents=True, exist_ok=True)

    if DECK is None:
        print("[X] 找不到 ppt-deck-builder-pro (含 rerun_single_page.sh)")
        return 1
    if BASH is None:
        print("[X] 找不到 bash (Git Bash / WSL), Windows 建议装 Git for Windows")
        return 1
    print(f"[OK] deck skill : {DECK}")
    print(f"[OK] bash       : {BASH}")
    print(f"[OK] plan       : {plan_path}")
    print(f"[OK] images dir : {images_dir}")
    if args.provider:
        print(f"[OK] provider   : {args.provider}"
              + (f"  cmd={args.provider_command}" if args.provider_command else ""))
    else:
        print("[!!] 未指定 --provider, 重跑会回落到 plan 里的 image_provider (真实 API)")

    lock = threading.Lock()
    handler = make_handler(plan_path, images_dir, out_pptx, lock, args.resolution, args.aspect,
                           args.provider, args.provider_command, args.provider_option)
    srv = ThreadingHTTPServer((args.host, args.port), handler)
    url = f"http://{args.host}:{args.port}/"
    print(f"\n▶ 可视化编辑器已启动: {url}")
    print(f"  打包输出: {out_pptx}")
    print("  Ctrl+C 停止\n")
    if args.open:
        threading.Timer(1.2, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n停止。")
    finally:
        srv.server_close()
    return 0


def cmd_index(args):
    plan_path = Path(args.plan).resolve()
    images_dir = Path(args.images_dir).resolve()
    plan = load_plan(plan_path)
    slides = plan.get("slides", [])
    print("=" * 78)
    print(f"{plan.get('title', 'deck')}  共 {len(slides)} 页  preset={plan.get('style_preset', '')}")
    print("=" * 78)
    print(f"{'页':>3}  {'图片':<28} {'类型':<14} {'标题':<26} 状态")
    print("-" * 78)
    for s in slides:
        n = s.get("slide_number")
        f = img_path(images_dir, n)
        rel = str(f.relative_to(images_dir)) if f.exists() else "(缺失)"
        st = "OK" if f.exists() else "缺图"
        print(f"{n:>3}  {rel:<28} {str(s.get('page_type','')):<14} "
              f"{str(s.get('content',''))[:24]:<26} {st}")
    print("-" * 78)
    return 0


def cmd_status(args):
    plan_path = Path(args.plan).resolve()
    images_dir = Path(args.images_dir).resolve()
    plan = load_plan(plan_path)
    changed = []
    for s in plan.get("slides", []):
        n = s.get("slide_number")
        f = img_path(images_dir, n)
        if not f.exists():
            changed.append((n, "缺图"))
        elif f.stat().st_mtime < plan_path.stat().st_mtime - 1:
            changed.append((n, "图比 plan 旧 → 需重跑"))
    if not changed:
        print("✅ 全部页与 plan 同步")
        return 0
    print(f"⚠️ {len(changed)} 页需处理:")
    for n, why in changed:
        print(f"   第 {n} 页 — {why}")
    return 0


def cmd_patch(args):
    plan_path = Path(args.plan).resolve()
    images_dir = Path(args.images_dir).resolve()
    plan = load_plan(plan_path)
    s = find_slide(plan, args.slide)
    if not s:
        print(f"[X] 第 {args.slide} 页不存在")
        return 1
    for kv in args.set or []:
        if "=" not in kv:
            continue
        k, v = kv.split("=", 1)
        k = k.strip()
        if k in ("text_regions", "approved_text_lines"):
            s[k] = [x.strip() for x in v.split("|") if x.strip()]
        else:
            s[k] = v
    save_plan(plan_path, plan)
    print(f"[OK] 第 {args.slide} 页已更新: {list(s.keys())[:0] or ''}")
    print(f"     改动字段: {[kv.split('=')[0].strip() for kv in (args.set or [])]}")
    if args.rerun:
        print("     正在重跑…")
        ok, tail = rerun_one(plan_path, images_dir, args.slide,
                             provider=args.provider,
                             provider_command=args.provider_command,
                             provider_options=args.provider_option)
        print(("     重跑成功 ✓" if ok else "     重跑失败 ✗") + "\n" + tail)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="PPT 在线可视化编辑器")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("serve", help="启动预览+编辑服务器")
    s.add_argument("--plan", required=True)
    s.add_argument("--images-dir", required=True)
    s.add_argument("--out-pptx", default=None)
    s.add_argument("--port", type=int, default=8765)
    s.add_argument("--host", default="127.0.0.1")
    s.add_argument("--resolution", default="4k")
    s.add_argument("--aspect", default="16:9")
    s.add_argument("--provider", default=None, help="图像 provider, 如 command / runninghub_g31")
    s.add_argument("--provider-command", default=None, help="provider=command 时的本地命令")
    s.add_argument("--provider-option", action="append", default=[], help="KEY=VALUE, 可多次")
    s.add_argument("--open", action="store_true", help="自动打开浏览器")
    s.set_defaults(fn=cmd_serve)

    s = sub.add_parser("index", help="建索引并打印状态表")
    s.add_argument("--plan", required=True)
    s.add_argument("--images-dir", required=True)
    s.set_defaults(fn=cmd_index)

    s = sub.add_parser("status", help="列出需重跑的页")
    s.add_argument("--plan", required=True)
    s.add_argument("--images-dir", required=True)
    s.set_defaults(fn=cmd_status)

    s = sub.add_parser("patch", help="命令行改一页")
    s.add_argument("--plan", required=True)
    s.add_argument("--images-dir", required=True)
    s.add_argument("--slide", type=int, required=True)
    s.add_argument("--set", action="append", help="key=value (可多次)")
    s.add_argument("--rerun", action="store_true")
    s.add_argument("--provider", default=None)
    s.add_argument("--provider-command", default=None)
    s.add_argument("--provider-option", action="append", default=[])
    s.set_defaults(fn=cmd_patch)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
