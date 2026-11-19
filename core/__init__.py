"""Nemr UI Cloner Core Package (v3.0.0)."""

__version__ = "3.0.0"

from core.css_extractor import CssExtractor, DesignTokens
from core.component_generator import ComponentGenerator
from core.dom_transpiler import DomTranspiler, DomNode
from core.rtl_adapter import RtlAdapter
from core.palette_synthesizer import PaletteSynthesizer
from core.a11y_auditor import A11yResponsiveAuditor

__all__ = [
    "__version__",
    "CssExtractor",
    "DesignTokens",
    "ComponentGenerator",
    "DomTranspiler",
    "DomNode",
    "RtlAdapter",
    "PaletteSynthesizer",
    "A11yResponsiveAuditor",
]
