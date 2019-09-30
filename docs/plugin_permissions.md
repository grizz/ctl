# Plugin Operation Permissioning via expose

You can use the `expose` dectorator from `ctl.auth` to enable permission
checking on plugin operations

By default permission requirement is read from the plugin config and default to `r`

Any exposed function will have `exposed` property set to True


## Example Config: version plugin

```
    - name: version
      type: version
      config:
        # require `c` level permissions for all the tagging operations
        # in this instance of the version plugin
        permissions:
          tag: c
          bump: c
```

## Example Config: command plugin

```
    - name: ls
      type: command
      config:
        # here we require `c` level permission in order to execute the command
        # in this particular command type plugin instance
        permissions:
          execute: c
        command:
          - ls -all
```


## Static namespace

```
class ExamplePlugin(PluginBase):
  @expose("ctl.example.do_something")
  def do_something(self, something):
    ...
```

## Dynamic namespace via formatting

```
class ExamplePlugin(PluginBase):
  @expose("ctl.{plugin_name}.do_something")
  def do_something(self, something):
    ...
```

## Hardcode permission level requirement

Sometimes you may want to hardcode a permission requirement, or perhaps obtain
it dynamically, this can be done with the level argument

```
@expose("namespace", "r")
```

```
@expose("namespace", lambda plugin: "r")
```
