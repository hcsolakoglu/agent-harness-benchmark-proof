from pathlib import Path


def safe_join(root, user_path):
    """Return ``root`` joined with the relative ``user_path``.

    The result is guaranteed to be contained strictly below ``root`` both
    lexically and physically (symlinks are resolved, including for final
    components that do not exist yet).

    Raises ValueError when ``user_path`` is absolute, contains a parent
    directory component (``..``), refers to ``root`` itself, or escapes
    ``root`` through a symlink.
    """
    root_path = Path(root)
    user = Path(user_path)

    if user.is_absolute():
        raise ValueError(f"absolute path is not allowed: {user_path!r}")

    parts = user.parts
    if not parts:
        raise ValueError(f"path refers to the root itself: {user_path!r}")
    if ".." in parts:
        raise ValueError(f"parent traversal is not allowed: {user_path!r}")

    joined = root_path.joinpath(*parts)

    real_root = root_path.resolve(strict=False)
    real_joined = joined.resolve(strict=False)
    if real_joined == real_root or real_root not in real_joined.parents:
        raise ValueError(f"path escapes root via symlinks: {user_path!r}")

    return joined
