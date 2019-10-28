# PyPI plugin

The PyPI plugin allows you to facilitate python package releases

## Requirements

The `twine` module needs to be installed

```
py(27|34|35): pip install twine>=1.14.0,<2
py36: pip install twine>=2,<3
```

## Config

```yaml
{!examples/plugins/pypi/Ctl/config.yaml!}
```

## Through filepath

```
ctl pypi release 1.2.3 path/to/my/local/checkout
```

## Through git plugin

Set up a git plugin in the config

```yaml
ctl:
  plugins:
    - type: git
      name: my_repo
      config:
        repo_url: git@github.com:me/my_repo
```

Then just use the plugin name as a repository

```
ctl pypi release 1.2.3 my_repo
```

## Set default repository

You can also set a default repository so you dont need to specify
it in the cli

```yaml
ctl:
  plugins:

    - type: pypi
      name: pypi_my_repo
      config:
        config_file: ~/.pypirc
        repository: my_repo
```

```
ctl pypi_my_repo release 1.2.3
```

## Usage

!!! note "Plugin name"
    This usage documentation assumes that the plugin instance name
    is `pypi`

{pymdgen-cmd:ctl --home=docs pypi --help}

### Release

{pymdgen-cmd:ctl --home=docs pypi release --help}

### Validate

{pymdgen-cmd:ctl --home=docs pypi validate --help}
