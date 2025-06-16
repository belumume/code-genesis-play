#!/bin/bash
# Deployment script for AI Genesis Engine on Render
# Includes Playwright browser installation

echo "🚀 Starting AI Genesis Engine deployment..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
playwright install chromium
playwright install-deps

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p generated_games
mkdir -p logs

# Set permissions
echo "🔒 Setting permissions..."
chmod +x run_server_prod.py

# Verify installation
echo "✅ Verifying installation..."
python -c "import playwright; print('Playwright installed successfully')"
python -c "import fastapi; print('FastAPI installed successfully')"
python -c "import anthropic; print('Anthropic SDK installed successfully')"

echo "✨ Deployment setup complete!"
echo "🎮 AI Genesis Engine is ready to generate games!" 