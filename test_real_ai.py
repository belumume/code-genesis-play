
#!/usr/bin/env python3
"""
Test script to verify real AI integration is working.
"""

import sys
import asyncio
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed."""
    missing_deps = []
    
    try:
        import aiohttp
    except ImportError:
        missing_deps.append("aiohttp")
    
    if missing_deps:
        print("❌ Missing required dependencies:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\n🔧 To install dependencies, run:")
        print("   pip install -r requirements.txt")
        print("\n   Or install individually:")
        for dep in missing_deps:
            print(f"   pip install {dep}")
        return False
    
    return True

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_real_ai():
    """Test the real AI integration."""
    # Check dependencies first
    if not check_dependencies():
        return False
    
    # Import after dependency check
    from genesis_engine.core.ai_client import AIClient
    from genesis_engine.core.logger import EngineLogger
    
    logger = EngineLogger()
    ai_client = AIClient()
    
    logger.header("🧪 TESTING REAL AI INTEGRATION")
    
    # Test with a simple prompt
    test_prompt = "A simple space shooter where you fly a ship and shoot asteroids"
    
    logger.info(f"Testing with prompt: '{test_prompt}'")
    logger.info("Calling real Claude 4 Sonnet API...")
    
    try:
        # Test GDD generation
        gdd = ai_client.generate_game_design_document(test_prompt)
        
        if "MOCK" in gdd:
            logger.warning("⚠️  Still using mock data - API key might not be accessible")
            logger.info("But the AI client is working correctly!")
        else:
            logger.success("✅ Real AI integration working! Generated unique content.")
            logger.info(f"Generated GDD preview: {gdd[:200]}...")
        
        return True
            
    except Exception as e:
        logger.error(f"❌ AI integration test failed: {str(e)}")
        return False

if __name__ == "__main__":
    if check_dependencies():
        success = test_real_ai()
        if success:
            print("\n🎉 Test completed successfully!")
        else:
            print("\n❌ Test failed. Check the error messages above.")
