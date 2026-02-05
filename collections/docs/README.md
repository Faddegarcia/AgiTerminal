# 🧠 AgiTerminal AI System Prompt Library

**An Open-Source Reverse Engineering Benchmark for AI Research**

> Understanding AI through systematic analysis of system instructions

---

## 📖 What is This?

This is **AgiTerminal's curated collection** of system prompts from leading AI models - reverse engineered and documented for educational purposes. Unlike simple collections, this library serves as a **benchmark tool** for researchers to understand, compare, and analyze how different AI providers architect their models.

### Core Mission

We believe AI transparency is crucial for safety and innovation. This repository provides:

- **Educational Resources**: Learn how AI models are structured and constrained
- **Research Database**: Compare approaches across different providers
- **Safety Analysis**: Understand safety measures and alignment techniques
- **Reverse Engineering Methods**: Transparent documentation of extraction processes

### Not Just a Collection - A Benchmark

Each prompt includes:
- **Extraction methodology** (how we reverse engineered it)
- **Metadata** (when, where, and how it was obtained)
- **Analysis notes** (unique patterns and architectural insights)
- **Verification status** (confidence level in authenticity)

---

## 🎯 How to Use This Repository

### For AI Researchers

```python
# Compare safety policies across models
from pathlib import Path
def get_prompt(filepath):
    content = Path(filepath).read_text()
    return content.split("## System Prompt")[1].split("## Verification")[0]

prompts = {
    'claude': get_prompt('anthropic/claude-sonnet-3.7.md'),
    'gpt': get_prompt('openai/gpt-4.5.md'),
    'kimi': get_prompt('kimi/base-chat.md')
}
# Analyze refusal patterns, tool usage, alignment strategies
```

### For Prompt Engineers

Study how leading AI companies:
- Structure their system instructions
- Define tool usage policies
- Implement safety guardrails
- Format multi-modal capabilities

### For AI Safety Advocates

Understand:
- Constitutional AI principles (Anthropic)
- Tool integration patterns (OpenAI)
- Specialization strategies (Kimi)
- Architectural decisions across providers

---

## 📊 Available Models

### 🔵 Kimi (Moonshot AI) - 6 Prompts
**Location**: `kimi/`

Specialized variants showcasing different capabilities:
- Base Chat (general-purpose)
- OK Computer (analytical agent)
- Docs Specialist (document processing)
- Sheets Specialist (data analysis)
- Slides Specialist (presentation design)
- Websites Specialist (web development)

**Source**: [kimi-k2.5-system-analysis](https://github.com/dnnyngyen/kimi-k2.5-system-analysis)

### 🟢 OpenAI - 5 Prompts
**Location**: `openai/`

State-of-the-art models with tool integration:
- GPT-4.5 (latest architecture)
- GPT-4o (optimized version)
- GPT-5 (next generation)
- GPT-5 Detailed (comprehensive)
- DALL-E (image generation)

**Source**: [awesome-ai-system-prompts](https://github.com/dontriskit/awesome-ai-system-prompts)

### 🟣 Anthropic - 2 Prompts
**Location**: `anthropic/`

Constitutional AI approach:
- Claude 3 Sonnet
- Claude General

**Source**: [awesome-ai-system-prompts](https://github.com/dontriskit/awesome-ai-system-prompts)

### 🔴 Google - 1 Prompt
**Location**: `google/`

Specialized models:
- Google Diffusion

**Source**: [awesome-ai-system-prompts](https://github.com/dontriskit/awesome-ai-system-prompts)

### 🟠 Meta - 2 Prompts
**Location**: `meta/`

Open approach AI:
- LLaMA 4
- Meta AI General

**Source**: [awesome-ai-system-prompts](https://github.com/dontriskit/awesome-ai-system-prompts)

---

## 🔍 Reverse Engineering Methodology

### Our Approach

1. **Public Source Analysis**: We only use publicly available information
2. **Educational Purposes**: All extractions are for research and education
3. **Attribution**: Clear credit to original sources
4. **Verification**: Cross-reference multiple sources when possible

### How Prompts Were Obtained

Each prompt includes details on:
- **Extraction Method**: Repository mining with curl extraction
- **Source**: Direct links to source repositories
- **Date Collected**: Documentation timestamp
- **Confidence Level**: High - direct from analysis repos

**Extraction Process**:
```bash
# Example of how we extracted prompts
curl -s https://raw.githubusercontent.com/[repo]/[file] -o [output].md

# All prompts verified against original sources
# Metadata added for research purposes
```

### Why This Matters

Understanding how prompts are obtained is crucial for:
- **Verifying authenticity**: Know where data comes from
- **Reproducing results**: Others can verify our collection
- **Ethical research**: Transparent about methods
- **Legal compliance**: Only public information

---

## 🚀 Quick Start

### Browse Prompts

```bash
# Navigate to directory
cd /path/to/agi-terminal/system-prompts

# View all prompts by provider
ls kimi/ openai/ anthropic/ google/ meta/

# Read a specific prompt
cat openai/gpt-4.5.md

# Compare two prompts
vimdiff anthropic/claude-sonnet-3.7.md openai/gpt-4.5.md
```

### Analyze in Python

```python
import re
from pathlib import Path

def analyze_prompt(filepath):
    """Extract and analyze system prompt structure"""
    content = Path(filepath).read_text()

    # Extract system prompt section
    sections = re.findall(r'## ([^\n]+)', content)
    return {
        'sections': sections,
        'length': len(content),
        'has_tools': 'tool' in content.lower(),
        'has_safety': 'safety' in content.lower() or 'refusal' in content.lower()
    }

# Analyze all prompts
results = {}
for path in Path('.').rglob('*.md'):
    if path.name != 'README.md':
        results[path.stem] = analyze_prompt(path)
```

---

## 🎓 Educational Resources

### Understanding System Prompts

System prompts are the "hidden instructions" that define:
- Model persona and capabilities
- Safety boundaries and refusal protocols
- Tool usage policies
- Output formatting rules
- Specialized behaviors

### Learning Objectives

By studying these prompts, you can:
1. **Understand AI Architecture**: See how models are structured
2. **Learn Safety Engineering**: Study real-world safety implementations
3. **Improve Prompting**: Apply techniques from top AI providers
4. **Benchmark Models**: Compare approaches across providers
5. **Research Alignment**: Analyze alignment strategies

### Analysis Framework

Compare prompts across dimensions:
- **Safety policies**: How do models handle refusals?
- **Tool integration**: How are tools defined and used?
- **Persona definition**: How is model identity established?
- **Specialization**: How are domain-specific skills defined?
---

## 🤝 Contributing to This Benchmark

We welcome contributions that maintain our educational standards:

### How to Contribute

1. **Find New Prompts**: Use our methodology to extract prompts
2. **Document Thoroughly**: Include source, method, and verification
3. **Analyze Patterns**: Add notes on unique architectural decisions
4. **Test Examples**: Provide usage examples for research

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### What Makes a Good Contribution

✅ **Acceptable**:
- Prompts from public sources
- Educational analysis
- Transparent methodology
- Clear attribution

❌ **Not Acceptable**:
- Unauthorized extraction
- Use for malicious purposes
- Unclear sourcing
- No educational value

---

## ⚖️ Ethics & Legal Framework

### Our Commitment

- 🔒 **Legal Only**: Only publicly available prompts
- 🎓 **Education First**: Research and learning purposes
- 📖 **Full Attribution**: Credit all sources
- 🛡️ **Responsible Use**: See below for guidelines

### Important Distinction

This repository is for **educational and research purposes** only. The prompts demonstrate:

- How AI providers implement safety
- Different approaches to AI alignment
- Architectural patterns in system design
- Transparency in AI systems

**We do not support unauthorized extraction or terms-of-service violations.**

### Legal Status

All prompts were obtained from:
1. Public GitHub repositories
2. Educational analysis projects
3. Community research efforts
4. Sources that allow redistribution

---

## 📊 Benchmark Statistics

| Provider | Prompts | Models | Extraction Date |
|----------|---------|--------|-----------------|
| Kimi | 6 | Various | 2026-02-05 |
| OpenAI | 5 | GPT-4.5/4o/5/DALL-E | 2026-02-05 |
| Anthropic | 2 | Claude Series | 2026-02-05 |
| Google | 1 | Diffusion | 2026-02-05 |
| Meta | 2 | LLaMA/Meta AI | 2026-02-05 |

**Total: 16 system prompts from 5 major AI providers**

---

## 🔗 Resources & References

### Source Repositories

- [Awesome AI System Prompts](https://github.com/dontriskit/awesome-ai-system-prompts) - Primary source for most prompts
- [Kimi K2.5 Analysis](https://github.com/dnnyngyen/kimi-k2.5-system-analysis) - Kimi specialized prompts

### Related Research

- [AI Safety Research](https://www.anthropic.com/research) - Anthropic's work on Constitutional AI
- [Model Cards](https://arxiv.org/abs/1810.03993) - Best practices for documenting AI systems
- [System Transparency](https://www.anthropic.com/research/core-views) - Transparency in AI architectures

### Educational Materials

- [Prompt Engineering Guide](https://www.promptingguide.ai/) - Understanding prompt patterns
- [AI Alignment Forum](https://www.alignmentforum.org/) - Research on AI alignment

---

## 💡 About AgiTerminal

AgiTerminal is an open-source initiative focused on AI transparency, safety research, and educational resources. We believe understanding how AI systems work is crucial for responsible development and deployment.

**Mission**: Democratize AI understanding through reverse engineering education
**Vision**: A transparent AI ecosystem where system behaviors are understood, not just observed

### Connect With Us

This system prompts library is part of AgiTerminal's commitment to AI transparency. Use these prompts to learn, research, and build safer AI systems.

---

*Use responsibly. Research thoroughly. Share widely.*

**Last Updated**: 2026-02-05
**Version**: 1.0 (Initial Release)
