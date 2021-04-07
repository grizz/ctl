import pytest
import semver

import ctl.util.versioning as versioning


@pytest.mark.parametrize("version,tupled", [("1.0.0", (1, 0, 0, None, None))])
def test_version_tuple(version, tupled):
    # Use VersionInfo.parse to parse a string
    version = semver.VersionInfo.parse(version)
    assert version.to_tuple() == tupled


@pytest.mark.parametrize("version,string", [(("1", "0", "0"), "1.0.0")])
def test_version_string(version, string):
    # Unpack a tuple as arguments for a VersionInfo instance
    version = semver.VersionInfo(*version)
    assert str(version) == string


@pytest.mark.parametrize(
    "prerelease,expected,raises",
    [
        ("alpha", "alpha.1", None),
        ("alpha.1", "alpha.1", None),
        ("0.3.7", "0.3.7", None),
        ("x-y-z.-", "x-y-z.-.1", None),
        ("&&&", None, ValueError),
        ("abc.01", None, ValueError),
        ("foo..bar", None, ValueError),
    ],
)
def test_validate_prerelease(prerelease, expected, raises):
    if raises:
        with pytest.raises(raises):
            assert versioning.validate_prerelease(prerelease)
    else:
        assert versioning.validate_prerelease(prerelease) == expected


@pytest.mark.parametrize(
    "version,segment,expected",
    [
        ("1.2.3", "major", "2.0.0"),
        ("1.2.3", "minor", "1.3.0"),
        ("1.2.3", "patch", "1.2.4"),
    ],
)
def test_bump_semantic(version, segment, expected):
    assert versioning.bump_semantic(version, segment) == expected
