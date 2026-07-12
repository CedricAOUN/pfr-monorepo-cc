#!/usr/bin/env python3

import os
import subprocess
import sys


def run(command):
    print(f"> {' '.join(command)}")

    result = subprocess.run(
        command,
        text=True,
        capture_output=True
    )

    if result.stdout:
        print(result.stdout.strip())

    if result.returncode != 0:
        if result.stderr:
            print(result.stderr.strip())

        sys.exit(result.returncode)


def main():
    repo_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(repo_root)

    print(f"Working directory: {repo_root}")

    # Ensure local submodule configuration matches .gitmodules
    run([
        "git",
        "submodule",
        "sync",
        "--recursive"
    ])

    # Initialize missing submodules and update to latest tracked branches
    run([
        "git",
        "submodule",
        "update",
        "--init",
        "--remote",
        "--recursive"
    ])

    # Stage updated submodule references
    run([
        "git",
        "add",
        "."
    ])

    # Check whether there is anything to commit
    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"]
    )

    if result.returncode == 0:
        print("No submodule updates detected.")
        return

    # Commit updated submodule pointers
    run([
        "git",
        "commit",
        "-m",
        "Bump submodules"
    ])

    # Push monorepo update
    run([
        "git",
        "push"
    ])

    print("Submodules updated and monorepo pushed successfully.")


if __name__ == "__main__":
    main()