import os
import re
import math
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from bot.config import KNOWLEDGE_BASE_DIR

try:
    import frontmatter
except ImportError:
    frontmatter = None

EXCLUDED_DIRS = {
    ".git", ".system_generated", "bot", "scratch", "venv", ".venv",
    "__pycache__", "chroma_db", "chroma_data", "data_cache", "build",
    "dist", "var", "path", "tests"
}
EXCLUDED_FILES = {"README.md", "AGENT_INSTRUCTIONS.md", "INDEX.md", "ROUTER_GUIDE.md"}

TURKISH_STOPWORDS = {
    've', 'bir', 'bu', 'da', 'de', 'icin', 'için', 'ile', 'veya', 'mi', 'mı', 'mu', 'mü',
    'gibi', 'olan', 'kadar', 'en', 'cok', 'çok', 'daha', 'ama', 'ancak', 'ise', 'su', 'şu',
    'o', 'ne', 'var', 'yok', 'gore', 'göre', 'acisindan', 'açısından', 'ben', 'sen', 'bana',
    'sana', 'yap', 'et', 'soyle', 'söyle', 'acikla', 'açıkla', 'detayli', 'detaylı', 'analiz',
    'benzeri', 'seyler', 'şeyler', 'durumu', 'nasil', 'nasıl', 'hangi', 'varsa', 'olup',
    'eder', 'edebilir', 'olur', 'muamelesi', 'hakkim', 'hakkım', 'miyim', 'mıyım'
}

def tr_lower(text: str) -> str:
    if not text:
        return ""
    mapping = {"I": "ı", "İ": "i", "Ğ": "ğ", "Ü": "ü", "Ş": "ş", "Ö": "ö", "Ç": "ç"}
    for k, v in mapping.items():
        text = text.replace(k, v)
    return text.lower()

def tokenize(text: str) -> List[str]:
    text = tr_lower(text)
    return [t for t in re.findall(r"[a-z0-9çğıöşü]+", text) if len(t) > 1 and t not in TURKISH_STOPWORDS]

def parse_frontmatter_safe(raw_text: str) -> Tuple[Dict[str, Any], str]:
    """YAML Frontmatter'ı ayrıştırır ve gövde Markdown metnini döndürür."""
    if frontmatter is not None:
        try:
            post = frontmatter.loads(raw_text)
            return dict(post.metadata), post.content
        except Exception:
            pass

    # Regex tabanlı hafif fallback
    if raw_text.startswith("---"):
        parts = raw_text.split("---", 2)
        if len(parts) >= 3:
            yaml_block = parts[1]
            body = parts[2].strip()
            meta = {}
            for line in yaml_block.split("\n"):
                line = line.strip()
                if ":" in line and not line.startswith("#"):
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"').strip("'")
            return meta, body

    return {}, raw_text

class DocumentChunk:
    def __init__(
        self,
        file_path: str,
        title: str,
        section: str,
        content: str,
        tier: str = "Tier 1 (Resmi Belge)",
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.file_path = file_path
        self.title = title
        self.section = section
        self.content = content
        self.tier = tier
        self.metadata = metadata or {}
        # Arama indeksine sadece başlık, bölüm ve gövdeyi dahil et; YAML anahtarlarını karıştırma
        self.tokens = tokenize(title + " " + section + " " + content)

class SimpleBM25:
    """Okapi BM25 Arama Motoru."""
    def __init__(self, chunks: List[DocumentChunk], k1: float = 1.5, b: float = 0.75):
        self.chunks = chunks
        self.k1 = k1
        self.b = b
        self.doc_len = [len(c.tokens) for c in chunks]
        self.avg_doc_len = sum(self.doc_len) / len(self.doc_len) if self.doc_len else 1.0

        self.df: Dict[str, int] = {}
        self.tf: List[Dict[str, int]] = []
        for c in chunks:
            term_freq = {}
            for t in c.tokens:
                term_freq[t] = term_freq.get(t, 0) + 1
            self.tf.append(term_freq)
            for t in term_freq:
                self.df[t] = self.df.get(t, 0) + 1

        self.N = len(chunks)
        self.idf: Dict[str, float] = {}
        for t, freq in self.df.items():
            self.idf[t] = math.log(1 + (self.N - freq + 0.5) / (freq + 0.5))

    def score(self, query_tokens: List[str], top_k: int = 5) -> List[DocumentChunk]:
        if not self.chunks or not query_tokens:
            return []

        scores = [0.0] * self.N
        for t in query_tokens:
            if t not in self.idf:
                continue
            idf_val = self.idf[t]
            for idx, term_freq in enumerate(self.tf):
                if t in term_freq:
                    tf_val = term_freq[t]
                    numerator = tf_val * (self.k1 + 1)
                    denominator = tf_val + self.k1 * (1 - self.b + self.b * (self.doc_len[idx] / self.avg_doc_len))
                    scores[idx] += idf_val * (numerator / denominator)

        ranked_indices = sorted(range(self.N), key=lambda i: scores[i], reverse=True)
        # SIFIR EŞLEŞME GÜVENLİĞİ: Sadece pozitif skora sahip parçaları döndür
        results = [self.chunks[i] for i in ranked_indices if scores[i] > 0]
        return results[:top_k]

class RAGEngine:
    def __init__(self, kb_dir: Path = KNOWLEDGE_BASE_DIR):
        self.kb_dir = kb_dir
        self.chunks: List[DocumentChunk] = []
        self.bm25: Optional[SimpleBM25] = None
        self.last_sync_info = "Yerel bilgi bankası yüklendi."
        
        # Dökümanları yükle ve indeksle
        self._load_and_index_documents()

    def reload_index(self) -> Tuple[bool, str]:
        """Bilgi bankası dökümanlarını yeniden okur ve bellek içi indeksi günceller."""
        try:
            self._load_and_index_documents()
            msg = f"✅ Bilgi bankası tazelendi: {len(self.chunks)} bölüm parçası indekslendi."
            self.last_sync_info = msg
            return True, msg
        except Exception as e:
            msg = f"❌ İndeks yenileme hatası: {e}"
            self.last_sync_info = msg
            return False, msg

    def _determine_tier_fallback(self, rel_path: str, meta: Dict[str, Any]) -> str:
        """Frontmatter'da guvenilirlik_duzeyi yoksa güvenli hiyerarşik varsayılan belirler."""
        if "guvenilirlik_duzeyi" in meta and meta["guvenilirlik_duzeyi"]:
            return str(meta["guvenilirlik_duzeyi"])

        rel_lower = rel_path.lower()
        if "00_genel_ve_kurumsal/ogrenci_topluluklari" in rel_lower or "itiraf" in rel_lower or "reddit" in rel_lower:
            return "Tier 4 (Gayriresmî Öğrenci Deneyimi / Doğrulamaya Muhtaç)"
        if "vikipedi" in rel_lower or "taban_puan" in rel_lower:
            return "Tier 3 (İkincil / İstatistiki Kaynak)"
        if "05_fakulteler" in rel_lower or "bologna" in rel_lower:
            return "Tier 2 (Resmi Bologna ve Bölüm Portalı)"
        return "Tier 1 (Resmi Mevzuat ve Senato Kararları)"

    def _load_and_index_documents(self):
        """Tüm markdown dökümanlarını frontmatter ayrıştırmasıyla granüler parçalar olarak indeksler."""
        all_chunks = []
        if not self.kb_dir.exists():
            return

        for root, dirs, files in os.walk(self.kb_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
            for file in files:
                if not file.endswith(".md") or file in EXCLUDED_FILES:
                    continue
                file_path = Path(root) / file
                rel_path = str(file_path.relative_to(self.kb_dir))

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        raw_text = f.read()
                except Exception:
                    continue

                meta, body = parse_frontmatter_safe(raw_text)
                tier = self._determine_tier_fallback(rel_path, meta)
                chunks = self._chunk_markdown(body, rel_path, tier, meta)
                all_chunks.extend(chunks)

        self.chunks = all_chunks
        if self.chunks:
            self.bm25 = SimpleBM25(self.chunks)

    def _chunk_markdown(
        self,
        body_text: str,
        rel_path: str,
        tier: str,
        meta: Dict[str, Any]
    ) -> List[DocumentChunk]:
        """Markdown gövdesini ## ve ### başlıklarına göre ayırır."""
        sections = re.split(r'\n(?=###? )', body_text)
        default_title = meta.get("baslik") or Path(rel_path).stem.replace("_", " ").title()
        doc_title = default_title
        chunks = []

        for s in sections:
            s_clean = s.strip()
            if not s_clean:
                continue
            lines = s_clean.split("\n")
            first_line = lines[0]

            if first_line.startswith("# ") and doc_title == default_title:
                doc_title = first_line.replace("#", "").strip()

            sec_title = first_line.replace("#", "").strip() if first_line.startswith("#") else "Genel"
            content = "\n".join(lines[1:]).strip() if len(lines) > 1 else s_clean

            if len(content) > 35:
                chunks.append(DocumentChunk(rel_path, doc_title, sec_title, content, tier, meta))

        if not chunks and body_text.strip():
            chunks.append(DocumentChunk(rel_path, doc_title, "Genel", body_text.strip(), tier, meta))

        return chunks

    def _extract_semester_and_department(self, q_lower: str) -> Tuple[Optional[str], Optional[str]]:
        """Sorgudan bölüm ve hedeflenen Bologna yarıyıl dosyasını regex ile güvenle çıkarır."""
        dept_keywords = {
            "elektronik": "elektronik_ve_haberlesme",
            "haberleşme": "elektronik_ve_haberlesme",
            "ehm": "elektronik_ve_haberlesme",
            "bilgisayar": "bilgisayar_muhendisligi",
            "makine": "makine_muhendisligi",
            "endüstri": "endustri_muhendisligi",
            "mekatronik": "mekatronik_muhendisligi",
            "kimya": "kimya_muhendisligi",
            "biyomühendislik": "biyomuhendislik",
            "gıda": "gida_muhendisligi",
            "matematik": "matematik_muhendisligi",
            "metalurji": "metalurji_ve_malzeme",
            "elektrik": "elektrik_muhendisligi",
            "kontrol": "kontrol_ve_otomasyon",
            "biyomedikal": "biyomedikal_muhendisligi",
            "yapay zeka": "yapay_zeka_ve_veri",
            # İnşaat Fakültesi
            "inşaat": "insaat_muhendisligi",
            "insaat": "insaat_muhendisligi",
            "inm": "insaat_muhendisligi",
            "çevre": "cevre_muhendisligi",
            "cevre": "cevre_muhendisligi",
            "cem": "cevre_muhendisligi",
            "harita": "harita_muhendisligi",
            "geomatik": "harita_muhendisligi",
            "hrm": "harita_muhendisligi",
            # Gemi İnşaatı ve Denizcilik Fakültesi
            "gemi makineleri işletme": "gemi_makineleri_isletme_muhendisligi",
            "gemi makinaları işletme": "gemi_makineleri_isletme_muhendisligi",
            "gmim": "gemi_makineleri_isletme_muhendisligi",
            "vardiya": "gemi_makineleri_isletme_muhendisligi",
            "çarkçı": "gemi_makineleri_isletme_muhendisligi",
            "gemi inşaatı": "gemi_insaati_ve_gemi_makineleri_muhendisligi",
            "gemi insaati": "gemi_insaati_ve_gemi_makineleri_muhendisligi",
            "gim": "gemi_insaati_ve_gemi_makineleri_muhendisligi",
            "gemi": "gemi_insaati_ve_gemi_makineleri_muhendisligi",
            # Mimarlık Fakültesi
            "şehir ve bölge planlama": "sehir_ve_bolge_planlama",
            "sehir ve bolge planlama": "sehir_ve_bolge_planlama",
            "şehir planlama": "sehir_ve_bolge_planlama",
            "sehir planlama": "sehir_ve_bolge_planlama",
            "sbp": "sehir_ve_bolge_planlama",
            "endüstriyel tasarım": "endustriyel_tasarim",
            "endustriyel tasarim": "endustriyel_tasarim",
            "endüstri ürünleri tasarımı": "endustriyel_tasarim",
            "ürün tasarımı": "endustriyel_tasarim",
            "ent": "endustriyel_tasarim",
            "mimarlık": "mimarlik",
            "mimarlik": "mimarlik",
            "mim": "mimarlik",
            # İktisadi ve İdari Bilimler Fakültesi (İİBF)
            "siyaset bilimi ve uluslararası ilişkiler": "siyaset_bilimi_ve_uluslararasi_iliskiler",
            "siyaset bilimi": "siyaset_bilimi_ve_uluslararasi_iliskiler",
            "uluslararası ilişkiler": "siyaset_bilimi_ve_uluslararasi_iliskiler",
            "uluslararasi iliskiler": "siyaset_bilimi_ve_uluslararasi_iliskiler",
            "sbui": "siyaset_bilimi_ve_uluslararasi_iliskiler",
            "sbu": "siyaset_bilimi_ve_uluslararasi_iliskiler",
            "iktisat": "iktisat",
            "ekonomi": "iktisat",
            "ikt": "iktisat",
            "işletme": "isletme",
            "isletme": "isletme",
            "isl": "isletme",
            # Sanat ve Tasarım Fakültesi
            "müzik ve sahne sanatları": "muzik_ve_sahne_sanatlari",
            "muzik ve sahne sanatlari": "muzik_ve_sahne_sanatlari",
            "ses sanatları tasarımı": "muzik_ve_sahne_sanatlari",
            "ses sanatları": "muzik_ve_sahne_sanatlari",
            "müzik toplulukları": "muzik_ve_sahne_sanatlari",
            "müzik": "muzik_ve_sahne_sanatlari",
            "muzik": "muzik_ve_sahne_sanatlari",
            "dans": "muzik_ve_sahne_sanatlari",
            "mssb": "muzik_ve_sahne_sanatlari",
            "iletişim ve tasarımı": "iletisim_tasarimi",
            "iletişim tasarımı": "iletisim_tasarimi",
            "iletisim tasarimi": "iletisim_tasarimi",
            "ilts": "iletisim_tasarimi",
            "bileşik sanatlar": "sanat",
            "bilesik sanatlar": "sanat",
            "grafik tasarımı": "sanat",
            "grafik tasarimi": "sanat",
            "grafik": "sanat",
            "fotoğraf ve video": "sanat",
            "fotograf ve video": "sanat",
            "sanat ve kültür yönetimi": "sanat",
            "sab": "sanat",
            "sanat": "sanat"
        }

        detected_dept = None
        for k, folder in dept_keywords.items():
            if k in q_lower:
                detected_dept = folder
                break

        # Güvenli Regex Yarıyıl Tespiti (Örn: "3. yarıyıl", "3 yarıyıl", "5. dönem")
        sem_num = None
        m_yariyil = re.search(r'\b([1-8])\.?\s*(yarıyıl|yariyil|dönem|donem)\b', q_lower)
        if m_yariyil:
            sem_num = int(m_yariyil.group(1))
        else:
            # Sınıf + Güz/Bahar Tespiti (Örn: "2. sınıf güz" -> 3, "1. sınıf bahar" -> 2)
            m_sinif = re.search(r'\b([1-4])\.?\s*sınıf\b', q_lower)
            if m_sinif:
                s_val = int(m_sinif.group(1))
                if "bahar" in q_lower:
                    sem_num = s_val * 2
                elif "güz" in q_lower or "guz" in q_lower:
                    sem_num = (s_val * 2) - 1

        sem_file = f"{sem_num}_yariyil.md" if sem_num else None
        return detected_dept, sem_file

    def search(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        """Kullanıcı sorusuyla en alakalı döküman parçalarını seçer ve döküman çeşitliliği sağlar."""
        if not self.chunks or not self.bm25:
            return []

        tokens = tokenize(query)
        if not tokens:
            return []

        raw_matches = self.bm25.score(tokens, top_k=50)
        if not raw_matches:
            return []

        selected: List[DocumentChunk] = []
        seen_files: set = set()
        
        has_mevzuat = False
        has_bolum = False

        q_lower = tr_lower(query)
        is_academic_query = any(w in q_lower for w in ["hak", "izinli", "yönetmelik", "ders alma", "irregular", "iys", "hazırlık", "mazeret", "yaz okulu", "çap", "yandal", "staj"])

        for c in raw_matches:
            if c.file_path not in seen_files:
                selected.append(c)
                seen_files.add(c.file_path)
                if "01_mevzuat" in c.file_path:
                    has_mevzuat = True
                if "05_fakulteler" in c.file_path:
                    has_bolum = True
            if len(selected) >= top_k:
                break

        # 2. Eğer mevzuat sorusuysa ve seçilenler arasında 01_mevzuat yoksa doğrudan mevzuatı ekle
        if is_academic_query and not has_mevzuat:
            mevzuat_matches = [c for c in self.chunks if "01_mevzuat" in c.file_path]
            if mevzuat_matches:
                mevzuat_bm25 = SimpleBM25(mevzuat_matches)
                best_mevzuat = mevzuat_bm25.score(tokens, top_k=1)
                if best_mevzuat and best_mevzuat[0] not in selected:
                    selected.append(best_mevzuat[0])

        # 3. Akıllı Müfredat ve Bologna Yönlendirmesi
        detected_dept_folder, detected_sem_file = self._extract_semester_and_department(q_lower)
        if detected_dept_folder and detected_sem_file:
            for c in self.chunks:
                if detected_dept_folder in c.file_path and detected_sem_file in c.file_path:
                    if "ders listesi" in tr_lower(c.section) or "|" in c.content:
                        if c in selected:
                            selected.remove(c)
                        selected.insert(0, c)
                        has_bolum = True
                        break

        # 4. Bölüm sorusuysa ve henüz bölüm dökümanı yoksa bölüm ekle
        if detected_dept_folder and not has_bolum:
            dept_matches = [c for c in self.chunks if "05_fakulteler" in c.file_path and detected_dept_folder in c.file_path]
            if dept_matches:
                dept_bm25 = SimpleBM25(dept_matches)
                best_dept = dept_bm25.score(tokens, top_k=1)
                if best_dept and best_dept[0] not in selected:
                    selected.append(best_dept[0])

        return [{
            "file_path": c.file_path,
            "title": c.title,
            "section": c.section,
            "content": c.content,
            "tier": c.tier,
            "metadata": c.metadata
        } for c in selected]
