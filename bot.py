import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramUnauthorizedError

from config import config
from handlers.checker_handler import router as checker_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger(__name__)


async def main():
    log.info("Validating configuration...")
    config.validate()

    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    try:
        me = await bot.get_me()
    except TelegramUnauthorizedError:
        log.error(
            "Telegram rejected BOT_TOKEN as invalid (401 Unauthorized). "
            "Double-check the token in Railway's Variables tab against the one "
            "@BotFather gave you — no quotes, no extra spaces, no line breaks."
        )
        sys.exit(1)

    log.info("Authenticated as @%s (id=%s)", me.username, me.id)

    dp = Dispatcher()
    dp.include_router(checker_router)

    log.info("Deleting any stale webhook and starting long polling...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Shutting down.")
    except Exception:
        log.exception("Bot crashed on startup — see traceback above.")
        sys.exit(1)
