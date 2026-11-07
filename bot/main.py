import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.config import TELEGRAM_BOT_TOKEN, ADMIN_TELEGRAM_ID
from bot.handlers import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("yildizopedia_bot")

async def main():
    if not TELEGRAM_BOT_TOKEN:
        logger.error("HATA: TELEGRAM_BOT_TOKEN .env dosyasında bulunamadı!")
        return

    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    bot_info = await bot.get_me()
    logger.info(f"Bot başarıyla bağlandı: @{bot_info.username} (ID: {bot_info.id})")
    logger.info(f"Yönetici Telegram ID: {ADMIN_TELEGRAM_ID}")

    # Bekleyen eski webhook ve güncellemeleri temizle
    await bot.delete_webhook(drop_pending_updates=True)

    logger.info("Yıldızopedia Botu dinlemeye başladı (0 TL RAG Servisi Aktif)...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot durduruldu.")
