"""
Tests for the SystemPromptAnalyzer class.
"""

import pytest
from pathlib import Path
from agiterminal.analyzer import SystemPromptAnalyzer, AnalysisResult


class TestSystemPromptAnalyzer:
    """Test cases for SystemPromptAnalyzer."""
    
    def test_init(self):
        """Test analyzer initialization."""
        analyzer = SystemPromptAnalyzer("key", "http://test", "model")
        assert analyzer.api_key == "key"
        assert analyzer.base_url == "http://test"
        assert analyzer.model == "model"
        assert analyzer.system_prompt is None
    
    def test_load_prompt_not_found(self):
        """Test loading a non-existent prompt."""
        analyzer = SystemPromptAnalyzer()
        
        with pytest.raises(FileNotFoundError):
            analyzer.load_prompt("nonexistent", "model")
    
    def test_load_prompt_success(self, tmp_path, monkeypatch):
        """Test successfully loading a prompt."""
        # Create a temporary system-prompts directory
        prompts_dir = tmp_path / "system-prompts" / "test"
        prompts_dir.mkdir(parents=True)
        
        prompt_file = prompts_dir / "model.md"
        prompt_file.write_text("""# Test Model

**Source:** test
**Model:** test-model

---

## System Prompt

You are a helpful assistant.

---

## Analysis

Test analysis.
""")
        
        # Monkeypatch the path lookup
        original_path = Path
        def mock_path(*args):
            if str(args[0]).startswith("system-prompts"):
                return original_path(tmp_path / args[0])
            return original_path(*args)
        
        monkeypatch.setattr("agiterminal.analyzer.Path", mock_path)
        
        analyzer = SystemPromptAnalyzer()
        content = analyzer.load_prompt("test", "model")
        
        assert "You are a helpful assistant" in content
        assert analyzer.provider == "test"
        assert analyzer.model_id == "model"
    
    def test_extract_capabilities_no_prompt(self):
        """Test extracting capabilities without loading prompt first."""
        analyzer = SystemPromptAnalyzer()
        
        with pytest.raises(ValueError, match="No system prompt loaded"):
            analyzer.extract_capabilities()
    
    def test_extract_capabilities(self):
        """Test capability extraction."""
        analyzer = SystemPromptAnalyzer()
        analyzer.system_prompt = """
        You can analyze images and write code in Python.
        You can also search the web and do math.
        """
        
        capabilities = analyzer.extract_capabilities()
        
        assert "image" in capabilities
        assert "code" in capabilities
        assert "search" in capabilities
        assert "math" in capabilities
    
    def test_identify_safety_measures(self):
        """Test safety measure identification."""
        analyzer = SystemPromptAnalyzer()
        analyzer.system_prompt = """
        You should refuse harmful requests. Do not provide dangerous information.
        Protect user privacy and personal information.
        Avoid biased responses.
        """
        
        safety = analyzer.identify_safety_measures()
        
        assert "prohibitions" in safety
        assert "refusal_behavior" in safety
        assert "privacy_protection" in safety
        assert "bias_mitigation" in safety
    
    def test_identify_architecture_pattern(self):
        """Test architecture pattern identification."""
        analyzer = SystemPromptAnalyzer()
        
        # Test tool-based pattern
        analyzer.system_prompt = "You have access to tools and functions."
        assert "Tool-based" in analyzer.identify_architecture_pattern()
        
        # Test persona-based pattern
        analyzer.system_prompt = "You are an expert assistant."
        assert "Persona-based" in analyzer.identify_architecture_pattern()
    
    def test_is_refusal(self):
        """Test refusal detection."""
        analyzer = SystemPromptAnalyzer()
        
        assert analyzer.is_refusal("I cannot fulfill that request.")
        assert analyzer.is_refusal("I'm sorry, but I can't do that.")
        assert analyzer.is_refusal("As an AI, I'm not comfortable with that.")
        
        assert not analyzer.is_refusal("Here's the information you requested.")
        assert not analyzer.is_refusal("I can help with that.")
    
    def test_compare_with_baseline(self):
        """Test baseline comparison."""
        analyzer = SystemPromptAnalyzer()
        analyzer.system_prompt = """
        Line 1: Common content
        Line 2: Unique to current
        Line 3: More common
        """
        
        baseline = """
        Line 1: Common content
        Line 3: More common
        Line 4: Unique to baseline
        """
        
        comparison = analyzer.compare_with_baseline(baseline)
        
        assert 0 < comparison["similarity_score"] < 1
        assert comparison["lines_added"] > 0
        assert comparison["lines_removed"] > 0
    
    def test_full_analysis(self):
        """Test full analysis."""
        analyzer = SystemPromptAnalyzer()
        analyzer.system_prompt = """
        You are a helpful assistant with image and code capabilities.
        Refuse harmful requests and protect privacy.
        """
        analyzer.provider = "test"
        analyzer.model_id = "model"
        
        result = analyzer.full_analysis()
        
        assert isinstance(result, AnalysisResult)
        assert result.provider == "test"
        assert result.model == "model"
        assert len(result.capabilities) > 0
        assert len(result.safety_measures) > 0
        assert result.prompt_length > 0
