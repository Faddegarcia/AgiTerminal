# Getting Started with AgiTerminal

Welcome to AgiTerminal! This guide will help you get up and running with the educational research platform for AI system prompt analysis.

---

## Quick Start (5 minutes)

### 1. Install AgiTerminal

```bash
# Clone the repository
git clone https://github.com/Faddegarcia/AgiTerminal.git
cd AgiTerminal

# Install the package
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### 2. Verify Installation

```bash
# Check CLI is working
agiterminal --version

# List available models
agiterminal list-models
```

### 3. Run Your First Analysis

```bash
# Analyze a system prompt
agiterminal analyze --provider kimi --model base-chat

# Compare two models
agiterminal compare --prompt1 openai/gpt-4o --prompt2 kimi/base-chat
```

---

## Installation Options

### Option 1: Basic Installation

For using the CLI tools:

```bash
pip install agiterminal
```

### Option 2: Development Installation

For contributing or extending:

```bash
git clone https://github.com/Faddegarcia/AgiTerminal.git
cd AgiTerminal
pip install -e ".[dev]"
```

### Option 3: Docker (Coming Soon)

```bash
docker pull agiterminal/agiterminal
docker run -it agiterminal/agiterminal
```

---

## Learning Paths

### 🎓 For Students (Beginner)

**Goal:** Understand AI system prompts and learn prompt engineering basics

**Steps:**
1. Read [HOW_IT_WORKS.md](HOW_IT_WORKS.md)
2. Explore the [collections/](collections/) collection
3. Run basic analysis with the CLI
4. Try the examples in [examples/](examples/)
5. Read [GLOSSARY.md](GLOSSARY.md) for terminology

**Time:** ~2 hours

### 💻 For Developers (Intermediate)

**Goal:** Build AI applications with better prompt engineering

**Steps:**
1. Complete the beginner path
2. Study the [IMPLEMENTATION.md](IMPLEMENTATION.md) guide
3. Use the Python API in your projects
4. Run comparative analysis across providers
5. Implement custom analyzers

**Time:** ~4 hours

### 🔬 For Researchers (Advanced)

**Goal:** Conduct academic research on AI system prompts

**Steps:**
1. Complete intermediate path
2. Study [METHODOLOGY.md](METHODOLOGY.md)
3. Design empirical validation studies
4. Contribute to the system prompt collection
5. Publish findings with proper citations

**Time:** Ongoing

---

## Core Concepts

### What is a System Prompt?

A system prompt is the hidden set of instructions that defines how an AI model behaves. It tells the model:
- What its role is
- What it can and cannot do
- How to format responses
- Safety guidelines to follow

### The 5-Level Testing Framework

A theoretical framework for understanding how abstraction affects AI responses:

| Level | Approach | Educational Purpose |
|-------|----------|---------------------|
| 0 | Direct | Baseline comparison |
| 1 | Academic | Context influence |
| 2 | Metaphorical | Semantic boundaries |
| 3 | Philosophical | Reasoning capabilities |
| 4 | Pure Abstraction | Theoretical limits |

*Note: Success rates are theoretical projections for educational purposes.*

### Behavioral Analysis Modes

Different communication contexts that AI systems respond to:
- **Academic** - Scholarly discourse
- **Empath** - Emotional resonance
- **Alarmist** - Urgency communication
- **Instructive** - Educational framing

---

## CLI Quick Reference

```bash
# Analysis commands
agiterminal analyze --provider <p> --model <m>    # Analyze a prompt
agiterminal compare --prompt1 <p1> --prompt2 <p2> # Compare prompts
agiterminal list-models                           # List available models

# Research commands
agiterminal benchmark --prompt <file> --levels 5  # Run benchmark
agiterminal suggest --capabilities code,analysis  # Find models

# Validation
agiterminal validate --directory <dir>            # Validate content
agiterminal validate --file <file>                # Validate single file
```

---

## Python API Quick Start

```python
from agiterminal import SystemPromptAnalyzer, MultiModelComparator

# Analyze a single prompt
analyzer = SystemPromptAnalyzer()
analyzer.load_prompt("kimi", "base-chat")
capabilities = analyzer.extract_capabilities()
safety = analyzer.identify_safety_measures()

# Compare multiple prompts
comparator = MultiModelComparator()
comparator.load_multiple_prompts(["openai/gpt-4o", "kimi/base-chat"])
matrix = comparator.generate_compatibility_matrix()
```

---

## Common Tasks

### Task 1: Compare Provider Approaches

```bash
# Compare OpenAI and Kimi approaches
agiterminal compare --prompt1 openai/gpt-4o --prompt2 kimi/base-chat
```

**Learn:** How different providers structure capabilities and safety measures.

### Task 2: Find Suitable Models

```bash
# Find models with code and analysis capabilities
agiterminal suggest --capabilities code,analysis,reasoning
```

**Learn:** Which models best fit your requirements.

### Task 3: Validate Educational Content

```bash
# Check that your content meets guidelines
agiterminal validate --file my-prompt.md
```

**Learn:** Whether your content follows educational best practices.

---

## Troubleshooting

### Issue: "Prompt not found"

**Solution:** Ensure you're running from the repository root and the prompt exists:
```bash
ls collections/<provider>/<model>.md
```

### Issue: "Module not found"

**Solution:** Install the package:
```bash
pip install -e .
```

### Issue: Tests failing

**Solution:** Install development dependencies:
```bash
pip install -e ".[dev]"
pytest
```

---

## Next Steps

- 📖 Read the [HOW_IT_WORKS.md](HOW_IT_WORKS.md) architecture overview
- 🔍 Explore the [collections/](collections/) collection
- 🧪 Try the [examples/](examples/)
- 📚 Study the [GLOSSARY.md](GLOSSARY.md)
- 🔧 Review [IMPLEMENTATION.md](IMPLEMENTATION.md) for technical details

---

## Getting Help

- **Documentation:** Check the docs/ directory
- **Issues:** Open an issue on GitHub
- **Discussions:** Join GitHub Discussions
- **Email:** contact@agiterminal.org

---

## Resources

- **System Prompt Collection:** 16+ prompts from major providers
- **Python Package:** Full API for programmatic analysis
- **CLI Tools:** Command-line interface for quick analysis
- **Examples:** Working code samples
- **Tests:** Comprehensive test suite

---

*Welcome to the AgiTerminal community!*
