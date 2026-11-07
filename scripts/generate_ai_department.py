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
    print("=== FETCHING AI BOLOGNA CURRICULUM ===")
    bologna_url = 'http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=557&aid=181'
    soup = get_soup(bologna_url)
    
    t2 = None
    for t in soup.find_all('table'):
        if '1.Yıl' in t.get_text() and 'Güz Yarıyılı' in t.get_text():
            t2 = t
            break
    if not t2:
        t2 = soup.find_all('table')[1]
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
                
    base_dir = "05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/yapay_zeka_ve_veri_muhendisligi"
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
baslik: "Yapay Zeka ve Veri Mühendisliği (%100 İngilizce) - {sem_title} Ders Planı"
kategori: "fakulteler_ve_bolumler"
bolum: "Yapay Zeka ve Veri Mühendisliği"
yariyil: {sem_num}
toplam_akts: {total_ects}
toplam_kredi: {total_credit}
kaynak: "{bologna_url}"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"
---

# Yapay Zeka ve Veri Mühendisliği (%100 İngilizce) - {sem_title}

Bu belgede, YTÜ Yapay Zeka ve Veri Mühendisliği Lisans Programı'nın ({sem_title}) dersleri, kredileri, AKTS değerleri, haftalık saatleri ve önkoşul koşulları listelenmektedir.

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
baslik: "Yapay Zeka ve Veri Mühendisliği Önkoşul Zinciri ve Bağımlılık Haritası"
kategori: "fakulteler_ve_bolumler"
bolum: "Yapay Zeka ve Veri Mühendisliği"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"
kaynak: "{bologna_url}"
---

# Yapay Zeka ve Veri Mühendisliği Lisans Programı Önkoşul Zinciri

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
    YZM1021["YZM1021 Introduction to Programming"] --> YZM1022["YZM1022 Object Oriented Programming"]
    YZM1022 --> YZM2031["YZM2031 Data Structures and Algorithms"]
    YZM2031 --> YZM3011["YZM3011 Machine Learning"]
    YZM3011 --> YZM3022["YZM3022 Deep Learning"]
    YZM3011 --> YZM4011["YZM4011 Natural Language Processing"]
    YZM4901["YZM4901 Engineering Design Project"] --> YZM4902["YZM4902 Graduation Thesis"]
```
"""
    with open(os.path.join(bologna_dir, "onkosul_zinciri.md"), 'w', encoding='utf-8') as f:
        f.write(onkosul_md)

    # secimlik_ders_havuzlari.md
    secimli_md = f"""---
baslik: "Yapay Zeka ve Veri Mühendisliği Seçmeli Ders Havuzları"
kategori: "fakulteler_ve_bolumler"
bolum: "Yapay Zeka ve Veri Mühendisliği"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"
kaynak: "{bologna_url}"
---

# Yapay Zeka ve Veri Mühendisliği Seçmeli Ders Havuzları

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

    # bologna README.md
    bologna_readme = f"""---
baslik: "Yapay Zeka ve Veri Mühendisliği Bologna Ders Planı Master İndeksi"
kategori: "fakulteler_ve_bolumler"
bolum: "Yapay Zeka ve Veri Mühendisliği"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"
---

# Yapay Zeka ve Veri Mühendisliği (%100 İngilizce) Bologna Ders Planı

Bologna Program ID: 557, 8 yarıyıl ve 240 AKTS'lik lisans müfredatına sahiptir.

## Yarıyıllar
- [1. Yarıyıl (Güz)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/yapay_zeka_ve_veri_muhendisligi/bologna_ders_plani/1_yariyil.md)
- [2. Yarıyıl (Bahar)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/yapay_zeka_ve_veri_muhendisligi/bologna_ders_plani/2_yariyil.md)
- [3. Yarıyıl (Güz)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/yapay_zeka_ve_veri_muhendisligi/bologna_ders_plani/3_yariyil.md)
- [4. Yarıyıl (Bahar)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/yapay_zeka_ve_veri_muhendisligi/bologna_ders_plani/4_yariyil.md)
- [5. Yarıyıl (Güz)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/yapay_zeka_ve_veri_muhendisligi/bologna_ders_plani/5_yariyil.md)
- [6. Yarıyıl (Bahar)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/yapay_zeka_ve_veri_muhendisligi/bologna_ders_plani/6_yariyil.md)
- [7. Yarıyıl (Güz)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/yapay_zeka_ve_veri_muhendisligi/bologna_ders_plani/7_yariyil.md)
- [8. Yarıyıl (Bahar)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/yapay_zeka_ve_veri_muhendisligi/bologna_ders_plani/8_yariyil.md)
- [Önkoşul Zinciri](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/yapay_zeka_ve_veri_muhendisligi/bologna_ders_plani/onkosul_zinciri.md)
- [Seçmeli Ders Havuzları](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/yapay_zeka_ve_veri_muhendisligi/bologna_ders_plani/secimlik_ders_havuzlari.md)
"""
    with open(os.path.join(bologna_dir, "README.md"), 'w', encoding='utf-8') as f:
        f.write(bologna_readme)
    print("Generated AI bologna_ders_plani/README.md")

    # Core AI files
    print("=== BUILDING CORE AI DEPARTMENT FILES ===")
    
    # README.md
    with open(os.path.join(base_dir, "README.md"), 'w', encoding='utf-8') as f:
        f.write("""---
baslik: "YTÜ Yapay Zeka ve Veri Mühendisliği Bölümü Külliyatı"
kategori: "fakulteler_ve_bolumler"
bolum: "Yapay Zeka ve Veri Mühendisliği"
fakulte: "Elektrik-Elektronik Fakültesi"
web: "https://ai.yildiz.edu.tr/"
bologna_program_id: 557
bologna_birim_id: 181
egitim_dili: "%100 İngilizce"
anahtar_kelimeler: ["yapay zeka mühendisliği", "veri mühendisliği", "ai", "yzm", "makine öğrenmesi", "derin öğrenme", "büyük veri"]
---

# YTÜ Yapay Zeka ve Veri Mühendisliği Bölümü

Yıldız Teknik Üniversitesi Yapay Zeka ve Veri Mühendisliği Bölümü, yapay zeka, makine öğrenmesi, derin öğrenme, büyük veri analitiği, doğal dil işleme ve otonom sistemler alanlarında dünya standartlarında uzmanlar yetiştirmek üzere kurulmuş Türkiye'nin öncü ve en yüksek puanlı mühendislik programlarından biridir.

Program dili **%100 İngilizce**dir.

---

## 🏛️ Akademik Odak Alanları
1. **Makine Öğrenmesi ve Derin Öğrenme:** Denetimli/denetimsiz öğrenme, takviyeli öğrenme (reinforcement learning), üretken yapay zeka (GenAI).
2. **Doğal Dil İşleme (NLP) ve LLM:** Büyük dil modelleri, metin madenciliği, konuşma tanıma.
3. **Bilgisayarla Görü (Computer Vision):** Görüntü işleme, video analitiği, nesne algılama.
4. **Büyük Veri Mimarileri ve Veri Mühendisliği:** Dağıtık veri tabanları, veri ambarları, akış verisi işleme (Kafka/Spark).

---

## 📚 Dokümantasyon Rehberi
- [Lisans Eğitim Yapısı (%100 İngilizce)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/yapay_zeka_ve_veri_muhendisligi/lisans_egitim_yapisi.md): %100 İngilizce program yapısı, programlar arası geçiş ve eğitim çıktıları.
- [Staj, Laboratuvar ve Formlar](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/yapay_zeka_ve_veri_muhendisligi/staj_ve_formlar.md): Staj yönergeleri, YZM laboratuvar dersleri ve bitirme esasları.
- [Laboratuvarlar ve Araştırma Altyapısı](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/yapay_zeka_ve_veri_muhendisligi/laboratuvarlar_ve_arastirma.md): GPU kümeleri, yüksek başarımlı hesaplama ve veri laboratuvarları.
- [Komisyonlar ve Öğrenci Danışmanlığı](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/yapay_zeka_ve_veri_muhendisligi/komisyonlar_ve_ogrenci_danismanligi.md): Bölüm komisyonları ve danışmanlık.
- [Lisansüstü Programlar](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/yapay_zeka_ve_veri_muhendisligi/lisansustu_programlar.md): Tezli YL Programı (Bologna ID: 562).
- [Yapay Zeka ve Veri Mühendisliği SSS](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/yapay_zeka_ve_veri_muhendisligi/sikca_sorulan_sorular.md): Sık sorulan sorular ve yanıtları.
- [Bologna Lisans Ders Planı (1-8. Yarıyıllar)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/yapay_zeka_ve_veri_muhendisligi/bologna_ders_plani/README.md): 8 yarıyılın YZM kodlu dersleri, önkoşulları ve seçmelileri.
""")
    print("Generated AI README.md")

    # lisans_egitim_yapisi.md
    with open(os.path.join(base_dir, "lisans_egitim_yapisi.md"), 'w', encoding='utf-8') as f:
        f.write("""---
baslik: "YTÜ Yapay Zeka ve Veri Mühendisliği Lisans Eğitim Yapısı"
kategori: "fakulteler_ve_bolumler"
bolum: "Yapay Zeka ve Veri Mühendisliği"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bölüm & Bologna Portalı)"
kaynak: "https://ai.yildiz.edu.tr/"
---

# YTÜ Yapay Zeka ve Veri Mühendisliği Lisans Eğitim Yapısı

Program, %100 İngilizce (Bologna ID: 557) lisans eğitimi vermektedir. Toplam 240 AKTS'den oluşan müfredat; ileri matematik, istatistik, algoritma analizi, büyük veri mimarileri ve modern yapay zeka modelleri üzerine kuruludur.

---

## 🎯 Program Eğitim Amaçları
1. Ulusal ve küresel teknoloji şirketlerinde Yapay Zeka Mühendisi, Veri Mühendisi, Makine Öğrenmesi Mühendisi veya Veri Bilimci olarak görev almak.
2. Dünya çapında saygın üniversitelerde doktora ve akademik araştırmalar yürüterek yapay zeka bilimine öncülük etmek.
3. Kendi yapay zeka odaklı derin teknoloji (deep-tech) girişimlerini kurmak.
""")
    print("Generated AI lisans_egitim_yapisi.md")

    # staj_ve_formlar.md
    with open(os.path.join(base_dir, "staj_ve_formlar.md"), 'w', encoding='utf-8') as f:
        f.write("""---
baslik: "YTÜ Yapay Zeka ve Veri Mühendisliği Staj ve Proje Esasları"
kategori: "fakulteler_ve_bolumler"
bolum: "Yapay Zeka ve Veri Mühendisliği"
guvenilirlik_duzeyi: "Tier 1 / Tier 2"
orijinal_dosya: "arsiv/fakulteler/eef/ai/AI_EEF_Staj_Uygulama_Ilkeleri.pdf"
kaynak: "https://ai.yildiz.edu.tr/"
---

# YTÜ Yapay Zeka ve Veri Mühendisliği Staj ve Proje Esasları

---

## 🛠️ 1. Staj Esasları (Toplam 60 İş Günü)
- **Staj 1 (Yazılım ve Veri Altyapısı - 30 İş Günü):** Veri tabanı yönetimi, veri hatları (data pipelines), yazılım geliştirme.
- **Staj 2 (Yapay Zeka ve Veri Bilimi - 30 İş Günü):** Makine öğrenmesi modelleri geliştirme, derin öğrenme, büyük veri analitiği, AR-GE departmanlarında algoritmik geliştirme.

---

## 🎓 2. Proje Kademeleri
- **YZM4901 Mühendislik Tasarımı:** Karmaşık bir yapay zeka mimarisinin projelendirilmesi ve veri setinin modellenmesi.
- **YZM4902 Bitirme Tezi:** İngilizce olarak hazırlanan, canlı model demosu içeren ve akademik jüriye sunulan tez çalışması.
""")
    print("Generated AI staj_ve_formlar.md")

    # laboratuvarlar_ve_arastirma.md
    with open(os.path.join(base_dir, "laboratuvarlar_ve_arastirma.md"), 'w', encoding='utf-8') as f:
        f.write("""---
baslik: "YTÜ Yapay Zeka ve Veri Mühendisliği Laboratuvarları"
kategori: "fakulteler_ve_bolumler"
bolum: "Yapay Zeka ve Veri Mühendisliği"
guvenilirlik_duzeyi: "Tier 2"
kaynak: "https://ai.yildiz.edu.tr/"
---

# YTÜ Yapay Zeka ve Veri Mühendisliği Laboratuvarları

1. **Yapay Zeka ve Derin Öğrenme Hesaplama Kümesi:** Çoklu NVIDIA GPU hızlandırıcılı sunucular, PyTorch ve TensorFlow dağıtık eğitim altyapısı.
2. **Büyük Veri Laboratuvarı:** Hadoop, Apache Spark, Kafka veri akış simülasyonları ve büyük veri işleme iş istasyonları.
3. **Veri Mühendisliği Laboratuvarı (YZM1021 ve YZM2031 Uygulamaları):** Lisans öğrencilerinin programlama, veri yapıları ve algoritmik tasarım deneylerini gerçekleştirdiği bilgisayar laboratuvarları.
""")
    print("Generated AI laboratuvarlar_ve_arastirma.md")

    # komisyonlar_ve_ogrenci_danismanligi.md
    with open(os.path.join(base_dir, "komisyonlar_ve_ogrenci_danismanligi.md"), 'w', encoding='utf-8') as f:
        f.write("""---
baslik: "YTÜ Yapay Zeka ve Veri Mühendisliği Komisyonlar"
kategori: "fakulteler_ve_bolumler"
bolum: "Yapay Zeka ve Veri Mühendisliği"
guvenilirlik_duzeyi: "Tier 2"
kaynak: "https://ai.yildiz.edu.tr/b%C3%B6l%C3%BCm/komisyonlar"
---

# YTÜ Yapay Zeka ve Veri Mühendisliği Komisyonlar

- **Staj Komisyonu:** Yapay zeka ve veri bilimi staj yerlerinin denetimi.
- **İntibak ve Muafiyet Komisyonu:** Programlar arası yatay geçiş ve ÇAP intibakları.
- **Bitirme ve Tasarım Komisyonu:** YZM4901 ve YZM4902 jürileri.
- **Programlar Arası Geçiş Danışmanlığı:** Bilgisayar ve Matematik mühendislikleriyle çift anadal koordinasyonu.
""")
    print("Generated AI komisyonlar_ve_ogrenci_danismanligi.md")

    # lisansustu_programlar.md
    with open(os.path.join(base_dir, "lisansustu_programlar.md"), 'w', encoding='utf-8') as f:
        f.write("""---
baslik: "YTÜ Yapay Zeka ve Veri Mühendisliği Lisansüstü Programlar"
kategori: "fakulteler_ve_bolumler"
bolum: "Yapay Zeka ve Veri Mühendisliği"
guvenilirlik_duzeyi: "Tier 2"
orijinal_dosya: "arsiv/fakulteler/eef/ai/AI_Yuksek_Lisans_Programi_Tanitim_Kilavuzu.pdf"
kaynak: "http://www.fbe.yildiz.edu.tr/"
---

# YTÜ Yapay Zeka ve Veri Mühendisliği Lisansüstü Programlar

| Program Adı | Tür | Bologna ID | Eğitim Dili |
| :--- | :--- | :---: | :--- |
| **Yapay Zeka ve Veri Mühendisliği Tezli YL Programı** | Tezli YL | 562 | İngilizce |

- **Yasal Dayanak:** YTÜ Fen Bilimleri Enstitüsü (FBE).
- **Detaylı Bilgilendirme Kılavuzu:** [AI_Yuksek_Lisans_Programi_Tanitim_Kilavuzu.pdf](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/arsiv/fakulteler/eef/ai/AI_Yuksek_Lisans_Programi_Tanitim_Kilavuzu.pdf)
""")
    print("Generated AI lisansustu_programlar.md")

    # sikca_sorulan_sorular.md
    with open(os.path.join(base_dir, "sikca_sorulan_sorular.md"), 'w', encoding='utf-8') as f:
        f.write("""---
baslik: "YTÜ Yapay Zeka ve Veri Mühendisliği SSS"
kategori: "fakulteler_ve_bolumler"
bolum: "Yapay Zeka ve Veri Mühendisliği"
guvenilirlik_duzeyi: "Tier 2"
kaynak: "https://ai.yildiz.edu.tr/"
---

# YTÜ Yapay Zeka ve Veri Mühendisliği Sıkça Sorulan Sorular

### S1: Bilgisayar Mühendisliği ile Yapay Zeka Mühendisliği arasındaki fark nedir?
> **Cevap:** Bilgisayar Mühendisliği daha genel kapsamlı olup bilgisayar mimarisi, donanım, işletim sistemleri, mikroişlemciler ve yazılımı eşit ağırlıkla kapsar. Yapay Zeka ve Veri Mühendisliği ise doğrudan matematiksel modelleme, makine öğrenmesi, derin öğrenme, büyük veri analitiği, optimizasyon ve yapay zeka yazılımlarına odaklanır.

### S2: Program dili yüzde kaç İngilizcedir?
> **Cevap:** %100 İngilizcedir. Öğrencilerin kayıt yaptırabilmesi için İYS'den en az 60 veya eşdeğer uluslararası sınav puanı alması zorunludur.

### S3: YZM kodlu laboratuvar derslerinin devam şartı nedir?
> **Cevap:** YTÜ Lisans Eğitim-Öğretim Yönetmeliği Madde 23 uyarınca laboratuvar ve uygulamalı derslere devam zorunluluğu en az %80'dir.
""")
    print("Generated AI sikca_sorulan_sorular.md")

if __name__ == '__main__':
    run()
