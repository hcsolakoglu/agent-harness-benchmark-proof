"""Safe lexical/physical path joining.

``safe_join`` joins a user supplied path onto a trusted root directory and
guarantees the result stays *strictly* contained inside that root, both

* lexically -- after collapsing ``.`` and ``..`` components the joined path
  must still live under ``root`` (so ``../`` escapes are rejected), and
* physically -- after resolving every symlink, ``realpath`` of the result must
  still live under the resolved root (so symlink escapes are rejected, even
  when the final target does not exist yet).

Absolute paths, parent traversal that escapes the root, and the root itself
are rejected with :class:`ValueError`.
"""

import os
from pathlib import Path

__all__ = ["safe_join"]


def _is_within(path, root):
    """Return ``True`` when *path* is *root* or lives underneath it."""
    return path == root or root in path.parents


def safe_join(root, user_path):
    """Join *user_path* onto *root*, rejecting anything that escapes it.

    Parameters
    ----------
    root:
        Trusted directory. It does not have to exist yet.
    user_path:
        Untrusted relative path supplied by a caller.

    Returns
    -------
    pathlib.Path
        ``root`` joined with the lexically normalised *user_path*.

    Raises
    ------
    ValueError
        If *user_path* is absolute, resolves to ``root`` itself, escapes
        *root* through ``..`` components, or escapes it through symlinks.
    """
    root_path = Path(root)

    # A user supplied absolute path would discard ``root`` entirely when
    # joined, so it is always rejected.
    if os.path.isabs(str(user_path)) or Path(user_path).is_absolute():
        raise ValueError("user_path must be a relative path: %r" % (user_path,))

    # Collapse ``.`` / ``..`` lexically *before* touching the filesystem.  This
    # is what neutralises tricks such as ``symlink/../file``: any ``..`` that
    # could re-target an earlier symlink is removed first.
    normalised = os.path.normpath(str(user_path))

    # After normalisation a surviving leading ``..`` can only escape.
    parts = Path(normalised).parts
    if normalised in ("", os.curdir) or (parts and parts[0] == os.pardir):
        raise ValueError("user_path escapes the root: %r" % (user_path,))

    candidate = root_path / normalised

    # --- lexical containment ------------------------------------------------
    # Compare absolute, lexically-normalised forms (no symlink resolution).
    root_abs = Path(os.path.abspath(root_path))
    candidate_abs = Path(os.path.abspath(candidate))
    if candidate_abs == root_abs or not _is_within(candidate_abs, root_abs):
        raise ValueError("user_path escapes the root: %r" % (user_path,))

    # --- physical containment ----------------------------------------------
    # ``realpath`` resolves symlinks in every part that exists and leaves a
    # non-existent tail untouched, so a not-yet-created final target is still
    # validated against the symlinks of its existing ancestors.
    real_root = Path(os.path.realpath(root_path))
    real_candidate = Path(os.path.realpath(candidate))
    if real_candidate == real_root or not _is_within(real_candidate, real_root):
        raise ValueError("user_path escapes the root: %r" % (user_path,))

    return candidate
