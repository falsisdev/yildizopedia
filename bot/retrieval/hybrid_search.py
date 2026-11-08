import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from bot.config import BASE_DIR
from bot.retrieval.query_rewriter import extract_course_codes

logger = logging.getLogger("yildizopedia.retrieval.hybrid")

class PrerequisiteGraphRetriever:
    """Derlenmiş önkoşul grafı (data/prerequisites_graph.json) üzerinden anlık doğrudan bilgi getirici."""

    def __init__(self, graph_path: Optional[Path] = None):
        if graph_path is None:
            graph_path = BASE_DIR / "data" / "prerequisites_graph.json"
        self.graph_path = graph_path
        self.graph: Dict[str, Any] = {}
        self.load_graph()

    def load_graph(self):
        if self.graph_path.exists():
            try:
                with open(self.graph_path, "r", encoding="utf-8") as f:
                    self.graph = json.load(f)
                logger.info(f"Önkoşul Grafı yüklendi: {len(self.graph)} ders aktif.")
            except Exception as e:
                logger.warning(f"Önkoşul grafı yüklenemedi: {e}")

    def lookup_course(self, course_code: str) -> Optional[Dict[str, Any]]:
        """Ders kodunu (örn. BLM2012) grafta arar."""
        normalized = course_code.replace(" ", "").upper()
        return self.graph.get(normalized)

    def get_prerequisite_context(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Sorguda geçen ders kodunu graftan bulur ve doğrudan yapısal bir
        RAG bağlam parçasına (DocumentChunk formatında) dönüştürür.
        """
        if not self.graph:
            return None

        codes = extract_course_codes(query)
        for code in codes:
            match = self.lookup_course(code)
            if match:
                prereq_info = match.get("prerequisite") or "Önkoşulsuz (Doğrudan Alınabilir)"
                content = (
                    f"Resmi Ders Kodu: {code}\n"
                    f"Ders Adı: {match.get('name')}\n"
                    f"Resmi Önkoşul Durumu: {prereq_info}\n"
                    f"Müfredat Belgesi: {match.get('source_file')}"
                )
                return {
                    "file_path": match.get("source_file", "data/prerequisites_graph.json"),
                    "title": f"{code} - {match.get('name')}",
                    "section": "Resmi Bologna Önkoşul Bilgisi",
                    "content": content,
                    "tier": "Tier 2 (Resmi Bologna Bilgi Sistemi Grafı)",
                    "metadata": match
                }
        return None
