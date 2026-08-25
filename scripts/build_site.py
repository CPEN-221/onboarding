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
    LANG,
    NOTES_ROOT,
    PANDOC_ARGUMENTS,
    PANDOC_VERSION,
    PUBLISHED_SOURCES,
    READINGS,
    READINGS_ROOT,
    SITE_ROOT,
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


def reading_page(
    reading: Reading,
    body: str,
    sections: list[tuple[str, str]],
    previous: Reading | None,
    following: Reading | None,
    digest: str,
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
  <meta name="description" content="{escape(reading.description)}">
  <title>{escape(reading.title)} · Java On-ramp</title>
  <link rel="stylesheet" href="../../assets/css/site.css">
  <script defer src="../../assets/js/quick-checks.js"></script>
</head>
<body id="top">
  {provenance_comments(reading.source, digest)}
  <a class="skip-link" href="#reading-content">Skip to reading</a>
  <header class="site-header">
    <a class="wordmark" href="../../"><strong>Java On-ramp</strong><span>CPEN 221 preparation</span></a>
  </header>
  <div class="reading-layout">
    <nav class="contents" aria-label="On this page">
      <p>Reading {reading.number} of {len(READINGS)}</p>
      <ol>
{section_links}
      </ol>
    </nav>
    <main id="reading-content">
      <article class="reading">
        <header class="reading-header">
          <p>Java on-ramp {reading.number}</p>
          <h1>{escape(reading.title)}</h1>
          <p class="lede">{escape(reading.description)}</p>
        </header>
{body}
        <aside class="source-links" aria-label="Reading files">
          <h2>Use the complete files</h2>
          <p><a href="../../examples/{escape(reading.slug)}/">Browse the Java examples</a> or <a href="../../sources/{escape(reading.source)}">open the Markdown source</a>.</p>
        </aside>
        <nav class="reading-nav" aria-label="Reading sequence">
          {previous_link}
          {next_link}
        </nav>
      </article>
    </main>
  </div>
  <footer><p>Ungraded preparation for CPEN 221. Answers remain in your browser and are not submitted.</p></footer>
</body>
</html>
"""


def landing_page() -> str:
    cards = "\n".join(
        f"""      <li>
        <a href="readings/{reading.slug}/">
          <span>Reading {reading.number}</span>
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
  <meta name="description" content="A self-paced Java 25 on-ramp for CPEN 221.">
  <title>Java On-ramp · CPEN 221</title>
  <link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
  <a class="skip-link" href="#main">Skip to readings</a>
  <header class="hero">
    <p>CPEN 221 preparation</p>
    <h1>Java On-ramp</h1>
    <p>Three short readings for learning or refreshing the Java needed at the start of Software Construction.</p>
  </header>
  <main id="main" class="landing">
    <section aria-labelledby="how-to-use">
      <h2 id="how-to-use">How to use this on-ramp</h2>
      <p>Begin with the first reading if Java is new to you. If the material is familiar, predict the examples and use the practice to decide where to spend time. The checks are for feedback only: there is no account, score, or submission.</p>
      <ol class="reading-cards">
{cards}
      </ol>
    </section>
    <section class="requirements" aria-labelledby="requirements">
      <h2 id="requirements">What you need</h2>
      <p>The readings work without JavaScript. To run the downloadable examples, install a Java 25 JDK and use a terminal. Each example directory includes the exact commands and observed output.</p>
    </section>
  </main>
  <footer><p>Java 25 · No tracking · No grades</p></footer>
</body>
</html>
"""


def example_index(directory: Path) -> str:
    files = sorted(path for path in directory.iterdir() if path.is_file())
    items = "\n".join(
        f'      <li><a href="{escape(path.name)}">{escape(path.name)}</a></li>'
        for path in files
    )
    title = directory.name.replace("-", " ").title()
    return f"""<!doctype html>
<html lang="{LANG}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)} · Java On-ramp examples</title>
  <link rel="stylesheet" href="../../assets/css/site.css">
</head>
<body>
  <header class="site-header"><a class="wordmark" href="../../"><strong>Java On-ramp</strong><span>Example files</span></a></header>
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
    for generated in (READINGS_ROOT, PUBLISHED_SOURCES, SITE_ROOT / "examples"):
        if generated.exists():
            shutil.rmtree(generated)
        generated.mkdir(parents=True)

    for index, reading in enumerate(READINGS):
        source = NOTES_ROOT / reading.source
        markdown = source.read_text(encoding="utf-8")
        source_copy = PUBLISHED_SOURCES / reading.source
        shutil.copy2(source, source_copy)
        digest = sha256(source_copy.read_bytes()).hexdigest()

        without_title = re.sub(r"^# .+?\n+", "", markdown, count=1)
        body, sections = transform_body(render_markdown(without_title))
        target = READINGS_ROOT / reading.slug
        target.mkdir(parents=True)
        (target / "index.html").write_text(
            reading_page(
                reading,
                body,
                sections,
                READINGS[index - 1] if index else None,
                READINGS[index + 1] if index + 1 < len(READINGS) else None,
                digest,
            ),
            encoding="utf-8",
        )

    published_examples = SITE_ROOT / "examples"
    for source_directory in sorted(path for path in EXAMPLES_ROOT.iterdir() if path.is_dir()):
        target_directory = published_examples / source_directory.name
        shutil.copytree(source_directory, target_directory, dirs_exist_ok=True)
        (target_directory / "index.html").write_text(
            example_index(target_directory), encoding="utf-8"
        )

    (SITE_ROOT / "index.html").write_text(landing_page(), encoding="utf-8")
    print(f"Built {len(READINGS)} readings and {len(list(EXAMPLES_ROOT.iterdir()))} example sets.")


if __name__ == "__main__":
    main()
