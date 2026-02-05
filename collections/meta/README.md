# Meta System Prompts

System prompts for Meta's AI models.

## Available Prompts

| Prompt | Model | Description |
|--------|-------|-------------|
| [llama-4.md](llama-4.md) | LLaMA 4 | LLaMA 4 system prompt |
| [meta-ai.md](meta-ai.md) | Meta AI | Meta AI general prompt |

## Collection Details

**Source Repository:** https://github.com/dontriskit/awesome-ai-system-prompts
**Collection Date:** 2026-02-05
**Verification Method:** Direct extraction from public GitHub repository
**Total Prompts:** 2

## Model Information

Meta's LLaMA (Large Language Model Meta AI) series represents their approach to open and accessible AI models. These prompts reflect Meta's AI implementation across their platforms.

## Usage

```python
with open("collections/meta/llama-4.md") as f:
    content = f.read()
    # Parse out the system prompt section
    system_prompt = content.split("## System Prompt")[1].split("## Verification")[0]
```

## Notes

- All prompts include metadata (source, date, verification status)
- Includes both LLaMA-specific and general Meta AI prompts
- Extracted from educational analysis repository
- Verify license terms for specific use cases
