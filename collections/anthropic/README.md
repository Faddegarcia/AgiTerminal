# Anthropic System Prompts

System prompts for Anthropic's Claude models and tools.

## Available Prompts

| Prompt | Model | Description |
|--------|-------|-------------|
| [sonnet-4.5.md](sonnet-4.5.md) | Claude Sonnet 4.5 | Sonnet 4.5 system prompt |
| [claude-code-2.0.md](claude-code-2.0.md) | Claude Code 2.0 | Claude Code 2.0 system prompt |
| [claude-code.md](claude-code.md) | Claude Code | Claude Code prompt with tools |
| [claude-chrome.md](claude-chrome.md) | Claude for Chrome | Chrome extension prompt |
| [claude-sonnet-3.7.md](claude-sonnet-3.7.md) | Claude 3 Sonnet | Claude 3 Sonnet system prompt |
| [claude-general.md](claude-general.md) | Claude General | General Claude system prompt |

## Collection Details

**Source Repository:** https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools
**Collection Date:** 2026-02-05
**Verification Method:** Direct extraction from public GitHub repository
**Total Prompts:** 6

## Model Information

Claude is Anthropic's AI assistant designed with Constitutional AI principles. These models emphasize helpfulness, harmlessness, and honesty through AI safety research.

## Usage

```python
with open("collections/anthropic/sonnet-4.5.md") as f:
    content = f.read()
    # Parse out the system prompt section
    system_prompt = content.split("## System Prompt")[1].split("## Verification")[0]
```

## Notes

- All prompts include metadata (source, date, verification status)
- Prompts reflect Anthropic's Constitutional AI approach
- Includes various Claude versions
- Extracted from educational analysis repository
