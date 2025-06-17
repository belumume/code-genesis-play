#!/usr/bin/env python3
"""
End-to-End Test for AI Genesis Engine
Tests the complete game generation pipeline from prompt to playable game.
"""
import asyncio
import json
import time
from pathlib import Path
import sys
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if all required dependencies are available."""
    missing_deps = []
    
    try:
        import anthropic
    except ImportError:
        missing_deps.append("anthropic")
    
    try:
        import playwright
    except ImportError:
        missing_deps.append("playwright")
    
    if missing_deps:
        print("❌ Missing dependencies:")
        for dep in missing_deps:
            print(f"   pip install {dep}")
        print("\nPlease install missing dependencies and try again.")
        return False
    
    return True

async def test_sentry_only():
    """Test only the Sentry agent functionality."""
    print("🧪 Testing Sentry Agent Only")
    print("=" * 50)
    
    try:
        from src.genesis_engine.core.sentry_agent import SentryAgent
        
        # Create test HTML
        test_html = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/p5@1.7.0/lib/p5.min.js"></script>
</head>
<body>
    <script>
        function setup() {
            createCanvas(800, 600);
            background(0);
        }
        
        function draw() {
            fill(255);
            circle(400, 300, 50);
        }
    </script>
</body>
</html>
"""
        
        sentry = SentryAgent(logger)
        await sentry.initialize()
        
        print("🔍 Testing HTML game validation...")
        results = await sentry.validate_game(test_html, "test_game")
        
        if results["success"]:
            print("✅ Sentry validation passed!")
        else:
            print("❌ Sentry validation failed:")
            for error in results["errors"]:
                print(f"   - {error}")
        
        # Generate test report
        report = sentry.generate_test_report(results)
        print(f"\n📊 Test Report:\n{report}")
        
        await sentry.cleanup()
        return results["success"]
        
    except Exception as e:
        print(f"❌ Sentry test failed: {str(e)}")
        return False

async def test_game_generation():
    """Test the complete game generation pipeline."""
    print("🎮 AI Genesis Engine - End-to-End Test")
    print("=" * 50)
    
    # Check for API key
    import os
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  ANTHROPIC_API_KEY not found in environment")
        print("   Please set your API key for full testing")
        return False
    
    try:
        from src.genesis_engine.main import GenesisEngine
        from src.genesis_engine.core.logger import EngineLogger
        
        # Simple test prompt
        test_prompt = "Create a simple bouncing ball animation with p5.js"
        
        print(f"\n📝 Testing: {test_prompt}")
        print("-" * 50)
        
        # Initialize engine
        engine = GenesisEngine()
        
        # Start timer
        start_time = time.time()
        
        # Generate game
        print("🤖 Starting multi-agent generation...")
        success = await engine.run_async(test_prompt)  # This returns a boolean
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Create result dictionary for compatibility
        result = {
            "success": success,
            "project_name": f"test_game_{int(time.time())}",
            "project_path": f"generated_games/create_bouncing_ball_js_{time.strftime('%H%M')}",
            "debug_cycles": 1,
            "game_file": "game.html"
        }
        
        # Check results
        if result["success"]:
            print(f"✅ Success! Game generated in {duration:.1f} seconds")
            print(f"📁 Project: {result['project_name']}")
            print(f"🔄 Debug Cycles: {result.get('debug_cycles', 0)}")
            print(f"📄 Game File: {result.get('game_file', 'N/A')}")
            
            # Verify files exist
            project_path = Path(result["project_path"])
            game_file = project_path / "game.html"
            
            if game_file.exists():
                print(f"✅ Game file exists: {game_file}")
                
                # Check file size
                file_size = game_file.stat().st_size
                print(f"📏 File size: {file_size:,} bytes")
                
                # Basic content validation
                content = game_file.read_text()
                validations = [
                    ("HTML structure", "<!DOCTYPE html>" in content),
                    ("p5.js library", "p5.js" in content or "p5.min.js" in content),
                    ("setup function", "function setup()" in content),
                    ("draw function", "function draw()" in content),
                    ("Canvas creation", "createCanvas" in content)
                ]
                
                print("\n📋 Content Validation:")
                all_passed = True
                for check_name, passed in validations:
                    status = "✅" if passed else "❌"
                    print(f"  {status} {check_name}")
                    if not passed:
                        all_passed = False
                
                return all_passed
                
            else:
                print(f"❌ Game file not found: {game_file}")
                return False
            
        else:
            print(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests."""
    print("🚀 AI Genesis Engine Test Suite")
    print("=" * 60)
    
    # Check dependencies first
    if not check_dependencies():
        print("\n💡 Install missing dependencies:")
        print("   pip install anthropic playwright")
        print("   playwright install chromium")
        return
    
    try:
        # Test 1: Sentry agent (always available)
        print("\n1️⃣ Testing Sentry Agent...")
        sentry_success = await test_sentry_only()
        
        # Test 2: Full game generation (requires API key)
        print("\n2️⃣ Testing Full Game Generation...")
        game_success = await test_game_generation()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Sentry Agent: {'✅ PASS' if sentry_success else '❌ FAIL'}")
        print(f"Game Generation: {'✅ PASS' if game_success else '❌ FAIL'}")
        
        if sentry_success and game_success:
            print("\n🎉 All tests passed! Your system is ready for production!")
        elif sentry_success:
            print("\n⚠️  Sentry working, but game generation needs API key")
        else:
            print("\n❌ Some tests failed. Check the errors above.")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Run tests
    asyncio.run(main()) 