from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PHONE_PATTERN = re.compile(r"(?<!\d)(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}(?!\d)")
OLD_EMAIL = "christopher.neville.66@gmail.com"


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        if attr_map.get("id"):
            self.ids.add(attr_map["id"] or "")
        for name in ("href", "src"):
            if attr_map.get(name):
                self.links.append((name, attr_map[name] or ""))


def local_target(source: Path, raw: str) -> Path | None:
    parsed = urlparse(raw)
    if parsed.scheme or raw.startswith(("mailto:", "tel:", "data:", "#")):
        return None
    clean = parsed.path
    if not clean:
        return None
    if clean.startswith("/"):
        candidate = ROOT / clean.lstrip("/")
    else:
        candidate = source.parent / clean
    if clean.endswith("/"):
        candidate /= "index.html"
    return candidate


def main() -> int:
    errors: list[str] = []
    html_files = sorted(ROOT.glob("*.html"))
    if not html_files:
        errors.append("No HTML files found")

    for path in html_files:
        text = path.read_text(encoding="utf-8")
        parser = LinkParser()
        parser.feed(text)
        if PHONE_PATTERN.search(text):
            errors.append(f"Phone-number-like text found in {path.name}")
        if OLD_EMAIL.lower() in text.lower():
            errors.append(f"Old email found in {path.name}")
        for _, raw in parser.links:
            target = local_target(path, raw)
            if target is not None and not target.exists():
                errors.append(f"Broken local reference in {path.name}: {raw}")
            if raw.startswith("#") and raw[1:] not in parser.ids:
                errors.append(f"Missing anchor in {path.name}: {raw}")

    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in {".git", "tmp"} for part in path.parts):
            continue
        if path.suffix.lower() not in {".html", ".css", ".js", ".md", ".xml", ".txt", ".json", ".svg"}:
            continue
        text = path.read_text(encoding="utf-8")
        if PHONE_PATTERN.search(text):
            errors.append(f"Phone-number-like text found in {path.relative_to(ROOT)}")
        if OLD_EMAIL.lower() in text.lower():
            errors.append(f"Old email found in {path.relative_to(ROOT)}")

    try:
        json.loads((ROOT / "site.webmanifest").read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"Invalid site.webmanifest: {exc}")

    try:
        ET.parse(ROOT / "sitemap.xml")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"Invalid sitemap.xml: {exc}")

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print(f"Checked {len(html_files)} HTML files; local references and privacy rules pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
