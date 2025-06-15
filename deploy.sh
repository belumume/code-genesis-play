#!/bin/bash

echo "🚀 AI Genesis Engine - Quick Deploy to Railway"
echo "============================================"

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

# Login to Railway
echo "📝 Logging into Railway..."
railway login

# Deploy
echo "🚀 Deploying to Railway..."
railway up

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Copy your Railway URL from above"
echo "2. In Lovable, add these environment variables:"
echo "   VITE_API_BASE_URL=https://your-app.railway.app"
echo "   VITE_WS_BASE_URL=wss://your-app.railway.app"
echo "3. Redeploy your Lovable app"
echo ""
echo "🏆 Good luck in the competition!" 