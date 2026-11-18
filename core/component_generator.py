"""
Nemr UI Cloner - Multi-Target Component Generator
Generates clean Tailwind CSS markup and responsive Flutter Dart widget trees.
"""

from __future__ import annotations
from typing import Dict, Any


class ComponentGenerator:
    """Generates idiomatic UI components for Tailwind CSS and Flutter."""

    @classmethod
    def generate_tailwind_card(
        cls,
        title: str,
        subtitle: str,
        cta_text: str = "Explore",
        primary_color: str = "indigo-600"
    ) -> str:
        return f"""<div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm hover:shadow-md transition-all duration-200">
  <div class="flex items-center justify-between mb-4">
    <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-{primary_color}/10 text-{primary_color}">
      Featured
    </span>
    <span class="text-xs text-slate-400 font-mono">v1.0</span>
  </div>
  <h3 class="text-xl font-bold text-slate-900 dark:text-white tracking-tight mb-2">
    {title}
  </h3>
  <p class="text-sm text-slate-600 dark:text-slate-400 leading-relaxed mb-6">
    {subtitle}
  </p>
  <button class="w-full inline-flex justify-center items-center px-4 py-2.5 rounded-xl font-semibold text-sm text-white bg-{primary_color} hover:opacity-90 transition-opacity">
    {cta_text}
  </button>
</div>"""

    @classmethod
    def generate_flutter_card(
        cls,
        title: str,
        subtitle: str,
        cta_text: str = "Explore"
    ) -> str:
        return f"""import 'package:flutter/material.dart';

class NemrCardWidget extends StatelessWidget {{
  final String title;
  final String subtitle;
  final String ctaText;
  final VoidCallback? onCtaPressed;

  const NemrCardWidget({{
    super.key,
    this.title = '{title}',
    this.subtitle = '{subtitle}',
    this.ctaText = '{cta_text}',
    this.onCtaPressed,
  }});

  @override
  Widget build(BuildContext context) {{
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Container(
      padding: const EdgeInsets.all(20.0),
      decoration: BoxDecoration(
        color: isDark ? const Color(0xFF0F172A) : Colors.white,
        borderRadius: BorderRadius.circular(16.0),
        border: Border.all(
          color: isDark ? const Color(0xFF1E293B) : const Color(0xFFE2E8F0),
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            blurRadius: 8,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            title,
            style: TextStyle(
              fontSize: 18.0,
              fontWeight: FontWeight.bold,
              color: isDark ? Colors.white : const Color(0xFF0F172A),
            ),
          ),
          const SizedBox(height: 8.0),
          Text(
            subtitle,
            style: TextStyle(
              fontSize: 14.0,
              color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
              height: 1.5,
            ),
          ),
          const SizedBox(height: 16.0),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: onCtaPressed,
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF4F46E5),
                foregroundColor: Colors.white,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12.0),
                ),
                padding: const EdgeInsets.symmetric(vertical: 12.0),
              ),
              child: Text(ctaText, style: const TextStyle(fontWeight: FontWeight.bold)),
            ),
          ),
        ],
      ),
    );
  }}
}}"""
