import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("yildizopedia.compiler")

BASE_DIR = Path(__file__).resolve().parent.parent

EXCLUDED_DIRS = {
    ".git", ".system_generated", "bot", "scratch", "venv", ".venv",
    "__pycache__", "chroma_db", "chroma_data", "data_cache", "build",
    "dist", "var", "path", "tests"
}

def fix_broken_links_globally():
    """Tüm markdown dosyalarındaki mutlak 'file:///Users/...' linklerini göreli temiz linklere dönüştürür."""
    count = 0
    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for file in files:
            if not file.endswith(".md"):
                continue
            filepath = Path(root) / file
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                continue

            if "file:///Users" in content:
                # file:///Users/.../Docs/.../00_genel_ve_kurumsal/xyz.md -> 00_genel_ve_kurumsal/xyz.md
                fixed = re.sub(r'file:///Users/[^\)]*?/(0[0-5]_[^\)]+)', r'\1', content)
                fixed = re.sub(r'file:///Users/[^\)]*?/(arsiv/[^\)]+)', r'\1', fixed)
                fixed = re.sub(r'file:///Users/[^\)]*?/(ROUTER_GUIDE\.md|INDEX\.md|README\.md)', r'\1', fixed)
                if fixed != content:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(fixed)
                    count += 1

    logger.info(f"✅ Toplam {count} adet Markdown dosyasındaki kırık mutlak yerel linkler düzeltildi.")

def enrich_missing_frontmatter_tiers():
    """Frontmatter'ında guvenilirlik_duzeyi eksik olan dosyalara standart Tier ekler."""
    enriched_count = 0
    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for file in files:
            if not file.endswith(".md") or file in ["README.md", "INDEX.md", "ROUTER_GUIDE.md", "AGENT_INSTRUCTIONS.md"]:
                continue
            filepath = Path(root) / file
            rel_path = str(filepath.relative_to(BASE_DIR)).lower()

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                continue

            if not content.startswith("---"):
                continue

            if "guvenilirlik_duzeyi" not in content[:500]:
                tier = "Tier 1 (Resmi Mevzuat ve Senato Kararları)"
                if "ogrenci_topluluklari" in rel_path or "itiraf" in rel_path or "reddit" in rel_path:
                    tier = "Tier 4 (Düşük Güvenilirlik / Gayriresmî Öğrenci Deneyimi)"
                elif "vikipedi" in rel_path or "taban_puan" in rel_path:
                    tier = "Tier 3 (İkincil / İstatistiki Kaynak)"
                elif "05_fakulteler" in rel_path or "bologna" in rel_path or "03_yabanci" in rel_path:
                    tier = "Tier 2 (Resmi Üniversite Portalı ve Bologna Bilgi Sistemi)"

                # --- sonrasına ekle
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    yaml_part = parts[1].rstrip()
                    new_yaml = yaml_part + f'\nguvenilirlik_duzeyi: "{tier}"\n'
                    new_content = "---" + new_yaml + "---" + parts[2]
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    enriched_count += 1

    logger.info(f"✅ {enriched_count} adet dosyanın frontmatter'ına resmî güvenilirlik derecesi (Tier) eklendi.")

def compile_prerequisites_graph() -> Dict[str, Any]:
    """Tüm yarıyıl markdown tablolarındaki önkoşul verilerini çıkarıp graph JSON'ı derler."""
    graph: Dict[str, Any] = {}
    fakulteler_dir = BASE_DIR / "05_fakulteler_ve_bolumler"
    if not fakulteler_dir.exists():
        return graph

    for root, _, files in os.walk(fakulteler_dir):
        for file in files:
            if not file.endswith("_yariyil.md"):
                continue
            fpath = Path(root) / file
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    lines = f.readlines()
            except Exception:
                continue

            for line in lines:
                if not line.strip().startswith("|") or "---" in line or "Ders Kodu" in line:
                    continue
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 3:
                    code_raw = parts[0].replace("*", "")
                    prereq_raw = parts[1].replace("*", "")
                    name_raw = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', parts[2]).replace("*", "")

                    if code_raw and len(code_raw) >= 3:
                        graph[code_raw] = {
                            "name": name_raw,
                            "prerequisite": prereq_raw if prereq_raw not in ["-", "Yok", "yok", ""] else None,
                            "source_file": str(fpath.relative_to(BASE_DIR))
                        }

    out_file = BASE_DIR / "data" / "prerequisites_graph.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)

    logger.info(f"✅ Ders Önkoşul Grafı derlendi: {len(graph)} ders kaydedildi ({out_file.relative_to(BASE_DIR)}).")
    return graph

def update_kb_statistics() -> Dict[str, int]:
    """Bilgi bankasındaki toplam markdown dosya ve kelime sayısını hesaplar."""
    md_count = 0
    total_words = 0

    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for file in files:
            if file.endswith(".md"):
                md_count += 1
                fpath = Path(root) / file
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        total_words += len(f.read().split())
                except Exception:
                    pass

    logger.info(f"📊 Bilgi Bankası İstatistiği: {md_count} Markdown dosyası, {total_words:,} toplam kelime.")
    return {"md_count": md_count, "total_words": total_words}

def run_compiler():
    logger.info("🚀 Yıldızopedia Veri ve Dokümantasyon Derleyici Başlatılıyor...")
    fix_broken_links_globally()
    enrich_missing_frontmatter_tiers()
    compile_prerequisites_graph()
    update_kb_statistics()
    logger.info("🎉 Derleme işlemi başarıyla tamamlandı.")

if __name__ == "__main__":
    run_compiler()
