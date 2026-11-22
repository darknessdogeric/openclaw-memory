fp = r'D:\B166ER-OpenClaw\workspace\skills\@wangjiaocheng\cad-editor\examples\build_sichuan_hotel_1f.py'
text = open(fp, encoding='utf-8').read()
# Use proper quote replacements via bytes
# The problematic chars are U+2019 (RIGHT SINGLE QUOTATION MARK) which look like apostrophe
text = text.replace("v_axis[4\u2019]", "v_axis[4]")
text = text.replace("v_axis[6\u2019]", "v_axis[6]")
text = text.replace("v_axis[5\u2019]", "v_axis[5]")
text = text.replace("v_axis[3\u2019]", "v_axis[3]")
# Also any 'text'
open(fp, 'w', encoding='utf-8').write(text)
print('done')