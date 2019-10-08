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

```
usage: ctl pypi [-h] {release,validate} ...

optional arguments:
  -h, --help          show this help message and exit

Operation:
  {release,validate}
    release           execute release
    validate          validate release
```

### Release

```
usage: ctl pypi release [-h] [--dry] [--config-file CONFIG_FILE]
                        [--identity IDENTITY] [--repository REPOSITORY]
                        [--sign] [--sign-with SIGN_WITH]
                        version [repository]

optional arguments:
  -h, --help            show this help message and exit
  --dry                 Do a dry run (nothing will be uploaded)
  --config-file CONFIG_FILE
                        path to pypi config file (e.g. ~/.pypirc) (~/.pypirc-
                        vegu)
  --identity IDENTITY   sign release with this identity
  --pypi-repository REPOSITORY
                        PyPI repository name - needs to exist in your pypi
                        config file (pypi)
  --sign                sign releases
  --sign-with SIGN_WITH
                        sign release with this program (gpg)

  version               release version - if repository is managed by git,
                        checkout this branch/tag
  repository                repository for release - should be a path to a python
                        package or the name of a repository type plugin
```

### Validate

```
usage: ctl pypi validate [-h] version [repository]

optional arguments:
  -h, --help  show this help message and exit

  version     release version - if repository is managed by git, checkout this
              branch/tag
  repository      repository for release - should be a path to a python package or the
              name of a repository type plugin
```
