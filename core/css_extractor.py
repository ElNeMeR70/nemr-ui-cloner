"""
Nemr UI Cloner - Design Token, WCAG Contrast Auditor & Theme Exporter (v2.0.0)
Extracts CSS tokens, computes WCAG 2.1 luminance contrast ratios, and exports CSS variables, Tailwind config, or Flutter ThemeData.
"""

from __future__ import annotations
import json
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Set, Tuple


@dataclass
class DesignTokens:
    colors: Set[str] = field(default_factory=set)
    fonts: Set[str] = field(default_factory=set)
    border_radiuses: Set[str] = field(default_factory=set)
    box_shadows: Set[str] = field(default_factory=set)


class CssExtractor:
    """Extracts design tokens, audits WCAG contrast, and exports multi-target themes."""

    HEX_REGEX = re.compile(r"#(?:[0-9a-fA-F]{3,4}){1,2}\b")
    RGB_REGEX = re.compile(r"rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+(?:\s*,\s*[\d\.]+)?\s*\)")
    FONT_REGEX = re.compile(r"font-family\s*:\s*([^;]+);", re.IGNORECASE)
    RADIUS_REGEX = re.compile(r"border-radius\s*:\s*([^;]+);", re.IGNORECASE)
    SHADOW_REGEX = re.compile(r"box-shadow\s*:\s*([^;]+);", re.IGNORECASE)

    @classmethod
    def extract_tokens(cls, source_code: str) -> DesignTokens:
        tokens = DesignTokens()

        for m in cls.HEX_REGEX.finditer(source_code):
            tokens.colors.add(m.group(0).lower())
        for m in cls.RGB_REGEX.finditer(source_code):
            tokens.colors.add(m.group(0).lower())

        for m in cls.FONT_REGEX.finditer(source_code):
            raw_font = m.group(1).split(",")[0].strip().strip("'\"")
            if raw_font:
                tokens.fonts.add(raw_font)

        for m in cls.RADIUS_REGEX.finditer(source_code):
            tokens.border_radiuses.add(m.group(1).strip())

        for m in cls.SHADOW_REGEX.finditer(source_code):
            tokens.box_shadows.add(m.group(1).strip())

        return tokens

    @staticmethod
    def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        h = hex_color.strip().lstrip("#")
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h[:3])
        elif len(h) == 8:
            h = h[:6]
        if len(h) != 6:
            raise ValueError(f"Unsupported hex color: {hex_color}")
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

    @staticmethod
    def _relative_luminance(rgb: Tuple[int, int, int]) -> float:
        def chan(c: int) -> float:
            s = c / 255.0
            return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4

        r, g, b = rgb
        return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)

    @classmethod
    def compute_contrast_ratio(cls, hex1: str, hex2: str) -> float:
        """Computes WCAG 2.1 contrast ratio between two hex colors (1.0 to 21.0)."""
        lum1 = cls._relative_luminance(cls._hex_to_rgb(hex1))
        lum2 = cls._relative_luminance(cls._hex_to_rgb(hex2))
        lighter = max(lum1, lum2)
        darker = min(lum1, lum2)
        return round((lighter + 0.05) / (darker + 0.05), 2)

    @classmethod
    def audit_contrast(cls, colors: Set[str]) -> List[Dict[str, Any]]:
        """Audits extracted hex colors against light (#ffffff) and dark (#0f172a) surfaces."""
        hex_colors = sorted(c for c in colors if c.startswith("#") and len(c) in (4, 7))
        results: List[Dict[str, Any]] = []
        for col in hex_colors:
            try:
                on_white = cls.compute_contrast_ratio(col, "#ffffff")
                on_dark = cls.compute_contrast_ratio(col, "#0f172a")
            except ValueError:
                continue
            best = max(on_white, on_dark)
            level = "AAA" if best >= 7.0 else ("AA" if best >= 4.5 else ("AA-Large" if best >= 3.0 else "FAIL"))
            results.append({
                "color": col,
                "contrast_on_white": on_white,
                "contrast_on_dark": on_dark,
                "wcag_rating": level,
                "recommended_text_on_bg": "#ffffff" if on_white >= on_dark else "#0f172a",
            })
        return results

    @classmethod
    def export_theme(cls, tokens: DesignTokens, target: str = "css") -> str:
        """Exports DesignTokens into CSS custom properties, tailwind.config.js, or Flutter ThemeData."""
        hex_palette = sorted(c for c in tokens.colors if c.startswith("#"))
        primary = hex_palette[0] if hex_palette else "#4f46e5"
        surface = "#ffffff" if "#ffffff" in hex_palette else (hex_palette[1] if len(hex_palette) > 1 else "#f8fafc")
        font_primary = sorted(tokens.fonts)[0] if tokens.fonts else "Plus Jakarta Sans"
        radius = sorted(tokens.border_radiuses)[0] if tokens.border_radiuses else "12px"

        tgt = target.lower()
        if tgt == "css":
            color_vars = "\n".join(f"  --color-token-{i}: {c};" for i, c in enumerate(hex_palette, 1))
            return f""":root {{
  --color-primary: {primary};
  --color-surface: {surface};
  --font-sans: '{font_primary}', system-ui, sans-serif;
  --radius-base: {radius};
{color_vars}
}}

[data-theme="dark"] {{
  --color-surface: #0f172a;
}}
"""
        elif tgt == "tailwind":
            color_obj = {f"token-{i}": c for i, c in enumerate(hex_palette, 1)}
            color_obj["primary"] = primary
            cfg = {
                "theme": {
                    "extend": {
                        "colors": color_obj,
                        "fontFamily": {"sans": [font_primary, "system-ui", "sans-serif"]},
                        "borderRadius": {"base": radius},
                    }
                }
            }
            return f"module.exports = {json.dumps(cfg, indent=2)};\n"

        elif tgt == "flutter":
            dart_colors = []
            for i, col in enumerate(hex_palette, 1):
                try:
                    r, g, b = cls._hex_to_rgb(col)
                    dart_colors.append(f"  static const Color token{i} = Color(0xFF{r:02X}{g:02X}{b:02X});")
                except ValueError:
                    continue
            r0, g0, b0 = cls._hex_to_rgb(primary if primary.startswith("#") else "#4f46e5")
            primary_hex = f"0xFF{r0:02X}{g0:02X}{b0:02X}"
            return f"""import 'package:flutter/material.dart';

class NemrThemeTokens {{
  static const Color primary = Color({primary_hex});
{chr(10).join(dart_colors)}

  static ThemeData lightTheme() => ThemeData(
        useMaterial3: true,
        colorSchemeSeed: primary,
        fontFamily: '{font_primary}',
      );
}}
"""
        raise ValueError(f"Unsupported theme export target: {target}")
