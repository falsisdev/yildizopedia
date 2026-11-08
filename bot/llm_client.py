import json
import logging
from typing import List, Dict, Any, Tuple, Optional
import httpx
from bot.config import GROQ_API_KEY, GEMINI_API_KEY

logger = logging.getLogger("yildizopedia_bot.llm")

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

async def call_groq_async(
    prompt: str,
    context: str,
    history: Optional[List[Dict[str, str]]] = None,
    timeout: float = 14.0
) -> str:
    """Groq Cloud API (Llama 3.3 70B) asenkron HTTP çağrısı."""
    if not GROQ_API_KEY or GROQ_API_KEY.startswith("gsk_placeholder"):
        raise ValueError("Groq API anahtarı girilmedi veya geçersiz.")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        for turn in history:
            role = "assistant" if turn.get("role") in ["model", "assistant"] else "user"
            messages.append({"role": role, "content": turn.get("content", "")})

    user_content = (
        f"Aşağıdaki resmi YTÜ dökümanlarını kullanarak sorumu cevapla:\n\n"
        f"[RESMİ BAĞLAM]:\n{context}\n\n"
        f"[ÖĞRENCİ SORUSU]:\n{prompt}"
    )
    messages.append({"role": "user", "content": user_content})

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "temperature": 0.2,
        "max_tokens": 1500
    }

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

async def call_gemini_async(
    prompt: str,
    context: str,
    history: Optional[List[Dict[str, str]]] = None,
    timeout: float = 16.0
) -> Tuple[str, str]:
    """Google Gemini Flash modelleri asenkron HTTP çağrısı (x-goog-api-key header güvenliği ile)."""
    if not GEMINI_API_KEY:
        raise ValueError("Gemini API anahtarı girilmedi.")

    models = ["gemini-2.5-flash", "gemini-flash-lite-latest", "gemini-flash-latest"]

    raw_contents = []
    if history:
        for turn in history:
            role = "model" if turn.get("role") in ["model", "assistant"] else "user"
            raw_contents.append({
                "role": role,
                "parts": [{"text": turn.get("content", "")}]
            })

    current_content = (
        f"Aşağıdaki resmi YTÜ dökümanlarını kullanarak sorumu cevapla:\n\n"
        f"[RESMİ BAĞLAM]:\n{context}\n\n"
        f"[ÖĞRENCİ SORUSU]:\n{prompt}"
    )
    raw_contents.append({
        "role": "user",
        "parts": [{"text": current_content}]
    })

    # Gemini içerik validasyonu (İlk rol 'user' olmalı, ardışık aynı roller birleştirilmeli)
    contents = []
    for turn in raw_contents:
        if not contents and turn["role"] != "user":
            continue
        if contents and contents[-1]["role"] == turn["role"]:
            contents[-1]["parts"][0]["text"] += "\n" + turn["parts"][0]["text"]
        else:
            contents.append(turn)

    payload = {
        "systemInstruction": {
            "parts": [{"text": SYSTEM_PROMPT}]
        },
        "contents": contents,
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 2048
        }
    }

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }

    last_error = None
    async with httpx.AsyncClient(timeout=timeout) as client:
        for model_name in models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
            try:
                logger.info(f"Gemini deneniyor: {model_name}")
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                candidates = data.get("candidates", [])
                if candidates and "content" in candidates[0]:
                    parts = candidates[0]["content"].get("parts", [])
                    if parts and "text" in parts[0]:
                        display_name = "Gemini Flash-Lite" if "lite" in model_name else "Gemini 2.5 Flash"
                        return parts[0]["text"].strip(), display_name
            except Exception as e:
                logger.warning(f"Gemini {model_name} çağrı hatası: {e}")
                last_error = e

    raise last_error or ValueError("Gemini modellerinden yanıt alınamadı.")

class LLMClient:
    def __init__(self):
        pass

    async def generate_response(
        self,
        user_query: str,
        contexts: List[Dict[str, Any]],
        history: Optional[List[Dict[str, str]]] = None
    ) -> Tuple[str, str]:
        """
        Kullanıcı sorusuna bağlam ve sohbet geçmişi üzerinden yanıt üretir.
        Döner: (cevap_metni, kullanilan_model_adi)
        Hata durumunda exception fırlatır (kotanın korunması için).
        """
        if contexts:
            context_str = "\n\n---\n\n".join([
                f"Dosya: {c['file_path']}\nBölüm: {c['title']} - {c['section']}\nGüvenilirlik: {c.get('tier', 'Tier 1')}\nİçerik:\n{c['content']}"
                for c in contexts
            ])
        else:
            context_str = "İlgili doğrudan resmi döküman bulunamadı. Genel kurumsal YTÜ ilkelerine göre yanıtla."

        # 1. Öncelik: Groq Cloud (Llama 3.3 70B)
        try:
            answer = await call_groq_async(user_query, context_str, history)
            return answer, "Groq (Llama 3.3 70B)"
        except Exception as e:
            logger.info(f"Groq yanıt veremedi ({e}), Gemini fallback deneniyor...")

        # 2. Yedek Öncelik: Google Gemini Flash
        try:
            answer, model_name = await call_gemini_async(user_query, context_str, history)
            return answer, model_name
        except Exception as e:
            logger.error(f"Tüm LLM servisleri başarısız oldu: {e}")
            raise RuntimeError(f"Yapay zeka modellerine ulaşılamıyor: {e}") from e
