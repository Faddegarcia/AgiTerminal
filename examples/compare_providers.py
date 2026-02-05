#!/usr/bin/env python3
"""
Example: Compare system prompts across providers.

This example demonstrates how to use the MultiModelComparator
to compare system prompts from different AI providers.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agiterminal import MultiModelComparator


def main():
    """Run the comparison example."""
    print("=" * 60)
    print("Example: Comparing System Prompts")
    print("=" * 60)
    
    # Initialize the comparator
    comparator = MultiModelComparator()
    
    # Models to compare
    models = [
        "openai/gpt-4o",
        "kimi/base-chat",
    ]
    
    print(f"\nLoading models: {', '.join(models)}")
    print("-" * 60)
    
    try:
        # Load the prompts
        comparator.load_multiple_prompts(models)
        
        if not comparator.results:
            print("❌ No models could be loaded.")
            return 1
        
        print(f"✅ Successfully loaded {len(comparator.results)} models")
        
        # Compare capabilities
        print("\n" + "=" * 60)
        print("Capability Comparison")
        print("=" * 60)
        
        caps = comparator.compare_capabilities()
        
        for model, capabilities in caps.get("model_capabilities", {}).items():
            print(f"\n{model}:")
            for cap in capabilities:
                print(f"  • {cap}")
        
        # Show common capabilities
        if "common_capabilities" in caps:
            print("\n🔗 Common Capabilities:")
            for cap in caps["common_capabilities"]:
                print(f"  • {cap}")
        
        # Compatibility matrix
        print("\n" + "=" * 60)
        print("Compatibility Matrix")
        print("=" * 60)
        
        matrix = comparator.generate_compatibility_matrix()
        
        # Print header
        model_names = list(matrix.keys())
        print("\n" + " " * 20, end="")
        for name in model_names:
            print(f"{name[:10]:>12}", end="")
        print()
        
        # Print rows
        for m1 in model_names:
            print(f"{m1[:20]:20}", end="")
            for m2 in model_names:
                score = matrix[m1][m2]
                print(f"{score:>12.1%}", end="")
            print()
        
        # Safety comparison
        print("\n" + "=" * 60)
        print("Safety Measures Comparison")
        print("=" * 60)
        
        safety = comparator.compare_safety_measures()
        
        for model, measures in safety.get("model_safety", {}).items():
            print(f"\n{model}:")
            for measure in measures:
                print(f"  • {measure}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n" + "=" * 60)
    print("Comparison complete!")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
