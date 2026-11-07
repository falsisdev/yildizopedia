import os
from pathlib import Path

# Proje kök dizini
BASE_DIR = Path(__file__).resolve().parent.parent

def load_env_file(filepath: Path = None):
    """
    python-dotenv kurulu olmasa bile .env dosyasını güvenle yükleyen hafif okuyucu.
    """
    if filepath is None:
        filepath = BASE_DIR / ".env"
    
    if not filepath.exists():
        return

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key not in os.environ:
                os.environ[key] = val

# Ortam değişkenlerini yükle
load_env_file()

# Konfigürasyon Değerleri
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
ADMIN_TELEGRAM_ID = int(os.getenv("ADMIN_TELEGRAM_ID", "0"))
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
DAILY_QUESTION_LIMIT = int(os.getenv("DAILY_QUESTION_LIMIT", "15"))

GITHUB_REPO_URL = os.getenv("GITHUB_REPO_URL", "https://github.com/falsisdev/yildizopedia").strip().rstrip("/")
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "main").strip()

KNOWLEDGE_BASE_DIR = Path(os.getenv("KNOWLEDGE_BASE_DIR", str(BASE_DIR)))
if not KNOWLEDGE_BASE_DIR.is_absolute():
    KNOWLEDGE_BASE_DIR = BASE_DIR / KNOWLEDGE_BASE_DIR

DATA_CACHE_DIR = BASE_DIR / "data_cache"

SQLITE_DB_PATH = Path(os.getenv("SQLITE_DB_PATH", "bot_data.sqlite3"))
if not SQLITE_DB_PATH.is_absolute():
    SQLITE_DB_PATH = BASE_DIR / SQLITE_DB_PATH

CHROMA_PERSIST_DIR = Path(os.getenv("CHROMA_PERSIST_DIR", "chroma_db"))
if not CHROMA_PERSIST_DIR.is_absolute():
    CHROMA_PERSIST_DIR = BASE_DIR / CHROMA_PERSIST_DIR
