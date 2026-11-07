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

def build_bologna_program(program_id, aid, target_dir, prog_title, prog_lang):
    print(f"=== FETCHING KOM BOLOGNA: {prog_title} (ID: {program_id}) ===")
    url = f"http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id={program_id}&aid={aid}"
    soup = get_soup(url)
    os.makedirs(target_dir, exist_ok=True)
    
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
baslik: "Kontrol ve Otomasyon Mühendisliği ({prog_lang}) - {sem_title} Ders Planı"
kategori: "fakulteler_ve_bolumler"
bolum: "Kontrol ve Otomasyon Mühendisliği"
program: "{prog_title}"
yariyil: {sem_num}
toplam_akts: {total_ects}
toplam_kredi: {total_credit}
kaynak: "{url}"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"
---

# Kontrol ve Otomasyon Mühendisliği ({prog_lang}) - {sem_title}

Bu belgede, YTÜ Kontrol ve Otomasyon Mühendisliği ({prog_title}) Lisans Programı'nın ({sem_title}) dersleri, kredileri, AKTS değerleri, haftalık saatleri ve önkoşul koşulları listelenmektedir.

> [!NOTE] Yarıyıl Özeti
> - **Dönem:** {sem_title} ({prog_lang})
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
            
        filepath = os.path.join(target_dir, fname)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"Generated {filepath}")
        
    # onkosul_zinciri.md
    onkosul_md = f"""---
baslik: "Kontrol ve Otomasyon Mühendisliği ({prog_lang}) Önkoşul Zinciri"
kategori: "fakulteler_ve_bolumler"
bolum: "Kontrol ve Otomasyon Mühendisliği"
program: "{prog_title}"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"
kaynak: "{url}"
---

# Kontrol ve Otomasyon Mühendisliği ({prog_lang}) Önkoşul Zinciri

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
    KOM2111["KOM2111 Devre ve Sistem Analizi"] --> KOM3111["KOM3111 Otomatik Kontrol I"]
    KOM3111 --> KOM3112["KOM3112 Otomatik Kontrol II"]
    KOM3112 --> KOM4111["KOM4111 Dijital Kontrol"]
    KOM4901["KOM4901 Tasarım Projesi"] --> KOM4902["KOM4902 Bitirme Çalışması"]
```
"""
    with open(os.path.join(target_dir, "onkosul_zinciri.md"), 'w', encoding='utf-8') as f:
        f.write(onkosul_md)

    # secimlik_ders_havuzlari.md
    secimli_md = f"""---
baslik: "Kontrol ve Otomasyon Mühendisliği ({prog_lang}) Seçmeli Ders Havuzları"
kategori: "fakulteler_ve_bolumler"
bolum: "Kontrol ve Otomasyon Mühendisliği"
program: "{prog_title}"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"
kaynak: "{url}"
---

# Kontrol ve Otomasyon Mühendisliği ({prog_lang}) Seçmeli Ders Havuzları

---
"""
    for sec_name, courses in curriculum.items():
        if 'Seçmeli' in sec_name or 'Seçim' in sec_name:
            secimli_md += f"\n## 📚 {sec_name} ({len(courses)} Ders)\n\n"
            secimli_md += "| Kodu | Ders Adı | T | U | L | Kredi | AKTS |\n| :--- | :--- | :---: | :---: | :---: | :---: | :---: |\n"
            for c in courses[:20]:
                secimli_md += f"| **{c['code']}** | [{c['name']}]({c['link']}) | {c['lec']} | {c['app']} | {c['lab']} | {c['credit']} | **{c['ects']}** |\n"

    with open(os.path.join(target_dir, "secimlik_ders_havuzlari.md"), 'w', encoding='utf-8') as f:
        f.write(secimli_md)

    # README.md
    bologna_readme = f"""---
baslik: "Kontrol ve Otomasyon Mühendisliği ({prog_lang}) Bologna İndeksi"
kategori: "fakulteler_ve_bolumler"
bolum: "Kontrol ve Otomasyon Mühendisliği"
program: "{prog_title}"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"
---

# Kontrol ve Otomasyon Mühendisliği ({prog_lang}) Bologna Ders Planı

Bologna Program ID: {program_id} ({prog_title}), 8 yarıyıl ve 240 AKTS'lik lisans müfredatına sahiptir.

## Yarıyıllar
- [1. Yarıyıl (Güz)](file://{target_dir}/1_yariyil.md)
- [2. Yarıyıl (Bahar)](file://{target_dir}/2_yariyil.md)
- [3. Yarıyıl (Güz)](file://{target_dir}/3_yariyil.md)
- [4. Yarıyıl (Bahar)](file://{target_dir}/4_yariyil.md)
- [5. Yarıyıl (Güz)](file://{target_dir}/5_yariyil.md)
- [6. Yarıyıl (Bahar)](file://{target_dir}/6_yariyil.md)
- [7. Yarıyıl (Güz)](file://{target_dir}/7_yariyil.md)
- [8. Yarıyıl (Bahar)](file://{target_dir}/8_yariyil.md)
- [Önkoşul Zinciri](file://{target_dir}/onkosul_zinciri.md)
- [Seçmeli Ders Havuzları](file://{target_dir}/secimlik_ders_havuzlari.md)
"""
    with open(os.path.join(target_dir, "README.md"), 'w', encoding='utf-8') as f:
        f.write(bologna_readme)
    print(f"Completed Bologna {prog_title}")

def run():
    base_dir = "05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/kontrol_ve_otomasyon_muhendisligi"
    os.makedirs(base_dir, exist_ok=True)
    
    # 1. Build %30 English Bologna
    build_bologna_program(29, 18, os.path.join(base_dir, "bologna_ders_plani_yuzde30"), "Kontrol ve Otomasyon Müh. (%30 İngilizce)", "%30 İngilizce")
    
    # 2. Build %100 English Bologna
    build_bologna_program(403, 18, os.path.join(base_dir, "bologna_ders_plani_yuzde100"), "Kontrol ve Otomasyon Müh. (%100 İngilizce)", "%100 İngilizce")
    
    # 3. Build Core KOM files
    print("=== BUILDING CORE KOM DEPARTMENT FILES ===")
    
    # README.md
    with open(os.path.join(base_dir, "README.md"), 'w', encoding='utf-8') as f:
        f.write("""---
baslik: "YTÜ Kontrol ve Otomasyon Mühendisliği Bölümü Külliyatı"
kategori: "fakulteler_ve_bolumler"
bolum: "Kontrol ve Otomasyon Mühendisliği"
fakulte: "Elektrik-Elektronik Fakültesi"
web: "https://kom.yildiz.edu.tr/"
bologna_birim_id: 18
egitim_dili: "%30 İngilizce (ID: 29) & %100 İngilizce (ID: 403)"
akreditasyon: "MÜDEK (EUR-ACE)"
anahtar_kelimeler: ["kontrol ve otomasyon", "kom", "robotik", "plc", "scada", "omron", "schneider", "endüstriyel otomasyon"]
---

# YTÜ Kontrol ve Otomasyon Mühendisliği Bölümü

Yıldız Teknik Üniversitesi Kontrol ve Otomasyon Mühendisliği Bölümü, endüstriyel proseslerin modellenmesi, kontrol algoritmalarının tasarımı, robotik sistemler, otonom araçlar, mekatronik ve akıllı otomasyon sistemleri alanlarında Türkiye'nin lider bölümüdür.

Bölümde hem **%30 İngilizce** hem de **%100 İngilizce** olmak üzere iki ayrı örgün lisans programı yürütülmektedir.

---

## 🏛️ Anabilim Dalları
1. **Kontrol Sistemleri Anabilim Dalı:** Lineer ve lineer olmayan kontrol, adaptif kontrol, optimal kontrol, gürbüz (robust) kontrol.
2. **Otomasyon Anabilim Dalı:** Endüstriyel otomasyon, PLC/SCADA sistemleri, dağıtık kontrol sistemleri (DCS), endüstriyel haberleşme protokolleri.
3. **Robotik ve Mekatronik Anabilim Dalı:** Manipülatör robotiği, mobil ve otonom robotlar, sensör tümleşimi.

---

## 📚 Dokümantasyon Rehberi
- [Lisans Eğitim Yapısı (%30 ve %100 İngilizce)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/kontrol_ve_otomasyon_muhendisligi/lisans_egitim_yapisi.md): İki programın profilleri, MÜDEK çıktıları, eğitim hedefleri.
- [Staj, Tasarım ve Bitirme Esasları](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/kontrol_ve_otomasyon_muhendisligi/staj_ve_bitirme_esaslari.md): Genel ve Mesleki Staj, Staj Saydırma, Tasarım Projesi ve Bitirme Çalışması (DD-022, KOM9000 şablonları).
- [Laboratuvarlar ve Araştırma Altyapısı](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/kontrol_ve_otomasyon_muhendisligi/laboratuvarlar_ve_arastirma.md): Omron, Schneider Electric, Phoenix Contact Otomasyon Laboratuvarları ve Robotik altyapısı.
- [Komisyonlar ve Öğrenci Danışmanlığı](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/kontrol_ve_otomasyon_muhendisligi/komisyonlar_ve_ogrenci_danismanligi.md): Bölüm komisyonları ve akran danışmanı Emirhan Çelik.
- [Lisansüstü Programlar](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/kontrol_ve_otomasyon_muhendisligi/lisansustu_programlar.md): Tezli/Tezsiz YL ve Doktora programları.
- [Kontrol ve Otomasyon SSS](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/kontrol_ve_otomasyon_muhendisligi/sikca_sorulan_sorular.md): Sık sorulan sorular ve yanıtları.
- [Bologna Ders Planı (%30 İngilizce)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/kontrol_ve_otomasyon_muhendisligi/bologna_ders_plani_yuzde30/README.md)
- [Bologna Ders Planı (%100 İngilizce)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/kontrol_ve_otomasyon_muhendisligi/bologna_ders_plani_yuzde100/README.md)
""")
    print("Generated KOM README.md")

    # lisans_egitim_yapisi.md
    with open(os.path.join(base_dir, "lisans_egitim_yapisi.md"), 'w', encoding='utf-8') as f:
        f.write("""---
baslik: "YTÜ Kontrol ve Otomasyon Mühendisliği Lisans Eğitim Yapısı"
kategori: "fakulteler_ve_bolumler"
bolum: "Kontrol ve Otomasyon Mühendisliği"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bölüm & Bologna Portalı)"
kaynak: "https://kom.yildiz.edu.tr/"
---

# YTÜ Kontrol ve Otomasyon Mühendisliği Lisans Eğitim Yapısı

Bölümde iki ayrı örgün lisans programı bulunmaktadır:
1. **Kontrol ve Otomasyon Mühendisliği (%30 İngilizce - Bologna ID: 29):** 240 AKTS, Türkçe ve İngilizce karma eğitim.
2. **Kontrol ve Otomasyon Mühendisliği (%100 İngilizce - Bologna ID: 403):** 240 AKTS, tüm teknik ve mesleki derslerin İngilizce yürütüldüğü uluslararası program.

Her iki program da MÜDEK (EUR-ACE) akreditasyonuna sahiptir.

---

## 🎯 Program Eğitim Amaçları
1. Otomasyon, robotik, havacılık-uzay, savunma sanayii, enerji, otomotiv ve kimya endüstrisinde tasarım, kontrol ve Ar-Ge mühendisi olarak liderlik yapmak.
2. Ulusal ve uluslararası saygın üniversitelerde yüksek lisans ve doktora çalışmaları yürüterek bilime katkı sağlamak.
3. Otomasyon sistemleri ve akıllı üretim teknolojileri alanında girişimci olarak yenilikçi çözümler üretmek.
""")
    print("Generated KOM lisans_egitim_yapisi.md")

    # staj_ve_bitirme_esaslari.md
    with open(os.path.join(base_dir, "staj_ve_bitirme_esaslari.md"), 'w', encoding='utf-8') as f:
        f.write("""---
baslik: "YTÜ Kontrol ve Otomasyon Mühendisliği Staj ve Bitirme Esasları"
kategori: "fakulteler_ve_bolumler"
bolum: "Kontrol ve Otomasyon Mühendisliği"
guvenilirlik_duzeyi: "Tier 1 / Tier 2"
yasal_dayanak: "DD-022, YÖ-103"
kaynak: "https://kom.yildiz.edu.tr/staj"
---

# YTÜ Kontrol ve Otomasyon Mühendisliği Staj ve Bitirme Esasları

---

## 🛠️ 1. Staj Esasları (Toplam 60 İş Günü)
1. **Genel Staj (Staj 1 - 30 İş Günü):** Temel elektrik, elektronik, mekanik atölye, şantiye veya bakım-onarım birimlerinde yapılır.
2. **Mesleki Staj (Staj 2 - 30 İş Günü):** PLC/SCADA yazılımı, endüstriyel otomasyon hatları, robotik hücre entegrasyonu, proses kontrol veya Ar-Ge merkezlerinde yapılır.
3. **Staj Saydırma:** Başka yükseköğretim kurumlarından geçiş yapan öğrenciler veya fiilen sigortalı mühendislik işi yapanlar, Bölüm Staj Komisyonu'na dilekçe ile başvurarak staj saydırma talebinde bulunabilirler.

---

## 🎓 2. Tasarım ve Bitirme Çalışması (DD-022)
- **KOM4901 Tasarım Projesi (7. Yarıyıl):** 4 AKTS. Bir kontrol veya otomasyon sisteminin simülasyonu ve prototip tasarımı.
- **KOM4902 Bitirme Çalışması (8. Yarıyıl):** 6 AKTS. Tasarım projesini başarma önkoşulu vardır.
- **Tez Yazımı:** [KOM9000_Bitirme_Calismasi_Sablonu_TR.docx](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/arsiv/fakulteler/eef/kom/KOM9000_Bitirme_Calismasi_Sablonu_TR.docx) ve İngilizce şablonuna uygun olarak hazırlanır ve jüri önünde sözlü savunulur.
""")
    print("Generated KOM staj_ve_bitirme_esaslari.md")

    # laboratuvarlar_ve_arastirma.md
    with open(os.path.join(base_dir, "laboratuvarlar_ve_arastirma.md"), 'w', encoding='utf-8') as f:
        f.write("""---
baslik: "YTÜ Kontrol ve Otomasyon Mühendisliği Laboratuvarları"
kategori: "fakulteler_ve_bolumler"
bolum: "Kontrol ve Otomasyon Mühendisliği"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bölüm Portalı)"
kaynak: "https://kom.yildiz.edu.tr/"
---

# YTÜ Kontrol ve Otomasyon Mühendisliği Laboratuvarları

Bölümümüz, endüstriyel otomasyon liderlerinin kurduğu sponsorlu ve yüksek teknolojili laboratuvarlara sahiptir:

1. **Omron Otomasyon Laboratuvarı (`kom.yildiz.edu.tr/omron1`):** Omron PLC sistemleri, Sysmac Studio yazılım platformu, HMI operatör panelleri, servo sürücüler ve görüntü işleme (machine vision) sistemleri.
2. **Schneider Electric Otomasyon Laboratuvarı (`kom.yildiz.edu.tr/schneider`):** Modicon M serisi PLC'ler, EcoStruxure yazılımı, endüstriyel haberleşme ve proses kontrol setleri.
3. **Phoenix Contact Otomasyon Laboratuvarı (`kom.yildiz.edu.tr/phoenix`):** PLCnext teknolojisi, açık kaynaklı endüstriyel otomasyon, endüstriyel Ethernet ve güvenlik röleleri.
4. **Elektronik ve Temel Kontrol Laboratuvarı:** Analog/dijital PID kontrolör deney setleri, servo motor pozisyon ve hız kontrol düzenekleri, ters sarkaç ve manyetik askılama (maglev) test kitleri.
5. **Robotik Araştırma Laboratuvarı:** Çok eksenli endüstriyel robot kolları (KUKA/ABB), mobil robot platformları, ROS (Robot Operating System) iş istasyonları.
""")
    print("Generated KOM laboratuvarlar_ve_arastirma.md")

    # komisyonlar_ve_ogrenci_danismanligi.md
    with open(os.path.join(base_dir, "komisyonlar_ve_ogrenci_danismanligi.md"), 'w', encoding='utf-8') as f:
        f.write("""---
baslik: "YTÜ Kontrol ve Otomasyon Mühendisliği Komisyonlar ve Öğrenci Danışmanlığı"
kategori: "fakulteler_ve_bolumler"
bolum: "Kontrol ve Otomasyon Mühendisliği"
guvenilirlik_duzeyi: "Tier 2"
kaynak: "https://kom.yildiz.edu.tr/komisyonlar"
---

# YTÜ Kontrol ve Otomasyon Mühendisliği Komisyonlar

- **Staj Komisyonu:** Staj yerlerinin uygunluk onayı ve defter incelemeleri.
- **İntibak ve Muafiyet Komisyonu:** Yatay geçiş, DGS ve ÇAP intibak kararları.
- **Tasarım ve Bitirme Komisyonu:** KOM4901 ve KOM4902 jüri organizasyonu.
- **MÜDEK Komisyonu:** Sürekli iyileştirme ve eğitim çıktıları ölçümü.
- **Akran Danışmanı:** Emirhan ÇELİK (`emirhan.celik@std.yildiz.edu.tr`)
""")
    print("Generated KOM komisyonlar_ve_ogrenci_danismanligi.md")

    # lisansustu_programlar.md
    with open(os.path.join(base_dir, "lisansustu_programlar.md"), 'w', encoding='utf-8') as f:
        f.write("""---
baslik: "YTÜ Kontrol ve Otomasyon Mühendisliği Lisansüstü Programlar"
kategori: "fakulteler_ve_bolumler"
bolum: "Kontrol ve Otomasyon Mühendisliği"
guvenilirlik_duzeyi: "Tier 2"
kaynak: "http://www.fbe.yildiz.edu.tr/"
---

# YTÜ Kontrol ve Otomasyon Mühendisliği Lisansüstü Programlar

Fen Bilimleri Enstitüsü (FBE) bünyesinde yürütülen lisansüstü programlar:

| Program Adı | Tür | Bologna ID | Eğitim Dili |
| :--- | :--- | :---: | :--- |
| **Kontrol ve Otomasyon Mühendisliği YL Programı** | Tezli YL | 265 | Türkçe |
| **Kontrol ve Otomasyon Mühendisliği YL (Tezsiz)** | Tezsiz YL | 374 | Türkçe |
| **Kontrol ve Otomasyon YL (Tezsiz, İ.Ö. İngilizce)** | Tezsiz YL | 375 | İngilizce |
| **Kontrol ve Otomasyon YL (Tezsiz, İ.Ö. Türkçe)** | Tezsiz YL | 318 | Türkçe |
| **Kontrol ve Otomasyon Mühendisliği Doktora Programı** | Doktora | 266 | Türkçe |
""")
    print("Generated KOM lisansustu_programlar.md")

    # sikca_sorulan_sorular.md
    with open(os.path.join(base_dir, "sikca_sorulan_sorular.md"), 'w', encoding='utf-8') as f:
        f.write("""---
baslik: "YTÜ Kontrol ve Otomasyon Mühendisliği SSS"
kategori: "fakulteler_ve_bolumler"
bolum: "Kontrol ve Otomasyon Mühendisliği"
guvenilirlik_duzeyi: "Tier 2"
kaynak: "https://kom.yildiz.edu.tr/"
---

# YTÜ Kontrol ve Otomasyon Mühendisliği Sıkça Sorulan Sorular

### S1: %30 ve %100 İngilizce programları arasında geçiş yapılabilir mi?
> **Cevap:** Evet, YTÜ Kurumiçi Yatay Geçiş Yönergesi (YÖ-098) uyarınca başarı şartı (AGNO) veya ÖSYM taban puanı (Ek Madde-1) ile kontenjan dahilinde geçiş yapılabilir. %100 İngilizce programa geçiş için yabancı dil şartı sağlanmalıdır.

### S2: Staj süresi kaç gündür ve nerelerde yapılabilir?
> **Cevap:** Toplam 60 iş günüdür (30 gün Genel + 30 gün Mesleki). Otomotiv, savunma, robotik, endüstriyel otomasyon (PLC/SCADA), beyaz eşya ve fabrika otomasyon sistemleri geliştiren kurumlarda yapılabilir.

### S3: Bitirme Çalışması (KOM4902) önkoşulu nedir?
> **Cevap:** KOM4901 Tasarım Projesi dersinin başarılmış olması zorunlu önkoşuldur.

### S4: Hangi endüstriyel otomasyon laboratuvarları bulunmaktadır?
> **Cevap:** Omron Otomasyon Laboratuvarı, Schneider Electric Otomasyon Laboratuvarı ve Phoenix Contact Otomasyon Laboratuvarı doğrudan endüstriyel donanımlarla kurulmuştur.
""")
    print("Generated KOM sikca_sorulan_sorular.md")

if __name__ == '__main__':
    run()
