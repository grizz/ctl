import os
import subprocess
import sys

import pytest

import ctl
from ctl.exceptions import UsageError

from util import instantiate_test_plugin

def instantiate(tmpdir, ctlr=None, **kwargs):
    vi = sys.version_info
    config = {
        "config" : {
            "pipfile": os.path.join(os.path.dirname(__file__), "data", "venv", "Pipfile"),
            "python_version" :"{}.{}".format(vi[0], vi[1])
        }
    }
    print(config)
    config["config"].update(**kwargs)
    plugin = instantiate_test_plugin("venv", "test_venv", _ctl=ctlr, **config)
    return plugin


def test_init():
    ctl.plugin.get_plugin_class('venv')


def test_build_and_exists(tmpdir, ctlr):
    path = os.path.join(str(tmpdir.mkdir("test_venv")), "venv")
    plugin = instantiate(tmpdir, ctlr)
    plugin.execute(op="build", output=path)
    assert plugin.venv_exists() == True
    assert plugin.venv_exists(path) == True
    assert plugin.venv_exists("does.not.exist") == False
    plugin.venv_validate()
    plugin.venv_validate(path)
    with pytest.raises(UsageError):
        plugin.venv_validate("does.not.exist")

def test_sync(tmpdir, ctlr):
    path = os.path.join(str(tmpdir.mkdir("test_venv")), "venv")
    plugin = instantiate(tmpdir, ctlr)
    plugin.execute(op="sync", output=path)

    output = subprocess.check_output(
        ["source {}/bin/activate; pip freeze;".format(path)], shell=True)

    assert u"{}".format(output).find(u"cfu==") > -1

def test_copy(tmpdir, ctlr):
    path_dir = str(tmpdir.mkdir("test_venv"))
    path = os.path.join(path_dir, "venv")
    path_copy = os.path.join(path_dir, "venv_copy")

    plugin = instantiate(tmpdir, ctlr)
    plugin.execute(op="build", output=path)
    plugin.execute(op="copy", source=path, output=path_copy)

    assert plugin.venv_exists(path_copy) == True
    plugin.venv_validate(path_copy)
