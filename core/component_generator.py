"""
Nemr UI Cloner - Multi-Target Component Generator (v2.0.0)
Generates clean Tailwind CSS 3.4+ markup and responsive Flutter Dart widget trees for cards, heroes, pricing, navbars, and auth screens.
"""

from __future__ import annotations


class ComponentGenerator:
    """Generates idiomatic UI components for Tailwind CSS and Flutter."""

    @classmethod
    def generate_tailwind_card(
        cls,
        title: str,
        subtitle: str,
        cta_text: str = "Explore",
        primary_color: str = "indigo-600",
    ) -> str:
        return f"""<div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm hover:shadow-md transition-all duration-200">
  <div class="flex items-center justify-between mb-4">
    <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-{primary_color}/10 text-{primary_color}">
      Featured
    </span>
    <span class="text-xs text-slate-400 font-mono">v2.0</span>
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
        cta_text: str = "Explore",
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

    @classmethod
    def generate_component(
        cls,
        kind: str,
        target: str = "tailwind",
        title: str = "Nemr Cloud",
        subtitle: str = "Enterprise Suite",
        cta_text: str = "Get Started",
    ) -> str:
        k = kind.lower()
        t = target.lower()

        if k == "card":
            return cls.generate_flutter_card(title, subtitle, cta_text) if t == "flutter" else cls.generate_tailwind_card(title, subtitle, cta_text)

        if t == "tailwind":
            templates = {
                "hero": f"""<section class="py-16 px-6 bg-slate-50 dark:bg-slate-950 text-center">
  <div class="max-w-3xl mx-auto">
    <h1 class="text-4xl md:text-5xl font-extrabold text-slate-900 dark:text-white tracking-tight mb-4">{title}</h1>
    <p class="text-lg text-slate-600 dark:text-slate-300 mb-8">{subtitle}</p>
    <a href="#start" class="inline-flex items-center px-6 py-3 rounded-xl font-bold text-white bg-indigo-600 hover:bg-indigo-700 shadow-sm">{cta_text}</a>
  </div>
</section>""",
                "pricing": f"""<div class="max-w-sm bg-white dark:bg-slate-900 border border-indigo-200 dark:border-indigo-900 rounded-2xl p-8 shadow-md">
  <h3 class="text-lg font-bold text-indigo-600 mb-2">{title}</h3>
  <div class="text-4xl font-extrabold text-slate-900 dark:text-white mb-2">$49<span class="text-sm font-medium text-slate-500">/mo</span></div>
  <p class="text-sm text-slate-600 dark:text-slate-400 mb-6">{subtitle}</p>
  <ul class="space-y-2 text-sm text-slate-700 dark:text-slate-300 mb-6">
    <li>✓ Unlimited API Requests</li>
    <li>✓ Zero-Downtime Deployments</li>
  </ul>
  <button class="w-full py-2.5 rounded-xl bg-indigo-600 text-white font-semibold hover:bg-indigo-700">{cta_text}</button>
</div>""",
                "navbar": f"""<header class="sticky top-0 z-40 bg-white/90 dark:bg-slate-900/90 backdrop-blur border-b border-slate-200 dark:border-slate-800">
  <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
    <span class="text-xl font-extrabold text-slate-900 dark:text-white">{title}</span>
    <nav class="hidden md:flex items-center gap-6 text-sm font-semibold text-slate-600 dark:text-slate-300">
      <a href="#features">Features</a>
      <a href="#pricing">Pricing</a>
      <button class="px-4 py-2 rounded-lg bg-indigo-600 text-white">{cta_text}</button>
    </nav>
  </div>
</header>""",
                "auth": f"""<form class="max-w-md mx-auto bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-8 space-y-4">
  <h2 class="text-2xl font-bold text-slate-900 dark:text-white">{title}</h2>
  <p class="text-sm text-slate-500">{subtitle}</p>
  <input type="email" placeholder="Email address" class="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm" />
  <input type="password" placeholder="Password" class="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm" />
  <button type="submit" class="w-full py-2.5 rounded-xl bg-indigo-600 text-white font-bold">{cta_text}</button>
</form>""",
            }
            if k in templates:
                return templates[k]

        if t == "flutter":
            class_map = {
                "hero": "NemrHeroSection",
                "pricing": "NemrPricingCard",
                "navbar": "NemrTopNavBar",
                "auth": "NemrAuthForm",
            }
            if k in class_map:
                cname = class_map[k]
                return f"""import 'package:flutter/material.dart';

class {cname} extends StatelessWidget {{
  const {cname}({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return Container(
      padding: const EdgeInsets.all(24.0),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16.0),
        border: Border.all(color: const Color(0xFFE2E8F0)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          const Text('{title}', style: TextStyle(fontSize: 24.0, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8.0),
          const Text('{subtitle}', style: TextStyle(fontSize: 14.0, color: Color(0xFF64748B))),
          const SizedBox(height: 16.0),
          ElevatedButton(onPressed: () {{}}, child: const Text('{cta_text}')),
        ],
      ),
    );
  }}
}}"""

        raise ValueError(f"Unsupported component kind/target: {kind}/{target}")
