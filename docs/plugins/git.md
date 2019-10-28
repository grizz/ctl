# Git Plugin

Allows the management of a git repository

## Example:

```yaml
{!examples/plugins/git/Ctl/config.yaml!}
```

When you first run ctl after a new git plugin has been configured, it will automatically clone it to the ctl tmp directory `~/.ctl/tmp`. Depending on your ssh key you may be asked for a passphrase.

This plugin is mostly used in combination with other plugins and seldomly by itself. For a more complex example of other plugins making use of the git plugin check the [quickstart examples](/quickstart).

The plugin will expose three operations to the ctl cli:

1. `clone` (happens automatically on first init)
2. `pull` (pull remote)
3. `checkout` (checkout a tag or branch)

Operations like `commit` and `push` are also available but are not exposed to the ctl cli at this point. However other plugins may use them.


## Usage

!!! note "Plugin name"
    This usage documentation assumes that the plugin instance name
    is `git`

{pymdgen-cmd:ctl --home=docs git --help}
