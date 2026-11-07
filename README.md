<p align="center">
  <img src="assets/logo.jpg" alt="Yıldızopedia Logo" width="220" style="border-radius: 16px;"/>
</p>

# 🌟 Yıldızopedia: Yıldız Teknik Üniversitesi Yapay Zeka Ansiklopedisi ve Dijital Bilgi Bankası

[![Veritabanı Durumu](https://img.shields.io/badge/Veritaban%C4%B1-407%20Markdown%20Dosyas%C4%B1-blue.svg)](#)
[![Metin Hacmi](https://img.shields.io/badge/Kelime%20Hacmi-242.895%20Kelime-success.svg)](#)
[![Resmi Arşiv](https://img.shields.io/badge/Resmi%20Ar%C5%9Fiv%20Belgesi-93%20Orijinal%20Dosya-orange.svg)](#)
[![Bologna Müfredatı](https://img.shields.io/badge/Bologna%20Lisans%20Program%C4%B1-20%20Aktif%20M%C3%BCfredat-purple.svg)](#)
[![Doğrulama Testi](https://img.shields.io/badge/Otomasyon%20Do%C4%9Frulamas%C4%B1-%25100%20Ba%C5%9Far%C4%B1l%C4%B1-brightgreen.svg)](#)
[![Yıldız Teknik Üniversitesi](https://img.shields.io/badge/YT%C3%9C-1911-red.svg)](https://yildiz.edu.tr)

**Yıldızopedia**, Yıldız Teknik Üniversitesi (YTÜ) hakkında sorulabilecek her türlü soruya (mevzuat, öğrenci işleri, sınav kuralları, hazırlık okulu, not sistemi, taban puanları, kurumsal yönetim, tarihi kökler, fakülte ve bölüm müfredatları, laboratuvarlar, staj esasları ve öğrenci toplulukları) **yapay zeka modellerinin ve ajanların sıfır spekülasyon, maksimum doğruluk ve standart kaynak atfıyla** anında yanıt vermesini sağlamak üzere inşa edilmiş kapsamlı bir açık kaynaklı dijital ansiklopedidir.

---

## 🎯 Projenin Temel İlkeleri ve Felsefesi

1. **Sıfır Halüsinasyon (Zero-Hallucination):** Yapay zeka modelleri genel kültürlerinden ya da internet tahminlerinden değil; doğrudan bu veri tabanındaki Senato kararları, yönetmelik maddeleri ve Bologna ders kodlarıyla yanıt verir.
2. **Hibrit Depolama Mimarisi:**
   - `arsiv/` klasöründe Senato kararlarının, resmi yönergelerin, sınav örneklerinin, staj defterlerinin ve formların **orijinal PDF, DOCX ve XLSX** kopyaları kalıcı olarak saklanır.
   - Ana kategorilerde (`00_` - `05_`) ise her belgenin ve konunun yapay zeka modelleri tarafından anında indekslenip okunmasını sağlayan **yapılandırılmış, YAML frontmatter'lı, tam metin Markdown** karşılıkları yer alır.
3. **Standart Kaynak ve Güvenilirlik Bildirimi:** Bilgi bankasından beslenen her yapay zeka cevabının sonunda belgenin adı, hukuki dayanağı, geçerlilik yılı ve güvenilirlik kademesi (Tier 1-4) zorunlu olarak sunulur.
4. **Akıllı Karar Ağacı ([ROUTER_GUIDE.md](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/ROUTER_GUIDE.md)):** Herhangi bir LLM'in kullanıcı sorusunu analiz ederek en doğru dosyaya doğrudan yönelmesini sağlayan karar matrisi içerir.

---

## ⚖️ 4 Kademeli Güvenilirlik Hiyerarşisi (Tiers)

Bilgi kaynakları arasında çelişki olması halinde daima şu üstünlük sırası geçerlidir:
- **Tier 1 (Resmi Mevzuat ve Senato Kararları - En Yüksek Hukuki Bağlayıcılık):** Resmi Gazete Yönetmelikleri, 2547 s.K., YTÜ Senato Kararları, YÖ- ve DD- kodlu yönergeler.
- **Tier 2 (Resmi Üniversite Portalları ve Bologna Bilgi Sistemi):** `yildiz.edu.tr`, `ogi.yildiz.edu.tr`, `ybd.yildiz.edu.tr`, fakülte ve bölüm web siteleri.
- **Tier 3 (İkincil / İstatistiki Kaynaklar):** ÖSYM / Kariyer.net taban puanları ve başarı sıralamaları, Vikipedi YTÜ külliyatı.
- **Tier 4 (Gayriresmî Topluluk Paylaşımları / Doğrulamaya Muhtaç):** Reddit `r/ytu`, `ytuitirafediyor.com`, `ytukampus.com`. Hoca tavsiyesi ve kampüs deneyimi için faydalanılır; resmi bağlayıcılığı yoktur.

---

## 📈 Canlı İlerleme ve Kapsam Tablosu

Aşağıdaki tablo, projenin mevcut tamamlanma durumunu ve gelecek yol haritasını göstermektedir:

### ✅ 1. Tamamlanan ve Kullanıma Hazır Kısımlar (3 Fakülte, 14 Bölüm, 20 Lisans Müfredatı)

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
| **Resmi Doküman Arşivi (`arsiv/`)** | Senato kararları, yönergeler, acil durum planları, örnek staj defterleri, bitirme tez şablonları, ÇAP tabloları, İYS sınav kitapçıkları | **HAZIR** | 93 Orijinal Belge |

---

### ⏳ 2. Gelecek Yol Haritası ve Eklenecek Fakülteler (Roadmap)

Projenin nihai hedefi Yıldız Teknik Üniversitesi'nin tüm akademik ve idari birimlerini bünyesine katmaktır:

- [ ] **İnşaat Fakültesi:** İnşaat Mühendisliği, Çevre Mühendisliği, Harita (Geomatik) Mühendisliği
- [ ] **Mimarlık Fakültesi:** Mimarlık, Şehir ve Bölge Planlama, Endüstriyel Tasarım
- [ ] **Fen-Edebiyat Fakültesi:** Fizik, Kimya, Matematik, Moleküler Biyoloji ve Genetik, İstatistik, Türk Dili ve Edebiyatı, Batı Dilleri ve Edebiyatları, İnsan ve Toplum Bilimleri
- [ ] **İktisadi ve İdari Bilimler Fakültesi (İİBF):** İktisat, İşletme, Siyaset Bilimi ve Uluslararası İlişkiler
- [ ] **Gemi İnşaatı ve Denizcilik Fakültesi:** Gemi İnşaatı ve Gemi Makineleri Mühendisliği, Gemi Makineleri İşletme Mühendisliği
- [ ] **Sanat ve Tasarım Fakültesi:** Müzik ve Sahne Sanatları, İletişim Tasarımı, Sanat
- [ ] **Eğitim Fakültesi:** Bilgisayar ve Öğretim Teknolojileri, Eğitim Bilimleri, Temel Eğitim, Türkçe ve Sosyal Bilimler, Yabancı Diller Eğitimi
- [ ] **Uygulamalı Bilimler Fakültesi:** Havacılık Elektroniği
- [ ] **Enstitüler:** Fen Bilimleri Enstitüsü (FBE) ve Sosyal Bilimler Enstitüsü (SBE) lisansüstü tez/yayın yönergeleri

---

## 📁 Dizin Hiyerarşisi

```
Yıldızopedia/
├── README.md                                # Proje ana tanıtımı ve canlı ilerleme durumu
├── INDEX.md                                 # Master konu indeksi ve A'dan Z'ye fihrist
├── ROUTER_GUIDE.md                          # Yapay Zeka Karar Ağacı ve Soru Yönlendirme Matrisi
├── AGENT_INSTRUCTIONS.md                    # Yapay Zeka Ajanları İçin Çalışma Kuralları
├── .gitignore                               # Git takip dışı dosyalar listesi
│
├── 00_genel_ve_kurumsal/                   # Rektörlük, 2026-2027 Takvim, Yerleşkeler, Forumlar
├── 01_mevzuat_ve_yonetmelikler/             # Lisans Yönetmeliği (15812), Disiplin (2547 m.54)
│   ├── yonergeler/                          # YÖ-075, YÖ-007, YÖ-098, YÖ-103, YÖ-096 vb.
│   └── senato_esaslari_ve_tablolar/         # DD-007, DD-125, DD-040, Not Dönüşüm Tabloları vb.
├── 02_ogrenci_isleri_ogi/                   # OGİ 73 SSS tam metin, Raporlar, Harçlar, Mezuniyet
├── 03_yabanci_diller_yuksekokulu_ybd/       # Hazırlık, Kurlar (A1-C1), 46 SSS, İYS Sınav Arşivi
├── 04_bologna_ve_not_sistemi/               # BDS Bağıl Değerlendirme, Harf Notları, YKS Sıralamaları
│
├── 05_fakulteler_ve_bolumler/               # Fakülte ve Bölüm Külliyatları
│   ├── elektrik_elektronik_fakultesi/       # EEF Dekanlığı + ELM, CE, EHM, KOM, BME, AI
│   ├── makine_fakultesi/                    # Makine Dekanlığı + MKM, ENM, MKT
│   └── kimya_metalurji_fakultesi/           # Kimya-Metalurji Dekanlığı + BIO, FOOD, KMM, MTM, MET
│
├── bot/                                     # 7/24 Telegram Botu & 0 TL RAG Servisi
│   ├── main.py                              # aiogram 3.x başlatıcı servis
│   ├── rag_engine.py                        # Yerel ChromaDB + Okapi BM25 hibrit arama motoru
│   ├── llm_client.py                        # Groq (Llama 3.3 70B) & Gemini Flash failover katmanı
│   ├── database.py                          # SQLite kullanıcı kotası (15 soru/gün) & Admin takibi
│   ├── handlers.py                          # /start, /yardim, /kalan, /stats komutları
│   ├── Dockerfile                           # Python 3.11-slim konteyner tanımı
│   └── requirements.txt                     # Bot bağımlılıkları
├── docker-compose.yml                       # Tek komutla VPS dağıtım dosyası
├── arsiv/                                   # 93 adet orijinal PDF, DOCX, XLSX arşiv belgesi
└── scripts/                                 # Otomatik veri çekme ve %100 doğrulama test araçları
```

---

## 📱 7/24 Canlı Telegram Botu (`@yildizopedia_bot`)

Yıldızopedia, teknik bilgisi olmayan tüm Yıldız öğrencilerinin doğrudan akıllı telefonlarından veya bilgisayarlarından soru sorabilmesi için resmi bir **Telegram Botu** olarak paketlenmiştir.

- **Bot Adı:** Yıldızopedia
- **Kullanıcı Adı:** `@yildizopedia_bot`
- **0 TL İşletim Maliyeti:** Öğrenciden API anahtarı istenmez. Sunucuda Groq Cloud (Llama 3.3 70B) birincil model, Google AI Studio (Gemini Flash) ise otomatik yedek model olarak çalışır.
- **Eşit ve Sürdürülebilir Erişim:** Sistemin tek bir kullanıcı tarafından kilitlenmesini önlemek için öğrenci başına **günde 15 soru limiti** (SQLite tabanlı) uygulanır. Her gece 00:00'da sayaçlar sıfırlanır.
- **Yönetici Modu:** Bot yöneticisi (`ADMIN_TELEGRAM_ID`) sınırsız soru hakkına sahiptir ve `/stats` komutuyla günün aktif öğrenci sayısını, sorulan toplam soruları anlık izleyebilir.

---

## 🌐 Tamamen Açık Kaynaklı Bilgi Bankası

> [!NOTE]
> **Öğrenci Odaklı Açık Kaynak Politikası:**
> Yıldızopedia projesindeki 407 adet kurumsal Markdown belgesi, Senato arşivleri, ders planları ve yönergeler; tüm Yıldız Teknik Üniversitesi öğrencilerinin, kulüplerinin ve araştırmacılarının serbestçe faydalanabilmesi, kendi projelerine entegre edebilmesi amacıyla **GitHub üzerinde tamamen açık kaynak olarak paylaşılmaktadır.**
>
> Projede yalnızca `.env` gibi özel API anahtarları ve yerel veritabanı dosyaları (`.sqlite3`, `chroma_db/`) güvenlik sebebiyle `.gitignore` ile korunmaktadır.

---

## 🚀 VPS Dağıtım ve Çalıştırma Seçenekleri

Botunuzu sunucuda çalıştırmak için **iki ultra pratik yol** mevcuttur:

### 1. Yol: Tek Bağımsız Binary İle Çalıştırma (En Hızlı & Sıfır Bağımlılık)
Herhangi bir Python veya Docker kurmadan doğrudan tek bir çalıştırılabilir binary dosyasıyla başlatabilirsiniz:

1. **Binary'yi Derleyin (veya `dist/yildizopedia-bot` dosyasını sunucuya atın):**
   ```bash
   bash scripts/build_binary.sh
   ```
2. **Çalıştırın:**
   ```bash
   ./dist/yildizopedia-bot
   ```
   *Bot ayağa kalktığında dökümanları doğrudan `github.com/falsisdev/yildizopedia` üzerinden otomatik olarak çeker ve hafızaya indeksler. Sunucunuzda döküman klasörlerini tutmanıza bile gerek yoktur!*

3. **Canlı Senkronizasyon (`/sync` Komutu):**
   GitHub'a yeni bir mevzuat veya bölüm dökümanı yüklediğinizde, botu yeniden başlatmanıza gerek kalmaz. Telegram'dan yöneticinizle `/sync` yazmanız yeterlidir; bot GitHub'dan en güncel arşivi 1 saniyede indirip yeniden indeksler.

---

### 2. Yol: Docker & Docker Compose İle Çalıştırma (Kalıcı Arka Plan Servisi)

1. **Repoyu Klonlayın ve `.env` Oluşturun:**
   ```bash
   git clone https://github.com/falsisdev/yildizopedia.git
   cd yildizopedia
   cp .env.example .env
   ```
2. **Konteyneri Başlatın:**
   ```bash
   docker compose up -d --build
   ```
3. **Logları İzleyin:**
   ```bash
   docker compose logs -f
   ```

---

## 🤖 Yapay Zeka Modelleri İçin Kullanım Kılavuzu

Bir LLM (Gemini, Claude, GPT, DeepSeek vb.) veya AI Agent bu projeyi kullandığında:

1. **Doğru Dosyayı Bulma:** Kullanıcı sorusunu önce [ROUTER_GUIDE.md](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/ROUTER_GUIDE.md) dosyasındaki yönlendirme tablosuyla eşleştirin.
2. **Hukuki Dayanak Bildirme:** Cevap verirken genel konuşmayın; yönetmelik madde numarasını (örn: *Lisans Yönetmeliği Madde 23*), Senato yönerge kodunu (*YÖ-075, DD-007*) veya Bologna ders kodunu belirtin.
3. **Zorunlu Kapanış Bloğu:** Her yanıtın sonuna aşağıdaki doğrulama paneli eklenmelidir:

```markdown
---
### 📌 Kaynak ve Güvenilirlik Bilgisi
- **Birincil Kaynak:** [Belge veya Sayfa Adı](dosya-yolu-veya-link)
- **Güvenilirlik Düzeyi:** [Tier 1 | Tier 2 | Tier 3 | Tier 4]
- **Geçerlilik / Güncelleme Tarihi:** [2026-2027 Akademik Yılı]
- **Yasal Dayanak / Belge No:** [Örn: Senato YÖ-075 Yönergesi Madde 9]
```

---

## 👥 Öğrenciler ve Geliştiriciler İçin Kullanım

- **VS Code / Cursor / Obsidian / Typora:** Projeyi doğrudan bir çalışma alanı (workspace) olarak açarak Markdown dosyaları arasında hızlı arama (`Ctrl+Shift+F` veya `Cmd+Shift+F`) yapabilirsiniz.
- **AI Coding Ajanları (Google Antigravity, Claude Code, Roo Code, Aider):** Bu klasörü aktif workspace olarak gösterip doğrudan sohbet penceresinden *"Makine Fakültesi staj kuralları nelerdir?"*, *"Yaz okulunda en fazla kaç kredi alabilirim?"*, *"Biyomedikal ÇDTP şartları nelerdir?"* gibi sorular yöneltebilirsiniz.
- **Otomatik Bütünlük Testi:** Projede herhangi bir dosyanın eksik olup olmadığını veya verilerin tutarlılığını test etmek için:
  ```bash
  python scripts/verify_knowledge_base.py
  ```
  Test çıktısı tüm 407 dosyayı ve 27 kritik mevzuat kriterini denetleyerek sonucu raporlar.

---

## 📜 Lisans ve Sorumluluk Reddi
Bu proje, Yıldız Teknik Üniversitesi öğrencilerine ve araştırmacılarına doğru, tarafsız ve güncel bilgi sunmak amacıyla hazırlanmış bir açık kaynak kamu hizmetidir. Resmi kararlarda ve ihtilaflı durumlarda YTÜ Senatosu, Rektörlüğü ve ilgili Fakülte Yönetim Kurulları'nın ıslak imzalı veya EBYS üzerinden yayımlanan nihai resmi kararları esastır.
