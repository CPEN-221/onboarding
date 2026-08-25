#!/usr/bin/env python3
"""Validate the concrete Gradle and Git workflows used by the preparation guides."""

from __future__ import annotations

from pathlib import Path
import os
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parent.parent
PROJECT = ROOT / "examples" / "build-process-and-tools"


def run(
    arguments: list[str], *, cwd: Path, expected_output: str | None = None
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(arguments, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(
            f"Command failed: {' '.join(arguments)}\n{result.stdout}{result.stderr}"
        )
    if expected_output is not None and result.stdout != expected_output:
        raise SystemExit(
            f"Unexpected output from {' '.join(arguments)}\n"
            f"expected: {expected_output!r}\nobserved: {result.stdout!r}"
        )
    return result


def java_executable() -> str:
    java_home = os.environ.get("JAVA_HOME")
    if java_home:
        candidate = Path(java_home) / "bin" / "java"
        if candidate.exists():
            return str(candidate)
    java = shutil.which("java")
    if java is None:
        raise SystemExit("Cannot find Java; install a Java 25 JDK")
    return java


def validate_java() -> None:
    result = run([java_executable(), "-version"], cwd=ROOT)
    version_text = result.stdout + result.stderr
    match = re.search(r'version "(\d+)', version_text)
    if not match or match.group(1) != "25":
        raise SystemExit(f"Java 25 is required; observed:\n{version_text}")


def validate_gradle_project() -> None:
    wrapper = str(PROJECT / "gradlew")
    version = run([wrapper, "--version", "--no-daemon"], cwd=PROJECT)
    if "Gradle 9.6.1" not in version.stdout:
        raise SystemExit(f"Expected Gradle 9.6.1 wrapper:\n{version.stdout}")

    run([wrapper, "clean", "test", "build", "--no-daemon", "--console=plain"], cwd=PROJECT)
    application = run(
        [wrapper, "run", "--no-daemon", "--console=plain", "--quiet"], cwd=PROJECT
    )
    if application.stdout != "Route 44: ON TIME\n":
        raise SystemExit(f"Unexpected application output: {application.stdout!r}")

    jar = PROJECT / "build" / "libs" / "build-process-and-tools-1.0.jar"
    report = PROJECT / "build" / "reports" / "tests" / "test" / "index.html"
    if not jar.is_file() or not report.is_file():
        raise SystemExit("Gradle build did not produce the documented JAR and test report")
    run([wrapper, "clean", "--no-daemon", "--console=plain"], cwd=PROJECT)


def validate_git_workflow() -> None:
    git = shutil.which("git")
    if git is None:
        raise SystemExit("Cannot find Git")

    with tempfile.TemporaryDirectory(prefix="onboarding-git-") as temporary:
        repository = Path(temporary)
        run([git, "init", "-b", "main"], cwd=repository)
        run([git, "config", "user.name", "Guide Validator"], cwd=repository)
        run([git, "config", "user.email", "validator@example.invalid"], cwd=repository)

        source = repository / "TransitSummary.java"
        source.write_text("final class TransitSummary { }\n", encoding="utf-8")
        status = run([git, "status", "--short"], cwd=repository)
        if status.stdout != "?? TransitSummary.java\n":
            raise SystemExit(f"Unexpected untracked state: {status.stdout!r}")

        run([git, "add", "TransitSummary.java"], cwd=repository)
        staged = run([git, "diff", "--staged", "--name-only"], cwd=repository)
        if staged.stdout != "TransitSummary.java\n":
            raise SystemExit(f"Unexpected staged state: {staged.stdout!r}")

        run([git, "commit", "-m", "Add transit summary"], cwd=repository)
        source.write_text("final class TransitSummary { /* changed */ }\n", encoding="utf-8")
        run([git, "restore", "TransitSummary.java"], cwd=repository)
        clean = run([git, "status", "--porcelain"], cwd=repository)
        if clean.stdout:
            raise SystemExit(f"Git workflow did not return to a clean state: {clean.stdout!r}")


def main() -> None:
    validate_java()
    validate_gradle_project()
    validate_git_workflow()
    print("Observed Java 25 and Gradle 9.6.1; tests, run, build, JAR, and report matched the guide.")
    print("Observed the documented Git untracked, staged, committed, restored, and clean states.")


if __name__ == "__main__":
    main()
