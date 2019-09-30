# Template

Allows you walk sub directories inside a directory and template all files to an output directory

*Need to install to work*
```
tmpl jinja2
```

## Example

### config.yaml

```yaml
    - name: template
      type: template
      config:
        source: /home/dev/sandbox/ctl/tmpl/source
        output: /home/dev/sandbox/ctl/tmpl/output
        walk_dirs:
          - dir_1
        vars:
          - /home/dev/sandbox/ctl/Ctl/tmplvars.yaml
```

### tmplvars.yaml

```yaml
some:
  extra:
    data: 123
```

```sh
[2018-10-19 09:50:22,306] [ctl.plugins.template] Templating /home/dev/sandbox/ctl/tmpl/source/dir_1/file_a.tmpl to /home/dev/sandbox/ctl/tmpl/output/dir_1/file_a.tmpl
```
