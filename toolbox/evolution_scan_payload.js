// evolution_scan_payload.js - 自进化扫描（script payload，头���执行，不调模型）
// 依据 R-AUTO-07：机械任务用确定性脚本，不用 agentTurn（省 token、无 LLM 漂移、结果可复现）
// 产出由 evolution_scan.py 负责（写 ~/self-improving/eval/YYYY-MM-DD.json）；本脚本只负责触发 + 留存状态
// 不返回 notify -> 不投递、不打扰 Eric（告警由 B166ER-自进化缺席告警 独立承担）
const cmd = 'C:/Users/ericz/AppData/Local/Programs/Python/Python314/python.exe D:/B166ER-openclaw/workspace/toolbox/evolution_scan.py';
let out = '';
let ok = true;
try {
  const r = await exec({ command: cmd });
  out = String(r?.aggregated ?? r?.output ?? r?.stdout ?? r ?? '').trim();
} catch (e) {
  ok = false;
  out = 'ERR ' + String(e && e.message ? e.message : e).slice(0, 400);
}
return json({
  state: {
    lastRunAt: new Date().toISOString(),
    execOk: ok,
    lastOut: out.slice(0, 1200)
  }
});
