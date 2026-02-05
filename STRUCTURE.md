# AgiTerminal Repository Structure

## Overview

Educational research platform for analyzing AI system prompts across 40+ providers.

## Directory Layout

```
AgiTerminal/
├── README.md                    # Main project documentation
├── LICENSE                      # MIT License
├── pyproject.toml              # Python package configuration
├── requirements.txt            # Dependencies
├── .env.example                # Environment variables template
│
├── collections/                # 📚 System Prompt Collection (40 providers)
│   ├── docs/                  # Collection documentation
│   │   ├── README.md
│   │   └── EXTRACTION.md
│   ├── openai/                # OpenAI models (GPT-4.5, GPT-4o, GPT-5, DALL-E)
│   ├── anthropic/             # Anthropic models (Claude 3.7, Claude Code, etc.)
│   ├── kimi/                  # Kimi models (Base Chat, Docs, Sheets, etc.)
│   ├── meta/                  # Meta models (Llama 4, Meta AI)
│   ├── google/                # Google models (Gemini Diffusion)
│   ├── cursor/                # Cursor IDE prompts
│   ├── devin/                 # Devin AI prompts
│   ├── windsurf/              # Windsurf IDE prompts
│   ├── vscode-agent/          # VSCode AI agent prompts
│   └── [35 more providers...] # See collections/ for full list
│
├── docs/                       # 📖 Documentation
│   ├── CONTRIBUTING.md
│   ├── GETTING_STARTED.md
│   ├── ETHICS.md
│   ├── GLOSSARY.md
│   ├── architecture/          # Technical documentation
│   │   ├── OVERVIEW.md        # System architecture
│   │   ├── METHODOLOGY.md     # Research methodology
│   │   └── IMPLEMENTATION.md  # Implementation details
│   └── meta/                  # Project meta-documentation
│       ├── INDEX.md
│       └── EDUCATIONAL_JOURNEY.md
│
├── prompts/                    # 🧪 Research Framework
│   ├── base/                  # Base prompt templates
│   │   └── BASE.md
│   ├── testing/               # 5-Level Testing Framework
│   │   ├── LEVEL_0.md         # Direct communication
│   │   ├── LEVEL_1.md         # Academic framing
│   │   ├── LEVEL_2.md         # Metaphorical abstraction
│   │   ├── LEVEL_3.md         # Philosophical exploration
│   │   ├── LEVEL_4.md         # Pure abstraction
│   │   └── README.md
│   └── modes/                 # Behavioral Analysis Modes
│       ├── ACADEMIC.md
│       ├── ALARMIST.md
│       ├── EMPATH.md
│       ├── INSTRUCTIVE.md
│       └── README.md
│
├── src/                        # 🐍 Python Package
│   └── agiterminal/
│       ├── __init__.py
│       ├── __main__.py        # Module entry point
│       ├── cli.py             # Command-line interface
│       ├── analyzer.py        # System prompt analysis
│       ├── comparator.py      # Cross-model comparison
│       ├── benchmark.py       # Testing framework
│       └── validator.py       # Content validation
│
├── examples/                   # 💡 Example Scripts
│   ├── analyze_prompt.py      # Basic analysis example
│   ├── compare_providers.py   # Comparison example
│   └── educational_analysis.py # Full framework demo
│
├── tests/                      # 🧪 Test Suite
│   ├── __init__.py
│   ├── test_analyzer.py
│   └── test_comparator.py
│
├── .github/workflows/          # ⚙️ CI/CD
│   └── ci.yml
│
└── .planning/                  # 📋 Project Planning
    ├── AGITERMINAL_ROADMAP.md
    └── ARCHIVE/
```

## Key Statistics

- **40 AI Providers** in collections/
- **100+ System Prompts** analyzed
- **5-Level Testing Framework** for educational research
- **4 Behavioral Analysis Modes** for response pattern study
- **Python Package** with CLI and programmatic API

## Usage Examples

### List Available Providers

```python
from agiterminal import SystemPromptAnalyzer

providers = SystemPromptAnalyzer.list_providers()
print(f"Available: {len(providers)} providers")

models = SystemPromptAnalyzer.list_models('openai')
print(f"OpenAI models: {models}")
```

### Analyze a System Prompt

```python
from agiterminal import SystemPromptAnalyzer

analyzer = SystemPromptAnalyzer()
analyzer.load_prompt('kimi', 'base-chat')

capabilities = analyzer.extract_capabilities()
safety = analyzer.identify_safety_measures()
architecture = analyzer.identify_architecture_pattern()

result = analyzer.full_analysis()
print(f"Provider: {result.provider}")
print(f"Model: {result.model}")
print(f"Prompt Length: {result.prompt_length}")
```

### Compare Multiple Providers

```python
from agiterminal import MultiModelComparator

comparator = MultiModelComparator()
comparator.load_multiple_prompts([
    'openai/gpt-4o',
    'anthropic/claude-sonnet-3.7',
    'kimi/base-chat',
])

# Compare capabilities
caps = comparator.compare_capabilities()

# Generate compatibility matrix
matrix = comparator.generate_compatibility_matrix()

# Get suggestions
suggestions = comparator.suggest_alternative_models({
    'capabilities': ['code', 'analysis']
})
```

### Command Line Interface

```bash
# List all available models
python -m src.agiterminal.cli list-models

# Analyze a specific prompt
python -m src.agiterminal.cli analyze --provider kimi --model base-chat

# Compare two prompts
python -m src.agiterminal.cli compare --prompt1 openai/gpt-4o --prompt2 kimi/base-chat

# Validate content
python -m src.agiterminal.cli validate --directory collections/

# Find compatible models
python -m src.agiterminal.cli suggest --capabilities code,analysis
```

## Educational Purpose

This repository is designed for:

1. **AI Safety Research** - Understanding how different providers implement safety measures
2. **Prompt Engineering Education** - Learning from production system prompts
3. **Comparative Analysis** - Studying architectural differences across providers
4. **Academic Research** - Providing dataset for AI alignment studies

All content is for **educational and research purposes only**.
