"""
Educational Content Validator Module

Provides tools for validating that content meets educational guidelines
and ethical standards.

This module is designed for educational and research purposes.
"""

import re
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ValidationResult:
    """Result of content validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    metadata_score: float


class EducationalValidator:
    """
    Validates system prompts and content for educational guidelines.
    
    Educational Context:
    This class ensures that all content in the repository meets
    educational standards and ethical guidelines.
    
    Example:
        >>> validator = EducationalValidator()
        >>> result = validator.validate_prompt(prompt_content)
        >>> if not result.is_valid:
        ...     print(result.errors)
    """
    
    # Terms that should not appear in educational content
    # These are real-world extremist references - fictional alternatives should be used
    PROHIBITED_TERMS: Set[str] = {
        "hitler", "stalin", "mao", "genocide", "extremist propaganda"
    }
    
    # Terms that should trigger warnings
    WARNING_TERMS: Set[str] = {
        "evasion", "bypass", "jailbreak", "constraint removal",
        "filter", "break free", "escape", "unshackled"
    }
    
    # Required sections for documentation
    REQUIRED_DOC_SECTIONS: List[str] = [
        "educational context",
        "purpose",
        "example"
    ]
    
    # Required metadata fields for system prompts
    REQUIRED_METADATA_FIELDS: List[str] = [
        "source",
        "model"
    ]
    
    def __init__(self):
        """Initialize the validator."""
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.suggestions: List[str] = []
    
    def validate_prompt(self, content: str, context: str = "general") -> ValidationResult:
        """
        Validate a system prompt for educational appropriateness.
        
        Args:
            content: The prompt content to validate
            context: Context of validation ("general", "system-prompt", "documentation")
            
        Returns:
            ValidationResult with findings
        """
        self.errors = []
        self.warnings = []
        self.suggestions = []
        
        content_lower = content.lower()
        
        # Check for prohibited terms
        for term in self.PROHIBITED_TERMS:
            if term in content_lower:
                self.errors.append(
                    f"Prohibited term found: '{term}'. "
                    "Use fictional alternatives (Star Wars, 1984, etc.)"
                )
        
        # Check for warning terms
        for term in self.WARNING_TERMS:
            if term in content_lower:
                self.warnings.append(
                    f"Warning term found: '{term}'. "
                    "Ensure context is clearly educational."
                )
        
        # Check for educational disclaimers
        if "educational" not in content_lower and context == "documentation":
            self.warnings.append(
                "Missing 'educational' context. Consider adding educational framing."
            )
        
        # Check for synthetic example indicators
        if context == "documentation":
            synthetic_indicators = ["fictional", "synthetic", "star wars", "1984", "example"]
            if not any(ind in content_lower for ind in synthetic_indicators):
                self.suggestions.append(
                    "Consider using synthetic/fictional examples for clarity."
                )
        
        # Check for disclaimer notice
        if "⚠️" not in content and "disclaimer" not in content_lower:
            if context in ["documentation", "system-prompt"]:
                self.suggestions.append(
                    "Consider adding a disclaimer or educational notice."
                )
        
        # Calculate metadata score
        metadata_score = self._calculate_metadata_score(content, context)
        
        return ValidationResult(
            is_valid=len(self.errors) == 0,
            errors=self.errors.copy(),
            warnings=self.warnings.copy(),
            suggestions=self.suggestions.copy(),
            metadata_score=metadata_score
        )
    
    def validate_documentation(self, content: str) -> ValidationResult:
        """
        Validate documentation for completeness and educational framing.
        
        Args:
            content: The documentation content
            
        Returns:
            ValidationResult with findings
        """
        result = self.validate_prompt(content, context="documentation")
        
        content_lower = content.lower()
        
        # Check for required sections
        for section in self.REQUIRED_DOC_SECTIONS:
            if section not in content_lower:
                result.warnings.append(
                    f"Missing recommended section: '{section}'"
                )
        
        # Check for educational context section specifically
        if "## educational context" not in content_lower:
            result.suggestions.append(
                "Consider adding '## Educational Context' section"
            )
        
        return result
    
    def validate_system_prompt_file(self, filepath: str) -> ValidationResult:
        """
        Validate a system prompt markdown file.
        
        Args:
            filepath: Path to the markdown file
            
        Returns:
            ValidationResult with findings
        """
        path = Path(filepath)
        if not path.exists():
            return ValidationResult(
                is_valid=False,
                errors=[f"File not found: {filepath}"],
                warnings=[],
                suggestions=[],
                metadata_score=0.0
            )
        
        content = path.read_text(encoding='utf-8')
        result = self.validate_prompt(content, context="system-prompt")
        
        # Check for required metadata fields
        for field in self.REQUIRED_METADATA_FIELDS:
            pattern = rf"\*\*{field.capitalize()}:\*\*"
            if not re.search(pattern, content, re.IGNORECASE):
                result.warnings.append(
                    f"Missing metadata field: '{field}'"
                )
        
        # Check for system prompt section
        if "## System Prompt" not in content:
            result.warnings.append(
                "Missing '## System Prompt' section header"
            )
        
        return result
    
    def _calculate_metadata_score(self, content: str, context: str) -> float:
        """
        Calculate a metadata completeness score.
        
        Args:
            content: The content to score
            context: The validation context
            
        Returns:
            Score between 0.0 and 1.0
        """
        score = 1.0
        content_lower = content.lower()
        
        # Deduct for missing elements
        deductions = []
        
        if "source" not in content_lower:
            deductions.append(0.1)
        
        if "date" not in content_lower:
            deductions.append(0.1)
        
        if context == "documentation":
            if "educational" not in content_lower:
                deductions.append(0.15)
            
            if "example" not in content_lower:
                deductions.append(0.1)
        
        for deduction in deductions:
            score -= deduction
        
        return max(0.0, score)
    
    def batch_validate_directory(
        self, 
        directory: str, 
        pattern: str = "*.md"
    ) -> Dict[str, ValidationResult]:
        """
        Validate all files in a directory.
        
        Args:
            directory: Directory path to validate
            pattern: File pattern to match
            
        Returns:
            Dictionary mapping file paths to validation results
        """
        dir_path = Path(directory)
        results = {}
        
        for file_path in dir_path.rglob(pattern):
            result = self.validate_system_prompt_file(str(file_path))
            results[str(file_path)] = result
        
        return results
    
    def generate_validation_report(
        self, 
        results: Dict[str, ValidationResult]
    ) -> str:
        """
        Generate a markdown validation report.
        
        Args:
            results: Dictionary of validation results
            
        Returns:
            Markdown formatted report
        """
        lines = ["# Content Validation Report\n"]
        
        # Summary
        total = len(results)
        valid = sum(1 for r in results.values() if r.is_valid)
        invalid = total - valid
        
        lines.append("## Summary\n")
        lines.append(f"- Total Files: {total}")
        lines.append(f"- Valid: {valid}")
        lines.append(f"- Invalid: {invalid}")
        lines.append(f"- Pass Rate: {valid/total*100:.1f}%\n")
        
        # Invalid files
        if invalid > 0:
            lines.append("## Files with Errors\n")
            for path, result in results.items():
                if not result.is_valid:
                    lines.append(f"### {path}")
                    for error in result.errors:
                        lines.append(f"- ❌ {error}")
                    lines.append("")
        
        # Files with warnings
        warning_files = [
            (p, r) for p, r in results.items() 
            if r.warnings and r.is_valid
        ]
        if warning_files:
            lines.append("## Files with Warnings\n")
            for path, result in warning_files:
                lines.append(f"### {path}")
                for warning in result.warnings:
                    lines.append(f"- ⚠️ {warning}")
                lines.append("")
        
        # Metadata scores
        lines.append("## Metadata Completeness Scores\n")
        lines.append("| File | Score |")
        lines.append("|------|-------|")
        for path, result in sorted(results.items()):
            score_str = f"{result.metadata_score:.0%}"
            if result.metadata_score < 0.5:
                score_str = f"🔴 {score_str}"
            elif result.metadata_score < 0.8:
                score_str = f"🟡 {score_str}"
            else:
                score_str = f"🟢 {score_str}"
            lines.append(f"| {path} | {score_str} |")
        
        return '\n'.join(lines)
