# Getting Started with CPEN 221

**Software Tools and Java**

This repository contains two self-paced preparation tracks for the start of CPEN
221. Five guides establish the development environment and workflow:

1. **Software to Install**
2. **Using the Command Line Interface**
3. **Installing and Using Visual Studio Code**
4. **The Build Process and Tools**
5. **Git and GitHub**

Three Java readings then teach or refresh the required language material:

1. **Running Java Programs**
2. **Objects, State, and References**
3. **Iteration, Collections, and Interfaces**

The segments and activities are deliberately separate from the core course notes
and from PrairieLearn. The activities provide immediate browser feedback but have
no accounts, grades, analytics, or network requests. A later readiness assessment
can be offered separately in PrairieLearn without changing this material.

## Repository layout

| Path | Contents |
|---|---|
| `notes/` | Authoritative Markdown guides and Java readings |
| `examples/` | Complete Java 25 source files and deliberate failure fixtures |
| `assets/` | Editable figure sources and figure metadata |
| `site/` | Generated static site committed for review and deployed by Pages |
| `site/assets/fonts/` | Self-hosted reading and code fonts with SIL OFL notices |
| `site/assets/figures/` | Generated SVG figures copied from the editable sources |
| `scripts/` | Site build, publication checks, and Java example validation |
| `PLAN.md` | Design decisions and crosswalk from the inherited material |
| `STATUS.md` | Completed work and observed validation results |

## Preview the site

Install Pandoc 3.10 and a Java 25 JDK. From the repository root:

```sh
python3 scripts/build_site.py
python3 scripts/check_site.py
python3 scripts/validate_examples.py
python3 scripts/validate_guides.py
python3 -m http.server 8000 --directory site
```

Then open <http://localhost:8000/>. The generated HTML includes source hashes, and
the checker refuses stale pages, missing local links, invalid fragments, or a
mismatch between the declared and published guides, readings, or figures.

## Publish with GitHub Pages

The workflow in `.github/workflows/pages.yml` rebuilds the committed pages, checks
that the build creates no diff, validates the site, tests every Java example under
Java 25, exercises the Gradle and Git guide workflows, and deploys `site/`. After
pushing the repository to GitHub, select
**GitHub Actions** as the Pages source in the repository settings.
