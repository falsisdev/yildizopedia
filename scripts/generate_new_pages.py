import os
import re

def write_file(path, content):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {path}")

# ========================================================
# 1. 00_genel_ve_kurumsal/universite_yonetim_ve_kurumsal_yapi.md
# ========================================================
write_file(
    "00_genel_ve_kurumsal/universite_yonetim_ve_kurumsal_yapi.md",
    """---
baslik: "YTÜ Üniversite Yönetimi, Kurumsal Yapı ve Daire Başkanlıkları"
kaynak_url: "https://yildiz.edu.tr/universite"
arsivlenmis_belge: "arsiv/mevzuat_ve_yonergeler/ytu_ogrenci_rehberi.pdf"
kategori: "kurumsal_yapi"
guvenilirlik_duzeyi: "Tier 2 (Resmi Üniversite Portalı ve Öğrenci Rehberi)"
son_guncelleme_tarihi: "2026-2027"
anahtar_kelimeler: ["rektörlük", "eyüp debik", "senato", "yönetim kurulu", "daire başkanlıkları", "koordinatörlükler", "ebys", "obs", "avesis"]
---

# YTÜ Üniversite Yönetimi ve Kurumsal Yapısı

> [!NOTE] Özet
> Yıldız Teknik Üniversitesi (YTÜ), 2547 sayılı Yükseköğretim Kanunu çerçevesinde Rektörlük, Üniversite Senatosu, Üniversite Yönetim Kurulu, Genel Sekreterlik, Daire Başkanlıkları ve Koordinatörlükler hiyerarşisiyle yönetilen bir "Araştırma Üniversitesi"dir.

## 1. Üst Yönetim ve Karar Organları

### Rektörlük
- **Rektör:** Prof. Dr. Eyüp Debik
- **Görev ve Yetki:** Üniversitenin ve bağlı birimlerinin öğretim kapasitesinin rasyonel bir biçimde kullanılmasını, geliştirilmesini, öğrencilere gerekli sosyal hizmetlerin sağlanmasını ve eğitim-öğretim, bilimsel araştırma ve yayım faaliyetlerinin devlet plan ve ilkeleri doğrultusunda yürütülmesini sağlar.
- **Rektör Yardımcılıkları:**
  - Eğitim-Öğretim Rektör Yardımcılığı
  - Araştırma-Geliştirme ve İnovasyon Rektör Yardımcılığı
  - İdari ve Mali İşler / Yerleşkeler Rektör Yardımcılığı

### Üniversite Senatosu
- Üniversitenin akademik organıdır. Rektör başkanlığında, rektör yardımcıları, dekanlar ve her fakülteden fakülte kurullarınca seçilen birer temsilci öğretim üyesinden oluşur.
- Yönetmelikleri, senato esaslarını ve akademik takvimi karara bağlar.

### Üniversite Yönetim Kurulu
- Üniversitenin idari organıdır. Rektör başkanlığında, dekanlar ve Senato tarafından belirlenen profesör üyelerden oluşur.

---

## 2. İdari Teşkilat ve Daire Başkanlıkları

1. **Öğrenci İşleri Daire Başkanlığı (OGİ):** Öğrenci kayıtları, ders seçimleri, transkript, mezuniyet ve askerlik tecil işlemlerini yürütür (Davutpaşa Kışla Binası A-Blok).
2. **Sağlık, Kültür ve Spor Daire Başkanlığı (SKS):** Yemekhane hizmetleri, öğrenci kulüpleri, spor tesisleri, burs ve mediko-sosyal sağlık hizmetlerini koordine eder.
3. **Kütüphane ve Dokümantasyon Daire Başkanlığı:** Davutpaşa ve Yıldız yerleşkelerindeki kütüphanelerin yönetimi, 7/24 çalışma salonları ve elektronik veritabanı aboneliklerini sağlar.
4. **Bilgi İşlem Daire Başkanlığı (BİDB):** Kampüs internet altyapısı (Eduroam), OBS, e-posta hesapları ve dijital altyapıyı yönetir.
5. **Personel Daire Başkanlığı:** Akademik ve idari personelin özlük haklarını yürütür.
6. **İdari ve Mali İşler Daire Başkanlığı:** Üniversitenin bütçe, lojistik ve satın alma operasyonlarını yönetir.
7. **Yapı İşleri ve Teknik Daire Başkanlığı:** Kampüs binalarının inşası, bakım ve onarım işlerini yürütür.

---

## 3. Temel Dijital Yönetim Sistemleri

- **OBS (Öğrenci Bilgi Sistemi / USIS):** `https://obs.yildiz.edu.tr/` - Ders kayıtları, harf notları, devamsızlık ve transkript.
- **Online Kampüs / UZEM:** `https://online.yildiz.edu.tr/` - Uzaktan eğitim, ders modülleri ve çevrim içi sınavlar.
- **EBYS (Elektronik Belge Yönetim Sistemi):** `https://ebys.yildiz.edu.tr/` - Resmi yazışmalar ve dilekçeler.
- **BKYS (Kalite Yönetim Sistemi):** `https://bkys.yildiz.edu.tr/` - Şikayet, öneri ve memnuniyet yönetim sistemi.
- **AVESİS:** `https://avesis.yildiz.edu.tr/` - Akademik veri yönetim ve öğretim üyesi yayın sistemi.

---

## 4. İletişim ve Yerleşke Bilgileri

- **Yıldız Yerleşkesi (Tarihi Merkez):** Barbaros Bulvarı 34349 Yıldız - Beşiktaş / İstanbul | Tel: 0212 383 70 70
- **Davutpaşa Yerleşkesi (Ana Kampüs):** Davutpaşa Mah. Davutpaşa Cad. 34220 Esenler / İstanbul | Tel: 0212 383 70 70
- **Resmi Web:** https://yildiz.edu.tr/

---
### 📌 Kaynak ve Güvenilirlik Bilgisi
- **Birincil Kaynak:** [YTÜ Üniversite Portalı](https://yildiz.edu.tr/universite) ve [YTÜ Öğrenci Rehberi](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/arsiv/mevzuat_ve_yonergeler/ytu_ogrenci_rehberi.pdf)
- **Güvenilirlik Düzeyi:** Tier 2 (Resmi Üniversite Portalı ve Rektörlük Yayını)
- **Geçerlilik / Güncelleme Tarihi:** 2026-2027 Eğitim-Öğretim Yılı
- **Yasal Dayanak:** 2547 Sayılı Yükseköğretim Kanunu Madde 13, 14, 15 ve YTÜ Teşkilat Şeması
"""
)

# ========================================================
# 2. 00_genel_ve_kurumsal/akademik_takvim_ve_isleyis.md (Official 2026-2027)
# ========================================================
write_file(
    "00_genel_ve_kurumsal/akademik_takvim_ve_isleyis.md",
    """---
baslik: "YTÜ Resmi Akademik Takvimi (2026-2027) ve Dönem İşleyiş Esasları"
kaynak_url: "https://ogi.yildiz.edu.tr/akademik-takvim"
arsivlenmis_belge: "arsiv/mevzuat_ve_yonergeler/ytu_2026_2027_lisans_akademik_takvimi.xlsx"
kategori: "akademik_takvim"
guvenilirlik_duzeyi: "Tier 1 (Resmi Senato Kararı ve Lisans Akademik Takvimi)"
senato_karar_no: "25.06.2026 / 06-09"
son_guncelleme_tarihi: "2026-2027"
anahtar_kelimeler: ["akademik takvim 2026-2027", "ders kayıt tarihleri", "vize haftası", "final haftası", "bütünleme", "iys sınav tarihi", "yaz okulu", "mezuniyet sınavı"]
---

# YTÜ 2026-2027 Eğitim-Öğretim Yılı Resmi Akademik Takvimi

> [!IMPORTANT] Resmi Senato Onayı
> Bu takvim, **25.06.2026 tarih ve 06-09 sayılı YTÜ Senato Kararı** ile kabul edilmiş olup lisans ve hazırlık (YDYO) eğitimine ilişkin kesinleşmiş resmi tarihlerdir.

---

## 🍂 1. Güz Yarıyılı Takvimi (2026-2027)

| Süreç / Etkinlik | Başlangıç / Tarih | Bitiş Tarihi | Açıklama ve Detaylar |
|---|---|---|---|
| **YKS İlk Kayıtlar (e-Devlet)** | 24 Ağustos 2026 | 26 Ağustos 2026 | e-Devlet Kapısı üzerinden online ilk kayıt |
| **YKS İlk Kayıtlar (Şahsen)** | 24 Ağustos 2026 | 28 Ağustos 2026 | Mazereti nedeniyle şahsen fakülteye başvuranlar |
| **İYS 1. Kısım (Use of English + Reading)** | **8 Eylül 2026 (Saat: 10:00)** | 8 Eylül 2026 | %30 ve %100 İngilizce bölümler ile beklemeli öğrenciler |
| **İYS 2. Kısım (Listening + Writing)** | **10 Eylül 2026 (Saat: 10:00)** | 10 Eylül 2026 | Dinleme ve Akademik Essay oturumu |
| **İYS Sonuçlarının İlanı** | 16 Eylül 2026 | 16 Eylül 2026 | YBD web sitesi üzerinden ilan |
| **Katkı Payı / Harç Ödeme** | 14 Eylül 2026 | 09 Ekim 2026 | Süre uzatanlar ve II. öğretim öğrencileri |
| **4. Sınıf Ders Kayıtları** | 15 Eylül 2026 | 15 Eylül 2026 | USIS/OBS üzerinden online seçim |
| **3. Sınıf Ders Kayıtları** | 16 Eylül 2026 | 16 Eylül 2026 | USIS/OBS üzerinden online seçim |
| **2. Sınıf Ders Kayıtları** | 17 Eylül 2026 | 17 Eylül 2026 | USIS/OBS üzerinden online seçim |
| **1. Sınıf Ders Kayıtları** | 18 Eylül 2026 | 18 Eylül 2026 | USIS/OBS üzerinden online seçim |
| **Bağımsız Ders Kayıtları** | 21 Eylül 2026 | 22 Eylül 2026 | Kapanan/açılan kontenjanlar için seçim |
| **GÜZ YARIYILI DERS BAŞLANGICI** | **28 Eylül 2026** | - | **Tüm lisans ve hazırlık sınıfları için ilk ders günü** |
| **Önceki Öğrenmenin Tanınması Başvuru** | 28 Eylül 2026 | 01 Ekim 2026 | Muafiyet başvuruları |
| **Güz Yarıyılı Ara Sınavları (Vizeler)** | **16 Kasım 2026** | **21 Kasım 2026** | 8. Hafta vize sınavları |
| **Güz Yarıyılı Ders Sonu** | **26 Aralık 2026** | - | 13 haftalık derslerin tamamlanması |
| **Güz Yarıyılı Final Sınavları** | **28 Aralık 2026** | **07 Ocak 2027** | Yarıyıl sonu final sınavları periyodu |
| **Güz Final Not Girişleri Son Gün** | - | 09 Ocak 2027 | Notların OBS'ye girilmesi |
| **İYS Yeterlik Sınavı (Kayıtlılar İçin)** | **12 Ocak 2027** | 12 Ocak 2027 | Güz dönemi sonunda hazırlığı bitirme sınavı |
| **Güz Yarıyılı Bütünleme Sınavları** | **11 Ocak 2027** | **16 Ocak 2027** | Bütünleme sınav haftası |
| **Güz Bütünleme Not Girişleri Son Gün**| - | 18 Ocak 2027 | Bütünleme notlarının kesinleşmesi |
| **Güz Mezuniyet Sınavı Başvuru** | 19 Ocak 2027 | 19 Ocak 2027 | Tek/çift ders mezuniyet sınavı başvurusu |
| **Güz Mezuniyet Sınavı** | **21 Ocak 2027** | 21 Ocak 2027 | Mezuniyet sınavı uygulanması |

---

## 🌸 2. Bahar Yarıyılı Takvimi (2026-2027)

| Süreç / Etkinlik | Başlangıç / Tarih | Bitiş Tarihi | Açıklama ve Detaylar |
|---|---|---|---|
| **Bahar Katkı Payı / Harç Ödeme** | 18 Ocak 2027 | 12 Şubat 2027 | Süre uzatanlar ve II. öğretim öğrencileri |
| **Bahar Ders Kayıtları (Tüm Sınıflar)** | 19 Ocak 2027 | 22 Ocak 2027 | Sınıf bazında kademeli OBS ders seçimi |
| **Bağımsız Ders Kayıtları** | 25 Ocak 2027 | 26 Ocak 2027 | Kontenjan ve çakışma düzenleme |
| **BAHAR YARIYILI DERS BAŞLANGICI** | **01 Şubat 2027** | - | **Bahar dönemi ilk ders günü** |
| **Bahar Yarıyılı Ara Sınavları (Vizeler)**| **22 Mart 2027** | **27 Mart 2027** | 8. Hafta vize sınavları |
| **Bahar Yarıyılı Ders Sonu** | **30 Nisan 2027** | - | Derslerin son günü |
| **Bahar Yarıyılı Final Sınavları** | **03 Mayıs 2027** | **13 Mayıs 2027** | Bahar dönemi finalleri |
| **Bahar Final Not Girişleri Son Gün** | - | 15 Mayıs 2027 | Final notlarının OBS'ye işlenmesi |
| **Bahar Yarıyılı Bütünleme Sınavları** | **24 Mayıs 2027** | **28 Mayıs 2027** | Bütünleme sınavları periyodu |
| **İYS Yeterlik Sınavı (Haziran/Bahar)** | **24 Mayıs 2027** | 24 Mayıs 2027 | Hazırlık okulu bitirme İYS sınavı |
| **Bahar Bütünleme Not Girişleri Son Gün**| - | 31 Mayıs 2027 | Bütünleme notlarının kesinleşmesi |
| **Bahar Mezuniyet Sınavı Başvuru** | 31 Ağustos 2027 | 31 Ağustos 2027 | Bölüm başkanlıklarına dilekçe teslimi |
| **Bahar Mezuniyet Sınavı** | **02 Eylül 2027** | 02 Eylül 2027 | Mezuniyet sınavı uygulanması |
| **2027-2028 Güz Yarıyılı Ders Başlangıcı**| **27 Eylül 2027** | - | Yeni akademik yıl başlangıcı |

---

## ☀️ 3. Yaz Okulu Esasları ve Dönem İşleyişi
- Yaz Okulu takvimi Senato tarafından Bahar yarıyılı içinde ilan edilir.
- Yaz okulu süresi en az 5 hafta ders + 1 hafta final sınavı olmak üzere toplam 6 haftadır.
- Yaz okulunda en fazla **9 kredi** ders alınabilir (YÖ-007 Yönergesi).

---
### 📌 Kaynak ve Güvenilirlik Bilgisi
- **Birincil Kaynak:** [YTÜ Öğrenci İşleri Akademik Takvim Sayfası](https://ogi.yildiz.edu.tr/akademik-takvim) ve [2026-2027 Lisans Akademik Takvimi Excel Dosyası](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/arsiv/mevzuat_ve_yonergeler/ytu_2026_2027_lisans_akademik_takvimi.xlsx)
- **Güvenilirlik Düzeyi:** Tier 1 (Resmi Senato Kararı - En Yüksek Hukuki Bağlayıcılık)
- **Geçerlilik / Güncelleme Tarihi:** 25.06.2026 (2026-2027 Eğitim-Öğretim Yılı)
- **Yasal Dayanak:** 25.06.2026 tarih ve 06-09 sayılı YTÜ Senato Kararı
"""
)

# ========================================================
# 3. 00_genel_ve_kurumsal/vikipedi_ytu_kulliyati_ve_tarihce.md
# ========================================================
write_file(
    "00_genel_ve_kurumsal/vikipedi_ytu_kulliyati_ve_tarihce.md",
    """---
baslik: "Vikipedi YTÜ Külliyatı: Tarihçe, Tarihi Yapılar, Rektörler ve Kulüpler"
kaynak_url: "https://tr.wikipedia.org/wiki/Y%C4%B1ld%C4%B1z_Teknik_%C3%9Cniversitesi"
kategori: "tarihce_ve_kulliyat"
guvenilirlik_duzeyi: "Tier 3 (Ansiklopedik ve İkincil Kaynak - Tarihsel Derleme)"
son_guncelleme_tarihi: "2026"
anahtar_kelimeler: ["vikipedi", "kondüktör mektebi", "idmma", "çukur saray", "bekir sami paşa", "otağ-ı hümayun", "rektörler kronolojisi", "öğrenci kulüpleri", "amblem"]
---

# Vikipedi YTÜ Külliyatı ve Tarihsel Gelişim

> [!NOTE] Özet
> Bu doküman, Vikipedi'nin Yıldız Teknik Üniversitesi maddesinde yer alan derin tarihsel kökleri, Osmanlı saray ve kışla binalarının mimari geçmişini, kurucu rektörler kronolojisini ve köklü öğrenci kulüpleri kültürünü derlemektedir.

---

## 1. Kronolojik Dönemler ve İsim Değişiklikleri

1. **Kondüktör Mekteb-i Âlisi (1911 - 1922):**
   - Osmanlı Devleti Nafıa Nezareti'ne (Bayındırlık Bakanlığı) bağlı vilayet idarelerinin yol, köprü ve fen memuru (kondüktör) ihtiyacını karşılamak üzere 1911'de kurulmuştur. Okul, Paris'teki *École Conducteur* modeli örnek alınarak oluşturulmuştur.
2. **Nâfıa Fen Mektebi (1922 - 1937):**
   - Cumhuriyetin ilanıyla okulun süresi ve programları genişletilerek bayındırlık fen memurları yetiştirilmeye devam edilmiştir.
3. **İstanbul Teknik Okulu (İTO) (1937 - 1969):**
   - 1937 tarihli ve 3074 sayılı Kanunla Nâfıa Fen Mektebi lağvedilerek yerine 4 yıllık mühendislik eğitimi veren İstanbul Teknik Okulu kurulmuştur. Okul, Yıldız Sarayı müştemilatı binalarına taşınmıştır.
4. **İstanbul Devlet Mühendislik ve Mimarlık Akademisi (İDMMA) (1969 - 1982):**
   - 1184 sayılı Devlet Mühendislik ve Mimarlık Akademileri Kanunu ile özerk bir akademi haline gelmiştir. Galatasaray Mühendislik Yüksekokulu ve Vatan Mühendislik Yüksekokulu akademinin bünyesine katılmıştır.
5. **Yıldız Üniversitesi (1982 - 1992):**
   - 1982 tarihli 2547 sayılı Kanun ve 2809 sayılı KHK ile İDMMA, Kocaeli Devlet Mimarlık ve Mühendislik Akademisi ile birleştirilerek Yıldız Üniversitesi adını almıştır.
6. **Yıldız Teknik Üniversitesi (1992 - Günümüz):**
   - 03.07.1992 tarih ve 3837 sayılı Kanunla üniversite yeniden yapılandırılarak **Yıldız Teknik Üniversitesi (YTÜ)** adını almış; mühendislik bölümleri fakültelere dönüştürülmüştür.

---

## 2. Tarihi Saray Binaları ve Yerleşke Mimarisi

YTÜ, Osmanlı İmparatorluğu'nun son dönem saray ve kışla yapılarını koruyan ve eğitimde kullanan nadir üniversitelerdendir:

- **Yıldız Sarayı Çukur Saray (Hanedan Yapısı):** Beşiktaş Yıldız Kampüsü'nde yer alır. Sultan II. Abdülhamid döneminde inşa edilmiş olup günümüzde Mimarlık Fakültesi tarafından kullanılmaktadır.
- **Bekir Sami Paşa Köşkü:** Rektörlük idari merkezinin yer aldığı tarihi köşk binası.
- **Agavat Binası (Ağalar Dairesi):** Yıldız Kampüsü avlusunda yer alan tarihi taş yapı.
- **Davutpaşa Kışlası (Kışla-i Hümayun):** Fatih Sultan Mehmed döneminden beri ordugah olan ve II. Mahmud döneminde (1826-1827) modern taş kışla olarak yeniden inşa edilen devasa tarihi yapı. Günümüzde Fen-Edebiyat ve İktisadi ve İdari Bilimler fakültelerine ev sahipliği yapar.
- **Otağ-ı Hümayun:** Padişahların sefere çıkarken konakladığı Davutpaşa yerleşkesindeki tarihi köşk; günümüzde rektörlük etkinlik ve protokol binasıdır.

---

## 3. YTÜ Rektörleri Kronolojisi (Akademi ve Üniversite Dönemi)

| Dönem | Rektör / Başkan | Unvan / Notlar |
|---|---|---|
| **1969 - 1976** | Prof. Dr. Süha Toner | İDMMA İlk Başkanı |
| **1976 - 1982** | Prof. Dr. İsmet Aka | İDMMA Başkanı |
| **1982 - 1992** | Prof. Dr. Suha Atük | Yıldız Üniversitesi Kurucu Rektörü |
| **1992 - 1996** | Prof. Dr. Turgut Uzel | YTÜ Dönemi İlk Rektörü |
| **1996 - 2004** | Prof. Dr. Ayhan Alkış | 2 Dönem Rektör |
| **2004 - 2008** | Prof. Dr. Durul Ören | Rektör |
| **2008 - 2016** | Prof. Dr. İsmail Yüksek | 2 Dönem Rektör |
| **2016 - 2020** | Prof. Dr. Bahri Şahin | Rektör |
| **2020 - 2024** | Prof. Dr. Tamer Yılmaz | Rektör |
| **2024 - Günümüz** | **Prof. Dr. Eyüp Debik** | Görevdeki Rektör |

---

## 4. Üniversite Amblemi ve Anlamı

YTÜ'nün amblemi, gökyüzünü, bilimi ve yükselişi simgeleyen **kutup yıldızı** motifinden ve üniversitenin köklü teknik geçmişini simgeleyen geometrik çizgilerden oluşur. Amblemdeki çizgiler aynı zamanda Kondüktör Mektebi'nin harita ve cetvel hassasiyetine atıfta bulunur.

---

## 5. Öğrenci Kulüpleri ve Kültürel Yaşam

YTÜ bünyesinde Sağlık Kültür ve Spor Daire Başkanlığı'na bağlı 80'den fazla aktif öğrenci kulübü bulunur. En köklü kulüpler:
- **IEEE YTÜ Öğrenci Kolu:** Türkiye'nin en aktif öğrenci kollarından biri olup RLC Günleri, İdeaKent vb. etkinlikleri düzenler.
- **Yıldız Robotik ve Otomasyon Kulübü (ROK):** Ulusal ve uluslararası yarışmalarda Yıldız Savaşları robot yarışmasını organize eder.
- **Havacılık Kulübü:** Model uydu ve İHA takımları (Teknofest birincilikleri).
- **Yıldız Dağcılık ve Doğa Sporları Kulübü (YÜDAK):** Türkiye'nin en köklü üniversite dağcılık kulüplerinden biridir.

---
### 📌 Kaynak ve Güvenilirlik Bilgisi
- **Birincil Kaynak:** [Vikipedi - Yıldız Teknik Üniversitesi Maddesi](https://tr.wikipedia.org/wiki/Y%C4%B1ld%C4%B1z_Teknik_%C3%9Cniversitesi) ve YTÜ Stratejik Planları
- **Güvenilirlik Düzeyi:** Tier 3 (Ansiklopedik ve İkincil Kaynak - Tarihsel Derleme)
- **Geçerlilik / Güncelleme Tarihi:** 2026
- **Not:** Hukuki ve mevzuat sorularında bu dosya yerine Tier 1 Senato belgeleri esas alınmalıdır.
"""
)

# ========================================================
# 4. 04_bologna_ve_not_sistemi/yks_taban_puanlari_ve_basari_siralamalari.md
# ========================================================
write_file(
    "04_bologna_ve_not_sistemi/yks_taban_puanlari_ve_basari_siralamalari.md",
    """---
baslik: "YTÜ Lisans Programları YKS Taban Puanları, Başarı Sıralamaları ve Kontenjanları"
kaynak_url: "https://www.kariyer.net/universite-taban-puanlari/yildiz-teknik-universitesi"
kategori: "taban_puanlar_ve_kontenjan"
guvenilirlik_duzeyi: "Tier 3 (Üçüncü Taraf İstatistik / Kariyer Portalı - ÖSYM/YÖK Kaynaklı)"
son_guncelleme_tarihi: "2026 Sınav Verileri / 2025-2026 Yerleştirme"
anahtar_kelimeler: ["taban puanları", "başarı sıralaması", "kontenjan", "ehm taban puan", "bilgisayar mühendisliği sıralama", "say", "ea", "yks 2026"]
---

# YTÜ Lisans Programları YKS Taban Puanları ve Başarı Sıralamaları

> [!NOTE] Özet
> Aşağıdaki veriler Kariyer.net ve ÖSYM/YÖK Atlas yerleştirme sonuçlarına dayanan, Yıldız Teknik Üniversitesi lisans programlarının güncel kontenjanları, taban puanları ve başarı sıralamalarıdır.

---

## 1. Mühendislik ve Fen Lisans Programları (SAY Puan Türü)

| Bölüm / Program Adı | Öğretim Dili | Puan Türü | 2026 Kontenjan | 2026 Taban Puan | 2026 Başarı Sıralaması | 2025 Başarı Sıralaması |
|---|---|---|---|---|---|---|
| **Matematik Mühendisliği (İngilizce)** | %100 İngilizce | SAY | 75 | 508,78 | **13.670** | 10.143 |
| **Bilgisayar Mühendisliği** | %30 İngilizce | SAY | 100 | 506,82 | **14.954** | 7.395 |
| **Endüstri Mühendisliği (İngilizce)** | %100 İngilizce | SAY | 55 | 506,73 | **15.016** | 10.264 |
| **Yapay Zeka ve Veri Mühendisliği** | %100 İngilizce | SAY | 35 | 506,59 | **15.129** | 8.423 |
| **Elektronik ve Haberleşme Mühendisliği**| %30 İngilizce | SAY | 100 | 505,42 | **15.911** | 12.260 |
| **Matematik Mühendisliği** | %30 İngilizce | SAY | 70 | 505,37 | **15.944** | 12.171 |
| **Endüstri Mühendisliği** | %30 İngilizce | SAY | 60 | 503,26 | **17.327** | 13.503 |
| **Kontrol ve Otomasyon Müh. (İng.)** | %100 İngilizce | SAY | 55 | 501,39 | **18.650** | 14.037 |
| **Kontrol ve Otomasyon Mühendisliği** | %30 İngilizce | SAY | 60 | 499,02 | **20.390** | 15.313 |
| **Makine Mühendisliği** | %30 İngilizce | SAY | 125 | 498,06 | **21.066** | 17.686 |
| **Mekatronik Mühendisliği (İngilizce)** | %100 İngilizce | SAY | 55 | 495,57 | **23.006** | 18.650 |
| **Elektrik Mühendisliği** | %30 İngilizce | SAY | 100 | 492,87 | **25.095** | 24.412 |
| **Kimya Mühendisliği (İngilizce)** | %100 İngilizce | SAY | 50 | 492,31 | **25.560** | 23.852 |
| **Mekatronik Mühendisliği** | %30 İngilizce | SAY | 65 | 491,26 | **26.401** | 21.993 |
| **Kimya Mühendisliği** | %30 İngilizce | SAY | 50 | 486,76 | **30.169** | 30.176 |
| **Gemi İnşaatı ve Gemi Mak. Müh.** | %30 İngilizce | SAY | 85 | 485,63 | **31.107** | 28.588 |
| **Metalurji ve Malzeme Müh. (İng.)** | %100 İngilizce | SAY | 55 | 484,77 | **31.809** | 30.427 |
| **Metalurji ve Malzeme Mühendisliği** | %30 İngilizce | SAY | 60 | 482,31 | **33.897** | 34.796 |
| **İstatistik** | %30 İngilizce | SAY | 40 | 478,72 | **37.105** | 41.938 |
| **Gemi Makineleri İşletme Müh.** | %30 İngilizce | SAY | 75 | 470,87 | **44.144** | 48.502 |

---

## 2. Elektronik ve Haberleşme Mühendisliği (EHM) Özel Analizi
- **Puan Türü:** SAY (Sayısal)
- **Kontenjan:** 100 kişi
- **2026 Taban Puanı:** ~505,42
- **2026 Başarı Sıralaması:** ~15.911 (Türkiye geneli ilk 16 bin)
- **Yerleşim:** Elektrik-Elektronik Fakültesi, Davutpaşa Kampüsü
- **Zorunlu Hazırlık:** %30 İngilizce program olduğu için kayıt sonrası İYS veya muafiyet sınavına girmek zorunludur.

---
### 📌 Kaynak ve Güvenilirlik Bilgisi
- **Birincil Kaynak:** [Kariyer.net YTÜ Taban Puanları Sayfası](https://www.kariyer.net/universite-taban-puanlari/yildiz-teknik-universitesi) ve ÖSYM YKS Yerleştirme Sonuçları Kılavuzu
- **Güvenilirlik Düzeyi:** Tier 3 (Üçüncü Taraf İstatistik / Kariyer Portalı - ÖSYM Kaynaklı İkincil Veri)
- **Geçerlilik / Güncelleme Tarihi:** 2026 YKS Sınavı / 2025-2026 Yerleştirme Verileri
- **Not:** Kesin kayıt ve kontenjan bilgileri için her yıl ÖSYM tarafından yayınlanan YKS Yükseköğretim Programları ve Kontenjanları Kılavuzu esas alınmalıdır.
"""
)

# ========================================================
# 5. AGENT_INSTRUCTIONS.md (Strict Citation & Response Format)
# ========================================================
write_file(
    "AGENT_INSTRUCTIONS.md",
    """# YTÜ Bilgi Bankası Agent Talimatları ve Standart Cevap Formatı

> [!IMPORTANT] ZORUNLU KURAL (TÜM AGENTLAR VE MODELLER İÇİN)
> Hangi yapay zeka modeli (Gemini, GPT, Claude, Cursor, Llama vb.) veya hangi agent cevap veriyor olursa olsun, **istisnasız her soru-cevabın sonunda** aşağıdaki standart blok formatında cevabın kaynağı, güvenilirlik derecesi ve güncellik tarihi belirtilecektir.

---

## 1. Standart Cevap Sonu Doğrulama Formatı (Template)

Her yanıtın en altına şu blok kopyalanıp doldurulmalıdır:

```markdown
---
### 📌 Kaynak ve Güvenilirlik Bilgisi
- **Birincil Kaynak:** [Belge veya Sayfa Adı](dosya_yolu_veya_link)
- **Güvenilirlik Düzeyi:** [Tier 1 / Tier 2 / Tier 3] (Açıklama)
- **Geçerlilik / Güncelleme Tarihi:** [Yıl / Eğitim-Öğretim Dönemi, örn: 2026-2027]
- **Yasal Dayanak / Belge No:** [Örn: YTÜ Lisans Eğitim-Öğretim Yönetmeliği Madde 23 / YÖ-075 / 25.06.2026 Senato Kararı]
```

---

## 2. Güvenilirlik Seviyeleri (Reliability Tiers)

Agentlar yanıt verirken bilgiyi aldıkları kaynağa göre aşağıdaki 3 seviyeden birini belirtmek zorundadır:

- **Tier 1 (En Yüksek Hukuki Güvenilirlik):**
  - Resmi Gazete yönetmelikleri (Örn: Lisans Yönetmeliği No: 15812)
  - 2547 Sayılı Yükseköğretim Kanunu (Örn: Madde 54 Disiplin, Madde 44 Azami Süre)
  - YTÜ Senatosu Kararları ve Resmi Yönergeler (YÖ Serisi, DD Serisi, Senato Onaylı Akademik Takvim)
- **Tier 2 (Resmi İdari ve Akademik Portal):**
  - `yildiz.edu.tr`, `ogi.yildiz.edu.tr`, `ybd.yildiz.edu.tr`, `ehm.yildiz.edu.tr` resmi birim sayfaları
  - Resmi Bologna Bilgi Sistemi ders içerikleri
  - Rektörlük Resmi Öğrenci Rehberi (`ytu_ogrenci_rehberi.pdf`)
- **Tier 3 (İkincil / İstatistiki / Ansiklopedik Kaynak):**
  - Kariyer.net taban puanları ve başarı sıralamaları tablosu
  - Vikipedi YTÜ maddesi (Tarihsel anlatım, mimari köşkler, rektör kronolojisi)
  - *Not:* Tier 3 kaynaklar genel bilgi ve istatistiki rehberlik sağlar; mevzuat uyuşmazlığında Tier 1 ve Tier 2 daima önceliklidir.

---

## 3. Bilgi Arama ve Cevaplama Akış Protokolü

1. **Önce Yönlendiriciyi Oku:** Soru geldiğinde ilk olarak [ROUTER_GUIDE.md](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/ROUTER_GUIDE.md) dosyasındaki matrise bakın.
2. **Asla Uydurma / Halüsinasyon Yok:** Dosyalarda açıkça yer almayan bir kural veya tarih varsa genel tahmin yürütmeyin; "Bu husus ilgili birimin özel kurul kararına tabidir" deyin.
3. **Madde ve Kod Belirt:** Yanıtta "Mazeret raporu 3 iş gününde verilmelidir" derken yanına `(DD-007 Esasları Madde 2)` veya `(Lisans Yönetmeliği Madde 23)` yasal dayanağını ekleyin.
4. **Formatı Kapat:** Yanıtı yukarıdaki "Kaynak ve Güvenilirlik Bilgisi" kutusuyla sonlandırın.
"""
)

print("Batch new pages generated successfully!")
