import pytest

import ctl.util.versioning as versioning


@pytest.mark.parametrize("version,tupled", [("1.0.0", ("1", "0", "0"))])
def test_version_tuple(version, tupled):
    assert versioning.version_tuple(version) == tupled


@pytest.mark.parametrize("version,string", [(("1", "0", "0"), "1.0.0")])
def test_version_string(version, string):
    assert versioning.version_string(version) == string


@pytest.mark.parametrize(
    "version,expected,raises",
    [
        ("1.0.0", (1, 0, 0), None),
        ((1, 0, 0), (1, 0, 0), None),
        ("1.0.0.0", (1, 0, 0, 0), None),
        ((1, 0, 0, 0), (1, 0, 0, 0), None),
        ("1.0", (1, 0), None),
        ("a.b.c", None, ValueError),
    ],
)
def test_validate_semantic(version, expected, raises):
    if raises:
        with pytest.raises(raises):
            assert versioning.validate_semantic(version) == expected
    else:
        assert versioning.validate_semantic(version) == expected


@pytest.mark.parametrize(
    "prerelease,raises",
    [
        ("alpha", None),
        ("alpha.1", None),
        ("0.3.7", None),
        ("x-y-z.-", None),
        ("&&&", ValueError),
        ("abc.01", ValueError),
        ("foo..bar", ValueError),
    ],
)
def test_validate_prerelease(prerelease, raises):
    if raises:
        with pytest.raises(raises):
            assert versioning.validate_prerelease(prerelease)
    else:
        assert versioning.validate_prerelease(prerelease)


@pytest.mark.parametrize(
    "version,segment,expected",
    [
        ("1.2.3.4", "major", (2, 0, 0)),
        ("1.2.3", "minor", (1, 3, 0)),
        ("1.2.3.4", "patch", (1, 2, 4)),
        ("1.2.3.4", "dev", (1, 2, 3, 5)),
    ],
)
def test_bump_semantic(version, segment, expected):
    assert versioning.bump_semantic(version, segment) == expected
