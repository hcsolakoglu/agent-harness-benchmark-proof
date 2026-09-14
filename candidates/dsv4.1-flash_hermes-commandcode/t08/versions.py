"""SemVer 2.0 version handling utilities.

The public entry point is :func:`newest`, which returns the highest-precedence
version string from an iterable, preserving the original spelling of the winner.
"""

import re

__all__ = ["newest"]


# A SemVer version, optionally prefixed with a lowercase ``v`` and optionally
# omitting the minor and/or patch components (treated as zero).  Prerelease and
# build-metadata identifiers follow the grammar from the SemVer 2.0.0 spec.
#
#   * Core numeric components MUST NOT contain leading zeroes.
#   * Prerelease numeric identifiers MUST NOT contain leading zeroes.
#   * Build metadata identifiers have no leading-zero restriction.
_SEMVER_RE = re.compile(
    r"^v?"
    r"(?P<major>0|[1-9]\d*)"
    r"(?:\.(?P<minor>0|[1-9]\d*))?"
    r"(?:\.(?P<patch>0|[1-9]\d*))?"
    r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*))?"
    r"(?:\+(?P<build>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"$"
)


def _prerelease_key(prerelease):
    """Return a sortable key for a SemVer prerelease string.

    Numeric identifiers sort below alphanumeric ones, numeric identifiers are
    compared numerically, alphanumeric identifiers are compared lexically, and
    a shorter list of identifiers sorts below a longer list sharing its prefix.
    """
    identifiers = []
    for part in prerelease.split("."):
        if part.isdigit():
            identifiers.append((0, int(part), ""))
        else:
            identifiers.append((1, 0, part))
    return tuple(identifiers)


def _parse(version):
    """Parse *version* into a precedence key.

    Build metadata is intentionally excluded from the key because it does not
    affect precedence.  Raises :class:`ValueError` for anything that is not a
    valid SemVer 2.0 version string.
    """
    if not isinstance(version, str):
        raise ValueError(f"invalid version: {version!r}")

    match = _SEMVER_RE.match(version)
    if match is None:
        raise ValueError(f"invalid version: {version!r}")

    major = int(match.group("major"))
    minor = int(match.group("minor") or 0)
    patch = int(match.group("patch") or 0)

    prerelease = match.group("prerelease")
    if prerelease is None:
        # A normal release has higher precedence than any prerelease.
        prerelease_key = (1,)
    else:
        prerelease_key = (0, _prerelease_key(prerelease))

    return (major, minor, patch, prerelease_key)


def newest(versions):
    """Return the version with the highest SemVer 2.0 precedence.

    ``versions`` may be any iterable of version strings.  Each is validated;
    an invalid version raises :class:`ValueError`.  The original spelling of
    the winning version is returned.  When two versions have equal precedence
    (for example they differ only in build metadata), either spelling may be
    returned.  An empty input yields ``None``.
    """
    winner = None
    winner_key = None
    for version in versions:
        key = _parse(version)
        if winner_key is None or key > winner_key:
            winner = version
            winner_key = key
    return winner
