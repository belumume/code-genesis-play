# 🚀 AI Genesis Engine - Competition Deployment Guide

## Quick Deployment Options (Choose One)

### Option 1: Render.com (Recommended - 5 minutes)
1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Configure:
   - **Name**: `ai-genesis-engine-backend`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.genesis_engine.web_server:app --host 0.0.0.0 --port $PORT`
5. Add environment variable:
   - `ANTHROPIC_API_KEY` = your-api-key
6. Deploy!

**Your backend URL**: `https://ai-genesis-engine-backend.onrender.com`

### Option 2: Replit.com (Fastest - 3 minutes)
1. Go to https://replit.com
2. Click "Create Repl" → "Import from GitHub"
3. Import your repo
4. Add Secret: `ANTHROPIC_API_KEY`
5. Click "Run"

**Your backend URL**: `https://ai-genesis-engine.your-username.repl.co`

### Option 3: Railway (If login works)
```bash
railway login --browserless
# Enter pairing code on website
railway up
```

### Option 4: Local Tunnel (Temporary - 1 minute)
```bash
# Terminal 1
python run_server.py

# Terminal 2
ngrok http 8000
```

## Configure Lovable Frontend

1. In Lovable, go to Settings → Environment Variables
2. Add these variables:
   ```
   VITE_API_BASE_URL=https://your-backend-url
   VITE_WS_BASE_URL=wss://your-backend-url
   ```

3. Redeploy your Lovable app

## Testing Your Deployment

1. Visit your Lovable app URL
2. Enter a game prompt
3. Click "Generate Game"
4. Watch the real-time AI generation!

## Troubleshooting

- **CORS errors**: Make sure your backend URL is added to `allow_origins` in `web_server.py`
- **WebSocket issues**: Ensure WSS protocol is used for secure connections
- **API Key errors**: Double-check your `ANTHROPIC_API_KEY` is set correctly

## For the Demo Video

1. Show the Lovable UI
2. Enter an exciting game prompt
3. Show real-time generation progress
4. Download and run the generated game
5. Play the game!

Good luck! 🏆 