# Running Java Programs — example files

Use a Java 25 JDK. From this directory:

```sh
java RawDifference.java
java ArrivalDisplay.java
javac -Xlint:all ArrivalDisplayExpanded.java
java ArrivalDisplayExpanded
javac -Xlint:all RuntimeFailure.java
java RuntimeFailure.java
```

Observed with Eclipse Temurin 25.0.4.1:

- `RawDifference.java` printed `Arrival in -3 minutes`;
- both arrival-display forms printed `EARLY by 3 minutes`; and
- `RuntimeFailure.java` compiled, then terminated with a
  `NumberFormatException` for `"soon"`.

`TypeMismatch.java.txt` is deliberately named as text because it does not compile.
Copy it to `TypeMismatch.java` to observe the compiler reject an attempt to assign a
`String` value to an `int` variable.

