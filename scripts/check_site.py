#!/usr/bin/env python3
"""Check structure, provenance, and local links in the generated site."""

from __future__ import annotations

from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys
import xml.etree.ElementTree as ElementTree

from site_contract import (
    FIGURE_FILES,
    FIGURE_MANIFEST,
    FIGURE_SOURCE_ROOT,
    FONT_FILES,
    FONT_LICENSES,
    GUIDES,
    GUIDES_ROOT,
    LANG,
    PUBLISHED_FIGURES_ROOT,
    PUBLISHED_SOURCES,
    READINGS,
    READINGS_ROOT,
    SITE_SUBTITLE,
    SITE_TITLE,
    SITE_ROOT,
    read_provenance,
)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.references: list[str] = []
        self.image_alt: list[str | None] = []
        self.figure_count = 0
        self.figcaption_count = 0
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
        if tag == "figure":
            self.figure_count += 1
        if tag == "figcaption":
            self.figcaption_count += 1
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
    referenced_figures: set[Path] = set()

    for path, page in pages.items():
        relative = path.relative_to(SITE_ROOT)
        if not page.has_language:
            failures.append(f'{relative}: missing lang="{LANG}"')
        if not page.has_main:
            failures.append(f"{relative}: missing main landmark")
        if not page.title.strip():
            failures.append(f"{relative}: missing title")
        elif SITE_TITLE not in page.title:
            failures.append(f"{relative}: page title does not name the site")
        page_source = path.read_text(encoding="utf-8")
        if any(ord(character) < 32 and character not in "\n\r\t" for character in page_source):
            failures.append(f"{relative}: unexpected control character")
        if "typeface-switcher.js" not in page_source:
            failures.append(f"{relative}: missing typeface preference script")
        if "data-typeface-picker" not in page_source:
            failures.append(f"{relative}: missing typeface selector")
        if SITE_SUBTITLE not in page_source:
            failures.append(f"{relative}: missing site subtitle")
        if len(page.ids) != len(set(page.ids)):
            failures.append(f"{relative}: duplicate id")
        if any(alt is None or not alt.strip() for alt in page.image_alt):
            failures.append(f"{relative}: image without useful alt text")
        if page.figure_count != page.figcaption_count:
            failures.append(f"{relative}: every figure must have one caption")
        for reference in page.references:
            parsed_reference = urlsplit(reference)
            if (
                not parsed_reference.scheme
                and not parsed_reference.netloc
                and "sources" in Path(parsed_reference.path).parts
                and Path(parsed_reference.path).suffix.lower() == ".md"
            ):
                failures.append(f"{relative}: links to published Markdown source")
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
            if target.exists() and target.suffix.lower() == ".svg":
                try:
                    target.relative_to(PUBLISHED_FIGURES_ROOT)
                except ValueError:
                    pass
                else:
                    referenced_figures.add(target)

    for label, items, root in (
        ("guide", GUIDES, GUIDES_ROOT),
        ("reading", READINGS, READINGS_ROOT),
    ):
        expected_slugs = {item.slug for item in items}
        actual_slugs = {path.parent.name for path in root.glob("*/index.html")}
        if actual_slugs != expected_slugs:
            failures.append(f"published {label} directories do not match the contract")

    for items, root, prefix in (
        (GUIDES, GUIDES_ROOT, "guides"),
        (READINGS, READINGS_ROOT, "readings"),
    ):
        for item in items:
            page_path = root / item.slug / "index.html"
            page_source = page_path.read_text(encoding="utf-8")
            source_name, observed_digest = read_provenance(page_source)
            source_path = PUBLISHED_SOURCES / item.source
            expected_digest = sha256(source_path.read_bytes()).hexdigest()
            if source_name != item.source or observed_digest != expected_digest:
                failures.append(
                    f"{prefix}/{item.slug}/: stale or missing source provenance"
                )

            check_count = len(re.findall(r"<form\b[^>]*data-quick-check", page_source))
            for marker in (
                "<fieldset",
                "<legend",
                "quick-check-explanation",
                "data-answer=",
            ):
                if page_source.count(marker) != check_count:
                    failures.append(
                        f"{prefix}/{item.slug}/: {marker} count does not match quick checks"
                    )
            if check_count and "quick-checks.js" not in page_source:
                failures.append(f"{prefix}/{item.slug}/: checks lack enhancement script")

    expected_sources = {item.source for item in (*GUIDES, *READINGS)}
    actual_sources = {path.name for path in PUBLISHED_SOURCES.glob("*.md")}
    if actual_sources != expected_sources:
        failures.append("published Markdown sources do not match the contract")

    fonts_root = SITE_ROOT / "assets" / "fonts"
    actual_fonts = {path.name for path in fonts_root.glob("*.woff2")}
    if actual_fonts != set(FONT_FILES):
        failures.append("published font files do not match the contract")
    for font_name in FONT_FILES:
        if (fonts_root / font_name).read_bytes()[:4] != b"wOF2":
            failures.append(f"assets/fonts/{font_name}: not a WOFF2 font")

    licences_root = fonts_root / "licenses"
    actual_licences = {path.name for path in licences_root.glob("*.txt")}
    if actual_licences != set(FONT_LICENSES):
        failures.append("published font licences do not match the contract")
    for licence_name in FONT_LICENSES:
        licence = (licences_root / licence_name).read_text(encoding="utf-8")
        if "SIL OPEN FONT LICENSE Version 1.1" not in licence:
            failures.append(f"assets/fonts/licenses/{licence_name}: invalid licence")

    stylesheet = SITE_ROOT / "assets" / "css" / "site.css"
    for font_name in FONT_FILES:
        if f'../fonts/{font_name}' not in stylesheet.read_text(encoding="utf-8"):
            failures.append(f"assets/css/site.css: does not declare {font_name}")

    expected_figures = set(FIGURE_FILES)
    source_figures = {
        path.relative_to(FIGURE_SOURCE_ROOT).as_posix()
        for path in FIGURE_SOURCE_ROOT.rglob("*.svg")
    }
    published_figures = {
        path.relative_to(PUBLISHED_FIGURES_ROOT).as_posix()
        for path in PUBLISHED_FIGURES_ROOT.rglob("*.svg")
    }
    if source_figures != expected_figures:
        failures.append("editable figure sources do not match the contract")
    if published_figures != expected_figures:
        failures.append("published figures do not match the contract")

    for figure_name in FIGURE_FILES:
        source_figure = FIGURE_SOURCE_ROOT / figure_name
        published_figure = PUBLISHED_FIGURES_ROOT / figure_name
        if not source_figure.exists() or not published_figure.exists():
            continue
        if source_figure.read_bytes() != published_figure.read_bytes():
            failures.append(f"assets/figures/{figure_name}: stale rendered figure")
        try:
            root = ElementTree.parse(source_figure).getroot()
        except ElementTree.ParseError as error:
            failures.append(f"assets/diagrams/source/{figure_name}: invalid SVG: {error}")
            continue
        namespace = "{http://www.w3.org/2000/svg}"
        title = root.find(f"{namespace}title")
        description = root.find(f"{namespace}desc")
        if root.tag != f"{namespace}svg" or not root.get("viewBox"):
            failures.append(f"assets/diagrams/source/{figure_name}: missing SVG viewBox")
        if title is None or not "".join(title.itertext()).strip():
            failures.append(f"assets/diagrams/source/{figure_name}: missing title")
        if description is None or not "".join(description.itertext()).strip():
            failures.append(f"assets/diagrams/source/{figure_name}: missing description")
        if root.get("role") != "img" or not root.get("aria-labelledby"):
            failures.append(f"assets/diagrams/source/{figure_name}: missing image semantics")

    expected_figure_targets = {
        (PUBLISHED_FIGURES_ROOT / figure_name).resolve()
        for figure_name in FIGURE_FILES
    }
    if referenced_figures != expected_figure_targets:
        failures.append("published figures are not each referenced by the site")

    if not FIGURE_MANIFEST.exists():
        failures.append("assets/manifest.yml: missing figure metadata")
    else:
        manifest = FIGURE_MANIFEST.read_text(encoding="utf-8")
        for figure_name in FIGURE_FILES:
            for declared_path in (
                f"assets/diagrams/source/{figure_name}",
                f"site/assets/figures/{figure_name}",
            ):
                if declared_path not in manifest:
                    failures.append(
                        f"assets/manifest.yml: missing metadata for {declared_path}"
                    )

    if failures:
        print("\n".join(failures), file=sys.stderr)
        raise SystemExit(1)
    print(
        f"Checked {len(html_files)} HTML pages: local links, fragments, landmarks, "
        f"{len(expected_sources)} source digests, {len(FONT_FILES)} self-hosted fonts, "
        f"{len(FIGURE_FILES)} accessible figures, and all client-side checks are valid."
    )


if __name__ == "__main__":
    main()
