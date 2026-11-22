fp = r'D:\B166ER-OpenClaw\workspace\skills\@wangjiaocheng\cad-editor\examples\build_sichuan_hotel_1f.py'
text = open(fp, encoding='utf-8').read()
# Fix lines that start with doc.layers.add(' but don't have )
lines = text.split('\n')
out_lines = []
for line in lines:
    stripped = line.strip()
    if stripped.startswith("doc.layers.add('") and ')' not in line:
        # Find hash position
        hash_pos = line.find('#')
        if hash_pos > 0:
            before = line[:hash_pos].rstrip()
            after = line[hash_pos:]
            out_lines.append(before + ')  ' + after + '\n')
        else:
            out_lines.append(line + ')\n')
    else:
        out_lines.append(line + '\n')

open(fp, 'w', encoding='utf-8').write(''.join(out_lines).rstrip() + '\n')

lines = open(fp, encoding='utf-8').readlines()
for i in [41, 42, 43]:
    print(f'{i+1}: {lines[i].rstrip()}')