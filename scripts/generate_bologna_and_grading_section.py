import os
import json

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {path}")

def generate_bologna():
    print("Generating 04_bologna_ve_not_sistemi...")

    # README
    write_file(
        "04_bologna_ve_not_sistemi/README.md",
        """---
baslik: "YTÜ Bologna Süreci, Kabul ve Not Sistemi Rehberi"
kategori: "bologna_ve_not_sistemi"
anahtar_kelimeler: ["bologna", "not sistemi", "harf notları", "akts", "bağıl sistem", "kabul koşulları", "agno"]
---

# YTÜ Bologna Süreci, Not ve Değerlendirme Sistemi

> [!NOTE] Özet
> Yıldız Teknik Üniversitesi, Avrupa Yükseköğretim Alanı (EHEA) Bologna Süreci standartlarına tam uyumlu olarak AKTS (Avrupa Kredi Transfer Sistemi), diploma eki etiketi ve bağıl not değerlendirme sistemini uygulamaktadır.

## Bu Bölümün İçeriği
- [Kabul ve Kayıt Koşulları](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/04_bologna_ve_not_sistemi/kabul_ve_kayit_kosullari.md): YKS, DGS, Merkezi Yerleştirme (Ek Madde-1), Kurumlararası/Kurumiçi Yatay Geçiş, YÖS ve ÇAP kayıt koşulları.
- [Not Sistemi ve Harf Notları](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/04_bologna_ve_not_sistemi/not_sistemi_ve_harf_notlari.md): AA'dan FF'ye katsayılar, geçme notları, koşullu geçiş (DC, DD), F0 ve FG tanımları.
- [Bağıl Değerlendirme Sistemi](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/04_bologna_ve_not_sistemi/bagil_degerlendirme_sistemi.md): Yarıyıl içi (%60) ve yarıyıl sonu (%40) ağırlıkları, sınıf ortalaması, standart sapma, T-skoru ve harf notu baremleri.
- [AGNO ve Akademik Başarı Tanımları](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/04_bologna_ve_not_sistemi/agno_ve_akademik_basari_tanimlari.md): YNO, AGNO hesaplama formülü, başarılı, koşullu ve başarısız öğrenci durumları.
"""
    )

    # Kabul ve Kayıt Koşulları
    write_file(
        "04_bologna_ve_not_sistemi/kabul_ve_kayit_kosullari.md",
        """---
baslik: "YTÜ Lisans Programları Genel Kabul ve Kayıt Koşulları"
kaynak_url: "https://www.bologna.yildiz.edu.tr/index.php?r=institution/admission"
kategori: "kabul_ve_kayit"
anahtar_kelimeler: ["yks", "dgs", "yatay geçiş", "ek madde 1", "yurtdışı kabul", "çap", "kayıt"]
---

# YTÜ Lisans Programları Genel Kabul ve Kayıt Koşulları

> [!NOTE] Özet
> YTÜ lisans programlarına öğrenci kabulü ÖSYM tarafından yapılan Yükseköğretim Kurumları Sınavı (YKS - TYT/AYT Sayısal Puanı), Dikey Geçiş Sınavı (DGS), Yatay Geçiş (Not ortalaması veya Ek Madde-1) ve Yurt Dışından Öğrenci Kabulü (YTÜYÖS / SAT) yoluyla gerçekleşir.

## 1. YKS ile Yerleşen Öğrenciler
- Türkiye Cumhuriyeti ve KKTC vatandaşı öğrenciler ÖSYM'nin merkezi yerleştirmesi ile kayıt hakkı kazanırlar.
- Kayıtlar belirlenen tarihlerde **e-Devlet Kapısı** üzerinden şifre ile veya e-Devlet kaydı yapılamayan özel durumlarda şahsen üniversiteye başvurularak yapılır.
- %30 ve %100 İngilizce programlara yerleşen adayların e-Devlet kaydından sonra Eylül ayında düzenlenen İngilizce Yeterlik Sınavı'na (İYS) girmeleri veya uluslararası muafiyet belgesi sunmaları gerekir.

## 2. Dikey Geçiş Sınavı (DGS) ile Kabul
- Meslek Yüksekokulu ve Açıköğretim önlisans mezunları DGS ile lisans programlarına yerleştirilirler.
- Öğrenciler daha önce aldıkları önlisans dersleri için Bölüm İntibak Komisyonu'na muafiyet başvurusunda bulunur ve eşdeğer sayılan derslere göre intibakları yapılır (YÖ-015 Yönergesi).

## 3. Yatay Geçiş ile Kabul
- **Merkezi Yerleştirme Puanı ile (Ek Madde-1):** Öğrencinin kayıt olduğu yıldaki ÖSYS/YKS puanı, geçmek istediği YTÜ programının o yılki taban puanına eşit veya yüksekse hazırlık sınıfı dahil her yarıyılda yatay geçiş yapılabilir.
- **Başarı Not Ortalaması ile (Kurumlararası / Kurumiçi):** En erken 3. yarıyıl, en geç 5. yarıyıl başında; alttan başarısız dersi olmamak ve AGNO'su en az belirlenen barajda (genellikle 3.00 ve üzeri) olmak kaydıyla kontenjan dahilinde başvuru yapılabilir.

## 4. Yurt Dışından Kabul (Uluslararası Öğrenciler)
- YTÜ Senatosu tarafından kabul edilen uluslararası sınavlar (SAT, ACT, GCE A-Level, Bakalorya vb.) veya YTÜ Uluslararası Öğrenci Sınavı (YTÜYÖS) puanı ile başvuran adaylar değerlendirilir (YÖ-102 Yönergesi).
"""
    )

    # Not Sistemi ve Harf Notları
    write_file(
        "04_bologna_ve_not_sistemi/not_sistemi_ve_harf_notlari.md",
        """---
baslik: "YTÜ Not Sistemi, Harf Notları ve Katsayıları"
kaynak_url: "https://www.bologna.yildiz.edu.tr/index.php?r=institution/grading"
kategori: "not_sistemi"
anahtar_kelimeler: ["harf notu", "katsayı", "aa", "ba", "bb", "cb", "cc", "dc", "dd", "ff", "f0", "fg"]
---

# YTÜ Not Sistemi ve Harf Notları

> [!NOTE] Özet
> YTÜ'de 4.00'lük katsayı sistemi uygulanır. AA-CC arası doğrudan başarılı, DC ve DD koşullu başarılı (Mezuniyet için AGNO >= 2.00 şartı aranır), FF, F0 ve FG ise başarısız notlardır.

## Resmi Harf Notu ve Katsayı Tablosu

| Başarı Notu | Katsayı | Başarı Düzeyi | Durum ve Açıklama |
|---|---|---|---|
| **AA** | 4.00 | Mükemmel | Başarılı (Doğrudan geçer) |
| **BA** | 3.50 | Pekiyi | Başarılı |
| **BB** | 3.00 | İyi | Başarılı |
| **CB** | 2.50 | Orta | Başarılı |
| **CC** | 2.00 | Yeterli | Başarılı (Asgari mezuniyet barajı) |
| **DC** | 1.50 | Koşullu Başarılı | AGNO >= 2.00 ise geçer, aksi halde tekrar edilebilir |
| **DD** | 1.00 | Koşullu Başarılı | AGNO >= 2.00 ise geçer, aksi halde tekrar edilebilir |
| **FF** | 0.00 | Başarısız | Sınav ve çalışmalarda başarısız, ders tekrarı zorunlu |
| **F0** | 0.00 | Devamsız Başarısız | Derse devam şartını sağlamayan öğrenci; finale giremez |
| **FG** | 0.00 | Sınava Girmedi | Devam şartını sağladığı halde yarıyıl sonu sınavına girmedi |

## Diğer Not Kodları
- **BL (Başarılı / Pass):** Kredisiz derslerden veya stajlardan başarılı olanlara verilir; ortalamaya katılmaz.
- **BS (Başarısız / Fail):** Kredisiz derslerden veya stajlardan başarısız olanlara verilir.
- **M (Muaf):** Daha önce başka programda başardığı için intibakla muaf tutulan dersler.
- **G (Geçer):** Kredisiz tamamlama dersleri.
- **I (Eksik / Incomplete):** Belgelenebilir mazereti sebebiyle ders içi projesi veya laboratuvarı tamamlayamamış öğrenciye verilir; belirtilen sürede tamamlanmazsa FF'ye dönüşür.
"""
    )

    # Bağıl Değerlendirme Sistemi
    write_file(
        "04_bologna_ve_not_sistemi/bagil_degerlendirme_sistemi.md",
        """---
baslik: "YTÜ Bağıl Değerlendirme Sistemi ve Başarı Hesaplama Esasları"
kategori: "bagil_sistem"
anahtar_kelimeler: ["bağıl değerlendirme", "sınıf ortalaması", "standart sapma", "t-skoru", "vize ağırlığı %60", "final ağırlığı %40"]
---

# YTÜ Bağıl Değerlendirme Sistemi

> [!NOTE] Özet
> YTÜ'de bir dersin başarı notu mutlak barem yerine sınıfın genel başarı düzeyi, aritmetik ortalaması ve standart sapması dikkate alınarak bağıl değerlendirme sistemi (BDS) ile belirlenir.

## Yarıyıl İçi ve Yarıyıl Sonu Ağırlıkları
- **Yarıyıl İçi Notu (Yİ):** Ara sınavlar, kısa sınavlar (quiz), ödevler, laboratuvar ve projelerden oluşur. Kural olarak ders başarı notuna katkısı **%60**'tır.
- **Yarıyıl Sonu Notu (YS):** Final veya bütünleme sınavıdır. Başarı notuna katkısı **%40**'tır.
- **Ders Başarı Puanı (DBP):** `DBP = (Yarıyıl İçi Notu * 0.60) + (Yarıyıl Sonu Notu * 0.40)` formülü ile 100 üzerinden hesaplanır. (Dersin Bologna formunda farklı ağırlıklar tanımlanmışsa o ağırlıklar esas alınır).

## Bağıl Değerlendirme Uygulama Şartları
1. **Derse Devam ve Sınava Giriş:** Devamsızlıktan kalan (F0) veya finale girmeyen (FG) öğrenciler sınıf ortalaması ve standart sapma hesabına dahil edilmez.
2. **Ham Başarı Alt Sınırı:** Yarıyıl sonu sınavından veya ham başarı puanından belirlenen asgari barajın (örneğin 35 veya 40 ham puan) altında kalan öğrenciler bağıl hesaba katılmadan doğrudan FF alabilirler.
3. **Sınıf Mevcudu:** Bağıl değerlendirmenin istatistiksel olarak sağlıklı uygulanabilmesi için derse kayıtlı ve sınava girmiş öğrenci sayısının Senato tarafından belirlenen eşiğin (genellikle 15-20 öğrenci) üzerinde olması gerekir. Öğrenci sayısı az olan sınıflarda mutlak değerlendirme uygulanabilir.
"""
    )

    # AGNO ve Akademik Başarı
    write_file(
        "04_bologna_ve_not_sistemi/agno_ve_akademik_basari_tanimlari.md",
        """---
baslik: "YTÜ YNO, AGNO Hesaplama Formülü ve Akademik Başarı Tanımları"
kategori: "akademik_basari"
anahtar_kelimeler: ["agno", "yno", "ağırlıklı genel not ortalaması", "başarılı öğrenci", "sınamalı öğrenci", "kredi"]
---

# YTÜ YNO ve AGNO Hesaplama Esasları

> [!NOTE] Özet
> Yarıyıl Not Ortalaması (YNO), öğrencinin o yarıyılda aldığı derslerin ağırlıklı ortalamasıdır. Ağırlıklı Genel Not Ortalaması (AGNO) ise öğrencinin üniversiteye başladığı andan itibaren aldığı tüm derslerin toplam ağırlıklı ortalamasıdır.

## Hesaplama Formülü

$$\\text{AGNO} = \\frac{\\sum (\\text{Dersin Kredisi} \\times \\text{Dersin Harf Notu Katsayısı})}{\\sum \\text{Toplam Alınan Kredi}}$$

### Örnek Hesaplama Tablosu:
| Ders Kodu | Kredi | Harf Notu | Katsayı | Ağırlıklı Puan (Kredi x Katsayı) |
|---|---|---|---|---|
| MAT1071 | 4 | BA | 3.50 | 14.00 |
| FIZ1001 | 4 | BB | 3.00 | 12.00 |
| EHM1051 | 3 | AA | 4.00 | 12.00 |
| MDB1031 | 3 | CC | 2.00 | 6.00 |
| **Toplam** | **14** | - | - | **44.00** |

$$\\text{Dönem Not Ortalaması} = \\frac{44.00}{14} = 3.14$$

## Akademik Durumlar ve Sonuçları
- **Başarılı Öğrenci:** AGNO'su en az **2.00** olan öğrenciler başarılı kabul edilir. Bu öğrenciler alt yarıyıllardan başarısız dersi yoksa ve AGNO'ları 3.00 üzerindeyse üst yarıyıldan ilave ders alabilirler.
- **Koşullu Başarılı Dersler (DC / DD):** Öğrencinin AGNO'su 2.00 veya üzerinde ise DC ve DD aldığı derslerden geçmiş sayılır; tekrar almak zorunda değildir. Ancak AGNO'sunu yükseltmek isterse bu dersleri tekrar seçebilir (Son alınan not geçerli olur).
- **Mezuniyet Barajı:** Bir öğrencinin tüm derslerini tamamlasa dahi mezun olabilmesi için son AGNO'sunun en az **2.00 / 4.00** olması şarttır.
"""
    )

    print("04_bologna_ve_not_sistemi completed successfully!")

if __name__ == '__main__':
    generate_bologna()
