from setuptools import find_packages, setup


def read_file(name):
    with open(name) as fobj:
        return fobj.read().strip()


LONG_DESCRIPTION = read_file("README.md")
VERSION = read_file("Ctl/VERSION")
REQUIREMENTS = read_file("Ctl/requirements.txt").split("\n")
TEST_REQUIREMENTS = read_file("Ctl/requirements-test.txt").split("\n")


setup(
    name="ctl",
    version=VERSION,
    author="20C",
    author_email="code@20c.com",
    description="Control your environment",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="LICENSE",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    url="https://github.com/20c/ctl",
    download_url=f"https://github.com/20c/ctl/{VERSION}",
    install_requires=REQUIREMENTS,
    test_requires=TEST_REQUIREMENTS,
    entry_points={"console_scripts": ["ctl=ctl.cli:main"]},
    scripts=[
        # virtualenv helper scripts
        "src/ctl/bin/ctl_venv_build",
        "src/ctl/bin/ctl_venv_copy",
        "src/ctl/bin/ctl_venv_sync",
    ],
    zip_safe=True,
)
