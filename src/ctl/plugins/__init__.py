"""
Base classes for ctl plugins
"""

from __future__ import absolute_import, division, print_function

import pluginmgr.config
import confu.schema
from confu.cli import argparse_options
import ctl

from ctl.log import Log
from ctl.events import common_events
from ctl.exceptions import ConfigError, UsageError, OperationNotExposed

__all__ = ["command", "config"]

class ConfuArgparseRouter(object):
    """
    An instance of this will be passed to plugin's `add_arguments`
    class method and can be used to route cli parameters
    generated by confu to sub-parsers

    This is useful in cases where you dont want to just attach
    all confu generated cli parameters to the main argparse parser
    which is the default behavior
    """

    def __init__(self, parser, schema, defaults):
        self.parser = parser
        self.schema = schema
        self.defaults = defaults
        self.routes = []

    def route(self, parser, *attributes):
        self.routes.append([parser, *attributes])
        argparse_options(parser, self.schema, defaults=self.defaults, attributes=attributes)



class PluginConfigSchema(confu.schema.Schema):
    """
    Configuration Schema for [PluginBase](#pluginbase)

    When creating new configuration schemas for extended plugins
    extend this.
    """

    name = confu.schema.Str("name", default="", help="Plugin name")
    type = confu.schema.Str("type", help="Plugin type")
    description = confu.schema.Str(
        "description", default="", blank=True, help="description of plugin"
    )

    # we also want to create an empty sub schema for `config` key
    # this should be overwritten in the classes extending this plugin
    config = confu.schema.Schema("config", help="plugin specific config")


class PluginBase(pluginmgr.config.PluginBase):

    """
    Base plugin class

    Extend other plugins from this class.

    !!! note "CLI Executable Plugins"
        If your intention is a cli executable plugin please have
        a look at the [ExecutablePlugin](#executableplugin) class.

    # Instanced Attributes

    - config (`dict`): plugin config
    - ctl (`Ctl`): ctl context
    - args (`list`): args passed during `__init__`
    - kwargs (`dict`): kwargs passed during `__init__`
    """

    ConfigSchema = PluginConfigSchema
    ConfigSchema.help = "Base plugin config schema"

    #    def init(self):
    #        pass

    def __init__(self, plugin_config, ctx, *args, **kwargs):

        """
        **Argument(s)**:

        - plugin_config (`dict`)
        - ctx: ctl context (`Ctl`)

        Any unknown arguments will be kept in `self.args`

        **Keyword Argument(s)**:

        Any keyword arguments will be kept in `self.kwargs`
        """

        self.ctl = ctx
        self.pluginmgr_config = plugin_config

        # TODO: this can be removed once confu can have proxy schemas
        # apply defaults
        schema = self.ConfigSchema()
        confu.schema.apply_defaults(schema, plugin_config)

        self.config = plugin_config.get("config", {})

        self.args = args
        self.kwargs = kwargs
        self.init()
        self.attach_events(self.pluginmgr_config.get("events", {}))

    @classmethod
    def option_list(cls):
        # deprecated?
        return []

    @classmethod
    def add_arguments(cls, parser, plugin_config, confu_router):
        """
        override this to add custom cli arguments to your plugin
        """
        pass

    @classmethod
    def confu_router_cls(cls):
        return ConfuArgparseRouter

    @property
    def log(self):
        """
        logger instance for the plugin
        """

        if not getattr(self, "_logger", None):
            self._logger = Log("ctl.plugins.{}".format(self.plugin_type))
        return self._logger

    @property
    def plugin_name(self):
        """
        name of the plugin instance
        """

        return self.pluginmgr_config.get("name")

    def attach_events(self, events):
        """
        attach plugin events
        """
        for event_name, event_config in events.items():
            self.attach_event(event_name, event_config)

    def attach_event(self, name, config):
        """
        Attaches the plugin instance to an event, allowing to
        execute an action on the plugin when the event triggers.

        **Argument(s)**

        - name(str): event name
        - config(dict): event config
        """

        for handler_name, instances in config.items():
            handler = getattr(self, handler_name, None)

            if not handler:
                raise ValueError(
                    "Tried to attach unknown plugin method `{}` to event `{}`".format(
                        handler_name, name
                    )
                )

            def callback(events, handler=handler, *args, **kwargs):
                if not instances:
                    handler()
                    return
                for params in instances:
                    handler(**params)

            common_events.on(name, callback)

    def init(self):
        """
        called after the plugin is initialized, plugin may define this for any
        other initialization code
        """
        pass

    def call(self, *args, **kwargs):
        print("command call ")

    def other_plugin(self, name):
        """
        return plugin instance by name
        convenience function as plugins often reference other
        plugins
        """

        if name == "self":
            return self

        other = ctl.plugin._instance.get(name)
        if not other:
            raise KeyError("Plugin instance with name `{}` does not exist".format(name))
        return other

    def render_tmpl(self, content, env=None):
        tmpl = self.ctl.ctx.tmpl

        if not tmpl.get("engine"):
            return content

        if env:
            _env = {"kwargs": env}
            _env.update(tmpl["env"])
            env = _env
        else:
            env = tmpl["env"]
        return tmpl["engine"]._render_str_to_str(content, env)

    def get_op(self, op):
        if not op:
            # TODO UsageError
            raise ValueError("operation not defined")
        elif not callable(getattr(self, op, None)):
            # TODO Usage Error
            raise ValueError("invalid operation")

        fn = getattr(self, op)

        if not getattr(fn, "exposed", False):
            raise OperationNotExposed(op)

        return fn


class ExecutablePlugin(PluginBase):

    """
    Base plugin class for CLI executable plugins
    """

    def prepare(self, **kwargs):
        """
        prepare plugin for execution

        override this to set instance properties
        and prepare for execution
        """
        pass

    def execute(self, **kwargs):
        """
        Execute the plugin's main action

        Will automatically call `prepare`

        **Keyword Arguments**

        Any keyword arguments passed to this function will
        be stored in the plugin's `kwargs` attribute
        """

        self.kwargs = kwargs
        self.prepare()

    def get_config(self, name):
        """
        Retrieve configuration properties from cli parameters
        and plugin config.

        For a property that exist as both a cli argument and
        a config property the cli argument takes priority, but
        it's default value will be informed by the configuration
        property - so you get to have your cake, and eat it too.

        Argument(s):

        - name(str): config key

        Returns:

        - config / cli parameter property

        """

        return self.kwargs.get(name, self.config.get(name))


# TODO PluginStageBase
