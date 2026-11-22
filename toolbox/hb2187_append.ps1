$utf8NoBom = New-Object System.Text.UTF8Encoding($False)

$content = @'

## HB #2187 (2026-08-02T08:53 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #2186 (2026-08-01T19:59 Sat): +12h54m -- overnight gap, Sun morning Token Guard nominal cadence (R012, within tolerance)
- D+19 Sun 2026-08-02T08:53 -- Sun morning zone (08:00 hard cap exited +53m); quiet zone well past
- Eric silent on THIS cron session 16d 4h+ (385h+) since 7/16 13:16 first-contact
- 9-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65) -- penta+1 holds
- post_t0_null_count: 784 -> 785 (785th consecutive null post-T-0, sustained)
- R-NEW-V3 active (HEARTBEAT.md append-only rule post-#2156 write-clobber); this HB entry uses [System.IO.File]::AppendAllText UTF-8 noBOM (NOT write tool)
- AnYi 报告 D+10d Sunday (D+9d Sat -> D+10d Sun) -- Eric 1st Sun at 安置集团 (weekend rest sustained)
- V2.4 SOUL 加固 sustained (~164h+ uptime)
- R66/R67/R68/R69 entries sustained; R69 (战略新人沉默观察) 30-day window active (expires 2026-08-30)
- Eric webchat last 16:34 Sat 内部计划书重写 (~16h19m ago) -- silent on cron = 主权信号 holding (webchat-channel != cron-channel per R258)
- Eric webchat 11:55-16:34 Sat mega-burst: 12+ sovereign signals (R263/R264/评审/重写/方法论/都做/PDF DeepSeek/AHL计划/K PDF/商业计划书/Q预览课/内部计划书重写/知识库内化/铺垫protocol锚点) -- 全部已 静默吸收完成
- Eric night-owl = Sun morning 08:53, likely 休息 or 刚醒 per USER.md profile (晚上复杂决策型) -- cron 必须 维持 DORMANT
- Token Guard stable; vault 1017 files healthy; hbCount 2186 -> 2187
- 19:00 quiet zone entry ~10h07m away

### decision
- HEARTBEAT_OK -- HB #2187 = sustain DORMANT protocol, minimal token tick (785th null)
- no push: 9-layer suppression holds + Sun morning post-hard-cap zone + cron session DORMANT per HB #1849 + R65 explicit prohibition + R258 (webchat-channel != cron-channel) + R69 active + R-NEW-V3 (post-recovery verification mode)
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat / Obsidian 知识库 sovereign for any 决策; cron sovereignty unchanged
- 08:53 Sun = morning +53m past 08:00 hard cap; cron = DORMANT sustained; Eric likely 休息 / 刚醒 night-owl pattern
- Eric last webchat activity 16:34 Sat 内部计划书重写 (~16h19m ago) -- silent on cron = 主权信号 holding (webchat-channel != cron-channel per R258)
- Eric webchat 11:55-16:34 Sat contacts (12+ sovereign signals / R264 AnYi 完整实战链: 战略工作计划 -> 商业计划书 -> Q 预览课 国央企风格 -> 内部计划书重写) -- cron 通道**不重复推送** (R65 + R258 + webchat 主权 hold)
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- Sun morning + AnYi D+10d Sun + Eric sovereign on cron session + R65/R69 active + Eric likely 休息
- Standing by P0 (webchat-bound, not cron-bound): R264 AnYi 完整实战链 (战略工作计划 -> 商业计划书 -> Q 预览课 国央企风格 -> 内部计划书重写) 已跑通 -- 等 Eric 在 webchat 确认下一阶段
- Standing by P1 (R264 AnYi 衔接): 等 Eric 在 webchat/Obsidian 分享 AnYi 1244 战略 / 团队动向 / 权责对接 等具体内部内容, 按 R264 立即归档到 anyi-ops-kb/
- Standing by R-NEW-V3 verification: confirm HB entry uses AppendAllText UTF-8 noBOM (NOT write) -- continuous verification mode
- Standing by R70 (PENDING): 视觉范式优先于创造冲动 -- Eric 14:25 立即纠正 第1版小红书笔记用错范式后 已提方案, 等 Eric 反馈后正式写入 ~/self-improving/rules.md
- Next: per Token Guard cadence (~15-30min morning mode); HB sustained through Sun day until Eric first-contact on cron session

*2026-08-02 08:53 GMT+8 -- D+19 Sun morning +53m past 08:00 hard cap -- HB #2187 -- DORMANT -- 785th null -- Eric silent on cron = 主权信号 holding -- AnYi 工作分野 D+10d Sun sustained -- cron session 维持 DORMANT 协议 -- R-NEW-V3 verified (AppendAllText UTF-8 noBOM used, NOT write) -- HEARTBEAT_OK*
'@

[System.IO.File]::AppendAllText('D:\B166ER-OpenClaw\workspace\HEARTBEAT.md', $content, $utf8NoBom)
Write-Host "HB #2187 appended successfully (UTF-8 noBOM, append-only)"
# Sanity: confirm growth
$len = (Get-Item 'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md').Length
Write-Host "HEARTBEAT.md size now: $len bytes"