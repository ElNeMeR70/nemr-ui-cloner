"""
Nemr UI Cloner - HTML DOM Transpiler (v2.0.0)
Parses HTML markup into a lightweight DOM AST and transpiles into Flutter Dart widget trees or clean Tailwind HTML.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from html import escape
from html.parser import HTMLParser
from typing import Dict, List


@dataclass
class DomNode:
    tag: str
    attrs: Dict[str, str] = field(default_factory=dict)
    text: str = ""
    children: List["DomNode"] = field(default_factory=list)


class _AstParser(HTMLParser):
    VOID_TAGS = {"img", "input", "br", "hr", "meta", "link"}

    def __init__(self) -> None:
        super().__init__()
        self.root = DomNode(tag="root")
        self.stack: List[DomNode] = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_dict = {k: (v or "") for k, v in attrs}
        node = DomNode(tag=tag.lower(), attrs=attr_dict)
        self.stack[-1].children.append(node)
        if tag.lower() not in self.VOID_TAGS:
            self.stack.append(node)

    def handle_endtag(self, tag: str) -> None:
        lower = tag.lower()
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == lower:
                del self.stack[i:]
                break

    def handle_data(self, data: str) -> None:
        stripped = " ".join(data.split())
        if stripped:
            if self.stack[-1].text:
                self.stack[-1].text += " " + stripped
            else:
                self.stack[-1].text = stripped


class DomTranspiler:
    """Transpiles real HTML DOM trees into Flutter widgets or clean semantic Tailwind HTML."""

    HEADING_SIZES = {"h1": 28.0, "h2": 22.0, "h3": 18.0, "h4": 16.0, "h5": 14.0, "h6": 13.0}
    SKIP_TAGS = {"script", "style", "meta", "link", "noscript"}
    STRIP_ATTRS_PREFIX = ("on", "data-v-", "data-reactid")

    @classmethod
    def parse_html(cls, html: str) -> DomNode:
        parser = _AstParser()
        parser.feed(html)
        parser.close()
        return parser.root

    @classmethod
    def _render_flutter_node(cls, node: DomNode, indent: int = 2) -> List[str]:
        pad = " " * indent
        tag = node.tag

        if tag in cls.SKIP_TAGS:
            return []

        if tag in cls.HEADING_SIZES:
            size = cls.HEADING_SIZES[tag]
            txt = node.text.replace("'", "\\'")
            return [
                f"{pad}Text('{txt}', style: const TextStyle(fontSize: {size}, fontWeight: FontWeight.bold)),"
            ]

        if tag in ("p", "span", "label", "li"):
            txt = (node.text or cls._collect_text(node)).replace("'", "\\'")
            if not txt:
                return []
            return [f"{pad}Text('{txt}', style: const TextStyle(fontSize: 14.0)),"]

        if tag == "button" or (tag == "a" and "btn" in node.attrs.get("class", "").lower()):
            txt = (node.text or cls._collect_text(node) or "Action").replace("'", "\\'")
            return [
                f"{pad}ElevatedButton(",
                f"{pad}  onPressed: () {{}},",
                f"{pad}  child: const Text('{txt}'),",
                f"{pad}),",
            ]

        if tag == "a":
            txt = (node.text or cls._collect_text(node) or "Link").replace("'", "\\'")
            return [f"{pad}TextButton(onPressed: () {{}}, child: const Text('{txt}')),"]

        if tag == "input":
            placeholder = node.attrs.get("placeholder", "Enter value").replace("'", "\\'")
            return [
                f"{pad}TextField(",
                f"{pad}  decoration: const InputDecoration(hintText: '{placeholder}', border: OutlineInputBorder()),",
                f"{pad}),",
            ]

        if tag == "img":
            src = node.attrs.get("src", "").replace("'", "\\'")
            return [f"{pad}Image.network('{src}', fit: BoxFit.cover),"]

        # Container / layout node
        child_lines: List[str] = []
        if node.text:
            txt = node.text.replace("'", "\\'")
            child_lines.append(f"{pad}    Text('{txt}'),")
        for ch in node.children:
            child_lines.extend(cls._render_flutter_node(ch, indent + 4))

        if not child_lines:
            return []

        cls_attr = node.attrs.get("class", "").lower()
        layout_widget = "Row" if ("flex-row" in cls_attr or tag == "nav") else "Column"
        lines = [
            f"{pad}Container(",
            f"{pad}  padding: const EdgeInsets.all(12.0),",
            f"{pad}  child: {layout_widget}(",
            f"{pad}    crossAxisAlignment: CrossAxisAlignment.start,",
            f"{pad}    children: [",
            *child_lines,
            f"{pad}    ],",
            f"{pad}  ),",
            f"{pad}),",
        ]
        return lines

    @classmethod
    def _collect_text(cls, node: DomNode) -> str:
        parts = [node.text] if node.text else []
        for ch in node.children:
            sub = cls._collect_text(ch)
            if sub:
                parts.append(sub)
        return " ".join(parts).strip()

    @classmethod
    def to_flutter_widget(cls, html: str, widget_name: str = "ClonedSectionWidget") -> str:
        ast_root = cls.parse_html(html)
        body_nodes = [n for n in ast_root.children if n.tag not in cls.SKIP_TAGS]
        rendered: List[str] = []
        for node in body_nodes:
            rendered.extend(cls._render_flutter_node(node, indent=8))

        if not rendered:
            rendered = ["        const SizedBox.shrink(),"]

        return f"""import 'package:flutter/material.dart';

class {widget_name} extends StatelessWidget {{
  const {widget_name}({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
{chr(10).join(rendered)}
      ],
    );
  }}
}}
"""

    @classmethod
    def _render_tailwind_node(cls, node: DomNode, indent: int = 0) -> List[str]:
        if node.tag in cls.SKIP_TAGS:
            return []

        pad = "  " * indent
        default_classes = {
            "h1": "text-3xl font-bold text-slate-900 dark:text-white tracking-tight",
            "h2": "text-2xl font-bold text-slate-800 dark:text-slate-100",
            "h3": "text-lg font-semibold text-slate-800 dark:text-slate-100",
            "p": "text-sm text-slate-600 dark:text-slate-300 leading-relaxed",
            "button": "px-4 py-2 rounded-xl font-semibold text-sm text-white bg-indigo-600 hover:bg-indigo-700",
            "input": "w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500",
            "a": "text-indigo-600 hover:underline font-medium",
        }

        clean_attrs: Dict[str, str] = {}
        for k, v in node.attrs.items():
            kl = k.lower()
            if kl == "style" or any(kl.startswith(p) for p in cls.STRIP_ATTRS_PREFIX):
                continue
            clean_attrs[k] = v

        if node.tag in default_classes:
            existing_cls = clean_attrs.get("class", "").strip()
            clean_attrs["class"] = f"{existing_cls} {default_classes[node.tag]}".strip()

        attr_str = "".join(f' {k}="{escape(v, quote=True)}"' for k, v in clean_attrs.items())
        if node.tag in _AstParser.VOID_TAGS:
            return [f"{pad}<{node.tag}{attr_str} />"]

        if not node.children:
            return [f"{pad}<{node.tag}{attr_str}>{escape(node.text)}</{node.tag}>"]

        lines = [f"{pad}<{node.tag}{attr_str}>"]
        if node.text:
            lines.append(f"{pad}  {escape(node.text)}")
        for ch in node.children:
            lines.extend(cls._render_tailwind_node(ch, indent + 1))
        lines.append(f"{pad}</{node.tag}>")
        return lines

    @classmethod
    def to_clean_tailwind(cls, html: str) -> str:
        ast_root = cls.parse_html(html)
        lines: List[str] = []
        for node in ast_root.children:
            lines.extend(cls._render_tailwind_node(node, indent=0))
        return "\n".join(lines)
