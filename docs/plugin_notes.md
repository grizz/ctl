
### Plugins

#### Configuration

```yaml
ctl:
	plugins:
		name: runthis
		type: command
		description: optional description
```

Description is taken from, in order, `description` in config, class Docstring, or can be left blank.

#### Attributes


calls init()
calls `execute(**kwargs)` -- kwargs built from `add_arguments()`


#### Design notes

plugins get instantiated from a slice of a Config object, so they lose meta because `get_nested('ctl', 'plugins')` returns a dict (although by doing so, it should call the data property and set defaults, should look into that

defaults are only applied to the Config object if data is accessed, which is still very unintuitive, doesn't work if it's just a dict

if we just validate() each plugins config separately off it's config slice, we'll get warnings at each level for

##### confu

sticking with the argument that validate() should apply_defaults by default, switch if you somehow want it not to happen, but I still can't see a reason to try to validate a config without all of it's data

default=None is ignored -- maybe that's correct
