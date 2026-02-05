"""
System Prompt Builder Module

Provides intelligent templating and customization for system prompts.
Users can take a base prompt from any provider and customize it for their
specific use case while preserving the structural patterns that make it effective.

This is the core innovation of AgiTerminal - making system prompts
installable AND customizable.
"""

import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum


class CustomizationType(Enum):
    """Types of customizations that can be applied."""
    ROLE = "role"                    # Change the persona/role
    CAPABILITY_ADD = "cap_add"       # Add capabilities
    CAPABILITY_REMOVE = "cap_rem"    # Remove capabilities
    TONE = "tone"                    # Adjust tone/style
    CONSTRAINT_ADD = "con_add"       # Add constraints/rules
    CONSTRAINT_REMOVE = "con_rem"    # Remove constraints
    KNOWLEDGE = "knowledge"          # Adjust knowledge domains
    OUTPUT_FORMAT = "output"         # Change output format instructions


@dataclass
class PromptTemplate:
    """A parsed system prompt template."""
    original: str
    role_section: Optional[str] = None
    capability_sections: List[str] = field(default_factory=list)
    instruction_sections: List[str] = field(default_factory=list)
    constraint_sections: List[str] = field(default_factory=list)
    tone_indicators: List[str] = field(default_factory=list)
    structure_pattern: str = "standard"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for inspection."""
        return {
            "structure_pattern": self.structure_pattern,
            "has_role": self.role_section is not None,
            "capability_count": len(self.capability_sections),
            "instruction_count": len(self.instruction_sections),
            "constraint_count": len(self.constraint_sections),
            "tone_indicators": self.tone_indicators,
        }


@dataclass
class CustomizationRequest:
    """A request to customize a system prompt."""
    base_provider: str
    base_model: str
    use_case: str
    role_description: Optional[str] = None
    target_audience: Optional[str] = None
    tone_preference: Optional[str] = None
    capabilities_needed: List[str] = field(default_factory=list)
    constraints_to_add: List[str] = field(default_factory=list)
    constraints_to_remove: List[str] = field(default_factory=list)
    output_format: Optional[str] = None
    additional_context: Optional[str] = None


class PromptBuilder:
    """
    Builds customized system prompts from templates.
    
    This is the core engine that makes AgiTerminal more than just a library -
    it's a system prompt scaffolding tool.
    
    Example:
        >>> builder = PromptBuilder()
        >>> 
        >>> # Parse a base prompt
        >>> template = builder.parse_prompt(kimi_base_prompt)
        >>> 
        >>> # Create customization
        >>> request = CustomizationRequest(
        ...     base_provider="kimi",
        ...     base_model="base-chat",
        ...     use_case="Python coding tutor for beginners",
        ...     role_description="A patient Python tutor who explains concepts simply",
        ...     capabilities_needed=["code_examples", "error_explanation", "best_practices"],
        ...     tone_preference="friendly and encouraging"
        ... )
        >>> 
        >>> # Build customized prompt
        >>> custom_prompt = builder.build(request)
    """
    
    # Common patterns in system prompts
    ROLE_PATTERNS = [
        r"You are\s+([^.]+)\.",
        r"You are\s+([^.]+),",
        r"Your role is\s+([^.]+)\.",
        r"Act as\s+([^.]+)\.",
        r"You are an?\s+([^.]+)\.?",
    ]
    
    CAPABILITY_PATTERNS = [
        r"(?:capabilities?|skills?|abilities?)(?::|,|\s+include)\s+([^#]+?)(?:\n\n|\n#|##|$)",
        r"You can\s+([^#]+?)(?:\n\n|\n#|##|$)",
        r"(?:Core|Key)\s+(?:capabilities?|features?)(?::|\n)([^#]+?)(?:\n\n|\n#|##|$)",
    ]
    
    CONSTRAINT_PATTERNS = [
        r"(?:do not|don't|never|always|must|should|refuse)([^.]*)",
        r"(?:constraints?|rules?|guidelines?)(?::|\n)([^#]+?)(?:\n\n|\n#|##|$)",
    ]
    
    TONE_PATTERNS = [
        r"(?:tone|style|manner)(?::|is|should be)\s+([^.]+)",
        r"(?:friendly|professional|casual|formal|technical|simple)",
    ]
    
    def __init__(self):
        """Initialize the prompt builder."""
        self.template_cache: Dict[str, PromptTemplate] = {}
    
    def parse_prompt(self, prompt_text: str) -> PromptTemplate:
        """
        Parse a system prompt into its structural components.
        
        Args:
            prompt_text: The system prompt text to parse
            
        Returns:
            PromptTemplate with extracted sections
        """
        template = PromptTemplate(original=prompt_text)
        text_lower = prompt_text.lower()
        
        # Detect structure pattern
        if "you are" in text_lower and "capabilities" in text_lower:
            template.structure_pattern = "persona_with_capabilities"
        elif "###" in prompt_text or "## " in prompt_text:
            template.structure_pattern = "sectioned"
        elif "- " in prompt_text and prompt_text.count("\n-") > 3:
            template.structure_pattern = "bullet_list"
        else:
            template.structure_pattern = "narrative"
        
        # Extract role
        for pattern in self.ROLE_PATTERNS:
            match = re.search(pattern, prompt_text, re.IGNORECASE)
            if match:
                template.role_section = match.group(0)
                break
        
        # Extract capabilities
        for pattern in self.CAPABILITY_PATTERNS:
            matches = re.finditer(pattern, prompt_text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                template.capability_sections.append(match.group(0))
        
        # Extract constraints
        for pattern in self.CONSTRAINT_PATTERNS:
            matches = re.finditer(pattern, prompt_text, re.IGNORECASE)
            for match in matches:
                template.constraint_sections.append(match.group(0))
        
        # Detect tone indicators
        tone_words = ["friendly", "professional", "casual", "formal", 
                     "technical", "simple", "enthusiastic", "patient",
                     "direct", "detailed", "concise"]
        for word in tone_words:
            if word in text_lower:
                template.tone_indicators.append(word)
        
        # Extract instruction sections (numbered or bulleted)
        instruction_patterns = [
            r"(?:\d+\.\s+[^\n]+\n?)+",  # Numbered lists
            r"(?:[-•]\s+[^\n]+\n?){3,}",  # Bullet lists
        ]
        for pattern in instruction_patterns:
            matches = re.finditer(pattern, prompt_text)
            for match in matches:
                template.instruction_sections.append(match.group(0))
        
        return template
    
    def analyze_base_prompt(self, provider: str, model: str, 
                           prompt_text: str) -> Dict[str, Any]:
        """
        Analyze a base prompt and provide insights for customization.
        
        Args:
            provider: Provider name
            model: Model name
            prompt_text: The prompt text
            
        Returns:
            Analysis dictionary with customization suggestions
        """
        template = self.parse_prompt(prompt_text)
        
        analysis = {
            "provider": provider,
            "model": model,
            "structure": template.structure_pattern,
            "detected_role": template.role_section,
            "detected_capabilities": len(template.capability_sections),
            "detected_constraints": len(template.constraint_sections),
            "tone": template.tone_indicators,
            "customization_opportunities": [],
        }
        
        # Suggest customization opportunities
        if template.role_section:
            analysis["customization_opportunities"].append(
                "Role/persona can be adapted to your specific use case"
            )
        
        if template.capability_sections:
            analysis["customization_opportunities"].append(
                f"{len(template.capability_sections)} capability section(s) can be customized"
            )
        
        if template.structure_pattern in ["persona_with_capabilities", "sectioned"]:
            analysis["customization_opportunities"].append(
                "Well-structured template - easy to customize sections"
            )
        
        return analysis
    
    def build(self, request: CustomizationRequest, 
              base_prompt_text: str) -> str:
        """
        Build a customized system prompt from a template and request.
        
        Args:
            request: The customization request
            base_prompt_text: The base prompt to customize
            
        Returns:
            Customized system prompt text
        """
        template = self.parse_prompt(base_prompt_text)
        
        # Start with the original
        customized = base_prompt_text
        
        # Apply role customization
        if request.role_description:
            customized = self._apply_role_customization(
                customized, template, request.role_description
            )
        
        # Apply capability customization
        if request.capabilities_needed:
            customized = self._apply_capability_customization(
                customized, template, request.capabilities_needed
            )
        
        # Apply tone customization
        if request.tone_preference:
            customized = self._apply_tone_customization(
                customized, template, request.tone_preference
            )
        
        # Apply constraint customization
        if request.constraints_to_add or request.constraints_to_remove:
            customized = self._apply_constraint_customization(
                customized, template, 
                request.constraints_to_add,
                request.constraints_to_remove
            )
        
        # Apply output format customization
        if request.output_format:
            customized = self._apply_output_customization(
                customized, request.output_format
            )
        
        # Add context header if provided
        if request.additional_context:
            customized = self._add_context_section(
                customized, request.additional_context
            )
        
        return customized
    
    def _apply_role_customization(self, text: str, template: PromptTemplate,
                                  new_role: str) -> str:
        """Apply role/persona customization."""
        if template.role_section:
            # Replace existing role statement
            for pattern in self.ROLE_PATTERNS:
                if re.search(pattern, text, re.IGNORECASE):
                    new_role_statement = f"You are {new_role}."
                    text = re.sub(pattern, new_role_statement, text, 
                                count=1, flags=re.IGNORECASE)
                    break
        else:
            # Add role statement at the beginning
            text = f"You are {new_role}.\n\n{text}"
        
        return text
    
    def _apply_capability_customization(self, text: str, template: PromptTemplate,
                                       capabilities: List[str]) -> str:
        """Apply capability customization."""
        if not capabilities:
            return text
        
        # Format capabilities as a list
        cap_lines = "\n".join(f"- {cap}" for cap in capabilities)
        
        if template.capability_sections:
            # Replace first capability section
            # Find a good spot to insert
            sections = text.split("\n\n")
            for i, section in enumerate(sections):
                if any(indicator in section.lower() 
                      for indicator in ["capability", "can", "able to"]):
                    sections[i] = f"### Capabilities\n\n{cap_lines}"
                    break
            text = "\n\n".join(sections)
        else:
            # Add capabilities section after role
            text = f"{text}\n\n### Capabilities\n\n{cap_lines}"
        
        return text
    
    def _apply_tone_customization(self, text: str, template: PromptTemplate,
                                 tone: str) -> str:
        """Apply tone/style customization."""
        tone_section = f"\n\n### Communication Style\n\nYour tone should be {tone}."
        
        # Check if there's already a tone section
        if "tone" in text.lower() or "style" in text.lower():
            # Replace existing tone instructions
            text = re.sub(
                r"(?:tone|style|communication)[^.]*(?:is|should be|must be)[^.]*\.?",
                f"Your tone is {tone}.",
                text,
                flags=re.IGNORECASE
            )
        else:
            # Add tone section
            text = f"{text}{tone_section}"
        
        return text
    
    def _apply_constraint_customization(self, text: str, template: PromptTemplate,
                                       add_constraints: List[str],
                                       remove_constraints: List[str]) -> str:
        """Apply constraint customization."""
        # Add new constraints
        if add_constraints:
            constraint_lines = "\n".join(f"- {c}" for c in add_constraints)
            
            if template.constraint_sections:
                # Append to existing
                text = f"{text}\n\n### Additional Guidelines\n\n{constraint_lines}"
            else:
                # Add new section
                text = f"{text}\n\n### Guidelines\n\n{constraint_lines}"
        
        # Remove constraints (basic implementation)
        for constraint in remove_constraints:
            # Remove lines containing the constraint
            lines = text.split("\n")
            lines = [l for l in lines if constraint.lower() not in l.lower()]
            text = "\n".join(lines)
        
        return text
    
    def _apply_output_customization(self, text: str, 
                                   output_format: str) -> str:
        """Apply output format customization."""
        output_section = f"\n\n### Output Format\n\n{output_format}"
        
        # Remove existing output format section if present
        text = re.sub(
            r"\n\n### Output Format.*?(?=\n\n###|$)",
            "",
            text,
            flags=re.DOTALL
        )
        
        # Add new output section
        text = f"{text}{output_section}"
        
        return text
    
    def _add_context_section(self, text: str, context: str) -> str:
        """Add additional context section."""
        context_section = f"\n\n### Context\n\n{context}"
        text = f"{text}{context_section}"
        return text
    
    def suggest_template_for_use_case(self, use_case: str) -> List[Tuple[str, str, float]]:
        """
        Suggest base templates that might work well for a use case.
        
        Args:
            use_case: Description of the use case
            
        Returns:
            List of (provider, model, relevance_score) tuples
        """
        use_case_lower = use_case.lower()
        suggestions = []
        
        # Keyword matching for suggestions
        keyword_mapping = {
            "code": [("cursor", "agent-prompt-2.0", 0.95),
                    ("augment-code", "gpt-5-agent-prompts", 0.90),
                    ("github-copilot", "agent", 0.85)],
            "write": [("kimi", "docs", 0.90),
                     ("notion", "prompt", 0.85)],
            "chat": [("kimi", "base-chat", 0.95),
                    ("openai", "gpt-4o", 0.90)],
            "agent": [("cursor", "agent-cli-prompt-2025-08-07", 0.95),
                     ("devin", "prompt", 0.90)],
            "creative": [("lovable", "agent-prompt", 0.90),
                        ("v0", "prompt", 0.85)],
        }
        
        for keyword, templates in keyword_mapping.items():
            if keyword in use_case_lower:
                suggestions.extend(templates)
        
        # Sort by relevance
        suggestions.sort(key=lambda x: x[2], reverse=True)
        
        # Default suggestion if no match
        if not suggestions:
            suggestions = [
                ("kimi", "base-chat", 0.70),
                ("openai", "gpt-4o", 0.65),
            ]
        
        return suggestions[:5]  # Top 5
    
    def preview_customization(self, request: CustomizationRequest,
                             base_prompt_text: str) -> str:
        """
        Generate a preview of what will change.
        
        Args:
            request: The customization request
            base_prompt_text: The base prompt
            
        Returns:
            Preview text describing changes
        """
        template = self.parse_prompt(base_prompt_text)
        
        preview_lines = [
            "=" * 60,
            "CUSTOMIZATION PREVIEW",
            "=" * 60,
            "",
            f"Base Template: {request.base_provider}/{request.base_model}",
            f"Structure Pattern: {template.structure_pattern}",
            "",
            "Proposed Changes:",
        ]
        
        if request.role_description:
            preview_lines.append(f"  [+] Role: {request.role_description[:50]}...")
        
        if request.capabilities_needed:
            preview_lines.append(f"  [+] Capabilities: {len(request.capabilities_needed)} items")
        
        if request.tone_preference:
            preview_lines.append(f"  [+] Tone: {request.tone_preference}")
        
        if request.constraints_to_add:
            preview_lines.append(f"  [+] Constraints: {len(request.constraints_to_add)} added")
        
        if request.constraints_to_remove:
            preview_lines.append(f"  [-] Constraints: {len(request.constraints_to_remove)} removed")
        
        if request.output_format:
            preview_lines.append(f"  [+] Output Format: Custom")
        
        preview_lines.extend([
            "",
            "=" * 60,
        ])
        
        return "\n".join(preview_lines)
