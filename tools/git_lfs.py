"""Git LFS policy and index-integrity checks for binary source originals.

The working tree contains the real bytes for an LFS file.  The Git index/tree
must contain the small LFS pointer instead.  Checking only the working tree
therefore cannot detect a malformed commit; this module deliberately inspects
the index and the attributes resolved by Git.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

LFS_POINTER_HEADER = b"version https://git-lfs.github.com/spec/v1\n"


def _run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def _index_blobs(root: Path, paths: list[str]) -> dict[str, bytes]:
    """Read index blobs in one ``git cat-file --batch`` process."""
    if not paths:
        return {}
    process = subprocess.Popen(
        ["git", "-C", str(root), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.stdin is None or process.stdout is None:
        process.kill()
        raise ValueError("git_cat_file_pipe_failed")
    process.stdin.write("".join(f":{path}\n" for path in paths).encode())
    process.stdin.close()
    blobs: dict[str, bytes] = {}
    for path in paths:
        header = process.stdout.readline().split()
        if len(header) != 3 or header[1] != b"blob":
            continue
        size = int(header[2])
        blobs[path] = process.stdout.read(size)
        process.stdout.readline()
    if process.wait() != 0:
        raise ValueError("git_cat_file_failed")
    return blobs


def _git_text(root: Path, *args: str) -> str:
    result = _run_git(root, *args)
    if result.returncode:
        raise ValueError(result.stderr.strip() or "git_command_failed")
    return result.stdout


def is_lfs_pointer(data: bytes) -> bool:
    """Return whether *data* is a syntactically recognizable LFS pointer."""
    return data.startswith(LFS_POINTER_HEADER)


def _lfs_paths(root: Path, paths: list[str], *, cached: bool = False) -> set[str]:
    """Resolve the LFS attribute for many paths in one Git subprocess."""
    if not paths:
        return set()
    cached_flag = ["--cached"] if cached else []
    result = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "check-attr",
            *cached_flag,
            "-z",
            "filter",
            "--",
            *paths,
        ],
        capture_output=True,
        check=False,
    )
    if result.returncode:
        return set()
    fields = result.stdout.split(b"\0")
    matched: set[str] = set()
    for index in range(0, len(fields) - 3, 3):
        path, attribute, value = fields[index : index + 3]
        if attribute == b"filter" and value == b"lfs":
            matched.add(path.decode())
    return matched


def require_pdf_lfs(root: Path, relative_path: str) -> str | None:
    """Validate the repository prerequisites before importing a PDF.

    The import writes real PDF bytes into the working tree; the subsequent
    commit must be able to clean them into an LFS pointer.  Return a stable
    error code for the caller, or ``None`` when the repository is ready.
    """
    root = Path(root).resolve()
    if _run_git(root, "rev-parse", "--show-toplevel").returncode:
        return "pdf_requires_git_lfs"
    if _run_git(root, "lfs", "version").returncode:
        return "pdf_requires_git_lfs"
    if relative_path not in _lfs_paths(root, [relative_path]):
        return "pdf_lfs_rule_missing"
    return None


def lfs_index_errors(root: Path) -> list[dict[str, str]]:
    """Return all tracked LFS-rule paths whose index entries are not pointers."""
    root = Path(root).resolve()
    paths = _git_text(root, "ls-files", "-z").split("\0")
    errors: list[dict[str, str]] = []
    paths = list(filter(None, paths))
    lfs_paths = _lfs_paths(root, paths, cached=True)
    blobs = _index_blobs(root, sorted(lfs_paths))
    for relative_path in sorted(lfs_paths):
        data = blobs.get(relative_path)
        if data is None:
            errors.append({"path": relative_path, "code": "lfs_index_entry_unreadable"})
            continue
        if not is_lfs_pointer(data):
            errors.append(
                {
                    "path": relative_path,
                    "code": "lfs_pointer_required",
                }
            )
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    try:
        errors = lfs_index_errors(args.root)
    except (OSError, ValueError) as exc:
        print(f"git-lfs check blocked: {exc}")
        return 2
    if errors:
        for error in errors:
            print(f"{error['code']}: {error['path']}")
        return 1
    print("git-lfs index valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
