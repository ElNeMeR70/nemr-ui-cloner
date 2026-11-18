#!/usr/bin/env python3
"""
Nemr UI Cloner - Unified CLI
Design token extraction, multi-target component generation (Tailwind, Flutter), and RTL Arabic mirroring.
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from core.css_extractor import CssExtractor
from core.component_generator import ComponentGenerator
from core.rtl_adapter import RtlAdapter


def cmd_tokens(args: argparse.Namespace) -> None:
    source_file = Path(args.file)
    if not source_file.exists():
        print(f"Error: File {source_file} not found.")
        sys.exit(1)

    print(f"\n🎨 Extracting Design Tokens from: {source_file}...\n")
    tokens = CssExtractor.extract_tokens(source_file.read_text(encoding="utf-8", errors="ignore"))

    print(f"Colors Extracted ({len(tokens.colors)}): {list(tokens.colors)[:8]}")
    print(f"Fonts ({len(tokens.fonts)}): {list(tokens.fonts)}")
    print(f"Border Radiuses ({len(tokens.border_radiuses)}): {list(tokens.border_radiuses)}")
    print(f"Shadows ({len(tokens.box_shadows)}): {list(tokens.box_shadows)[:4]}\n")


def cmd_tailwind(args: argparse.Namespace) -> None:
    print(f"\n⚡ Generating Tailwind CSS 3.4 Card Component...\n")
    card = ComponentGenerator.generate_tailwind_card(
        title=args.title,
        subtitle=args.subtitle,
        cta_text=args.cta
    )
    print("=" * 60)
    print(card)
    print("=" * 60 + "\n")


def cmd_flutter(args: argparse.Namespace) -> None:
    print(f"\n📱 Generating Flutter Responsive Widget Tree...\n")
    widget = ComponentGenerator.generate_flutter_card(
        title=args.title,
        subtitle=args.subtitle,
        cta_text=args.cta
    )
    print("=" * 60)
    print(widget)
    print("=" * 60 + "\n")


def cmd_rtl(args: argparse.Namespace) -> None:
    source_file = Path(args.file)
    if not source_file.exists():
        print(f"Error: File {source_file} not found.")
        sys.exit(1)

    print(f"\n🔄 Converting Markup to Arabic RTL: {source_file}...\n")
    converted = RtlAdapter.convert_to_rtl(source_file.read_text(encoding="utf-8", errors="ignore"))
    out_file = Path(args.out or (source_file.stem + "_rtl" + source_file.suffix))
    out_file.write_text(converted, encoding="utf-8")
    print(f"✓ Saved RTL markup to: {out_file}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Nemr UI Cloner: Pixel-Clean UI & RTL Adapter")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # clone-tokens
    p_tok = subparsers.add_parser("clone-tokens", help="Extract colors, fonts, and shadows")
    p_tok.add_argument("file", type=str, help="HTML or CSS file")
    p_tok.set_defaults(func=cmd_tokens)

    # to-tailwind
    p_tw = subparsers.add_parser("to-tailwind", help="Generate Tailwind card component")
    p_tw.add_argument("--title", type=str, default="Nemr Apex Cloud", help="Card title")
    p_tw.add_argument("--subtitle", type=str, default="Enterprise Cloud Engineering OS", help="Card subtitle")
    p_tw.add_argument("--cta", type=str, default="Get Started", help="CTA label")
    p_tw.set_defaults(func=cmd_tailwind)

    # to-flutter
    p_fl = subparsers.add_parser("to-flutter", help="Generate Flutter responsive card widget")
    p_fl.add_argument("--title", type=str, default="Nemr Apex Cloud", help="Card title")
    p_fl.add_argument("--subtitle", type=str, default="Enterprise Cloud Engineering OS", help="Card subtitle")
    p_fl.add_argument("--cta", type=str, default="Get Started", help="CTA label")
    p_fl.set_defaults(func=cmd_flutter)

    # rtl-convert
    p_rtl = subparsers.add_parser("rtl-convert", help="Convert LTR HTML to Arabic RTL")
    p_rtl.add_argument("file", type=str, help="Input HTML file")
    p_rtl.add_argument("--out", type=str, default=None, help="Output file")
    p_rtl.set_defaults(func=cmd_rtl)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
