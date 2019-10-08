# Venv Plugin

Manages a python virtualenv 

## Requirements

We currently use `pipenv` to maintain the virtualenv, although support for other solutions like `poetry` are being discussed.

```
pip install pipenv
```

## Example

In the following example we want to set up a virtualenv for python3.6. For the sake of simplicity it will only install the latest version of the `requests` module into it.

`Ctl/config.yaml`

```yaml
{!examples/plugins/venv/Ctl/config.yaml!}
```

By default it will be looking for a pipenv `Pipfile` in your ctl home

`Ctl/Pipfile`

```ini
{!examples/plugins/venv/Ctl/Pipfile!}
```

## Run the command

The command will be exposed as an operation to the ctl cli by it's name and also provide three sub operations: `build`, `sync` and `copy`

### Build / Sync

`build` is used to initially build the virtualenv
`sync` will build the virtualenv if it does not exist and otherwise update that it with the latest requirements

```sh
ctl venv36 sync output/venv36
```

### Copy

Copies an existing virtualenv to a new location

```sh
ctl venv36 copy output/venv36 output/venv36_copy
```

## Usage

```sh
usage: ctl venv36 [-h] [--pipfile PIPFILE] [--python-version PYTHON_VERSION]
                  {build,sync,copy} ...

optional arguments:
  -h, --help            show this help message and exit
  --pipfile PIPFILE     path to Pipfile ({{ctx.home}}/Pipfile)
  --python-version PYTHON_VERSION
                        (3.6)

Operation:
  {build,sync,copy}
    build               build virtualenv
    sync                sync virtualenv using pipenv, will build venv first if
                        it does not exist
    copy                copy virtualenv
```

### Build

```sh
usage: ctl venv36 build [-h] [output]

positional arguments:
  output      venv location

optional arguments:
  -h, --help  show this help message and exit
```

### Sync

```sh
usage: ctl venv36 sync [-h] [output]

positional arguments:
  output      venv location

optional arguments:
  -h, --help  show this help message and exit
```

### Copy

```sh
usage: ctl venv36 copy [-h] [source] [output]

positional arguments:
  source      venv source location
  output      venv output location

optional arguments:
  -h, --help  show this help message and exit
```
