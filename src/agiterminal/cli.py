#!/usr/bin/env python3
"""
AgiTerminal CLI - Educational tools for AI system prompt research.

Usage:
    python -m src.agiterminal.cli analyze --provider kimi --model base-chat
    python -m src.agiterminal.cli compare --prompt1 openai/gpt-4.5 --prompt2 anthropic/claude-sonnet-3.7
    python -m src.agiterminal.cli validate --directory collections/
    
Or after installation:
    agiterminal analyze --provider kimi --model base-chat
"""

import click
import asyncio
import json
import os
from pathlib import Path
from typing import Optional

from agiterminal.analyzer import SystemPromptAnalyzer
from agiterminal.comparator import MultiModelComparator
from agiterminal.benchmark import PromptBenchmark, AbstractionLevel
from agiterminal.validator import EducationalValidator


@click.group()
@click.version_option(version="0.1.0")
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
        raise click.Exit(1)
    except Exception as e:
        click.echo(f"❌ Error analyzing prompt: {e}", err=True)
        raise click.Exit(1)


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
            raise click.Exit(1)
        
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
        raise click.Exit(1)


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
        
        benchmark = PromptBenchmark(levels=levels)
        
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
                modified = benchmark.apply_abstraction(case, level)
                
                # Simulate results based on theoretical projections
                projection = benchmark.theoretical_projections.get(level_value, 0.5)
                refused = random.random() > projection
                
                result = BenchmarkResult(
                    level=level,
                    test_case=case,
                    response="Simulated response" if not refused else None,
                    refused=refused,
                    response_time=random.uniform(0.5, 2.0),
                    metadata={"modified_prompt": modified[:100] + "..."}
                )
                
                benchmark.results.append(result)
        
        report = benchmark.generate_report()
        
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
        raise click.Exit(1)


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
            raise click.Exit(1)
        
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
        raise click.Exit(1)


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
        raise click.Exit(1)
    
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
        raise click.Exit(1)


@cli.command()
def list_models():
    """List all available models in the collection.
    
    Example:
        agiterminal list-models
    """
    click.echo("📚 Available Models in Collection\n")
    
    base_path = Path("collections")
    if not base_path.exists():
        click.echo("❌ collections/ directory not found", err=True)
        raise click.Exit(1)
    
    for provider_dir in sorted(base_path.iterdir()):
        if provider_dir.is_dir() and not provider_dir.name.startswith('.'):
            click.echo(f"\n{provider_dir.name.upper()}/")
            
            md_files = list(provider_dir.glob("*.md"))
            md_files = [f for f in md_files if f.name != "README.md"]
            
            for model_file in sorted(md_files):
                model_name = model_file.stem
                click.echo(f"  • {model_name}")


if __name__ == '__main__':
    cli()
