"""
Nemr UI Cloner - Design Token & Style Extractor
Parses raw HTML and CSS styles to extract color palettes, typography, spacing, and border radius.
"""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import Dict, List, Set


@dataclass
class DesignTokens:
    colors: Set[str] = field(default_factory=set)
    fonts: Set[str] = field(default_factory=set)
    border_radiuses: Set[str] = field(default_factory=set)
    box_shadows: Set[str] = field(default_factory=set)


class CssExtractor:
    """Extracts design systems and tokens from raw HTML/CSS strings."""

    HEX_REGEX = re.compile(r"#(?:[0-9a-fA-F]{3,4}){1,2}\b")
    RGB_REGEX = re.compile(r"rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+(?:\s*,\s*[\d\.]+)?\s*\)")
    FONT_REGEX = re.compile(r"font-family\s*:\s*([^;]+);", re.IGNORECASE)
    RADIUS_REGEX = re.compile(r"border-radius\s*:\s*([^;]+);", re.IGNORECASE)
    SHADOW_REGEX = re.compile(r"box-shadow\s*:\s*([^;]+);", re.IGNORECASE)

    @classmethod
    def extract_tokens(cls, source_code: str) -> DesignTokens:
        tokens = DesignTokens()

        # Colors
        for m in cls.HEX_REGEX.finditer(source_code):
            tokens.colors.add(m.group(0).lower())
        for m in cls.RGB_REGEX.finditer(source_code):
            tokens.colors.add(m.group(0).lower())

        # Fonts
        for m in cls.FONT_REGEX.finditer(source_code):
            raw_font = m.group(1).split(",")[0].strip().strip("'\"")
            if raw_font:
                tokens.fonts.add(raw_font)

        # Border radius
        for m in cls.RADIUS_REGEX.finditer(source_code):
            tokens.border_radiuses.add(m.group(1).strip())

        # Shadows
        for m in cls.SHADOW_REGEX.finditer(source_code):
            tokens.box_shadows.add(m.group(1).strip())

        return tokens
