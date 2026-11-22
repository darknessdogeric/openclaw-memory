# -*- coding: utf-8 -*-
"""把 2026-10-29 安逸会话恢复的教训追加到 ~/self-improving/corrections.md（UTF-8 显式，不污染文件）"""
import io, os, sys, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

TARGET = os.path.join(os.environ['USERPROFILE'], 'self-improving', 'corrections.md')
ROW = (
    "| 2026-10-29 | **会话\"消失\"误判为\"被删\"**：Eric 报「安逸集团相关」对话框没了，要求重建并找回内容。"
    "我第一反应是\"建一个新会话\"——**这个动作会丢掉 56 万 token 历史，是错解**。"
    "实查 `sessions_list(archived:\"all\")` 才发现会话实体完好，`archived: true` 只是让侧边栏不显示。"
    "根因：我把\"侧边栏看不见\"直接等同于\"数据没了\"，没有先查 archived 状态就准备动手删重建。"
    "**更深一层**：我的第一反应是\"满足字面要求\"（重建），而不是\"满足真实意图\"（找回内容）——"
    "重建会给出一个空壳窗口，看起来完成了任务，实际把 Eric 56 万 token 的上下文价值清零。"
    "**错误顺序**：先答应重建 → 再调查 → 发现只需 restore。"
    "**正确顺序**：先 `sessions_list(archived:\"all\")` 查状态 → 确认 archived → `sessions patch(archived:false, expectedSessionId)` 恢复 → 只有实体真不在才考虑新建。"
    "本次 15 个安逸相关会话中 9 个仍是 archived 状态（同样\"看不见\"），全部保留完好。"
    "| **会话生命周期铁律**：① \"窗口不见了\"先分诊 archived / deleted / renamed，绝不默认 delete-rebuild；"
    "② `sessions patch` 支持 `archived` 双向切换，恢复零成本、保留全部上下文；"
    "③ `expectedSessionId` 是防误操作护栏，archive/restore/delete 他会话必填；"
    "④ 场景化会话应归入独立 sidebar group + 置顶 + 图标，让\"看不见\"从技术问题降级为视觉问题；"
    "⑤ 用户说\"重建\"时，先判断\"恢复\"是否已足够——**字面要求 ≠ 真实意图，意图优先** | "
    "已记录，本次零返工恢复。**推广**：凡\"内容丢了/窗口没了/找不到了\"类请求，第一动作是 inventory（查全量状态），第二动作才是动作 | 立即生效 |\n"
)

if not os.path.exists(TARGET):
    print('!! target not found: %s' % TARGET)
    sys.exit(2)

before = os.path.getsize(TARGET)
with open(TARGET, 'rb') as f:
    raw = f.read()
# 编码探测：BOM -> utf-8-sig，否则尝试 utf-8，失败则 gbk
enc = 'utf-8'
try:
    text = raw.decode('utf-8')
except UnicodeDecodeError:
    enc = 'gbk'
    text = raw.decode('gbk')

shutil.copy2(TARGET, TARGET + '.bak-20261029-preAnYiRestore')

if '2026-10-29' in text and '会话\\"消失\\"误判' in text:
    print('已存在同日同条，跳过追加')
    print('size=%d enc=%s' % (before, enc))
    sys.exit(0)

# 追加到表格末尾（文件是 table，追加行）
if not text.endswith('\n'):
    text += '\n'
text += ROW

with open(TARGET, 'w', encoding=enc, newline='') as f:
    f.write(text)

after = os.path.getsize(TARGET)
with open(TARGET, 'rb') as f:
    chk = f.read()
chk.decode(enc)  # 编码自检：写完必须能按原编码解回来
print('OK  enc=%s  %d -> %d bytes  (+%d)' % (enc, before, after, after - before))
print('tail check:')
print(chk.decode(enc).splitlines()[-1][:120])
