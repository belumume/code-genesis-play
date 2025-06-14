
"""
Enhanced logging system for the Genesis Engine.
Provides colored, structured output for different phases of generation.
"""
import sys
from enum import Enum
from typing import Optional
from datetime import datetime

class LogLevel(Enum):
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    PHASE = "PHASE"

class Colors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    # Standard colors
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    
    # Background colors
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"

class EngineLogger:
    """Sophisticated logging system for Genesis Engine operations."""
    
    def __init__(self, enable_colors: bool = True):
        self.enable_colors = enable_colors and sys.stdout.isatty()
        self.current_phase = None
    
    def _colorize(self, text: str, color: str) -> str:
        """Apply color to text if colors are enabled."""
        if not self.enable_colors:
            return text
        return f"{color}{text}{Colors.RESET}"
    
    def _format_timestamp(self) -> str:
        """Get formatted timestamp."""
        return datetime.now().strftime("%H:%M:%S")
    
    def _log(self, level: LogLevel, message: str, color: str = Colors.WHITE):
        """Core logging method."""
        timestamp = self._format_timestamp()
        level_str = f"[{level.value:^8}]"
        
        if level == LogLevel.PHASE:
            # Special formatting for phase headers
            separator = "=" * 60
            print(f"\n{self._colorize(separator, Colors.CYAN)}")
            print(f"{self._colorize(level_str, Colors.BG_MAGENTA + Colors.WHITE)} {self._colorize(message, Colors.BOLD + Colors.MAGENTA)}")
            print(f"{self._colorize(separator, Colors.CYAN)}")
        else:
            colored_level = self._colorize(level_str, color)
            colored_message = self._colorize(message, color)
            print(f"{Colors.DIM}[{timestamp}]{Colors.RESET} {colored_level} {colored_message}")
    
    def header(self, message: str):
        """Display a prominent header message."""
        border = "█" * len(message)
        print(f"\n{self._colorize(border, Colors.BOLD + Colors.CYAN)}")
        print(f"{self._colorize(message, Colors.BOLD + Colors.CYAN)}")
        print(f"{self._colorize(border, Colors.BOLD + Colors.CYAN)}\n")
    
    def phase(self, phase_name: str, message: str):
        """Log a new phase of operation."""
        self.current_phase = phase_name
        self._log(LogLevel.PHASE, f"{phase_name}: {message}")
    
    def info(self, message: str):
        """Log an informational message."""
        self._log(LogLevel.INFO, message, Colors.BLUE)
    
    def success(self, message: str):
        """Log a success message."""
        self._log(LogLevel.SUCCESS, f"✓ {message}", Colors.GREEN)
    
    def warning(self, message: str):
        """Log a warning message."""
        self._log(LogLevel.WARNING, f"⚠ {message}", Colors.YELLOW)
    
    def error(self, message: str):
        """Log an error message."""
        self._log(LogLevel.ERROR, f"✗ {message}", Colors.RED)
    
    def step(self, step_name: str, details: Optional[str] = None):
        """Log a step within the current phase."""
        if self.current_phase:
            prefix = f"[{self.current_phase}]"
        else:
            prefix = "[STEP]"
            
        message = f"{prefix} {step_name}"
        if details:
            message += f" - {details}"
        
        self._log(LogLevel.INFO, message, Colors.CYAN)
    
    def thinking(self, thought: str):
        """Log AI thinking/reasoning process."""
        self._log(LogLevel.INFO, f"💭 {thought}", Colors.MAGENTA)
    
    def progress(self, current: int, total: int, task: str):
        """Display progress information."""
        percentage = (current / total) * 100
        bar_length = 30
        filled_length = int(bar_length * current // total)
        bar = "█" * filled_length + "▒" * (bar_length - filled_length)
        
        progress_text = f"[{bar}] {percentage:.1f}% - {task}"
        self._log(LogLevel.INFO, progress_text, Colors.GREEN)
