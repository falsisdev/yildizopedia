import sqlite3
from datetime import datetime, timezone, timedelta
from typing import Tuple, Dict, Any
from bot.config import SQLITE_DB_PATH, ADMIN_TELEGRAM_ID, DAILY_QUESTION_LIMIT

# Türkiye Saati (UTC+3)
TR_TZ = timezone(timedelta(hours=3))

def get_today_str() -> str:
    """Türkiye yerel saatine göre YYYY-MM-DD döner."""
    return datetime.now(TR_TZ).strftime("%Y-%m-%d")

class Database:
    def __init__(self, db_path=SQLITE_DB_PATH):
        self.db_path = str(db_path)
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            # Kullanıcılar tablosu
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_active TEXT,
                created_at TEXT
            )
            """)
            
            # Günlük kullanım kotaları tablosu
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_usage (
                telegram_id INTEGER,
                date TEXT,
                count INTEGER DEFAULT 0,
                PRIMARY KEY (telegram_id, date)
            )
            """)
            
            # Soru logları tablosu
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS query_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER,
                query TEXT,
                model_used TEXT,
                source_file TEXT,
                created_at TEXT
            )
            """)
            conn.commit()
        finally:
            conn.close()

    def check_user_quota(self, telegram_id: int) -> Tuple[bool, int, bool]:
        """
        Kullanıcının soru sorma hakkını kontrol eder.
        Döner: (izin_var_mi, kalan_hak, admin_mi)
        """
        is_admin = (telegram_id == ADMIN_TELEGRAM_ID)
        if is_admin:
            return True, 9999, True

        today = get_today_str()
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT count FROM daily_usage WHERE telegram_id = ? AND date = ?",
                (telegram_id, today)
            )
            row = cursor.fetchone()
            current_count = row["count"] if row else 0
        finally:
            conn.close()

        remaining = max(0, DAILY_QUESTION_LIMIT - current_count)
        is_allowed = (current_count < DAILY_QUESTION_LIMIT)
        return is_allowed, remaining, False

    def record_query(
        self,
        telegram_id: int,
        username: str,
        first_name: str,
        query: str,
        model_used: str,
        source_file: str = ""
    ) -> int:
        """
        Soruyu kaydeder ve günlük sayacı 1 artırır. Kalan hakkı döner.
        """
        today = get_today_str()
        now_str = datetime.now(TR_TZ).strftime("%Y-%m-%d %H:%M:%S")

        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            # 1. Kullanıcıyı güncelle veya ekle
            cursor.execute("""
            INSERT INTO users (telegram_id, username, first_name, last_active, created_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET
                username = excluded.username,
                first_name = excluded.first_name,
                last_active = excluded.last_active
            """, (telegram_id, username or "", first_name or "", now_str, now_str))

            # 2. Günlük sayacı artır
            cursor.execute("""
            INSERT INTO daily_usage (telegram_id, date, count)
            VALUES (?, ?, 1)
            ON CONFLICT(telegram_id, date) DO UPDATE SET
                count = count + 1
            """, (telegram_id, today))

            # 3. Log kaydet
            cursor.execute("""
            INSERT INTO query_logs (telegram_id, query, model_used, source_file, created_at)
            VALUES (?, ?, ?, ?, ?)
            """, (telegram_id, query, model_used, source_file, now_str))

            # Kalan hakkı hesapla
            cursor.execute(
                "SELECT count FROM daily_usage WHERE telegram_id = ? AND date = ?",
                (telegram_id, today)
            )
            row = cursor.fetchone()
            new_count = row["count"] if row else 1
            conn.commit()
        finally:
            conn.close()

        if telegram_id == ADMIN_TELEGRAM_ID:
            return 9999
        return max(0, DAILY_QUESTION_LIMIT - new_count)

    def get_stats(self) -> Dict[str, Any]:
        """Yönetici için kullanım istatistiklerini hesaplar."""
        today = get_today_str()
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            # Toplam kayıtlı kullanıcı
            cursor.execute("SELECT COUNT(*) AS total_users FROM users")
            total_users = cursor.fetchone()["total_users"]

            # Bugün aktif olan kullanıcılar
            cursor.execute("SELECT COUNT(DISTINCT telegram_id) AS active_today FROM daily_usage WHERE date = ?", (today,))
            active_today = cursor.fetchone()["active_today"]

            # Bugün sorulan toplam soru
            cursor.execute("SELECT SUM(count) AS questions_today FROM daily_usage WHERE date = ?", (today,))
            row = cursor.fetchone()
            questions_today = row["questions_today"] if row and row["questions_today"] else 0

            # Genel toplam soru
            cursor.execute("SELECT COUNT(*) AS all_time_queries FROM query_logs")
            all_time_queries = cursor.fetchone()["all_time_queries"]

            # En son 5 soru logu
            cursor.execute(
                "SELECT query, model_used, created_at FROM query_logs ORDER BY id DESC LIMIT 5"
            )
            recent_logs = [dict(r) for r in cursor.fetchall()]
        finally:
            conn.close()

        return {
            "today": today,
            "total_users": total_users,
            "active_today": active_today,
            "questions_today": questions_today,
            "all_time_queries": all_time_queries,
            "recent_logs": recent_logs
        }
