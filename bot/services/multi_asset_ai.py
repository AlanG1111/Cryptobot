from openai import OpenAIError
from bot.services.ai import get_openai_client
from bot.services.market_ai import parse_market_response

ASSETS = ["BTC", "ETH"]
TIMEFRAMES = ["1H", "4H", "1D"]

def analyze_multi_asset_scenario(summaries: list[str]) -> dict:
    """
    Возвращает словарь:
    {
        "BTC": {
            "1H": {scenario, confidence, reasons, risks},
            "4H": {...},
            "1D": {...}
        },
        "ETH": { ... }
    }
    """
    result = {}
    client = get_openai_client()

    for asset in ASSETS:
        result[asset] = {}
        for tf in TIMEFRAMES:
            prompt = (
                f"Ты профессиональный крипто-аналитик.\n"
                f"На основе новостных тезисов оцени рынок для {asset}.\n"
                f"Таймфрейм: {tf}.\n"
                "Правила:\n"
                "- Только SCENARIO: LONG / SHORT / WAIT\n"
                "- CONFIDENCE: LOW / MEDIUM / HIGH\n"
                "- 2–3 причины, 1–2 риска\n"
                "- Без советов по входу и ценам\n\n"
                "Тезисы:\n"
            )
            for item in summaries:
                prompt += f"- {item}\n"

            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                )
                text = response.choices[0].message.content
                result[asset][tf] = parse_market_response(text)

            except OpenAIError:
                result[asset][tf] = {
                    "scenario": "WAIT",
                    "confidence": "LOW",
                    "reasons": ["ИИ временно недоступен"],
                    "risks": ["Недостаточно данных"]
                }

    return result
