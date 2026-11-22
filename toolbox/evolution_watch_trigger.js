// evolution_watch_trigger.js - 自进化缺席/失败探测器（automation trigger script）
//
// 契约（automation/cron-jobs/schedules.md · Event triggers）：
//   必须返回 { fire, message?, state? }；上一次状态以 trigger.state 冻结传入；
//   message 会成为触发后 agentTurn 的完整事件上下文 -> 必须自包含。
//   json(...) 是 code-mode 执行器的返回形式。
//
// 判据依据 R-AUTO-09：产出链之外，必须有一条独立路径校验"是否按时来了"。
// 文档警告：watcher 要围绕 actionable state 而非 success —— 检查失败时沉默 = 看起来健康实则已坏。
const prev = trigger.state || {};
const cmd = 'C:/Users/ericz/AppData/Local/Programs/Python/Python314/python.exe D:/B166ER-openclaw/workspace/toolbox/evolution_watch.py';
let out = '';
let execFailed = false;
try {
  const r = await exec({ command: cmd });
  out = String(r?.aggregated ?? r?.output ?? r?.stdout ?? r ?? '').trim();
} catch (e) {
  execFailed = true;
  out = String(e && e.message ? e.message : e).slice(0, 300);
}
let j = null;
try { j = JSON.parse(out); } catch (e) { j = null; }
if (!j) {
  // 探测器本身坏了 -> 必须报警，不能沉默（沉默即"看起来健康"）
  return json({
    fire: true,
    message: '【自进化链路告警】缺席探测器本身无法输出合法 JSON（探测器可能已损坏或 Python 路径失效）。原始输出：' + String(out).slice(0, 400) + ' 处置：手工运行 D:/B166ER-openclaw/workspace/toolbox/evolution_watch.py 排查。',
    state: { lastErrorAt: new Date().toISOString(), lastRaw: String(out).slice(0, 400), prevSeen: prev.last_seen || null, errorCount: (prev.errorCount || 0) + 1 }
  });
}
const st = j.state || {};
const streak = st.fail_streak || 0;
const age = st.age_days;
if (j.fire) {
  return json({
    fire: true,
    message: j.message,
    state: Object.assign({}, prev, st, { firedAt: new Date().toISOString(), fireCount: (prev.fireCount || 0) + 1 })
  });
}
return json({
  fire: false,
  message: '',
  state: Object.assign({}, prev, st, { checkedAt: new Date().toISOString(), lastSeen: st.last_seen || prev.last_seen || null, ageDays: age, streak })
});
