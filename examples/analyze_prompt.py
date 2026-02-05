#!/usr/bin/env python3
"""
Example: Analyze a system prompt from the collection.

This example demonstrates how to use the SystemPromptAnalyzer
to extract information from a system prompt.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agiterminal import SystemPromptAnalyzer


def main():
    """Run the analysis example."""
    print("=" * 60)
    print("Example: Analyzing a System Prompt")
    print("=" * 60)
    
    # Initialize the analyzer
    analyzer = SystemPromptAnalyzer()
    
    # Load and analyze a prompt
    provider = "kimi"
    model = "base-chat"
    
    print(f"\nLoading: {provider}/{model}")
    print("-" * 60)
    
    try:
        # Load the prompt
        analyzer.load_prompt(provider, model)
        
        # Extract capabilities
        capabilities = analyzer.extract_capabilities()
        print(f"\n🔧 Capabilities ({len(capabilities)}):")
        for cap in capabilities:
            print(f"  • {cap}")
        
        # Identify safety measures
        safety = analyzer.identify_safety_measures()
        print(f"\n🛡️  Safety Measures ({len(safety)}):")
        for measure, desc in safety.items():
            print(f"  • {measure}")
        
        # Get architecture pattern
        architecture = analyzer.identify_architecture_pattern()
        print(f"\n🏗️  Architecture Pattern:")
        print(f"  {architecture}")
        
        # Get unique features
        features = analyzer.extract_unique_features()
        print(f"\n✨ Unique Features ({len(features)}):")
        for feature in features:
            print(f"  • {feature}")
        
        # Full analysis
        print("\n" + "=" * 60)
        print("Full Analysis Result:")
        print("=" * 60)
        
        result = analyzer.full_analysis()
        print(f"\nProvider: {result.provider}")
        print(f"Model: {result.model}")
        print(f"Prompt Length: {result.prompt_length} characters")
        print(f"Architecture: {result.architecture_pattern}")
        
    except FileNotFoundError:
        print(f"\n❌ Error: Could not find prompt for {provider}/{model}")
        print("Make sure you're running from the repository root.")
        return 1
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
