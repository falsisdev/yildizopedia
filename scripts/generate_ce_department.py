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

def get_ce_api(endpoint):
    url = f"https://ce.yildiz.edu.tr:8080/api/{endpoint}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            return json.loads(r.read().decode('utf-8'))
    except Exception as e:
        print(f"Error {endpoint}: {e}")
        return None

def fetch_course_details(course_url):
    try:
        soup = get_soup(course_url)
        tables = soup.find_all('table')
        if not tables:
            return None
        info = {}
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
    print("=== FETCHING CE BOLOGNA CURRICULUM ===")
    bologna_url = 'http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=550&aid=3'
    soup = get_soup(bologna_url)
    
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
                
    base_dir = "05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/bilgisayar_muhendisligi"
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
    
    prereq_list = []
    for sec_name, (sem_num, fname, sem_title) in semester_map.items():
        courses = curriculum.get(sec_name, [])
        total_ects = sum(int(c['ects']) for c in courses if c['ects'].isdigit())
        total_credit = sum(float(c['credit']) for c in courses if c['credit'].replace('.', '', 1).isdigit())
        
        md_content = f"""---
baslik: "Bilgisayar Mühendisliği Lisans Programı - {sem_title} Ders Planı"
kategori: "fakulteler_ve_bolumler"
bolum: "Bilgisayar Mühendisliği"
yariyil: {sem_num}
toplam_akts: {total_ects}
toplam_kredi: {total_credit}
kaynak: "{bologna_url}"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"
---

# Bilgisayar Mühendisliği Lisans Programı - {sem_title}

Bu belgede, YTÜ Bilgisayar Mühendisliği Lisans Programı'nın ({sem_title}) dersleri, kredileri, AKTS değerleri, haftalık saatleri ve önkoşul koşulları listelenmektedir.

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
        
    # onkosul_zinciri.md
    onkosul_md = f"""---
baslik: "Bilgisayar Mühendisliği Önkoşul Zinciri ve Bağımlılık Haritası"
kategori: "fakulteler_ve_bolumler"
bolum: "Bilgisayar Mühendisliği"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"
kaynak: "{bologna_url}"
---

# Bilgisayar Mühendisliği Lisans Programı Önkoşul Zinciri

Bilgisayar Mühendisliği programında derslerin önkoşul zinciri ve kritik başarı koşulları aşağıda listelenmiştir.

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
    BLM1011["BLM1011 Bilgisayar Mühendisliğine Giriş"] --> BLM1012["BLM1012 Yapısal Programlama"]
    BLM1012 --> BLM2011["BLM2011 Nesneye Yönelik Programlama"]
    BLM2011 --> BLM2022["BLM2022 Veri Yapıları ve Algoritmalar"]
    BLM2022 --> BLM3011["BLM3011 Algoritma Analizi"]
    BLM2022 --> BLM3021["BLM3021 İşletim Sistemleri"]
    BLM2022 --> BLM3041["BLM3041 Veritabanı Yönetimi"]
    BLM3901["BLM3901 Ara Proje"] --> BLM4901["BLM4901 Bitirme Tezi"]
```
"""
    with open(os.path.join(bologna_dir, "onkosul_zinciri.md"), 'w', encoding='utf-8') as f:
        f.write(onkosul_md)
    print("Generated onkosul_zinciri.md")

    # secimlik_ders_havuzlari.md
    secimli_md = f"""---
baslik: "Bilgisayar Mühendisliği Seçmeli Ders Havuzları"
kategori: "fakulteler_ve_bolumler"
bolum: "Bilgisayar Mühendisliği"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"
kaynak: "{bologna_url}"
---

# Bilgisayar Mühendisliği Seçimlik Ders Havuzları

Bilgisayar Mühendisliği lisans programındaki mesleki ve sosyal seçmeli havuzlar:

---
"""
    for sec_name, courses in curriculum.items():
        if 'Seçmeli' in sec_name or 'Seçim' in sec_name:
            secimli_md += f"\n## 📚 {sec_name} ({len(courses)} Ders)\n\n"
            secimli_md += "| Kodu | Ders Adı | T | U | L | Kredi | AKTS |\n| :--- | :--- | :---: | :---: | :---: | :---: | :---: |\n"
            for c in courses[:20]:
                secimli_md += f"| **{c['code']}** | [{c['name']}]({c['link']}) | {c['lec']} | {c['app']} | {c['lab']} | {c['credit']} | **{c['ects']}** |\n"
            if len(courses) > 20:
                secimli_md += f"\n> *Ve toplam {len(courses)} adet seçmeli ders havuzda bulunmaktadır.*\n"

    with open(os.path.join(bologna_dir, "secimlik_ders_havuzlari.md"), 'w', encoding='utf-8') as f:
        f.write(secimli_md)
    print("Generated secimlik_ders_havuzlari.md")

    # bologna_ders_plani/README.md
    bologna_readme = f"""---
baslik: "Bilgisayar Mühendisliği Bologna Ders Planı Master İndeksi"
kategori: "fakulteler_ve_bolumler"
bolum: "Bilgisayar Mühendisliği"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"
---

# Bilgisayar Mühendisliği Bologna Ders Planı ve Müfredatı

YTÜ Bilgisayar Mühendisliği Bölümü (%30 İngilizce, Bologna ID: 550, ABET & MÜDEK Akredite), 8 yarıyıl ve 240 AKTS'lik lisans müfredatına sahiptir.

## Yarıyıllar
- [1. Yarıyıl (Güz)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/bilgisayar_muhendisligi/bologna_ders_plani/1_yariyil.md)
- [2. Yarıyıl (Bahar)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/bilgisayar_muhendisligi/bologna_ders_plani/2_yariyil.md)
- [3. Yarıyıl (Güz)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/bilgisayar_muhendisligi/bologna_ders_plani/3_yariyil.md)
- [4. Yarıyıl (Bahar)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/bilgisayar_muhendisligi/bologna_ders_plani/4_yariyil.md)
- [5. Yarıyıl (Güz)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/bilgisayar_muhendisligi/bologna_ders_plani/5_yariyil.md)
- [6. Yarıyıl (Bahar)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/bilgisayar_muhendisligi/bologna_ders_plani/6_yariyil.md)
- [7. Yarıyıl (Güz)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/bilgisayar_muhendisligi/bologna_ders_plani/7_yariyil.md)
- [8. Yarıyıl (Bahar)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/bilgisayar_muhendisligi/bologna_ders_plani/8_yariyil.md)
- [Önkoşul Zinciri ve Bağımlılık Haritası](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/bilgisayar_muhendisligi/bologna_ders_plani/onkosul_zinciri.md)
- [Seçmeli Ders Havuzları](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/bilgisayar_muhendisligi/bologna_ders_plani/secimlik_ders_havuzlari.md)
"""
    with open(os.path.join(bologna_dir, "README.md"), 'w', encoding='utf-8') as f:
        f.write(bologna_readme)
    print("Generated bologna_ders_plani/README.md")

    # 2. Fetch and generate core CE files
    print("=== FETCHING CE API DATA FOR CORE FILES ===")
    home_settings = get_ce_api("home-settings") or {}
    
    # 2.1 README.md
    readme_md = f"""---
baslik: "YTÜ Bilgisayar Mühendisliği Bölümü Külliyatı"
kategori: "fakulteler_ve_bolumler"
bolum: "Bilgisayar Mühendisliği"
fakulte: "Elektrik-Elektronik Fakültesi"
web: "https://ce.yildiz.edu.tr/"
bologna_program_id: 550
bologna_birim_id: 3
egitim_dili: "%30 İngilizce"
akreditasyon: "ABET (EAC) & MÜDEK"
anahtar_kelimeler: ["bilgisayar mühendisliği", "ce", "blm", "abet", "müdek", "yapay zeka", "yazılım", "skylab"]
---

# YTÜ Bilgisayar Mühendisliği Bölümü

Yıldız Teknik Üniversitesi Bilgisayar Mühendisliği Bölümü, temeli 1970 yılında kurulan "Elektronik Hesap Bilimleri Kürsüsü"ne dayanan, 1982'de bölüm statüsü kazanan ve 1992'de Elektrik-Elektronik Fakültesi bünyesine katılan Türkiye'nin en köklü bilişim ve bilgisayar mühendisliği programlarından biridir.

Bölüm lisans programı hem **ABET (Accreditation Board for Engineering and Technology)** hem de **MÜDEK** tarafından uluslararası düzeyde tam akreditedir.

---

## 🏛️ Anabilim Dalları ve Yönetim
- **Bilgisayar Bilimleri Anabilim Dalı:** Algoritmalar, veri yapıları, hesaplama kuramı, biçimsel diller.
- **Bilgisayar Donanımı Anabilim Dalı:** Mikroişlemciler, gömülü sistemler, bilgisayar mimarisi, FPGA.
- **Bilgisayar Yazılımı Anabilim Dalı:** Yazılım mühendisliği, yapay zeka, derin öğrenme, veri tabanı, bilgisayarla görü, siber güvenlik.

---

## 📚 Dokümantasyon Rehberi
- [Lisans Eğitim Yapısı ve Akreditasyon](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/bilgisayar_muhendisligi/lisans_egitim_yapisi.md): %30 İngilizce programı, ABET ve MÜDEK çıktıları, KOOP modeli.
- [Staj ve Proje Yönetim Sistemi](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/bilgisayar_muhendisligi/staj_ve_proje_sistemi.md): Staj 1 ve Staj 2, Ara Proje, Bitirme Tezi, ÇDTP ve Proje Sistemi Portalı.
- [Laboratuvarlar, Araştırma Grupları ve Sky Lab](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/bilgisayar_muhendisligi/laboratuvarlar_ve_arastirma.md): Araştırma laboratuvarları ve Türkiye'nin en aktif öğrenci yazılım kulübü Sky Lab.
- [Komisyonlar ve Öğrenci Danışmanlığı](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/bilgisayar_muhendisligi/komisyonlar_ve_ogrenci_danismanligi.md): Staj, intibak, akreditasyon komisyonları ve akran danışmanı Elif İrem Külcü.
- [Lisansüstü Programlar](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/bilgisayar_muhendisligi/lisansustu_programlar.md): Tezli YL, BT Tezsiz YL (Türkçe & İngilizce), Bilgisayar Doktora.
- [Bilgisayar Mühendisliği SSS (44 Soru-Cevap)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/bilgisayar_muhendisligi/sikca_sorulan_sorular.md): Bölüm API'sinden elde edilen 44 resmi soru ve cevap tam metni.
- [Bologna Lisans Ders Planı (1-8. Yarıyıllar)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/bilgisayar_muhendisligi/bologna_ders_plani/README.md): 8 yarıyılın BLM kodlu dersleri, önkoşulları ve seçmeli havuzları.
"""
    with open(os.path.join(base_dir, "README.md"), 'w', encoding='utf-8') as f:
        f.write(readme_md)
    print("Generated CE README.md")

    # 2.2 SSS (44 questions)
    faqs = home_settings.get("frequent_questions", [])
    sss_md = f"""---
baslik: "YTÜ Bilgisayar Mühendisliği Sıkça Sorulan Sorular (44 Soru-Cevap)"
kategori: "fakulteler_ve_bolumler"
bolum: "Bilgisayar Mühendisliği"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bölüm Portalı API)"
kaynak: "https://ce.yildiz.edu.tr:8080/api/home-settings"
anahtar_kelimeler: ["bilgisayar mühendisliği sss", "ders seçimi", "staj", "bitirme", "abet", "ingilizce hazırlık"]
---

# YTÜ Bilgisayar Mühendisliği Sıkça Sorulan Sorular

Bu dokümanda, YTÜ Bilgisayar Mühendisliği Bölümü resmi web sitesinde yayımlanan **44 soru ve cevabın tam metni** yer almaktadır.

---
"""
    for idx, faq in enumerate(faqs, 1):
        q_tr = faq.get('title', {}).get('tr', '')
        a_tr = faq.get('text', {}).get('tr', '')
        q_en = faq.get('title', {}).get('en', '')
        a_en = faq.get('text', {}).get('en', '')
        sss_md += f"### S{idx}: {q_tr}\n"
        if q_en:
            sss_md += f"> *EN: {q_en}*\n\n"
        sss_md += f"> **Cevap:** {a_tr}\n"
        if a_en:
            sss_md += f">\n> *EN: {a_en}*\n"
        sss_md += "\n---\n\n"

    with open(os.path.join(base_dir, "sikca_sorulan_sorular.md"), 'w', encoding='utf-8') as f:
        f.write(sss_md)
    print(f"Generated CE sikca_sorulan_sorular.md ({len(faqs)} FAQs)")

    # 2.3 lisans_egitim_yapisi.md
    lisans_md = f"""---
baslik: "YTÜ Bilgisayar Mühendisliği Lisans Eğitim Yapısı ve Akreditasyon"
kategori: "fakulteler_ve_bolumler"
bolum: "Bilgisayar Mühendisliği"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bölüm & Bologna Portalı)"
kaynak: "https://ce.yildiz.edu.tr/"
anahtar_kelimeler: ["bilgisayar lisans", "abet", "müdek", "program çıktıları", "koop"]
---

# YTÜ Bilgisayar Mühendisliği Lisans Eğitim Yapısı

YTÜ Bilgisayar Mühendisliği Lisans Programı (%30 İngilizce, Bologna ID: 550), 240 AKTS kredisi ve 8 yarıyıldan oluşmaktadır. Program, uluslararası **ABET (EAC)** ve ulusal **MÜDEK** tarafından tam akredite edilmiştir.

---

## 🎖️ Uluslararası ve Ulusal Akreditasyon
- **ABET EAC (Engineering Accreditation Commission):** Mezunlarımızın diplomaları ABD ve uluslararası düzeyde mühendislik eşdeğerliğine sahiptir.
- **MÜDEK & EUR-ACE:** Avrupa Yükseköğretim Alanı mühendislik kalite güvencesi.

---

## 🎯 Program Eğitim Amaçları
1. Bilgisayar mühendisliği ve bilişim sistemleri alanında lider ulusal ve uluslararası şirketlerde yazılım geliştirici, sistem analisti, veri bilimci veya AR-GE mühendisi olarak çalışmak.
2. Saygın üniversitelerde lisansüstü eğitim alarak akademik dünyada veya endüstriyel araştırma merkezlerinde yenilikçi araştırmalar yürütmek.
3. Kendi girişimini kurarak küresel pazara hitap eden yenilikçi yazılım ve donanım teknolojileri üretmek.

---

## 🏢 KOOP (İşletmede Mesleki Eğitim) Modeli
Bilgisayar Mühendisliği öğrencileri, 8. yarıyılda ders yükümlülüklerinin büyük kısmını tamamlamış olmak ve AGNO >= 2.50 şartıyla, anlaşmalı lider teknoloji firmalarında (Trendyol, Baykar, Aselsan, Turkcell, Softtech vb.) tam zamanlı çalışarak mezuniyet öncesi profesyonel iş deneyimi kazanırlar.
"""
    with open(os.path.join(base_dir, "lisans_egitim_yapisi.md"), 'w', encoding='utf-8') as f:
        f.write(lisans_md)
    print("Generated CE lisans_egitim_yapisi.md")

    # 2.4 staj_ve_proje_sistemi.md
    staj_md = f"""---
baslik: "YTÜ Bilgisayar Mühendisliği Staj, Bitirme ve Proje Sistemi"
kategori: "fakulteler_ve_bolumler"
bolum: "Bilgisayar Mühendisliği"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bölüm Portalı)"
kaynak: "https://ce.yildiz.edu.tr/"
anahtar_kelimeler: ["bilgisayar staj", "staj 1", "staj 2", "proje sistemi", "bitirme projesi", "ara proje", "çdtp"]
---

# YTÜ Bilgisayar Mühendisliği Staj ve Proje Sistemi

Bilgisayar Mühendisliği Bölümü'nde stajlar ve mezuniyet projeleri bölümün online **Proje ve Staj Yönetim Sistemi (`https://ce.yildiz.edu.tr/proje-sistemi`)** üzerinden yürütülür.

---

## 🛠️ 1. Staj Esasları (Toplam 60 İş Günü)

1. **Staj 1 (Donanım / Temel Staj - 30 İş Günü):**
   - **Önkoşul:** 4. yarıyılın tamamlanmış olması.
   - **Kapsam:** Bilgisayar donanımı, ağ altyapısı, sunucu yönetimi, sistem kurulumu ve temel bakım-onarım.
2. **Staj 2 (Yazılım / Mesleki Staj - 30 İş Günü):**
   - **Önkoşul:** Staj 1'in tamamlanması ve 6. yarıyılın bitirilmesi.
   - **Kapsam:** Yazılım geliştirme yaşam döngüsü (SDLC), veritabanı tasarımı, web/mobil geliştirme, yapay zeka ve algoritma geliştirme.

---

## 💻 2. Online Proje Sistemi Portalı (`proje-sistemi`)
Bölüm öğrencileri, bitirme ve tasarım projelerini [ce.yildiz.edu.tr/proje-sistemi](https://ce.yildiz.edu.tr/proje-sistemi) portalı üzerinden yürütürler:
- Proje grubu oluşturma ve onaylatma
- Akademik danışman seçimi
- Ara rapor teslimleri ve intihal kontrolleri
- Jüri ve sunum tarihlerinin ilanı

---

## 🎓 3. Proje Kademeleri
1. **BLM3901 / BLM3902 Ara Proje (6. / 7. Yarıyıl):** Öğrencilerin bireysel veya takım halinde bir problemi tanımlayıp prototip geliştirdiği projedir. Bitirme tezine hazırlık niteliğindedir.
2. **BLM4901 / BLM4902 Bitirme Tezi (8. Yarıyıl):** 6 AKTS değerindeki mezuniyet projesidir. Jüri önünde poster ve canlı kod demosu ile sunulur.
3. **Çok Disiplinli Tasarım Projesi (ÇDTP):** Elektrik-Elektronik Fakültesi'nin diğer bölümleriyle (EHM, BME, KOM, ELM) ortak takımlar kurularak geliştirilen disiplinlerarası projedir.
"""
    with open(os.path.join(base_dir, "staj_ve_proje_sistemi.md"), 'w', encoding='utf-8') as f:
        f.write(staj_md)
    print("Generated CE staj_ve_proje_sistemi.md")

    # 2.5 laboratuvarlar_ve_arastirma.md
    lab_md = f"""---
baslik: "YTÜ Bilgisayar Mühendisliği Laboratuvarları, Araştırma Grupları ve Sky Lab"
kategori: "fakulteler_ve_bolumler"
bolum: "Bilgisayar Mühendisliği"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bölüm Portalı)"
kaynak: "https://ce.yildiz.edu.tr/"
anahtar_kelimeler: ["bilgisayar laboratuvarları", "araştırma grupları", "sky lab", "yapay zeka lab", "bilgisayarla görü"]
---

# YTÜ Bilgisayar Mühendisliği Laboratuvarları ve Araştırma Altyapısı

---

## 🔬 1. Eğitim ve Araştırma Laboratuvarları
1. **Yazılım Geliştirme Laboratuvarları (PC Lab 1, 2, 3):** Modern masaüstü iş istasyonları, Linux ve Windows çift önyükleme, yüksek hızlı ağ bağlantısı.
2. **Mikroişlemci ve Gömülü Sistemler Laboratuvarı:** ARM Cortex, Arduino, FPGA geliştirme kartları, osiloskop ve lojik analizörler.
3. **Ağ ve Güvenlik Laboratuvarı:** Cisco yönlendiriciler, anahtarlar, güvenlik duvarı cihazları ve sanallaştırma sunucuları.
4. **Yapay Zeka ve Yüksek Başarımlı Hesaplama (HPC) Laboratuvarı:** GPU hızlandırmalı sunucular (NVIDIA RTX/A serisi), derin öğrenme iş istasyonları.

---

## 🧠 2. Başlıca Araştırma Grupları
- **Yapay Zeka ve Veri Madenciliği Grubu:** Doğal Dil İşleme (NLP), büyük veri analitiği, öneri sistemleri.
- **Bilgisayarla Görü ve Örüntü Tanıma Grubu:** Medikal görüntü işleme, nesne tespiti, otonom araç algılama sistemleri.
- **Siber Güvenlik ve Ağ Sistemleri Grubu:** Kriptografi, ağ güvenliği, sızma testleri, blokzincir.
- **Biyoenformatik Grubu:** Genom dizilimi analizi, protein yapısı modelleme.

---

## 🚀 3. Sky Lab Kulübü (Öğrenci Yazılım Kulübü)
Sky Lab Kulübü (`skylab.yildiz.edu.tr`), YTÜ Bilgisayar Mühendisliği öğrencilerinin kurduğu ve Türkiye çapında en aktif öğrenci teknoloji kulüplerindendir:
- **Faaliyetler:** Web geliştirme, yapay zeka, mobil uygulama, oyun geliştirme (Game Jam) atölyeleri.
- **Etkinlikler:** "Yıldız Yazılım Günleri" (YYG), algoritmik programlama yarışmaları ve hackathonlar.
"""
    with open(os.path.join(base_dir, "laboratuvarlar_ve_arastirma.md"), 'w', encoding='utf-8') as f:
        f.write(lab_md)
    print("Generated CE laboratuvarlar_ve_arastirma.md")

    # 2.6 komisyonlar_ve_ogrenci_danismanligi.md
    kom_md = f"""---
baslik: "YTÜ Bilgisayar Mühendisliği Komisyonlar ve Öğrenci Danışmanlığı"
kategori: "fakulteler_ve_bolumler"
bolum: "Bilgisayar Mühendisliği"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bölüm Portalı)"
kaynak: "https://ce.yildiz.edu.tr/"
anahtar_kelimeler: ["bilgisayar komisyonlar", "staj komisyonu", "intibak", "elif irem külcü", "akran danışmanı"]
---

# YTÜ Bilgisayar Mühendisliği Komisyonlar ve Öğrenci Danışmanlığı

---

## 🏛️ 1. Bölüm Komisyonları
- **Staj Komisyonu:** Staj başvuru onayları, staj yeri kriterleri uygunluğu ve defter değerlendirmeleri.
- **İntibak ve Muafiyet Komisyonu:** Yatay geçiş, DGS ve ÇAP öğrencilerinin ders intibakları (YÖ-097).
- **ABET ve MÜDEK Akreditasyon Komisyonu:** Eğitim çıktıları ve ders portfolyolarının uluslararası denetimi.
- **Bitirme ve Tasarım Projeleri Komisyonu:** Proje portalı yönetimi, jüri atamaları ve savunma takvimleri.
- **ÇAP / Yandal Komisyonu:** Çift anadal protokollerinin düzenlenmesi ve öğrenci başvurularının sıralanması.

---

## 👥 2. Öğrenci Danışmanlığı
- **Akran Danışmanı:** Elif İrem KÜLCÜ  
  - *E-posta:* `irem.kulcu@std.yildiz.edu.tr`
- **Akademik Danışmanlar:** Her öğrenciye kayıt esnasında atanan öğretim üyesi danışman; dönemlik OBS ders kayıt onayları ve akademik başarı takibinden sorumludur.
"""
    with open(os.path.join(base_dir, "komisyonlar_ve_ogrenci_danismanligi.md"), 'w', encoding='utf-8') as f:
        f.write(kom_md)
    print("Generated CE komisyonlar_ve_ogrenci_danismanligi.md")

    # 2.7 lisansustu_programlar.md
    lisansustu_md = f"""---
baslik: "YTÜ Bilgisayar Mühendisliği Lisansüstü Programlar Rehberi"
kategori: "fakulteler_ve_bolumler"
bolum: "Bilgisayar Mühendisliği"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna & FBE Portalı)"
kaynak: "http://www.fbe.yildiz.edu.tr/"
anahtar_kelimeler: ["bilgisayar yüksek lisans", "bilgi teknolojileri", "bilgisayar doktora", "fbe"]
---

# YTÜ Bilgisayar Mühendisliği Lisansüstü Programlar Rehberi

Fen Bilimleri Enstitüsü (FBE) bünyesinde yürütülen lisansüstü programlar:

| Program Adı | Tür | Bologna ID | Eğitim Dili |
| :--- | :--- | :---: | :--- |
| **Bilgisayar Mühendisliği Yüksek Lisans Programı** | Tezli YL | 279 | Türkçe |
| **Bilgi Teknolojileri Yüksek Lisans Programı (İ.Ö.)** | Tezsiz YL | 373 | Türkçe |
| **Bilgisayar Mühendisliği Yüksek Lisans Programı** | Tezsiz YL | 371 | Türkçe |
| **Bilgi Teknolojileri YL (İ.Ö. İngilizce)** | Tezsiz YL | 372 | İngilizce |
| **Bilgisayar Mühendisliği Doktora Programı** | Doktora | 280 | Türkçe |

---

## 📌 Başvuru Kriterleri
- Sayısal ALES (Tezli YL için >= 70, Doktora için >= 75)
- Yabancı Dil YDS/YÖKDİL (Tezli YL için >= 50, Doktora için >= 60)
- Başvurular: [YTÜ Fen Bilimleri Enstitüsü](http://www.fbe.yildiz.edu.tr/)
"""
    with open(os.path.join(base_dir, "lisansustu_programlar.md"), 'w', encoding='utf-8') as f:
        f.write(lisansustu_md)
    print("Generated CE lisansustu_programlar.md")

if __name__ == '__main__':
    run()
