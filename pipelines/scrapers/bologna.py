import re
import ssl
import json
import logging
from typing import Dict, List, Any, Optional
import urllib.request
from bs4 import BeautifulSoup

logger = logging.getLogger("yildizopedia.pipeline.bologna")

class BolognaScraper:
    """YTÜ Bologna Bilgi Paketi genel ve modüler kazıyıcı motoru."""

    def __init__(self, base_url: str = "http://www.bologna.yildiz.edu.tr/index.php"):
        self.base_url = base_url.rstrip("/")
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def fetch_program_courses(self, program_id: int, aid: int = 3) -> Dict[int, List[Dict[str, Any]]]:
        """
        Belirtilen Bologna lisans program ID'si için tüm yarıyılların ders listesini çeker.
        Döner: {1: [ders1, ders2, ...], 2: [...], ..., 8: [...]}
        """
        url = f"{self.base_url}?r=program/view&id={program_id}&aid={aid}"
        req = urllib.request.Request(url, headers=self.headers)
        
        try:
            with urllib.request.urlopen(req, context=self.ssl_context, timeout=20) as resp:
                html_content = resp.read().decode("utf-8", errors="ignore")
        except Exception as e:
            logger.error(f"Bologna program {program_id} çekilemedi: {e}")
            return {}

        soup = BeautifulSoup(html_content, "html.parser")
        semesters: Dict[int, List[Dict[str, Any]]] = {i: [] for i in range(1, 9)}

        # Bologna tabloları genellikle yarıyıl bazında class veya başlık içerir
        tables = soup.find_all("table")
        current_sem = 1

        for table in tables:
            caption = table.find("caption") or table.find_previous(["h3", "h4", "strong"])
            if caption:
                cap_text = caption.get_text()
                m = re.search(r'([1-8])\.\s*(Yarıyıl|Dönem|Semester)', cap_text, re.IGNORECASE)
                if m:
                    current_sem = int(m.group(1))

            rows = table.find_all("tr")
            for tr in rows:
                cols = tr.find_all("td")
                if len(cols) < 5:
                    continue

                code = cols[0].get_text(strip=True)
                if not code or len(code) < 3 or not re.search(r'[A-Z]{2,}', code):
                    continue

                # Tipik Bologna sütunları: Kod | Önkoşul | Ders Adı | T | U | L | Kredi | AKTS
                name_tag = cols[1].find("a") or (cols[2].find("a") if len(cols) > 2 else None)
                name = name_tag.get_text(strip=True) if name_tag else ""
                course_url = name_tag.get("href") if name_tag else ""

                prereq = "-"
                # Eğer 2. sütun önkoşul ise
                if len(cols) >= 6:
                    possible_prereq = cols[1].get_text(strip=True)
                    if possible_prereq and possible_prereq != name:
                        prereq = possible_prereq

                # Kredi ve AKTS yakalama
                akts = ""
                local_credit = ""
                try:
                    akts = cols[-1].get_text(strip=True)
                    local_credit = cols[-2].get_text(strip=True)
                except Exception:
                    pass

                semesters[current_sem].append({
                    "code": code,
                    "name": name,
                    "prereq": prereq,
                    "local_credit": local_credit,
                    "akts": akts,
                    "url": course_url
                })

        return semesters
