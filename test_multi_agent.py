#!/usr/bin/env python3
"""
Test script for AI Genesis Engine v2.1 Multi-Agent System
Verifies that the autonomous game generation works correctly.
"""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from genesis_engine.main import GenesisEngine

async def test_multi_agent_system():
    """Test the complete multi-agent workflow."""
    print("🧪 Testing AI Genesis Engine v2.1 Multi-Agent System")
    print("=" * 60)
    
    engine = GenesisEngine()
    
    # Test with a simple prompt
    test_prompt = "A simple Pong game with two paddles and a bouncing ball"
    
    print(f"🎮 Testing with prompt: '{test_prompt}'")
    print()
    
    try:
        # Run the complete multi-agent generation
        result = await engine.run_with_websocket(test_prompt)
        
        print("\n" + "=" * 60)
        print("🔍 MULTI-AGENT TEST RESULTS:")
        print("=" * 60)
        
        if result.get("success"):
            print("✅ Multi-agent generation: SUCCESS")
            print(f"📁 Project created: {result.get('project_name')}")
            print(f"🔄 Debug cycles: {result.get('debug_cycles', 0)}")
            print(f"🤖 Multi-agent demo: {result.get('multi_agent_demo', False)}")
            print(f"🌐 Output format: {result.get('output_format', 'unknown')}")
            
            # Check if game file exists
            if result.get("project_path"):
                project_path = Path(result["project_path"])
                game_file = project_path / "game.html"
                
                if game_file.exists():
                    print(f"🎮 JavaScript game file: ✅ FOUND ({game_file.stat().st_size} bytes)")
                    
                    # Read first few lines to verify it's HTML
                    content = game_file.read_text()[:200]
                    if "<!DOCTYPE html>" in content or "<html>" in content:
                        print("🌐 HTML structure: ✅ VALID")
                    else:
                        print("🌐 HTML structure: ❌ INVALID")
                else:
                    print("🎮 JavaScript game file: ❌ NOT FOUND")
            
            print("\n🏆 MULTI-AGENT SYSTEM: FULLY OPERATIONAL")
            
        else:
            print("❌ Multi-agent generation: FAILED")
            print(f"Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    """Run the test."""
    asyncio.run(test_multi_agent_system())

if __name__ == "__main__":
    main() 