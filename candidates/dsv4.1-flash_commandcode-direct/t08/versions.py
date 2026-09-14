import re

_VERSION_RE = re.compile(
    r'^v?'
    r'(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)'
    r'(?:\.(?P<patch>0|[1-9]\d*))?'
    r'(?:-(?P<prerelease>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?'
    r'(?:\+(?P<build>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$'
)

_PRERELEASE_ID_RE = re.compile(r'^(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)$')


def _parse(version):
    if not isinstance(version, str):
        raise ValueError(f'invalid version: {version!r}')
    match = _VERSION_RE.match(version)
    if match is None:
        raise ValueError(f'invalid version: {version!r}')
    prerelease = match.group('prerelease')
    return (
        int(match.group('major')),
        int(match.group('minor')),
        int(match.group('patch') or 0),
        _prerelease_key(prerelease),
    )


def _prerelease_key(prerelease):
    if prerelease is None:
        return (1,)
    identifiers = []
    for identifier in prerelease.split('.'):
        if _PRERELEASE_ID_RE.match(identifier) is None:
            raise ValueError(f'invalid prerelease identifier: {identifier!r}')
        if identifier.isdigit():
            identifiers.append((0, int(identifier)))
        else:
            identifiers.append((1, identifier))
    return (0, tuple(identifiers))


def newest(versions):
    best = None
    best_key = None
    for version in versions:
        key = _parse(version)
        if best_key is None or key > best_key:
            best, best_key = version, key
    return best
