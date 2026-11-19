"""
Nemr UI Cloner - Directional RTL / LTR & CSS Logical Properties Adapter (v2.0.0)
Mirrors Tailwind classes & raw CSS properties for Arabic RTL, and supports modern CSS logical classes.
"""

from __future__ import annotations
import re


class RtlAdapter:
    """Converts LTR HTML/CSS markup into Arabic RTL or logical Tailwind equivalents."""

    REPLACEMENTS = [
        (r"\btext-left\b", "text-right"),
        (r"\btext-right\b", "text-left"),
        (r"\bmr-(\d+)\b", r"ml-\1"),
        (r"\bml-(\d+)\b", r"mr-\1"),
        (r"\bpr-(\d+)\b", r"pl-\1"),
        (r"\bpl-(\d+)\b", r"pr-\1"),
        (r"\bleft-(\d+)\b", r"right-\1"),
        (r"\bright-(\d+)\b", r"left-\1"),
        (r"\brounded-l-", "rounded-r-"),
        (r"\brounded-r-", "rounded-l-"),
    ]

    CSS_PROP_SWAP = {
        "margin-left": "margin-right",
        "margin-right": "margin-left",
        "padding-left": "padding-right",
        "padding-right": "padding-left",
        "border-left": "border-right",
        "border-right": "border-left",
    }

    @classmethod
    def convert_to_rtl(cls, markup: str, inject_arabic_font: bool = True) -> str:
        converted = markup

        if '<html lang="en"' in converted:
            converted = converted.replace('<html lang="en"', '<html lang="ar" dir="rtl"')
        elif '<html' in converted and 'dir="rtl"' not in converted:
            converted = converted.replace('<html', '<html dir="rtl"')

        token_map = {
            "text-left": "text-right",
            "text-right": "text-left",
            "rounded-l-": "rounded-r-",
            "rounded-r-": "rounded-l-",
        }
        converted = re.sub(
            r"\b(text-left|text-right)\b|(rounded-l-|rounded-r-)",
            lambda m: token_map.get(m.group(0), m.group(0)),
            converted,
        )

        swap_prefix = {
            "mr-": "ml-",
            "ml-": "mr-",
            "pr-": "pl-",
            "pl-": "pr-",
            "left-": "right-",
            "right-": "left-",
        }
        converted = re.sub(
            r"\b(mr-|ml-|pr-|pl-|left-|right-)(\d+)\b",
            lambda m: f"{swap_prefix.get(m.group(1), m.group(1))}{m.group(2)}",
            converted,
        )

        # Single-pass raw CSS property mirroring
        converted = re.sub(
            r"\b(margin-left|margin-right|padding-left|padding-right|border-left|border-right)\b(?=\s*:)",
            lambda m: cls.CSS_PROP_SWAP.get(m.group(1).lower(), m.group(1)),
            converted,
            flags=re.IGNORECASE,
        )
        converted = re.sub(
            r"(text-align|float)\s*:\s*(left|right)\b",
            lambda m: f"{m.group(1)}: {'right' if m.group(2).lower() == 'left' else 'left'}",
            converted,
            flags=re.IGNORECASE,
        )

        if inject_arabic_font and "Cairo" not in converted:
            converted = converted.replace(
                "</head>",
                '  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap">\n</head>',
            )

        return converted

    @classmethod
    def convert_to_logical(cls, markup: str) -> str:
        """Converts physical Tailwind classes to CSS logical equivalents (ms-/me-/ps-/pe-/text-start/rounded-s)."""
        static_map = {
            "text-left": "text-start",
            "text-right": "text-end",
            "rounded-l-": "rounded-s-",
            "rounded-r-": "rounded-e-",
        }
        out = re.sub(
            r"\b(text-left|text-right)\b|(rounded-l-|rounded-r-)",
            lambda m: static_map.get(m.group(0), m.group(0)),
            markup,
        )
        param_map = {
            "ml-": "ms-",
            "mr-": "me-",
            "pl-": "ps-",
            "pr-": "pe-",
        }
        return re.sub(
            r"\b(ml-|mr-|pl-|pr-)(\d+)\b",
            lambda m: f"{param_map.get(m.group(1), m.group(1))}{m.group(2)}",
            out,
        )
