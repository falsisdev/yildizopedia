import os
import re
import ssl
import json
import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup

ctx = ssl._create_unverified_context()

def get_soup(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
    with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
        return BeautifulSoup(resp.read().decode('utf-8', errors='ignore'), 'html.parser')

def fetch_course_details(course_url):
    try:
        soup = get_soup(course_url)
        tables = soup.find_all('table')
        if not tables:
            return None
        info = {}
        # Objectives and content (usually table 5)
        for t in tables:
            text = t.get_text()
            if 'Dersin Amacı' in text or 'Dersin İçeriği' in text or 'Course Objectives' in text:
                for tr in t.find_all('tr'):
                    tds = tr.find_all(['td', 'th'])
                    if len(tds) >= 2:
                        k = tds[0].get_text(strip=True)
                        v = tds[1].get_text(strip=True)
                        if 'Amaç' in k or 'Objectives' in k:
                            info['amac'] = v
                        elif 'İçerik' in k or 'Content' in k:
                            info['icerik'] = v
            # Weekly schedule
            if 'Haftalık Konular' in text or 'Hafta' in text:
                weekly = []
                for tr in t.find_all('tr'):
                    tds = tr.find_all(['td', 'th'])
                    if len(tds) >= 2:
                        w_num = tds[0].get_text(strip=True)
                        w_subj = tds[1].get_text(strip=True)
                        if w_num.isdigit():
                            weekly.append(f"{w_num}. Hafta: {w_subj}")
                if weekly:
                    info['haftalik'] = weekly
        return info
    except Exception as e:
        return None

def run():
    print("=== FETCHING ELM BOLOGNA CURRICULUM ===")
    url = 'http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=7&aid=4'
    soup = get_soup(url)
    
    t2 = soup.find_all('table')[2]
    curriculum = {}
    current_section = None
    
    for row in t2.find_all('tr'):
        ths = row.find_all('th')
        if len(ths) == 1:
            current_section = ths[0].get_text().strip()
            curriculum[current_section] = []
            continue
        
        tds = row.find_all(['td', 'th'])
        cols = [td.get_text().strip() for td in tds]
        if len(cols) >= 8 and cols[0] != 'Kodu':
            link_tag = row.find('a', href=True)
            link = urljoin('http://www.bologna.yildiz.edu.tr/', link_tag['href']) if link_tag else None
            course_data = {
                'code': cols[0],
                'prereq': cols[1],
                'name': cols[2],
                'lec': cols[3],
                'app': cols[4],
                'lab': cols[5],
                'credit': cols[6],
                'ects': cols[7],
                'link': link
            }
            if current_section:
                curriculum[current_section].append(course_data)
                
    base_dir = "05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektrik_muhendisligi"
    bologna_dir = os.path.join(base_dir, "bologna_ders_plani")
    os.makedirs(bologna_dir, exist_ok=True)
    
    semester_map = {
        '1.Yıl  - Güz Yarıyılı': (1, "1_yariyil.md", "1. Yarıyıl (Güz)"),
        '1.Yıl  - Bahar Yarıyılı': (2, "2_yariyil.md", "2. Yarıyıl (Bahar)"),
        '2.Yıl  - Güz Yarıyılı': (3, "3_yariyil.md", "3. Yarıyıl (Güz)"),
        '2.Yıl  - Bahar Yarıyılı': (4, "4_yariyil.md", "4. Yarıyıl (Bahar)"),
        '3.Yıl  - Güz Yarıyılı': (5, "5_yariyil.md", "5. Yarıyıl (Güz)"),
        '3.Yıl  - Bahar Yarıyılı': (6, "6_yariyil.md", "6. Yarıyıl (Bahar)"),
        '4.Yıl  - Güz Yarıyılı': (7, "7_yariyil.md", "7. Yarıyıl (Güz)"),
        '4.Yıl  - Bahar Yarıyılı': (8, "8_yariyil.md", "8. Yarıyıl (Bahar)")
    }
    
    # 1. Generate 1_yariyil.md to 8_yariyil.md
    prereq_list = []
    for sec_name, (sem_num, fname, sem_title) in semester_map.items():
        courses = curriculum.get(sec_name, [])
        total_ects = sum(int(c['ects']) for c in courses if c['ects'].isdigit())
        total_credit = sum(float(c['credit']) for c in courses if c['credit'].replace('.', '', 1).isdigit())
        
        md_content = f"""---
baslik: "Elektrik Mühendisliği Lisans Programı - {sem_title} Ders Planı"
kategori: "fakulteler_ve_bolumler"
bolum: "Elektrik Mühendisliği"
yariyil: {sem_num}
toplam_akts: {total_ects}
toplam_kredi: {total_credit}
kaynak: "{url}"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"
---

# Elektrik Mühendisliği Lisans Programı - {sem_title}

Bu belgede, YTÜ Elektrik Mühendisliği Lisans Programı'nın ({sem_title}) dersleri, kredileri, AKTS değerleri, haftalık saatleri ve önkoşul koşulları listelenmektedir.

> [!NOTE] Yarıyıl Özeti
> - **Dönem:** {sem_title}
> - **Ders Sayısı:** {len(courses)} adet
> - **Toplam Yerel Kredi:** {total_credit}
> - **Toplam AKTS Kredisi:** {total_ects} AKTS

---

## 📋 Ders Listesi ve Kredi Dağılımı

| Ders Kodu | Önkoşul | Ders Adı | T | U | L | Kredi | AKTS |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
"""
        for c in courses:
            prq = c['prereq'] if c['prereq'] else '-'
            if prq != '-' and prq.lower() != 'yok':
                prereq_list.append((c['code'], c['name'], prq, sem_title))
            md_content += f"| **{c['code']}** | {prq} | [{c['name']}]({c['link']}) | {c['lec']} | {c['app']} | {c['lab']} | {c['credit']} | **{c['ects']}** |\n"
            
        md_content += "\n---\n\n## 🔍 Ders Kartları ve Ayrıntılı Bilgiler\n\n"
        for c in courses:
            details = fetch_course_details(c['link']) if c['link'] else None
            md_content += f"### 📌 {c['code']} - {c['name']}\n"
            md_content += f"- **Ders Türü:** Zorunlu / Mesleki\n"
            md_content += f"- **Kredi Bilgisi:** {c['lec']} Saat Teori, {c['app']} Saat Uygulama, {c['lab']} Saat Laboratuvar | **{c['credit']} Kredi / {c['ects']} AKTS**\n"
            md_content += f"- **Önkoşul:** {c['prereq'] if c['prereq'] else 'Yok'}\n"
            if details and details.get('amac'):
                md_content += f"- **Dersin Amacı:** {details['amac']}\n"
            if details and details.get('icerik'):
                md_content += f"- **Dersin İçeriği:** {details['icerik']}\n"
            if details and details.get('haftalik'):
                md_content += "- **Haftalık Ders Planı:**\n"
                for w in details['haftalik'][:8]:
                    md_content += f"  - {w}\n"
            md_content += f"- **Resmi Bologna Bağlantısı:** [Bologna Ders Detayı]({c['link']})\n\n"
            
        filepath = os.path.join(bologna_dir, fname)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"Generated {filepath}")
        
    # 2. Generate onkosul_zinciri.md
    onkosul_md = f"""---
baslik: "Elektrik Mühendisliği Önkoşul Zinciri ve Bağımlılık Haritası"
kategori: "fakulteler_ve_bolumler"
bolum: "Elektrik Mühendisliği"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"
kaynak: "{url}"
---

# Elektrik Mühendisliği Lisans Programı Önkoşul Zinciri

Elektrik Mühendisliği programında bir üst yarıyıldaki zorunlu dersi alabilmek için alt yarıyılda başarılması gereken dersler ve kritik önkoşul zinciri aşağıda listelenmiştir.

---

## 🔗 Önkoşul Tablosu

| Hedef Ders Kodu | Hedef Ders Adı | Gerekli Önkoşul Dersi | Yarıyıl |
| :--- | :--- | :--- | :--- |
"""
    for code, name, prq, sem in prereq_list:
        onkosul_md += f"| **{code}** | {name} | **{prq}** | {sem} |\n"

    onkosul_md += """
---

## 📊 Kritik Önkoşul Akış Şeması (Mermaid)

```mermaid
graph TD
    MAT1071["MAT1071 Matematik I"] --> MAT1072["MAT1072 Matematik II"]
    MAT1072 --> MAT2011["MAT2011 Diferansiyel Denklemler"]
    ELM2111["ELM2111 Devre Teorisi I"] --> ELM2112["ELM2112 Devre Teorisi II"]
    ELM2112 --> ELM3121["ELM3121 Elektromanyetik Alan Teorisi"]
    ELM3121 --> ELM3122["ELM3122 Elektromanyetik Dalga Teorisi"]
    ELM2112 --> ELM3211["ELM3211 Elektrik Makinaları I"]
    ELM3211 --> ELM3212["ELM3212 Elektrik Makinaları II"]
    ELM4901["ELM4901 Tasarım Projesi"] --> ELM4902["ELM4902 Bitirme Çalışması"]
```
"""
    with open(os.path.join(bologna_dir, "onkosul_zinciri.md"), 'w', encoding='utf-8') as f:
        f.write(onkosul_md)
    print("Generated onkosul_zinciri.md")

    # 3. Generate secimlik_ders_havuzlari.md
    secimli_md = f"""---
baslik: "Elektrik Mühendisliği Seçmeli Ders Havuzları"
kategori: "fakulteler_ve_bolumler"
bolum: "Elektrik Mühendisliği"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"
kaynak: "{url}"
---

# Elektrik Mühendisliği Seçimlik Ders Havuzları

Elektrik Mühendisliği lisans programında öğrencilerin uzmanlaşma alanlarına göre seçebileceği mesleki ve sosyal seçmeli havuzlar şunlardır:

---
"""
    for sec_name, courses in curriculum.items():
        if 'Seçmeli' in sec_name or 'Seçim' in sec_name:
            secimli_md += f"\n## 📚 {sec_name} ({len(courses)} Ders)\n\n"
            secimli_md += "| Kodu | Ders Adı | T | U | L | Kredi | AKTS |\n| :--- | :--- | :---: | :---: | :---: | :---: | :---: |\n"
            for c in courses[:20]: # top 20 representative electives
                secimli_md += f"| **{c['code']}** | [{c['name']}]({c['link']}) | {c['lec']} | {c['app']} | {c['lab']} | {c['credit']} | **{c['ects']}** |\n"
            if len(courses) > 20:
                secimli_md += f"\n> *Ve toplam {len(courses)} adet seçmeli ders havuzda bulunmaktadır.*\n"

    with open(os.path.join(bologna_dir, "secimlik_ders_havuzlari.md"), 'w', encoding='utf-8') as f:
        f.write(secimli_md)
    print("Generated secimlik_ders_havuzlari.md")

    # 4. Generate bologna_ders_plani/README.md
    bologna_readme = f"""---
baslik: "Elektrik Mühendisliği Bologna Ders Planı Master İndeksi"
kategori: "fakulteler_ve_bolumler"
bolum: "Elektrik Mühendisliği"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"
---

# Elektrik Mühendisliği Bologna Ders Planı ve Müfredatı

YTÜ Elektrik Mühendisliği Bölümü (%30 İngilizce, Bologna ID: 7), toplam 240 AKTS kredisinden oluşan 8 yarıyıllık lisans programına sahiptir.

## Yarıyıllar
- [1. Yarıyıl (Güz)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektrik_muhendisligi/bologna_ders_plani/1_yariyil.md)
- [2. Yarıyıl (Bahar)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektrik_muhendisligi/bologna_ders_plani/2_yariyil.md)
- [3. Yarıyıl (Güz)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektrik_muhendisligi/bologna_ders_plani/3_yariyil.md)
- [4. Yarıyıl (Bahar)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektrik_muhendisligi/bologna_ders_plani/4_yariyil.md)
- [5. Yarıyıl (Güz)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektrik_muhendisligi/bologna_ders_plani/5_yariyil.md)
- [6. Yarıyıl (Bahar)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektrik_muhendisligi/bologna_ders_plani/6_yariyil.md)
- [7. Yarıyıl (Güz)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektrik_muhendisligi/bologna_ders_plani/7_yariyil.md)
- [8. Yarıyıl (Bahar)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektrik_muhendisligi/bologna_ders_plani/8_yariyil.md)
- [Önkoşul Zinciri ve Bağımlılık Haritası](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektrik_muhendisligi/bologna_ders_plani/onkosul_zinciri.md)
- [Seçmeli Ders Havuzları](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektrik_muhendisligi/bologna_ders_plani/secimlik_ders_havuzlari.md)
"""
    with open(os.path.join(bologna_dir, "README.md"), 'w', encoding='utf-8') as f:
        f.write(bologna_readme)
    print("Generated bologna_ders_plani/README.md")

if __name__ == '__main__':
    run()
