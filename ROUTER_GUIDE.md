# YTÜ Bilgi Bankası Yapay Zeka Karar Ağacı ve Yönlendirme Kılavuzu (ROUTER GUIDE)

> [!IMPORTANT]
> **Tüm Yapay Zeka Modelleri İçin ZORUNLU Sistem Talimatı:**
> Kullanıcı Yıldız Teknik Üniversitesi (YTÜ) veya Elektronik ve Haberleşme Mühendisliği (EHM) ile ilgili herhangi bir soru sorduğunda:
> 1. Harici tahminlerde bulunmadan veya genel kültürden cevap vermeden **doğrudan aşağıdaki Karar Ağacı tablosunu izleyin**, ilgili Markdown dosyasını inceleyin ve yasal dayanağını (Madde No, Senato Esas Kodu) belirterek cevap verin.
> 2. **İstisnasız her cevabın sonunda** aşağıda tanımlanan standart blok formatında **Cevabın Kaynağını, Güvenilirlik Düzeyini ve En Güncel Geçerlilik Tarihini** belirtin.

---

## 🧭 Karar Ağacı ve Soru - Dosya Yönlendirme Matrisi

| Kullanıcının Soru Tipi / Konusu | Doğrudan İncelenecek Dosya Yolu | İlgili Madde / Bölüm | Güvenilirlik Seviyesi |
|---|---|---|---|
| **Resmi 2026-2027 Akademik Takvim tarihleri**, ders kayıt, vize/final haftaları, mezuniyet sınavı günleri | `00_genel_ve_kurumsal/akademik_takvim_ve_isleyis.md` | 25.06.2026 / 06-09 Senato Kararı | **Tier 1** (En Yüksek) |
| **Üniversite üst yönetimi, rektör (Prof. Dr. Eyüp Debik)**, daire başkanlıkları, koordinatörlükler, EBYS/OBS | `00_genel_ve_kurumsal/universite_yonetim_ve_kurumsal_yapi.md` | YTÜ Kurumsal Teşkilat Şeması | **Tier 2** (Resmi Portal) |
| **YTÜ tarihi kökleri, Kondüktör Mektebi**, tarihi saray binaları (Çukur Saray, Davutpaşa Kışlası), rektörler listesi, kulüpler | `00_genel_ve_kurumsal/vikipedi_ytu_kulliyati_ve_tarihce.md` | Tarihçe, Yerleşkeler, Kronoloji | **Tier 3** (Ansiklopedik Derleme) |
| **YKS taban puanları, başarı sıralamaları**, kontenjanlar, EHM ve diğer mühendislik sıralama trendleri | `04_bologna_ve_not_sistemi/yks_taban_puanlari_ve_basari_siralamalari.md` | 2026 YKS / 2025-2026 Yerleştirme | **Tier 3** (İstatistiki / Kariyer) |
| **Hoca tavsiyeleri, öğrenci deneyimleri, kampüs dedikoduları, çıkmış sorular, forum tartışmaları** | `00_genel_ve_kurumsal/ogrenci_topluluklari_ve_sosyal_mecralar.md` | Reddit r/ytu, ytuitirafediyor, ytukampus | **Tier 4** (Düşük Güvenilirlik) |
| **Derse devam zorunluluğu**, devamsızlık sınırı, F0 notu | `01_mevzuat_ve_yonetmelikler/lisans_egitim_ogretim_yonetmeligi.md` | Madde 23 (Teorik %70, Lab %80) | **Tier 1** (En Yüksek) |
| **Hazırlık sınıfı devamsızlığı**, devamsızlıktan kalma, YBD kuralları | `03_yabanci_diller_yuksekokulu_ybd/sinav_ve_degerlendirme_kurallari.md` | Devam zorunluluğu %85, SSS 13-22 | **Tier 1 / Tier 2** |
| **Sağlık raporu teslim süresi**, vize mazeret sınavına başvuru | `01_mevzuat_ve_yonetmelikler/senato_esaslari_ve_tablolar/DD-007_mazeret_sinavlari_esaslari.md` | 3 iş günü kuralı, Yarıyıl içi sınavları | **Tier 1** (En Yüksek) |
| **Sınav çakışması**, aynı gün/saatte iki sınav olması | `01_mevzuat_ve_yonetmelikler/yonergeler/YO-075_sinav_yonergesi.md` | Madde 9 (Çakışma mazeret hakkı) | **Tier 1** (En Yüksek) |
| **Sınav notuna itiraz**, maddi hata başvurusu | `01_mevzuat_ve_yonetmelikler/senato_esaslari_ve_tablolar/DD-042_sinav_itiraz_esaslari.md` | 3 iş günü içinde dilekçe | **Tier 1** (En Yüksek) |
| **Yaz okulunda kredi sınırı ve başka üniversiteden alma** | `01_mevzuat_ve_yonetmelikler/yonergeler/YO-007_yaz_okulu_yonergesi.md` | Madde 11 (Maks 9 kredi, %65 kredi, %75 içerik) | **Tier 1** (En Yüksek) |
| **Çift Anadal (ÇAP) ve Yandal başvuru koşulları** | `01_mevzuat_ve_yonetmelikler/yonergeler/YO-098_yatay_gecis_cap_yandal_yonergesi.md` | ÇAP: AGNO >= 3.00, %20; Yandal: AGNO >= 2.50 | **Tier 1** (En Yüksek) |
| **Merkezi yerleştirme puanı ile yatay geçiş (Ek Madde-1)** | `01_mevzuat_ve_yonetmelikler/yonergeler/YO-098_yatay_gecis_cap_yandal_yonergesi.md` | Giriş yılı taban puanı şartı | **Tier 1** (En Yüksek) |
| **Harf notları, AA-FF katsayıları ve geçme koşulları** | `04_bologna_ve_not_sistemi/not_sistemi_ve_harf_notlari.md` | AA=4.0, CC=2.0, DC=1.5, DD=1.0, FF=0.0 | **Tier 1 / Tier 2** |
| **Bağıl değerlendirme, vize ve final ağırlıkları** | `04_bologna_ve_not_sistemi/bagil_degerlendirme_sistemi.md` | Yarıyıl içi %60, Yarıyıl sonu %40 | **Tier 1 / Tier 2** |
| **İkinci öğretimde %10'a girip harç indirimi alma** | `01_mevzuat_ve_yonetmelikler/senato_esaslari_ve_tablolar/DD-040_ikinci_ogretim_yuzde_on_siralamasi.md` | Tüm dersleri başarma, YNO >= 2.00 | **Tier 1** (En Yüksek) |
| **Azami öğrenim süresi (7 yıl) bittiğinde ek sınav hakları** | `01_mevzuat_ve_yonetmelikler/yonergeler/YO-096_azami_ogrenim_suresi_ek_sinav_yonergesi.md` | İki ek sınav hakkı ve ek süreler | **Tier 1** (En Yüksek) |
| **Mezuniyet tek/çift ders sınavı şartları** | `01_mevzuat_ve_yonetmelikler/senato_esaslari_ve_tablolar/DD-015_mezuniyet_sinavi_esaslari.md` | En fazla 2 başarısız ders | **Tier 1** (En Yüksek) |
| **Sınavda kopya çekmenin disiplin cezası** | `01_mevzuat_ve_yonetmelikler/yuksekogretim_ogrenci_disiplin_yonetmeligi.md` | 2547 s.K. Md. 54 (Bir yarıyıl uzaklaştırma) | **Tier 1** (En Yüksek) |
| **İYS baraj puanı, TOEFL / PTE muafiyet puanları** | `03_yabanci_diller_yuksekokulu_ybd/hakkinda_ve_egitim_yapisi.md` | İYS >= 60, TOEFL IBT >= 72, PTE >= 55 | **Tier 1 / Tier 2** |
| **İYS sınavının yapısı, soru tipleri, essay kriterleri** | `03_yabanci_diller_yuksekokulu_ybd/ornek_sinavlar_ve_iys/README.md` | 1. Oturum (%50) & 2. Oturum (%50) | **Tier 2** (Resmi Sınav Arşivi) |
| **EHM staj gün sayısı ve sırası (Genel ve Mesleki)** | `05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/staj_ve_bitirme_esaslari.md` | 30 gün Genel Staj (önce), 30 gün Mesleki Staj | **Tier 1 / Tier 2** |
| **EHM Tasarım Projesi (EHM4200) ve Bitirme (EHM9000)** | `05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/staj_ve_bitirme_esaslari.md` | EHM9000 için EHM4200 zorunlu önkoşuldur | **Tier 1 / Tier 2** |
| **EHM derslerinin önkoşulları (Hangi ders hangisini kilitler?)** | `05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/bologna_ders_plani/onkosul_zinciri.md` | Tam önkoşul tablosu ve Mermaid akış şeması | **Tier 2** (Resmi Bologna) |
| **EHM herhangi bir yarıyılın ders içeriği ve haftalık planı** | `05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/bologna_ders_plani/{1-8}_yariyil.md` | İlgili yarıyıl dosyasındaki ders kartı | **Tier 2** (Resmi Bologna) |
| **EEF Dekanlığı, Fakülte Yönetimi (Dekan Prof. Dr. Ahmet Faruk BAKAN), teşkilat** | `05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/dekanlik_ve_teskilat_yapisi.md` | Dekan, Dekan Yardımcıları, Fakülte Yönetim Kurulu | **Tier 2** (Resmi Fakülte) |
| **EEF Etik İlkeler Yönergesi (YÖ-033), akademik dürüstlük, intihal ve sınav disiplini** | `05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/etik_ilkeler_ve_yonergeler.md` | Senato YÖ-033 Yönergesi | **Tier 1** (En Yüksek) |
| **EEF Fakülte SSS (Fakülte içi yatay geçiş, çift anadal, staj genel kuralları)** | `05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/fakulte_sikca_sorulan_sorular.md` | Resmi Fakülte SSS (12 Soru-Cevap) | **Tier 2** (Resmi Fakülte) |
| **EEF Akran Danışmanlığı Sistemi ve Acil Durum Eylem Planı** | `05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/akran_danismanligi_ve_ogrenci_rehberi.md` | Akran Danışmanları Listesi & Acil Eylem Planı | **Tier 2** (Resmi Fakülte) |
| **Elektrik Mühendisliği (ELM) Lisans müfredatı, 1-8 yarıyıl dersleri** | `05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektrik_muhendisligi/bologna_ders_plani/{1-8}_yariyil.md` | Bologna ID: 7 Ders Planları | **Tier 2** (Resmi Bologna) |
| **Elektrik Mühendisliği (ELM) Staj, Tasarım (ELM4200) ve Bitirme (ELM4901/4902)** | `05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektrik_muhendisligi/staj_tasarim_ve_bitirme_esaslari.md` | 60 gün staj, DD-087 KOOP ve Bitirme | **Tier 1 / Tier 2** |
| **Elektrik Mühendisliği (ELM) Laboratuvarları (Yüksek Gerilim, Elektrik Makineleri vb.)** | `05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektrik_muhendisligi/laboratuvarlar_ve_arastirma.md` | 8 LABSİS Laboratuvarı | **Tier 2** (Resmi Bölüm) |
| **Bilgisayar Mühendisliği (CE) Lisans müfredatı, 1-8 yarıyıl dersleri** | `05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/bilgisayar_muhendisligi/bologna_ders_plani/{1-8}_yariyil.md` | Bologna ID: 550 Ders Planları | **Tier 2** (Resmi Bologna) |
| **Bilgisayar Mühendisliği (CE) Staj, Proje Sistemi (proje-sistemi), Bitirme BLM4900** | `05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/bilgisayar_muhendisligi/staj_ve_proje_sistemi.md` | 60 gün staj ve Dijital Proje Teslimi | **Tier 1 / Tier 2** |
| **Bilgisayar Mühendisliği (CE) Resmi Sıkça Sorulan Sorular (44 SSS Türkçe/İngilizce)** | `05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/bilgisayar_muhendisligi/sikca_sorulan_sorular.md` | CE API Veritabanı (44 Soru) | **Tier 2** (Resmi Bölüm) |
| **Bilgisayar Mühendisliği (CE) Araştırma Labları ve Sky Lab Öğrenci Kulübü** | `05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/bilgisayar_muhendisligi/laboratuvarlar_ve_arastirma.md` | LABSİS Araştırma Laboratuvarları | **Tier 2** (Resmi Bölüm) |
| **Kontrol ve Otomasyon Mühendisliği (KOM) %30 ve %100 İngilizce Bologna Ders Planları** | `05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/kontrol_ve_otomasyon_muhendisligi/bologna_ders_plani_{yuzde30,yuzde100}/` | Bologna ID: 29 & 403 | **Tier 2** (Resmi Bologna) |
| **Kontrol ve Otomasyon Mühendisliği (KOM) Staj ve Bitirme (KOM9000)** | `05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/kontrol_ve_otomasyon_muhendisligi/staj_ve_bitirme_esaslari.md` | 60 gün staj, KOM9000 Şablonları | **Tier 1 / Tier 2** |
| **Kontrol ve Otomasyon Mühendisliği (KOM) Sanayi Laboratuvarları (Omron, Schneider, Phoenix Contact)** | `05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/kontrol_ve_otomasyon_muhendisligi/laboratuvarlar_ve_arastirma.md` | Endüstri Destekli PLC & Otomasyon Labları | **Tier 2** (Resmi Bölüm) |
| **Biyomedikal Mühendisliği (BME) Lisans (%100 İngilizce) Ders Planı** | `05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/biyomedikal_muhendisligi/bologna_ders_plani/{1-8}_yariyil.md` | Bologna ID: 504 (%100 İngilizce) | **Tier 2** (Resmi Bologna) |
| **Biyomedikal Mühendisliği (BME) Hastane/Klinik Stajı ve Çok Disiplinli Tasarım (ÇDTP)** | `05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/biyomedikal_muhendisligi/staj_ve_cdtp_esaslari.md` | Staj 1 (Hastane), ÇDTP ve Bitirme | **Tier 1 / Tier 2** |
| **Yapay Zeka ve Veri Mühendisliği (AI) Lisans (%100 İngilizce) Ders Planı** | `05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/yapay_zeka_ve_veri_muhendisligi/bologna_ders_plani/{1-8}_yariyil.md` | Bologna ID: 557 (YZM Kodlu Dersler) | **Tier 2** (Resmi Bologna) |
| **Yapay Zeka ve Veri Mühendisliği (AI) Staj, Yüksek Lisans ve GPU/Donanım Altyapısı** | `05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/yapay_zeka_ve_veri_muhendisligi/{staj_ve_formlar,laboratuvarlar_ve_arastirma}.md` | Bölüm Altyapısı ve Staj Kuralları | **Tier 2** (Resmi Bölüm) |
| **Makine Fakültesi Dekanlığı, Teşkilat (Dekan Prof. Dr. Zehra YUMURTACI), Yönetim** | `05_fakulteler_ve_bolumler/makine_fakultesi/dekanlik_ve_teskilat_yapisi.md` | Dekan, Dekan Yardımcıları, Fakülte Kurulu | **Tier 2** (Resmi Fakülte) |
| **Makine Fakültesi SSS, Staj ve KOOP Genel Kuralları** | `05_fakulteler_ve_bolumler/makine_fakultesi/{fakulte_sikca_sorulan_sorular,staj_ve_koop_genel_esaslari}.md` | Fakülte SSS ve Staj Esasları | **Tier 2** (Resmi Fakülte) |
| **Makine Mühendisliği (MKM) Lisans Müfredatı (%30 İngilizce), 1-8. Yarıyıllar** | `05_fakulteler_ve_bolumler/makine_fakultesi/makine_muhendisligi/bologna_ders_plani/{1-8}_yariyil.md` | Bologna ID: 391 Ders Planları | **Tier 2** (Resmi Bologna) |
| **Makine Mühendisliği (MKM) Otomotiv ve İmalat Stajı, ÇAP Eşlenik Dersleri** | `05_fakulteler_ve_bolumler/makine_fakultesi/makine_muhendisligi/staj_tasarim_ve_bitirme_esaslari.md` | 60 gün staj, ÇAP tablosu, Makine Tasarımı | **Tier 1 / Tier 2** |
| **Endüstri Mühendisliği (ENM) Lisans Müfredatı (%30 ve %100 İngilizce)** | `05_fakulteler_ve_bolumler/makine_fakultesi/endustri_muhendisligi/bologna_ders_plani_{yuzde30,yuzde100}/` | Bologna ID: 45 & 405 | **Tier 2** (Resmi Bologna) |
| **Endüstri Mühendisliği (ENM) ÇDTP (Multidisciplinary Project), FR-1917, END4000** | `05_fakulteler_ve_bolumler/makine_fakultesi/endustri_muhendisligi/staj_tasarim_ve_bitirme_esaslari.md` | ÇDTP Şablonu, END4000 Tez Kılavuzu | **Tier 1 / Tier 2** |
| **Mekatronik Mühendisliği (MKT) Lisans Müfredatı (%30 ve %100 İngilizce)** | `05_fakulteler_ve_bolumler/makine_fakultesi/mekatronik_muhendisligi/bologna_ders_plani_{yuzde30,yuzde100}/` | Bologna ID: 46 & 404 | **Tier 2** (Resmi Bologna) |
| **Mekatronik Mühendisliği (MKT) MST Tasarım, Bitirme Çalışması Kılavuzu ve Staj** | `05_fakulteler_ve_bolumler/makine_fakultesi/mekatronik_muhendisligi/staj_tasarim_ve_bitirme_esaslari.md` | 2026-2027 MST ve Bitirme Kılavuzu | **Tier 1 / Tier 2** |
| **Kimya-Metalurji Fakültesi Dekanlığı, Teşkilat (Dekan Prof. Dr. Musa TÜRKER)** | `05_fakulteler_ve_bolumler/kimya_metalurji_fakultesi/dekanlik_ve_teskilat_yapisi.md` | Dekan, Dekan Yardımcıları, Yönetim Kurulu | **Tier 2** (Resmi Fakülte) |
| **Kimya-Metalurji Fakültesi Hizmet Standartları, SSS ve Acil Eylem Planı** | `05_fakulteler_ve_bolumler/kimya_metalurji_fakultesi/{hizmet_standartlari_ve_envanteri,fakulte_sikca_sorulan_sorular}.md` | Hizmet Standart Tablosu ve Envanter | **Tier 2** (Resmi Fakülte) |
| **Biyomühendislik (BIOENG) Lisans Müfredatları (%30 ve %100 İngilizce)** | `05_fakulteler_ve_bolumler/kimya_metalurji_fakultesi/biyomuhendislik/bologna_ders_plani_{yuzde30,yuzde100}/` | Bologna ID: 147 & 163 | **Tier 2** (Resmi Bologna) |
| **Biyomühendislik (BIOENG) Staj Yönetmeliği, Hastane ve Biyoreaktör Labları** | `05_fakulteler_ve_bolumler/kimya_metalurji_fakultesi/biyomuhendislik/{staj_tasarim_ve_bitirme_esaslari,laboratuvarlar_ve_arastirma}.md` | 60 gün staj, Biyoproses ve Güvenlik | **Tier 1 / Tier 2** |
| **Gıda Mühendisliği (FOOD) Lisans Müfredatı (%30 İngilizce), 1-8. Yarıyıllar** | `05_fakulteler_ve_bolumler/kimya_metalurji_fakultesi/gida_muhendisligi/bologna_ders_plani/{1-8}_yariyil.md` | Bologna ID: 195 Ders Planı | **Tier 2** (Resmi Bologna) |
| **Gıda Mühendisliği (FOOD) Laboratuvar Güvenlik Kuralları ve Staj Esasları** | `05_fakulteler_ve_bolumler/kimya_metalurji_fakultesi/gida_muhendisligi/{staj_tasarim_ve_bitirme_esaslari,laboratuvarlar_ve_arastirma}.md` | 60 gün staj (Analiz/İşletme), Güvenlik | **Tier 1 / Tier 2** |
| **Kimya Mühendisliği (KMM) Lisans Müfredatları (%30 ve %100 İngilizce)** | `05_fakulteler_ve_bolumler/kimya_metalurji_fakultesi/kimya_muhendisligi/bologna_ders_plani_{yuzde30,yuzde100}/` | Bologna ID: 36 & 398 | **Tier 2** (Resmi Bologna) |
| **Kimya Mühendisliği (KMM) Staj Rehberi, FR-0750/0751, Bitirme Esasları** | `05_fakulteler_ve_bolumler/kimya_metalurji_fakultesi/kimya_muhendisligi/{staj_tasarim_ve_bitirme_esaslari,laboratuvarlar_ve_arastirma}.md` | Laboratuvar ve İşletme Stajı, Güvenlik | **Tier 1 / Tier 2** |
| **Matematik Mühendisliği (MTM) Lisans Müfredatları (%30 ve %100 İngilizce)** | `05_fakulteler_ve_bolumler/kimya_metalurji_fakultesi/matematik_muhendisligi/bologna_ders_plani_{yuzde30,yuzde100}/` | Bologna ID: 37 & 222 | **Tier 2** (Resmi Bologna) |
| **Matematik Mühendisliği (MTM) Staj 1 (Donanım) ve Staj 2 (Yazılım) Defterleri** | `05_fakulteler_ve_bolumler/kimya_metalurji_fakultesi/matematik_muhendisligi/staj_tasarim_ve_bitirme_esaslari.md` | Resmi MTM Staj Defteri Formatı | **Tier 1 / Tier 2** |
| **Metalurji ve Malzeme Müh. (MET) Lisans Müfredatları (%30 ve %100 İngilizce)** | `05_fakulteler_ve_bolumler/kimya_metalurji_fakultesi/metalurji_ve_malzeme_muhendisligi/bologna_ders_plani_{yuzde30,yuzde100}/` | Bologna ID: 38 & 401 | **Tier 2** (Resmi Bologna) |
| **Metalurji ve Malzeme Müh. (MET) STAJ-1/2, Yürütme Esasları, Döküm ve SEM Labı** | `05_fakulteler_ve_bolumler/kimya_metalurji_fakultesi/metalurji_ve_malzeme_muhendisligi/{staj_tasarim_ve_bitirme_esaslari,laboratuvarlar_ve_arastirma}.md` | Metalurjik Prosesler ve Şekillendirme | **Tier 1 / Tier 2** |
| **İnşaat Fakültesi Dekanlığı, Teşkilatı, DD-074 Staj İlkeleri ve SSS** | `05_fakulteler_ve_bolumler/insaat_fakultesi/{README,dekanlik_ve_teskilat_yapisi,fakulte_sikca_sorulan_sorular,staj_uygulama_ilkeleri}.md` | Davutpaşa Yerleşkesi, DD-074 | **Tier 1 / Tier 2** |
| **İnşaat Mühendisliği (INM) Lisans Müfredatları (%30 ve %100 İngilizce)** | `05_fakulteler_ve_bolumler/insaat_fakultesi/insaat_muhendisligi/bologna_ders_plani{,_yuzde100}/{1-8}_yariyil.md` | Bologna ID: 40 & 397 | **Tier 2** (Resmi Bologna) |
| **İnşaat Mühendisliği (INM) Şantiye/Büro Stajı, Zemin ve Yapı Mekaniği Labları** | `05_fakulteler_ve_bolumler/insaat_fakultesi/insaat_muhendisligi/{staj_tasarim_ve_bitirme_esaslari,laboratuvarlar_ve_arastirma}.md` | 60 gün staj, Kutay Özaydın Labı | **Tier 1 / Tier 2** |
| **Çevre Mühendisliği (CEM) Lisans Müfredatı (%30 İngilizce), 1-8. Yarıyıllar** | `05_fakulteler_ve_bolumler/insaat_fakultesi/cevre_muhendisligi/bologna_ders_plani/{1-8}_yariyil.md` | Bologna ID: 43 | **Tier 2** (Resmi Bologna) |
| **Çevre Mühendisliği (CEM) DD-071 Staj Esasları, Su ve Arıtma Laboratuvarları** | `05_fakulteler_ve_bolumler/insaat_fakultesi/cevre_muhendisligi/{staj_tasarim_ve_bitirme_esaslari,laboratuvarlar_ve_arastirma}.md` | DD-071, 60 gün arıtma stajı | **Tier 1 / Tier 2** |
| **Harita Mühendisliği (HRM / Geomatik) Lisans Müfredatı (%30 İngilizce)** | `05_fakulteler_ve_bolumler/insaat_fakultesi/harita_muhendisligi/bologna_ders_plani/{1-8}_yariyil.md` | Bologna ID: 44 | **Tier 2** (Resmi Bologna) |
| **Harita Mühendisliği (HRM) CBS, Fotogrametri, Arazi Ölçme Stajı ve Labları** | `05_fakulteler_ve_bolumler/insaat_fakultesi/harita_muhendisligi/{staj_tasarim_ve_bitirme_esaslari,laboratuvarlar_ve_arastirma}.md` | 60 gün ölçme/CBS stajı | **Tier 1 / Tier 2** |
| **Gemi İnşaatı ve Denizcilik Fakültesi (GİDF) Dekanlığı, Teşkilatı ve STCW** | `05_fakulteler_ve_bolumler/gemi_insaati_ve_denizcilik_fakultesi/{README,dekanlik_ve_teskilat_yapisi,staj_ve_deniz_egitimi_esaslari}.md` | Beşiktaş Kampüsü, STCW | **Tier 1 / Tier 2** |
| **Gemi İnşaatı ve Gemi Makineleri (GİM) Lisans Müfredatı (%30 İngilizce)** | `05_fakulteler_ve_bolumler/gemi_insaati_ve_denizcilik_fakultesi/gemi_insaati_ve_gemi_makineleri_muhendisligi/bologna_ders_plani/{1-8}_yariyil.md` | Bologna ID: 48 | **Tier 2** (Resmi Bologna) |
| **GİM Tersane Stajı, Çekme Tankı ve Gemi Dizayn Laboratuvarları** | `05_fakulteler_ve_bolumler/gemi_insaati_ve_denizcilik_fakultesi/gemi_insaati_ve_gemi_makineleri_muhendisligi/{staj_tasarim_ve_bitirme_esaslari,laboratuvarlar_ve_arastirma}.md` | 60 gün tersane stajı, Çekme tankı | **Tier 1 / Tier 2** |
| **Gemi Makineleri İşletme (GMİM) Lisans Müfredatı (%30 İngilizce)** | `05_fakulteler_ve_bolumler/gemi_insaati_ve_denizcilik_fakultesi/gemi_makineleri_isletme_muhendisligi/bologna_ders_plani/{1-8}_yariyil.md` | Bologna ID: 141 | **Tier 2** (Resmi Bologna) |
| **GMİM 150 Gün Atölye ve 180 Gün Açık Deniz Stajı, Simülatör Labı, GASM** | `05_fakulteler_ve_bolumler/gemi_insaati_ve_denizcilik_fakultesi/gemi_makineleri_isletme_muhendisligi/{staj_tasarim_ve_bitirme_esaslari,laboratuvarlar_ve_arastirma}.md` | Liman Cüzdanı, Çarkçıbaşı | **Tier 1 / Tier 2** |
| **Mimarlık Fakültesi Dekanlığı, Teşkilatı (Dekan Prof. Dr. Sırma TURGUT) ve Staj/Atölye Esasları** | `05_fakulteler_ve_bolumler/mimarlik_fakultesi/{README,dekanlik_ve_teskilat_yapisi,fakulte_sikca_sorulan_sorular,staj_ve_atolye_esaslari}.md` | Tarihi Yıldız Yerleşkesi, Atölye Kuralları | **Tier 2** (Resmi Fakülte) |
| **Mimarlık (MİM) %30 ve %100 İngilizce Bologna Müfredatları, Stüdyo ve Şantiye/Büro Stajı** | `05_fakulteler_ve_bolumler/mimarlik_fakultesi/mimarlik/{bologna_ders_plani,bologna_ders_plani_yuzde100,staj_tasarim_ve_bitirme_esaslari}.md` | Bologna ID: 50 & 429, MİAK / NAAB | **Tier 1 / Tier 2** |
| **Şehir ve Bölge Planlama (ŞBP) Bologna Müfredatı, Planlama Stüdyosu ve CBS Labı** | `05_fakulteler_ve_bolumler/mimarlik_fakultesi/sehir_ve_bolge_planlama/{bologna_ders_plani,staj_tasarim_ve_bitirme_esaslari,laboratuvarlar_ve_arastirma}.md` | Bologna ID: 51, Kamu ve Büro Stajı | **Tier 2** (Resmi Bölüm/Bologna) |
| **Endüstriyel Tasarım Lisans Müfredatı, Ürün Tasarım Stüdyoları ve Prototip Labı** | `05_fakulteler_ve_bolumler/mimarlik_fakultesi/endustriyel_tasarim/{bologna_ders_plani,staj_tasarim_ve_bitirme_esaslari,laboratuvarlar_ve_arastirma}.md` | Bologna ID: 516, Üretim ve Ofis Stajı | **Tier 2** (Resmi Bölüm/Bologna) |
| **İktisadi ve İdari Bilimler Fakültesi (İİBF) Dekanlığı (Dekan Prof. Dr. Yasin ŞEHİTOĞLU), Kariyer ve Staj** | `05_fakulteler_ve_bolumler/iktisadi_ve_idari_bilimler_fakultesi/{README,dekanlik_ve_teskilat_yapisi,staj_ve_kariyer_esaslari}.md` | Davutpaşa Taş Kışla, SGK ve Kariyer | **Tier 2** (Resmi Fakülte) |
| **İktisat Bölümü %30 ve %100 İngilizce Bologna Müfredatları ve Ekonometri Labı** | `05_fakulteler_ve_bolumler/iktisadi_ve_idari_bilimler_fakultesi/iktisat/{bologna_ders_plani,bologna_ders_plani_yuzde100,laboratuvarlar_ve_arastirma}.md` | Bologna ID: 54 & 535, Finans Labı | **Tier 2** (Resmi Bölüm/Bologna) |
| **İşletme Bölümü %30 ve %100 İngilizce Bologna Müfredatları, ERP/SAP Simülasyonu** | `05_fakulteler_ve_bolumler/iktisadi_ve_idari_bilimler_fakultesi/isletme/{bologna_ders_plani,bologna_ders_plani_yuzde100,laboratuvarlar_ve_arastirma}.md` | Bologna ID: 55 & 539, Denetim/Pazarlama | **Tier 2** (Resmi Bölüm/Bologna) |
| **Siyaset Bilimi ve Uluslararası İlişkiler (SBUI) Bologna Müfredatı ve Diplomasi Simülasyonu** | `05_fakulteler_ve_bolumler/iktisadi_ve_idari_bilimler_fakultesi/siyaset_bilimi_ve_uluslararasi_iliskiler/{bologna_ders_plani,laboratuvarlar_ve_arastirma}.md` | Bologna ID: 56, MUN ve Dışişleri | **Tier 2** (Resmi Bölüm/Bologna) |
| **Sanat ve Tasarım Fakültesi (STF) Dekanlığı (Dekan Prof. Dr. Mehmet Emin KAHRAMAN) ve Özel Yetenek** | `05_fakulteler_ve_bolumler/sanat_ve_tasarim_fakultesi/{README,dekanlik_ve_teskilat_yapisi,ozel_yetenek_ve_sanatsal_etkinlik_esaslari}.md` | Davutpaşa STF Binası, Otağ-ı Hümayun | **Tier 2** (Resmi Fakülte) |
| **Müzik ve Sahne Sanatları (MSSB) Müzik, Ses Tasarımı, Dans Müfredatları ve Kayıt Stüdyosu** | `05_fakulteler_ve_bolumler/sanat_ve_tasarim_fakultesi/muzik_ve_sahne_sanatlari/{bologna_ders_plani,bologna_ders_plani_ses,bologna_ders_plani_dans}.md` | Bologna ID: 208, 206, 207 | **Tier 2** (Resmi Bölüm/Bologna) |
| **İletişim Tasarımı Lisans Müfredatı, UI/UX, Animasyon ve Video Kurgu Laboratuvarları** | `05_fakulteler_ve_bolumler/sanat_ve_tasarim_fakultesi/iletisim_tasarimi/{bologna_ders_plani,laboratuvarlar_ve_arastirma}.md` | Bologna ID: 52, Medya/Ajans Stajı | **Tier 2** (Resmi Bölüm/Bologna) |
| **Sanat Bölümü (Bileşik Sanatlar, Grafik, Fotoğraf, Sanat Yönetimi) Müfredatları ve Atölyeler** | `05_fakulteler_ve_bolumler/sanat_ve_tasarim_fakultesi/sanat/{bologna_ders_plani,bologna_ders_plani_grafik,bologna_ders_plani_fotograf,bologna_ders_plani_yonetim}.md` | Bologna ID: 259, 513, 281, 263 | **Tier 2** (Resmi Bölüm/Bologna) |


---

## 📌 ZORUNLU CEVAP SONU FORMATI (HER YANITIN SONUNA EKLENECEKTİR)

Herhangi bir agent veya yapay zeka modeli yanıt verirken yanıtını aşağıdaki standart doğrulama bloğu ile kapatmalıdır:

```markdown
---
### 📌 Kaynak ve Güvenilirlik Bilgisi
- **Birincil Kaynak:** [Belge veya Sayfa Adı](dosya-yolu-veya-link)
- **Güvenilirlik Düzeyi:** [Tier 1 (Resmi Mevzuat) | Tier 2 (Resmi Portal) | Tier 3 (İkincil / İstatistiki) | Tier 4 (Düşük Güvenilirlik - Gayriresmî Topluluk/Forum)]
- **Geçerlilik / Güncelleme Tarihi:** [İlgili Belgenin Yılı veya Karar Tarihi, örn: 2026-2027]
- **Yasal Dayanak / Belge No:** [Örn: YTÜ Lisans Eğitim-Öğretim Yönetmeliği Madde 23 / YÖ-075 / 25.06.2026 Senato Kararı / Gayriresmî Topluluk Paylaşımı]
```

---

## ⚖️ Kesin Hukuki Hiyerarşi

Bilgiler arasında çelişki olması halinde daima şu üstünlük sırası geçerlidir:
1. **Tier 1 (Resmi Kanun, Yönetmelik ve Senato Esasları - En Yüksek)**
2. **Tier 2 (Resmi Birim Web Portalları ve Bologna Bilgi Sistemi)**
3. **Tier 3 (Kariyer.net, Vikipedi ve Diğer Dış İkincil Kaynaklar)**
4. **Tier 4 (Reddit r/ytu, ytuitirafediyor, ytukampus - Düşük Güvenilirlik / Doğrulamaya Muhtaç)**
