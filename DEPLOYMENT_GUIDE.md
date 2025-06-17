# AI Genesis Engine - Production Deployment Guide

**Deploy your AI Genesis Engine to production platforms for maximum availability and performance.**

---

## 🎯 Deployment Overview

This guide covers deploying the AI Genesis Engine as a production-ready application:

- **Frontend**: React/TypeScript app on Lovable
- **Backend**: Python/FastAPI server on Render
- **Storage**: Cloud storage (AWS S3 or Cloudflare R2)
- **AI**: Claude 4 Sonnet via Anthropic API

---

## 🚀 Backend Deployment (Render)

### Step 1: Prepare Repository

Ensure your repository has these files:
- `requirements.txt` - Python dependencies
- `run_server_prod.py` - Production server script
- `render.yaml` - Render configuration

### Step 2: Deploy to Render

1. **Sign up** at [render.com](https://render.com)
2. **Connect GitHub** repository
3. **Create Web Service**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python run_server_prod.py`
   - Environment: Python 3

### Step 3: Configure Environment Variables

Add these in Render dashboard:
```
ANTHROPIC_API_KEY=your_anthropic_api_key
ANTHROPIC_MODEL=claude-sonnet-4-20250514
FRONTEND_URL=https://your-app.lovable.app
CLOUD_ACCESS_KEY_ID=your_cloud_access_key
CLOUD_SECRET_ACCESS_KEY=your_cloud_secret_key
CLOUD_BUCKET_NAME=ai-genesis-games
CLOUD_ENDPOINT_URL=https://your-cloud-endpoint.com
```

### Step 4: Verify Deployment

Test these endpoints:
- Health check: `https://your-app.onrender.com/api/health`
- API docs: `https://your-app.onrender.com/docs`
- WebSocket: `wss://your-app.onrender.com/ws/generate`

---

## 🎨 Frontend Deployment (Lovable)

### Step 1: Configure Environment

In Lovable project settings, add:
```
VITE_API_BASE_URL=https://your-app.onrender.com
VITE_WS_BASE_URL=wss://your-app.onrender.com
```

### Step 2: Deploy Frontend

1. **Push to main branch** - Lovable auto-deploys
2. **Verify build** in Lovable dashboard
3. **Test live URL**: `https://your-app.lovable.app`

---

## ☁️ Cloud Storage Setup

### Option 1: Cloudflare R2 (Recommended)

1. **Create R2 bucket** at cloudflare.com
2. **Generate API tokens** with R2 permissions
3. **Configure CORS** for browser access
4. **Set environment variables** in Render

### Option 2: AWS S3

1. **Create S3 bucket** in AWS Console
2. **Create IAM user** with S3 permissions
3. **Configure bucket policy** for public read
4. **Set AWS credentials** in Render

---

## 🧪 Production Testing

### End-to-End Testing

1. **Open frontend URL**
2. **Sign in** with authentication
3. **Generate test game**: "A simple space shooter"
4. **Verify progression**:
   - Architect creates design
   - Engineer writes code
   - Sentry tests automatically
   - Debugger fixes issues
   - Game uploads to cloud
5. **Play generated game** in browser

### Performance Testing

- **Generation time**: Should be 3-5 minutes
- **WebSocket latency**: <100ms for real-time updates
- **Game loading**: Instant from cloud URLs
- **Browser compatibility**: All modern browsers

---

## 🔧 Production Configuration

### Security Settings

- API keys stored securely in environment variables
- CORS configured for specific origins
- Rate limiting enabled (10 requests/hour)
- Input validation on all endpoints

### Performance Optimization

- Async FastAPI server for concurrent requests
- Cloud storage for permanent game hosting
- WebSocket with polling fallback
- Efficient retry logic with exponential backoff

### Monitoring

- Health check endpoint for uptime monitoring
- Comprehensive error logging
- Real-time progress tracking
- Session-based generation management

---

## 📊 Production Architecture

```
User Request
     │
     ▼
Frontend (Lovable)
     │
     ▼
Backend (Render)
     │
     ▼
Multi-Agent System
     │
     ▼
Cloud Storage (R2/S3)
     │
     ▼
Permanent Game URL
```

---

## 🎯 Success Criteria

Your deployment is successful when:

- [ ] Frontend loads without errors
- [ ] Authentication system works
- [ ] Real-time WebSocket updates function
- [ ] Games generate successfully (100% success rate)
- [ ] Generated games upload to cloud storage
- [ ] Games are playable from permanent URLs
- [ ] All error scenarios handled gracefully

---

## 🚀 Production Features

1. **Multi-Agent Collaboration**: Autonomous AI agents working together
2. **Self-Correcting System**: Automatic testing and debugging
3. **Cloud Persistence**: Games stored permanently with public URLs
4. **Real-time Updates**: Live progress tracking during generation
5. **Production Architecture**: Scalable and reliable infrastructure

Your AI Genesis Engine is now ready for production use! 🎮 