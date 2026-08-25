#!/usr/bin/env python3
"""Shared publication contract for the standalone Java onboarding site."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import subprocess


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
NOTES_ROOT = REPOSITORY_ROOT / "notes"
EXAMPLES_ROOT = REPOSITORY_ROOT / "examples"
SITE_ROOT = REPOSITORY_ROOT / "site"
READINGS_ROOT = SITE_ROOT / "readings"
PUBLISHED_SOURCES = SITE_ROOT / "sources"

PANDOC_VERSION = "3.10"
PANDOC_ARGUMENTS = (
    "--from=gfm",
    "--to=html5",
    "--wrap=none",
    "--syntax-highlighting=none",
)
LANG = "en-CA"


@dataclass(frozen=True)
class Reading:
    source: str
    slug: str
    number: int
    title: str
    description: str


READINGS = (
    Reading(
        "01-running-java-programs.md",
        "01-running-java-programs",
        1,
        "Running Java Programs",
        "Run, trace, and repair a small Java 25 program before translating it to the form used in course projects.",
    ),
    Reading(
        "02-objects-state-and-references.md",
        "02-objects-state-and-references",
        2,
        "Objects, State, and References",
        "Construct objects and trace mutable state, aliases, reassignment, identity, and null references.",
    ),
    Reading(
        "03-iteration-collections-and-interfaces.md",
        "03-iteration-collections-and-interfaces",
        3,
        "Iteration, Collections, and Interfaces",
        "Traverse values, choose collection contracts, and combine behaviour through interfaces and composition.",
    ),
)

SOURCE_DIGEST_PATTERN = re.compile(r"source-sha256:\s*([0-9a-f]{64})")
SOURCE_FILE_PATTERN = re.compile(r"source-file:\s*([A-Za-z0-9_.-]+\.md)")


def installed_pandoc_version() -> str:
    try:
        output = subprocess.run(
            ["pandoc", "--version"],
            capture_output=True,
            check=True,
            text=True,
        ).stdout
    except (FileNotFoundError, subprocess.CalledProcessError):
        return "unavailable"
    first_line = output.splitlines()[0]
    return first_line.removeprefix("pandoc ").strip()


def provenance_comments(source_name: str, digest: str) -> str:
    return (
        f"<!-- source-sha256: {digest} -->\n"
        f"  <!-- source-file: {source_name} -->"
    )


def read_provenance(page_source: str) -> tuple[str | None, str | None]:
    digest = SOURCE_DIGEST_PATTERN.search(page_source)
    source = SOURCE_FILE_PATTERN.search(page_source)
    return (
        source.group(1) if source else None,
        digest.group(1) if digest else None,
    )

