# Template Plugin

**extends**: [copy plugin](/plugins/copy)

Allows you walk sub directories inside a directory and render templates to an output directory

## Requirements

This plugin relies on the `jinja2` templating engine and 20c's `tmpl` module

```
pip install tmpl jinja2
```

## Example

`Ctl/config.yaml`

```yaml
{!examples/plugins/template/Ctl/config.yaml!}
```

`Ctl/tmplvars.yaml`

```yaml
{!examples/plugins/template/Ctl/tmplvars.yaml!}
```

## Run the command

The plugin will be exposed to the ctl cli as an operation using it's name

```sh
ctl template
```

```sh
[2019-10-10 06:46:54,396] [usage] ran command: `template`
[2019-10-10 06:46:54,396] [ctl.plugins.template] Skip dotfiles: True
[2019-10-10 06:46:54,400] [ctl.plugins.template] output/dir_1/template.txt
```

## Usage

!!! note "Plugin name"
    This usage documentation assumes that the plugin instance name
    is `template`

{pymdgen-cmd:ctl --home=docs template --help}
