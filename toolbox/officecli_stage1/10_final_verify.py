"""Final verification - read bytes only, write to UTF-8 file."""
import zipfile, re, json, sys, io

# Force stdout to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Read XML directly with bytes
print("=== PPTX XML Titles (bytes inspected directly) ===")
results_xml = {}
with zipfile.ZipFile(r'D:\OfficeCLI-test\test_demo.pptx') as z:
    for i in range(1, 6):
        with z.open(f'ppt/slides/slide{i}.xml') as f:
            x_bytes = f.read()
        x = x_bytes.decode('utf-8')
        m = re.search(r'<a:t>(.*?)</a:t>', x)
        title = m.group(1) if m else '<no title>'
        results_xml[f'slide{i}'] = title
        print(f"Slide {i}: utf-8 bytes: {m.group(1).encode('utf-8').hex()}")

# Read outline.json
print()
print("=== Outline JSON (raw bytes inspected) ===")
raw = open(r'D:\OfficeCLI-test\outline.json','rb').read()
print(f"BOM: {raw[:3].hex()}")
text = raw.decode('utf-16-le').lstrip('\ufeff')
pattern = re.compile(r'"title":\s*"([^"]+)"', re.MULTILINE)
matches = pattern.findall(text)
results_json = {}
for i, m in enumerate(matches, 1):
    if ',' in m:
        m = m.split(',')[0]
    results_json[f'slide{i}'] = m
    print(f"Slide {i}: UTF-16-LE hex: {m.encode('utf-16-le').hex()}")

print()
print("=== MATCH CHECK ===")
all_match = True
for k in results_xml:
    if results_xml[k] == results_json.get(k):
        print(f"{k}: MATCH  ({results_xml[k]!r})")
    else:
        all_match = False
        print(f"{k}: MISMATCH")
        print(f"  XML:  {results_xml[k]!r} (bytes: {results_xml[k].encode('utf-8').hex()})")
        print(f"  JSON: {results_json.get(k, '<missing>')!r} (bytes: {results_json.get(k, '').encode('utf-16-le', errors='replace').hex()})")

# Save clean JSON
clean = {"xml": results_xml, "json": results_json, "match": all_match}
with open(r'D:\B166ER-OpenClaw\workspace\toolbox\officecli_stage1\comparison.json', 'w', encoding='utf-8') as f:
    json.dump(clean, f, ensure_ascii=False, indent=2)
print()
print("Saved comparison.json")
print(f"ALL MATCH: {all_match}")
