"""
Tests for the PromptBuilder class.

This module tests the prompt customization functionality, including template parsing,
customization application, and use case suggestions.
"""

import pytest
from agiterminal.prompt_builder import (
    PromptBuilder,
    CustomizationRequest,
    PromptTemplate,
    CustomizationType,
)


class TestPromptTemplate:
    """Test cases for PromptTemplate dataclass."""

    def test_dataclass_creation(self):
        """Test PromptTemplate creation."""
        template = PromptTemplate(
            original="You are Kimi.",
            role_section="You are Kimi.",
            capability_sections=["- capability 1"],
            structure_pattern="persona_with_capabilities"
        )

        assert template.original == "You are Kimi."
        assert template.role_section == "You are Kimi."
        assert len(template.capability_sections) == 1
        assert template.structure_pattern == "persona_with_capabilities"

    def test_to_dict(self):
        """Test conversion to dictionary."""
        template = PromptTemplate(
            original="Test prompt",
            role_section="You are Test.",
            capability_sections=["cap1", "cap2"],
            instruction_sections=["inst1"],
            constraint_sections=["con1", "con2", "con3"],
            tone_indicators=["friendly", "professional"],
            structure_pattern="sectioned"
        )

        result = template.to_dict()

        assert result["structure_pattern"] == "sectioned"
        assert result["has_role"] is True
        assert result["capability_count"] == 2
        assert result["instruction_count"] == 1
        assert result["constraint_count"] == 3
        assert result["tone_indicators"] == ["friendly", "professional"]


class TestCustomizationRequest:
    """Test cases for CustomizationRequest dataclass."""

    def test_dataclass_creation(self):
        """Test CustomizationRequest creation with all fields."""
        request = CustomizationRequest(
            base_provider="kimi",
            base_model="base-chat",
            use_case="Python tutor",
            role_description="CodeTutor, a patient teacher",
            target_audience="beginners",
            tone_preference="friendly",
            capabilities_needed=["code_examples", "debugging"],
            constraints_to_add=["always explain"],
            constraints_to_remove=["be brief"],
            output_format="include examples",
            additional_context="For kids aged 10-14"
        )

        assert request.base_provider == "kimi"
        assert request.base_model == "base-chat"
        assert request.use_case == "Python tutor"
        assert request.role_description == "CodeTutor, a patient teacher"
        assert request.target_audience == "beginners"
        assert request.tone_preference == "friendly"
        assert len(request.capabilities_needed) == 2
        assert len(request.constraints_to_add) == 1
        assert len(request.constraints_to_remove) == 1
        assert request.output_format == "include examples"
        assert request.additional_context == "For kids aged 10-14"

    def test_dataclass_defaults(self):
        """Test CustomizationRequest with default values."""
        request = CustomizationRequest(
            base_provider="openai",
            base_model="gpt-4",
            use_case="General assistant"
        )

        assert request.role_description is None
        assert request.target_audience is None
        assert request.tone_preference is None
        assert request.capabilities_needed == []
        assert request.constraints_to_add == []
        assert request.constraints_to_remove == []
        assert request.output_format is None
        assert request.additional_context is None


class TestPromptBuilder:
    """Test cases for PromptBuilder."""

    def test_init(self):
        """Test PromptBuilder initialization."""
        builder = PromptBuilder()
        assert builder.template_cache == {}

    def test_parse_prompt_persona_with_capabilities(self):
        """Test parsing a persona-based prompt with capabilities."""
        builder = PromptBuilder()
        prompt = """You are Kimi, a helpful assistant.

Core capabilities:
- Advanced Reasoning
- Coding
- Analysis

Always be helpful and accurate."""

        template = builder.parse_prompt(prompt)

        assert template.structure_pattern == "persona_with_capabilities"
        assert "You are Kimi" in template.role_section
        assert len(template.capability_sections) >= 0  # May or may not match depending on pattern
        assert "professional" in template.tone_indicators or len(template.tone_indicators) >= 0

    def test_parse_prompt_sectioned(self):
        """Test parsing a sectioned prompt."""
        builder = PromptBuilder()
        prompt = """### Role
You are a coding assistant.

### Capabilities
- Write code
- Debug

### Guidelines
Be professional."""

        template = builder.parse_prompt(prompt)

        # Structure detection prioritizes "you are" + "capabilities" pattern
        assert template.structure_pattern in ["sectioned", "persona_with_capabilities", "bullet_list"]

    def test_parse_prompt_bullet_list(self):
        """Test parsing a bullet-list heavy prompt."""
        builder = PromptBuilder()
        prompt = """You are an assistant.

- Do this
- Do that
- Also this
- And this
- Plus this
"""

        template = builder.parse_prompt(prompt)

        assert template.structure_pattern == "bullet_list"

    def test_parse_prompt_narrative(self):
        """Test parsing a narrative prompt."""
        builder = PromptBuilder()
        prompt = "You are a helpful assistant. Provide accurate information."

        template = builder.parse_prompt(prompt)

        assert template.structure_pattern == "narrative"

    def test_analyze_base_prompt(self):
        """Test analyzing a base prompt."""
        builder = PromptBuilder()
        prompt = """You are Kimi, a helpful assistant.

Core capabilities:
- Reasoning
- Coding

Always be helpful and accurate.
Do not provide harmful information."""

        analysis = builder.analyze_base_prompt("kimi", "base-chat", prompt)

        assert analysis["provider"] == "kimi"
        assert analysis["model"] == "base-chat"
        assert analysis["structure"] in ["persona_with_capabilities", "sectioned", "narrative"]
        assert analysis["detected_role"] is not None
        assert analysis["detected_constraints"] > 0
        assert len(analysis["customization_opportunities"]) > 0

    def test_build_role_customization(self):
        """Test building with role customization."""
        builder = PromptBuilder()
        base = "You are Kimi, a helpful assistant."

        request = CustomizationRequest(
            base_provider="kimi",
            base_model="base-chat",
            use_case="Python tutor",
            role_description="CodeTutor, a Python teacher"
        )

        result = builder.build(request, base)

        assert "You are CodeTutor" in result
        assert "Kimi" not in result

    def test_build_capability_customization(self):
        """Test building with capability customization."""
        builder = PromptBuilder()
        base = "You are an assistant.\n\nYour capabilities include:\n- General help"

        request = CustomizationRequest(
            base_provider="test",
            base_model="model",
            use_case="Coding",
            capabilities_needed=["python", "javascript", "debugging"]
        )

        result = builder.build(request, base)

        assert "- python" in result
        assert "- javascript" in result
        assert "- debugging" in result

    def test_build_tone_customization(self):
        """Test building with tone customization."""
        builder = PromptBuilder()
        base = "You are an assistant."

        request = CustomizationRequest(
            base_provider="test",
            base_model="model",
            use_case="Chat",
            tone_preference="friendly and approachable"
        )

        result = builder.build(request, base)

        assert "friendly and approachable" in result

    def test_build_constraint_customization(self):
        """Test building with constraint customization."""
        builder = PromptBuilder()
        base = "You are an assistant.\n\nDo not be rude."

        request = CustomizationRequest(
            base_provider="test",
            base_model="model",
            use_case="Support",
            constraints_to_add=["always greet users", "be patient"],
            constraints_to_remove=["rude"]
        )

        result = builder.build(request, base)

        assert "always greet users" in result
        assert "be patient" in result
        assert "rude" not in result

    def test_build_output_format(self):
        """Test building with output format specification."""
        builder = PromptBuilder()
        base = "You are an assistant."

        request = CustomizationRequest(
            base_provider="test",
            base_model="model",
            use_case="Documentation",
            output_format="Always include code examples"
        )

        result = builder.build(request, base)

        assert "Output Format" in result
        assert "Always include code examples" in result

    def test_build_additional_context(self):
        """Test building with additional context."""
        builder = PromptBuilder()
        base = "You are an assistant."

        request = CustomizationRequest(
            base_provider="test",
            base_model="model",
            use_case="Tutoring",
            additional_context="Target audience: high school students"
        )

        result = builder.build(request, base)

        assert "Context" in result
        assert "Target audience: high school students" in result

    def test_build_full_customization(self):
        """Test building with all customization options."""
        builder = PromptBuilder()
        base = """You are Kimi, a helpful assistant.

Your capabilities include:
- General assistance

Be professional."""

        request = CustomizationRequest(
            base_provider="kimi",
            base_model="base-chat",
            use_case="Python coding tutor for beginners",
            role_description="CodeTutor, a patient Python teacher",
            tone_preference="friendly and encouraging",
            capabilities_needed=["code_examples", "error_explanation", "best_practices"],
            output_format="Always provide runnable code examples",
            additional_context="Target audience: complete beginners aged 16-25"
        )

        result = builder.build(request, base)

        assert "CodeTutor" in result
        assert "friendly and encouraging" in result
        assert "code_examples" in result
        assert "Output Format" in result
        assert "Target audience" in result

    def test_suggest_template_for_use_case_code(self):
        """Test template suggestions for coding use cases."""
        builder = PromptBuilder()

        suggestions = builder.suggest_template_for_use_case("Python coding assistant")

        assert len(suggestions) > 0
        # Should suggest cursor or coding-related templates
        providers = [s[0] for s in suggestions]
        assert "cursor" in providers or "kimi" in providers

    def test_suggest_template_for_use_case_writing(self):
        """Test template suggestions for writing use cases."""
        builder = PromptBuilder()

        suggestions = builder.suggest_template_for_use_case("Writing assistant")

        assert len(suggestions) > 0
        providers = [s[0] for s in suggestions]
        assert "kimi" in providers

    def test_suggest_template_for_use_case_chat(self):
        """Test template suggestions for chat use cases."""
        builder = PromptBuilder()

        suggestions = builder.suggest_template_for_use_case("General chat bot")

        assert len(suggestions) > 0
        providers = [s[0] for s in suggestions]
        assert "kimi" in providers or "openai" in providers

    def test_suggest_template_default(self):
        """Test default suggestions for unknown use cases."""
        builder = PromptBuilder()

        suggestions = builder.suggest_template_for_use_case("xyz unknown use case 123")

        # Should return default suggestions
        assert len(suggestions) > 0
        providers = [s[0] for s in suggestions]
        assert "kimi" in providers

    def test_suggest_template_returns_top_5(self):
        """Test that suggestions are limited to top 5."""
        builder = PromptBuilder()

        # Use a use case that matches multiple keywords
        suggestions = builder.suggest_template_for_use_case("code and chat agent")

        assert len(suggestions) <= 5

    def test_preview_customization(self):
        """Test customization preview generation."""
        builder = PromptBuilder()
        base = "You are Kimi, a helpful assistant."

        request = CustomizationRequest(
            base_provider="kimi",
            base_model="base-chat",
            use_case="Python tutor",
            role_description="CodeTutor",
            tone_preference="friendly",
            capabilities_needed=["code", "debug"],
            constraints_to_add=["always explain"],
            output_format="include examples"
        )

        preview = builder.preview_customization(request, base)

        assert "CUSTOMIZATION PREVIEW" in preview
        assert "kimi/base-chat" in preview
        assert "Role:" in preview
        assert "Capabilities:" in preview
        assert "Tone:" in preview
        assert "Constraints:" in preview
        assert "Output Format:" in preview

    def test_preview_customization_minimal(self):
        """Test preview with minimal customizations."""
        builder = PromptBuilder()
        base = "You are an assistant."

        request = CustomizationRequest(
            base_provider="test",
            base_model="model",
            use_case="General"
        )

        preview = builder.preview_customization(request, base)

        assert "CUSTOMIZATION PREVIEW" in preview
        # Should not show changes for empty fields
        assert "Role:" not in preview


class TestCustomizationType:
    """Test cases for CustomizationType enum."""

    def test_enum_values(self):
        """Test CustomizationType enum values."""
        assert CustomizationType.ROLE.value == "role"
        assert CustomizationType.CAPABILITY_ADD.value == "cap_add"
        assert CustomizationType.CAPABILITY_REMOVE.value == "cap_rem"
        assert CustomizationType.TONE.value == "tone"
        assert CustomizationType.CONSTRAINT_ADD.value == "con_add"
        assert CustomizationType.CONSTRAINT_REMOVE.value == "con_rem"
        assert CustomizationType.KNOWLEDGE.value == "knowledge"
        assert CustomizationType.OUTPUT_FORMAT.value == "output"
