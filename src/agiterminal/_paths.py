"""
Shared path utilities for loading system prompts from the collections directory.

Centralizes path resolution, sanitization, and file loading logic used by
both the analyzer and installer modules.
"""

from pathlib import Path
from typing import List, Optional


def get_collections_path() -> Path:
    """
    Get the path to the collections directory.

    Returns:
        Path to the collections/ directory
    """
    return Path(__file__).parent.parent.parent / "collections"


def sanitize_path_component(component: str) -> str:
    """
    Sanitize a path component to prevent path traversal attacks.

    Args:
        component: The path component to sanitize

    Returns:
        Sanitized component safe for path construction
    """
    sanitized = component.replace('/', '').replace('\\', '').replace('..', '')
    sanitized = ''.join(c for c in sanitized if c.isalnum() or c in '-_.')
    return sanitized


def list_providers(collections_path: Optional[Path] = None) -> List[str]:
    """
    List all available providers in the collections directory.

    Args:
        collections_path: Optional path to collections directory

    Returns:
        List of provider directory names
    """
    if collections_path is None:
        collections_path = get_collections_path()

    providers = []
    if collections_path.exists():
        for item in collections_path.iterdir():
            if item.is_dir() and item.name != "docs":
                providers.append(item.name)
    return sorted(providers)


def list_models(provider: str, collections_path: Optional[Path] = None) -> List[str]:
    """
    List all available models for a given provider.

    Args:
        provider: Provider name
        collections_path: Optional path to collections directory

    Returns:
        List of model file names (without .md extension)
    """
    if collections_path is None:
        collections_path = get_collections_path()

    provider_path = collections_path / provider
    if not provider_path.exists():
        return []

    models = []
    for item in provider_path.iterdir():
        if item.is_file() and item.suffix == '.md':
            models.append(item.stem)
    return sorted(models)


def resolve_prompt_path(provider: str, model: str,
                        collections_path: Optional[Path] = None) -> Path:
    """
    Resolve and validate the file path for a provider/model prompt.

    Args:
        provider: Provider name (will be sanitized)
        model: Model identifier (will be sanitized)
        collections_path: Optional path to collections directory

    Returns:
        Resolved Path to the prompt file

    Raises:
        FileNotFoundError: If prompt file doesn't exist
        ValueError: If provider or model is empty after sanitization
    """
    provider = sanitize_path_component(provider)
    model = sanitize_path_component(model)

    if not provider or not model:
        raise ValueError("Provider and model must not be empty after sanitization")

    if collections_path is None:
        collections_path = get_collections_path()

    possible_paths = [
        collections_path / provider / f"{model}.md",
        collections_path / provider / f"{model.replace('-', '_')}.md",
        collections_path / provider / f"{model.replace('_', '-')}.md",
    ]

    for path in possible_paths:
        try:
            resolved = path.resolve()
            base_resolved = collections_path.resolve()
            if not str(resolved).startswith(str(base_resolved)):
                continue
            if resolved.exists():
                return resolved
        except (OSError, ValueError):
            continue

    raise FileNotFoundError(
        f"Prompt not found for {provider}/{model}. "
        f"Tried: {[str(p) for p in possible_paths]}"
    )


def load_prompt_file(provider: str, model: str,
                     collections_path: Optional[Path] = None) -> str:
    """
    Load raw content from a prompt file.

    Args:
        provider: Provider name
        model: Model identifier
        collections_path: Optional path to collections directory

    Returns:
        Raw file content as string

    Raises:
        FileNotFoundError: If prompt file doesn't exist
        ValueError: If provider or model is invalid
    """
    prompt_path = resolve_prompt_path(provider, model, collections_path)
    return prompt_path.read_text(encoding='utf-8')


def extract_system_prompt(content: str) -> str:
    """
    Extract the system prompt section from markdown content.

    Looks for '## System Prompt' markers; falls back to full content
    minus the first heading line.

    Args:
        content: Raw markdown content

    Returns:
        Extracted system prompt text
    """
    if "## System Prompt" in content:
        parts = content.split("## System Prompt")
        if len(parts) > 1:
            prompt_part = parts[1]
            for separator in ["\n---\n", "\n## "]:
                if separator in prompt_part:
                    prompt_part = prompt_part.split(separator)[0]
                    break
            return prompt_part.strip()

    lines = content.split('\n')
    if lines and lines[0].startswith('#'):
        content = '\n'.join(lines[1:]).strip()

    return content.strip()
