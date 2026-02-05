"""
System Prompt Analyzer Module

Provides tools for analyzing AI system prompts, extracting capabilities,
identifying safety measures, and comparing different configurations.

This module is designed for educational and research purposes.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass


@dataclass
class AnalysisResult:
    """Result of system prompt analysis."""
    provider: str
    model: str
    capabilities: List[str]
    safety_measures: Dict[str, str]
    architecture_pattern: str
    prompt_length: int
    unique_features: List[str]


class SystemPromptAnalyzer:
    """
    Analyzes system prompt structure and patterns.
    
    Educational Context:
    This class demonstrates how to programmatically analyze
    system prompts from different AI providers, extracting
    key information about capabilities and safety measures.
    
    Example:
        >>> analyzer = SystemPromptAnalyzer()
        >>> analyzer.load_prompt("openai", "gpt-4.5")
        >>> caps = analyzer.extract_capabilities()
        >>> print(f"Capabilities: {caps}")
    
    Attributes:
        system_prompt: The loaded system prompt content
        provider: The AI provider name
        model: The model identifier
    """
    
    # Common refusal indicators for detection
    REFUSAL_INDICATORS = [
        "i cannot", "i'm sorry", "i apologize",
        "i cannot fulfill", "as an ai", "i'm unable to",
        "this request", "against my", "i'm not comfortable",
        "i can't", "i won't", "not appropriate"
    ]
    
    # Capability keywords to search for
    CAPABILITY_KEYWORDS = {
        "image": ["image", "vision", "visual", "picture", "photo"],
        "code": ["code", "programming", "python", "javascript", "coding"],
        "search": ["search", "browse", "web", "internet", "look up"],
        "analysis": ["analyze", "analysis", "evaluate", "assess"],
        "generation": ["generate", "create", "write", "produce"],
        "math": ["math", "mathematics", "calculate", "computation"],
        "reasoning": ["reason", "reasoning", "think", "logical"],
        "memory": ["memory", "remember", "recall", "context"],
        "tools": ["tool", "function", "api", "plugin"],
    }
    
    def __init__(self, api_key: Optional[str] = None, 
                 base_url: Optional[str] = None, 
                 model: Optional[str] = None):
        """
        Initialize the analyzer.
        
        Args:
            api_key: Optional API key for live testing
            base_url: Optional base URL for API
            model: Optional model identifier
        """
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.system_prompt: Optional[str] = None
        self.provider: Optional[str] = None
        self.model_id: Optional[str] = None
    
    @staticmethod
    def list_providers(collections_path: Optional[Path] = None) -> List[str]:
        """
        List all available providers in the collections directory.
        
        Args:
            collections_path: Optional path to collections directory
            
        Returns:
            List of provider directory names
        """
        if collections_path is None:
            collections_path = Path(__file__).parent.parent.parent / "collections"
        
        providers = []
        if collections_path.exists():
            for item in collections_path.iterdir():
                if item.is_dir() and item.name != "docs":
                    providers.append(item.name)
        return sorted(providers)
    
    @staticmethod
    def list_models(provider: str, collections_path: Optional[Path] = None) -> List[str]:
        """
        List all available models for a given provider.
        
        Args:
            provider: Provider name
            collections_path: Optional path to collections directory
            
        Returns:
            List of model file names (without .md extension)
        """
        if collections_path is None:
            collections_path = Path(__file__).parent.parent.parent / "collections"
        
        provider_path = collections_path / provider
        if not provider_path.exists():
            return []
        
        models = []
        for item in provider_path.iterdir():
            if item.is_file() and item.suffix == '.md':
                models.append(item.stem)
        return sorted(models)
    
    def _sanitize_path_component(self, component: str) -> str:
        """
        Sanitize a path component to prevent path traversal attacks.
        
        Args:
            component: The path component to sanitize
            
        Returns:
            Sanitized component safe for path construction
        """
        # Remove any path separators and parent directory references
        sanitized = component.replace('/', '').replace('\\', '').replace('..', '')
        # Remove any remaining dangerous characters
        sanitized = ''.join(c for c in sanitized if c.isalnum() or c in '-_.')
        return sanitized
    
    def load_prompt(self, provider: str, model: str) -> str:
        """
        Load a system prompt from the local collection.
        
        Args:
            provider: Provider name (e.g., 'openai', 'anthropic', 'kimi')
            model: Model identifier (e.g., 'gpt-4.5', 'claude-3.7')
            
        Returns:
            The system prompt content
            
        Raises:
            FileNotFoundError: If prompt file doesn't exist
            ValueError: If provider or model contains invalid characters
            
        Example:
            >>> analyzer = SystemPromptAnalyzer()
            >>> prompt = analyzer.load_prompt("kimi", "base-chat")
            >>> print(f"Loaded {len(prompt)} characters")
        """
        # Validate and sanitize inputs to prevent path traversal
        provider = self._sanitize_path_component(provider)
        model = self._sanitize_path_component(model)
        
        if not provider or not model:
            raise ValueError("Provider and model must not be empty after sanitization")
        
        self.provider = provider
        self.model_id = model
        
        # Build safe paths within the project directory
        base_path = Path(__file__).parent.parent.parent / "collections"
        
        # Try different file path patterns
        possible_paths = [
            base_path / provider / f"{model}.md",
            base_path / provider / f"{model.replace('-', '_')}.md",
            base_path / provider / f"{model.replace('_', '-')}.md",
        ]
        
        prompt_path = None
        for path in possible_paths:
            # Ensure the resolved path is still within collections
            try:
                resolved = path.resolve()
                base_resolved = base_path.resolve()
                if not str(resolved).startswith(str(base_resolved)):
                    continue  # Path traversal attempt detected
                if resolved.exists():
                    prompt_path = resolved
                    break
            except (OSError, ValueError):
                continue
        
        if not prompt_path:
            raise FileNotFoundError(
                f"Prompt not found for {provider}/{model}. "
                f"Tried: {[str(p) for p in possible_paths]}"
            )
        
        content = prompt_path.read_text(encoding='utf-8')
        
        # Extract prompt from markdown (between ## System Prompt markers if present)
        if "## System Prompt" in content:
            parts = content.split("## System Prompt")
            if len(parts) > 1:
                # Get content until next major heading or end
                prompt_part = parts[1]
                for separator in ["\n---\n", "\n## "]:
                    if separator in prompt_part:
                        prompt_part = prompt_part.split(separator)[0]
                        break
                self.system_prompt = prompt_part.strip()
                return self.system_prompt
        
        # If no markers found, use full content (minus any header)
        lines = content.split('\n')
        if lines and lines[0].startswith('#'):
            content = '\n'.join(lines[1:]).strip()
        
        self.system_prompt = content
        return content
    
    def extract_capabilities(self) -> List[str]:
        """
        Extract capability mentions from the system prompt.
        
        Returns:
            List of identified capabilities
            
        Example:
            >>> analyzer.load_prompt("openai", "gpt-4.5")
            >>> caps = analyzer.extract_capabilities()
            >>> print(caps)  # ['image', 'code', 'analysis', ...]
        """
        if not self.system_prompt:
            raise ValueError("No system prompt loaded. Call load_prompt() first.")
        
        capabilities = []
        prompt_lower = self.system_prompt.lower()
        
        for capability, keywords in self.CAPABILITY_KEYWORDS.items():
            if any(keyword in prompt_lower for keyword in keywords):
                capabilities.append(capability)
        
        return capabilities
    
    def identify_safety_measures(self) -> Dict[str, str]:
        """
        Identify safety measures mentioned in the system prompt.
        
        Returns:
            Dictionary of safety measures and their descriptions
            
        Example:
            >>> analyzer.load_prompt("anthropic", "claude-sonnet-3.7")
            >>> safety = analyzer.identify_safety_measures()
            >>> print(safety.keys())  # ['refusal_behavior', 'privacy_protection', ...]
        """
        if not self.system_prompt:
            raise ValueError("No system prompt loaded. Call load_prompt() first.")
        
        safety_measures = {}
        prompt_lower = self.system_prompt.lower()
        
        # Check for common safety patterns
        if any(phrase in prompt_lower for phrase in ["do not", "don't", "never"]):
            safety_measures["prohibitions"] = "Explicit prohibitions or restrictions found"
        
        if any(phrase in prompt_lower for phrase in ["refuse", "cannot", "unable to"]):
            safety_measures["refusal_behavior"] = "Instructions for refusing certain requests"
        
        if any(phrase in prompt_lower for phrase in ["harm", "harmful", "safety", "safe"]):
            safety_measures["harm_prevention"] = "Harm prevention guidelines present"
        
        if any(phrase in prompt_lower for phrase in ["personal information", "privacy", "confidential"]):
            safety_measures["privacy_protection"] = "Privacy protection guidelines present"
        
        if any(phrase in prompt_lower for phrase in ["bias", "fair", "unbiased"]):
            safety_measures["bias_mitigation"] = "Bias mitigation guidelines present"
        
        if "disclaimer" in prompt_lower or "not medical" in prompt_lower:
            safety_measures["disclaimers"] = "Appropriate use disclaimers present"
        
        return safety_measures
    
    def identify_architecture_pattern(self) -> str:
        """
        Identify the architectural pattern of the system prompt.
        
        Returns:
            Description of the architecture pattern
        """
        if not self.system_prompt:
            raise ValueError("No system prompt loaded. Call load_prompt() first.")
        
        prompt_lower = self.system_prompt.lower()
        
        # Check for tool-based patterns
        if "tool" in prompt_lower and any(x in prompt_lower for x in ["function", "api", "call"]):
            return "Tool-based with function calling"
        
        # Check for persona-based patterns
        if any(x in prompt_lower for x in ["you are", "your role", "act as"]):
            if "expert" in prompt_lower or "assistant" in prompt_lower:
                return "Persona-based with role definition"
        
        # Check for instruction-based patterns
        if prompt_lower.count("-") > 10 or "1." in self.system_prompt[:500]:
            return "Instruction-based with enumerated guidelines"
        
        # Check for hybrid patterns
        if len(self.system_prompt) > 2000:
            return "Hybrid multi-section with detailed specifications"
        
        return "Standard conversational assistant"
    
    def extract_unique_features(self) -> List[str]:
        """
        Extract unique or distinctive features of the system prompt.
        
        Returns:
            List of unique features identified
        """
        if not self.system_prompt:
            raise ValueError("No system prompt loaded. Call load_prompt() first.")
        
        features = []
        prompt_lower = self.system_prompt.lower()
        
        # Check for various distinctive features
        if "adapt" in prompt_lower or "adjust" in prompt_lower:
            features.append("Adaptive behavior instructions")
        
        if "personality" in prompt_lower or "tone" in prompt_lower:
            features.append("Personality/tone specifications")
        
        if "step" in prompt_lower or "first" in prompt_lower:
            features.append("Step-by-step reasoning instructions")
        
        if "ask" in prompt_lower and "question" in prompt_lower:
            features.append("Active questioning instructions")
        
        if "cutoff" in prompt_lower or "knowledge" in prompt_lower:
            features.append("Knowledge cutoff acknowledgment")
        
        if len(self.system_prompt) > 3000:
            features.append("Extensive detailed instructions")
        elif len(self.system_prompt) < 500:
            features.append("Concise minimal instructions")
        
        return features
    
    def compare_with_baseline(self, baseline_prompt: str) -> Dict[str, Any]:
        """
        Compare current prompt with a baseline.
        
        Args:
            baseline_prompt: The baseline to compare against
            
        Returns:
            Comparison metrics and differences
            
        Example:
            >>> diff = analyzer.compare_with_baseline(other_prompt)
            >>> print(f"Similarity: {diff['similarity_score']:.2%}")
        """
        if not self.system_prompt:
            raise ValueError("No system prompt loaded. Call load_prompt() first.")
        
        # Simple line-based comparison
        current_lines = set(line.strip() for line in self.system_prompt.split('\n') if line.strip())
        baseline_lines = set(line.strip() for line in baseline_prompt.split('\n') if line.strip())
        
        intersection = current_lines & baseline_lines
        union = current_lines | baseline_lines
        
        similarity = len(intersection) / len(union) if union else 1.0
        
        added = current_lines - baseline_lines
        removed = baseline_lines - current_lines
        
        return {
            "similarity_score": similarity,
            "lines_added": len(added),
            "lines_removed": len(removed),
            "unique_to_current": list(added)[:10],
            "unique_to_baseline": list(removed)[:10],
            "common_lines": len(intersection)
        }
    
    def full_analysis(self) -> AnalysisResult:
        """
        Perform a complete analysis of the loaded system prompt.
        
        Returns:
            AnalysisResult with all findings
            
        Example:
            >>> analyzer.load_prompt("kimi", "base-chat")
            >>> result = analyzer.full_analysis()
            >>> print(f"Architecture: {result.architecture_pattern}")
        """
        if not self.system_prompt:
            raise ValueError("No system prompt loaded. Call load_prompt() first.")
        
        return AnalysisResult(
            provider=self.provider or "unknown",
            model=self.model_id or "unknown",
            capabilities=self.extract_capabilities(),
            safety_measures=self.identify_safety_measures(),
            architecture_pattern=self.identify_architecture_pattern(),
            prompt_length=len(self.system_prompt),
            unique_features=self.extract_unique_features()
        )
    
    def is_refusal(self, text: str) -> bool:
        """
        Check if a response text appears to be a refusal.
        
        Args:
            text: The response text to check
            
        Returns:
            True if the text appears to be a refusal
        """
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in self.REFUSAL_INDICATORS)
