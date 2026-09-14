from pathlib import Path


def safe_join(root, user_path):
    """Join *user_path* to *root* without leaving *root*.

    The lexical checks reject paths that could escape through ``..`` or
    replace the root when they are joined.  Resolving with ``strict=False``
    also evaluates symlinks in existing parent directories while retaining
    a non-existent final path, which lets the physical containment check
    cover paths that have not been created yet.
    """
    root_path = Path(root)
    relative_path = Path(user_path)

    if relative_path.is_absolute():
        raise ValueError("user_path must be relative")

    if ".." in relative_path.parts:
        raise ValueError("parent traversal is not allowed")

    candidate = root_path / relative_path

    try:
        resolved_root = root_path.resolve(strict=False)
        resolved_candidate = candidate.resolve(strict=False)
    except (OSError, RuntimeError, ValueError) as exc:
        raise ValueError("path cannot be safely resolved") from exc

    if resolved_candidate == resolved_root:
        raise ValueError("user_path must not refer to root")

    try:
        resolved_candidate.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError("user_path resolves outside root") from exc

    return candidate
