import re

import semver


def validate_prerelease(prerelease):
    if not isinstance(prerelease, (list, tuple)):
        prerelease = list(prerelease.split("."))

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

    # If the last part of the prerelease is not a number
    # we want to append ".1" so we can bump in the future
    if not re.match(r"[0-9]", prerelease[-1]):
        prerelease.append("1")

    return ".".join(prerelease)


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
    elif segment == "prerelease":

        if not version.prerelease:
            raise ValueError(
                "Cannot bump the prerelease if it's not a prereleased version"
            )
        else:
            return str(version.bump_prerelease())
    else:
        raise ValueError
