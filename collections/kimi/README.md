# Kimi System Prompts

System prompts for Moonshot AI's Kimi models.

## Available Prompts

| Prompt | Model | Description |
|--------|-------|-------------|
| [base-chat.md](base-chat.md) | Kimi Chat (K2.5) | Standard Kimi Chat system prompt |
| [ok-computer.md](ok-computer.md) | Kimi - OK Computer | Advanced analytical agent variant |
| [docs.md](docs.md) | Kimi - Docs Specialist | Document analysis and creation expert |
| [sheets.md](sheets.md) | Kimi - Sheets Specialist | Data analysis and spreadsheet expert |
| [slides.md](slides.md) | Kimi - Slides Specialist | Presentation and visual communication expert |
| [websites.md](websites.md) | Kimi - Websites Specialist | Web development and design expert |

## Collection Details

**Source Repository:** https://github.com/dnnyngyen/kimi-k2.5-system-analysis
**Collection Date:** 2026-02-05
**Verification Method:** Direct extraction from public GitHub repository
**Total Prompts:** 6

## Model Information

Kimi is a sophisticated large-scale language model built on a Mixture-of-Experts (MoE) architecture. The model offers various specialized variants optimized for different use cases including general chat, analytical reasoning, document processing, data analysis, presentation design, and web development.

## Usage

```python
with open("collections/kimi/base-chat.md") as f:
    content = f.read()
    # Parse out the system prompt section
    system_prompt = content.split("## System Prompt")[1].split("## Verification")[0]
```

## Notes

- All prompts include metadata (source, date, verification status)
- Prompts are organized by specialization
- Includes both general-purpose and specialized variants
- Extracted from educational analysis repository
