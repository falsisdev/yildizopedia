import os
import sys
from pathlib import Path
from typing import List, Tuple

try:
    import frontmatter
except ImportError:
    frontmatter = None

BASE_DIR = Path(__file__).resolve().parent.parent

EXCLUDED_DIRS = {
    ".git", ".system_generated", "bot", "scratch", "venv", ".venv",
    "__pycache__", "chroma_db", "chroma_data", "data_cache", "build",
    "dist", "var", "path", "tests"
}

VALID_TIERS = ["Tier 1", "Tier 2", "Tier 3", "Tier 4"]

def validate_knowledge_base() -> bool:
    print("==================================================================")
    print("🔍 Yıldızopedia Bilgi Bankası Standartları ve Bütünlük Doğrulaması")
    print("==================================================================")

    total_files = 0
    missing_frontmatter: List[str] = []
    invalid_tier: List[Tuple[str, str]] = []
    broken_links: List[Tuple[str, int]] = []
    empty_files: List[str] = []

    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for file in files:
            if not file.endswith(".md"):
                continue

            rel_path = os.path.relpath(os.path.join(root, file), BASE_DIR)
            # Kök dizin rehber dosyaları frontmatter gerektirmez
            if rel_path in ["README.md", "INDEX.md", "ROUTER_GUIDE.md", "AGENT_INSTRUCTIONS.md"]:
                continue

            total_files += 1
            full_path = os.path.join(root, file)
            size = os.path.getsize(full_path)

            if size < 40:
                empty_files.append(rel_path)
                continue

            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    text = f.read()
            except Exception as e:
                print(f"❌ Dosya okuma hatası ({rel_path}): {e}")
                continue

            # Kırık mutlak yerel link kontrolü
            if "file:///Users" in text:
                broken_count = text.count("file:///Users")
                broken_links.append((rel_path, broken_count))

            # Frontmatter kontrolü
            if not text.startswith("---"):
                missing_frontmatter.append(rel_path)
                continue

            # Tier kontrolü
            has_valid_tier = False
            for tier in VALID_TIERS:
                if tier in text[:400]:
                    has_valid_tier = True
                    break

            if not has_valid_tier:
                tier_line = ""
                for line in text[:400].split("\n"):
                    if "guvenilirlik" in line.lower():
                        tier_line = line.strip()
                        break
                invalid_tier.append((rel_path, tier_line or "Tanımsız Tier"))

    print(f"📄 Toplam İncelenen Bilgi Dosyası: {total_files}")
    print(f"✅ Frontmatter İçeren Dosya: {total_files - len(missing_frontmatter)}")

    if broken_links:
        print(f"\n⚠️  {len(broken_links)} dosyada mutlak dosya linki tespit edildi:")
        for f, cnt in broken_links[:5]:
            print(f"   • {f} ({cnt} adet link)")

    if missing_frontmatter:
        print(f"\nℹ️  Frontmatter içermeyen bölüm README'leri: {len(missing_frontmatter)} adet")

    if invalid_tier:
        print(f"\n⚠️  Geçersiz veya eksik Tier tanımlı dosyalar: {len(invalid_tier)} adet")
        for f, t in invalid_tier[:5]:
            print(f"   • {f} -> {t}")

    if empty_files:
        print(f"\n❌ Boş / Çok Küçük Dosyalar: {len(empty_files)} adet")
        for f in empty_files:
            print(f"   • {f}")
        return False

    print("\n==================================================================")
    print("🎉 BİLGİ BANKASI DOĞRULAMASI BAŞARIYLA TAMAMLANDI!")
    print("==================================================================")
    return True

if __name__ == "__main__":
    success = validate_knowledge_base()
    sys.exit(0 if success else 1)
