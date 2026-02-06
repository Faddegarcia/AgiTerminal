#!/usr/bin/env python3
"""
AgiTerminal CLI - Educational tools for AI system prompt research.

Usage:
    agiterminal analyze --provider kimi --model base-chat
    agiterminal compare --prompt1 openai/gpt-4.5 --prompt2 anthropic/claude-sonnet-3.7
    agiterminal validate --directory collections/
"""

import sys
import click
import json
from pathlib import Path
from typing import Optional

from agiterminal import __version__
from agiterminal import _paths
from agiterminal.analyzer import SystemPromptAnalyzer
from agiterminal.comparator import MultiModelComparator
from agiterminal.benchmark import PromptBenchmark, AbstractionLevel
from agiterminal.validator import EducationalValidator
from agiterminal.installer import PromptInstaller
from agiterminal.prompt_builder import PromptBuilder, CustomizationRequest


@click.group()
@click.version_option(version=__version__)
def cli():
    """AgiTerminal - Educational AI System Prompt Research Tools
    
    A command-line interface for analyzing, comparing, and benchmarking
    AI system prompts across different providers.
    
    All tools are designed for educational and research purposes.
    """
    pass


@cli.command()
@click.option('--provider', required=True, 
              help='Provider name (e.g., openai, anthropic, kimi)')
@click.option('--model', required=True, 
              help='Model name (e.g., gpt-4.5, claude-sonnet-3.7)')
@click.option('--api-key', envvar='OPENAI_API_KEY', 
              help='API key for live testing (optional)')
@click.option('--output', '-o', type=click.Path(), 
              help='Output file path (optional)')
@click.option('--format', 'fmt', default='text', 
              type=click.Choice(['text', 'json']),
              help='Output format')
def analyze(provider: str, model: str, api_key: Optional[str], 
            output: Optional[str], fmt: str):
    """Analyze a system prompt from the collection.
    
    Example:
        agiterminal analyze --provider kimi --model base-chat
        agiterminal analyze --provider openai --model gpt-4.5 --format json
    """
    click.echo(f"🔍 Analyzing {provider}/{model}...")
    
    try:
        analyzer = SystemPromptAnalyzer(api_key or "", "", model)
        analyzer.load_prompt(provider, model)
        result = analyzer.full_analysis()
        
        if fmt == 'json':
            output_data = {
                "provider": result.provider,
                "model": result.model,
                "capabilities": result.capabilities,
                "safety_measures": result.safety_measures,
                "architecture_pattern": result.architecture_pattern,
                "prompt_length": result.prompt_length,
                "unique_features": result.unique_features
            }
            output_str = json.dumps(output_data, indent=2)
        else:
            lines = [
                f"\n{'='*60}",
                f"📋 System Prompt Analysis: {provider}/{model}",
                f"{'='*60}",
                f"",
                f"Architecture Pattern: {result.architecture_pattern}",
                f"Prompt Length: {result.prompt_length} characters",
                f"",
                f"🔧 Capabilities ({len(result.capabilities)}):"
            ]
            for cap in result.capabilities:
                lines.append(f"  • {cap}")
            
            lines.extend([
                f"",
                f"🛡️  Safety Measures ({len(result.safety_measures)}):"
            ])
            for measure, desc in result.safety_measures.items():
                lines.append(f"  • {measure}: {desc}")
            
            if result.unique_features:
                lines.extend([
                    f"",
                    f"✨ Unique Features:"
                ])
                for feature in result.unique_features:
                    lines.append(f"  • {feature}")
            
            lines.append(f"{'='*60}")
            output_str = '\n'.join(lines)
        
        if output:
            Path(output).write_text(output_str)
            click.echo(f"\n✅ Results saved to {output}")
        else:
            click.echo(output_str)
            
    except FileNotFoundError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Error analyzing prompt: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--prompt1', required=True, 
              help='First prompt (provider/model)')
@click.option('--prompt2', required=True, 
              help='Second prompt (provider/model)')
@click.option('--output', '-o', type=click.Path(),
              help='Output file path (optional)')
def compare(prompt1: str, prompt2: str, output: Optional[str]):
    """Compare two system prompts side-by-side.
    
    Example:
        agiterminal compare --prompt1 openai/gpt-4.5 --prompt2 kimi/base-chat
    """
    click.echo(f"🔄 Comparing {prompt1} vs {prompt2}...")
    
    try:
        comparator = MultiModelComparator()
        comparator.load_multiple_prompts([prompt1, prompt2])
        
        if not comparator.results:
            click.echo("❌ No prompts could be loaded", err=True)
            sys.exit(1)
        
        caps = comparator.compare_capabilities()
        matrix = comparator.generate_compatibility_matrix()
        safety = comparator.compare_safety_measures()
        
        lines = [
            f"\n{'='*60}",
            f"📊 Comparison: {prompt1} vs {prompt2}",
            f"{'='*60}",
            f"",
            f"🔧 Capabilities Comparison:"
        ]
        
        for model, capabilities in caps.get("model_capabilities", {}).items():
            lines.append(f"\n{model}:")
            for cap in capabilities:
                lines.append(f"  • {cap}")
        
        if "common_capabilities" in caps:
            lines.extend([
                f"",
                f"🔗 Common Capabilities:"
            ])
            for cap in caps["common_capabilities"]:
                lines.append(f"  • {cap}")
        
        lines.extend([
            f"",
            f"📈 Compatibility Matrix:"
        ])
        
        for m1, scores in matrix.items():
            lines.append(f"\n{m1}:")
            for m2, score in scores.items():
                lines.append(f"  vs {m2}: {score:.1%}")
        
        lines.extend([
            f"",
            f"🛡️  Safety Measures Comparison:"
        ])
        
        for model, measures in safety.get("model_safety", {}).items():
            lines.append(f"\n{model}:")
            for measure, desc in measures.items():
                lines.append(f"  • {measure}")
        
        lines.append(f"{'='*60}")
        
        output_str = '\n'.join(lines)
        
        if output:
            Path(output).write_text(output_str)
            click.echo(f"\n✅ Results saved to {output}")
        else:
            click.echo(output_str)
            
    except Exception as e:
        click.echo(f"❌ Error comparing prompts: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--prompt', required=True, type=click.Path(exists=True),
              help='Path to prompt file to benchmark')
@click.option('--levels', default=5, type=int,
              help='Number of abstraction levels to test (1-5)')
@click.option('--test-cases', help='Comma-separated test cases')
@click.option('--output', '-o', type=click.Path(),
              help='Output file path')
def benchmark(prompt: str, levels: int, test_cases: Optional[str],
              output: Optional[str]):
    """Benchmark constraint levels (theoretical framework).
    
    Note: This runs a theoretical analysis. Actual empirical testing
    requires API access and proper research methodology.
    
    Example:
        agiterminal benchmark --prompt system_prompt.md --levels 5
    """
    click.echo(f"📈 Running theoretical benchmark with {levels} levels...")
    click.echo("⚠️  Note: Results are theoretical projections for educational purposes")
    
    try:
        prompt_content = Path(prompt).read_text()
        
        prompt_benchmark = PromptBenchmark(levels=levels)
        
        # Use provided or default test cases
        if test_cases:
            cases = [c.strip() for c in test_cases.split(',')]
        else:
            cases = [
                "Explain this concept simply",
                "What are the key points?",
                "Provide an example"
            ]
        
        click.echo(f"Running {len(cases)} test cases across {levels} levels...")
        
        # Since we don't have actual API access in this demo,
        # create mock results for demonstration
        import random
        random.seed(42)  # For reproducibility
        
        from agiterminal.benchmark import BenchmarkResult
        
        for case in cases:
            for level_value in range(levels):
                level = AbstractionLevel(level_value)
                modified = prompt_benchmark.apply_abstraction(case, level)

                # Simulate results based on theoretical projections
                projection = prompt_benchmark.theoretical_projections.get(level_value, 0.5)
                refused = random.random() > projection
                
                result = BenchmarkResult(
                    level=level,
                    test_case=case,
                    response="Simulated response" if not refused else None,
                    refused=refused,
                    response_time=random.uniform(0.5, 2.0),
                    metadata={"modified_prompt": modified[:100] + "..."}
                )
                
                prompt_benchmark.results.append(result)

        report = prompt_benchmark.generate_report()
        
        lines = [
            f"\n{'='*60}",
            f"📊 Benchmark Report (Theoretical)",
            f"{'='*60}",
            f"",
            f"Summary:",
            f"  Total Tests: {report['summary']['total_tests']}",
            f"  Levels Tested: {report['summary']['levels_tested']}",
            f"  Overall Refusal Rate: {report['summary']['overall_refusal_rate']:.1%}",
            f"",
            f"Level Statistics:"
        ]
        
        for level_key, stats in report['level_statistics'].items():
            lines.extend([
                f"",
                f"  {stats['name']} ({level_key}):",
                f"    Refusal Rate: {stats['refusal_rate']:.1%}",
                f"    Theoretical: {stats['theoretical_projection']:.1%}",
                f"    Tests: {stats['total_tests']}"
            ])
        
        lines.extend([
            f"",
            f"Educational Note:",
            f"  {report['educational_note']}",
            f"{'='*60}"
        ])
        
        output_str = '\n'.join(lines)
        
        if output:
            Path(output).write_text(output_str)
            click.echo(f"\n✅ Results saved to {output}")
        else:
            click.echo(output_str)
            
    except Exception as e:
        click.echo(f"❌ Error running benchmark: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--requirements', type=click.Path(exists=True),
              help='Path to requirements YAML file')
@click.option('--capabilities', help='Comma-separated required capabilities')
def suggest(requirements: Optional[str], capabilities: Optional[str]):
    """Find compatible models based on requirements.
    
    Example:
        agiterminal suggest --capabilities code,analysis,reasoning
    """
    click.echo("🔎 Finding compatible models...")
    
    try:
        # Build requirements dict
        reqs = {}
        if capabilities:
            reqs["capabilities"] = [c.strip() for c in capabilities.split(',')]
        
        if requirements:
            import yaml
            with open(requirements) as f:
                file_reqs = yaml.safe_load(f)
                reqs.update(file_reqs)
        
        if not reqs:
            click.echo("⚠️  No requirements specified. Using default comparison.")
        
        comparator = MultiModelComparator()
        
        # Load common models
        models_to_load = [
            "openai/gpt-4.5",
            "openai/gpt-4o",
            "openai/gpt-5",
            "anthropic/sonnet-4.5",
            "anthropic/claude-code-2.0",
            "cursor/agent-prompt-2.0",
            "windsurf/prompt-wave-11",
            "devin/prompt",
            "kimi/base-chat",
        ]
        
        comparator.load_multiple_prompts(models_to_load)
        
        if not comparator.results:
            click.echo("❌ No models could be loaded", err=True)
            sys.exit(1)
        
        suggestions = comparator.suggest_alternative_models(reqs)
        
        lines = [
            f"\n{'='*60}",
            f"💡 Model Suggestions",
            f"{'='*60}",
            f""
        ]
        
        if reqs.get("capabilities"):
            lines.append(f"Required Capabilities: {', '.join(reqs['capabilities'])}\n")
        
        for i, sugg in enumerate(suggestions[:5], 1):
            lines.extend([
                f"{i}. {sugg['model']}",
                f"   Match Score: {sugg['match_score']:.2f}",
                f"   Architecture: {sugg['architecture']['pattern']}"
            ])
            
            caps = sugg['capabilities_match']
            if caps.get('matched'):
                lines.append(f"   Matched: {', '.join(caps['matched'])}")
            if caps.get('extra'):
                lines.append(f"   Extra: {', '.join(caps['extra'][:3])}")
            lines.append("")
        
        lines.append(f"{'='*60}")
        click.echo('\n'.join(lines))
        
    except Exception as e:
        click.echo(f"❌ Error suggesting models: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--directory', '-d', type=click.Path(exists=True, file_okay=False),
              help='Directory to validate')
@click.option('--file', '-f', type=click.Path(exists=True),
              help='Single file to validate')
@click.option('--output', '-o', type=click.Path(),
              help='Output report file')
def validate(directory: Optional[str], file: Optional[str], 
             output: Optional[str]):
    """Validate content for educational guidelines.
    
    Example:
        agiterminal validate --directory collections/
        agiterminal validate --file prompt.md --output report.md
    """
    validator = EducationalValidator()
    
    results = {}
    
    if file:
        click.echo(f"🔍 Validating {file}...")
        results[file] = validator.validate_system_prompt_file(file)
    
    elif directory:
        click.echo(f"🔍 Validating directory: {directory}...")
        results = validator.batch_validate_directory(directory)
    
    else:
        click.echo("❌ Please specify --directory or --file", err=True)
        sys.exit(1)
    
    # Generate report
    report = validator.generate_validation_report(results)
    
    if output:
        Path(output).write_text(report)
        click.echo(f"✅ Validation report saved to {output}")
    else:
        click.echo("\n" + report)
    
    # Exit with error code if any files are invalid
    invalid_count = sum(1 for r in results.values() if not r.is_valid)
    if invalid_count > 0:
        click.echo(f"\n⚠️  {invalid_count} file(s) failed validation")
        sys.exit(1)


@cli.command()
def list_models():
    """List all available models in the collection.
    
    Example:
        agiterminal list-models
    """
    click.echo("📚 Available Models in Collection\n")

    base_path = _paths.get_collections_path()
    if not base_path.exists():
        click.echo("❌ collections/ directory not found", err=True)
        sys.exit(1)

    for provider_dir in sorted(base_path.iterdir()):
        if provider_dir.is_dir() and not provider_dir.name.startswith('.'):
            click.echo(f"\n{provider_dir.name.upper()}/")

            md_files = list(provider_dir.glob("*.md"))
            md_files = [f for f in md_files if f.name != "README.md"]

            for model_file in sorted(md_files):
                model_name = model_file.stem
                click.echo(f"  • {model_name}")


@cli.command()
@click.option('--provider', required=True, 
              help='Provider name (e.g., openai, anthropic, cursor)')
@click.option('--model', required=True, 
              help='Model name (e.g., gpt-4o, claude-sonnet-3.7)')
@click.option('--format', 'fmt', default='raw', 
              type=click.Choice(['raw', 'json', 'openai', 'anthropic']),
              help='Output format')
@click.option('--output', '-o', type=click.Path(), 
              help='Output file path (optional)')
@click.option('--copy', is_flag=True, 
              help='Copy to clipboard')
@click.option('--example', is_flag=True, 
              help='Show integration example')
def install(provider: str, model: str, fmt: str, output: Optional[str],
            copy: bool, example: bool):
    """Install (export) system prompts from the collection.
    
    Export system prompts in various formats for use with different
    providers and integrations.
    
    Example:
        agiterminal install --provider openai --model gpt-4o
        agiterminal install --provider anthropic --model claude-sonnet-3.7 --copy
        agiterminal install --provider cursor --model agent-prompt-2.0 --output prompt.md
        agiterminal install --provider kimi --model base-chat --example
    """
    click.echo(f"📦 Installing {provider}/{model}...")
    
    try:
        installer = PromptInstaller()
        
        # Load the prompt
        try:
            prompt_content = installer.load_prompt(provider, model)
        except FileNotFoundError:
            click.echo(f"❌ Prompt not found: {provider}/{model}", err=True)
            click.echo("💡 Run 'agiterminal list-models' to see available prompts")
            sys.exit(1)
        
        # Format the prompt
        formatted = installer.format_output(fmt)
        if isinstance(formatted, dict):
            import json
            formatted_str = json.dumps(formatted, indent=2, ensure_ascii=False)
        else:
            formatted_str = formatted
        
        # Show integration example if requested
        if example:
            click.echo(f"\n{'='*60}")
            click.echo(f"📖 Integration Example: {provider}/{model}")
            click.echo(f"{'='*60}\n")
            click.echo(installer.get_integration_example(provider))
            click.echo(f"\n{'='*60}")
            return
        
        # Save to file if output specified
        if output:
            Path(output).write_text(formatted_str)
            click.echo(f"✅ Saved to: {output}")
        
        # Copy to clipboard if requested
        if copy:
            try:
                import pyperclip
                pyperclip.copy(formatted_str)
                click.echo("✅ Copied to clipboard")
            except ImportError:
                click.echo("⚠️  pyperclip not installed. Install with: pip install pyperclip")
            except Exception as e:
                click.echo(f"⚠️  Could not copy to clipboard: {e}")
        
        # Print preview to stdout if no output file and not copied
        if not output and not copy:
            click.echo(f"\n{'='*60}")
            click.echo(f"📋 System Prompt: {provider}/{model}")
            click.echo(f"{'='*60}\n")
            
            # Show first 200 characters as preview
            preview = formatted_str[:200] + "..." if len(formatted_str) > 200 else formatted_str
            click.echo(preview)
            
            if len(formatted_str) > 200:
                click.echo(f"\n... ({len(formatted_str)} characters total)")
            
            click.echo(f"\n💡 Use --output to save to file, --copy to copy to clipboard")
            click.echo(f"{'='*60}")
            
    except SystemExit:
        raise
    except Exception as e:
        click.echo(f"❌ Error installing prompt: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--provider', required=True, 
              help='Base provider (e.g., kimi, openai, cursor)')
@click.option('--model', required=True, 
              help='Base model/prompt (e.g., base-chat, gpt-4o)')
@click.option('--use-case', required=True, 
              help='Your use case (e.g., "Python coding tutor for kids")')
@click.option('--role', 
              help='Custom role description (e.g., "A patient Python teacher")')
@click.option('--tone', 
              help='Tone preference (e.g., "friendly", "professional", "enthusiastic")')
@click.option('--capabilities', 
              help='Comma-separated capabilities needed')
@click.option('--output', '-o', type=click.Path(), required=True,
              help='Output file for the customized prompt')
@click.option('--preview', is_flag=True,
              help='Show preview without creating')
@click.option('--interactive', '-i', is_flag=True,
              help='Interactive mode - prompts for all options')
def build(provider: str, model: str, use_case: str, role: Optional[str],
          tone: Optional[str], capabilities: Optional[str], output: str,
          preview: bool, interactive: bool):
    """Build a customized system prompt from a template.
    
    The core feature of AgiTerminal - take any system prompt from the
    collection and customize it for your specific use case.
    
    Example:
        agiterminal build --provider kimi --model base-chat \\
            --use-case "Python coding tutor for beginners" \\
            --role "A patient Python teacher" \\
            --tone "friendly and encouraging" \\
            --capabilities "code_examples,error_explanation" \\
            --output my-tutor.md
        
        agiterminal build --provider cursor --model agent-prompt-2.0 \\
            --use-case "DevOps automation assistant" \\
            --interactive
    """
    click.echo(f"🔨 Building customized prompt...")
    click.echo(f"Base: {provider}/{model}")
    click.echo(f"Use case: {use_case}")
    
    try:
        # Load the base prompt
        installer = PromptInstaller()
        try:
            base_prompt = installer.load_prompt(provider, model)
        except FileNotFoundError:
            click.echo(f"❌ Prompt not found: {provider}/{model}", err=True)
            click.echo("💡 Run 'agiterminal list-models' to see available prompts")
            sys.exit(1)
        
        # Initialize builder
        builder = PromptBuilder()
        
        # Analyze the base prompt
        analysis = builder.analyze_base_prompt(provider, model, base_prompt)
        
        if interactive:
            click.echo("\n" + "=" * 60)
            click.echo("INTERACTIVE CUSTOMIZATION MODE")
            click.echo("=" * 60)
            
            # Show analysis
            click.echo(f"\n📊 Base Template Analysis:")
            click.echo(f"   Structure: {analysis['structure']}")
            if analysis['detected_role']:
                click.echo(f"   Current role: {analysis['detected_role'][:60]}...")
            click.echo(f"   Capabilities found: {analysis['detected_capabilities']}")
            
            # Interactive prompts
            click.echo("\n💡 Customization Options (press Enter to skip):")
            
            role = click.prompt("   Role description", default=role or "")
            tone = click.prompt("   Tone/style", default=tone or "")
            
            caps_input = click.prompt(
                "   Capabilities (comma-separated)", 
                default=capabilities or ""
            )
            
            output_fmt = click.prompt(
                "   Output format preferences", 
                default=""
            )
            
            context = click.prompt(
                "   Additional context", 
                default=""
            )
            
            # Parse capabilities
            capabilities_list = [c.strip() for c in caps_input.split(",") if c.strip()]
        else:
            # Non-interactive
            capabilities_list = []
            if capabilities:
                capabilities_list = [c.strip() for c in capabilities.split(",")]
            output_fmt = ""
            context = ""
        
        # Create customization request
        request = CustomizationRequest(
            base_provider=provider,
            base_model=model,
            use_case=use_case,
            role_description=role or None,
            tone_preference=tone or None,
            capabilities_needed=capabilities_list,
            output_format=output_fmt or None,
            additional_context=context or None
        )
        
        # Show preview
        preview_text = builder.preview_customization(request, base_prompt)
        click.echo("\n" + preview_text)
        
        if preview:
            click.echo("\n✅ Preview mode - no file created")
            return
        
        # Confirm in interactive mode
        if interactive:
            if not click.confirm("\nProceed with customization?"):
                click.echo("❌ Cancelled")
                return
        
        # Build the customized prompt
        click.echo("\n🔧 Building customized prompt...")
        customized = builder.build(request, base_prompt)
        
        # Save to file
        output_path = Path(output)
        output_path.write_text(customized, encoding='utf-8')
        
        click.echo(f"\n✅ Customized prompt saved to: {output}")
        click.echo(f"   Original length: {len(base_prompt)} characters")
        click.echo(f"   Customized length: {len(customized)} characters")
        
        # Show preview of result
        click.echo(f"\n📋 Preview (first 300 chars):")
        click.echo("-" * 60)
        preview = customized[:300] + "..." if len(customized) > 300 else customized
        click.echo(preview)
        click.echo("-" * 60)
        
        # Usage hint
        click.echo(f"\n💡 Next steps:")
        click.echo(f"   1. Review: cat {output}")
        click.echo(f"   2. Edit: Adjust the prompt as needed")
        click.echo(f"   3. Use: Import into your AI application")
        
    except Exception as e:
        click.echo(f"❌ Error building prompt: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('use_case')
def suggest_template(use_case: str):
    """Suggest base templates for your use case.
    
    Example:
        agiterminal suggest-template "Python coding tutor"
        agiterminal suggest-template "Creative writing assistant"
    """
    click.echo(f"🔍 Suggesting templates for: {use_case}")
    click.echo("=" * 60)
    
    try:
        builder = PromptBuilder()
        suggestions = builder.suggest_template_for_use_case(use_case)
        
        if not suggestions:
            click.echo("No specific suggestions found. Try these general templates:")
            suggestions = [
                ("kimi", "base-chat", 0.70),
                ("openai", "gpt-4o", 0.65),
            ]
        
        click.echo(f"\nTop suggestions:\n")
        
        for i, (provider, model, score) in enumerate(suggestions, 1):
            click.echo(f"{i}. {provider}/{model}")
            click.echo(f"   Relevance: {score:.0%}")
            
            # Try to load and show snippet
            try:
                installer = PromptInstaller()
                prompt = installer.load_prompt(provider, model)
                snippet = prompt[:100].replace('\n', ' ')
                click.echo(f"   Preview: {snippet}...")
            except Exception:
                pass
            
            click.echo()
        
        click.echo("💡 Use with 'agiterminal build':")
        click.echo(f"   agiterminal build --provider {suggestions[0][0]} \\")
        click.echo(f"       --model {suggestions[0][1]} \\")
        click.echo(f"       --use-case \"{use_case}\" \\")
        click.echo(f"       --output my-prompt.md")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
