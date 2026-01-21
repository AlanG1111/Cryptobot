from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
import time

from bot.services.news import get_latest_news
from bot.services.full_analysis_ai import full_market_analysis

router = Router()

LAST_CALL = 0
COOLDOWN = 0  # секунд

# 🧊 КЕШ
CACHE = {
    "data": None,
    "time": 0
}
CACHE_TTL = 300  # 5 минут

# 🔘 КНОПКА ОБНОВЛЕНИЯ
refresh_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔄 Обновить анализ",
                callback_data="refresh_analysis"
            )
        ]
    ]
)


@router.message(Command("news_ai"))
async def news_ai_handler(message: Message):
    global LAST_CALL

    now = time.time()

    # ✅ Если есть свежий кеш — сразу отдаем с кнопкой
    if CACHE["data"] and now - CACHE["time"] < CACHE_TTL:
        await message.answer(CACHE["data"], reply_markup=refresh_kb)
        return

    # Защита от частых запросов
    if now - LAST_CALL < COOLDOWN:
        await message.answer("⏳ Подожди минуту перед следующим анализом")
        return

    LAST_CALL = now

    try:
        # Получаем новости
        raw_news = get_latest_news(limit=5)

        # 🔥 ОДИН запрос в ИИ
        analysis = full_market_analysis(raw_news)
        print(analysis)
        if not analysis or "error" in analysis:
            await message.answer("⚠️ ИИ временно недоступен, попробуй позже", reply_markup=refresh_kb)
            return

        # -------- Формируем ответ --------
        text = "🧠 Кратко по рынку:\n\n"
        for item in analysis["summaries"]:
            text += f"• {item}\n"

        overall = analysis["overall"]

        text += "\n📊 Общий рыночный сценарий:\n"
        text += f"Сценарий: {overall['scenario']}\n"
        text += f"Уверенность: {overall['confidence']}\n\n"

        text += "Причины:\n"
        for r in overall["reasons"]:
            text += f"- {r}\n"

        text += "\nРиски:\n"
        for r in overall["risks"]:
            text += f"- {r}\n"

        # -------- Активы --------
        text += "\n📊 Сценарии по активам:\n"

        for asset, tfs in analysis["assets"].items():
            text += f"\n=== {asset} ===\n"
            for tf, data in tfs.items():
                text += f"\n{tf}:\n"
                text += f"Сценарий: {data['scenario']}\n"
                text += f"Уверенность: {data['confidence']}\n"

                text += "Причины:\n"
                for r in data["reasons"]:
                    text += f"- {r}\n"

                text += "Риски:\n"
                for r in data["risks"]:
                    text += f"- {r}\n"

        # 🧊 Сохраняем в кеш
        CACHE["data"] = text
        CACHE["time"] = time.time()

        # Отправляем с кнопкой
        await message.answer(text, reply_markup=refresh_kb)

    except Exception:
        await message.answer("❌ Ошибка при анализе новостей", reply_markup=refresh_kb)


# 🔘 ОБРАБОТЧИК КНОПКИ
@router.callback_query(F.data == "refresh_analysis")
async def refresh_analysis_handler(call: CallbackQuery):
    # ⛔️ Сбрасываем кеш
    CACHE["data"] = None
    CACHE["time"] = 0

    await call.answer("🔄 Обновляю анализ...")
    await news_ai_handler(call.message)
