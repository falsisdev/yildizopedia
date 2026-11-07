import os
import re
import math
import io
import zipfile
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Dict, Any, Tuple
from bot.config import KNOWLEDGE_BASE_DIR, CHROMA_PERSIST_DIR, GITHUB_REPO_URL, GITHUB_BRANCH, DATA_CACHE_DIR

EXCLUDED_DIRS = {".git", ".system_generated", "bot", "scratch", "venv", ".venv", "__pycache__", "chroma_db", "chroma_data"}
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

class DocumentChunk:
    def __init__(self, file_path: str, title: str, section: str, content: str, tier: str = "Tier 1"):
        self.file_path = file_path
        self.title = title
        self.section = section
        self.content = content
        self.tier = tier
        self.tokens = tokenize(content + " " + title + " " + section)

class SimpleBM25:
    """Saf Python Okapi BM25 Arama Motoru."""
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
        results = [self.chunks[i] for i in ranked_indices if scores[i] > 0]
        return results[:top_k] if results else self.chunks[:top_k]

class RAGEngine:
    def __init__(self, kb_dir: Path = KNOWLEDGE_BASE_DIR):
        self.kb_dir = kb_dir
        self.chunks: List[DocumentChunk] = []
        self.bm25: SimpleBM25 = None
        self.last_sync_info = "Henüz senkronize edilmedi."
        
        # 1. Başlangıçta GitHub'dan en güncel veriyi çekmeyi dene
        self.sync_from_github()
        
        # 2. İndeksle
        self._load_and_index_documents()

    def sync_from_github(self) -> Tuple[bool, str]:
        """
        github.com/falsisdev/yildizopedia reposundan en güncel dökümanları senkronize eder.
        Eğer yerel git reposu mevcutsa 'git pull' ile anında (0.2 sn) günceller.
        Tekil binary modunda ise zip arşivini indirir.
        """
        import subprocess
        from bot.config import BASE_DIR

        # 1. Eğer yerel git deposu varsa doğrudan hızlı git pull yap
        git_dir = BASE_DIR / ".git"
        if git_dir.exists():
            try:
                print(f"[Git Senkronizasyonu]: 'git pull origin {GITHUB_BRANCH}' çalıştırılıyor...")
                res = subprocess.run(
                    ["git", "pull", "origin", GITHUB_BRANCH],
                    cwd=str(BASE_DIR),
                    capture_output=True,
                    text=True,
                    timeout=8
                )
                if res.returncode == 0:
                    self.kb_dir = KNOWLEDGE_BASE_DIR
                    self._load_and_index_documents()
                    status_text = res.stdout.strip().split("\n")[-1]
                    msg = f"✅ Git Senkronizasyonu Başarılı: {status_text}"
                    print(f"[Git Senkronizasyonu]: {msg}")
                    self.last_sync_info = msg
                    return True, msg
            except Exception as e:
                print(f"[Git Senkronizasyon Uyarısı]: {e}")

        # 2. Standart ZIP İndirme (Git olmayan ortamlar için)
        zip_url = f"{GITHUB_REPO_URL}/archive/refs/heads/{GITHUB_BRANCH}.zip"
        req = urllib.request.Request(zip_url, headers={"User-Agent": "YildizopediaBot/1.0"})
        
        try:
            print(f"[GitHub ZIP Senkronizasyonu]: {zip_url} kontrol ediliyor...")
            with urllib.request.urlopen(req, timeout=12) as res:
                zip_bytes = io.BytesIO(res.read())

            target_dir = DATA_CACHE_DIR
            target_dir.mkdir(parents=True, exist_ok=True)
            extracted_count = 0

            with zipfile.ZipFile(zip_bytes) as z:
                for member in z.namelist():
                    parts = member.split("/", 1)
                    if len(parts) > 1 and parts[1]:
                        rel_path = parts[1]
                        if rel_path.endswith(".md"):
                            dest_file = target_dir / rel_path
                            dest_file.parent.mkdir(parents=True, exist_ok=True)
                            with z.open(member) as src, open(dest_file, "wb") as dst:
                                dst.write(src.read())
                            extracted_count += 1

            self.kb_dir = target_dir
            self._load_and_index_documents()
            msg = f"✅ GitHub ({GITHUB_REPO_URL}) üzerinden {extracted_count} adet güncel döküman başarıyla çekildi ve indekslendi."
            print(f"[GitHub Senkronizasyonu Başarılı]: {msg}")
            self.last_sync_info = msg
            return True, msg
        except Exception as e:
            msg = f"⚠️ GitHub ({GITHUB_REPO_URL}) senkronizasyonu yapılamadı ({e}). Yerel dökümanlar kullanılıyor."
            print(f"[GitHub Senkronizasyon Bildirimi]: {msg}")
            self.last_sync_info = msg
            return False, msg

    def _determine_tier(self, rel_path: str) -> str:
        if "reddit" in rel_path or "itiraf" in rel_path or "kariyer" in rel_path or "wikipedia" in rel_path:
            return "İkincil / Öğrenci Platformu (Tier 2)"
        return "Resmi Kurumsal Belge (Tier 1)"

    def _load_and_index_documents(self):
        """Tüm dökümanları hem ## hem de ### (Madde/Soru) bazında granüler parçalar olarak indeksler."""
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
                        text = f.read()
                except Exception:
                    continue

                tier = self._determine_tier(rel_path)
                chunks = self._chunk_markdown(text, rel_path, tier)
                all_chunks.extend(chunks)

        self.chunks = all_chunks
        if self.chunks:
            self.bm25 = SimpleBM25(self.chunks)

    def _chunk_markdown(self, text: str, rel_path: str, tier: str) -> List[DocumentChunk]:
        """Markdown dökümanını ## ve ### başlıklarına göre ayırır (Maddeler ve sorular izole edilir)."""
        sections = re.split(r'\n(?=###? )', text)
        doc_title = Path(rel_path).stem.replace("_", " ").title()
        chunks = []

        for s in sections:
            s_clean = s.strip()
            if not s_clean:
                continue
            lines = s_clean.split("\n")
            first_line = lines[0]

            if first_line.startswith("# ") and doc_title == Path(rel_path).stem.replace("_", " ").title():
                doc_title = first_line.replace("#", "").strip()

            sec_title = first_line.replace("#", "").strip() if first_line.startswith("#") else "Genel"
            content = "\n".join(lines[1:]).strip() if len(lines) > 1 else s_clean

            if len(content) > 35:
                chunks.append(DocumentChunk(rel_path, doc_title, sec_title, content, tier))

        if not chunks and text.strip():
            chunks.append(DocumentChunk(rel_path, doc_title, "Genel", text.strip(), tier))

        return chunks

    def search(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        """Kullanıcı sorusuyla en alakalı döküman parçalarını seçer ve döküman çeşitliliği sağlar."""
        if not self.chunks or not self.bm25:
            return []

        tokens = tokenize(query)
        raw_matches = self.bm25.score(tokens, top_k=50)

        # 1. Genel arama sonuçlarından en iyi parçaları topla (dosya başına max 1)
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

        # 3. Eğer bölüm adı geçiyorsa ve seçilenler arasında bölüm dökümanı yoksa bölümden ekle
        for dept in ["elektronik", "haberleşme", "makine", "endüstri", "mekatronik", "kimya", "biyomühendislik", "gıda", "matematik", "metalurji", "bilgisayar", "elektrik", "biyomedikal"]:
            if dept in q_lower and not has_bolum:
                dept_matches = [c for c in self.chunks if "05_fakulteler" in c.file_path and dept in tr_lower(c.file_path)]
                if dept_matches:
                    dept_bm25 = SimpleBM25(dept_matches)
                    best_dept = dept_bm25.score(tokens, top_k=1)
                    if best_dept and best_dept[0] not in selected:
                        selected.append(best_dept[0])
                break

        return [{
            "file_path": c.file_path,
            "title": c.title,
            "section": c.section,
            "content": c.content,
            "tier": c.tier
        } for c in selected]
