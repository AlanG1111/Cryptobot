import os
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv()


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY не задан")
    return OpenAI(api_key=api_key)


def summarize_news(news: list[str]) -> list[str]:
    news = news[:3]

    prompt = (
        "Ты крипто-аналитик.\n"
        "Сожми каждую новость в 1 короткий тезис.\n"
        "Без эмоций, без прогнозов, без советов.\n\n"
        "Новости:\n"
    )

    for i, item in enumerate(news, start=1):
        prompt += f"{i}. {item}\n"

    prompt += (
        "\nОтвет верни строго в виде списка:\n"
        "- тезис 1\n"
        "- тезис 2\n"
        "- тезис 3\n"
    )

    try:
        client = get_openai_client()

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        text = response.choices[0].message.content
        return [
            line.strip("- ").strip()
            for line in text.split("\n")
            if line.strip()
        ]

    except (OpenAIError, RuntimeError):
        # fallback — если ключа нет или OpenAI недоступен
        return [item[:120] + "..." for item in news]
