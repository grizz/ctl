# Quickstart

## Install

```
pip install ctl
```

## Plugin centric approach

Ctl is driven by plugins. When a plugin is configured it will expose itself to the ctl cli by it's name and you may then execute operations on it.

Plugins are aware of and can make use of one another (were it is sensical), this allows for a streamlined approach when implementing complex operations.

## Example: Package / Release management

This example shows how to set up ctl to tag releases in a git repository and then build a python package and upload it to pypi

## Create a ctl config file

Create a `Ctl` directory in the location where you want to run ctl from.

Alternatively you can also create a `.ctl` directory in your home directory.

When trying to read your config file, ctl will look in these places, in order:

- `$CTL_HOME`
- `./Ctl`
- `~/.ctl`

open `Ctl/config.yaml` in your favorite editor and add the following

```yaml
{!examples/quickstart/package_management/Ctl/config.yaml!}
```

This configures 3 plugins we will need for our package management

1. git: access to a git repository
2. version: tag a release in the git repository
3. pypi: build a package and upload to pypi

## Run ctl

You can run `ctl --help` and it should show the three plugins under `Configured Operations`:

```sh
ctl --help
```

```
[ALL] Configured Operations:
  {git_example,version,pypi}
    git_example
    version             Manipulates repository versions.
    pypi                Facilitates a PyPI package release
```

### Push a version tag to git

For the sake of this example, let's assume that the repository we are targeting has never been versioned with ctl before.

So we now need to tag and push the initial version. This will create a `Ctl/VERSION` file in your repository that holds the version as well as create and push a git tag.

```sh
ctl version tag 0.1.0 --init
```

### Bump the version in a semantic way

Once the repository has been versioned by ctl, you can now use the `bump` operation to bump semantic versions

```sh
# bump the version to 0.1.1
ctl version bump patch
```

### Release to PyPI

Once our versions exist, we can use the `pypi` plugin to build and push a release to pypi

Let's start by doing a dry run to see if everything is in order.

```sh
ctl pypi release 0.1.1 --dry
```

If all is good, we can commit and also sign the release in the process

```sh
ctl pypi release 0.1.1 --sign
```
