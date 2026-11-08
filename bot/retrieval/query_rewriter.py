import re
from typing import List, Dict, Optional

COURSE_CODE_REGEX = re.compile(r'\b([A-ZÇĞİÖŞÜ]{2,4}\s*\d{3,4})\b', re.IGNORECASE)

FOLLOW_UP_INDICATORS = [
    "önkoşul", "onkosul", "kredi", "akts", "kalırsam", "kalirsam",
    "geçme", "gecme", "hangi dönem", "hangi donem", "hangi yarıyıl",
    "kimler alabilir", "zorunlu mu", "seçmeli mi", "hocası", "hocasi",
    "peki", "o ders", "bu ders", "bunun", "şunun", "onun", "içeriği"
]

def extract_course_codes(text: str) -> List[str]:
    """Metin içindeki BLM2012, EHM3011, MAT1071 gibi ders kodlarını yakalar."""
    matches = COURSE_CODE_REGEX.findall(text)
    return [m.replace(" ", "").upper() for m in matches]

def rewrite_query_with_history(query: str, history: Optional[List[Dict[str, str]]] = None) -> str:
    """
    Kullanıcı bir takip sorusu sorduysa (örn: 'Peki önkoşulu var mı?'),
    sohbet geçmişindeki son ders veya konuyu sorguya enjekte ederek
    RAG arama motorunun doğru bağlamı yakalamasını sağlar.
    """
    if not history:
        return query

    q_lower = query.lower()
    is_follow_up = any(ind in q_lower for ind in FOLLOW_UP_INDICATORS) or len(query.split()) <= 4

    # Eğer sorguda zaten bir ders kodu açıkça geçiyorsa değiştirmeye gerek yok
    current_codes = extract_course_codes(query)
    if current_codes:
        return query

    if not is_follow_up:
        return query

    # Geçmişteki mesajları sondan başa doğru tara
    detected_code = None
    for turn in reversed(history):
        content = turn.get("content", "")
        codes = extract_course_codes(content)
        if codes:
            detected_code = codes[0]
            break

    if detected_code:
        enhanced_query = f"{detected_code} {query}"
        return enhanced_query

    return query
