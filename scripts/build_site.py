#!/usr/bin/env python3
"""Render the standalone Java onboarding readings as a static Pages site."""

from __future__ import annotations

from hashlib import sha256
from html import escape
from pathlib import Path
import re
import shutil
import subprocess

from site_contract import (
    EXAMPLES_ROOT,
    FIGURE_FILES,
    FIGURE_SOURCE_ROOT,
    GUIDES,
    GUIDES_ROOT,
    LANG,
    NOTES_ROOT,
    PANDOC_ARGUMENTS,
    PANDOC_VERSION,
    PUBLISHED_FIGURES_ROOT,
    PUBLISHED_SOURCES,
    READINGS,
    READINGS_ROOT,
    SITE_SUBTITLE,
    SITE_TITLE,
    SITE_ROOT,
    Guide,
    Reading,
    installed_pandoc_version,
    provenance_comments,
)


def require_pandoc() -> None:
    observed = installed_pandoc_version()
    if observed != PANDOC_VERSION:
        raise SystemExit(
            f"This site requires pandoc {PANDOC_VERSION}; found {observed}."
        )


def render_markdown(markdown: str) -> str:
    try:
        result = subprocess.run(
            ["pandoc", *PANDOC_ARGUMENTS],
            input=markdown,
            text=True,
            capture_output=True,
            check=True,
        )
    except FileNotFoundError as error:
        raise SystemExit(f"pandoc {PANDOC_VERSION} is required") from error
    except subprocess.CalledProcessError as error:
        raise SystemExit(error.stderr) from error
    return result.stdout.strip()


def transform_body(
    body: str, item_number: int
) -> tuple[str, list[tuple[str, str, str]]]:
    body = re.sub(
        r"(<pre(?:\s+class=\"[^\"]+\")?><code>.*?</code></pre>)",
        r'<div class="code-block">\1</div>',
        body,
        flags=re.DOTALL,
    )
    body = re.sub(
        r"<blockquote>\s*(<p><strong>Design principle:)",
        r'<blockquote class="design-note">\1',
        body,
    )
    body = re.sub(
        r"<p>By the end(?: of this reading)?, you should be able to:</p>\n(<ul>.*?</ul>)",
        lambda match: (
            '<section class="learning-outcomes" aria-labelledby="learning-outcomes">'
            '<h2 id="learning-outcomes">Learning outcomes</h2>'
            f"{match.group(1)}</section>"
        ),
        body,
        count=1,
        flags=re.DOTALL,
    )

    sections: list[tuple[str, str, str]] = []

    def link_heading(match: re.Match[str]) -> str:
        level, identifier, contents = match.groups()
        visible = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", contents)).strip()
        local_number = ""
        numeric = re.match(r"^(\d+)\.\s+(.*)$", visible)
        if numeric:
            local_number = numeric.group(1)
            contents = re.sub(r"^\d+\.\s+", "", contents, count=1)
            visible = numeric.group(2)
        display_number = (
            f"{item_number}.{local_number}"
            if local_number and level == "2"
            else ""
        )
        if level == "2" and identifier not in {"learning-outcomes", "references"}:
            sections.append((identifier, display_number or "§", visible))
        number_html = (
            f'<span class="section-number">{escape(display_number)}</span>'
            if display_number
            else ""
        )
        return (
            f'<h{level} id="{identifier}"><a href="#{identifier}">'
            f"{number_html}{contents}</a></h{level}>"
        )

    body = re.sub(
        r'<h([23]) id="([^"]+)">(.*?)</h\1>',
        link_heading,
        body,
        flags=re.DOTALL,
    )
    return body, sections


def typeface_tools() -> str:
    return """  <div class="typeface-tools">
    <label>
      <span>Reading type</span>
      <select data-typeface-picker aria-label="Reading typeface combination">
        <option value="plex">IBM Plex Serif + Sans + Mono</option>
        <option value="google-sans">Google Sans Flex + Code</option>
      </select>
    </label>
  </div>"""


def content_page(
    item: Reading | Guide,
    body: str,
    sections: list[tuple[str, str, str]],
    previous: Reading | Guide | None,
    following: Reading | Guide | None,
    digest: str,
    *,
    label: str,
    total: int,
) -> str:
    nav_items = "\n".join(
        "        <li>"
        f'<a href="#{escape(identifier)}"><small>{escape(number)}</small>'
        f"<span>{escape(title)}</span></a></li>"
        for identifier, number, title in sections
    )
    next_link = (
        f'<a href="../{following.slug}/">Next →</a>'
        if following
        else '<a href="../../">Contents ↑</a>'
    )
    previous_link = (
        f'<a href="../{previous.slug}/">← Previous</a>'
        if previous
        else '<a href="../../">← Contents</a>'
    )
    mobile_previous = f"../{previous.slug}/" if previous else "../../"
    mobile_previous_label = previous.title if previous else "contents"
    mobile_next = f"../{following.slug}/" if following else "../../"
    mobile_next_label = following.title if following else "contents"
    item_code = f"{'G' if isinstance(item, Guide) else 'J'}{item.number}"
    part_label = "Preparation guides" if isinstance(item, Guide) else "Java foundations"
    footer_next = (
        f'<a class="next" href="../{following.slug}/">'
        f"{escape(following.title)} →</a>"
        if following
        else '<a class="next" href="../../">Return to contents ↑</a>'
    )
    return f"""<!doctype html>
<html lang="{LANG}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(item.description)}">
  <title>{escape(item.title)} · {escape(SITE_TITLE)}</title>
  <link rel="stylesheet" href="../../assets/css/site.css">
  <script src="../../assets/js/typeface-switcher.js"></script>
  <script defer src="../../assets/js/quick-checks.js"></script>
</head>
<body id="top">
  {provenance_comments(item.source, digest)}
  <a class="skip-link" href="#chapter-content">Skip to reading</a>

  <nav class="book-nav" aria-label="Reading navigation">
    <a class="wordmark" href="../../">
      <strong>CPEN 221</strong>
      <span>Getting Started</span>
    </a>
    <div class="nav-contents">
      <p class="part-label">{escape(part_label)}</p>
      <h2><a href="#top" aria-current="page">{escape(item.title)} <small>{escape(item_code)}</small></a></h2>
      <ul>
{nav_items}
      </ul>
      <div class="prev-next">
        {previous_link}
        <a href="../../">Up</a>
        {next_link}
      </div>
    </div>
  </nav>

  <nav class="book-nav-mobile" aria-label="Compact reading navigation">
    <a class="mobile-arrow" href="{mobile_previous}" aria-label="Previous: {escape(mobile_previous_label)}">←</a>
    <a class="mobile-title" href="../../">CPEN 221</a>
    <a class="mobile-arrow" href="{mobile_next}" aria-label="Next: {escape(mobile_next_label)}">{'→' if following else '↑'}</a>
  </nav>

{typeface_tools()}

  <main id="chapter-content" class="page">
    <article class="chapter">
      <div class="chapter-number" aria-hidden="true">{escape(item_code)}</div>
      <header class="chapter-header">
        <p class="chapter-kicker">{escape(label)} {item.number} of {total}</p>
        <h1>{escape(item.title)}</h1>
        <p class="lede">{escape(item.description)}</p>
      </header>
{body}
{example_links(item)}

      <footer class="book-footer">
        {footer_next}
        CPEN 221 · Getting Started · {escape(SITE_SUBTITLE)}
      </footer>
    </article>
  </main>
</body>
</html>
"""


def example_links(item: Reading | Guide) -> str:
    example_slug = item.slug if isinstance(item, Reading) else item.example_slug
    if not example_slug:
        return ""
    return f"""<p class="chapter-examples"><a href="../../examples/{escape(example_slug)}/">Browse the complete example files →</a></p>"""


def landing_page() -> str:
    guide_items = "\n".join(
        f"""            <li>
              <span class="num">{guide.number}</span>
              <div>
                <strong><a href="guides/{guide.slug}/">{escape(guide.title)}</a></strong>
                <p>{escape(guide.description)}</p>
              </div>
            </li>"""
        for guide in GUIDES
    )
    reading_items = "\n".join(
        f"""            <li>
              <span class="num">{reading.number}</span>
              <div>
                <strong><a href="readings/{reading.slug}/">{escape(reading.title)}</a></strong>
                <p>{escape(reading.description)}</p>
              </div>
            </li>"""
        for reading in READINGS
    )
    return f"""<!doctype html>
<html lang="{LANG}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Software tools and Java preparation for CPEN 221.">
  <title>{escape(SITE_TITLE)}</title>
  <link rel="stylesheet" href="assets/css/site.css">
  <script src="assets/js/typeface-switcher.js"></script>
</head>
<body id="top">
  <a class="skip-link" href="#main-content">Skip to the contents</a>

  <nav class="book-nav" aria-label="Book navigation">
    <a class="wordmark" href="./" aria-current="page">
      <strong>CPEN 221</strong>
      <span>Getting Started</span>
    </a>
    <div class="nav-contents">
      <p class="part-label">{escape(SITE_SUBTITLE)}</p>
      <h2><a href="#top" aria-current="page">Contents</a></h2>
      <ul>
        <li><a href="#preparation-guides"><small>G</small><span>Preparation guides</span></a></li>
        <li><a href="#java-segments"><small>J</small><span>Java foundations</span></a></li>
      </ul>
      <div class="prev-next">
        <a href="#preparation-guides">Guides</a>
        <a href="guides/software-to-install/">Read →</a>
      </div>
    </div>
  </nav>

  <nav class="book-nav-mobile" aria-label="Compact book navigation">
    <span class="mobile-arrow" aria-hidden="true">❧</span>
    <a class="mobile-title" href="./" aria-current="page">CPEN 221</a>
    <a class="mobile-arrow" href="guides/software-to-install/" aria-label="Next: Software to Install">→</a>
  </nav>

{typeface_tools()}

  <main id="main-content" class="page">
    <article class="contents-page">
      <header class="contents-header">
        <p class="kicker">CPEN 221 preparation</p>
        <h1>{escape(SITE_TITLE)}</h1>
        <p class="deck">{escape(SITE_SUBTITLE)}</p>
      </header>

      <p>These guides and readings establish the development environment, project workflow, and Java foundations used at the start of CPEN 221.</p>

      <div class="ornament" aria-hidden="true">❧</div>

      <div class="contents-group">
        <section aria-labelledby="preparation-guides">
          <h2 id="preparation-guides">Preparation guides</h2>
          <ol class="contents-list">
{guide_items}
          </ol>
        </section>
        <section aria-labelledby="java-segments">
          <h2 id="java-segments">Java foundations</h2>
          <ol class="contents-list">
{reading_items}
          </ol>
        </section>
      </div>

      <section class="prototype-note" aria-labelledby="requirements">
        <h2 id="requirements">Where to begin</h2>
        <p>Begin with <a href="guides/software-to-install/">Software to Install</a>. If Java is already familiar, use the examples and practice in the Java readings to decide where to spend time.</p>
      </section>

      <footer class="book-footer">
        <a class="next" href="guides/software-to-install/">Software to Install →</a>
        CPEN 221 · Getting Started · {escape(SITE_SUBTITLE)}
      </footer>
    </article>
  </main>
</body>
</html>
"""


def example_index(directory: Path) -> str:
    files = sorted(
        path
        for path in directory.rglob("*")
        if path.is_file() and path.name != "index.html"
    )
    items = "\n".join(
        f'        <li><a href="{escape(path.relative_to(directory).as_posix())}">{escape(path.relative_to(directory).as_posix())}</a></li>'
        for path in files
    )
    linked_item = next(
        (
            item
            for item in (*GUIDES, *READINGS)
            if (
                item.example_slug if isinstance(item, Guide) else item.slug
            )
            == directory.name
        ),
        None,
    )
    title = (
        linked_item.title
        if linked_item
        else directory.name.replace("-", " ").title()
    )
    material_path = (
        f"../../{'guides' if isinstance(linked_item, Guide) else 'readings'}/{linked_item.slug}/"
        if linked_item
        else "../../"
    )
    material_label = linked_item.title if linked_item else "contents"
    return f"""<!doctype html>
<html lang="{LANG}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)} · {escape(SITE_TITLE)}</title>
  <link rel="stylesheet" href="../../assets/css/site.css">
  <script src="../../assets/js/typeface-switcher.js"></script>
</head>
<body id="top">
  <a class="skip-link" href="#chapter-content">Skip to example files</a>

  <nav class="book-nav" aria-label="Example navigation">
    <a class="wordmark" href="../../">
      <strong>CPEN 221</strong>
      <span>Getting Started</span>
    </a>
    <div class="nav-contents">
      <p class="part-label">Example files</p>
      <h2><a href="#top" aria-current="page">{escape(title)}</a></h2>
      <ul>
        <li><a href="{material_path}"><small>←</small><span>Back to the reading</span></a></li>
        <li><a href="../../"><small>↑</small><span>All contents</span></a></li>
      </ul>
    </div>
  </nav>

  <nav class="book-nav-mobile" aria-label="Compact example navigation">
    <a class="mobile-arrow" href="{material_path}" aria-label="Back to {escape(material_label)}">←</a>
    <a class="mobile-title" href="../../">CPEN 221</a>
    <a class="mobile-arrow" href="../../" aria-label="All contents">↑</a>
  </nav>

{typeface_tools()}

  <main id="chapter-content" class="page">
    <article class="chapter example-index">
      <div class="chapter-number" aria-hidden="true">EX</div>
      <header class="chapter-header">
        <p class="chapter-kicker">Complete source</p>
        <h1>{escape(title)}</h1>
        <p class="lede">Download these files rather than copying code from the rendered reading.</p>
      </header>
      <ul class="file-list">
{items}
      </ul>
      <footer class="book-footer">
        <a class="next" href="{material_path}">Return to the reading ↑</a>
        CPEN 221 · Getting Started · {escape(SITE_SUBTITLE)}
      </footer>
    </article>
  </main>
</body>
</html>
"""


def main() -> None:
    require_pandoc()
    for generated in (
        GUIDES_ROOT,
        READINGS_ROOT,
        PUBLISHED_SOURCES,
        PUBLISHED_FIGURES_ROOT,
        SITE_ROOT / "examples",
    ):
        if generated.exists():
            shutil.rmtree(generated)
        generated.mkdir(parents=True)

    for figure_name in FIGURE_FILES:
        published_figure = PUBLISHED_FIGURES_ROOT / figure_name
        published_figure.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(
            FIGURE_SOURCE_ROOT / figure_name,
            published_figure,
        )

    def build_collection(
        items: tuple[Reading | Guide, ...], target_root: Path, label: str
    ) -> None:
        for index, item in enumerate(items):
            source = NOTES_ROOT / item.source
            markdown = source.read_text(encoding="utf-8")
            source_copy = PUBLISHED_SOURCES / item.source
            shutil.copy2(source, source_copy)
            digest = sha256(source_copy.read_bytes()).hexdigest()

            without_title = re.sub(r"^# .+?\n+", "", markdown, count=1)
            body, sections = transform_body(
                render_markdown(without_title), item.number
            )
            target = target_root / item.slug
            target.mkdir(parents=True)
            (target / "index.html").write_text(
                content_page(
                    item,
                    body,
                    sections,
                    items[index - 1] if index else None,
                    items[index + 1] if index + 1 < len(items) else None,
                    digest,
                    label=label,
                    total=len(items),
                ),
                encoding="utf-8",
            )

    build_collection(GUIDES, GUIDES_ROOT, "Preparation guide")
    build_collection(READINGS, READINGS_ROOT, "Segment")

    published_examples = SITE_ROOT / "examples"
    for source_directory in sorted(path for path in EXAMPLES_ROOT.iterdir() if path.is_dir()):
        target_directory = published_examples / source_directory.name
        shutil.copytree(
            source_directory,
            target_directory,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("build", ".gradle", "index.html"),
        )
        (target_directory / "index.html").write_text(
            example_index(target_directory), encoding="utf-8"
        )

    (SITE_ROOT / "index.html").write_text(landing_page(), encoding="utf-8")
    print(
        f"Built {len(GUIDES)} guides, {len(READINGS)} readings, "
        f"{len([path for path in EXAMPLES_ROOT.iterdir() if path.is_dir()])} example sets, "
        f"and {len(FIGURE_FILES)} figures."
    )


if __name__ == "__main__":
    main()
