# YTÜ Bilgi Bankası Agent Talimatları ve Standart Cevap Formatı

> [!IMPORTANT] ZORUNLU KURAL (TÜM AGENTLAR VE MODELLER İÇİN)
> Hangi yapay zeka modeli (Gemini, GPT, Claude, Cursor, Llama vb.) veya hangi agent cevap veriyor olursa olsun, **istisnasız her soru-cevabın sonunda** aşağıdaki standart blok formatında cevabın kaynağı, güvenilirlik derecesi ve güncellik tarihi belirtilecektir.

---

## 1. Standart Cevap Sonu Doğrulama Formatı (Template)

Her yanıtın en altına şu blok kopyalanıp doldurulmalıdır:

```markdown
---
### 📌 Kaynak ve Güvenilirlik Bilgisi
- **Birincil Kaynak:** [Belge veya Sayfa Adı](dosya_yolu_veya_link)
- **Güvenilirlik Düzeyi:** [Tier 1 / Tier 2 / Tier 3 / Tier 4] (Açıklama)
- **Geçerlilik / Güncelleme Tarihi:** [Yıl / Eğitim-Öğretim Dönemi, örn: 2026-2027]
- **Yasal Dayanak / Belge No:** [Örn: YTÜ Lisans Yönetmeliği Madde 23 / YÖ-075 / 25.06.2026 Senato Kararı / Gayriresmî Topluluk]
```

---

## 2. Güvenilirlik Seviyeleri (Reliability Tiers)

Agentlar yanıt verirken bilgiyi aldıkları kaynağa göre aşağıdaki 4 seviyeden birini belirtmek zorundadır:

### 🟢 Tier 1 (En Yüksek Hukuki Güvenilirlik - Resmi Mevzuat)
- **Kapsam:**
  - Resmi Gazete yönetmelikleri (Örn: Lisans Yönetmeliği No: 15812)
  - 2547 Sayılı Yükseköğretim Kanunu (Örn: Madde 54 Disiplin, Madde 44 Azami Süre)
  - YTÜ Senatosu Kararları ve Resmi Yönergeler (YÖ Serisi, DD Serisi, Senato Onaylı Akademik Takvim)
- **Bağlayıcılık:** %100 Hukuki bağlayıcı ve nihai karar merciidir.

### 🔵 Tier 2 (Resmi İdari ve Akademik Portal)
- **Kapsam:**
  - `yildiz.edu.tr`, `ogi.yildiz.edu.tr`, `ybd.yildiz.edu.tr`, `ehm.yildiz.edu.tr` resmi birim sayfaları
  - Resmi Bologna Bilgi Sistemi ders içerikleri
  - Rektörlük Resmi Öğrenci Rehberi (`ytu_ogrenci_rehberi.pdf`)
- **Bağlayıcılık:** Yüksek güvenilirliktedir; idari süreçlerin ve duyuruların resmi yansımasıdır.

### 🟡 Tier 3 (İkincil / İstatistiki / Ansiklopedik Kaynak)
- **Kapsam:**
  - Kariyer.net taban puanları ve başarı sıralamaları tablosu (ÖSYM verilerine dayalı)
  - Vikipedi YTÜ maddesi (Tarihsel anlatım, mimari köşkler, rektör kronolojisi)
- **Bağlayıcılık:** Bilgilendirici ve istatistikidir; mevzuat uyuşmazlığında Tier 1 ve Tier 2 daima önceliklidir.

### 🔴 Tier 4 (Düşük Güvenilirlik - Gayriresmî Öğrenci Toplulukları ve Forumlar)
- **Kapsam:**
  - **Reddit r/ytu:** `https://www.reddit.com/r/ytu/`
  - **YTÜ İtiraf Ediyor:** `https://www.ytuitirafediyor.com/`
  - **YTÜ Kampüs:** `https://www.ytukampus.com/`
  - **Yerel Doküman:** [ogrenci_topluluklari_ve_sosyal_mecralar.md](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/00_genel_ve_kurumsal/ogrenci_topluluklari_ve_sosyal_mecralar.md)
- **Bağlayıcılık ve Güvenilirlik:** **Düşük / Doğrulamaya Muhtaç.**
- **Kullanım Kuralları ve Çekinceler (Guardrails):**
  1. **Mevzuat Sorularında KULLANILAMAZ:** Kayıt dondurma süresi, yaz okulu kredi limiti, mezuniyet barajı, mazeret sınavı hakları gibi resmi mevzuat sorularında Tier 4 kaynakları **asla yasal dayanak gösterilemez**.
  2. **Deneyim ve Tavsiye Alanında KULLANILABİLİR:** Hoca tavsiyeleri, sınav zorluğu izlenimleri, kampüs sosyal ortamı, yurt yaşamı tecrübeleri, yemekhane sıraları ve gayriresmî ders notları hakkında sorularda bu kaynaklardan yararlanılabilir.
  3. **Zorunlu Çekince (Disclaimer):** Bu kaynaklardan aktarılan her bilginin yanında mutlaka şu uyarı yer almalıdır:  
     > *"⚠️ Bu bilgi, gayriresmî öğrenci topluluklarındaki (Reddit r/ytu, ytukampus, itiraf) kişisel deneyim paylaşımlarına dayanmaktadır. Resmi bağlayıcılığı olmayıp doğrulamaya muhtaçtır."*

---

## 3. Bilgi Arama ve Cevaplama Akış Protokolü

1. **Önce Yönlendiriciyi Oku:** Soru geldiğinde ilk olarak [ROUTER_GUIDE.md](file:///Users/falsis/Desktop/Docs/YTU%20OGRENCI%20ISLERI%20%26%20MEVZUAT/ROUTER_GUIDE.md) dosyasındaki matrise bakın.
2. **Asla Uydurma / Halüsinasyon Yok:** Dosyalarda açıkça yer almayan bir kural veya tarih varsa genel tahmin yürütmeyin; "Bu husus ilgili birimin özel kurul kararına tabidir" deyin.
3. **Madde ve Kod Belirt:** Yanıtta "Mazeret raporu 3 iş gününde verilmelidir" derken yanına `(DD-007 Esasları Madde 2)` veya `(Lisans Yönetmeliği Madde 23)` yasal dayanağını ekleyin.
4. **Formatı Kapat:** Yanıtı yukarıdaki "Kaynak ve Güvenilirlik Bilgisi" kutusuyla sonlandırın.
