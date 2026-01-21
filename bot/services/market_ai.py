from openai import OpenAIError
from bot.services.ai import get_openai_client


def analyze_market_scenario(summaries: list[str]) -> dict:
    prompt = (
        "Ты профессиональный крипто-аналитик.\n"
        "На основе новостных тезисов оцени ОБЩИЙ рыночный сценарий.\n\n"
        "Правила:\n"
        "- НЕ давай финансовых советов\n"
        "- НЕ указывай цены, входы, плечи\n"
        "- Только настроение рынка\n\n"
        "Верни ответ СТРОГО в формате:\n"
        "SCENARIO: LONG / SHORT / WAIT\n"
        "CONFIDENCE: LOW / MEDIUM / HIGH\n"
        "REASONS:\n"
        "- причина 1\n"
        "- причина 2\n"
        "RISKS:\n"
        "- риск 1\n\n"
        "Тезисы:\n"
    )

    for item in summaries:
        prompt += f"- {item}\n"

    try:
        client = get_openai_client()

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )

        text = response.choices[0].message.content
        return parse_market_response(text)

    except OpenAIError:
        return {
            "scenario": "WAIT",
            "confidence": "LOW",
            "reasons": ["ИИ временно недоступен"],
            "risks": ["Недостаточно данных"]
        }


def parse_market_response(text: str) -> dict:
    result = {
        "scenario": "WAIT",
        "confidence": "LOW",
        "reasons": [],
        "risks": []
    }

    lines = [line.strip() for line in text.split("\n") if line.strip()]
    current = None

    for line in lines:
        if line.startswith("SCENARIO:"):
            result["scenario"] = line.split(":")[1].strip()
        elif line.startswith("CONFIDENCE:"):
            result["confidence"] = line.split(":")[1].strip()
        elif line.startswith("REASONS"):
            current = "reasons"
        elif line.startswith("RISKS"):
            current = "risks"
        elif line.startswith("-") and current:
            result[current].append(line.lstrip("- ").strip())

    return result
