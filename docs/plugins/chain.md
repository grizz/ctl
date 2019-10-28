# Chain Plugin

Chain plugin operations together in a stage driven approach.

### Example

In the following example we are setting up a chain with 2 stages.

The first stage will copy files and the second stage will render
some templates

For more information on the [template](/plugins/template) and [copy](/plugins/copy) plugins please refer to their documenation in the [plugins](/plugins) section.

`Ctl/config.yaml`

```yaml
{!examples/plugins/chain/Ctl/config.yaml!}
```

`Ctl/tmplvars.yaml`

```yaml
{!examples/plugins/chain/Ctl/tmplvars.yaml!}
```

### Execute the chain

The chain will be exposed as an operation to the ctl cli by it's name, so
you simply run it like that.

```sh
ctl test_chain
```

#### Specify starting stage

If you want to skip one ore more stages you can specify which stage
to start from by passing the `--start` argument

```sh
ctl test_chain --start template

[2019-10-09 07:41:20,882] [usage] ran command: `test_chain --start template`
[2019-10-09 07:41:20,882] [ctl.plugins.chain] skip copy
[2019-10-09 07:41:20,883] [ctl.plugins.chain] exec template [1/2]
[2019-10-09 07:41:20,883] [ctl.plugins.template] Skip dotfiles: True
[2019-10-09 07:41:20,886] [ctl.plugins.template] output/dir_2/template.txt
```

#### Specify ending stage

Likewise you can have the chain end early by setting the `--end`
argument

```sh
ctl test_chain --end copy

[2019-10-09 07:41:49,458] [usage] ran command: `test_chain --end copy`
[2019-10-09 07:41:49,458] [ctl.plugins.chain] exec copy [1/2]
[2019-10-09 07:41:49,458] [ctl.plugins.copy] Skip dotfiles: True
[2019-10-09 07:41:49,460] [ctl.plugins.copy] output/dir_1/file.txt
[2019-10-09 07:41:49,460] [ctl.plugins.chain] end copy
```

### Customize arguments

In some cases you may want to add custom input arguments to a chain
You can do so by using the `arguments` config.

```yaml
    - name: chain
      type: chain
      config:
        arguments:
          - name: tag
            help: deploy this tag (e.g. 1.0.0)
        chain:
          - stage: copy
            plugin: copy
          - stage: template
            plugin: template
```

Arguments are passed to argparse, so --help will now show

{pymdgen-cmd:ctl --home=docs chain --help}


### Customize stage actions

By default stages call the targeted plugins `execute` function, however
in cases where you want to pass arguments or call an entirely different
function you can do so.

```yaml
    - name: test_chain
      type: chain
      config:
        arguments:
          - name: tag
            help: deploy this tag (e.g. 1.0.0)
        chains:
          - stage: checkout
            plugin: git
            action:
              name: checkout
              args:
                # input arguments are rendered so we can
                # pass the tag through
                tag: "{{ input.plugin.tag }}"
```
