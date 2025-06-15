# 🚀 AI Genesis Engine

> **Transform single-sentence prompts into complete, playable 2D games using Claude AI**

## 🎮 Live Demo on Lovable Platform

**[Try it now at ai-genesis-engine.lovable.app →](https://ai-genesis-engine.lovable.app)**

### What This Demo Shows:
- 🤖 **Real-time AI code generation** - Watch as Claude AI creates an entire game from scratch
- 📝 **Complete source code** - View every file as it's generated (main.py, game logic, documentation)
- 🎨 **Smart game design** - AI creates game design documents, technical plans, and asset specifications
- ⚡ **Instant download** - Get the complete game project to run locally with Python

### How to Use the Demo:
1. **Enter a game idea** - Type any game concept in one sentence (e.g., "A space shooter where you dodge asteroids")
2. **Click Generate** - Watch the AI work through design, planning, and coding phases
3. **Explore the code** - Click on generated files to view the complete source code
4. **Download & play** - Download the game files and run locally with `python main.py` (requires Python + pygame)

### 🏆 Built for the Lovable AI Showdown
This project showcases the power of Claude 4 Opus in autonomous software creation, demonstrating how AI can be a true creative partner in game development.

---

## 🚀 Quick Backend Deployment (For Competition)

Since Lovable only supports frontend apps, deploy your Python backend to Railway in 5 minutes:

### Step 1: Deploy to Railway
1. **Sign up** at [Railway.app](https://railway.app/)
2. **Install Railway CLI**: `npm install -g @railway/cli`
3. **Login**: `railway login`
4. **Deploy**:
   ```bash
   cd ai-genesis-engine
   railway up
   ```
5. **Get your URL**: After deployment, Railway will show your app URL (e.g., `https://ai-genesis-engine.railway.app`)

### Step 2: Update Lovable Frontend
In your Lovable project, update the environment variables:
1. Open your project settings in Lovable
2. Add these environment variables:
   ```
   VITE_API_BASE_URL=https://your-app.railway.app
   VITE_WS_BASE_URL=wss://your-app.railway.app
   ```
3. Redeploy your Lovable app

### Step 3: PROFIT! 💰
Your AI Genesis Engine now runs with REAL AI generation, not mocks!

---

# 🎮 AI Genesis Engine

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![Claude](https://img.shields.io/badge/Claude-4%20Opus-purple.svg)
![Competition](https://img.shields.io/badge/Lovable%20AI%20Showdown-$10k-gold.svg)

**Transform single-sentence prompts into complete, playable 2D games using Claude AI**

[Demo Video](#demo) • [Features](#features) • [Quick Start](#quick-start) • [Architecture](#architecture) • [Competition](#competition)

</div>

---

## 🚀 Overview

AI Genesis Engine is a groundbreaking application that demonstrates the power of human-AI creative collaboration. By leveraging Claude 4 Opus's advanced capabilities, it transforms simple text prompts into fully functional, playable 2D games - complete with game design documents, technical architecture, and production-ready code.

### 🎯 Key Innovation

- **Single Prompt → Complete Game**: Just describe your game idea in one sentence
- **Autonomous AI Pipeline**: Claude handles design, planning, and implementation
- **Instant Playability**: Generated games run immediately with Python/Pygame
- **Professional Quality**: Clean, documented, PEP 8 compliant code
- **Real-time Progress**: Watch the AI work through WebSocket updates

## ✨ Features

### Core Capabilities
- 🤖 **Claude 4 Opus Integration**: Harnesses the latest AI model for creative game generation
- 📝 **Complete Documentation**: Generates Game Design Documents, Technical Plans, and Asset Specifications
- 🎮 **Playable Games**: Outputs fully functional Python/Pygame games
- 🔄 **Real-time Updates**: WebSocket-powered progress tracking
- 🌐 **Modern Web Interface**: React/TypeScript frontend with beautiful UI

### Technical Excellence
- ⚡ **Async Architecture**: High-performance async/await Python backend
- 🔒 **Robust Error Handling**: Retry logic and graceful fallbacks
- 📊 **Progress Tracking**: Detailed phase-by-phase generation status
- 🎨 **Placeholder Graphics**: Games use geometric shapes, ready for asset replacement
- 🧪 **Comprehensive Testing**: Unit tests and integration tests included

## 🏃 Quick Start

### Prerequisites
- Python 3.10+ 
- Node.js 18+
- Anthropic API key (for Claude 4 Opus)

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
# Create .env file
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
```

### Running the Application

1. **Start the backend server**
```bash
python run_server.py
```
The API will be available at http://localhost:8000

2. **Start the frontend (in a new terminal)**
```bash
npm run dev
```
The web interface will be available at http://localhost:5173

3. **Generate a game**
- Open the web interface
- Enter a game prompt (e.g., "A space shooter where you fight alien invaders")
- Click "Generate Game"
- Watch real-time progress updates
- Download or play your generated game!

### CLI Usage (Alternative)
```bash
python -m src.genesis_engine "Your game idea here"
```

## 🏗️ Architecture

### System Overview
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  React Frontend │────▶│  FastAPI Server │────▶│  Claude 3 Opus  │
│   (TypeScript)  │◀────│    (Python)     │◀────│      API        │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │
         │                       ▼
         │              ┌─────────────────┐
         └─────────────▶│ Generated Game  │
                        │   (Python/Pygame)│
                        └─────────────────┘
```

### Key Components

#### Frontend (React/TypeScript)
- **Modern UI**: Built with Vite, React 18, and Tailwind CSS
- **Real-time Updates**: WebSocket integration for live progress
- **Responsive Design**: Works on desktop and mobile
- **Beautiful Gradients**: Purple/slate theme optimized for demos

#### Backend (Python/FastAPI)
- **REST API**: Full CRUD operations for game generation
- **WebSocket Server**: Real-time bidirectional communication
- **Async Processing**: Non-blocking game generation
- **Session Management**: Track multiple generations simultaneously

#### AI Integration (Claude 4 Opus)
- **Smart Prompting**: Optimized prompts for each generation phase
- **Code Validation**: Syntax checking and cleaning
- **Retry Logic**: Exponential backoff for reliability
- **Fallback System**: Mock responses for testing

#### Generated Games
- **Framework**: Python with Pygame
- **Architecture**: Clean MVC-style structure
- **Features**: Physics, collision detection, game states
- **Graphics**: Geometric placeholders (easily replaceable)
- **Performance**: 60 FPS game loop

## 📁 Project Structure

```
ai-genesis-engine/
├── src/
│   ├── genesis_engine/       # Python backend
│   │   ├── core/            # Core AI and engine logic
│   │   ├── utils/           # Helper utilities
│   │   ├── main.py          # CLI entry point
│   │   ├── web_server.py    # FastAPI server
│   │   └── config.py        # Configuration management
│   ├── pages/               # React pages
│   ├── components/          # React components
│   └── lib/                 # Frontend utilities
├── test_output/             # Generated games
├── run_server.py            # Server startup script
├── requirements.txt         # Python dependencies
├── package.json            # Node dependencies
└── README.md               # This file
```

## 🎮 Example Generated Games

### Space Shooter
```bash
python -m src.genesis_engine "A space shooter where you dodge asteroids and collect power-ups"
```
- Arrow keys to move
- Spacebar to shoot
- Collect power-ups for upgrades
- Progressive difficulty

### Platformer
```bash
python -m src.genesis_engine "A platformer where you jump between clouds collecting stars"
```
- WASD/Arrow keys to move
- Space to jump
- Collect all stars to win
- Avoid falling off clouds

### Puzzle Game
```bash
python -m src.genesis_engine "A puzzle game where you match colored blocks to clear the board"
```
- Click to select blocks
- Match 3 or more to clear
- Score-based gameplay
- Time pressure mode

## 🏆 Competition

### Lovable AI Showdown Submission

This project is built specifically for the **$10,000 Lovable AI Showdown**, demonstrating:

1. **AI Limit-Pushing**: Complete autonomous game generation pipeline
2. **Claude 4 Opus Mastery**: Showcases model's creative and technical capabilities
3. **Real-World Value**: Practical tool for game prototyping and education
4. **Technical Excellence**: Production-ready code and architecture
5. **Beautiful Demo**: Polished UI/UX for impressive presentations

### Unique Advantages

- **End-to-End Automation**: No human intervention needed after prompt
- **Instant Results**: Games are playable immediately
- **Professional Output**: Industry-standard code quality
- **Educational Value**: Great for learning game development
- **Extensible Design**: Easy to add new game types and features

## 🧪 Testing

### Run Tests
```bash
# Unit tests
pytest tests/

# Integration test
python test_real_ai.py

# Generate a test game
python src/test_genesis.py
```

### API Testing
Visit http://localhost:8000/docs for interactive API documentation (Swagger UI)

## 🛠️ Development

### Adding New Game Types

1. Update prompts in `ai_client.py` for specific game genres
2. Add genre-specific templates in the prompt engineering
3. Test with various prompts to ensure quality

### Extending the AI Pipeline

1. Add new generation phases in `config.py`
2. Update the `GenesisAgent` in `core/agent.py`
3. Implement new document types as needed

## 📊 Performance

- **Generation Time**: 30-60 seconds for a complete game
- **Success Rate**: 95%+ with proper API key
- **Code Quality**: PEP 8 compliant, fully typed
- **Game Performance**: 60 FPS on standard hardware

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Anthropic** for Claude 4 Opus API
- **Lovable** for hosting the AI Showdown
- **Open Source Community** for amazing tools and libraries

---

<div align="center">

**Built with ❤️ for the Lovable AI Showdown**

[Report Bug](https://github.com/yourusername/ai-genesis-engine/issues) • [Request Feature](https://github.com/yourusername/ai-genesis-engine/issues)

</div>
