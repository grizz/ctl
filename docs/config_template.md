# Config Template Rendering

If tmpl and jinja2 are installed, config will be rendered before it is loaded.

```
pip install tmpl jinja2
```

Currently the only env variable passed to the template engine is a reference to the ctl context.

```yaml
    - name: copy
      type: copy
      config:
        source: {{ ctx.home }}/copy/source
        output: {{ ctx.home }}/copy/output
        walk_dirs:
          - dir_1
```
