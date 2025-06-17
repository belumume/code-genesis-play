# Environment Setup Guide

Complete setup instructions for AI Genesis Engine development and deployment.

## 🔧 Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- Git
- Anthropic API key (for Claude Sonnet 4)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-genesis-engine.git
cd ai-genesis-engine
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Set Up Frontend
```bash
# Install Node dependencies
npm install
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:

```bash
# REQUIRED: Get from https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE

# Optional: Override defaults
SERVER_PORT=8000
LOG_LEVEL=INFO
```

### 5. Start the Application

**Terminal 1 - Backend Server:**
```bash
python run_server.py
```

**Terminal 2 - Frontend:**
```bash
npm run dev
```

Access the application at http://localhost:5173

## 📋 Environment Variables Reference

### Required Variables

| Variable | Description | How to Get |
|----------|-------------|------------|
| `ANTHROPIC_API_KEY` | Claude 4 Sonnet API key | [Anthropic Console](https://console.anthropic.com/) |

### Optional Configuration

#### Server Settings
```bash
# Server Configuration
SERVER_HOST=0.0.0.0              # Host to bind to
SERVER_PORT=8000                 # Port for FastAPI server
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]

# API Configuration
ANTHROPIC_MODEL=claude-sonnet-4-20250514  # Claude model to use
API_TIMEOUT=60                   # API timeout in seconds
MAX_RETRIES=3                    # Number of retry attempts
```

#### Generation Settings
```bash
# Output Directories
OUTPUT_DIR=generated_games       # Where games are saved
TEST_OUTPUT_DIR=test_output      # Test game output

# Game Generation
GAME_MAX_TOKENS=4096            # Max tokens for code generation
GAME_TEMPERATURE=0.7            # AI creativity (0-1)
MAX_PROMPT_LENGTH=500           # Max prompt characters
MIN_PROMPT_LENGTH=10            # Min prompt characters
```

#### Feature Flags
```bash
# Feature Control
ENABLE_MOCK_MODE=false          # Use mock responses (no API)
ENABLE_WEBSOCKETS=true          # Real-time updates
ENABLE_GAME_DOWNLOAD=true       # Allow ZIP downloads
ENABLE_RATE_LIMITING=true       # API rate limiting
```

#### Security & Logging
```bash
# Security
RATE_LIMIT_REQUESTS=10          # Requests per window
RATE_LIMIT_WINDOW=3600          # Rate limit window (seconds)

# Logging
LOG_LEVEL=INFO                  # DEBUG, INFO, WARNING, ERROR
LOG_FORMAT=json                 # json or text
```

#### Frontend Configuration
```bash
# For Vite frontend
VITE_API_URL=http://localhost:8000  # Backend API URL
```

## 🔐 Getting API Keys

### Anthropic API Key (Required)

1. **Sign up** at [Anthropic Console](https://console.anthropic.com/)
2. **Navigate** to API Keys section
3. **Create** a new API key
4. **Copy** the key (starts with `sk-ant-api03-`)
5. **Add** to your `.env` file

⚠️ **Important**: 
- Keep your API key secret
- Don't commit `.env` to version control
- Use different keys for dev/production

### Supabase (Optional)

If using Supabase for secrets management:

1. Install Supabase CLI
2. Run `supabase functions deploy get-secret`
3. Store your Anthropic key as a secret

## 🧪 Testing Your Setup

### 1. Test Backend Connection
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "ai_available": true,
  "model": "claude-sonnet-4-20250514",
  "version": "1.0.0"
}
```

### 2. Test AI Integration
```bash
python test_real_ai.py
```

### 3. Generate a Test Game
```bash
python -m src.genesis_engine "A simple test game"
```

## 🚀 Production Deployment

### Using Docker
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
CMD ["python", "run_server.py"]
```

### Platform-Specific Setup

#### Vercel/Netlify (Frontend)
```bash
# Build command
npm run build

# Environment variables in dashboard
VITE_API_URL=https://your-backend-url.com
```

#### Railway/Render (Backend)
```bash
# Start command
python run_server.py

# Add environment variables in dashboard
ANTHROPIC_API_KEY=your_key_here
```

## 🐛 Troubleshooting

### Common Issues

**"No Anthropic API key found"**
- Check `.env` file exists in project root
- Verify `ANTHROPIC_API_KEY` is set correctly
- Ensure no spaces around `=` sign

**"API call failed: 401"**
- Invalid API key
- Check key starts with `sk-ant-api03-`
- Verify key is active in Anthropic Console

**"CORS error" in browser**
- Backend server not running
- Check `CORS_ORIGINS` includes your frontend URL
- Verify backend is accessible at configured URL

**"Connection refused" errors**
- Ensure backend is running (`python run_server.py`)
- Check firewall settings
- Verify correct port in `SERVER_PORT`

### Debug Mode

Enable detailed logging:
```bash
LOG_LEVEL=DEBUG
ENABLE_DEBUG_MODE=true
```

Check logs for:
- API request/response details
- WebSocket connection status
- Generation phase progress

## 🔒 Security Best Practices

1. **API Keys**
   - Never commit `.env` files
   - Use environment-specific keys
   - Rotate keys regularly
   - Monitor usage in Anthropic Console

2. **Production**
   - Enable HTTPS
   - Use environment variables, not files
   - Implement proper authentication
   - Set rate limiting appropriately

3. **Development**
   - Use `.env.example` as template
   - Add `.env` to `.gitignore`
   - Use mock mode for testing

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Anthropic API Reference](https://docs.anthropic.com/)
- [Project README](README.md)
- [Competition Guide](COMPETITION_GUIDE.md)

## 💡 Tips

- Start with minimal `.env` (just API key)
- Use mock mode for UI development
- Monitor API usage to avoid limits
- Test with various game prompts
- Keep generated games organized

---

Need help? Check the [README](README.md) or open an issue! 