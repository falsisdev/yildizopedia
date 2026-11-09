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
    brm.append("---")
    brm.append(f'baslik: "{dept_name} Bologna Ders Planı ({prog_title})"')
    brm.append('kategori: "fakulteler_ve_bolumler"')
    brm.append(f'bolum: "{dept_name}"')
    brm.append('guvenilirlik_duzeyi: "Tier 2 (Resmi Bologna Bilgi Sistemi)"')
    brm.append("---\n")
    brm.append(f"# {dept_name} Bologna Ders Planı ({prog_title})\n")
    brm.append(f"Bu dizin, {dept_name} lisans eğitiminin tüm 8 yarıyılını içerir.\n")
    brm.append("- [1. Yarıyıl](1_yariyil.md)\n- [2. Yarıyıl](2_yariyil.md)\n- [3. Yarıyıl](3_yariyil.md)\n- [4. Yarıyıl](4_yariyil.md)")
    brm.append("- [5. Yarıyıl](5_yariyil.md)\n- [6. Yarıyıl](6_yariyil.md)\n- [7. Yarıyıl](7_yariyil.md)\n- [8. Yarıyıl](8_yariyil.md)")
    brm.append("- [Önkoşul Zinciri](onkosul_zinciri.md)\n- [Seçimlik Ders Havuzları](secimlik_ders_havuzlari.md)\n")
    with open(breadme, 'w', encoding='utf-8') as fp:
        fp.write("\n".join(brm))
    print(f"Bologna tamamlandı: {output_dir}")

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
    sss_list: list,
    extra_bologna_links: list = None
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

Yıldız Teknik Üniversitesi **{faculty_name}** bünyesinde yer alan {dept_name}, {yerleske} Yerleşkesi'nde modern araştırma altyapısı, stüdyoları, laboratuvarları ve yetkin akademik kadrosuyla eğitim ve bilimsel faaliyetlerini sürdürmektedir.

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
        if extra_bologna_links:
            for el_name, el_path in extra_bologna_links:
                fp.write(f"- [{el_name}]({el_path}/README.md)\n")

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
- **Akademik Başarı Koşulu:** Mezuniyet için Ağırlıklı Genel Not Ortalamasının (AGNO) en az 2.00 / 4.00 olması şarttır.
- **Ders Grupları ve Dağılımı:**
  - Temel Kuramsal ve Mesleki Temel Dersler
  - Stüdyo, Tasarım, Atölye veya Uygulama Dersleri
  - Bölüm Mesleki / Teknik Seçmeli Dersleri
  - Sosyal ve Kültürel Seçmeli Dersler (Üniversite Havuzu)

## 📚 Hazırlık ve Dil Koşulları
- Bölüm öğretim planı gereğince öğrenciler İYS (İngilizce Yeterlik Sınavı) ile hazırlığı geçmeli veya Yabancı Diller Yüksekokulu hazırlık sınıfını başarıyla tamamlamalıdır.
- Programın eğitim diline göre (%30 veya %100 İngilizce) belirlenen asgari İngilizce ders kotası tamamlanmalıdır.
""")

    # 3. laboratuvarlar_ve_arastirma.md
    with open(os.path.join(dept_dir, "laboratuvarlar_ve_arastirma.md"), "w", encoding="utf-8") as fp:
        fp.write(f"""---
baslik: "{dept_name} Laboratuvarlar, Stüdyolar ve Araştırma Altyapısı"
kategori: "fakulteler_ve_bolumler"
fakulte: "{faculty_name}"
bolum: "{dept_name}"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bölüm Portalı)"
---

# {dept_name} Laboratuvarlar, Stüdyolar ve Araştırma Altyapısı

Bölümümüz, lisans eğitimindeki pratik uygulamaları, stüdyo üretimlerini ve lisansüstü bilimsel araştırmaları destekleyen donanımlı araştırma ve uygulama birimlerine sahiptir:

## 🔬 Aktif Stüdyo, Atölye ve Laboratuvarlar
""")
        for lab in lab_list:
            fp.write(f"### 📍 {lab['name']}\n")
            fp.write(f"- **Açıklama:** {lab['desc']}\n")
            fp.write(f"- **Kullanım:** Lisans proje/stüdyo dersleri, bitirme çalışmaları ve bilimsel araştırmalar.\n\n")

    # 4. staj_tasarim_ve_bitirme_esaslari.md
    with open(os.path.join(dept_dir, "staj_tasarim_ve_bitirme_esaslari.md"), "w", encoding="utf-8") as fp:
        fp.write(f"""---
baslik: "{dept_name} Staj, Proje ve Bitirme Esasları"
kategori: "fakulteler_ve_bolumler"
fakulte: "{faculty_name}"
bolum: "{dept_name}"
guvenilirlik_duzeyi: "Tier 2 (Resmi Bölüm Portalı)"
---

# {dept_name} Staj, Proje ve Bitirme Esasları

## 🛠️ Staj Esasları ve Yükümlülükler
{staj_detay}

## 📐 Tasarım, Proje ve Bitirme Çalışması Esasları
- **Bitirme Çalışması / Diploma Projesi:** Lisans eğitiminin son yılında (7. veya 8. yarıyıl) akademik danışman yönetiminde bağımsız bir araştırma, tasarım veya uygulama projesi olarak hazırlanır.
- **Jüri Savunması:** Hazırlanan bitirme çalışması ilgili kılavuza uygun olarak teslim edilir ve akademik jüri önünde sözlü sunum/sergi yoluyla savunulur.
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

YTÜ Lisansüstü Eğitim Enstitüsü (Sosyal Bilimler / Fen Bilimleri) koordinatörlüğünde bölümümüz bünyesinde yürütülen programlar:

- **Tezli Yüksek Lisans (M.Sc. / M.A.):** İleri uzmanlık dersleri ve bilimsel tez/proje çalışması (120 AKTS).
- **Tezsiz Yüksek Lisans:** Mesleki uzmanlaşmaya yönelik dersler ve dönem projesi (90 AKTS).
- **Doktora / Sanatta Yeterlik (Ph.D. / Proficiency in Art):** Özgün bilimsel/sanatsal araştırma, yeterlik sınavı, tez izleme komitesi ve doktora/sanatta yeterlik tezi (240 AKTS).
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
    print("🚀 MİMARLIK, İİBF VE SANAT-TASARIM FAKÜLTELERİ ENTEGRASYONU BAŞLATILIYOR...")

    # =============================================================
    # 1. MİMARLIK FAKÜLTESİ
    # =============================================================
    mim_fac_dir = BASE_DIR / "05_fakulteler_ve_bolumler" / "mimarlik_fakultesi"
    os.makedirs(mim_fac_dir, exist_ok=True)

    # 1.1 README
    with open(mim_fac_dir / "README.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "Mimarlık Fakültesi Genel Tanıtımı ve Teşkilat Yapısı"
kategori: "fakulteler_ve_bolumler"
fakulte: "Mimarlık Fakültesi"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# Mimarlık Fakültesi

Yıldız Teknik Üniversitesi **Mimarlık Fakültesi**, Türkiye'nin en köklü ve saygın mimarlık ve tasarım okullarından biridir. Tarihi Beşiktaş (Yıldız) Yerleşkesi'nde (Yıldız Sarayı Dış Bahçesi / Çukur Saray kompleksi) özgün mimari stüdyoları, laboratuvarları ve uluslararası akreditasyonlarıyla eğitim ve tasarım faaliyetlerini yürütmektedir.

## 🏛️ Fakülte Bölümleri
- [Mimarlık](mimarlik/README.md)
- [Şehir ve Bölge Planlama](sehir_ve_bolge_planlama/README.md)
- [Endüstriyel Tasarım](endustriyel_tasarim/README.md)

## 🗂️ Fakülte Dokümantasyon Rehberi
- [Dekanlık ve Teşkilat Yapısı](dekanlik_ve_teskilat_yapisi.md)
- [Fakülte Sıkça Sorulan Sorular](fakulte_sikca_sorulan_sorular.md)
- [Akran Danışmanlığı ve Öğrenci Rehberi](akran_danismanligi_ve_ogrenci_rehberi.md)
- [Staj ve Atölye Esasları](staj_ve_atolye_esaslari.md)
""")

    # 1.2 Dekanlık
    with open(mim_fac_dir / "dekanlik_ve_teskilat_yapisi.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "Mimarlık Fakültesi Dekanlığı ve Teşkilat Yapısı"
kategori: "fakulteler_ve_bolumler"
fakulte: "Mimarlık Fakültesi"
kaynak: "http://www.mmr.yildiz.edu.tr/"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# Mimarlık Fakültesi Dekanlığı ve Teşkilat Yapısı

## 👥 Üst Yönetim
- **Dekan:** Prof. Dr. Sırma TURGUT
- **Dekan Yardımcıları:** Fakülte eğitim-öğretim ve araştırma koordinatörleri
- **Fakülte Sekreterliği:** İdari işler ve öğrenci bürosu
- **Yerleşke:** Beşiktaş (Yıldız) Merkez Kampüsü, Çukur Saray / E-Blok

## 🏛️ Kurullar ve Karar Mekanizmaları
- **Fakülte Kurulu:** Dekan başkanlığında bölüm başkanları ve öğretim üyesi temsilcilerinden oluşur.
- **Fakülte Yönetim Kurulu:** Mazeret sınavları, staj intibakları, tek ders ve çift anadal/yandal kararlarını alır.
""")

    # 1.3 Fakülte SSS
    with open(mim_fac_dir / "fakulte_sikca_sorulan_sorular.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "Mimarlık Fakültesi Sıkça Sorulan Sorular"
kategori: "fakulteler_ve_bolumler"
fakulte: "Mimarlık Fakültesi"
kaynak: "http://www.mmr.yildiz.edu.tr/"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# Mimarlık Fakültesi Sıkça Sorulan Sorular

### ❓ Mimarlık Fakültesi nerede yer almaktadır?
**Cevap:** Mimarlık Fakültesi, Yıldız Teknik Üniversitesi'nin tarihi Beşiktaş (Yıldız) Yerleşkesi'nde yer almaktadır.

### ❓ Tasarım stüdyoları nasıl işler?
**Cevap:** Tasarım stüdyoları haftada 8-12 saatlik uygulamalı dersler olup, kritik alma, ara jüri ve final jürisi değerlendirmelerine dayanır. Devam zorunluluğu %80'dir.

### ❓ Staj yükümlülükleri nelerdir?
**Cevap:** Mimarlık ve tasarım bölümlerinde Şantiye / Üretim ve Büro / Ofis stajları olmak üzere zorunlu stajlar bulunmaktadır.
""")

    # 1.4 Akran Danışmanlığı
    with open(mim_fac_dir / "akran_danismanligi_ve_ogrenci_rehberi.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "Mimarlık Fakültesi Akran Danışmanlığı ve Öğrenci Rehberi"
kategori: "fakulteler_ve_bolumler"
fakulte: "Mimarlık Fakültesi"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# Mimarlık Fakültesi Akran Danışmanlığı ve Öğrenci Rehberi

Fakülteye yeni başlayan birinci sınıf öğrencilerine üst sınıflardaki deneyimli akran danışmanlar eşlik eder:
- Stüdyo malzemelerinin temini (maket bıçağı, cetveller, çizim kağıtları, dijital çizim tabletleri).
- Bilgisayar destekli tasarım yazılımlarının (AutoCAD, Revit, Rhino, Photoshop, SketchUp) öğrenci lisanslarının edinilmesi.
- Çukur Saray ve fakülte kütüphanesinin çalışma saatleri ve stüdyo kuralları.
""")

    # 1.5 Staj ve Atölye Esasları
    with open(mim_fac_dir / "staj_ve_atolye_esaslari.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "Mimarlık Fakültesi Staj ve Atölye Esasları"
kategori: "fakulteler_ve_bolumler"
fakulte: "Mimarlık Fakültesi"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# Mimarlık Fakültesi Staj ve Atölye Esasları

## 🏗️ Staj Türleri
1. **Şantiye / Saha / Uygulama Stajı (30 İş Günü):** Kaba ve ince yapı imalatları, restorasyon şantiyeleri veya kentsel planlama saha çalışmaları.
2. **Büro / Ofis Stajı (30 İş Günü):** Mimari proje çizimi, kentsel tasarım, modelleme, ruhsat projeleri ve sunum çalışmaları.

## 🛠️ Atölye ve Fabrikasyon Kuralları
- **Maket Atölyesi:** Lazer kesici, CNC ve 3B yazıcılar iş güvenliği eğitimi alındıktan sonra gözetmen teknisyen eşliğinde kullanılabilir.
- **Güvenlik:** Atölye ve stüdyolarda koruyucu ekipman (gözlük, eldiven) kullanımı zorunludur.
""")

    # -------------------------------------------------------------
    # 1.A Mimarlık Bölümü
    # -------------------------------------------------------------
    mim_dir = mim_fac_dir / "mimarlik"
    generate_department_core(
        dept_dir=str(mim_dir),
        dept_name="Mimarlık",
        faculty_name="Mimarlık Fakültesi",
        web_url="http://mim.yildiz.edu.tr/",
        yerleske="Beşiktaş (Yıldız)",
        baskan_info="""- **Bölüm Başkanı:** Prof. Dr. Almula KÖKSAL IŞIKKAYA (E-posta: `almula@yildiz.edu.tr`)
- **Bölüm Başkan Yardımcıları:** Lisans ve lisansüstü koordinatörleri
- **Sekreterlik:** Yıldız Yerleşkesi Mimarlık Bölüm Başkanlığı Binası""",
        staj_detay="""- **Toplam Süre:** 60 İş Günü (30 gün Şantiye Stajı + 30 gün Büro Stajı).
- **Önkoşul:** Şantiye stajına 2. sınıfın bitiminde (en az 4 yarıyıl tamamlandıktan sonra), Büro stajına ise Şantiye stajı tamamlandıktan sonra başlanabilir.
- **Değerlendirme:** Staj defteri ve işyeri sicil fişi Bölüm Staj Komisyonu tarafından mülakat ve dosya incelemesiyle onaylanır.""",
        lab_list=[
            {"name": "Mimari Tasarım Stüdyoları (MTS)", "desc": "MTS 1'den MTS 8'e kadar her yarıyıl mimari konsept, mekan kurgusu ve uygulama projelerinin geliştirildiği stüdyolar."},
            {"name": "Model ve Maket Atölyesi", "desc": "Lazer kesim üniteleri, 3B yazıcılar, köpük kesiciler ve ahşap/pleksi işleme tezgahları."},
            {"name": "Yapı Fiziği ve Çevre Kontrolü Laboratuvarı", "desc": "Isı, ses, ışık ve akustik ölçüm cihazları, rüzgar simülasyonları."},
            {"name": "Yapı Malzemeleri ve Restorasyon Laboratuvarı", "desc": "Tarihi ve modern yapı malzemelerinin dayanım, porozite ve kimyasal analiz birimleri."},
            {"name": "Bilgisayarlı Tasarım (CAD/BIM) Laboratuvarı", "desc": "Revit, ArchiCAD, Rhino, Grasshopper ve AutoCAD donanımlı bilgisayar laboratuvarı."}
        ],
        komisyon_list=[
            {"name": "Staj Komisyonu", "desc": "Şantiye ve büro staj başvurularını, SGK girişlerini ve defter değerlendirmelerini yürütür."},
            {"name": "Diploma ve Bitirme Projesi Komisyonu", "desc": "Bitirme projesi jürilerini, teslim takvimini ve sergi süreçlerini organize eder."},
            {"name": "Akreditasyon Komisyonu (MİAK / NAAB)", "desc": "Ulusal MİAK ve uluslararası NAAB eşdeğerlik kalite güvence çalışmalarını yürütür."},
            {"name": "Erasmus ve Dış İlişkiler Komisyonu", "desc": "Avrupa mimarlık okullarıyla öğrenci ve staj değişimlerini koordine eder."}
        ],
        sss_list=[
            {"q": "Mimarlık Tasarım Stüdyoları önkoşullu mudur?", "a": "Evet, her Mimari Tasarım Stüdyosu (MTS) bir önceki MTS dersinin başarılmış olmasını önkoşul olarak arar."},
            {"q": "Bitirme projesine (Diploma Projesi) ne zaman kayıt olunabilir?", "a": "Müfredattaki tüm tasarım stüdyoları başarıyla tamamlandıktan ve asgari 200 AKTS kredisine ulaşıldıktan sonra kayıt olunabilir."},
            {"q": "MİAK akreditasyonu mezuniyette ne avantaj sağlar?", "a": "MİAK (Mimarlık Akreditasyon Kurulu) uluslararası geçerliliği ve mimarlık meslek odaları nezdinde tam yetkinlik tanınırlığını tesciller."}
        ],
        extra_bologna_links=[("%100 İngilizce Programı", "bologna_ders_plani_yuzde100")]
    )
    # Mimarlık %30 Bologna
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=50&aid=38", str(mim_dir / "bologna_ders_plani"), "%30 İngilizce", "Mimarlık")
    # Mimarlık %100 Bologna
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=429&aid=38", str(mim_dir / "bologna_ders_plani_yuzde100"), "%100 İngilizce", "Mimarlık")

    # -------------------------------------------------------------
    # 1.B Şehir ve Bölge Planlama Bölümü
    # -------------------------------------------------------------
    sbp_dir = mim_fac_dir / "sehir_ve_bolge_planlama"
    generate_department_core(
        dept_dir=str(sbp_dir),
        dept_name="Şehir ve Bölge Planlama",
        faculty_name="Mimarlık Fakültesi",
        web_url="http://sbp.yildiz.edu.tr/",
        yerleske="Beşiktaş (Yıldız)",
        baskan_info="""- **Bölüm Başkanı:** Prof. Dr. Senay OĞUZTİMUR
- **Bölüm Başkan Yardımcıları:** Doç. Dr. C. Cenk HAMAMCIOĞLU, Öğr. Gör. Dr. Gözdem AYSU
- **Sekreterlik:** Yıldız Yerleşkesi ŞBP Bölüm Başkanlığı Binası""",
        staj_detay="""- **Toplam Süre:** 60 İş Günü (30 gün Kamu/Belediye Stajı + 30 gün Özel Planlama Bürosu Stajı).
- **Kamu Stajı:** Çevre Şehircilik ve İklim Değişikliği Bakanlığı, İller Bankası veya Büyükşehir/İlçe Belediyeleri İmar ve Planlama Müdürlükleri.
- **Büro Stajı:** Şehir planlama, kentsel tasarım ve gayrimenkul geliştirme müşavirlik ofisleri.""",
        lab_list=[
            {"name": "Planlama Stüdyoları", "desc": "Kentsel ve bölgesel ölçekli arazi kullanımı, ulaşım ve stratejik planlama projelerinin hazırlandığı çizim stüdyoları."},
            {"name": "Coğrafi Bilgi Sistemleri (CBS / GIS) Laboratuvarı", "desc": "ArcGIS, QGIS ve mekansal analiz yazılımlarıyla kentsel veri tabanı analizleri."},
            {"name": "Kentsel Tasarım ve Modelleme Laboratuvarı", "desc": "3B kentsel silüet analizleri, dijital maket ve görselleştirme istasyonları."}
        ],
        komisyon_list=[
            {"name": "Staj Komisyonu", "desc": "Kamu ve büro staj başvurularını denetler, staj defterlerini değerlendirir."},
            {"name": "Stüdyolar Koordinasyon Komisyonu", "desc": "8 yarıyıllık planlama stüdyoları arasındaki tematik kurguyu koordine eder."},
            {"name": "Bitirme Projesi Komisyonu", "desc": "Diploma projesi çalışma alanlarını, jüri oturumlarını organize eder."}
        ],
        sss_list=[
            {"q": "Planlama stüdyoları arasındaki önkoşul nasıldır?", "a": "Her planlama stüdyosu bir önceki dönemin stüdyosunun başarıyla geçilmesini gerektirir."},
            {"q": "CBS yazılımları lisanslı olarak sağlanıyor mu?", "a": "Evet, üniversitemiz Esri ArcGIS öğrenci lisanslarını YTÜ öğrencilerine ücretsiz sunmaktadır."}
        ]
    )
    # ŞBP Bologna
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=51&aid=39", str(sbp_dir / "bologna_ders_plani"), "%30 İngilizce", "Şehir ve Bölge Planlama")

    # -------------------------------------------------------------
    # 1.C Endüstriyel Tasarım Bölümü
    # -------------------------------------------------------------
    ent_dir = mim_fac_dir / "endustriyel_tasarim"
    generate_department_core(
        dept_dir=str(ent_dir),
        dept_name="Endüstriyel Tasarım",
        faculty_name="Mimarlık Fakültesi",
        web_url="http://www.mmr.yildiz.edu.tr/",
        yerleske="Beşiktaş (Yıldız)",
        baskan_info="""- **Program Koordinatörlüğü:** Mimarlık Fakültesi Endüstriyel Tasarım Bölüm Koordinatörlüğü
- **Sekreterlik:** Yıldız Yerleşkesi Tasarım Bölümleri İdari Ofisi""",
        staj_detay="""- **Toplam Süre:** 60 İş Günü (30 gün Üretim/Fabrika Stajı + 30 gün Tasarım Ofisi Stajı).
- **Üretim Stajı:** Seri imalat tesisleri, kalıphane, plastik/metal/ahşap işleme fabrikaları.
- **Ofis Stajı:** Endüstriyel ürün tasarımı ofisleri, kurumsal Ar-Ge ve tasarım merkezleri.""",
        lab_list=[
            {"name": "Endüstriyel Ürün Tasarımı Stüdyoları", "desc": "Ürün konsept geliştirme, eskizleme ve sunum ortamları."},
            {"name": "Hızlı Prototipleme ve 3B Baskı Laboratuvarı", "desc": "SLA, FDM 3B yazıcılar, silikon kalıplama ve prototip atölyesi."},
            {"name": "Ergonomi ve Kullanıcı Deneyimi Laboratuvarı", "desc": "Antropometrik ölçüm kitleri ve kullanıcı etkileşimi test düzenekleri."}
        ],
        komisyon_list=[
            {"name": "Staj Komisyonu", "desc": "Üretim ve ofis staj onay ve sicil işlemlerini yürütür."},
            {"name": "Sanayi İşbirlikleri ve Sergi Komisyonu", "desc": "Öğrenci tasarımlarının sektör firmalarıyla buluşmasını ve yıl sonu sergisini düzenler."}
        ],
        sss_list=[
            {"q": "Endüstriyel Tasarım ile Endüstri Mühendisliği arasındaki fark nedir?", "a": "Endüstriyel Tasarım fiziksel ve dijital ürünlerin form, estetik, kullanıcı deneyimi ve işlevsellik tasarımına odaklanırken; Endüstri Mühendisliği üretim sistemleri ve süreç optimizasyonuna odaklanır."}
        ]
    )
    # Endüstriyel Tasarım Bologna
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=516&aid=41", str(ent_dir / "bologna_ders_plani"), "Lisans Programı", "Endüstriyel Tasarım")


    # =============================================================
    # 2. İKTİSADİ VE İDARİ BİLİMLER FAKÜLTESİ (İİBF)
    # =============================================================
    iib_fac_dir = BASE_DIR / "05_fakulteler_ve_bolumler" / "iktisadi_ve_idari_bilimler_fakultesi"
    os.makedirs(iib_fac_dir, exist_ok=True)

    # 2.1 README
    with open(iib_fac_dir / "README.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "İktisadi ve İdari Bilimler Fakültesi (İİBF) Genel Tanıtımı"
kategori: "fakulteler_ve_bolumler"
fakulte: "İktisadi ve İdari Bilimler Fakültesi"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# İktisadi ve İdari Bilimler Fakültesi (İİBF)

Yıldız Teknik Üniversitesi **İktisadi ve İdari Bilimler Fakültesi**, Davutpaşa Yerleşkesi'ndeki Tarihi Taş Kışla Binası'nda yer almaktadır. Ekonomi, işletme, uluslararası ilişkiler ve kamu yönetimi alanlarında Türkiye'nin en köklü akademik birimlerindendir.

## 🏛️ Fakülte Bölümleri
- [İktisat](iktisat/README.md)
- [İşletme](isletme/README.md)
- [Siyaset Bilimi ve Uluslararası İlişkiler](siyaset_bilimi_ve_uluslararasi_iliskiler/README.md)

## 🗂️ Fakülte Dokümantasyon Rehberi
- [Dekanlık ve Teşkilat Yapısı](dekanlik_ve_teskilat_yapisi.md)
- [Fakülte Sıkça Sorulan Sorular](fakulte_sikca_sorulan_sorular.md)
- [Akran Danışmanlığı ve Öğrenci Rehberi](akran_danismanligi_ve_ogrenci_rehberi.md)
- [Staj ve Kariyer Esasları](staj_ve_kariyer_esaslari.md)
""")

    # 2.2 Dekanlık
    with open(iib_fac_dir / "dekanlik_ve_teskilat_yapisi.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "İİBF Dekanlığı ve Yönetim Kadrosu"
kategori: "fakulteler_ve_bolumler"
fakulte: "İktisadi ve İdari Bilimler Fakültesi"
kaynak: "https://iib.yildiz.edu.tr/dekanlik"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# İİBF Dekanlığı ve Yönetim Kadrosu

## 👥 Üst Yönetim
- **Dekan:** Prof. Dr. Yasin ŞEHİTOĞLU
- **Dekan Yardımcısı:** Dr. Öğr. Üyesi Erhan BEKTAŞ
- **Dekan Yardımcısı:** Dr. Öğr. Üyesi Hasan Ali KAPLAN
- **Fakülte Sekreteri:** İdari Hizmetler Koordinatörlüğü
- **Yerleşke:** Davutpaşa Kampüsü, Tarihi Kışla Binası A/B Blokları

## 🏛️ Kurullar
- **Fakülte Kurulu:** Dekan, Bölüm Başkanları ve seçilmiş öğretim üyelerinden oluşur.
- **Fakülte Yönetim Kurulu:** Mazeret, kayıt dondurma, yatay geçiş ve ÇAP/Yandal kararlarını karara bağlar.
""")

    # 2.3 Fakülte SSS
    with open(iib_fac_dir / "fakulte_sikca_sorulan_sorular.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "İİBF Sıkça Sorulan Sorular"
kategori: "fakulteler_ve_bolumler"
fakulte: "İktisadi ve İdari Bilimler Fakültesi"
kaynak: "https://iib.yildiz.edu.tr/"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# İİBF Sıkça Sorulan Sorular

### ❓ İİBF hangi yerleşkededir?
**Cevap:** Davutpaşa Yerleşkesi Tarihi Taş Kışla Binası'nda hizmet vermektedir.

### ❓ Çift Anadal (ÇAP) ve Yandal olanakları nasıldır?
**Cevap:** İİBF bölümleri arasında (İktisat, İşletme, SBUI) ve mühendislik fakülteleriyle (özellikle Endüstri ve Matematik Mühendisliği) geniş ÇAP ve Yandal anlaşmaları mevcuttur.

### ❓ Staj yapmak zorunlu mudur?
**Cevap:** Bölüm müfredatlarına göre zorunlu ve isteğe bağlı staj imkanları mevcuttur. Öğrencilerin SGK primleri üniversitemiz tarafından karşılanmaktadır.
""")

    # 2.4 Akran Danışmanlığı
    with open(iib_fac_dir / "akran_danismanligi_ve_ogrenci_rehberi.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "İİBF Akran Danışmanlığı ve Öğrenci Rehberi"
kategori: "fakulteler_ve_bolumler"
fakulte: "İktisadi ve İdari Bilimler Fakültesi"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# İİBF Akran Danışmanlığı ve Öğrenci Rehberi

İİBF öğrencileri için akran rehberliği:
- Kışla Binası derslik düzeni ve kütüphane olanakları.
- Kulüp faaliyetleri (İşletme Kulübü, Finans Kulübü, Uluslararası İlişkiler Kulübü).
- Vize-final dönemleri, ekonometri ve muhasebe dersleri için çalışma stratejileri.
""")

    # 2.5 Staj ve Kariyer Esasları
    with open(iib_fac_dir / "staj_ve_kariyer_esaslari.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "İİBF Staj ve Kariyer Esasları"
kategori: "fakulteler_ve_bolumler"
fakulte: "İktisadi ve İdari Bilimler Fakültesi"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# İİBF Staj ve Kariyer Esasları

## 💼 Staj Alanları
- **Finans ve Bankacılık:** Kamu ve özel bankalar, Borsa İstanbul, aracı kurumlar.
- **Denetim ve Danışmanlık:** Big 4 bağımsız denetim şirketleri, vergi ve yönetim danışmanlığı firmaları.
- **Kurumsal Şirketler:** Pazarlama, insan kaynakları, tedarik zinciri ve operasyon departmanları.
- **Kamu ve Diplomasi:** Bakanlıklar, Merkez Bankası (TCMB), SPK, BDDK, Rekabet Kurumu ve büyükelçilikler/konsolosluklar.

## 📄 SGK İşlemleri
- Staj onay formu staj başlangıç tarihinden en az 15 gün önce Bölüm Staj Komisyonuna iletilmelidir. SGK iş kazası ve meslek hastalığı primleri rektörlükçe ödenir.
""")

    # -------------------------------------------------------------
    # 2.A İktisat Bölümü
    # -------------------------------------------------------------
    ikt_dir = iib_fac_dir / "iktisat"
    generate_department_core(
        dept_dir=str(ikt_dir),
        dept_name="İktisat",
        faculty_name="İktisadi ve İdari Bilimler Fakültesi",
        web_url="http://ikt.yildiz.edu.tr/",
        yerleske="Davutpaşa",
        baskan_info="""- **Bölüm Başkanı:** Prof. Dr. Fazıl KAYIKÇI
- **Bölüm Başkan Yardımcıları:** Lisans ve Bologna koordinatörleri
- **Sekreterlik:** Davutpaşa Kampüsü İİBF İktisat Bölüm Bürosu""",
        staj_detay="""- **Staj Süresi:** 20-30 İş Günü (Zorunlu / İsteğe Bağlı seçenekleri).
- **Kurumlar:** TCMB, Hazine ve Maliye Bakanlığı, bankalar, yatırım fonları, araştırma merkezleri.
- **Değerlendirme:** Staj defteri ve kurum değerlendirme formu komisyonca incelenir.""",
        lab_list=[
            {"name": "Ekonometri ve Veri Analizi Laboratuvarı", "desc": "Stata, EViews, R, Python ve SPSS yüklü bilgisayar laboratuvarı."},
            {"name": "Finansal Piyasalar ve Modelleme Laboratuvarı", "desc": "Borsa veri akışları ve zaman serisi analiz istasyonları."}
        ],
        komisyon_list=[
            {"name": "Staj Komisyonu", "desc": "Staj onay ve SGK süreçlerini yönetir."},
            {"name": "Erasmus ve Değişim Komisyonu", "desc": "Avrupa ekonomi fakülteleriyle ikili anlaşmaları koordine eder."}
        ],
        sss_list=[
            {"q": "İktisat mezunları hangi unvanla mezun olur?", "a": "İktisat Lisans diploması ile 'Ekonomist / İktisatçı' unvanı alınır."},
            {"q": "%100 İngilizce programa geçiş mümkün mü?", "a": "Yeterli AGNO ve dil puanına sahip öğrenciler kontenjan dahilinde kurum içi yatay geçiş yapabilir."}
        ],
        extra_bologna_links=[("%100 İngilizce Programı", "bologna_ders_plani_yuzde100")]
    )
    # İktisat %30 Bologna
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=54&aid=45", str(ikt_dir / "bologna_ders_plani"), "%30 İngilizce", "İktisat")
    # İktisat %100 Bologna
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=535&aid=45", str(ikt_dir / "bologna_ders_plani_yuzde100"), "%100 İngilizce", "İktisat")

    # -------------------------------------------------------------
    # 2.B İşletme Bölümü
    # -------------------------------------------------------------
    isl_dir = iib_fac_dir / "isletme"
    generate_department_core(
        dept_dir=str(isl_dir),
        dept_name="İşletme",
        faculty_name="İktisadi ve İdari Bilimler Fakültesi",
        web_url="http://isl.yildiz.edu.tr/",
        yerleske="Davutpaşa",
        baskan_info="""- **Bölüm Başkanı:** Prof. Dr. Beyza Ahlatcıoğlu Özkök
- **Bölüm Başkan Yardımcıları:** Bölüm koordinatörleri
- **Sekreterlik:** Davutpaşa Kampüsü İİBF İşletme Bölüm Bürosu""",
        staj_detay="""- **Staj Süresi:** 30 İş Günü.
- **Kapsam:** Muhasebe-Finansman, Pazarlama, Yönetim-Organizasyon, Üretim Yönetimi veya İnsan Kaynakları departmanlarında staj.
- **Onay:** Staj başlangıcından önce işyerinin bölüm komisyonu tarafından onaylanması şarttır.""",
        lab_list=[
            {"name": "İşletme Simülasyonu ve ERP Laboratuvarı", "desc": "SAP ERP, kurumsal kaynak planlama ve vaka analiz sistemleri."},
            {"name": "Pazarlama ve Tüketici Davranışları Laboratuvarı", "desc": "Pazar araştırması ve anket analiz laboratuvarı."}
        ],
        komisyon_list=[
            {"name": "Staj Komisyonu", "desc": "Öğrenci staj süreçlerini ve defter teslimlerini koordine eder."},
            {"name": "Müfredat ve Bologna Komisyonu", "desc": "Ders havuzlarının güncellenmesi ve akreditasyon süreçlerini yürütür."}
        ],
        sss_list=[
            {"q": "İşletme programında hangi anabilim dalları bulunur?", "a": "Muhasebe ve Finansman, Yönetim ve Organizasyon, Üretim Yönetimi ve Pazarlama, Sayısal Yöntemler, Ticaret Hukuku anabilim dalları bulunmaktadır."}
        ],
        extra_bologna_links=[("%100 İngilizce Programı", "bologna_ders_plani_yuzde100")]
    )
    # İşletme %30 Bologna
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=55&aid=46", str(isl_dir / "bologna_ders_plani"), "%30 İngilizce", "İşletme")
    # İşletme %100 Bologna
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=539&aid=46", str(isl_dir / "bologna_ders_plani_yuzde100"), "%100 İngilizce", "İşletme")

    # -------------------------------------------------------------
    # 2.C Siyaset Bilimi ve Uluslararası İlişkiler Bölümü
    # -------------------------------------------------------------
    sbu_dir = iib_fac_dir / "siyaset_bilimi_ve_uluslararasi_iliskiler"
    generate_department_core(
        dept_dir=str(sbu_dir),
        dept_name="Siyaset Bilimi ve Uluslararası İlişkiler",
        faculty_name="İktisadi ve İdari Bilimler Fakültesi",
        web_url="http://sbu.yildiz.edu.tr/",
        yerleske="Davutpaşa",
        baskan_info="""- **Bölüm Başkanı:** Prof. Dr. Mehmet Akif OKUR
- **Bölüm Başkan Yardımcıları:** Lisans ve Erasmus koordinatörleri
- **Sekreterlik:** Davutpaşa Kampüsü İİBF SBUI Bölüm Bürosu""",
        staj_detay="""- **Staj Süresi:** 20-30 İş Günü (İsteğe Bağlı / Zorunlu opsiyonları).
- **Kurumlar:** Dışişleri Bakanlığı, büyükelçilikler, düşünce kuruluşları (SETA, TASAM, ORSAM), uluslararası örgütler, medya organları ve STK'lar.
- **Değerlendirme:** Staj raporu komisyonca incelenir.""",
        lab_list=[
            {"name": "Diplomasi ve Simülasyon Salonu", "desc": "Model Birleşmiş Milletler (MUN), kriz masası ve çok taraflı müzakere simülasyonları salonu."},
            {"name": "Uluslararası Çalışmalar Dokümantasyon Merkezi", "desc": "Bölgesel siyasi raporlar ve uluslararası antlaşmalar arşivi."}
        ],
        komisyon_list=[
            {"name": "Staj ve Kariyer Komisyonu", "desc": "Kamu ve uluslararası örgüt staj koordinasyonunu yürütür."},
            {"name": "Dış İlişkiler ve Erasmus Komisyonu", "desc": "Avrupa üniversiteleriyle öğrenci değişimini yürütür."}
        ],
        sss_list=[
            {"q": "Bölüm mezunları Dışişleri Bakanlığı sınavlarına girebilir mi?", "a": "Evet, bölüm mezunları Meslek Memurluğu ve Konsolosluk ve İhtisas Memurluğu sınavlarına doğrudan katılma hakkına sahiptir."}
        ]
    )
    # SBUI Bologna
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=56&aid=47", str(sbu_dir / "bologna_ders_plani"), "%30 İngilizce", "Siyaset Bilimi ve Uluslararası İlişkiler")


    # =============================================================
    # 3. SANAT VE TASARIM FAKÜLTESİ
    # =============================================================
    stf_fac_dir = BASE_DIR / "05_fakulteler_ve_bolumler" / "sanat_ve_tasarim_fakultesi"
    os.makedirs(stf_fac_dir, exist_ok=True)

    # 3.1 README
    with open(stf_fac_dir / "README.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "Sanat ve Tasarım Fakültesi Genel Tanıtımı ve Teşkilat Yapısı"
kategori: "fakulteler_ve_bolumler"
fakulte: "Sanat ve Tasarım Fakültesi"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# Sanat ve Tasarım Fakültesi

Yıldız Teknik Üniversitesi **Sanat ve Tasarım Fakültesi**, sanat, müzik, sahne sanatları, iletişim ve görsel tasarım disiplinlerini tek çatı altında buluşturan öncü bir fakültedir. Davutpaşa Yerleşkesi'ndeki modern stüdyoları, ses kayıt tesisleri, konser salonları ve atölyeleriyle zengin bir üretim ekosistemine sahiptir.

## 🏛️ Fakülte Bölümleri
- [Müzik ve Sahne Sanatları](muzik_ve_sahne_sanatlari/README.md)
- [İletişim Tasarımı](iletisim_tasarimi/README.md)
- [Sanat](sanat/README.md)

## 🗂️ Fakülte Dokümantasyon Rehberi
- [Dekanlık ve Teşkilat Yapısı](dekanlik_ve_teskilat_yapisi.md)
- [Fakülte Sıkça Sorulan Sorular](fakulte_sikca_sorulan_sorular.md)
- [Akran Danışmanlığı ve Öğrenci Rehberi](akran_danismanligi_ve_ogrenci_rehberi.md)
- [Özel Yetenek ve Sanatsal Etkinlik Esasları](ozel_yetenek_ve_sanatsal_etkinlik_esaslari.md)
""")

    # 3.2 Dekanlık
    with open(stf_fac_dir / "dekanlik_ve_teskilat_yapisi.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "Sanat ve Tasarım Fakültesi Dekanlığı"
kategori: "fakulteler_ve_bolumler"
fakulte: "Sanat ve Tasarım Fakültesi"
kaynak: "http://www.sts.yildiz.edu.tr/"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# Sanat ve Tasarım Fakültesi Dekanlığı

## 👥 Üst Yönetim
- **Dekan:** Prof. Dr. Mehmet Emin KAHRAMAN
- **Dekan Yardımcıları:** Fakülte akademik ve sanatsal koordinatörleri
- **Fakülte Sekreteri:** İdari Hizmetler Birimi
- **Yerleşke:** Davutpaşa Kampüsü, Sanat ve Tasarım Fakültesi Binası & Otağ-ı Hümayun

## 🏛️ Sanat ve Tasarım Kurulları
- **Fakülte Kurulu:** Dekan ve bölüm başkanlarından oluşur.
- **Sanat ve Sergi Kurulu:** Fakülte bünyesindeki yıllık sergi, konser, festival ve sanatsal jürileri koordine eder.
""")

    # 3.3 Fakülte SSS
    with open(stf_fac_dir / "fakulte_sikca_sorulan_sorular.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "Sanat ve Tasarım Fakültesi Sıkça Sorulan Sorular"
kategori: "fakulteler_ve_bolumler"
fakulte: "Sanat ve Tasarım Fakültesi"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# Sanat ve Tasarım Fakültesi Sıkça Sorulan Sorular

### ❓ Fakülte bölümlerine öğrenci alımı nasıl yapılmaktadır?
**Cevap:** Bölümlerin bazı programları merkezi YKS puanı ile (örn. İletişim Tasarımı), bazı programları ise TYT baraj puanı sonrası YTÜ Özel Yetenek Sınavları ile (Müzik, Dans vb.) öğrenci almaktadır.

### ❓ Stüdyo ve konser salonu kullanım saatleri nasıldır?
**Cevap:** Ses kayıt stüdyoları, prova odaları ve dans salonları randevu sistemiyle öğrencilerin bireysel ve grup çalışmalarına açıktır.
""")

    # 3.4 Akran Danışmanlığı
    with open(stf_fac_dir / "akran_danismanligi_ve_ogrenci_rehberi.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "Sanat ve Tasarım Fakültesi Akran Danışmanlığı"
kategori: "fakulteler_ve_bolumler"
fakulte: "Sanat ve Tasarım Fakültesi"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# Sanat ve Tasarım Fakültesi Akran Danışmanlığı

Sanat ve Tasarım Fakültesi öğrencileri için rehberlik:
- Portfolyo hazırlama ve sanatsal sunum teknikleri.
- Ses ve video kurgu yazılımları (Logic Pro, Pro Tools, Premiere, After Effects, DaVinci Resolve) laboratuvar erişimleri.
- Yıl sonu bitirme sergileri ve konser organizasyonları.
""")

    # 3.5 Özel Yetenek ve Sanatsal Etkinlik Esasları
    with open(stf_fac_dir / "ozel_yetenek_ve_sanatsal_etkinlik_esaslari.md", "w", encoding="utf-8") as fp:
        fp.write("""---
baslik: "Özel Yetenek Sınavı ve Sanatsal Etkinlik Esasları"
kategori: "fakulteler_ve_bolumler"
fakulte: "Sanat ve Tasarım Fakültesi"
guvenilirlik_duzeyi: "Tier 2 (Resmi Fakülte Portalı)"
---

# Özel Yetenek Sınavı ve Sanatsal Etkinlik Esasları

## 🎭 Özel Yetenek Sınavları
- Her yıl rektörlük tarafından ilan edilen takvim uyarınca yaz aylarında gerçekleştirilir.
- Müzik ve Sahne Sanatları için duyma/algılama, enstrüman icrası ve sahne performansı sınavları uygulanır.

## 🎨 Sergi ve Konser Katılım Kuralları
- Öğrenciler her yarıyıl en az bir fakülte sergisi veya konser projesinde yer almakla teşvik edilir.
- Sanatsal eserlerin telif ve fikri hakları üniversitemiz kuralları çerçevesinde korunur.
""")

    # -------------------------------------------------------------
    # 3.A Müzik ve Sahne Sanatları Bölümü
    # -------------------------------------------------------------
    mssb_dir = stf_fac_dir / "muzik_ve_sahne_sanatlari"
    generate_department_core(
        dept_dir=str(mssb_dir),
        dept_name="Müzik ve Sahne Sanatları",
        faculty_name="Sanat ve Tasarım Fakültesi",
        web_url="https://mssb.yildiz.edu.tr/",
        yerleske="Davutpaşa",
        baskan_info="""- **Bölüm Başkanı V.:** Doç. Aslıhan ERUZUN ÖZEL
- **Anasanat Dalı Başkanları:** Müzik Toplulukları, Ses Sanatları Tasarımı, Dans
- **Sekreterlik:** Davutpaşa Kampüsü Sanat ve Tasarım Fakültesi MSSB Ofisi""",
        staj_detay="""- **Staj / Sahne Uygulaması:** 30 İş Günü.
- **Kapsam:** Devlet veya özel orkestralar, opera ve bale müdürlükleri, ses kayıt stüdyoları, müzik prodüksiyon firmaları veya sahne sanatları merkezleri.
- **Değerlendirme:** Performans raporu ve staj dosyası bölüm jürisi tarafından onaylanır.""",
        lab_list=[
            {"name": "Profesyonel Ses Kayıt Stüdyosu", "desc": "Pro Tools HD, Neve mikser, mikrofon parkı ve çok kanallı kayıt odası."},
            {"name": "Akustik Prova Salonları", "desc": "Ses yalıtımlı piyano ve oda müziği bireysel çalışma odaları."},
            {"name": "Dans ve Beden Hareket Stüdyosu", "desc": "Özel dans zemini, aynalı duvarlar ve bale barlarıyla donatılmış prova stüdyosu."}
        ],
        komisyon_list=[
            {"name": "Özel Yetenek Sınav Komisyonu", "desc": "Giriş yetenek sınavlarının tasarım ve jüri koordinasyonunu yürütür."},
            {"name": "Staj ve Performans Komisyonu", "desc": "Öğrencilerin dış sahne ve staj etkinliklerini denetler."}
        ],
        sss_list=[
            {"q": "Bölümde hangi anasanat dalları bulunmaktadır?", "a": "Müzik Toplulukları, Ses Sanatları Tasarımı ve Dans anasanat dalları bulunmaktadır."}
        ],
        extra_bologna_links=[
            ("Ses Sanatları Tasarımı Programı", "bologna_ders_plani_ses"),
            ("Dans Programı", "bologna_ders_plani_dans")
        ]
    )
    # MSSB Bologna Curricula
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=208&aid=43", str(mssb_dir / "bologna_ders_plani"), "Müzik Toplulukları", "Müzik ve Sahne Sanatları")
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=206&aid=43", str(mssb_dir / "bologna_ders_plani_ses"), "Ses Sanatları Tasarımı", "Müzik ve Sahne Sanatları")
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=207&aid=43", str(mssb_dir / "bologna_ders_plani_dans"), "Dans", "Müzik ve Sahne Sanatları")

    # -------------------------------------------------------------
    # 3.B İletişim Tasarımı Bölümü
    # -------------------------------------------------------------
    ilet_dir = stf_fac_dir / "iletisim_tasarimi"
    generate_department_core(
        dept_dir=str(ilet_dir),
        dept_name="İletişim Tasarımı",
        faculty_name="Sanat ve Tasarım Fakültesi",
        web_url="https://ilet.yildiz.edu.tr/",
        yerleske="Davutpaşa",
        baskan_info="""- **Bölüm Başkanı:** Prof. Dr. Bahadır UÇAN
- **Bölüm Başkan Yardımcıları:** Tasarım ve staj koordinatörleri
- **Sekreterlik:** Davutpaşa Kampüsü STF İletişim Tasarımı Bölüm Ofisi""",
        staj_detay="""- **Staj Süresi:** 40 İş Günü (20 gün Dijital Medya/Ajans + 20 gün Prodüksiyon/Kurgu).
- **Kurumlar:** Reklam ajansları, dijital oyun stüdyoları, post-prodüksiyon şirketleri, televizyon kanalları ve kurumsal iletişim birimleri.
- **Değerlendirme:** Portfolyo destekli staj raporu komisyonca incelenir.""",
        lab_list=[
            {"name": "Görsel İletişim ve Dijital Medya Laboratuvarı", "desc": "Apple Mac Pro istasyonları, Adobe Creative Cloud ve etkileşimli medya geliştirme yazılımları."},
            {"name": "Animasyon ve Hareketli Grafik Stüdyosu", "desc": "2D/3D animasyon tezgahları, çizim tabletleri ve hareket yakalama düzenekleri."},
            {"name": "Video Kurgu ve Post-Prodüksiyon Ünitesi", "desc": "Renk düzenleme (Color Grading), ses montajı ve efekt işleme stüdyosu."}
        ],
        komisyon_list=[
            {"name": "Staj ve Portfolyo Komisyonu", "desc": "Staj onaylarını ve öğrenci portfolyo değerlendirmelerini yürütür."},
            {"name": "Bitirme Projesi Komisyonu", "desc": "Mezuniyet projelerinin sergi ve sunum organizasyonunu yapar."}
        ],
        sss_list=[
            {"q": "İletişim Tasarımı hangi puan türüyle öğrenci alır?", "a": "YKS Sözel puan türüyle merkezi olarak öğrenci almaktadır."}
        ]
    )
    # İletişim Tasarımı Bologna
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=52&aid=42", str(ilet_dir / "bologna_ders_plani"), "Lisans Programı", "İletişim Tasarımı")

    # -------------------------------------------------------------
    # 3.C Sanat Bölümü
    # -------------------------------------------------------------
    sab_dir = stf_fac_dir / "sanat"
    generate_department_core(
        dept_dir=str(sab_dir),
        dept_name="Sanat",
        faculty_name="Sanat ve Tasarım Fakültesi",
        web_url="https://sab.yildiz.edu.tr/",
        yerleske="Davutpaşa",
        baskan_info="""- **Bölüm Başkanı V.:** Prof. Dr. Kader SÜRMELİ
- **Anasanat Dalı Başkanları:** Bileşik Sanatlar, Grafik Tasarımı, Fotoğraf ve Video, Sanat ve Kültür Yönetimi
- **Sekreterlik:** Davutpaşa Kampüsü STF Sanat Bölüm Bürosu""",
        staj_detay="""- **Staj Süresi:** 30 İş Günü.
- **Kurumlar:** Sanat galerileri, müzeler, yayınevleri, grafik tasarım atölyeleri, fotoğraf stüdyoları ve kültür merkezleri.
- **Değerlendirme:** Staj dosyası ve sanatsal rapor komisyonca değerlendirilir.""",
        lab_list=[
            {"name": "Resim ve Özgün Baskı Atölyesi", "desc": "Litografi, serigrafi, gravür ve litografik baskı presleri."},
            {"name": "Heykel ve Seramik Atölyesi", "desc": "Seramik fırınları, döküm ve modelleme tezgahları."},
            {"name": "Karanlık Oda ve Fotoğraf Stüdyosu", "desc": "Analog film banyosu, optik agrandisörler ve profesyonel flaş ışık sistemleri."},
            {"name": "Grafik Tasarım Laboratuvarı", "desc": "Tipografi, kurumsal kimlik ve ambalaj tasarımı bilgisayar üniteleri."}
        ],
        komisyon_list=[
            {"name": "Sergi ve Etkinlik Komisyonu", "desc": "Öğrenci ve fakülte sergilerinin kürasyonunu ve açılışlarını düzenler."},
            {"name": "Staj ve Dış İlişkiler Komisyonu", "desc": "Kültür-sanat kurumlarıyla staj protokollerini koordine eder."}
        ],
        sss_list=[
            {"q": "Sanat Bölümü altında hangi programlar yer almaktadır?", "a": "Bileşik Sanatlar, Grafik Tasarımı, Fotoğraf ve Video ile Sanat ve Kültür Yönetimi lisans programları yer almaktadır."}
        ],
        extra_bologna_links=[
            ("Grafik Tasarımı Programı", "bologna_ders_plani_grafik"),
            ("Fotoğraf ve Video Programı", "bologna_ders_plani_fotograf"),
            ("Sanat ve Kültür Yönetimi Programı", "bologna_ders_plani_yonetim")
        ]
    )
    # Sanat Bölümü Bologna Curricula
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=259&aid=41", str(sab_dir / "bologna_ders_plani"), "Bileşik Sanatlar", "Sanat")
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=513&aid=41", str(sab_dir / "bologna_ders_plani_grafik"), "Grafik Tasarımı", "Sanat")
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=281&aid=41", str(sab_dir / "bologna_ders_plani_fotograf"), "Fotoğraf ve Video", "Sanat")
    fetch_bologna_curriculum("http://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=263&aid=41", str(sab_dir / "bologna_ders_plani_yonetim"), "Sanat ve Kültür Yönetimi", "Sanat")

    print("\n🎉 TÜM FAKÜLTE, BÖLÜM VE BOLOGNA DOSYALARI BAŞARIYLA OLUŞTURULDU!")

if __name__ == "__main__":
    generate_all()
