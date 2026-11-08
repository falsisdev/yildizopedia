import html
import re
import logging
from typing import List
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command

from bot.config import ADMIN_TELEGRAM_ID, DAILY_QUESTION_LIMIT, BASE_DIR
from bot.database import Database
from bot.rag_engine import RAGEngine
from bot.llm_client import LLMClient
from bot.retrieval.query_rewriter import rewrite_query_with_history
from bot.retrieval.hybrid_search import PrerequisiteGraphRetriever

logger = logging.getLogger("yildizopedia_bot.handlers")
router = Router()

def format_for_telegram(text: str) -> str:
    """Markdown metnini Telegram'ın desteklediği şık HTML formatına dönüştürür."""
    # 1. Başlıkları emoji ve kalın etikete dönüştür
    text = re.sub(r'(?m)^#{1,4}\s*(.*?)$', r'\n📌 <b>\1</b>', text)
    # 2. Kalın yazıları dönüştür
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # 3. İtalik yazıları dönüştür
    text = re.sub(r'(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', r'<i>\1</i>', text)
    # 4. Madde imlerini dönüştür (- veya *)
    text = re.sub(r'(?m)^[\s]*[\*\-]\s+', '• ', text)
    # 5. Markdown yatay çizgilerini temizle
    text = re.sub(r'(?m)^---+$', '', text)
    # 6. Çoklu satır boşluklarını toparla
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def split_telegram_message(text: str, max_length: int = 3900) -> List[str]:
    """
    Telegram 4096 karakter sınırına karşı metni güvenle böler.
    HTML tag'lerini ve paragrafları mümkün mertebe korur; aşırı uzun tekil satırları dilimler.
    """
    if len(text) <= max_length:
        return [text]

    chunks = []
    paragraphs = text.split("\n\n")
    current_chunk = ""

    for p in paragraphs:
        if len(p) > max_length:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""
            lines = p.split("\n")
            for line in lines:
                if len(line) > max_length:
                    if current_chunk:
                        chunks.append(current_chunk)
                        current_chunk = ""
                    for i in range(0, len(line), max_length):
                        chunks.append(line[i:i + max_length])
                elif len(current_chunk) + len(line) + 1 <= max_length:
                    current_chunk = (current_chunk + "\n" + line).strip()
                else:
                    if current_chunk:
                        chunks.append(current_chunk)
                    current_chunk = line
        elif len(current_chunk) + len(p) + 2 <= max_length:
            current_chunk = (current_chunk + "\n\n" + p).strip()
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = p

    if current_chunk:
        chunks.append(current_chunk)

    return chunks if chunks else [text[:max_length]]

db = Database()
rag = RAGEngine()
llm = LLMClient()
graph_retriever = PrerequisiteGraphRetriever()

WELCOME_MESSAGE = f"""🎓 <b>Yıldızopedia Telegram Botuna Hoş Geldiniz!</b>

Yıldız Teknik Üniversitesi (YTÜ) kurumsal mevzuatı, öğrenci işleri süreçleri, sınavlar, staj esasları, Bologna bilgi paketi ve fakülte/bölüm rehberleri hakkında sorularınızı 7/24 resmi dökümanlara dayanarak yanıtlıyorum.

💡 <b>Örnek Sorular:</b>
• <i>"Mazeret sınavı başvurusu nasıl yapılır ve süresi nedir?"</i>
• <i>"Kimya mühendisliği staj defteri nereye teslim edilir?"</i>
• <i>"Bilgisayar mühendisliği 3. yarıyıl ders planı nedir?"</i>
• <i>"Çift Anadal (ÇAP) ve Yandal başvuru şartları nelerdir?"</i>

🎫 <b>Günlük Soru Limitiniz:</b> {DAILY_QUESTION_LIMIT} Soru (Gece 00:00'da yenilenir)
📌 <b>Komutlar:</b> /yardim, /kalan, /temizle
"""

HELP_MESSAGE = f"""ℹ️ <b>Yıldızopedia Bot Rehberi ve Kuralları:</b>

1. <b>Resmi Kaynaklar:</b> Yanıtlar doğrudan YTÜ Senato Esasları, Yönetmelikleri ve Fakülte/Bölüm web sitelerinden derlenen resmî dökümanlara dayanır.
2. <b>Çok Turlu Sohbet Hafızası:</b> Bot, sorduğunuz önceki soruları ve verdiği cevapları hatırlar. Takip sorularınızı (<i>"Peki önkoşulu var mı?", "O dersten kalırsam ne olur?"</i>) doğrudan sorabilirsiniz.
3. <b>Günlük Limit:</b> Sistemimizin tüm Yıldız öğrencilerine ücretsiz ve eşit hizmet sunabilmesi için her öğrencinin günde <b>{DAILY_QUESTION_LIMIT} soru hakkı</b> vardır.
4. <b>Komutlar:</b>
   • /start : Botu başlatır ve karşılama mesajını gösterir.
   • /temizle : Sohbet hafızasını sıfırlar ve yeni bir konuya başlar.
   • /kalan : Bugün kalan soru hakkınızı görüntüler.
   • /yardim : Bu bilgilendirme mesajını açar.
"""

@router.message(CommandStart())
async def handle_start(message: Message):
    is_allowed, remaining, is_admin = db.check_user_quota(message.from_user.id)
    limit_text = "Sınırsız (Yönetici)" if is_admin else f"{remaining} / {DAILY_QUESTION_LIMIT}"
    caption = WELCOME_MESSAGE + f"\n🎫 <b>Mevcut Kalan Hakkınız:</b> {limit_text}"
    
    logo_path = BASE_DIR / "assets" / "logo.jpg"
    if logo_path.exists():
        try:
            photo = FSInputFile(str(logo_path))
            await message.answer_photo(photo, caption=caption, parse_mode="HTML")
            return
        except Exception as e:
            logger.warning(f"Logo gönderme uyarısı: {e}")

    await message.answer(caption, parse_mode="HTML")

@router.message(Command("yardim", "help"))
async def handle_help(message: Message):
    await message.answer(HELP_MESSAGE, parse_mode="HTML")

@router.message(Command("kalan", "limit", "quota"))
async def handle_quota(message: Message):
    is_allowed, remaining, is_admin = db.check_user_quota(message.from_user.id)
    if is_admin:
        await message.answer("👑 <b>Yönetici Hesabı:</b> Soru limitiniz sınırsızdır.", parse_mode="HTML")
    else:
        await message.answer(
            f"🎫 <b>Bugün Kalan Soru Hakkınız:</b> {remaining} / {DAILY_QUESTION_LIMIT}\n"
            f"<i>Hakkınız bu gece Türkiye saatiyle 00:00'da sıfırlanacaktır.</i>",
            parse_mode="HTML"
        )

@router.message(Command("stats", "istatistik"))
async def handle_stats(message: Message):
    if message.from_user.id != ADMIN_TELEGRAM_ID:
        await message.answer("⛔ Bu komutu yalnızca sistem yöneticisi kullanabilir.")
        return

    stats = db.get_stats()
    stats_text = (
        f"📊 <b>Yıldızopedia Bot Yönetici İstatistikleri ({stats['today']})</b>\n\n"
        f"👥 <b>Toplam Kayıtlı Kullanıcı:</b> {stats['total_users']}\n"
        f"⚡ <b>Bugün Aktif Öğrenci:</b> {stats['active_today']}\n"
        f"💬 <b>Bugün Sorulan Toplam Soru:</b> {stats['questions_today']}\n"
        f"📈 <b>Genel Toplam Sorgu Sayısı:</b> {stats['all_time_queries']}\n\n"
        f"🔄 <b>Bilgi Bankası Durumu:</b> {html.escape(rag.last_sync_info)}\n\n"
        f"📝 <b>Son Sorulan Sorular:</b>\n"
    )
    for log in stats["recent_logs"][:3]:
        stats_text += f"• <i>{html.escape(log['query'][:40])}...</i> ({log['model_used']})\n"

    await message.answer(stats_text, parse_mode="HTML")

@router.message(Command("temizle", "reset", "yeni"))
async def handle_clear_history(message: Message):
    db.clear_chat_history(message.from_user.id)
    await message.answer(
        "🧹 <b>Sohbet Hafızası Sıfırlandı!</b>\n\n"
        "Önceki konuşma geçmişimiz temizlendi. Yeni bir soru veya konuyla tertemiz bir başlangıç yapabiliriz. Sana nasıl yardımcı olabilirim?",
        parse_mode="HTML"
    )

@router.message(Command("reload_kb", "yenile", "sync"))
async def handle_reload_kb(message: Message):
    if message.from_user.id != ADMIN_TELEGRAM_ID:
        await message.answer("⛔ Bu komutu yalnızca sistem yöneticisi kullanabilir.")
        return

    status_msg = await message.answer("🔄 <i>Bilgi bankası dökümanları taranıyor ve indeks yenileniyor...</i>", parse_mode="HTML")
    success, msg = rag.reload_index()
    graph_retriever.load_graph()
    await status_msg.edit_text(f"{msg}\n\n🚀 <b>Arama motoru ve önkoşul grafı kesintisiz olarak güncellendi.</b>", parse_mode="HTML")

@router.message(F.text)
async def handle_question(message: Message):
    user_id = message.from_user.id
    query = message.text.strip()
    if not query:
        return

    # 1. Kota Kontrolü
    is_allowed, remaining, is_admin = db.check_user_quota(user_id)
    if not is_allowed and not is_admin:
        await message.answer(
            f"⚠️ <b>Günlük Soru Limitiniz Doldu! ({DAILY_QUESTION_LIMIT}/{DAILY_QUESTION_LIMIT})</b>\n\n"
            "Sistemin tüm Yıldız öğrencilerine ücretsiz ve eşit hizmet verebilmesi için kullanıcı başına günlük soru limiti 15'tir.\n\n"
            "Hakkınız bu gece saat 00:00'da tekrar yenilenecektir. Acil resmi işlemleriniz için lütfen "
            "<a href='https://ogi.yildiz.edu.tr'>Öğrenci İşleri Portalı</a>'nı ziyaret ediniz.",
            parse_mode="HTML",
            disable_web_page_preview=True
        )
        return

    # 2. Canlı Durum Bildirimi Gönder
    status_msg = await message.answer("🔍 <i>Resmi mevzuat ve dökümanlar taranıyor...</i>", parse_mode="HTML")

    # 3. Geçmiş Sohbet Turlarını Getir
    history = db.get_chat_history(user_id, limit=6)

    # 3.1 Takip Sorusu Zenginleştirmesi (Query Rewriter)
    search_query = rewrite_query_with_history(query, history=history)

    # 4. İlgili Bağlamları Bul (RAG + Yapısal Önkoşul Grafı)
    try:
        logger.info(f"Gelen Soru: {query[:80]}... (Arama Sorgusu: {search_query})")
        contexts = rag.search(search_query, top_k=3)

        # Önkoşul grafından doğrudan yapısal bilgi enjekte et
        graph_ctx = graph_retriever.get_prerequisite_context(search_query)
        if graph_ctx:
            contexts.insert(0, graph_ctx)

        await status_msg.edit_text("✍️ <i>Resmi belgeler inceleniyor ve cevap hazırlanıyor...</i>", parse_mode="HTML")
    except Exception as e:
        logger.error(f"RAG Arama Hatası: {e}")
        await status_msg.edit_text("⚠️ Döküman arama motorunda geçici bir aksaklık oluştu. Lütfen tekrar deneyiniz.")
        return

    # 5. Yapay Zekadan Yanıt Al (Groq -> Gemini Fallback)
    try:
        answer, model_used = await llm.generate_response(query, contexts, history=history)
    except Exception as e:
        logger.error(f"LLM Yanıt Hatası: {e}")
        # HATA DURUMUNDA KOTA DÜŞÜLMEZ VE GEÇMİŞE YAZILMAZ
        await status_msg.edit_text(
            "⚠️ Üzgünüm, şu anda yapay zeka model servislerine ulaşılamadı. Soru hakkınız eksilmedi. "
            "Lütfen birkaç saniye sonra tekrar deneyiniz.",
            parse_mode="HTML"
        )
        return

    # 6. Başarılıysa Sohbet Hafızasına Ekle & Kotayı Düşür
    try:
        db.add_chat_message(user_id, "user", query)
        db.add_chat_message(user_id, "model", answer)
    except Exception as e:
        logger.warning(f"Hafıza Kayıt Uyarısı: {e}")

    source_file = contexts[0]["file_path"] if contexts else "Belirtilmedi"
    remaining_after = db.record_query(
        telegram_id=user_id,
        username=message.from_user.username or "",
        first_name=message.from_user.first_name or "",
        query=query,
        model_used=model_used,
        source_file=source_file
    )

    # 7. Yanıtı Standart Güvenilirlik Formatıyla Birleştir
    if contexts:
        primary_ctx = contexts[0]
        source_label = f"{primary_ctx['title']} ({primary_ctx['section']})"
        tier_label = primary_ctx["tier"]
    else:
        source_label = "Genel YTÜ Bilgi Tabanı"
        tier_label = "Tier 1 (Resmi Kurumsal Belge)"

    limit_footer = "Sınırsız (Yönetici)" if is_admin else f"{remaining_after} / {DAILY_QUESTION_LIMIT}"
    formatted_answer = format_for_telegram(answer)

    formatted_response = (
        f"{formatted_answer}\n\n"
        f"───────────────────────\n"
        f"📌 <b>Kaynak:</b> {html.escape(source_label)}\n"
        f"🛡️ <b>Güvenilirlik:</b> {html.escape(tier_label)}\n"
        f"📅 <b>Dönem:</b> 2026-2027\n"
        f"⚡ <b>Model:</b> {model_used}\n"
        f"🎫 <b>Kalan Günlük Soru Hakkınız:</b> {limit_footer}"
    )

    # 8. Mesaj Bölme ve Güvenli Gönderim (4096 Karakter Sınırı Koruması)
    message_chunks = split_telegram_message(formatted_response, max_length=3900)

    # İlk parçayı mevcut durum mesajını güncelleyerek ilet
    first_chunk = message_chunks[0]
    try:
        await status_msg.edit_text(first_chunk, parse_mode="HTML", disable_web_page_preview=True)
    except Exception as e:
        logger.warning(f"HTML Parse Hatası, Düz Metin Gönderiliyor: {e}")
        plain_first = format_for_telegram(first_chunk).replace("<b>", "").replace("</b>", "").replace("<i>", "").replace("</i>", "")
        await status_msg.edit_text(plain_first, parse_mode=None, disable_web_page_preview=True)

    # Kalan parçalar varsa (4096'yı aşan kısımlar) peş peşe yeni mesaj olarak gönder
    for extra_chunk in message_chunks[1:]:
        try:
            await message.answer(extra_chunk, parse_mode="HTML", disable_web_page_preview=True)
        except Exception:
            await message.answer(extra_chunk, parse_mode=None, disable_web_page_preview=True)
