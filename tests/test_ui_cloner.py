#!/usr/bin/env python3
"""Unit tests for Nemr UI Cloner."""

import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from core.css_extractor import CssExtractor
from core.component_generator import ComponentGenerator
from core.rtl_adapter import RtlAdapter


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


if __name__ == "__main__":
    unittest.main()
