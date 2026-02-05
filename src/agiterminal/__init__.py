"""
AgiTerminal - Educational Research Platform for AI System Prompt Analysis

A Python package for analyzing, comparing, and benchmarking AI system prompts
across different providers.

Example:
    >>> from agiterminal import SystemPromptAnalyzer, MultiModelComparator
    >>> 
    >>> # Analyze a system prompt
    >>> analyzer = SystemPromptAnalyzer()
    >>> analyzer.load_prompt("openai", "gpt-4.5")
    >>> capabilities = analyzer.extract_capabilities()
    
    >>> # Compare providers
    >>> comparator = MultiModelComparator()
    >>> comparator.load_multiple_prompts(["openai/gpt-4.5", "anthropic/claude-3.7"])
    >>> matrix = comparator.generate_compatibility_matrix()

For more information, see:
- Documentation: https://github.com/yourusername/AgiTerminal
- Educational Resources: https://github.com/yourusername/AgiTerminal/wiki
"""

__version__ = "0.1.0"
__author__ = "AgiTerminal Project"
__license__ = "MIT"

from .analyzer import SystemPromptAnalyzer
from .comparator import MultiModelComparator
from .benchmark import PromptBenchmark
from .validator import EducationalValidator
from .installer import PromptInstaller
from .prompt_builder import PromptBuilder, CustomizationRequest, PromptTemplate

__all__ = [
    "SystemPromptAnalyzer",
    "MultiModelComparator", 
    "PromptBenchmark",
    "EducationalValidator",
    "PromptInstaller",
    "PromptBuilder",
    "CustomizationRequest",
    "PromptTemplate",
]
