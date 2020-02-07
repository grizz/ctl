import os
import json
import pytest
import ctl
from util import instantiate_test_plugin


def instantiate(tmpdir, ctlr=None, **kwargs):
    config = {
        "config": {
            "source": os.path.join(os.path.dirname(__file__), "data"),
            "output": str(tmpdir.mkdir("template_out")),
            "debug": True,
            "vars": [os.path.join(os.path.dirname(__file__), "data", "tmplvars.json")],
            "walk_dirs": ["template"],
        }
    }
    config["config"].update(**kwargs)
    plugin = instantiate_test_plugin("template", "test_template", _ctl=ctlr, **config)
    return plugin


def test_init():
    ctl.plugin.get_plugin_class("template")


def test_process(tmpdir, ctlr):
    plugin = instantiate(tmpdir, ctlr)
    plugin.execute()

    assert len(plugin.debug_info["rendered"]) == 2
    for processed in plugin.debug_info["rendered"]:
        with open(processed, "r") as fh:
            assert fh.read() == "some content first variable\n"


def test_expose_vars(tmpdir, ctlr):
    plugin = instantiate(tmpdir, ctlr)

    env = {}
    plugin.expose_vars(env, plugin.config)
    assert env == {"var1": "first variable"}


def test_invalid_vars(tmpdir, ctlr):
    plugin = instantiate(tmpdir, ctlr, vars=["does.not.exist.json"])
    env = {}
    errors = plugin.expose_vars(env, plugin.config)
    assert "does.not.exist.json" in errors
