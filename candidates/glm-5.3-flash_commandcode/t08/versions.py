import re

# SemVer 2.0.0 grammar (https://semver.org/), relaxed to allow an optional
# leading "v" and an omitted patch component (treated as zero).
_SEMVER_RE = re.compile(
    r"v?(0|[1-9]\d*)\.(0|[1-9]\d*)(?:\.(0|[1-9]\d*))?"
    r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?",
    re.ASCII,
)


def _precedence_key(version):
    """Return a sort key implementing SemVer 2.0.0 precedence."""
    match = _SEMVER_RE.fullmatch(version)
    if match is None:
        raise ValueError(f"invalid semantic version: {version!r}")
    major, minor, patch, prerelease, _build = match.groups()
    key = (int(major), int(minor), int(patch) if patch is not None else 0)
    if prerelease is None:
        return key + (1, ())
    identifiers = tuple(
        (0, int(identifier)) if identifier.isdigit() else (1, identifier)
        for identifier in prerelease.split(".")
    )
    return key + (0, identifiers)


def newest(versions):
    """Return the version string with the highest SemVer 2.0.0 precedence.

    Accepts an optional leading "v", an omitted patch component (treated as
    zero), and pre-release/build metadata. Build metadata is ignored for
    precedence, so on ties the first maximal spelling is returned. Returns
    None for an empty iterable and raises ValueError for invalid versions.
    """
    return max(versions, key=_precedence_key, default=None)
