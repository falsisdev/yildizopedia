import os
import re
import subprocess
from docx import Document
from pypdf import PdfReader
from scripts.generate_all_regulations_md import write_document

# Remaining Directives
write_document(
    "01_mevzuat_ve_yonetmelikler/yonergeler/YO-031_akademik_danismanlik_yonergesi.md",
    {
        "kod": "YÖ-031",
        "baslik": "YTÜ Akademik Danışmanlık Yönergesi",
        "kategori": "yonerge",
        "anahtar_kelimeler": ["danışman", "akademik danışman", "ders seçimi", "onay", "rehberlik"]
    },
    "YTÜ Akademik Danışmanlık Yönergesi (YÖ-031)",
    "Öğrencilere kayıt, ders seçimi, intibak, kariyer ve akademik gelişim süreçlerinde rehberlik edecek öğretim elemanlarının görev ve sorumluluklarıdır.",
    "arsiv/mevzuat_ve_yonergeler/YTÜ_Akademik_Danışmanlık_Yönergesi_(YÖ-031)_belgesine_ulaşmak_için.docx",
    [
        ("Danışman onayı olmadan ders kaydı geçerli olur mu?", "Hayır. Öğrencinin sistem üzerinden seçtiği dersler akademik danışmanı tarafından incelenip onaylanmadıkça ders kaydı kesinleşmez.")
    ]
)

write_document(
    "01_mevzuat_ve_yonetmelikler/yonergeler/YO-119_diploma_ve_mezuniyet_belgeleri_yonergesi.md",
    {
        "kod": "YÖ-119",
        "baslik": "YTÜ Diploma, Diploma Eki ve Mezuniyete İlişkin Belgelerin Düzenlenme Yönergesi",
        "kategori": "yonerge",
        "anahtar_kelimeler": ["diploma", "diploma eki", "geçici mezuniyet", "kayıp diploma", "ilişik kesme"]
    },
    "YTÜ Diploma, Diploma Eki ve Mezuniyete İlişkin Belgelerin Düzenlenme Yönergesi (YÖ-119)",
    "Mezuniyet hakkı kazanan öğrencilere verilecek diploma, diploma eki, geçici mezuniyet belgesi, onur/yüksek onur belgelerinin hazırlanması ve teslim esaslarıdır.",
    "arsiv/mevzuat_ve_yonergeler/YTÜ_Diploma,_Diploma_Eki_ve_Mezuniyete_İlişkin_Belgelerin_Düzenlenme_Yönergesi_(YÖ-119)_belgesine_ulaşmak_için.docx",
    [
        ("Geçici mezuniyet belgesi diplomayı alırken geri verilir mi?", "Evet. Diplomanın aslı teslim alınırken daha önce verilmiş olan Geçici Mezuniyet Belgesinin aslının iade edilmesi zorunludur.")
    ]
)

write_document(
    "01_mevzuat_ve_yonetmelikler/yonergeler/YO-014_ozel_ogrenci_yonergesi.md",
    {
        "kod": "YÖ-014",
        "baslik": "YTÜ Özel Öğrenci Yönergesi",
        "kategori": "yonerge",
        "anahtar_kelimeler": ["özel öğrenci", "misafir öğrenci", "başka üniversiteden ders alma", "kredi transferi"]
    },
    "YTÜ Özel Öğrenci Yönergesi (YÖ-014)",
    "Farklı bir yükseköğretim kurumunda kayıtlı olup YTÜ'den ders almak isteyen veya YTÜ öğrencisi olup başka bir üniversitede özel öğrenci statüsünde ders almak isteyen öğrencilerin işlemleridir.",
    "arsiv/mevzuat_ve_yonergeler/YTÜ_Özel_Öğrenci_Yönergesi_(YÖ-014)_belgesine_ulaşmak_için.doc",
    [
        ("Özel öğrenci YTÜ diploması alabilir mi?", "Hayır. Özel öğrencilik sadece ders alma hakkı verir, diploma veya derece kazandırmaz; alınan dersleri ve notları gösteren onaylı bir transkript düzenlenir.")
    ]
)

write_document(
    "01_mevzuat_ve_yonetmelikler/yonergeler/YO-088_isletmede_mesleki_egitim_yonergesi.md",
    {
        "kod": "YÖ-088",
        "baslik": "YTÜ İşletmede Mesleki Eğitim Yönergesi",
        "kategori": "yonerge",
        "anahtar_kelimeler": ["işletmede mesleki eğitim", "ime", "aday mühendislik", "sanayi işbirliği", "tam zamanlı staj"]
    },
    "YTÜ İşletmede Mesleki Eğitim Yönergesi (YÖ-088)",
    "Lisans öğrencilerinin son sınıfta bir yarıyıl boyunca tam zamanlı olarak sanayi veya araştırma kuruluşlarında çalışarak mesleki tecrübe edinmelerini düzenleyen yönergedir.",
    "arsiv/mevzuat_ve_yonergeler/YTÜ_İşletmede_Mesleki_Eğitim_Yönergesi_belgesine_ulaşmak_için.docx",
    [
        ("İME programına hangi şartlarda başvurulabilir?", "Öğrencinin 7. yarıyılın sonuna kadar olan tüm zorunlu derslerini başarmış olması ve belirlenen asgari AGNO şartını sağlaması gereklidir.")
    ]
)

write_document(
    "01_mevzuat_ve_yonetmelikler/yonergeler/YO-064_onceki_ogrenmenin_taninmasi_yonergesi.md",
    {
        "kod": "YÖ-064",
        "baslik": "YTÜ Önceki Öğrenmenin Tanınmasına İlişkin Yönerge",
        "kategori": "yonerge",
        "anahtar_kelimeler": ["önceki öğrenme", "sertifika", "yeterlilik sınavı", "akreditasyon", "muafiyet"]
    },
    "YTÜ Önceki Öğrenmenin Tanınmasına İlişkin Yönerge (YÖ-064)",
    "Öğrencilerin örgün eğitim dışında edindikleri bilgi, beceri ve yetkinliklerin ölçülerek üniversite müfredatındaki derslere eşdeğer sayılması esaslarıdır.",
    "arsiv/mevzuat_ve_yonergeler/YTÜ_Önceki_Öğrenmenin_Tanınmasına_İlişkin_Yönerge_(YÖ-064)_belgesine_ulaşmak_için.docx"
)

write_document(
    "01_mevzuat_ve_yonetmelikler/yonergeler/YO-102_yurtdisindan_ogrenci_kabul_yonergesi.md",
    {
        "kod": "YÖ-102",
        "baslik": "YTÜ Yurt Dışından Lisans Programlarına Öğrenci Kabul Yönergesi",
        "kategori": "yonerge",
        "anahtar_kelimeler": ["yurtdışı kabul", "yös", "sat", "uluslararası öğrenci", "yabancı uyruklu"]
    },
    "YTÜ Yurt Dışından Lisans Programlarına Öğrenci Kabul Yönergesi (YÖ-102)",
    "Yabancı uyruklu veya yurtdışında lise öğrenimini tamamlamış adayların YTÜ lisans programlarına kabul koşulları ve sınav/diploma eşdeğerlikleridir.",
    "arsiv/mevzuat_ve_yonergeler/YTÜ_Yurt_Dışından_Lisans_Programlarına_Öğrenci_Kabul_Yönergesi_(YÖ-102)_belgesine_ulaşmak_için.docx"
)

write_document(
    "01_mevzuat_ve_yonetmelikler/yonergeler/YO-015_myo_mezunlari_lisans_devam_yonergesi.md",
    {
        "kod": "YÖ-015",
        "baslik": "YTÜ Meslek Yüksekokulları Mezunlarının Lisans Öğrenimine Devamları Hakkında Yönerge",
        "kategori": "yonerge",
        "anahtar_kelimeler": ["dgs", "dikey geçiş", "myo intibak", "önlisans mezunu"]
    },
    "YTÜ Meslek Yüksekokulları Mezunlarının Lisans Öğrenimine Devamları Hakkında Yönerge (YÖ-015)",
    "Dikey Geçiş Sınavı (DGS) ile yerleşen önlisans mezunlarının lisans programlarına intibakı ve ders saydırma süreçleridir.",
    "arsiv/mevzuat_ve_yonergeler/YTÜ_Meslek_Yüksekokulları_Mezunlarının_Lisans_Öğrenimine_Devamları_Hakkında_Yönerge_(YÖ-015)_belgesine_ulaşmak_için.doc"
)

write_document(
    "01_mevzuat_ve_yonetmelikler/senato_esaslari_ve_tablolar/DD-022_bitirme_calismasi_ilkeleri.md",
    {
        "kod": "DD-022",
        "baslik": "YTÜ Lisans Öğretimi Bitirme Çalışması İlkeleri",
        "kategori": "senato_esasi",
        "anahtar_kelimeler": ["bitirme", "bitirme çalışması", "tez", "jüri", "sunum", "ehm9000"]
    },
    "YTÜ Lisans Öğretimi Bitirme Çalışması İlkeleri (DD-022)",
    "Lisans bitirme projesi / tezinin seçimi, danışman atanması, ara raporlar, tez yazım kuralları, jüri önünde sözlü savunma ve intihal raporu yükümlülükleridir.",
    "arsiv/mevzuat_ve_yonergeler/YTÜ_Lisans_Öğretimi_Bitirme_Çalışması_İlkeleri_(DD-022)_belgesine_ulaşmak_için.docx"
)

write_document(
    "01_mevzuat_ve_yonetmelikler/senato_esaslari_ve_tablolar/DD-118_ve_DD-013_dereceye_giren_mezunlarin_tespiti.md",
    {
        "kod": "DD-118 / DD-013",
        "baslik": "YTÜ Lisans Mezunlarının Derece Tespitine Yönelik Usul ve Esaslar",
        "kategori": "senato_esasi",
        "anahtar_kelimeler": ["derece", "bölüm birincisi", "fakülte birincisi", "üniversite derecesi", "onur öğrencisi"]
    },
    "YTÜ Lisans Mezunlarının Derece Tespitine Yönelik Usul ve Esaslar (DD-118 / DD-013)",
    "Bölüm, fakülte ve üniversite birincisi, ikincisi ve üçüncüsü olan mezunların tespit edilmesinde aranan normal öğrenim süresi, disiplin cezası almamış olma ve asgari AGNO şartlarıdır.",
    "arsiv/mevzuat_ve_yonergeler/YTÜ_Lisans_Mezunlarının_Derece_Tespitine_Yönelik_Usul_ve_Esaslar_(DD-118)_belgesine_ulaşmak_için.docx"
)

write_document(
    "01_mevzuat_ve_yonetmelikler/senato_esaslari_ve_tablolar/DD-058_bologna_intibak_esaslari.md",
    {
        "kod": "DD-058",
        "baslik": "YTÜ Bologna Öğretim Planı Geçiş ve İntibak Esasları",
        "kategori": "senato_esasi",
        "anahtar_kelimeler": ["bologna intibak", "müfredat değişikliği", "kod değişikliği", "ders intibakı"]
    },
    "YTÜ Bologna Öğretim Planı Geçiş ve İntibak Esasları (DD-058)",
    "Müfredat değişikliklerinde eski plandaki derslerin yeni plandaki derslere intibakı ve kazanılmış hakların korunması kurallarıdır.",
    "arsiv/mevzuat_ve_yonergeler/YTÜ_Bologna_2013_Öğretim_Planından_Bologna_2018_Öğretim_Planına_Geçişte_Uygulanacak_İntibak_Esasları_(DD-058)_belgesine_ulaşmak_için.docx"
)

print("Batch 2 completed successfully!")
