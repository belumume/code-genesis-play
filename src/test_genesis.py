
#!/usr/bin/env python3
"""
Test script to run the Genesis Engine with a sample prompt.
Used for development and debugging.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from genesis_engine.main import GenesisEngine

def test_basic_generation():
    """Test basic game generation with a simple prompt."""
    print("🧪 Testing Genesis Engine with sample prompt...")
    
    # Test prompt
    test_prompt = "A space platformer where you collect crystals while avoiding alien enemies"
    
    # Initialize engine
    engine = GenesisEngine()
    
    # Run generation (using the correct method name)
    success = engine.run(test_prompt, output_dir="test_output")
    
    if success:
        print("✅ Test successful! Check the test_output directory.")
        print("💡 To play the game: cd test_output/[game_folder] && python main.py")
    else:
        print("❌ Test failed!")
    
    return success

if __name__ == "__main__":
    test_basic_generation()
