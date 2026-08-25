# Getting Started with Java — Design Record

Last updated: August 25, 2026

## Purpose

This document records the replacement of the Fall 2025 *Introduction to Java*
material formerly delivered from `pl-ubc-cpen221/`. The inherited material combines approximately
40,000 words of reading, 220 PrairieLearn pages, and 122 externally hosted Tech.io
widgets. The replacement will separate reading and formative practice from any
later graded assessment.

The student-facing replacement lives in this independent repository and can be
published directly with GitHub Pages. It does not form part of the core course-note
sequence. PrairieLearn may later host a separate Java readiness assessment, but the
activities embedded here do not report grades.

## Decisions Already Made

- Write the replacement from a new outline rather than translating the 220 pages.
- Publish the canonical prose and formative activities on GitHub Pages.
- Keep any later graded Java assessment separate in PrairieLearn.
- Target Java 25 and use JUnit 6 when testing first appears.
- Keep all replacement source, questions, answers, Java examples, and observed
  outputs together in this standalone repository.
- Treat the Tech.io repository at
  `/Users/sg/Dropbox/Teaching/CPEN 221/playground-e2mi6c9i` as reference material.
  It contains the starter source, Tech.io manifest, launch scripts, Tester 3.0 JAR,
  and Git history.
- Do not carry Tester Prima into the replacement. Its reflective object printout is
  not Java's execution model, and its numbered object labels are not Java reference
  values.
- Use one recurring transit example where it supports the concept. Do not preserve
  an old example merely because its source is available.
- Make every activity usable without an account. Client-side answers are therefore
  formative and intentionally inspectable.

## Relationship to the Core Readings

Chapter 1 currently begins with a packaged class containing a private constructor,
a static method, local variables, conditionals, and string results. It then moves
directly to Gradle and JUnit. A novice must already understand enough Java syntax to
read that example.

The replacement should therefore be a **preparatory sequence** that precedes Chapter 1. It
is not Chapter 1 itself: the sequence explains Java programs, values, methods,
objects, references, iteration, collections, and interfaces. Chapter 1 then uses
those mechanisms to establish the build, test, Git, and evidence loop.

Students with prior Java experience should be able to use a short readiness check
to identify which segments they need. Later chapters may assume the
sequence's stated outcomes whether a student learned them here or elsewhere.

The sequence has its own landing page and three-segment navigation. This
keeps preparatory material out of the numbered core readings while preserving a
clear transition: the sequence establishes enough Java to read the opening example,
then Chapter 1 introduces the course build, test, Git, and evidence loop.

## Segment Sequence

### Segment 1 — Running Java Programs

Central problem: a transit display prints a negative waiting time because the
program reports a calculation without interpreting what the value means.

Outcomes:

- run a Java 25 compact source file and identify its observable entry point;
- trace expressions, local variables, assignments, and method calls;
- use `int`, `boolean`, and `String` values without treating the types as
  interchangeable;
- predict the branch selected by an `if` statement;
- distinguish compilation failure, runtime failure, and an unwanted result; and
- translate a compact source example into the explicit class-and-`static` form used
  in course projects.

This reading replaces the calculator-first opening and introduces an observable
program before classes and object inspection.

### Segment 2 — Objects, State, and References

Central problem: two variables refer to the same mutable arrival board, so a change
through one name becomes visible through the other.

Outcomes:

- distinguish a class declaration, an object, a reference, and a variable;
- construct an object and invoke an instance method;
- use constructors, private fields, and accessors;
- trace aliases using abstract object labels that are explicitly diagram notation;
- distinguish local variables, parameters, instance fields, and static fields; and
- explain what `null` means without presenting a physical-memory layout as a Java
  language guarantee.

This reading supplies only the aliasing foundation. Chapter 4 remains responsible
for representation exposure, defensive copying, and debugging mutable systems.

### Segment 3 — Iteration, Collections, and Shared Behaviour

Central problem: the program must classify several predictions, reject duplicate
stop identifiers, and look up a stop by identifier without duplicating traversal
code.

Outcomes:

- trace `for` and enhanced `for` loops;
- use arrays where fixed indexed storage matters;
- choose among `List`, `Set`, and `Map` from their behavioural contracts;
- read a generic type such as `List<ArrivalPrediction>`;
- distinguish an unspecified iteration order from a random order;
- use an interface as the type shared by several implementations; and
- prefer composition unless an inheritance relationship has a behavioural reason.

Abstract classes and implementation inheritance do not belong in this sequence. The
core readings develop behavioural subtyping and composition with stronger design
motivation.

## Current-Material Crosswalk

The table maps conceptual units rather than individual page fragments. The precise
question-level source remains available under `pl-ubc-cpen221/questions/java/`, and
the corresponding runnable source remains in the Tech.io repository.

| Current unit | Useful material | Replacement location | Disposition |
|---|---|---|---|
| 1 — programs, calculator, syntax | Predicting output; deliberate syntax failures | Segment 1 | Replace the Tester opening with a Java 25 compact program. Combine arithmetic and syntax into expression traces and diagnostic classification. |
| 2 — fields and types | String concatenation; numeric types; compiler type checks | Segment 1 | Start with local variables rather than fields. Retain type-error reasoning. Replace the gravity, wages, and video-game examples. State overflow and floating-point limits precisely. |
| 3 — methods and design recipe | Repeated computation; parameters; return values; compiler diagnostics | Segment 1 | Retain the problem-before-method progression. State the contract before implementation. Remove exact-diagnostic transcription and Tester-specific execution. |
| 4 — booleans and conditionals | Branch prediction; boundary cases | Segment 1 | Retain and compress. Repair inconsistent boundaries and use the transit classification example. |
| 5 — compound data, references, scope | Constructors; method calls; aliases; local scope | Segment 2 | Rebuild around private fields and explicit object diagrams. Do not use Tester labels as reference values. Correct the account of parameter and local-variable scopes. |
| 6 — more classes and testing | String methods; examples becoming tests | Segment 2 and Chapter 1 | Retain selected method-call practice. Replace Tester with JUnit 6, introduced by Chapter 1's feedback loop. |
| 7 — nested data and geometry | Nested objects; approximate equality; boundary testing | Segment 2 | Retain nested-object tracing and one numerical caveat. Replace the geometry hierarchy and repair the circle-boundary inconsistency. |
| 8 — interfaces and query composition | Interface types; several implementations; composite queries | Segment 3 | Retain the conceptual progression but use the transit example. Emphasize contracts and composition rather than field visibility by directory. |
| 9 — arrays, static methods, and `main` | Indexed access; class methods; command-line execution | Segments 1 and 3 | Teach Java 25 launch rules accurately. Present `public static void main(String[] args)` as the course-project convention, not the only Java entry point. |
| 10 — loops and array manipulation | Loop traces; boundary conditions; construction of result arrays | Segment 3 | Retain prediction and repair tasks. Prefer enhanced loops and collections when indexing is not the point. Remove or repair non-compiling examples. |
| 11 — nested arrays and loops | Row/column traversal | Optional practice after Segment 3 | Keep one trace only if later labs require it. Remove the incorrect explanation of `[Z` and avoid treating allocation location as a language guarantee. |
| 12 — generics and collections | Generic types; `ArrayList`, `HashSet`, and `HashMap` | Segment 3 | Rewrite against Java 25. Correct `add`'s return value, autoboxing, Go generics, wrapper construction, and collection-order guarantees. |
| 13 — abstract classes and inheritance | Recognition of shared implementation | Core Chapters 7 and 8 | Remove from the preparatory sequence. The one-line `and` method is better expressed as an interface default method; inheritance needs a behavioural-subtyping motivation. |

Across all units, remove standalone summary pages and fold concise summaries into
the end of each reading. Replace questions that ask students to copy code, count
changed lines, or reproduce one compiler's exact wording with prediction,
explanation, diagnosis, or repair.

## Formative Interaction Model

The first release needs a small interaction vocabulary, not an in-browser learning
management system.

1. **Predict** — select or enter an output before revealing the result.
2. **Trace** — complete a table of variable values, branches, calls, or reference
   relationships.
3. **Classify** — identify a type, diagnostic category, collection contract, or
   kind of program failure.
4. **Order** — arrange statements or execution events.
5. **Repair** — choose or write the smallest change that makes code meet a stated
   requirement.
6. **Explain** — compare a short written explanation with a supplied model.

Each activity should use ordinary semantic HTML. JavaScript may add a Check button,
immediate feedback, retries, and local completion state. Without JavaScript, the
question and a disclosure containing the explanation should remain readable. The
site will not transmit answers, identify students, or claim that completion proves
mastery.

An arbitrary Java runner is not required for the pilot. Every example will be
available as a source download and will be compiled and run during validation. If a
runner is added later, it should be a replaceable enhancement whose absence does
not remove the explanation or activity.

## Validation Rules

- Keep the authoritative example source in the repository; do not extract source
  from rendered HTML.
- Compile every complete example with Java 25 and `-Xlint:all`.
- Run every example whose output the reading reports and save the observed output
  used during review.
- Mark incomplete fragments as fragments and compile their surrounding complete
  example.
- Check the no-JavaScript and keyboard-only activity experience.
- Do not pin questions to exact `javac` wording unless the wording itself is the
  subject and the JDK version is stated.
- End each segment with only the references directly used by that segment.

## Implemented Publication Model

All three readings are complete under `notes/`. Each has complete downloadable Java
source under `examples/`, and the generated site publishes both the rendered prose
and the source files. Client-side JavaScript adds Check buttons to nine
multiple-choice questions. Ordinary HTML disclosures supply the explanations when
JavaScript is disabled.

The repository does not include an arbitrary Java runner. The build validates all
examples with Java 25, while students run the same files locally. This keeps the
reading host replaceable, avoids a dependency on the former Tech.io execution
platform, and leaves grading to a separate system if it is wanted later.
