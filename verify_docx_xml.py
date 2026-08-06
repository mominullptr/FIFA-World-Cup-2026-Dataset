import zipfile, re

with zipfile.ZipFile('FIFA_World_Cup_2026_Q1_Data_Descriptor.docx') as z:
    xml_content = z.read('word/document.xml').decode('utf-8')

print("=== MANDATORY VERIFICATION AUDIT RESULTS ===")

fig_counts = {}
for i in range(1, 5):
    pattern = f"Figure {i} |"
    count = len(re.findall(re.escape(pattern), xml_content))
    fig_counts[pattern] = count
    print(f"Count of '{pattern}': {count}")

star_matches = len(re.findall(r'<w:t[^>]*>[^<]*\*\*[^<]*</w:t>', xml_content))
print(f"Count of literal '**' inside <w:t>: {star_matches}")

dollar_matches = len(re.findall(r'<w:t[^>]*>[^<]*\$[^<]*</w:t>', xml_content))
print(f"Count of literal '$' inside <w:t>: {dollar_matches}")

bs_matches = len(re.findall(r'<w:t[^>]*>[^<]*\\[a-zA-Z]+[^<]*</w:t>', xml_content))
print(f"Count of backslash-letter pattern inside <w:t>: {bs_matches}")
