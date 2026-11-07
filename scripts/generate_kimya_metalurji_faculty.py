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

def download_file(url, target_path):
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    if os.path.exists(target_path) and os.path.getsize(target_path) > 1000:
        return
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
            data = resp.read()
            with open(target_path, 'wb') as fp:
                fp.write(data)
            print(f"Downloaded: {target_path} ({len(data)} bytes)")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def fetch_bologna_curriculum(bologna_url, output_dir, prog_title, dept_name):
    print(f"=== FETCHING BOLOGNA: {dept_name} ({prog_title}) ===")
    os.makedirs(output_dir, exist_ok=True)
    soup = get_soup(bologna_url)
    
    t_curr = None
    for t in soup.find_all('table'):
        if '1.Yıl' in t.get_text() and 'Güz Yarıyılı' in t.get_text():
            t_curr = t
            break
    if not t_curr:
        tables = soup.find_all('table')
        t_curr = tables[1] if len(tables) > 1 else tables[0]

    curriculum = {}
    current_section = None
    
    for row in t_curr.find_all('tr'):
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
    
    all_courses = []
    prereqs = []
    
    for sec_name, (sem_num, filename, display_name) in semester_map.items():
        courses = curriculum.get(sec_name, [])
        filepath = os.path.join(output_dir, filename)
        
        tot_ects = sum(float(c['ects'].replace(',', '.')) for c in courses if c['ects'].replace(',', '.').replace('.', '', 1).isdigit())
        tot_credit = sum(float(c['credit'].replace(',', '.')) for c in courses if c['credit'].replace(',', '.').replace('.', '', 1).isdigit())
        
        md = []
        md.append("---")
        md.append(f'baslik: "{dept_name} ({prog_title}) - {display_name} Ders Planı"')
        md.append(f'kategori: "fakulteler_ve_bolumler"')
        md.append(f'bolum: "{dept_name}"')
        md.append(f'yariyil: {sem_num}')
        md.append(f'toplam_akts: {int(tot_ects)}')
        md.append(f'toplam_kredi: {tot_credit}')
        md.append(f'kaynak: "{bologna_url}"')
        md.append(f'guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"')
        md.append("---\n")
        
        md.append(f"# {dept_name} ({prog_title}) - {display_name}\n")
        md.append(f"Bu belgede, YTÜ {dept_name} Lisans Programı'nın ({display_name}) dersleri, kredileri, AKTS değerleri, haftalık saatleri ve önkoşul koşulları listelenmektedir.\n")
        
        md.append("> [!NOTE] Yarıyıl Özeti")
        md.append(f"> - **Dönem:** {display_name} ({prog_title})")
        md.append(f"> - **Ders Sayısı:** {len(courses)} adet")
        md.append(f"> - **Toplam Yerel Kredi:** {tot_credit}")
        md.append(f"> - **Toplam AKTS Kredisi:** {int(tot_ects)} AKTS\n")
        md.append("---\n")
        
        md.append("## 📋 Ders Listesi ve Kredi Dağılımı\n")
        md.append("| Ders Kodu | Önkoşul | Ders Adı | T | U | L | Kredi | AKTS |")
        md.append("| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: |")
        for c in courses:
            prq = c['prereq'] if c['prereq'] else "-"
            c_link = f"[{c['name']}]({c['link']})" if c['link'] else c['name']
            md.append(f"| **{c['code']}** | {prq} | {c_link} | {c['lec']} | {c['app']} | {c['lab']} | {c['credit']} | **{c['ects']}** |")
            all_courses.append((sem_num, c))
            if c['prereq']:
                prereqs.append((c['code'], c['name'], c['prereq'], sem_num))
        
        md.append("\n---\n")
        md.append("## 🔍 Ders Kartları ve Bilgileri\n")
        for c in courses:
            md.append(f"### 📌 {c['code']} - {c['name']}")
            md.append(f"- **Ders Türü:** Zorunlu / Mesleki")
            md.append(f"- **Kredi Bilgisi:** {c['lec']} Saat Teori, {c['app']} Saat Uygulama, {c['lab']} Saat Laboratuvar | **{c['credit']} Kredi / {c['ects']} AKTS**")
            md.append(f"- **Önkoşul:** {c['prereq'] if c['prereq'] else 'Yok'}")
            if c['link']:
                md.append(f"- **Resmi Bologna Bağlantısı:** [Bologna Ders Detayı]({c['link']})")
            md.append("")
        
        with open(filepath, 'w', encoding='utf-8') as fp:
            fp.write("\n".join(md))
        print(f"Generated {filepath}")
        
    # Önkoşul zinciri
    prq_file = os.path.join(output_dir, "onkosul_zinciri.md")
    pmd = []
    pmd.append("---")
    pmd.append(f'baslik: "{dept_name} Önkoşul Zinciri ve Bağımlılık Haritası"')
    pmd.append(f'kategori: "fakulteler_ve_bolumler"')
    pmd.append(f'bolum: "{dept_name}"')
    pmd.append(f'kaynak: "{bologna_url}"')
    pmd.append(f'guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"')
    pmd.append("---\n")
    pmd.append(f"# {dept_name} Önkoşul Zinciri ve Bağımlılık Haritası ({prog_title})\n")
    pmd.append("Bu belgede, bölüm müfredatında yer alan derslerin önkoşul kuralları listelenmektedir.\n")
    pmd.append("| Hedef Ders Kodu | Hedef Ders Adı | Yarıyıl | Gerekli Önkoşul(lar) |")
    pmd.append("| :--- | :--- | :---: | :--- |")
    if prereqs:
        for code, name, prq, sem in prereqs:
            pmd.append(f"| **{code}** | {name} | {sem}. Yarıyıl | `{prq}` |")
    else:
        pmd.append("| - | Doğrudan önkoşul bağımlılığı bulunmamaktadır. | - | - |")
    
    with open(prq_file, 'w', encoding='utf-8') as fp:
        fp.write("\n".join(pmd))
    print(f"Generated {prq_file}")
    
    # Seçimlik ders havuzları
    sec_file = os.path.join(output_dir, "secimlik_ders_havuzlari.md")
    smd = []
    smd.append("---")
    smd.append(f'baslik: "{dept_name} Seçimlik Ders Havuzları"')
    smd.append(f'kategori: "fakulteler_ve_bolumler"')
    smd.append(f'bolum: "{dept_name}"')
    smd.append(f'kaynak: "{bologna_url}"')
    smd.append(f'guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"')
    smd.append("---\n")
    smd.append(f"# {dept_name} Seçimlik Ders Havuzları ({prog_title})\n")
    smd.append("Bölümün teknik ve sosyal seçimlik dersleri Bologna Bilgi Paketi uyarınca dönem bazlı olarak ilan edilir.\n")
    with open(sec_file, 'w', encoding='utf-8') as fp:
        fp.write("\n".join(smd))
    print(f"Generated {sec_file}")

    # Bologna README
    breadme = os.path.join(output_dir, "README.md")
    brm = []
    brm.append(f"# {dept_name} Bologna Ders Planı ({prog_title})\n")
    brm.append(f"Bu dizin, {dept_name} lisans eğitiminin tüm 8 yarıyılını içerir.\n")
    brm.append("- [1. Yarıyıl](1_yariyil.md)\n- [2. Yarıyıl](2_yariyil.md)\n- [3. Yarıyıl](3_yariyil.md)\n- [4. Yarıyıl](4_yariyil.md)")
    brm.append("- [5. Yarıyıl](5_yariyil.md)\n- [6. Yarıyıl](6_yariyil.md)\n- [7. Yarıyıl](7_yariyil.md)\n- [8. Yarıyıl](8_yariyil.md)")
    brm.append("- [Önkoşul Zinciri](onkosul_zinciri.md)\n- [Seçimlik Ders Havuzları](secimlik_ders_havuzlari.md)\n")
    with open(breadme, 'w', encoding='utf-8') as fp:
        fp.write("\n".join(brm))
    print(f"Generated {breadme}")

def generate_core_files(dept_dir, dept_name, faculty_name, code_prefix, lab_info, staj_info, sss_list):
    os.makedirs(dept_dir, exist_ok=True)
    
    # 1. README.md
    with open(os.path.join(dept_dir, "README.md"), "w", encoding="utf-8") as fp:
        fp.write(f"""---
baslik: "{dept_name} Bölüm Tanıtımı ve Yönetim"
kategori: "fakulteler_ve_bolumler"
fakulte: "{faculty_name}"
bolum: "{dept_name}"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bölüm Portalı)"
---

# {dept_name}

Yıldız Teknik Üniversitesi **{faculty_name}** bünyesinde yer alan {dept_name}, Davutpaşa Yerleşkesi Kimya-Metalurji Binası'nda modern araştırma altyapısıyla eğitim ve bilimsel faaliyetlerini sürdürmektedir.

## 🗂️ Bölüm Dokümantasyon Rehberi
- [Lisans Eğitim Yapısı](lisans_egitim_yapisi.md)
- [Staj ve Bitirme Esasları](staj_tasarim_ve_bitirme_esaslari.md)
- [Laboratuvarlar ve Araştırma](laboratuvarlar_ve_arastirma.md)
- [Komisyonlar ve Öğrenci Danışmanlığı](komisyonlar_ve_ogrenci_danismanligi.md)
- [Lisansüstü Programlar](lisansustu_programlar.md)
- [Sıkça Sorulan Sorular](sikca_sorulan_sorular.md)
""")

    # 2. lisans_egitim_yapisi.md
    with open(os.path.join(dept_dir, "lisans_egitim_yapisi.md"), "w", encoding="utf-8") as fp:
        fp.write(f"""---
baslik: "{dept_name} Lisans Eğitim Yapısı"
kategori: "fakulteler_ve_bolumler"
fakulte: "{faculty_name}"
bolum: "{dept_name}"
---

# {dept_name} Lisans Eğitim Yapısı

Bölüm lisans programı toplam 240 AKTS kredisinden oluşur. Öğrenciler temel bilimler, mesleki dersler, laboratuvar uygulamaları, staj ve bitirme çalışması yükümlülüklerini tamamlayarak mezun olurlar.
Eğitim dili YÖK ve Senato kararları doğrultusunda yürütülmektedir.
""")

    # 3. staj_tasarim_ve_bitirme_esaslari.md
    with open(os.path.join(dept_dir, "staj_tasarim_ve_bitirme_esaslari.md"), "w", encoding="utf-8") as fp:
        fp.write(f"""---
baslik: "{dept_name} Staj, Tasarım ve Bitirme Esasları"
kategori: "fakulteler_ve_bolumler"
fakulte: "{faculty_name}"
bolum: "{dept_name}"
---

# {dept_name} Staj, Tasarım ve Bitirme Esasları

## 📌 Staj Esasları
{staj_info}

## 📌 Tasarım ve Bitirme Çalışması
Bölüm lisans programında tasarım projesi ve bitirme tezi mezuniyetin zorunlu bileşenleridir. Öğrenciler danışman öğretim üyesi gözetiminde araştırma ve uygulama projelerini tamamlayarak jüri önünde savunurlar.
""")

    # 4. laboratuvarlar_ve_arastirma.md
    with open(os.path.join(dept_dir, "laboratuvarlar_ve_arastirma.md"), "w", encoding="utf-8") as fp:
        fp.write(f"""---
baslik: "{dept_name} Laboratuvarlar ve Araştırma Altyapısı"
kategori: "fakulteler_ve_bolumler"
fakulte: "{faculty_name}"
bolum: "{dept_name}"
---

# {dept_name} Laboratuvarları ve Araştırma Altyapısı

{lab_info}
""")

    # 5. komisyonlar_ve_ogrenci_danismanligi.md
    with open(os.path.join(dept_dir, "komisyonlar_ve_ogrenci_danismanligi.md"), "w", encoding="utf-8") as fp:
        fp.write(f"""---
baslik: "{dept_name} Komisyonlar ve Danışmanlık"
kategori: "fakulteler_ve_bolumler"
fakulte: "{faculty_name}"
bolum: "{dept_name}"
---

# {dept_name} Komisyonlar ve Öğrenci Danışmanlığı

Bölümde eğitim-öğretim ve idari süreçlerin yürütülmesi amacıyla Staj Komisyonu, İntibak ve Muafiyet Komisyonu, ÇAP/Yandal Komisyonu, MÜDEK/Kalite Komisyonu ve Bitirme Çalışması Komisyonu görev yapmaktadır.
Her öğrenciye kayıt anında bir akademik danışman atanır.
""")

    # 6. lisansustu_programlar.md
    with open(os.path.join(dept_dir, "lisansustu_programlar.md"), "w", encoding="utf-8") as fp:
        fp.write(f"""---
baslik: "{dept_name} Lisansüstü Programlar"
kategori: "fakulteler_ve_bolumler"
fakulte: "{faculty_name}"
bolum: "{dept_name}"
---

# {dept_name} Lisansüstü Programları

Bölüm Fen Bilimleri Enstitüsü (FBE) koordinasyonunda Tezli Yüksek Lisans ve Doktora programları yürütmektedir. Başvuru takvimi, ALES/YDS taban puanları ve kontenjanlar FBE tarafından ilan edilir.
""")

    # 7. sikca_sorulan_sorular.md
    with open(os.path.join(dept_dir, "sikca_sorulan_sorular.md"), "w", encoding="utf-8") as fp:
        fp.write(f"""---
baslik: "{dept_name} Sıkça Sorulan Sorular"
kategori: "fakulteler_ve_bolumler"
fakulte: "{faculty_name}"
bolum: "{dept_name}"
---

# {dept_name} Sıkça Sorulan Sorular

""")
        for q, a in sss_list:
            fp.write(f"### ❓ {q}\n**Cevap:** {a}\n\n")

def run():
    print("=== STARTING KIMYA-METALURJI FAKULTESI INTEGRATION ===")
    
    # Archives download
    archives = [
        ("https://kim.yildiz.edu.tr/sites/kim.yildiz.edu.tr/files/2025-11/kmf-hizmet-standart-tablosu.pdf", "arsiv/fakulteler/kim/dekanlik/KMF_Hizmet_Standart_Tablosu.pdf"),
        ("https://kim.yildiz.edu.tr/sites/kim.yildiz.edu.tr/files/2025-11/kimya-metalurji-fak.hizmet-envanteriyeni2025.pdf", "arsiv/fakulteler/kim/dekanlik/KMF_Hizmet_Envanteri_2025.pdf"),
        ("https://kim.yildiz.edu.tr/sites/kim.yildiz.edu.tr/files/2022-05/Acil%20Durum%20Eylem%20Plani.pdf", "arsiv/fakulteler/kim/dekanlik/KMF_Acil_Durum_Eylem_Plani.pdf"),
        ("https://bioeng.yildiz.edu.tr/media/files/ShowFile-10.pdf", "arsiv/fakulteler/kim/bioeng/BIOENG_Staj_Yonetmeligi.pdf"),
        ("https://food.yildiz.edu.tr/media/files/Gıda Mühendisliği Laboratuvarları için Genel Güvenlik Kuralları(1).doc", "arsiv/fakulteler/kim/food/Gida_Muhendisligi_Laboratuvar_Guvenlik_Kurallari.doc"),
        ("https://kmm.yildiz.edu.tr/sites/kmm.yildiz.edu.tr/files/2025-10/staj-bilgilendirme.pdf", "arsiv/fakulteler/kim/kmm/KMM_Staj_Bilgilendirme.pdf"),
        ("https://kmm.yildiz.edu.tr/sites/kmm.yildiz.edu.tr/files/2024-02/kimya-muhendisligi-laboratuvar-guvenligi-kitapcik.pdf", "arsiv/fakulteler/kim/kmm/Kimya_Muhendisligi_Laboratuvar_Guvenligi_Kitapcik.pdf"),
        ("https://kmm.yildiz.edu.tr/sites/kmm.yildiz.edu.tr/files/2024-03/01-bitirme_calismasi_esaslari_2023-24.pdf", "arsiv/fakulteler/kim/kmm/KMM_Bitirme_Calismasi_Esaslari.pdf"),
        ("http://www.mtm.yildiz.edu.tr/media/files/1_STAJ_BİLGİSAYAR DONANIMI VE TEMEL UYGULAMALARI STAJ DEFTERİ(TÜRKÇE).docx", "arsiv/fakulteler/kim/mtm/MTM_Staj_1_Defteri_TR.docx"),
        ("http://www.mtm.yildiz.edu.tr/media/files/2_STAJ_SORUN ÇÖZÜM TEKNİKLERİ STAJ DEFTERİ(TÜRKÇE)(1).docx", "arsiv/fakulteler/kim/mtm/MTM_Staj_2_Defteri_TR.docx"),
        ("http://www.met.yildiz.edu.tr/media/files/Metalurji STAJ Yürütme Esasları yükleme.docx", "arsiv/fakulteler/kim/met/MET_Staj_Yurutme_Esaslari.docx"),
        ("http://www.met.yildiz.edu.tr/media/files/YTU-MMM-Staj Defteri (1).docx", "arsiv/fakulteler/kim/met/MET_Staj_Defteri.docx")
    ]
    for url, path in archives:
        download_file(url, path)
        
    # Dean's office files
    kim_dir = "05_fakulteler_ve_bolumler/kimya_metalurji_fakultesi"
    os.makedirs(kim_dir, exist_ok=True)
    
    with open(os.path.join(kim_dir, "README.md"), "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "Kimya-Metalurji Fakültesi Genel Tanıtımı ve Teşkilat Yapısı"
kategori: "fakulteler_ve_bolumler"
fakulte: "Kimya-Metalurji Fakültesi"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# YTÜ Kimya-Metalurji Fakültesi

Yıldız Teknik Üniversitesi Kimya-Metalurji Fakültesi, Davutpaşa Yerleşkesi'ndeki modern fakülte binası ve ileri teknoloji laboratuvarlarında 5 mühendislik bölümüyle faaliyet göstermektedir.

## 🏛️ Bağlı Bölümler
- [Biyomühendislik](biyomuhendislik/README.md)
- [Gıda Mühendisliği](gida_muhendisligi/README.md)
- [Kimya Mühendisliği](kimya_muhendisligi/README.md)
- [Matematik Mühendisliği](matematik_muhendisligi/README.md)
- [Metalurji ve Malzeme Mühendisliği](metalurji_ve_malzeme_muhendisligi/README.md)

## 📌 Temel Fakülte Belgeleri
- [Dekanlık ve Teşkilat Yapısı](dekanlik_ve_teskilat_yapisi.md)
- [Fakülte Sıkça Sorulan Sorular](fakulte_sikca_sorulan_sorular.md)
- [Hizmet Standartları ve Envanteri](hizmet_standartlari_ve_envanteri.md)
- [Akran Danışmanlığı ve Öğrenci Rehberi](akran_danismanligi_ve_ogrenci_rehberi.md)
""")

    with open(os.path.join(kim_dir, "dekanlik_ve_teskilat_yapisi.md"), "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "Kimya-Metalurji Fakültesi Dekanlığı ve Teşkilat Yapısı"
kategori: "fakulteler_ve_bolumler"
fakulte: "Kimya-Metalurji Fakültesi"
kaynak: "https://kim.yildiz.edu.tr/yonetim"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# Kimya-Metalurji Fakültesi Dekanlığı ve Yönetim Kadrosu

## 👥 Üst Yönetim
- **Dekan:** Prof. Dr. Musa TÜRKER
- **Dekan Yardımcısı:** Prof. Dr. Salih KARASU
- **Dekan Yardımcısı:** Prof. Dr. Cem Bülent ÜSTÜNDAĞ
- **Fakülte Sekreteri:** Filiz MAYAKON

## 🏛️ Teşkilat ve Karar Organları
- **Fakülte Kurulu:** Dekan başkanlığında 5 bölüm başkanının ve seçilmiş öğretim üyelerinin katılımıyla toplanır.
- **Fakülte Yönetim Kurulu:** İdari, mali ve öğrenci işleri intibak/muafiyet onay kararlarını yürütür.
""")

    with open(os.path.join(kim_dir, "fakulte_sikca_sorulan_sorular.md"), "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "Kimya-Metalurji Fakültesi Sıkça Sorulan Sorular"
kategori: "fakulteler_ve_bolumler"
fakulte: "Kimya-Metalurji Fakültesi"
kaynak: "https://kim.yildiz.edu.tr/sss"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# Kimya-Metalurji Fakültesi Sıkça Sorulan Sorular

### ❓ Lisansüstü başvuruları nereye yapılmaktadır?
**Cevap:** Başvurular Fen Bilimleri Enstitüsü (FBE) üzerinden merkezi olarak alınmaktadır (`http://www.fbe.yildiz.edu.tr/`).

### ❓ Ders intibakı ve muafiyet için nereye başvurulmalıdır?
**Cevap:** Kayıtlı olunan bölüm başkanlığına ders içerikleri ve onaylı transkript ile dilekçe verilmelidir.

### ❓ Aynı dönemde çift anadal ve kurum içi yatay geçiş yapılabilir mi?
**Cevap:** İlgili Senato yönergelerine göre aynı yarıyılda hem ÇAP hem yatay geçiş kesin kaydı yapılamaz, öğrencinin birini tercih etmesi gerekir.
""")

    with open(os.path.join(kim_dir, "hizmet_standartlari_ve_envanteri.md"), "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "Kimya-Metalurji Fakültesi Hizmet Standartları ve Envanteri"
kategori: "fakulteler_ve_bolumler"
fakulte: "Kimya-Metalurji Fakültesi"
kaynak: "https://kim.yildiz.edu.tr/kalite-formlari"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# Hizmet Standartları Tablosu ve Süreç Envanteri

Fakülte Dekanlığı ve bölüm sekreterliklerinin öğrenci dilekçeleri, staj SGK girişleri, askerlik tecil yazıları, transkript ve mezuniyet ilişik kesme süreçleri resmi Hizmet Standartları Tablosu'nda tanımlanmış yasal sürelerde sonuçlandırılmaktadır.
""")

    with open(os.path.join(kim_dir, "akran_danismanligi_ve_ogrenci_rehberi.md"), "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "Kimya-Metalurji Fakültesi Akran Danışmanlığı ve Acil Eylem Planı"
kategori: "fakulteler_ve_bolumler"
fakulte: "Kimya-Metalurji Fakültesi"
kaynak: "https://kim.yildiz.edu.tr/acil-durum-eylem-plani"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# Akran Danışmanlığı Sistemi ve Acil Durum Eylem Planı

Kimya-Metalurji Fakültesi Davutpaşa binasında laboratuvar güvenliği en üst seviyede tutulur. Kimyasal dökülme, yangın ve tahliye durumlarında Acil Durum Eylem Planı geçerlidir.
Yeni öğrencilere uyum sürecinde akran danışmanları destek verir.
""")

    # 1. Biyomühendislik (BIOENG)
    bio_dir = os.path.join(kim_dir, "biyomuhendislik")
    generate_core_files(
        bio_dir, "Biyomühendislik", "Kimya-Metalurji Fakültesi", "BIO",
        lab_info="""Bölümde Biyoreaktör ve Fermantasyon Laboratuvarı, Doku Mühendisliği ve Biyomalzeme Laboratuvarı, Moleküler Biyoloji ve Genetik Laboratuvarı, Biyoanaliz ve Kromatografi Laboratuvarı, Biyosensör Laboratuvarı bulunmaktadır. Laboratuvar Güvenliği Föyü ve Kişisel Koruyucu Donanım (KKD) kullanımı zorunludur.""",
        staj_info="""Biyomühendislik Bölümü'nde toplam 60 iş günü staj zorunludur. Staj 1 (Laboratuvar/Ar-Ge - 30 gün) ve Staj 2 (Endüstriyel Üretim/Biyoproses - 30 gün) olarak yapılır. Stajlar `BIOENG_Staj_Yonetmeligi.pdf` hükümlerine tabidir.""",
        sss_list=[
            ("Biyomühendislik stajını hastanede yapabilir miyim?", "Klinik genetik, biyokimya veya doku tipleme laboratuvarı bulunan akredite hastanelerde Staj 1 kapsamında yapılabilir."),
            ("Laboratuvar güvenliği sınavı zorunlu mudur?", "Evet, araştırma laboratuvarlarına giriş öncesinde bölüm laboratuvar güvenlik eğitiminin tamamlanması şarttır.")
        ]
    )
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=147&aid=26", os.path.join(bio_dir, "bologna_ders_plani_yuzde30"), "%30 İngilizce", "Biyomühendislik")
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=163&aid=26", os.path.join(bio_dir, "bologna_ders_plani_yuzde100"), "%100 İngilizce", "Biyomühendislik")

    # 2. Gıda Mühendisliği (FOOD)
    food_dir = os.path.join(kim_dir, "gida_muhendisligi")
    generate_core_files(
        food_dir, "Gıda Mühendisliği", "Kimya-Metalurji Fakültesi", "GDM",
        lab_info="""Bölümde Gıda Mikrobiyolojisi Laboratuvarı, Gıda Kimyası ve Analizleri Laboratuvarı, Süt ve Et Teknolojisi Laboratuvarı, Hububat ve Yağ Teknolojisi Laboratuvarı, Duyusal Analiz Laboratuvarı bulunmaktadır. Laboratuvarlarda Genel Güvenlik Kuralları kitapçığı uygulanır.""",
        staj_info="""Gıda Mühendisliği Bölümü'nde 60 iş günü zorunlu staj vardır. Laboratuvar Analiz Stajı (30 gün) ve Gıda İşletmesi Üretim Stajı (30 gün) olarak iki grupta tamamlanır.""",
        sss_list=[
            ("Gıda Mühendisliği staj defteri dili nedir?", "%30 İngilizce programında staj defteri Türkçe veya İngilizce doldurulabilir."),
            ("Bitirme tezi için deneysel çalışma şart mı?", "Bölüm laboratuvarlarında deneysel araştırma tezi veya kapsamlı bir gıda fabrikası tasarım projesi şeklinde yürütülür.")
        ]
    )
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=195&aid=109", os.path.join(food_dir, "bologna_ders_plani"), "%30 İngilizce", "Gıda Mühendisliği")

    # 3. Kimya Mühendisliği (KMM)
    kmm_dir = os.path.join(kim_dir, "kimya_muhendisligi")
    generate_core_files(
        kmm_dir, "Kimya Mühendisliği", "Kimya-Metalurji Fakültesi", "KMB",
        lab_info="""Bölümde Temel İşlemler (Unit Operations) Laboratuvarı, Kimyasal Reaksiyon Mühendisliği Laboratuvarı, Polimer ve Kolloid Laboratuvarı, Proses Kontrol Laboratuvarı ve Enerji Teknolojileri Laboratuvarı bulunmaktadır. Güvenlik Kitapçığı ve FR-1251 mesai dışı izin formu zorunludur.""",
        staj_info="""Kimya Mühendisliği Bölümü'nde toplam 60 iş günü staj zorunludur. Staj 1 (Laboratuvar Stajı - FR-0751) ve Staj 2 (İşletme Stajı - FR-0750) olarak yapılır. Staj Defteri Hazırlama Rehberi ve FR-1800 Staj Defteri Onay Formu kullanılır.""",
        sss_list=[
            ("Laboratuvar ve İşletme stajı sırası önemli mi?", "Önce Laboratuvar stajının (en az 4. yarıyıl sonunda), ardından İşletme proses stajının yapılması tavsiye edilir."),
            ("Bitirme çalışması takvimi nasıldır?", "Bölüm web sitesinde her dönem başında Bitirme Çalışması Esasları ve Takvimi ilan edilir. Dış kapak formatına tam uyum aranır.")
        ]
    )
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=36&aid=23", os.path.join(kmm_dir, "bologna_ders_plani_yuzde30"), "%30 İngilizce", "Kimya Mühendisliği")
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=398&aid=23", os.path.join(kmm_dir, "bologna_ders_plani_yuzde100"), "%100 İngilizce", "Kimya Mühendisliği")

    # 4. Matematik Mühendisliği (MTM)
    mtm_dir = os.path.join(kim_dir, "matematik_muhendisligi")
    generate_core_files(
        mtm_dir, "Matematik Mühendisliği", "Kimya-Metalurji Fakültesi", "MTM",
        lab_info="""Bölümde Yüksek Başarımlı Hesaplama Laboratuvarı, Veri Analitiği ve İstatistik Laboratuvarı, Bilgisayar Programlama Laboratuvarları bulunmaktadır. Modern yazılım geliştirme ve matematiksel modelleme araçları kuruludur.""",
        staj_info="""Matematik Mühendisliği Bölümü'nde 60 iş günü staj vardır. Staj 1: Bilgisayar Donanımı ve Temel Uygulamaları (30 gün), Staj 2: Sorun Çözüm Teknikleri ve Algoritma/Yazılım Modelleme (30 gün) olarak resmi bölüm defterleri (`1_STAJ_...docx`, `2_STAJ_...docx`) ile teslim edilir.""",
        sss_list=[
            ("Yazılım firmalarında staj yapabilir miyim?", "Evet, Staj 1 ve Staj 2 bilişim, finans, telekomünikasyon ve veri analitiği departmanlarında yapılabilir."),
            ("İngilizce programda staj defteri hangi dilde olmalı?", "%100 İngilizce programı öğrencileri İngilizce staj defteri şablonunu kullanmalıdır.")
        ]
    )
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=37&aid=24", os.path.join(mtm_dir, "bologna_ders_plani_yuzde30"), "%30 İngilizce", "Matematik Mühendisliği")
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=222&aid=24", os.path.join(mtm_dir, "bologna_ders_plani_yuzde100"), "%100 İngilizce", "Matematik Mühendisliği")

    # 5. Metalurji ve Malzeme Mühendisliği (MET)
    met_dir = os.path.join(kim_dir, "metalurji_ve_malzeme_muhendisligi")
    generate_core_files(
        met_dir, "Metalurji ve Malzeme Mühendisliği", "Kimya-Metalurji Fakültesi", "MET",
        lab_info="""Bölümde Döküm Laboratuvarı, Isıl İşlem Laboratuvarı, Kaynak Teknolojileri Laboratuvarı, Mekanik Testler ve Yorulma Laboratuvarı, X-Işınları Kırınımı (XRD) ve Taramalı Elektron Mikroskobu (SEM) Laboratuvarı, Korozyon ve Yüzey İşlemleri Laboratuvarı, Seramik ve Kompozit Laboratuvarı bulunmaktadır.""",
        staj_info="""Bölümde 60 gün staj zorunludur: STAJ-1 Metalurjik Üretim Prosesleri Stajı (30 gün) ve STAJ-2 Şekillendirme Prosesleri ve Yönetim Stajı (30 gün) olarak yürütülür. Staj defteri `YTU-MMM-Staj Defteri.docx` formatında, anket ise FR-0997 ile teslim edilir.""",
        sss_list=[
            ("Dökümhane stajı zorunlu mu?", "STAJ-1 kapsamında demir-çelik, demir dışı döküm veya primer metal üretim tesislerinde staj yapılması beklenir."),
            ("İşletmede Mesleki Eğitim (KOOP) var mıdır?", "Evet, metalurji ve savunma sanayii kuruluşlarında son sınıf öğrencileri için KOOP uygulanmaktadır.")
        ]
    )
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=38&aid=25", os.path.join(met_dir, "bologna_ders_plani_yuzde30"), "%30 İngilizce", "Metalurji ve Malzeme Mühendisliği")
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=401&aid=25", os.path.join(met_dir, "bologna_ders_plani_yuzde100"), "%100 İngilizce", "Metalurji ve Malzeme Mühendisliği")

    print("=== KIMYA-METALURJI FAKULTESI INTEGRATION COMPLETED ===")

if __name__ == "__main__":
    run()
