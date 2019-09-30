# Copy

allows you to walk directories in a source dir and copy files to an output dir

## Example config

```yaml
    - name: copy
      type: copy
      config:
        source: /home/dev/sandbox/ctl/copy/source
        # output dir will be created if it does not exist
        output: /home/dev/sandbox/ctl/copy/output
        walk_dirs:
          # copy everthing in {source}/dir_1
          - dir_1

        # if you dont want to copy metadata (default=true)
        #copy_metadata: false
```

## Ignore files based on pattern

You can use the `ignore` config to ignore certain file types or paths

```yaml
    - name: copy
      type: copy
      config:
        source: /home/dev/sandbox/ctl/copy/source
        output: /home/dev/sandbox/ctl/copy/output
        ignore:
          - \.cfg$
```

## Call command plugin on files based on pattern

You can use the `process` config to call another plugin on files, in this example we do
javascript obfuscation

```yaml

    # the command plugin that does the obfuscating
    - name: minify
      type: command
      config:
        arguments:
          # `source` and `output` will be individual file paths passed on
          # from the `copy` plugin, so we need to make sure the
          # command knows about them
          - name: source
            type: str
          - name: output
            type: str
        command:
          -  "java -jar ~/.local/google/compiler.jar --js {{ kwargs.source }} --js_output_file {{ kwargs.output }}"

    - name: copy
      type: copy
      config:
        source: /home/dev/sandbox/ctl/copy/source
        output: /home/dev/sandbox/ctl/copy/output
        process:
            # do this for any js file
          - pattern: \.js$
            # plugin name
            plugin: minify
            # plugin method
            action: execute
```


