# Installing and Using Visual Studio Code

For CPEN 221, open the complete Gradle project in Visual Studio Code (VS Code),
not an individual Java file. The Java and Gradle extensions then read the build,
find the source and test directories, and use the project's Java configuration.

By the end, you should be able to:

- install VS Code and the extensions needed for a CPEN 221 Java project;
- open a repository at its project root and select Java 25;
- edit, navigate, run, test, and debug Java code;
- use the integrated terminal and built-in Git interface without treating them as
  separate project states; and
- distinguish required support from optional GitHub conveniences.

## 1. Install the Editor

Follow the operating-system steps in [Software to Install](../software-to-install/)
or the official VS Code setup page for [macOS](https://code.visualstudio.com/docs/setup/mac),
[Linux](https://code.visualstudio.com/docs/setup/linux), or
[Windows](https://code.visualstudio.com/docs/setup/windows). Enable the `code`
command, then verify it in a new terminal:

```text
code --version
```

VS Code updates independently of your projects. Installing an update does not
change the Java version declared by a Gradle build.

## 2. Install a Small Extension Set

Open **Extensions** and install:

1. **Extension Pack for Java**, published by Microsoft;
2. **Gradle for Java**, published by Microsoft.

The Java pack includes language support, a debugger, a test runner, and project
management. Gradle for Java imports Gradle projects and exposes their tasks. Check
the publisher before installing: similarly named extensions are not necessarily
the same software.

Git support is built into VS Code and uses the Git executable installed on your
computer. No Git extension is required for staging, committing, branching,
pulling, or pushing. **GitHub Pull Requests and Issues**, published by GitHub, is an
optional extension for reviewing pull requests and issues inside the editor. It is
not required for the basic Git workflow in this preparation material.

Avoid installing a large collection of extensions at the outset. Extensions can
add commands, formatters, authentication prompts, and generated files. Begin with
the required set so that a problem has fewer possible causes.

<form class="quick-check" data-quick-check data-answer="built-in">
<fieldset>
<legend>Which extension is required to make basic Git staging and commits available in VS Code?</legend>
<label><input type="radio" name="git-extension" value="built-in"> None; Git support is built in and uses the installed Git program</label>
<label><input type="radio" name="git-extension" value="java"> Extension Pack for Java</label>
<label><input type="radio" name="git-extension" value="pull-request"> GitHub Pull Requests and Issues</label>
</fieldset>
<details class="quick-check-explanation">
<summary>Show the explanation</summary>
<p>VS Code includes its Git source-control provider. The GitHub extension adds pull-request and issue workflows, while the Java pack supplies Java language tooling.</p>
</details>
</form>

## 3. Open the Folder, Not an Isolated File

Clone or download a project, then open the directory containing these files. To follow
along, clone the onboarding repository, which holds these guides and their example
projects:

```sh
git clone https://github.com/CPEN-221/onboarding.git
cd onboarding/examples/build-process-and-tools
ls
```

You should see:

```text
README.md
build.gradle.kts
gradle
gradlew
gradlew.bat
settings.gradle.kts
src
```

From a terminal already in that directory, run:

```sh
code .
```

The dot means the current directory. Alternatively, use **File → Open Folder**.
The folder shown at the top of the Explorer should be the project root.

Opening only `TransitBoard.java` deprives the Java extension of the build file,
test source set, and dependency declarations. A source file may still be editable,
but the editor cannot accurately reproduce the project build.

VS Code may display a **Workspace Trust** prompt. A repository can contain tasks,
debug configurations, and extension recommendations that execute code. Trust a
course repository obtained from its official location after confirming that you
opened the intended folder. Do not automatically trust an unrelated archive.

The build definition specifies the project. Configure the editor to read it.

## 4. Confirm Java 25 and Import the Build

After the extensions start, VS Code shows Java's progress in the status bar. Let
the initial import finish. The first Gradle wrapper run may download Gradle and
test dependencies.

Open the Command Palette and run **Java: Configure Java Runtime**. Confirm that the
project resolves a Java 25 JDK. The editor can know about several JDKs; the one
used for language services and the one requested by the Gradle toolchain should
both support the project.

Also open VS Code's terminal and run:

```text
java -version
javac -version
```

Then, from the project root:

```sh
./gradlew test
```

or in Windows PowerShell:

```powershell
.\gradlew.bat test
```

The editor can run a selected class or test. The wrapper runs the versioned task
that the project and continuous-integration service share.

If imports stay red after a successful command-line build, use **Java: Clean Java
Language Server Workspace** and allow the project to re-import. If the wrapper
also fails, fix that build failure before resetting editor caches.

## 5. Edit and Navigate Java

The Java language server can:

- complete names and show method parameters;
- jump to a declaration or find references;
- report compiler diagnostics while you edit;
- rename a symbol across the project; and
- organize imports.

Treat automated edits as proposed changes. Review the diff after a rename or
import reorganization. Compilation is still required: a diagnostic underline can
lag behind the file or omit a build-specific check.

The Explorer reflects the filesystem. Java source belongs under
`src/main/java`, while tests belong under `src/test/java`. Package declarations
and directory names should match. Do not move a Java file merely to make the
Explorer look tidy; use the project's layout.

## 6. Run and Test

The **Testing** view discovers JUnit tests after the Gradle project imports. It can
run one test or display a failure beside its source. The Java editor also offers
Run and Debug links above runnable classes and tests.

Use those controls for a focused investigation, then run the project command
before considering the work complete:

```sh
./gradlew test
```

The wrapper may run more checks than the selected editor test. It also records the
same task failure that another developer or the CI service will see.

<form class="quick-check" data-quick-check data-answer="wrapper-test">
<fieldset>
<legend>One JUnit test passes when launched from the editor. What should you run before concluding that the project passes?</legend>
<label><input type="radio" name="test-authority" value="reload"> Reload the VS Code window</label>
<label><input type="radio" name="test-authority" value="wrapper-test"> The project's <code>gradlew test</code> command</label>
<label><input type="radio" name="test-authority" value="commit"> <code>git commit</code></label>
</fieldset>
<details class="quick-check-explanation">
<summary>Show the explanation</summary>
<p>The editor run is useful but focused. The wrapper executes the versioned build and its complete test task, which is the shared project interface.</p>
</details>
</form>

## 7. Debug a Failing Test

A debugger pauses a running program and lets you inspect its current state. To
investigate a failure:

1. reproduce it with a small test;
2. place a breakpoint on an executable line before the failure;
3. choose **Debug Test**;
4. inspect local variables and the call stack;
5. use **Step Over** for the next line or **Step Into** to enter a method call; and
6. stop, edit, and rerun the test.

The debugger shows one execution. It does not prove a rule about every execution,
and it does not replace a test assertion. Record the observation that changed your
explanation, then encode the required behaviour in a test where appropriate.

### Debugger Changes Do Not Edit the Source

“The debugger changed my code” is usually a confusion between state and source.
Editing a variable in a debug session changes that running process, not the Java
source. The change disappears when the process ends unless you also edit and save
the source file.

## 8. Use the Integrated Terminal

Open **Terminal → New Terminal**. VS Code normally starts it at the workspace root,
but verify:

```sh
pwd
ls
```

The integrated terminal can run the same `git`, `java`, and wrapper commands as an
external terminal. It is not an emulator with a separate copy of the repository.
Changes made by a terminal command appear in the Explorer and Source Control view.

On Windows, choose PowerShell or Git Bash from the terminal-profile menu and stay
aware of which syntax you are using. The project wrapper provides a POSIX script
for Git Bash and a `.bat` script for PowerShell.

## 9. Use Source Control Without Hiding the Model

The Source Control view displays changed files. Selecting a file opens its diff.
The plus button stages a file; the Commit action creates a local commit from staged
changes; synchronization communicates with a remote.

These actions operate on the same Git repository as terminal commands. Run `git
status` at any time to see the underlying state. Learn the commands in
[Git and GitHub](../git-and-github/) even if you prefer the interface: command
output is easier to share exactly when something goes wrong.

Do not use **Discard Changes** casually. For an uncommitted file, discarding can
remove work that Git has no snapshot of. Inspect the diff and know which version
will replace it.

## 10. A Setup Exercise

Open the companion Gradle project from the build-process guide and complete this
checklist:

1. confirm the Explorer root contains both Gradle build files and wrapper scripts;
2. confirm Java 25 under **Java: Configure Java Runtime**;
3. locate the main class and use **Go to Definition** on one method call;
4. run all tests in the Testing view;
5. run the wrapper `test` task in the integrated terminal;
6. introduce a failing expected value, debug that test, then undo the edit; and
7. open Source Control and verify that your repository is clean again.

Explain any difference between the editor test result and the wrapper output. If
there is no difference, state which two independent observations agreed.

## 11. Summary

Install the Java and Gradle extensions, while relying on VS Code's built-in Git
support for ordinary version control. Open the project root as a folder, select
Java 25, let Gradle import the build, and use the editor for navigation and focused
runs. Use the checked-in wrapper for the complete build and tests.

## References

- [Visual Studio Code: Getting Started with Java](https://code.visualstudio.com/docs/java/java-tutorial)
- [Visual Studio Marketplace: Extension Pack for Java](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-java-pack)
- [Visual Studio Marketplace: Gradle for Java](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-gradle)
- [Visual Studio Code: Source Control](https://code.visualstudio.com/docs/sourcecontrol/overview)
- [Visual Studio Code: Terminal Basics](https://code.visualstudio.com/docs/terminal/basics)
- [Visual Studio Marketplace: GitHub Pull Requests and Issues](https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-pull-request-github)
