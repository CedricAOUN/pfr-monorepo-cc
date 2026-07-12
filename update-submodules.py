#!/usr/bin/env python3

import os
import subprocess
import sys

SUBMODULES = [
    "pfr-backend-cc",
    "projet-fil-rouge-cc",
]

BRANCH = "main"


def run(cmd, cwd):
    print(f"\n> {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        capture_output=True
    )

    if result.stdout:
        print(result.stdout.strip())

    if result.returncode != 0:
        print(result.stderr.strip())
        sys.exit(result.returncode)


def main():
    monorepo_root = os.path.dirname(os.path.abspath(__file__))

    print(f"Monorepo: {monorepo_root}")

    # Update each submodule
    for submodule in SUBMODULES:
        path = os.path.join(monorepo_root, submodule)

        if not os.path.isdir(path):
            print(f"Missing submodule: {path}")
            sys.exit(1)

        print(f"\nUpdating {submodule}")

        run(["git", "checkout", BRANCH], path)
        run(["git", "pull", "origin", BRANCH], path)

    # Update parent repo pointers
    print("\nUpdating monorepo references")

    run(["git", "add", *SUBMODULES], monorepo_root)

    status = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=monorepo_root,
        text=True,
        capture_output=True
    )

    if status.stdout.strip():
        run(
            ["git", "commit", "-m", "Update submodules to latest commits"],
            monorepo_root
        )

        run(
            ["git", "push", "origin", 'master'],
            monorepo_root
        )

        print("\nDone: monorepo updated and pushed.")
    else:
        print("\nNo submodule changes detected.")


if __name__ == "__main__":
    main()