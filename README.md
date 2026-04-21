# Sentiment Analysis App (Multi-User Version)

This version includes:
- React + Tailwind dashboard inspired by a modern analytics layout
- FastAPI backend with JWT authentication
- MongoDB storage for users and per-user prediction history
- Private dashboard analytics for each user
- Single prediction and batch prediction
- Sentiment distribution pie chart and trend chart

## Backend setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -m app.train_model
uvicorn app.main:app --reload
```

## Frontend setup

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

## Important API routes
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `POST /api/v1/predictions/predict`
- `POST /api/v1/predictions/batch`
- `GET /api/v1/analytics/stats`
- `GET /api/v1/analytics/history`
- `GET /api/v1/analytics/trends`

## Notes
- Every prediction is stored against the authenticated user.
- Dashboard history and charts are filtered by `user_id`.
- Make sure MongoDB is running before using the authenticated app.
