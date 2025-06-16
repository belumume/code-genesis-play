#!/usr/bin/env python3
"""
Test script to validate security fixes and improvements in AI Genesis Engine.
"""
import asyncio
import httpx
import json
import time
import sys
from typing import Dict, List

# Test configuration
API_BASE_URL = "http://localhost:8000"
TEST_PROMPTS = [
    "Create a simple pong game",
    "<script>alert('xss')</script>",  # XSS attempt
    "a" * 600,  # Too long prompt
    "short",  # Too short prompt
    "Create a space shooter with power-ups and enemies"
]

async def check_server_running(client: httpx.AsyncClient) -> bool:
    """Check if the server is running."""
    try:
        response = await client.get(f"{API_BASE_URL}/api/health", timeout=5.0)
        return response.status_code == 200
    except Exception:
        return False

async def test_cors_headers(client: httpx.AsyncClient):
    """Test CORS configuration and security headers."""
    print("\n🔍 Testing CORS and Security Headers...")
    
    if not await check_server_running(client):
        print("❌ Server not running. Please start the server with: python run_dev.py --backend-only")
        return False
    
    # Test with invalid origin
    response = await client.get(
        f"{API_BASE_URL}/api/health",
        headers={"Origin": "https://evil-site.com"}
    )
    
    cors_header = response.headers.get("access-control-allow-origin")
    if cors_header == "*":
        print("❌ CORS wildcard detected - SECURITY RISK!")
    else:
        print(f"✅ CORS properly configured: {cors_header}")
    
    # Check security headers
    security_headers = [
        ("X-Content-Type-Options", "nosniff"),
        ("X-Frame-Options", "DENY"),
        ("X-XSS-Protection", "1; mode=block"),
        ("Strict-Transport-Security", "max-age=31536000"),
        ("Content-Security-Policy", None)  # Just check existence
    ]
    
    for header, expected_value in security_headers:
        actual_value = response.headers.get(header)
        if actual_value:
            if expected_value and actual_value != expected_value:
                print(f"⚠️  {header}: {actual_value} (expected: {expected_value})")
            else:
                print(f"✅ {header}: {actual_value}")
        else:
            print(f"❌ Missing security header: {header}")
    
    return True

async def test_rate_limiting(client: httpx.AsyncClient):
    """Test rate limiting implementation."""
    print("\n🔍 Testing Rate Limiting...")
    
    if not await check_server_running(client):
        print("❌ Server not running. Skipping rate limiting test.")
        return False
    
    # Make rapid requests
    request_count = 0
    rate_limited = False
    
    for i in range(35):  # Exceeds 30/minute limit
        try:
            response = await client.get(f"{API_BASE_URL}/api/health")
            if response.status_code == 429:
                rate_limited = True
                print(f"✅ Rate limited after {request_count} requests")
                break
            request_count += 1
        except Exception as e:
            print(f"❌ Request failed: {str(e)}")
            break
    
    if not rate_limited:
        print(f"❌ Rate limiting not working - made {request_count} requests without limit")
    
    return rate_limited

async def test_input_sanitization(client: httpx.AsyncClient):
    """Test input sanitization on prompts."""
    print("\n🔍 Testing Input Sanitization...")
    
    if not await check_server_running(client):
        print("❌ Server not running. Skipping input sanitization test.")
        return False
    
    test_cases = [
        {
            "prompt": "<script>alert('xss')</script>Create a game",
            "expected_error": True,
            "description": "XSS attempt"
        },
        {
            "prompt": "javascript:void(0)",
            "expected_error": True,
            "description": "JavaScript injection"
        },
        {
            "prompt": "a" * 600,
            "expected_error": True,
            "description": "Exceeds length limit"
        },
        {
            "prompt": "abc",
            "expected_error": True,
            "description": "Too short"
        },
        {
            "prompt": "Create a simple pong game with paddles",
            "expected_error": False,
            "description": "Valid prompt"
        }
    ]
    
    passed_tests = 0
    
    for test in test_cases:
        try:
            response = await client.post(
                f"{API_BASE_URL}/api/generate",
                json={"prompt": test["prompt"]},
                timeout=10.0
            )
            
            if test["expected_error"]:
                if response.status_code >= 400:
                    print(f"✅ {test['description']}: Properly rejected")
                    passed_tests += 1
                else:
                    print(f"❌ {test['description']}: Should have been rejected")
            else:
                if response.status_code == 200:
                    print(f"✅ {test['description']}: Accepted as expected")
                    passed_tests += 1
                else:
                    print(f"❌ {test['description']}: Should have been accepted")
                    
        except Exception as e:
            print(f"❌ {test['description']}: Request failed - {str(e)}")
    
    return passed_tests == len(test_cases)

async def test_sentry_validation():
    """Test the enhanced Sentry agent validation."""
    print("\n🔍 Testing Sentry Agent Validation...")
    
    try:
        # Import with path fix
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent))
        
        from src.genesis_engine.core.sentry_agent import SentryAgent
        import logging
        
        # Set up logger
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        # Test cases
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
        }
        
        function draw() {
            background(0);
            circle(400, 300, 50);
        }
    </script>
</body>
</html>
"""
        
        invalid_html = """
<html>
    <script>
        // Missing p5.js and functions
        console.log("Invalid game");
    </script>
</html>
"""
        
        sentry = SentryAgent(logger)
        await sentry.initialize()
        
        # Test valid HTML
        print("Testing valid HTML game...")
        valid_results = await sentry.validate_game(test_html, "test_valid_game")
        print(f"Valid game result: {'✅ PASSED' if valid_results['success'] else '❌ FAILED'}")
        
        # Test invalid HTML
        print("Testing invalid HTML game...")
        invalid_results = await sentry.validate_game(invalid_html, "test_invalid_game")
        print(f"Invalid game result: {'✅ CORRECTLY FAILED' if not invalid_results['success'] else '❌ SHOULD HAVE FAILED'}")
        
        # Show validation details
        if invalid_results['errors']:
            print("Detected errors:")
            for error in invalid_results['errors'][:3]:
                print(f"  - {error}")
        
        # Clean up
        await sentry.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ Sentry test failed: {str(e)}")
        return False

async def main():
    """Run all security tests."""
    print("🚀 AI Genesis Engine Security Test Suite")
    print("=" * 50)
    
    print("\n💡 To run complete tests, start the server first:")
    print("   python run_dev.py --backend-only")
    print("   (Then run this test in another terminal)")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Check if server is running
        server_running = await check_server_running(client)
        
        if server_running:
            print("\n✅ Server is running - executing full test suite")
            await test_cors_headers(client)
            await test_rate_limiting(client)
            await test_input_sanitization(client)
        else:
            print("\n⚠️  Server not running - executing offline tests only")
            print("   Start server with: python run_dev.py --backend-only")
    
    # Always test Sentry validation (offline)
    await test_sentry_validation()
    
    print("\n✅ Security test suite completed!")
    
    if not server_running:
        print("\n💡 To run complete tests, start the backend server and re-run this script")

if __name__ == "__main__":
    asyncio.run(main()) 