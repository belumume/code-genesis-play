
#!/usr/bin/env python3
"""
Genesis Engine CLI Runner
Entry point for the AI Genesis Engine system.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path so we can import genesis_engine
sys.path.insert(0, str(Path(__file__).parent))

try:
    from genesis_engine.main import main
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"Error importing Genesis Engine: {e}")
    print("Make sure you're running from the correct directory and all dependencies are installed.")
    sys.exit(1)
except Exception as e:
    print(f"Error running Genesis Engine: {e}")
    sys.exit(1)
