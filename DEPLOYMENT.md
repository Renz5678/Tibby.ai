# Deployment Guide - Tibby Chatbot

## Backend Deployment (Render)

### Prerequisites
- GitHub account
- Render account (free tier)
- Gemini API key

### Steps

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Tibby v2.0"
   git branch -M main
   git remote add origin https://github.com/yourusername/tibby-chatbot.git
   git push -u origin main
   ```

2. **Create Web Service on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `tibby-backend`
     - **Region**: Choose closest to Philippines (Singapore)
     - **Branch**: `main`
     - **Root Directory**: Leave empty
     - **Runtime**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn backend.app:app`
     - **Instance Type**: `Free`

3. **Set Environment Variables**
   - Click "Environment" tab
   - Add variables:
     ```
     GEMINI_API_KEY=your_actual_api_key_here
     FLASK_ENV=production
     FRONTEND_URL=https://tibby-chatbot.vercel.app
     ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Note your backend URL: `https://tibby-backend.onrender.com`

### Testing Backend

```bash
# Health check
curl https://tibby-backend.onrender.com/health

# Test chat
curl -X POST https://tibby-backend.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'
```

---

## Frontend Deployment (Vercel)

### Prerequisites
- GitHub account
- Vercel account (free tier)
- Backend deployed on Render

### Steps (After Phase 3 - React Migration)

1. **Build Frontend Locally**
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy to Vercel**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Add New..." → "Project"
   - Import your GitHub repository
   - Configure:
     - **Framework Preset**: `Vite`
     - **Root Directory**: `frontend`
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist`

3. **Set Environment Variables**
   - Click "Environment Variables"
   - Add:
     ```
     VITE_API_URL=https://tibby-backend.onrender.com
     ```

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment (2-3 minutes)
   - Your app will be live at: `https://tibby-chatbot.vercel.app`

### Custom Domain (Optional)

1. Go to Vercel project settings
2. Click "Domains"
3. Add your custom domain
4. Update DNS records as instructed

---

## Environment Variables Reference

### Backend (Render)

| Variable | Value | Required |
|----------|-------|----------|
| `GEMINI_API_KEY` | Your Gemini API key | Yes |
| `FLASK_ENV` | `production` | Yes |
| `FRONTEND_URL` | Vercel frontend URL | Yes |

### Frontend (Vercel)

| Variable | Value | Required |
|----------|-------|----------|
| `VITE_API_URL` | Render backend URL | Yes |

---

## Post-Deployment

### Update CORS Origins

After deployment, update `backend/app.py` CORS configuration:

```python
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:5173",
            "https://tibby-chatbot.vercel.app",  # Your actual Vercel URL
            os.getenv("FRONTEND_URL", "")
        ]
    }
})
```

### Monitor Usage

- **Render**: Check logs in Render dashboard
- **Vercel**: Check analytics in Vercel dashboard
- **Gemini**: Monitor usage at [Google AI Studio](https://aistudio.google.com/)

---

## Troubleshooting

### Backend Issues

**Problem**: "Application failed to start"
- Check Render logs
- Verify `requirements.txt` is correct
- Ensure `GEMINI_API_KEY` is set

**Problem**: "CORS error"
- Verify `FRONTEND_URL` matches your Vercel URL
- Check CORS configuration in `app.py`

### Frontend Issues

**Problem**: "API calls failing"
- Verify `VITE_API_URL` is set correctly
- Check backend is running on Render
- Test backend health endpoint

**Problem**: "Build failed"
- Check Node.js version compatibility
- Verify all dependencies are installed
- Check build logs on Vercel

---

## Free Tier Limits

### Render (Backend)
- ✅ 750 hours/month (enough for 24/7)
- ✅ Spins down after 15 min inactivity
- ✅ First request after spin-down takes ~30s

### Vercel (Frontend)
- ✅ 100 GB bandwidth/month
- ✅ Unlimited deployments
- ✅ Automatic HTTPS

### Gemini API
- ✅ 15 requests/minute
- ✅ 1,500 requests/day
- ✅ 1M tokens/day
- ✅ Our usage: ~1,080 tokens/day (0.1%)

---

## Continuous Deployment

Both Render and Vercel support automatic deployments:

1. Push changes to GitHub
2. Render/Vercel automatically detect changes
3. New deployment starts automatically
4. Live site updates in 2-5 minutes

---

## Backup & Rollback

### Render
- Go to "Deploys" tab
- Click "Rollback" on previous deployment

### Vercel
- Go to "Deployments" tab
- Click "Promote to Production" on previous deployment

---

## Support

For deployment issues:
- Render: https://render.com/docs
- Vercel: https://vercel.com/docs
- Gemini API: https://ai.google.dev/docs
