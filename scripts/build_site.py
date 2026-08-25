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
    GUIDES,
    GUIDES_ROOT,
    LANG,
    NOTES_ROOT,
    PANDOC_ARGUMENTS,
    PANDOC_VERSION,
    PUBLISHED_SOURCES,
    READINGS,
    READINGS_ROOT,
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


def transform_body(body: str) -> tuple[str, list[tuple[str, str]]]:
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

    sections: list[tuple[str, str]] = []

    def link_heading(match: re.Match[str]) -> str:
        level, identifier, contents = match.groups()
        visible = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", contents)).strip()
        if level == "2" and identifier not in {"learning-outcomes", "references"}:
            visible = re.sub(r"^\d+\.\s+", "", visible)
            sections.append((identifier, visible))
        return (
            f'<h{level} id="{identifier}"><a href="#{identifier}">'
            f"{contents}</a></h{level}>"
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
    <label for="typeface-picker">Typeface set</label>
    <select id="typeface-picker" data-typeface-picker>
      <option value="plex">IBM Plex Serif + Sans</option>
      <option value="google-sans">Google Sans Flex + Code</option>
    </select>
  </div>"""


def content_page(
    item: Reading | Guide,
    body: str,
    sections: list[tuple[str, str]],
    previous: Reading | Guide | None,
    following: Reading | Guide | None,
    digest: str,
    *,
    label: str,
    total: int,
) -> str:
    section_links = "\n".join(
        f'          <li><a href="#{escape(identifier)}">{escape(title)}</a></li>'
        for identifier, title in sections
    )
    previous_link = (
        f'<a href="../{previous.slug}/">← {escape(previous.title)}</a>'
        if previous
        else '<a href="../../">← Contents</a>'
    )
    next_link = (
        f'<a href="../{following.slug}/">{escape(following.title)} →</a>'
        if following
        else '<a href="../../">Contents ↑</a>'
    )
    return f"""<!doctype html>
<html lang="{LANG}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(item.description)}">
  <title>{escape(item.title)} · Getting Started with Java</title>
  <link rel="stylesheet" href="../../assets/css/site.css">
  <script src="../../assets/js/typeface-switcher.js"></script>
  <script defer src="../../assets/js/quick-checks.js"></script>
</head>
<body id="top">
  {provenance_comments(item.source, digest)}
  <a class="skip-link" href="#reading-content">Skip to reading</a>
  <header class="site-header">
    <a class="wordmark" href="../../"><strong>Getting Started with Java</strong><span>CPEN 221 preparation</span></a>
  </header>
{typeface_tools()}
  <div class="reading-layout">
    <nav class="contents" aria-label="On this page">
      <p>{escape(label)} {item.number} of {total}</p>
      <ol>
{section_links}
      </ol>
    </nav>
    <main id="reading-content">
      <article class="reading">
        <header class="reading-header">
          <p>{escape(label)} {item.number}</p>
          <h1>{escape(item.title)}</h1>
          <p class="lede">{escape(item.description)}</p>
        </header>
{body}
        {source_links(item)}
        <nav class="reading-nav" aria-label="{escape(label)} sequence">
          {previous_link}
          {next_link}
        </nav>
      </article>
    </main>
  </div>
</body>
</html>
"""


def source_links(item: Reading | Guide) -> str:
    example_slug = item.slug if isinstance(item, Reading) else item.example_slug
    if example_slug:
        heading = "Use the complete files"
        links = (
            f'<a href="../../examples/{escape(example_slug)}/">Browse the complete example files</a> '
            f'or <a href="../../sources/{escape(item.source)}">open the Markdown source</a>.'
        )
    else:
        heading = "Read the source"
        links = f'<a href="../../sources/{escape(item.source)}">Open the Markdown source</a>.'
    kind = "Reading" if isinstance(item, Reading) else "Guide"
    return f"""<aside class="source-links" aria-label="{kind} files">
          <h2>{heading}</h2>
          <p>{links}</p>
        </aside>"""


def landing_page() -> str:
    guide_cards = "\n".join(
        f"""      <li>
        <a href="guides/{guide.slug}/">
          <span>Guide {guide.number}</span>
          <strong>{escape(guide.title)}</strong>
          <small>{escape(guide.description)}</small>
        </a>
      </li>"""
        for guide in GUIDES
    )
    reading_cards = "\n".join(
        f"""      <li>
        <a href="readings/{reading.slug}/">
          <span>Segment {reading.number}</span>
          <strong>{escape(reading.title)}</strong>
          <small>{escape(reading.description)}</small>
        </a>
      </li>"""
        for reading in READINGS
    )
    return f"""<!doctype html>
<html lang="{LANG}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Getting started with Java in preparation for CPEN 221.">
  <title>Getting Started with Java · CPEN 221</title>
  <link rel="stylesheet" href="assets/css/site.css">
  <script src="assets/js/typeface-switcher.js"></script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="hero">
    <p>CPEN 221 preparation</p>
    <h1>Getting Started with Java</h1>
    <p>Preparing for CPEN 221 in Three Segments</p>
  </header>
{typeface_tools()}
  <main id="main" class="landing">
    <section aria-labelledby="preparation-guides">
      <h2 id="preparation-guides">Set up your tools and workflow</h2>
      <p>Use these guides to establish the same development environment and project workflow used in CPEN 221. Start with installation, then follow the guides in order if the command line, build tools, or Git are new to you.</p>
      <ol class="reading-cards">
{guide_cards}
      </ol>
    </section>
    <section aria-labelledby="java-segments">
      <h2 id="java-segments">Learn or refresh Java</h2>
      <p>Begin with the first segment if Java is new to you. If the material is familiar, predict the examples and use the practice to decide where to spend time.</p>
      <ol class="reading-cards">
{reading_cards}
      </ol>
    </section>
    <section class="requirements" aria-labelledby="requirements">
      <h2 id="requirements">What you need</h2>
      <p>The readings work without JavaScript. Begin with <a href="guides/software-to-install/">Software to Install</a>, then use the downloadable examples to check the complete toolchain.</p>
    </section>
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
        f'      <li><a href="{escape(path.relative_to(directory).as_posix())}">{escape(path.relative_to(directory).as_posix())}</a></li>'
        for path in files
    )
    title = directory.name.replace("-", " ").title()
    return f"""<!doctype html>
<html lang="{LANG}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)} · Getting Started with Java examples</title>
  <link rel="stylesheet" href="../../assets/css/site.css">
  <script src="../../assets/js/typeface-switcher.js"></script>
</head>
<body>
  <header class="site-header"><a class="wordmark" href="../../"><strong>Getting Started with Java</strong><span>Example files</span></a></header>
{typeface_tools()}
  <main class="file-list">
    <h1>{escape(title)}</h1>
    <p>Download these authoritative files rather than copying code from the rendered reading.</p>
    <ul>
{items}
    </ul>
  </main>
  <footer><p><a href="../../">Return to the readings</a></p></footer>
</body>
</html>
"""


def main() -> None:
    require_pandoc()
    for generated in (
        GUIDES_ROOT,
        READINGS_ROOT,
        PUBLISHED_SOURCES,
        SITE_ROOT / "examples",
    ):
        if generated.exists():
            shutil.rmtree(generated)
        generated.mkdir(parents=True)

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
            body, sections = transform_body(render_markdown(without_title))
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
        f"Built {len(GUIDES)} guides, {len(READINGS)} readings, and "
        f"{len([path for path in EXAMPLES_ROOT.iterdir() if path.is_dir()])} example sets."
    )


if __name__ == "__main__":
    main()
