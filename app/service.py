from app.llm import classify_with_llm
from app.db import get_connection

def triage_request(text: str, channel: str, client_id: str) -> dict:
    fallback = {
        "category": "other",
        "draft_reply": "Ваше обращение передано оператору для дальнейшей обработки.",
        "confidence": "low",
        "escalate": True
    }

    try:
        result = classify_with_llm(text)
    except Exception:
        conn = get_connection()
        try:
            conn.execute(
                """INSERT INTO tickets (text, channel, client_id, error)
                   VALUES (?, ?, ?, ?)""",
                (text, channel, client_id, "LLM error")
            )
            conn.commit()
        finally:
            conn.close()
        return fallback

    conn = get_connection()
    try:
        conn.execute(
            """INSERT INTO tickets (text, channel, client_id, category, draft_reply, confidence, escalate)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (text, channel, client_id, result["category"], result["draft_reply"], result["confidence"], result["escalate"])
        )
        conn.commit()
    finally:
        conn.close()

    return result