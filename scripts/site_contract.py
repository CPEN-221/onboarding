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
GUIDES_ROOT = SITE_ROOT / "guides"
PUBLISHED_SOURCES = SITE_ROOT / "sources"

PANDOC_VERSION = "3.10"
PANDOC_ARGUMENTS = (
    "--from=gfm",
    "--to=html5",
    "--wrap=none",
    "--syntax-highlighting=none",
)
LANG = "en-CA"

FONT_FILES = (
    "GoogleSansCode-Latin.woff2",
    "GoogleSansFlex-Latin.woff2",
    "IBMPlexSans-Bold.woff2",
    "IBMPlexSans-Italic.woff2",
    "IBMPlexSans-Regular.woff2",
    "IBMPlexSerif-Bold.woff2",
    "JetBrainsMono-Bold.woff2",
    "JetBrainsMono-Regular.woff2",
)
FONT_LICENSES = (
    "Google-Sans-Code-OFL.txt",
    "Google-Sans-Flex-OFL.txt",
    "IBM-Plex-OFL.txt",
    "JetBrains-Mono-OFL.txt",
)


@dataclass(frozen=True)
class Reading:
    source: str
    slug: str
    number: int
    title: str
    description: str


@dataclass(frozen=True)
class Guide:
    source: str
    slug: str
    number: int
    title: str
    description: str
    example_slug: str | None = None


GUIDES = (
    Guide(
        "guide-software-to-install.md",
        "software-to-install",
        1,
        "Software to Install",
        "Install and verify Java 25, Git, VS Code, and the project-supplied Gradle wrapper on macOS, Linux, or Windows.",
    ),
    Guide(
        "guide-command-line-interface.md",
        "using-command-line-interface",
        2,
        "Using the Command Line Interface",
        "Navigate a project, read paths and commands, operate on files carefully, and preserve useful diagnostic output.",
    ),
    Guide(
        "guide-vscode.md",
        "installing-and-using-vscode",
        3,
        "Installing and Using Visual Studio Code",
        "Configure Java, Gradle, Git, testing, debugging, and the integrated terminal without hiding the project build.",
    ),
    Guide(
        "guide-build-process-and-tools.md",
        "build-process-and-tools",
        4,
        "The Build Process and Tools",
        "Follow Java source through compilation, testing, execution, and packaging with the Gradle wrapper and JUnit.",
        "build-process-and-tools",
    ),
    Guide(
        "guide-git-and-github.md",
        "git-and-github",
        5,
        "Git and GitHub",
        "Understand why projects need version control, then record commits, share work, use branches, and recover changes.",
    ),
)


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
