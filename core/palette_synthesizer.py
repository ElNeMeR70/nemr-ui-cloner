"""
Nemr UI Cloner - Algorithmic Palette Scale, Harmony & Contrast Synthesizer (v3.0.0)
Generates 11-stop Tailwind-style color ramps (50..950), color harmonies, and CSS/Tailwind/Flutter exports.
"""

from __future__ import annotations
import colorsys
import json
from typing import Any, Dict, List
from core.css_extractor import CssExtractor


class PaletteSynthesizer:
    """Synthesizes harmonious 11-stop color scales with WCAG-verified foreground pairings."""

    STOP_LIGHTNESS: Dict[str, float] = {
        "50": 0.96,
        "100": 0.91,
        "200": 0.83,
        "300": 0.72,
        "400": 0.60,
        "500": 0.50,
        "600": 0.42,
        "700": 0.34,
        "800": 0.26,
        "900": 0.18,
        "950": 0.10,
    }

    @staticmethod
    def _hls_to_hex(h: float, l: float, s: float) -> str:
        r, g, b = colorsys.hls_to_rgb(h % 1.0, max(0.02, min(0.98, l)), max(0.0, min(1.0, s)))
        return f"#{round(r * 255):02x}{round(g * 255):02x}{round(b * 255):02x}"

    @classmethod
    def generate_scale(cls, base_hex: str, name: str = "brand") -> Dict[str, Any]:
        r, g, b = CssExtractor._hex_to_rgb(base_hex)
        h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)

        stops: Dict[str, Dict[str, Any]] = {}
        for stop_key, target_l in cls.STOP_LIGHTNESS.items():
            # Slightly soften extreme light/dark stops for natural luminance curve
            adj_s = s * (0.85 if target_l > 0.85 or target_l < 0.15 else 1.0)
            stop_hex = cls._hls_to_hex(h, target_l, adj_s)
            c_white = CssExtractor.compute_contrast_ratio(stop_hex, "#ffffff")
            c_dark = CssExtractor.compute_contrast_ratio(stop_hex, "#0f172a")
            fg = "#ffffff" if c_white >= c_dark else "#0f172a"
            stops[stop_key] = {
                "hex": stop_hex,
                "foreground": fg,
                "contrast_ratio": max(c_white, c_dark),
            }

        harmonies = {
            "complementary": cls._hls_to_hex(h + 0.5, l, s),
            "analogous": [
                cls._hls_to_hex(h - 30.0 / 360.0, l, s),
                cls._hls_to_hex(h + 30.0 / 360.0, l, s),
            ],
            "triadic": [
                cls._hls_to_hex(h + 120.0 / 360.0, l, s),
                cls._hls_to_hex(h + 240.0 / 360.0, l, s),
            ],
        }

        return {
            "name": name,
            "base_hex": base_hex.lower(),
            "stops": stops,
            "harmonies": harmonies,
        }

    @classmethod
    def export_scale(cls, scale_data: Dict[str, Any], target: str = "css") -> str:
        name = scale_data["name"]
        stops = scale_data["stops"]
        tgt = target.lower()

        if tgt == "json":
            return json.dumps(scale_data, indent=2)

        if tgt == "css":
            lines = [":root {"]
            for stop, info in stops.items():
                lines.append(f"  --{name}-{stop}: {info['hex']};")
                lines.append(f"  --{name}-{stop}-fg: {info['foreground']};")
            lines.append("}")
            return "\n".join(lines) + "\n"

        if tgt == "tailwind":
            palette_dict = {stop: info["hex"] for stop, info in stops.items()}
            cfg = {"theme": {"extend": {"colors": {name: palette_dict}}}}
            return f"module.exports = {json.dumps(cfg, indent=2)};\n"

        if tgt == "flutter":
            class_name = "".join(p.capitalize() for p in name.replace("-", "_").split("_")) + "Palette"
            lines = [
                "import 'package:flutter/material.dart';",
                "",
                f"class {class_name} {{",
            ]
            for stop, info in stops.items():
                r, g, b = CssExtractor._hex_to_rgb(info["hex"])
                lines.append(f"  static const Color shade{stop} = Color(0xFF{r:02X}{g:02X}{b:02X});")
            lines.append("}")
            return "\n".join(lines) + "\n"

        raise ValueError(f"Unsupported export target: {target}")
