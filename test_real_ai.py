
#!/usr/bin/env python3
"""
Test script to verify real AI integration is working.
"""

import sys
import asyncio
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from genesis_engine.core.ai_client import AIClient
from genesis_engine.core.logger import EngineLogger

async def test_real_ai():
    """Test the real AI integration."""
    logger = EngineLogger()
    ai_client = AIClient()
    
    logger.header("🧪 TESTING REAL AI INTEGRATION")
    
    # Test with a simple prompt
    test_prompt = "A simple space shooter where you fly a ship and shoot asteroids"
    
    logger.info(f"Testing with prompt: '{test_prompt}'")
    logger.info("Calling real Claude 4 Opus API...")
    
    try:
        # Test GDD generation
        gdd = ai_client.generate_game_design_document(test_prompt)
        
        if "MOCK" in gdd:
            logger.warning("⚠️  Still using mock data - API key might not be accessible")
        else:
            logger.success("✅ Real AI integration working! Generated unique content.")
            logger.info(f"Generated GDD preview: {gdd[:200]}...")
            
    except Exception as e:
        logger.error(f"❌ AI integration test failed: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(test_real_ai())
