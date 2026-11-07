import os
import re
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

def generate_ybd():
    print("Generating 03_yabanci_diller_yuksekokulu_ybd...")

    # README
    write_file(
        "03_yabanci_diller_yuksekokulu_ybd/README.md",
        """---
baslik: "Yabancı Diller Yüksekokulu (YBD) Genel Rehberi"
kategori: "hazirlik_ve_yabanci_dil"
kaynak_url: "https://ybd.yildiz.edu.tr/"
anahtar_kelimeler: ["ybd", "hazırlık", "temel ingilizce", "iys", "muafiyet", "kurlar", "erasmus", "dbs"]
---

# YTÜ Yabancı Diller Yüksekokulu (YBD) Genel Rehberi

> [!NOTE] Özet
> Yabancı Diller Yüksekokulu (YBD), Yıldız Teknik Üniversitesi'nin %30 ve %100 İngilizce lisans/lisansüstü programlarına kayıt yaptıran öğrencilerin zorunlu hazırlık eğitimini yürüten ve İngilizce Yeterlik Sınavı'nı (İYS) düzenleyen akademik birimdir.

## İletişim ve Yerleşim
- **Konum:** Davutpaşa Yerleşkesi, Yabancı Diller Yüksekokulu Binası, 34220 Esenler / İstanbul
- **Web Sitesi:** https://ybd.yildiz.edu.tr/
- **Bölümler:** 
  1. **Temel İngilizce Bölümü:** Zorunlu hazırlık sınıflarının eğitim-öğretimini yürütür.
  2. **Modern Diller Bölümü:** Fakültelerde verilen İleri İngilizce 1 (MDB1031), İleri İngilizce 2 (MDB1032) ve seçmeli ikinci yabancı dilleri (Almanca, Fransızca, İspanyolca, İtalyanca, Rusça vb.) yürütür.

## Bu Bölümün İçeriği
- [Hakkında ve Eğitim Yapısı](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/03_yabanci_diller_yuksekokulu_ybd/hakkinda_ve_egitim_yapisi.md): Misyon, hazırlık zorunluluğu, %30 ve %100 programlar, muafiyet şartları.
- [Kurlar, Ders İçerikleri ve Hedefler](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/03_yabanci_diller_yuksekokulu_ybd/kurlar_ders_icerikleri_hedefler.md): A1, A2, B1, B2, C1 kurları, haftalık ders saatleri ve CEFR dil kazanımları.
- [YBD Sıkça Sorulan Sorular (46 Madde)](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/03_yabanci_diller_yuksekokulu_ybd/sikca_sorulan_sorular.md): Devamsızlık, kitaplar, kurlar arası geçiş, raporlar ve İYS hakları.
- [Sınav ve Değerlendirme Kuralları](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/03_yabanci_diller_yuksekokulu_ybd/sinav_ve_degerlendirme_kurallari.md): Vize, kısa sınav, portfolyo, speaking, kur geçme ve İYS baraj puanları.
- [Sınavlarda Uyulacak Kurallar](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/03_yabanci_diller_yuksekokulu_ybd/sinavlarda_uyulacak_kurallar.md): Salon disiplini, kimlik kontrolü, optik form ve kopya cezaları.
- [Örnek Sınavlar ve İYS İncelemeleri](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/03_yabanci_diller_yuksekokulu_ybd/ornek_sinavlar_ve_iys/README.md): İYS 1. Oturum, 2. Oturum (dinleme/not alma), Essay kriterleri, Erasmus ve Lisansüstü sınav analizleri.
"""
    )

    # Hakkında ve Eğitim Yapısı
    write_file(
        "03_yabanci_diller_yuksekokulu_ybd/hakkinda_ve_egitim_yapisi.md",
        """---
baslik: "YBD Hakkında ve Hazırlık Eğitimi Yapısı"
kaynak_url: "https://ybd.yildiz.edu.tr/temel-ingilizce/hakkinda"
kategori: "hazirlik_yapisi"
anahtar_kelimeler: ["hazırlık süresi", "%30 ingilizce", "%100 ingilizce", "muafiyet", "iys", "toefl", "pte"]
---

# YBD Hakkında ve Hazırlık Eğitimi Yapısı

> [!NOTE] Özet
> YTÜ'de eğitim dili en az %30 veya %100 İngilizce olan tüm lisans ve lisansüstü program öğrencileri için İngilizce hazırlık eğitimi zorunludur. Öğrenciler İYS sınavından veya Senato tarafından eşdeğer kabul edilen uluslararası sınavlardan (TOEFL IBT, PTE Academic vb.) geçerli puan alarak hazırlıktan muaf olabilirler.

## Hazırlık Eğitimi Süresi ve Hakları
- **Normal Süre:** 1 akademik yıl (2 yarıyıl).
- **Azami Süre:** 2 akademik yıl (4 yarıyıl).
- İlk yılında hazırlığı geçemeyen öğrenciler, ikinci yıllarında hazırlık sınıfını tekrar edebilir veya sadece İYS sınavlarına girerek "Beklemeli Öğrenci" statüsünde dışarıdan hazırlanabilirler.
- 2. yılın sonunda da hazırlığı başaramayan %30 veya %100 İngilizce program öğrencilerinin üniversite ile ilişiği kesilir (veya YÖK tarafından Türkçe bir programa merkezi yerleştirme hakkı verilir).

## Hazırlık Muafiyet Koşulları
1. **YTÜ İYS (İngilizce Yeterlik Sınavı):** 100 üzerinden en az **60 puan** alan öğrenciler hazırlıktan muaf olur ve 1. sınıfa başlar. (Bölümü %100 İngilizce olan bazı programlar veya İleri İngilizce muafiyeti için daha yüksek puan gerekebilir).
2. **Uluslararası Eşdeğer Sınavlar (Senato Esasları):**
   - **TOEFL IBT:** En az 72 (YTÜ Senato denkliği)
   - **PTE Academic:** En az 55
   - *Not:* Başka devlet veya vakıf üniversitelerinin hazırlık muafiyet sınavları YTÜ'de geçerli **DEĞİLDİR**. Yalnızca uluslararası akredite sınavlar ve YTÜ İYS geçerlidir.
"""
    )

    # Kurlar, Ders İçerikleri, Hedefler
    write_file(
        "03_yabanci_diller_yuksekokulu_ybd/kurlar_ders_icerikleri_hedefler.md",
        """---
baslik: "YBD Kurlar, Ders İçerikleri ve Program Amaçları"
kaynak_url: "https://ybd.yildiz.edu.tr/temel-ingilizce/duzeyler-ders-icerikleri-program-amaclari"
kategori: "kurlar_ve_icerik"
anahtar_kelimeler: ["a1 kuru", "a2 kuru", "b1 kuru", "b2 kuru", "c1 kuru", "haftalık ders saati", "cefr"]
---

# YBD Kurlar, Ders İçerikleri ve Düzey Amaçları

> [!NOTE] Özet
> Temel İngilizce Bölümü'nde eğitim, Avrupa Ortak Dil Kriterleri (CEFR) standardına göre A1 (Başlangıç), A2 (Temel), B1 (Orta Öncesi), B2 (Orta) ve C1 (İleri) olmak üzere 5 kur düzeyinde yürütülür.

## Düzeyler ve Haftalık Ders Saatleri

### 1. A1 Düzeyi (Beginner / Elementary)
- **Haftalık Ders Saati:** 24 - 26 saat
- **Hedef:** Günlük temel ifadeleri anlama, kendini ve ailesini tanıtma, basit sorular sorma ve yanıtlama.
- **Odak:** Temel dilbilgisi yapıları, temel sözcük dağarcığı, fonetik ve telaffuz, basit paragraf yazımı.

### 2. A2 Düzeyi (Pre-Intermediate)
- **Haftalık Ders Saati:** 22 - 24 saat
- **Hedef:** Sık kullanılan ifadeleri kavrama, tanıdık konularda basit ve doğrudan bilgi alışverişi yapma, geçmişi ve yakın çevresini anlatma.
- **Odak:** Zamanlar, bağlaçlar, kısa okuma metinleri analizi, fikir belirten kısa paragraflar (Opinion Paragraph).

### 3. B1 Düzeyi (Intermediate)
- **Haftalık Ders Saati:** 20 - 22 saat
- **Hedef:** İşte, okulda ve serbest zamanda karşılaşılan konuların ana fikirlerini kavrama; olayları, deneyimleri, hayalleri ve hedefleri betimleme.
- **Odak:** Karmaşık cümle yapıları, akademik okuma stratejileri (skimming, scanning), kompozisyon yapısına giriş (Cause & Effect, Compare & Contrast).

### 4. B2 Düzeyi (Upper-Intermediate)
- **Haftalık Ders Saati:** 18 - 20 saat
- **Hedef:** Soyut ve somut konulardaki karmaşık metinlerin ana fikirlerini kavrama; akıcı ve spontane iletişim kurma; bir konuda avantaj ve dezavantajları sunabilme.
- **Odak:** Akademik dinleme ve not alma (Note-taking), akademik essay yazımı (Opinion Essay, Argumentative Essay), eleştirel okuma.

### 5. C1 Düzeyi (Advanced)
- **Haftalık Ders Saati:** 16 - 18 saat
- **Hedef:** Uzun ve zorlu metinleri kavrama ve örtük anlamları sezebilme; dili toplumsal, akademik ve mesleki amaçlar için esnek ve etkin kullanabilme.
- **Odak:** Araştırma raporu yazımı, akademik tartışma ve sunum teknikleri, İYS hazırlığı.
"""
    )

    # Scrape 46 SSS items from YBD
    print("Scraping 46 SSS from YBD...")
    soup_ybd_sss = get_soup("https://ybd.yildiz.edu.tr/temel-ingilizce/sikca-sorulan-sorular")
    ybd_sss_content = """---
baslik: "YBD Sıkça Sorulan Sorular (46 Madde Tam Metin)"
kaynak_url: "https://ybd.yildiz.edu.tr/temel-ingilizce/sikca-sorulan-sorular"
kategori: "ybd_sss"
anahtar_kelimeler: ["ybd sss", "devamsızlık", "kitap", "iys", "sağlık raporu", "beklemeli öğrenci", "kur geçme"]
---

# YBD Sıkça Sorulan Sorular (Eksiksiz Resmi Kılavuz)

> [!NOTE] Özet
> Aşağıda Yabancı Diller Yüksekokulu resmi web sitesindeki 46 sorunun tamamı, devamsızlık hesaplamaları, sağlık raporu prosedürleri, İYS kuralları ve kur atlama şartları yer almaktadır.

"""
    # parse strong tags with questions
    strong_tags = soup_ybd_sss.find_all('strong')
    q_num = 1
    for st in strong_tags:
        t = st.get_text(strip=True)
        if re.match(r'^\d+\.', t):
            # next elements are the answer
            ans_parts = []
            curr = st.parent.find_next_sibling()
            while curr and not curr.find('strong', text=re.compile(r'^\d+\.')):
                txt = curr.get_text(' ', strip=True)
                if txt:
                    ans_parts.append(txt)
                curr = curr.find_next_sibling()
                if curr and curr.name in ['h1', 'h2', 'h3']:
                    break
            ans_text = "\n\n".join(ans_parts) if ans_parts else "İlgili YBD yönergesine bakınız."
            ybd_sss_content += f"### {t}\n\n**Cevap:**\n{ans_text}\n\n---\n\n"
            q_num += 1

    write_file("03_yabanci_diller_yuksekokulu_ybd/sikca_sorulan_sorular.md", ybd_sss_content)

    # Sınav ve Değerlendirme Kuralları
    write_file(
        "03_yabanci_diller_yuksekokulu_ybd/sinav_ve_degerlendirme_kurallari.md",
        """---
baslik: "YBD Sınav ve Başarı Değerlendirme Esasları"
kategori: "ybd_sinavlar"
anahtar_kelimeler: ["kur başarı notu", "portfolyo", "writing", "speaking", "iys barajı", "devamsızlık sınırı %85"]
---

# YBD Sınav ve Başarı Değerlendirme Esasları

> [!NOTE] Özet
> Hazırlık sınıfında her kurun başarı notu yarıyıl içi etkinlikler (Vize, Kısa Sınav/Quiz, Writing Task, Speaking Task, Ödev/Portfolyo) ile belirlenir. Derse devam oranı en az **%85** olmak zorundadır.

## Devamsızlık ve Sınav İlişkisi
- **Devam Zorunluluğu:** Öğrenciler kayıtlı oldukları kurun toplam ders saatlerinin en az **%85'ine** devam etmekle yükümlüdür (%15 devamsızlık hakkı).
- **Sağlık Raporu:** Sağlık raporları devamsızlık süresinden **DÜŞMEZ**. Raporlu olunan günler devamsızlık sayılır; ancak mazeret vize sınavına girmek için rapor sunulabilir.
- **F0 Durumu:** Devamsızlık sınırını aşan öğrenci F0 ile kalır, yarıyıl içindeki kalan sınavlara ve o yarıyıl sonundaki İYS'ye **GİREMEZ**.

## Kur Geçme ve İYS'ye Girme Şartları
- Her kur sonunda öğrencinin Kur Başarı Notu (KBN) hesaplanır (Vize %30, Quizler %20, Writing/Speaking %30, Portfolyo %20).
- KBN ortalaması **60.00 ve üzeri** olan öğrenci bir üst kura geçer.
- Bahar yarıyılı sonunda B2 veya C1 kurunu başarıyla tamamlayan veya belirlenen başarı barajını aşan öğrenciler Haziran ayındaki İYS sınavına girme hakkı kazanır.

## İYS Puanı ve Fakülteye Geçiş
- İYS'den **60 ve üzeri** alan lisans öğrencileri başarılı sayılarak bölümlerine geçerler.
"""
    )

    # Sınavlarda Uyulacak Kurallar
    write_file(
        "03_yabanci_diller_yuksekokulu_ybd/sinavlarda_uyulacak_kurallar.md",
        """---
baslik: "YBD Sınavlarda Uyulması Zorunlu Kurallar"
kaynak_url: "https://ybd.yildiz.edu.tr/ogrenci/sinavlarda-uyulmasi-zorunlu-kurallar"
kategori: "sinav_disiplini"
anahtar_kelimeler: ["sınav salonu", "kimlik kontrolü", "akıllı saat", "cep telefonu", "optik form", "kopya"]
---

# YBD Sınavlarda Uyulması Zorunlu Kurallar

> [!NOTE] Özet
> İYS, DBS ve kur sınavlarında öğrencilerin kimlik belgesi bulundurması, cep telefonu ve akıllı cihazları tamamen kapatması ve optik form kodlamasını doğru yapması zorunludur.

## Sınav Salonuna Giriş ve Kimlik
1. Öğrenciler sınav başlamadan en az **15 dakika önce** sınav salonunda hazır bulunmalıdır.
2. Sınava girebilmek için fotoğraflı ve onaylı **YTÜ Öğrenci Kimlik Kartı** veya geçerli **T.C. Kimlik Kartı / Pasaport** bulundurulması zorunludur. Kimliksiz öğrenci sınava alınmaz.
3. Sınavın ilk 30 dakikası ve son 15 dakikası içinde salondan çıkmak yasaktır.

## Yasak Eşyalar ve Cihazlar
- Sınav salonuna cep telefonu, akıllı saat, kablosuz kulaklık, programlanabilir hesap makinesi ve her türlü elektronik iletişim aygıtı ile girilmesi kesinlikle yasaktır. Cihazlar gözetmenin belirleyeceği alana kapalı konumda bırakılır.
- Masada sadece kimlik, kurşun kalem, silgi ve şeffaf şişede su bulundurulabilir.

## Optik Form ve Cevap Kağıdı
- Soru kitapçığı üzerindeki cevaplar optik forma aktarılmalıdır. Optik forma işaretlenmeyen cevaplar değerlendirmeye alınmaz.
- Kitapçık türü, öğrenci numarası ve ad-soyad kodlamasındaki hatalardan tamamen öğrenci sorumludur.

## Kopya ve Yaptırımlar
- Kopya çeken, çekmeye teşebbüs eden veya kopya veren öğrenci hakkında tutanak tutularak 2547 sayılı Kanun Madde 54 uyarınca **bir veya iki yarıyıl uzaklaştırma cezası** istemiyle derhal disiplin soruşturması başlatılır.
"""
    )

    # ornek_sinavlar_ve_iys / README ve detaylar
    write_file(
        "03_yabanci_diller_yuksekokulu_ybd/ornek_sinavlar_ve_iys/README.md",
        """---
baslik: "YBD Örnek Sınavlar ve İYS Arşivi Rehberi"
kaynak_url: "https://ybd.yildiz.edu.tr/ogrenci/sinav-ornekleri"
kategori: "iys_ornekleri"
anahtar_kelimeler: ["iys oturum 1", "iys oturum 2", "listening", "note-taking", "writing rubrik", "erasmus", "iaeste", "p-epe"]
---

# YBD İngilizce Yeterlik Sınavı (İYS) ve Örnek Sınavlar Arşivi

> [!NOTE] Özet
> İYS, iki ayrı oturumdan oluşan 100 puanlık kapsamlı bir akademik İngilizce yeterlik sınavıdır. Orijinal sınav kağıtları, cevap anahtarları ve dinleme metinleri `arsiv/ybd_belgeleri/` dizininde saklanmaktadır.

## Sınav Formatı ve Oturumlar

| Oturum | Bölüm | Süre | Soru Sayısı / Format | Ağırlık |
|---|---|---|---|---|
| **1. Oturum** | Reading & Use of English | ~90 dk | Paragraf tamamlama, okuduğunu anlama, çoktan seçmeli | %50 |
| **2. Oturum (Listening)** | Note-Taking & While-Listening | ~40 dk | Akademik ders dinleme, not alma ve soruları yanıtlama | %25 |
| **2. Oturum (Writing)** | Academic Essay Writing | ~45 dk | 250-300 kelimelik akademik kompozisyon (Opinion / Argumentative) | %25 |

## Bu Bölümün İçeriği
- [İYS 1. Oturum Örnek Analizi](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/03_yabanci_diller_yuksekokulu_ybd/ornek_sinavlar_ve_iys/iys_sample_session_1.md): Okuma parçaları soru tipleri ve cevap anahtarı analizi.
- [İYS 2. Oturum Dinleme ve Not Alma](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/03_yabanci_diller_yuksekokulu_ybd/ornek_sinavlar_ve_iys/iys_sample_session_2.md): Note-Taking yöntemi, script dökümleri ve soru formatları.
- [İYS Essay Yazım Kriterleri ve Rubrik](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/03_yabanci_diller_yuksekokulu_ybd/ornek_sinavlar_ve_iys/iys_writing_kriterleri.md): Task Achievement, Coherence, Lexical Resource ve Grammatical Range değerlendirme puanları.
- [Erasmus, IAESTE ve Lisansüstü (P-EPE) Sınavları](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/03_yabanci_diller_yuksekokulu_ybd/ornek_sinavlar_ve_iys/iys_erasmus_ve_lisansustu.md): Değişim programları ve yüksek lisans/doktora yabancı dil sınav formatları.
"""
    )

    write_file(
        "03_yabanci_diller_yuksekokulu_ybd/ornek_sinavlar_ve_iys/iys_sample_session_1.md",
        """---
baslik: "İYS 1. Oturum Örnek Sınav Analizi"
arsivlenmis_dosya: "arsiv/ybd_belgeleri/Session_I_(Sample_EPE.pdf"
kategori: "iys_ornekleri"
anahtar_kelimeler: ["session 1", "reading comprehension", "vocabulary", "close test"]
---

# İYS 1. Oturum: Reading & Language Use

**Orijinal Belge:** `arsiv/ybd_belgeleri/Session_I_(Sample_EPE.pdf` ve `Sample_EPE-Answer_Key_(Session_I_&_Session_II).pdf`

## Soru Tipleri ve Kapsam
1. **Academic Reading Comprehension (2-3 Uzun Metin):**
   - Popüler bilim, psikoloji, tarih veya çevre konulu 700-1000 kelimelik akademik makaleler.
   - Ana fikir bulma (Main Idea), referans zamirleri çıkarma (Reference Words), kelime anlamı çıkarma (Context Clues), çıkarım yapma (Inference).
2. **Text Completion / Sentence Insertion:**
   - Metin akışını bozan cümleyi bulma veya boş bırakılan yere en uygun cümleyi yerleştirme.
3. **Vocabulary & Collocations:**
   - Akademik kelime listesi (AWL) kelimeleri ve edat kalıpları.
"""
    )

    write_file(
        "03_yabanci_diller_yuksekokulu_ybd/ornek_sinavlar_ve_iys/iys_sample_session_2.md",
        """---
baslik: "İYS 2. Oturum Dinleme ve Not Alma (Listening & Note-Taking)"
arsivlenmis_dosyalar: ["arsiv/ybd_belgeleri/Session_II_(Sample_EPE).pdf", "arsiv/ybd_belgeleri/Listening_Scripts_(Session_II-Sample_EPE).pdf"]
kategori: "iys_ornekleri"
anahtar_kelimeler: ["listening", "note-taking", "listening script", "dinleme sınavı"]
---

# İYS 2. Oturum: Dinleme ve Not Alma (Note-Taking)

**Orijinal Belgeler:** 
- `arsiv/ybd_belgeleri/Session_II_(Sample_EPE).pdf`
- `arsiv/ybd_belgeleri/Listening_Scripts_(Session_II-Sample_EPE).pdf`
- `arsiv/ybd_belgeleri/Note-Taking_Questions_(Session_II-Sample_EPE).pdf`

## Sınav Süreci
1. **Not Alma Aşaması:** Öğrencilere boş not kağıdı dağıtılır. Yaklaşık 8-12 dakikalık akademik ders anlatımı (Lecture) dinletilir. Öğrenciler bu sırada anahtar noktaları, neden-sonuç ilişkilerini ve örnekleri not alırlar.
2. **Soru Cevaplama Aşaması:** Dinleme bittikten sonra soru kitapçığı dağıtılır. Öğrenciler aldıkları notları kullanarak açık uçlu veya çoktan seçmeli soruları belirlenen süre içinde yanıtlarlar.
"""
    )

    write_file(
        "03_yabanci_diller_yuksekokulu_ybd/ornek_sinavlar_ve_iys/iys_writing_kriterleri.md",
        """---
baslik: "İYS Academic Essay Yazım Formatı ve Değerlendirme Kriterleri"
arsivlenmis_dosya: "arsiv/ybd_belgeleri/Sample_EPE_Writing_&_Essay_Writing_Criteria.pdf"
kategori: "iys_writing"
anahtar_kelimeler: ["writing rubrik", "opinion essay", "argumentative essay", "thesis statement", "250 kelime"]
---

# İYS Essay Yazım Kriterleri ve Rubrik

**Orijinal Belge:** `arsiv/ybd_belgeleri/Sample_EPE_Writing_&_Essay_Writing_Criteria.pdf`

## Essay Formatı ve Beklentiler
- **Uzunluk:** 250 - 350 kelime arası 4 veya 5 paragraflık kompozisyon.
- **Standart Yapı:**
  1. **Introduction:** Hook (Giriş), Background Information (Genel Bilgi), Thesis Statement (Açık ve net tez cümlesi).
  2. **Body Paragraph 1:** Topic Sentence + Supporting Ideas + Specific Examples.
  3. **Body Paragraph 2:** İkinci argüman + Destekleyici açıklamalar.
  4. **(Opsiyonel) Counter-Argument & Refutation:** Karşıt görüş ve çürütme.
  5. **Conclusion:** Restatement of Thesis (Tezin yeniden ifadesi), Summary of main points, Final thought.

## 4 Temel Değerlendirme Kriteri (Her biri 25 Puan)
1. **Task Achievement & Content (Görev Başarımı):** Konuya tam odaklanma, argümanları somut ve mantıklı geliştirebilme.
2. **Coherence & Cohesion (Tutarlılık ve Bağlantı):** Paragraflar arası mantıklı geçişler, bağlaçların (Furthermore, However, On the other hand) doğru kullanımı.
3. **Lexical Resource (Sözcük Çeşitliliği):** Zengin ve akademik kelime hazinesi, tekrar etmeyen kelimeler.
4. **Grammatical Range & Accuracy (Gramer Doğruluğu):** Karmaşık cümle yapıları (Relative clauses, passives, conditionals) ve hatasız noktalama/yazım.
"""
    )

    write_file(
        "03_yabanci_diller_yuksekokulu_ybd/ornek_sinavlar_ve_iys/iys_erasmus_ve_lisansustu.md",
        """---
baslik: "Erasmus, IAESTE ve Lisansüstü (P-EPE) Sınav Formatları"
arsivlenmis_dosyalar: ["arsiv/ybd_belgeleri/ERASMUS_EXAM_SAMPLE-1.pdf", "arsiv/ybd_belgeleri/IAESTE_ENGLISH_EXAM_SAMPLE-1.pdf", "arsiv/ybd_belgeleri/Postgraduate_English_Proficiency_Exam_(P-EPE).pdf"]
kategori: "diger_sinavlar"
anahtar_kelimeler: ["erasmus sınavı", "iaeste", "p-epe", "lisansüstü ingilizce sınavı"]
---

# Erasmus, IAESTE ve Lisansüstü Dil Sınavları

## 1. Erasmus Yabancı Dil Sınavı
- **Amaç:** Avrupa öğrenci değişim programlarına başvuracak öğrencilerin yabancı dil seviyesini belirler.
- **Baraj Puan:** Çoğu bölüm için en az 50 veya 60; ikili anlaşma yapılan bazı yabancı üniversiteler için 70 veya B2 düzeyidir.
- **İçerik:** Çoktan seçmeli okuma, dilbilgisi, kelime ve dinleme soruları içerir.

## 2. Postgraduate English Proficiency Exam (P-EPE)
- **Amaç:** YTÜ Fen Bilimleri ve Sosyal Bilimler Enstitülerine yüksek lisans ve doktora başvurusu yapacak adayların yabancı dil yeterliğini ölçer.
- **Baraj Puan:** Tezli yüksek lisans için en az 60, Doktora programları için en az 65 puandır.
"""
    )

    print("03_yabanci_diller_yuksekokulu_ybd completed successfully!")

if __name__ == '__main__':
    generate_ybd()
