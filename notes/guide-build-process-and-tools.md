# The Build Process and Tools

`TransitSummary.java` compiles on one laptop, yet a teammate cannot even start its
tests. The source file is identical. The difference is outside that file: one
person manually assembled a compiler command and a collection of JAR paths, while
the other has no record of those choices.

A build turns those hidden choices into a versioned, repeatable procedure.

By the end, you should be able to:

- distinguish Java source, compiled classes, dependencies, test results, and a
  packaged JAR;
- explain the roles of the JDK, Gradle, the Gradle wrapper, and JUnit;
- read the main parts of a Gradle Java project;
- run focused and complete build tasks on macOS, Linux, and Windows; and
- use the first failed task to classify a build problem.

This guide has a [complete companion project](../../examples/build-process-and-tools/).
Clone or download the [onboarding repository](https://github.com/CPEN-221/onboarding)
so that the project's directories and wrapper files remain intact.

## 1. One Source File Is Not the Build

A small Java program can be compiled directly:

```sh
javac TransitSummary.java
java TransitSummary
```

`javac` reads Java source and produces JVM class files. `java` launches a JVM and
loads the requested class. This is useful for learning the language, but a course
project also has packages, several source files, tests, external libraries,
compiler options, and generated reports.

For a typical Gradle Java project, the build performs work such as:

1. resolve the requested JDK and external dependencies;
2. compile production source from `src/main/java`;
3. compile test source from `src/test/java` against production code and JUnit;
4. run the tests and record reports; and
5. package production classes and resources in a JAR.

This is not a C-style “compile, then link” pipeline. The ordinary Java build in
this guide has no separate native linker stage. Dependencies are made available on
compile-time and runtime class paths, and the JVM loads classes when needed.

## 2. Meet the Tools

The **JDK** supplies `javac`, `java`, and standard libraries. A Gradle Java
**toolchain** declaration asks build tasks to use a particular Java language
version—in this project, Java 25.

**Gradle** is the build tool. Plugins add conventions and tasks. The `application`
plugin, for example, supplies Java compilation, testing, packaging, and a `run`
task.

The **Gradle wrapper** is the checked-in launch mechanism:

```text
gradlew
gradlew.bat
gradle/wrapper/gradle-wrapper.jar
gradle/wrapper/gradle-wrapper.properties
```

The wrapper properties name a Gradle distribution. The scripts download that
version when needed and then run it. Every contributor therefore invokes the same
Gradle version without maintaining a global installation.

**JUnit** is the testing framework used by the test source. Gradle resolves the
declared JUnit dependencies and its `test` task launches the tests.

> **Design principle: version the build definition and its launcher with the
> source so that the same command reconstructs the same procedure.**

## 3. Read the Project Layout

The companion project has this structure:

```text
build-process-and-tools/
├── build.gradle.kts
├── settings.gradle.kts
├── gradlew
├── gradlew.bat
├── gradle/wrapper/
├── src/main/java/ca/ubc/ece/cpen221/prep/TransitSummary.java
└── src/test/java/ca/ubc/ece/cpen221/prep/TransitSummaryTest.java
```

`settings.gradle.kts` names the Gradle build. `build.gradle.kts` applies plugins
and declares the Java toolchain, repositories, dependencies, compiler options, and
test configuration. The `src/main` and `src/test` directories are separate
**source sets**: production code must not depend on test code.

Here are the central declarations, abbreviated only by omitting blank lines:

```kotlin
plugins {
    application
}

repositories {
    mavenCentral()
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(25)
    }
}

dependencies {
    testImplementation(platform("org.junit:junit-bom:6.1.3"))
    testImplementation("org.junit.jupiter:junit-jupiter")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}
```

The dependency declarations are inputs to the build, not copies of JUnit source
inside the repository. On the first build, Gradle resolves the named modules from
the declared repository and stores them in a local cache.

The full file also names the application entry point and enables all `javac` lint
warnings. Read the checked-in file rather than reproducing it from the excerpt.

<form class="quick-check" data-quick-check data-answer="test-source">
<fieldset>
<legend>Where should <code>TransitSummaryTest.java</code> be placed in this Gradle project?</legend>
<label><input type="radio" name="source-set" value="main-source"> Under <code>src/main/java</code></label>
<label><input type="radio" name="source-set" value="test-source"> Under <code>src/test/java</code></label>
<label><input type="radio" name="source-set" value="build-output"> Under <code>build/classes</code></label>
</fieldset>
<details class="quick-check-explanation">
<summary>Show the explanation</summary>
<p>Test code belongs to the test source set. The <code>build/</code> tree is generated output, not authoritative source.</p>
</details>
</form>

## 4. Run the Wrapper

From the project root on macOS, Linux, or Git Bash:

```sh
./gradlew test
./gradlew run
./gradlew build
```

From Windows PowerShell:

```powershell
.\gradlew.bat test
.\gradlew.bat run
.\gradlew.bat build
```

These are three requested tasks:

- `test` compiles the required sources and runs all configured tests;
- `run` compiles the production source and launches the configured main class;
- `build` performs the standard verification and assembly work, including tests
  and the JAR.

Tasks form a dependency graph. Requesting `build` causes Gradle to run the tasks on
which `build` depends; it does not merely execute every conceivable task in a fixed
list. A task whose inputs and outputs have not changed may be reported as
`UP-TO-DATE`.

The validated `run` task for the companion project printed:

```text
Route 44: ON TIME
```

The validated `test` and `build` tasks both ended with `BUILD SUCCESSFUL`. These
observations were produced with Java 25 and the checked-in Gradle 9.6.1 wrapper.

## 5. Locate the Outputs

Gradle writes generated files under `build/`:

```text
build/
├── classes/
├── libs/build-process-and-tools-1.0.jar
├── reports/tests/test/index.html
└── test-results/test/
```

Class files are JVM instructions produced from source. The JAR is a ZIP-format
archive containing production classes and metadata. Test reports record what the
test task observed.

These outputs can be reconstructed, so they should not normally be committed. The
project's `.gitignore` excludes `build/`. Remove generated output through the
build's narrowly scoped task:

```sh
./gradlew clean
```

`clean` deletes the project build directory. It does not mean “repair the project,”
and it should not be a ritual before every build. An incremental build is normally
faster and is designed to determine which work must be repeated.

<form class="quick-check" data-quick-check data-answer="generated">
<fieldset>
<legend>After a successful build, Git reports hundreds of files under <code>build/</code>. What is the underlying problem?</legend>
<label><input type="radio" name="build-directory" value="source"> Gradle moved the Java source</label>
<label><input type="radio" name="build-directory" value="generated"> Generated output is not being ignored correctly</label>
<label><input type="radio" name="build-directory" value="junit"> JUnit needs to be reinstalled globally</label>
</fieldset>
<details class="quick-check-explanation">
<summary>Show the explanation</summary>
<p>The <code>build/</code> directory is reconstructable output. A suitable <code>.gitignore</code> keeps it out of ordinary commits; <code>gradlew clean</code> removes it locally when needed.</p>
</details>
</form>

## 6. Read a Failure from the First Failed Task

Gradle output names tasks with a leading colon. The first failed task narrows the
search:

| Failed area | Likely evidence | First question |
|---|---|---|
| Wrapper startup | no download, permissions, wrong directory | Are the wrapper files present and is Java available? |
| Dependency resolution | repository/network/module diagnostic | Is the dependency declared correctly, and is the network available? |
| `compileJava` | source path and compiler diagnostic | Which production source violates Java's rules? |
| `compileTestJava` | test source diagnostic | Does test code compile against the current production API and JUnit? |
| `test` | failed test name, expected/actual values, stack trace | What behaviour did the test observe? |
| `jar` or another assembly task | packaging path or duplicate entry | Which declared output could not be assembled? |

Begin with the earliest concrete failure, not the final generic “build failed”
line. A test assertion failure does not mean Java failed to compile. Conversely, a
compile failure means no test involving that source was run.

Useful focused commands include:

```sh
./gradlew tasks
./gradlew test --tests '*TransitSummaryTest'
./gradlew test --stacktrace
```

Use `--stacktrace` when the normal message does not expose the cause. More output
is useful only if you can connect it to the failed task.

### Common misconception

“It works in VS Code” and “the project builds” are not equivalent statements. The
editor can run one class or one test with its own launch configuration. The wrapper
executes the versioned project tasks. Use editor controls for focused investigation
and the wrapper as the shared build interface.

## 7. Practice with One Controlled Failure

In the companion project:

1. run `test`, `run`, and `build` and record the summaries;
2. inspect `build/libs` and the HTML test report;
3. change the expected string in one test from `"ON TIME"` to `"LATE"`;
4. run `test` and identify the first failed task, failed test, expected value, and
   observed value;
5. restore the test and run `test` again; and
6. run `clean`, inspect which directory disappeared, and run `build` once more.

Explain why step 4 is a test failure rather than a compilation failure. Then
explain why step 6 does not delete the source or wrapper.

## 8. Summary

A Java build compiles source, resolves dependencies, compiles and runs tests, and
can package production classes. The JDK performs Java compilation and execution;
Gradle defines and schedules the work; the wrapper pins Gradle; and JUnit supplies
the test model. Source and build definitions are authoritative, while `build/` is
generated. Run the wrapper from the project root and diagnose the first failed
task.

## References

- [Gradle User Manual: Installing Gradle](https://docs.gradle.org/current/userguide/installation.html)
- [Gradle User Manual: Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html)
- [Gradle User Manual: Building Java and JVM Projects](https://docs.gradle.org/current/userguide/building_java_projects.html)
- [Gradle User Manual: The Java Plugin](https://docs.gradle.org/current/userguide/java_plugin.html)
- [Gradle User Manual: Build Lifecycle](https://docs.gradle.org/current/userguide/build_lifecycle.html)
- [JUnit 6.1.3 User Guide](https://docs.junit.org/6.1.3/)
