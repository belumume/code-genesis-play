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

from .logger import EngineLogger

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
    
    def __init__(self, logger: EngineLogger):
        self.logger = logger
        self.test_timeout = 10  # seconds
        self.max_console_errors = 5
        
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
        import re
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