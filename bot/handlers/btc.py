from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.services.binance import get_btc_price

router = Router()


@router.message(Command("btc"))
async def btc_price_handler(message: Message):
    try:
        price = get_btc_price()
        await message.answer(
            f"₿ BTC / USDT\n\n"
            f"Цена: {price:,.2f} $"
        )
    except Exception:
        await message.answer("❌ Не удалось получить цену BTC")
