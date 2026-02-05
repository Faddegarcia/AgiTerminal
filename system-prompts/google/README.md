# Google System Prompts

System prompts for Google's AI models.

## Available Prompts

| Prompt | Model | Description |
|--------|-------|-------------|
| [google-diffusion.md](google-diffusion.md) | Google Diffusion | Google diffusion model prompt |

## Collection Details

**Source Repository:** https://github.com/dontriskit/awesome-ai-system-prompts
**Collection Date:** 2026-02-05
**Verification Method:** Direct extraction from public GitHub repository
**Total Prompts:** 1

## Model Information

Google's AI models include various specialized systems for different tasks including diffusion models for image generation and other AI applications.

## Usage

```python
with open("system-prompts/google/google-diffusion.md") as f:
    content = f.read()
    # Parse out the system prompt section
    system_prompt = content.split("## System Prompt")[1].split("## Verification")[0]
```

## Notes

- All prompts include metadata (source, date, verification status)
- Limited collection currently - more Google prompts may be available
- Extracted from educational analysis repository
