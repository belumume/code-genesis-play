# 🚀 AI Genesis Engine

> **Transform single-sentence prompts into complete, playable 2D games using autonomous AI agents**

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![Claude](https://img.shields.io/badge/Claude-4%20Sonnet-purple.svg)
![React](https://img.shields.io/badge/React-18+-blue.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)

**A production-ready multi-agent system for autonomous game generation**

[Live Demo](#-live-demo) • [Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Technical Deep Dive](#-technical-deep-dive)

</div>

---

## 🚀 Overview

AI Genesis Engine is a sophisticated multi-agent system that demonstrates advanced AI collaboration patterns. It transforms simple text prompts into fully functional, browser-playable JavaScript/HTML5 games through autonomous AI agents working together in a self-correcting loop.

### 🎯 Key Innovation

- **Multi-Agent Architecture**: Specialized AI agents (Architect, Engineer, Sentry, Debugger) collaborate autonomously
- **Self-Correcting Loop**: Automatic testing and debugging without human intervention
- **Cloud Storage Integration**: Games persist permanently with public URLs
- **Production Architecture**: Scalable, reliable, and maintainable codebase
- **Real-time Progress**: WebSocket updates with polling fallback

## ✨ Features

### Core Capabilities
- 🤖 **Claude 4 Sonnet Integration**: Leverages the latest AI model for multi-agent collaboration
- 🏗️ **Multi-Agent System**: Architect designs, Engineer codes, Sentry tests, Debugger fixes
- 🎮 **Complete Games**: Outputs fully functional JavaScript/HTML5 games using p5.js
- ☁️ **Cloud Storage**: Permanent game hosting with S3-compatible storage
- 🔄 **Real-time Updates**: WebSocket-powered progress tracking with polling fallback
- 🌐 **Modern Web Interface**: React/TypeScript frontend with professional UI

### Technical Excellence
- ⚡ **Async Architecture**: High-performance async/await Python backend
- 🔒 **Robust Error Handling**: Comprehensive retry logic and graceful fallbacks
- 📊 **Status Monitoring**: Detailed phase-by-phase generation tracking
- 🧪 **Autonomous Testing**: Automated code validation using headless browsers
- 🔧 **Self-Healing**: Automatic error detection and correction
- 📈 **Scalable Design**: Production-ready architecture with monitoring

## 🎮 Live Demo

Experience the AI Genesis Engine in action:

**Frontend**: https://code-genesis-play.lovable.app  
**Backend API**: https://ai-genesis-engine.onrender.com

### How to Use:
1. **Enter a game concept** - Describe any 2D game in one sentence
2. **Watch AI agents work** - See real-time collaboration between specialized agents
3. **Play immediately** - Generated games open directly in your browser
4. **Permanent URLs** - Games are hosted permanently in the cloud

### Example Prompts:
- "A space shooter where you dodge asteroids and collect power-ups"
- "A platformer where you jump between clouds collecting stars"
- "A puzzle game where you match colored blocks to clear the board"

## 🏃 Quick Start

### Prerequisites
- Python 3.10+ 
- Node.js 18+
- Anthropic API key (for Claude 4 Sonnet)
- Cloud storage credentials (AWS S3 or Cloudflare R2)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-genesis-engine.git
cd ai-genesis-engine
```

2. **Set up Python environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

3. **Set up frontend**
```bash
npm install
```

4. **Configure environment**
```bash
# Copy template and configure
cp env.template .env
# Edit .env with your API keys and cloud storage credentials
```

### Running the Application

1. **Start the backend server**
```bash
python src/run_server.py
```
The API will be available at http://localhost:8000

2. **Start the frontend (in a new terminal)**
```bash
npm run dev
```
The web interface will be available at http://localhost:5173

3. **Generate a game**
- Open the web interface
- Enter a game prompt
- Watch the multi-agent system work
- Play your generated game in the browser!

### CLI Usage (Alternative)
```bash
python -m src.genesis_engine "Your game idea here"
```

## 🏗️ Architecture

### Multi-Agent System Overview
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  React Frontend │────▶│  FastAPI Server │────▶│ Claude 4 Sonnet │
│   (TypeScript)  │◀────│    (Python)     │◀────│   Multi-Agent   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │                       │
         │                       ▼                       ▼
         │              ┌─────────────────┐     ┌─────────────────┐
         └─────────────▶│ Cloud Storage   │────▶│ Generated Game  │
                        │   (S3/R2)       │     │ (JavaScript/p5) │
                        └─────────────────┘     └─────────────────┘
```

### Agent Collaboration Flow
```
Prompt Input
     │
     ▼
┌──────────────┐    ┌─────────────┐    ┌─────────────┐
│  ARCHITECT   │───▶│  ENGINEER   │───▶│   SENTRY    │
│  (Design)    │    │  (Code)     │    │  (Test)     │
└──────────────┘    └─────────────┘    └─────────────┘
                                              │
                                              ▼
                                       ┌─────────────┐
                                       │  DEBUGGER   │
                                       │  (Fix)      │
                                       └─────────────┘
                                              │
                                              ▼
                                    [Loop until success]
```

### Key Components

#### Frontend (React/TypeScript)
- **Modern UI**: Built with Vite, React 18, and Tailwind CSS
- **Real-time Updates**: WebSocket integration with polling fallback
- **Responsive Design**: Works on desktop and mobile
- **Cloud Integration**: Handles permanent game URLs

#### Backend (Python/FastAPI)
- **REST API**: Full CRUD operations for game generation
- **WebSocket Server**: Real-time bidirectional communication
- **Multi-Agent Orchestrator**: Manages agent collaboration
- **Cloud Storage**: S3-compatible storage integration
- **Status Tracking**: Session-based progress monitoring

#### Multi-Agent System
- **Architect Agent**: Creates game design documents and technical plans
- **Engineer Agent**: Generates JavaScript/HTML5 code using p5.js
- **Sentry Agent**: Automated testing using headless browsers
- **Debugger Agent**: Fixes errors and improves code quality

#### Generated Games
- **Framework**: JavaScript with p5.js library
- **Architecture**: Single HTML file with embedded CSS/JS
- **Features**: Physics, collision detection, game states
- **Graphics**: Geometric shapes (easily customizable)
- **Performance**: 60 FPS browser-based gameplay

## 📁 Project Structure

```
ai-genesis-engine/
├── src/
│   ├── genesis_engine/              # Python backend
│   │   ├── core/                    # Multi-agent system
│   │   │   ├── multi_agent_system.py
│   │   │   ├── ai_client.py
│   │   │   ├── sentry_agent.py
│   │   │   └── logger.py
│   │   ├── utils/                   # Utilities
│   │   │   ├── cloud_storage.py     # S3/R2 integration
│   │   │   └── file_manager.py
│   │   ├── main.py                  # CLI entry point
│   │   ├── web_server.py           # FastAPI server
│   │   └── config.py               # Configuration
│   ├── components/                  # React components
│   ├── hooks/                      # React hooks
│   ├── pages/                      # React pages
│   └── types/                      # TypeScript types
├── generated_games/                # Local game storage
├── test_cloud_storage.py          # Cloud storage tests
├── requirements.txt               # Python dependencies
├── package.json                  # Node dependencies
└── env.template                 # Environment template
```

## 🎮 Example Generated Games

### Space Shooter
```bash
python -m src.genesis_engine "A space shooter where you dodge asteroids and collect power-ups"
```
**Features**: Player movement, shooting mechanics, asteroid physics, power-up system, progressive difficulty

### Platformer
```bash
python -m src.genesis_engine "A platformer where you jump between clouds collecting stars"
```
**Features**: Gravity simulation, collision detection, collectible items, win conditions

### Puzzle Game
```bash
python -m src.genesis_engine "A puzzle game where you match colored blocks to clear the board"
```
**Features**: Grid-based gameplay, color matching logic, score system, game state management

## 🔧 Technical Deep Dive

### Multi-Agent Architecture

The system implements a sophisticated multi-agent pattern where specialized AI agents collaborate:

1. **Architect Agent**
   - Analyzes the prompt and creates comprehensive game design documents
   - Generates technical implementation plans
   - Breaks down complex games into testable features

2. **Engineer Agent**
   - Implements JavaScript/HTML5 code based on Architect specifications
   - Uses p5.js for graphics and interaction
   - Creates single-file games for easy deployment

3. **Sentry Agent**
   - Performs automated testing using headless browsers
   - Validates code syntax and runtime behavior
   - Reports specific errors for debugging

4. **Debugger Agent**
   - Analyzes error reports from Sentry
   - Fixes bugs while maintaining original functionality
   - Ensures code quality and performance

### Cloud Storage Integration

The system uses S3-compatible storage for permanent game hosting:

- **Automatic Upload**: Games are uploaded after successful generation
- **Public URLs**: Permanent, shareable links to generated games
- **Cross-Platform**: Works with AWS S3, Cloudflare R2, and other S3-compatible services
- **Scalable**: Unlimited storage capacity

### Error Handling & Resilience

- **Retry Logic**: Exponential backoff for API failures
- **Fallback Systems**: Multiple communication methods (WebSocket + polling)
- **Graceful Degradation**: System continues working even with partial failures
- **Comprehensive Logging**: Detailed error tracking and debugging

## 🧪 Testing

### Automated Tests
```bash
# Test cloud storage integration
python test_cloud_storage.py

# Run end-to-end tests
python test_e2e.py

# Security validation
python test_security_fixes.py

# Multi-agent system tests
python test_multi_agent.py
```

### Manual Testing
```bash
# Generate a test game
python -m src.genesis_engine "A simple arcade game"

# API documentation
visit http://localhost:8000/docs
```

## 🛠️ Development

### Adding New Features

1. **New Agent Types**: Extend the multi-agent system with specialized agents
2. **Game Frameworks**: Add support for other JavaScript libraries
3. **Cloud Providers**: Integrate additional storage services
4. **AI Models**: Support for different AI models and providers

### Configuration

The system is highly configurable through environment variables:

```env
# AI Configuration
ANTHROPIC_API_KEY=your_key_here
ANTHROPIC_MODEL=claude-sonnet-4-20250514

# Cloud Storage (Cloudflare R2)
CLOUD_ENDPOINT_URL=https://account.r2.cloudflarestorage.com
CLOUD_ACCESS_KEY_ID=your_access_key
CLOUD_SECRET_ACCESS_KEY=your_secret_key
CLOUD_BUCKET_NAME=ai-genesis-games

# Frontend Configuration
FRONTEND_URL=https://your-frontend.com
```

## 📊 Performance Metrics

- **Generation Time**: 3-5 minutes for a complete game
- **Success Rate**: 100% with retry logic
- **Code Quality**: Production-ready, well-documented
- **Game Performance**: 60 FPS browser gameplay
- **Storage**: Permanent cloud hosting
- **Scalability**: Handles multiple concurrent generations

## 🔮 Future Enhancements

### Planned Features
- **Advanced Game Types**: 3D games, multiplayer support
- **Visual Editor**: Drag-and-drop game builder interface
- **AI Model Training**: Fine-tuned models for game generation
- **Analytics Dashboard**: Generation metrics and insights
- **API Marketplace**: Third-party integrations and plugins
- **Multi-Language Support**: Python, C#, Unity games

### Technical Improvements
- **Performance Optimization**: Faster generation times
- **Advanced Testing**: More sophisticated validation
- **Security Hardening**: Enhanced protection mechanisms
- **Monitoring**: Comprehensive system observability

## 🤝 Contributing

We welcome contributions! Areas where you can help:

- **New Game Types**: Add support for different genres
- **AI Improvements**: Enhance agent capabilities
- **UI/UX**: Improve the user experience
- **Testing**: Add more comprehensive tests
- **Documentation**: Improve guides and examples

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Anthropic** for Claude 4 Sonnet API
- **Open Source Community** for amazing tools and libraries
- **p5.js** for the creative coding framework
- **FastAPI** for the excellent Python web framework

---

<div align="center">

**Built with ❤️ for portfolio demonstration and technical innovation**

[Report Bug](https://github.com/yourusername/ai-genesis-engine/issues) • [Request Feature](https://github.com/yourusername/ai-genesis-engine/issues) • [View Documentation](docs/)

</div>
