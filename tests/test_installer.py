"""
Tests for the PromptInstaller class.

This module tests the installation and export functionality for system prompts,
including format conversion, path security, and batch operations.
"""

import json
import pytest
from pathlib import Path

from agiterminal.installer import PromptInstaller, FormattedPrompt


class TestPromptInstaller:
    """Test cases for PromptInstaller."""

    def test_init(self):
        """Test installer initialization."""
        installer = PromptInstaller()
        assert installer.system_prompt is None
        assert installer.provider is None
        assert installer.model_id is None
        assert installer.raw_content is None

    def test_sanitize_path_component(self):
        """Test path component sanitization for security."""
        installer = PromptInstaller()

        # Test normal paths
        assert installer._sanitize_path_component("kimi") == "kimi"
        assert installer._sanitize_path_component("base-chat") == "base-chat"
        assert installer._sanitize_path_component("gpt-4.5") == "gpt-4.5"

        # Test path traversal attempts
        assert installer._sanitize_path_component("../../../etc/passwd") == "etcpasswd"
        assert installer._sanitize_path_component("..\\windows\\system") == "windowssystem"
        assert installer._sanitize_path_component("/absolute/path") == "absolutepath"

        # Test injection attempts
        assert installer._sanitize_path_component("model;rm -rf") == "modelrm-rf"
        assert installer._sanitize_path_component("model$(whoami)") == "modelwhoami"

    def test_validate_format_type(self):
        """Test format type validation."""
        installer = PromptInstaller()

        # Valid formats
        assert installer._validate_format_type("raw") == "raw"
        assert installer._validate_format_type("json") == "json"
        assert installer._validate_format_type("openai") == "openai"
        assert installer._validate_format_type("anthropic") == "anthropic"
        assert installer._validate_format_type("JSON") == "json"  # Case insensitive

        # Invalid format
        with pytest.raises(ValueError, match="Unsupported format type"):
            installer._validate_format_type("invalid")

    def test_extract_clean_prompt(self):
        """Test extraction of clean prompt from markdown."""
        installer = PromptInstaller()

        # Test with System Prompt section
        markdown_with_section = """# Model Name

**Source:** test

---

## System Prompt

You are a helpful assistant.

### Capabilities

- Feature 1
- Feature 2

---

## Analysis

Some analysis text.
"""
        clean = installer.extract_clean_prompt(markdown_with_section)
        assert "You are a helpful assistant." in clean
        assert "### Capabilities" in clean
        assert "## Analysis" not in clean

        # Test without System Prompt section
        markdown_no_section = """# Model Name

You are a helpful assistant.

More content here.
"""
        clean = installer.extract_clean_prompt(markdown_no_section)
        assert "You are a helpful assistant." in clean

    def test_format_output_raw(self):
        """Test raw format output."""
        installer = PromptInstaller()
        installer.system_prompt = "You are a helpful assistant."
        installer.provider = "test"
        installer.model_id = "model"

        result = installer.format_output("raw")
        assert result == "You are a helpful assistant."

    def test_format_output_json(self):
        """Test JSON format output."""
        installer = PromptInstaller()
        installer.system_prompt = "You are a helpful assistant."
        installer.provider = "test"
        installer.model_id = "model"

        result = installer.format_output("json")
        assert isinstance(result, dict)
        assert result["system_prompt"] == "You are a helpful assistant."
        assert result["provider"] == "test"
        assert result["model"] == "model"
        assert result["format"] == "json"
        assert result["length"] == 28

    def test_format_output_openai(self):
        """Test OpenAI API format output."""
        installer = PromptInstaller()
        installer.system_prompt = "You are a helpful assistant."

        result = installer.format_output("openai")
        assert isinstance(result, dict)
        assert result["role"] == "system"
        assert result["content"] == "You are a helpful assistant."

    def test_format_output_anthropic(self):
        """Test Anthropic API format output."""
        installer = PromptInstaller()
        installer.system_prompt = "You are a helpful assistant."
        installer.model_id = "claude-3-opus"

        result = installer.format_output("anthropic")
        assert isinstance(result, dict)
        assert result["model"] == "claude-3-opus"
        assert result["system"] == "You are a helpful assistant."
        assert result["max_tokens"] == 4096
        assert result["messages"] == []

    def test_format_output_not_loaded(self):
        """Test format output without loaded prompt."""
        installer = PromptInstaller()

        with pytest.raises(ValueError, match="No system prompt loaded"):
            installer.format_output("raw")

    def test_save_to_file(self, tmp_path):
        """Test saving prompt to file."""
        installer = PromptInstaller()
        installer.system_prompt = "You are a helpful assistant."
        installer.provider = "test"
        installer.model_id = "model"

        output_file = tmp_path / "prompt.json"
        result = installer.save_to_file(output_file, format_type="json")

        assert result.exists()
        content = json.loads(result.read_text())
        assert content["system_prompt"] == "You are a helpful assistant."

    def test_get_integration_example(self):
        """Test getting integration examples."""
        installer = PromptInstaller()
        installer.system_prompt = "You are a helpful assistant."
        installer.model_id = "gpt-4"

        # Test OpenAI example
        openai_example = installer.get_integration_example("openai")
        assert "openai" in openai_example.lower() or "OpenAI" in openai_example
        assert "You are a helpful assistant." in openai_example
        assert "gpt-4" in openai_example

        # Test Anthropic example
        anthropic_example = installer.get_integration_example("anthropic")
        assert "anthropic" in anthropic_example.lower() or "Anthropic" in anthropic_example

        # Test unknown provider defaults to generic
        unknown_example = installer.get_integration_example("unknown")
        assert "requests.post" in unknown_example

    def test_list_integration_examples(self):
        """Test listing available integration examples."""
        installer = PromptInstaller()
        examples = installer.list_integration_examples()

        assert "openai" in examples
        assert "anthropic" in examples
        assert "default" in examples

    def test_get_formatted_prompt(self):
        """Test getting FormattedPrompt dataclass."""
        installer = PromptInstaller()
        installer.system_prompt = "You are a helpful assistant."
        installer.provider = "test"
        installer.model_id = "model"

        result = installer.get_formatted_prompt("json")

        assert isinstance(result, FormattedPrompt)
        assert result.format_type == "json"
        assert result.provider == "test"
        assert result.model == "model"
        assert "system_prompt" in result.content
        assert result.metadata["length"] == 28

    def test_batch_export(self, tmp_path, monkeypatch):
        """Test batch export of multiple prompts."""
        installer = PromptInstaller()

        # Create temporary mock files
        mock_dir = tmp_path / "collections"
        (mock_dir / "provider1").mkdir(parents=True)
        (mock_dir / "provider2").mkdir(parents=True)

        (mock_dir / "provider1" / "model1.md").write_text(
            "## System Prompt\n\nPrompt 1 content."
        )
        (mock_dir / "provider2" / "model2.md").write_text(
            "## System Prompt\n\nPrompt 2 content."
        )

        # Monkeypatch the path resolution in load_prompt
        original_load = installer.load_prompt
        def mock_load(provider, model):
            # Directly set state without path lookup
            installer.provider = provider
            installer.model_id = model
            installer.raw_content = f"## System Prompt\n\n{provider}/{model} content."
            installer.system_prompt = f"{provider}/{model} content."
            return installer.system_prompt

        monkeypatch.setattr(installer, "load_prompt", mock_load)

        prompts = [
            {"provider": "provider1", "model": "model1"},
            {"provider": "provider2", "model": "model2"},
        ]

        output_dir = tmp_path / "exports"
        paths = installer.batch_export(prompts, output_dir, "json")

        assert len(paths) == 2
        assert all(p.exists() for p in paths)

    def test_batch_export_restores_state(self, tmp_path, monkeypatch):
        """Test that batch export restores original state."""
        installer = PromptInstaller()

        # Set initial state
        installer.provider = "original"
        installer.model_id = "original-model"
        installer.system_prompt = "original prompt"

        # Create temporary mock file
        mock_dir = tmp_path / "collections" / "test"
        mock_dir.mkdir(parents=True)
        (mock_dir / "model.md").write_text("## System Prompt\n\nTest content.")

        # Monkeypatch
        import agiterminal.installer as installer_module
        original_path_method = installer_module.Path

        def mock_path(*args):
            if len(args) > 0 and str(args[0]).endswith("collections"):
                return original_path_method(mock_dir)
            return original_path_method(*args)

        monkeypatch.setattr(installer_module, "Path", mock_path)

        prompts = [{"provider": "test", "model": "model"}]
        installer.batch_export(prompts, tmp_path / "exports", "json")

        # Verify state is restored
        assert installer.provider == "original"
        assert installer.model_id == "original-model"
        assert installer.system_prompt == "original prompt"


class TestFormattedPrompt:
    """Test cases for FormattedPrompt dataclass."""

    def test_dataclass_creation(self):
        """Test FormattedPrompt dataclass creation."""
        fp = FormattedPrompt(
            content="test content",
            format_type="json",
            provider="openai",
            model="gpt-4",
            metadata={"length": 12}
        )

        assert fp.content == "test content"
        assert fp.format_type == "json"
        assert fp.provider == "openai"
        assert fp.model == "gpt-4"
        assert fp.metadata["length"] == 12

    def test_dataclass_defaults(self):
        """Test FormattedPrompt with default metadata."""
        fp = FormattedPrompt(
            content="test",
            format_type="raw",
            provider="test",
            model="model"
        )

        assert fp.metadata is None
