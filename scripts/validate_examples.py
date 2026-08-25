#!/usr/bin/env python3
"""Compile and run every complete example with Java 25."""

from __future__ import annotations

from pathlib import Path
import os
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"


def java_tool(name: str) -> str:
    java_home = os.environ.get("JAVA_HOME")
    if java_home:
        candidate = Path(java_home) / "bin" / name
        if candidate.exists():
            return str(candidate)
    found = shutil.which(name)
    if found is None:
        raise SystemExit(f"Cannot find {name}; install a Java 25 JDK")
    return found


JAVA = java_tool("java")
JAVAC = java_tool("javac")


def command(arguments: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(arguments, cwd=cwd, capture_output=True, text=True)


def expect_success(
    arguments: list[str], expected_output: str, *, cwd: Path | None = None
) -> None:
    result = command(arguments, cwd=cwd)
    if result.returncode != 0:
        raise SystemExit(
            f"Command failed: {' '.join(arguments)}\n{result.stdout}{result.stderr}"
        )
    if result.stdout != expected_output:
        raise SystemExit(
            f"Unexpected output from {' '.join(arguments)}\n"
            f"expected: {expected_output!r}\nobserved: {result.stdout!r}"
        )


def expect_failure(
    arguments: list[str], required_text: str, *, cwd: Path | None = None
) -> None:
    result = command(arguments, cwd=cwd)
    combined = result.stdout + result.stderr
    if result.returncode == 0 or required_text not in combined:
        raise SystemExit(
            f"Expected {' '.join(arguments)} to fail with {required_text!r}\n{combined}"
        )


def compile_directory(source: Path, output: Path) -> None:
    files = sorted(str(path) for path in source.glob("*.java"))
    result = command([JAVAC, "-Xlint:all", "-d", str(output), *files])
    if result.returncode != 0:
        raise SystemExit(result.stdout + result.stderr)
    if result.stdout or result.stderr:
        raise SystemExit(
            f"javac reported output while compiling {source.name}:\n"
            f"{result.stdout}{result.stderr}"
        )


def main() -> None:
    version = command([JAVA, "-version"])
    version_text = version.stdout + version.stderr
    match = re.search(r'version "(\d+)', version_text)
    if not match or match.group(1) != "25":
        raise SystemExit(f"Java 25 is required; observed:\n{version_text}")

    with tempfile.TemporaryDirectory(prefix="java-onboarding-") as temporary:
        build_root = Path(temporary)

        first = EXAMPLES / "01-running-java-programs"
        first_build = build_root / "01"
        first_build.mkdir()
        compile_directory(first, first_build)
        expect_success([JAVA, str(first / "RawDifference.java")], "Arrival in -3 minutes\n")
        expect_success([JAVA, str(first / "ArrivalDisplay.java")], "EARLY by 3 minutes\n")
        expect_success([JAVA, "-cp", str(first_build), "ArrivalDisplayExpanded"], "EARLY by 3 minutes\n")
        expect_failure([JAVA, str(first / "RuntimeFailure.java")], "NumberFormatException")

        invalid = build_root / "TypeMismatch.java"
        shutil.copy2(first / "TypeMismatch.java.txt", invalid)
        expect_failure([JAVAC, str(invalid)], "incompatible types")

        second = EXAMPLES / "02-objects-state-and-references"
        second_build = build_root / "02"
        second_build.mkdir()
        compile_directory(second, second_build)
        expect_success(
            [JAVA, "-cp", str(second_build), "ArrivalBoardDemo"],
            "Brock Hall: 10 minutes\nBrock Hall: 14 minutes\n",
        )
        expect_success(
            [JAVA, "-cp", str(second_build), "ReassignmentDemo"],
            "Brock Hall: 10 minutes\nUBC Exchange: 28 minutes\n",
        )
        expect_failure(
            [JAVA, "-cp", str(second_build), "NullReferenceFailure"],
            "NullPointerException",
        )

        third = EXAMPLES / "03-iteration-collections-and-interfaces"
        third_build = build_root / "03"
        third_build.mkdir()
        compile_directory(third, third_build)
        expect_success(
            [JAVA, "-cp", str(third_build), "ArraySummary"],
            "late predictions: 2\n",
        )
        expect_success(
            [JAVA, "-cp", str(third_build), "CollectionsDemo"],
            (
                "observations: 3\n"
                "distinct routes: 2\n"
                "contains 44: true\n"
                "latest delay for 44: 7\n"
            ),
        )
        expect_success(
            [JAVA, "-cp", str(third_build), "RuleDemo"],
            "matching delays: 2\n",
        )
        expect_failure(
            [JAVA, "-cp", str(third_build), "ArrayBoundsFailure"],
            "ArrayIndexOutOfBoundsException",
        )

    print("Observed Java 25 and validated all 13 Java source files and fixtures.")
    print("Successful outputs and intended compilation/runtime failures matched the readings.")


if __name__ == "__main__":
    main()
