// evolution_watch_trigger2.js - 自进化缺席/失败探测器 v2（零子进程）
// v1 的教训：trigger evaluation 只有 30 秒预算 + 5 tool calls；v1 在里面 exec 启 Python 进程
//              冷启动经常撞线 -> evaluation timeout -> 文档说"失败/超时也会 fire" -> 反而空烧 payload。
// v2 做法：只 read 一个极小状态文件（由扫描器写），判断逻辑全在 JS 里，零进程启动。
const STATUS_FILE = 'C:\\Users\\ericz\\self-improving\\eval\\.last_scan.json';
const MAX_AGE_DAYS = 8;
const FAIL_STREAK = 2;
const prev = trigger.state || {};
let st = null;
let readFailed = false;
try {
  const r = await read({ path: STATUS_FILE });
  const txt = String(r?.content ?? r?.text ?? r?.data ?? r ?? '').trim();
  st = JSON.parse(txt);
} catch (e) {
  readFailed = true;
  st = null;
}
const nowMs = Date.now();
const base = { checkedAt: new Date().toISOString(), prevSeen: prev.lastSeen || null, readFailed };
if (readFailed || !st || !st.date) {
  // 状态文件读不到 = 扫描器从未成功跑过 -> 必须报警（沉默即"看起来健康"）
  return json({
    fire: true,
    message: '【自进化链路告警】扫描状态文件不可读或不存在（扫描器可能从未成功运行/路径失效）。目标文件：' + STATUS_FILE + '。处置：手工运行 D:/B166ER-openclaw/workspace/toolbox/evolution_scan.py 确认能写出该文件；再查 B166ER-自进化扫描 automation 是否 enabled。',
    state: Object.assign({}, prev, base, { errorCount: (prev.errorCount || 0) + 1 })
  });
}
const lastMs = Date.parse(st.ts || (st.date + 'T09:00:00+08:00'));
const ageDays = lastMs ? Math.floor((nowMs - lastMs) / 86400000) : 999;
const streak = (st.status === 'red') ? (prev.streak || 0) + 1 : 0;
const reasons = [];
if (ageDays > MAX_AGE_DAYS) reasons.push('自进化扫描已缺席 ' + ageDays + ' 天（阈值 ' + MAX_AGE_DAYS + ' 天，最后一次 ' + st.date + '）');
if (streak >= FAIL_STREAK) reasons.push('自进化扫描连续 ' + streak + ' 次未全绿（最近 ' + st.date + '）');
const nextState = Object.assign({}, prev, base, {
  lastSeen: st.date, lastStatus: st.status, ageDays, streak,
  fireCount: prev.fireCount || 0
});
if (reasons.length) {
  nextState.firedAt = new Date().toISOString();
  nextState.fireCount = (prev.fireCount || 0) + 1;
  return json({
    fire: true,
    message: '【自进化链路告警】' + reasons.join('；') + '。\n产出链存在但未被检测 —— 请检查 B166ER-自进化扫描 automation 是否仍 enabled、C:/Users/ericz/self-improving/eval/ 是否仍能落盘。\n处置：先跑 D:/B166ER-openclaw/workspace/toolbox/selfcheck.py，逐条修 FAIL 断言；修完重跑直到全绿。',
    state: nextState
  });
}
return json({ fire: false, message: '', state: nextState });
