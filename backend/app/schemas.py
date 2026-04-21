from pydantic import BaseModel, Field, EmailStr


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)


class BatchPredictRequest(BaseModel):
    texts: list[str] = Field(default_factory=list)


class PredictResponse(BaseModel):
    text: str
    cleaned_text: str
    label: str
    confidence: float
    probabilities: dict[str, float]


class BatchPredictResponse(BaseModel):
    results: list[PredictResponse]


class HistoryItem(BaseModel):
    text: str
    label: str
    confidence: float
    created_at: str | None = None


class HistoryResponse(BaseModel):
    history: list[HistoryItem]


class StatsResponse(BaseModel):
    total_predictions: int
    negative: int
    neutral: int
    positive: int


class TrendPoint(BaseModel):
    date: str
    positive: int
    neutral: int
    negative: int


class TrendsResponse(BaseModel):
    trends: list[TrendPoint]
