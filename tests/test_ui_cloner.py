#!/usr/bin/env python3
"""Unit tests for Nemr UI Cloner v2.0.0."""

import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from core.css_extractor import CssExtractor
from core.component_generator import ComponentGenerator
from core.dom_transpiler import DomTranspiler
from core.rtl_adapter import RtlAdapter
from core.palette_synthesizer import PaletteSynthesizer
from core.a11y_auditor import A11yResponsiveAuditor


class TestUiCloner(unittest.TestCase):
    def test_css_extractor(self):
        sample_css = """
        body { font-family: 'Plus Jakarta Sans', sans-serif; background: #0f172a; }
        .card { border-radius: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: #ffffff; }
        """
        tokens = CssExtractor.extract_tokens(sample_css)
        self.assertIn("#0f172a", tokens.colors)
        self.assertIn("#ffffff", tokens.colors)
        self.assertIn("Plus Jakarta Sans", tokens.fonts)
        self.assertIn("16px", tokens.border_radiuses)

    def test_tailwind_component_generator(self):
        tw = ComponentGenerator.generate_tailwind_card("Apex Pro", "Cloud Developer Suite")
        self.assertIn("Apex Pro", tw)
        self.assertIn("bg-white dark:bg-slate-900", tw)
        self.assertIn("rounded-2xl", tw)

    def test_flutter_component_generator(self):
        fl = ComponentGenerator.generate_flutter_card("Mobile Pro", "Flutter Widget")
        self.assertIn("class NemrCardWidget extends StatelessWidget", fl)
        self.assertIn("Mobile Pro", fl)
        self.assertIn("BorderRadius.circular(16.0)", fl)

    def test_rtl_adapter(self):
        ltr_html = '<html lang="en"><head></head><body><div class="ml-4 text-left pr-6">Hello</div></body></html>'
        rtl_html = RtlAdapter.convert_to_rtl(ltr_html)
        self.assertIn('dir="rtl"', rtl_html)
        self.assertIn("mr-4", rtl_html)
        self.assertIn("text-right", rtl_html)
        self.assertIn("pl-6", rtl_html)
        self.assertIn("Cairo", rtl_html)

    # v2.0.0 Tests
    def test_wcag_contrast_ratio(self):
        self.assertEqual(CssExtractor.compute_contrast_ratio("#000000", "#ffffff"), 21.0)
        audit = CssExtractor.audit_contrast({"#0f172a", "#4f46e5"})
        self.assertEqual(len(audit), 2)
        dark_entry = [a for a in audit if a["color"] == "#0f172a"][0]
        self.assertEqual(dark_entry["wcag_rating"], "AAA")

    def test_export_theme_targets(self):
        tokens = CssExtractor.extract_tokens("body { font-family: 'Cairo', sans-serif; color: #4f46e5; border-radius: 12px; }")
        css_out = CssExtractor.export_theme(tokens, target="css")
        self.assertIn("--color-primary:", css_out)
        tw_out = CssExtractor.export_theme(tokens, target="tailwind")
        self.assertIn("module.exports =", tw_out)
        fl_out = CssExtractor.export_theme(tokens, target="flutter")
        self.assertIn("class NemrThemeTokens", fl_out)

    def test_dom_transpiler(self):
        html = '<section onclick="track()"><h1>Nemr OS</h1><p>Fast Engine</p><input placeholder="Email" /><button>Launch</button></section>'
        fl = DomTranspiler.to_flutter_widget(html, widget_name="HeroBox")
        self.assertIn("class HeroBox extends StatelessWidget", fl)
        self.assertIn("Text('Nemr OS'", fl)
        self.assertIn("ElevatedButton(", fl)
        self.assertIn("TextField(", fl)

        tw = DomTranspiler.to_clean_tailwind(html)
        self.assertNotIn("onclick", tw)
        self.assertIn("text-3xl font-bold", tw)

    def test_component_generator_kinds(self):
        hero_tw = ComponentGenerator.generate_component("hero", target="tailwind", title="Launch Fast")
        self.assertIn("<section", hero_tw)
        self.assertIn("Launch Fast", hero_tw)
        pricing_fl = ComponentGenerator.generate_component("pricing", target="flutter", title="Pro Plan")
        self.assertIn("class NemrPricingCard", pricing_fl)

    def test_rtl_logical_and_css_mirroring(self):
        css = ".box { margin-left: 16px; padding-right: 8px; text-align: left; }"
        mirrored = RtlAdapter.convert_to_rtl(css, inject_arabic_font=False)
        self.assertIn("margin-right: 16px;", mirrored)
        self.assertIn("padding-left: 8px;", mirrored)
        self.assertIn("text-align: right;", mirrored)

        logical = RtlAdapter.convert_to_logical('<div class="ml-4 pr-2 text-left rounded-l-lg"></div>')
        self.assertIn("ms-4", logical)
        self.assertIn("pe-2", logical)
        self.assertIn("text-start", logical)
        self.assertIn("rounded-s-lg", logical)

    # v3.0.0 Tests
    def test_palette_synthesizer_scale_and_harmonies(self):
        pal = PaletteSynthesizer.generate_scale("#4f46e5", name="indigo")
        self.assertEqual(len(pal["stops"]), 11)
        self.assertIn("50", pal["stops"])
        self.assertIn("950", pal["stops"])
        self.assertIn("complementary", pal["harmonies"])
        css = PaletteSynthesizer.export_scale(pal, target="css")
        self.assertIn("--indigo-500:", css)
        fl = PaletteSynthesizer.export_scale(pal, target="flutter")
        self.assertIn("class IndigoPalette", fl)

    def test_a11y_auditor_catches_violations(self):
        bad_html = '<div style="width: 800px"><h1>Title</h1><h4>Skipped</h4><img src="x.png"><button></button><input type="text"></div>'
        rep = A11yResponsiveAuditor.audit(bad_html)
        codes = {i["code"] for i in rep["issues"]}
        self.assertIn("A11Y_IMG_ALT_MISSING", codes)
        self.assertIn("A11Y_EMPTY_BUTTON_OR_LINK", codes)
        self.assertIn("A11Y_UNLABELED_INPUT", codes)
        self.assertIn("A11Y_HEADING_SKIP", codes)
        self.assertIn("RESPONSIVE_FIXED_WIDTH", codes)
        self.assertLess(rep["score"], 60)

    def test_a11y_auditor_clean_markup(self):
        good_html = '<main class="max-w-xl"><h1>Hello</h1><h2>Sub</h2><img src="x.png" alt="Logo"><input type="email" aria-label="Email"><button>Submit</button></main>'
        rep = A11yResponsiveAuditor.audit(good_html)
        self.assertEqual(rep["score"], 100)
        self.assertEqual(rep["grade"], "A+")
        self.assertEqual(rep["issues_count"], 0)


if __name__ == "__main__":
    unittest.main()
