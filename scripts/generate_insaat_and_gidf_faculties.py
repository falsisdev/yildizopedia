import os
import re
import ssl
import json
import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from pathlib import Path

ctx = ssl._create_unverified_context()
BASE_DIR = Path(__file__).resolve().parent.parent

def get_soup(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
    with urllib.request.urlopen(req, context=ctx, timeout=25) as resp:
        return BeautifulSoup(resp.read().decode('utf-8', errors='ignore'), 'html.parser')

def fetch_bologna_curriculum(bologna_url, output_dir, prog_title, dept_name):
    print(f"=== BOLOGNA ÇEKİLİYOR: {dept_name} ({prog_title}) ===")
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

    # Olası varyasyonlar (boşluk sayıları vb.)
    def find_section(keywords):
        for sec in curriculum.keys():
            if all(k.lower() in sec.lower() for k in keywords):
                return sec
        return None

    semester_definitions = [
        (1, "1_yariyil.md", "1. Yarıyıl (Güz)", ['1.yıl', 'güz']),
        (2, "2_yariyil.md", "2. Yarıyıl (Bahar)", ['1.yıl', 'bahar']),
        (3, "3_yariyil.md", "3. Yarıyıl (Güz)", ['2.yıl', 'güz']),
        (4, "4_yariyil.md", "4. Yarıyıl (Bahar)", ['2.yıl', 'bahar']),
        (5, "5_yariyil.md", "5. Yarıyıl (Güz)", ['3.yıl', 'güz']),
        (6, "6_yariyil.md", "6. Yarıyıl (Bahar)", ['3.yıl', 'bahar']),
        (7, "7_yariyil.md", "7. Yarıyıl (Güz)", ['4.yıl', 'güz']),
        (8, "8_yariyil.md", "8. Yarıyıl (Bahar)", ['4.yıl', 'bahar'])
    ]

    all_courses = []
    prereqs = []
    
    for sem_num, filename, display_name, kw in semester_definitions:
        sec_name = find_section(kw)
        courses = curriculum.get(sec_name, []) if sec_name else []
        filepath = os.path.join(output_dir, filename)
        
        tot_ects = 0.0
        tot_credit = 0.0
        for c in courses:
            try:
                tot_ects += float(c['ects'].replace(',', '.'))
            except Exception:
                pass
            try:
                tot_credit += float(c['credit'].replace(',', '.'))
            except Exception:
                pass

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
        print(f"Oluşturuldu: {filepath}")

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
    smd.append("Bölümün teknik, mesleki ve sosyal seçimlik dersleri Bologna Bilgi Paketi uyarınca dönem bazlı olarak aşağıda listelenmiştir:\n")
    
    elective_sections = [k for k in curriculum.keys() if 'seçmeli' in k.lower() or 'secmeli' in k.lower()]
    for es in elective_sections:
        smd.append(f"\n### 📚 {es}")
        smd.append("| Ders Kodu | Ders Adı | Kredi | AKTS |")
        smd.append("| :--- | :--- | :---: | :---: |")
        for c in curriculum[es]:
            c_link = f"[{c['name']}]({c['link']})" if c['link'] else c['name']
            smd.append(f"| **{c['code']}** | {c_link} | {c['credit']} | **{c['ects']}** |")
    
    with open(sec_file, 'w', encoding='utf-8') as fp:
        fp.write("\n".join(smd))

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

def generate_department_core(
    dept_dir: str,
    dept_name: str,
    faculty_name: str,
    web_url: str,
    yerleske: str,
    baskan_info: str,
    staj_detay: str,
    lab_list: list,
    komisyon_list: list,
    sss_list: list
):
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

Yıldız Teknik Üniversitesi **{faculty_name}** bünyesinde yer alan {dept_name}, {yerleske} Yerleşkesi'nde modern araştırma laboratuvarları ve yetkin akademik kadrosuyla eğitim ve bilimsel faaliyetlerini sürdürmektedir.

## 🏛️ Yönetim
{baskan_info}

## 🌐 Resmî Bağlantılar
- **Web Sitesi:** [{web_url}]({web_url})
- **Yerleşke:** {yerleske} Kampüsü

## 🗂️ Bölüm Dokümantasyon Rehberi
- [Lisans Eğitim Yapısı](lisans_egitim_yapisi.md)
- [Staj, Tasarım ve Bitirme Esasları](staj_tasarim_ve_bitirme_esaslari.md)
- [Laboratuvarlar ve Araştırma](laboratuvarlar_ve_arastirma.md)
- [Komisyonlar ve Öğrenci Danışmanlığı](komisyonlar_ve_ogrenci_danismanligi.md)
- [Lisansüstü Programlar](lisansustu_programlar.md)
- [Sıkça Sorulan Sorular](sikca_sorulan_sorular.md)
- [Bologna Ders Planı](bologna_ders_plani/README.md)
""")

    # 2. lisans_egitim_yapisi.md
    with open(os.path.join(dept_dir, "lisans_egitim_yapisi.md"), "w", encoding="utf-8") as fp:
        fp.write(f"""---
baslik: "{dept_name} Lisans Eğitim Yapısı"
kategori: "fakulteler_ve_bolumler"
fakulte: "{faculty_name}"
bolum: "{dept_name}"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bölüm Portalı)"
---

# {dept_name} Lisans Eğitim Yapısı

## 🎓 Program Genel Yapısı
- **Eğitim Süresi:** 4 Yıl (8 Yarıyıl) (+1 Yıl Zorunlu İngilizce Hazırlık)
- **Mezuniyet Kredisi:** Minimum 240 AKTS kredisi ve tüm zorunlu/seçmeli derslerin başarıyla tamamlanması.
- **Akademik Başarı:** Mezuniyet için Ağırlıklı Genel Not Ortalamasının (AGNO) en az 2.00 / 4.00 olması şarttır.
- **Ders Grupları:**
  - Temel Fen ve Matematik Dersleri (Matematik, Fizik, Kimya)
  - Temel Mühendislik Dersleri (Mekanik, Mukavemet, Malzeme vb.)
  - Mesleki Uzmanlık ve Tasarım Dersleri
  - Sosyal ve Üniversite Seçmeli Dersleri

## 📚 Hazırlık ve Dil Koşulları
- Bölüm öğretim planı gereğince öğrenciler İYS (İngilizce Yeterlik Sınavı) ile hazırlığı geçmeli veya hazırlık sınıfını başarıyla tamamlamalıdır.
""")

    # 3. laboratuvarlar_ve_arastirma.md
    with open(os.path.join(dept_dir, "laboratuvarlar_ve_arastirma.md"), "w", encoding="utf-8") as fp:
        fp.write(f"""---
baslik: "{dept_name} Laboratuvarlar ve Araştırma Altyapısı"
kategori: "fakulteler_ve_bolumler"
fakulte: "{faculty_name}"
bolum: "{dept_name}"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bölüm Portalı)"
---

# {dept_name} Laboratuvarlar ve Araştırma Altyapısı

Bölümümüz, lisans eğitimindeki pratik uygulamaları ve lisansüstü bilimsel araştırmaları destekleyen donanımlı laboratuvarlara sahiptir:

## 🔬 Aktif Laboratuvarlar
""")
        for lab in lab_list:
            fp.write(f"### 📍 {lab['name']}\n")
            fp.write(f"- **Açıklama:** {lab['desc']}\n")
            fp.write(f"- **Kullanım:** Lisans deneyleri, bitirme tezleri ve Ar-Ge projeleri.\n\n")

    # 4. staj_tasarim_ve_bitirme_esaslari.md
    with open(os.path.join(dept_dir, "staj_tasarim_ve_bitirme_esaslari.md"), "w", encoding="utf-8") as fp:
        fp.write(f"""---
baslik: "{dept_name} Staj, Tasarım ve Bitirme Esasları"
kategori: "fakulteler_ve_bolumler"
fakulte: "{faculty_name}"
bolum: "{dept_name}"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bölüm Portalı)"
---

# {dept_name} Staj, Tasarım ve Bitirme Esasları

## 🛠️ Staj Esasları ve Yükümlülükler
{staj_detay}

## 📐 Tasarım ve Bitirme Projesi Esasları
- **Bitirme Tezi:** Lisans eğitiminin son yılında (7. veya 8. yarıyıl) akademik danışman yönetiminde bağımsız bir mühendislik problemi çözülür.
- **Jüri Değerlendirmesi:** Hazırlanan bitirme çalışması tez yazım kılavuzuna uygun olarak teslim edilir ve akademik jüri önünde sözlü sunumla savunulur.
""")

    # 5. komisyonlar_ve_ogrenci_danismanligi.md
    with open(os.path.join(dept_dir, "komisyonlar_ve_ogrenci_danismanligi.md"), "w", encoding="utf-8") as fp:
        fp.write(f"""---
baslik: "{dept_name} Komisyonlar ve Öğrenci Danışmanlığı"
kategori: "fakulteler_ve_bolumler"
fakulte: "{faculty_name}"
bolum: "{dept_name}"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bölüm Portalı)"
---

# {dept_name} Komisyonlar ve Öğrenci Danışmanlığı

Bölümün idari, akademik ve öğrenci odaklı süreçleri ihtisas komisyonları tarafından yürütülmektedir:

## 📋 Bölüm Komisyonları
""")
        for kom in komisyon_list:
            fp.write(f"- **{kom['name']}:** {kom['desc']}\n")
        
        fp.write("""
## 🧑‍🏫 Akademik Danışmanlık
- Her öğrenciye kayıt anında bir öğretim üyesi akademik danışman olarak atanır.
- Ders seçimleri, intibaklar, ÇAP/Yandal başvuruları ve mazeret işlemleri danışman onayıyla Öğrenci İşleri Bilgi Sistemi (OBS) üzerinden yürütülür.
""")

    # 6. lisansustu_programlar.md
    with open(os.path.join(dept_dir, "lisansustu_programlar.md"), "w", encoding="utf-8") as fp:
        fp.write(f"""---
baslik: "{dept_name} Lisansüstü Programlar"
kategori: "fakulteler_ve_bolumler"
fakulte: "{faculty_name}"
bolum: "{dept_name}"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bölüm Portalı)"
---

# {dept_name} Lisansüstü Programlar

YTÜ Fen Bilimleri Enstitüsü (FBE) koordinatörlüğünde bölümümüz bünyesinde yürütülen tezli yüksek lisans ve doktora programları:

- **Tezli Yüksek Lisans (M.Sc.):** İleri mühendislik dersleri ve bilimsel tez çalışması (120 AKTS).
- **Doktora (Ph.D.):** Özgün bilimsel araştırma, yeterlik sınavı, tez izleme komitesi ve doktora tezi (240 AKTS).
""")

    # 7. sikca_sorulan_sorular.md
    with open(os.path.join(dept_dir, "sikca_sorulan_sorular.md"), "w", encoding="utf-8") as fp:
        fp.write(f"""---
baslik: "{dept_name} Sıkça Sorulan Sorular"
kategori: "fakulteler_ve_bolumler"
fakulte: "{faculty_name}"
bolum: "{dept_name}"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bölüm Portalı)"
---

# {dept_name} Sıkça Sorulan Sorular (SSS)

""")
        for sss in sss_list:
            fp.write(f"### ❓ {sss['q']}\n")
            fp.write(f"**Cevap:** {sss['a']}\n\n")

def generate_all():
    print("🚀 İNŞAAT VE GEMİ İNŞAATI FAKÜLTELERİ ENTEGRASYONU BAŞLATILIYOR...")

    # -------------------------------------------------------------
    # 1. İNŞAAT FAKÜLTESİ
    # -------------------------------------------------------------
    ins_dir = BASE_DIR / "05_fakulteler_ve_bolumler" / "insaat_fakultesi"
    os.makedirs(ins_dir, exist_ok=True)

    # 1.1 Fakülte README
    with open(ins_dir / "README.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "İnşaat Fakültesi Genel Tanıtımı ve Teşkilat Yapısı"
kategori: "fakulteler_ve_bolumler"
fakulte: "İnşaat Fakültesi"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# İnşaat Fakültesi

Yıldız Teknik Üniversitesi **İnşaat Fakültesi**, 1911 yılındaki *Kondüktör Mekteb-i Âlisi* köklerine dayanan üniversitemizin kurucu fakültelerindendir. Davutpaşa Yerleşkesi'ndeki modern Tarihi Kışla ve laboratuvar kompleksinde eğitim ve araştırma faaliyetlerini sürdürmektedir.

## 🏛️ Fakülte Bölümleri
- [İnşaat Mühendisliği](insaat_muhendisligi/README.md)
- [Çevre Mühendisliği](cevre_muhendisligi/README.md)
- [Harita Mühendisliği (Geomatik)](harita_muhendisligi/README.md)

## 🗂️ Fakülte Dokümantasyon Rehberi
- [Dekanlık ve Teşkilat Yapısı](dekanlik_ve_teskilat_yapisi.md)
- [Fakülte Sıkça Sorulan Sorular](fakulte_sikca_sorulan_sorular.md)
- [Akran Danışmanlığı ve Öğrenci Rehberi](akran_danismanligi_ve_ogrenci_rehberi.md)
- [Fakülte Staj Uygulama İlkeleri (DD-074)](staj_uygulama_ilkeleri.md)
""")

    # 1.2 Dekanlık ve Teşkilat Yapısı
    with open(ins_dir / "dekanlik_ve_teskilat_yapisi.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "İnşaat Fakültesi Dekanlığı ve Yönetim Kadrosu"
kategori: "fakulteler_ve_bolumler"
fakulte: "İnşaat Fakültesi"
kaynak: "https://ins.yildiz.edu.tr/yonetim"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# İnşaat Fakültesi Dekanlığı ve Yönetim Kadrosu

## 👥 Üst Yönetim
- **Dekan Vekili:** Prof. Dr. Uğur KURT (E-posta: `ukurt@yildiz.edu.tr`, Tel: `0212 383 5100`)
- **Dekan Yardımcısı (Ar-Ge):** Prof. Dr. Barış SEVİM (E-posta: `basevim@yildiz.edu.tr`)
- **Dekan Yardımcısı (Eğitim-Öğretim):** Prof. Dr. Metin SOYCAN (E-posta: `soycan@yildiz.edu.tr`)
- **Fakülte Sekreteri:** İlkay AŞIK

## 🏛️ Kurullar ve Yetkiler
- **Fakülte Kurulu:** Dekan başkanlığında tüm bölüm başkanları ve fakülte öğretim üyesi temsilcilerinden oluşur.
- **Fakülte Yönetim Kurulu:** Öğrenci mazeretleri, intibaklar, staj onayları ve idari kararları alan yetkili organdır.
- **Yerleşke:** YTÜ Davutpaşa Yerleşkesi, Esenler / İstanbul.
""")

    # 1.3 Fakülte SSS
    with open(ins_dir / "fakulte_sikca_sorulan_sorular.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "İnşaat Fakültesi Sıkça Sorulan Sorular"
kategori: "fakulteler_ve_bolumler"
fakulte: "İnşaat Fakültesi"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# İnşaat Fakültesi Sıkça Sorulan Sorular

### ❓ Fakülte hangi yerleşkededir?
**Cevap:** İnşaat Fakültesi ve tüm bölümleri (İnşaat, Çevre, Harita) Davutpaşa Yerleşkesi'ndedir.

### ❓ Fakülte staj esasları nelerdir?
**Cevap:** Fakültemiz Senato onaylı DD-074 kodlu İnşaat Fakültesi Staj Uygulama İlkeleri'ne tabidir. Sigorta işlemleri için staj başlangıcından en az 10 gün önce evrakların teslim edilmesi şarttır.

### ❓ Çift Anadal (ÇAP) ve Yandal olanakları nelerdir?
**Cevap:** İnşaat Fakültesi bölümleri birbirleri arasında ve Makine, Mimarlık, Kimya-Metalurji fakültelerinin ilgili bölümleriyle aktif ÇAP ve Yandal protokollerine sahiptir. Başvuru için AGNO'nun en az 3.00 olması gerekir.
""")

    # 1.4 Akran Danışmanlığı
    with open(ins_dir / "akran_danismanligi_ve_ogrenci_rehberi.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "İnşaat Fakültesi Akran Danışmanlığı ve Öğrenci Rehberi"
kategori: "fakulteler_ve_bolumler"
fakulte: "İnşaat Fakültesi"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# İnşaat Fakültesi Akran Danışmanlığı ve Öğrenci Rehberi

Fakültemize yeni başlayan 1. sınıf öğrencilerine üniversite yaşamına, kampüse ve bölüm derslerine uyum sağlamaları amacıyla üst sınıflardan seçilen deneyimli akran danışmanlar rehberlik eder.

- **Ders Kayıtları Rehberliği:** USİS/OBS üzerinden ders seçimi ve çakışma durumlarında yönlendirme.
- **Laboratuvar Güvenliği:** Davutpaşa laboratuvarlarında İSG kuralları ve güvenlik formları bilgilendirmesi.
- **Öğrenci Kulüpleri:** Yapı Kulübü, Çevre Kulübü ve Geomatik Kulübü etkinliklerine katılım desteği.
""")

    # 1.5 Staj Uygulama İlkeleri
    with open(ins_dir / "staj_uygulama_ilkeleri.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "İnşaat Fakültesi Staj Uygulama İlkeleri (DD-074)"
kategori: "fakulteler_ve_bolumler"
fakulte: "İnşaat Fakültesi"
kaynak: "https://ins.yildiz.edu.tr/staj"
guvenilirlik_duzeyi: "Tier 1 / Tier 2 (Senato Esası & Fakülte Portalı)"
---

# İnşaat Fakültesi Staj Uygulama İlkeleri (DD-074)

1. **Staj Süresi:** Bölüm kurullarınca belirlenen şantiye, ofis, arazi ve laboratuvar stajlarının toplamı ilgili bölüm yönergesinde belirtilen iş gününden az olamaz.
2. **Başvuru Takvimi:** Staj başlangıç tarihinden en geç 10 gün önce FR-1877 Staj Başvuru Formu ve ilgili evraklar Fakülte Öğrenci İşleri Bürosuna teslim edilmelidir.
3. **Değerlendirme:** Staj bitiminden itibaren en geç 1 ay içinde staj sicil fişi ve staj defteri bölüm staj komisyonuna imza karşılığı teslim edilir.
""")

    # -------------------------------------------------------------
    # 2. GEMİ İNŞAATI VE DENİZCİLİK FAKÜLTESİ (GİDF)
    # -------------------------------------------------------------
    gidf_dir = BASE_DIR / "05_fakulteler_ve_bolumler" / "gemi_insaati_ve_denizcilik_fakultesi"
    os.makedirs(gidf_dir, exist_ok=True)

    # 2.1 Fakülte README
    with open(gidf_dir / "README.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "Gemi İnşaatı ve Denizcilik Fakültesi Tanıtımı ve Yönetimi"
kategori: "fakulteler_ve_bolumler"
fakulte: "Gemi İnşaatı ve Denizcilik Fakültesi"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# Gemi İnşaatı ve Denizcilik Fakültesi (GİDF)

Yıldız Teknik Üniversitesi **Gemi İnşaatı ve Denizcilik Fakültesi (GİDF)**, Türkiye'nin denizcilik ve gemi inşa sanayisine yön veren köklü bir eğitim kurumudur. Yıldız (Beşiktaş) Merkez Yerleşkesi'nde deniz manzaralı tarihi binalarda eğitim vermektedir.

## 🏛️ Fakülte Bölümleri
- [Gemi İnşaatı ve Gemi Makineleri Mühendisliği](gemi_insaati_ve_gemi_makineleri_muhendisligi/README.md)
- [Gemi Makineleri İşletme Mühendisliği](gemi_makineleri_isletme_muhendisligi/README.md)

## 🗂️ Fakülte Dokümantasyon Rehberi
- [Dekanlık ve Teşkilat Yapısı](dekanlik_ve_teskilat_yapisi.md)
- [Fakülte Sıkça Sorulan Sorular](fakulte_sikca_sorulan_sorular.md)
- [Akran Danışmanlığı ve Öğrenci Rehberi](akran_danismanligi_ve_ogrenci_rehberi.md)
- [Staj ve Deniz Eğitimi Esasları (STCW)](staj_ve_deniz_egitimi_esaslari.md)
""")

    # 2.2 Dekanlık ve Teşkilat Yapısı
    with open(gidf_dir / "dekanlik_ve_teskilat_yapisi.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "Gemi İnşaatı ve Denizcilik Fakültesi Dekanlığı ve Yönetim Kadrosu"
kategori: "fakulteler_ve_bolumler"
fakulte: "Gemi İnşaatı ve Denizcilik Fakültesi"
kaynak: "https://gidf.yildiz.edu.tr/yonetim"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# Gemi İnşaatı ve Denizcilik Fakültesi Dekanlığı

## 👥 Üst Yönetim
- **Dekan:** Prof. Dr. Serkan EKİNCİ (E-posta: `sekinci@yildiz.edu.tr`)
- **Dekan Yardımcısı (Eğitim-Öğretim):** Doç. Dr. Asım Sinan KARAKURT
- **Dekan Yardımcısı (Ar-Ge):** Doç. Dr. Ahmet YURTSEVEN
- **Fakülte Sekreteri:** Elgin KÖKSAL

## 🏛️ Kurullar ve Komisyonlar
- **Fakülte Kurulu & Yönetim Kurulu:** Fakülte akademik ve idari organları.
- **Kalite ve Akreditasyon Komisyonu:** STCW ve MÜDEK akreditasyon süreçlerini yürütür.
- **Yerleşke:** YTÜ Yıldız (Merkez/Beşiktaş) Yerleşkesi, Barbaros Bulvarı, Beşiktaş / İstanbul.
""")

    # 2.3 Fakülte SSS
    with open(gidf_dir / "fakulte_sikca_sorulan_sorular.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "Gemi İnşaatı ve Denizcilik Fakültesi SSS"
kategori: "fakulteler_ve_bolumler"
fakulte: "Gemi İnşaatı ve Denizcilik Fakültesi"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# Gemi İnşaatı ve Denizcilik Fakültesi Sıkça Sorulan Sorular

### ❓ Fakülte hangi kampüstedir?
**Cevap:** Fakültemiz İstanbul'un merkezinde, Beşiktaş Yıldız Yerleşkesi'ndedir. Hazırlık eğitimi Davutpaşa'da verilir; lisans meslek dersleri Yıldız Kampüsü'ndedir.

### ❓ Üniforma giyme zorunluluğu var mıdır?
**Cevap:** Günlük derslerde üniforma zorunluluğu bulunmamaktadır. Ancak resmî törenlerde, denizcilik etkinliklerinde ve deniz stajı süreçlerinde denizcilik örf ve adetlerine uygun üniforma giyilir.

### ❓ STCW ve Gemiadamı Cüzdanı veriliyor mu?
**Cevap:** GMİM ve GİM bölümleri Ulaştırma ve Altyapı Bakanlığı Denizcilik Genel Müdürlüğü denetiminde STCW sözleşmesine uygun eğitim verir. Gerekli açık deniz stajlarını ve GASM sınavlarını tamamlayan mezunlar Uzakyol Vardiya Mühendisi ehliyeti alabilirler.
""")

    # 2.4 Akran Danışmanlığı
    with open(gidf_dir / "akran_danismanligi_ve_ogrenci_rehberi.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "GİDF Akran Danışmanlığı ve Öğrenci Rehberi"
kategori: "fakulteler_ve_bolumler"
fakulte: "Gemi İnşaatı ve Denizcilik Fakültesi"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# GİDF Akran Danışmanlığı ve Öğrenci Rehberi

- **Liman Cüzdanı Süreci:** Öğrencilere liman başkanlıklarından gemiadamı cüzdanı çıkarma, sağlık raporu alma ve emniyet tahkikatı adımlarında üst sınıf rehberliği.
- **Tersane ve Gemi Stajları:** Tersane ortamında İSG kuralları, tulum/baret kullanımı ve staj defteri yazımı mentörlüğü.
- **Kulüpler:** Denizcilik Kulübü ve Gemi İnşaatı Topluluğu teknik gezileri ve kariyer günleri.
""")

    # 2.5 Staj ve Deniz Eğitimi
    with open(gidf_dir / "staj_ve_deniz_egitimi_esaslari.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "GİDF Staj ve Deniz Eğitimi Esasları (STCW)"
kategori: "fakulteler_ve_bolumler"
fakulte: "Gemi İnşaatı ve Denizcilik Fakültesi"
guvenilirlik_duzeyi: "Tier 1 / Tier 2 (Resmi Fakülte Esasları)"
---

# GİDF Staj ve Deniz Eğitimi Esasları

1. **Gemi İnşaatı ve Gemi Makineleri Mühendisliği (GİM):**
   - Atölye ve Tersane stajları (minimum 60 iş günü)
   - Başvurular staja başlamadan en geç 14 gün önce online sisteme yüklenmelidir.
2. **Gemi Makineleri İşletme Mühendisliği (GMİM):**
   - **Atölye Stajı:** 150 iş günü atölye/fabrika/tersane uygulaması
   - **Uzakyol Gemi Stajı:** Uluslararası sularda çalışan ticari gemilerde en az 6 ay (180 gün) açık deniz stajı.
   - GASM (Gemiadamları Sınav Merkezi) sınavlarına giriş için zorunlu staj tamamlama şartı.
""")

    # -------------------------------------------------------------
    # 3. BÖLÜM MÜFREDATLARI (BOLOGNA)
    # -------------------------------------------------------------
    bologna_tasks = [
        # İnşaat Müh %30
        ("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=40&aid=28",
         ins_dir / "insaat_muhendisligi" / "bologna_ders_plani",
         "%30 İngilizce", "İnşaat Mühendisliği"),
        # İnşaat Müh %100
        ("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=397&aid=28",
         ins_dir / "insaat_muhendisligi" / "bologna_ders_plani_yuzde100",
         "%100 İngilizce", "İnşaat Mühendisliği"),
        # Çevre Müh %30
        ("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=43&aid=29",
         ins_dir / "cevre_muhendisligi" / "bologna_ders_plani",
         "%30 İngilizce", "Çevre Mühendisliği"),
        # Harita Müh %30
        ("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=44&aid=30",
         ins_dir / "harita_muhendisligi" / "bologna_ders_plani",
         "%30 İngilizce", "Harita Mühendisliği"),
        # GİGM Müh %30
        ("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=48&aid=35",
         gidf_dir / "gemi_insaati_ve_gemi_makineleri_muhendisligi" / "bologna_ders_plani",
         "%30 İngilizce", "Gemi İnşaatı ve Gemi Makineleri Mühendisliği"),
        # GMİM %30
        ("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=141&aid=36",
         gidf_dir / "gemi_makineleri_isletme_muhendisligi" / "bologna_ders_plani",
         "%30 İngilizce", "Gemi Makineleri İşletme Mühendisliği"),
    ]

    for b_url, b_out, b_prog, b_name in bologna_tasks:
        fetch_bologna_curriculum(b_url, b_out, b_prog, b_name)

    # -------------------------------------------------------------
    # 4. BÖLÜM ÇEKİRDEK DOKÜMANLARI
    # -------------------------------------------------------------
    # 4.1 İnşaat Mühendisliği
    generate_department_core(
        dept_dir=str(ins_dir / "insaat_muhendisligi"),
        dept_name="İnşaat Mühendisliği",
        faculty_name="İnşaat Fakültesi",
        web_url="https://inm.yildiz.edu.tr",
        yerleske="Davutpaşa",
        baskan_info="""- **Bölüm Başkanı:** Prof. Dr. Bilge DORAN
- **Bölüm Başkan Yardımcıları:** Doç. Dr. Yurdakul AYGÖRMEZ, Doç. Dr. Abdullah H. AKCA""",
        staj_detay="""- **Toplam Staj Süresi:** 60 İş Günü (Şantiye Stajı: 30 gün, Büro/Ofis Stajı: 30 gün)
- **Önkoşul:** Şantiye stajı için Yapı Malzemeleri ve Temel Mühendislik derslerinin tamamlanmış olması tavsiye edilir.
- **Teslim:** Staj bitiminden sonraki 30 gün içinde staj defteri Bölüm Staj Komisyonuna teslim edilir.""",
        lab_list=[
            {"name": "Prof. Dr. Kutay Özaydın Zemin Mekaniği Laboratuvarı", "desc": "Geoteknik zemin deneyleri, konsolidasyon, üç eksenli basınç deney sistemleri."},
            {"name": "Yapı ve Depem Mühendisliği Laboratuvarı", "desc": "Büyük ölçekli yapı elemanları test sistemleri, sarsma tablası ve betonarme deney düzenekleri."},
            {"name": "Hidrolik ve Kıyı Liman Mühendisliği Laboratuvarı", "desc": "Açık kanal akım düzenekleri, dalga kanalları ve savak deney setleri."},
            {"name": "Yapı Malzemeleri Laboratuvarı", "desc": "Çimento, agrega, taze ve sertleşmiş beton testleri, ultrases ve tahribatsız muayene altyapısı."}
        ],
        komisyon_list=[
            {"name": "Staj Komisyonu", "desc": "Şantiye ve büro staj başvurularını, firma uygunluğunu ve staj defterlerini inceler."},
            {"name": "İntibak ve Muafiyet Komisyonu", "desc": "Yatay geçiş, DGS ve Erasmus intibaklarını karara bağlar."},
            {"name": "Eğitim ve Müfredat Komisyonu", "desc": "Bologna ders planları ve MÜDEK akreditasyon kriterlerini yönetir."},
            {"name": "Bitirme Çalışması Komisyonu", "desc": "Bitirme tezi konularını ve jüri dağılımlarını koordine eder."}
        ],
        sss_list=[
            {"q": "Şantiye ve büro stajı aynı yerde yapılabilir mi?", "a": "İlgili firma hem şantiye hem proje ofisi barındırıyorsa ve yetkili inşaat mühendisi imzası bulunuyorsa ayrı tarihlerde yapılabilir."},
            {"q": "İnşaat Mühendisliği öğretim dili nedir?", "a": "Bölümümüzde hem %30 İngilizce hem de %100 İngilizce lisans programı bulunmaktadır."},
            {"q": "Derslerde devam zorunluluğu nedir?", "a": "YTÜ Lisans Yönetmeliği uyarınca teorik derslerin en az %70'ine, uygulamaların en az %80'ine devam şarttır."}
        ]
    )

    # 4.2 Çevre Mühendisliği
    generate_department_core(
        dept_dir=str(ins_dir / "cevre_muhendisligi"),
        dept_name="Çevre Mühendisliği",
        faculty_name="İnşaat Fakültesi",
        web_url="https://cem.yildiz.edu.tr",
        yerleske="Davutpaşa",
        baskan_info="""- **Bölüm Başkanı:** Prof. Dr. Yaşar AVŞAR (E-posta: `avsar@yildiz.edu.tr`)
- **Bölüm Başkan Yardımcısı:** Prof. Dr. Ömer APAYDIN (E-posta: `apaydin@yildiz.edu.tr`)""",
        staj_detay="""- **Toplam Staj Süresi:** 60 İş Günü (Laboratuvar/Tesis Stajı ve İşletme/Büro Stajı)
- **Mevzuat:** DD-071 Çevre Mühendisliği Bölümü Staj Uygulama Esasları geçerlidir.
- **Sigorta İşlemleri:** Staja başlamadan en az 10 gün önce evrakların fakülteye teslim edilmesi zorunludur.""",
        lab_list=[
            {"name": "Çevre Kimyası ve Analiz Laboratuvarı", "desc": "Su, atıksu, spektrofotometrik ve kromatografik çevre analiz cihazları."},
            {"name": "Çevre Mikrobiyolojisi Laboratuvarı", "desc": "Biyolojik arıtma, patojen tespiti ve mikrobiyolojik kültür altyapısı."},
            {"name": "Hava Kirliliği ve Kontrolü Laboratuvarı", "desc": "Baca gazı emisyon ölçümleri ve partikül madde analiz düzenekleri."},
            {"name": "Katı Atık ve Toprak Kirliliği Laboratuvarı", "desc": "Kompostlaştırma, sızıntı suyu analizleri ve katı atık karakterizasyonu."}
        ],
        komisyon_list=[
            {"name": "Staj Komisyonu", "desc": "Arıtma tesisi ve çevre danışmanlık firması stajlarını onaylar."},
            {"name": "MÜDEK ve Kalite Komisyonu", "desc": "Program eğitim amaçları ve çıktılarını denetler."},
            {"name": "Dış İlişkiler ve Erasmus Komisyonu", "desc": "Yurtdışı üniversite eşdeğerlik ve değişim protokollerini yürütür."}
        ],
        sss_list=[
            {"q": "Çevre Mühendisliği stajı nerelerde yapılabilir?", "a": "İSKİ vb. içme suyu ve atıksu arıtma tesislerinde, çevre laboratuvarlarında, belediyelerin çevre müdürlüklerinde ve endüstriyel tesislerin arıtma ünitelerinde yapılabilir."},
            {"q": "Bölümde ÇAP imkânı var mıdır?", "a": "Evet; İnşaat, Kimya, Biyomühendislik ve Kimya Mühendisliği ile aktif ÇAP anlaşmaları mevcuttur."}
        ]
    )

    # 4.3 Harita Mühendisliği (Geomatik)
    generate_department_core(
        dept_dir=str(ins_dir / "harita_muhendisligi"),
        dept_name="Harita Mühendisliği",
        faculty_name="İnşaat Fakültesi",
        web_url="https://hrm.yildiz.edu.tr",
        yerleske="Davutpaşa",
        baskan_info="""- **Bölüm Başkanı:** Prof. Dr. Cüneyt AYDIN (E-posta: `caydin@yildiz.edu.tr`)
- **Bölüm Başkan Yardımcıları:** Prof. Dr. Burak AKPINAR, Dr. Öğr. Üyesi Barış SÜLEYMANOĞLU""",
        staj_detay="""- **Toplam Staj Süresi:** 60 İş Günü (Arazi Ölçme Stajı ve Büro/CBS/Fotogrametri Stajı)
- **Staj Alanları:** Tapu Kadastro Müdürlükleri, İller Bankası, Harita Genel Müdürlüğü, belediyeler ve özel harita/CBS şirketleri.
- **Zamanlama:** 4. ve 6. yarıyıl sonu yaz dönemlerinde gerçekleştirilir.""",
        lab_list=[
            {"name": "Fotogrametri ve Lidar Laboratuvarı", "desc": "İHA fotogrametrisi, 3B lazer tarama ve dijital hava fotoğrafları işleme istasyonları."},
            {"name": "Uzaktan Algılama ve CBS Laboratuvarı", "desc": "Uydu görüntüsü analizi, mekânsal veri analitiği ve ArcGIS/QGIS altyapısı."},
            {"name": "Jeodezi ve GNSS Laboratuvarı", "desc": "Hassas GNSS/GPS alıcıları, gravimetreler ve yerkabuğu deformasyon izleme sistemleri."},
            {"name": "Ölçme Tekniği Alet Parkı", "desc": "Total station, dijital nivo ve elektronik teodolit ölçme ekipmanları."}
        ],
        komisyon_list=[
            {"name": "Staj Komisyonu", "desc": "Arazi ve büro staj başvurularını ve harita defterlerini inceler."},
            {"name": "Ölçme Aletleri ve Kamp Komisyonu", "desc": "Arazi ölçme kampları ve teçhizat lojistiğini organize eder."},
            {"name": "Akreditasyon Komisyonu", "desc": "MÜDEK ve uluslararası mühendislik denkliklerini yürütür."}
        ],
        sss_list=[
            {"q": "Harita Mühendisliği ile Geomatik Mühendisliği aynı mıdır?", "a": "Evet; Harita Mühendisliği uluslararası terminolojide Geomatics Engineering olarak adlandırılmaktadır ve CBS, uydu navigasyonu ve fotogrametriyi kapsar."},
            {"q": "Arazi uygulamaları nasıl yapılmaktadır?", "a": "Dersler kapsamında Davutpaşa Kampüsü'nün geniş arazisinde total station ve GNSS ölçümleriyle pratik saha uygulamaları gerçekleştirilir."}
        ]
    )

    # 4.4 Gemi İnşaatı ve Gemi Makineleri Mühendisliği
    generate_department_core(
        dept_dir=str(gidf_dir / "gemi_insaati_ve_gemi_makineleri_muhendisligi"),
        dept_name="Gemi İnşaatı ve Gemi Makineleri Mühendisliği",
        faculty_name="Gemi İnşaatı ve Denizcilik Fakültesi",
        web_url="https://gim.yildiz.edu.tr",
        yerleske="Yıldız (Beşiktaş)",
        baskan_info="""- **Bölüm Başkanı:** Prof. Dr. Hüseyin YILMAZ
- **Bölüm Başkan Yardımcıları:** Doç. Dr. Taner ÇOŞGUN, Dr. Öğr. Üyesi Serdar Turgut İNCE""",
        staj_detay="""- **Toplam Staj Süresi:** 60 İş Günü (Tersane İmalat Stajı, Dizayn/Büro Stajı)
- **Başvuru Kuralı:** Staja başlamadan en az 14 gün önce online staj sistemine belgeler (FR-1877, FR-1323, FR-1936) yüklenmelidir.
- **Staj Yerleri:** Tersaneler, gemi tasarım büroları, klas kuruluşları (Türk Loydu vb.) ve marinler.""",
        lab_list=[
            {"name": "Gemi Hidrodinamiği ve Çekme Tankı Laboratuvarı", "desc": "Gemi direnç deneyleri, sevk sistemleri ve model tekne hidrodinamik testleri."},
            {"name": "Gemi Yapısal Mekaniği Laboratuvarı", "desc": "Gemi elemanları sonlu elemanlar analizi (FEA) ve mukavemet testleri."},
            {"name": "Bilgisayar Destekli Gemi Tasarım (CAD/CAM) Laboratuvarı", "desc": "Maxsurf, Rhino, NAPA ve AutoCAD gemi dizayn yazılımları istasyonları."}
        ],
        komisyon_list=[
            {"name": "Staj Komisyonu", "desc": "Tersane ve gemi dizayn ofisi stajlarını denetler."},
            {"name": "Eğitim ve Müfredat Komisyonu", "desc": "Bologna ders planları ve MÜDEK süreçlerini koordine eder."},
            {"name": "Bitirme ve Tasarım Projesi Komisyonu", "desc": "Gemi dizayn projeleri ve jüri değerlendirmelerini yürütür."}
        ],
        sss_list=[
            {"q": "Gemi İnşaatı Mühendisleri nerelerde çalışır?", "a": "Tersanelerde gemi ve yat inşa mühendisi, dizayn bürolarında gemi tasarımcısı, klas kuruluşlarında enspektör ve denizcilik şirketlerinde yönetici olarak çalışırlar."},
            {"q": "Bölüm hangi kampüstedir?", "a": "Hazırlık sınıfı hariç tüm mesleki eğitim ve laboratuvarlar Yıldız (Beşiktaş) Yerleşkesi'ndedir."}
        ]
    )

    # 4.5 Gemi Makineleri İşletme Mühendisliği
    generate_department_core(
        dept_dir=str(gidf_dir / "gemi_makineleri_isletme_muhendisligi"),
        dept_name="Gemi Makineleri İşletme Mühendisliği",
        faculty_name="Gemi İnşaatı ve Denizcilik Fakültesi",
        web_url="https://gmim.yildiz.edu.tr",
        yerleske="Yıldız (Beşiktaş)",
        baskan_info="""- **Bölüm Başkanı:** Prof. Dr. Ömer SAVAŞ (E-posta: `osavas@yildiz.edu.tr`, Tel: `0212 383 2940`)
- **Bölüm Başkan Yardımcıları:** Dr. Öğr. Üyesi Araks EKMEKÇİOĞLU, Doç. Dr. Kenan YİĞİT""",
        staj_detay="""- **Staj Türleri ve Süreleri:**
  - **150 İş Günü Atölye Stajı:** Tersanelerde veya gemi makineleri bakım onarım atölyelerinde mekanik, elektrik, kaynak ve torna-tesviye uygulamaları.
  - **180 Gün Uzakyol Gemi Stajı:** Uluslararası sularda çalışan ticari gemilerde vardiya mühendisliği açık deniz stajı.
- **Liman Cüzdanı:** Açık deniz stajına çıkacak öğrencilerin Liman Başkanlığı'ndan onaylı Gemiadamı Cüzdanı çıkarması zorunludur.
- **GASM:** Mezuniyet sonrası Uzakyol Vardiya Mühendisi ehliyeti için GASM sınavlarına girilir.""",
        lab_list=[
            {"name": "Gemi Makineleri Simülatör Laboratuvarı", "desc": "Tam ölçekli köprüüstü ve makine dairesi konsoluyla arıza ve işletim senaryoları."},
            {"name": "Gemi Dizel Motorları ve Güç Sistemleri Laboratuvarı", "desc": "Deniz dizel motorları, yakıt püskürtme sistemleri ve yardımcı makineler test ünitesi."},
            {"name": "Denizcilik Emniyet ve İleri Yangın Eğitim Merkezi", "desc": "STCW temel deniz emniyeti, filika kullanma ve yangınla mücadele simülasyonları."}
        ],
        komisyon_list=[
            {"name": "Açık Deniz Stajı Komisyonu", "desc": "180 günlük uzakyol gemi stajı gemi protokollerini ve staj defterlerini onaylar."},
            {"name": "Atölye Stajı Komisyonu", "desc": "150 günlük mekanik atölye stajını koordine eder."},
            {"name": "STCW ve Denizcilik Akreditasyon Komisyonu", "desc": "Ulaştırma Bakanlığı denetimlerini ve STCW eğitim standartlarını yönetir."}
        ],
        sss_list=[
            {"q": "Açık deniz stajı için gemi nasıl bulunur?", "a": "Bölümümüzün ve Fakültemizin anlaşmalı olduğu Türk ve yabancı bayraklı denizcilik armatörlük şirketleri her yıl yapılan mülakatlarla stajyer alımı gerçekleştirmektedir."},
            {"q": "Mezun olunca doğrudan çarkçıbaşı olunabilir mi?", "a": "Mezunlar öncelikle 'Uzakyol Vardiya Mühendisi' (4. veya 3. Çarkçı) olarak başlar; gerekli deniz hizmet sürelerini ve sınavları tamamladıkça 2. Mühendis ve Uzakyol Başmühendisi (Çarkçıbaşı) olurlar."},
            {"q": "Bölümde üniforma zorunluluğu var mı?", "a": "Derslerde zorunlu değildir; resmî tören ve deniz stajı boyunca denizcilik teamüllerine uygun üniforma giyilir."}
        ]
    )

    print("🎉 TÜM İNŞAAT VE GEMİ İNŞAATI FAKÜLTELERİ DOSYALARI EKSİKSİZ OLUŞTURULDU!")

if __name__ == "__main__":
    generate_all()
