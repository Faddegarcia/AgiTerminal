# Contributing to AgiTerminal

Thank you for your interest in contributing to AgiTerminal! This document provides guidelines for contributing to this educational research platform.

---

## Code of Conduct

This project and everyone participating in it is governed by our commitment to:
- **Educational Excellence** - All contributions should enhance learning
- **Ethical Research** - Follow responsible AI research practices
- **Inclusive Community** - Welcome contributors from all backgrounds
- **Transparency** - Be clear about methods and limitations

---

## How Can I Contribute?

### Reporting Issues

If you find a bug or have a suggestion:

1. **Check existing issues** - Search to avoid duplicates
2. **Create a detailed report** - Include:
   - Clear description of the issue
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - System information
   - Screenshots if applicable

### Contributing System Prompts

We welcome additions to our system prompt collection:

1. **Verify the source** - Must be publicly available or legally obtained
2. **Follow the template** - Include all required metadata
3. **Add analysis** - Include educational applications section
4. **Validate** - Run the validator before submitting

Template for new system prompts:
```markdown
# [Provider] [Model] System Prompt

**Source:** [URL or "Direct from API"]
**Date Collected:** YYYY-MM-DD
**Model Version:** [Version]
**Extraction Method:** [Manual/Direct/API]
**Confidence Level:** High/Medium/Low
**Research Value:** [What researchers can learn]

---

## System Prompt

[Content]

---

## Verification Steps

[How to verify this is authentic]

---

## Analysis Notes

**Architecture Pattern:** [Single/Multi/Tool-based persona]
**Specialization Strategy:** [Generalist/Specialist/Hybrid]
**Safety Integration:** [How safety is implemented]
**Unique Features:** [What makes this approach distinct]

---

## Educational Applications

- Use case 1
- Use case 2
- Use case 3
```

### Code Contributions

#### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/AgiTerminal.git
cd AgiTerminal

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

#### Coding Standards

- **Python 3.9+** compatibility
- **Type hints** for all functions
- **Docstrings** for all public functions
- **Black** formatting (line length: 100)
- **Flake8** linting
- **Tests** for new functionality

#### Commit Message Format

Follow conventional commits:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Maintenance tasks

Examples:
```
feat(analyzer): add support for new model format

docs: update README with new CLI commands
test(benchmark): add tests for level 4 abstraction
```

### Documentation Contributions

- Fix typos or unclear explanations
- Add examples to existing docs
- Improve educational context sections
- Translate documentation (contact us first)

---

## Pull Request Process

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our guidelines
3. **Add tests** for new functionality
4. **Update documentation** as needed
5. **Ensure tests pass** - Run the full test suite
6. **Validate content** - If adding prompts, run the validator
7. **Submit PR** with clear description of changes

### PR Review Criteria

- Code follows style guidelines
- Tests pass and coverage is maintained
- Documentation is updated
- Educational appropriateness is verified
- No prohibited content is added

---

## Development Guidelines

### Adding New Features

1. **Discuss first** - Open an issue to discuss major changes
2. **Design document** - For significant features, write a brief design doc
3. **Incremental changes** - Break large changes into smaller PRs
4. **Documentation** - Update docs with the code

### Adding New System Prompts

1. Place in `system-prompts/{provider}/{model}.md`
2. Follow the metadata template
3. Include educational applications
4. Run validation:
   ```bash
   python -m src.cli validate --file system-prompts/{provider}/{model}.md
   ```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=agiterminal

# Run specific test file
pytest tests/test_analyzer.py

# Run specific test
pytest tests/test_analyzer.py::TestSystemPromptAnalyzer::test_init
```

---

## Questions?

- **General questions** - Open a discussion
- **Bug reports** - Open an issue
- **Security concerns** - Email security@agiterminal.org
- **Private inquiries** - Email contact@agiterminal.org

---

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in relevant documentation

Thank you for helping make AI research more accessible!

---

*This project is for educational and research purposes only.*
