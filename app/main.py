from fastapi import FastAPI, HTTPException
from app.schemas import TriageRequest, TriageResponse
from app.service import triage_request
from app.limiter import rate_limiter
from app.api import router as api_router

app = FastAPI(title="SupportPulse", version="1.0.0")

# Подключаем API роутер (это новые эндпоинты для базы данных)
app.include_router(api_router)

@app.post("/triage", response_model=TriageResponse)
def triage(req: TriageRequest):
    if not rate_limiter.is_allowed(req.client_id):
        raise HTTPException(status_code=429, detail="Превышен лимит запросов (10 в минуту)")
    
    try:
        result = triage_request(req.text, req.channel, req.client_id)
        return TriageResponse(**result)
    except Exception:
        fallback = {
            "category": "other",
            "draft_reply": "Ваше обращение передано оператору для дальнейшей обработки.",
            "confidence": "low",
            "escalate": True
        }
        return TriageResponse(**fallback)

@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}