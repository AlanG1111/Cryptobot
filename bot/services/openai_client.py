from openai import OpenAI

client = OpenAI(
    max_retries=0  # ❗ ОБЯЗАТЕЛЬНО — иначе 429 = 2–3 запроса
)
