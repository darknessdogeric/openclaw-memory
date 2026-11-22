fp = r'D:\B166ER-OpenClaw\workspace\skills\@wangjiaocheng\cad-editor\examples\build_sichuan_hotel_1f.py'
# Read as bytes, replace problem byte
data = open(fp, 'rb').read()
# Find v_axis[4'] - the bad char is 0x27 (regular apostrophe) which is fine in single-quoted strings
# But it's followed by ), which closes the string prematurely
# Actually the issue: it's "v_axis[4" + "'" + ")" - the ' closes the string then ) is invalid
# So I need to change "v_axis[4'])" to "v_axis[4])"
old = b"v_axis[4'])"
new = b"v_axis[4])"
data = data.replace(old, new)
# Same for other variants
data = data.replace(b"v_axis[6'])", b"v_axis[6])")
data = data.replace(b"v_axis[5'])", b"v_axis[5])")
data = data.replace(b"v_axis[3'])", b"v_axis[3])")
open(fp, 'wb').write(data)
print('done')