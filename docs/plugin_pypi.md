# PyPI plugin

The PyPI plugin allows you to facilitate python package releases

## Config

```yaml
ctl:
  plugins:

    - type: pypi
      name: pypi
      config:
        config_file: ~/.pypirc

    - type: pypi
      name: pypi_test
      config:
        config_file: ~/.pypirc
        repository: testpypi
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

Then just use the plugin name as a target

```
ctl pypi release 1.2.3 my_repo
```

## Set default target

You can also set a default target so you dont need to specify
it in the cli

```yaml
ctl:
  plugins:

    - type: pypi
      name: pypi_my_repo
      config:
        config_file: ~/.pypirc
        target: my_repo
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
                        version [target]

optional arguments:
  -h, --help            show this help message and exit
  --dry                 Do a dry run (nothing will be uploaded)
  --config-file CONFIG_FILE
                        path to pypi config file (e.g. ~/.pypirc) (~/.pypirc-
                        vegu)
  --identity IDENTITY   sign release with this identity
  --repository REPOSITORY
                        PyPI repository name - needs to exist in your pypi
                        config file (pypi)
  --sign                sign releases
  --sign-with SIGN_WITH
                        sign release with this program (gpg)

  version               release version - if target is managed by git,
                        checkout this branch/tag
  target                target for release - should be a path to a python
                        package or the name of a repository type plugin
```

### Validate

```
usage: ctl pypi validate [-h] version [target]

optional arguments:
  -h, --help  show this help message and exit

  version     release version - if target is managed by git, checkout this
              branch/tag
  target      target for release - should be a path to a python package or the
              name of a repository type plugin
```

