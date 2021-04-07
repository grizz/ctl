import re
import semver


def validate_semantic(version, pad=0):
    if not isinstance(version, (list, tuple)):
        version = version_tuple(version)

    parts = len(version)

    if parts < 1:
        raise ValueError("Semantic version needs to contain at least a major version")
    if parts > 4:
        raise ValueError("Semantic version can not contain more than 4 parts")

    if parts < pad:
        version = tuple(list(version) + [0 for i in range(0, pad - parts)])

    return tuple([int(n) for n in version])


def validate_prerelease(prerelease):
    if not isinstance(prerelease, (list, tuple)):
        prerelease = tuple(prerelease.split("."))

    for identifier in prerelease:

        if identifier == "":
            raise ValueError("Identifiers must not be empty")

        regex = r"[0-9A-Za-z-]+"
        match = re.match(regex, identifier)
        if not bool(match):
            raise ValueError(
                "Prerelease identifier must comprise only ASCII alphanumerics and hyphens"
            )

        regex = r"^0[0-9]+"
        match = re.match(regex, identifier)
        if bool(match):
            raise ValueError("Numeric identifiers must not have leading zeroes")

    return True


def bump_semantic(version, segment):
    """
    Uses the semver package to bump a version

    **Arguments**

    - version (`str`): existing version string
    - segment (`str`): major, minor, patch or prerelease


    **Output**
    - version (`str`): bumped version string

    """
    version = semver.VersionInfo.parse(version)
    if segment == "major":
        return str(version.bump_major())
    elif segment == "minor":
        return str(version.bump_minor())
    elif segment == "patch":
        return str(version.bump_patch())
    else:
        raise ValueError
