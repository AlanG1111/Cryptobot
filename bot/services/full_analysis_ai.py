import json
from bot.services.openai_client import client


def full_market_analysis(news: list) -> dict:
    try:
        news_text = "\n".join(
            f"- {n['title']} ({n.get('source', 'unknown')})"
            for n in news
        )

        prompt = f"""
Ты крипто-аналитик.
На основе новостей ниже верни СТРОГО JSON без комментариев.

Новости:
{news_text}

Формат ответа:
{{
  "summaries": ["...", "..."],
  "overall": {{
    "scenario": "bullish | bearish | neutral",
    "confidence": "low | medium | high",
    "reasons": ["...", "..."],
    "risks": ["...", "..."]
  }},
  "assets": {{
    "BTC": {{
      "1D": {{
        "scenario": "...",
        "confidence": "...",
        "reasons": ["..."],
        "risks": ["..."]
      }}
    }}
  }}
}}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        return json.loads(response.choices[0].message.content)

    except Exception as e:
        return {"error": str(e)}
