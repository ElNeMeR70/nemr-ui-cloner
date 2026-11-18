"""
Nemr UI Cloner - Directional RTL / LTR Adapter
Swaps horizontal alignments, margins, and paddings for Arabic RTL layout rendering.
"""

from __future__ import annotations
import re


class RtlAdapter:
    """Converts LTR CSS/Tailwind classes into Arabic RTL compatible equivalents."""

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

    @classmethod
    def convert_to_rtl(cls, markup: str, inject_arabic_font: bool = True) -> str:
        converted = markup

        # Swap direction in <html> or wrapper
        if '<html lang="en"' in converted:
            converted = converted.replace('<html lang="en"', '<html lang="ar" dir="rtl"')
        elif '<html' in converted and 'dir="rtl"' not in converted:
            converted = converted.replace('<html', '<html dir="rtl"')

        # Single-pass directional replacement to prevent reciprocal flip-flops
        token_map = {
            "text-left": "text-right",
            "text-right": "text-left",
            "rounded-l-": "rounded-r-",
            "rounded-r-": "rounded-l-",
        }

        def token_replacer(match):
            val = match.group(0)
            return token_map.get(val, val)

        pattern = r"\b(text-left|text-right)\b|(rounded-l-|rounded-r-)"
        converted = re.sub(pattern, token_replacer, converted)

        # Handle parameterized margins and paddings: ml- <-> mr-, pl- <-> pr-
        def margin_replacer(match):
            prefix = match.group(1)
            num = match.group(2)
            swap_prefix = {
                "mr-": "ml-",
                "ml-": "mr-",
                "pr-": "pl-",
                "pl-": "pr-",
                "left-": "right-",
                "right-": "left-",
            }
            return f"{swap_prefix.get(prefix, prefix)}{num}"

        converted = re.sub(r"\b(mr-|ml-|pr-|pl-|left-|right-)(\d+)\b", margin_replacer, converted)

        if inject_arabic_font and "Cairo" not in converted:
            converted = converted.replace(
                "</head>",
                '  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap">\n</head>'
            )

        return converted
