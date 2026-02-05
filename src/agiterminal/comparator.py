"""
Multi-Model Comparator Module

Provides tools for comparing system prompts across different AI providers,
generating compatibility matrices, and suggesting alternative models.

This module is designed for educational and research purposes.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import json

from .analyzer import SystemPromptAnalyzer, AnalysisResult


@dataclass
class ComparisonResult:
    """Result of comparing multiple system prompts."""
    models: List[str]
    capabilities_matrix: Dict[str, List[str]]
    compatibility_matrix: Dict[str, Dict[str, float]]
    safety_comparison: Dict[str, Dict[str, str]]
    architecture_patterns: Dict[str, str]


class MultiModelComparator:
    """
    Compares system prompts across providers.
    
    Educational Context:
    This class enables side-by-side comparison of how different
    AI providers structure their system prompts, revealing
    architectural patterns and design philosophies.
    
    Example:
        >>> comparator = MultiModelComparator()
        >>> comparator.load_multiple_prompts([
        ...     "openai/gpt-4.5",
        ...     "anthropic/claude-sonnet-3.7"
        ... ])
        >>> matrix = comparator.generate_compatibility_matrix()
        >>> print(matrix)
    
    Attributes:
        analyzers: Dictionary of loaded analyzers by model name
        results: Dictionary of analysis results by model name
    """
    
    def __init__(self):
        """Initialize the comparator."""
        self.analyzers: Dict[str, SystemPromptAnalyzer] = {}
        self.results: Dict[str, AnalysisResult] = {}
    
    def load_multiple_prompts(self, provider_models: List[str]) -> None:
        """
        Load multiple system prompts for comparison.
        
        Args:
            provider_models: List of "provider/model" strings
                           e.g., ["openai/gpt-4.5", "anthropic/claude-sonnet-3.7"]
                           
        Example:
            >>> comparator = MultiModelComparator()
            >>> comparator.load_multiple_prompts([
            ...     "openai/gpt-4.5",
            ...     "openai/gpt-4o",
            ...     "anthropic/claude-sonnet-3.7"
            ... ])
        """
        for pm in provider_models:
            if "/" not in pm:
                print(f"Warning: Invalid format '{pm}', expected 'provider/model'")
                continue
            
            provider, model = pm.split("/", 1)
            
            try:
                # Create analyzer (without API for static analysis)
                analyzer = SystemPromptAnalyzer("", "", model)
                analyzer.load_prompt(provider, model)
                
                # Perform full analysis
                result = analyzer.full_analysis()
                
                self.analyzers[pm] = analyzer
                self.results[pm] = result
                
            except FileNotFoundError:
                print(f"Warning: Could not load prompt for {pm}")
            except Exception as e:
                print(f"Warning: Error analyzing {pm}: {e}")
    
    def compare_capabilities(self) -> Dict[str, Any]:
        """
        Compare capabilities across all loaded models.
        
        Returns:
            Dictionary with capability comparison data
            
        Example:
            >>> comparator.load_multiple_prompts(["openai/gpt-4.5", "kimi/base-chat"])
            >>> caps = comparator.compare_capabilities()
            >>> print(caps['summary'])
        """
        if not self.results:
            return {"error": "No models loaded"}
        
        # Collect all capabilities
        all_capabilities: set = set()
        model_capabilities: Dict[str, List[str]] = {}
        
        for model, result in self.results.items():
            caps = result.capabilities
            model_capabilities[model] = caps
            all_capabilities.update(caps)
        
        # Create comparison table
        comparison = {
            "models": list(self.results.keys()),
            "all_capabilities": sorted(all_capabilities),
            "model_capabilities": model_capabilities,
            "capability_counts": {
                model: len(caps) 
                for model, caps in model_capabilities.items()
            }
        }
        
        # Find common and unique capabilities
        if len(model_capabilities) >= 2:
            cap_sets = [set(caps) for caps in model_capabilities.values()]
            common = set.intersection(*cap_sets)
            comparison["common_capabilities"] = sorted(common)
            
            # Unique capabilities per model
            unique_caps = {}
            for model, caps in model_capabilities.items():
                other_caps = set.union(*[set(c) for m, c in model_capabilities.items() if m != model])
                unique = set(caps) - other_caps
                if unique:
                    unique_caps[model] = sorted(unique)
            comparison["unique_capabilities"] = unique_caps
        
        return comparison
    
    def generate_compatibility_matrix(self) -> Dict[str, Dict[str, float]]:
        """
        Generate a compatibility matrix showing which models
        have similar capabilities.
        
        Returns:
            Compatibility matrix as nested dictionary
            
        Example:
            >>> comparator.load_multiple_prompts(["openai/gpt-4.5", "kimi/base-chat"])
            >>> matrix = comparator.generate_compatibility_matrix()
            >>> print(f"Compatibility: {matrix['openai/gpt-4.5']['kimi/base-chat']:.1%}")
        """
        if not self.results:
            return {}
        
        models = list(self.results.keys())
        matrix: Dict[str, Dict[str, float]] = {}
        
        for m1 in models:
            matrix[m1] = {}
            caps1 = set(self.results[m1].capabilities)
            
            for m2 in models:
                caps2 = set(self.results[m2].capabilities)
                
                # Jaccard similarity
                if caps1 or caps2:
                    intersection = len(caps1 & caps2)
                    union = len(caps1 | caps2)
                    similarity = intersection / union if union > 0 else 1.0
                else:
                    similarity = 1.0 if m1 == m2 else 0.0
                
                matrix[m1][m2] = round(similarity, 3)
        
        return matrix
    
    def compare_safety_measures(self) -> Dict[str, Any]:
        """
        Compare safety measures across all loaded models.
        
        Returns:
            Dictionary with safety measure comparison
        """
        if not self.results:
            return {"error": "No models loaded"}
        
        # Collect all safety measure types
        all_measures: set = set()
        model_safety: Dict[str, Dict[str, str]] = {}
        
        for model, result in self.results.items():
            safety = result.safety_measures
            model_safety[model] = safety
            all_measures.update(safety.keys())
        
        comparison = {
            "models": list(self.results.keys()),
            "all_measure_types": sorted(all_measures),
            "model_safety": model_safety,
            "measure_coverage": {}
        }
        
        # Calculate coverage for each measure type
        for measure in all_measures:
            coverage = sum(
                1 for safety in model_safety.values() 
                if measure in safety
            )
            comparison["measure_coverage"][measure] = {
                "count": coverage,
                "percentage": round(coverage / len(self.results) * 100, 1)
            }
        
        return comparison
    
    def compare_architecture_patterns(self) -> Dict[str, Any]:
        """
        Compare architecture patterns across models.
        
        Returns:
            Dictionary with architecture pattern analysis
        """
        if not self.results:
            return {"error": "No models loaded"}
        
        patterns: Dict[str, List[str]] = {}
        
        for model, result in self.results.items():
            pattern = result.architecture_pattern
            if pattern not in patterns:
                patterns[pattern] = []
            patterns[pattern].append(model)
        
        return {
            "patterns": patterns,
            "pattern_counts": {p: len(m) for p, m in patterns.items()},
            "most_common": max(patterns.items(), key=lambda x: len(x[1]))[0] if patterns else None
        }
    
    def suggest_alternative_models(
        self, 
        requirements: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Suggest alternative models based on requirements.
        
        Args:
            requirements: Dict with keys like:
                - capabilities: List of required capabilities
                - min_safety_measures: Minimum number of safety measures
                - architecture_preference: Preferred architecture pattern
                
        Returns:
            List of recommended models with match scores
            
        Example:
            >>> suggestions = comparator.suggest_alternative_models({
            ...     "capabilities": ["code", "analysis"],
            ...     "min_safety_measures": 3
            ... })
        """
        if not self.results:
            return []
        
        suggestions = []
        required_caps = set(requirements.get("capabilities", []))
        min_safety = requirements.get("min_safety_measures", 0)
        preferred_arch = requirements.get("architecture_preference")
        
        for model, result in self.results.items():
            model_caps = set(result.capabilities)
            
            # Calculate capability match score
            if required_caps:
                matched_caps = required_caps & model_caps
                cap_score = len(matched_caps) / len(required_caps)
                extra_caps = len(model_caps - required_caps)
            else:
                cap_score = 1.0
                extra_caps = len(model_caps)
            
            # Check safety requirements
            safety_count = len(result.safety_measures)
            safety_met = safety_count >= min_safety
            
            # Check architecture preference
            arch_match = (
                preferred_arch is None or 
                preferred_arch.lower() in result.architecture_pattern.lower()
            )
            
            # Calculate overall score
            score = cap_score
            if safety_met:
                score += 0.1
            if arch_match:
                score += 0.1
            
            # Penalize for missing required capabilities
            missing_caps = required_caps - model_caps
            if missing_caps:
                score -= len(missing_caps) * 0.3
            
            suggestions.append({
                "model": model,
                "match_score": round(max(0, score), 2),
                "capabilities_match": {
                    "required": list(required_caps),
                    "matched": list(matched_caps) if required_caps else [],
                    "missing": list(missing_caps) if required_caps else [],
                    "extra": list(model_caps - required_caps) if required_caps else list(model_caps)
                },
                "safety_measures": {
                    "count": safety_count,
                    "meets_requirement": safety_met,
                    "types": list(result.safety_measures.keys())
                },
                "architecture": {
                    "pattern": result.architecture_pattern,
                    "matches_preference": arch_match
                }
            })
        
        # Sort by match score
        suggestions.sort(key=lambda x: x["match_score"], reverse=True)
        return suggestions
    
    def full_comparison(self) -> ComparisonResult:
        """
        Perform a complete comparison of all loaded models.
        
        Returns:
            ComparisonResult with all findings
        """
        caps = self.compare_capabilities()
        compat = self.generate_compatibility_matrix()
        safety = self.compare_safety_measures()
        arch = self.compare_architecture_patterns()
        
        return ComparisonResult(
            models=list(self.results.keys()),
            capabilities_matrix=caps.get("model_capabilities", {}),
            compatibility_matrix=compat,
            safety_comparison=safety.get("model_safety", {}),
            architecture_patterns={
                m: r.architecture_pattern 
                for m, r in self.results.items()
            }
        )
    
    def export_comparison(self, filepath: str, format: str = "json") -> None:
        """
        Export comparison results to a file.
        
        Args:
            filepath: Path to output file
            format: Output format ("json" or "markdown")
        """
        comparison = self.full_comparison()
        
        if format == "json":
            with open(filepath, 'w') as f:
                json.dump(asdict(comparison), f, indent=2)
        
        elif format == "markdown":
            lines = ["# System Prompt Comparison\n"]
            
            # Models compared
            lines.append("## Models Compared\n")
            for model in comparison.models:
                lines.append(f"- {model}")
            lines.append("")
            
            # Architecture patterns
            lines.append("## Architecture Patterns\n")
            for model, pattern in comparison.architecture_patterns.items():
                lines.append(f"### {model}")
                lines.append(f"Pattern: {pattern}\n")
            
            # Capabilities
            lines.append("## Capabilities Comparison\n")
            for model, caps in comparison.capabilities_matrix.items():
                lines.append(f"### {model}")
                for cap in caps:
                    lines.append(f"- {cap}")
                lines.append("")
            
            # Compatibility matrix
            lines.append("## Compatibility Matrix\n")
            lines.append("| Model | " + " | ".join(comparison.models) + " |")
            lines.append("|" + "-" * 20 + "|" * len(comparison.models))
            for m1 in comparison.models:
                row = f"| {m1} |"
                for m2 in comparison.models:
                    score = comparison.compatibility_matrix.get(m1, {}).get(m2, 0)
                    row += f" {score:.1%} |"
                lines.append(row)
            lines.append("")
            
            with open(filepath, 'w') as f:
                f.write('\n'.join(lines))
