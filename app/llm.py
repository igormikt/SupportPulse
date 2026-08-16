import httpx
from openai import OpenAI
from app.config import PROXYAPI_API_KEY, PROXYAPI_BASE_URL, MODEL_NAME
import json

def classify_with_llm(text: str) -> dict:
    if not PROXYAPI_API_KEY:
        raise ValueError("PROXYAPI_API_KEY is not set in .env")

    print(f"\n🤖 Запрос к LLM: {text[:50]}...")

    # Явно создаем httpx.Client, чтобы обойти баг openai SDK с аргументом 'proxies'
    http_client = httpx.Client(
        headers={"User-Agent": "SupportPulse/1.0"},
        follow_redirects=True
    )

    client = OpenAI(
        api_key=PROXYAPI_API_KEY,
        base_url=PROXYAPI_BASE_URL,
        http_client=http_client
    )

    prompt = f"""Classify this support request into one category: billing, support, complaint, other.
Return ONLY a JSON object with these fields:
- category: one of billing, support, complaint, other
- confidence: high, medium, or low
- escalate: true or false (boolean)
- draft_reply: a 1-6 sentence reply to the user. IMPORTANT: Reply in the exact same language as the user's input text.


Request text:
{text}"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.3
    )

    raw_content = response.choices[0].message.content
    print(f"📥 Ответ LLM: {raw_content}")

    result = json.loads(raw_content)
    return {
        "category": result.get("category", "other"),
        "confidence": result.get("confidence", "low"),
        "escalate": result.get("escalate", False),
        "draft_reply": result.get("draft_reply", "Your request has been forwarded to an operator.")
    }