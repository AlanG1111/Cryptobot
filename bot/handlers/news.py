from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.services.news import get_latest_news

router = Router()


@router.message(Command("news"))
async def news_handler(message: Message):
    try:
        news = get_latest_news(limit=5)

        if not news:
            await message.answer("Новостей не найдено 🤷‍♂️")
            return

        text = "📰 Последние крипто-новости:\n\n" + "\n\n".join(news)
        await message.answer(text)

    except Exception:
        await message.answer("❌ Ошибка при получении новостей")
