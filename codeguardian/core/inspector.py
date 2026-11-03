"""Inspect tracked changes between exact commits in a trusted checkout."""

import re
import subprocess
from pathlib import Path


def git(root: Path, *args: str) -> bytes:
    result = subprocess.run(
        ("git", "-C", str(root), *args),
        check=False,
        capture_output=True,
        timeout=15,
    )
    if result.returncode:
        raise ValueError(f"Git could not complete {args[0]}")
    return result.stdout


def changed_python(root: Path, base: str, head: str) -> tuple[Path, ...]:
    for sha in (base, head):
        if not re.fullmatch(r"[0-9a-f]{40}", sha):
            raise ValueError("Expected full commit SHAs")
        if git(root, "cat-file", "-t", sha).strip() != b"commit":
            raise ValueError("Expected a commit")
    if (
        Path(git(root, "rev-parse", "--show-toplevel").decode().strip()).resolve()
        != root
    ):
        raise ValueError("Use the root of the checkout")
    if git(root, "rev-parse", "HEAD").decode().strip() != head:
        raise ValueError("Checkout must be at the review head")
    if git(root, "status", "--porcelain", "--untracked-files=all", "--ignored"):
        raise ValueError("Use a clean checkout, including ignored files")
    paths = (
        git(
            root,
            "diff",
            "--name-only",
            "--no-renames",
            "--diff-filter=ACMT",
            "-z",
            base,
            head,
            "--",
        )
        .decode()
        .split("\0")
    )
    return tuple(
        Path(path)
        for path in paths
        if path.endswith((".py", ".pyi"))
        and (root / path).is_file()
        and (root / path).resolve().is_relative_to(root)
        and not (root / path).is_symlink()
    )
