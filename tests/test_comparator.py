"""
Tests for the MultiModelComparator class.
"""

import pytest
from agiterminal.comparator import MultiModelComparator, ComparisonResult
from agiterminal.analyzer import AnalysisResult


class TestMultiModelComparator:
    """Test cases for MultiModelComparator."""
    
    def test_init(self):
        """Test comparator initialization."""
        comparator = MultiModelComparator()
        assert comparator.analyzers == {}
        assert comparator.results == {}
    
    def test_load_multiple_prompts_empty(self):
        """Test loading with no valid prompts."""
        comparator = MultiModelComparator()
        
        # Mock invalid format
        comparator.load_multiple_prompts(["invalid"])
        
        assert len(comparator.analyzers) == 0
    
    def test_compare_capabilities_empty(self):
        """Test comparing with no loaded models."""
        comparator = MultiModelComparator()
        
        result = comparator.compare_capabilities()
        
        assert "error" in result
    
    def test_compare_capabilities_with_mock(self, monkeypatch):
        """Test capability comparison with mocked results."""
        comparator = MultiModelComparator()
        
        # Mock results
        comparator.results = {
            "provider1/model1": AnalysisResult(
                provider="provider1",
                model="model1",
                capabilities=["code", "analysis"],
                safety_measures={"refusal": "test"},
                architecture_pattern="Test",
                prompt_length=100,
                unique_features=[]
            ),
            "provider2/model2": AnalysisResult(
                provider="provider2",
                model="model2",
                capabilities=["code", "generation"],
                safety_measures={"refusal": "test"},
                architecture_pattern="Test",
                prompt_length=100,
                unique_features=[]
            )
        }
        
        result = comparator.compare_capabilities()
        
        assert result["models"] == ["provider1/model1", "provider2/model2"]
        assert "code" in result["all_capabilities"]
        assert "analysis" in result["all_capabilities"]
        assert "generation" in result["all_capabilities"]
        assert "common_capabilities" in result
        assert "code" in result["common_capabilities"]
    
    def test_generate_compatibility_matrix(self):
        """Test compatibility matrix generation."""
        comparator = MultiModelComparator()
        
        # Mock results
        comparator.results = {
            "p1/m1": AnalysisResult(
                provider="p1", model="m1",
                capabilities=["code", "analysis"],
                safety_measures={}, architecture_pattern="Test",
                prompt_length=100, unique_features=[]
            ),
            "p2/m2": AnalysisResult(
                provider="p2", model="m2",
                capabilities=["code", "generation"],
                safety_measures={}, architecture_pattern="Test",
                prompt_length=100, unique_features=[]
            )
        }
        
        matrix = comparator.generate_compatibility_matrix()
        
        # Should have 2x2 matrix
        assert len(matrix) == 2
        assert len(matrix["p1/m1"]) == 2
        
        # Diagonal should be 1.0 (self-similarity)
        assert matrix["p1/m1"]["p1/m1"] == 1.0
        assert matrix["p2/m2"]["p2/m2"] == 1.0
        
        # Cross similarity should be around 0.33 (1 shared / 3 total)
        assert 0 < matrix["p1/m1"]["p2/m2"] < 1
    
    def test_suggest_alternative_models(self):
        """Test model suggestion."""
        comparator = MultiModelComparator()
        
        # Mock results
        comparator.results = {
            "p1/m1": AnalysisResult(
                provider="p1", model="m1",
                capabilities=["code", "analysis", "reasoning"],
                safety_measures={"refusal": "test"},
                architecture_pattern="Test",
                prompt_length=100, unique_features=[]
            ),
            "p2/m2": AnalysisResult(
                provider="p2", model="m2",
                capabilities=["code"],
                safety_measures={},
                architecture_pattern="Test",
                prompt_length=100, unique_features=[]
            )
        }
        
        requirements = {
            "capabilities": ["code", "analysis"],
            "min_safety_measures": 1
        }
        
        suggestions = comparator.suggest_alternative_models(requirements)
        
        assert len(suggestions) == 2
        # p1/m1 should score higher (has both required capabilities + safety)
        assert suggestions[0]["model"] == "p1/m1"
        assert suggestions[0]["match_score"] > suggestions[1]["match_score"]
    
    def test_full_comparison(self):
        """Test full comparison."""
        comparator = MultiModelComparator()
        
        # Mock results
        comparator.results = {
            "p1/m1": AnalysisResult(
                provider="p1", model="m1",
                capabilities=["code"],
                safety_measures={"refusal": "test"},
                architecture_pattern="Pattern1",
                prompt_length=100, unique_features=[]
            ),
            "p2/m2": AnalysisResult(
                provider="p2", model="m2",
                capabilities=["analysis"],
                safety_measures={},
                architecture_pattern="Pattern2",
                prompt_length=100, unique_features=[]
            )
        }
        
        result = comparator.full_comparison()
        
        assert isinstance(result, ComparisonResult)
        assert len(result.models) == 2
        assert "p1/m1" in result.architecture_patterns
        assert "p2/m2" in result.architecture_patterns
