# 🎨 Nemr UI Cloner (استنساخ وتحويل الواجهات برمجياً)

Autonomous design token extractor, multi-target component generator (Tailwind CSS 3.4 & Flutter), and bidirectional Arabic RTL layout adapter.

## 🚀 Capabilities

- **Token Extraction**: Automatically parses hex colors, typography, border radiuses, and shadow elevations from raw HTML/CSS.
- **Tailwind & Flutter Synthesis**: Emits clean responsive components with dark/light mode support.
- **RTL Arabic Mirroring**: Automatically inverts alignments, paddings, and margins for native RTL display.

## 📦 Usage

```bash
python cli.py clone-tokens index.html
python cli.py to-tailwind --title "Apex AI"
python cli.py to-flutter --title "Apex Mobile"
python cli.py rtl-convert page.html
```

## 🧪 Testing

```bash
python -m unittest discover -s tests
```
