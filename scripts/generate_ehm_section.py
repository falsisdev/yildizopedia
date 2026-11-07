import os
import json
import re

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {path}")

with open('scripts/bologna_ehm_detailed.json', 'r', encoding='utf-8') as f:
    bologna_data = json.load(f)

def generate_ehm():
    base_dir = "05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi"
    print("Generating EHM section...")

    # 1. README
    write_file(
        f"{base_dir}/README.md",
        """---
baslik: "Elektronik ve Haberleşme Mühendisliği (EHM) Bölüm Rehberi"
kategori: "bolum_rehberi"
kaynak_url: "https://ehm.yildiz.edu.tr/"
anahtar_kelimeler: ["ehm", "elektronik ve haberleşme", "mühendislik", "elektrik-elektronik fakültesi", "müdek", "bologna"]
---

# YTÜ Elektronik ve Haberleşme Mühendisliği (EHM) Bölümü

> [!NOTE] Özet
> Yıldız Teknik Üniversitesi Elektrik-Elektronik Fakültesi bünyesinde yer alan Elektronik ve Haberleşme Mühendisliği Bölümü, MÜDEK ve ABET akreditasyonuna sahip, analog/sayısal elektronik, haberleşme sistemleri, mikrodalga, antenler, sinyal işleme ve gömülü sistemler alanında Türkiye'nin lider mühendislik bölümlerinden biridir.

## İletişim ve Yerleşim
- **Konum:** Davutpaşa Kampüsü, Elektrik-Elektronik Fakültesi Binası, 34220 Esenler / İstanbul
- **Telefon:** 0212 383 58 81
- **E-Posta:** ehmblm@yildiz.edu.tr
- **Web Sitesi:** https://ehm.yildiz.edu.tr/

## Bu Bölümün İçeriği
- [Program Çıktıları (MÜDEK/ABET)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/program_ciktilari.md): PÇ-1.1 ile PÇ-11.2 arasındaki tüm öğrenme kazanımları.
- [TYYÇ Uyumu](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/tyyc_uyumu.md): Türkiye Yükseköğretim Yeterlilikler Çerçevesi 6. Düzey Lisans eşleşmesi.
- [Lisans Eğitim Yapısı](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/lisans_egitim_yapisi.md): %30 ve %100 İngilizce programlar, laboratuvarlar, yandal ve ÇAP olanakları.
- [Yönetmelik ve Esaslar](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/yonetmelik_ve_esaslar.md): Bölüme özgü yönergeler, intibak ve proje yürütme kuralları.
- [Staj ve Bitirme Esasları](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/staj_ve_bitirme_esaslari.md): 30 gün Genel Staj (EHM2002) + 30 gün Mesleki Staj (EHM3002), Tasarım Projesi (EHM4200) ve Bitirme Çalışması (EHM9000).
- [Sınav Kuralları](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/sinav_kurallari.md): Bölüm sınav salon kuralları ve itiraz prosedürü.
- [Bölüm Sıkça Sorulan Sorular](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/sikca_sorulan_sorular.md): Staj, bitirme tezi, önkoşullar, çift anadal sınav çakışması ve laboratuvar soruları.
- [Bologna Ders Planı (8 Yarıyıl)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/bologna_ders_plani/README.md): 8 yarıyılın tüm ders kartları, önkoşul zincirleri ve seçmeli ders havuzları.
"""
    )

    # 2. Program Çıktıları
    write_file(
        f"{base_dir}/program_ciktilari.md",
        """---
baslik: "EHM MÜDEK ve ABET Program Çıktıları (PÇ-1 ile PÇ-11)"
kaynak_url: "https://ehm.yildiz.edu.tr/bolum/program-ciktilari"
kategori: "program_ciktilari"
anahtar_kelimeler: ["program çıktıları", "pç", "müdek", "abet", "akreditasyon", "öğrenme çıktıları"]
---

# EHM Bölümü Program Çıktıları (PÇ)

> [!NOTE] Özet
> EHM lisans programından mezun olan her mühendisin kazanmış olması gereken bilgi, beceri ve yetkinlikleri tanımlayan MÜDEK / ABET akreditasyon ölçütleridir.

## Program Çıktıları Listesi

- **PÇ-1.1:** Matematik ve fen bilimleri gibi konularda yeterli bilgi birikimi.
- **PÇ-1.2:** İlgili mühendislik disiplinine özgü konularda yeterli bilgi birikimi.
- **PÇ-1.3:** Bu alanlardaki kuramsal ve uygulamalı bilgileri, karmaşık mühendislik problemlerinin çözümünde kullanabilme becerisi.
- **PÇ-2.1:** Karmaşık mühendislik problemlerini tanımlama, formüle etme ve çözme becerisi.
- **PÇ-2.2:** Bu amaçla uygun analiz ve modelleme yöntemlerini seçme ve uygulama becerisi.
- **PÇ-3.1:** Karmaşık bir sistemi, süreci, cihazı veya ürünü gerçekçi kısıtlar ve koşullar altında, belirli gereksinimleri karşılayacak şekilde tasarlama becerisi.
- **PÇ-3.2:** Bu amaçla modern tasarım yöntemlerini uygulama becerisi.
- **PÇ-4.1:** Mühendislik uygulamalarında karşılaşılan karmaşık problemlerin analizi ve çözümü için gerekli olan modern teknik ve araçları geliştirme, seçme ve kullanma becerisi.
- **PÇ-4.2:** Bilişim teknolojilerini etkin bir şekilde kullanma becerisi.
- **PÇ-5.1:** Karmaşık mühendislik problemlerinin veya disipline özgü araştırma konularının incelenmesi için deney tasarlama becerisi.
- **PÇ-5.2:** Karmaşık mühendislik problemlerinin veya disipline özgü araştırma konularının incelenmesi için deney yapma becerisi.
- **PÇ-5.3:** Karmaşık mühendislik problemlerinin veya disipline özgü araştırma konularının incelenmesi için veri toplama becerisi.
- **PÇ-5.4:** Karmaşık mühendislik problemlerinin veya disipline özgü araştırma konularının incelenmesi için deney sonuçlarını analiz etme ve yorumlama becerisi.
- **PÇ-6.1:** Disiplin içi bireysel çalışma becerisi.
- **PÇ-6.2:** Disiplin içi takımlarda etkin biçimde çalışabilme becerisi.
- **PÇ-6.3:** Çok disiplinli takımlarda etkin biçimde çalışabilme becerisi.
- **PÇ-7.1:** Sözlü ve yazılı etkin iletişim kurma ve sunum yapabilme becerisi.
- **PÇ-7.2:** En az bir yabancı dil bilgisi.
- **PÇ-7.3:** Etkin rapor yazma ve yazılı raporları anlama becerisi.
- **PÇ-7.4:** Tasarım ve üretim raporları hazırlayabilme becerisi.
- **PÇ-7.5:** Açık ve anlaşılır talimat verme ve alma becerisi.
- **PÇ-8.1:** Yaşam boyu öğrenmenin gerekliliği konusunda farkındalık.
- **PÇ-8.2:** Bilgiye erişebilme, bilim ve teknolojideki gelişmeleri izleme ve kendini sürekli yenileme becerisi.
- **PÇ-9.1:** Etik ilkelerine uygun davranma, mesleki ve etik sorumluluk hakkında bilgi.
- **PÇ-9.2:** Mühendislik uygulamalarında kullanılan standartlar hakkında bilgi.
- **PÇ-10.1:** Proje yönetimi, risk yönetimi ve değişiklik yönetimi gibi, iş hayatındaki uygulamalar hakkında bilgi.
- **PÇ-10.2:** Girişimcilik, yenilikçilik hakkında farkındalık.
- **PÇ-10.3:** Sürdürülebilir kalkınma hakkında bilgi.
- **PÇ-11.1:** Mühendislik uygulamalarının evrensel ve toplumsal boyutlarda sağlık, çevre ve güvenlik üzerindeki etkileri ve çağın mühendislik alanına yansıyan sorunları hakkında bilgi.
- **PÇ-11.2:** Mühendislik çözümlerinin hukuksal sonuçları konusunda farkındalık.
"""
    )

    # 3. TYYÇ Uyumu
    write_file(
        f"{base_dir}/tyyc_uyumu.md",
        """---
baslik: "EHM Türkiye Yükseköğretim Yeterlilikler Çerçevesi (TYYÇ) Uyumu"
kaynak_url: "https://ehm.yildiz.edu.tr/bolum/turkiye-yuksek-ogretim-yeterlilikler-cercevesi"
kategori: "tyyc"
anahtar_kelimeler: ["tyyç", "seviye 6", "lisans yeterlilikleri", "bilgi", "beceri", "yetkinlik"]
---

# EHM Bölümü TYYÇ (Lisans Düzeyi 6) Uyumu

> [!NOTE] Özet
> EHM Lisans Programı, Avrupa Yükseköğretim Alanı Yeterlilikler Çerçevesi (QF-EHEA) 1. Düzey ve TYYÇ 6. Düzey (Lisans Eğitimi) Yeterlilikleri ile tam uyumlu olarak tasarlanmıştır.

## TYYÇ Temel Alan Yeterlilikleri Eşleşmesi

### 1. Bilgi (Kuramsal ve Olgusal)
- Matematik, fen bilimleri ve elektronik/haberleşme mühendisliği alanına özgü kuramsal ve uygulamalı bilgilere ileri düzeyde sahip olma.
- Alanındaki güncel gelişmeleri, standartları ve ileri teknolojileri kavrama.

### 2. Beceri (Bilişsel ve Uygulamalı)
- Elektronik devreler, mikrodalga, haberleşme sistemleri ve gömülü donanımlar tasarlayabilme, simüle edebilme ve laboratuvar ortamında test edebilme.
- Karmaşık mühendislik problemlerinin çözümü için uygun modern mühendislik yazılımlarını (MATLAB, SPICE, Altium, ADS, Vivado vb.) etkin kullanabilme.

### 3. Yetkinlikler
- **Bağımsız Çalışabilme ve Sorumluluk Alabilme:** Tasarım projesi ve bitirme tezinde bağımsız proje yürütebilme veya çok disiplinli takımlarda liderlik/sorumluluk üstlenebilme.
- **Öğrenme Yetkinliği:** Mesleki kariyeri boyunca yaşam boyu öğrenmeyi sürdürebilme, yeni teknolojilere hızla adapte olabilme.
- **İletişim ve Sosyal Yetkinlik:** Mühendislik çözümlerini teknik raporlar ve sözlü sunumlarla ulusal ve uluslararası platformlarda ifade edebilme.
- **Alana Özgü Yetkinlik:** Mühendislik uygulamalarında meslek etiği, iş sağlığı ve güvenliği, patent/fikri mülkiyet ve çevresel sürdürülebilirlik ilkelerine uygun davranma.
"""
    )

    # 4. Lisans Eğitim Yapısı
    write_file(
        f"{base_dir}/lisans_egitim_yapisi.md",
        """---
baslik: "EHM Lisans Eğitim Yapısı (%30 ve %100 İngilizce)"
kaynak_url: "https://ehm.yildiz.edu.tr/egitim/lisans"
kategori: "lisans_egitimi"
anahtar_kelimeler: ["%30 ingilizce", "%100 ingilizce", "laboratuvarlar", "yandal", "çap", "bologna"]
---

# EHM Lisans Eğitim Yapısı

> [!NOTE] Özet
> Elektronik ve Haberleşme Mühendisliği Bölümü'nde lisans eğitimi iki ayrı akışta yürütülür: %30 İngilizce Program ve %100 İngilizce Program. Her iki program da 8 yarıyıl ve 240 AKTS'den oluşur.

## Eğitim Programları
1. **%30 İngilizce Lisans Programı:** Müfredattaki zorunlu ve seçmeli derslerin toplam AKTS kredisinin en az %30'u İngilizce olarak verilir.
2. **%100 İngilizce Lisans Programı:** Müfredattaki tüm meslek ve temel dersler İngilizce olarak okutulur.

## Laboratuvar Altyapısı
EHM Bölümü eğitiminde uygulamalı laboratuvarlar hayati öneme sahiptir. Lisans laboratuvarları:
- **Devre ve Sistemler Laboratuvarı (BB02):** Elektrik Devre Temelleri ve Devre Analizi deneyleri.
- **Haberleşme Laboratuvarı (BB03):** Analog ve sayısal modülasyon, spektrum analizi deneyleri.
- **Mikrodalga ve Anten Laboratuvarı (BB04):** Dalga kılavuzları, anten ışıma diyagramları, S-parametreleri.
- **İleri Lojik Devreler Laboratuvarı (BB05):** FPGA, CPLD, VHDL/Verilog uygulamaları.
- **Elektronik Laboratuvarı (BB07):** BJT, MOSFET, Op-Amp devreleri ve güç elektroniği.
- **Mikroişlemcili Sistem Tasarımı Laboratuvarı (BB09):** ARM mikrodenetleyiciler ve gömülü yazılım.
- **CAD Laboratuvarı (BB10):** Devre simülasyonu, PCB tasarımı ve elektromanyetik simülasyon.

## Yandal ve Çift Anadal (ÇAP)
- Bilgisayar Mühendisliği, Elektrik Mühendisliği, Kontrol ve Otomasyon Mühendisliği ve Matematik Mühendisliği ile aktif ÇAP ve Yandal anlaşmaları mevcuttur.
"""
    )

    # 5. Staj ve Bitirme Esasları
    write_file(
        f"{base_dir}/staj_ve_bitirme_esaslari.md",
        """---
baslik: "EHM Staj, Tasarım Projesi ve Bitirme Çalışması Esasları"
kaynak_url: "https://ehm.yildiz.edu.tr/ogrenci/staj"
kategori: "staj_ve_bitirme"
anahtar_kelimeler: ["ehm staj", "genel staj 30 gün", "mesleki staj 30 gün", "ehm4200", "ehm9000", "staj defteri fr-1876"]
---

# EHM Staj, Tasarım Projesi ve Bitirme Çalışması Esasları

> [!NOTE] Özet
> EHM öğrencileri mezun olabilmek için 30 iş günü Genel Staj ve 30 iş günü Mesleki Staj olmak üzere toplam **60 iş günü zorunlu staj** yapmak ve Tasarım Projesi (EHM4200) ile Bitirme Çalışmasını (EHM9000) başarıyla tamamlamak zorundadır.

## 1. Staj Kuralları ve Aşamaları
- **Genel Staj (EHM2002 - 30 İş Günü):** En erken 2. sınıfın (4. yarıyıl) bitiminde yaz döneminde yapılabilir. Donanım montaj, test, lehimleme, basit devre analizleri ve fabrika üretim hatları süreçlerini kapsar.
- **Mesleki Staj (EHM3002 - 30 İş Günü):** Genel stajı onaylanmayan öğrenci mesleki staja başlayamaz! En erken 3. sınıfın (6. yarıyıl) bitiminde yapılır. Elektronik tasarım, haberleşme sistemleri, gömülü yazılım, RF/mikrodalga veya Ar-Ge birimlerinde mühendislik düzeyinde yapılır.
- **Staj Başvuru Evrakları:**
  - `FR-0284` - YTÜ SGK Staj Formu (Staja başlamadan en az 10 gün önce teslim edilmeli)
  - `FR-0286` - Staj Sicil Formu
  - `FR-1266` - İşsizlik Fonu Katkısı Bilgi Formu
- **Staj Defteri Teslimi:**
  - Staj tamamlandıktan sonra en geç **1 ay içinde** `FR-1876` formatında hazırlanmış, mühendis tarafından kaşeli/imzalı staj defteri bölüm staj komisyonuna teslim edilmelidir. Süresi içinde teslim edilmeyen stajlar geçersiz sayılır.

## 2. Tasarım Projesi (EHM4200)
- 7. Yarıyılda (4. sınıf güz) alınır. Kredisi: 4, AKTS: 5.
- Öğrencinin mühendislik tasarımı yapma, komponent seçme, simülasyon ve prototipleme becerilerini ölçer.
- `FR-1486` ve `FR-1487` formları ile komisyonca değerlendirilir.
- **Önkoşul:** EHM9000 Bitirme Çalışması dersini alabilmek için EHM4200 Tasarım Projesi dersinin başarılmış olması zorunludur!

## 3. Bitirme Çalışması (EHM9000)
- 8. Yarıyılda (4. sınıf bahar) alınır. Kredisi: 5, AKTS: 10.
- Öğretim üyesi danışmanlığında kapsamlı bir araştırma veya özgün donanım/yazılım projesi yürütülür.
- Tez yazım kılavuzuna (`DD-022`) uygun tez raporu hazırlanır, intihal raporu (Turnitin en fazla %20) alınır ve jüri önünde sözlü sunum yapılır.
- `FR-1484` ve `FR-1485` formları ile jüri tarafından notlandırılır.
"""
    )

    # 6. Sınav Kuralları
    write_file(
        f"{base_dir}/sinav_kurallari.md",
        """---
baslik: "EHM Bölüm Sınav Kuralları ve Salon Disiplini"
kaynak_url: "https://ehm.yildiz.edu.tr/ogrenci/sinav-kurallari"
kategori: "sinav_kurallari"
anahtar_kelimeler: ["ehm sınav kuralları", "hesap makinesi", "salon disiplini", "sınav itirazı", "yö-075"]
---

# EHM Bölümü Sınav Kuralları

> [!NOTE] Özet
> EHM sınavları YTÜ Sınav Yönergesi (YÖ-075) ve bölüm kurallarına göre yürütülür. Programlanabilir hesap makineleri ve akıllı cihazların kullanımı öğretim elemanının açık iznine tabidir.

## Sınav Salon Kuralları
1. **Kimlik:** Öğrenciler YTÜ Öğrenci Kimlik Kartını sınav süresince sıralarında görünür şekilde bulundurmak zorundadır.
2. **Hesap Makinesi:** Sadece standart bilimsel fonksiyonlu (non-programmable) hesap makinelerine izin verilir. Metin saklayabilen veya kablosuz bağlantısı olan hesap makineleri yasaktır.
3. **Cep Telefonları:** Telefonlar sınav başlamadan önce kapatılarak çantaya veya gözetmenin gösterdiği masaya konulmalıdır. Masada veya cepte telefon bulunması doğrudan kopya teşebbüsü sayılır.
4. **İlk ve Son Çıkış Kısıtlaması:** Sınavın ilk 30 dakikası ve son 15 dakikası salondan çıkış yasaktır.
5. **İtiraz Süresi:** İlan edilen sınav sonucuna itiraz, not ilanından itibaren **3 iş günü içinde** bölüm başkanlığına verilecek maddi hata dilekçesi ile yapılır.
"""
    )

    # 7. Sıkça Sorulan Sorular
    write_file(
        f"{base_dir}/sikca_sorulan_sorular.md",
        """---
baslik: "EHM Bölümü Sıkça Sorulan Sorular (Resmi Bölüm Kılavuzu)"
kaynak_url: "https://ehm.yildiz.edu.tr/ogrenci/sikca-sorulan-sorular"
kategori: "ehm_sss"
anahtar_kelimeler: ["ehm sss", "staj sırası", "staj belgeleri", "çap sınav çakışması", "tasarım projesi", "bitirme komisyonu"]
---

# EHM Bölümü Sıkça Sorulan Sorular

> [!NOTE] Özet
> Aşağıda EHM Bölüm Başkanlığı resmi web sitesindeki tüm soru ve cevaplar, staj süreçleri, bitirme çalışması ve sınav çakışma prosedürleri yer almaktadır.

### Soru 1: Önce hangi stajımı yapmam gerekiyor?
**Cevap:** Öncelikle 30 günlük Genel Stajınızı (EHM2002) yapmanız gereklidir. Genel stajınız Bölüm Staj Komisyonu tarafından kabul edilmeden Mesleki Stajınızı (EHM3002) yapamazsınız.

### Soru 2: En erken ne zaman staj yapabilirim?
**Cevap:** 2. sınıfın bitiminde (4. yarıyılın sonundaki yaz döneminde) staj yapabilirsiniz.

### Soru 3: Staja başlamak için hangi belgeleri hazırlamam gerekli?
**Cevap:**
1. `FR-0284` - Yıldız Teknik Üniversitesi SGK Staj Formu
2. `FR-0286` - Staj Sicil Formu
3. `FR-1266` - Staj Ücretlerine İşsizlik Fonu Katkısı Bilgi Formu (Kamu kurumlarında staj yapılması durumunda vermenize gerek yoktur).

### Soru 4: Evraklarımı verip hemen ertesi gün staja başlayabilir miyim?
**Cevap:** Hayır. SGK işe giriş bildirgelerinin yasal süresinde yapılabilmesi için evrak teslim tarihinden itibaren en erken 10 gün sonrasında staja başlanabilir.

### Soru 5: 30 günlük stajımı iki defada bölebilir miyim?
**Cevap:** Zorunlu olmadıkça stajların bölünmeden tek seferde yapılması esastır; istisnai durumlarda staj komisyonunun önceden onayı gerekir.

### Soru 6: Staja başladıktan sonra erken bitirme veya uzatma işlemi yapabilir miyim?
**Cevap:** Evet yapabilirsiniz. Dekanlık Staj Ofisine dilekçe vererek erken bitirme veya uzatma işlemi gerçekleştirebilirsiniz.

### Soru 7: Genel ve mesleki staj dışında gönüllü staj yapabilir miyim?
**Cevap:** Evet, zorunlu olmayan (gönüllü) staj yapabilirsiniz. Staja başlama evraklarınızı ve dilekçenizi ekleyerek Bölüm Başkanlığına başvurmanız gereklidir.

### Soru 8: Dönem (yarıyıl) içerisinde staj yapabilir miyim?
**Cevap:** Ders döneminde staj yapılamaz; stajlar kural olarak yaz tatillerinde yapılır. Ancak tüm derslerini tamamlamış ve sadece stajı kalmış olan öğrenciler dönem içinde staj yapabilirler.

### Soru 9: Staj bitiminde hangi formatta defter teslim etmeliyim?
**Cevap:** `FR-1876` - Yıldız Teknik Üniversitesi Staj Defteri (Rapor Formatı) kullanılmalıdır.

### Soru 10: Staj bitiminden itibaren ne kadarlık sürede staj defterimi teslim etmem gerekli?
**Cevap:** Stajın tamamlanmasından itibaren en geç **bir (1) ay içerisinde** teslim edilmeyen staj defteri değerlendirmeye alınmaz ve staj iptal edilir.

### Soru 11: Bütünleme sınav haftasında staj yapabilir miyim?
**Cevap:** Bütünleme sınavlarına girmeyeceğinize dair yazılı dilekçe verirseniz bütünleme sınav haftasında staj yapabilirsiniz.

### Soru 12: Staj yerim cumartesi günleri yarım gün çalışıyor, staj gününe saydırabilir miyim?
**Cevap:** Hayır, yarım günler staj günü olarak sayılmaz. Cumartesi gününün sayılabilmesi için kurumun tam gün çalıştığının belgelenmesi gerekir.

### Soru 13: Staj defterimi kim imzalamalıdır?
**Cevap:** Yapmış olduğunuz staj çalışması mühendislik birikimi gerektirdiğinden staj defterinizi ilgili alanda çalışan bir Elektrik, Elektronik veya Haberleşme Mühendisinin imzalaması ve kaşelemesi zorunludur.

### Soru 14: Tasarım Projesi ve Bitirme Çalışması Komisyonu iletişim adresi nedir?
**Cevap:** Bölüm web sitesinde ilan edilen Tasarım Projesi ve Bitirme Çalışması Komisyonu e-posta adresine başvurulmalıdır.

### Soru 15: Çift anadal (ÇAP) öğrencisiyim, sınav programımda çakışma olması durumunda ne yapmalıyım?
**Cevap:** Sınav takvimi açıklandıktan sonra belirlenen süre içinde ilgili bölüm başkanlığına sınav çakışma dilekçesi vererek mazeret sınavına girmeyi talep etmelisiniz.
"""
    )

    # 8. Bologna Ders Planı Dosyaları
    bologna_dir = f"{base_dir}/bologna_ders_plani"
    
    # 8.1 README
    write_file(
        f"{bologna_dir}/README.md",
        """---
baslik: "EHM Bologna 8 Yarıyıl Müfredatı ve AKTS Dağılımı"
kaynak_url: "https://www.bologna.yildiz.edu.tr/index.php?r=program/view&id=6&aid=5"
kategori: "bologna_mufredat"
anahtar_kelimeler: ["bologna ders planı", "akts", "kredi", "8 yarıyıl", "zorunlu dersler", "seçmeli dersler"]
---

# EHM Bologna Lisans Öğretim Planı Genel Matrisi

> [!NOTE] Özet
> EHM Lisans Programı toplam **240 AKTS** ve 8 yarıyıldan oluşmaktadır. Her yarıyıl 30 AKTS kredi yüküne sahiptir.

## Yarıyıllara Göre AKTS Dağılımı

| Yarıyıl | Dönem | Zorunlu AKTS | Seçmeli AKTS | Toplam AKTS |
|---|---|---|---|---|
| **1. Yarıyıl** | 1. Sınıf Güz | 30 | 0 | 30 |
| **2. Yarıyıl** | 1. Sınıf Bahar | 30 | 0 | 30 |
| **3. Yarıyıl** | 2. Sınıf Güz | 30 | 0 | 30 |
| **4. Yarıyıl** | 2. Sınıf Bahar | 27 | 3 (USS-1) | 30 |
| **5. Yarıyıl** | 3. Sınıf Güz | 24 | 6 (MES-1) | 30 |
| **6. Yarıyıl** | 3. Sınıf Bahar | 27 | 3 (USS-2) | 30 |
| **7. Yarıyıl** | 4. Sınıf Güz | 20 | 10 (MES-3, UMS) | 30 |
| **8. Yarıyıl** | 4. Sınıf Bahar | 15 (EHM9000 vb.) | 15 (MES-4) | 30 |
| **GENEL TOPLAM** | **8 Yarıyıl** | **203** | **37** | **240 AKTS** |

## Dosyalar ve İnceleme Linkleri
- [Önkoşul Zinciri ve Bağımlılık Haritası](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/bologna_ders_plani/onkosul_zinciri.md)
- [1. Yarıyıl Dersleri](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/bologna_ders_plani/1_yariyil.md)
- [2. Yarıyıl Dersleri](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/bologna_ders_plani/2_yariyil.md)
- [3. Yarıyıl Dersleri](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/bologna_ders_plani/3_yariyil.md)
- [4. Yarıyıl Dersleri](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/bologna_ders_plani/4_yariyil.md)
- [5. Yarıyıl Dersleri](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/bologna_ders_plani/5_yariyil.md)
- [6. Yarıyıl Dersleri](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/bologna_ders_plani/6_yariyil.md)
- [7. Yarıyıl Dersleri](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/bologna_ders_plani/7_yariyil.md)
- [8. Yarıyıl Dersleri](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/bologna_ders_plani/8_yariyil.md)
- [Seçimlik Ders Havuzları](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/05_fakulteler_ve_bolumler/elektrik_elektronik_fakultesi/elektronik_ve_haberlesme_muhendisligi/bologna_ders_plani/secimlik_ders_havuzlari.md)
"""
    )

    # 8.2 Önkoşul Zinciri
    write_file(
        f"{bologna_dir}/onkosul_zinciri.md",
        """---
baslik: "EHM Bologna Önkoşul Zincirleri ve Ders Bağımlılık Haritası"
kategori: "onkosul_haritasi"
anahtar_kelimeler: ["önkoşul", "bağımlılık", "kilit dersler", "bitirme önkoşulu", "laboratuvar önkoşulları"]
---

# EHM Bologna Önkoşul Zincirleri ve Bağımlılık Haritası

> [!IMPORTANT] Kritik Bilgi
> Önkoşullu bir dersi alabilmek için, o dersin önkoşulu olarak tanımlanan dersin/derslerin önceden alınmış ve **başarılmış (en az DD/DC ve üzeri)** olması zorunludur. Önkoşulu sağlanmayan ders OBS üzerinde seçilemez.

## 1. Resmi Önkoşul Listesi

| Ders Kodu | Ders Adı | Yarıyıl | Zorunlu Önkoşul Dersi | Açıklama |
|---|---|---|---|---|
| **EHM2171** | Elektrik Devre Temelleri Laboratuvarı | 3. Yarıyıl | **EHM1012** (Elektrik Devre Temelleri) | Devre temelleri teorisini geçmeyen laboratuvara giremez. |
| **EHM2162** | Lojik Devre Laboratuvarı | 4. Yarıyıl | **EHM2141** (Lojik Devreler) | Lojik devreler teorisi başarılmalıdır. |
| **EHM3151** | Elektronik Devreler 1 Laboratuvarı | 5. Yarıyıl | **EHM2122** (Elektronik Devreler 1) | Elektronik 1 teorisi başarılmalıdır. |
| **EHM3172** | Elektronik Devreler 2 Laboratuvarı | 6. Yarıyıl | **EHM3111** (Elektronik Devreler 2) | Elektronik 2 teorisi başarılmalıdır. |
| **EHM3152** | Haberleşme Laboratuvarı | 6. Yarıyıl | **EHM3131** (Haberleşme 1) | Haberleşme 1 teorisi başarılmalıdır. |
| **EHM3162** | Mikrodalga ve Anten Laboratuvarı | 6. Yarıyıl | **EHM3121** (Mikrodalga 1) | Mikrodalga 1 teorisi başarılmalıdır. |
| **EHM9000** | Bitirme Çalışması | 8. Yarıyıl | **EHM4200** (Tasarım Projesi) | Tasarım projesini başarmayan öğrenci Bitirme Tezine başlayamaz! |

## 2. Staj ve İlerleme Zincirleri
1. **Genel Staj (EHM2002):** En erken 4. yarıyılın sonunda yapılabilir.
2. **Mesleki Staj (EHM3002):** Önkoşul olarak Genel Stajın (EHM2002) yapılmış ve komisyonca kabul edilmiş olması şarttır.
3. **Tasarım Projesi (EHM4200):** En erken 7. yarıyılda alınabilir.

## 3. Görsel Önkoşul Akış Şeması

```mermaid
graph TD
    subgraph Devre_ve_Elektronik_Hatti
        EHM1012["EHM1012 Elektrik Devre Temelleri"] --> EHM2171["EHM2171 Elektrik Devre Temelleri Lab"]
        EHM1012 --> EHM2121["EHM2121 Devre ve Sistem Analizi"]
        EHM2121 --> EHM2122["EHM2122 Elektronik Devreler 1"]
        EHM2122 --> EHM3151["EHM3151 Elektronik Devreler 1 Lab"]
        EHM2122 --> EHM3111["EHM3111 Elektronik Devreler 2"]
        EHM3111 --> EHM3172["EHM3172 Elektronik Devreler 2 Lab"]
    end

    subgraph Lojik_ve_Islemci_Hatti
        EHM2141["EHM2141 Lojik Devreler"] --> EHM2162["EHM2162 Lojik Devre Lab"]
        EHM2141 --> EHM3141["EHM3141 Mikroişlemci Sistemleri"]
    end

    subgraph Haberlesme_ve_Mikrodalga_Hatti
        EHM2131["EHM2131 Elektromanyetik Alan"] --> EHM2132["EHM2132 Elektromanyetik Dalga"]
        EHM2132 --> EHM3121["EHM3121 Mikrodalga 1"]
        EHM3121 --> EHM3162["EHM3162 Mikrodalga ve Anten Lab"]
        EHM3121 --> EHM3112["EHM3112 Antenler ve Propagasyon"]
        EHM2152["EHM2152 İşaret ve Sistemler"] --> EHM3131["EHM3131 Haberleşme 1"]
        EHM3131 --> EHM3152["EHM3152 Haberleşme Lab"]
        EHM3131 --> EHM3122["EHM3122 Haberleşme 2"]
    end

    subgraph Bitirme_Hatti
        EHM4200["EHM4200 Tasarım Projesi (7. Yarıyıl)"] -->|Zorunlu Önkoşul| EHM9000["EHM9000 Bitirme Çalışması (8. Yarıyıl)"]
    end
```
"""
    )

    # 8.3 Yarıyıllar 1 - 8
    sem_keys = list(bologna_data.keys())
    for idx, sem_key in enumerate(sem_keys):
        sem_num = idx + 1
        course_list = bologna_data[sem_key]
        sem_filename = f"{bologna_dir}/{sem_num}_yariyil.md"
        
        md_text = f"""---
baslik: "EHM Bologna {sem_num}. Yarıyıl Dersleri ve Detay Kartları"
yariyil: {sem_num}
kategori: "bologna_yariyil"
anahtar_kelimeler: ["ehm {sem_num}. yarıyıl", "ders içerikleri", "akts", "haftalık izlence", "değerlendirme"]
---

# EHM {sem_num}. Yarıyıl Ders Programı ve Detaylı Kartları

> [!NOTE] Yarıyıl Özeti
> **Dönem:** {sem_key}  
> **Toplam Ders Sayısı:** {len(course_list)}  
> **Hedef AKTS:** 30 AKTS

## Ders Listesi Tablosu

| Kodu | Önkoşul | Ders Adı | T+U+L | Kredi | AKTS |
|---|---|---|---|---|---|
"""
        for c in course_list:
            p = c.get('prerequisites') or c.get('prereq') or 'Yok'
            t = c.get('theory', '0')
            u = c.get('app', '0')
            l = c.get('lab', '0')
            md_text += f"| **{c['code']}** | {p} | {c['name']} | {t}+{u}+{l} | {c['credit']} | {c['ects']} |\n"

        md_text += "\n---\n\n## Ders Detay Kartları ve İzlenceleri\n\n"

        for c in course_list:
            c_name = c['name']
            c_code = c['code']
            c_ects = c['ects']
            c_cred = c['credit']
            c_obj = c.get('objective', 'Bu dersin amacı Bologna bilgi sisteminde tanımlıdır.')
            c_content = c.get('content', 'Ders içeriği teorik ve pratik konuları kapsar.')
            c_prereq = c.get('prerequisites') or c.get('prereq') or 'Yok'
            
            md_text += f"### {c_code} - {c_name}\n"
            md_text += f"- **Kredi:** {c_cred} | **AKTS:** {c_ects} | **Önkoşul:** `{c_prereq}`\n"
            if c.get('link'):
                md_text += f"- **Bologna Bağlantısı:** [Resmi Ders Sayfası]({c['link']})\n"
            md_text += f"\n**Dersin Amacı:**\n{c_obj}\n\n"
            md_text += f"**Dersin İçeriği:**\n{c_content}\n\n"

            # Weekly Plan
            weekly = c.get('weekly_plan', [])
            if weekly:
                md_text += "**Haftalık Ders Planı:**\n\n"
                md_text += "| Hafta | Konular |\n|---|---|\n"
                for w in weekly:
                    md_text += f"| {w['week']} | {w['topic']} |\n"
                md_text += "\n"

            # Assessments
            assessments = c.get('assessments', [])
            if assessments:
                md_text += "**Değerlendirme Sistemi:**\n\n"
                md_text += "| Etkinlik | Sayı | Katkı Payı (%) |\n|---|---|---|\n"
                for a in assessments:
                    md_text += f"| {a['activity']} | {a['count']} | %{a['weight']} |\n"
                md_text += "\n"

            md_text += "---\n\n"

        write_file(sem_filename, md_text)

    # 8.4 Seçimlik Ders Havuzları
    write_file(
        f"{bologna_dir}/secimlik_ders_havuzlari.md",
        """---
baslik: "EHM Seçimlik Ders Havuzları ve Teknik Seçmeli Grupları"
kategori: "secimli_dersler"
anahtar_kelimeler: ["mesleki seçmeli", "teknik seçmeli", "sosyal seçmeli", "uss", "mes", "ums"]
---

# EHM Seçimlik Ders Havuzları

> [!NOTE] Özet
> EHM lisans programında öğrenciler 4. yarıyıldan itibaren Üniversite Sosyal Seçmeli (USS), Üniversite Mesleki Seçmeli (UMS) ve Alan İçi Mesleki Seçmeli (MES) ders havuzlarından ders seçerler.

## 1. Seçmeli Ders Kategorileri
- **USS (Üniversite Sosyal Seçmeli):** Felsefe, sosyoloji, psikoloji, sanat tarihi, müzik, girişimcilik, ekonomi ve yabancı dil gibi üniversite genel havuzundan seçilen dersler.
- **UMS (Üniversite Mesleki Seçmeli):** Mühendislik fakültelerinin diğer bölümlerinden (Bilgisayar, Elektrik, Makine, Kontrol vb.) alınan disiplinlerarası teknik dersler.
- **MES (Mesleki Seçmeli Dersler - EHM Havuzu):** EHM öğrencilerinin uzmanlaşmak istedikleri alt dallara göre bölüm tarafından açılan ileri düzey dersler.

## 2. EHM Öne Çıkan Mesleki Seçmeli Dersleri
- **MTH4110:** Üründe Elektronik Donanım Geliştirme ve Onay Süreçleri (AKTS: 5)
- **MTH4100:** Derin Öğrenme Uygulamaları (AKTS: 5)
- **MTH4200:** Model Tabanlı Tasarım ve Yapay Zeka (AKTS: 5)
- **MTH4300:** Elektrikli Araç Teknolojileri (AKTS: 5)
- **MTH4400:** Yeni Nesil Kablosuz Haberleşme Teknolojileri (5G/6G) (AKTS: 5)
- **MTH4500:** Vakum Mikrodalga Tüp Teknolojisi (AKTS: 5)
- **EHM3741:** Gömülü Sistemlerde Makine Öğrenmesi (AKTS: 5)
- **EHM3161:** İleri Elektronik Uygulamaları (AKTS: 5)
- **EHM3171:** Devre Sentezi (AKTS: 5)
- **EHM4131:** Sayısal Haberleşme (AKTS: 5)
- **EHM4141:** Optik Haberleşme (AKTS: 5)
- **EHM4151:** Radar Sistemleri (AKTS: 5)
"""
    )

    print("05_fakulteler_ve_bolumler completed successfully!")

if __name__ == '__main__':
    generate_ehm()
