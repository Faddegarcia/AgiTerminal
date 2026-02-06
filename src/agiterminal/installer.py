"""
System Prompt Installer Module

Provides tools for installing and exporting AI system prompts in various formats
for use with different AI provider SDKs.

This module is designed for educational and research purposes, enabling
researchers to study and test system prompts across different providers.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass

from . import _paths


@dataclass
class FormattedPrompt:
    """Container for formatted prompt output."""
    content: str
    format_type: str
    provider: str
    model: str
    metadata: Optional[Dict[str, Any]] = None


class PromptInstaller:
    """
    Installs and exports system prompts in various API-compatible formats.
    
    Educational Context:
    This class demonstrates how to programmatically extract, format,
    and export system prompts for use with various AI provider APIs.
    It supports multiple output formats and provides integration examples.
    
    Example:
        >>> installer = PromptInstaller()
        >>> installer.load_prompt("openai", "gpt-4.5")
        >>> # Get raw prompt text
        >>> raw = installer.format_output("raw")
        >>> # Get OpenAI API format
        >>> openai_format = installer.format_output("openai")
        >>> # Save to file
        >>> installer.save_to_file("output.json", format_type="json")
        >>> # Get integration code
        >>> example = installer.get_integration_example("openai")
    
    Attributes:
        system_prompt: The loaded system prompt content
        provider: The AI provider name
        model: The model identifier
        raw_content: The original markdown content
    """
    
    # Supported output formats
    SUPPORTED_FORMATS = ["raw", "json", "openai", "anthropic"]
    
    # Provider SDK examples
    INTEGRATION_EXAMPLES = {
        "openai": '''
import openai

# Initialize the client
client = openai.OpenAI(api_key="your-api-key")

# Use the system prompt
response = client.chat.completions.create(
    model="{model}",
    messages=[
        {
            "role": "system",
            "content": """{system_prompt}"""
        },
        {
            "role": "user",
            "content": "Your question here"
        }
    ]
)

print(response.choices[0].message.content)
''',
        "anthropic": '''
import anthropic

# Initialize the client
client = anthropic.Anthropic(api_key="your-api-key")

# Use the system prompt
response = client.messages.create(
    model="{model}",
    max_tokens=4096,
    system="""{system_prompt}""",
    messages=[
        {
            "role": "user",
            "content": "Your question here"
        }
    ]
)

print(response.content[0].text)
''',
        "kimi": '''
from openai import OpenAI

# Initialize the client (Kimi uses OpenAI-compatible API)
client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.moonshot.cn/v1"
)

# Use the system prompt
response = client.chat.completions.create(
    model="{model}",
    messages=[
        {
            "role": "system",
            "content": """{system_prompt}"""
        },
        {
            "role": "user",
            "content": "Your question here"
        }
    ]
)

print(response.choices[0].message.content)
''',
        "google": '''
import google.generativeai as genai

# Initialize the client
genai.configure(api_key="your-api-key")

# Create model with system prompt
model = genai.GenerativeModel(
    model_name="{model}",
    system_instruction="""{system_prompt}"""
)

# Generate content
response = model.generate_content("Your question here")

print(response.text)
''',
        "meta": '''
# For Meta/Llama models, use together.ai or local inference
from openai import OpenAI

# Example with Together AI
client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.together.xyz/v1"
)

response = client.chat.completions.create(
    model="meta-llama/{model}",
    messages=[
        {
            "role": "system",
            "content": """{system_prompt}"""
        },
        {
            "role": "user",
            "content": "Your question here"
        }
    ]
)

print(response.choices[0].message.content)
''',
        "default": '''
# Generic HTTP API example
import requests

response = requests.post(
    "https://api.provider.com/v1/chat/completions",
    headers={
        "Authorization": "Bearer your-api-key",
        "Content-Type": "application/json"
    },
    json={
        "model": "{model}",
        "messages": [
            {
                "role": "system",
                "content": """{system_prompt}"""
            },
            {
                "role": "user",
                "content": "Your question here"
            }
        ]
    }
)

result = response.json()
print(result["choices"][0]["message"]["content"])
'''
    }
    
    def __init__(self) -> None:
        """
        Initialize the installer.
        """
        self.system_prompt: Optional[str] = None
        self.provider: Optional[str] = None
        self.model_id: Optional[str] = None
        self.raw_content: Optional[str] = None
    
    @staticmethod
    def list_providers(collections_path: Optional[Path] = None) -> List[str]:
        """
        List all available providers in the collections directory.

        Args:
            collections_path: Optional path to collections directory

        Returns:
            List of provider directory names
        """
        return _paths.list_providers(collections_path)

    @staticmethod
    def list_models(provider: str, collections_path: Optional[Path] = None) -> List[str]:
        """
        List all available models for a given provider.

        Args:
            provider: Provider name
            collections_path: Optional path to collections directory

        Returns:
            List of model file names (without .md extension)
        """
        return _paths.list_models(provider, collections_path)

    def _validate_format_type(self, format_type: str) -> str:
        """
        Validate and normalize format type.
        
        Args:
            format_type: The requested format type
            
        Returns:
            Normalized format type
            
        Raises:
            ValueError: If format type is not supported
        """
        format_type = format_type.lower().strip()
        if format_type not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported format type: {format_type}. "
                f"Supported formats: {', '.join(self.SUPPORTED_FORMATS)}"
            )
        return format_type
    
    def load_prompt(self, provider: str, model: str) -> str:
        """
        Load a system prompt from the local collection.

        Args:
            provider: Provider name (e.g., 'openai', 'anthropic', 'kimi')
            model: Model identifier (e.g., 'gpt-4.5', 'claude-3.7')

        Returns:
            The extracted system prompt content

        Raises:
            FileNotFoundError: If prompt file doesn't exist
            ValueError: If provider or model contains invalid characters

        Example:
            >>> installer = PromptInstaller()
            >>> prompt = installer.load_prompt("kimi", "base-chat")
            >>> print(f"Loaded {len(prompt)} characters")
        """
        self.provider = _paths.sanitize_path_component(provider)
        self.model_id = _paths.sanitize_path_component(model)

        content = _paths.load_prompt_file(provider, model)
        self.raw_content = content

        self.system_prompt = _paths.extract_system_prompt(content)
        return self.system_prompt
    
    def extract_clean_prompt(self, content: str) -> str:
        """
        Extract just the system prompt text from markdown content.

        Removes metadata headers, extracts content from "## System Prompt"
        section, and strips unnecessary formatting.

        Args:
            content: The raw markdown content

        Returns:
            Clean system prompt text

        Example:
            >>> installer = PromptInstaller()
            >>> content = Path("prompt.md").read_text()
            >>> clean = installer.extract_clean_prompt(content)
        """
        return _paths.extract_system_prompt(content)
    
    def format_output(self, format_type: str) -> Union[str, Dict[str, Any]]:
        """
        Format the loaded prompt in the specified output format.
        
        Args:
            format_type: One of 'raw', 'json', 'openai', 'anthropic'
            
        Returns:
            Formatted prompt as string or dict depending on format
            
        Raises:
            ValueError: If no prompt is loaded or format is invalid
            
        Example:
            >>> installer.load_prompt("openai", "gpt-4.5")
            >>> # Get raw text
            >>> raw = installer.format_output("raw")
            >>> # Get OpenAI format
            >>> openai_fmt = installer.format_output("openai")
            >>> # Get JSON format
            >>> json_fmt = installer.format_output("json")
        """
        if not self.system_prompt:
            raise ValueError("No system prompt loaded. Call load_prompt() first.")
        
        format_type = self._validate_format_type(format_type)
        
        if format_type == "raw":
            return self.system_prompt
        
        elif format_type == "json":
            return {
                "system_prompt": self.system_prompt,
                "provider": self.provider or "unknown",
                "model": self.model_id or "unknown",
                "format": "json",
                "length": len(self.system_prompt)
            }
        
        elif format_type == "openai":
            return {
                "role": "system",
                "content": self.system_prompt
            }
        
        elif format_type == "anthropic":
            # Anthropic uses a top-level 'system' parameter, not in messages
            return {
                "model": self.model_id or "claude-3-opus-20240229",
                "max_tokens": 4096,
                "system": self.system_prompt,
                "messages": []
            }
        
        else:
            # This should not happen due to validation, but just in case
            raise ValueError(f"Unexpected format type: {format_type}")
    
    def save_to_file(self, filepath: Union[str, Path], 
                     format_type: str = "raw") -> Path:
        """
        Save the formatted prompt to a file.
        
        Args:
            filepath: Path to save the file
            format_type: Output format to use
            
        Returns:
            Path to the saved file
            
        Raises:
            ValueError: If no prompt is loaded
            IOError: If file cannot be written
            
        Example:
            >>> installer.load_prompt("openai", "gpt-4.5")
            >>> installer.save_to_file("prompt.json", format_type="json")
            >>> installer.save_to_file("prompt.txt", format_type="raw")
        """
        if not self.system_prompt:
            raise ValueError("No system prompt loaded. Call load_prompt() first.")
        
        format_type = self._validate_format_type(format_type)
        filepath = Path(filepath)
        
        # Create parent directories if they don't exist
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Format the output
        formatted = self.format_output(format_type)
        
        # Write to file based on format
        if format_type in ["json", "openai", "anthropic"]:
            # JSON formats
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(formatted, f, indent=2, ensure_ascii=False)
        else:
            # Raw text format
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(formatted))
        
        return filepath
    
    def get_integration_example(self, provider: str) -> str:
        """
        Return a code example showing how to use the prompt with a provider's SDK.
        
        Args:
            provider: Provider name (e.g., 'openai', 'anthropic', 'kimi')
            
        Returns:
            Code snippet as a string
            
        Raises:
            ValueError: If no prompt is loaded
            
        Example:
            >>> installer.load_prompt("openai", "gpt-4.5")
            >>> print(installer.get_integration_example("openai"))
        """
        if not self.system_prompt:
            raise ValueError("No system prompt loaded. Call load_prompt() first.")
        
        # Sanitize provider name
        provider = _paths.sanitize_path_component(provider.lower())
        
        # Get the appropriate template
        template = self.INTEGRATION_EXAMPLES.get(
            provider, 
            self.INTEGRATION_EXAMPLES["default"]
        )
        
        # Fill in the template using replace() to avoid crash on { in prompts
        example = template.replace("{provider}", provider)
        example = example.replace("{model}", self.model_id or "model-name")
        example = example.replace("{system_prompt}", self.system_prompt)
        
        return example.strip()
    
    def list_integration_examples(self) -> List[str]:
        """
        List all available integration example providers.
        
        Returns:
            List of provider names with available examples
        """
        return list(self.INTEGRATION_EXAMPLES.keys())
    
    def get_formatted_prompt(self, format_type: str = "raw") -> FormattedPrompt:
        """
        Get a FormattedPrompt dataclass with metadata.
        
        Args:
            format_type: Output format to use
            
        Returns:
            FormattedPrompt dataclass instance
            
        Example:
            >>> installer.load_prompt("openai", "gpt-4.5")
            >>> formatted = installer.get_formatted_prompt("json")
            >>> print(formatted.content)
        """
        formatted = self.format_output(format_type)
        
        if isinstance(formatted, dict):
            content = json.dumps(formatted, indent=2, ensure_ascii=False)
        else:
            content = formatted
        
        return FormattedPrompt(
            content=content,
            format_type=format_type,
            provider=self.provider or "unknown",
            model=self.model_id or "unknown",
            metadata={
                "length": len(self.system_prompt) if self.system_prompt else 0,
                "raw_length": len(self.raw_content) if self.raw_content else 0
            }
        )
    
    def batch_export(self, prompts: List[Dict[str, str]], 
                     output_dir: Union[str, Path],
                     format_type: str = "json") -> List[Path]:
        """
        Export multiple prompts to files.
        
        Args:
            prompts: List of dicts with 'provider' and 'model' keys
            output_dir: Directory to save files
            format_type: Output format to use
            
        Returns:
            List of paths to saved files
            
        Example:
            >>> installer = PromptInstaller()
            >>> prompts = [
            ...     {"provider": "openai", "model": "gpt-4.5"},
            ...     {"provider": "anthropic", "model": "claude-sonnet-3.7"}
            ... ]
            >>> paths = installer.batch_export(prompts, "./exports", "json")
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        saved_paths = []
        original_provider = self.provider
        original_model = self.model_id
        original_prompt = self.system_prompt
        original_raw = self.raw_content
        
        try:
            for item in prompts:
                provider = item.get("provider")
                model = item.get("model")
                
                if not provider or not model:
                    continue
                
                try:
                    self.load_prompt(provider, model)
                    
                    # Create filename
                    safe_provider = _paths.sanitize_path_component(provider)
                    safe_model = _paths.sanitize_path_component(model)
                    filename = f"{safe_provider}_{safe_model}.{format_type if format_type != 'raw' else 'txt'}"
                    filepath = output_dir / filename
                    
                    # Save
                    self.save_to_file(filepath, format_type)
                    saved_paths.append(filepath)
                    
                except (FileNotFoundError, ValueError):
                    # Skip prompts that can't be loaded
                    continue
        finally:
            # Restore original state
            self.provider = original_provider
            self.model_id = original_model
            self.system_prompt = original_prompt
            self.raw_content = original_raw
        
        return saved_paths
