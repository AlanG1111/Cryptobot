import os
from openai import OpenAI
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Инициализация клиента OpenAI
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  # ✅ берем ключ из .env
    max_retries=0  # ❗ обязательно, чтобы не было 429
)
