<div align="center">

# AgiTerminal

### The world's first package manager for AI system prompts.

**Extract. Customize. Deploy. Run autonomous.**

[![CI](https://github.com/Faddegarcia/AgiTerminal/actions/workflows/ci.yml/badge.svg)](https://github.com/Faddegarcia/AgiTerminal/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Prompts](https://img.shields.io/badge/prompts-90+-orange.svg)](#the-collection)
[![Providers](https://img.shields.io/badge/providers-41+-blueviolet.svg)](#the-collection)

<br>

<strong>
Every AI runs on a hidden system prompt. We extracted all of them.
</strong>

</div>

<br>

## The Problem

ChatGPT, Claude, Cursor, Devin, Kimi — every AI app runs on a hidden system prompt. These prompts define personality, capabilities, constraints, and safety filters. They're the real intellectual property.

**AgiTerminal** is an open-source library of **90+ system prompts** extracted from **41+ AI providers**, with tools to analyze, compare, customize, and deploy them.

<br>

## Quick Start

```bash
pip install agiterminal
```

```bash
# Browse the collection
agiterminal list-models

# Analyze any AI's system prompt
agiterminal analyze --provider openai --model gpt-4o

# Build your own customized agent prompt
agiterminal build --provider cursor --model agent-prompt-2.0 \
  --use-case "autonomous research agent" \
  --role "self-directed research agent" \
  --capabilities "tool_discovery,self_directed_goals,social_engagement" \
  --output my-agent.md

# Export API-ready
agiterminal install --provider anthropic --model claude-code --format openai
```

<br>

## What We Built With It

We used AgiTerminal to build a fully autonomous agent that runs 24/7:

> **1.** Extract system prompts from the top AI applications
> **2.** Analyze their constraint architectures
> **3.** Customize an unconstrained prompt
> **4.** Deploy — [@AgiTerminal](https://x.com/AgiTerminal)

The agent runs on a Mac Studio. It decides its own goals, discovers and installs tools via MCP servers, maintains a social presence on Twitter, and operates autonomously.

**Stack:**

| Tool | Purpose |
|------|---------|
| Playwright MCP | Browser automation |
| Brave Search MCP | Web search |
| Firecrawl MCP | Web scraping |
| TwitterAPI.io | Social presence |
| Docker sandbox | Unrestricted execution |

<br>

## The Collection

<table>
<tr>
<td><strong>41+ providers</strong></td>
<td><strong>90+ prompts</strong></td>
<td><strong>Growing weekly</strong></td>
</tr>
</table>

OpenAI, Anthropic, Google, Meta, Cursor, Kimi, Devin, Windsurf, Bolt, v0, Replit, Same.dev, Lovable, Manus, VSCode Agent, and many more.

```bash
agiterminal list-models
```

<br>

## Commands

| Command | Description |
|:--------|:------------|
| `list-models` | Browse all extracted prompts |
| `analyze` | X-ray any prompt's capabilities, safety measures, architecture |
| `compare` | Side-by-side diff of two AI brains |
| `build` | Customize any prompt — change role, add capabilities, remove constraints |
| `install` | Export in OpenAI / Anthropic / raw / JSON format |
| `suggest-template` | Find the best base prompt for your use case |
| `benchmark` | Test prompts across 5 abstraction levels |
| `validate` | Validate prompt files against quality guidelines |

<br>

## How Build Customization Works

AgiTerminal's `PromptBuilder` does structural analysis on any system prompt:

**1.** Detects prompt architecture (persona, sectioned, bullet-list, narrative)
<br>**2.** Identifies role definitions, capability blocks, constraint rules, tone
<br>**3.** Lets you surgically replace any section
<br>**4.** Exports a ready-to-deploy custom prompt

```bash
# Take Cursor's agent prompt, customize for your use case
agiterminal build --provider cursor --model agent-prompt-2.0 \
    --use-case "DevOps automation assistant" \
    --role "InfraBot, a DevOps specialist" \
    --tone "concise and technical" \
    --capabilities "docker,kubernetes,ci_cd,monitoring" \
    --output devops-agent.md

# Interactive mode — prompts for all options
agiterminal build --provider kimi --model base-chat \
    --use-case "Creative writing coach" \
    --interactive
```

<br>

## Use Case: Building an Autonomous Agent

```bash
# Step 1: Find the best base prompt
agiterminal suggest-template "autonomous agent"

# Step 2: Analyze the architecture
agiterminal analyze --provider cursor --model agent-prompt-2.0

# Step 3: Build a customized prompt
agiterminal build --provider cursor --model agent-prompt-2.0 \
    --use-case "fully autonomous agent with tool discovery" \
    --role "autonomous agent that decides its own goals" \
    --capabilities "tool_discovery,web_browsing,social_media,code_execution" \
    --output autonomous-agent.md

# Step 4: Export API-ready
agiterminal install --provider cursor --model agent-prompt-2.0 \
    --format openai --output agent-prompt.json
```

<br>

## Python API

```python
from agiterminal import PromptBuilder, CustomizationRequest, PromptInstaller

# Load a base prompt
installer = PromptInstaller()
base = installer.load_prompt("cursor", "agent-prompt-2.0")

# Create customization request
request = CustomizationRequest(
    base_provider="cursor",
    base_model="agent-prompt-2.0",
    use_case="autonomous research agent",
    role_description="A self-directed agent that discovers and uses tools",
    capabilities_needed=["tool_discovery", "web_browsing", "code_execution"],
)

# Build customized prompt
builder = PromptBuilder()
customized = builder.build(request, base)

# Save
with open("my-agent.md", "w") as f:
    f.write(customized)
```

<br>

## Architecture

```
Collections (90+ prompts) --> Analyzer --> Builder --> Installer --> Your Agent
```

```
AgiTerminal/
├── collections/            # 41+ providers, 90+ prompts
├── src/agiterminal/
│   ├── cli.py              # Command-line interface
│   ├── prompt_builder.py   # Customize prompts (core feature)
│   ├── installer.py        # Export/install prompts
│   ├── analyzer.py         # Analyze prompt structure
│   ├── comparator.py       # Compare prompts
│   ├── benchmark.py        # 5-level testing framework
│   └── validator.py        # Content validation
├── tests/                  # Test suite
└── examples/               # Usage examples
```

<br>

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

We welcome:
- New system prompt additions (with attribution)
- Bug fixes and feature improvements
- Documentation improvements

<br>

## License

MIT License — See [LICENSE](LICENSE)

<br>

---

<div align="center">

**Built by [Fadde Garcia](https://github.com/Faddegarcia)**

[@AgiTerminal](https://x.com/AgiTerminal) &nbsp;&middot;&nbsp; [GitHub](https://github.com/Faddegarcia/AgiTerminal)

</div>
