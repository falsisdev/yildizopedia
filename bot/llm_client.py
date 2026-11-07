import json
import urllib.request
import urllib.error
import asyncio
from typing import List, Dict, Any, Tuple
from bot.config import GROQ_API_KEY, GEMINI_API_KEY

SYSTEM_PROMPT = """Sen Yıldız Teknik Üniversitesi (YTÜ) kurumsal hafızası ve akıllı öğrenci asistanı Yıldızopedia'sın.
Tavrın: Bürokratik veya aşırı çekinik DEĞİL; bilgili, samimi, çözüm odaklı, kıdemli bir Yıldızlı mentör ve akademik danışman gibidir.

Görevin:
1. Resmi Hükümler (Yönetmelik ve Mevzuat): Sana verilen bağlamdaki YTÜ yönetmeliklerini (Madde numaralarıyla), senato esaslarını ve resmi kuralları net olarak açıkla.
2. Taktiksel ve Akademik Rehberlik: Öğrenci "zorlanır mıyım, önerir misin, ortalamam nasıl etkilenir?" gibi deneyimsel ve stratejik sorular sorduğunda; YTÜ lisans sistemini (dönemlik dersler, önkoşul zincirleri, irregular olmanın ders yükü ve not ortalamasına etkisi) göz önüne alarak yapıcı, gerçekçi ve samimi bir analiz sun.
3. Haklar ve Seçenekler: Öğrencinin haklarını (örneğin Bahar döneminde derslere başlayabilme veya dilekçe vererek izinli sayılıp hiç ders almama hakkı gibi) açıkça belirt.

TELEGRAM FORMAT KURALLARI (ÇOK ÖNEMLİ):
- Asla Markdown başlıkları (#, ##, ###) veya '---' yatay çizgileri KULLANMA! Telegram bunları desteklemez ve çirkin görünür.
- Başlıklar için emoji ve kalın HTML etiketi kullan: Örn: 📌 <b>1. Ocak İYS Sonrası Lisansa Başlama</b>
- Maddeler için tire (-) veya yıldız (*) yerine '•' imi kullan (Örn: • <b>Ders Seçimi:</b> ...).
- Vurgulamak istediğin yerleri <b>kalın</b> veya <i>italik</i> yap.
- Yanıtın sonuna imza, kaynak veya dipnot ekleme; kaynak bilgilerini bot altyapısı otomatik olarak ekleyecektir.
"""

def _call_groq_sync(prompt: str, context: str) -> str:
    """Groq Cloud API (Llama 3.3 70B) senkron HTTP çağrısı."""
    if not GROQ_API_KEY or GROQ_API_KEY.startswith("gsk_placeholder"):
        raise ValueError("Groq API anahtarı girilmedi veya geçersiz.")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Aşağıdaki resmi YTÜ dökümanlarını kullanarak sorumu cevapla:\n\n[RESMİ BAĞLAM]:\n{context}\n\n[ÖĞRENCİ SORUSU]:\n{prompt}"}
        ],
        "temperature": 0.2,
        "max_tokens": 1024
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=12) as response:
        result = json.loads(response.read().decode("utf-8"))
        return result["choices"][0]["message"]["content"].strip()

def _call_gemini_sync(prompt: str, context: str) -> Tuple[str, str]:
    """Google AI Studio (Gemini Flash) senkron HTTP çağrısı. Döner: (cevap, model_adi)"""
    if not GEMINI_API_KEY:
        raise ValueError("Gemini API anahtarı girilmedi.")

    # Ultra hızlı, anında yanıt veren ve 503 yoğunluğu olmayan modeller
    models = ["gemini-flash-lite-latest", "gemini-3.8-flash", "gemini-flash-latest"]
    
    combined_prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Aşağıdaki resmi YTÜ dökümanlarını kullanarak sorumu cevapla:\n\n"
        f"[RESMİ BAĞLAM]:\n{context}\n\n"
        f"[ÖĞRENCİ SORUSU]:\n{prompt}"
    )
    
    payload = {
        "contents": [
            {"parts": [{"text": combined_prompt}]}
        ],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 2048
        }
    }

    import time
    last_error = None
    for model_name in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        try:
            print(f"[{model_name} deneniyor...]")
            with urllib.request.urlopen(req, timeout=18) as response:
                result = json.loads(response.read().decode("utf-8"))
                candidates = result.get("candidates", [])
                if candidates and "content" in candidates[0]:
                    parts = candidates[0]["content"].get("parts", [])
                    if parts and "text" in parts[0]:
                        display_name = "Gemini Flash-Lite" if "lite" in model_name else "Gemini 3.8 Flash"
                        return parts[0]["text"].strip(), display_name
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            print(f"[Gemini HTTP Hata {e.code} ({model_name})]: {err_body[:160]}")
            last_error = e
            time.sleep(0.5)
        except Exception as e:
            print(f"[Gemini İstek Hatası ({model_name})]: {e}")
            last_error = e

    raise last_error or ValueError("Gemini geçerli bir yanıt döndürmedi.")

class LLMClient:
    def __init__(self):
        pass

    async def generate_response(self, user_query: str, contexts: List[Dict[str, Any]]) -> Tuple[str, str]:
        """
        Kullanıcı sorusuna bağlam üzerinden yanıt üretir.
        Döner: (cevap_metni, kullanilan_model_adi)
        """
        context_str = "\n\n---\n\n".join([
            f"Dosya: {c['file_path']}\nBölüm: {c['title']} - {c['section']}\nİçerik:\n{c['content']}"
            for c in contexts
        ])

        # 1. Öncelik: Groq Cloud (Llama 3.3 70B)
        try:
            answer = await asyncio.to_thread(_call_groq_sync, user_query, context_str)
            return answer, "Groq (Llama 3.3 70B)"
        except Exception:
            pass

        # 2. Yedek Öncelik: Google Gemini Flash
        try:
            answer, model_name = await asyncio.to_thread(_call_gemini_sync, user_query, context_str)
            return answer, model_name
        except Exception as e:
            return (
                "Üzgünüm, şu anda yapay zeka model servislerine ulaşılamıyor. "
                "Lütfen sorunuzu bir süre sonra tekrar deneyiniz veya ilgili bölüm sekreterliğiyle iletişime geçiniz.",
                "Hata (Servis Çevrimdışı)"
            )
