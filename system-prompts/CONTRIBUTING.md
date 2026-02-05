# Contributing to AgiTerminal AI System Prompts

Thank you for your interest in contributing to our reverse engineering benchmark! This guide will help you maintain our high standards for educational value and research integrity.

## 📋 Table of Contents

- [What Makes a Good Contribution](#what-makes-a-good-contribution)
- [How to Find New Prompts](#how-to-find-new-prompts)
- [Documentation Standards](#documentation-standards)
- [Submission Process](#submission-process)
- [Quality Guidelines](#quality-guidelines)

---

## What Makes a Good Contribution

We welcome contributions that enhance our educational benchmark. Here are the types we accept:

### ✅ Acceptable Contributions

1. **New System Prompts**
   - From public GitHub repositories
   - From educational analysis projects
   - From sources with clear redistribution rights
   - Properly attributed and verified

2. **Analysis & Insights**
   - Pattern analysis across prompts
   - Comparative studies
   - Safety implementation analysis
   - Architectural insights

3. **Educational Content**
   - Examples of prompt usage
   - Analysis notebooks (Jupyter/RMarkdown)
   - Case studies on specific features
   - Visualization tools

4. **Methodology Improvements**
   - Better extraction techniques
   - Verification processes
   - Metadata standards
   - Quality control improvements

### ❌ Unacceptable Contributions

- Prompts obtained through unauthorized access
- Content from sources with restrictive licenses
- Analysis for malicious purposes
- Unclear sourcing or attribution

---

## How to Find New Prompts

### Methodology Overview

We collect prompts using these approaches:

1. **Repository Mining**
```bash
# Find prompt files in public repositories
git clone https://github.com/user/repo.git
grep -r "system prompt" --include="*.md" --include="*.txt"
```

2. **Educational Analysis Projects**
- Monitor academic repositories
- Follow AI safety research projects
- Track transparency initiatives

3. **Community Sources**
- Verify credentials of contributors
- Check licensing before inclusion
- Document the discovery process

### Key Resources

**GitHub Search Queries**:
```
"system prompt" in:file language:md OR language:txt
ai "prompt extraction" repository
model analysis "system instruction"
```

**Academic Sources**:
- ArXiv papers with supplementary materials
- University AI labs with public repos
- AI safety research organizations

**Community Sources**:
- Maintained analysis repositories
- Verified contributor submissions
- Transparency demonstrations

---

## Documentation Standards

### File Structure

Each prompt file must follow this structure:

```markdown
# [Model Name] System Prompt

**Source:** URL to original source
**Date Collected:** YYYY-MM-DD
**Model:** [Name]
**Confidence Level:** High/Medium/Low

---

## System Prompt

[The extracted prompt text here]

---

## Verification

**Verified By:** [Methods used]
**Confidence:** [High/Medium/Low]
**Cross-References:** [Other sources confirming]

---

## Analysis Notes

[Your insights about this prompt's structure,
unique features, safety implementations, etc.]
```

### Metadata Requirements

Every prompt must include:

- **Source URL**: Direct link to where you found it
- **Collection Date**: When you added it to the repository
- **Model Version**: What model this applies to
- **Extraction Method**: How you obtained it (web scraping, direct access, etc.)
- **Verification**: How you confirmed it's authentic
- **Confidence Level**: Your certainty about authenticity

### README Requirements

Each provider directory needs a README.md with:

```markdown
# [Provider] System Prompts

## Available Prompts

| Prompt | Model | Description | Date Added |
|--------|-------|-------------|------------|

## Collection Details

**Source Repository**: URL
**Total Prompts**: X

## Model Information

[Brief description of provider and models]

## Usage Example

[Python snippet for loading prompts]

## Notes

[Any special considerations]
```

---

## Submission Process

### Step 1: Verify the Source

Before extracting, ensure:
- [ ] Source is publicly accessible
- [ ] No terms of service violations
- [ ] License allows redistribution
- [ ] Educational/research purpose is clear

### Step 2: Extract the Prompt

Use appropriate methods:
```bash
# Direct download (preferred)
curl -s "URL" -o filename.md

# Verify content is complete
head -20 filename.md

# Check for any encoding issues
file filename.md
```

### Step 3: Document Thoroughly

Add metadata at the top:
```markdown
# Model Name System Prompt

**Source:** https://github.com/user/repo/file.md
**Date Collected:** 2026-02-05
**Model:** Model Name vX.X
**Extraction Method:** Direct download via curl from public repository
**Confidence Level:** High
```

### Step 4: Verify Authenticity

Research if possible:
- [ ] Check if other sources have the same prompt
- [ ] Look for official documentation mentioning it
- [ ] Check community discussions about authenticity
- [ ] Note any discrepancies found

### Step 5: Add Analysis

Write brief notes on:
- Any unique patterns you notice
- Similarities/differences with other prompts
- Interesting safety implementations
- Tool integration approaches

### Step 6: Submit

Create a pull request with:
- [ ] The new prompt files
- [ ] Updated README for that provider
- [ ] Source documentation
- [ ] Your analysis notes

---

## Quality Guidelines

### Accuracy Standards

- **High Confidence**: Multiple sources confirm this prompt
- **Medium Confidence**: Single reliable source, but makes sense architecturally
- **Low Confidence**: Unclear source or seems unusual - flag for review

### Format Requirements

- Use `.md` extension (Markdown format)
- Follow the standard template
- Include all required metadata
- Keep original formatting where possible
- Use UTF-8 encoding

### Analysis Depth

Good analysis includes:
```markdown
## Analysis Notes

**Architecture Pattern**: [e.g., "Uses hierarchical role definition"]

**Safety Approach**: [e.g., "Multi-layer refusal with specific wording"]

**Tool Integration**: [e.g., "TypeScript schemas embedded in prompt"]

**Unique Features**: [What makes this different from others]

**Similarities**: [Patterns shared with other models]

**Research Implications**: [Why this is interesting for AI research]
```

---

## FAQ

### Q: Can I add prompts from my own experiments?

A: Only if you can legally share them. Prompts from public APIs that are undocumented should not be included without careful consideration of terms of service.

### Q: What if I find multiple versions of the same prompt?

A: Add version numbers to the filename (e.g., `model-v1.md`, `model-v2.md`) and note the differences in the README.

### Q: How do I handle prompts that seem incomplete or wrong?

A: Mark them with low confidence and add a note explaining your concerns. Include them only if they have research value despite uncertainty.

### Q: Can I contribute tools for analyzing prompts?

A: Absolutely! Analysis tools, notebooks, and frameworks are welcome. Add them to the [examples/](examples/) directory.

---

## Review Process

All contributions are reviewed for:

1. **Legal compliance** - Are we allowed to include this?
2. **Educational value** - Does this help researchers?
3. **Documentation quality** - Is it well-documented?
4. **Accuracy** - Is it likely authentic?
5. **Attribution** - Are sources properly credited?

---

## Contact

For questions about contributing:
- Open an issue with "[Contribution Question]" prefix
- Tag @maintainers for methodology questions
- Refer to [ETHICS.md](ETHICS.md) for ethical concerns

Thank you for helping make AI more transparent and understandable!
</content>