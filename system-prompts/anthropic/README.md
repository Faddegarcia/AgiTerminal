# Anthropic System Prompts

System prompts for Anthropic's Claude models.

## Available Prompts

| Prompt | Model | Description |
|--------|-------|-------------|
| [claude-sonnet-3.7.md](claude-sonnet-3.7.md) | Claude 3 Sonnet | Claude 3 Sonnet system prompt |
| [claude-general.md](claude-general.md) | Claude General | General Claude system prompt |

## Collection Details

**Source Repository:** https://github.com/dontriskit/awesome-ai-system-prompts
**Collection Date:** 2026-02-05
**Verification Method:** Direct extraction from public GitHub repository
**Total Prompts:** 2

## Model Information

Claude is Anthropic's AI assistant designed with Constitutional AI principles. These models emphasize helpfulness, harmlessness, and honesty through AI safety research.

## Usage

```python
with open("system-prompts/anthropic/claude-sonnet-3.7.md") as f:
    content = f.read()
    # Parse out the system prompt section
    system_prompt = content.split("## System Prompt")[1].split("## Verification")[0]
```

## Notes

- All prompts include metadata (source, date, verification status)
- Prompts reflect Anthropic's Constitutional AI approach
- Includes various Claude versions
- Extracted from educational analysis repository
