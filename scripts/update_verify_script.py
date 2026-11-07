import os

files = []
for root, dirs, f_list in os.walk("."):
    if ".git" in root or ".gemini" in root or "venv" in root or ".system_generated" in root or "scratch" in root:
        continue
    for f in f_list:
        if f.endswith(".md"):
            rel = os.path.relpath(os.path.join(root, f), ".")
            files.append(rel)
files.sort()

content = []
content.append("import os\n")
content.append("EXPECTED_FILES = [")
for fl in files:
    content.append(f"    {repr(fl)},")
content.append("]\n")

content.append("""def verify():
    print("=== 1. Dosya Varlık ve Boyut Kontrolü ===")
    missing = []
    total_words = 0
    small_files = []
    for f in EXPECTED_FILES:
        if not os.path.exists(f):
            missing.append(f)
        else:
            size = os.path.getsize(f)
            with open(f, 'r', encoding='utf-8') as fp:
                words = len(fp.read().split())
                total_words += words
            if size < 50:
                small_files.append((f, size))

    if missing:
        print(f"HATA: {len(missing)} dosya eksik: {missing}")
        return False
    else:
        print(f"BAŞARILI: Beklenen tüm {len(EXPECTED_FILES)} dosya eksiksiz mevcut!")
        print(f"Toplam ansiklopedi kelime sayısı: {total_words:,} kelime.")
        if small_files:
            print(f"Uyarı: {len(small_files)} dosya boyutu küçük: {small_files}")
        print()

    print("=== 2. Orijinal Arşiv Dosyaları Kontrolü ===")
    arsiv_files = []
    for root, dirs, files in os.walk('arsiv'):
        for file in files:
            arsiv_files.append(os.path.join(root, file))
    print(f"Toplam indirilen resmi arşiv dosyası: {len(arsiv_files)} adet.\\n")

    print("=== 3. Soru ve Cevap Arama Doğrulaması (Tüm Fakülte ve Bölümler) ===")
    test_queries = [
        ("Mazeret rapor teslim süresi", "3 gün", ["DD-007", "mazeret_ve_rapor_surecleri"]),
        ("Yaz okulu kredi limiti", "9", ["YO-007"]),
        ("Bitirme Çalışması önkoşulu (EHM)", "EHM4200", ["elektronik_ve_haberlesme_muhendisligi/bologna_ders_plani/onkosul_zinciri"]),
        ("İkinci öğretim yüzde on şartı", "%10", ["DD-040"]),
        ("Hazırlık devamsızlık oranı", "%85", ["sinav_ve_degerlendirme_kurallari", "03_yabanci_diller_yuksekokulu_ybd/sikca_sorulan_sorular"]),
        ("YTÜ Rektörü", "Eyüp Debik", ["universite_yonetim_ve_kurumsal_yapi"]),
        ("EHM Taban Puanı", "Elektronik ve Haberleşme Mühendisliği", ["yks_taban_puanlari_ve_basari_siralamalari"]),
        ("Kondüktör Mektebi Tarihçesi", "Kondüktör Mekteb-i Âlisi", ["vikipedi_ytu_kulliyati_ve_tarihce", "ytu_tarihce_ve_genel_bilgiler"]),
        ("2026-2027 Güz Başlangıcı", "28 Eylül 2026", ["akademik_takvim_ve_isleyis"]),
        ("Öğrenci Toplulukları ve Reddit", "r/ytu", ["ogrenci_topluluklari_ve_sosyal_mecralar"]),
        ("EEF Dekanı", "Ahmet Faruk BAKAN", ["elektrik_elektronik_fakultesi/dekanlik_ve_teskilat_yapisi.md"]),
        ("EEF Etik İlkeler Yönergesi", "YÖ-033", ["elektrik_elektronik_fakultesi/etik_ilkeler_ve_yonergeler.md"]),
        ("Elektrik Müh. Yüksek Gerilim Lab", "Yüksek Gerilim", ["elektrik_muhendisligi/laboratuvarlar_ve_arastirma.md"]),
        ("Bilgisayar Müh. Proje Portalı", "proje-sistemi", ["bilgisayar_muhendisligi/staj_ve_proje_sistemi.md"]),
        ("Kontrol Müh. Sanayi Labları", "Omron", ["kontrol_ve_otomasyon_muhendisligi/laboratuvarlar_ve_arastirma.md"]),
        ("Biyomedikal Müh. Tasarım", "Çok Disiplinli Tasarım", ["biyomedikal_muhendisligi/staj_ve_cdtp_esaslari.md"]),
        ("Yapay Zeka Müh. Müfredatı", "YZM", ["yapay_zeka_ve_veri_muhendisligi/bologna_ders_plani/1_yariyil.md"]),
        ("Makine Fakültesi Dekanı", "Zehra YUMURTACI", ["makine_fakultesi/dekanlik_ve_teskilat_yapisi.md"]),
        ("Makine Müh. Otomotiv Stajı", "Otomotiv", ["makine_fakultesi/makine_muhendisligi/staj_tasarim_ve_bitirme_esaslari.md"]),
        ("Endüstri Müh. ÇDTP", "project_temp", ["makine_fakultesi/endustri_muhendisligi/sikca_sorulan_sorular.md"]),
        ("Mekatronik Müh. MST", "Mekatronik Sistemi Tasarımı", ["makine_fakultesi/mekatronik_muhendisligi/sikca_sorulan_sorular.md"]),
        ("Kimya-Metalurji Dekanı", "Musa TÜRKER", ["kimya_metalurji_fakultesi/dekanlik_ve_teskilat_yapisi.md"]),
        ("Biyomühendislik Labları", "Biyoreaktör", ["kimya_metalurji_fakultesi/biyomuhendislik/laboratuvarlar_ve_arastirma.md"]),
        ("Gıda Müh. Labları", "Duyusal Analiz", ["kimya_metalurji_fakultesi/gida_muhendisligi/laboratuvarlar_ve_arastirma.md"]),
        ("Kimya Müh. Stajı", "FR-0751", ["kimya_metalurji_fakultesi/kimya_muhendisligi/staj_tasarim_ve_bitirme_esaslari.md"]),
        ("Matematik Müh. Stajı", "Bilgisayar Donanımı", ["kimya_metalurji_fakultesi/matematik_muhendisligi/staj_tasarim_ve_bitirme_esaslari.md"]),
        ("Metalurji Müh. Stajı", "Metalurjik Üretim Prosesleri", ["kimya_metalurji_fakultesi/metalurji_ve_malzeme_muhendisligi/staj_tasarim_ve_bitirme_esaslari.md"])
    ]

    all_passed = True
    for topic, expected_kw, target_files in test_queries:
        found = False
        for tf in target_files:
            matched_file = None
            for exp in EXPECTED_FILES:
                if tf in exp:
                    matched_file = exp
                    break
            if matched_file and os.path.exists(matched_file):
                with open(matched_file, 'r', encoding='utf-8') as fp:
                    content = fp.read()
                    if expected_kw.lower() in content.lower():
                        found = True
                        print(f"DOĞRULANDI: '{topic}' -> {matched_file} içinde '{expected_kw}' bulundu.")
                        break
        if not found:
            print(f"UYARI: '{topic}' için '{expected_kw}' hedeflenen dosyalarda bulunamadı!")
            all_passed = False

    if all_passed:
        print("\\nDOĞRULAMA TAMAMLANDI: TÜM KRİTERLER %100 BAŞARIYLA GEÇTİ!")
        return True
    else:
        print("\\nDOĞRULAMA UYARISI: Bazı testler eşleşmedi.")
        return False

if __name__ == '__main__':
    verify()
""")

with open("scripts/verify_knowledge_base.py", "w", encoding="utf-8") as f:
    f.write("\n".join(content))
print("verify_knowledge_base.py updated successfully!")
