import xml.etree.ElementTree as ET
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

workspace_dir = os.path.dirname(os.path.abspath(__file__))

log_lines = []

for fname in ['fig2_xg_scatter.svg', 'fig3_team_market_values.svg']:
    log_lines.append(f"\n================ {fname} TEXT LABELS ================")
    fpath = os.path.join(workspace_dir, fname)
    tree = ET.parse(fpath)
    root = tree.getroot()
    for elem in root.iter():
        if elem.tag.endswith('text'):
            txt = elem.text
            x = elem.attrib.get('x', '')
            y = elem.attrib.get('y', '')
            anchor = elem.attrib.get('text-anchor', 'start')
            log_lines.append(f"  Pos: (x={x:>6}, y={y:>6}) | Anchor: {anchor:>6} | Text: '{txt}'")

report_text = "\n".join(log_lines)
print(report_text)

with open(os.path.join(workspace_dir, 'figure_labels_audit.txt'), 'w', encoding='utf-8') as f:
    f.write(report_text)
