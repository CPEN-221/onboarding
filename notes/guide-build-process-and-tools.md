# The Build Process and Tools

A Java project usually contains more than one source file. It may also depend on
libraries, tests, compiler options, resources, and packaging instructions. The
**build process** turns those inputs into compiled code, test results, and other
outputs. A build tool records and runs that process.

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

## 1. What the Build Includes

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

The build definition records this work as part of the project. It specifies the
inputs, the tools and versions to use, and the relationships among build steps.
Generated class files, reports, and archives are outputs. If the outputs disappear,
the build should be able to reconstruct them from the source and build definition.

## 2. The Tools and Their Roles

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

Keep the build definition and wrapper with the source. A fresh clone can then use
the same command and Gradle version as every other clone.

## 3. Build Tools and Why We Use Gradle

Build automation predates Java, and several tools use different models for the
same general problem:

- `make` defines targets, their prerequisites, and the commands that produce
  them. It uses file timestamps to avoid rebuilding targets whose inputs have not
  changed. It works with many languages, but dependency download and Java project
  layout require additional conventions or tools.
- Maven describes a project in `pom.xml` and supplies a standard lifecycle with
  phases such as `compile`, `test`, and `package`. Its fixed conventions make many
  Java builds similar to one another.
- Gradle describes a graph of **tasks**. Plugins supply standard tasks and project
  conventions, while Groovy or Kotlin build scripts can configure or extend them.

CPEN 221 uses Gradle. This is a course choice, not a claim that Gradle is the best
tool for every project. The important ideas transfer: a build tool records the
procedure, tracks dependencies among steps, and decides which work is required for
the requested output.

Gradle handles one invocation in three phases. It first initializes the build and
finds its projects. It then evaluates the build scripts and constructs the task
graph. Finally, it executes the requested tasks and the tasks they depend on. This
explains why `./gradlew build` can run compilation and tests even though the command
names only `build`.

Gradle also resolves external libraries. A declaration such as
`org.junit.jupiter:junit-jupiter` identifies a module, while the JUnit bill of
materials used below supplies compatible versions. Gradle searches the declared
repositories, downloads the required artifacts and their declared dependencies,
and keeps them in a local cache. A first build may therefore need network access;
later builds can often reuse the cache.

## 4. The Gradle Project Layout

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

## 5. Run Gradle Through the Wrapper

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
which `build` depends. Gradle does not execute every task defined by every plugin.
A task whose inputs and outputs have not changed may be reported as `UP-TO-DATE`.

The validated `run` task for the companion project printed:

```text
Route 44: ON TIME
```

The validated `test` and `build` tasks both ended with `BUILD SUCCESSFUL`. These
observations were produced with Java 25 and the checked-in Gradle 9.6.1 wrapper.

## 6. Locate the Outputs

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

## 7. Read a Failure from the First Failed Task

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

### The Editor and the Build Can Run Different Work

“It works in VS Code” and “the project builds” are not equivalent statements. The
editor can run one class or one test with its own launch configuration. The wrapper
executes the versioned project tasks. Use editor controls for focused investigation
and the wrapper as the shared build interface.

## 8. Practice with One Controlled Failure

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

## 9. Summary

A Java build compiles source, resolves dependencies, compiles and runs tests, and
can package production classes. The JDK performs Java compilation and execution;
Gradle defines and schedules the work; the wrapper pins Gradle; and JUnit supplies
the test model. Source and build definitions are authoritative, while `build/` is
generated. Run the wrapper from the project root and diagnose the first failed
task.

## References

- [GNU Make Manual: What a Rule Looks Like](https://www.gnu.org/software/make/manual/html_node/Rule-Introduction.html)
- [Apache Maven: Introduction to the Build Lifecycle](https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html)
- [Gradle User Manual: Installing Gradle](https://docs.gradle.org/current/userguide/installation.html)
- [Gradle User Manual: Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html)
- [Gradle User Manual: Building Java and JVM Projects](https://docs.gradle.org/current/userguide/building_java_projects.html)
- [Gradle User Manual: The Java Plugin](https://docs.gradle.org/current/userguide/java_plugin.html)
- [Gradle User Manual: Build Lifecycle](https://docs.gradle.org/current/userguide/build_lifecycle.html)
- [JUnit 6.1.3 User Guide](https://docs.junit.org/6.1.3/)
