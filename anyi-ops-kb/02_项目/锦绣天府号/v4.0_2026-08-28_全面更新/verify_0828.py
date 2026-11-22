import docx, re, sys

PATH = r"C:\Users\ericz\Desktop\产业发展部\熊猫专列\安逸-铁路成都局-心已远-锦绣天府号经营转委确认书（三方）0828.docx"

try:
    d = docx.Document(PATH)
except Exception as e:
    print(f"ERROR opening: {e}")
    sys.exit(1)

all_text = "\n".join([p.text for p in d.paragraphs])
print("=== 银创出现次数 ===")
print("银创:", all_text.count("银创"))
print("银创产融:", all_text.count("银创产融"))
print("45%:", all_text.count("45%"))
print("45（裸数字）:", all_text.count("45"))
print()

print("=== 文档基本信息 ===")
print("总字符数:", len(all_text))
print("段落数:", len(d.paragraphs))
print("表格数:", len(d.tables))
print()

print("=== 日期搜索 ===")
patterns = [
    r"[0-9]{4}\s*年\s*[0-9]+\s*月\s*[0-9]+\s*日",
    r"[0-9]{4}[.\-/][0-9]{1,2}[.\-/][0-9]{1,2}",
    r"[0-9]{8}",
]
for p in patterns:
    matches = re.findall(p, all_text)
    print(f"  模式 {p}: {len(matches)} 个")
    for m in matches[:5]:
        print("    ", m)
print()

print("=== 表格内容（前 5 个表）===")
for i, t in enumerate(d.tables[:5]):
    print(f"--- Table {i} ({len(t.rows)} 行 x {len(t.columns)} 列) ---")
    for r_idx, r in enumerate(t.rows[:8]):
        print(f"  R{r_idx}: " + " | ".join(c.text[:50] for c in r.cells))
    print()