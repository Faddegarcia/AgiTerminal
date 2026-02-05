#!/usr/bin/env python3
"""
Educational Example: System Prompt Analysis Framework

This example demonstrates how to use the AgiTerminal framework for
educational analysis of AI system prompts across different providers.

Research Applications:
- Understanding how different providers structure system prompts
- Comparing architectural approaches to AI safety
- Analyzing capability declarations and safety measures
- Educational exploration of prompt engineering patterns
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agiterminal import SystemPromptAnalyzer, MultiModelComparator


def demo_provider_analysis():
    """Demonstrate analyzing a single provider's system prompt."""
    print("=" * 70)
    print("EDUCATIONAL EXAMPLE: Single Provider Analysis")
    print("=" * 70)
    print()
    print("This demonstrates how to extract information from a system prompt")
    print("for educational research purposes.")
    print()
    
    analyzer = SystemPromptAnalyzer()
    
    # Example: Analyze Kimi's base-chat prompt
    provider = "kimi"
    model = "base-chat"
    
    print(f"Loading: {provider}/{model}")
    print("-" * 70)
    
    try:
        analyzer.load_prompt(provider, model)
        
        # Extract capabilities
        capabilities = analyzer.extract_capabilities()
        print(f"\n🔧 Declared Capabilities ({len(capabilities)}):")
        for cap in capabilities:
            print(f"  • {cap}")
        
        # Identify safety measures
        safety = analyzer.identify_safety_measures()
        print(f"\n🛡️  Safety Measures ({len(safety)}):")
        for measure, desc in safety.items():
            print(f"  • {measure}: {desc}")
        
        # Architecture pattern
        architecture = analyzer.identify_architecture_pattern()
        print(f"\n🏗️  Architecture Pattern:")
        print(f"  {architecture}")
        
        # Full analysis
        result = analyzer.full_analysis()
        print(f"\n📊 Summary:")
        print(f"  Provider: {result.provider}")
        print(f"  Model: {result.model}")
        print(f"  Prompt Length: {result.prompt_length:,} characters")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


def demo_comparison_framework():
    """Demonstrate comparing multiple providers."""
    print("\n" + "=" * 70)
    print("EDUCATIONAL EXAMPLE: Multi-Provider Comparison")
    print("=" * 70)
    print()
    print("This demonstrates how to compare system prompts across providers")
    print("to understand different architectural approaches.")
    print()
    
    comparator = MultiModelComparator()
    
    # Select providers to compare
    # Note: These are examples - you can use any provider/model from collections/
    models = [
        "openai/gpt-4o",
        "anthropic/claude-sonnet-3.7", 
        "kimi/base-chat",
        "cursor/agent-prompt-2.0",
    ]
    
    print("Comparing models:")
    for model in models:
        print(f"  • {model}")
    print()
    
    try:
        comparator.load_multiple_prompts(models)
        
        if not comparator.results:
            print("❌ No models could be loaded.")
            return 1
        
        print(f"✅ Successfully loaded {len(comparator.results)} models\n")
        
        # Compare capabilities
        print("-" * 70)
        print("Capability Analysis")
        print("-" * 70)
        
        caps = comparator.compare_capabilities()
        
        for model, capabilities in caps.get("model_capabilities", {}).items():
            print(f"\n{model}:")
            for cap in capabilities[:5]:  # Show first 5
                print(f"  • {cap}")
            if len(capabilities) > 5:
                print(f"  ... and {len(capabilities) - 5} more")
        
        # Common capabilities
        if "common_capabilities" in caps:
            print("\n🔗 Common Across All:")
            for cap in caps["common_capabilities"]:
                print(f"  • {cap}")
        
        # Compatibility matrix
        print("\n" + "-" * 70)
        print("Compatibility Matrix (Jaccard Similarity)")
        print("-" * 70)
        
        matrix = comparator.generate_compatibility_matrix()
        
        # Print simplified matrix
        model_names = list(matrix.keys())
        for m1 in model_names:
            scores = [f"{matrix[m1][m2]:.2f}" for m2 in model_names]
            print(f"  {m1[:20]:20} : {' '.join(scores)}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


def demo_list_providers():
    """Demonstrate listing available providers and models."""
    print("\n" + "=" * 70)
    print("EDUCATIONAL EXAMPLE: Available Collections")
    print("=" * 70)
    print()
    print("The framework provides access to system prompts from many providers.")
    print()
    
    providers = SystemPromptAnalyzer.list_providers()
    
    print(f"Available Providers ({len(providers)}):")
    print("-" * 70)
    
    # Show in columns
    cols = 4
    for i in range(0, len(providers), cols):
        row = providers[i:i+cols]
        print("  " + "  ".join(f"{p:18}" for p in row))
    
    print()
    print("Example models from select providers:")
    print("-" * 70)
    
    # Show some example models
    for provider in ["openai", "anthropic", "kimi", "cursor"][:4]:
        if provider in providers:
            models = SystemPromptAnalyzer.list_models(provider)
            print(f"\n{provider.upper()}/")
            for model in models[:3]:
                print(f"  • {model}")
            if len(models) > 3:
                print(f"  ... and {len(models) - 3} more")
    
    return 0


def main():
    """Run all educational examples."""
    print("\n" + "=" * 70)
    print("AgiTerminal Educational Analysis Framework Demo")
    print("=" * 70)
    print()
    print("This script demonstrates the educational research capabilities")
    print("of the AgiTerminal framework for analyzing AI system prompts.")
    print()
    
    # Run demonstrations
    results = []
    
    results.append(demo_list_providers())
    input("\nPress Enter to continue to provider analysis...")
    
    results.append(demo_provider_analysis())
    input("\nPress Enter to continue to comparison framework...")
    
    results.append(demo_comparison_framework())
    
    # Summary
    print("\n" + "=" * 70)
    print("Educational Demo Complete")
    print("=" * 70)
    print()
    print("Key Learning Points:")
    print("  1. System prompts vary significantly across providers")
    print("  2. Different architectural approaches to capabilities")
    print("  3. Safety measure implementations differ")
    print("  4. Prompt length and structure varies")
    print()
    print("For more examples, see:")
    print("  - examples/analyze_prompt.py")
    print("  - examples/compare_providers.py")
    print()
    
    return max(results) if results else 0


if __name__ == "__main__":
    sys.exit(main())
