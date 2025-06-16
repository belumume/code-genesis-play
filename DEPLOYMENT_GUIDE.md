# AI Genesis Engine - Deployment Guide

## 🚀 Quick Deployment Steps

### 1. Backend Deployment (Render.com)

**Deploy the backend first as the frontend needs the API URL.**

#### Option A: One-Click Deploy
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

#### Option B: Manual Deploy
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name:** ai-genesis-engine
   - **Runtime:** Python
   - **Build Command:** `chmod +x deploy_render.sh && ./deploy_render.sh`
   - **Start Command:** `python -m src.genesis_engine.run_server_prod`
5. Add Environment Variables:
   - `ANTHROPIC_API_KEY`: Your Anthropic API key
   - `FRONTEND_URL`: https://code-genesis-play.lovable.app
   - `PLAYWRIGHT_BROWSERS_PATH`: /opt/render/project/.cache/ms-playwright

### 2. Frontend Deployment (Lovable)

**Deploy to Lovable platform for the competition.**

#### Steps:
1. Open [Lovable.app](https://lovable.app)
2. Create new project or open existing
3. Import this repository
4. Set environment variables in Lovable:
   ```
   VITE_API_BASE_URL=https://ai-genesis-engine.onrender.com/api
   VITE_WS_BASE_URL=wss://ai-genesis-engine.onrender.com
   ```
5. Deploy the application

### 3. Verify Deployment

#### Backend Health Check:
```bash
curl https://ai-genesis-engine.onrender.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "2.1.0",
  "features": {
    "multi_agent_system": true,
    "javascript_output": true,
    "autonomous_debugging": true,
    "real_time_updates": true
  }
}
```

#### Frontend Check:
1. Visit: https://code-genesis-play.lovable.app
2. Test game generation with: "Create a simple pong game"
3. Verify WebSocket real-time updates work

## 📋 Pre-Deployment Checklist

- [ ] Anthropic API key ready
- [ ] Backend deployed and accessible
- [ ] Frontend environment variables configured
- [ ] CORS origins updated in backend
- [ ] Test game generation works

## 🔧 Troubleshooting

### Backend Issues:
- **"No API key"**: Add ANTHROPIC_API_KEY in Render environment
- **"CORS error"**: Check FRONTEND_URL is set correctly
- **"502 Bad Gateway"**: Wait 2-3 minutes for cold start

### Frontend Issues:
- **"Cannot connect to API"**: Verify VITE_API_BASE_URL is correct
- **"WebSocket failed"**: Check VITE_WS_BASE_URL uses wss:// protocol
- **"Game won't play"**: Ensure browser allows iframe execution

## 🎯 Competition Submission URLs

Once deployed, your submission URLs will be:
- **Live Demo:** https://code-genesis-play.lovable.app
- **API Docs:** https://ai-genesis-engine.onrender.com/docs
- **Backend Health:** https://ai-genesis-engine.onrender.com/api/health

## ⏱️ Estimated Deployment Time

- Backend on Render: 5-10 minutes (first deploy)
- Frontend on Lovable: 2-3 minutes
- Total: ~15 minutes

Good luck with the competition! 🏆 