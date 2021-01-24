import os

import ctl


def test_ctr_config_reset(config_dir):
    ctlr0 = ctl.Ctl(config_dir=os.path.join(config_dir, "standard"))
    git0 = ctlr0.get_plugin("ls")
    git0.config["command"] = "changed"

    ctlr1 = ctl.Ctl(config_dir=os.path.join(config_dir, "standard"))
    git1 = ctlr1.get_plugin("ls")
    assert git0.config != git1.config


def test_plugin_config_default():
    pass
