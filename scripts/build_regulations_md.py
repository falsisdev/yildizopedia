import os
import re
import subprocess
from docx import Document
from pypdf import PdfReader

def get_text_from_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.docx':
        try:
            doc = Document(filepath)
            return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        except Exception as e:
            print(f"docx error {filepath}: {e}")
    elif ext == '.doc':
        try:
            res = subprocess.run(['textutil', '-convert', 'txt', filepath, '-stdout'], capture_output=True, text=True, check=True)
            return res.stdout
        except Exception as e:
            print(f"textutil error {filepath}: {e}")
    elif ext == '.pdf':
        try:
            reader = PdfReader(filepath)
            return "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
        except Exception as e:
            print(f"pdf error {filepath}: {e}")
    return ""

def clean_text_for_markdown(raw_text):
    lines = raw_text.splitlines()
    cleaned = []
    for line in lines:
        line_s = line.strip()
        if not line_s:
            continue
        # Check if line looks like article header
        if re.match(r'^(Madde|MADDE)\s+\d+', line_s, re.IGNORECASE):
            cleaned.append(f"\n### {line_s}\n")
        elif re.match(r'^(BİRİNCİ|İKİNCİ|ÜÇÜNCÜ|DÖRDÜNCÜ|BEŞİNCİ|ALTINCI|YEDİNCİ)\s+(BÖLÜM|KISIM)', line_s, re.IGNORECASE):
            cleaned.append(f"\n## {line_s}\n")
        elif re.match(r'^[a-zçğıöşü]\)\s+', line_s):
            cleaned.append(f"- **{line_s[:2]}** {line_s[2:].strip()}")
        elif re.match(r'^\d+\)\s+', line_s):
            cleaned.append(f"1. {line_s.split(')', 1)[1].strip()}")
        else:
            cleaned.append(line_s)
    return "\n".join(cleaned)

def create_md(target_path, frontmatter, title, summary, text, faq_list=None, rel_links=None):
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    
    fm_str = "---\n"
    for k, v in frontmatter.items():
        if isinstance(v, list):
            fm_str += f"{k}: {v}\n"
        else:
            fm_str += f"{k}: \"{v}\"\n"
    fm_str += "---\n\n"

    md = fm_str
    md += f"# {title}\n\n"
    md += f"> [!NOTE] Özet ve Amacı\n> {summary}\n\n"
    md += "## Yasal Dayanak ve Kapsam\n"
    md += f"Bu belge Yıldız Teknik Üniversitesi Senatosu ve ilgili mevzuat hükümlerine tabidir.\n\n"
    md += "## Belge Tam Metni\n\n"
    md += text + "\n\n"

    if faq_list:
        md += "## Öğrenciler İçin Kritik Sorular ve Cevaplar\n\n"
        for q, a in faq_list:
            md += f"### {q}\n{a}\n\n"

    if rel_links:
        md += "## İlgili Mevzuat ve Bağlantılar\n\n"
        for l_title, l_path in rel_links:
            md += f"- [{l_title}]({l_path})\n"
        md += "\n"

    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"Generated: {target_path}")

print("Helper script ready.")
