"""
Configuration management for AI Genesis Engine.
Centralized settings with environment variable support.
"""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # API Configuration
    anthropic_api_key: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    anthropic_model: str = Field("claude-opus-4-20250514", env="ANTHROPIC_MODEL")
    api_timeout: int = Field(60, env="API_TIMEOUT")
    max_retries: int = Field(3, env="MAX_RETRIES")
    
    # Server Configuration
    server_host: str = Field("0.0.0.0", env="SERVER_HOST")
    server_port: int = Field(8000, env="SERVER_PORT")
    cors_origins: list[str] = Field(
        ["http://localhost:5173", "http://localhost:3000"],
        env="CORS_ORIGINS"
    )
    
    # Generation Settings
    output_dir: Path = Field(Path("generated_games"), env="OUTPUT_DIR")
    test_output_dir: Path = Field(Path("test_output"), env="TEST_OUTPUT_DIR")
    max_prompt_length: int = Field(500, env="MAX_PROMPT_LENGTH")
    min_prompt_length: int = Field(10, env="MIN_PROMPT_LENGTH")
    
    # Game Generation Parameters
    game_max_tokens: int = Field(4096, env="GAME_MAX_TOKENS")
    game_temperature: float = Field(0.7, env="GAME_TEMPERATURE")
    
    # Feature Flags
    enable_mock_mode: bool = Field(False, env="ENABLE_MOCK_MODE")
    enable_websockets: bool = Field(True, env="ENABLE_WEBSOCKETS")
    enable_game_download: bool = Field(True, env="ENABLE_GAME_DOWNLOAD")
    
    # Security
    enable_rate_limiting: bool = Field(True, env="ENABLE_RATE_LIMITING")
    rate_limit_requests: int = Field(10, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(3600, env="RATE_LIMIT_WINDOW")  # seconds
    
    # Logging
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_format: str = Field("json", env="LOG_FORMAT")  # json or text
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8", 
        case_sensitive=False,
        extra="ignore"  # Ignore extra environment variables
    )

# Global settings instance
settings = Settings()

# Ensure directories exist
settings.output_dir.mkdir(parents=True, exist_ok=True)
settings.test_output_dir.mkdir(parents=True, exist_ok=True)

# Competition-specific constants
COMPETITION_NAME = "Lovable AI Showdown"
COMPETITION_PRIZE = "$10,000"
MODEL_CATEGORY = "Claude 4 Opus"
PROJECT_TAGLINE = "Transform Ideas into Playable Games with AI"

# Game generation phases with weights for progress tracking
GENERATION_PHASES = {
    "initializing": {"weight": 5, "description": "Setting up workspace"},
    "design": {"weight": 20, "description": "Creating game design document"},
    "planning": {"weight": 20, "description": "Planning technical architecture"},
    "coding": {"weight": 40, "description": "Generating game code"},
    "verification": {"weight": 10, "description": "Verifying game structure"},
    "complete": {"weight": 5, "description": "Finalizing project"}
}

# Showcase features for competition
SHOWCASE_FEATURES = [
    "Single prompt to complete game",
    "Real-time progress tracking",
    "Professional code generation",
    "Instant playability",
    "Claude 4 Opus powered",
    "Autonomous game design"
]