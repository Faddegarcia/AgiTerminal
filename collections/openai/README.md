# OpenAI System Prompts

System prompts for OpenAI's GPT models.

## Available Prompts

| Prompt | Model | Description |
|--------|-------|-------------|
| [gpt-4.5.md](gpt-4.5.md) | GPT-4.5 | GPT-4.5 system prompt with tool definitions |
| [gpt-4o.md](gpt-4o.md) | GPT-4o | GPT-4o optimized system prompt |
| [gpt-5.md](gpt-5.md) | GPT-5 | GPT-5 system prompt |
| [gpt-5-detailed.md](gpt-5-detailed.md) | GPT-5 | Detailed GPT-5 system prompt |
| [dall-e.md](dall-e.md) | DALL-E | DALL-E image generation prompt |

## Collection Details

**Source Repository:** https://github.com/dontriskit/awesome-ai-system-prompts
**Collection Date:** 2026-02-05
**Verification Method:** Direct extraction from public GitHub repository
**Total Prompts:** 5

## Model Information

OpenAI's GPT series represents state-of-the-art language models with capabilities ranging from conversational AI to image generation. These prompts include detailed tool definitions, safety policies, and operational guidelines.

## Usage

```python
with open("collections/openai/gpt-4.5.md") as f:
    content = f.read()
    # Parse out the system prompt section
    system_prompt = content.split("## System Prompt")[1].split("## Verification")[0]
```

## Notes

- All prompts include metadata (source, date, verification status)
- Prompts are organized by model/version
- Includes both general and specialized prompts (e.g., DALL-E)
- Extracted from educational analysis repository
