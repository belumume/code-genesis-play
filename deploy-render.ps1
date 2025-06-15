Write-Host "🚀 AI Genesis Engine - Deploy to Render.com" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

Write-Host "`n📋 Step 1: Create account at https://render.com" -ForegroundColor Yellow
Write-Host "Press any key when ready..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')

Write-Host "`n📋 Step 2: Install Render CLI (optional, or use web UI)" -ForegroundColor Yellow
Write-Host "For manual deployment via web UI, follow these steps:" -ForegroundColor Cyan

Write-Host "`n1. Go to https://dashboard.render.com/create?type=web" -ForegroundColor White
Write-Host "2. Connect your GitHub repo (or use 'Public Git repository')" -ForegroundColor White
Write-Host "3. Use these settings:" -ForegroundColor White
Write-Host "   - Name: ai-genesis-engine-backend" -ForegroundColor Gray
Write-Host "   - Environment: Python" -ForegroundColor Gray
Write-Host "   - Build Command: pip install -r requirements.txt" -ForegroundColor Gray
Write-Host "   - Start Command: uvicorn src.genesis_engine.web_server:app --host 0.0.0.0 --port `$PORT" -ForegroundColor Gray

Write-Host "`n4. Add environment variable:" -ForegroundColor White
Write-Host "   - ANTHROPIC_API_KEY = [your-api-key]" -ForegroundColor Gray

Write-Host "`n5. Click 'Create Web Service'" -ForegroundColor Green

Write-Host "`n✅ Your backend URL will be: https://ai-genesis-engine-backend.onrender.com" -ForegroundColor Green
Write-Host "`n📝 Update Lovable environment variables:" -ForegroundColor Yellow
Write-Host "   VITE_API_BASE_URL=https://ai-genesis-engine-backend.onrender.com" -ForegroundColor Gray
Write-Host "   VITE_WS_BASE_URL=wss://ai-genesis-engine-backend.onrender.com" -ForegroundColor Gray 