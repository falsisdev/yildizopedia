import html
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.enums import ChatAction

from bot.config import ADMIN_TELEGRAM_ID, DAILY_QUESTION_LIMIT, BASE_DIR
from bot.database import Database
from bot.rag_engine import RAGEngine
from bot.llm_client import LLMClient
from aiogram.types import FSInputFile
import re

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

db = Database()
rag = RAGEngine()
llm = LLMClient()

WELCOME_MESSAGE = f"""🎓 <b>Yıldızopedia Telegram Botuna Hoş Geldiniz!</b>

Yıldız Teknik Üniversitesi (YTÜ) kurumsal mevzuatı, öğrenci işleri süreçleri, sınavlar, staj esasları, Bologna bilgi paketi ve fakülte/bölüm rehberleri hakkında sorularınızı 7/24 resmi dökümanlara dayanarak yanıtlıyorum.

💡 <b>Örnek Sorular:</b>
• <i>"Mazeret sınavı başvurusu nasıl yapılır ve süresi nedir?"</i>
• <i>"Kimya mühendisliği staj defteri nereye teslim edilir?"</i>
• <i>"Mekatronik mühendisliği Bologna kodu ve ders planı nedir?"</i>
• <i>"Çift Anadal (ÇAP) ve Yandal başvuru şartları nelerdir?"</i>

🎫 <b>Günlük Soru Limitiniz:</b> {DAILY_QUESTION_LIMIT} Soru (Gece 00:00'da yenilenir)
📌 <b>Komutlar:</b> /yardim, /kalan
"""

HELP_MESSAGE = f"""ℹ️ <b>Yıldızopedia Bot Rehberi ve Kuralları:</b>

1. <b>Resmi Kaynaklar:</b> Yanıtlar doğrudan YTÜ Senato Esasları, Yönetmelikleri ve Fakülte/Bölüm web sitelerinden derlenen 407 resmi dökümana dayanır.
2. <b>Günlük Limit:</b> Sistemimizin tüm Yıldız öğrencilerine ücretsiz ve eşit hizmet sunabilmesi için her öğrencinin günde <b>{DAILY_QUESTION_LIMIT} soru hakkı</b> vardır.
3. <b>Komutlar:</b>
   • /start : Botu başlatır ve karşılama mesajını gösterir.
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
            print(f"[Logo Gönderme Uyarısı]: {e}")

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
        f"🔄 <b>GitHub Durumu:</b> {html.escape(rag.last_sync_info)}\n\n"
        f"📝 <b>Son Sorulan Sorular:</b>\n"
    )
    for log in stats["recent_logs"][:3]:
        stats_text += f"• <i>{html.escape(log['query'][:40])}...</i> ({log['model_used']})\n"

    await message.answer(stats_text, parse_mode="HTML")

@router.message(Command("sync", "guncelle"))
async def handle_sync(message: Message):
    if message.from_user.id != ADMIN_TELEGRAM_ID:
        await message.answer("⛔ Bu komutu yalnızca sistem yöneticisi kullanabilir.")
        return

    status_msg = await message.answer("🔄 <i>GitHub'dan en güncel kodlar ve dökümanlar çekiliyor...</i>", parse_mode="HTML")
    success, msg = rag.sync_from_github()
    
    await status_msg.edit_text(
        f"{msg}\n\n🚀 <b>Bot yeni kodlar ve müfredatla anında yeniden başlatılıyor... (1 saniye)</b>",
        parse_mode="HTML"
    )
    
    # Telegram mesajının iletilmesi için 1 saniye bekle ve prosesi hafızada yeniden başlat
    import sys, os, asyncio
    await asyncio.sleep(1)
    os.execv(sys.executable, [sys.executable] + sys.argv)

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

    # 2. Canlı Durum Bildirimi Gönder (Kullanıcıya bilgi ver)
    status_msg = await message.answer("🔍 <i>Resmi mevzuat ve dökümanlar taranıyor...</i>", parse_mode="HTML")

    # 3. İlgili Bağlamları Bul (RAG)
    try:
        print(f"\n[GELEN SORU]: {query[:80]}... (Kullanıcı: {user_id})")
        contexts = rag.search(query, top_k=3)
        print(f"[RAG BULUNAN BAĞLAM]: {len(contexts)} adet döküman parçası.")
        await status_msg.edit_text("✍️ <i>Resmi belgeler inceleniyor ve cevap hazırlanıyor...</i>", parse_mode="HTML")
    except Exception as e:
        print(f"[HATA - RAG]: {e}")
        await status_msg.edit_text("⚠️ Döküman arama motorunda bir hata oluştu. Lütfen tekrar deneyiniz.")
        return

    # 4. Yapay Zekadan Yanıt Al (Groq -> Gemini Fallback)
    try:
        print("[LLM İSTEĞİ GÖNDERİLİYOR]...")
        answer, model_used = await llm.generate_response(query, contexts)
        print(f"[LLM CEVAP GELDİ] Model: {model_used}")
    except Exception as e:
        print(f"[HATA - LLM]: {e}")
        await status_msg.edit_text(f"⚠️ Yapay zeka yanıt üretirken bir hata oluştu: {e}")
        return

    # 5. Veritabanına Kaydet & Kotayı Düşür
    source_file = contexts[0]["file_path"] if contexts else "Belirtilmedi"
    remaining_after = db.record_query(
        telegram_id=user_id,
        username=message.from_user.username or "",
        first_name=message.from_user.first_name or "",
        query=query,
        model_used=model_used,
        source_file=source_file
    )

    # 6. Yanıtı Standart Güvenilirlik Formatıyla Birleştir
    if contexts:
        primary_ctx = contexts[0]
        source_label = f"{primary_ctx['title']} ({primary_ctx['section']})"
        tier_label = primary_ctx["tier"]
    else:
        source_label = "Genel YTÜ Bilgi Tabanı"
        tier_label = "Resmi Kurumsal Belge (Tier 1)"

    limit_footer = "Sınırsız (Yönetici)" if is_admin else f"{remaining_after} / {DAILY_QUESTION_LIMIT}"

    # Yanıtı Telegram HTML formatına uyarla
    formatted_answer = format_for_telegram(answer)

    formatted_response = (
        f"{formatted_answer}\n\n"
        f"───────────────────────\n"
        f"📌 <b>Kaynak:</b> {html.escape(source_label)}\n"
        f"🛡️ <b>Güvenilirlik:</b> {tier_label}\n"
        f"📅 <b>Güncellik:</b> 2026 Bahar\n"
        f"⚡ <b>Model:</b> {model_used}\n"
        f"🎫 <b>Kalan Günlük Soru Hakkınız:</b> {limit_footer}"
    )

    # Durum mesajını nihai cevaba dönüştür (HTML hatası olursa düz metin fallback)
    try:
        await status_msg.edit_text(
            formatted_response,
            parse_mode="HTML",
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"[HTML Parse Hatası, Düz Metin Gönderiliyor]: {e}")
        plain_response = (
            f"{answer}\n\n"
            f"───────────────────────\n"
            f"📌 Kaynak: {source_label}\n"
            f"🛡️ Güvenilirlik: {tier_label}\n"
            f"📅 Güncellik: 2026 Bahar\n"
            f"⚡ Model: {model_used}\n"
            f"🎫 Kalan Günlük Soru Hakkınız: {limit_footer}"
        )
        await status_msg.edit_text(
            plain_response,
            parse_mode=None,
            disable_web_page_preview=True
        )
