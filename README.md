<p align="center">
  <img src="assets/logo.jpg" alt="Yıldızopedia Logo" width="220" style="border-radius: 16px;"/>
</p>

# 🌟 Yıldızopedia: Yıldız Teknik Üniversitesi Yapay Zeka Ansiklopedisi ve Dijital Bilgi Bankası

[![Veritabanı Durumu](https://img.shields.io/badge/Veritaban%C4%B1-519%20Markdown%20Dosyas%C4%B1-blue.svg)](#)
[![Metin Hacmi](https://img.shields.io/badge/Kelime%20Hacmi-296.714%20Kelime-success.svg)](#)
[![Ders Önkoşul Grafı](https://img.shields.io/badge/%C3%96nko%C5%9Ful%20Graf%C4%B1-925%20Resm%C3%AE%20Ders-purple.svg)](#)
[![Bologna Müfredatı](https://img.shields.io/badge/Bologna%20Lisans%20Program%C4%B1-26%20Aktif%20M%C3%BCfredat-orange.svg)](#)
[![Doğrulama Testi](https://img.shields.io/badge/Otomasyon%20Testi-%25100%20Ba%C5%9Far%C4%B1l%C4%B1-brightgreen.svg)](#)
[![Yıldız Teknik Üniversitesi](https://img.shields.io/badge/YT%C3%9C-1911-red.svg)](https://yildiz.edu.tr)

**Yıldızopedia**, Yıldız Teknik Üniversitesi (YTÜ) hakkında sorulabilecek her türlü soruya (mevzuat, öğrenci işleri, sınav kuralları, hazırlık okulu, not sistemi, taban puanları, kurumsal yönetim, tarihi kökler, fakülte ve bölüm müfredatları, laboratuvarlar, staj esasları ve öğrenci toplulukları) **yapay zeka modellerinin ve ajanların sıfır halüsinasyon, maksimum doğruluk ve kesin hukuki dayanakla** anında yanıt vermesini sağlamak üzere inşa edilmiş kapsamlı bir açık kaynaklı dijital bilgi bankası ve akıllı öğrenci danışmanıdır.

---

## 🎯 Projenin Temel İlkeleri ve Mimarisi

1. **Sıfır Halüsinasyon (Zero-Hallucination):** Yapay zeka modelleri genel internet varsayımlarından veya diğer üniversitelerin yönetmeliklerinden değil; doğrudan bu veri tabanındaki Senato kararları, yönetmelik maddeleri ve Bologna ders önkoşul grafıyla yanıt verir.
2. **Otomatize Veri Kaynağı Derleme Motoru (`pipelines/`):**
   - 400+ doküman statik olarak bırakılmaz; tekil modüler scraper'lar (`pipelines/scrapers/`) aracılığıyla Bologna, Mevzuat ve Fakülte portallarından derlenir.
   - `python -m pipelines.compiler` ile ders önkoşulları taranarak anında yapısal bir **Ders Önkoşul Grafı (`data/prerequisites_graph.json`)** üretilir.
   - `python -m pipelines.validator` ile tüm dökümanların YAML frontmatter ve hukuki güvenilirlik seviyeleri (Tier) otomatik denetlenir.
3. **Çok Turlu Akıllı Takip Sorusu Çözücü (`query_rewriter`):**
   - Öğrenciler *"Peki önkoşulu var mı?"*, *"Bu dersten kalırsam ne olur?"* gibi zamirli takip soruları sorduğunda, bot konuşma geçmişinden ders kodunu (örn: `BLM2012`) tespit ederek arama sorgusunu otomatik zenginleştirir.
4. **Hukuki Güvenilirlik Seviyeleri (Tiers):**
   - Her dokümanın başında doğrulanmış `guvenilirlik_duzeyi` yer alır ve bot her cevabın altında yasal dayanağını şeffafça ilan eder:
     - **Tier 1 (Resmi Mevzuat ve Senato Kararları):** Resmi Gazete Yönetmelikleri, 2547 s.K., YTÜ Senato Kararları, YÖ- ve DD- kodlu yönergeler.
     - **Tier 2 (Resmi Üniversite Portalları ve Bologna Sistemi):** `yildiz.edu.tr`, `ogi.yildiz.edu.tr`, `ybd.yildiz.edu.tr`, fakülte ve bölüm müfredatları.
     - **Tier 3 (İkincil / İstatistiki Kaynaklar):** ÖSYM / Kariyer.net taban puanları, başarı sıralamaları, tarihsel külliyat.
     - **Tier 4 (Gayriresmî Öğrenci Deneyimi):** Reddit `r/ytu`, `ytuitirafediyor.com`. Kampüs kültürü için faydalanılır; resmi bağlayıcılığı yoktur.
5. **Akıllı Karar Ağacı ([ROUTER_GUIDE.md](ROUTER_GUIDE.md)):** Herhangi bir LLM'in veya ajanın kullanıcı sorusunu analiz ederek en doğru dosyaya doğrudan yönelmesini sağlayan karar matrisi içerir.

---

## 📈 Kapsam ve İlerleme Durumu

### ✅ Tamamlanan ve Kullanıma Hazır Kısımlar (5 Fakülte, 19 Bölüm, 26 Lisans Müfredatı)

| Kategori / Birim | Kapsam ve İçerik | Durum | Dosya Adedi |
|---|---|:---:|:---:|
| **00. Genel ve Kurumsal Yapı** | Rektörlük teşkilatı, Rektör Prof. Dr. Eyüp Debik, 2026-2027 Senato onaylı Akademik Takvim, Yerleşkeler (Davutpaşa, Yıldız, Maslak), Tarihçe (1911 Kondüktör Mektebi), Reddit/İtiraf/YTÜ Kampüs topluluk analizleri | **HAZIR** | 7 Dosya |
| **01. Mevzuat ve Yönetmelikler** | 15812 Lisans Yönetmeliği, 2547 s.K. Md. 54 Disiplin Hükümleri, 11 Yönerge (YÖ-075 Sınav, YÖ-007 Yaz Okulu, YÖ-098 ÇAP/Yatay Geçiş, YÖ-103 Staj vb.), 8 Senato Esası (DD-007 Mazeret, DD-125 Ders Kayıt, DD-040 %10, Not Dönüşüm Tabloları) | **HAZIR** | 22 Dosya |
| **02. Öğrenci İşleri Daire Bşk. (OGİ)** | 73 resmi Sıkça Sorulan Soru (tam metin), Kayıt Dondurma, Mazeret ve Sağlık Raporları, Harç İşlemleri, Mezuniyet ve İlişik Kesme | **HAZIR** | 7 Dosya |
| **03. Yabancı Diller Yüksekokulu (YBD)** | Hazırlık zorunluluğu, A1-C1 kurları ve haftalık saatleri, 46 YBD SSS, %85 devam kuralı, İYS Örnek Sınavları (1. ve 2. Oturum metinleri, Writing rubrikleri, Erasmus & Lisansüstü İYS) | **HAZIR** | 11 Dosya |
| **04. Bologna ve Not Sistemi** | Genel Kabul Koşulları, YKS Taban Puanları ve Başarı Sıralamaları, Bağıl Değerlendirme Sistemi (BDS), Harf Notu Katsayıları (AA-FF), AGNO/YNO baremleri | **HAZIR** | 6 Dosya |
| **05.1 Elektrik-Elektronik Fakültesi (EEF)** | **Dekanlık:** Prof. Dr. Ahmet Faruk BAKAN, YÖ-033 Etik Yönergesi, Akran Danışmanlığı, 12 Fakülte SSS.<br/>**6 Bölüm (Bologna 1-8. yarıyıl kartları, önkoşullar, staj, lablar):**<br/>• Elektrik Mühendisliği (%30 İng - ID: 7, Yüksek Gerilim Labı, DD-087 KOOP)<br/>• Bilgisayar Mühendisliği (%30 İng - ID: 550, 44 SSS TR/EN, Sky Lab, Proje Portalı)<br/>• Elektronik ve Haberleşme Mühendisliği (%30 İng - ID: 6, MÜDEK PÇ-1..11, 30+30 Staj)<br/>• Kontrol ve Otomasyon Mühendisliği (%30 [ID: 29] & %100 İng [ID: 403], Omron/Schneider)<br/>• Biyomedikal Mühendisliği (%100 İng - ID: 504, Hastane Stajı, ÇDTP FR-1558)<br/>• Yapay Zeka ve Veri Mühendisliği (%100 İng - ID: 557, YZM Müfredatı, GPU Altyapısı) | **HAZIR** | 125 Dosya |
| **05.2 Makine Fakültesi** | **Dekanlık:** Prof. Dr. Zehra YUMURTACI, Fakülte SSS, KOOP Esasları, Acil Eylem Planı.<br/>**3 Bölüm (Bologna 1-8. yarıyıl kartları, önkoşullar, staj, lablar):**<br/>• Makine Mühendisliği (%30 İng - ID: 391, Otomotiv Stajı, ÇAP Eşlenik Tablosu)<br/>• Endüstri Mühendisliği (%30 [ID: 45] & %100 İng [ID: 405], ÇDTP Şablonu, END4000 Kılavuzu)<br/>• Mekatronik Mühendisliği (%30 [ID: 46] & %100 İng [ID: 404], 2026-2027 MST ve Bitirme) | **HAZIR** | 73 Dosya |
| **05.3 Kimya-Metalurji Fakültesi** | **Dekanlık:** Prof. Dr. Musa TÜRKER, KMF Hizmet Standartları Tablosu ve Envanteri.<br/>**5 Bölüm (Bologna 1-8. yarıyıl kartları, önkoşullar, staj, lablar):**<br/>• Biyomühendislik (%30 [ID: 147] & %100 İng [ID: 163], Staj Yönetmeliği, Biyoreaktör Labı)<br/>• Gıda Mühendisliği (%30 İng - ID: 195, Duyusal Analiz ve Mikrobiyoloji Güvenlik Föyü)<br/>• Kimya Mühendisliği (%30 [ID: 36] & %100 İng [ID: 398], Staj Rehberi, FR-0750/0751, Unit Op.)<br/>• Matematik Mühendisliği (%30 [ID: 37] & %100 İng [ID: 222], Donanım ve Yazılım Staj Defterleri)<br/>• Metalurji ve Malzeme Müh. (%30 [ID: 38] & %100 İng [ID: 401], STAJ-1/2 Esasları, SEM/XRD) | **HAZIR** | 128 Dosya |
| **05.4 İnşaat Fakültesi** | **Dekanlık:** Prof. Dr. Uğur KURT, DD-074 Staj İlkeleri, Fakülte SSS, Akran Danışmanlığı.<br/>**3 Bölüm (Bologna 1-8. yarıyıl kartları, önkoşullar, staj, lablar):**<br/>• İnşaat Mühendisliği (%30 [ID: 40] & %100 İng [ID: 397], Kutay Özaydın Labı, 60 Gün Şantiye/Büro Stajı)<br/>• Çevre Mühendisliği (%30 İng - ID: 43, DD-071 Staj Esasları, Su ve Arıtma Labları)<br/>• Harita Mühendisliği (%30 İng - ID: 44, Fotogrametri, CBS ve Jeodezi Labları, 60 Gün Arazi/Büro Stajı) | **HAZIR** | 59 Dosya |
| **05.5 Gemi İnşaatı ve Denizcilik Fakültesi (GİDF)** | **Dekanlık:** Prof. Dr. Serkan EKİNCİ, STCW Deniz Eğitimi Esasları, Fakülte SSS, Akran Rehberi.<br/>**2 Bölüm (Bologna 1-8. yarıyıl kartları, önkoşullar, staj, lablar):**<br/>• Gemi İnşaatı ve Gemi Makineleri (%30 İng - ID: 48, Çekme Tankı, FEA Labı, 60 Gün Tersane/Dizayn Stajı)<br/>• Gemi Makineleri İşletme (%30 İng - ID: 141, Köprüüstü Simülatörü, 150 Gün Atölye + 180 Gün Açık Deniz Stajı, GASM/Liman Cüzdanı) | **HAZIR** | 52 Dosya |
| **Resmi Doküman Arşivi (`arsiv/`)** | Senato kararları, yönergeler, acil durum planları, örnek staj defterleri, bitirme tez şablonları, ÇAP tabloları, İYS sınav kitapçıkları | **HAZIR** | 93 Orijinal Belge |

---

## 📁 Dizin Hiyerarşisi

```
Yıldızopedia/
├── README.md                                # Proje ana tanıtımı ve canlı ilerleme durumu
├── INDEX.md                                 # Master konu indeksi ve A'dan Z'ye fihrist
├── ROUTER_GUIDE.md                          # Yapay Zeka Karar Ağacı ve Soru Yönlendirme Matrisi
├── AGENT_INSTRUCTIONS.md                    # Yapay Zeka Ajanları İçin Standart Kurallar
├── docker-compose.yml                       # Docker Compose üretim servis tanımı
├── pytest.ini                               # Otomatik test yapılandırması
│
├── 00_genel_ve_kurumsal/                   # Rektörlük, 2026-2027 Takvim, Yerleşkeler, Topluluklar
├── 01_mevzuat_ve_yonetmelikler/             # Lisans Yönetmeliği (15812), Disiplin (2547 m.54)
│   ├── yonergeler/                          # YÖ-075, YÖ-007, YÖ-098, YÖ-103, YÖ-096 vb.
│   └── senato_esaslari_ve_tablolar/         # DD-007, DD-125, DD-040, Not Dönüşüm Tabloları vb.
├── 02_ogrenci_isleri_ogi/                   # OGİ 73 SSS tam metin, Raporlar, Harçlar, Mezuniyet
├── 03_yabanci_diller_yuksekokulu_ybd/       # Hazırlık, Kurlar (A1-C1), 46 SSS, İYS Sınav Arşivi
├── 04_bologna_ve_not_sistemi/               # BDS Bağıl Değerlendirme, Harf Notları, YKS Sıralamaları
├── 05_fakulteler_ve_bolumler/               # 5 Fakülte ve 19 Lisans Bölüm Külliyatı
│   ├── elektrik_elektronik_fakultesi/       # EEF Dekanlığı + ELM, CE, EHM, KOM, BME, AI
│   ├── makine_fakultesi/                    # Makine Dekanlığı + MKM, ENM, MKT
│   ├── kimya_metalurji_fakultesi/           # Kimya-Metalurji Dekanlığı + BIO, FOOD, KMM, MTM, MET
│   ├── insaat_fakultesi/                    # İnşaat Fakültesi Dekanlığı + INM, CEM, HRM
│   └── gemi_insaati_ve_denizcilik_fakultesi/# GİDF Dekanlığı + GİM, GMİM
│
├── pipelines/                               # Veri Kaynağı Derleme Motoru (Data Pipeline)
│   ├── sources.yaml                         # Tüm birimlerin Bologna ID ve URL kayıt defteri
│   ├── compiler.py                          # Link düzeltici, graph üretici, istatistik derleyici
│   ├── validator.py                         # %100 Frontmatter ve Tier bütünlük denetleyicisi
│   └── scrapers/                            # Bologna ve portal kazıyıcı modülleri
│
├── data/                                    # Derlenmiş Yapısal Veriler
│   └── prerequisites_graph.json             # 925 dersin resmi önkoşul haritası
│
├── var/                                     # Kalıcı Veritabanı ve Loglar (Docker Mount)
│   └── bot_data.sqlite3                     # SQLite kota, kullanıcı ve hafıza veritabanı
│
├── bot/                                     # 7/24 Telegram Botu & 0 TL Hibrit RAG Servisi
│   ├── main.py                              # aiogram 3.x başlatıcı servis
│   ├── config.py                            # Pydantic tabanlı ortam değişkenleri
│   ├── database.py                          # Günlük kota (15 soru/gün) ve sohbet hafızası
│   ├── handlers.py                          # /start, /yardim, /kalan, /stats, /reload_kb
│   ├── llm_client.py                        # Async httpx Groq Llama 3.3 70B & Gemini Flash failover
│   ├── rag_engine.py                        # YAML frontmatter ayrıştırıcılı Okapi BM25 motoru
│   ├── Dockerfile                           # Ultra hafif Python 3.11-slim konteyner tanımı
│   ├── requirements.txt                     # Bot bağımlılıkları
│   └── retrieval/                           # Akıllı Sorgu ve Arama Modülleri
│       ├── query_rewriter.py                # Takip soruları çözücü (BLM2012 entity enjektörü)
│       └── hybrid_search.py                 # Önkoşul grafı sentetik bağlam entegratörü
│
├── tests/                                   # Otomasyon Test Süiti (pytest)
│   └── test_retrieval.py                    # Tier ayrıştırma, split, rewriter ve graph testleri
└── arsiv/                                   # 93 adet orijinal PDF, DOCX, XLSX arşiv belgesi
```

---

## 📱 7/24 Canlı Telegram Botu (`@yildizopedia_bot`)

Yıldızopedia, tüm Yıldız öğrencilerinin akıllı telefonlarından doğrudan soru sorabilmesi için resmî bir **Telegram Botu** olarak paketlenmiştir.

- **Bot Adı:** Yıldızopedia
- **Kullanıcı Adı:** `@yildizopedia_bot`
- **🧠 Çok Turlu Sohbet Hafızası & Takip Soruları (`query_rewriter`):**
  Bot, kullanıcının sorduğu önceki soruları hatırlar. Öğrenci *"Peki bu dersin önkoşulu var mı?"* dediğinde, geçmiş konuşmadan ders kodunu çıkararak doğrudan Bologna grafından yanıt verir.
- **🛡️ Sıfır Spekülasyon & Kesin Önkoşul Grafı:** Ders sorularında doğrudan derlenmiş `prerequisites_graph.json` devreye girerek en güncel Bologna önkoşulunu 1. sıraya yerleştirir.
- **🧹 Hafıza Sıfırlama (`/temizle`):** Yeni bir konuya geçerken hafızayı tek komutla temizleyip sıfırdan başlama imkanı sunar.
- **⚡ Kesintisiz Bilgi Bankası Tazeleme (`/reload_kb`):** Dökümanlar güncellendiğinde botu kapatıp açmaya gerek kalmaz. Yönetici `/reload_kb` yazdığında bellek içi arama indeksi ve önkoşul grafı 0.1 saniyede kesintisiz yenilenir.
- **0 TL İşletim Maliyeti:** Öğrenciden API anahtarı istenmez. Sunucuda Groq Cloud (Llama 3.3 70B) birincil model, Google AI Studio (Gemini Flash) ise otomatik yedek model olarak çalışır.
- **Eşit ve Sürdürülebilir Erişim:** Sistemin kilitlenmesini önlemek için öğrenci başına **günde 15 soru limiti** uygulanır. Her gece 00:00'da sayaçlar sıfırlanır. Hata anında öğrencinin kotası düşmez.
- **Yönetici Modu:** Bot yöneticisi (`ADMIN_TELEGRAM_ID`) sınırsız soru hakkına sahiptir ve `/stats` komutuyla günün istatistiklerini anlık izleyebilir.

---

## 🚀 Sunucu (VPS) Dağıtım Kılavuzu

Botu sunucuda kalıcı (7/24) çalıştırmak için önerilen yöntemler:

### 1. Yol: Docker Compose İle Çalıştırma (Önerilen)

```bash
# 1. Repoyu klonlayın ve klasöre girin
git clone https://github.com/falsisdev/yildizopedia.git
cd yildizopedia

# 2. .env dosyasını oluşturup API anahtarlarınızı girin
cp .env.example .env
nano .env

# 3. Kalıcı veritabanı klasörünü açın
mkdir -p var

# 4. Arka planda derleyip başlatın
docker compose up -d --build

# 5. Logları izleyin
docker compose logs -f
```

*(Sunucunuzda `docker compose` yerine doğrudan Docker kullanmak isterseniz:)*
```bash
docker build -t yildizopedia-bot -f bot/Dockerfile .
docker run -d --name yildizopedia_bot --restart unless-stopped --env-file .env -v $(pwd):/app -v $(pwd)/var:/app/var yildizopedia-bot
```

---

### 2. Yol: Linux Systemd Servisi Olarak Çalıştırma

```bash
# 1. Sanal ortamı kurun ve bağımlılıkları yükleyin
python3 -m venv venv
source venv/bin/activate
pip install -r bot/requirements.txt

# 2. Servis dosyasını hazırlayın (/etc/systemd/system/yildizopedia.service)
sudo nano /etc/systemd/system/yildizopedia.service
```

```ini
[Unit]
Description=Yıldızopedia 7/24 Telegram Bot Servisi
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/yildizopedia
ExecStart=/root/yildizopedia/venv/bin/python -m bot.main
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

```bash
# 3. Servisi başlatın
sudo systemctl daemon-reload
sudo systemctl enable yildizopedia
sudo systemctl start yildizopedia
```

---

## 🛠️ Geliştirici ve Veri Derleme Araçları (Pipelines)

```bash
# 1. Ders Önkoşul Grafını ve İstatistikleri Derleme
python -m pipelines.compiler

# 2. Bilgi Bankası Standartlarını ve Frontmatter Bütünlüğünü Denetleme
python -m pipelines.validator

# 3. Arama ve RAG Alt Sistem Testlerini Çalıştırma (pytest)
pytest tests/test_retrieval.py
```

---

## 📜 Lisans ve Sorumluluk Reddi

Bu proje, Yıldız Teknik Üniversitesi öğrencilerine ve araştırmacılarına doğru, tarafsız ve güncel bilgi sunmak amacıyla hazırlanmış bir açık kaynak kamu hizmetidir. Resmi kararlarda ve ihtilaflı durumlarda YTÜ Senatosu, Rektörlüğü ve ilgili Fakülte Yönetim Kurulları'nın ıslak imzalı veya EBYS üzerinden yayımlanan nihai resmi kararları esastır.
