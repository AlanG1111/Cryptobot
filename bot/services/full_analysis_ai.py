# bot/services/full_analysis_ai.py
import json
from bot.services.openai_client import client

def full_market_analysis(news_list: list) -> dict:
    """
    Принимает список новостей и возвращает dict:
    {
        "summaries": [...],
        "overall": {"scenario": ..., "confidence": ..., "reasons": [...], "risks": [...]},
        "assets": { "BTC": {"1h": {...}, "4h": {...}}, ... }
    }
    """
    # Превращаем новости в текст для ИИ
    news_text = "\n".join(f"- {n}" for n in news_list)

    prompt = f"""
Ты — эксперт по крипторынку. На основе следующих новостей:
{news_text}

Сделай:
1. Краткое резюме каждой новости (списком).
2. Общий сценарий рынка (scenario), уверенность (confidence), причины (reasons), риски (risks).
3. Сценарий по каждому активу (assets) и таймфрейму, с теми же полями.

Верни строго JSON в формате:
{{
    "summaries": [],
    "overall": {{"scenario": "", "confidence": "", "reasons": [], "risks": []}},
    "assets": {{}}
}}
Не добавляй пояснительный текст, только JSON!
"""

    try:
        response_text = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500
        ).choices[0].message.content

        # Пробуем распарсить JSON
        analysis = json.loads(response_text)

        # Проверка на корректность полей
        if not all(k in analysis for k in ("summaries", "overall", "assets")):
            return {"error": "Некорректный формат ответа ИИ"}

        return analysis

    except json.JSONDecodeError:
        return {"error": "Не удалось разобрать JSON от ИИ"}
    except Exception as e:
        return {"error": str(e)}
