# Software to Install

By the end, you should be able to:

- install a Java 25 **JDK**, Git, and Visual Studio Code on macOS, Linux, or
  Windows;
- explain why course projects use the Gradle wrapper instead of a separately
  installed Gradle command;
- verify which program and version a terminal will run; and
- diagnose the common case in which an installation succeeded but the terminal
  still finds an older program.

Use an account with permission to install software. If your computer is managed by
an employer or school and you cannot install a required tool, ask the course staff
before changing security settings.

## 1. What You Need

Install these components before beginning the other preparation guides:

| Component | Course choice | What it supplies |
|---|---|---|
| Java Development Kit | Eclipse Temurin 25 | `java`, `javac`, and the standard Java libraries |
| Git | A current Git 2 release | Local version control and communication with GitHub |
| Visual Studio Code | Current stable release | Editor, integrated terminal, debugger, and extension host |
| Gradle | The wrapper included in each project | A reproducible build, test, and packaging command |

A **JDK** is a Java Development Kit. It includes the Java launcher and the compiler.
A runtime-only installation is insufficient: `java` might work while `javac` is
missing.

Gradle is the unusual row. When a project contains `gradlew`, `gradlew.bat`, and
`gradle/wrapper/`, Gradle's own installation guide says that no separate Gradle
installation is required. The first wrapper run downloads the version named by the
project. CPEN 221 projects use this mechanism, so `gradle test` is not the course
command.

A project should declare the tool version it needs instead of relying on whichever
version happens to be installed globally.

## 2. Identify Your Operating System and Processor

Choose instructions for the operating system on which you will actually edit and
run the project. A Linux virtual machine inside Windows is a separate environment;
software installed only in Windows is not automatically installed inside it.

You may also have to choose a processor architecture:

- `aarch64` or `arm64` is used by Apple silicon Macs and some Windows/Linux
  computers;
- `x64` or `x86_64` is used by most Intel and AMD computers.

On macOS, **Apple menu → About This Mac** names the chip. On Windows, **Settings →
System → About → System type** reports the architecture. On Linux, `uname -m`
reports it. Choose the installer matching that result.

## 3. macOS

### Install Java 25

Open the [Eclipse Temurin 25 downloads](https://adoptium.net/temurin/releases/?version=25),
select macOS and your architecture, and download the JDK `.pkg` installer. Run the
installer. The package format registers the JDK in the standard macOS location.

Open a **new** terminal and run:

```sh
java -version
javac -version
/usr/libexec/java_home -V
```

The first two commands must report major version `25`. The last command lists the
JDKs macOS knows about. If an older JDK is selected, set `JAVA_HOME` for Java 25 in
your shell configuration; do not delete another JDK that other software may use.

### Install Git

First try:

```sh
git --version
```

If that opens an Apple developer-tools installer, completing that installer gives
you Git. You may instead use one of the current installers linked from the official
[Git installation page](https://git-scm.com/install/). If you already manage
software with Homebrew, `brew install git` is also an option. The course does not
require Homebrew.

### Install VS Code

Download the macOS build from the [official VS Code instructions](https://code.visualstudio.com/docs/setup/mac),
open the `.dmg`, and drag Visual Studio Code to **Applications**. In VS Code, open
the Command Palette and run **Shell Command: Install 'code' command in PATH**. Open
a new terminal before testing `code --version`.

## 4. Linux

Linux distributions use different package formats. Use the repository instructions
for your distribution rather than pasting a command intended for another one.

### Install Java 25

Adoptium publishes signed DEB, RPM, and APK packages. Follow its
[Linux package instructions](https://adoptium.net/installation/) for your
distribution and choose the Temurin 25 JDK package, not a JRE package. Then run:

```sh
java -version
javac -version
command -v java
```

If several Java versions are installed, use your distribution's alternatives
mechanism to select Java 25. Both `java` and `javac` must select version 25.

### Install Git and VS Code

Install Git through your distribution's package manager, following the Linux link
on the [official Git installation page](https://git-scm.com/install/). For VS Code,
use Microsoft's [Linux installation instructions](https://code.visualstudio.com/docs/setup/linux).
They provide `.deb` and `.rpm` packages and distribution-specific repository
instructions. A repository installation has the advantage that normal system
updates can update VS Code.

Verify:

```sh
git --version
code --version
```

## 5. Windows

Use a normal PowerShell terminal for installation and verification. The later
command-line guide shows both PowerShell and Git Bash commands.

### Install Java 25

On a current Windows system with `winget`, run:

```powershell
winget install EclipseAdoptium.Temurin.25.JDK
```

The command is published by Adoptium. Its Windows MSI installer is an equivalent
graphical option. Accept the options that add Java to `PATH`; setting `JAVA_HOME`
is also useful for build tools.

Close all open terminals, open a new PowerShell window, and run:

```powershell
java -version
javac -version
where.exe java
```

### Install Git

Download **Git for Windows** through the [official Git installation page](https://git-scm.com/install/).
The installer includes Git Bash and Git Credential Manager. Keeping the default
options is suitable for this material. After installation, a new terminal should
accept `git --version`.

### Install VS Code

Use the **User Installer** described in Microsoft's
[Windows installation instructions](https://code.visualstudio.com/docs/setup/windows).
It does not normally require administrator rights and adds `code` to `PATH`. Close
and reopen the terminal, then run `code --version`.

## 6. Verify the Complete Toolchain

Open a fresh terminal and run the four version checks:

```text
java -version
javac -version
git --version
code --version
```

The exact patch numbers will change. The properties that matter are:

- both Java commands report major version 25;
- Git reports a version rather than “command not found”;
- VS Code reports a version; and
- the paths point to the installations you intended.

In a downloaded course project, verify Gradle from the project's top-level
directory:

```sh
./gradlew --version
```

In Windows PowerShell, use:

```powershell
.\gradlew.bat --version
```

The first run may download Gradle and therefore needs a network connection. A later
run can use the cached distribution. Do not replace the wrapper files merely
because the pinned version differs from the newest Gradle release.

<form class="quick-check" data-quick-check data-answer="wrapper">
<fieldset>
<legend>A course repository contains <code>gradlew</code> and <code>gradlew.bat</code>. What should you install globally before running its build?</legend>
<label><input type="radio" name="gradle-install" value="latest"> The newest global Gradle release</label>
<label><input type="radio" name="gradle-install" value="wrapper"> No global Gradle; install Java 25 and run the wrapper</label>
<label><input type="radio" name="gradle-install" value="jre"> A Java runtime without a compiler</label>
</fieldset>
<details class="quick-check-explanation">
<summary>Show the explanation</summary>
<p>The checked-in wrapper downloads and runs the Gradle version declared by the project. It still needs a suitable JDK, which is why both <code>java</code> and <code>javac</code> are verified.</p>
</details>
</form>

## 7. Diagnose a Version Mismatch

Installing a program does not change terminals that are already running. Start by
closing and reopening the terminal and VS Code. If an older Java still appears,
locate the executable:

```sh
command -v java       # macOS or Linux
```

```powershell
where.exe java        # Windows
```

`PATH` is an ordered list of directories. The shell chooses the first matching
program. A stale Java directory earlier in `PATH` can therefore win even after Java
25 is installed. `JAVA_HOME` should name the JDK directory, while `PATH` should
contain that JDK's `bin` directory. Do not make random path edits: first record the
observed paths and compare them with the installed JDK location.

A second common failure is opening a project at the wrong level. The directory you
open should contain `settings.gradle.kts`, `build.gradle.kts`, and the wrapper
scripts. If those files are in a child directory, the terminal is not yet at the
project root.

<form class="quick-check" data-quick-check data-answer="path">
<fieldset>
<legend>You installed Java 25, but <code>java -version</code> still reports Java 21. What should you inspect first?</legend>
<label><input type="radio" name="java-mismatch" value="source"> The Java source file</label>
<label><input type="radio" name="java-mismatch" value="path"> The executable selected through <code>PATH</code></label>
<label><input type="radio" name="java-mismatch" value="github"> Your GitHub repository visibility</label>
</fieldset>
<details class="quick-check-explanation">
<summary>Show the explanation</summary>
<p>The shell may still select an older executable. A fresh terminal plus <code>command -v java</code> or <code>where.exe java</code> reveals what is actually being run.</p>
</details>
</form>

## 8. Installation Check

Before moving on, collect the output from all version commands in one text file.
Then answer:

1. Which JDK distribution, major version, and architecture did you install?
2. Which path contains the `java` executable selected by your terminal?
3. Does `javac -version` agree with `java -version`?
4. In a project with wrapper files, which command reports the pinned Gradle
   version on your operating system?

If you ask for installation help, include the operating system, processor
architecture, commands entered, and complete output. “Java does not work” hides the
evidence needed to distinguish a missing executable from a wrong version or wrong
directory.

## 9. Summary

The required base is a Java 25 JDK, Git, and VS Code. A course project supplies its
own Gradle wrapper, so a global Gradle installation is unnecessary. Verification is
part of installation: check both Java tools, Git, VS Code, and the project wrapper
from a new terminal. When a version is wrong, identify the executable selected by
`PATH` before changing configuration.

## References

- [Adoptium: Install Eclipse Temurin](https://adoptium.net/installation/)
- [Adoptium: Eclipse Temurin 25 releases](https://adoptium.net/temurin/releases/?version=25)
- [Gradle User Manual: Installing Gradle](https://docs.gradle.org/current/userguide/installation.html)
- [Git: Install](https://git-scm.com/install/)
- [Visual Studio Code setup for macOS](https://code.visualstudio.com/docs/setup/mac)
- [Visual Studio Code setup for Linux](https://code.visualstudio.com/docs/setup/linux)
- [Visual Studio Code setup for Windows](https://code.visualstudio.com/docs/setup/windows)
