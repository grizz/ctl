# Chain

Allows you to call other plugins in a chain

### Example

```yaml
    # copy plugin, that will be used in the copy stage
    - name: copy
      type: copy
      config:
        source: /home/dev/sandbox/ctl/copy/source
        output: /home/dev/sandbox/ctl/copy/output
        walk_dirs:
          - dir_1

    # template plugin that will be used in the template stage
    - name: template
      type: template
      config:
        source: /home/dev/sandbox/ctl/tmpl/source
        output: /home/dev/sandbox/ctl/tmpl/output
        walk_dirs:
          - dir_1
        vars:
          - ./Ctl/tmplvars.yaml

    # chain plugin
    - name: facs
      type: chain
      config:
        chain:
          - stage: copy
            plugin: copy
          - stage: template
            plugin: template
```

### Help

```sh
ctl facs --help
```

```sh
usage: ctl facs [-h] [--end END] [--start START]

optional arguments:
  -h, --help     show this help message and exit
  --end END      stop at this stage
  --start START  start at this stage
```

### Execute

```sh
ctl facs
```

### Customize arguments

In some cases you may want to add custom input arguments to a chain
You can do so by using the `arguments` config.

```yaml
    - name: facs
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

```sh
positional arguments:
  tag            deploy this tag (e.g. 1.0.0)

optional arguments:
  -h, --help     show this help message and exit
  --end END      stop at this stage
  --start START  start at this stage
```

### Customize stages

By default stages call the targeted plugins `execute` function, however
in cases where you want to pass arguments or call an entirely different
function you can do so.

```yaml
    - name: facs
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

