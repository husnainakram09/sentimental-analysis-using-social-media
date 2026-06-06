# Sentiment Analysis App (Multi-User + Sign in with X)

This version includes:
- React + Tailwind dashboard inspired by a modern analytics layout
- FastAPI backend with JWT authentication
- MongoDB storage for users and per-user prediction history
- Private dashboard analytics for each user
- Single prediction and batch prediction
- Sign in with X using OAuth 2.0 Authorization Code Flow with PKCE
- Import and analyze recent tweets from the connected X account

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

## X developer setup

1. Create an app in the X developer console.
2. Enable OAuth 2.0 Authorization Code Flow with PKCE.
3. Set callback URL to: `http://127.0.0.1:8000/api/v1/x/auth/callback` for local development.
4. Copy `X_CLIENT_ID`, `X_CLIENT_SECRET` (if using confidential client), and `X_REDIRECT_URI` into `backend/.env`.
5. Recommended scopes: `tweet.read users.read offline.access`.

## Important API routes
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `GET /api/v1/x/auth/login?frontend_url=http://localhost:5173`
- `GET /api/v1/x/auth/callback`
- `GET /api/v1/x/me`
- `POST /api/v1/x/import-self`
- `POST /api/v1/predictions/predict`
- `POST /api/v1/predictions/batch`
- `GET /api/v1/analytics/stats`
- `GET /api/v1/analytics/history`
- `GET /api/v1/analytics/trends`

## Notes
- Every prediction is stored against the authenticated user.
- Imported tweets are stored with `source = x` and include tweet links when available.
- Dashboard history and charts are filtered by `user_id`.
- Make sure MongoDB is running before using the authenticated app.
- Add `backend/runtime.txt` for Render to use Python 3.11.9.
