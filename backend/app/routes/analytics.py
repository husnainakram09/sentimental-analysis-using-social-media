from collections import defaultdict
from fastapi import APIRouter, Depends
from ..deps import get_current_user
from ..database import get_predictions_collection
from ..schemas import HistoryResponse, StatsResponse, TrendsResponse

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/history", response_model=HistoryResponse)
def history(limit: int = 20, current_user=Depends(get_current_user)):
    collection = get_predictions_collection()
    items = list(
        collection.find({"user_id": str(current_user["_id"])}, {"_id": 0, "user_id": 0})
        .sort("created_at", -1)
        .limit(limit)
    )
    for item in items:
        if item.get("created_at"):
            item["created_at"] = item["created_at"].isoformat()
    return {"history": items}


@router.get("/stats", response_model=StatsResponse)
def stats(current_user=Depends(get_current_user)):
    collection = get_predictions_collection()
    uid = str(current_user["_id"])
    return {
        "total_predictions": collection.count_documents({"user_id": uid}),
        "negative": collection.count_documents({"user_id": uid, "label": "negative"}),
        "neutral": collection.count_documents({"user_id": uid, "label": "neutral"}),
        "positive": collection.count_documents({"user_id": uid, "label": "positive"}),
    }


@router.get("/trends", response_model=TrendsResponse)
def trends(current_user=Depends(get_current_user)):
    collection = get_predictions_collection()
    uid = str(current_user["_id"])
    items = list(collection.find({"user_id": uid}, {"_id": 0, "label": 1, "created_at": 1}).sort("created_at", 1))
    grouped = defaultdict(lambda: {"positive": 0, "neutral": 0, "negative": 0})
    for item in items:
        dt = item.get("created_at")
        if not dt:
            continue
        date_key = dt.strftime("%b %d")
        grouped[date_key][item.get("label", "neutral")] += 1
    trends_data = [
        {"date": date, "positive": counts["positive"], "neutral": counts["neutral"], "negative": counts["negative"]}
        for date, counts in grouped.items()
    ]
    return {"trends": trends_data}
