from openai import OpenAI
from dotenv import load_dotenv
import os

# Загружаем переменные из .env
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("❌ OPENAI_API_KEY не найден в .env!")

client = OpenAI(
    api_key=API_KEY,
    max_retries=0  # ❗ чтобы не было лишних повторов при 429
)
