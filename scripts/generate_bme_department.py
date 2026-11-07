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

def run():
    print("=== FETCHING BME BOLOGNA CURRICULUM ===")
    bologna_url = 'http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=504&aid=151'
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
                
    base_dir = "05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/biyomedikal_muhendisligi"
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
baslik: "Biyomedikal Mühendisliği (%100 İngilizce) - {sem_title} Ders Planı"
kategori: "fakulteler_ve_bolumler"
bolum: "Biyomedikal Mühendisliği"
yariyil: {sem_num}
toplam_akts: {total_ects}
toplam_kredi: {total_credit}
kaynak: "{bologna_url}"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"
---

# Biyomedikal Mühendisliği (%100 İngilizce) - {sem_title}

Bu belgede, YTÜ Biyomedikal Mühendisliği Lisans Programı'nın ({sem_title}) dersleri, kredileri, AKTS değerleri, haftalık saatleri ve önkoşul koşulları listelenmektedir.

> [!NOTE] Yarıyıl Özeti
> - **Dönem:** {sem_title} (%100 İngilizce)
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
baslik: "Biyomedikal Mühendisliği Önkoşul Zinciri ve Bağımlılık Haritası"
kategori: "fakulteler_ve_bolumler"
bolum: "Biyomedikal Mühendisliği"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"
kaynak: "{bologna_url}"
---

# Biyomedikal Mühendisliği Lisans Programı Önkoşul Zinciri

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
    BME2111["BME2111 Circuits in Biomedical Eng."] --> BME3111["BME3111 Biomedical Electronics"]
    BME3111 --> BME3211["BME3211 Biomedical Instrumentation"]
    BME3211 --> BME4111["BME4111 Medical Imaging Systems"]
    BME4901["BME4901 Multidisciplinary Design Project"] --> BME4902["BME4902 Graduation Thesis"]
```
"""
    with open(os.path.join(bologna_dir, "onkosul_zinciri.md"), 'w', encoding='utf-8') as f:
        f.write(onkosul_md)

    # secimlik_ders_havuzlari.md
    secimli_md = f"""---
baslik: "Biyomedikal Mühendisliği Seçmeli Ders Havuzları"
kategori: "fakulteler_ve_bolumler"
bolum: "Biyomedikal Mühendisliği"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"
kaynak: "{bologna_url}"
---

# Biyomedikal Mühendisliği Seçmeli Ders Havuzları

---
"""
    for sec_name, courses in curriculum.items():
        if 'Seçmeli' in sec_name or 'Seçim' in sec_name:
            secimli_md += f"\n## 📚 {sec_name} ({len(courses)} Ders)\n\n"
            secimli_md += "| Kodu | Ders Adı | T | U | L | Kredi | AKTS |\n| :--- | :--- | :---: | :---: | :---: | :---: | :---: |\n"
            for c in courses[:20]:
                secimli_md += f"| **{c['code']}** | [{c['name']}]({c['link']}) | {c['lec']} | {c['app']} | {c['lab']} | {c['credit']} | **{c['ects']}** |\n"

    with open(os.path.join(bologna_dir, "secimlik_ders_havuzlari.md"), 'w', encoding='utf-8') as f:
        f.write(secimli_md)

    # README.md (bologna)
    bologna_readme = f"""---
baslik: "Biyomedikal Mühendisliği Bologna Ders Planı Master İndeksi"
kategori: "fakulteler_ve_bolumler"
bolum: "Biyomedikal Mühendisliği"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"
---

# Biyomedikal Mühendisliği (%100 İngilizce) Bologna Ders Planı

Bologna Program ID: 504, 8 yarıyıl ve 240 AKTS'lik lisans müfredatına sahiptir.

## Yarıyıllar
- [1. Yarıyıl (Güz)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/biyomedikal_muhendisligi/bologna_ders_plani/1_yariyil.md)
- [2. Yarıyıl (Bahar)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/biyomedikal_muhendisligi/bologna_ders_plani/2_yariyil.md)
- [3. Yarıyıl (Güz)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/biyomedikal_muhendisligi/bologna_ders_plani/3_yariyil.md)
- [4. Yarıyıl (Bahar)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/biyomedikal_muhendisligi/bologna_ders_plani/4_yariyil.md)
- [5. Yarıyıl (Güz)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/biyomedikal_muhendisligi/bologna_ders_plani/5_yariyil.md)
- [6. Yarıyıl (Bahar)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/biyomedikal_muhendisligi/bologna_ders_plani/6_yariyil.md)
- [7. Yarıyıl (Güz)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/biyomedikal_muhendisligi/bologna_ders_plani/7_yariyil.md)
- [8. Yarıyıl (Bahar)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/biyomedikal_muhendisligi/bologna_ders_plani/8_yariyil.md)
- [Önkoşul Zinciri](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/biyomedikal_muhendisligi/bologna_ders_plani/onkosul_zinciri.md)
- [Seçmeli Ders Havuzları](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/biyomedikal_muhendisligi/bologna_ders_plani/secimlik_ders_havuzlari.md)
"""
    with open(os.path.join(bologna_dir, "README.md"), 'w', encoding='utf-8') as f:
        f.write(bologna_readme)
    print("Generated BME bologna_ders_plani/README.md")

    # Core BME department files
    print("=== BUILDING CORE BME DEPARTMENT FILES ===")
    
    # README.md
    with open(os.path.join(base_dir, "README.md"), 'w', encoding='utf-8') as f:
        f.write("""---
baslik: "YTÜ Biyomedikal Mühendisliği Bölümü Külliyatı"
kategori: "fakulteler_ve_bolumler"
bolum: "Biyomedikal Mühendisliği"
fakulte: "Elektrik-Elektronik Fakültesi"
web: "https://bme.yildiz.edu.tr/"
bologna_program_id: 504
bologna_birim_id: 151
egitim_dili: "%100 İngilizce"
akreditasyon: "MÜDEK"
anahtar_kelimeler: ["biyomedikal mühendisliği", "bme", "tıbbi cihaz", "biyomedikal enstrümantasyon", "hastane stajı", "çdtp"]
---

# YTÜ Biyomedikal Mühendisliği Bölümü

Yıldız Teknik Üniversitesi Biyomedikal Mühendisliği Bölümü, tıp ve mühendislik disiplinlerinin kesişim noktasında, sağlık sektörünün ihtiyaç duyduğu tıbbi cihaz, biyomalzeme, biyomedikal görüntüleme ve biyoinformatik teknolojilerini geliştirmek üzere kurulmuş öncü bir akademik birimdir.

Eğitim dili **%100 İngilizce**dir.

---

## 🏛️ Anabilim Dalları
1. **Biyoelektronik ve Biyomedikal Enstrümantasyon:** Biyopotansiyel yükselteçler, EKG/EEG/EMG cihazları, tıbbi sensörler.
2. **Medikal Görüntüleme ve Sinyal İşleme:** MR, BT, Ultrasonografi sinyal ve görüntü işleme algoritmaları.
3. **Biyomekanik ve Biyomalzemeler:** Protez/ortez biyomekaniği, doku mühendisliği, yapay organlar.
4. **Klinik Mühendisliği:** Hastane teknolojisi yönetimi, medikal kalibrasyon ve tıbbi cihaz standartları.

---

## 📚 Dokümantasyon Rehberi
- [Lisans Eğitim Yapısı (%100 İngilizce)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/biyomedikal_muhendisligi/lisans_egitim_yapisi.md): %100 İngilizce program profili, program çıktıları ve eğitim hedefleri.
- [Staj ve ÇDTP / Bitirme Esasları](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/biyomedikal_muhendisligi/staj_ve_cdtp_esaslari.md): Hastane/Klinik ve Endüstri stajları, Çok Disiplinli Tasarım Projesi (ÇDTP) süreçleri ve Bitirme Tezi.
- [Laboratuvarlar ve Araştırma Altyapısı](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/biyomedikal_muhendisligi/laboratuvarlar_ve_arastirma.md): Biyomedikal laboratuvarları, donanımları ve araştırma alanları.
- [Komisyonlar ve Öğrenci Danışmanlığı](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/biyomedikal_muhendisligi/komisyonlar_ve_ogrenci_danismanligi.md): Bölüm komisyonları ve danışmanlık.
- [Lisansüstü Programlar](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/biyomedikal_muhendisligi/lisansustu_programlar.md): Biyomedikal Mühendisliği Tezli YL (Bologna ID: 542).
- [Biyomedikal Mühendisliği SSS](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/biyomedikal_muhendisligi/sikca_sorulan_sorular.md): Bölüm ve staj SSS tam metni.
- [Bologna Ders Planı (1-8. Yarıyıllar)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/biyomedikal_muhendisligi/bologna_ders_plani/README.md): 8 yarıyılın BME kodlu dersleri ve önkoşulları.
""")
    print("Generated BME README.md")

    # lisans_egitim_yapisi.md
    with open(os.path.join(base_dir, "lisans_egitim_yapisi.md"), 'w', encoding='utf-8') as f:
        f.write("""---
baslik: "YTÜ Biyomedikal Mühendisliği Lisans Eğitim Yapısı"
kategori: "fakulteler_ve_bolumler"
bolum: "Biyomedikal Mühendisliği"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Portalı)"
kaynak: "https://bme.yildiz.edu.tr/"
---

# YTÜ Biyomedikal Mühendisliği Lisans Eğitim Yapısı

YTÜ Biyomedikal Mühendisliği Lisans Programı (%100 İngilizce, Bologna ID: 504), 8 yarıyıl ve 240 AKTS kredisinden oluşmaktadır. Derslerin tamamı İngilizce olarak yürütülür.

---

## 🎯 Program Eğitim Amaçları
1. Medikal cihaz üreticilerinde, hastanelerin biyomedikal/klinik mühendislik departmanlarında, ilaç ve biyoteknoloji şirketlerinde AR-GE, tasarım, kalite kontrol ve satış-pazarlama mühendisi olarak istihdam edilmek.
2. Sağlık teknolojileri ve biyomedikal alanında ulusal/uluslararası üniversitelerde lisansüstü eğitim almak ve akademik araştırmalar yapmak.
3. Sağlık sektöründe yenilikçi tıbbi tanı ve tedavi cihazları geliştiren biyomedikal girişimler kurmak.
""")
    print("Generated BME lisans_egitim_yapisi.md")

    # staj_ve_cdtp_esaslari.md
    with open(os.path.join(base_dir, "staj_ve_cdtp_esaslari.md"), 'w', encoding='utf-8') as f:
        f.write("""---
baslik: "YTÜ Biyomedikal Mühendisliği Staj, ÇDTP ve Bitirme Esasları"
kategori: "fakulteler_ve_bolumler"
bolum: "Biyomedikal Mühendisliği"
guvenilirlik_duzeyi: "Tier 1 / Tier 2"
kaynak: "https://bme.yildiz.edu.tr/staj"
---

# YTÜ Biyomedikal Mühendisliği Staj ve Proje Esasları

---

## 🛠️ 1. Staj Esasları (Toplam 60 İş Günü)
Biyomedikal Mühendisliği'nde iki aşamalı zorunlu staj uygulanır:
1. **Staj 1 (Hastane / Klinik Mühendisliği Stajı - 30 İş Günü):** Tam teşekküllü üniversite hastaneleri, şehir hastaneleri veya kamu/özel hastanelerin Biyomedikal / Klinik Mühendislik birimlerinde yapılır. Tıbbi cihazların kalibrasyonu, bakımı, arıza tespiti ve klinik ortamdaki işleyişi yerinde incelenir.
2. **Staj 2 (Endüstri / AR-GE Stajı - 30 İş Günü):** Tıbbi cihaz üreten, ithal eden veya AR-GE faaliyeti yürüten biyomedikal firmalarında, kalibrasyon laboratuvarlarında yapılır.

---

## 🔬 2. Çok Disiplinli Tasarım Projesi (ÇDTP / BME4901)
- Fakültenin diğer bölümleriyle (Elektrik, Bilgisayar, Elektronik, Kontrol) disiplinlerarası takımlar oluşturularak gerçek bir sağlık/mühendislik probleminin çözülmesine yönelik prototip geliştirilir.
- FR-1558 Yönetim Planı Formatı ve resmi ÇDTP takvimine göre yürütülür.

---

## 🎓 3. Bitirme Tezi (BME4902)
- [BME_Graduation_Thesis_Template.docx](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/arsiv/fakulteler/eef/bme/BME_Graduation_Thesis_Template.docx) şablonuna uygun olarak tamamen İngilizce yazılır ve jüri önünde sözlü savunulur.
""")
    print("Generated BME staj_ve_cdtp_esaslari.md")

    # laboratuvarlar_ve_arastirma.md
    with open(os.path.join(base_dir, "laboratuvarlar_ve_arastirma.md"), 'w', encoding='utf-8') as f:
        f.write("""---
baslik: "YTÜ Biyomedikal Mühendisliği Laboratuvarları"
kategori: "fakulteler_ve_bolumler"
bolum: "Biyomedikal Mühendisliği"
guvenilirlik_duzeyi: "Tier 2"
kaynak: "https://bme.yildiz.edu.tr/"
---

# YTÜ Biyomedikal Mühendisliği Laboratuvarları

1. **Biyomedikal Enstrümantasyon Laboratuvarı:** Biyopotansiyel elektrotlar, EKG/EMG sinyal amplifikatörleri, dijital filtre test düzenekleri.
2. **Biyomalzeme ve Biyomekanik Laboratuvarı:** Mekanik çekme-basma test cihazları, doku iskelesi üretim setleri, biyouyumluluk test altyapısı.
3. **Medikal Görüntüleme ve Sinyal İşleme Laboratuvarı:** Ultrasonik dönüştürücüler, fantom test setleri, medikal görüntü analizi iş istasyonları.
4. **Biyosensör Araştırma Laboratuvarı:** Elektrokimyasal ve optik biyosensör geliştirme, mikroakışkan sistemler.
""")
    print("Generated BME laboratuvarlar_ve_arastirma.md")

    # komisyonlar_ve_ogrenci_danismanligi.md
    with open(os.path.join(base_dir, "komisyonlar_ve_ogrenci_danismanligi.md"), 'w', encoding='utf-8') as f:
        f.write("""---
baslik: "YTÜ Biyomedikal Mühendisliği Komisyonlar"
kategori: "fakulteler_ve_bolumler"
bolum: "Biyomedikal Mühendisliği"
guvenilirlik_duzeyi: "Tier 2"
---

# YTÜ Biyomedikal Mühendisliği Komisyonlar

- **Staj Komisyonu:** Hastane ve endüstri staj yerlerinin onaylanması, defter mülakatları.
- **İntibak ve Muafiyet Komisyonu:** Yatay geçiş ve ÇAP intibakları.
- **ÇDTP ve Bitirme Komisyonu:** Disiplinlerarası proje takımları ve tez jürileri.
- **Bölüm Akran Koordinatörlüğü:** Yeni kayıt yaptıran öğrencilerin oryantasyonu.
""")
    print("Generated BME komisyonlar_ve_ogrenci_danismanligi.md")

    # lisansustu_programlar.md
    with open(os.path.join(base_dir, "lisansustu_programlar.md"), 'w', encoding='utf-8') as f:
        f.write("""---
baslik: "YTÜ Biyomedikal Mühendisliği Lisansüstü Programlar"
kategori: "fakulteler_ve_bolumler"
bolum: "Biyomedikal Mühendisliği"
guvenilirlik_duzeyi: "Tier 2"
kaynak: "http://www.fbe.yildiz.edu.tr/"
---

# YTÜ Biyomedikal Mühendisliği Lisansüstü Programlar

| Program Adı | Tür | Bologna ID | Eğitim Dili |
| :--- | :--- | :---: | :--- |
| **Biyomedikal Mühendisliği Tezli Yüksek Lisans Programı** | Tezli YL | 542 | İngilizce |

Fen Bilimleri Enstitüsü (FBE) aracılığıyla başvurular kabul edilir. Sayısal ALES >= 70 ve İngilizce Yabancı Dil >= 60 şartı aranır.
""")
    print("Generated BME lisansustu_programlar.md")

    # sikca_sorulan_sorular.md
    with open(os.path.join(base_dir, "sikca_sorulan_sorular.md"), 'w', encoding='utf-8') as f:
        f.write("""---
baslik: "YTÜ Biyomedikal Mühendisliği Sıkça Sorulan Sorular"
kategori: "fakulteler_ve_bolumler"
bolum: "Biyomedikal Mühendisliği"
guvenilirlik_duzeyi: "Tier 2"
orijinal_dosya: "arsiv/fakulteler/eef/bme/BME_Staj_SSS.pdf"
---

# YTÜ Biyomedikal Mühendisliği Sıkça Sorulan Sorular

### S1: Biyomedikal Mühendisliği stajı nerelerde yapılmalıdır?
> **Cevap:** Toplam 60 gündür. En az 30 günü tam teşekküllü bir hastanenin Biyomedikal/Klinik Mühendislik biriminde, kalan 30 günü ise tıbbi cihaz üreten/ithal eden veya AR-GE yapan özel bir biyomedikal kuruluşunda yapılmalıdır.

### S2: Eğitim dili tamamen İngilizce midir?
> **Cevap:** Evet, Biyomedikal Mühendisliği programı %100 İngilizce olarak yürütülmektedir. Tüm dersler, sınavlar, projeler ve bitirme tezi İngilizce sunulur.

### S3: Çok Disiplinli Tasarım Projesi (ÇDTP) nedir?
> **Cevap:** BME öğrencilerinin EEF'nin diğer bölümleriyle (Bilgisayar, Elektrik, Elektronik, Kontrol) bir araya gelerek medikal ve teknolojik bir problemi ortak tasarımla çözdüğü zorunlu projedir.
""")
    print("Generated BME sikca_sorulan_sorular.md")

if __name__ == '__main__':
    run()
