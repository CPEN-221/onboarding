# Work Completed and Validation Log

Last updated: August 25, 2026

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

## Publication validation

The static-site build uses pinned Pandoc 3.10 and publishes the authoritative
Markdown and complete example files alongside the rendered readings. The generated
site has seven HTML pages: one landing page, three readings, and three example-file
indexes.

The published title is **Getting Started with Java**, organized as three segments.
Every page includes a typeface selector with balanced, serif, and sans-serif
choices. The preference is applied locally across the site and the content remains
usable when the enhancement script is unavailable.

`scripts/check_site.py` accepted every local link, fragment, page landmark, source
digest, and embedded quick-check structure. `node --check` accepted the progressive
enhancement script. The activities remain readable as ordinary questions and
answer disclosures without JavaScript; with JavaScript, they gain local Check
buttons and retry feedback. They make no network requests and retain no completion
record. Responsive and print rules are present, but final visual review in the
target browsers remains part of the instructor review.
