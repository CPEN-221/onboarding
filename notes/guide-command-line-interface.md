# Using the Command Line Interface

You have downloaded a project and can see it in a file browser. The instructions
say to run `./gradlew test`, but the terminal replies that no such file exists.
Nothing is wrong with Gradle: the terminal is in the wrong directory.

This small failure captures why command-line fluency matters. A command runs in a
specific working directory, with specific arguments, and produces evidence you can
read and share.

By the end, you should be able to:

- identify the shell, prompt, command, arguments, and working directory;
- navigate a project using absolute and relative paths;
- inspect and perform basic file operations without losing track of their effects;
- run a program or Gradle wrapper from the project root; and
- preserve complete command output when diagnosing a failure.

## 1. Terminal, Shell, and Prompt

A **terminal** is the window or panel that displays text input and output. A
**shell** is the program inside it that reads commands. macOS commonly uses Zsh,
Linux commonly uses Bash, and Windows commonly uses PowerShell. Git for Windows
also supplies Git Bash.

VS Code's integrated terminal runs one of these real shells. Open it with **Terminal
→ New Terminal**. It normally starts in the folder open in VS Code.

A shell displays a **prompt** when it is ready. Prompts vary:

```text
alex@laptop transit-board %
PS C:\Users\alex\transit-board>
```

Instructions often show a leading `$` or `>` to represent that prompt:

```text
$ git status
```

Type only `git status`. The prompt is not part of the command.

Commands consist of a program name followed by arguments:

```text
git status --short
```

Here `git` is the program. `status` selects an operation and `--short` requests a
compact display. Spaces separate arguments. The shell then finds `git` using
`PATH`, starts it in the current working directory, and prints its output.

## 2. Know Where You Are

We will use this project tree:

```text
transit-board/
├── build.gradle.kts
├── gradlew
├── gradlew.bat
├── settings.gradle.kts
└── src/
    ├── main/java/TransitBoard.java
    └── test/java/TransitBoardTest.java
```

On macOS, Linux, or Git Bash:

```sh
pwd
ls
```

In PowerShell:

```powershell
Get-Location
Get-ChildItem
```

`pwd` prints the **working directory**. `ls` lists its contents. PowerShell accepts
`pwd` and `ls` as interactive aliases, but its full command names make scripts
clearer.

The wrapper command works only if the listing includes `gradlew` or
`gradlew.bat`. If the listing shows a directory named `transit-board` instead, move
into it:

```sh
cd transit-board
```

Then list again. Checking after navigation is quick and prevents a long chain of
commands from operating in the wrong place.

<form class="quick-check" data-quick-check data-answer="parent">
<fieldset>
<legend>Your current directory contains a folder named <code>transit-board</code>, but no <code>gradlew</code>. What is the likely next command?</legend>
<label><input type="radio" name="working-directory" value="parent"> <code>cd transit-board</code></label>
<label><input type="radio" name="working-directory" value="delete"> <code>rm transit-board</code></label>
<label><input type="radio" name="working-directory" value="run"> <code>./gradlew test</code></label>
</fieldset>
<details class="quick-check-explanation">
<summary>Show the explanation</summary>
<p>The project root is one level below the current directory. Move there, confirm that the wrapper and build files are present, and then run the build.</p>
</details>
</form>

## 3. Read Paths

A path identifies a location in the filesystem. An **absolute path** begins from a
filesystem root:

```text
/Users/alex/cpen221/transit-board        macOS
/home/alex/cpen221/transit-board         Linux
C:\Users\alex\cpen221\transit-board      Windows
```

A **relative path** begins from the current directory. These names have special
meanings:

- `.` is the current directory;
- `..` is its parent directory;
- `src/main` descends through two child directories; and
- `../other-project` goes to the parent, then into a sibling.

Suppose the current directory is `transit-board/src/main`. `cd ../..` returns to
`transit-board`. `cd /` does not: it jumps to the filesystem root.

On macOS and Linux, a path beginning with `/` is absolute. On Windows, a drive
letter and backslash commonly begin an absolute path. Both Git Bash and many Java
tools display Windows paths using forward slashes. Read the shell's convention
rather than mixing syntaxes within one command.

Quote a path containing spaces:

```sh
cd "CPEN 221/transit-board"
```

Tab completion is safer than typing a long path. Enter a few characters and press
Tab. The shell completes an unambiguous name or offers choices.

> **Design principle: establish and verify the working directory before running a
> project command.**

## 4. Inspect Before You Change

The following table uses POSIX commands, which work in macOS, Linux, and Git Bash,
and gives the corresponding PowerShell command.

| Purpose | macOS/Linux/Git Bash | PowerShell |
|---|---|---|
| Print working directory | `pwd` | `Get-Location` |
| List files | `ls` | `Get-ChildItem` |
| Include hidden files | `ls -la` | `Get-ChildItem -Force` |
| Change directory | `cd path` | `Set-Location path` |
| Create a directory | `mkdir notes` | `New-Item -ItemType Directory notes` |
| Copy a file | `cp a.txt b.txt` | `Copy-Item a.txt b.txt` |
| Move or rename | `mv old.txt new.txt` | `Move-Item old.txt new.txt` |
| Remove one file | `rm draft.txt` | `Remove-Item draft.txt` |
| Display a short text file | `cat README.md` | `Get-Content README.md` |

Before a copy, move, or removal, use `pwd` and `ls` to resolve both source and
destination. Shell removal normally bypasses a graphical trash folder. This guide
therefore does not ask you to use recursive deletion. Generated Gradle files should
be removed with `./gradlew clean`, which has a narrowly defined target.

Wildcards such as `*.java` are expanded by many shells. They are convenient, but
they can select more files than you intended. Inspect the matching names before
using a wildcard in a command that modifies or removes files.

## 5. Run Programs from the Project Root

In macOS, Linux, or Git Bash, `./` explicitly names a program in the current
directory:

```sh
./gradlew test
```

The shell does not usually search the current directory for security reasons, so
`gradlew test` may fail even when `gradlew` is visible in `ls`.

PowerShell runs the Windows script with:

```powershell
.\gradlew.bat test
```

In both cases, `test` is an argument passed to the wrapper. The wrapper launches
the project's pinned Gradle version, which reads the build files and runs the test
task.

The same principle applies to Java's tools:

```sh
javac Hello.java
java Hello
```

The first command compiles source. The second asks the Java launcher to find and
run the named class. A Gradle project normally supplies these invocations through
its build, so prefer the wrapper command documented by that project.

<form class="quick-check" data-quick-check data-answer="dot-slash">
<fieldset>
<legend>On macOS or Linux, <code>ls</code> shows <code>gradlew</code> in the current directory. Why does the course command begin with <code>./</code>?</legend>
<label><input type="radio" name="wrapper-path" value="java"> It selects Java 25</label>
<label><input type="radio" name="wrapper-path" value="dot-slash"> It names the wrapper file in the current directory</label>
<label><input type="radio" name="wrapper-path" value="remote"> It sends the command to GitHub</label>
</fieldset>
<details class="quick-check-explanation">
<summary>Show the explanation</summary>
<p><code>.</code> denotes the current directory. The slash joins it to the executable file name, avoiding reliance on the shell's program-search path.</p>
</details>
</form>

## 6. Read Output as Evidence

A successful command can print nothing, and a failed command can print several
screenfuls. The prompt returning only means the process ended. Check the final
summary and do not infer success from the presence of some green text near the top.

For a build failure, preserve:

1. the command you entered;
2. the working directory;
3. the first task reported as failed;
4. the complete diagnostic, including lines following “Caused by”; and
5. any changes made immediately before the failure.

Use the terminal's scrollback or copy the output as text. Screenshots often cut off
the command, paths, or final cause. Do not post passwords, access tokens, or private
repository URLs containing embedded credentials.

Shells maintain command history. Press Up to recall a command, edit only the needed
argument, and run it again. This reduces transcription errors and makes an
experiment reproducible.

## 7. Interrupt, Do Not Close Blindly

Some commands keep running: a web server waits for requests, and a program may be
stuck in a loop. In a terminal, `Ctrl+C` usually asks the foreground process to
stop. It is not the normal copy shortcut inside many terminals. VS Code uses the
platform's terminal copy shortcuts and can copy a selection through its context
menu.

If `Ctrl+C` does not return a prompt, wait for the program's shutdown message and
try once more. Closing the entire terminal loses context that might help diagnose
the program.

## 8. A Navigation Exercise

Create a disposable practice directory somewhere you can identify clearly. Then:

1. print the working directory;
2. create `cli-practice` and enter it;
3. create `src` and `notes` inside it;
4. list the resulting tree;
5. move from `src` to its sibling `notes` using `..`;
6. return to `cli-practice`; and
7. explain, before acting, how you would remove the practice directory safely.

Do not memorize command lists in isolation. For each step, state the location before
and after the command. The transferable skill is maintaining a correct model of
where the shell is and what a path will select.

### Common misconception

The file explorer and terminal are not separate filesystems. They are two views of
the same files. A change made in one should appear in the other after refresh. If
it does not, compare their full paths: you probably opened two similarly named
directories or two copies of the repository.

## 9. Summary

The terminal hosts a shell, and the shell runs a command in a working directory.
Paths may be absolute or relative; `.`, `..`, quoting, and tab completion make
relative navigation reliable. Inspect before modifying files, run the Gradle
wrapper from the project root, and preserve complete commands and output as
diagnostic evidence.

## References

- [Visual Studio Code: Terminal Basics](https://code.visualstudio.com/docs/terminal/basics)
- [GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)
- [Microsoft Learn: About aliases in PowerShell](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_aliases)
