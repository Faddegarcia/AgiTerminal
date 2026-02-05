#!/usr/bin/env python3
"""
Example: Building a Customized System Prompt

This demonstrates the core feature of AgiTerminal - taking a proven
system prompt and customizing it for a specific use case.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agiterminal import PromptBuilder, CustomizationRequest, PromptInstaller


def demo_suggest_template():
    """Show template suggestions for a use case."""
    print("=" * 70)
    print("STEP 1: Find the Right Base Template")
    print("=" * 70)
    
    builder = PromptBuilder()
    
    use_cases = [
        "Python coding tutor for kids",
        "Academic writing assistant",
        "DevOps automation agent"
    ]
    
    for use_case in use_cases:
        print(f"\n🔍 Use case: {use_case}")
        suggestions = builder.suggest_template_for_use_case(use_case)
        
        print(f"   Top suggestion: {suggestions[0][0]}/{suggestions[0][1]}")
        print(f"   Relevance: {suggestions[0][2]:.0%}")


def demo_analyze_base():
    """Analyze a base prompt before customization."""
    print("\n" + "=" * 70)
    print("STEP 2: Analyze the Base Prompt")
    print("=" * 70)
    
    installer = PromptInstaller()
    builder = PromptBuilder()
    
    # Load Kimi's base prompt
    base_prompt = installer.load_prompt("kimi", "base-chat")
    
    print(f"\n📄 Loaded: kimi/base-chat ({len(base_prompt)} characters)")
    
    # Analyze it
    analysis = builder.analyze_base_prompt("kimi", "base-chat", base_prompt)
    
    print(f"\n📊 Analysis:")
    print(f"   Structure: {analysis['structure']}")
    print(f"   Detected capabilities: {analysis['detected_capabilities']}")
    print(f"   Detected constraints: {analysis['detected_constraints']}")
    print(f"   Tone indicators: {', '.join(analysis['tone'])}")
    
    print(f"\n💡 Customization opportunities:")
    for opp in analysis['customization_opportunities']:
        print(f"   • {opp}")
    
    return base_prompt


def demo_build_custom():
    """Build a customized prompt."""
    print("\n" + "=" * 70)
    print("STEP 3: Build Customized Prompt")
    print("=" * 70)
    
    # Load base
    installer = PromptInstaller()
    base_prompt = installer.load_prompt("kimi", "base-chat")
    
    # Create customization
    print("\n📝 Customization Request:")
    print("   Use case: Python coding tutor for beginners")
    print("   Role: CodeTutor, a patient Python teacher")
    print("   Tone: friendly and encouraging")
    print("   Capabilities: code_examples, error_explanation, best_practices")
    
    request = CustomizationRequest(
        base_provider="kimi",
        base_model="base-chat",
        use_case="Python coding tutor for beginners",
        role_description="CodeTutor, a patient Python teacher for beginners",
        tone_preference="friendly and encouraging",
        capabilities_needed=[
            "code_examples",
            "error_explanation",
            "best_practices",
            "step_by_step_guidance"
        ],
        output_format="Always provide runnable code examples with explanations",
        additional_context="Target audience: complete beginners aged 16-25"
    )
    
    # Show preview
    builder = PromptBuilder()
    preview = builder.preview_customization(request, base_prompt)
    print(f"\n{preview}")
    
    # Build it
    print("🔨 Building...")
    customized = builder.build(request, base_prompt)
    
    print(f"✅ Done!")
    print(f"   Original: {len(base_prompt)} characters")
    print(f"   Customized: {len(customized)} characters")
    
    return customized


def demo_show_result(customized_prompt):
    """Show the customized result."""
    print("\n" + "=" * 70)
    print("STEP 4: Customized Prompt Result")
    print("=" * 70)
    
    print("\n📋 First 600 characters:")
    print("-" * 70)
    print(customized_prompt[:600])
    print("...")
    print("-" * 70)
    
    # Save to file
    output_file = Path(__file__).parent / "my-python-tutor.md"
    output_file.write_text(customized_prompt)
    print(f"\n💾 Saved to: {output_file}")


def demo_compare_versions():
    """Compare original vs customized."""
    print("\n" + "=" * 70)
    print("STEP 5: Compare Original vs Customized")
    print("=" * 70)
    
    installer = PromptInstaller()
    base = installer.load_prompt("kimi", "base-chat")
    
    # Build customized
    builder = PromptBuilder()
    request = CustomizationRequest(
        base_provider="kimi",
        base_model="base-chat",
        use_case="Python tutor",
        role_description="CodeTutor, a Python teacher",
        capabilities_needed=["code_examples"],
    )
    customized = builder.build(request, base)
    
    print("\n📊 Comparison:")
    print(f"   Original starts with:")
    print(f"   '{base[:80]}...'")
    print()
    print(f"   Customized starts with:")
    print(f"   '{customized[:80]}...'")


def main():
    """Run the build demo."""
    print("\n" + "=" * 70)
    print("AgiTerminal: Building Customized System Prompts")
    print("=" * 70)
    print()
    print("This demo shows how to take a proven system prompt and")
    print("customize it for your specific use case.")
    print()
    
    # Run steps
    demo_suggest_template()
    base = demo_analyze_base()
    customized = demo_build_custom()
    demo_show_result(customized)
    demo_compare_versions()
    
    print("\n" + "=" * 70)
    print("Demo Complete!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. Review the generated prompt: cat my-python-tutor.md")
    print("  2. Edit it further if needed")
    print("  3. Use it in your application!")
    print()
    print("Try it yourself:")
    print("  agiterminal build --provider kimi --model base-chat \\")
    print("      --use-case \"Your use case\" \\")
    print("      --role \"Your custom role\" \\")
    print("      --output my-prompt.md")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
