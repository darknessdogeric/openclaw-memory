with open('C:/Users/ericz/.openclaw/workspace/memory/hotel-industry-knowledge-base.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find exact range to replace
start_line = None  # line 28: "     - 4.7.4 [营"
end_line = None    # line 45: "     - 4.7.7 [工" (last of old 4.7.x block)
next_after = None  # line 46: "   - 4.8 [第"

for i, line in enumerate(lines):
    if '     - 4.7.4 [营' in line:
        start_line = i
    if '     - 4.7.7 [工' in line:
        end_line = i
    if '   - 4.8 [第' in line:
        next_after = i

print(f'Range: {start_line} to {end_line} (next section at {next_after})')

new_toc_block = '''     - 4.7.4 [OTA运营方法与流程体系（含自动化节点）](#474-ota运营方法与流程体系含自动化节点)
       - 4.7.4.1 [OTA运营的历史沿革](#4741-ota运营的历史沿革)
       - 4.7.4.2 [OTA运营的核心方法论](#4742-ota运营的核心方法论)
       - 4.7.4.3 [OTA运营全流程SOP](#4743-ota运营全流程sop)
       - 4.7.4.4 [OTA运营要点总结](#4744-ota运营要点总结)
       - 4.7.4.5 [OTA运营自动化节点](#4745-ota运营自动化节点)
       - 4.7.4.6 [OTA运营的发展现状](#4746-ota运营的发展现状)
       - 4.7.4.7 [OTA运营的自动化发展方向](#4747-ota运营的自动化发展方向)
       - 4.7.4.8 [OTA运营检查清单](#4748-ota运营检查清单可打印)
     - 4.7.5 [营销工具清单与实操指南](#475-营销工具清单与实操指南)
     - 4.7.6 [会员运营与私域流量的行业演变（历史沿革+现状+未来）](#476-会员运营与私域流量的行业演变历史沿革现状未来)
       - 4.7.6.1 [会员制历史沿革](#4761-会员运营与私域概念的历史沿革)
       - 4.7.6.2 [酒店预订方式的历史沿革与现状](#4762-酒店预订方式的历史沿革与行业现状)
       - 4.7.6.3 [未来发展趋势](#4763-未来发展趋势)
       - 4.7.6.4 [未来时间轴](#4764-酒店预订与会员运营的未来时间轴)
       - 4.7.6.5 [历史启示](#4765-历史沿革对酒店营销的启示)
     - 4.7.7 [公域-私域营销闭环与新媒体矩阵](#477-公域-私域营销闭环与新媒体矩阵)
       - 4.7.7.1 [公域-私域闭环核心逻辑](#4771-公域-私域闭环的核心逻辑)
       - 4.7.7.2 [新媒体公域流量矩阵与各平台打法](#4772-新媒体公域流量矩阵与各平台打法)
       - 4.7.7.3 [公域→私域全链路转化SOP](#4773-公域私域全链路转化sop)
       - 4.7.7.4 [完整营销闭环SOP](#4774-完整营销闭环sop公域私域成交复购裂变)
       - 4.7.7.5 [新媒体内容日历与运营排期](#4775-新媒体内容日历与运营排期)
       - 4.7.7.6 [各平台数据指标体系](#4776-各平台数据指标体系)
       - 4.7.7.7 [工具矩阵全景图](#4777-公域-私域运营工具矩阵全景图)
       - 4.7.7.8 [典型案例](#4778-典型酒店新媒体运营案例)
       - 4.7.7.9 [运营检查清单](#4779-公域-私域运营检查清单可打印)
     - 4.7.8 [工具协同架构图（AHL方向）](#478-工具协同架构图ahl方向)
'''

# Replace lines[start_line:end_line+1] with new_toc_block
new_lines = lines[:start_line] + [new_toc_block + '\n'] + lines[next_after:]

with open('C:/Users/ericz/.openclaw/workspace/memory/hotel-industry-knowledge-base.md', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f'Done. Old lines: {len(lines)}, New lines: {len(new_lines)}')
