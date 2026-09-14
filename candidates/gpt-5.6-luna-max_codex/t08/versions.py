"""Utilities for selecting the newest semantic version."""

import re


_VERSION_RE = re.compile(
    r"^v?(?P<core>[0-9]+(?:\.[0-9]+){1,2})"
    r"(?:-(?P<prerelease>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+(?P<build>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)


def _numeric_component(value, part):
    """Return an orderable core number, rejecting non-canonical zeros."""
    if len(value) > 1 and value[0] == "0":
        raise ValueError(f"invalid {part} component: {value!r}")
    # Canonical decimal strings can be compared numerically by length first,
    # then lexicographically.  This also handles values larger than Python's
    # configured maximum integer-conversion length.
    return (len(value), value)


def _prerelease_key(value):
    """Return an ordering key for a validated prerelease string."""
    if value is None:
        return ()

    identifiers = []
    for identifier in value.split("."):
        if identifier.isdigit():
            if len(identifier) > 1 and identifier[0] == "0":
                raise ValueError(
                    f"numeric prerelease identifier has leading zero: {identifier!r}"
                )
            # Numeric identifiers have lower precedence than non-numeric ones.
            # As with core numbers, compare their canonical decimal forms.
            identifiers.append((0, len(identifier), identifier))
        else:
            identifiers.append((1, identifier))
    return tuple(identifiers)


def _precedence_key(version):
    """Parse *version* and return a key implementing SemVer precedence."""
    if not isinstance(version, str):
        raise ValueError(f"version must be a string, got {type(version).__name__}")

    match = _VERSION_RE.fullmatch(version)
    if match is None:
        raise ValueError(f"invalid semantic version: {version!r}")

    core = match.group("core").split(".")
    major = _numeric_component(core[0], "major")
    minor = _numeric_component(core[1], "minor")
    patch = (
        _numeric_component(core[2], "patch")
        if len(core) == 3
        else _numeric_component("0", "patch")
    )

    # Build metadata is intentionally not included: it has no effect on
    # precedence.  A stable release ranks above every prerelease.
    prerelease = _prerelease_key(match.group("prerelease"))
    release_rank = 1 if match.group("prerelease") is None else 0
    return (major, minor, patch, release_rank, prerelease)


def newest(versions):
    """Return the original spelling of the highest-precedence version.

    An empty iterable returns ``None``.  Every non-empty value is validated,
    including values that do not end up being the newest version.
    """
    return max(versions, key=_precedence_key, default=None)
