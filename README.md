# Tibby Chatbot - GTDLNHS

A friendly chatbot for General Tiburcio de Leon National High School (GTDLNHS) that answers school-related queries using intelligent intent matching with fuzzy logic.

## Features

- ✅ Intent-based pattern matching with fuzzy logic
- ✅ Typo tolerance (Levenshtein distance)
- ✅ Filipino/Taglish support
- ✅ Response caching (30min TTL)
- ✅ Rate limiting (10 req/min per user)
- ✅ React frontend with Vite
- ✅ **100% Free** - No API costs
- ✅ **Fast** - Instant responses
- ✅ **Reliable** - No external dependencies

## Project Structure

```
Tibby.ai/
├── backend/          # Flask API
│   ├── app.py
│   └── intents.json
├── frontend/         # React app (to be created)
├── requirements.txt
├── Procfile         # Render deployment
└── runtime.txt      # Python version
```

## Local Development

### Backend Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask server
cd backend
python app.py
```

Backend runs on `http://localhost:5000`

### Frontend Setup (Coming in Phase 3)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

## Deployment

### Backend (Render)

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn backend.app:app`
   - **Environment Variables**:
     - `GEMINI_API_KEY`: Your Gemini API key
     - `FLASK_ENV`: `production`
     - `FRONTEND_URL`: Your Vercel frontend URL

### Frontend (Vercel)

1. Push code to GitHub
2. Import project on Vercel
3. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Environment Variables**:
     - `VITE_API_URL`: Your Render backend URL

## API Endpoints

### `POST /chat`
Send a message to the chatbot.

**Request:**
```json
{
  "message": "How to enroll?"
}
```

**Response:**
```json
{
  "reply": "📝 To enroll, visit the Registrar's Office...",
  "confidence": 0.95,
  "cached": false
}
```

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "gemini_configured": true,
  "intents_loaded": 48,
  "cache_size": 15
}
```

## Configuration

### Environment Variables

- `FLASK_ENV`: `development` or `production`
- `FRONTEND_URL`: Frontend URL for CORS

### System Settings

- **Response caching**: 30 minutes TTL
- **Rate limit**: 10 requests/minute per user
- **Max input length**: 500 characters
- **Confidence threshold**: 0.70 (70%)

## How It Works

Tibby uses a **pure intent-based system**:

1. User sends a message
2. System uses fuzzy matching to find best intent
3. Returns pre-written response from `intents.json`
4. Caches response for 30 minutes

**No AI API required!** All responses are pre-written and curated for accuracy.

## Improvements (v2.0)

### Phase 1 ✅
- Fixed intent matching regex bug with fuzzy matching
- Added CORS support for React
- Implemented response caching
- Added rate limiting
- Optimized for Gemini free tier
- Input validation

### Phase 2 (In Progress)
- Token optimization
- Enhanced error handling

### Phase 3 (Planned)
- React frontend migration
- Component-based architecture
- Quick question chips

### Phase 4 (Planned)
- Taglish support for all intents
- 48+ intent categories
- 20-25 patterns per intent

## License

MIT License - Created for GTDLNHS

## Contributors

- Lawrenz (Developer)
- Antigravity AI (Assistant)
