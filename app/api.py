from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.db import get_connection
from app.schemas import TriageResponse

router = APIRouter(prefix="/api", tags=["API"])

@router.get("/tickets", response_model=List[dict])
def get_tickets(
    limit: int = Query(10, ge=1, le=100, description="Максимальное количество записей"),
    client_id: Optional[str] = Query(None, description="Фильтр по client_id"),
    category: Optional[str] = Query(None, description="Фильтр по категории")
):
    """Получить список всех обращений из базы данных"""
    conn = get_connection()
    try:
        query = "SELECT id, text, channel, client_id, category, confidence, escalate, created_at FROM tickets WHERE 1=1"
        params = []
        
        if client_id:
            query += " AND client_id = ?"
            params.append(client_id)
        if category:
            query += " AND category = ?"
            params.append(category)
        
        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)
        
        cursor = conn.execute(query, params)
        rows = cursor.fetchall()
        
        columns = ["id", "text", "channel", "client_id", "category", "confidence", "escalate", "created_at"]
        tickets = [dict(zip(columns, row)) for row in rows]
        
        return tickets
    finally:
        conn.close()

@router.get("/stats", response_model=dict)
def get_stats():
    """Получить статистику по обращениям"""
    conn = get_connection()
    try:
        # Общее количество
        total = conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
        
        # По категориям
        categories = conn.execute(
            "SELECT category, COUNT(*) as count FROM tickets GROUP BY category"
        ).fetchall()
        
        # По каналам
        channels = conn.execute(
            "SELECT channel, COUNT(*) as count FROM tickets GROUP BY channel"
        ).fetchall()
        
        # По confidence
        confidences = conn.execute(
            "SELECT confidence, COUNT(*) as count FROM tickets GROUP BY confidence"
        ).fetchall()
        
        return {
            "total_tickets": total,
            "by_category": dict(categories),
            "by_channel": dict(channels),
            "by_confidence": dict(confidences)
        }
    finally:
        conn.close()

@router.get("/ticket/{ticket_id}", response_model=dict)
def get_ticket(ticket_id: int):
    """Получить конкретное обращение по ID"""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT id, text, channel, client_id, category, draft_reply, confidence, escalate, error, created_at FROM tickets WHERE id = ?",
            (ticket_id,)
        ).fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Обращение не найдено")
        
        columns = ["id", "text", "channel", "client_id", "category", "draft_reply", "confidence", "escalate", "error", "created_at"]
        return dict(zip(columns, row))
    finally:
        conn.close()