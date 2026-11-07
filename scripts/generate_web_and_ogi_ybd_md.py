import os
import json
import re

with open('scripts/scraped_web_pages.json', 'r', encoding='utf-8') as f:
    scraped = json.load(f)

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")
    print(f"Written: {path}")

# ==========================================
# 00_GENEL_VE_KURUMSAL
# ==========================================

write_file(
    "00_genel_ve_kurumsal/README.md",
    """---
baslik: "YTÜ Genel ve Kurumsal Yapı Rehberi"
kategori: "genel_ve_kurumsal"
anahtar_kelimeler: ["yıldız teknik üniversitesi", "tarihçe", "kampüsler", "akademik takvim", "rektörlük"]
---

# Yıldız Teknik Üniversitesi Genel ve Kurumsal Bilgiler

Yıldız Teknik Üniversitesi (YTÜ), 1911 yılında kurulan "Kondüktör Mekteb-i Âlisi"ne dayanan köklü geçmişiyle Türkiye'nin en köklü teknik ve araştırma üniversitelerinden biridir.

## Bu Bölümün İçeriği
- [YTÜ Tarihçe ve Genel Bilgiler](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/00_genel_ve_kurumsal/ytu_tarihce_ve_genel_bilgiler.md): Üniversitenin kuruluşu, misyonu, vizyonu, fakülteleri ve akademik profili.
- [Kampüsler ve Yerleşkeler](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/00_genel_ve_kurumsal/kampusler_ve_yerleskeler.md): Davutpaşa, Yıldız ve Maslak yerleşkeleri, ulaşım ve yurt olanakları.
- [Akademik Takvim ve İşleyiş](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/00_genel_ve_kurumsal/akademik_takvim_ve_isleyis.md): Güz, Bahar ve Yaz Okulu dönemleri, kayıt, ekle-sil, sınav ve mazeret süreçleri takvimi.
"""
)

write_file(
    "00_genel_ve_kurumsal/ytu_tarihce_ve_genel_bilgiler.md",
    f"""---
baslik: "YTÜ Tarihçe, Vizyon, Misyon ve Genel Bilgiler"
kaynak_url: "https://yildiz.edu.tr/"
kategori: "genel_bilgiler"
anahtar_kelimeler: ["tarihçe", "kondüktör mektebi", "yıldız teknik", "vizyon", "misyon", "araştırma üniversitesi"]
---

# Yıldız Teknik Üniversitesi Tarihçe ve Genel Bilgiler

> [!NOTE] Özet
> Yıldız Teknik Üniversitesi, 1911 yılından bugüne mühendislik, mimarlık, fen, sosyal bilimler ve sanat alanlarında lider teknik eğitim veren, YÖK tarafından belirlenmiş "Araştırma Üniversitesi" statüsünde bir devlet üniversitesidir.

## Tarihçe ve Kuruluş
- **1911:** Vilayet nafıa idarelerinin fen memuru ihtiyacını karşılamak amacıyla *Kondüktör Mekteb-i Âlisi* kuruldu.
- **1922:** Okulun adı *Nâfıa Fen Mektebi* olarak değiştirildi.
- **1937:** TBMM tarafından kabul edilen kanunla *İstanbul Teknik Okulu* adını aldı ve 4 yıllık mühendislik eğitimi vermeye başladı.
- **1969:** 1184 sayılı Kanunla *İstanbul Devlet Mühendislik ve Mimarlık Akademisi (İDMMA)* haline geldi.
- **1982:** 2809 sayılı Kanunla *Yıldız Üniversitesi* adını aldı.
- **1992:** 3837 sayılı Kanunla bugünkü adı olan **Yıldız Teknik Üniversitesi** unvanını aldı.

## Misyon ve Vizyon
- **Misyon:** Evrensel standartlarda eğitim-öğretim vererek, araştırma, teknoloji üretimi ve toplumsal katkı alanlarında öncü bireyler yetiştirmek; bilim ve teknolojiyi insanlık yararına dönüştürmek.
- **Vizyon:** Bilim ve teknoloji üretiminde uluslararası alanda tanınan, öncü ve yenilikçi bir araştırma üniversitesi olmak.

## Akademik Birimler
YTÜ bünyesinde 11 Fakülte, 2 Enstitü (Fen Bilimleri ve Sosyal Bilimler), 1 Yabancı Diller Yüksekokulu ve 1 Meslek Yüksekokulu bulunmaktadır. Elektrik-Elektronik, Makine, İnşaat, Kimya-Metalurji ve Mimarlık fakülteleri üniversitenin kurucu ve en güçlü teknik omurgasını oluşturur.
"""
)

write_file(
    "00_genel_ve_kurumsal/kampusler_ve_yerleskeler.md",
    """---
baslik: "YTÜ Kampüsleri ve Yerleşke Olanakları"
kategori: "yerleskeler"
anahtar_kelimeler: ["davutpaşa", "yıldız kampüsü", "maslak", "yurtlar", "ulaşım", "ring", "yemekhane"]
---

# YTÜ Kampüsleri ve Yerleşkeler

> [!NOTE] Özet
> YTÜ'nün ana eğitim ve yaşam yerleşkesi Esenler'deki tarihi ve modern **Davutpaşa Kampüsü**'dür. Beşiktaş'taki tarihi **Yıldız Kampüsü** ve Maslak'taki ek yerleşkesiyle eğitim vermektedir.

## 1. Davutpaşa Kampüsü (Ana Yerleşke)
- **Konum:** Esenler / İstanbul (M1A Yenikapı - Atatürk Havalimanı Metro Hattı üzerinde Davutpaşa - YTÜ İstasyonu).
- **Yer Alan Fakülteler:** 
  - Elektrik-Elektronik Fakültesi (EHM, Elektrik, Bilgisayar, Kontrol)
  - Kimya-Metalurji Fakültesi
  - Fen-Edebiyat Fakültesi
  - İktisadi ve İdari Bilimler Fakültesi
  - Eğitim Fakültesi
  - Sanat ve Tasarım Fakültesi
  - Yabancı Diller Yüksekokulu (Hazırlık Binası)
  - İnşaat Fakültesi
- **Sosyal ve Yaşam Olanakları:**
  - KYK Kız ve Erkek Öğrenci Yurtları
  - YTÜ Teknopark (Yıldız Teknopark - Türkiye'nin en büyük teknoparklarından biri)
  - Otağ-ı Hümayun ve Tarihi Kışla Binaları
  - Merkezi Kütüphane (7/24 çalışma salonları)
  - Kapalı Spor Salonu, Yüzme Havuzu, Halı Sahalar
  - Merkez Yemekhane ve Mediko-Sosyal Sağlık Merkezi

## 2. Yıldız Kampüsü (Tarihi Merkez)
- **Konum:** Beşiktaş / İstanbul (Yıldız Sarayı koruluğu ve Çırağan Caddesi yakınında).
- **Yer Alan Fakülteler:**
  - Makine Fakültesi
  - Mimarlık Fakültesi
  - Gemi İnşaatı ve Denizcilik Fakültesi
  - Rektörlük Tarihi Binası
- **Ulaşım:** Beşiktaş ve Ortaköy iskelelerine, metrobüs ve otobüs hatlarına yürüme mesafesinde.

## 3. Maslak Yerleşkesi
- Maslak plazalar bölgesinde bulunan birimler ve Meslek Yüksekokulu programları.
"""
)

write_file(
    "00_genel_ve_kurumsal/akademik_takvim_ve_isleyis.md",
    """---
baslik: "YTÜ Akademik Takvim Yapısı ve Dönem İşleyişi"
kategori: "akademik_takvim"
anahtar_kelimeler: ["güz yarıyılı", "bahar yarıyılı", "ekle sil", "vize haftası", "final haftası", "bütünleme", "yaz okulu"]
---

# YTÜ Akademik Takvim Yapısı ve Dönem İşleyişi

> [!NOTE] Özet
> YTÜ'de bir eğitim-öğretim yılı Güz ve Bahar olmak üzere en az 14'er haftalık iki yarıyıldan oluşur. Ayrıca yaz aylarında isteğe bağlı 7 haftalık (5 hafta ders + 1 hafta final) Yaz Okulu açılır.

## Yarıyıl İşleyiş Aşamaları

### 1. Dönem Başı Kayıt ve Danışman Onayı
- Öğrenciler ilan edilen tarihlerde USIS/OBS üzerinden derslerini seçer.
- Danışman onay süresi içinde akademik danışman ders seçimini onaylar veya düzeltme talep eder.
- Kayıt haftasından sonraki hafta **Ders Ekle-Sil Haftası**'dır. Bu sürede kontenjanı açılan dersler eklenebilir veya bırakılabilir.

### 2. Yarıyıl İçi Ders ve Ara Sınav Dönemi
- En az 14 hafta ders işlenir.
- 7. ve 9. haftalar arasında Yarıyıl İçi Ara Sınavları (Vizeler) yapılır.
- Mazeret sınavları yarıyıl sonu sınavlarından önce ilgili Bölüm Başkanlığı tarafından duyurulan takvimde yapılır.

### 3. Yarıyıl Sonu Sınavları (Finaller) ve Bütünlemeler
- 14 haftalık ders bitimini takip eden iki hafta boyunca Final sınavları uygulanır.
- Final sınavlarında başarısız (FF/FD) veya koşullu (DD/DC) not alan öğrenciler için **Bütünleme Sınavları** yapılır. Bütünleme notu final notu yerine geçer.

### 4. Yaz Okulu
- Senato tarafından her yıl takvimi ilan edilir. Temmuz - Ağustos aylarında 5 hafta yoğunlaştırılmış ders + 1 hafta sınav periyodu şeklinde uygulanır.
"""
)

print("00_genel_ve_kurumsal done.")
