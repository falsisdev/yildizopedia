import os
import urllib.request
import ssl
from bs4 import BeautifulSoup

ctx = ssl._create_unverified_context()

def get_soup(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        return BeautifulSoup(resp.read(), 'html.parser')

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {path}")

def generate_ogi():
    print("Generating 02_ogrenci_isleri_ogi...")

    # README
    write_file(
        "02_ogrenci_isleri_ogi/README.md",
        """---
baslik: "Öğrenci İşleri Daire Başkanlığı (OGİ) Rehberi"
kategori: "ogrenci_isleri"
kaynak_url: "https://ogi.yildiz.edu.tr/"
anahtar_kelimeler: ["öğrenci işleri", "ogi", "kayıt", "harç", "belge talebi", "mezuniyet", "danışman"]
---

# YTÜ Öğrenci İşleri Daire Başkanlığı (OGİ) Rehberi

> [!NOTE] Özet
> Öğrenci İşleri Daire Başkanlığı (OGİ), Yıldız Teknik Üniversitesi öğrencilerinin ilk kayıt anından mezuniyet aşamasına kadar tüm akademik sicil, ders kaydı, katkı payı/öğrenim ücreti, yatay geçiş, intibak, mazeret, transkript ve diploma işlemlerini yürüten idari birimdir.

## İletişim ve Yerleşim
- **Konum:** Davutpaşa Kampüsü, Kışla Binası A-Blok, Esenler / İstanbul
- **Web Sitesi:** https://ogi.yildiz.edu.tr/
- **E-Posta:** ogidb@yildiz.edu.tr
- **Öğrenci Bilgi Sistemi (OBS/USIS):** https://obs.yildiz.edu.tr/

## Bu Bölümün İçeriği
- [Sıkça Sorulan Sorular (73 Madde)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/02_ogrenci_isleri_ogi/sikca_sorulan_sorular.md): Kayıt, harç, dondurma, sınav, belge ve mezuniyet ile ilgili OGİ'nin resmi yanıtları.
- [Öğrenci Bilgilendirmeleri ve Duyurular](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/02_ogrenci_isleri_ogi/ogrenci_bilgilendirmeleri.md): Mezuniyet sınavları, kayıt silme usulü, belge talepleri, akreditasyon ve YÖKSİS işlemleri.
- [Kayıt Dondurma ve İzinli Ayrılma](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/02_ogrenci_isleri_ogi/kayit_dondurma_ve_izinli_ayrilma.md): Haklı ve geçerli sebepler, başvuru süreleri ve azami izin limitleri.
- [Mazeret ve Rapor Süreçleri](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/02_ogrenci_isleri_ogi/mazeret_ve_rapor_surecleri.md): Sağlık raporu teslim kuralları (3 iş günü) ve vize mazeret sınav hakları.
- [Harç ve Katkı Payı İşlemleri](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/02_ogrenci_isleri_ogi/harc_ve_katki_payi_islemleri.md): Normal süre, uzatan öğrenciler, ikinci üniversite ve ikinci öğretim ücretleri.
- [Mezuniyet ve Diploma İşlemleri](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/02_ogrenci_isleri_ogi/mezuniyet_ve_diploma_islemleri.md): İlişik kesme formu (FR-0294), geçici mezuniyet belgesi ve diploma teslimi.
"""
    )

    # Scrape 73 SSS items
    print("Scraping exact 73 SSS from OGİ...")
    soup_sss = get_soup("https://ogi.yildiz.edu.tr/birim-hakkinda/hizli-erisim/sikca-sorulan-sorular")
    accordions = soup_sss.find_all('div', class_='accordion')
    sss_content = """---
baslik: "YTÜ Öğrenci İşleri Daire Başkanlığı Sıkça Sorulan Sorular (73 Madde Tam Metin)"
kaynak_url: "https://ogi.yildiz.edu.tr/birim-hakkinda/hizli-erisim/sikca-sorulan-sorular"
kategori: "sss"
anahtar_kelimeler: ["öğrenci işleri sss", "kayıt", "e-devlet", "harç", "kayıt dondurma", "mazeret", "diploma", "çap", "yatay geçiş"]
---

# OGİ Sıkça Sorulan Sorular (Tam ve Güncel Liste)

> [!NOTE] Özet
> Aşağıdaki 73 soru ve yanıt, YTÜ Öğrenci İşleri Daire Başkanlığı'nın resmi web sitesindeki tüm kategorileri (İlk Kayıt, Öğrenci Numarası, Harçlar, Kayıt Dondurma, Mazeret, ÇAP/Yandal, Mezuniyet) eksiksiz olarak içermektedir.

"""
    for i, acc in enumerate(accordions):
        q = acc.find('div', class_=lambda c: c and 'question' in c)
        a = acc.find('div', class_=lambda c: c and 'answer' in c)
        q_txt = q.get_text(' ', strip=True) if q else f"Soru {i+1}"
        a_txt = a.get_text('\n\n', strip=True) if a else "Bilgi bulunamadı."
        sss_content += f"### Soru {i+1}: {q_txt}\n\n**Cevap:**\n{a_txt}\n\n---\n\n"

    write_file("02_ogrenci_isleri_ogi/sikca_sorulan_sorular.md", sss_content)

    # Öğrenci Bilgilendirmeleri
    write_file(
        "02_ogrenci_isleri_ogi/ogrenci_bilgilendirmeleri.md",
        """---
baslik: "YTÜ Öğrenci İşleri Resmi Bilgilendirmeleri ve Usulleri"
kaynak_url: "https://ogi.yildiz.edu.tr/birim-hakkinda/hizli-erisim/bilgilendirmeler"
kategori: "bilgilendirmeler"
anahtar_kelimeler: ["mezuniyet sınavı", "kayıt silme", "ilişik kesme", "belge talebi", "akreditasyon", "yöksis aktif pasif"]
---

# YTÜ Öğrenci İşleri Resmi Bilgilendirmeleri

## 1. Güz ve Bahar Mezuniyet Sınavları Esasları (DD-015)
- **Kabul Tarihi:** 07.02.2013 tarih ve 2013/03-26 sayılı Senato Kararı.
- **Kimler Girebilir:**
  - Mezuniyet aşamasına gelmiş, öğretim planındaki tüm dersleri almış ve devam şartını yerine getirmiş olmak kaydıyla,
  - Başarısız en fazla **iki (2) dersi** (FF veya FD) kalan öğrenciler,
  - Veya tüm dersleri başarmış ancak AGNO'su 2.00'ın altında kaldığı için mezun olamayan öğrenciler (koşullu başarılı DD/DC derslerinden en fazla iki ders seçerek not yükseltmek amacıyla).
- **Şartlar:** Mezuniyet sınavına girilecek dersin yarıyıl sonu sınavına girebilme şartlarının (devam ve varsa laboratuvar/ödev şartları) önceden yerine getirilmiş olması zorunludur.
- **Sınav Hakkı:** Mezuniyet sınavlarına giremeyen öğrencilere mazeret sınavı açılmaz. Sınavda alınan not doğrudan harf notuna dönüştürülür.

## 2. Kendi İsteği ile Kayıt Sildirme İşlemleri
- **Gerekli Formlar:**
  - `FR-0364` - Öğrenci İşleri Daire Başkanlığı Dilekçe Formu
  - `FR-0294` - Kaydı Silinen / Mezun Olan Öğrenciler İçin İlişik Kesme Belgesi
- **Eklenecek Belgeler:**
  - Kimlik fotokopisi (Yabancı uyruklular için pasaport fotokopisi)
  - Öğrenci kimlik kartının aslı (Kayıp ise yerel/ulusal gazete kayıp ilanı)
- **Başvuru Yeri:** İlgili Fakülte/Enstitü Öğrenci İşleri Bürosu veya OGİ Merkezi. Kütüphane, Sağlık-Kültür-Spor ve laboratuvarlardan borcu yoktur onayı alınarak ilişik kesilir.

## 3. Belge Talepleri (Mezuniyet Yazısı, Transkript, Onay)
- **Mezuniyet Yazısı:** Diplomaların basım aşamasında öğrencilere en fazla 2 ay geçerli olmak üzere verilen resmi geçici belgedir. Diploma aslı teslim edilirken bu belgenin iadesi zorunludur.
- **Transkript (Not Döküm Belgesi):** e-Devlet kapısı üzerinden barkodlu olarak anında üretilebilir veya OBS üzerinden ıslak imzalı/mühürlü talep edilebilir.
- **Aslı Gibidir Onayı:** Üniversitemiz tarafından düzenlenmiş diploma ve belgelerin noter onayı yerine üniversitece yapılan resmi onay işlemidir.

## 4. YÖKSİS Üzerinde Aktif / Pasif Öğrenci Statüsü
- Yarıyıl başında harç yatırıp ders kaydı yapan ve kaydı danışmanınca onaylanan öğrenci YÖKSİS'te **AKTİF** görünür.
- Ders kaydı yapmayan, kayıt donduran veya azami süresini tamamlayan öğrenciler **PASİF** görünür. Pasif öğrenciler öğrencilik haklarından (öğrenci indirim kartı, askerlik tecili vb.) yararlanamaz.
"""
    )

    # Kayıt Dondurma
    write_file(
        "02_ogrenci_isleri_ogi/kayit_dondurma_ve_izinli_ayrilma.md",
        """---
baslik: "YTÜ Kayıt Dondurma ve İzinli Ayrılma Esasları"
kategori: "kayit_islemleri"
anahtar_kelimeler: ["kayıt dondurma", "izinli ayrılma", "askerlik", "sağlık kurulu raporu", "maddi imkansızlık"]
---

# YTÜ Kayıt Dondurma ve İzinli Ayrılma İşlemleri

> [!NOTE] Özet
> Öğrenciler haklı ve geçerli nedenlerin varlığı halinde ilgili Yönetim Kurulu kararıyla en fazla 2 yarıyıl (zorunlu hallerde 4 yarıyıl) süreyle kayıt dondurabilirler. Bu süreler 7 yıllık azami öğrenim süresinden sayılmaz.

## Haklı ve Geçerli Nedenler
1. **Sağlık Mazereti:** Heyet (Sağlık Kurulu) raporu ile belgelenen uzun süreli hastalık veya tedavi gereksinimi.
2. **Askerlik:** Askerlik tecilinin iptal olması ve askere sevk belgesi sunulması (Askerlik süresince izinli sayılır).
3. **Maddi ve Ailevi Nedenler:** Öğrencinin öğrenimine devam etmesini engelleyen ağır ailevi veya maddi durumların resmi belgelerle kanıtlanması.
4. **Yurtdışı Eğitim / Dil Eğitimi:** Üniversite veya uluslararası programlar kapsamında yurtdışında eğitim alacağını belgeleyenler.
5. **Tutukluluk Durumu:** Öğrencinin tutuklu bulunması (hüküm giymemiş olması kaydıyla).

## Başvuru Süresi ve Prosedürü
- Başvurular, yarıyılın başlangıcından itibaren en geç **4. haftanın sonuna kadar** ilgili Bölüm Başkanlığına / Fakülte Dekanlığına dilekçe ve gerekçeli resmi belgelerle yapılır.
- Ani gelişen kaza veya ameliyat gibi acil sağlık durumlarında bu süre şartı aranmaz.
- İlgili Fakülte Yönetim Kurulu kararı ile kayıt dondurma kesinleşir ve Öğrenci İşleri Daire Başkanlığı'na bildirilir.
- Kayıt dondurulan süre boyunca katkı payı / harç ödenmez (ödenmişse iade edilmez, saklı tutulur) ve derslere/sınavlara girilemez.
"""
    )

    # Mazeret ve Rapor Süreçleri
    write_file(
        "02_ogrenci_isleri_ogi/mazeret_ve_rapor_surecleri.md",
        """---
baslik: "YTÜ Mazeret ve Sağlık Raporu Süreçleri Rehberi"
kategori: "mazeret"
anahtar_kelimeler: ["mazeret sınavı", "sağlık raporu", "3 gün", "vize mazereti", "mediko", "bölüm başkanlığı"]
---

# YTÜ Mazeret ve Sağlık Raporu Süreçleri

> [!NOTE] Özet
> Ara sınavlara (vize) giremeyen öğrenciler, sağlık raporu veya yasal mazeret belgelerini mazeretin bitiminden itibaren en geç **3 iş günü içinde** Bölüm Başkanlığına teslim ederek mazeret sınavına girebilirler.

## Kritik Kurallar
1. **Teslim Süresi:** Sağlık raporu, rapor süresinin bitim tarihinden itibaren en geç **3 (üç) iş günü** içerisinde bir dilekçe ekinde ilgili bölüm sekreterliğine teslim edilmelidir. Geç teslim edilen raporlar işleme alınmaz.
2. **Hangi Sınavlar İçin Geçerlidir:** Mazeret sadece **yarıyıl içi ara sınavları (vize)** için geçerlidir. Final (yarıyıl sonu) sınavları için mazeret sınavı açılmaz (final mazereti bütünleme sınavıdır).
3. **Raporlu İken Sınava Girilmez:** Raporlu olduğu tarihte sınava giren öğrencinin sınavı **GEÇERSİZ** sayılır ve o sınav için daha sonra mazeret sınav hakkı talep edilemez.
4. **Mazeret Sınavının Mazereti Olmaz:** Mazeret sınavına herhangi bir sebeple giremeyen öğrenci için ikinci bir mazeret sınavı açılmaz.
5. **Mazeret Sınavı Kapsamı:** Mazeret sınavında öğrenci dersin o tarihe kadar işlenmiş tüm müfredatından sorumludur.
"""
    )

    # Harç ve Katkı Payı
    write_file(
        "02_ogrenci_isleri_ogi/harc_ve_katki_payi_islemleri.md",
        """---
baslik: "YTÜ Katkı Payı ve Öğrenim Ücreti (Harç) Esasları"
kategori: "mali_islemler"
anahtar_kelimeler: ["harç", "katkı payı", "ikinci öğretim", "uzatma", "ikinci üniversite", "halkbank"]
---

# YTÜ Katkı Payı ve Öğrenim Ücreti (Harç) Esasları

> [!NOTE] Özet
> Birinci öğretim lisans öğrencileri normal öğrenim süresi (4 yıl / 8 yarıyıl) boyunca harç ödemezler (Devlet karşılar). Ancak süresini uzatanlar, ikinci bir üniversitede kaydı bulunanlar ve tüm ikinci öğretim öğrencileri harç ödemekle yükümlüdür.

## Harç Ödemekle Yükümlü Olanlar
1. **Normal Süresini Aşanlar:** 4 yıllık lisans programında 8 yarıyılı tamamlayıp 9. yarıyıl ve sonrasına kalan birinci öğretim öğrencileri.
2. **Çift Üniversite Kaydı:** Başka bir yükseköğretim kurumunda (açıköğretim dahil) aktif kaydı bulunan birinci öğretim öğrencileri.
3. **İkinci Öğretim Öğrencileri:** Her yarıyıl başında belirlenen öğrenim ücretini ödemek zorundadır. (İlk %10'a girenler bir sonraki yarıyıl birinci öğretim katkı payı öder / indirim alır).
4. **Yabancı Uyruklu Öğrenciler:** Cumhurbaşkanlığı kararı ve Senato tarafından belirlenen uluslararası öğrenci harcını öderler.

## Ödeme Kanalları ve Ders Kaydı İlişkisi
- Harç ödemeleri her yarıyıl başında ilan edilen tarihlerde anlaşmalı banka (Halkbank) şubelerinden, ATM'lerinden veya internet bankacılığından **Öğrenci Numarası** ile yapılır.
- Harç borcu bulunan öğrenciler OBS üzerinden ders seçimi yapamaz veya seçtikleri dersler danışman onayına gönderilemez.
"""
    )

    # Mezuniyet ve Diploma
    write_file(
        "02_ogrenci_isleri_ogi/mezuniyet_ve_diploma_islemleri.md",
        """---
baslik: "YTÜ Mezuniyet Şartları, İlişik Kesme ve Diploma Teslim Rehberi"
kategori: "mezuniyet"
anahtar_kelimeler: ["mezuniyet", "240 akts", "agno 2.00", "ilişik kesme", "diploma eki", "onur belgesi"]
---

# YTÜ Mezuniyet Şartları ve Diploma İşlemleri

> [!NOTE] Özet
> Bir lisans öğrencisinin mezun olabilmesi için öğretim planındaki en az **240 AKTS** kredisini tamamlamış, tüm zorunlu ve seçmeli dersleri başarmış, stajlarını onaylatmış ve genel not ortalamasını (AGNO) en az **2.00 / 4.00** yapmış olması şarttır.

## Mezuniyet Koşulları
1. **Kredi ve AKTS:** Program öğretim planında yer alan 8 yarıyıllık tüm derslerin eksiksiz alınması ve toplamda en az 240 AKTS kredisinin sağlanması.
2. **Başarı Durumu:** Başarısız dersi (FF, F0, FG) bulunmaması (DC ve DD notları AGNO >= 2.00 olduğu takdirde başarılı kabul edilir).
3. **Zorunlu Stajlar:** EHM için 30 gün Genel Staj ve 30 gün Mesleki Staj olmak üzere toplam 60 iş günü stajın Bölüm Staj Komisyonu tarafından kabul edilmiş olması.
4. **Bitirme Projesi:** EHM9000 Bitirme Çalışması dersinin jüri önünde başarıyla savunulmuş olması.

## Dereceler ve Onur Belgeleri
- **Mezuniyet:** AGNO 2.00 - 2.99
- **Onur Öğrencisi:** Disiplin cezası almamış olmak kaydıyla AGNO 3.00 - 3.49
- **Yüksek Onur Öğrencisi:** Disiplin cezası almamış olmak kaydıyla AGNO 3.50 - 4.00

## İlişik Kesme ve Diploma Teslimi
- Mezuniyet kararı Fakülte Yönetim Kurulu tarafından alındıktan sonra öğrenci OBS üzerinde mezun durumuna geçer.
- Öğrenci `FR-0294` İlişik Kesme Formunu doldurarak Kütüphane ve ilgili birimlerden imza alır.
- Öğrenci kimlik kartı ve varsa Geçici Mezuniyet Belgesi iade edilerek diploma, diploma eki ve lise diploması aslı şahsen veya noter onaylı vekaletname ile teslim alınır.
"""
    )
    print("02_ogrenci_isleri_ogi completed successfully!")

if __name__ == '__main__':
    generate_ogi()
