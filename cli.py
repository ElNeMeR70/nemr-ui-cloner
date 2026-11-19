#!/usr/bin/env python3
"""
Nemr UI Cloner v3.0.0 - Unified CLI (Sovereign Edition)
Design token & WCAG auditing, 11-stop palette synthesizer, HTML A11y & responsive auditor,
DOM-to-Flutter/Tailwind transpiler, multi-pattern UI generation, and RTL/Logical adapter.
"""

from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from core.css_extractor import CssExtractor
from core.component_generator import ComponentGenerator
from core.dom_transpiler import DomTranspiler
from core.rtl_adapter import RtlAdapter
from core.palette_synthesizer import PaletteSynthesizer
from core.a11y_auditor import A11yResponsiveAuditor

VERSION = "3.0.0"


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
    print(f"Shadows ({len(tokens.box_shadows)}): {list(tokens.box_shadows)[:4]}")

    if args.contrast:
        audit = CssExtractor.audit_contrast(tokens.colors)
        print("\n👁️ WCAG 2.1 Contrast Audit:")
        for row in audit:
            print(f"  {row['color']:10} -> white={row['contrast_on_white']}:1, dark={row['contrast_on_dark']}:1 [{row['wcag_rating']}]")

    if args.export:
        theme_out = CssExtractor.export_theme(tokens, target=args.export)
        print(f"\n📦 Exported Theme ({args.export.upper()}):\n" + "=" * 60)
        print(theme_out)
        print("=" * 60)
    print()


def cmd_tailwind(args: argparse.Namespace) -> None:
    print(f"\n⚡ Generating Tailwind CSS 3.4 `{args.kind}` Component...\n")
    comp = ComponentGenerator.generate_component(
        kind=args.kind,
        target="tailwind",
        title=args.title,
        subtitle=args.subtitle,
        cta_text=args.cta,
    )
    print("=" * 60)
    print(comp)
    print("=" * 60 + "\n")


def cmd_flutter(args: argparse.Namespace) -> None:
    print(f"\n📱 Generating Flutter Responsive `{args.kind}` Widget...\n")
    widget = ComponentGenerator.generate_component(
        kind=args.kind,
        target="flutter",
        title=args.title,
        subtitle=args.subtitle,
        cta_text=args.cta,
    )
    print("=" * 60)
    print(widget)
    print("=" * 60 + "\n")


def cmd_transpile(args: argparse.Namespace) -> None:
    source_file = Path(args.html_file)
    if not source_file.exists():
        print(f"Error: File {source_file} not found.")
        sys.exit(1)

    html = source_file.read_text(encoding="utf-8", errors="ignore")
    output = DomTranspiler.to_flutter_widget(html, widget_name=args.widget_name) if args.target == "flutter" else DomTranspiler.to_clean_tailwind(html)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
        print(f"\n✓ Transpiled `{source_file}` -> `{out_path}` ({args.target}).\n")
    else:
        print("=" * 60)
        print(output)
        print("=" * 60 + "\n")


def cmd_rtl(args: argparse.Namespace) -> None:
    source_file = Path(args.file)
    if not source_file.exists():
        print(f"Error: File {source_file} not found.")
        sys.exit(1)

    raw = source_file.read_text(encoding="utf-8", errors="ignore")
    if args.logical:
        converted = RtlAdapter.convert_to_logical(raw)
        default_suffix = "_logical"
    else:
        converted = RtlAdapter.convert_to_rtl(raw)
        default_suffix = "_rtl"

    out_file = Path(args.out or (source_file.stem + default_suffix + source_file.suffix))
    out_file.write_text(converted, encoding="utf-8")
    print(f"\n✓ Saved converted markup to: {out_file}\n")


def cmd_palette(args: argparse.Namespace) -> None:
    scale_data = PaletteSynthesizer.generate_scale(args.hex, name=args.name)
    exported = PaletteSynthesizer.export_scale(scale_data, target=args.export)
    print(exported)


def cmd_audit_ui(args: argparse.Namespace) -> None:
    target = Path(args.html_file)
    if not target.exists():
        print(f"Error: HTML file '{target}' not found.")
        sys.exit(1)

    report = A11yResponsiveAuditor.audit(target.read_text(encoding="utf-8", errors="ignore"))
    if args.json:
        print(json.dumps(report, indent=2))
        return

    print(f"\n♿ UI Accessibility & Responsive Audit ({target.name}): Grade {report['grade']} ({report['score']}/100)\n" + "=" * 60)
    if report["issues"]:
        for iss in report["issues"]:
            print(f"  [{iss['severity']}] {iss['code']}: {iss['detail']}")
    else:
        print("  ✓ Zero WCAG A11y or responsive layout violations detected!")
    print("=" * 60 + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Nemr UI Cloner v3.0.0: Design Tokens, Palette & A11y Engine")
    parser.add_argument("--version", action="version", version=VERSION)
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_tok = subparsers.add_parser("clone-tokens", help="Extract colors, fonts, shadows & audit WCAG contrast")
    p_tok.add_argument("file", type=str, help="HTML or CSS file")
    p_tok.add_argument("--contrast", action="store_true", help="Compute WCAG 2.1 contrast audit")
    p_tok.add_argument("--export", type=str, default=None, choices=["css", "tailwind", "flutter"], help="Export theme tokens")
    p_tok.set_defaults(func=cmd_tokens)

    p_tw = subparsers.add_parser("to-tailwind", help="Generate Tailwind CSS component")
    p_tw.add_argument("--kind", type=str, default="card", choices=["card", "hero", "pricing", "navbar", "auth"], help="Component type")
    p_tw.add_argument("--title", type=str, default="Nemr Apex Cloud", help="Component title")
    p_tw.add_argument("--subtitle", type=str, default="Enterprise Cloud Engineering OS", help="Component subtitle")
    p_tw.add_argument("--cta", type=str, default="Get Started", help="CTA label")
    p_tw.set_defaults(func=cmd_tailwind)

    p_fl = subparsers.add_parser("to-flutter", help="Generate Flutter responsive widget")
    p_fl.add_argument("--kind", type=str, default="card", choices=["card", "hero", "pricing", "navbar", "auth"], help="Widget type")
    p_fl.add_argument("--title", type=str, default="Nemr Apex Cloud", help="Widget title")
    p_fl.add_argument("--subtitle", type=str, default="Enterprise Cloud Engineering OS", help="Widget subtitle")
    p_fl.add_argument("--cta", type=str, default="Get Started", help="CTA label")
    p_fl.set_defaults(func=cmd_flutter)

    p_tr = subparsers.add_parser("transpile", help="Transpile raw HTML DOM into Flutter widget or clean Tailwind")
    p_tr.add_argument("html_file", type=str, help="Input HTML file")
    p_tr.add_argument("--target", type=str, default="flutter", choices=["flutter", "tailwind"], help="Target format")
    p_tr.add_argument("--widget-name", type=str, default="ClonedSectionWidget", help="Flutter class name")
    p_tr.add_argument("--out", type=str, default=None, help="Output file path")
    p_tr.set_defaults(func=cmd_transpile)

    p_rtl = subparsers.add_parser("rtl-convert", help="Convert LTR HTML/CSS to Arabic RTL or Logical utilities")
    p_rtl.add_argument("file", type=str, help="Input HTML/CSS file")
    p_rtl.add_argument("--logical", action="store_true", help="Convert to logical ms-/me-/ps-/pe- Tailwind utilities")
    p_rtl.add_argument("--out", type=str, default=None, help="Output file")
    p_rtl.set_defaults(func=cmd_rtl)

    p_pal = subparsers.add_parser("palette", help="Generate 11-stop color scale & harmonies from base hex")
    p_pal.add_argument("hex", type=str, help="Base hex color e.g. #4f46e5")
    p_pal.add_argument("--name", type=str, default="brand", help="Scale token name")
    p_pal.add_argument("--export", type=str, default="css", choices=["css", "tailwind", "flutter", "json"], help="Export format")
    p_pal.set_defaults(func=cmd_palette)

    p_aui = subparsers.add_parser("audit-ui", help="Audit HTML file for A11y & responsive mobile layout bugs")
    p_aui.add_argument("html_file", type=str, help="Input HTML file")
    p_aui.add_argument("--json", action="store_true", help="Emit JSON output")
    p_aui.set_defaults(func=cmd_audit_ui)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
