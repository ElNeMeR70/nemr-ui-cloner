"""
Nemr UI Cloner - HTML Accessibility (WCAG A11y) & Responsive Audit Engine (v3.0.0)
Scans HTML markup to detect missing alt texts, unlabeled inputs, empty links/buttons, skipped heading levels, and fixed-width overflows.
"""

from __future__ import annotations
from html.parser import HTMLParser
import re
from typing import Any, Dict, List


class _A11yHtmlScanner(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.issues: List[Dict[str, str]] = []
        self.heading_levels: List[int] = []
        self._active_interactive: List[Dict[str, Any]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tl = tag.lower()
        attr_map = {k.lower(): (v or "") for k, v in attrs}

        # 1. Missing img alt
        if tl == "img" and "alt" not in attr_map:
            self.issues.append({
                "severity": "HIGH",
                "code": "A11Y_IMG_ALT_MISSING",
                "detail": f"<img> (src={attr_map.get('src', '')!r}) is missing an alt attribute.",
            })

        # 2. Unlabeled input (ignore hidden/submit/button inputs)
        if tl == "input":
            itype = attr_map.get("type", "text").lower()
            if itype not in ("hidden", "submit", "button", "reset"):
                has_label_hint = any(k in attr_map and attr_map[k].strip() for k in ("aria-label", "aria-labelledby", "placeholder", "id"))
                if not has_label_hint:
                    self.issues.append({
                        "severity": "HIGH",
                        "code": "A11Y_UNLABELED_INPUT",
                        "detail": f"<input type='{itype}'> lacks id, placeholder, or aria-label.",
                    })

        # 3. Track interactive buttons/anchors to detect empty accessible names
        if tl in ("button", "a"):
            self._active_interactive.append({
                "tag": tl,
                "has_aria": bool(attr_map.get("aria-label", "").strip() or attr_map.get("title", "").strip()),
                "text": "",
            })

        # 4. Track heading hierarchy (h1..h6)
        if tl in ("h1", "h2", "h3", "h4", "h5", "h6"):
            lvl = int(tl[1])
            if self.heading_levels and lvl > self.heading_levels[-1] + 1:
                self.issues.append({
                    "severity": "MEDIUM",
                    "code": "A11Y_HEADING_SKIP",
                    "detail": f"Heading jumped from <h{self.heading_levels[-1]}> directly to <{tl}>.",
                })
            self.heading_levels.append(lvl)

        # 5. Fixed pixel width >= 500px causing mobile horizontal overflow
        style_val = attr_map.get("style", "")
        cls_val = attr_map.get("class", "")
        m_style_w = re.search(r"(?:^|;)\s*width\s*:\s*(\d+)px", style_val, re.IGNORECASE)
        if m_style_w and int(m_style_w.group(1)) >= 500 and "max-width" not in style_val.lower():
            self.issues.append({
                "severity": "MEDIUM",
                "code": "RESPONSIVE_FIXED_WIDTH",
                "detail": f"<{tl}> sets fixed `width: {m_style_w.group(1)}px` without max-width, risking mobile overflow.",
            })
        m_tw_w = re.search(r"\bw-\[(\d+)px\]", cls_val)
        if m_tw_w and int(m_tw_w.group(1)) >= 500 and "max-w-" not in cls_val:
            self.issues.append({
                "severity": "MEDIUM",
                "code": "RESPONSIVE_FIXED_WIDTH",
                "detail": f"<{tl}> uses fixed Tailwind `w-[{m_tw_w.group(1)}px]` without `max-w-*`.",
            })

    def handle_data(self, data: str) -> None:
        if self._active_interactive:
            self._active_interactive[-1]["text"] += data.strip()

    def handle_endtag(self, tag: str) -> None:
        tl = tag.lower()
        if tl in ("button", "a") and self._active_interactive:
            for idx in range(len(self._active_interactive) - 1, -1, -1):
                if self._active_interactive[idx]["tag"] == tl:
                    item = self._active_interactive.pop(idx)
                    if not item["has_aria"] and not item["text"]:
                        self.issues.append({
                            "severity": "HIGH",
                            "code": "A11Y_EMPTY_BUTTON_OR_LINK",
                            "detail": f"<{tl}> has neither visible text nor aria-label.",
                        })
                    break


class A11yResponsiveAuditor:
    """Audits HTML templates for WCAG 2.1 accessibility and responsive layout defects."""

    @classmethod
    def audit(cls, html: str) -> Dict[str, Any]:
        scanner = _A11yHtmlScanner()
        scanner.feed(html)
        scanner.close()

        penalty = 0
        for iss in scanner.issues:
            penalty += 20 if iss["severity"] == "HIGH" else 10

        score = max(0, 100 - penalty)
        if score >= 95:
            grade = "A+"
        elif score >= 85:
            grade = "A"
        elif score >= 70:
            grade = "B"
        elif score >= 50:
            grade = "C"
        else:
            grade = "F"

        return {
            "score": score,
            "grade": grade,
            "issues_count": len(scanner.issues),
            "issues": scanner.issues,
        }
