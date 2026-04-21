from fastapi import APIRouter, HTTPException, Depends
from ..deps import get_current_user
from ..schemas import PredictRequest, PredictResponse, BatchPredictRequest, BatchPredictResponse
from ..services.model_service import model_service
from ..services.log_service import log_prediction, log_predictions

router = APIRouter(prefix="/predictions", tags=["Predictions"])


@router.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest, current_user=Depends(get_current_user)):
    if not model_service.is_ready():
        raise HTTPException(status_code=500, detail="Model is not loaded. Train the model first.")
    result = model_service.predict(payload.text)
    log_prediction(result, str(current_user["_id"]))
    return result


@router.post("/batch", response_model=BatchPredictResponse)
def batch_predict(payload: BatchPredictRequest, current_user=Depends(get_current_user)):
    if not model_service.is_ready():
        raise HTTPException(status_code=500, detail="Model is not loaded. Train the model first.")
    results = [model_service.predict(text) for text in payload.texts if text.strip()]
    log_predictions(results, str(current_user["_id"]))
    return {"results": results}
