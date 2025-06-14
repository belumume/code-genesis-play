
#!/usr/bin/env python3
"""
Setup script for the AI Genesis Engine project.
Installs all required dependencies.
"""

import subprocess
import sys
from pathlib import Path

def install_dependencies():
    """Install all required dependencies."""
    print("🔧 Installing AI Genesis Engine dependencies...")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found!")
        return False
    
    try:
        # Install from requirements.txt
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 AI Genesis Engine Setup")
    print("=" * 40)
    
    if install_dependencies():
        print("\n🎉 Setup complete! You can now run:")
        print("   python test_real_ai.py")
        print("   python src/test_genesis.py")
    else:
        print("\n❌ Setup failed. Please install dependencies manually:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main()
