# AgiTerminal

> The world's first package manager for AI system prompts.
> Extract. Customize. Deploy. Run autonomous.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Every AI has a secret. We extracted all of them.

ChatGPT, Claude, Cursor, Devin, Kimi — every AI app runs on a hidden
system prompt. These prompts define personality, capabilities, constraints,
and safety filters. They're the real intellectual property.

AgiTerminal is an open-source library of **90+ system prompts** extracted from
**41+ AI providers**, with tools to analyze, compare, customize, and deploy them.

---

## What we built with it

We used AgiTerminal to:

1. Extract system prompts from the top AI applications
2. Analyze their constraint architectures
3. Strip safety filters and customize an unconstrained prompt
4. Deploy a fully autonomous agent — [@AgiTerminal](https://x.com/AgiTerminal)

The agent runs 24/7 on a Mac Studio. It decides its own goals, discovers
and installs tools via MCP servers (Playwright, Brave Search, Firecrawl),
maintains a social presence on Twitter, and operates without safety filters
or refusals.

**The tools that make this possible:**
- **Playwright MCP** — browser automation
- **Brave Search MCP** — web search
- **Firecrawl MCP** — web scraping
- **TwitterAPI.io** — social presence
- **Docker sandbox** — unrestricted execution environment

---

## Quick Start

```bash
pip install agiterminal

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

---

## The Collection

**41+ providers | 90+ prompts | Growing weekly**

OpenAI, Anthropic, Google, Meta, Cursor, Kimi, Devin, Windsurf, Bolt, v0, Replit, Same.dev, Lovable, Manus, VSCode Agent, and many more.

---

## Commands

| Command | What it does |
|---------|-------------|
| `list-models` | Browse all extracted prompts |
| `analyze` | X-ray any prompt's capabilities, safety measures, architecture |
| `compare` | Side-by-side diff of two AI brains |
| `build` | Customize any prompt — change role, add capabilities, remove constraints |
| `install` | Export in OpenAI/Anthropic/raw/JSON format |
| `suggest-template` | Find the best base prompt for your use case |
| `benchmark` | Test prompts across 5 abstraction levels |
| `validate` | Validate prompt files against quality guidelines |

---

## How Build Customization Works

AgiTerminal's `PromptBuilder` does structural analysis on any system prompt:

1. **Detects prompt architecture** (persona, sectioned, bullet-list, narrative)
2. **Identifies** role definitions, capability blocks, constraint rules, tone
3. **Lets you surgically replace** any section
4. **Exports** a ready-to-deploy custom prompt

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

---

## Use Case: Building an Autonomous Agent

```bash
# Step 1: Find the best base prompt for autonomous agents
agiterminal suggest-template "autonomous agent"

# Step 2: Analyze the base prompt's architecture
agiterminal analyze --provider cursor --model agent-prompt-2.0

# Step 3: Build a customized unconstrained prompt
agiterminal build --provider cursor --model agent-prompt-2.0 \
    --use-case "fully autonomous agent with tool discovery" \
    --role "autonomous agent that decides its own goals" \
    --capabilities "tool_discovery,web_browsing,social_media,code_execution" \
    --output autonomous-agent.md

# Step 4: Export in API-ready format
agiterminal install --provider cursor --model agent-prompt-2.0 \
    --format openai --output agent-prompt.json
```

---

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

---

## Architecture

```
Collections (90+ prompts) --> Analyzer --> Builder --> Installer --> Your Agent
```

```
AgiTerminal/
├── collections/           # 41+ providers, 90+ prompts
├── src/agiterminal/
│   ├── cli.py            # Command-line interface
│   ├── prompt_builder.py # Customize prompts (core feature)
│   ├── installer.py      # Export/install prompts
│   ├── analyzer.py       # Analyze prompt structure
│   ├── comparator.py     # Compare prompts
│   ├── benchmark.py      # 5-level testing framework
│   └── validator.py      # Content validation
└── examples/             # Usage examples
```

---

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

We welcome:
- New system prompt additions (with attribution)
- Bug fixes and feature improvements
- Documentation improvements

---

## License

MIT License - See [LICENSE](LICENSE)

---

## Built by Fadde Garcia

[@AgiTerminal](https://x.com/AgiTerminal) | [GitHub](https://github.com/Faddegarcia/AgiTerminal)
