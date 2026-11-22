fp = r'D:\B166ER-OpenClaw\workspace\skills\@wangjiaocheng\cad-editor\examples\build_sichuan_hotel_1f.py'
text = open(fp, encoding='utf-8').read()
# Replace any '6' (with stray apostrophe?) - it's a PowerShell encoding artifact
text = text.replace("v_axis[6']", 'v_axis[6]')
text = text.replace("v_axis[5']", 'v_axis[5]')
text = text.replace("v_axis[3']", 'v_axis[3]')
open(fp, 'w', encoding='utf-8').write(text)
print('done')