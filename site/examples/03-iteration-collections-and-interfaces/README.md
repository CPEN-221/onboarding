# Iteration, collections, and interfaces

Compile with Java 25:

```bash
javac -Xlint:all *.java
```

Run the deterministic examples:

```bash
java ArraySummary
java CollectionsDemo
java RuleDemo
```

`ArrayBoundsFailure` deliberately produces `ArrayIndexOutOfBoundsException` after
compiling successfully. None of the reported outputs depends on `HashSet` or
`HashMap` iteration order.
