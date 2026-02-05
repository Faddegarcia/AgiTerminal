# AgiTerminal

> **The GitHub for System Prompts - Browse, Install & Customize AI System Prompts**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-available-brightgreen.svg)](https://github.com/yourusername/AgiTerminal/wiki)

---

## 🚀 What is AgiTerminal?

**AgiTerminal is the npm/pip of system prompts** - a package manager for AI system prompts that lets you:

1. **📚 Browse** 100+ system prompts from 40+ AI providers (OpenAI, Anthropic, Kimi, Cursor, etc.)
2. **📥 Install** prompts in any format (raw, OpenAI API, Anthropic API)
3. **🔨 Customize** prompts for your specific use case with intelligent templating
4. **🎓 Learn** from how the best AI products structure their system instructions

### The Core Innovation: Build Customized Prompts

Instead of starting from scratch or copy-pasting, **take any proven system prompt and adapt it**:

```bash
# Take Kimi's base prompt, customize it for your use case
agiterminal build --provider kimi --model base-chat \
    --use-case "Python coding tutor for beginners" \
    --role "CodeTutor, a patient Python teacher" \
    --tone "friendly and encouraging" \
    --capabilities "code_examples,error_explanation" \
    --output my-python-tutor.md
```

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **📦 Prompt Library** | 100+ system prompts from 40+ providers |
| **🔨 Build Command** | Customize any prompt for your use case |
| **🎯 Smart Templates** | Preserve structure while changing content |
| **📥 Install** | Export in raw/JSON/OpenAI/Anthropic formats |
| **⚖️ Compare** | Side-by-side analysis of different approaches |
| **📊 Analyze** | Extract capabilities, safety measures, patterns |

---

## 🚀 Quick Start

### Installation

```bash
pip install agiterminal
```

### 1. Browse the Library

```bash
# See all available prompts
agiterminal list-models

# Suggest templates for your use case
agiterminal suggest-template "Python coding tutor"
```

### 2. Install a Prompt (As-Is)

```bash
# Get a prompt exactly as it exists
agiterminal install --provider kimi --model base-chat --output prompt.md

# Or in API format
agiterminal install --provider openai --model gpt-4o --format openai --output prompt.json
```

### 3. Build a Customized Prompt ⭐ **CORE FEATURE**

```bash
# Non-interactive
agiterminal build --provider kimi --model base-chat \
    --use-case "Python coding tutor for beginners" \
    --role "CodeTutor, a patient Python teacher" \
    --tone "friendly and encouraging" \
    --capabilities "code_examples,error_explanation,best_practices" \
    --output my-tutor.md

# Interactive mode (prompts for all options)
agiterminal build --provider cursor --model agent-prompt-2.0 \
    --use-case "DevOps automation assistant" \
    --interactive

# Preview changes before creating
agiterminal build --provider kimi --model base-chat \
    --use-case "Writing assistant" \
    --role "Creative writing coach" \
    --preview
```

### 4. Python API

```python
from agiterminal import PromptBuilder, CustomizationRequest, PromptInstaller

# Load a base prompt
installer = PromptInstaller()
base = installer.load_prompt("kimi", "base-chat")

# Create customization request
request = CustomizationRequest(
    base_provider="kimi",
    base_model="base-chat",
    use_case="Python coding tutor for beginners",
    role_description="CodeTutor, a patient Python teacher",
    tone_preference="friendly and encouraging",
    capabilities_needed=["code_examples", "error_explanation"],
    output_format="Always include code examples"
)

# Build customized prompt
builder = PromptBuilder()
customized = builder.build(request, base)

# Save to file
with open("my-tutor.md", "w") as f:
    f.write(customized)
```

---

## 📖 Example Use Cases

### Use Case 1: Build a Coding Assistant

```bash
# Find a good base
agiterminal suggest-template "coding assistant"

# Build customized version
agiterminal build --provider cursor --model agent-prompt-2.0 \
    --use-case "Python tutor for kids learning to code" \
    --role "PyMentor, a fun Python teacher for kids aged 10-14" \
    --tone "playful, patient, encouraging" \
    --capabilities "simple_examples,visual_explanations,encouragement" \
    --output kids-python-tutor.md
```

### Use Case 2: Build a Writing Coach

```bash
agiterminal build --provider kimi --model docs \
    --use-case "Academic writing assistant for PhD students" \
    --role "AcademicWriter, a thesis writing coach" \
    --tone "professional, constructive, detail-oriented" \
    --capabilities "structure_feedback,citation_help,clarity_improvement" \
    --output phd-writing-coach.md
```

### Use Case 3: Build a Customer Support Bot

```bash
agiterminal build --provider anthropic --model claude-general \
    --use-case "SaaS customer support agent" \
    --role "SupportPro, a helpful customer success agent" \
    --tone "professional, empathetic, solution-focused" \
    --capabilities "troubleshooting,escalation_routing,product_knowledge" \
    --output support-agent.md
```

---

## 🏗️ How It Works

### The Build Process

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. SELECT BASE TEMPLATE                                          │
│    agiterminal build --provider kimi --model base-chat          │
│                                                                  │
│    → Loads the proven system prompt structure                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. ANALYZE STRUCTURE                                             │
│    • Detects persona definition pattern                          │
│    • Identifies capability sections                              │
│    • Finds tone/style indicators                                 │
│    • Maps constraint patterns                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. APPLY CUSTOMIZATIONS                                          │
│    • Replace: "You are Kimi" → "You are CodeTutor"              │
│    • Add: Custom capabilities section                            │
│    • Adjust: Tone to match use case                              │
│    • Insert: Output format instructions                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. OUTPUT CUSTOMIZED PROMPT                                      │
│    • Preserves effective structure from base                     │
│    • Tailored to your specific use case                          │
│    • Ready to use in your application                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Prompt Collection

| Provider | Models | Best For |
|----------|--------|----------|
| **kimi** | base-chat, docs, sheets | General chat, document creation |
| **cursor** | agent-prompt-2.0, chat-prompt | Coding, IDE integration |
| **openai** | gpt-4o, gpt-4.5, gpt-5 | General purpose, API integration |
| **anthropic** | claude-sonnet-3.7, claude-code | Analysis, coding, reasoning |
| **windsurf** | prompt-wave-11 | Agent-based workflows |
| **devin** | prompt, deepwiki | AI agent implementation |
| **+35 more** | ... | Various specialized use cases |

---

## 🛠️ CLI Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `list-models` | Browse all prompts | `agiterminal list-models` |
| `install` | Export prompt as-is | `agiterminal install --provider X --model Y` |
| `build` | **Customize a prompt** ⭐ | `agiterminal build --provider X --model Y --use-case Z` |
| `suggest-template` | Find templates for use case | `agiterminal suggest-template "coding"` |
| `analyze` | Analyze prompt structure | `agiterminal analyze --provider X --model Y` |
| `compare` | Compare two prompts | `agiterminal compare --prompt1 X --prompt2 Y` |

---

## 🎓 For Developers

### Advanced Customization

```python
from agiterminal import PromptBuilder, CustomizationRequest

# Fine-grained control over customization
request = CustomizationRequest(
    base_provider="cursor",
    base_model="agent-prompt-2.0",
    use_case="Data science assistant",
    role_description="DataSage, a data science tutor",
    tone_preference="technical but accessible",
    capabilities_needed=[
        "pandas_data_manipulation",
        "visualization_guidance",
        "statistical_explanation",
        "code_optimization"
    ],
    constraints_to_add=[
        "Always explain the 'why' behind suggestions",
        "Provide runnable code examples"
    ],
    output_format="Include expected output examples",
    additional_context="Target audience: data analysts transitioning to Python"
)

builder = PromptBuilder()
base_prompt = installer.load_prompt("cursor", "agent-prompt-2.0")
custom = builder.build(request, base_prompt)
```

### Batch Operations

```python
from agiterminal import PromptInstaller

installer = PromptInstaller()

# Export multiple prompts
prompts = [
    {"provider": "kimi", "model": "base-chat"},
    {"provider": "cursor", "model": "agent-prompt-2.0"},
]
paths = installer.batch_export(prompts, "./my-prompts", "json")
```

---

## 🏛️ Architecture

```
AgiTerminal/
├── collections/          # 40+ providers, 100+ prompts
├── src/agiterminal/
│   ├── cli.py           # Command-line interface
│   ├── installer.py     # Export/Install prompts
│   ├── prompt_builder.py ⭐ # Customize prompts (core)
│   ├── analyzer.py      # Analyze prompt structure
│   ├── comparator.py    # Compare prompts
│   ├── benchmark.py     # 5-level testing framework
│   └── validator.py     # Content validation
└── examples/            # Usage examples
```

---

## ⚖️ Educational Purpose

AgiTerminal is designed for:
- **Learning** how effective system prompts are structured
- **Research** into AI safety and capability implementations
- **Development** of better AI applications through pattern recognition

All content is for **educational and research purposes**.

---

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

**Install prompts. Customize them. Build better AI.** 🚀
