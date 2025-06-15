Write-Host "🚀 AI Genesis Engine - Quick Deploy to Railway" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# Check if Railway CLI is installed
try {
    railway --version | Out-Null
    Write-Host "✅ Railway CLI found" -ForegroundColor Green
} catch {
    Write-Host "❌ Railway CLI not found. Installing..." -ForegroundColor Red
    npm install -g @railway/cli
}

# Login to Railway
Write-Host "`n📝 Logging into Railway..." -ForegroundColor Yellow
railway login

# Deploy
Write-Host "`n🚀 Deploying to Railway..." -ForegroundColor Yellow
railway up

Write-Host "`n✅ Deployment complete!" -ForegroundColor Green
Write-Host "`n📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Copy your Railway URL from above"
Write-Host "2. In Lovable, add these environment variables:"
Write-Host "   VITE_API_BASE_URL=https://your-app.railway.app" -ForegroundColor Yellow
Write-Host "   VITE_WS_BASE_URL=wss://your-app.railway.app" -ForegroundColor Yellow
Write-Host "3. Redeploy your Lovable app"
Write-Host "`n🏆 Good luck in the competition!" -ForegroundColor Magenta 