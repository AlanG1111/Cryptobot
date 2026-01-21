import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

from bot.handlers.btc import router as btc_router
from bot.handlers.news import router as news_router
from bot.handlers.news_ai import router as news_ai_router


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не найден в .env")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(btc_router)
dp.include_router(news_router)
dp.include_router(news_ai_router)


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "🤖 Бот запущен!\n\n"
        "Команды:\n"
        "/btc — цена BTC\n"
        "/news — заголовки новостей\n"
        "/news_ai — краткий анализ новостей"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
