# Work Completed and Validation Log

Last updated: August 25, 2026

## Complete preparation-guide sequence

Five student-facing guides were written from new outlines, using the three
documents in `CPEN 221 Aux` as topic references where applicable:

| Guide | Words | Formative checks |
|---|---:|---:|
| Software to Install | 1,598 | 2 |
| Using the Command Line Interface | 2,295 | 2 |
| Installing and Using Visual Studio Code | 1,643 | 2 |
| The Build Process and Tools | 1,871 | 2 |
| Git and GitHub | 3,454 | 4 |

The command-line guide now develops the filesystem hierarchy before introducing
navigation: root, home, and project directories; parent, child, sibling, and
descendant relationships; absolute and relative paths; and the working directory
maintained by each shell. The build guide compares `make`, Maven, and Gradle before
explaining Gradle phases, its task graph, dependency resolution, caching, wrapper,
and outputs. The Git guide first explains why software projects need version
control: related files must be recorded as one project state, temporary saves
should not become permanent checkpoints, and concurrent changes need a controlled
merge. It then develops repository storage, file states, remotes, branches, and
recovery.

The command-line guide now includes two original SVG figures. The first places the
filesystem root, home directory, course directory, project root, and sibling
directories in one hierarchy. The second marks a working directory in the project
tree and resolves `.`, `..`, `../test`, and `../..` from that location. The prose
also distinguishes directories from files and explains how a shell resolves a
relative path one component at a time.

The Git guide now includes three original SVG figures: linked project-wide
snapshots, the working-tree/staging/local-repository/GitHub flow, and the branch
pointers before and after a fast-forward merge. Each figure has nearby explanatory
prose, alternative text, a caption, and an internal SVG title and description.
Narrow screens retain a legible figure size in a keyboard-scrollable region.
Editable sources and publication metadata live under `assets/`; the site build
copies the declared files to `site/assets/figures/`.

The rewrite replaces outdated JUnit 4, Spring, `master`, `checkout`, password, and
global-build-tool advice with Java 25, JUnit 6.1.3, Gradle wrappers, `main`, modern
Git recovery commands, and current GitHub authentication guidance. The 33 direct
references point to official Adoptium, Gradle, Git, GitHub, VS Code, Microsoft, GNU,
and JUnit documentation.

The build guide has a complete companion project. Its wrapper pins Gradle 9.6.1,
its toolchain requests Java 25, its tests use JUnit 6.1.3, and all Java compilation
enables `-Xlint:all`.

## Complete Java preparation sequence

The standalone sequence contains three student-facing readings written from new
outlines:

| Reading | Words | Formative checks | Explanation practice |
|---|---:|---:|---:|
| Running Java Programs | 2,787 | 3 | 5 |
| Objects, State, and References | 2,530 | 3 | 5 |
| Iteration, Collections, and Interfaces | 2,582 | 3 | 6 |

Each reading begins with a transit-display problem, states its learning outcomes,
develops one central example and a design principle, addresses a misconception,
ends with prediction or explanation practice and a summary, and cites only the
Java 25 material it uses. All thirteen external references resolve to current
Oracle Java 25 language, virtual-machine, or API documentation.

The source repository at
`/Users/sg/Dropbox/Teaching/CPEN 221/playground-e2mi6c9i` supplied the complete
Tech.io manifest, launch scripts, original examples, Tester 3.0, and Git history.
No further export from Tech.io was required. The new readings do not depend on
Tech.io, Tester Prima, PrairieLearn, or a hosted Java runner.

## Java validation

Validated all thirteen Java source files and compilation fixtures under `examples/`
with Eclipse Temurin 25.0.4.1. All twelve complete `.java` files compiled with
`javac -Xlint:all` without reported warnings.
The following output and failure observations matched the readings:

- the first example set printed `Arrival in -3 minutes` and `EARLY by 3 minutes`;
- `RuntimeFailure` threw `NumberFormatException`, while the deliberately invalid
  type-mismatch fixture was rejected by `javac`;
- the object examples showed the `10`-to-`14` alias update and the reassignment to
  `UBC Exchange: 28 minutes`;
- the null-receiver example threw `NullPointerException`;
- the array example counted two late predictions;
- the collection example reported three observations, two distinct routes, and a
  latest delay of seven for route 44;
- the interface-composition example counted two matching delays; and
- the invalid array access threw `ArrayIndexOutOfBoundsException`.

`scripts/validate_examples.py` reproduces these observations and refuses a Java
version other than 25.

`scripts/validate_guides.py` observed Eclipse Temurin 25.0.4.1 and Gradle 9.6.1,
ran the companion project's `test`, `run`, and `build` tasks, and found the expected
JAR and HTML test report. The application printed `Route 44: ON TIME`. The same
script created a temporary Git 2.50.1 repository and observed the documented
untracked, staged, committed, restored, and clean states.

## Publication validation

The static-site build uses pinned Pandoc 3.10 and publishes the authoritative
Markdown and complete example files alongside the rendered guides and readings.
The generated site has thirteen HTML pages: one landing page, five preparation
guides, three Java readings, and four example-file indexes. Rendered pages do not
link to the published Markdown copies; pages with companion code link only to the
complete example files.

The published title is **Getting Started with CPEN 221**, with the subtitle
**Software Tools and Java**. Five preparation guides form one track, while the
Java material remains organized as three segments. Every page
includes a selector for two self-hosted type systems: IBM Plex Sans with IBM Plex
Serif headings and JetBrains Mono code, or Google Sans Flex with Google Sans Code.
The preference is applied locally across the site and the content remains usable
when the enhancement script is unavailable. The font binaries and their SIL OFL
1.1 licence notices are committed under `site/assets/fonts/`; selecting either set
makes no request to a font CDN.

`scripts/check_site.py` accepted every local link, fragment, page landmark, all
eight source digests, all eight WOFF2 font assets and their four licence notices,
all five figure source/output pairs, and all twenty-one embedded quick-check
structures. `node --check` accepted the progressive-enhancement scripts. The
activities remain readable as ordinary questions and answer disclosures without
JavaScript. With JavaScript, they gain local Check buttons and retry feedback.
They make no network
requests and retain no completion record. Responsive and print rules are present,
but final visual review in the target browsers remains part of the instructor
review.
