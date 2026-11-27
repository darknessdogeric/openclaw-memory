# -*- coding: utf-8 -*-
"""企业级 AgentOS 架构成熟度体检（12 层）。

对应《企业级AgentOS架构设计与工程实践》第 12 章「成熟度模型」：
用文件系统证据逐层判定 有 / 半 / 缺，输出成熟度分与下一步动作。

诚实边界：判定基于文件系统证据（有无某类文件/字段/工具），
能发现缺环，不能证明环是好的。成熟度分是启发式加权，非行业标准。
"""
import io, sys, os, json, argparse, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# 每层：id / 名称 / 对应章 / 权重 / 探针列表
# 探针：(标签, 判定函数)  判定函数返回 True/False/None(未知)
LAYERS = [
    ("L01", "对象契约（可校验的业务对象）", 2, [
        ("存在 schema 定义文件", lambda r: _glob(r, "**/*schema*.json") or _glob(r, "**/contracts/**")),
        ("存在对象模型代码", lambda r: _grep_py(r, "BaseModel|pydantic|dataclass")),
        ("交付件附带机器可校验契约", lambda r: _glob(r, "**/*.schema.json")),
    ]),
    ("L02", "状态编排与断点续跑", 2, [
        ("存在状态图/编排代码", lambda r: _grep_py(r, "StateGraph|langgraph|checkpointer|interrupt")),
        ("自动化任务可恢复（cron/at 作业存在）", lambda r: _glob(r, "**/*automation*") or _glob(r, "**/*.cron*")),
        ("存在运行台账（可回放）", lambda r: _glob(r, "data/*ledger*.jsonl") or _glob(r, "data/*run*.jsonl")),
    ]),
    ("L03", "模型网关（统一入口/路由/降级/成本）", 2, [
        ("存在模型路由或降级记录", lambda r: _grep_all(r, "fallback|降级|alias|router")),
        ("存在成本台账", lambda r: _glob(r, "data/*cost*.jsonl")),
        ("成本台账非空", lambda r: _nonempty(r, "data/*cost*.jsonl")),
    ]),
    ("L04", "工具协议与授权（MCP/工具目录）", 1, [
        ("存在工具目录或 MCP 配置", lambda r: _glob(r, "**/mcp*.json") or _glob(r, "**/tools/**")),
        ("工具带权限/授权声明", lambda r: _grep_all(r, "requires_approval|授权|approval|permission")),
    ]),
    ("L05", "知识检索与证据溯源（RAG/EvidenceRef）", 2, [
        ("存在索引或检索代码", lambda r: _grep_py(r, "chroma|llamaindex|embedding|retriev|semantic_search")),
        ("引用可溯源（带来源字段）", lambda r: _grep_all(r, "source_ref|来源|EvidenceRef|引用")),
    ]),
    ("L06", "策略审批与幂等", 3, [
        ("存在策略/审批对象", lambda r: _grep_all(r, "PolicyDecision|ApprovalRequest|ApprovalGrant|审批")),
        ("存在幂等键机制", lambda r: _grep_all(r, "幂等|idempot|dedup|去重")),
        ("机器可执行策略层（非仅文字）", lambda r: _glob(r, "**/policy*.py") or _glob(r, "**/policy*.rego")),
    ]),
    ("L07", "可观测与评测（Trace/Audit 分离）", 3, [
        ("存在任务级 Trace 记录", lambda r: _glob(r, "data/*trace*.jsonl")),
        ("审计事件独立成账", lambda r: _glob(r, "data/*audit*.jsonl")),
        ("存在评测/断言体系", lambda r: _glob(r, "**/selfcheck.py") or _glob(r, "**/eval*/**")),
        ("失败样本回灌（回归集）", lambda r: _glob(r, "**/*regression*") or _glob(r, "**/*回灌*")),
    ]),
    ("L08", "长任务运行时与恢复演练", 2, [
        ("存在持久化运行时", lambda r: _grep_py(r, "temporal|worker|queue")),
        ("有恢复/重放演练记录", lambda r: _grep_all(r, "恢复演练|drill|replay|重放")),
    ]),
    ("L09", "工程组合（模块责任/配置入口）", 1, [
        ("存在单一配置入口", lambda r: _glob(r, "config/*.yaml") or _glob(r, "config/*.yml") or _glob(r, "config/*.json")),
        ("技能注册表存在", lambda r: _glob(r, "**/SKILL_REGISTRY.json") or _glob(r, "output/audit_skills/SKILL_REGISTRY.json") or os.path.exists(os.path.join(r, "output", "audit_skills", "SKILL_REGISTRY.json"))),
    ]),
    ("L10", "能力目录（负责人/成熟度/接入）", 2, [
        ("注册表含负责人字段", lambda r: _grep_all(r, "owner|负责人")),
        ("注册表含成熟度字段", lambda r: _grep_all(r, "maturity|成熟度")),
    ]),
    ("L11", "成本归因与预算", 2, [
        ("成本可按任务归因", lambda r: _glob(r, "data/*cost*.jsonl")),
        ("存在预算/上限约束", lambda r: _grep_all(r, "budget|预算|cost_limit|上限")),
    ]),
    ("L12", "失败路径与端到端验证", 2, [
        ("存在失败路径测试", lambda r: _grep_py(r, "pytest|unittest|fail_path|失败路径")),
        ("端到端验证脚本", lambda r: _glob(r, "**/*e2e*") or _glob(r, "**/verify*.py")),
    ]),
]

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".archive", "_archive",
             ".tmp_a6g1", ".tools", "output", "outputs", "media", ".chroma_db"}

TEXT_EXT = {".py", ".md", ".json", ".yaml", ".yml", ".txt", ".jsonl", ".html", ".css", ".js"}

_FILE_CACHE = {}
_TEXT_CACHE = {}

def _files(root):
    """遍历一次并缓存：30+ 探针各走一次全库是体检慢的根因。"""
    key = os.path.abspath(root)
    if key in _FILE_CACHE:
        return _FILE_CACHE[key]
    out = []
    for base, dirs, fs in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for f in fs:
            out.append(os.path.join(base, f))
    _FILE_CACHE[key] = out
    return out

def _read_text(fp):
    """读文本并缓存，避免同一文件被多个探针重复读取。"""
    if fp in _TEXT_CACHE:
        return _TEXT_CACHE[fp]
    try:
        if os.path.getsize(fp) > 400000:
            _TEXT_CACHE[fp] = ""
            return ""
        t = open(fp, encoding="utf-8", errors="replace").read()
    except Exception:
        t = ""
    _TEXT_CACHE[fp] = t
    return t

_GLOB_CACHE = {}

def _glob(root, pattern):
    import glob as g
    key = (os.path.abspath(root), pattern)
    if key in _GLOB_CACHE:
        return _GLOB_CACHE[key]
    pat = os.path.join(root, pattern)
    hits = []
    for p in g.glob(pat, recursive=True):
        if any(s in SKIP_DIRS for s in p.split(os.sep)):
            continue
        hits.append(p)
    _GLOB_CACHE[key] = hits
    return hits

def _grep_all(root, needle):
    """支持正则（探针里写的是 "a|b|c" 这种 alternation）与字面量两种写法。"""
    try:
        rx = re.compile(needle)
        use_rx = True
    except re.error:
        rx = None
        use_rx = False
    hits = []
    for fp in _files(root):
        if os.path.splitext(fp)[1].lower() not in TEXT_EXT:
            continue
        body = _read_text(fp)
        if not body:
            continue
        ok = (rx.search(body) is not None) if use_rx else (needle in body)
        if ok:
            hits.append(fp)
            if len(hits) >= 3:
                break
    return hits

def _grep_py(root, pattern):
    rx = re.compile(pattern)
    hits = []
    for fp in _files(root):
        if not fp.endswith(".py"):
            continue
        if rx.search(_read_text(fp)):
            hits.append(fp)
            if len(hits) >= 3:
                break
    return hits

def _nonempty(root, pattern):
    hits = _glob(root, pattern)
    for h in hits:
        try:
            if os.path.getsize(h) > 20:
                return True
        except Exception:
            pass
    return False

def audit(root=ROOT, as_json=False):
    rows = []
    total_w = 0
    total_s = 0.0
    for lid, name, w, probes in LAYERS:
        passed = 0
        detail = []
        for label, fn in probes:
            try:
                r = bool(fn(root))
            except Exception:
                r = False
            detail.append((label, r))
            if r:
                passed += 1
        ratio = passed / float(len(probes))
        score = round(w * ratio, 2)
        total_w += w
        total_s += score
        status = "有" if ratio >= 0.99 else ("半" if ratio > 0 else "缺")
        rows.append({"id": lid, "name": name, "weight": w, "passed": passed,
                     "total": len(probes), "ratio": ratio, "score": score,
                     "status": status, "detail": detail})
    maturity = round(100.0 * total_s / total_w, 1)
    out = {"root": root, "maturity": maturity, "max": 100,
           "layers": rows,
           "gaps": [{"id": r["id"], "name": r["name"], "missing": [d[0] for d in r["detail"] if not d[1]]}
                    for r in rows if r["status"] != "有"]}
    if as_json:
        return out
    return out

def render(out):
    L = []
    L.append("=" * 78)
    L.append("企业级 AgentOS 架构成熟度体检 · 12 层")
    L.append("依据《企业级AgentOS架构设计与工程实践》第 12 章成熟度模型")
    L.append("=" * 78)
    L.append("")
    for r in out["layers"]:
        mark = {"有": "[PASS]", "半": "[WARN]", "缺": "[FAIL]"}[r["status"]]
        L.append("%s %s  %-34s 得分 %4.1f / %d   (%d/%d 探针通过)" % (
            mark, r["id"], r["name"], r["score"], r["weight"], r["passed"], r["total"]))
        for label, ok in r["detail"]:
            L.append("        %s %s" % ("OK  " if ok else "--  ", label))
        L.append("")
    L.append("-" * 78)
    L.append("成熟度总分：%.1f / 100" % out["maturity"])
    L.append("")
    L.append("★ 缺口清单（按需补齐顺序）")
    gaps = sorted(out["gaps"], key=lambda g: g["id"])
    for g in gaps:
        L.append("  %s %s" % (g["id"], g["name"]))
        for m in g["missing"]:
            L.append("        - " + m)
    L.append("")
    L.append("说明：判定基于文件系统证据，能发现缺环，不能证明环是好的；")
    L.append("      成熟度分为启发式加权，非行业标准分数。")
    L.append("")
    L.append("★ ★ 测量效度警告（务必读）")
    L.append("  本工具的探针检的是「某类文件/字段是否存在」，不是「该环节是否好用」。")
    L.append("  因此存在自证偏差：补环之后，分数上升的部分只是「文件出现了」，")
    L.append("  不等于「质量达标」。")
    L.append("  正确用法：① 看**缺口清单**定位该补哪一环；")
    L.append("            ② 补完后**另做端到端验证**，别拿分数当验收；")
    L.append("            ③ 分数只用于**横向比较与排期**，不用于宣告「系统已合格」。")
    L.append("  自证偏差的一个信号：一次补环后分数跳到接近满分，此时更应警惕而非庆祝。")
    return "\n".join(L)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    out = audit(a.root)
    if a.json:
        s = json.dumps(out, ensure_ascii=False, indent=2)
    else:
        s = render(out)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(s)
        print("已写出:", a.out)
    else:
        print(s)

if __name__ == "__main__":
    main()
