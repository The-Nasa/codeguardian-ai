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


def changed_python(
    root: Path, base: str, head: str
) -> tuple[tuple[Path, ...], tuple[Path, ...]]:
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
    changes = (
        git(
            root,
            "diff",
            "--raw",
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
    eligible, excluded = [], []
    for metadata, name in zip(changes[:-1:2], changes[1::2], strict=True):
        if not name.endswith((".py", ".pyi")):
            continue
        path = root / name
        if (
            metadata.split()[1] in {"100644", "100755"}
            and path.is_file()
            and not path.is_symlink()
            and path.resolve().is_relative_to(root)
        ):
            eligible.append(Path(name))
        else:
            excluded.append(Path(name))
    return tuple(eligible), tuple(excluded)
