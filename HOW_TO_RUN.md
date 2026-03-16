# 🐾 How to Run Tibby – GTDLNHS Chatbot

## Prerequisites

Make sure you have these installed:
- **Python 3.9+** – [python.org/downloads](https://www.python.org/downloads/)
- **Node.js 18+** – [nodejs.org](https://nodejs.org/)

---

## Running Locally (Development)

You need **two terminals** — one for the backend, one for the frontend.

### Terminal 1 – Backend (Flask API)

```powershell
# Navigate to the project root
cd c:\Users\Lawrenz\Desktop\tibby\Tibby.ai

# Activate the virtual environment
.\venv\Scripts\activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Start the backend server
python backend/app.py
```

✅ The API will start at **http://localhost:5000**

> To enable debug mode locally, set the environment variable before running:
> ```powershell
> $env:FLASK_DEBUG="true"; python backend/app.py
> ```

---

### Terminal 2 – Frontend (React + Vite)

```powershell
# Navigate to the frontend folder
cd c:\Users\Lawrenz\Desktop\tibby\Tibby.ai\frontend

# Install dependencies (first time only)
npm install

# Start the development server
npm run dev
```

✅ The app will open at **http://localhost:5173**

---

## Running Tests

With the virtual environment activated and from the project root:

```powershell
cd c:\Users\Lawrenz\Desktop\tibby\Tibby.ai
.\venv\Scripts\activate

python test_phase1.py
python test_phase2.py
python test_comprehensive.py
```

---

## Project Structure

```
Tibby.ai/
├── backend/
│   ├── app.py          ← Flask API server
│   └── intents.json    ← Chatbot knowledge base (FAQ answers)
├── frontend/
│   └── src/
│       ├── components/ ← UI components (ChatBox, Sidebar, etc.)
│       ├── context/    ← Chat state management
│       ├── hooks/      ← Custom hooks (typing effect, localStorage)
│       └── services/   ← API communication layer
├── requirements.txt    ← Python dependencies
└── Procfile            ← For deployment (Render/Heroku)
```

---

## Deployment (Production)

### Backend (Render / Railway / Heroku)

1. Push your code to GitHub
2. Create a new **Web Service** on [Render](https://render.com) or similar
3. Set the **Start Command** to: `gunicorn backend.app:app`
4. Set these **environment variables**:
   - `FRONTEND_URL` → your deployed frontend URL (e.g., `https://tibby.vercel.app`)
   - `PORT` → usually auto-set by the platform

### Frontend (Vercel)

1. Push your code to GitHub
2. Import your repo at [vercel.com](https://vercel.com)
3. Set **Root Directory** to `frontend`
4. Set **Build Command** to: `npm run build`
5. Set **Output Directory** to: `dist`
6. Add an **environment variable**:
   - `VITE_API_URL` → your deployed backend URL (e.g., `https://tibby-api.onrender.com`)

---

## Environment Variables Summary

| Variable | Where | Purpose |
|---|---|---|
| `FLASK_DEBUG` | Backend | Set to `true` for debug mode |
| `PORT` | Backend | Port to run on (default: 5000) |
| `FRONTEND_URL` | Backend | Add to CORS allowlist |
| `VITE_API_URL` | Frontend | Backend API base URL |
