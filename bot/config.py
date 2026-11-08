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

admin_id_raw = os.getenv("ADMIN_TELEGRAM_ID", "0").strip()
try:
    ADMIN_TELEGRAM_ID = int(admin_id_raw) if admin_id_raw else 0
except ValueError:
    ADMIN_TELEGRAM_ID = 0

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

try:
    DAILY_QUESTION_LIMIT = int(os.getenv("DAILY_QUESTION_LIMIT", "15"))
except ValueError:
    DAILY_QUESTION_LIMIT = 15

GITHUB_REPO_URL = os.getenv("GITHUB_REPO_URL", "https://github.com/falsisdev/yildizopedia").strip().rstrip("/")
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "main").strip()

KNOWLEDGE_BASE_DIR = Path(os.getenv("KNOWLEDGE_BASE_DIR", str(BASE_DIR)))
if not KNOWLEDGE_BASE_DIR.is_absolute():
    KNOWLEDGE_BASE_DIR = BASE_DIR / KNOWLEDGE_BASE_DIR

db_env = os.getenv("SQLITE_DB_PATH", "var/bot_data.sqlite3").strip()
SQLITE_DB_PATH = Path(db_env)
if not SQLITE_DB_PATH.is_absolute():
    SQLITE_DB_PATH = BASE_DIR / SQLITE_DB_PATH

# Eğer var/bot_data.sqlite3 mevcutsa orayı garantiye al
if not SQLITE_DB_PATH.exists() and (BASE_DIR / "var" / "bot_data.sqlite3").exists():
    SQLITE_DB_PATH = BASE_DIR / "var" / "bot_data.sqlite3"
