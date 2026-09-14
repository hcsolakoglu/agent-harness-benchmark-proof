"""Safe joining of untrusted, caller-supplied paths onto a trusted root.

``safe_join`` is a security boundary: it maps a user supplied path onto a
location inside ``root`` and refuses anything that could name the root itself
or a location outside of it, whether by lexical tricks (``/etc/passwd``,
``../../etc``) or by filesystem indirection (symlinks that point elsewhere).
"""

from __future__ import annotations

import os
from pathlib import Path, PureWindowsPath

__all__ = ["UnsafePathError", "safe_join"]


class UnsafePathError(ValueError, PermissionError):
    """Raised when a path cannot be safely joined under the trusted root.

    The error doubles as a :class:`ValueError` (the supplied path is not a
    valid relative path) and as a :class:`PermissionError` (the path would
    escape the root), so callers may catch whichever is idiomatic for them.
    """


def _canonical(path: str) -> str:
    """Collapse runs of leading separators for comparison purposes.

    POSIX gives ``//`` an implementation defined meaning but on every real
    system it names the same directory as ``/``; ``os.path.commonpath`` does
    not know that and would treat ``//x`` as unrelated to root ``//``.
    """
    drive, tail = os.path.splitdrive(path)
    while tail[:2] == os.sep * 2:
        tail = tail[1:]
    return drive + tail


def _contains(base: str, target: str) -> bool:
    """Return whether *target* is *base* or lies lexically underneath it.

    ``os.path.commonpath`` compares whole path components, so a sibling such
    as ``/srv/root2`` is correctly reported as *not* being inside ``/srv/root``.
    """
    base, target = _canonical(base), _canonical(target)
    if base == target:
        return True
    try:
        return os.path.commonpath((base, target)) == base
    except ValueError:
        # Mixed absolute/relative paths or different drives on Windows.
        return False


def _strictly_contains(base: str, target: str) -> bool:
    """Like :func:`_contains`, but the root itself does not count as inside."""
    return _canonical(base) != _canonical(target) and _contains(base, target)


def safe_join(
    root: str | bytes | os.PathLike[str] | os.PathLike[bytes],
    user_path: str | bytes | os.PathLike[str] | os.PathLike[bytes],
) -> Path:
    """Join *user_path* onto *root*, guaranteeing the result stays inside it.

    Args:
        root: Trusted directory (``str`` or path-like).  It does not have to
            exist yet; relative roots are interpreted against the current
            working directory.
        user_path: Untrusted relative path (``str`` or path-like).

    Returns:
        A :class:`pathlib.Path` pointing at a strict descendant of *root*.
        The caller's spelling of *root* is preserved and the result is
        lexically normalised (``a/./b`` becomes ``a/b``).

    Raises:
        UnsafePathError: If *user_path* is absolute, contains a ``..``
            component, resolves to *root* itself, or would leave *root* once
            symlinks are taken into account.  Symlink checks also cover
            targets that do not exist yet: a dangling symlink pointing
            outside *root* is rejected, while new files may be created under
            directories that really are inside *root*.
        TypeError: If either argument is not a path-like object.

    Note:
        The result is a path, so re-checking is subject to the usual
        time-of-check/time-of-use window; callers that need an atomic
        guarantee should open the file with ``O_NOFOLLOW`` relative to an
        already validated directory descriptor.
    """
    root_str = os.fsdecode(os.fspath(root))
    rel_str = os.fsdecode(os.fspath(user_path))

    if not root_str:
        raise UnsafePathError("root must not be empty")
    if "\x00" in root_str or "\x00" in rel_str:
        raise UnsafePathError("path must not contain NUL bytes")

    rel = Path(rel_str)
    # Paths may arrive from cross-platform clients, so also refuse input that
    # only *looks* harmless on the current platform (``..\x`` on POSIX) or
    # that is absolute under Windows semantics (``C:\x``, ``\\srv\share``).
    win_rel = PureWindowsPath(rel_str)
    if rel.is_absolute() or rel.root or rel.drive or win_rel.is_absolute():
        raise UnsafePathError(f"absolute path {rel_str!r} is not allowed")
    if ".." in rel.parts or ".." in win_rel.parts:
        raise UnsafePathError(
            f"parent traversal in {rel_str!r} is not allowed"
        )
    if not rel.parts:
        # '', '.', './' and friends all designate the root itself.
        raise UnsafePathError(f"{rel_str!r} designates the root itself")

    # Lexical normalisation only; symlinks are deliberately left untouched in
    # the returned path so that it keeps pointing at the same place as the
    # caller's root.
    lexical = os.path.normpath(os.path.join(root_str, rel_str))
    abs_root = os.path.abspath(root_str)
    abs_candidate = os.path.normpath(os.path.join(abs_root, rel_str))

    if not _strictly_contains(abs_root, abs_candidate):
        raise UnsafePathError(f"{rel_str!r} escapes root {root_str!r}")

    # Physical check: resolve every existing symlink in the root and in the
    # candidate ("non-strict" resolution also follows a symlink whose target
    # does not exist yet, which is exactly the dangling-link escape case).
    real_root = os.path.realpath(abs_root)
    real_candidate = os.path.realpath(abs_candidate)
    if not _strictly_contains(real_root, real_candidate):
        raise UnsafePathError(
            f"{rel_str!r} resolves outside root {root_str!r} via a symlink"
        )

    return Path(lexical)
