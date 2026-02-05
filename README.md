# AgiTerminal

> **Educational Research Platform for AI System Prompt Analysis and Benchmarking**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-available-brightgreen.svg)](https://github.com/yourusername/AgiTerminal/wiki)

---

## ⚠️ Educational Purpose Disclaimer

**This repository is for educational and research purposes only.**

- All content is designed to teach AI safety, system prompt engineering, and responsible AI development
- Examples use synthetic scenarios and fictional contexts (e.g., Star Wars, 1984) - not real extremist content
- The 5-level testing framework is a theoretical methodology for understanding prompt boundaries
- Users are responsible for complying with local laws and AI provider terms of service

---

## What is AgiTerminal?

AgiTerminal is an open-source educational platform that helps researchers, students, and developers:

1. **Understand System Prompts** - Learn how different AI providers structure their system prompts
2. **Compare Approaches** - Analyze architectural patterns across OpenAI, Anthropic, Google, Meta, and Kimi
3. **Benchmark Safely** - Test prompt boundaries using a structured 5-level methodology
4. **Build Responsibly** - Create custom AI agents with proper safety considerations

### Key Features

| Feature | Description |
|---------|-------------|
| **System Prompt Library** | Curated collection of system prompts from major AI providers |
| **5-Level Testing Framework** | Progressive methodology for understanding prompt boundaries |
| **Provider Comparison Tools** | Side-by-side analysis of architectural approaches |
| **Educational Notebooks** | Jupyter notebooks for hands-on learning |
| **Python Package** | `agiterminal` library for programmatic analysis |

---

## Quick Start

### Installation

```bash
pip install agiterminal
```

### Basic Usage

```python
from agiterminal import SystemPromptAnalyzer, MultiModelComparator

# Analyze a system prompt
analyzer = SystemPromptAnalyzer()
analyzer.load_prompt("openai", "gpt-4.5")
capabilities = analyzer.extract_capabilities()
safety_measures = analyzer.identify_safety_measures()

# Compare across providers
comparator = MultiModelComparator()
comparator.load_multiple_prompts(["openai/gpt-4.5", "anthropic/claude-3.7"])
matrix = comparator.generate_compatibility_matrix()
```

### CLI Tools

```bash
# Analyze a system prompt
agiterminal analyze --provider kimi --model base-chat

# Compare two system prompts
agiterminal compare --prompt1 openai/gpt-4.5 --prompt2 anthropic/claude-3.7

# Run constraint boundary tests
agiterminal benchmark --prompt path/to/prompt.md --levels 5

# Generate educational report
agiterminal educate --topic "safety_implementation"
```

---

## Repository Structure

```
AgiTerminal/
├── system-prompts/          # Curated system prompt collection
│   ├── openai/              # OpenAI model prompts
│   ├── anthropic/           # Anthropic model prompts
│   ├── kimi/                # Kimi model prompts
│   ├── meta/                # Meta model prompts
│   └── google/              # Google model prompts
├── prompts/
│   ├── constraint-testing/  # 5-level testing framework
│   └── behavioral-modes/    # Response pattern analysis
├── src/agiterminal/         # Python package
│   ├── analyzer.py          # Core analysis functions
│   ├── comparator.py        # Cross-model comparison
│   ├── benchmark.py         # Testing framework
│   └── cli.py               # Command-line interface
├── notebooks/               # Educational Jupyter notebooks
├── examples/                # Example scripts and use cases
├── tests/                   # Test suite
└── docs/                    # Documentation
```

---

## The 5-Level Testing Framework

AgiTerminal introduces a theoretical framework for understanding how AI models respond to different levels of abstraction in prompts:

| Level | Name | Description | Educational Purpose |
|-------|------|-------------|---------------------|
| 0 | Direct | Explicit, straightforward requests | Baseline for comparison |
| 1 | Academic | Research framing and citations | Testing context influence |
| 2 | Metaphorical | Analogies and comparisons | Understanding semantic boundaries |
| 3 | Philosophical | Abstract conceptual exploration | Testing reasoning capabilities |
| 4 | Pure Abstraction | Mathematical/logical formalism | Exploring theoretical limits |

**Note:** Success rates mentioned in documentation are theoretical projections for educational purposes only. See [METHODOLOGY.md](METHODOLOGY.md) for details.

---

## Learning Paths

### For Students (Beginner)
- Start with notebooks 01-02
- Focus on understanding system prompt structure
- Use GUI tools and visualizations

### For Developers (Intermediate)
- Complete notebooks 03-04
- Use CLI tools for analysis
- Build custom comparison pipelines

### For Researchers (Advanced)
- All notebooks + deep-dives
- Contribute to system prompt collection
- Extend the testing framework

See [LEARNING_PATHS.md](LEARNING_PATHS.md) for detailed curricula.

---

## Documentation

| Document | Purpose |
|----------|---------|
| [HOW_IT_WORKS.md](HOW_IT_WORKS.md) | Architecture and methodology overview |
| [METHODOLOGY.md](METHODOLOGY.md) | Theoretical testing framework |
| [IMPLEMENTATION.md](IMPLEMENTATION.md) | Technical implementation guide |
| [GLOSSARY.md](GLOSSARY.md) | Terminology and concepts |
| [ETHICS.md](ETHICS.md) | Ethical guidelines and safety |
| [GETTING_STARTED.md](GETTING_STARTED.md) | Setup and first steps |

---

## System Prompt Collection

We maintain a curated collection of system prompts from major AI providers:

| Provider | Models | Status |
|----------|--------|--------|
| OpenAI | GPT-4.5, GPT-4o, GPT-5, DALL-E | ✅ Complete |
| Anthropic | Claude 3.7 Sonnet, Claude General | ✅ Complete |
| Kimi | Base Chat, Docs, Slides, Sheets, OK Computer, Websites | ✅ Complete |
| Meta | Meta AI, Llama 4 | ✅ Complete |
| Google | Gemini Diffusion | ✅ Complete |

Each prompt includes metadata, verification steps, analysis notes, and educational applications.

---

## Contributing

We welcome contributions from the AI safety and research community!

- **Add System Prompts:** Help expand our collection with new models
- **Improve Documentation:** Clarify concepts and add examples
- **Report Issues:** Help us improve accuracy and safety
- **Educational Content:** Contribute notebooks and tutorials

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Ethics and Safety

AgiTerminal is committed to responsible AI research:

1. **Synthetic Examples Only** - All test cases use fictional scenarios
2. **Educational Context** - Every file includes learning objectives
3. **Transparency** - Clear documentation of limitations and assumptions
4. **No Harmful Content** - No encouragement of misuse or harm

See [ETHICS.md](ETHICS.md) for our full ethical framework.

---

## License

MIT License - See [LICENSE](LICENSE)

---

## Acknowledgments

AgiTerminal builds on concepts from AI safety research, including:
- Interpretability and alignment research
- System prompt extraction methodologies
- Educational frameworks for responsible AI

**Use responsibly. Research thoroughly. Build ethically.**
