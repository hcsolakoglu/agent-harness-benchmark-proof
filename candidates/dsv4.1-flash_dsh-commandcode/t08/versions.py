"""Select the newest version from a collection using SemVer 2.0 precedence.

The public :func:`newest` helper compares versions according to the
`Semantic Versioning 2.0.0 <https://semver.org/spec/v2.0.0.html>`_ precedence
rules instead of comparing the raw strings lexically.
"""

import re

__all__ = ["newest"]

# A numeric identifier: either zero or a digit sequence without leading zeros.
_NUMERIC = r"0|[1-9][0-9]*"
# An alphanumeric prerelease identifier: non-empty, ASCII alphanumerics/hyphens.
_ALPHANUMERIC = r"[0-9]*[A-Za-z-][0-9A-Za-z-]*"
# One prerelease identifier: numeric ones must not contain leading zeros.
_PRERELEASE_IDENTIFIER = r"(?:{numeric}|{alphanumeric})".format(
    numeric=_NUMERIC, alphanumeric=_ALPHANUMERIC
)
# One build metadata identifier: leading zeros are allowed and ignored.
_BUILD_IDENTIFIER = r"[0-9A-Za-z-]+"

_SEMVER_RE = re.compile(
    r"v?"
    r"(?P<major>{numeric})"
    r"\.(?P<minor>{numeric})"
    r"(?:\.(?P<patch>{numeric}))?"
    r"(?:-(?P<prerelease>{identifier}(?:\.{identifier})*))?"
    r"(?:\+(?P<build>{build}(?:\.{build})*))?".format(
        numeric=_NUMERIC,
        identifier=_PRERELEASE_IDENTIFIER,
        build=_BUILD_IDENTIFIER,
    )
)


def _identifier_key(identifier):
    """Return a sort key for one prerelease identifier.

    Numeric identifiers always have lower precedence than alphanumeric ones
    (SemVer 2.0.0, item 11.4.3), hence the leading discriminator.
    """
    if identifier.isdigit():
        return (0, int(identifier), "")
    return (1, 0, identifier)


def _parse(version):
    """Parse a version string into a SemVer precedence sort key.

    Accepts an optional leading ``v``, omits the patch component as zero and
    tolerates prerelease and build metadata.  Build metadata never influences
    precedence.  Raises :class:`ValueError` for anything that is not a valid
    semantic version.
    """
    if not isinstance(version, str):
        raise ValueError("invalid semantic version: {!r}".format(version))

    match = _SEMVER_RE.fullmatch(version)
    if match is None:
        raise ValueError("invalid semantic version: {!r}".format(version))

    prerelease = match.group("prerelease")
    if prerelease is None:
        # A release has higher precedence than any prerelease of the same
        # major/minor/patch triple.
        prerelease_key = (1,)
    else:
        prerelease_key = (
            0,
            tuple(_identifier_key(part) for part in prerelease.split(".")),
        )

    return (
        int(match.group("major")),
        int(match.group("minor")),
        int(match.group("patch") or 0),
        prerelease_key,
    )


def newest(versions):
    """Return the version with the highest SemVer 2.0 precedence.

    ``versions`` is an iterable of version strings; the original spelling of
    the winner is returned unchanged, so ties in precedence (for example
    ``1.2`` versus ``1.2.0``, or versions differing only in build metadata)
    may yield any of the equivalent spellings.  Returns ``None`` when
    ``versions`` is empty or ``None``.

    Raises :class:`ValueError` if any entry is not a valid semantic version.
    """
    if versions is None:
        return None

    best_version = None
    best_key = None
    for version in versions:
        key = _parse(version)
        if best_key is None or key > best_key:
            best_version = version
            best_key = key
    return best_version
