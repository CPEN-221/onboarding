#!/usr/bin/env python3
"""Check structure, provenance, and local links in the generated site."""

from __future__ import annotations

from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys

from site_contract import (
    LANG,
    PUBLISHED_SOURCES,
    READINGS,
    READINGS_ROOT,
    SITE_ROOT,
    read_provenance,
)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.references: list[str] = []
        self.image_alt: list[str | None] = []
        self.has_language = False
        self.has_main = False
        self.in_title = False
        self.title = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "html" and attributes.get("lang", "").lower() == LANG.lower():
            self.has_language = True
        if tag == "main":
            self.has_main = True
        if tag == "title":
            self.in_title = True
        if "id" in attributes and attributes["id"] is not None:
            self.ids.append(attributes["id"] or "")
        if tag == "img":
            self.image_alt.append(attributes.get("alt"))
        for name in ("href", "src"):
            if attributes.get(name):
                self.references.append(attributes[name] or "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data


def parse(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return parser


def local_target(source: Path, reference: str) -> tuple[Path | None, str]:
    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc:
        return None, ""
    if parsed.path.startswith("/"):
        raise ValueError("root-relative URLs break project Pages sites")
    target = source if not parsed.path else (source.parent / unquote(parsed.path)).resolve()
    try:
        target.relative_to(SITE_ROOT)
    except ValueError as error:
        raise ValueError("URL leaves the site directory") from error
    if parsed.path.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target, unquote(parsed.fragment)


def main() -> None:
    failures: list[str] = []
    html_files = sorted(SITE_ROOT.rglob("*.html"))
    pages = {path: parse(path) for path in html_files}

    for path, page in pages.items():
        relative = path.relative_to(SITE_ROOT)
        if not page.has_language:
            failures.append(f'{relative}: missing lang="{LANG}"')
        if not page.has_main:
            failures.append(f"{relative}: missing main landmark")
        if not page.title.strip():
            failures.append(f"{relative}: missing title")
        page_source = path.read_text(encoding="utf-8")
        if any(ord(character) < 32 and character not in "\n\r\t" for character in page_source):
            failures.append(f"{relative}: unexpected control character")
        if len(page.ids) != len(set(page.ids)):
            failures.append(f"{relative}: duplicate id")
        if any(alt is None or not alt.strip() for alt in page.image_alt):
            failures.append(f"{relative}: image without useful alt text")
        for reference in page.references:
            try:
                target, fragment = local_target(path, reference)
            except ValueError as error:
                failures.append(f"{relative}: {reference}: {error}")
                continue
            if target is None:
                continue
            if not target.exists():
                failures.append(f"{relative}: missing target for {reference}")
            elif fragment and target.suffix == ".html":
                target_page = pages.get(target) or parse(target)
                if fragment not in target_page.ids:
                    failures.append(f"{relative}: missing fragment {reference}")

    expected_slugs = {reading.slug for reading in READINGS}
    actual_slugs = {path.parent.name for path in READINGS_ROOT.glob("*/index.html")}
    if actual_slugs != expected_slugs:
        failures.append("published reading directories do not match the contract")

    for reading in READINGS:
        page_path = READINGS_ROOT / reading.slug / "index.html"
        page_source = page_path.read_text(encoding="utf-8")
        source_name, observed_digest = read_provenance(page_source)
        source_path = PUBLISHED_SOURCES / reading.source
        expected_digest = sha256(source_path.read_bytes()).hexdigest()
        if source_name != reading.source or observed_digest != expected_digest:
            failures.append(f"readings/{reading.slug}/: stale or missing source provenance")

        check_count = len(re.findall(r"<form\b[^>]*data-quick-check", page_source))
        for marker in ("<fieldset", "<legend", "quick-check-explanation", "data-answer="):
            if page_source.count(marker) != check_count:
                failures.append(
                    f"readings/{reading.slug}/: {marker} count does not match quick checks"
                )
        if check_count and "quick-checks.js" not in page_source:
            failures.append(f"readings/{reading.slug}/: checks lack enhancement script")

    expected_sources = {reading.source for reading in READINGS}
    actual_sources = {path.name for path in PUBLISHED_SOURCES.glob("*.md")}
    if actual_sources != expected_sources:
        failures.append("published Markdown sources do not match the contract")

    if failures:
        print("\n".join(failures), file=sys.stderr)
        raise SystemExit(1)
    print(
        f"Checked {len(html_files)} HTML pages: local links, fragments, landmarks, "
        f"three source digests, and all client-side checks are valid."
    )


if __name__ == "__main__":
    main()
