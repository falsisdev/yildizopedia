#!/usr/bin/env python3
"""
Yıldızopedia Telegram Botu & RAG Alt Sistemleri Doğrulama Testi
"""

import os
import sys
import unittest
from pathlib import Path

# Proje kök dizinini ekle
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from bot.config import ADMIN_TELEGRAM_ID, DAILY_QUESTION_LIMIT
from bot.database import Database
from bot.rag_engine import RAGEngine
from bot.llm_client import LLMClient

class TestBotSubsystems(unittest.TestCase):
    def setUp(self):
        # Test amaçlı geçici sqlite db
        self.test_db_path = BASE_DIR / "test_bot_data.sqlite3"
        if self.test_db_path.exists():
            self.test_db_path.unlink()
        self.db = Database(self.test_db_path)

    def tearDown(self):
        if self.test_db_path.exists():
            self.test_db_path.unlink()

    def test_database_quota_and_admin(self):
        """Kullanıcı kotası ve admin ayrıcalıklarını doğrula."""
        normal_user_id = 99999999
        admin_id = ADMIN_TELEGRAM_ID

        # Başlangıçta 15 hak olmalı
        allowed, remaining, is_admin = self.db.check_user_quota(normal_user_id)
        self.assertTrue(allowed)
        self.assertEqual(remaining, DAILY_QUESTION_LIMIT)
        self.assertFalse(is_admin)

        # 15 soru sorulunca kotanın bitmesi
        for i in range(DAILY_QUESTION_LIMIT):
            rem = self.db.record_query(
                telegram_id=normal_user_id,
                username="test_user",
                first_name="Test",
                query=f"Soru {i+1}",
                model_used="Groq (Llama 3.3 70B)",
                source_file="02_ogrenci_isleri_ogi/test.md"
            )
            self.assertEqual(rem, DAILY_QUESTION_LIMIT - (i + 1))

        # 16. soruda izin verilmemeli
        allowed, remaining, is_admin = self.db.check_user_quota(normal_user_id)
        self.assertFalse(allowed)
        self.assertEqual(remaining, 0)

        # Admin kontrolü
        admin_allowed, admin_rem, admin_flag = self.db.check_user_quota(admin_id)
        self.assertTrue(admin_allowed)
        self.assertTrue(admin_flag)
        self.assertEqual(admin_rem, 9999)

        # İstatistikler testi
        stats = self.db.get_stats()
        self.assertEqual(stats["total_users"], 1)
        self.assertEqual(stats["active_today"], 1)
        self.assertEqual(stats["questions_today"], 15)

    def test_rag_engine_search(self):
        """407 dökümandan indekslenen parçaları ve arama doğruluğunu test et."""
        rag = RAGEngine(BASE_DIR)
        self.assertGreater(len(rag.chunks), 800)

        # Mazeret sorgusu
        res = rag.search("mazeret sınavı başvuru süresi")
        self.assertGreater(len(res), 0)
        self.assertIn("mazeret", res[0]["content"].lower() + res[0]["file_path"].lower())

        # Kimya Mühendisliği Staj sorgusu
        res = rag.search("kimya mühendisliği staj")
        self.assertGreater(len(res), 0)
        self.assertIn("kimya", res[0]["file_path"].lower() + res[0]["title"].lower())

    def test_gitignore_contains_intentional_exclusion(self):
        """Veritabanı ve gizli anahtarların gitignore'da olduğunu, resmi belgelerin ise açık olduğunu doğrula."""
        gitignore_path = BASE_DIR / ".gitignore"
        self.assertTrue(gitignore_path.exists())
        with open(gitignore_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Gizli kalması gerekenler
        self.assertIn("chroma_db/", content)
        self.assertIn("*.sqlite3", content)
        self.assertIn(".env", content)

        # GitHub'a açık olması gerekenler (gitignore'da olmamalı)
        self.assertNotIn("05_fakulteler_ve_bolumler/", content)
        self.assertNotIn("01_mevzuat_ve_yonetmelikler/", content)

if __name__ == "__main__":
    unittest.main()
