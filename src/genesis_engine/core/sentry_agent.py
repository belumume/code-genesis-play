"""
Sentry Agent for AI Genesis Engine v2.1
Performs automated testing of generated JavaScript/HTML5 games using headless browser.
Reports errors and success status back to the multi-agent orchestrator.
"""
import asyncio
import json
import logging
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Any
import subprocess
import time
import re
import os

# Set up logger at module level
logger = logging.getLogger(__name__)

# Try to import playwright, but gracefully handle if not installed
try:
    from playwright.async_api import async_playwright, Page, Browser, Error as PlaywrightError
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logger.warning("Playwright not installed. Using fallback syntax validation.")

class SentryAgent:
    """
    Automated testing agent that validates JavaScript/HTML5 games.
    
    Uses headless browser to:
    1. Load the generated HTML game
    2. Execute JavaScript code
    3. Detect console errors
    4. Check for basic functionality
    5. Report results to Debugger agent
    """
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.test_timeout = 10  # seconds
        self.max_console_errors = 5
        self.browser: Optional[Browser] = None
        self.playwright = None
        
    async def initialize(self):
        """Initialize Playwright browser for testing."""
        if PLAYWRIGHT_AVAILABLE:
            try:
                self.playwright = await async_playwright().start()
                self.browser = await self.playwright.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox']
                )
                self.logger.info("Playwright browser initialized successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize Playwright: {str(e)}")
                self.browser = None
    
    async def cleanup(self):
        """Clean up browser resources."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def test_javascript_code(self, html_content: str) -> Dict[str, Any]:
        """
        Test JavaScript/HTML5 game code in a headless browser environment.
        
        Args:
            html_content: Complete HTML file content with embedded JavaScript
            
        Returns:
            dict: Test results with success status and error details
        """
        self.logger.info("🔍 SENTRY: Starting automated code testing...")
        
        try:
            # First, do basic syntax validation
            basic_errors = self._validate_basic_syntax(html_content)
            if basic_errors:
                return {
                    "success": False,
                    "errors": basic_errors,
                    "error_count": len(basic_errors),
                    "validation_type": "basic_syntax",
                    "test_method": "static_analysis"
                }
            
            # Try to run in a simulated browser environment
            # For now, we'll do enhanced static analysis until Puppeteer is set up
            advanced_results = await self._advanced_static_testing(html_content)
            
            if advanced_results["success"]:
                self.logger.success("✅ SENTRY: All tests passed - code appears functional")
            else:
                self.logger.warning(f"⚠️ SENTRY: Found {advanced_results['error_count']} issues")
                for error in advanced_results.get("errors", []):
                    self.logger.error(f"  - {error}")
            
            return advanced_results
            
        except Exception as e:
            self.logger.error(f"SENTRY: Testing failed with exception: {str(e)}")
            return {
                "success": False,
                "errors": [f"Testing system error: {str(e)}"],
                "error_count": 1,
                "validation_type": "system_error",
                "test_method": "exception"
            }
    
    def _validate_basic_syntax(self, html_content: str) -> List[str]:
        """Perform basic syntax validation on the HTML/JavaScript code."""
        errors = []
        
        # Check for empty or very short content
        if not html_content or len(html_content.strip()) < 100:
            errors.append("Generated code is too short or empty")
            return errors
        
        # Check HTML structure
        if not html_content.strip().startswith("<!DOCTYPE html>") and not html_content.strip().startswith("<html"):
            errors.append("Missing proper HTML document structure")
        
        if "</html>" not in html_content:
            errors.append("HTML document appears incomplete - missing closing </html> tag")
        
        # Check for p5.js library inclusion
        if "p5.js" not in html_content and "p5.min.js" not in html_content:
            errors.append("Missing p5.js library reference")
        
        # Check for required p5.js functions
        if "function setup()" not in html_content and "function setup (" not in html_content:
            errors.append("Missing required p5.js setup() function")
        
        if "function draw()" not in html_content and "function draw (" not in html_content:
            errors.append("Missing required p5.js draw() function")
        
        # Check for basic JavaScript syntax issues
        javascript_errors = self._check_javascript_syntax(html_content)
        errors.extend(javascript_errors)
        
        return errors
    
    def _check_javascript_syntax(self, html_content: str) -> List[str]:
        """Check for common JavaScript syntax errors."""
        errors = []
        
        # Extract JavaScript content
        js_content = self._extract_javascript(html_content)
        if not js_content:
            errors.append("No JavaScript content found in HTML")
            return errors
        
        # Check for common syntax issues
        lines = js_content.split('\n')
        
        # Track brackets and parentheses
        bracket_count = 0
        paren_count = 0
        brace_count = 0
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            
            # Count brackets
            bracket_count += line.count('[') - line.count(']')
            paren_count += line.count('(') - line.count(')')
            brace_count += line.count('{') - line.count('}')
            
            # Check for common syntax errors
            if line.endswith('{') and not any(keyword in line for keyword in ['function', 'if', 'for', 'while', 'else', '{']):
                errors.append(f"Line {i}: Unexpected opening brace")
            
            # Check for missing semicolons on simple statements
            if (line.endswith(')') and not line.strip().startswith('if') and 
                not line.strip().startswith('for') and not line.strip().startswith('while') and
                not line.strip().startswith('function') and ';' not in line):
                pass  # This is often OK in modern JavaScript
        
        # Check final bracket balance
        if bracket_count != 0:
            errors.append(f"Unbalanced square brackets (missing {abs(bracket_count)} {'[' if bracket_count < 0 else ']'})")
        
        if paren_count != 0:
            errors.append(f"Unbalanced parentheses (missing {abs(paren_count)} {'(' if paren_count < 0 else ')'})")
        
        if brace_count != 0:
            errors.append(f"Unbalanced curly braces (missing {abs(brace_count)} {'{' if brace_count < 0 else '}'})")
        
        return errors
    
    def _extract_javascript(self, html_content: str) -> str:
        """Extract JavaScript content from HTML."""
        js_content = ""
        
        # Look for script tags
        script_pattern = r'<script[^>]*>(.*?)</script>'
        matches = re.findall(script_pattern, html_content, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            js_content += match + "\n"
        
        return js_content
    
    async def _advanced_static_testing(self, html_content: str) -> Dict[str, Any]:
        """Perform advanced static analysis of the game code."""
        errors = []
        warnings = []
        
        # Extract JavaScript for detailed analysis
        js_content = self._extract_javascript(html_content)
        
        # Check for game-specific requirements
        game_errors = self._validate_game_logic(js_content)
        errors.extend(game_errors)
        
        # Check for p5.js specific issues
        p5_errors = self._validate_p5js_usage(js_content)
        errors.extend(p5_errors)
        
        # Check for performance issues
        perf_warnings = self._check_performance_issues(js_content)
        warnings.extend(perf_warnings)
        
        success = len(errors) == 0
        
        result = {
            "success": success,
            "errors": errors,
            "warnings": warnings,
            "error_count": len(errors),
            "warning_count": len(warnings),
            "validation_type": "advanced_static",
            "test_method": "static_analysis_enhanced"
        }
        
        return result
    
    def _validate_game_logic(self, js_content: str) -> List[str]:
        """Validate basic game logic structure."""
        errors = []
        
        # Check if canvas is created
        if "createCanvas(" not in js_content:
            errors.append("Game doesn't create a canvas - missing createCanvas() call")
        
        # Check if draw loop exists and has content
        draw_match = self._find_function_body(js_content, "draw")
        if draw_match:
            draw_body = draw_match.strip()
            if len(draw_body) < 20:  # Very minimal draw function
                errors.append("Draw function appears to be empty or too minimal")
        
        # Check for basic game elements (very basic validation)
        if "rect(" not in js_content and "ellipse(" not in js_content and "circle(" not in js_content:
            errors.append("Game doesn't appear to draw any visible elements")
        
        return errors
    
    def _validate_p5js_usage(self, js_content: str) -> List[str]:
        """Validate proper p5.js API usage."""
        errors = []
        
        # Check for setup function content
        setup_body = self._find_function_body(js_content, "setup")
        if setup_body and "createCanvas(" not in setup_body:
            errors.append("setup() function missing createCanvas() call")
        
        # Check for common p5.js mistakes
        if "width" in js_content and "createCanvas(" not in js_content:
            errors.append("Code references 'width' but canvas may not be created")
        
        if "height" in js_content and "createCanvas(" not in js_content:
            errors.append("Code references 'height' but canvas may not be created")
        
        # Check for proper color usage
        if "fill(" in js_content:
            # Basic validation - could be enhanced
            pass
        
        return errors
    
    def _check_performance_issues(self, js_content: str) -> List[str]:
        """Check for potential performance issues."""
        warnings = []
        
        # Check for infinite loops (basic detection)
        if "while(true)" in js_content or "while (true)" in js_content:
            warnings.append("Potential infinite loop detected - may cause browser freeze")
        
        # Check for excessive object creation in draw loop
        draw_body = self._find_function_body(js_content, "draw")
        if draw_body:
            if draw_body.count("new ") > 5:
                warnings.append("High object creation in draw loop - may cause performance issues")
        
        return warnings
    
    def _find_function_body(self, js_content: str, function_name: str) -> Optional[str]:
        """Extract the body of a specific function."""
        import re
        
        # Pattern to match function definition and its body
        pattern = rf'function\s+{function_name}\s*\([^)]*\)\s*\{{'
        match = re.search(pattern, js_content)
        
        if not match:
            return None
        
        start_pos = match.end() - 1  # Position of the opening brace
        brace_count = 1
        i = start_pos + 1
        
        # Find the matching closing brace
        while i < len(js_content) and brace_count > 0:
            if js_content[i] == '{':
                brace_count += 1
            elif js_content[i] == '}':
                brace_count -= 1
            i += 1
        
        if brace_count == 0:
            return js_content[start_pos + 1:i - 1]  # Return function body without braces
        
        return None
    
    async def _run_in_headless_browser(self, html_content: str) -> Dict[str, Any]:
        """
        Run the HTML content in a headless browser (placeholder for future Puppeteer integration).
        For now, this is a placeholder that simulates browser testing.
        """
        self.logger.info("🌐 SENTRY: Simulating headless browser test...")
        
        # This is where we would integrate Puppeteer/Playwright
        # For now, return success for valid-looking code
        
        await asyncio.sleep(1)  # Simulate browser testing time
        
        return {
            "success": True,
            "console_errors": [],
            "runtime_errors": [],
            "test_method": "simulated_browser"
        }
    
    def _install_browser_testing(self) -> bool:
        """
        Install and configure browser testing dependencies.
        This would set up Puppeteer or Playwright for real browser testing.
        """
        try:
            # In the future, this would install and configure Puppeteer
            # For now, we'll use static analysis
            return False
        except Exception as e:
            self.logger.warning(f"Browser testing setup failed: {str(e)}")
            return False
    
    async def validate_game(self, html_content: str, game_name: str) -> Dict[str, any]:
        """
        Validate a generated HTML/JavaScript game.
        
        Args:
            html_content: The complete HTML content of the game
            game_name: Name of the game being tested
            
        Returns:
            Dictionary with validation results
        """
        results = {
            "success": False,
            "errors": [],
            "warnings": [],
            "syntax_valid": False,
            "browser_test_passed": False,
            "console_errors": [],
            "runtime_errors": []
        }
        
        # Step 1: Basic syntax validation
        syntax_results = self._validate_syntax(html_content)
        results["syntax_valid"] = syntax_results["valid"]
        results["errors"].extend(syntax_results["errors"])
        results["warnings"].extend(syntax_results["warnings"])
        
        if not results["syntax_valid"]:
            self.logger.error(f"Syntax validation failed for {game_name}")
            return results
        
        # Step 2: Browser-based testing (if available)
        if PLAYWRIGHT_AVAILABLE and self.browser:
            browser_results = await self._test_in_browser(html_content, game_name)
            results["browser_test_passed"] = browser_results["passed"]
            results["console_errors"].extend(browser_results["console_errors"])
            results["runtime_errors"].extend(browser_results["runtime_errors"])
            results["errors"].extend(browser_results["errors"])
        else:
            # Fallback: enhanced static analysis
            static_results = self._enhanced_static_analysis(html_content)
            results["errors"].extend(static_results["errors"])
            results["warnings"].extend(static_results["warnings"])
        
        # Determine overall success
        results["success"] = (
            results["syntax_valid"] and 
            len(results["errors"]) == 0 and
            (results["browser_test_passed"] if PLAYWRIGHT_AVAILABLE else True)
        )
        
        return results
    
    def _validate_syntax(self, html_content: str) -> Dict[str, any]:
        """Perform basic syntax validation on HTML/JS content."""
        results = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Check HTML structure
        if not html_content or len(html_content.strip()) < 100:
            results["errors"].append("Generated content is too short or empty")
            results["valid"] = False
            return results
        
        # Essential HTML tags
        required_tags = [
            ("<!DOCTYPE html>", "Missing DOCTYPE declaration"),
            ("<html", "Missing <html> tag"),
            ("</html>", "Missing closing </html> tag"),
            ("<head>", "Missing <head> tag"),
            ("</head>", "Missing closing </head> tag"),
            ("<body>", "Missing <body> tag"),
            ("</body>", "Missing closing </body> tag")
        ]
        
        for tag, error_msg in required_tags:
            if tag not in html_content:
                results["errors"].append(error_msg)
                results["valid"] = False
        
        # Check for p5.js library
        if "p5.js" not in html_content and "p5.min.js" not in html_content:
            results["errors"].append("Missing p5.js library reference")
            results["valid"] = False
        
        # Check for required p5.js functions
        if "function setup()" not in html_content and "setup = function()" not in html_content:
            results["errors"].append("Missing p5.js setup() function")
            results["valid"] = False
        
        if "function draw()" not in html_content and "draw = function()" not in html_content:
            results["errors"].append("Missing p5.js draw() function")
            results["valid"] = False
        
        # Check for balanced braces
        open_braces = html_content.count('{')
        close_braces = html_content.count('}')
        if open_braces != close_braces:
            results["errors"].append(f"Unbalanced braces: {open_braces} open, {close_braces} close")
            results["valid"] = False
        
        # Check for canvas element
        if "<canvas" not in html_content and "createCanvas" not in html_content:
            results["warnings"].append("No canvas element or createCanvas call found")
        
        return results
    
    def _enhanced_static_analysis(self, html_content: str) -> Dict[str, any]:
        """Enhanced static analysis when browser testing is not available."""
        results = {
            "errors": [],
            "warnings": []
        }
        
        # Extract JavaScript code
        js_matches = re.findall(r'<script[^>]*>(.*?)</script>', html_content, re.DOTALL)
        if not js_matches:
            results["errors"].append("No JavaScript code found in HTML")
            return results
        
        js_code = '\n'.join(js_matches)
        
        # Common JavaScript errors
        error_patterns = [
            (r'}\s*}\s*}', "Multiple closing braces - possible syntax error"),
            (r';\s*;', "Double semicolon detected"),
            (r'function\s+function', "Double 'function' keyword"),
            (r'const\s+const', "Double 'const' keyword"),
            (r'let\s+let', "Double 'let' keyword"),
            (r'var\s+var', "Double 'var' keyword")
        ]
        
        for pattern, msg in error_patterns:
            if re.search(pattern, js_code):
                results["errors"].append(msg)
        
        # Check for undefined variables (basic)
        common_undefined = [
            (r'\bplayer\b(?!\.)', "Reference to 'player' without definition"),
            (r'\benemy\b(?!\.)', "Reference to 'enemy' without definition"),
            (r'\bscore\b(?!\.)', "Reference to 'score' without definition")
        ]
        
        for pattern, msg in common_undefined:
            matches = re.findall(pattern, js_code)
            if matches and f"let {pattern[2:-6]}" not in js_code and f"var {pattern[2:-6]}" not in js_code:
                results["warnings"].append(msg)
        
        return results
    
    async def _test_in_browser(self, html_content: str, game_name: str) -> Dict[str, any]:
        """Test the game in an actual browser using Playwright."""
        results = {
            "passed": False,
            "console_errors": [],
            "runtime_errors": [],
            "errors": []
        }
        
        if not self.browser:
            results["errors"].append("Browser not initialized")
            return results
        
        page = None
        temp_file = None
        
        try:
            # Create temporary HTML file
            temp_file = tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.html',
                delete=False,
                encoding='utf-8'
            )
            temp_file.write(html_content)
            temp_file.close()
            
            # Create new page
            page = await self.browser.new_page()
            
            # Set up console message listener
            console_messages = []
            page.on("console", lambda msg: console_messages.append({
                "type": msg.type,
                "text": msg.text
            }))
            
            # Set up error listener
            page_errors = []
            page.on("pageerror", lambda error: page_errors.append(str(error)))
            
            # Navigate to the game
            await page.goto(f"file://{temp_file.name}", wait_until="networkidle")
            
            # Wait for p5.js to initialize
            await asyncio.sleep(2)
            
            # Check for JavaScript errors
            for msg in console_messages:
                if msg["type"] == "error":
                    results["console_errors"].append(msg["text"])
            
            results["runtime_errors"].extend(page_errors)
            
            # Test basic p5.js functionality
            try:
                # Check if canvas exists
                canvas_exists = await page.evaluate("() => document.querySelector('canvas') !== null")
                if not canvas_exists:
                    results["errors"].append("No canvas element found after initialization")
                
                # Check if p5 is defined
                p5_defined = await page.evaluate("() => typeof window.p5 !== 'undefined' || typeof p5 !== 'undefined'")
                if not p5_defined:
                    results["errors"].append("p5.js library not loaded properly")
                
                # Check if setup and draw functions exist
                setup_exists = await page.evaluate("() => typeof setup === 'function'")
                draw_exists = await page.evaluate("() => typeof draw === 'function'")
                
                if not setup_exists:
                    results["errors"].append("setup() function not defined")
                if not draw_exists:
                    results["errors"].append("draw() function not defined")
                
                # If no critical errors, mark as passed
                if (canvas_exists and p5_defined and setup_exists and draw_exists and
                    len(results["console_errors"]) == 0 and len(results["runtime_errors"]) == 0):
                    results["passed"] = True
                    
            except PlaywrightError as e:
                results["errors"].append(f"Browser evaluation error: {str(e)}")
            
        except Exception as e:
            results["errors"].append(f"Browser testing failed: {str(e)}")
            self.logger.error(f"Browser test error for {game_name}: {str(e)}")
        
        finally:
            # Cleanup
            if page:
                await page.close()
            if temp_file and os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
        
        return results
    
    def generate_test_report(self, validation_results: Dict[str, any]) -> str:
        """Generate a detailed test report."""
        report = []
        report.append("=== SENTRY AGENT TEST REPORT ===\n")
        
        # Overall status
        status = "✅ PASSED" if validation_results["success"] else "❌ FAILED"
        report.append(f"Overall Status: {status}")
        report.append(f"Syntax Valid: {'✅ Yes' if validation_results['syntax_valid'] else '❌ No'}")
        
        if PLAYWRIGHT_AVAILABLE:
            browser_status = '✅ Yes' if validation_results['browser_test_passed'] else '❌ No'
            report.append(f"Browser Test Passed: {browser_status}")
        
        # Errors
        if validation_results["errors"]:
            report.append("\n🔴 Errors:")
            for error in validation_results["errors"]:
                report.append(f"  - {error}")
        
        # Console errors
        if validation_results["console_errors"]:
            report.append("\n🔴 Console Errors:")
            for error in validation_results["console_errors"]:
                report.append(f"  - {error}")
        
        # Runtime errors
        if validation_results["runtime_errors"]:
            report.append("\n🔴 Runtime Errors:")
            for error in validation_results["runtime_errors"]:
                report.append(f"  - {error}")
        
        # Warnings
        if validation_results["warnings"]:
            report.append("\n⚠️ Warnings:")
            for warning in validation_results["warnings"]:
                report.append(f"  - {warning}")
        
        return '\n'.join(report)


# Singleton instance
_sentry_instance = None

async def get_sentry_agent() -> SentryAgent:
    """Get or create the singleton Sentry agent instance."""
    global _sentry_instance
    if _sentry_instance is None:
        _sentry_instance = SentryAgent(logger)
        await _sentry_instance.initialize()
    return _sentry_instance 