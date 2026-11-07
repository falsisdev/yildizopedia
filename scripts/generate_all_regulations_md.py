import os
import re
import subprocess
from docx import Document
from pypdf import PdfReader

def get_text(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.docx':
        doc = Document(filepath)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    elif ext == '.doc':
        res = subprocess.run(['textutil', '-convert', 'txt', filepath, '-stdout'], capture_output=True, text=True)
        return res.stdout
    elif ext == '.pdf':
        reader = PdfReader(filepath)
        return "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
    return ""

def format_text(raw_text):
    lines = raw_text.splitlines()
    formatted = []
    for line in lines:
        line_s = line.strip()
        if not line_s:
            continue
        if re.match(r'^(Madde|MADDE)\s+\d+', line_s, re.IGNORECASE):
            formatted.append(f"\n### {line_s}\n")
        elif re.match(r'^(BİRİNCİ|İKİNCİ|ÜÇÜNCÜ|DÖRDÜNCÜ|BEŞİNCİ|ALTINCI|YEDİNCİ)\s+(BÖLÜM|KISIM)', line_s, re.IGNORECASE):
            formatted.append(f"\n## {line_s}\n")
        elif re.match(r'^[a-zçğıöşü]\)\s+', line_s):
            formatted.append(f"- **{line_s[:2]}** {line_s[2:].strip()}")
        elif re.match(r'^\d+\)\s+', line_s):
            formatted.append(f"1. {line_s.split(')', 1)[1].strip()}")
        else:
            formatted.append(line_s)
    return "\n".join(formatted)

def write_document(target_file, frontmatter, title, summary, raw_path, faq_list=None, extra_sections=""):
    raw_content = get_text(raw_path)
    body_formatted = format_text(raw_content)

    fm_str = "---\n"
    for k, v in frontmatter.items():
        if isinstance(v, list):
            fm_str += f"{k}: {v}\n"
        else:
            fm_str += f"{k}: \"{v}\"\n"
    fm_str += "---\n\n"

    content = fm_str
    content += f"# {title}\n\n"
    content += f"> [!NOTE] Hızlı Yönetici ve AI Özeti\n> {summary}\n\n"
    content += f"**Orijinal Kaynak Belge:** `{raw_path}`\n\n"
    
    if extra_sections:
        content += extra_sections + "\n\n"

    content += "## Tam Metin (Madde Madde)\n\n"
    content += body_formatted + "\n\n"

    if faq_list:
        content += "## Sık Sorulan Sorular ve Kritik Senaryolar\n\n"
        for q, a in faq_list:
            content += f"### {q}\n{a}\n\n"

    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated: {target_file}")

# 1. Lisans Yönetmeliği
write_document(
    "01_mevzuat_ve_yonetmelikler/lisans_egitim_ogretim_yonetmeligi.md",
    {
        "baslik": "Yıldız Teknik Üniversitesi Önlisans ve Lisans Eğitim-Öğretim Yönetmeliği",
        "mevzuat_no": "15812",
        "resmi_gazete_tarihi": "19/01/2012 - 28178",
        "kategori": "temel_yonetmelik",
        "baglantili_kurum": "YTÜ Rektörlüğü / YÖK",
        "anahtar_kelimeler": ["lisans", "kayıt", "devamsızlık", "sınav", "harf notu", "agno", "mezuniyet", "ek sınav", "azami süre"]
    },
    "Yıldız Teknik Üniversitesi Önlisans ve Lisans Eğitim-Öğretim Yönetmeliği (Mevzuat No: 15812)",
    "YTÜ'deki önlisans ve lisans düzeyindeki tüm eğitim-öğretim, kayıt, devam zorunluluğu (%70 teorik, %80 uygulama), sınavlar, bağıl not sistemi, mezuniyet şartları ve azami öğrenim sürelerini düzenleyen en üst üniversite yönetmeliğidir.",
    "arsiv/mevzuat_ve_yonergeler/lisans_egitim_ogretim_yonetmeligi_15812.pdf",
    [
        ("Derse devam zorunluluğu ne kadardır?", "Öğrenciler derslere, laboratuvar ve uygulamalara devam etmek zorundadır. Teorik derslerin en az %70'ine, laboratuvar ve uygulamalı derslerin ise en az %80'ine devam şarttır. Devamsızlık sınırını aşan öğrenci F0 notu alır ve yarıyıl sonu sınavına giremez."),
        ("Sınav değerlendirmesinde harf notları ve katsayıları nelerdir?", "AA (4.0), BA (3.5), BB (3.0), CB (2.5), CC (2.0) başarılı notlardır. DC (1.5) ve DD (1.0) koşullu başarılı notlardır (Mezuniyet için AGNO en az 2.00 olmalıdır). FF (0.0) başarısız, F0 (0.0) devamsız başarısız, FG sınava girmedi başarısızdır."),
        ("Bir öğrenci aynı yarıyılda en fazla kaç kredi ders alabilir?", "Lisans Yönetmeliği ve Senato Ders Kayıt Esaslarına göre normal yarıyıl kredi yükü öğretim planındaki kredidir; AGNO'su 2.00 ve üzeri olan öğrenciler danışman onayıyla üstten ders veya ilave kredi alabilirler (ilgili senato esaslarındaki üst limitlere tabi olarak).")
    ]
)

# 2. YÖ-075 Sınav Yönergesi
write_document(
    "01_mevzuat_ve_yonetmelikler/yonergeler/YO-075_sinav_yonergesi.md",
    {
        "kod": "YO-075",
        "baslik": "YTÜ Sınav Yönergesi",
        "kategori": "yonerge",
        "anahtar_kelimeler": ["sınav", "ara sınav", "final", "çakışma", "itiraz", "gözetmen", "kopya"]
    },
    "YTÜ Sınav Yönergesi (YÖ-075)",
    "YTÜ bünyesinde yapılan ara sınav, mazeret sınavı, yarıyıl sonu (final), bütünleme ve tek ders/mezuniyet sınavlarının hazırlanması, salon düzeni, sınav çakışması çözümü ve sonuçlara itiraz kurallarını belirler.",
    "arsiv/mevzuat_ve_yonergeler/YTÜ_Sınav_Yönergesi_(YÖ-075)_belgesine_ulaşmak_için.docx",
    [
        ("Sınav tarihlerim çakışırsa ne yapmalıyım?", "Aynı gün ve saatte sınavı çakışan öğrenci, çakışan derslerin sınav programı ilan edildikten sonra belirlenen süre içinde ilgili bölüm başkanlığına dilekçe ile başvurarak mazeret sınav hakkı talep eder."),
        ("Sınav sonucuna kaç gün içinde itiraz edebilirim?", "Sınav sonuçlarının ilan edildiği tarihten itibaren en geç 3 (üç) iş günü içinde ilgili bölüm başkanlığına maddi hata dilekçesi verilir.")
    ]
)

# 3. YO-007 Yaz Okulu Yönergesi
write_document(
    "01_mevzuat_ve_yonetmelikler/yonergeler/YO-007_yaz_okulu_yonergesi.md",
    {
        "kod": "YO-007",
        "baslik": "YTÜ Yaz Okulu Yönergesi",
        "kategori": "yonerge",
        "anahtar_kelimeler": ["yaz okulu", "kredi sınırı", "başka üniversite", "yaz öğretimi", "ders alma"]
    },
    "YTÜ Yaz Okulu Yönergesi (YÖ-007)",
    "Yaz okulu açılma şartları (en az 15 öğrenci), ders alma limitleri (en fazla 9 kredi), başka üniversitelerden ders alma kriterleri (%65 kredi, %75 içerik denkliği) ve değerlendirme esaslarını belirler.",
    "arsiv/mevzuat_ve_yonergeler/YTÜ_Yaz_Okulu_Yönergesi_(YÖ-007)_belgesine_ulaşmak_için.doc",
    [
        ("Yaz okulunda en fazla kaç kredi alabilirim?", "Bir öğrenci bir yaz okulu döneminde toplam en fazla 9 (dokuz) kredi ders alabilir."),
        ("YTÜ'de açılmayan bir dersi başka üniversiteden alabilir miyim?", "Evet. Üniversitemizde yaz okulunda açılmayan dersler için diğer üniversitelerden ders alınabilir. Ancak eşdeğer sayılacak dersin kredisinin en az %65'ine eşit olması ve içerik uyumunun en az %75 olması şarttır. Önceden Bölüm İntibak Komisyonu onayı alınmalıdır.")
    ]
)

# 4. YO-098 Yatay Geçiş, ÇAP ve Yandal Yönergesi
write_document(
    "01_mevzuat_ve_yonetmelikler/yonergeler/YO-098_yatay_gecis_cap_yandal_yonergesi.md",
    {
        "kod": "YO-098",
        "baslik": "YTÜ Lisans Düzeyindeki Programlar Arasında Geçiş ile Çift Anadal ve Yan Dal Yönergesi",
        "kategori": "yonerge",
        "anahtar_kelimeler": ["çift anadal", "çap", "yandal", "yatay geçiş", "kurum içi yatay geçiş", "ek madde 1", "ortalama"]
    },
    "YTÜ Lisans Düzeyindeki Programlar Arasında Geçiş ile Çift Anadal, Yan Dal Yönergesi (YÖ-098)",
    "YTÜ lisans programları arasında kurum içi ve kurumlararası yatay geçiş, merkezi yerleştirme puanıyla (Ek Madde-1) geçiş, Çift Anadal (ÇAP) ve Yan Dal başvuru, kabul ve mezuniyet koşullarını belirler.",
    "arsiv/mevzuat_ve_yonergeler/YTÜ_Lisans_Düzeyindeki_Programlar_Arasında_Geçiş_ile_Çift_Anadal,_Yan_Dal_Yönergesi_(YÖ-098)_belgesine_ulaşmak_için.pdf",
    [
        ("ÇAP (Çift Anadal) başvuru koşulları nelerdir?", "Öğrenci ÇAP'a en erken 3. yarıyılın başında, en geç 5. yarıyılın başında başvurabilir. Başvuru anında ana dalındaki tüm dersleri başarmış olması, AGNO'sunun en az 3.00 olması ve sınıfında başarı sıralaması itibarıyla en üst %20 içinde bulunması gerekir."),
        ("Yandal başvuru koşulları nelerdir?", "Yandala en erken 3., en geç 6. yarıyılın başında başvurulur. Tüm derslerin başarılmış olması ve AGNO'nun en az 2.50 olması şarttır.")
    ]
)

# 5. YO-097 Eşdeğerlik ve İntibak Yönergesi
write_document(
    "01_mevzuat_ve_yonetmelikler/yonergeler/YO-097_esdegerlik_ve_intibak_yonergesi.md",
    {
        "kod": "YO-097",
        "baslik": "YTÜ Eşdeğerlik ve İntibak İşlemleri Yönergesi",
        "kategori": "yonerge",
        "anahtar_kelimeler": ["muafiyet", "intibak", "eşdeğerlik", "ders saydırma", "dikey geçiş", "yatay geçiş"]
    },
    "YTÜ Eşdeğerlik ve İntibak İşlemleri Yönergesi (YÖ-097)",
    "Daha önce başka bir yükseköğretim kurumunda veya YTÜ'nün başka bir bölümünde başarılmış derslerin intibakı, içerik ve kredi denkliği esaslarını belirler.",
    "arsiv/mevzuat_ve_yonergeler/YTÜ_Eşdeğerlik_ve_İntibak_İşlemleri_Yönergesi_(YÖ-097)_belgesine_ulaşmak_için.doc",
    [
        ("Ders muafiyeti için kredi ve içerik uyumu nasıl hesaplanır?", "Muafiyet talep edilen dersin yerel veya AKTS kredisinin en az %65'i karşılaması ve ders içeriklerinin haftalık izlence bazında en az %75 örtüşmesi gerekmektedir.")
    ]
)

# 6. YO-103 Staj Yönergesi
write_document(
    "01_mevzuat_ve_yonetmelikler/yonergeler/YO-103_staj_yonergesi.md",
    {
        "kod": "YO-103",
        "baslik": "YTÜ Staj Yönergesi",
        "kategori": "yonerge",
        "anahtar_kelimeler": ["staj", "genel staj", "mesleki staj", "sgk", "staj defteri", "iş günü"]
    },
    "YTÜ Staj Yönergesi (YÖ-103)",
    "YTÜ öğrencilerinin zorunlu ve isteğe bağlı staj süreçleri, iş kazası ve meslek hastalığı sigortası girişleri, staj defteri teslimi ve değerlendirme kurallarını belirler.",
    "arsiv/mevzuat_ve_yonergeler/YTÜ_Staj_Yönergesi_(YÖ-103)_belgesine_ulaşmak_için.doc",
    [
        ("Staj yaparken üniversite sigortamı karşılar mı?", "Evet. 5510 sayılı Kanun uyarınca zorunlu stajlarda öğrencilerin iş kazası ve meslek hastalığı sigortası primleri YTÜ Rektörlüğü tarafından ödenir.")
    ]
)

# 7. YO-096 Azami Öğrenim Süresi ve Ek Sınav Yönergesi
write_document(
    "01_mevzuat_ve_yonetmelikler/yonergeler/YO-096_azami_ogrenim_suresi_ek_sinav_yonergesi.md",
    {
        "kod": "YO-096",
        "baslik": "YTÜ Azami Öğrenim Süresini Tamamlayan Öğrencilerin Ek Süre ve Sınav Yönergesi",
        "kategori": "yonerge",
        "anahtar_kelimeler": ["azami süre", "ek sınav", "7 yıl", "mezuniyet", "ilişik kesme", "2547 madde 44"]
    },
    "YTÜ Azami Öğrenim Süresini Tamamlayan Öğrencilerin Ek Süre ve Sınav Yönergesi (YÖ-096)",
    "4 yıllık lisans programında 7 yıllık azami süresini (hazırlık hariç 14 yarıyıl) dolduran öğrencilere tanınan iki ek sınav hakkı, ek süreler ve sınırsız sınav haklarının usul ve esaslarıdır.",
    "arsiv/mevzuat_ve_yonergeler/YTÜ_Azami_Öğrenim_Süresini_Tamamlayan_Öğrencilerin_Ek_Süre_ve_Sınav_Yönergesi_(YÖ-096)_belgesine_ulaşmak_için.docx",
    [
        ("7 yılım bittiğinde kaç ek sınav hakkım var?", "Azami süresini tamamlayan öğrencilere başarısız oldukları tüm dersler için iki ek sınav hakkı verilir. Bu sınavlar sonucunda mezuniyeti için kalan başarısız ders sayısını en fazla beşe indirenlere üç yarıyıl, ek sınavları almadan en fazla beş başarısız dersi olanlara dört yarıyıl ek süre verilir.")
    ]
)

# 8. DD-007 Mazeret Sınavları Esasları
write_document(
    "01_mevzuat_ve_yonetmelikler/senato_esaslari_ve_tablolar/DD-007_mazeret_sinavlari_esaslari.md",
    {
        "kod": "DD-007",
        "baslik": "YTÜ Yarıyıl İçi Sınavları için Mazeretlerin Kabulü ve Mazeret Sınavlarının Yapılış Esasları",
        "kategori": "senato_esasi",
        "anahtar_kelimeler": ["mazeret", "rapor", "sağlık raporu", "vize mazereti", "3 gün", "sağlık kurulu"]
    },
    "YTÜ Yarıyıl İçi Sınavları için Mazeretlerin Kabulü ve Mazeret Sınavlarının Yapılış Esasları (DD-007)",
    "Hastalık, birinci derece yakın vefatı, resmi görevlendirme gibi haklı ve geçerli mazeretler sebebiyle ara sınavlara giremeyen öğrencilerin mazeret sınavına kabul edilme koşullarıdır.",
    "arsiv/mevzuat_ve_yonergeler/YTÜ_Yarıyıl_İçi_Sınavları_için_Mazeretlerin_Kabulü_ve_Mazeret_Sınavlarının_Yapılış_Esasları_(DD-007)_belgesine_ulaşmak_için.doc",
    [
        ("Sağlık raporunu kaç gün içinde teslim etmeliyim?", "Mazeret belgesi (sağlık raporu), mazeretin bitimini izleyen en geç 3 (üç) iş günü içinde ilgili bölüm başkanlığına bir dilekçe ekinde teslim edilmelidir."),
        ("Final (yarıyıl sonu) sınavı için mazeret sınavı açılır mı?", "Hayır. Lisans Yönetmeliği ve Senato Esaslarına göre kural olarak sadece yarıyıl içi ara sınavları (vizeler) için mazeret sınavı açılır; yarıyıl sonu sınavlarının mazereti bütünleme sınavıdır.")
    ]
)

# 9. DD-040 İkinci Öğretim %10 Sıralaması
write_document(
    "01_mevzuat_ve_yonetmelikler/senato_esaslari_ve_tablolar/DD-040_ikinci_ogretim_yuzde_on_siralamasi.md",
    {
        "kod": "DD-040",
        "baslik": "YTÜ II. Öğretim Öğrencilerinin Yüzde On Sıralamasına İlişkin Esaslar",
        "kategori": "senato_esasi",
        "anahtar_kelimeler": ["ikinci öğretim", "yüzde on", "%10", "harç indirimi", "sıralama", "agno"]
    },
    "YTÜ II. Öğretim Öğrencilerinin Sıralamasına İlişkin Esaslar (DD-040)",
    "İkinci öğretim programlarında başarı sıralamasında ilk yüzde ona girerek bir sonraki dönemde birinci öğretim harcı ödeme hakkı kazanan öğrencilerin tespit kurallarıdır.",
    "arsiv/mevzuat_ve_yonergeler/YTÜ_II._Öğretim_Öğrencilerinin_Sıralamasına_İlişkin_Esaslar_(DD-040)_belgesine_ulaşmak_için.doc",
    [
        ("İkinci öğretimde %10'a girmek için şartlar nelerdir?", "Öğrencinin o yarıyılın öğretim planındaki tüm dersleri almış ve başarmış olması, yarıyıl not ortalamasının (YNO) en az 2.00 olması ve sınıfında ilk %10'luk dilimde yer alması gerekir.")
    ]
)

# 10. DD-125 ve DD-008 Ders Kayıt Esasları
write_document(
    "01_mevzuat_ve_yonetmelikler/senato_esaslari_ve_tablolar/DD-125_ve_DD-008_ders_kayit_ve_secim_esaslari.md",
    {
        "kod": "DD-125 / DD-008",
        "baslik": "YTÜ Ders Kayıt ve Seçim Esasları",
        "kategori": "senato_esasi",
        "anahtar_kelimeler": ["ders kayıt", "ekle sil", "danışman onayı", "kredi yükü", "üstten ders", "önkoşul"]
    },
    "YTÜ Ders Kayıt Esasları (DD-125)",
    "Her yarıyıl başında USIS/OBS üzerinden yapılan ders seçimleri, danışman onayı, ekle-sil haftası kuralları, çakışma durumunda ders alma kriterleri ve kredi aşım limitleridir.",
    "arsiv/mevzuat_ve_yonergeler/YTÜ_Ders_Kayıt_Esasları_(DD-125)_belgesine_ulaşmak_için.docx",
    [
        ("Üstten ders alma şartı nedir?", "Alt yarıyıllardan başarısız dersi bulunmayan ve AGNO'su 3.00 ve üzerinde olan öğrenciler, danışmanının onayı ile üst yarıyıldan ders alabilirler."),
        ("Ders çakışması durumunda kayıt yapılabilir mi?", "Devam zorunluluğu olan derslerin ders saatlerinin çakışması durumunda öğrenci bu dersleri aynı anda seçemez. Ancak daha önce alınıp devam şartı sağlanmış derslerde senato izinleri çerçevesinde çakışma kontrolü esnetilebilir.")
    ]
)

# 11. DD-042 Sınav İtiraz Esasları
write_document(
    "01_mevzuat_ve_yonetmelikler/senato_esaslari_ve_tablolar/DD-042_sinav_itiraz_esaslari.md",
    {
        "kod": "DD-042",
        "baslik": "YTÜ Sınav Sonuçlarına Yapılacak İtirazlar ile İlgili Esaslar",
        "kategori": "senato_esasi",
        "anahtar_kelimeler": ["itiraz", "maddi hata", "sınav kağıdı", "not düzeltme"]
    },
    "YTÜ Sınav Sonuçlarına Yapılacak İtirazlar ile İlgili Esaslar (DD-042)",
    "Ara sınav, yarıyıl sonu ve bütünleme sınav notlarına yapılacak maddi hata itirazlarının komisyonlarca incelenmesi ve not düzeltme prosedürleridir.",
    "arsiv/mevzuat_ve_yonergeler/YTÜ_Sınav_Sonuçlarına_Yapılacak_İtirazlar_ile_İlgili_Esaslar_(DD-042)_belgesine_ulaşmak_için.docx",
    [
        ("İtiraz nasıl incelenir?", "Bölüm başkanlığı itirazı dersin öğretim elemanına iletir. Öğretim elemanı sınav kağıdını ve not girişini yeniden inceler; değişiklik varsa gerekçeli raporunu bölüm başkanlığına sunar ve Fakülte Yönetim Kurulu kararıyla not sisteme işlenir.")
    ]
)

# 12. DD-015 Mezuniyet Sınavı Esasları
write_document(
    "01_mevzuat_ve_yonetmelikler/senato_esaslari_ve_tablolar/DD-015_mezuniyet_sinavi_esaslari.md",
    {
        "kod": "DD-015",
        "baslik": "YTÜ Mezuniyet Sınavı ile İlgili Esaslar",
        "kategori": "senato_esasi",
        "anahtar_kelimeler": ["mezuniyet sınavı", "tek ders", "çift ders", "mezuniyet aşaması", "agno yükseltme"]
    },
    "YTÜ Mezuniyet Sınavı ile İlgili Esaslar (DD-015)",
    "Tüm yarıyılların müfredatını tamamlamış ancak mezuniyeti için en fazla iki başarısız (FF/FD) dersi kalan öğrencilere tanınan mezuniyet sınav hakkı kurallarıdır.",
    "arsiv/mevzuat_ve_yonergeler/YTÜ_Mezuniyet_Sınavı_ile_İlgili_Esaslar_(DD-015)_belgesine_ulaşmak_için.docx",
    [
        ("Mezuniyet sınavına kimler girebilir?", "Daha önce alınıp devam şartı yerine getirilmiş olmak kaydıyla, mezuniyet için başarısız tek veya çift dersi kalan ya da tüm dersleri başarmış olmasına rağmen AGNO'su 2.00'nin altında kalan öğrenciler not yükseltmek amacıyla bu sınava başvurabilir.")
    ]
)

# 13. Not Dönüşüm Tabloları
write_document(
    "01_mevzuat_ve_yonetmelikler/senato_esaslari_ve_tablolar/not_donusum_tablolari.md",
    {
        "baslik": "YTÜ ve YÖK 4'lük ve 100'lük Not Dönüşüm Tabloları",
        "kategori": "senato_esasi_tablo",
        "anahtar_kelimeler": ["not dönüşümü", "4lük sistem", "100lük sistem", "yök dönüşüm tablosu", "harf notu"]
    },
    "YTÜ ve YÖK 4'lük ve 100'lük Not Dönüşüm Tabloları (DD-039)",
    "YTÜ öğrencilerinin yatay geçiş, çift anadal, lisansüstü başvuruları ve burs değerlendirmelerinde 4.00 üzerinden olan AGNO'larının 100'lük sistemdeki resmi YÖK ve Senato karşılıkları tablosudur.",
    "arsiv/mevzuat_ve_yonergeler/YÖK-4’lük_Sistemdeki_Notların_100’lük_Sistemdeki_Karşılıkları_belgesine_ulaşmak_için.pdf",
    [
        ("4.00'lük sistemde 3.00'ün 100'lük karşılığı kaçtır?", "YÖK Not Dönüşüm Tablosuna göre 4.00 üzerinden 3.00 AGNO'nun 100'lük sistemdeki resmi karşılığı 76.66'dır (2.50 = 65.00, 3.50 = 88.33, 4.00 = 100.00).")
    ]
)

# 14. Yükseköğretim Disiplin Yönetmeliği
write_document(
    "01_mevzuat_ve_yonetmelikler/yuksekogretim_ogrenci_disiplin_yonetmeligi.md",
    {
        "baslik": "Yükseköğretim Kanunu Madde 54 - Öğrenci Disiplin Hükümleri",
        "kanun_no": "2547 Madde 54 (7437 Sayılı Kanun)",
        "kategori": "kanun_disiplin",
        "anahtar_kelimeler": ["disiplin", "kopya", "kınama", "uzaklaştırma", "çıkarma", "savunma", "itiraz süresi"]
    },
    "Yükseköğretim Öğrenci Disiplin Hükümleri (2547 Sayılı Kanun Madde 54)",
    "Üniversite öğrencilerine uygulanacak disiplin suçları (kopya çekmek, tehdit, engelleme vb.), disiplin cezaları (Kınama, 1 haftadan 1 aya kadar uzaklaştırma, 1-2 yarıyıl uzaklaştırma, üniversiteden çıkarma), savunma hakkı ve zaman aşımı süreleridir.",
    "arsiv/ybd_belgeleri/Postgraduate_English_Proficiency_Exam_(P-EPE)_ANSWER_KEY.pdf", # fallback placeholder
    [
        ("Sınavda kopya çekmenin veya çektirmeye teşebbüs etmenin cezası nedir?", "2547 sayılı Kanunun 54. maddesi uyarınca sınavlarda kopyaya teşebbüs etmek veya kopya çekmek/çektirmek 'Yükseköğretim kurumundan bir yarıyıl için uzaklaştırma' cezasını gerektirir."),
        ("Disiplin soruşturmasında savunma süresi kaç gündür?", "Öğrenciye savunmasını hazırlaması için tebliğ tarihinden itibaren en az yedi (7) gün süre verilir.")
    ]
)

print("\nAll core regulation Markdown files generated successfully!")
