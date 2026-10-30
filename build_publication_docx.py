import os
import re
import shutil
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

workspace_dir = os.path.dirname(os.path.abspath(__file__))

def clean_latex_math(text):
    """Converts LaTeX mathematical syntax to clean, publication-ready Unicode strings."""
    if not text:
        return ""
    text = text.replace(r'\%', '%')
    text = text.replace(r'\_', '_')
    text = text.replace(r'\times', '×')
    text = text.replace(r'\approx', '≈')
    # Replace brackets before inequality operators so \left( doesn't get corrupted by \le
    text = re.sub(r'\\left\(', '(', text)
    text = re.sub(r'\\right\)', ')', text)
    text = re.sub(r'\\left\[', '[', text)
    text = re.sub(r'\\right\]', ']', text)
    text = re.sub(r'\\left\\\{', '{', text)
    text = re.sub(r'\\right\\\}', '}', text)
    text = re.sub(r'\\left\b', '', text)
    text = re.sub(r'\\right\b', '', text)
    text = re.sub(r'\\text\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\mathbf\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\mathbb\{P\}', 'P', text)
    text = re.sub(r'\\mathbb\{E\}', 'E', text)
    text = re.sub(r'\\hat\{p\}', 'p̂', text)
    text = re.sub(r'\\Delta', 'Δ', text)
    text = re.sub(r'\\gamma', 'γ', text)
    text = re.sub(r'\\theta', 'θ', text)
    text = re.sub(r'\\sum_\{([^}]+)\}\^\{([^}]+)\}', r'∑(\1 to \2)', text)
    text = re.sub(r'\\sum', '∑', text)
    text = re.sub(r'\\succ\b', ' ≻ ', text)
    text = re.sub(r'\\implies\b', ' ⇒ ', text)
    text = re.sub(r'\\geq?\b', '≥', text)
    text = re.sub(r'\\leq?\b', '≤', text)
    text = re.sub(r'\\neq?\b', '≠', text)
    text = re.sub(r'\\in\b', '∈', text)
    text = re.sub(r'\\land\b', '∧', text)
    text = re.sub(r'\\frac\{1\}\{3\}', '(1/3)', text)
    text = re.sub(r'\\tag\{(\d+)\}', r'    (\1)', text)
    text = re.sub(r'_\{([^}]+)\}', r'_\1', text)
    text = text.replace('$', '')
    # Strip any remaining backslashes before plain alphanumeric words
    text = re.sub(r'\\([a-zA-Z]+)', r'\1', text)
    return text.strip()

def parse_inline_tokens(text):
    """
    Parses a markdown string into tokens:
    ('link', link_text, url)
    ('bold', bold_text)
    ('italic', italic_text)
    ('code', code_text)
    ('text', plain_text)
    """
    # First clean any LaTeX math inside text
    text = clean_latex_math(text)
    
    # Tokenize links, bold, italic, code
    # We use a non-destructive regex
    pattern = re.compile(r'(\[[^\]]+\]\([^)]+\)|\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)')
    tokens = []
    pos = 0
    for m in pattern.finditer(text):
        if m.start() > pos:
            tokens.append(('text', text[pos:m.start()]))
        val = m.group(0)
        if val.startswith('[') and '](' in val:
            lm = re.match(r'\[([^\]]+)\]\(([^)]+)\)', val)
            tokens.append(('link', lm.group(1), lm.group(2)))
        elif val.startswith('**'):
            tokens.append(('bold', val[2:-2]))
        elif val.startswith('*'):
            tokens.append(('italic', val[1:-1]))
        elif val.startswith('`'):
            tokens.append(('code', val[1:-1]))
        pos = m.end()
    if pos < len(text):
        tokens.append(('text', text[pos:]))
    return tokens

def add_formatted_runs(paragraph, text, base_font_size=Pt(10.5), base_color=RGBColor(0x1a, 0x1a, 0x1a)):
    """Appends styled runs to a paragraph based on markdown tokens."""
    tokens = parse_inline_tokens(text)
    for token_type, *args in tokens:
        if token_type == 'text':
            r = paragraph.add_run(args[0])
            r.font.name = 'Calibri'
            r.font.size = base_font_size
            r.font.color.rgb = base_color
        elif token_type == 'bold':
            r = paragraph.add_run(args[0])
            r.font.name = 'Calibri'
            r.font.size = base_font_size
            r.font.bold = True
            r.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
        elif token_type == 'italic':
            r = paragraph.add_run(args[0])
            r.font.name = 'Calibri'
            r.font.size = base_font_size
            r.font.italic = True
            r.font.color.rgb = base_color
        elif token_type == 'code':
            r = paragraph.add_run(args[0])
            r.font.name = 'Consolas'
            r.font.size = Pt(base_font_size.pt - 1.0)
            r.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
        elif token_type == 'link':
            # Add link text with subtle link styling
            link_text, url = args[0], args[1]
            r = paragraph.add_run(link_text)
            r.font.name = 'Calibri'
            r.font.size = base_font_size
            r.font.color.rgb = RGBColor(0x02, 0x84, 0xc7)
            r.font.underline = True

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E1", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_docx():
    md_path = os.path.join(workspace_dir, "DATA_PAPER.md")
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    doc = Document()

    # Standard 1-inch margins
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Base styling
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(0x1a, 0x1a, 0x1a)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    # 1. Title Block (Header)
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(12)
    run_title = p_title.add_run("The FIFA World Cup 2026 Master Dataset: A Normalized 3NF Relational Benchmark of the Expanded 48-Team International Football Tournament")
    run_title.font.name = 'Calibri'
    run_title.font.size = Pt(18)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)

    # Author
    p_auth = doc.add_paragraph()
    p_auth.paragraph_format.space_after = Pt(2)
    run_auth = p_auth.add_run("MD Mominul Islam")
    run_auth.font.bold = True
    run_auth.font.size = Pt(11.5)
    run_sup = p_auth.add_run("1,*")
    run_sup.font.superscript = True
    run_sup.font.bold = True

    # Affiliation
    p_aff = doc.add_paragraph()
    p_aff.paragraph_format.space_after = Pt(4)
    run_aff_sup = p_aff.add_run("1 ")
    run_aff_sup.font.superscript = True
    run_aff = p_aff.add_run("Department of Computer Science and Engineering, Shahjalal University of Science and Technology, Sylhet 3114, Bangladesh.")
    run_aff.font.italic = True
    run_aff.font.size = Pt(9.5)
    run_aff.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    # Correspondence
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_after = Pt(14)
    run_meta = p_meta.add_run("* Corresponding Author Email: mominulcse11@gmail.com  |  Open Access Repository: 10.5281/zenodo.21592427  |  ORCID: 0009-0009-1572-4830")
    run_meta.font.size = Pt(9)
    run_meta.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)

    # Divider line
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(14)
    r_div = p_div.add_run("_________________________________________________________________________________")
    r_div.font.color.rgb = RGBColor(0xcb, 0xd5, 0xe1)

    # Read body lines skipping title/author header block (lines 1 to 8)
    lines = md_text.split("\n")
    start_idx = 0
    for idx, line in enumerate(lines):
        if line.strip().startswith("### Abstract"):
            start_idx = idx
            break

    body_lines = lines[start_idx:]
    i = 0

    while i < len(body_lines):
        line = body_lines[i]
        stripped = line.strip()

        if not stripped or stripped == "---":
            i += 1
            continue

        # Headings
        if stripped.startswith("### "):
            h_text = stripped[4:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            add_formatted_runs(p, h_text, base_font_size=Pt(12), base_color=RGBColor(0x0f, 0x17, 0x2a))
            p.runs[0].font.bold = True
            i += 1
            continue
        elif stripped.startswith("#### "):
            h_text = stripped[5:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(3)
            add_formatted_runs(p, h_text, base_font_size=Pt(11), base_color=RGBColor(0x33, 0x41, 0x55))
            p.runs[0].font.bold = True
            i += 1
            continue
        elif stripped.startswith("## "):
            h_text = stripped[3:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(6)
            add_formatted_runs(p, h_text, base_font_size=Pt(14), base_color=RGBColor(0x0f, 0x17, 0x2a))
            p.runs[0].font.bold = True
            i += 1
            continue

        # Image Embeds
        img_match = re.match(r"!\[(.*?)\]\((.*?)\)", stripped)
        if img_match:
            caption = img_match.group(1)
            img_file = img_match.group(2)
            img_full = os.path.join(workspace_dir, img_file)
            if os.path.exists(img_full):
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = Pt(12)
                p_img.paragraph_format.space_after = Pt(6)
                width = Inches(6.0)
                if "xg_scatter" in img_file or "market_values" in img_file:
                    width = Inches(5.4)
                p_img.add_run().add_picture(img_full, width=width)
            i += 1
            continue

        # Figure Caption Line
        if stripped.startswith("**Figure "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(12)
            p.paragraph_format.left_indent = Inches(0.2)
            p.paragraph_format.right_indent = Inches(0.2)
            add_formatted_runs(p, stripped, base_font_size=Pt(9.5), base_color=RGBColor(0x33, 0x41, 0x55))
            i += 1
            continue

        # Markdown Table Detection
        if stripped.startswith("|") and stripped.endswith("|"):
            table_lines = []
            while i < len(body_lines) and body_lines[i].strip().startswith("|") and body_lines[i].strip().endswith("|"):
                table_lines.append(body_lines[i].strip())
                i += 1
            
            if len(table_lines) >= 2:
                header_row = [c.strip() for c in table_lines[0].split("|")[1:-1]]
                data_rows = []
                for row_line in table_lines[1:]:
                    if re.match(r"^\|(\s*:?-+:?\s*\|)+$", row_line):
                        continue
                    cells = [c.strip() for c in row_line.split("|")[1:-1]]
                    data_rows.append(cells)

                table = doc.add_table(rows=len(data_rows) + 1, cols=len(header_row))
                table.alignment = WD_TABLE_ALIGNMENT.CENTER
                set_table_borders(table)

                # Format Header
                hdr_cells = table.rows[0].cells
                for col_idx, h_text in enumerate(header_row):
                    clean_h = clean_latex_math(h_text.replace("`", "").replace("**", ""))
                    hdr_cells[col_idx].text = clean_h
                    p = hdr_cells[col_idx].paragraphs[0]
                    p.paragraph_format.space_before = Pt(3)
                    p.paragraph_format.space_after = Pt(3)
                    if p.runs:
                        p.runs[0].font.name = 'Calibri'
                        p.runs[0].font.size = Pt(9)
                        p.runs[0].font.bold = True
                        p.runs[0].font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
                    set_cell_background(hdr_cells[col_idx], "F1F5F9")
                    set_cell_margins(hdr_cells[col_idx], 80, 80, 120, 120)

                # Format Data Rows
                for r_idx, row_data in enumerate(data_rows):
                    row_cells = table.rows[r_idx + 1].cells
                    for c_idx in range(min(len(row_data), len(header_row))):
                        val_raw = row_data[c_idx]
                        cell_p = row_cells[c_idx].paragraphs[0]
                        cell_p.paragraph_format.space_before = Pt(2)
                        cell_p.paragraph_format.space_after = Pt(2)
                        add_formatted_runs(cell_p, val_raw, base_font_size=Pt(8.5), base_color=RGBColor(0x1e, 0x29, 0x3b))
                        set_cell_margins(row_cells[c_idx], 60, 60, 100, 100)
                        if r_idx % 2 == 1:
                            set_cell_background(row_cells[c_idx], "F8FAFC")

                p_sp = doc.add_paragraph()
                p_sp.paragraph_format.space_after = Pt(6)
            continue

        # Code block (SQL / Python) - Fix glued lines by adding a separate paragraph for every line!
        if stripped.startswith("```"):
            code_lines = []
            i += 1
            while i < len(body_lines) and not body_lines[i].strip().startswith("```"):
                code_lines.append(body_lines[i])
                i += 1
            i += 1 # skip closing ```

            # Container shading
            for line_idx, c_line in enumerate(code_lines):
                p_code = doc.add_paragraph()
                p_code.paragraph_format.left_indent = Inches(0.4)
                p_code.paragraph_format.space_before = Pt(4 if line_idx == 0 else 0)
                p_code.paragraph_format.space_after = Pt(6 if line_idx == len(code_lines) - 1 else 0)
                p_code.paragraph_format.line_spacing = 1.05
                r = p_code.add_run(c_line)
                r.font.name = 'Consolas'
                r.font.size = Pt(8.5)
                r.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)
            continue

        # Math display equations ($$ ... $$)
        if stripped.startswith("$$") and stripped.endswith("$$") and len(stripped) > 4:
            raw_eq = stripped[2:-2].strip()
            clean_eq = clean_latex_math(raw_eq)
            p_eq = doc.add_paragraph()
            p_eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_eq.paragraph_format.space_before = Pt(6)
            p_eq.paragraph_format.space_after = Pt(6)
            r = p_eq.add_run(clean_eq)
            r.font.name = 'Cambria Math'
            r.font.italic = True
            r.font.size = Pt(10.5)
            r.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
            i += 1
            continue

        # Bullet list item
        if stripped.startswith("* ") or stripped.startswith("- "):
            item_text = stripped[2:].strip()
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            add_formatted_runs(p, item_text, base_font_size=Pt(10), base_color=RGBColor(0x1e, 0x29, 0x3b))
            i += 1
            continue

        # Numbered list item / References (Hanging indent with exact numbering)
        num_match = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if num_match:
            num = num_match.group(1)
            item_text = num_match.group(2)
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.32)
            p.paragraph_format.first_line_indent = Inches(-0.32)
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(3)
            r_num = p.add_run(f"{num}.\t")
            r_num.font.name = 'Calibri'
            r_num.font.size = Pt(10)
            r_num.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)
            r_num.font.bold = True
            add_formatted_runs(p, item_text, base_font_size=Pt(10), base_color=RGBColor(0x1e, 0x29, 0x3b))
            i += 1
            continue

        # Regular Body Paragraph
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(5)
        add_formatted_runs(p, stripped, base_font_size=Pt(10.5), base_color=RGBColor(0x1a, 0x1a, 0x1a))
        i += 1

    # Save to primary targets
    out_docx_1 = os.path.join(workspace_dir, "FIFA_World_Cup_2026_Q1_Data_Descriptor.docx")
    doc.save(out_docx_1)
    print(f"Generated clean DOCX: {out_docx_1}")

    # Copy to downloads folder for immediate user availability
    downloads_dir = r"C:\Users\ASUS\Downloads"
    if os.path.exists(downloads_dir):
        out_dl_1 = os.path.join(downloads_dir, "FIFA_World_Cup_2026_Q1_Data_Descriptor_Clean.docx")
        out_dl_2 = os.path.join(downloads_dir, "FIFA_World_Cup_2026_Q1_Data_Descriptor (8).docx")
        shutil.copyfile(out_docx_1, out_dl_1)
        shutil.copyfile(out_docx_1, out_dl_2)
        print(f"Synced to Downloads: {out_dl_1} and {out_dl_2}")

if __name__ == "__main__":
    build_docx()
