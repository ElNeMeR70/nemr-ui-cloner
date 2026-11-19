---
name: nemr-ui-cloner
description: Autonomous UI engineering & design-system suite v3.0.0: 11-stop algorithmic color palette & harmony synthesizer, WCAG 2.1 contrast & HTML Accessibility/Responsive auditor, CSS/Tailwind/Flutter theme exporter, HTML DOM AST transpiler to Flutter widgets & clean Tailwind, multi-pattern component synthesizer, and RTL + CSS logical layout adapter. Use when building color palettes, auditing accessibility, extracting tokens, transpiling HTML, or adapting RTL UIs.
---

# Nemr UI Cloner v3.0.0 (استنساخ الواجهات وتوليد الألوان وفحص التوافقية)

Autonomous 11-stop palette synthesizer, HTML accessibility/responsive auditor, WCAG contrast checker, HTML-to-Flutter/Tailwind AST transpiler, component generator, and CSS-logical/RTL layout adapter.

## Key Capabilities

1. **11-Stop Palette & Harmony Synthesizer (`palette`)**:
   - Generates Tailwind-grade `50`–`950` shade ramps via HLS color space, computes complementary/analogous/triadic harmonies, pairs WCAG-safe foreground colors, and exports CSS, Tailwind, Flutter, or JSON.
2. **HTML Accessibility & Responsive Auditor (`audit-ui`)**:
   - Audits HTML markup for missing `alt` text, empty buttons/links, unlabeled inputs, skipped heading hierarchy (`h1` -> `h4`), and hardcoded pixel widths (`>=500px`), scoring `A+`–`F`.
3. **Token Extraction, WCAG Audit & Theme Export (`clone-tokens`)**:
   - Extracts colors, fonts, radiuses, and shadows; checks `AA`/`AAA` contrast; exports theme variables.
4. **DOM AST Transpiler & Component Generator (`transpile`, `to-tailwind`, `to-flutter`)**:
   - Converts real HTML sections into Flutter widget trees or stripped Tailwind HTML, and generates `card`/`hero`/`pricing`/`navbar`/`auth` templates.
5. **RTL Mirroring & CSS Logical Utilities (`rtl-convert`)**:
   - Mirrors Tailwind & raw CSS properties or upgrades physical spacing to logical `ms-`/`me-`/`ps-`/`pe-`/`text-start`.

## CLI Quick Reference

```bash
python cli.py --version
python cli.py palette "#4f46e5" --name brand --export tailwind
python cli.py audit-ui landing.html --json
python cli.py clone-tokens styles.css --contrast --export flutter
python cli.py transpile landing.html --target flutter --widget-name LandingHero --out hero.dart
python cli.py rtl-convert page.html --logical
```
