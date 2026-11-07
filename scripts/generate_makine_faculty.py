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
    print(f"=== FETCHING BOLOGNA: {prog_title} ===")
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
        md.append(f'baslik: "{dept_name} - {display_name} Ders Planı"')
        md.append(f'kategori: "fakulteler_ve_bolumler"')
        md.append(f'bolum: "{dept_name}"')
        md.append(f'yariyil: {sem_num}')
        md.append(f'toplam_akts: {int(tot_ects)}')
        md.append(f'toplam_kredi: {tot_credit}')
        md.append(f'kaynak: "{bologna_url}"')
        md.append(f'guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"')
        md.append("---\n")
        
        md.append(f"# {dept_name} ({prog_title}) - {display_name}\n")
        md.append(f"Bu belgede, YTÜ {dept_name} Lisans Programı'nın ({display_name}) dersleri, kredileri, AKTS değerleri, haftalık saatleri ve önkoşul koşulları yer almaktadır.\n")
        
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

Yıldız Teknik Üniversitesi **{faculty_name}** bünyesinde yer alan {dept_name}, ulusal ve uluslararası standartlarda mühendislik eğitimi vermektedir.

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

Bölüm lisans programı toplam 240 AKTS kredisinden oluşur. Öğrenciler temel bilimler, temel mühendislik, mesleki tasarım ve bitirme çalışmalarını tamamlayarak mezun olurlar.
Eğitim dili YÖK ve Senato esasları doğrultusunda yürütülmektedir.
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
Bölüm lisans programında tasarım ve bitirme çalışması zorunlu mezuniyet yükümlülüklerindendir. Bitirme çalışması öncesinde tasarım projesinin başarıyla tamamlanması zorunludur.
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

Bölümde eğitim-öğretim süreçlerinin düzenli yürütülmesi için Staj Komisyonu, İntibak ve Muafiyet Komisyonu, ÇAP/Yandal Komisyonu, MÜDEK/Akreditasyon Komisyonu ve Bitirme Komisyonu görev yapmaktadır.
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

Bölüm Fen Bilimleri Enstitüsü (FBE) koordinasyonunda Tezli Yüksek Lisans ve Doktora programları yürütmektedir. Başvuru takvimi ve kontenjanlar FBE tarafından ilan edilir.
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
    print("=== STARTING MAKINE FAKULTESI INTEGRATION ===")
    
    # Archives download
    archives = [
        ("https://mak.yildiz.edu.tr/sites/mak.yildiz.edu.tr/files/2022-05/Acil%20Eylem%20Plan%C4%B1.pdf", "arsiv/fakulteler/mak/dekanlik/Acil_Durum_Eylem_Plani.pdf"),
        ("https://mak.yildiz.edu.tr/sites/mak.yildiz.edu.tr/files/2023-12/makine-fakultesi-staj-uygulama-ilkeleri-2023.docx", "arsiv/fakulteler/mak/dekanlik/makine_fakultesi_staj_uygulama_ilkeleri.docx"),
        ("http://mkm.yildiz.edu.tr/sites/mkm.yildiz.edu.tr/files/2024-01/yildiz-teknik-universitesi-makine-fakultesi-lisans-ogretimi-staj-uygulama-ilkeleri.pdf", "arsiv/fakulteler/mak/mkm/MKM_Staj_Uygulama_Ilkeleri.pdf"),
        ("http://mkm.yildiz.edu.tr/sites/mkm.yildiz.edu.tr/images/files/Makine%20M%C3%BChendisli%C4%9Fi%20%C3%87ift%20Anadal%20E%C5%9Flenik%20B%C3%B6l%C3%BCm%20Dersleri.xlsx", "arsiv/fakulteler/mak/mkm/Makine_Muhendisligi_CAP_Eslenik_Dersleri.xlsx"),
        ("http://enm.yildiz.edu.tr/sites/enm.yildiz.edu.tr/files/end4000_tezyazim_tr_2025.docx", "arsiv/fakulteler/mak/enm/END4000_Tez_Yazim_Kilavuzu_TR.docx"),
        ("http://enm.yildiz.edu.tr/sites/enm.yildiz.edu.tr/files/project_temp-en.docx", "arsiv/fakulteler/mak/enm/Multidisciplinary_Design_Project_Template_EN.docx"),
        ("https://mkt.yildiz.edu.tr/sites/mkt.yildiz.edu.tr/files/2026-10/2026-2027-guz-mst-kilavuz.pdf", "arsiv/fakulteler/mak/mkt/Mekatronik_Sistemi_Tasarimi_Kilavuz_2026_2027.pdf"),
        ("https://mkt.yildiz.edu.tr/sites/mkt.yildiz.edu.tr/files/2026-10/2026-2027-guz-bc-kilavuz.pdf", "arsiv/fakulteler/mak/mkt/Mekatronik_Bitirme_Calismasi_Kilavuz_2026_2027.pdf"),
        ("https://mkt.yildiz.edu.tr/sites/mkt.yildiz.edu.tr/files/2025-04/staj-defteri-ornek.docx", "arsiv/fakulteler/mak/mkt/MKT_Staj_Defteri_Ornek.docx")
    ]
    for url, path in archives:
        download_file(url, path)
        
    # Dean's office files
    mak_dir = "05_fakulteler_ve_bolumler/makine_fakultesi"
    os.makedirs(mak_dir, exist_ok=True)
    
    with open(os.path.join(mak_dir, "README.md"), "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "Makine Fakültesi Genel Tanıtımı ve Teşkilat Yapısı"
kategori: "fakulteler_ve_bolumler"
fakulte: "Makine Fakültesi"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# YTÜ Makine Fakültesi

Yıldız Teknik Üniversitesi Makine Fakültesi, Yıldız Yerleşkesi'nde tarihi ve modern binalarda faaliyet gösteren, Makine Mühendisliği, Endüstri Mühendisliği ve Mekatronik Mühendisliği bölümlerini barındıran köklü bir fakültedir.

## 🏛️ Bağlı Bölümler
- [Makine Mühendisliği](makine_muhendisligi/README.md)
- [Endüstri Mühendisliği](endustri_muhendisligi/README.md)
- [Mekatronik Mühendisliği](mekatronik_muhendisligi/README.md)

## 📌 Temel Fakülte Belgeleri
- [Dekanlık ve Teşkilat Yapısı](dekanlik_ve_teskilat_yapisi.md)
- [Fakülte Sıkça Sorulan Sorular](fakulte_sikca_sorulan_sorular.md)
- [Akran Danışmanlığı ve Öğrenci Rehberi](akran_danismanligi_ve_ogrenci_rehberi.md)
- [Staj ve KOOP Genel Esasları](staj_ve_koop_genel_esaslari.md)
""")

    with open(os.path.join(mak_dir, "dekanlik_ve_teskilat_yapisi.md"), "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "Makine Fakültesi Dekanlığı ve Teşkilat Yapısı"
kategori: "fakulteler_ve_bolumler"
fakulte: "Makine Fakültesi"
kaynak: "https://mak.yildiz.edu.tr/dekanlik"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# Makine Fakültesi Dekanlığı ve Yönetim Kadrosu

## 👥 Üst Yönetim
- **Dekan:** Prof. Dr. Zehra YUMURTACI (E-posta: `zyumur@yildiz.edu.tr`)
- **Dekan Yardımcısı:** Prof. Dr. Binnur SAĞBAŞ (E-posta: `bzeybek@yildiz.edu.tr`)
- **Dekan Yardımcısı:** Doç. Dr. Ali KARAŞAN (E-posta: `akarasan@yildiz.edu.tr`)
- **Fakülte Sekreteri:** Güler GÜLER (E-posta: `gguler@yildiz.edu.tr`)

## 🏛️ Kurullar
- **Fakülte Kurulu:** Dekan başkanlığında bölüm başkanları ve profesör, doçent, doktor öğretim üyesi temsilcilerinden oluşur.
- **Fakülte Yönetim Kurulu:** İdari ve eğitim kararlarını alan karar organıdır.
""")

    with open(os.path.join(mak_dir, "fakulte_sikca_sorulan_sorular.md"), "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "Makine Fakültesi Sıkça Sorulan Sorular"
kategori: "fakulteler_ve_bolumler"
fakulte: "Makine Fakültesi"
kaynak: "https://mak.yildiz.edu.tr/sss"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# Makine Fakültesi Sıkça Sorulan Sorular

### ❓ Lisansüstü başvurularını nereye yapmalıyım?
**Cevap:** Lisansüstü eğitime ilişkin kontenjanlar ve süreçler Fen Bilimleri Enstitüsü (FBE) ve ilgili anabilim dallarınca takip edilmektedir (`http://www.fbe.yildiz.edu.tr/`).

### ❓ Diğer Yükseköğretim Kurumunda aldığım derslerden nasıl muaf olabilirim?
**Cevap:** Kayıtlı olduğunuz bölüm başkanlığına ders içeriklerinizi ve transkriptinizi eklediğiniz dilekçe ile başvurduğunuzda intibak komisyonu tarafından değerlendirilir.

### ❓ Fakülte bünyesindeki staj formları her bölüm için aynı mıdır?
**Cevap:** Hayır, Makine, Endüstri ve Mekatronik Mühendisliği bölümlerinin staj defteri, başvuru formu ve staj ilkeleri bölüm bazında farklılık gösterir. Her öğrenci kendi bölümünün staj sekmesindeki formları kullanmalıdır.
""")

    with open(os.path.join(mak_dir, "akran_danismanligi_ve_ogrenci_rehberi.md"), "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "Makine Fakültesi Akran Danışmanlığı ve Acil Eylem Planı"
kategori: "fakulteler_ve_bolumler"
fakulte: "Makine Fakültesi"
kaynak: "https://mak.yildiz.edu.tr/akran-danismanlari"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# Akran Danışmanlığı Sistemi ve Acil Durum Eylem Planı

Makine Fakültesi'ne yeni başlayan öğrencilerin oryantasyonu için üst sınıflardan seçilen akran danışmanları görev yapar.
Acil durumlarda Yıldız Yerleşkesi Makine Binası için hazırlanmış olan Acil Durum Eylem Planı uygulanır. İlgili ekipler Yangın Söndürme, İlkyardım, Tahliye ve Kurtarma ekiplerinden oluşmaktadır.
""")

    with open(os.path.join(mak_dir, "staj_ve_koop_genel_esaslari.md"), "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "Makine Fakültesi Staj ve KOOP Genel Esasları"
kategori: "fakulteler_ve_bolumler"
fakulte: "Makine Fakültesi"
kaynak: "https://mak.yildiz.edu.tr/stajlar"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# Makine Fakültesi Staj ve İşletmede Mesleki Eğitim (KOOP) Esasları

Fakültede toplam zorunlu staj süresi 60 iş günüdür. Stajlar Atölye, Üretim/İşletme ve Mesleki staj kategorilerine ayrılır.
Ayrıca başarılı son sınıf öğrencileri için İşletmede Mesleki Eğitim (KOOP) kapsamında tam zamanlı dönem içi sanayi çalışması imkânı bulunmaktadır.
""")

    # 1. Makine Mühendisliği
    mkm_dir = os.path.join(mak_dir, "makine_muhendisligi")
    generate_core_files(
        mkm_dir, "Makine Mühendisliği", "Makine Fakültesi", "MKM",
        lab_info="""Bölümde Termodinamik ve Isı Tekniği Laboratuvarı, Taşıt ve Motor Laboratuvarı, İmalat ve Talaşlı Şekillendirme Laboratuvarı, Akışkanlar Mekaniği Laboratuvarı, Malzeme Mekaniği ve Yorulma Laboratuvarı, Titreşim ve Dinamik Laboratuvarı, Otomotiv Laboratuvarı bulunmaktadır. Otomotiv stajı için özel tanımlı işyerleri mevcuttur.""",
        staj_info="""Makine Mühendisliği Bölümü'nde toplam 60 iş günü zorunlu staj vardır. Staj 1 (Atölye/İmalat - 30 gün) ve Staj 2 (İşletme/Organizasyon/Otomotiv - 30 gün) olarak tamamlanır. Staj başvuru takvimi güz ve bahar dönemlerinde ilan edilir.""",
        sss_list=[
            ("Otomotiv stajını nerede yapabilirim?", "Bölüm tarafından onaylanmış tanımlı otomotiv firmaları listesinde (`OTOMOTİV-STAJ YERLERİ.xlsx`) yer alan kurumlarda yapılabilir."),
            ("Çift Anadalda hangi dersler sayılır?", "Bölümün yayınladığı Çift Anadal Eşlenik Bölüm Dersleri listesindeki dersler geçerlidir."),
            ("MKM bitirme çalışması şartı nedir?", "Makine Tasarımı dersini başarmış olmak ve ilgili kredi sınırını sağlamak gerekir.")
        ]
    )
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=391&aid=97", os.path.join(mkm_dir, "bologna_ders_plani"), "%30 İngilizce", "Makine Mühendisliği")

    # 2. Endüstri Mühendisliği
    enm_dir = os.path.join(mak_dir, "endustri_muhendisligi")
    generate_core_files(
        enm_dir, "Endüstri Mühendisliği", "Makine Fakültesi", "ENM",
        lab_info="""Bölümde Ergonomi ve İş Etüdü Laboratuvarı, Benzetim ve Optimizasyon Laboratuvarı, Bilgisayarla Bütünleşik İmalat (CIM) Laboratuvarı ve Yöneylem Araştırması Laboratuvarı bulunmaktadır.""",
        staj_info="""Endüstri Mühendisliği Bölümü'nde 60 iş günü staj zorunluluğu vardır. Atölye Stajı (FR-1917) ve İşletme Stajı olarak iki aşamadan oluşur. Staj raporları için bölümün örnek staj defteri formatı kullanılır.""",
        sss_list=[
            ("Çok Disiplinli Tasarım Projesi (ÇDTP) nedir?", "Endüstri Mühendisliği öğrencilerinin diğer mühendislik disiplinleriyle ortak yürüttüğü kapsamlı tasarım projesidir (`project_temp-en.docx`)."),
            ("Bitirme çalışması yazım kılavuzu nerededir?", "Bölüm web sitesinde `end4000_tezyazim_tr_2025.docx` olarak mevcuttur.")
        ]
    )
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=45&aid=32", os.path.join(enm_dir, "bologna_ders_plani_yuzde30"), "%30 İngilizce", "Endüstri Mühendisliği")
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=405&aid=32", os.path.join(enm_dir, "bologna_ders_plani_yuzde100"), "%100 İngilizce", "Endüstri Mühendisliği")

    # 3. Mekatronik Mühendisliği
    mkt_dir = os.path.join(mak_dir, "mekatronik_muhendisligi")
    generate_core_files(
        mkt_dir, "Mekatronik Mühendisliği", "Makine Fakültesi", "MKT",
        lab_info="""Bölümde Robotik ve İleri Otomasyon Laboratuvarı, Gömülü Sistemler ve Mikrodenetleyici Laboratuvarı, Algılayıcılar ve Eyleyiciler Laboratuvarı, Hidrolik-Pnömatik Laboratuvarı ve Mekatronik Tasarım Atölyesi bulunmaktadır.""",
        staj_info="""Mekatronik Mühendisliği Bölümü'nde 60 gün staj (30 gün Donanım/İmalat, 30 gün Yazılım/Otomasyon) zorunludur. Öğrenciler mülakat listesi ve staj defteri örneğine göre evrak teslim eder.""",
        sss_list=[
            ("Mekatronik Sistemi Tasarımı (MST) ile Bitirme Çalışması farkı nedir?", "MST (güz dönemi) bitirme çalışmasının önkoşulu olup kapsamlı tasarım önerisi ve detaylı iş planı sunulmasını gerektirir. Bitirme Çalışması (bahar) ise fiziksel prototip veya simülasyon çıktısını kapsar."),
            ("MST ve Bitirme kılavuzları nereden temin edilir?", "Bölüm web sitesinde yayınlanan 2026-2027 Güz MST Kılavuzu ve Bitirme Çalışması Kılavuzu takip edilmelidir.")
        ]
    )
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=46&aid=33", os.path.join(mkt_dir, "bologna_ders_plani_yuzde30"), "%30 İngilizce", "Mekatronik Mühendisliği")
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=404&aid=33", os.path.join(mkt_dir, "bologna_ders_plani_yuzde100"), "%100 İngilizce", "Mekatronik Mühendisliği")

    print("=== MAKINE FAKULTESI INTEGRATION COMPLETED ===")

if __name__ == "__main__":
    run()
