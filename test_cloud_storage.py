#!/usr/bin/env python3
"""
Test script for AI Genesis Engine v2.3 Cloud Storage Integration
Tests the cloud storage functionality with a mock game file.
"""
import os
import sys
import asyncio
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from genesis_engine.utils.cloud_storage import get_cloud_storage

def create_test_game_html():
    """Create a simple test game HTML file."""
    return """<!DOCTYPE html>
<html>
<head>
    <title>Cloud Storage Test Game</title>
    <script src="https://cdn.jsdelivr.net/npm/p5@1.7.0/lib/p5.js"></script>
</head>
<body>
    <h1>Cloud Storage Test Game</h1>
    <p>Generated at: {timestamp}</p>
    <script>
    function setup() {{
        createCanvas(400, 400);
        background(0);
    }}
    
    function draw() {{
        fill(255, 0, 0);
        ellipse(mouseX, mouseY, 50, 50);
    }}
    </script>
</body>
</html>""".format(timestamp=datetime.now().isoformat())

async def test_cloud_storage():
    """Test cloud storage upload and retrieval."""
    print("🧪 Testing AI Genesis Engine v2.3 Cloud Storage Integration")
    print("=" * 60)
    
    # Get cloud storage instance
    storage = get_cloud_storage()
    
    # Check if cloud storage is available
    if not storage.is_available():
        print("❌ Cloud storage is not configured!")
        print("\nPlease set the following environment variables:")
        print("  - CLOUD_ACCESS_KEY_ID")
        print("  - CLOUD_SECRET_ACCESS_KEY")
        print("  - CLOUD_BUCKET_NAME")
        print("  - CLOUD_ENDPOINT_URL (for R2 or other S3-compatible)")
        return False
    
    print("✅ Cloud storage is configured and available")
    
    # Create a test game directory
    test_dir = Path("test_cloud_game_" + datetime.now().strftime("%H%M%S"))
    test_dir.mkdir(exist_ok=True)
    
    try:
        # Create test game file
        game_file = test_dir / "game.html"
        game_content = create_test_game_html()
        game_file.write_text(game_content)
        print(f"\n📝 Created test game file: {game_file}")
        
        # Upload to cloud storage
        print("\n☁️  Uploading to cloud storage...")
        cloud_url = storage.upload_game(game_file, test_dir.name)
        
        if cloud_url:
            print(f"✅ Successfully uploaded to: {cloud_url}")
            
            # Verify retrieval
            print("\n🔍 Verifying cloud URL...")
            retrieved_url = storage.get_game_url(test_dir.name)
            if retrieved_url == cloud_url:
                print("✅ Cloud URL verification successful!")
            else:
                print("❌ Cloud URL mismatch!")
            
            # List games
            print("\n📋 Listing games in cloud storage...")
            games = storage.list_games()
            print(f"Found {len(games)} games in cloud storage")
            
            # Clean up - delete from cloud
            print("\n🧹 Cleaning up test game from cloud...")
            if storage.delete_game(test_dir.name):
                print("✅ Test game deleted from cloud")
            else:
                print("⚠️  Failed to delete test game from cloud")
                
            return True
        else:
            print("❌ Upload failed!")
            return False
            
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Clean up local files
        if game_file.exists():
            game_file.unlink()
        if test_dir.exists():
            test_dir.rmdir()
        print("\n✅ Local test files cleaned up")

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run the test
    success = asyncio.run(test_cloud_storage())
    
    if success:
        print("\n🎉 Cloud storage integration test PASSED!")
        print("\nYou can now set up your cloud storage credentials in .env:")
        print("  - For Cloudflare R2: Set CLOUD_ENDPOINT_URL, CLOUD_ACCESS_KEY_ID, etc.")
        print("  - For AWS S3: Set CLOUD_ACCESS_KEY_ID, CLOUD_SECRET_ACCESS_KEY, etc.")
    else:
        print("\n❌ Cloud storage integration test FAILED!")
        print("\nPlease check your configuration and try again.")
    
    sys.exit(0 if success else 1) 