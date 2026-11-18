---
name: nemr-ui-cloner
description: Autonomous design token extractor, multi-target component generator (Tailwind CSS 3.4 & Flutter), and bidirectional Arabic RTL layout adapter. Use when the user asks to clone UI styling, extract color schemes, convert HTML to Tailwind or Flutter, or adapt web components to Arabic RTL.
---

# Nemr UI Cloner (استنساخ وتحويل الواجهات برمجياً)

Autonomous UI design token extractor, Tailwind CSS & Flutter responsive component generator, and Arabic RTL layout adapter.

## Key Capabilities

1. **Design Token Extractor (`clone-tokens`)**:
   - Analyzes HTML/CSS stylesheets and extracts clean color palettes (hex/rgb), typography families, border radiuses, and shadow elevations.

2. **Multi-Target Component Generator (`to-tailwind`, `to-flutter`)**:
   - Synthesizes production-ready Tailwind CSS 3.4+ glassmorphic and light-mode components.
   - Generates pixel-perfect, responsive Flutter Dart widget trees.

3. **Directional Arabic RTL Adapter (`rtl-convert`)**:
   - Performs single-pass bidirectional mirroring (`text-left` ↔ `text-right`, `ml-` ↔ `mr-`, `pl-` ↔ `pr-`) and injects native Arabic Cairo web typography.

## CLI Quick Reference

```bash
# 1. Extract Design Tokens
python cli.py clone-tokens index.html

# 2. Generate Tailwind Card
python cli.py to-tailwind --title "النمر للمدفوعات" --subtitle "أسرع بوابة دفع ذكية" --cta "ابدأ مجاناً"

# 3. Generate Flutter Widget Tree
python cli.py to-flutter --title "سلطان النمر" --subtitle "منظومة إدارة المشروعات"

# 4. Mirror HTML to Arabic RTL
python cli.py rtl-convert landing.html --out landing_ar.html
```
